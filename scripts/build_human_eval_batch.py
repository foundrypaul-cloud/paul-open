#!/usr/bin/env python3
"""Build blinded PAUL Open human-evaluation bundles from paired model outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paul_open_model.evaluation.human_eval import (
    HumanEvalBuildError,
    build_human_eval_batch,
    enforce_sealed_storage_boundary,
    find_repository_root,
    load_human_eval_records,
    write_human_eval_batch,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build deterministic, counterbalanced A/B human-evaluation bundles while keeping "
            "source identities in a separate private mapping."
        )
    )
    parser.add_argument("--left", required=True, help="Left source .json or .jsonl file")
    parser.add_argument("--right", required=True, help="Right source .json or .jsonl file")
    parser.add_argument("--left-label", required=True, help="Private identity label for left source")
    parser.add_argument("--right-label", required=True, help="Private identity label for right source")
    parser.add_argument(
        "--seed",
        required=True,
        help="Stable secret/research seed used for deterministic ordering and A/B assignment",
    )
    parser.add_argument(
        "--variant-count",
        type=int,
        default=2,
        help="Even number of complementary variants to generate (default: 2)",
    )
    parser.add_argument(
        "--partition",
        choices=("development", "sealed_assurance"),
        default="development",
        help="Human-evaluation partition (default: development)",
    )
    parser.add_argument(
        "--public-output-dir",
        default="outputs/human_eval/public",
        help="Reviewer-facing bundle directory (default is gitignored)",
    )
    parser.add_argument(
        "--private-mapping",
        default=".human-eval-private/mapping.json",
        help="Private source-identity mapping path (default is gitignored)",
    )
    parser.add_argument(
        "--sealed-storage-acknowledged",
        action="store_true",
        help=(
            "Required for sealed_assurance. Confirms that sealed prompts/outputs are being handled "
            "outside the public repository."
        ),
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        repo_root = find_repository_root(Path.cwd())
        if args.partition == "sealed_assurance":
            if not args.sealed_storage_acknowledged:
                raise HumanEvalBuildError(
                    "sealed_assurance requires --sealed-storage-acknowledged"
                )
            enforce_sealed_storage_boundary(
                [args.left, args.right, args.public_output_dir, args.private_mapping],
                repository_root=repo_root,
            )

        left = load_human_eval_records(args.left)
        right = load_human_eval_records(args.right)
        batch = build_human_eval_batch(
            left,
            right,
            left_label=args.left_label,
            right_label=args.right_label,
            seed=args.seed,
            variant_count=args.variant_count,
            partition=args.partition,
        )
        manifest_path, variant_paths, private_path = write_human_eval_batch(
            batch,
            public_output_dir=args.public_output_dir,
            private_mapping_path=args.private_mapping,
        )
    except HumanEvalBuildError as exc:
        parser.error(str(exc))

    summary = {
        "batch_id": batch.public_manifest["batch_id"],
        "partition": batch.public_manifest["partition"],
        "eligible_case_count": batch.public_manifest["eligible_case_count"],
        "skipped_identical_pair_count": batch.public_manifest[
            "skipped_identical_pair_count"
        ],
        "public_manifest": str(manifest_path),
        "public_variants": [str(path) for path in variant_paths],
        "private_mapping": str(private_path),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
