"""Deterministic, contamination-aware human-evaluation batch construction.

This module builds reviewer-facing A/B comparison bundles without exposing the
underlying source/checkpoint identities. It deliberately contains no Google
Forms API logic; Forms/Sheets integration is the next workflow layer.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "1.0"
_ALLOWED_PARTITIONS = {"development", "sealed_assurance"}
_ALLOWED_COHORTS = {
    "general_user",
    "educator",
    "bilingual",
    "stem_capable",
    "domain_expert",
}


class HumanEvalBuildError(ValueError):
    """Raised when a human-evaluation batch cannot be built safely."""


@dataclass(frozen=True)
class HumanEvalRecord:
    """One candidate response for a human-evaluation case."""

    case_id: str
    prompt: str
    response: str
    domain: str
    language: str
    reviewer_cohort: str


@dataclass(frozen=True)
class HumanEvalBatch:
    """Public reviewer bundles plus the separate private identity mapping."""

    public_manifest: dict[str, Any]
    public_variants: tuple[dict[str, Any], ...]
    private_mapping: dict[str, Any]


def _clean_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def _stable_digest(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _canonical_record_payload(record: HumanEvalRecord) -> dict[str, str]:
    return {
        "case_id": record.case_id,
        "prompt": record.prompt,
        "response": record.response,
        "domain": record.domain,
        "language": record.language,
        "reviewer_cohort": record.reviewer_cohort,
    }


def _records_fingerprint(records: dict[str, HumanEvalRecord]) -> str:
    payload = [_canonical_record_payload(records[key]) for key in sorted(records)]
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _parse_record(raw: Any, *, source: Path, index: int) -> HumanEvalRecord:
    if not isinstance(raw, dict):
        raise HumanEvalBuildError(f"{source}: record {index} must be a JSON object")

    required = {
        "case_id",
        "prompt",
        "response",
        "domain",
        "language",
        "reviewer_cohort",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise HumanEvalBuildError(
            f"{source}: record {index} missing required fields: {', '.join(missing)}"
        )

    values: dict[str, str] = {}
    for field in sorted(required):
        value = raw[field]
        if not isinstance(value, str):
            raise HumanEvalBuildError(f"{source}: record {index} field {field!r} must be text")
        cleaned = _clean_text(value)
        if not cleaned:
            raise HumanEvalBuildError(f"{source}: record {index} field {field!r} cannot be empty")
        values[field] = cleaned

    if values["reviewer_cohort"] not in _ALLOWED_COHORTS:
        allowed = ", ".join(sorted(_ALLOWED_COHORTS))
        raise HumanEvalBuildError(
            f"{source}: record {index} has unsupported reviewer_cohort; expected one of {allowed}"
        )

    return HumanEvalRecord(**values)


def load_human_eval_records(path: str | Path) -> dict[str, HumanEvalRecord]:
    """Load strict human-evaluation source records from JSON or JSONL."""

    source = Path(path)
    if not source.is_file():
        raise HumanEvalBuildError(f"source file does not exist: {source}")

    if source.suffix.lower() == ".jsonl":
        raw_records: list[Any] = []
        lines = source.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                raw_records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise HumanEvalBuildError(
                    f"{source}: invalid JSON on line {line_number}: {exc.msg}"
                ) from exc
    elif source.suffix.lower() == ".json":
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise HumanEvalBuildError(f"{source}: invalid JSON: {exc.msg}") from exc
        raw_records = payload.get("records") if isinstance(payload, dict) else payload
        if not isinstance(raw_records, list):
            raise HumanEvalBuildError(
                f"{source}: JSON input must be an array or an object containing a records array"
            )
    else:
        raise HumanEvalBuildError(f"{source}: expected .json or .jsonl input")

    records: dict[str, HumanEvalRecord] = {}
    for index, raw in enumerate(raw_records, start=1):
        record = _parse_record(raw, source=source, index=index)
        if record.case_id in records:
            raise HumanEvalBuildError(f"{source}: duplicate case_id {record.case_id!r}")
        records[record.case_id] = record

    if not records:
        raise HumanEvalBuildError(f"{source}: no records found")
    return records


def _validate_pair_sources(
    left: dict[str, HumanEvalRecord],
    right: dict[str, HumanEvalRecord],
) -> tuple[list[str], list[str]]:
    if set(left) != set(right):
        missing_left = sorted(set(right) - set(left))
        missing_right = sorted(set(left) - set(right))
        details = []
        if missing_left:
            details.append(f"missing from left: {missing_left}")
        if missing_right:
            details.append(f"missing from right: {missing_right}")
        raise HumanEvalBuildError("source case sets differ; " + "; ".join(details))

    eligible: list[str] = []
    duplicates: list[str] = []
    for case_id in sorted(left):
        a = left[case_id]
        b = right[case_id]
        for field in ("prompt", "domain", "language", "reviewer_cohort"):
            if getattr(a, field) != getattr(b, field):
                raise HumanEvalBuildError(
                    f"case {case_id!r} differs between sources for field {field!r}"
                )
        if a.response == b.response:
            duplicates.append(case_id)
        else:
            eligible.append(case_id)

    if not eligible:
        raise HumanEvalBuildError("all paired responses are identical; nothing useful to review")
    return eligible, duplicates


def build_human_eval_batch(
    left: dict[str, HumanEvalRecord],
    right: dict[str, HumanEvalRecord],
    *,
    left_label: str,
    right_label: str,
    seed: str,
    variant_count: int = 2,
    partition: str = "development",
) -> HumanEvalBatch:
    """Build deterministic, counterbalanced reviewer bundles.

    Public bundles contain only anonymous Response A / Response B text. Source
    labels and internal case IDs exist only in the returned private mapping.
    Variant counts must be even so every case appears equally often with each
    source in position A across the complete variant set.
    """

    left_label = _clean_text(left_label)
    right_label = _clean_text(right_label)
    seed = _clean_text(seed)
    if not left_label or not right_label:
        raise HumanEvalBuildError("source labels cannot be empty")
    if left_label == right_label:
        raise HumanEvalBuildError("source labels must be distinct")
    if not seed:
        raise HumanEvalBuildError("seed cannot be empty")
    if partition not in _ALLOWED_PARTITIONS:
        raise HumanEvalBuildError(
            f"unsupported partition {partition!r}; expected one of {sorted(_ALLOWED_PARTITIONS)}"
        )
    if variant_count < 2 or variant_count % 2:
        raise HumanEvalBuildError("variant_count must be an even integer of at least 2")

    eligible, duplicate_case_ids = _validate_pair_sources(left, right)
    left_fingerprint = _records_fingerprint(left)
    right_fingerprint = _records_fingerprint(right)
    batch_id = "HEB1-" + _stable_digest(
        PROTOCOL_VERSION,
        seed,
        left_fingerprint,
        right_fingerprint,
    )[:12].upper()

    side_order = sorted(eligible, key=lambda case_id: _stable_digest(seed, "side", case_id))
    base_left_on_a = set(side_order[: (len(side_order) + 1) // 2])

    public_variants: list[dict[str, Any]] = []
    mapping_entries: list[dict[str, str]] = []

    for variant_index in range(variant_count):
        variant_id = f"V{variant_index + 1:02d}"
        invert = bool(variant_index % 2)
        order = sorted(
            eligible,
            key=lambda case_id: _stable_digest(seed, "order", str(variant_index), case_id),
        )
        comparisons: list[dict[str, str]] = []

        for case_id in order:
            left_on_a = case_id in base_left_on_a
            if invert:
                left_on_a = not left_on_a

            source_a = left if left_on_a else right
            source_b = right if left_on_a else left
            label_a = left_label if left_on_a else right_label
            label_b = right_label if left_on_a else left_label
            record = left[case_id]
            comparison_id = "HEV1-" + _stable_digest(
                seed,
                "comparison",
                variant_id,
                case_id,
            )[:12].upper()

            comparisons.append(
                {
                    "comparison_id": comparison_id,
                    "domain": record.domain,
                    "language": record.language,
                    "reviewer_cohort": record.reviewer_cohort,
                    "prompt": record.prompt,
                    "response_a": source_a[case_id].response,
                    "response_b": source_b[case_id].response,
                }
            )
            mapping_entries.append(
                {
                    "comparison_id": comparison_id,
                    "variant_id": variant_id,
                    "case_id": case_id,
                    "response_a_source": label_a,
                    "response_b_source": label_b,
                }
            )

        public_variants.append(
            {
                "protocol_version": PROTOCOL_VERSION,
                "batch_id": batch_id,
                "partition": partition,
                "variant_id": variant_id,
                "comparisons": comparisons,
            }
        )

    public_manifest = {
        "protocol_version": PROTOCOL_VERSION,
        "batch_id": batch_id,
        "partition": partition,
        "variant_count": variant_count,
        "eligible_case_count": len(eligible),
        "skipped_identical_pair_count": len(duplicate_case_ids),
        "counterbalancing": "complementary_even_variants",
        "model_identity_exposed": False,
    }
    private_mapping = {
        "protocol_version": PROTOCOL_VERSION,
        "batch_id": batch_id,
        "partition": partition,
        "seed": seed,
        "sources": {
            "left": {"label": left_label, "fingerprint": left_fingerprint},
            "right": {"label": right_label, "fingerprint": right_fingerprint},
        },
        "skipped_identical_case_ids": duplicate_case_ids,
        "entries": mapping_entries,
    }
    return HumanEvalBatch(
        public_manifest=public_manifest,
        public_variants=tuple(public_variants),
        private_mapping=private_mapping,
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_human_eval_batch(
    batch: HumanEvalBatch,
    *,
    public_output_dir: str | Path,
    private_mapping_path: str | Path,
) -> tuple[Path, tuple[Path, ...], Path]:
    """Write public bundles and private mapping to physically separate paths."""

    public_dir = Path(public_output_dir).resolve()
    private_path = Path(private_mapping_path).resolve()
    if private_path == public_dir or private_path.is_relative_to(public_dir):
        raise HumanEvalBuildError(
            "private mapping must not be stored inside the reviewer-facing public output directory"
        )

    manifest_path = public_dir / "manifest.json"
    _write_json(manifest_path, batch.public_manifest)
    variant_paths: list[Path] = []
    for variant in batch.public_variants:
        variant_id = str(variant["variant_id"]).lower()
        path = public_dir / f"variant_{variant_id}.json"
        _write_json(path, variant)
        variant_paths.append(path)
    _write_json(private_path, batch.private_mapping)
    return manifest_path, tuple(variant_paths), private_path


def find_repository_root(start: str | Path) -> Path | None:
    """Find a likely repository root without invoking git."""

    current = Path(start).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".github").is_dir():
            return candidate
    return None


def enforce_sealed_storage_boundary(
    paths: list[str | Path],
    *,
    repository_root: str | Path | None,
) -> None:
    """Reject sealed-assurance inputs/outputs located inside the public repo."""

    if repository_root is None:
        return
    root = Path(repository_root).resolve()
    for value in paths:
        resolved = Path(value).resolve()
        if resolved == root or resolved.is_relative_to(root):
            raise HumanEvalBuildError(
                f"sealed-assurance material must stay outside the public repository: {resolved}"
            )
