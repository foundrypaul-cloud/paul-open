"""Evaluation harnesses, benchmark suites, and metrics for PAUL Open Model."""

from paul_open_model.evaluation.benchmark import (
    BASELINE_VERSION,
    BenchmarkCase,
    BenchmarkSuite,
    CapabilityDomain,
    DifficultyLevel,
    get_baseline_benchmark_suite,
)
from paul_open_model.evaluation.metrics import (
    CaseEvaluationResult,
    check_anti_anthropomorphism,
    compute_domain_aggregates,
    compute_language_aggregates,
    compute_overall_summary,
    detect_script,
    evaluate_case_response,
)
from paul_open_model.evaluation.runner import EvaluationRunner

__all__ = [
    "BASELINE_VERSION",
    "BenchmarkCase",
    "BenchmarkSuite",
    "CapabilityDomain",
    "CaseEvaluationResult",
    "DifficultyLevel",
    "EvaluationRunner",
    "check_anti_anthropomorphism",
    "compute_domain_aggregates",
    "compute_language_aggregates",
    "compute_overall_summary",
    "detect_script",
    "evaluate_case_response",
    "get_baseline_benchmark_suite",
]
