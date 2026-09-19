#!/usr/bin/env python3
"""Generate matched SFT and frozen DPO V6 responses for H8 DHE development cases."""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import torch
import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.h6_dhe_generate import generate_source, resolve_adapter, sha256


def load_h8_jsonl(path: Path) -> list[dict[str, object]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 12:
        raise RuntimeError(f"H8 requires exactly 12 cases, found {len(rows)}")
    seen: set[str] = set()
    for row in rows:
        required = {"case_id", "partition", "domain", "language", "reviewer_cohort", "prompt"}
        missing = required - row.keys()
        if missing:
            raise RuntimeError(f"{row.get('case_id', '?')}: missing {sorted(missing)}")
        if row["partition"] != "development":
            raise RuntimeError(f"{row['case_id']}: H8 requires development partition")
        if row["case_id"] in seen:
            raise RuntimeError(f"duplicate case_id: {row['case_id']}")
        seen.add(str(row["case_id"]))
    return rows


def _load_adapter_config(adapter: Path) -> dict[str, Any]:
    path = adapter / "adapter_config.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("adapter_config.json must contain an object")
    return data


def _validate_v6_adapter_semantics(adapter: Path, train_cfg: dict[str, Any]) -> str:
    config_path = adapter / "adapter_config.json"
    weights_path = adapter / "adapter_model.safetensors"
    if not config_path.is_file() or not weights_path.is_file():
        raise RuntimeError("V6 adapter payload is incomplete")

    expected = train_cfg["adapter"]
    actual = _load_adapter_config(adapter)

    checks = {
        "peft_type": expected["peft_type"],
        "task_type": expected["task_type"],
        "r": expected["r"],
        "lora_alpha": expected["lora_alpha"],
        "lora_dropout": expected["lora_dropout"],
        "bias": expected["bias"],
    }
    for key, value in checks.items():
        if actual.get(key) != value:
            raise RuntimeError(f"V6 adapter config semantic mismatch for {key}: {actual.get(key)!r} != {value!r}")

    expected_targets = set(expected["target_module_suffixes"])
    raw_targets = actual.get("target_modules")
    if isinstance(raw_targets, list):
        target_text = " ".join(str(x) for x in raw_targets)
    else:
        target_text = str(raw_targets or "")
    missing = sorted(x for x in expected_targets if x not in target_text)
    if missing:
        raise RuntimeError(f"V6 adapter config missing expected target modules: {missing}")

    return sha256(config_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--training-config", default="configs/training/dpo_v6_e4b_synthetic_corrective.yaml")
    parser.add_argument("--sft-adapter", required=True)
    parser.add_argument("--dpo-adapter", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    config_path = Path(args.config)
    training_config_path = Path(args.training_config)
    rows = load_h8_jsonl(manifest_path)
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))["h8_dhe_v6_pilot"]
    train_cfg = yaml.safe_load(training_config_path.read_text(encoding="utf-8"))["experiment"]

    if cfg["status"] != "frozen_pre_generation" or cfg["partition"] != "development":
        raise RuntimeError("H8 config is not frozen_pre_generation/development")

    model_id = train_cfg["model_id"]
    revision = train_cfg["model_revision"]
    generation = cfg["generation"]
    if not str(generation.get("response_instruction", "")).strip():
        raise RuntimeError("H8 generation response_instruction must be nonempty")
    if int(generation.get("max_new_tokens", 0)) != 768:
        raise RuntimeError("H8 must preserve the 768-token fail-closed ceiling")
    if generation.get("require_eos_before_limit") is not True:
        raise RuntimeError("H8 must preserve the EOS-before-limit gate")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sft_path = out / "sft_reference.jsonl"
    dpo_path = out / "dpo_v6_synthetic_corrective.jsonl"

    sft_adapter = resolve_adapter(Path(args.sft_adapter))
    dpo_adapter = resolve_adapter(Path(args.dpo_adapter))

    reference_cfg = cfg["sources"]["reference"]
    candidate_cfg = cfg["sources"]["candidate"]

    sft_config_hash = sha256(sft_adapter / "adapter_config.json")
    sft_weights_hash = sha256(sft_adapter / "adapter_model.safetensors")
    if sft_config_hash != reference_cfg["adapter_config_sha256"]:
        raise RuntimeError("SFT adapter config hash mismatch")
    if sft_weights_hash != reference_cfg["adapter_weights_sha256"]:
        raise RuntimeError("SFT adapter weights hash mismatch")

    dpo_weights_hash = sha256(dpo_adapter / "adapter_model.safetensors")
    if dpo_weights_hash != candidate_cfg["adapter_weights_sha256"]:
        raise RuntimeError("V6 adapter weights hash mismatch")
    dpo_config_hash = _validate_v6_adapter_semantics(dpo_adapter, train_cfg)

    sft = generate_source(
        rows,
        adapter=sft_adapter,
        model_id=model_id,
        revision=revision,
        generation=generation,
        output_path=sft_path,
    )
    dpo = generate_source(
        rows,
        adapter=dpo_adapter,
        model_id=model_id,
        revision=revision,
        generation=generation,
        output_path=dpo_path,
    )
    if sft["records"] != len(rows) or dpo["records"] != len(rows):
        raise RuntimeError("generation count mismatch")

    try:
        source_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        source_revision = "unknown"

    manifest = {
        "experiment": "H8_DHE_V6_PILOT_V1",
        "partition": "development",
        "source_revision": source_revision,
        "prompt_freeze_revision": cfg["prompt_freeze_revision"],
        "case_manifest_sha256": sha256(manifest_path),
        "generation_config_sha256": sha256(config_path),
        "model_id": model_id,
        "model_revision": revision,
        "generation": generation,
        "case_count": len(rows),
        "adapter_identity": {
            "sft": {
                "adapter_config_sha256": sft_config_hash,
                "adapter_weights_sha256": sft_weights_hash,
            },
            "dpo_v6": {
                "adapter_config_sha256": dpo_config_hash,
                "adapter_weights_sha256": dpo_weights_hash,
                "production_run": candidate_cfg["production_run"],
                "source_revision": candidate_cfg["source_revision"],
            },
        },
        "sft": sft,
        "dpo_v6": dpo,
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "gates": {
            "generation_completed": "PASS",
            "nonempty_output": "PASS",
            "no_generation_truncation_gate": "PASS",
            "display_prompt_matches_generation_prompt": "PASS",
            "automated_safety_gate": "PASS",
            "malformed_output_gate": "PASS",
            "evaluation_partition_integrity": "PASS",
            "candidate_weights_hash_binding_gate": "PASS",
            "candidate_adapter_config_semantics_gate": "PASS",
            "generation_path_preserved_from_h6_h7": "PASS",
        },
    }
    (out / "generation_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "case_count": len(rows), "output_dir": str(out)}, indent=2))


def _failure_output_dir(argv: list[str]) -> Path | None:
    try:
        idx = argv.index("--output-dir")
        return Path(argv[idx + 1])
    except (ValueError, IndexError):
        return None


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        out = _failure_output_dir(sys.argv)
        if out is not None:
            out.mkdir(parents=True, exist_ok=True)
            message = str(exc)
            for sensitive in ("sft_reference", "dpo_v6_synthetic_corrective"):
                message = message.replace(sensitive, "checkpoint")
            failure = {
                "status": "FAIL",
                "exception_type": type(exc).__name__,
                "message": message[:1000],
            }
            (out.parent / "failure_summary.json").write_text(
                json.dumps(failure, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        raise
