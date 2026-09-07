#!/usr/bin/env python3
"""Production entry point for the validated E4B DPO V2 corrective run."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
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
    validate_adapter,
    validate_dataset,
    validate_hardware,
    validate_hash,
    validate_versions,
)

ADAPTER_FILENAMES = ("adapter_config.json", "adapter_model.safetensors")


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
    experiment = config["experiment"]
    dpo = config["training"]["dpo_config"]
    expected = {
        "model_id": "google/gemma-4-E4B-it",
        "model_revision": "ee0ef6023621cff504d758262d4e04895a5af4a2",
        "dataset_path": "data/train/dpo_v2_corrective.jsonl",
        "dataset_records": 14,
        "adapter_source": "paulfoundry/paul-open-sft",
    }
    if any(experiment.get(key) != value for key, value in expected.items()):
        raise RuntimeError("Experiment identity differs from the validated DPO V2 contract")
    expected_dpo = {
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
        "loss_type": "sigmoid",
        "precompute_ref_log_probs": False,
        "sync_ref_model": False,
    }
    if any(dpo.get(key) != value for key, value in expected_dpo.items()):
        raise RuntimeError("Training methodology differs from the validated DPO V2 contract")


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
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
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
        )
        assert_placement(policy, 0, "policy after trainer")
        assert_placement(reference, 1, "reference after trainer")
        trainable = assert_adapter_topology(policy, reference, torch)
        trainer.create_optimizer()
        assert_optimizer_membership(trainer, trainable)
        pre_train_digest = trainable_digest(trainable)

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
        final_dir = Path(output_dir) / "final-dpo-adapter"
        trainer.save_model(str(final_dir))
        manifest = {
            "experiment_id": experiment["id"],
            "model_revision": revision,
            "dataset_sha256": experiment["dataset_sha256"],
            "adapter_config_sha256": experiment["adapter"]["config_sha256"],
            "adapter_weights_sha256": experiment["adapter"]["weights_sha256"],
            "versions": versions,
            "trainer_global_step": trainer.state.global_step,
            "pre_trainable_digest": pre_train_digest,
            "post_trainable_digest": post_train_digest,
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
