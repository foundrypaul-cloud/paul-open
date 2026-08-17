#!/usr/bin/env python3
"""CLI utility for validating SFT and DPO training datasets in PAUL Open Model Phase 3.

Evaluates datasets across:
- Tier 1: Hard validity constraints (syntax, schema, token budget).
- Tier 2: Heuristic screening signals (Socratic probe, translation, STEM).
- Tier 3: Human review metadata status.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from paul_open_model.data.validation import MAX_SINGLE_TURN_TOKENS, validate_dataset_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate SFT or DPO datasets against PAUL Phase 3 tri-tier quality standards."
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to JSON or JSONL dataset file to validate.",
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["sft", "dpo"],
        default="sft",
        help="Dataset format type (default: sft).",
    )
    parser.add_argument(
        "--max-tokens",
        "-m",
        type=int,
        default=MAX_SINGLE_TURN_TOKENS,
        help=f"Max tokens per turn/field (Tier 1 limit, default: {MAX_SINGLE_TURN_TOKENS}).",
    )
    parser.add_argument(
        "--json-output",
        "-j",
        type=str,
        help="Optional path to save full validation report as JSON.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed warnings and per-record findings.",
    )

    args = parser.parse_args()
    target_path = Path(args.file)

    if not target_path.exists():
        print(f"Error: File not found: {target_path}", file=sys.stderr)
        return 1

    try:
        report = validate_dataset_file(
            target_path, dataset_type=args.type, max_tokens_per_turn=args.max_tokens
        )
    except Exception as e:
        print(f"Error validating file: {e}", file=sys.stderr)
        return 1

    print("=" * 80)
    print(" PAUL OPEN MODEL — DATASET VALIDATION REPORT (PHASE 3)")
    print("=" * 80)
    print(f" File               : {report['file']}")
    print(f" Dataset Type       : {report['dataset_type'].upper()}")
    print(f" Max Tokens / Turn  : {report['max_tokens_per_turn']}")
    print(f" Total Records      : {report['total_records']}")
    print(f" Tier 1 Valid       : {report['valid_records']} / {report['total_records']}")
    print(f" Tier 1 Invalid     : {report['invalid_records']}")
    print(f" Tier 2 Warnings    : {report['total_warnings']}")
    print(f" Tier 3 Approved    : {report['tier3_approved_records']} / {report['total_records']}")
    print(f" Tier 3 Pending     : {report['tier3_pending_records']}")
    print("=" * 80)

    if report["errors"]:
        print("\n[TIER 1 HARD ERRORS - ACTION REQUIRED]:")
        for err in report["errors"][:15]:
            print(f"  ✗ {err}")
        if len(report["errors"]) > 15:
            print(f"  ... and {len(report['errors']) - 15} more errors.")

    if report["warnings"]:
        print("\n[TIER 2 HEURISTIC SCREENING WARNINGS - FOR AUDIT]:")
        for warn in report["warnings"][:15]:
            print(f"  ⚠ {warn}")
        if len(report["warnings"]) > 15:
            print(f"  ... and {len(report['warnings']) - 15} more warnings.")

    if args.verbose and report["results"]:
        print("\n--- PER-RECORD DETAILS ---")
        for res in report["results"]:
            status_symbol = "✓ PASS" if res["is_valid"] else "✗ FAIL"
            warn_count = len(res["warnings"])
            rev_status = res["tier3_review"].get("review_status", "pending")
            print(f"[{res['id']}] {status_symbol} | Warnings: {warn_count} | Review: {rev_status}")
            for err in res["errors"]:
                print(f"    Error: {err}")
            for w in res["warnings"]:
                print(f"    Warning: {w}")

    if args.json_output:
        out_path = Path(args.json_output)
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nDetailed JSON report saved to: {out_path}")

    return 0 if report["is_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
