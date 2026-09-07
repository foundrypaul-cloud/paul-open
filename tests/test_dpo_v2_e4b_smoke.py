import ast
import copy
import hashlib
import importlib.util
import json
import math
from array import array
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
from scripts.dpo_v2_e4b_train import (
    LOCKED_EXPERIMENT,
    assert_experiment_lock,
    assert_optimizer_membership,
    build_run_provenance,
    checkpoint_provenance_callback_class,
    resolve_adapter_directory,
    trainable_digest,
    trainable_value_digests,
    validate_final_trainables,
    validate_resume_checkpoint,
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
    ) == (4, 1, 8)
    assert (dpo["max_length"], dpo["optim"], dpo["seed"]) == (4096, "paged_adamw_8bit", 42)
    assert (dpo["fp16"], dpo["bf16"], dpo["gradient_checkpointing"]) == (
        True,
        False,
        True,
    )
    assert (dpo["save_strategy"], dpo["save_total_limit"], dpo["logging_steps"]) == (
        "epoch",
        1,
        1,
    )
    assert_experiment_lock(config)
    assert config["experiment"]["runtime"]["bitsandbytes_version"] == "0.50.1"


def locked_config() -> dict:
    return {key: copy.deepcopy(LOCKED_EXPERIMENT[key]) for key in ("experiment", "training")}


