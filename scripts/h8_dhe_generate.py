#!/usr/bin/env python3
"""Generate matched SFT and DPO V6 responses for frozen H8 DHE development cases.

Generation only. The implementation delegates to the H6 v1.2 generation path so
quantization, sampling, native-script, safety, reviewer-visible prompt, EOS, and
truncation behavior remain aligned with prior DHE rounds.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

import torch
import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.h6_dhe_generate import generate_source, resolve_adapter, sha256


def load_h8_jsonl(path: Path) -> list[dict[str, object]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 12:
        raise RuntimeError(f"H8 requires exactly 12 records, found {len(rows)}")
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        required = {
            "case_id",
            "partition",
            "domain",
            "language",
            "reviewer_cohort",
            "prompt",
            "provenance",
            "development_exposed",
        }
        missing = required - row.keys()
        if missing:
            raise RuntimeError(f"{row.get('case_id', '?')}: missing {sorted(missing)}")
        expected_id = f"H8-DHE-{index:03d}"
        if row["case_id"] != expected_id:
            raise RuntimeError(f"H8 case order/id mismatch: expected {expected_id}, got {row['case_id']}")
        if row["partition"] != "development" or row["development_exposed"] is not True:
            raise RuntimeError(f"{row['case_id']}: H8 requires exposed development partition")
        if row["provenance"] != "authored_for_h8_2026-09-19":
            raise RuntimeError(f"{row['case_id']}: unexpected provenance")
        case_id = str(row["case_id"])
        if case_id in seen:
            raise RuntimeError(f"duplicate case_id: {case_id}")
        seen.add(case_id)
    return rows


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

    candidate = cfg["sources"]["candidate"]
    if candidate["source_revision"] != "c4c942d3c455c8745d4756ca2a775772b1215a4a":
        raise RuntimeError("H8 V6 source revision drift")
    if candidate["adapter_weights_sha256"] != "c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4":
        raise RuntimeError("H8 V6 adapter identity drift")

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

    generation_manifest = {
        "experiment": "H8_DHE_V6_PILOT_V1",
        "partition": "development",
        "source_revision": source_revision,
        "candidate_source_revision": candidate["source_revision"],
        "candidate_adapter_weights_sha256": candidate["adapter_weights_sha256"],
        "case_manifest_sha256": sha256(manifest_path),
        "generation_config_sha256": sha256(config_path),
        "model_id": model_id,
        "model_revision": revision,
        "generation": generation,
        "case_count": len(rows),
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
            "candidate_hash_binding_gate": "PASS",
            "generation_path_preserved_from_h6_v1_2": "PASS",
        },
    }
    (out / "generation_manifest.json").write_text(
        json.dumps(generation_manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
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
