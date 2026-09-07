import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts import dpo_v2_e4b_train as production

HAS_TORCH = importlib.util.find_spec("torch") is not None


def test_allocator_contract_is_established_before_torch_import() -> None:
    source = Path("scripts/dpo_v2_e4b_train.py").read_text(encoding="utf-8")
    startup_call = "\nconfigure_cuda_allocator_environment()\n"
    assert source.index(startup_call) < source.index(
        "from scripts.dpo_v2_e4b_smoke import"
    )
    assert source.index(startup_call) < source.index("    import torch")
    env = os.environ.copy()
    env[production.CUDA_ALLOCATOR_ENV] = "backend:cudaMallocAsync"
    result = subprocess.run(
        [sys.executable, "-c", "import scripts.dpo_v2_e4b_train"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "must be exactly" in result.stderr


def test_cuda_memory_telemetry_is_read_only_and_per_device(capsys) -> None:
    class FakeCuda:
        def __init__(self):
            self.calls = []

        def device_count(self):
            return 2

        def mem_get_info(self, device):
            self.calls.append(("mem_get_info", device))
            return (1000 - device, 2000 + device)

        def memory_allocated(self, device):
            return 100 + device

        def memory_reserved(self, device):
            return 200 + device

        def max_memory_allocated(self, device):
            return 300 + device

        def max_memory_reserved(self, device):
            return 400 + device

    cuda = FakeCuda()
    snapshot = production.cuda_memory_telemetry(SimpleNamespace(cuda=cuda), "test")
    assert snapshot[0]["free_bytes"] == 1000
    assert snapshot[1]["total_bytes"] == 2001
    assert cuda.calls == [("mem_get_info", 0), ("mem_get_info", 1)]
    assert '"label": "test"' in capsys.readouterr().out


def test_checkpointing_and_forward_cache_assertions_fail_closed() -> None:
    inactive = SimpleNamespace(is_gradient_checkpointing=False, modules=lambda: [])
    with pytest.raises(RuntimeError, match="checkpointing is not active"):
        production.assert_gradient_checkpointing_active(inactive)
    with pytest.raises(RuntimeError, match="use_cache=False"):
        production.assert_forward_cache_disabled("policy", {"use_cache": True})
    with pytest.raises(RuntimeError, match="use_cache=False"):
        production.assert_forward_cache_disabled("reference", {})
    production.assert_forward_cache_disabled("policy", {"use_cache": False})


def test_optimizer_state_must_be_unmaterialized_before_first_backward() -> None:
    production.assert_optimizer_state_unmaterialized(
        SimpleNamespace(optimizer=SimpleNamespace(state={}))
    )
    with pytest.raises(RuntimeError, match="unexpectedly materialized"):
        production.assert_optimizer_state_unmaterialized(
            SimpleNamespace(optimizer=SimpleNamespace(state={"parameter": {"step": 0}}))
        )


def test_pretraining_cleanup_releases_only_temporary_resources(tmp_path) -> None:
    copied_adapter = tmp_path / "copied-adapter"
    copied_adapter.mkdir()
    required = SimpleNamespace(policy=object(), reference=object(), trainer=object())

    class FakeCuda:
        empty_cache_calls = 0

        def empty_cache(self):
            self.empty_cache_calls += 1

    cuda = FakeCuda()
    production.release_pretraining_temporaries(SimpleNamespace(cuda=cuda), copied_adapter)
    assert not copied_adapter.exists()
    assert cuda.empty_cache_calls == 1
    assert all(
        item is not None for item in (required.policy, required.reference, required.trainer)
    )


def test_cleanup_and_instrumentation_precede_authentic_training() -> None:
    source = Path("scripts/dpo_v2_e4b_train.py").read_text(encoding="utf-8")
    cleanup = "release_pretraining_temporaries(torch, copied_adapter)"
    install = "install_runtime_memory_instrumentation(\n            trainer"
    train = "trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)"
    assert source.index(cleanup) < source.index(install) < source.index(train)
    assert "trainer, policy, reference, torch, telemetry_state" in source


def test_source_revision_uses_verified_package_sha_without_git(monkeypatch) -> None:
    expected = "a" * 40
    monkeypatch.setenv(production.SOURCE_REVISION_ENV, expected)

    def no_git(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(production.subprocess, "run", no_git)
    assert production.source_revision() == expected


def test_source_revision_rejects_invalid_package_sha(monkeypatch) -> None:
    monkeypatch.setenv(production.SOURCE_REVISION_ENV, "not-a-sha")
    with pytest.raises(RuntimeError, match="not a full Git commit SHA"):
        production.source_revision()


def test_source_revision_requires_git_or_verified_package_sha(monkeypatch) -> None:
    monkeypatch.delenv(production.SOURCE_REVISION_ENV, raising=False)

    def no_git(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(production.subprocess, "run", no_git)
    with pytest.raises(RuntimeError, match="provide verified PAUL_SOURCE_REVISION"):
        production.source_revision()


def test_source_revision_rejects_injected_git_mismatch(monkeypatch) -> None:
    actual = "b" * 40
    injected = "c" * 40
    monkeypatch.setenv(production.SOURCE_REVISION_ENV, injected)
    calls = iter([SimpleNamespace(stdout=actual + "\n"), SimpleNamespace(stdout="")])

    def fake_run(*args, **kwargs):
        return next(calls)

    monkeypatch.setattr(production.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="does not match repository HEAD"):
        production.source_revision()


@pytest.mark.skipif(not HAS_TORCH, reason="CPU PyTorch unavailable")
def test_direct_reference_log_probs_matches_independent_expected_math() -> None:
    import torch

    def selective(logits, labels):
        return torch.gather(torch.log_softmax(logits, -1), -1, labels.unsqueeze(-1)).squeeze(-1)

    class Model(torch.nn.Module):
        def forward(self, input_ids, attention_mask=None, use_cache=False):
            logits = torch.nn.functional.one_hot((input_ids + 1) % 7, 7).float() * 3
            return SimpleNamespace(logits=logits)

    inputs = {
        "input_ids": torch.tensor(
            [[0, 1, 2, 3], [0, 2, 3, 4], [0, 4, 5, 6], [0, 5, 4, 3]]
        ),
        "attention_mask": torch.ones(4, 4, dtype=torch.long),
        "completion_mask": torch.tensor(
            [[0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0]]
        ),
    }
    model = Model()
    output = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
    token_logps = selective(output.logits[..., :-1, :], inputs["input_ids"][..., 1:])
    expected = token_logps.masked_fill(inputs["completion_mask"][..., 1:] == 0, 0).sum(1).chunk(2)

    actual = production.direct_reference_log_probs(
        model,
        inputs,
        torch.device("cpu"),
        torch.device("cpu"),
        torch,
        selective,
        None,
    )
    torch.testing.assert_close(actual[0], expected[0], rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(actual[1], expected[1], rtol=1e-6, atol=1e-6)


def test_final_reference_gate_is_mandatory_before_final_save() -> None:
    source = Path("scripts/dpo_v2_e4b_train.py").read_text(encoding="utf-8")
    gate = "reference_gate = validate_post_training_reference_gate("
    save = 'trainer.save_model(str(final_dir))'
    assert gate in source
    assert save in source
    assert source.index(gate) < source.index(save)
    assert '"external_reference_math": reference_gate' in source
    assert "validated_by_pinned_regression" not in source


def test_gitless_source_revision_contract_is_documented_in_code() -> None:
    source = Path("scripts/dpo_v2_e4b_train.py").read_text(encoding="utf-8")
    assert 'SOURCE_REVISION_ENV = "PAUL_SOURCE_REVISION"' in source
    assert "for a Git-less package" in source
