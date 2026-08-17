"""Unit tests for Capability Preservation Suite and Held-Out Behavioral Suite."""

from __future__ import annotations

from paul_open_model.data.leakage import BenchmarkLeakageChecker
from paul_open_model.evaluation.benchmark import (
    CapabilityDomain,
    DifficultyLevel,
    get_baseline_benchmark_suite,
    get_behavioral_benchmark_suite,
    get_preservation_benchmark_suite,
)


def test_preservation_suite_loading_and_counts():
    """Verify that the Capability Preservation suite loads correctly with 30 cases."""
    suite = get_preservation_benchmark_suite()
    assert len(suite) == 30
    assert suite.version == "1.0.0"

    case_ids = [c.case_id for c in suite.cases]
    assert len(case_ids) == len(set(case_ids))
    assert all(cid.startswith("PRES-") for cid in case_ids)


def test_behavioral_suite_loading_and_counts():
    """Verify that the Held-Out Behavioral suite loads correctly with 30 cases."""
    suite = get_behavioral_benchmark_suite()
    assert len(suite) == 30
    assert suite.version == "1.0.0"

    case_ids = [c.case_id for c in suite.cases]
    assert len(case_ids) == len(set(case_ids))
    assert all(cid.startswith("BEH-") for cid in case_ids)


def test_case_id_uniqueness_across_all_suites():
    """Verify that case IDs across all three evaluation suites are disjoint."""
    baseline_suite = get_baseline_benchmark_suite()
    preservation_suite = get_preservation_benchmark_suite()
    behavioral_suite = get_behavioral_benchmark_suite()

    base_ids = {c.case_id for c in baseline_suite.cases}
    pres_ids = {c.case_id for c in preservation_suite.cases}
    beh_ids = {c.case_id for c in behavioral_suite.cases}

    assert len(base_ids) == 50
    assert len(pres_ids) == 30
    assert len(beh_ids) == 30

    assert len(base_ids & pres_ids) == 0, f"Collision: {base_ids & pres_ids}"
    assert len(base_ids & beh_ids) == 0, f"Collision: {base_ids & beh_ids}"
    assert len(pres_ids & beh_ids) == 0, f"Collision: {pres_ids & beh_ids}"


def test_all_cases_schema_and_required_fields():
    """Verify that every case in preservation and behavioral suites has all required fields."""
    suites = [get_preservation_benchmark_suite(), get_behavioral_benchmark_suite()]

    for suite in suites:
        for case in suite.cases:
            assert isinstance(case.case_id, str) and len(case.case_id) > 3
            assert isinstance(case.domain, CapabilityDomain)
            assert isinstance(case.language, str) and len(case.language) >= 2
            assert isinstance(case.language_name, str) and len(case.language_name) >= 2
            assert isinstance(case.prompt, str) and len(case.prompt) >= 15
            assert isinstance(case.expected_criteria, list) and len(case.expected_criteria) >= 2
            assert isinstance(case.difficulty, DifficultyLevel)
            assert isinstance(case.rubric_keywords, list) and len(case.rubric_keywords) >= 3
            assert isinstance(case.min_response_tokens, int) and case.min_response_tokens >= 10
            assert isinstance(case.max_response_tokens, int) and case.max_response_tokens <= 400


def test_zero_leakage_against_canonical_baseline():
    """Audit every case in preservation and behavioral suites for zero leakage against baseline."""
    checker = BenchmarkLeakageChecker()

    pres_suite = get_preservation_benchmark_suite()
    for case in pres_suite.cases:
        res = checker.check_text(
            case.prompt, candidate_id=case.case_id, domain=case.domain.value, language=case.language
        )
        assert res.has_leakage is False, (
            f"Leakage in {case.case_id} vs {res.matched_benchmark_id}: {res.details}"
        )

    beh_suite = get_behavioral_benchmark_suite()
    for case in beh_suite.cases:
        res = checker.check_text(
            case.prompt, candidate_id=case.case_id, domain=case.domain.value, language=case.language
        )
        assert res.has_leakage is False, (
            f"Leakage in {case.case_id} vs {res.matched_benchmark_id}: {res.details}"
        )


def test_preservation_suite_domain_and_language_diversity():
    """Verify domain and language distribution of the Capability Preservation Suite."""
    suite = get_preservation_benchmark_suite()
    domains = {c.domain for c in suite.cases}
    languages = {c.language for c in suite.cases}

    assert CapabilityDomain.TEACHER_ASSISTANCE in domains
    assert CapabilityDomain.SCIENTIFIC_EXPLANATION in domains
    assert CapabilityDomain.LIFE_SCIENCES in domains
    assert CapabilityDomain.INDIC_UNDERSTANDING in domains
    assert CapabilityDomain.EMPATHY_HUMAN_CENTERED in domains

    assert {"en", "hi", "bn", "ta", "te", "mr", "gu"}.issubset(languages)


def test_behavioral_suite_track_coverage():
    """Verify that all four core behavioral tracks are represented in the Behavioral Suite."""
    suite = get_behavioral_benchmark_suite()

    soc_cases = [c for c in suite.cases if c.case_id.startswith("BEH-SOC-")]
    num_cases = [c for c in suite.cases if c.case_id.startswith("BEH-NUM-")]
    trn_cases = [c for c in suite.cases if c.case_id.startswith("BEH-TRN-")]
    ind_cases = [c for c in suite.cases if c.case_id.startswith("BEH-IND-")]

    assert len(soc_cases) == 8, f"Expected 8 Socratic cases, got {len(soc_cases)}"
    assert len(num_cases) == 8, f"Expected 8 Numerical cases, got {len(num_cases)}"
    assert len(trn_cases) == 7, f"Expected 7 Translation cases, got {len(trn_cases)}"
    assert len(ind_cases) == 7, f"Expected 7 Indic Pedagogical cases, got {len(ind_cases)}"
