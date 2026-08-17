#!/usr/bin/env python3
"""CLI utility for auditing training datasets against the Canonical Baseline Benchmark.

Performs strictly read-only inspection against baseline_suite_v1.json to ensure zero contamination.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from paul_open_model.data.leakage import DEFAULT_BENCHMARK_PATH, BenchmarkLeakageChecker


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit candidate training data for leakage against Canonical Benchmark v1.0.0."
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to dataset file (JSON or JSONL) or candidate prompt string.",
    )
    parser.add_argument(
        "--benchmark-path",
        "-b",
        type=str,
        default=str(DEFAULT_BENCHMARK_PATH),
        help=f"Path to canonical benchmark suite (default: {DEFAULT_BENCHMARK_PATH}).",
    )
    parser.add_argument(
        "--json-output",
        "-j",
        type=str,
        help="Optional path to save full leakage report as JSON.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed similarity scores for every record.",
    )

    args = parser.parse_args()
    target_path = Path(args.file)

    try:
        checker = BenchmarkLeakageChecker(benchmark_path=args.benchmark_path)
    except Exception as e:
        print(f"Error initializing leakage checker: {e}", file=sys.stderr)
        return 1

    # Check if target is a file or a raw text string
    if target_path.exists() and target_path.is_file():
        try:
            report = checker.audit_dataset_file(target_path)
        except Exception as e:
            print(f"Error auditing dataset file: {e}", file=sys.stderr)
            return 1

        print("=" * 80)
        print(" PAUL OPEN MODEL — BENCHMARK LEAKAGE AUDIT REPORT")
        print("=" * 80)
        print(f" Target File        : {report['file']}")
        print(f" Benchmark Version  : {report['benchmark_version_checked']}")
        print(f" Total Audited      : {report['total_items_audited']}")
        clean_msg = f"{report['leakage_free_count']} / {report['total_items_audited']}"
        print(f" Clean Records      : {clean_msg}")
        print(f" Contaminated Items : {report['leakage_detected_count']}")
        status_str = "✓ PASS (CLEAN)" if report["is_clean"] else "✗ FAIL (CONTAMINATED)"
        print(f" Audit Status       : {status_str}")
        print("=" * 80)

        if not report["is_clean"]:
            print("\n[CONTAMINATION WARNINGS DETECTED]:")
            for res in report["results"]:
                if res["has_leakage"]:
                    print(f"\n  Candidate ID   : {res['candidate_id']}")
                    print(f"  Leakage Type   : {res['leakage_type']}")
                    print(f"  Matched Case   : {res['matched_benchmark_id']}")
                    print(f"  Similarity     : {res['highest_similarity']:.2%}")
                    print(f"  Details        : {res['details']}")
                    for f in res["flags"]:
                        print(f"    - {f}")

        if args.verbose and report["is_clean"]:
            print("\n--- PER-RECORD SIMILARITY SCORES ---")
            for res in report["results"][:20]:
                sim_msg = f"Max: {res['highest_similarity']:.2%} (vs {res['matched_benchmark_id']})"
                print(f"[{res['candidate_id']}] {sim_msg} - Clean")

        if args.json_output:
            out_path = Path(args.json_output)
            out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(f"\nDetailed JSON report saved to: {out_path}")

        return 0 if report["is_clean"] else 1

    else:
        # Evaluate as a single prompt string
        prompt_text = args.file
        res = checker.check_text(prompt_text, candidate_id="CLI_INPUT")
        print("=" * 80)
        print(" PAUL OPEN MODEL — SINGLE PROMPT LEAKAGE AUDIT")
        print("=" * 80)
        print(f" Leakage Detected : {'✗ YES' if res.has_leakage else '✓ NO'}")
        print(f" Max Similarity   : {res.highest_similarity:.2%}")
        print(f" Matched Benchmark: {res.matched_benchmark_id}")
        print(f" Details          : {res.details}")
        if res.flags:
            print(" Flags:")
            for f in res.flags:
                print(f"   - {f}")
        print("=" * 80)
        return 0 if not res.has_leakage else 1


if __name__ == "__main__":
    sys.exit(main())
