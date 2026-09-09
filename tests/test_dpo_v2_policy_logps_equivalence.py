from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts import dpo_v2_e4b_train as production
from scripts.dpo_v2_e4b_train import (
    chunked_selected_logps,
    memory_efficient_policy_loss,
    sigmoid_dpo_losses,
)

torch = pytest.importorskip("torch")
from trl.trainer.utils import selective_log_softmax  # noqa: E402


def baseline_selected(hidden, labels, head, softcap):
    logits = head(hidden)
    if softcap is not None:
        logits = torch.tanh(logits / softcap) * softcap
    return selective_log_softmax(logits, labels)


@pytest.mark.parametrize(
    "batch,sequence,padding", [(2, 7, 0), (4, 11, 3), (6, 2, 1), (2, 514, 128)]
)
@pytest.mark.parametrize("softcap", [None, 30.0])
def test_policy_logps_forward_mask_shift_padding_and_eos_equivalence(
    batch, sequence, padding, softcap
) -> None:
    torch.manual_seed(42)
    hidden = torch.randn(batch, sequence, 9)
    head = torch.nn.Linear(9, 37, bias=False)
    input_ids = torch.randint(0, 37, (batch, sequence + 1))
    input_ids[:, -1] = 1  # deterministic EOS label
    completion_mask = torch.ones(batch, sequence + 1, dtype=torch.long)
    completion_mask[:, :2] = 0  # prompt mask
    if padding:
        completion_mask[1::2, -padding:] = 0
    labels = input_ids[:, 1:]
    mask = completion_mask[:, 1:]

    baseline_tokens = baseline_selected(hidden, labels, head, softcap).masked_fill(mask == 0, 0)
    optimized_tokens = chunked_selected_logps(
        hidden,
        labels,
        head,
        softcap,
        torch,
        selective_log_softmax,
        chunk_tokens=min(sequence, 64),
    ).masked_fill(mask == 0, 0)
    torch.testing.assert_close(optimized_tokens, baseline_tokens, rtol=1e-6, atol=1e-6)
    baseline_chosen, baseline_rejected = baseline_tokens.sum(1).chunk(2)
    chosen, rejected = optimized_tokens.sum(1).chunk(2)
    torch.testing.assert_close(chosen, baseline_chosen, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(rejected, baseline_rejected, rtol=1e-6, atol=1e-6)


def test_zero_length_completion_matches_pinned_zero_sum_semantics() -> None:
    hidden = torch.randn(2, 3, 4)
    labels = torch.zeros(2, 3, dtype=torch.long)
    mask = torch.zeros(2, 3, dtype=torch.long)
    head = torch.nn.Linear(4, 5, bias=False)
    actual = chunked_selected_logps(
        hidden, labels, head, None, torch, selective_log_softmax, chunk_tokens=2
    ).masked_fill(mask == 0, 0)
    assert torch.equal(actual.sum(1), torch.zeros(2))


def test_sigmoid_dpo_loss_logits_rewards_and_aggregate_equivalence() -> None:
    policy_chosen = torch.tensor([-3.0, -7.0], requires_grad=True)
    policy_rejected = torch.tensor([-4.0, -6.5], requires_grad=True)
    ref_chosen = torch.tensor([-3.5, -7.2])
    ref_rejected = torch.tensor([-3.8, -6.8])
    losses, chosen_rewards, rejected_rewards = sigmoid_dpo_losses(
        policy_chosen, policy_rejected, ref_chosen, ref_rejected, 0.1, torch
    )
    expected_chosen = 0.1 * (policy_chosen - ref_chosen)
    expected_rejected = 0.1 * (policy_rejected - ref_rejected)
    expected = -torch.nn.functional.logsigmoid(expected_chosen - expected_rejected)
    torch.testing.assert_close(chosen_rewards, expected_chosen, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(rejected_rewards, expected_rejected, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(losses, expected, rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(losses.mean(), expected.mean(), rtol=1e-6, atol=1e-6)


def _gradient_run(optimized: bool):
    torch.manual_seed(7)
    inputs = torch.randn(2, 6, 8, requires_grad=True)
    lora_a = torch.nn.Parameter(torch.randn(8, 3) * 0.1)
    lora_b = torch.nn.Parameter(torch.randn(3, 8) * 0.1)
    head = torch.nn.Linear(8, 29, bias=False)
    labels = torch.randint(0, 29, (2, 6))
    hidden = inputs + inputs @ lora_a @ lora_b
    selected = (
        chunked_selected_logps(
            hidden, labels, head, 12.0, torch, selective_log_softmax, chunk_tokens=2
        )
        if optimized
        else baseline_selected(hidden, labels, head, 12.0)
    )
    loss = selected.sum()
    loss.backward()
    return loss.detach(), [inputs.grad, head.weight.grad, lora_a.grad, lora_b.grad]


def test_gradient_equivalence_hidden_lm_head_and_lora_categories() -> None:
    baseline_loss, baseline_gradients = _gradient_run(False)
    optimized_loss, optimized_gradients = _gradient_run(True)
    torch.testing.assert_close(optimized_loss, baseline_loss, rtol=1e-6, atol=1e-6)
    for optimized, baseline in zip(optimized_gradients, baseline_gradients, strict=True):
        assert optimized.shape == baseline.shape
        assert torch.isfinite(optimized).all() and torch.isfinite(baseline).all()
        torch.testing.assert_close(optimized, baseline, rtol=1e-6, atol=1e-6)
        assert torch.nn.functional.cosine_similarity(
            optimized.flatten(), baseline.flatten(), dim=0
        ).item() > 0.999999


def test_gemma_softcap_extreme_values_and_gradients() -> None:
    logits = torch.tensor(
        [[[-300.0, -30.0, -0.01, 0.0, 0.01, 30.0, 300.0]]], requires_grad=True
    )
    optimized_logits = logits.detach().clone().requires_grad_(True)
    labels = torch.tensor([6])
    cap = 30.0
    head = torch.nn.Identity()
    baseline = selective_log_softmax(torch.tanh(logits / cap) * cap, labels.reshape(1, 1))
    optimized = chunked_selected_logps(
        optimized_logits,
        labels.reshape(1, 1),
        head,
        cap,
        torch,
        selective_log_softmax,
        chunk_tokens=1,
    )
    torch.testing.assert_close(optimized, baseline, rtol=1e-6, atol=1e-6)
    baseline.sum().backward(retain_graph=True)
    baseline_gradient = logits.grad.clone()
    optimized.sum().backward()
    torch.testing.assert_close(optimized_logits.grad, baseline_gradient, rtol=1e-6, atol=1e-6)


def test_cpu_fp16_autocast_forward_and_gradient_equivalence() -> None:
    torch.manual_seed(11)
    baseline_hidden = torch.randn(2, 5, 8, requires_grad=True)
    optimized_hidden = baseline_hidden.detach().clone().requires_grad_(True)
    baseline_head = torch.nn.Linear(8, 31, bias=False)
    optimized_head = torch.nn.Linear(8, 31, bias=False)
    optimized_head.load_state_dict(baseline_head.state_dict())
    labels = torch.randint(0, 31, (2, 5))
    with torch.autocast("cpu", dtype=torch.float16):
        baseline = baseline_selected(baseline_hidden, labels, baseline_head, 20.0).sum()
        optimized = chunked_selected_logps(
            optimized_hidden,
            labels,
            optimized_head,
            20.0,
            torch,
            selective_log_softmax,
            chunk_tokens=2,
        ).sum()
    baseline.backward()
    optimized.backward()
    torch.testing.assert_close(optimized, baseline, rtol=1e-3, atol=1e-3)
    torch.testing.assert_close(optimized_hidden.grad, baseline_hidden.grad, rtol=2e-3, atol=2e-3)
    torch.testing.assert_close(
        optimized_head.weight.grad, baseline_head.weight.grad, rtol=2e-3, atol=2e-3
    )


def test_checkpointed_chunks_do_not_save_full_vocabulary_tensor() -> None:
    torch.manual_seed(3)
    hidden = torch.randn(2, 12, 8, requires_grad=True)
    labels = torch.randint(0, 257, (2, 12))
    head = torch.nn.Linear(8, 257, bias=False)

    def maximum_saved_numel(call):
        saved = []

        def pack(tensor):
            saved.append(tensor.numel())
            return tensor

        with torch.autograd.graph.saved_tensors_hooks(pack, lambda tensor: tensor):
            call().sum().backward()
        return max(saved)

    baseline_max = maximum_saved_numel(lambda: baseline_selected(hidden, labels, head, 30.0))
    hidden.grad = None
    head.weight.grad = None
    optimized_max = maximum_saved_numel(
        lambda: chunked_selected_logps(
            hidden, labels, head, 30.0, torch, selective_log_softmax, chunk_tokens=3
        )
    )
    assert baseline_max >= 2 * 12 * 257
    assert optimized_max < 2 * 12 * 257


def test_production_integration_is_policy_only_and_lock_preserving() -> None:
    production = Path("scripts/dpo_v2_e4b_train.py").read_text(encoding="utf-8")
    reference = Path("scripts/dpo_v2_e4b_smoke.py").read_text(encoding="utf-8")
    assert "policy_loss=memory_efficient_policy_loss" in production
    assert 'model_inputs["use_cache"] = False' in reference
    assert "with torch.no_grad():" in reference
    assert "reference(**model_inputs)" in reference
    assert "POLICY_LOGIT_CHUNK_TOKENS = 16" in production


def test_integrated_policy_loss_matches_baseline_and_lora_gradients(monkeypatch) -> None:
    class Backbone(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lora_A = torch.nn.Parameter(torch.randn(7, 3) * 0.1)
            self.lora_B = torch.nn.Parameter(torch.randn(3, 7) * 0.1)

        def forward(self, input_ids, attention_mask, use_cache, **kwargs):
            hidden = torch.nn.functional.one_hot(input_ids, 7).float()
            hidden = hidden + hidden @ self.lora_A @ self.lora_B
            return SimpleNamespace(last_hidden_state=hidden)

    class Causal(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.model = Backbone()
            self.lm_head = torch.nn.Linear(7, 17, bias=False)
            self.config = SimpleNamespace(final_logit_softcapping=8.0)

        def get_output_embeddings(self):
            return self.lm_head

    class Policy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.causal = Causal()
            self.base_model = SimpleNamespace(model=self.causal)

    torch.manual_seed(19)
    baseline_policy = Policy()
    optimized_policy = Policy()
    optimized_policy.load_state_dict(baseline_policy.state_dict())
    input_ids = torch.randint(0, 7, (4, 6))
    completion_mask = torch.tensor(
        [[0, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0], [0, 1, 1, 0, 0, 0]]
    )
    inputs = {
        "input_ids": input_ids,
        "attention_mask": torch.ones_like(input_ids),
        "completion_mask": completion_mask,
        "ref_chosen_logps": torch.tensor([-5.0, -4.0]),
        "ref_rejected_logps": torch.tensor([-5.5, -4.2]),
    }
    baseline_output = baseline_policy.causal.model(
        input_ids=input_ids, attention_mask=inputs["attention_mask"], use_cache=False
    )
    baseline_tokens = baseline_selected(
        baseline_output.last_hidden_state[:, :-1],
        input_ids[:, 1:],
        baseline_policy.causal.lm_head,
        8.0,
    ).masked_fill(completion_mask[:, 1:] == 0, 0)
    baseline_chosen, baseline_rejected = baseline_tokens.sum(1).chunk(2)
    baseline_losses, _, _ = sigmoid_dpo_losses(
        baseline_chosen,
        baseline_rejected,
        inputs["ref_chosen_logps"],
        inputs["ref_rejected_logps"],
        0.1,
        torch,
    )
    baseline_loss = baseline_losses.mean()
    baseline_loss.backward()

    class Accelerator:
        @staticmethod
        def gather(value):
            return value

        @staticmethod
        def gather_for_metrics(value):
            return value

    trainer = SimpleNamespace(
        loss_types=["sigmoid"],
        loss_weights=[1.0],
        f_divergence_type="reverse_kl",
        ld_alpha=None,
        use_weighting=False,
        aux_loss_enabled=False,
        beta=0.1,
        model=optimized_policy,
        accelerator=Accelerator(),
        _total_train_tokens=0,
        _metrics={"train": defaultdict(list), "eval": defaultdict(list)},
        _paul_record_memory=lambda label: None,
        _paul_selective_log_softmax=selective_log_softmax,
    )
    optimized_policy.train()
    monkeypatch.setattr(production, "assert_placement", lambda *args: None)
    optimized_loss = memory_efficient_policy_loss(trainer, optimized_policy, inputs, False)
    optimized_loss.backward()
    torch.testing.assert_close(optimized_loss, baseline_loss, rtol=1e-6, atol=1e-6)
    for baseline, optimized in zip(
        baseline_policy.parameters(), optimized_policy.parameters(), strict=True
    ):
        torch.testing.assert_close(optimized.grad, baseline.grad, rtol=1e-6, atol=1e-6)
