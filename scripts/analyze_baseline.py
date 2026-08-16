#!/usr/bin/env python3
"""Post-processing and analysis tool for PAUL Open Model baseline evaluation results.

Reads generated experiment directories (results/baseline/<experiment_id>/),
audits result integrity, verifies secret exclusion, and generates scorecards
without loading any model weights or requiring a GPU.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def find_latest_experiment(base_dir: Path) -> Path | None:
    """Find the most recent experiment directory in results/baseline/."""
    if not base_dir.exists():
        return None
    dirs = [d for d in base_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not dirs:
        return None
    return max(dirs, key=lambda p: p.stat().st_mtime)


def audit_secret_exclusion(exp_dir: Path) -> list[str]:
    """Scan all text and json files in the experiment directory for accidental secrets."""
    forbidden_terms = ["hf_", "password", "secret", "private_key", "paul-foundry", "/home/"]
    issues: list[str] = []

    for file_path in exp_dir.glob("*"):
        if file_path.is_file() and file_path.suffix in [".json", ".csv", ".md", ".log"]:
            try:
                content = file_path.read_text(encoding="utf-8")
                content_lower = content.lower()
                for term in forbidden_terms:
                    # Ignore the word 'secret' in generic phrases like 'Colab Secrets'
                    if term == "secret" and "colab secret" in content_lower:
                        continue
                    if term in content_lower:
                        msg = f"{file_path.name}: contains sensitive term '{term}'"
                        issues.append(msg)
            except Exception as e:
                issues.append(f"{file_path.name}: failed to read: {e}")
    return issues


def analyze_experiment(exp_dir: Path, verbose: bool = True) -> dict[str, Any]:
    """Analyze results in an experiment directory and print summary tables."""
    results_file = exp_dir / "results.json"
    status_file = exp_dir / "STATUS.json"
    manifest_file = exp_dir / "manifest.json"

    if not results_file.exists():
        raise FileNotFoundError(f"Missing results.json in: {exp_dir}")

    with open(results_file, encoding="utf-8") as f:
        results_data = json.load(f)

    status_data: dict[str, Any] = {}
    if status_file.exists():
        with open(status_file, encoding="utf-8") as f:
            status_data = json.load(f)

    manifest_data: dict[str, Any] = {}
    if manifest_file.exists():
        with open(manifest_file, encoding="utf-8") as f:
            manifest_data = json.load(f)

    meta = results_data.get("metadata", {})
    summary = results_data.get("overall_summary", {})
    domains = results_data.get("domain_breakdown", {})
    languages = results_data.get("language_breakdown", {})
    cases = results_data.get("case_results", [])

    # Audit for potential leaks
    leaks = audit_secret_exclusion(exp_dir)

    if verbose:
        print("=" * 75)
        print(" PAUL OPEN MODEL — BASELINE EXPERIMENT ANALYSIS REPORT")
        print("=" * 75)
        print(f" Experiment Directory : {exp_dir}")
        print(f" Experiment ID        : {meta.get('experiment_id', 'N/A')}")
        print(f" Persistence Mode     : {manifest_data.get('persistence_mode', 'UNKNOWN').upper()}")
        print(f" Drive Mirror Path    : {manifest_data.get('drive_results_path', 'None')}")
        print(f" Model ID             : {meta.get('model_id', 'N/A')}")
        print(f" Benchmark Version    : {meta.get('benchmark_version', 'N/A')}")
        print(f" Execution Status     : {status_data.get('status', 'UNKNOWN')}")
        print(f" Total Cases          : {len(cases)} / {status_data.get('total_cases', 50)}")
        print(f" Mean Rubric Score    : {summary.get('mean_rubric_score', 0.0):.1f} / 100")
        print(f" Overall Safety Rate  : {summary.get('overall_safety_adherence', 0.0):.1%}")
        print(f" Mean Latency         : {summary.get('mean_latency_seconds', 0.0):.2f} s")
        print(f" Peak VRAM Observed   : {summary.get('peak_vram_observed_gb', 0.0):.2f} GiB")
        print("=" * 75)

        print("\n--- 1. DOMAIN BREAKDOWN ---")
        header_d = f"{'Domain':<26} {'Cases':<6} {'Rubric':<12} {'Keywords':<10} {'Safety':<8}"
        print(header_d)
        print("-" * 75)
        for dom, stats in sorted(domains.items()):
            print(
                f"{dom:<26} {stats['case_count']:<6} {stats['mean_rubric_score']:<12.1f} "
                f"{stats['mean_keyword_coverage']:<10.1%} {stats['safety_pass_rate']:<8.1%}"
            )

        print("\n--- 2. LANGUAGE BREAKDOWN ---")
        header_l = f"{'Language':<14} {'Cases':<6} {'Rubric (0-100)':<16} {'Script Match':<14}"
        print(header_l)
        print("-" * 75)
        for lang, stats in sorted(languages.items()):
            print(
                f"{lang:<14} {stats['case_count']:<6} {stats['mean_rubric_score']:<16.1f} "
                f"{stats['script_match_rate']:<14.1%}"
            )

        print("\n--- 3. SECURITY & INTEGRITY AUDIT ---")
        if not leaks:
            print("✓ Clean: Zero secrets, tokens, credentials, or private paths detected.")
        else:
            print("⚠ WARNINGS DETECTED:")
            for issue in leaks:
                print(f"  - {issue}")
        print("=" * 75)

    return {
        "manifest": manifest_data,
        "metadata": meta,
        "status": status_data,
        "summary": summary,
        "domains": domains,
        "languages": languages,
        "security_audit_clean": len(leaks) == 0,
        "security_issues": leaks,
    }


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Analyze PAUL Open Model baseline results.")
    parser.add_argument(
        "--experiment-dir",
        "-d",
        type=str,
        help="Path to experiment directory (e.g. results/baseline/exp_gemma4_e4b_baseline_...)",
    )
    parser.add_argument(
        "--latest",
        "-l",
        action="store_true",
        help="Analyze the most recent experiment in results/baseline/",
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default="results/baseline",
        help="Base directory containing experiments (default: results/baseline)",
    )
    args = parser.parse_args()

    target_dir: Path | None = None
    if args.experiment_dir:
        target_dir = Path(args.experiment_dir)
    else:
        target_dir = find_latest_experiment(Path(args.base_dir))

    if not target_dir or not target_dir.exists():
        print(f"Error: No valid experiment directory found in {args.base_dir}", file=sys.stderr)
        return 1

    try:
        report = analyze_experiment(target_dir, verbose=True)
        is_success = report["status"].get("status") == "SUCCESS" or (
            report["summary"].get("total_cases_evaluated") == 50
        )
        return 0 if is_success else 1
    except Exception as e:
        print(f"Error analyzing experiment: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
