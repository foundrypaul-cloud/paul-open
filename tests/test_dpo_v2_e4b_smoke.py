import ast
import hashlib
import importlib.util
import json
from collections import namedtuple
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts.dpo_v2_e4b_smoke import (
    assert_placement,
    assert_quantization,
    assert_trainability,
    external_reference_log_probs,
    external_reference_trainer_class,
    load_config,
    move_reference_inputs,
    validate_adapter,
    validate_dataset,
)

CONFIG = Path("configs/training/dpo_v2_e4b_corrective.yaml")
HAS_TORCH = importlib.util.find_spec("torch") is not None


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_exact_experiment_configuration() -> None:
    config = load_config(CONFIG)
    exp, dpo = config["experiment"], config["training"]["dpo_config"]
    assert exp["model_id"] == "google/gemma-4-E4B-it"
    assert exp["model_revision"] == "ee0ef6023621cff504d758262d4e04895a5af4a2"
    assert (exp["dataset_records"], exp["adapter"]["r"], exp["adapter"]["lora_alpha"]) == (
        14,
        16,
        32,
    )
    assert exp["adapter"]["lora_dropout"] == 0.05
    assert exp["adapter"]["modules_to_save"] is None
    assert (dpo["loss_type"], dpo["beta"], dpo["learning_rate"]) == ("sigmoid", 0.1, 5e-7)
    assert (
        dpo["num_train_epochs"],
        dpo["per_device_train_batch_size"],
        dpo["gradient_accumulation_steps"],
    ) == (1, 1, 8)
    assert (dpo["max_length"], dpo["optim"], dpo["seed"]) == (4096, "paged_adamw_8bit", 42)


def fake_adapter(tmp_path: Path, config: dict, **changes) -> Path:
    expected = config["experiment"]["adapter"]
    fields = (
        "base_model_name_or_path",
        "peft_type",
        "task_type",
        "r",
        "lora_alpha",
        "lora_dropout",
        "bias",
        "modules_to_save",
    )
    actual = {key: expected[key] for key in fields}
    actual["target_modules"] = [f"layer.{name}" for name in expected["target_module_suffixes"]]
    actual.update(changes)
    config_path = tmp_path / "adapter_config.json"
    config_path.write_text(json.dumps(actual))
    weights_path = tmp_path / "adapter_model.safetensors"
    weights_path.write_bytes(b"test")
    expected["config_sha256"] = digest(config_path)
    expected["weights_sha256"] = digest(weights_path)
    return tmp_path


def test_adapter_contract_and_rank_mismatch(tmp_path: Path) -> None:
    config = load_config(CONFIG)
    assert validate_adapter(fake_adapter(tmp_path, config), config)["r"] == 16
    config = load_config(CONFIG)
    path = fake_adapter(tmp_path, config, r=32)
    config["experiment"]["adapter"]["r"] = 16
    with pytest.raises(ValueError, match="r mismatch"):
        validate_adapter(path, config)


def test_corrective_dataset_provenance_schema_and_uniqueness() -> None:
    config = load_config(CONFIG)
    records = validate_dataset(Path(config["experiment"]["dataset_path"]), config)
    assert len(records) == len({row["id"] for row in records}) == 14
    assert all(row["chosen"] != row["rejected"] for row in records)


Device = namedtuple("Device", "type index")


class FakeTensor:
    def __init__(self, index, trainable=False, shape=(16, 2)):
        self.device = Device("cuda", index)
        self.requires_grad = trainable
        self.shape = shape


class FakeModel:
    def __init__(self, index, named, training=False):
        self._named = named
        self.training = training
        self.hf_device_map = {"": index}

    def named_parameters(self):
        return iter(self._named)

    def parameters(self):
        return (value for _, value in self._named)

    def buffers(self):
        return iter(())


