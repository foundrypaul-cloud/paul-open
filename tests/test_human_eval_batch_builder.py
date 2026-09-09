from __future__ import annotations

import json
from pathlib import Path

import pytest

from paul_open_model.evaluation.human_eval import (
    HumanEvalBuildError,
    HumanEvalRecord,
    build_human_eval_batch,
    enforce_sealed_storage_boundary,
    load_human_eval_records,
    write_human_eval_batch,
)


def _record(
    case_id: str,
    response: str,
    *,
    prompt: str | None = None,
    cohort: str = "general_user",
) -> HumanEvalRecord:
    synthetic_number = case_id.rsplit("-", maxsplit=1)[-1]
    return HumanEvalRecord(
        case_id=case_id,
        prompt=prompt or f"Synthetic question number {synthetic_number}?",
        response=response,
        domain="synthetic_domain",
        language="en",
        reviewer_cohort=cohort,
    )


def _paired_sources(
    count: int = 5,
) -> tuple[dict[str, HumanEvalRecord], dict[str, HumanEvalRecord]]:
    left: dict[str, HumanEvalRecord] = {}
    right: dict[str, HumanEvalRecord] = {}
    for index in range(count):
        case_id = f"SYN-{index + 1:03d}"
        left[case_id] = _record(case_id, f"Synthetic left answer {index + 1}.")
        right[case_id] = _record(case_id, f"Synthetic right answer {index + 1}.")
    return left, right


def test_batch_is_deterministic_for_same_seed() -> None:
    left, right = _paired_sources()
    kwargs = {
        "left_label": "checkpoint_alpha",
        "right_label": "checkpoint_beta",
        "seed": "synthetic-seed-001",
        "variant_count": 2,
        "partition": "development",
    }

    first = build_human_eval_batch(left, right, **kwargs)
    second = build_human_eval_batch(left, right, **kwargs)

    assert first == second


def test_public_bundle_never_exposes_source_labels_or_internal_case_ids() -> None:
    left, right = _paired_sources(4)
    batch = build_human_eval_batch(
        left,
        right,
        left_label="SFT_INTERNAL_DO_NOT_SHOW",
        right_label="DPO_INTERNAL_DO_NOT_SHOW",
        seed="blindness-seed",
    )

    serialized_public = json.dumps(
        {
            "manifest": batch.public_manifest,
            "variants": batch.public_variants,
        },
        sort_keys=True,
    )
    assert "SFT_INTERNAL_DO_NOT_SHOW" not in serialized_public
    assert "DPO_INTERNAL_DO_NOT_SHOW" not in serialized_public
    for case_id in left:
        assert case_id not in serialized_public
    for variant in batch.public_variants:
        for comparison in variant["comparisons"]:
            assert "case_id" not in comparison
            assert "response_a_source" not in comparison
            assert "response_b_source" not in comparison

    serialized_private = json.dumps(batch.private_mapping, sort_keys=True)
    assert "SFT_INTERNAL_DO_NOT_SHOW" in serialized_private
    assert "DPO_INTERNAL_DO_NOT_SHOW" in serialized_private


def test_two_variants_are_position_counterbalanced_per_case() -> None:
    left, right = _paired_sources(5)
    batch = build_human_eval_batch(
        left,
        right,
        left_label="left_source",
        right_label="right_source",
        seed="counterbalance-seed",
        variant_count=2,
    )

    by_case: dict[str, list[str]] = {}
    for entry in batch.private_mapping["entries"]:
        by_case.setdefault(entry["case_id"], []).append(entry["response_a_source"])

    assert set(by_case) == set(left)
    for assignments in by_case.values():
        assert sorted(assignments) == ["left_source", "right_source"]


def test_odd_case_count_is_balanced_across_complete_variant_set() -> None:
    left, right = _paired_sources(5)
    batch = build_human_eval_batch(
        left,
        right,
        left_label="left_source",
        right_label="right_source",
        seed="odd-case-seed",
        variant_count=4,
    )

    a_labels = [entry["response_a_source"] for entry in batch.private_mapping["entries"]]
    assert a_labels.count("left_source") == a_labels.count("right_source") == 10


