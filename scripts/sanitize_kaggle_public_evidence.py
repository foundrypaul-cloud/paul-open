#!/usr/bin/env python3
"""Create public-safe, aggregate-only evidence from a private Kaggle output tree.

PRIVATE SOURCE -> explicit field allowlist -> PUBLIC SAFE OUTPUT

The script never copies raw result objects, prompts, responses, mappings, seeds,
filesystem paths, credentials, checkpoints, or adapter weights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

STATUS_FIELDS = {
    "status",
    "experiment_id",
    "benchmark_version",
    "model_id",
    "model_revision",
    "persistence_mode",
    "completed_cases",
    "failed_cases",
    "total_cases",
    "peak_vram_gib",
    "peak_vram_gb",
    "average_latency_seconds",
    "mean_rubric_score",
    "timestamp_utc",
}

SUMMARY_FIELDS = {
    "total_cases_evaluated",
    "mean_rubric_score",
    "mean_keyword_coverage",
    "overall_safety_adherence",
    "mean_latency_seconds",
    "total_evaluation_time_seconds",
    "peak_vram_observed_gb",
    "cases_flagged_for_human_review",
    "automated_metric_coverage",
}

MANIFEST_FIELDS = {
    "experiment_id",
    "model_id",
    "model_revision",
    "source_revision",
    "dataset_records",
    "dataset_sha256",
    "configured_epochs",
    "trainer_global_step",
    "adapter_config_sha256",
    "adapter_weights_sha256",
}

TRAIN_METRIC_FIELDS = {
    "epoch",
    "train_loss",
    "train_runtime",
    "train_samples_per_second",
    "train_steps_per_second",
}

UPDATE_EVIDENCE_FIELDS = {
    "changed_tensor_count",
    "intended_tensor_count",
    "finite",
}

FAILURE_FIELDS = {
    "status",
    "failed_stage",
    "exception_type",
}

SAFE_SCALAR_TYPES = (str, int, float, bool, type(None))


def allow_scalars(source: Any, allowed: set[str]) -> dict[str, Any]:
    if not isinstance(source, dict):
        return {}
    return {
        key: source[key]
        for key in sorted(allowed)
        if key in source and isinstance(source[key], SAFE_SCALAR_TYPES)
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def classify(path: Path) -> str | None:
    name = path.name.lower()
    if name == "training_manifest.json":
        return "training_manifest"
    if name == "failure_summary.json":
        return "failure"
    if name.endswith("_status.json") or name == "status.json":
        return "status"
    if name.endswith("_results.json") or name in {"results.json", "evaluation.json"}:
        return "results"
    return None


def sanitize_json(path: Path, kind: str) -> dict[str, Any] | None:
    data = load_json(path)
    if not isinstance(data, dict):
        return None
    if kind == "training_manifest":
        out = allow_scalars(data, MANIFEST_FIELDS)
        metrics = allow_scalars(data.get("train_metrics"), TRAIN_METRIC_FIELDS)
        updates = allow_scalars(data.get("authentic_update_evidence"), UPDATE_EVIDENCE_FIELDS)
        if metrics:
            out["train_metrics"] = metrics
        if updates:
            out["authentic_update_evidence"] = updates
        return out or None
    if kind == "failure":
        out = allow_scalars(data, FAILURE_FIELDS)
        # H6 wrappers historically wrote `stage`; normalize it to the public schema.
        if "failed_stage" not in out and isinstance(data.get("stage"), SAFE_SCALAR_TYPES):
            out["failed_stage"] = data["stage"]
        return out or None
    if kind == "status":
        return allow_scalars(data, STATUS_FIELDS) or None
    if kind == "results":
        out: dict[str, Any] = {}
        manifest = allow_scalars(data.get("manifest"), STATUS_FIELDS)
        summary = allow_scalars(data.get("overall_summary"), SUMMARY_FIELDS)
        if manifest:
            out["manifest"] = manifest
        if summary:
            out["overall_summary"] = summary
        # Intentionally omit metadata, domain/language breakdowns, and case_results.
        return out or None
    return None


def collect(input_dir: Path) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "schema_version": 1,
        "publication_policy": "aggregate_allowlist_only",
        "source_classification": "private_kaggle_output",
        "records": [],
        "adapter_weight_digests": [],
    }

    for path in sorted(input_dir.rglob("*.json")):
        kind = classify(path)
        if not kind:
            continue
        sanitized = sanitize_json(path, kind)
        if sanitized:
            evidence["records"].append({"kind": kind, "data": sanitized})

    for path in sorted(input_dir.rglob("*.safetensors")):
        evidence["adapter_weight_digests"].append(
            {
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )

    evidence["structured_record_count"] = len(evidence["records"])
    evidence["adapter_digest_count"] = len(evidence["adapter_weight_digests"])
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.is_dir():
        raise SystemExit("private input directory not found")

    evidence = collect(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("Wrote aggregate-only public evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