def test_topology_freezing_rank_and_independence() -> None:
    policy = FakeModel(0, [("x.lora_A.dpo.weight", FakeTensor(0, True))], True)
    reference = FakeModel(1, [("x.lora_A.sft.weight", FakeTensor(1))])
    assert_placement(policy, 0, "policy")
    assert_placement(reference, 1, "reference")
    assert_trainability(policy, reference)


class Movable:
    def __init__(self):
        self.moves = []

    def to(self, device):
        self.moves.append(device)
        return self


class FakeTorch:
    @staticmethod
    def is_tensor(value):
        return isinstance(value, Movable)


def test_cross_device_copy_does_not_mutate_policy_batch() -> None:
    tensor = Movable()
    batch = {"input_ids": tensor, "completion_mask": tensor, "note": "value"}
    copied = move_reference_inputs(batch, "cuda:1", FakeTorch)
    assert copied == {"input_ids": tensor, "note": "value"}
    assert tensor.moves == ["cuda:1"]
    assert set(batch) == {"input_ids", "completion_mask", "note"}


def test_trainer_avoids_accelerate_and_implicit_reference() -> None:
    reference = FakeModel(1, [("x.lora_A.sft.weight", FakeTensor(1))])

    class Base:
        def __init__(self, *args, ref_model=None, **kwargs):
            assert ref_model is None
            self.ref_model = None
            self.precompute_ref_logps = False
            self.ld_alpha = None
            self.accelerator = SimpleNamespace(device="cuda:0")

    trainer = external_reference_trainer_class(
        Base, reference, "cuda:1", FakeTorch, lambda *_: None
    )(ref_model=reference)
    assert trainer.ref_model is reference
    assert trainer._external_reference is reference


@pytest.mark.skipif(not HAS_TORCH, reason="CPU PyTorch is unavailable")
def test_reference_math_equivalent_shift_mask_and_order() -> None:
    import torch

    def selective(logits, labels):
        return torch.gather(torch.log_softmax(logits, -1), -1, labels.unsqueeze(-1)).squeeze(-1)

    class Model(torch.nn.Module):
        def forward(self, input_ids, attention_mask=None, use_cache=False):
            logits = torch.nn.functional.one_hot((input_ids + 1) % 7, 7).float() * 3
            return SimpleNamespace(logits=logits)

    inputs = {
        "input_ids": torch.tensor([[0, 1, 2, 3], [0, 2, 3, 4], [0, 4, 5, 6], [0, 5, 4, 3]]),
        "attention_mask": torch.ones(4, 4, dtype=torch.long),
        "completion_mask": torch.tensor([[0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0]]),
    }
    model = Model()
    output = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
    expected = selective(output.logits[..., :-1, :], inputs["input_ids"][..., 1:])
    expected = expected.masked_fill(inputs["completion_mask"][..., 1:] == 0, 0).sum(1).chunk(2)
    actual = external_reference_log_probs(
        model, inputs, torch.device("cpu"), torch.device("cpu"), torch, selective
    )
    torch.testing.assert_close(actual[0], expected[0], rtol=1e-6, atol=1e-6)
    torch.testing.assert_close(actual[1], expected[1], rtol=1e-6, atol=1e-6)


def test_nf4_double_quantization_fp16_contract() -> None:
    model = SimpleNamespace(
        is_loaded_in_4bit=True,
        config=SimpleNamespace(
            quantization_config={
                "load_in_4bit": True,
                "bnb_4bit_quant_type": "nf4",
                "bnb_4bit_use_double_quant": True,
                "bnb_4bit_compute_dtype": "float16",
            }
        ),
    )
    assert_quantization(model, SimpleNamespace(float16="float16"), "model")


def test_absolute_zero_step_source_safety() -> None:
    source = Path("scripts/dpo_v2_e4b_smoke.py").read_text()
    assert "PinnedReferenceAccelerator" not in source
    assert "device_placement=False" not in source
    forbidden = {
        "train",
        "step",
        "backward",
        "save_pretrained",
        "merge_and_unload",
        "merge_adapter",
    }
    calls = {
        node.func.attr
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert not calls & forbidden
