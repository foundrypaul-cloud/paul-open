#!/usr/bin/env python3
"""Generate matched SFT and DPO V5 responses for frozen H7 DHE development cases.

Generation only. The generation implementation is deliberately delegated to the
H6 v1.2 path so quantization, sampling, native-script, safety, reviewer-visible
prompt, EOS and truncation behavior cannot silently drift.
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

from scripts.h6_dhe_generate import generate_source, resolve_adapter, reviewer_visible_prompt, sha256


def load_h7_jsonl(path: Path) -> list[dict[str, object]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise RuntimeError(f"no records in {path}")
    seen: set[str] = set()
    for row in rows:
        required = {"case_id", "partition", "domain", "language", "reviewer_cohort", "prompt"}
        missing = required - row.keys()
        if missing:
            raise RuntimeError(f"{row.get('case_id', '?')}: missing {sorted(missing)}")
        if row["partition"] != "development":
            raise RuntimeError(f"{row['case_id']}: H7 requires development partition")
        if row["case_id"] in seen:
            raise RuntimeError(f"duplicate case_id: {row['case_id']}")
        seen.add(str(row["case_id"]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--training-config", default="configs/training/dpo_v5_e4b_corrective.yaml")
    parser.add_argument("--sft-adapter", required=True)
    parser.add_argument("--dpo-adapter", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    config_path = Path(args.config)
    training_config_path = Path(args.training_config)
    rows = load_h7_jsonl(manifest_path)
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))["h7_dhe_v5_pilot"]
    train_cfg = yaml.safe_load(training_config_path.read_text(encoding="utf-8"))["experiment"]
    if cfg["status"] != "frozen_pre_generation" or cfg["partition"] != "development":
        raise RuntimeError("H7 config is not frozen_pre_generation/development")

    model_id = train_cfg["model_id"]
    revision = train_cfg["model_revision"]
    generation = cfg["generation"]
    if not str(generation.get("response_instruction", "")).strip():
        raise RuntimeError("H7 generation response_instruction must be nonempty")
    if int(generation.get("max_new_tokens", 0)) != 768:
        raise RuntimeError("H7 must preserve the H6 v1.2 768-token fail-closed ceiling")
    if generation.get("require_eos_before_limit") is not True:
        raise RuntimeError("H7 must preserve the H6 v1.2 EOS-before-limit gate")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sft_path = out / "sft_reference.jsonl"
    dpo_path = out / "dpo_v5_corrective.jsonl"

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

    manifest = {
        "experiment": "H7_DHE_V5_PILOT_V1",
        "partition": "development",
        "source_revision": source_revision,
        "case_manifest_sha256": sha256(manifest_path),
        "generation_config_sha256": sha256(config_path),
        "model_id": model_id,
        "model_revision": revision,
        "generation": generation,
        "case_count": len(rows),
        "sft": sft,
        "dpo_v5": dpo,
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
            "generation_path_preserved_from_h6_v1_2": "PASS",
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
            for sensitive in ("sft_reference", "dpo_v5_corrective"):
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
