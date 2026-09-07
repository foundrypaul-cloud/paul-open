#!/usr/bin/env python3
"""Production entry point for the validated E4B DPO V2 corrective run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.dpo_v2_e4b_smoke import (
    assert_placement,
    assert_quantization,
    assert_trainability,
    external_reference_trainer_class,
    load_config,
    move_reference_inputs,
    validate_adapter,
    validate_dataset,
    validate_hardware,
    validate_hash,
    validate_versions,
)

ADAPTER_FILENAMES = ("adapter_config.json", "adapter_model.safetensors")
CHECKPOINT_PROVENANCE_FILENAME = "checkpoint_provenance.json"
SOURCE_REVISION_ENV = "PAUL_SOURCE_REVISION"

# This is the independently approved production contract. Runtime inputs are
# projected onto this single representation before any artifact validation.
LOCKED_EXPERIMENT = {
    "experiment": {
        "id": "paul_e4b_dpo_v2_corrective",
        "name": "PAUL Open E4B DPO V2 Corrective",
        "provenance": "RECONSTRUCTED CANDIDATE — REVALIDATED FROM REVIEWED EXPERIMENT DESIGN",
        "model_id": "google/gemma-4-E4B-it",
        "model_revision": "ee0ef6023621cff504d758262d4e04895a5af4a2",
        "dataset_path": "data/train/dpo_v2_corrective.jsonl",
        "dataset_sha256": "046f9c74aefc4491cb14c769d8c94c4bdedd83b223d23476b4ba30a535269a73",
        "dataset_records": 14,
        "adapter_source": "paulfoundry/paul-open-sft",
        "adapter": {
            "config_sha256": "cff65bd42928536886168b09d9b133b25ac444c01d901d2a56d98c7b8b03a0ce",
            "weights_sha256": "73bab121009e2130f387b5deebfe1d15f4f7ac2afbd622164b11b3024000ec49",
            "base_model_name_or_path": "google/gemma-4-E4B-it",
            "peft_type": "LORA",
            "task_type": "CAUSAL_LM",
            "r": 16,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "bias": "none",
            "modules_to_save": None,
            "target_module_suffixes": [
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj"
            ]
        },
        "tokenizer": {
            "tokenizer_json_sha256": "cc8d3a0ce36466ccc1278bf987df5f71db1719b9ca6b4118264f45cb627bfe0f",
            "chat_template_sha256": "0a2c8073c878ab1da004bee933a998606537bbb62016310352c7285c3f01c5b5",
            "expected_max_formatted_length": 349
        },
        "runtime": {
            "transformers_version": "5.15.0",
            "trl_version": "1.10.0",
            "peft_version": "0.20.0",
            "accelerate_version": "1.14.0",
            "bitsandbytes_version": "0.50.1",
            "policy_device": 0,
            "reference_device": 1,
            "required_gpu_count": 2,
            "required_gpu_name": "Tesla T4"
        }
    },
    "training": {
        "method": "dpo",
        "dpo_config": {
            "output_dir": "./results/dpo_v2_e4b_corrective",
            "num_train_epochs": 4,
            "per_device_train_batch_size": 1,
            "gradient_accumulation_steps": 8,
            "learning_rate": 5e-7,
            "beta": 0.1,
            "max_length": 4096,
            "bf16": False,
            "fp16": True,
            "gradient_checkpointing": True,
            "optim": "paged_adamw_8bit",
            "seed": 42,
            "report_to": "none",
            "logging_steps": 1,
            "save_strategy": "epoch",
            "save_total_limit": 1,
            "loss_type": "sigmoid",
            "precompute_ref_log_probs": False,
            "sync_ref_model": False
        }
    },
    "topology": {
        "policy_adapter": "dpo",
        "reference_adapter": "sft",
        "trainable_tensor_count": 516,
        "external_reference": True,
        "native_amp_owner": "Trainer/Accelerate"
    }
}


def resolve_adapter_directory(mount: Path) -> Path:
    """Resolve an adapter at the mount root or its sole qualifying direct child."""

    def is_adapter_directory(path: Path) -> bool:
        return path.is_dir() and all((path / name).is_file() for name in ADAPTER_FILENAMES)

    if is_adapter_directory(mount):
        return mount
    if not mount.is_dir():
        raise FileNotFoundError(f"Adapter mount directory not found: {mount}")
    candidates = sorted(path for path in mount.iterdir() if is_adapter_directory(path))
    if not candidates:
        raise FileNotFoundError(f"No adapter directory found directly under: {mount}")
    if len(candidates) != 1:
        raise RuntimeError(f"Ambiguous adapter directories under {mount}: {candidates}")
    return candidates[0]


def assert_experiment_lock(config: dict[str, Any]) -> None:
    """Fail rather than silently changing any validated methodology field."""
    locked_config = {key: LOCKED_EXPERIMENT[key] for key in ("experiment", "training")}
    if config != locked_config:
        raise RuntimeError("Configuration differs from the validated DPO V2 contract")


def source_revision() -> str:
    """Return a verified source SHA from Git, or the verified package injection."""
    injected = os.environ.get(SOURCE_REVISION_ENV)
    if injected is not None and re.fullmatch(r"[0-9a-f]{40}", injected) is None:
        raise RuntimeError(f"{SOURCE_REVISION_ENV} is not a full Git commit SHA")

    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        if injected is not None:
            return injected
        raise RuntimeError(
            f"Cannot establish source revision; provide verified {SOURCE_REVISION_ENV} "
            "for a Git-less package"
        ) from error

    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise RuntimeError("Repository source revision is not a full Git commit SHA")
    try:
        subprocess.run(["git", "diff", "--quiet", "HEAD", "--"], check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        raise RuntimeError("Repository working tree is not clean") from error
    if injected is not None and injected != revision:
        raise RuntimeError(f"{SOURCE_REVISION_ENV} does not match repository HEAD")
    return revision


def build_run_provenance(output_dir: Path, revision: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source_revision": revision,
        "output_lineage": str(output_dir.resolve()),
        "locked_experiment": LOCKED_EXPERIMENT,
    }


def validate_resume_checkpoint(checkpoint: Path, expected: dict[str, Any]) -> dict[str, Any]:
    """Require explicit, exact provenance before Trainer is allowed to resume."""
    provenance_path = checkpoint / CHECKPOINT_PROVENANCE_FILENAME
    if not checkpoint.is_dir() or not provenance_path.is_file():
        raise RuntimeError("Resume checkpoint is missing provenance")
    try:
        actual = json.loads(provenance_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("Resume checkpoint provenance is malformed") from error
    if not isinstance(actual, dict) or actual != expected:
        raise RuntimeError("Resume checkpoint provenance does not match this run")
    return actual


def checkpoint_provenance_callback_class(base: type, provenance: dict[str, Any]) -> type:
    class CheckpointProvenanceCallback(base):
        def on_save(self, args: Any, state: Any, control: Any, **kwargs: Any) -> Any:
            checkpoint = Path(args.output_dir) / f"checkpoint-{state.global_step}"
            checkpoint.mkdir(parents=True, exist_ok=True)
            destination = checkpoint / CHECKPOINT_PROVENANCE_FILENAME
            destination.write_text(
                json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            return control

    return CheckpointProvenanceCallback


def assert_adapter_topology(policy: Any, reference: Any, torch: Any) -> list[tuple[str, Any]]:
    assert_trainability(policy, reference)
    if set(policy.peft_config) != {"dpo"} or set(reference.peft_config) != {"sft"}:
        raise RuntimeError("Unexpected policy/reference adapter topology")
    trainable = [
        (name, parameter)
        for name, parameter in policy.named_parameters()
        if parameter.requires_grad
    ]
    if len(trainable) != 516:
        raise RuntimeError(f"Expected 516 trainable dpo LoRA tensors, found {len(trainable)}")
    if any(parameter.dtype != torch.float32 for _, parameter in trainable):
        raise RuntimeError("Trainable dpo LoRA tensors must remain FP32")
    policy_parameters = list(policy.parameters())
    reference_parameters = list(reference.parameters())
    if {id(parameter) for parameter in policy_parameters} & {
        id(parameter) for parameter in reference_parameters
    }:
        raise RuntimeError("Policy/reference parameter identities overlap")
    policy_storage = {parameter.untyped_storage().data_ptr() for parameter in policy_parameters}
    reference_storage = {
        parameter.untyped_storage().data_ptr() for parameter in reference_parameters
    }
    if policy_storage & reference_storage:
        raise RuntimeError("Policy/reference parameter storage overlaps")
    return trainable


def assert_optimizer_membership(trainer: Any, trainable: list[tuple[str, Any]]) -> None:
    """Require every optimizer member, and only those members, to be a dpo LoRA tensor."""
    intended = {id(parameter): name for name, parameter in trainable}
    actual = [
        parameter for group in trainer.optimizer.param_groups for parameter in group["params"]
    ]
    if len(actual) != len(intended) or {id(parameter) for parameter in actual} != set(intended):
        raise RuntimeError("Optimizer membership differs from intended dpo LoRA parameters")


def trainable_digest(trainable: list[tuple[str, Any]]) -> str:
    """Hash trainable values so a skipped-only run cannot be published as trained."""
    digest = hashlib.sha256()
    for name, parameter in trainable:
        digest.update(name.encode("utf-8"))
        digest.update(parameter.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def trainable_value_digests(trainable: list[tuple[str, Any]]) -> dict[str, str]:
    return {
        name: hashlib.sha256(parameter.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
        for name, parameter in trainable
    }


def validate_final_trainables(
    trainable: list[tuple[str, Any]], initial: dict[str, str], torch: Any
) -> dict[str, Any]:
    """Prove exact topology, finite final values, and an authentic value change."""
    names = [name for name, _ in trainable]
    if len(names) != LOCKED_EXPERIMENT["topology"]["trainable_tensor_count"]:
        raise RuntimeError("Final intended trainable tensor count mismatch")
    if len(names) != len(set(names)) or set(names) != set(initial):
        raise RuntimeError("Final intended trainable tensor set mismatch")
    if any(not torch.isfinite(parameter.detach()).all().item() for _, parameter in trainable):
        raise RuntimeError("Non-finite final dpo LoRA value; refusing final adapter")
    final = trainable_value_digests(trainable)
    changed = sum(final[name] != initial[name] for name in names)
    if changed == 0:
        raise RuntimeError("No trainable parameter changed; refusing final adapter")
    return {"finite": True, "intended_tensor_count": len(names), "changed_tensor_count": changed}


def native_amp_evidence(trainer: Any) -> dict[str, Any]:
    scaler = getattr(trainer.accelerator, "scaler", None)
    final_scale = scaler.get_scale() if scaler is not None and hasattr(scaler, "get_scale") else None
    return {
        "owner": LOCKED_EXPERIMENT["topology"]["native_amp_owner"],
        "fp16_enabled": True,
        "final_scale": float(final_scale) if final_scale is not None else None,
    }


def direct_reference_log_probs(
    reference: Any,
    inputs: dict[str, Any],
    reference_device: Any,
    loss_device: Any,
    torch: Any,
    selective_log_softmax: Any,
    ld_alpha: float | None,
) -> tuple[Any, Any]:
    """Independent direct implementation for the post-training reference equivalence gate."""
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


def validate_post_training_reference_gate(
    trainer: Any,
    policy: Any,
    reference: Any,
    torch: Any,
    selective_log_softmax: Any,
) -> dict[str, Any]:
    """Run the real post-training GPU0/GPU1 probe and independent math comparison."""
    assert_placement(policy, 0, "policy post-training reference gate")
    assert_placement(reference, 1, "reference post-training reference gate")
    if trainer.ref_model is not reference:
        raise RuntimeError("Trainer replaced the external reference before final validation")
    if reference.training or any(parameter.requires_grad for parameter in reference.parameters()):
        raise RuntimeError("Reference is not frozen/eval during final validation")

    try:
        batch = next(iter(trainer.get_train_dataloader()))
    except StopIteration as error:
        raise RuntimeError("Cannot run final reference gate on an empty dataloader") from error

    policy_device = torch.device("cuda:0")
    reference_device = torch.device("cuda:1")
    policy_inputs = move_reference_inputs(batch, policy_device, torch)
    policy_inputs["use_cache"] = False
    with torch.no_grad():
        policy_output = policy(**policy_inputs)
    if not torch.isfinite(policy_output.logits).all().item():
        raise RuntimeError("Non-finite policy logits in final cross-device probe")

    custom_chosen, custom_rejected = trainer.compute_ref_log_probs(reference, batch)
    direct_chosen, direct_rejected = direct_reference_log_probs(
        reference,
        batch,
        reference_device,
        custom_chosen.device,
        torch,
        selective_log_softmax,
        trainer.ld_alpha,
    )

    for label, custom, direct in (
        ("chosen", custom_chosen, direct_chosen),
        ("rejected", custom_rejected, direct_rejected),
    ):
        if not torch.isfinite(custom).all().item() or not torch.isfinite(direct).all().item():
            raise RuntimeError(f"Non-finite {label} reference log-probability in final gate")
        torch.testing.assert_close(custom, direct, rtol=1e-6, atol=1e-6)

    differences = [
        (custom_chosen - direct_chosen).abs(),
        (custom_rejected - direct_rejected).abs(),
    ]
    max_abs = max(float(value.max().item()) for value in differences)
    relative = []
    for custom, direct in (
        (custom_chosen, direct_chosen),
        (custom_rejected, direct_rejected),
    ):
        floor = torch.full_like(direct, 1e-12)
        denominator = torch.maximum(direct.abs(), floor)
        relative.append(((custom - direct).abs() / denominator).max())
    max_rel = max(float(value.item()) for value in relative)
    return {
        "status": "PASS",
        "rtol": 1e-6,
        "atol": 1e-6,
        "max_absolute_difference": max_abs,
        "max_relative_difference": max_rel,
        "policy_device": 0,
        "reference_device": 1,
        "reference_frozen_eval": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train PAUL Open E4B DPO V2 Corrective")
    parser.add_argument("--config", default="configs/training/dpo_v2_e4b_corrective.yaml")
    parser.add_argument(
        "--adapter", required=True, help="Downloaded historical SFT adapter directory"
    )
    parser.add_argument("--output-dir", help="Override checkpoint output directory")
    parser.add_argument(
        "--resume-from-checkpoint", help="A checkpoint in the same output directory"
    )
    parser.add_argument(
        "--preflight-only", action="store_true", help="Construct and audit; do not train"
    )
    args = parser.parse_args()

    config = load_config(Path(args.config))
    assert_experiment_lock(config)
    experiment = config["experiment"]
    dpo = config["training"]["dpo_config"]
    records = validate_dataset(Path(experiment["dataset_path"]), config)
    adapter_directory = resolve_adapter_directory(Path(args.adapter))
    validate_adapter(adapter_directory, config)
    print(f"LOGICAL_ADAPTER_DATASET={experiment['adapter_source']}")
    print(f"RESOLVED_ADAPTER_PATH={adapter_directory}")
    print("ADAPTER_CONFIG_EXISTS=true")
    print("ADAPTER_WEIGHTS_EXIST=true")
    versions = validate_versions(config)

    import torch
    from datasets import Dataset
    from huggingface_hub import hf_hub_download
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainerCallback
    from trl import DPOConfig, DPOTrainer
    from trl.trainer.utils import selective_log_softmax

    validate_hardware(torch, config)
    revision = experiment["model_revision"]
    for filename, key in (
        ("tokenizer.json", "tokenizer_json_sha256"),
        ("chat_template.jinja", "chat_template_sha256"),
    ):
        downloaded = Path(hf_hub_download(experiment["model_id"], filename, revision=revision))
        validate_hash(downloaded, experiment["tokenizer"][key], filename)

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
        reference, adapter_directory, adapter_name="sft", is_trainable=False
    )
    for parameter in reference.parameters():
        parameter.requires_grad = False
    reference.eval()

    copied_adapter = Path(tempfile.gettempdir()) / f"paul_e4b_dpo_{uuid.uuid4().hex[:8]}"
    shutil.copytree(adapter_directory, copied_adapter)
    try:
        policy = PeftModel.from_pretrained(
            policy, copied_adapter, adapter_name="dpo", is_trainable=True
        )
        assert_placement(policy, 0, "policy")
        assert_placement(reference, 1, "reference")
        assert_quantization(policy, torch, "policy")
        assert_quantization(reference, torch, "reference")
        trainable = assert_adapter_topology(policy, reference, torch)

        output_dir = args.output_dir or dpo["output_dir"]
        output_path = Path(output_dir)
        provenance = build_run_provenance(output_path, source_revision())
        resumed_from = None
        if args.resume_from_checkpoint:
            resumed_from = validate_resume_checkpoint(Path(args.resume_from_checkpoint), provenance)
        training_args = DPOConfig(
            output_dir=output_dir,
            beta=dpo["beta"],
            loss_type=dpo["loss_type"],
            max_length=dpo["max_length"],
            per_device_train_batch_size=dpo["per_device_train_batch_size"],
            gradient_accumulation_steps=dpo["gradient_accumulation_steps"],
            learning_rate=dpo["learning_rate"],
            num_train_epochs=dpo["num_train_epochs"],
            fp16=dpo["fp16"],
            bf16=dpo["bf16"],
            gradient_checkpointing=dpo["gradient_checkpointing"],
            optim=dpo["optim"],
            seed=dpo["seed"],
            report_to=dpo["report_to"],
            save_strategy=dpo["save_strategy"],
            save_total_limit=dpo["save_total_limit"],
            logging_steps=dpo["logging_steps"],
            precompute_ref_log_probs=dpo["precompute_ref_log_probs"],
            sync_ref_model=dpo["sync_ref_model"],
        )
        dataset = Dataset.from_list(records)
        trainer_type = external_reference_trainer_class(
            DPOTrainer, reference, torch.device("cuda:1"), torch, selective_log_softmax
        )
        trainer = trainer_type(
            model=policy,
            ref_model=reference,
            args=training_args,
            train_dataset=dataset,
            processing_class=tokenizer,
            callbacks=[checkpoint_provenance_callback_class(TrainerCallback, provenance)()],
        )
        assert_placement(policy, 0, "policy after trainer")
        assert_placement(reference, 1, "reference after trainer")
        trainable = assert_adapter_topology(policy, reference, torch)
        trainer.create_optimizer()
        assert_optimizer_membership(trainer, trainable)
        pre_train_digest = trainable_digest(trainable)
        initial_value_digests = trainable_value_digests(trainable)

        if args.preflight_only:
            print("DPO V2 PRODUCTION PREFLIGHT: PASS")
            return

        result = trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
        assert_placement(policy, 0, "policy after training")
        assert_placement(reference, 1, "reference after training")
        trainable = assert_adapter_topology(policy, reference, torch)
        post_train_digest = trainable_digest(trainable)
        if post_train_digest == pre_train_digest:
            raise RuntimeError(
                "No trainable parameter changed; refusing to emit a final trained adapter"
            )
        completion = validate_final_trainables(trainable, initial_value_digests, torch)
        reference_gate = validate_post_training_reference_gate(
            trainer, policy, reference, torch, selective_log_softmax
        )

        final_dir = Path(output_dir) / "final-dpo-adapter"
        trainer.save_model(str(final_dir))
        manifest = {
            "experiment_id": experiment["id"],
            "source_revision": provenance["source_revision"],
            "run_provenance": provenance,
            "model_id": experiment["model_id"],
            "model_revision": revision,
            "dataset_path": experiment["dataset_path"],
            "dataset_sha256": experiment["dataset_sha256"],
            "dataset_records": experiment["dataset_records"],
            "historical_adapter": experiment["adapter_source"],
            "adapter_config_sha256": experiment["adapter"]["config_sha256"],
            "adapter_weights_sha256": experiment["adapter"]["weights_sha256"],
            "versions": versions,
            "locked_methodology": LOCKED_EXPERIMENT["training"],
            "gpu_topology": LOCKED_EXPERIMENT["experiment"]["runtime"],
            "adapter_topology": LOCKED_EXPERIMENT["topology"],
            "configured_epochs": dpo["num_train_epochs"],
            "trainer_global_step": trainer.state.global_step,
            "pre_trainable_digest": pre_train_digest,
            "post_trainable_digest": post_train_digest,
            "authentic_update_evidence": {
                "basis": "intended_trainable_value_change",
                **completion,
            },
            "native_amp": native_amp_evidence(trainer),
            "post_training_invariants": {
                "adapter_topology": "PASS",
                "placement": "PASS",
                "reference_frozen_eval": "PASS",
                "policy_reference_storage_independent": "PASS",
                "optimizer_membership": "PASS",
                "external_reference_math": reference_gate,
            },
            "checkpoint_provenance": resumed_from,
            "completion_gate": "PASS",
            "train_metrics": result.metrics,
            "final_adapter": str(final_dir),
        }
        (Path(output_dir) / "training_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    finally:
        shutil.rmtree(copied_adapter, ignore_errors=True)


if __name__ == "__main__":
    main()
