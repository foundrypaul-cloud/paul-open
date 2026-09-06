#!/usr/bin/env python3
"""Zero-step validation for PAUL Open E4B DPO V2 Corrective."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import shutil
import tempfile
import uuid
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import yaml

NON_MODEL_KEYS = {"completion_mask", "ref_chosen_logps", "ref_rejected_logps"}


def sha256_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_hash(path: Path, expected: str, label: str) -> None:
    if sha256_file(path) != expected:
        raise RuntimeError(f"{label} SHA-256 mismatch")


def validate_dataset(path: Path, config: Mapping[str, Any]) -> list[dict[str, Any]]:
    experiment = config["experiment"]
    validate_hash(path, experiment["dataset_sha256"], "corrective dataset")
    records = [json.loads(line) for line in path.read_text().splitlines() if line]
    if len(records) != experiment["dataset_records"]:
        raise ValueError("Corrective dataset record-count mismatch")
    identifiers: set[str] = set()
    pairs: set[tuple[str, str, str]] = set()
    for record in records:
        if not all(
            isinstance(record.get(key), str) and record[key]
            for key in ("id", "prompt", "chosen", "rejected")
        ):
            raise ValueError("Invalid corrective record schema")
        if record["id"] in identifiers:
            raise ValueError("Duplicate corrective record ID")
        pair = (record["prompt"], record["chosen"], record["rejected"])
        if pair in pairs:
            raise ValueError("Duplicate corrective preference pair")
        if record["chosen"] == record["rejected"]:
            raise ValueError("Chosen and rejected responses are identical")
        identifiers.add(record["id"])
        pairs.add(pair)
    return records


def validate_adapter(directory: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    expected = config["experiment"]["adapter"]
    config_path = directory / "adapter_config.json"
    weights_path = directory / "adapter_model.safetensors"
    if not config_path.is_file() or not weights_path.is_file() or weights_path.stat().st_size == 0:
        raise ValueError("Adapter config and non-empty safetensors weights are required")
    validate_hash(config_path, expected["config_sha256"], "adapter config")
    validate_hash(weights_path, expected["weights_sha256"], "adapter weights")
    actual = json.loads(config_path.read_text())
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
    for field in fields:
        if actual.get(field) != expected[field]:
            raise ValueError(f"Adapter {field} mismatch")
    suffixes = {name.rsplit(".", 1)[-1] for name in actual.get("target_modules", [])}
    if suffixes != set(expected["target_module_suffixes"]):
        raise ValueError("Adapter target modules mismatch")
    return actual


def validate_versions(config: Mapping[str, Any]) -> dict[str, str]:
    expected = config["experiment"]["runtime"]
    versions = {
        name: importlib.metadata.version(name)
        for name in ("transformers", "trl", "peft", "accelerate")
    }
    for name, version in versions.items():
        if version != expected[f"{name}_version"]:
            raise RuntimeError(f"{name} version mismatch: {version}")
    return versions


def validate_hardware(torch: Any, config: Mapping[str, Any]) -> None:
    runtime = config["experiment"]["runtime"]
    if not torch.cuda.is_available() or torch.cuda.device_count() != 2:
        raise RuntimeError("Exactly two CUDA devices are required")
    if any(runtime["required_gpu_name"] not in torch.cuda.get_device_name(i) for i in range(2)):
        raise RuntimeError("Exactly two approved Tesla T4 GPUs are required")


def assert_placement(model: Any, index: int, label: str) -> None:
    devices = {parameter.device for parameter in model.parameters()}
    devices.update(buffer.device for buffer in model.buffers())
    if not devices or any(device.type != "cuda" or device.index != index for device in devices):
        raise RuntimeError(f"{label} placement mismatch: {devices}")
    mapped = set(getattr(model, "hf_device_map", {}).values())
    normalized = {int(str(value).split(":")[-1]) for value in mapped} if mapped else {index}
    if normalized != {index}:
        raise RuntimeError(f"{label} device map mismatch: {mapped}")


def assert_quantization(model: Any, torch: Any, label: str) -> None:
    base = model.get_base_model() if hasattr(model, "get_base_model") else model
    quant = getattr(base, "quantization_config", None) or getattr(
        base.config, "quantization_config", {}
    )
    values = quant.to_dict() if hasattr(quant, "to_dict") else dict(quant)
    if not getattr(base, "is_loaded_in_4bit", False):
        raise RuntimeError(f"{label} is not loaded in four bit")
    expected = {
        "load_in_4bit": True,
        "bnb_4bit_quant_type": "nf4",
        "bnb_4bit_use_double_quant": True,
    }
    if any(values.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"{label} NF4 configuration mismatch")
    if values.get("bnb_4bit_compute_dtype") not in ("float16", torch.float16):
        raise RuntimeError(f"{label} compute dtype mismatch")


def assert_trainability(policy: Any, reference: Any) -> None:
    trainable = [(name, value) for name, value in policy.named_parameters() if value.requires_grad]
    if not trainable or any("lora_" not in name or ".dpo." not in name for name, _ in trainable):
        raise RuntimeError("Only dpo LoRA parameters may be trainable")
    if any(16 not in value.shape for _, value in trainable):
        raise RuntimeError("Trainable policy LoRA rank is not 16")
    if reference.training or any(value.requires_grad for value in reference.parameters()):
        raise RuntimeError("Reference is not frozen in evaluation mode")
    if {id(value) for value in policy.parameters()} & {
        id(value) for value in reference.parameters()
    }:
        raise RuntimeError("Policy and reference share parameter objects")


def move_reference_inputs(inputs: Mapping[str, Any], device: Any, torch: Any) -> dict[str, Any]:
    """Copy model-forward fields without mutating the policy batch."""
    return {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in inputs.items()
        if key not in NON_MODEL_KEYS
    }


def external_reference_log_probs(
    reference: Any,
    inputs: Mapping[str, Any],
    reference_device: Any,
    loss_device: Any,
    torch: Any,
    selective_log_softmax: Callable[[Any, Any], Any],
    ld_alpha: float | None = None,
) -> tuple[Any, Any]:
    """Route only reference inputs/results while preserving TRL log-probability math."""
    model_inputs = move_reference_inputs(inputs, reference_device, torch)
    model_inputs["use_cache"] = False
    with torch.no_grad():
        output = reference(**model_inputs)
        labels = model_inputs["input_ids"][..., 1:]
        mask = inputs["completion_mask"].to(reference_device)[..., 1:]
        token_logps = selective_log_softmax(output.logits[..., :-1, :], labels)
        token_logps = token_logps.masked_fill(mask == 0, 0.0)
        if ld_alpha is None:
            logps = token_logps.sum(dim=1)
        else:
            positions = mask.cumsum(dim=1)
            lengths = mask.sum(dim=1).long()
            chosen_lengths, rejected_lengths = lengths.chunk(2, dim=0)
            shared = torch.minimum(chosen_lengths, rejected_lengths)
            shared = torch.cat((shared, shared), dim=0)
            shared_mask = (positions > 0) & (positions <= shared.unsqueeze(1))
            tail_mask = positions > shared.unsqueeze(1)
            logps = (token_logps * shared_mask).sum(dim=1) + ld_alpha * (
                token_logps * tail_mask
            ).sum(dim=1)
        chosen, rejected = logps.chunk(2, dim=0)
        return chosen.to(loss_device), rejected.to(loss_device)


def external_reference_trainer_class(
    trainer_base: type,
    reference: Any,
    reference_device: Any,
    torch: Any,
    selective_log_softmax: Callable[[Any, Any], Any],
) -> type:
    """Keep the independent reference outside incompatible Accelerate preparation."""

    class ExternalReferenceDPOTrainer(trainer_base):  # type: ignore[misc, valid-type]
        def __init__(self, *args: Any, ref_model: Any = None, **kwargs: Any) -> None:
            if ref_model is not reference:
                raise RuntimeError("Trainer did not receive the approved reference")
            if reference.training or any(value.requires_grad for value in reference.parameters()):
                raise RuntimeError("Reference must be frozen before trainer construction")
            # TRL 1.10 only prepares an explicit non-None reference. A PEFT policy
            # on this branch leaves self.ref_model None and creates no replacement.
            super().__init__(*args, ref_model=None, **kwargs)
            if self.ref_model is not None:
                raise RuntimeError("TRL unexpectedly created an implicit reference")
            self.ref_model = reference
            self._external_reference = reference

        def compute_ref_log_probs(self, model: Any, inputs: Mapping[str, Any]) -> tuple[Any, Any]:
            if model is not self._external_reference:
                raise RuntimeError("Unexpected reference model")
            return external_reference_log_probs(
                model,
                inputs,
                reference_device,
                self.accelerator.device,
                torch,
                selective_log_softmax,
                self.ld_alpha,
            )

        def _compute_loss(self, model: Any, inputs: Mapping[str, Any], return_outputs: bool) -> Any:
            chosen, rejected = self.compute_ref_log_probs(self._external_reference, inputs)
            augmented = dict(inputs)
            augmented["ref_chosen_logps"] = chosen
            augmented["ref_rejected_logps"] = rejected
            previous = self.precompute_ref_logps
            self.precompute_ref_logps = True
            try:
                return super()._compute_loss(model, augmented, return_outputs)
            finally:
                self.precompute_ref_logps = previous

    return ExternalReferenceDPOTrainer


def main() -> None:
    parser = argparse.ArgumentParser(description="PAUL E4B DPO V2 zero-step validation")
    parser.add_argument("--config", default="configs/training/dpo_v2_e4b_corrective.yaml")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--manifest", default="results/dpo_v2_e4b_corrective/smoke.json")
    args = parser.parse_args()
    config = load_config(Path(args.config))
    experiment = config["experiment"]
    dpo = config["training"]["dpo_config"]
    if experiment["model_id"] != "google/gemma-4-E4B-it":
        raise RuntimeError("Smoke entry point is locked to E4B")
    if dpo["precompute_ref_log_probs"] or dpo["sync_ref_model"]:
        raise RuntimeError("Reference precompute/sync is forbidden")
    records = validate_dataset(Path(experiment["dataset_path"]), config)
    adapter_metadata = validate_adapter(Path(args.adapter), config)
    versions = validate_versions(config)

    import torch
    from datasets import Dataset
    from huggingface_hub import hf_hub_download
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import DPOConfig, DPOTrainer
    from trl.trainer.utils import selective_log_softmax

    validate_hardware(torch, config)
    revision = experiment["model_revision"]
    for filename, key in (
        ("tokenizer.json", "tokenizer_json_sha256"),
        ("chat_template.jinja", "chat_template_sha256"),
    ):
        path = Path(hf_hub_download(experiment["model_id"], filename, revision=revision))
        validate_hash(path, experiment["tokenizer"][key], filename)
    tokenizer = AutoTokenizer.from_pretrained(experiment["model_id"], revision=revision)
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    policy = AutoModelForCausalLM.from_pretrained(
        experiment["model_id"],
        revision=revision,
        device_map={"": 0},
        quantization_config=quantization,
    )
    reference = AutoModelForCausalLM.from_pretrained(
        experiment["model_id"],
        revision=revision,
        device_map={"": 1},
        quantization_config=quantization,
    )
    reference = PeftModel.from_pretrained(
        reference, args.adapter, adapter_name="sft", is_trainable=False
    )
    for parameter in reference.parameters():
        parameter.requires_grad = False
    reference.eval()
    copied_adapter = Path(tempfile.gettempdir()) / f"paul_e4b_{uuid.uuid4().hex[:8]}"
    shutil.copytree(args.adapter, copied_adapter)
    try:
        validate_hash(
            copied_adapter / "adapter_config.json",
            experiment["adapter"]["config_sha256"],
            "copied config",
        )
        validate_hash(
            copied_adapter / "adapter_model.safetensors",
            experiment["adapter"]["weights_sha256"],
            "copied weights",
        )
        policy = PeftModel.from_pretrained(
            policy, copied_adapter, adapter_name="dpo", is_trainable=True
        )
        for label, model, index in (("policy", policy, 0), ("reference", reference, 1)):
            assert_placement(model, index, label)
            assert_quantization(model, torch, label)
        assert_trainability(policy, reference)
        training_args = DPOConfig(
            output_dir=dpo["output_dir"],
            beta=dpo["beta"],
            loss_type=dpo["loss_type"],
            max_length=dpo["max_length"],
            per_device_train_batch_size=dpo["per_device_train_batch_size"],
            gradient_accumulation_steps=dpo["gradient_accumulation_steps"],
            learning_rate=dpo["learning_rate"],
            num_train_epochs=dpo["num_train_epochs"],
            fp16=True,
            bf16=False,
            gradient_checkpointing=True,
            optim=dpo["optim"],
            seed=dpo["seed"],
            report_to="none",
            precompute_ref_log_probs=False,
            sync_ref_model=False,
        )
        dataset = Dataset.from_list(
            [{key: item[key] for key in ("prompt", "chosen", "rejected")} for item in records]
        )
        trainer_type = external_reference_trainer_class(
            DPOTrainer, reference, torch.device("cuda:1"), torch, selective_log_softmax
        )
        trainer = trainer_type(
            model=policy,
            ref_model=reference,
            args=training_args,
            train_dataset=dataset,
            processing_class=tokenizer,
        )
        if trainer.ref_model is not reference:
            raise RuntimeError("Trainer replaced the external reference")
        assert_placement(policy, 0, "policy after trainer")
        assert_placement(reference, 1, "reference after trainer")
        assert_trainability(policy, reference)
        if trainer.state.global_step != 0 or trainer.optimizer is not None:
            raise RuntimeError("Zero-step invariant failed")
        manifest = {
            "provenance": experiment["provenance"],
            "experiment_id": experiment["id"],
            "status": "ZERO_STEP_DRY_RUN_SUCCESS",
            "model_id": experiment["model_id"],
            "model_revision": revision,
            "adapter_revision": adapter_metadata.get("revision"),
            "adapter_config_sha256": experiment["adapter"]["config_sha256"],
            "adapter_weights_sha256": experiment["adapter"]["weights_sha256"],
            "dataset_sha256": experiment["dataset_sha256"],
            "dataset_records": len(records),
            "versions": versions,
            "policy_device": 0,
            "reference_device": 1,
            "reference_accelerate_prepared": False,
            "global_step": 0,
            "train_called": False,
        }
        destination = Path(args.manifest)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(manifest, indent=2) + "\n")
        print("ZERO-STEP DRY RUN SUCCESS")
    finally:
        shutil.rmtree(copied_adapter, ignore_errors=True)


if __name__ == "__main__":
    main()
