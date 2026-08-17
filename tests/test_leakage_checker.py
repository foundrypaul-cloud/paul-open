"""Unit tests for the Benchmark Leakage Checker and isolation framework."""

from paul_open_model.data.leakage import (
    BenchmarkLeakageChecker,
    compute_ngram_overlap,
    extract_numerical_parameters,
)


def test_numerical_parameter_extraction():
    """Test extracting compound numbers and units."""
    text = "A particle accelerates at 9.8 m/s^2 from rest for 10 s covering 490 meters at 25 °C."
    params = extract_numerical_parameters(text)
    assert "9.8_m/s^2" in params
    assert "10_s" in params
    assert "490_meters" in params
    assert "25_°c" in params


def test_ngram_overlap_calculation():
    """Test word-level n-gram overlap computation."""
    text1 = "the quick brown fox jumps over the lazy dog"
    text2 = "the quick brown fox leaps across the sleeping dog"
    overlap = compute_ngram_overlap(text1, text2, n=3)
    assert overlap > 0.0
    assert overlap < 1.0

    # Identical texts
    assert compute_ngram_overlap(text1, text1, n=3) == 1.0

    # Completely disjoint texts
    assert (
        compute_ngram_overlap("photosynthesis in plants", "quantum mechanical tunneling", n=3)
        == 0.0
    )


def test_leakage_checker_clean_prompt():
    """Test that a novel, unrelated scientific prompt passes as clean (no leakage)."""
    checker = BenchmarkLeakageChecker()
    novel_prompt = (
        "Explain the working mechanism of a four-stroke internal combustion engine, "
        "focusing on intake, compression, power, and exhaust with a p-V indicator diagram."
    )
    result = checker.check_text(
        novel_prompt, candidate_id="test_clean_001", domain="physics", language="en"
    )
    assert result.has_leakage is False
    assert result.highest_similarity < 0.35
    assert len(result.flags) == 0


def test_leakage_checker_exact_match():
    """Test that an exact copy of a benchmark prompt is flagged as critical leakage."""
    checker = BenchmarkLeakageChecker()
    sample_case = checker.cases[0]
    exact_prompt = sample_case["prompt"]

    result = checker.check_text(exact_prompt, candidate_id="test_leak_exact")
    assert result.has_leakage is True
    assert result.leakage_type == "exact_match"
    assert result.highest_similarity == 1.0
    assert result.matched_benchmark_id == sample_case["case_id"]


def test_leakage_checker_high_overlap():
    """Test that a heavily paraphrased copy of a benchmark prompt is flagged."""
    checker = BenchmarkLeakageChecker()
    sample_case = checker.cases[0]
    words = sample_case["prompt"].split()
    paraphrased = " ".join(words[: len(words) - 2]) + " please explain."

    result = checker.check_text(paraphrased, candidate_id="test_leak_overlap")
    assert result.has_leakage is True
    assert result.matched_benchmark_id == sample_case["case_id"]