def test_identical_pairs_are_removed_before_human_review() -> None:
    left, right = _paired_sources(3)
    duplicate_id = "SYN-002"
    right[duplicate_id] = _record(duplicate_id, left[duplicate_id].response)

    batch = build_human_eval_batch(
        left,
        right,
        left_label="left_source",
        right_label="right_source",
        seed="duplicate-seed",
    )

    assert batch.public_manifest["eligible_case_count"] == 2
    assert batch.public_manifest["skipped_identical_pair_count"] == 1
    assert batch.private_mapping["skipped_identical_case_ids"] == [duplicate_id]
    assert all(entry["case_id"] != duplicate_id for entry in batch.private_mapping["entries"])


def test_mismatched_case_sets_fail_closed() -> None:
    left, right = _paired_sources(3)
    del right["SYN-003"]

    with pytest.raises(HumanEvalBuildError, match="source case sets differ"):
        build_human_eval_batch(
            left,
            right,
            left_label="left_source",
            right_label="right_source",
            seed="mismatch-seed",
        )


def test_prompt_or_routing_mismatch_fails_closed() -> None:
    left, right = _paired_sources(2)
    right["SYN-001"] = _record(
        "SYN-001",
        right["SYN-001"].response,
        prompt="A different synthetic prompt",
    )

    with pytest.raises(HumanEvalBuildError, match="differs between sources"):
        build_human_eval_batch(
            left,
            right,
            left_label="left_source",
            right_label="right_source",
            seed="prompt-mismatch-seed",
        )


def test_variant_count_must_be_even() -> None:
    left, right = _paired_sources(2)

    with pytest.raises(HumanEvalBuildError, match="even integer"):
        build_human_eval_batch(
            left,
            right,
            left_label="left_source",
            right_label="right_source",
            seed="variant-seed",
            variant_count=3,
        )


def test_private_mapping_cannot_be_written_inside_public_bundle(tmp_path: Path) -> None:
    left, right = _paired_sources(2)
    batch = build_human_eval_batch(
        left,
        right,
        left_label="left_source",
        right_label="right_source",
        seed="path-seed",
    )
    public_dir = tmp_path / "public"

    with pytest.raises(HumanEvalBuildError, match="private mapping"):
        write_human_eval_batch(
            batch,
            public_output_dir=public_dir,
            private_mapping_path=public_dir / "mapping.json",
        )


def test_write_outputs_separate_public_and_private_artifacts(tmp_path: Path) -> None:
    left, right = _paired_sources(2)
    batch = build_human_eval_batch(
        left,
        right,
        left_label="left_source",
        right_label="right_source",
        seed="write-seed",
    )
    public_dir = tmp_path / "public"
    private_path = tmp_path / "private" / "mapping.json"

    manifest, variants, mapping = write_human_eval_batch(
        batch,
        public_output_dir=public_dir,
        private_mapping_path=private_path,
    )

    assert manifest.is_file()
    assert len(variants) == 2
    assert all(path.is_file() for path in variants)
    assert mapping == private_path.resolve()
    assert mapping.is_file()
    assert "left_source" not in manifest.read_text(encoding="utf-8")
    assert "left_source" in mapping.read_text(encoding="utf-8")


def test_load_json_and_jsonl_inputs(tmp_path: Path) -> None:
    records = [
        {
            "case_id": "SYN-001",
            "prompt": "Synthetic prompt?",
            "response": "Synthetic response.",
            "domain": "synthetic",
            "language": "en",
            "reviewer_cohort": "general_user",
        }
    ]
    json_path = tmp_path / "records.json"
    jsonl_path = tmp_path / "records.jsonl"
    json_path.write_text(json.dumps({"records": records}), encoding="utf-8")
    jsonl_path.write_text(json.dumps(records[0]) + "\n", encoding="utf-8")

    assert load_human_eval_records(json_path)["SYN-001"].response == "Synthetic response."
    assert load_human_eval_records(jsonl_path)["SYN-001"].response == "Synthetic response."


def test_sealed_assurance_paths_inside_public_repo_are_rejected(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    inside = repo_root / "sealed" / "prompts.json"
    outside = tmp_path / "restricted" / "prompts.json"

    with pytest.raises(HumanEvalBuildError, match="outside the public repository"):
        enforce_sealed_storage_boundary([inside], repository_root=repo_root)

    enforce_sealed_storage_boundary([outside], repository_root=repo_root)
