import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

HAS_TORCH = importlib.util.find_spec("torch") is not None

from scripts import dpo_v2_e4b_train as production


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
