"""Tests for YAML configuration loading, notebook validity, and documentation."""

import json
from pathlib import Path

import yaml


def test_model_configs_exist_and_valid():
    """All model config files should exist and have required fields."""
    config_dir = Path("configs/models")
    expected = [
        "gemma4_26b_a4b_it.yaml",
        "gemma4_12b_it.yaml",
        "gemma4_31b_it.yaml",
        "gemma4_e4b_it.yaml",
        "gemma4_e2b_it.yaml",
    ]
    for name in expected:
        path = config_dir / name
        assert path.exists(), f"Missing model config: {name}"
        with open(path) as f:
            cfg = yaml.safe_load(f)
        assert "model" in cfg, f"{name}: missing 'model' key"
        assert "hf_model_id" in cfg["model"], f"{name}: missing 'hf_model_id'"
        assert cfg["model"]["hf_model_id"].startswith("google/gemma-4-"), (
            f"{name}: hf_model_id should start with 'google/gemma-4-'"
        )


def test_training_configs_exist_and_valid():
    """All training config files should exist and have valid structure."""
    config_dir = Path("configs/training")
    expected = ["sft_qlora.yaml", "sft_full.yaml", "dpo.yaml"]
    for name in expected:
        path = config_dir / name
        assert path.exists(), f"Missing training config: {name}"
        with open(path) as f:
            cfg = yaml.safe_load(f)
        assert "training" in cfg, f"{name}: missing 'training' key"


def test_data_configs_exist_and_valid():
    """All data pipeline configs should exist and have valid structure."""
    config_dir = Path("configs/data")
    expected = [
        "indic_languages.yaml",
        "translation.yaml",
        "science_education.yaml",
        "tutoring_empathy.yaml",
        "life_sciences.yaml",
        "scientific_research.yaml",
        "socratic_tutoring.yaml",
        "teacher_assistance.yaml",
        "multimodal_science.yaml",
    ]
    for name in expected:
        path = config_dir / name
        assert path.exists(), f"Missing data config: {name}"
        with open(path) as f:
            cfg = yaml.safe_load(f)
        assert "data" in cfg, f"{name}: missing 'data' key"
        assert "name" in cfg["data"], f"{name}: missing 'name' in data config"


def test_eval_configs_exist_and_valid():
    """All evaluation benchmark configs should exist and have valid structure."""
    config_dir = Path("configs/evaluation")
    expected = [
        "indicnlp_bench.yaml",
        "flores_translation.yaml",
        "mmlu_science.yaml",
        "science_reasoning.yaml",
        "life_sciences_bench.yaml",
        "socratic_tutoring_eval.yaml",
        "empathy_humancentered_eval.yaml",
    ]
    for name in expected:
        path = config_dir / name
        assert path.exists(), f"Missing eval config: {name}"
        with open(path) as f:
            cfg = yaml.safe_load(f)
        assert "evaluation" in cfg, f"{name}: missing 'evaluation' key"


def test_skills_and_dataset_registry_docs_exist():
    """SKILLS.md and DATASET_REGISTRY.md must exist."""
    assert Path("SKILLS.md").exists(), "SKILLS.md missing in root"
    assert Path("DATASET_REGISTRY.md").exists(), "DATASET_REGISTRY.md missing in root"
    assert Path("docs/SKILLS.md").exists(), "docs/SKILLS.md missing"
    assert Path("docs/DATASET_REGISTRY.md").exists(), "docs/DATASET_REGISTRY.md missing"


def test_colab_notebooks_valid_json():
    """Verify Colab notebooks are valid JSON and contain all required cells."""
    expected_notebooks = [
        "notebooks/01_colab_environment_setup.ipynb",
        "notebooks/02_first_model_validation_e4b.ipynb",
    ]
    for nb_rel in expected_notebooks:
        nb_path = Path(nb_rel)
        assert nb_path.exists(), f"Colab notebook missing: {nb_rel}"
        with open(nb_path, encoding="utf-8") as f:
            nb = json.load(f)
        assert "cells" in nb, f"{nb_rel} missing 'cells' key"
        assert len(nb["cells"]) >= 4, f"{nb_rel} should contain all setup/validation cells"
