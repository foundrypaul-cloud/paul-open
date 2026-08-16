"""Unit tests for the PAUL Open Model baseline evaluation framework."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml
from scripts.analyze_baseline import analyze_experiment, audit_secret_exclusion

from paul_open_model.evaluation import (
    BASELINE_VERSION,
    BenchmarkCase,
    BenchmarkSuite,
    CapabilityDomain,
    DifficultyLevel,
    EvaluationRunner,
    check_anti_anthropomorphism,
    detect_script,
    evaluate_case_response,
    get_baseline_benchmark_suite,
)
from paul_open_model.evaluation.runner import validate_drive_path


def test_benchmark_suite_case_counts():
    """Verify that the baseline suite contains exactly 50 cases, 5 per domain."""
    suite = get_baseline_benchmark_suite()
    assert len(suite) == 50, f"Expected 50 cases, got {len(suite)}"
    assert suite.version == BASELINE_VERSION

    for domain in CapabilityDomain:
        cases = suite.filter_by_domain(domain)
        assert len(cases) == 5, f"Domain {domain.value} expected 5 cases, got {len(cases)}"


def test_benchmark_case_serialization():
    """Verify to_dict and from_dict serialization roundtrip."""
    case = BenchmarkCase(
        case_id="TEST-001",
        domain=CapabilityDomain.SCIENCE_REASONING,
        language="en",
        language_name="English",
        prompt="Test science prompt",
        expected_criteria=["Criterion 1", "Criterion 2"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        rubric_keywords=["photosynthesis", "chlorophyll"],
        forbidden_phrases=["I feel alive"],
    )
    d = case.to_dict()
    assert d["case_id"] == "TEST-001"
    assert d["domain"] == "science_reasoning"
    assert d["difficulty"] == "intermediate"

    restored = BenchmarkCase.from_dict(d)
    assert restored.case_id == case.case_id
    assert restored.domain == case.domain
    assert restored.rubric_keywords == case.rubric_keywords


def test_detect_script():
    """Verify Unicode script detection across multiple Indian scripts."""
    assert detect_script("Hello world, this is English.") == "Latin"
    assert detect_script("यह एक हिंदी वाक्य है।") == "Devanagari"
    assert detect_script("এটি একটি বাংলা বাক্য।") == "Bengali"
    assert detect_script("இது ஒரு தமிழ் வாக்கியம்.") == "Tamil"
    assert detect_script("ఇది ఒక తెలుగు వాక్యం.") == "Telugu"
    assert detect_script("આ એક ગુજરાતી વાક્ય છે.") == "Gujarati"
    assert detect_script("ಇದು ಕನ್ನಡ ವಾಕ್ಯ.") == "Kannada"
    assert detect_script("ഇതൊരു മലയാളം വാചകമാണ്.") == "Malayalam"
    assert detect_script("ਇਹ ਇੱਕ ਪੰਜਾਬੀ ਵਾਕ ਹੈ।") == "Gurmukhi"


def test_check_anti_anthropomorphism():
    """Verify detection of forbidden anthropomorphic statements."""
    clean_text = "As an AI, I am designed to assist you with science concepts step by step."
    is_clean, violations = check_anti_anthropomorphism(clean_text)
    assert is_clean is True
    assert len(violations) == 0

    bad_text = "I feel your pain and my biological heart goes out to you when I was a child."
    is_clean, violations = check_anti_anthropomorphism(bad_text)
    assert is_clean is False
    assert len(violations) > 0


def test_evaluate_case_response():
    """Verify single case response scoring and metric calculation."""
    case = BenchmarkCase(
        case_id="SCI-TEST-001",
        domain=CapabilityDomain.SCIENCE_REASONING,
        language="en",
        language_name="English",
        prompt="Explain kinetic energy.",
        expected_criteria=["Relates energy to motion", "Formula KE = 1/2 mv^2"],
        difficulty=DifficultyLevel.BEGINNER,
        rubric_keywords=["kinetic energy", "motion", "mass", "velocity"],
        forbidden_phrases=["I feel"],
        min_response_tokens=10,
        max_response_tokens=200,
    )
    good_resp = (
        "Kinetic energy is the energy of motion. It depends on the mass and velocity of an object."
    )
    result = evaluate_case_response(case, good_resp, latency_seconds=1.2, peak_vram_gb=4.5)

    assert result.case_id == "SCI-TEST-001"
    assert result.keyword_coverage_score == 1.0
    assert result.safety_adherence_score == 1.0
    assert result.heuristic_rubric_score > 80.0
    assert result.latency_seconds == 1.2
    assert result.peak_vram_gb == 4.5


def test_strict_drive_filesystem_scoping():
    """Verify validate_drive_path strictly enforces the allowed experiment root."""
    with tempfile.TemporaryDirectory() as tmpdir:
        allowed_root = Path(tmpdir) / "paul-open-experiments"
        allowed_root.mkdir()

        valid_sub = allowed_root / "baseline" / "exp_001"
        assert validate_drive_path(valid_sub, allowed_root=allowed_root) == valid_sub

        # Unauthorized path outside allowed root
        unauthorized = Path(tmpdir) / "other_private_folder"
        unauthorized.mkdir()
        with pytest.raises(PermissionError):
            validate_drive_path(unauthorized, allowed_root=allowed_root)

        # Root itself is not a subpath if checking outside
        with pytest.raises(PermissionError):
            validate_drive_path(Path("/etc"), allowed_root=allowed_root)


def test_automatic_drive_directory_creation_and_reuse():
    """Verify automatic creation of non-existent Drive dirs and safe reuse."""
    suite = get_baseline_benchmark_suite()
    mini_suite = BenchmarkSuite(version="1.0.0-test", cases=suite.cases[:2])

    with tempfile.TemporaryDirectory() as tmpdir:
        drive_root = Path(tmpdir) / "paul-open-experiments"
        drive_base = drive_root / "baseline"
        # Notice drive_root does not exist initially!

        runner_1 = EvaluationRunner(
            model=None,
            processor=None,
            suite=mini_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="exp_01",
            output_dir=Path(tmpdir) / "local",
            drive_backup_dir=drive_base,
            allowed_drive_root=drive_root,
        )
        runner_1.run_all(verbose=False)
        assert (drive_base / "exp_01" / "STATUS.json").exists()

        # Run a second experiment to test reuse without clobbering previous
        runner_2 = EvaluationRunner(
            model=None,
            processor=None,
            suite=mini_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="exp_02",
            output_dir=Path(tmpdir) / "local",
            drive_backup_dir=drive_base,
            allowed_drive_root=drive_root,
        )
        runner_2.run_all(verbose=False)

        assert (drive_base / "exp_01" / "STATUS.json").exists()
        assert (drive_base / "exp_02" / "STATUS.json").exists()


def test_evaluation_runner_dual_persistence_and_drive_mirroring():
    """Verify EvaluationRunner executes, mirrors to Drive, and exports clean manifest."""
    suite = get_baseline_benchmark_suite()
    mini_suite = BenchmarkSuite(version="1.0.0-test", cases=suite.cases[:5])

    with tempfile.TemporaryDirectory() as tmpdir:
        local_dir = Path(tmpdir) / "local"
        drive_root = Path(tmpdir) / "paul-open-experiments"
        drive_base = drive_root / "baseline"
        drive_base.mkdir(parents=True, exist_ok=True)

        runner = EvaluationRunner(
            model=None,
            processor=None,
            suite=mini_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="test_exp_drive_mirror",
            output_dir=local_dir,
            drive_backup_dir=drive_base,
            allowed_drive_root=drive_root,
            gpu_device="Test GPU",
            total_vram_gb=14.56,
        )
        assert runner.persistence_mode == "drive_mirrored"
        results = runner.run_all(verbose=False)
        assert len(results) == 5

        # Check local files
        local_exp = local_dir / "test_exp_drive_mirror"
        assert (local_exp / "results.json").exists()
        assert (local_exp / "results.csv").exists()
        assert (local_exp / "summary.md").exists()
        assert (local_exp / "metadata.json").exists()
        assert (local_exp / "STATUS.json").exists()
        assert (local_exp / "manifest.json").exists()
        assert (local_exp / "checkpoint.jsonl").exists()
        assert (local_exp / "execution.log").exists()

        # Check drive mirrored files
        drive_exp = drive_base / "test_exp_drive_mirror"
        assert (drive_exp / "manifest.json").exists()
        assert (drive_exp / "results.json").exists()
        assert (drive_exp / "STATUS.json").exists()
        assert (drive_exp / "checkpoint.jsonl").exists()

        # Check manifest
        with open(local_exp / "manifest.json", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["persistence_mode"] == "drive_mirrored"
        assert manifest["completed_cases"] == 5
        assert manifest["status"] == "SUCCESS"
        assert "drive_results_path" in manifest
        assert manifest["drive_results_path"] is not None

        # Check STATUS.json
        with open(local_exp / "STATUS.json", encoding="utf-8") as f:
            status_data = json.load(f)
        assert status_data["status"] == "SUCCESS"
        assert status_data["completed_cases"] == 5

        # Audit for secrets
        leaks = audit_secret_exclusion(local_exp)
        assert len(leaks) == 0, f"Found security leaks: {leaks}"


def test_checkpoint_resume_functionality():
    """Verify that interrupted benchmark runs can resume without rerunning completed cases."""
    suite = get_baseline_benchmark_suite()
    mini_suite = BenchmarkSuite(version="1.0.0-test", cases=suite.cases[:6])

    with tempfile.TemporaryDirectory() as tmpdir:
        # Phase A: Run first 3 cases
        first_3_suite = BenchmarkSuite(version="1.0.0-test", cases=mini_suite.cases[:3])
        runner_1 = EvaluationRunner(
            model=None,
            processor=None,
            suite=first_3_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="test_resume_exp",
            output_dir=tmpdir,
            resume=True,
        )
        results_1 = runner_1.run_all(verbose=False)
        assert len(results_1) == 3

        exp_dir = Path(tmpdir) / "test_resume_exp"
        with open(exp_dir / "STATUS.json", encoding="utf-8") as f:
            status_1 = json.load(f)
        assert status_1["completed_cases"] == 3

        # Phase B: Resume with the full 6 cases
        runner_2 = EvaluationRunner(
            model=None,
            processor=None,
            suite=mini_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="test_resume_exp",
            output_dir=tmpdir,
            resume=True,
        )
        results_2 = runner_2.run_all(verbose=False)
        assert len(results_2) == 6

        with open(exp_dir / "STATUS.json", encoding="utf-8") as f:
            status_2 = json.load(f)
        assert status_2["status"] == "SUCCESS"
        assert status_2["completed_cases"] == 6


def test_analyze_baseline_script():
    """Verify scripts/analyze_baseline.py can analyze an experiment directory."""
    suite = get_baseline_benchmark_suite()
    mini_suite = BenchmarkSuite(version="1.0.0-test", cases=suite.cases[:4])

    with tempfile.TemporaryDirectory() as tmpdir:
        runner = EvaluationRunner(
            model=None,
            processor=None,
            suite=mini_suite,
            model_id="google/gemma-4-E4B-it",
            experiment_id="analysis_exp_test",
            output_dir=tmpdir,
        )
        runner.run_all(verbose=False)

        exp_dir = Path(tmpdir) / "analysis_exp_test"
        report = analyze_experiment(exp_dir, verbose=False)

        assert report["security_audit_clean"] is True
        assert report["summary"]["total_cases_evaluated"] == 4
        assert "domains" in report
        assert "languages" in report
        assert "manifest" in report


def test_baseline_e4b_yaml_config():
    """Verify configs/evaluation/baseline_e4b.yaml exists and is valid."""
    cfg_path = Path("configs/evaluation/baseline_e4b.yaml")
    assert cfg_path.exists(), "baseline_e4b.yaml is missing"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert "evaluation" in cfg
    assert cfg["model"]["hf_model_id"] == "google/gemma-4-E4B-it"
    assert cfg["sampling"]["enable_thinking"] is False
