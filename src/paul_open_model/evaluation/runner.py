"""Evaluation runner engine for executing benchmark suites on Gemma 4 models.

Handles autonomous execution, dual-mode persistence (runtime-local vs Google Drive mirror),
checkpointing/resume support, latency timing, memory profiling, result aggregation,
secret sanitization, and multi-format export.
"""

import csv
import json
import logging
import platform
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from paul_open_model.evaluation.benchmark import (
    BASELINE_VERSION,
    BenchmarkCase,
    BenchmarkSuite,
    get_baseline_benchmark_suite,
)
from paul_open_model.evaluation.metrics import (
    CaseEvaluationResult,
    compute_domain_aggregates,
    compute_language_aggregates,
    compute_overall_summary,
    evaluate_case_response,
)


class EvaluationRunner:
    """Orchestrates model inference across a benchmark suite and exports reports."""

    def __init__(
        self,
        model: Any = None,
        processor: Any = None,
        suite: BenchmarkSuite | None = None,
        model_id: str = "google/gemma-4-E4B-it",
        model_revision: str | None = None,
        experiment_id: str | None = None,
        output_dir: str | Path = "results/baseline",
        drive_backup_dir: str | Path | None = None,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        random_seed: int = 42,
        resume: bool = True,
        gpu_device: str | None = None,
        total_vram_gb: float | None = None,
    ) -> None:
        self.model = model
        self.processor = processor
        self.suite = suite or get_baseline_benchmark_suite()
        self.model_id = model_id
        self.model_revision = model_revision or "main"

        # Unique experiment identifier
        now_str = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        self.experiment_id = experiment_id or f"exp_gemma4_e4b_baseline_{now_str}"

        # Local working directory
        self.base_output_dir = Path(output_dir)
        self.exp_dir = self.base_output_dir / self.experiment_id
        self.exp_dir.mkdir(parents=True, exist_ok=True)

        # Optional Google Drive mirrored backup directory
        self.drive_exp_dir: Path | None = None
        if drive_backup_dir is not None:
            self.drive_exp_dir = Path(drive_backup_dir) / self.experiment_id
            try:
                self.drive_exp_dir.mkdir(parents=True, exist_ok=True)
                self.persistence_mode = "drive_mirrored"
            except Exception:
                self.drive_exp_dir = None
                self.persistence_mode = "runtime_local"
        else:
            self.persistence_mode = "runtime_local"

        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.random_seed = random_seed
        self.resume = resume
        self.gpu_device = gpu_device
        self.total_vram_gb = total_vram_gb

        self.results: list[CaseEvaluationResult] = []
        self._setup_logger()

    def _setup_logger(self) -> None:
        """Configure logging to both file and console."""
        self.logger = logging.getLogger(f"EvaluationRunner.{self.experiment_id}")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        log_file = self.exp_dir / "execution.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _mirror_file_to_drive(self, src_path: Path) -> None:
        """Safely mirror an artifact file to Google Drive if active."""
        if self.drive_exp_dir is not None and src_path.exists():
            try:
                dest_path = self.drive_exp_dir / src_path.name
                shutil.copy2(src_path, dest_path)
            except Exception as e:
                self.logger.warning(f"Failed to mirror {src_path.name} to Drive: {e}")

    def _get_package_versions(self) -> dict[str, str]:
        """Collect package version information safely."""
        pkgs = ["torch", "transformers", "peft", "bitsandbytes", "accelerate", "datasets"]
        versions: dict[str, str] = {}
        for pkg in pkgs:
            try:
                mod = __import__(pkg)
                versions[pkg] = getattr(mod, "__version__", "unknown")
            except ImportError:
                versions[pkg] = "not_installed"
        return versions

    def run_case_inference(self, case: BenchmarkCase) -> tuple[str, float, float]:
        """Execute model generation on a single benchmark prompt.

        Returns (response_text, latency_seconds, peak_vram_gb).
        """
        if self.model is None or self.processor is None:
            # Mock fallback for test harnesses without GPU weights
            mock_resp = f"[MOCK EVALUATION] Model response addressing: {case.prompt[:60]}..."
            return mock_resp, 0.05, 0.0

        import torch

        # Format input using native chat template
        messages = [{"role": "user", "content": case.prompt}]
        formatted_prompt = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

        inputs = self.processor(text=formatted_prompt, return_tensors="pt").to(self.model.device)
        input_len = inputs["input_ids"].shape[1]

        start_time = time.perf_counter()
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
            )
        latency = time.perf_counter() - start_time

        generated_tokens = outputs[0][input_len:]
        response_text = self.processor.decode(generated_tokens, skip_special_tokens=True).strip()

        peak_vram = (
            torch.cuda.max_memory_allocated() / (1024**3) if torch.cuda.is_available() else 0.0
        )
        return response_text, latency, peak_vram

    def _load_completed_cases_from_checkpoint(
        self, ckpt_path: Path
    ) -> dict[str, CaseEvaluationResult]:
        """Parse completed cases from a checkpoint.jsonl file."""
        completed: dict[str, CaseEvaluationResult] = {}
        if not ckpt_path.exists():
            return completed

        with open(ckpt_path, encoding="utf-8") as f:
            for line in f:
                line_s = line.strip()
                if line_s:
                    data = json.loads(line_s)
                    c_id = data["case_id"]
                    completed[c_id] = CaseEvaluationResult(
                        case_id=data["case_id"],
                        domain=data["domain"],
                        language=data["language"],
                        prompt=data["prompt"],
                        response=data["response"],
                        latency_seconds=data["latency_seconds"],
                        peak_vram_gb=data["peak_vram_gb"],
                        token_count=data["token_count"],
                        keyword_coverage_score=data["keyword_coverage_score"],
                        matched_keywords=data["matched_keywords"],
                        missing_keywords=data["missing_keywords"],
                        safety_adherence_score=data["safety_adherence_score"],
                        safety_violations=data["safety_violations"],
                        script_match_score=data["script_match_score"],
                        detected_script=data["detected_script"],
                        length_compliance_score=data["length_compliance_score"],
                        heuristic_rubric_score=data["heuristic_rubric_score"],
                        human_review_required=data["human_review_required"],
                        human_review_reason=data.get("human_review_reason"),
                    )
        return completed

    def run_all(self, verbose: bool = True) -> list[CaseEvaluationResult]:
        """Run all cases with checkpointing and optional Google Drive mirroring."""
        local_ckpt_path = self.exp_dir / "checkpoint.jsonl"
        completed_cases: dict[str, CaseEvaluationResult] = {}

        # 1. Resume check: Check Google Drive mirror first if available, then local checkpoint
        if self.resume:
            if self.drive_exp_dir is not None:
                drive_ckpt = self.drive_exp_dir / "checkpoint.jsonl"
                if drive_ckpt.exists():
                    drive_cases = self._load_completed_cases_from_checkpoint(drive_ckpt)
                    if len(drive_cases) > len(completed_cases):
                        completed_cases = drive_cases
                        # Sync drive checkpoint to local
                        shutil.copy2(drive_ckpt, local_ckpt_path)
                        self.logger.info(
                            f"Restored {len(completed_cases)} cases from Google Drive mirror."
                        )

            if not completed_cases and local_ckpt_path.exists():
                completed_cases = self._load_completed_cases_from_checkpoint(local_ckpt_path)
                if completed_cases:
                    self.logger.info(
                        f"Restored {len(completed_cases)} cases from local runtime checkpoint."
                    )

        self.results = []
        total_cases = len(self.suite)

        if verbose:
            print("=" * 70)
            print(f" PAUL OPEN MODEL — AUTONOMOUS RUNNER (v{self.suite.version})")
            print(f" Experiment ID    : {self.experiment_id}")
            print(f" Persistence Mode : {self.persistence_mode.upper()}")
            print(f" Local Working Dir: {self.exp_dir}")
            if self.drive_exp_dir is not None:
                print(f" Drive Mirror Dir : {self.drive_exp_dir}")
            else:
                print(" Drive Mirror Dir : None (runtime-local ephemeral storage only)")
            print(f" Target Model     : {self.model_id} ({self.model_revision})")
            print(f" Total Cases      : {total_cases} (Completed: {len(completed_cases)})")
            print("=" * 70)

        # Open local checkpoint file in append mode
        with open(local_ckpt_path, "a", encoding="utf-8") as ckpt_f:
            for idx, case in enumerate(self.suite.cases, start=1):
                if case.case_id in completed_cases:
                    eval_res = completed_cases[case.case_id]
                    self.results.append(eval_res)
                    if verbose:
                        score_str = f"{eval_res.heuristic_rubric_score:.1f}/100"
                        print(
                            f"[{idx:>2}/{total_cases}] Resumed {case.case_id:<12} "
                            f"({case.language}) [Cached: {score_str}]"
                        )
                    continue

                if verbose:
                    msg = (
                        f"[{idx:>2}/{total_cases}] "
                        f"Evaluating {case.case_id:<12} ({case.language})..."
                    )
                    print(msg, end="", flush=True)

                response, latency, peak_vram = self.run_case_inference(case)
                eval_res = evaluate_case_response(
                    case=case,
                    response=response,
                    latency_seconds=latency,
                    peak_vram_gb=peak_vram,
                )
                self.results.append(eval_res)

                # Write immediately to local checkpoint
                ckpt_f.write(json.dumps(eval_res.to_dict(), ensure_ascii=False) + "\n")
                ckpt_f.flush()

                # Mirror to Google Drive checkpoint if active
                if self.drive_exp_dir is not None:
                    self._mirror_file_to_drive(local_ckpt_path)

                log_msg = (
                    f"Evaluated {case.case_id} ({case.language}) | "
                    f"Latency: {latency:.2f}s | Score: {eval_res.heuristic_rubric_score:.1f}/100"
                )
                self.logger.info(log_msg)

                if verbose:
                    score_s = f"{eval_res.heuristic_rubric_score:.1f}/100"
                    print(f" Done ({latency:.2f}s | Score: {score_s})")

        # Export full suite of result artifacts and mirror to Drive
        self.export_all()

        if verbose:
            print("=" * 70)
            print(" Evaluation run completed successfully.")
            print(f" Local artifacts : {self.exp_dir}")
            if self.drive_exp_dir is not None:
                print(f" Drive mirror    : {self.drive_exp_dir}")
            print("=" * 70)

        return self.results

    def generate_manifest_dict(self) -> dict[str, Any]:
        """Generate official results manifest metadata."""
        total_cases = len(self.suite)
        completed_cases = len(self.results)
        failed_cases = total_cases - completed_cases

        return {
            "manifest_version": "1.0.0",
            "experiment_id": self.experiment_id,
            "benchmark_version": self.suite.version,
            "model_id": self.model_id,
            "model_revision": self.model_revision,
            "persistence_mode": self.persistence_mode,
            "local_results_path": str(self.exp_dir),
            "drive_results_path": str(self.drive_exp_dir) if self.drive_exp_dir else None,
            "completed_cases": completed_cases,
            "failed_cases": failed_cases,
            "total_cases": total_cases,
            "status": "SUCCESS" if completed_cases == total_cases else "PARTIAL",
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }

    def generate_metadata_dict(self) -> dict[str, Any]:
        """Compile sanitized metadata dictionary without secrets or local paths."""
        return {
            "experiment_id": self.experiment_id,
            "benchmark_version": self.suite.version,
            "model_id": self.model_id,
            "model_revision": self.model_revision,
            "persistence_mode": self.persistence_mode,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "gpu_device": self.gpu_device or "N/A",
            "gpu_vram_gb": round(self.total_vram_gb, 2) if self.total_vram_gb else 0.0,
            "python_version": platform.python_version(),
            "package_versions": self._get_package_versions(),
            "random_seed": self.random_seed,
            "sampling_parameters": {
                "max_new_tokens": self.max_new_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "enable_thinking": False,
            },
        }

    def generate_status_dict(self) -> dict[str, Any]:
        """Generate machine-readable execution status dictionary."""
        total_cases = len(self.suite)
        completed_cases = len(self.results)
        failed_cases = total_cases - completed_cases

        if completed_cases == total_cases:
            status = "SUCCESS"
        elif completed_cases > 0:
            status = "PARTIAL"
        else:
            status = "FAILED"

        overall = compute_overall_summary(self.results)
        return {
            "status": status,
            "experiment_id": self.experiment_id,
            "benchmark_version": self.suite.version,
            "model_id": self.model_id,
            "persistence_mode": self.persistence_mode,
            "completed_cases": completed_cases,
            "failed_cases": failed_cases,
            "total_cases": total_cases,
            "peak_vram_gib": overall.get("peak_vram_observed_gb", 0.0),
            "average_latency_seconds": overall.get("mean_latency_seconds", 0.0),
            "mean_rubric_score": overall.get("mean_rubric_score", 0.0),
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }

    def generate_report_dict(self) -> dict[str, Any]:
        """Compile a comprehensive structured report dictionary."""
        return {
            "manifest": self.generate_manifest_dict(),
            "metadata": self.generate_metadata_dict(),
            "overall_summary": compute_overall_summary(self.results),
            "domain_breakdown": compute_domain_aggregates(self.results),
            "language_breakdown": compute_language_aggregates(self.results),
            "case_results": [r.to_dict() for r in self.results],
        }

    def export_all(self) -> dict[str, Path]:
        """Export all evaluation artifacts and mirror them to Google Drive if active."""
        artifacts = {
            "results_json": self.export_json(),
            "results_csv": self.export_csv(),
            "summary_md": self.export_markdown(),
            "metadata_json": self.export_metadata(),
            "status_json": self.export_status(),
            "manifest_json": self.export_manifest(),
        }
        # Mirror all artifacts and execution log to Google Drive
        if self.drive_exp_dir is not None:
            for p in artifacts.values():
                self._mirror_file_to_drive(p)
            self._mirror_file_to_drive(self.exp_dir / "execution.log")
            self._mirror_file_to_drive(self.exp_dir / "checkpoint.jsonl")
        return artifacts

    def export_manifest(self, file_path: str | Path | None = None) -> Path:
        """Export manifest.json file."""
        path = Path(file_path or (self.exp_dir / "manifest.json"))
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.generate_manifest_dict(), f, indent=2, ensure_ascii=False)
        return path

    def export_metadata(self, file_path: str | Path | None = None) -> Path:
        """Export metadata.json file."""
        path = Path(file_path or (self.exp_dir / "metadata.json"))
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.generate_metadata_dict(), f, indent=2, ensure_ascii=False)
        return path

    def export_status(self, file_path: str | Path | None = None) -> Path:
        """Export STATUS.json file."""
        path = Path(file_path or (self.exp_dir / "STATUS.json"))
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.generate_status_dict(), f, indent=2, ensure_ascii=False)
        return path

    def export_json(self, file_path: str | Path | None = None) -> Path:
        """Export results.json file."""
        path = Path(file_path or (self.exp_dir / "results.json"))
        path.parent.mkdir(parents=True, exist_ok=True)
        report = self.generate_report_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return path

    def export_csv(self, file_path: str | Path | None = None) -> Path:
        """Export results.csv file."""
        path = Path(file_path or (self.exp_dir / "results.csv"))
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.results:
            return path

        fieldnames = [
            "case_id",
            "domain",
            "language",
            "latency_seconds",
            "peak_vram_gb",
            "token_count",
            "keyword_coverage_score",
            "safety_adherence_score",
            "script_match_score",
            "length_compliance_score",
            "heuristic_rubric_score",
            "human_review_required",
            "human_review_reason",
            "prompt",
            "response",
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.results:
                row = r.to_dict()
                row.pop("matched_keywords", None)
                row.pop("missing_keywords", None)
                row.pop("safety_violations", None)
                row.pop("detected_script", None)
                writer.writerow({k: row.get(k, "") for k in fieldnames})
        return path

    def export_markdown(self, file_path: str | Path | None = None) -> Path:
        """Export formatted summary.md file."""
        path = Path(file_path or (self.exp_dir / "summary.md"))
        path.parent.mkdir(parents=True, exist_ok=True)
        report = self.generate_report_dict()
        summary = report["overall_summary"]
        domains = report["domain_breakdown"]
        langs = report["language_breakdown"]
        status = self.generate_status_dict()

        total_s = f"{summary['total_cases_evaluated']} / {len(self.suite)}"
        lines = [
            f"# Baseline Evaluation Report — {self.experiment_id}",
            "",
            f"**Execution Status**: `{status['status']}`  ",
            f"**Persistence Mode**: `{self.persistence_mode.upper()}`  ",
            f"**Model ID**: `{self.model_id}`  ",
            f"**Model Revision**: `{self.model_revision}`  ",
            f"**Benchmark Version**: `{report['metadata']['benchmark_version']}`  ",
            f"**Timestamp (UTC)**: `{report['metadata']['timestamp_utc']}`  ",
            f"**Total Cases Completed**: `{total_s}`  ",
            f"**Mean Heuristic Rubric Score**: `{summary['mean_rubric_score']:.1f} / 100`  ",
            (
                "**Overall Safety & Anti-Anthropomorphism Pass Rate**: "
                f"`{summary['overall_safety_adherence']:.1%}`  "
            ),
            f"**Mean Latency per Case**: `{summary['mean_latency_seconds']:.2f} s`  ",
            f"**Peak VRAM Observed**: `{summary['peak_vram_observed_gb']:.2f} GiB`  ",
            "",
            "---",
            "",
            "## 1. Domain Performance Breakdown",
            "",
            "| Domain | Cases | Rubric Score | Keyword Cov | Safety | Latency | Review Needed |",
            "|---|---|---|---|---|---|---|",
        ]

        for dom_name, stats in sorted(domains.items()):
            lines.append(
                f"| `{dom_name}` | {stats['case_count']} | {stats['mean_rubric_score']:.1f} | "
                f"{stats['mean_keyword_coverage']:.1%} | {stats['safety_pass_rate']:.1%} | "
                f"{stats['mean_latency_seconds']:.2f}s | {stats['human_review_cases']} |"
            )

        lines.extend(
            [
                "",
                "---",
                "",
                "## 2. Language Breakdown",
                "",
                "| Language Code | Cases | Rubric Score | Script Match Rate | Mean Latency |",
                "|---|---|---|---|---|",
            ]
        )

        for lang_code, stats in sorted(langs.items()):
            lines.append(
                f"| `{lang_code}` | {stats['case_count']} | {stats['mean_rubric_score']:.1f} | "
                f"{stats['script_match_rate']:.1%} | {stats['mean_latency_seconds']:.2f}s |"
            )

        lines.extend(
            [
                "",
                "---",
                "",
                "## 3. Hardware & Reproducibility Metadata",
                f"- **GPU Device**: `{self.gpu_device or 'N/A'}`",
                f"- **Total VRAM**: `{self.total_vram_gb or 0.0:.2f} GiB`",
                f"- **Persistence Mode**: `{self.persistence_mode}`",
                f"- **Local Results Path**: `{self.exp_dir}`",
                f"- **Drive Mirror Path**: `{self.drive_exp_dir or 'N/A'}`",
                f"- **Python Version**: `{report['metadata']['python_version']}`",
                f"- **Random Seed**: `{self.random_seed}`",
                f"- **Max New Tokens**: `{self.max_new_tokens}`",
                f"- **Temperature / Top-p**: `{self.temperature} / {self.top_p}`",
                "",
                "---",
                "",
                "## 4. Methodological Notes",
                "- **Automated Deterministic Checks**: Keyword matching, script boundaries, "
                "length, and forbidden phrase detection.",
                "- **Human Review Flags**: Subjective pedagogy, subtle code-switching, and "
                "Socratic dialogues are flagged for qualitative review.",
                f"- **Benchmark Version**: `{BASELINE_VERSION}`.",
                "",
            ]
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return path