def leaf_paths(value, prefix=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaf_paths(child, prefix + (key,))
    elif isinstance(value, list):
        yield prefix
    else:
        yield prefix


@pytest.mark.parametrize("path", list(leaf_paths(locked_config())))
def test_every_locked_configuration_field_rejects_mutation(path) -> None:
    config = locked_config()
    target = config
    for key in path[:-1]:
        target = target[key]
    value = target[path[-1]]
    target[path[-1]] = list(reversed(value)) if isinstance(value, list) else object()
    with pytest.raises(RuntimeError, match="validated DPO V2 contract"):
        assert_experiment_lock(config)


def test_experiment_lock_rejects_missing_and_extra_fields() -> None:
    missing = locked_config()
    del missing["experiment"]["dataset_sha256"]
    with pytest.raises(RuntimeError, match="validated DPO V2 contract"):
        assert_experiment_lock(missing)
    extra = locked_config()
    extra["training"]["dpo_config"]["max_steps"] = 8
    with pytest.raises(RuntimeError, match="validated DPO V2 contract"):
        assert_experiment_lock(extra)


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


def write_adapter_files(directory: Path, *, config: bool = True, weights: bool = True) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    if config:
        (directory / "adapter_config.json").write_text("{}")
    if weights:
        (directory / "adapter_model.safetensors").write_bytes(b"weights")


def test_resolve_adapter_directory_at_mount_root(tmp_path: Path) -> None:
    write_adapter_files(tmp_path)
    assert resolve_adapter_directory(tmp_path) == tmp_path


def test_resolve_single_nested_adapter_directory(tmp_path: Path) -> None:
    adapter = tmp_path / "paul_gemma4_e4b_25d8e53a"
    write_adapter_files(adapter)
    assert resolve_adapter_directory(tmp_path) == adapter


@pytest.mark.parametrize("config,weights", [(False, False), (False, True), (True, False)])
def test_resolve_adapter_directory_rejects_missing_files(
    tmp_path: Path, config: bool, weights: bool
) -> None:
    write_adapter_files(tmp_path / "incomplete", config=config, weights=weights)
    with pytest.raises(FileNotFoundError, match="No adapter directory"):
        resolve_adapter_directory(tmp_path)


def test_resolve_adapter_directory_rejects_ambiguity(tmp_path: Path) -> None:
    write_adapter_files(tmp_path / "adapter-a")
    write_adapter_files(tmp_path / "adapter-b")
    with pytest.raises(RuntimeError, match="Ambiguous adapter directories"):
        resolve_adapter_directory(tmp_path)


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


def test_optimizer_membership_is_exact_and_rejects_extras() -> None:
    intended = [("x.lora_A.dpo.weight", object()), ("x.lora_B.dpo.weight", object())]
    optimizer = SimpleNamespace(param_groups=[{"params": [value for _, value in intended]}])
    assert_optimizer_membership(SimpleNamespace(optimizer=optimizer), intended)

    unexpected = object()
    optimizer.param_groups[0]["params"].append(unexpected)
    with pytest.raises(RuntimeError, match="Optimizer membership"):
        assert_optimizer_membership(SimpleNamespace(optimizer=optimizer), intended)


@pytest.mark.skipif(not HAS_TORCH, reason="CPU PyTorch is unavailable")
def test_trainable_digest_detects_parameter_change() -> None:
    import torch

    parameter = torch.nn.Parameter(torch.tensor([1.0], dtype=torch.float32))
    before = trainable_digest([("x.lora_A.dpo.weight", parameter)])
    with torch.no_grad():
        parameter.add_(1.0)
    assert trainable_digest([("x.lora_A.dpo.weight", parameter)]) != before


def test_resume_provenance_accepts_exact_match(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint-8"
    checkpoint.mkdir()
    expected = build_run_provenance(tmp_path, "abc123")
    (checkpoint / "checkpoint_provenance.json").write_text(json.dumps(expected))
    assert validate_resume_checkpoint(checkpoint, expected) == expected


def test_checkpoint_callback_writes_machine_readable_provenance(tmp_path: Path) -> None:
    provenance = build_run_provenance(tmp_path, "abc123")
    callback = checkpoint_provenance_callback_class(object, provenance)()
    control = object()
    assert callback.on_save(
        SimpleNamespace(output_dir=str(tmp_path)), SimpleNamespace(global_step=8), control
    ) is control
    written = json.loads((tmp_path / "checkpoint-8/checkpoint_provenance.json").read_text())
    assert written == provenance


@pytest.mark.parametrize(
    "mutation",
    [
        ("source_revision",),
        ("output_lineage",),
        ("locked_experiment", "experiment", "id"),
        ("locked_experiment", "experiment", "model_revision"),
        ("locked_experiment", "experiment", "dataset_sha256"),
        ("locked_experiment", "experiment", "adapter", "weights_sha256"),
        ("locked_experiment", "experiment", "runtime", "trl_version"),
        ("locked_experiment", "training", "dpo_config", "beta"),
        ("locked_experiment", "topology", "policy_adapter"),
    ],
)
def test_resume_provenance_rejects_mismatch(tmp_path: Path, mutation) -> None:
    checkpoint = tmp_path / "checkpoint-8"
    checkpoint.mkdir()
    expected = build_run_provenance(tmp_path, "abc123")
    actual = copy.deepcopy(expected)
    target = actual
    for key in mutation[:-1]:
        target = target[key]
    target[mutation[-1]] = "foreign"
    (checkpoint / "checkpoint_provenance.json").write_text(json.dumps(actual))
    with pytest.raises(RuntimeError, match="does not match"):
        validate_resume_checkpoint(checkpoint, expected)


@pytest.mark.parametrize("contents", [None, "not-json", "[]"])
def test_resume_provenance_rejects_missing_or_malformed(tmp_path: Path, contents) -> None:
    checkpoint = tmp_path / "checkpoint-8"
    checkpoint.mkdir()
    if contents is not None:
        (checkpoint / "checkpoint_provenance.json").write_text(contents)
    with pytest.raises(RuntimeError, match="missing provenance|malformed|does not match"):
        validate_resume_checkpoint(checkpoint, build_run_provenance(tmp_path, "abc123"))


class NumpyParameter:
    def __init__(self, value) -> None:
        self.value = array("f", value)

    def detach(self):
        return self

    def cpu(self):
        return self

    def contiguous(self):
        return self

    def numpy(self):
        return self.value


class FiniteResult:
    def __init__(self, value) -> None:
        self.value = value

    def all(self):
        return self

    def item(self):
        return self.value


class NumpyTorch:
    @staticmethod
    def isfinite(parameter):
        return FiniteResult(all(math.isfinite(value) for value in parameter.value))


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_final_trainables_reject_nonfinite_values(bad_value) -> None:
    trainable = [
        (f"layer.{index}.lora_A.dpo.weight", NumpyParameter([1.0]))
        for index in range(516)
    ]
    initial = trainable_value_digests(trainable)
    trainable[0][1].value[0] = bad_value
    with pytest.raises(RuntimeError, match="Non-finite"):
        validate_final_trainables(trainable, initial, NumpyTorch)


def test_final_trainables_require_change_and_exact_set() -> None:
    trainable = [
        (f"layer.{index}.lora_A.dpo.weight", NumpyParameter([1.0]))
        for index in range(516)
    ]
    initial = trainable_value_digests(trainable)
    with pytest.raises(RuntimeError, match="No trainable parameter changed"):
        validate_final_trainables(trainable, initial, NumpyTorch)
    with pytest.raises(RuntimeError, match="count mismatch"):
        validate_final_trainables(trainable[:-1], initial, NumpyTorch)
    replacement = trainable[:-1] + [("unexpected.dpo.weight", trainable[-1][1])]
    with pytest.raises(RuntimeError, match="tensor set mismatch"):
        validate_final_trainables(replacement, initial, NumpyTorch)
    trainable[0][1].value[0] += 1.0
    evidence = validate_final_trainables(trainable, initial, NumpyTorch)
    assert evidence == {"finite": True, "intended_tensor_count": 516, "changed_tensor_count": 1}


def test_production_entry_uses_native_trainer_amp_and_safe_save_topology() -> None:
    source = Path("scripts/dpo_v2_e4b_train.py").read_text()
    tree = ast.parse(source)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    attributes = {node.func.attr for node in calls if isinstance(node.func, ast.Attribute)}
    assert attributes.isdisjoint({"backward", "step", "merge_adapter", "merge_and_unload"})
    assert "GradScaler" not in source
    assert "init_scale" not in source
    assert "trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)" in source
    assert 'set(policy.peft_config) != {"dpo"}' in source
    assert 'set(reference.peft_config) != {"sft"}' in source
