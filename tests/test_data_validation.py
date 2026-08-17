"""Unit tests for Phase 3 training data validation and linting framework."""

from __future__ import annotations

import json
from pathlib import Path

from paul_open_model.data.validation import (
    validate_clean_translation_response,
    validate_dataset_file,
    validate_dpo_pair,
    validate_sft_example,
    validate_socratic_turn_structure,
    validate_stem_numerical_response,
)


def test_valid_sft_example():
    """Verify that a well-formed SFT example passes Tier 1 validation."""
    synthetic_sft = {
        "id": "paul_sft_test_optics_001",
        "track": "socratic_tutoring",
        "domain": "physics",
        "subdomain": "optics",
        "language": "en",
        "messages": [
            {
                "role": "user",
                "content": "Why does a pencil look bent when placed in a glass of water?",
            },
            {
                "role": "assistant",
                "content": (
                    "When light moves between air and water, its speed changes. "
                    "Imagine stepping into deep sand from pavement—what happens when one "
                    "foot slows down first?"
                ),
            },
        ],
        "metadata": {
            "difficulty": "basic",
            "target_grade": "middle_school",
            "human_verified": True,
            "benchmark_leakage_checked": True,
            "reviewer_id": "reviewer_01",
            "review_status": "approved",
            "approved": True,
        },
    }

    result = validate_sft_example(synthetic_sft, max_tokens_per_turn=350)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.tier3_review["approved"] is True
    assert result.tier3_review["reviewer_id"] == "reviewer_01"


def test_token_limit_enforcement_and_custom_override():
    """Test token budget enforcement: below 350 passes, at/above fails, custom override."""
    # Construct a turn with ~400 tokens (1600 characters)
    long_content = "This is a detailed physics explanation. " * 40
    long_sft = {
        "id": "paul_sft_test_length_001",
        "track": "preservation_core",
        "domain": "physics",
        "language": "en",
        "messages": [
            {"role": "user", "content": "Explain momentum in detail."},
            {"role": "assistant", "content": long_content},
        ],
        "metadata": {
            "difficulty": "advanced",
            "human_verified": True,
            "benchmark_leakage_checked": True,
        },
    }

    # 1. Default limit (350 tokens) -> Should fail Tier 1
    res_default = validate_sft_example(long_sft, max_tokens_per_turn=350)
    assert res_default.is_valid is False
    assert any("exceeds max token budget" in e for e in res_default.errors)
    assert any("Turn 1 (assistant)" in e for e in res_default.errors)

    # 2. Custom override (500 tokens) -> Should pass Tier 1
    res_custom = validate_sft_example(long_sft, max_tokens_per_turn=500)
    assert res_custom.is_valid is True
    assert len(res_custom.errors) == 0


def test_dpo_token_limit_enforcement():
    """Test token limit failure on DPO fields."""
    long_rejected = "Verbose lecture dumping text. " * 50
    dpo_data = {
        "id": "paul_dpo_test_len_001",
        "track": "socratic_tutoring",
        "domain": "physics",
        "language": "en",
        "prompt": "What is force?",
        "chosen": "Think about pushing a heavy cart. What causes it to accelerate?",
        "rejected": long_rejected,
        "rejection_reason": "lecture_dumping_in_socratic_mode",
        "metadata": {
            "difficulty": "basic",
            "human_verified": True,
            "benchmark_leakage_checked": True,
        },
    }

    # Default 350 limit fails on rejected field
    res_dpo = validate_dpo_pair(dpo_data, max_tokens_per_turn=350)
    assert res_dpo.is_valid is False
    assert any("Field 'rejected' exceeds max token budget" in e for e in res_dpo.errors)


def test_cli_max_tokens_override(tmp_path: Path):
    """Test CLI --max-tokens flag override on a temporary dataset file."""
    sample_sft = [
        {
            "id": "paul_sft_test_cli_001",
            "track": "preservation_core",
            "domain": "chemistry",
            "language": "en",
            "messages": [
                {"role": "user", "content": "What is an acid?"},
                {"role": "assistant", "content": "An acid donates protons in solution. " * 30},
            ],
            "metadata": {
                "difficulty": "basic",
                "human_verified": True,
                "benchmark_leakage_checked": True,
            },
        }
    ]
    test_file = tmp_path / "test_sft.json"
    test_file.write_text(json.dumps(sample_sft), encoding="utf-8")

    # Run with default 350 limit -> Should fail
    res_fail = validate_dataset_file(test_file, dataset_type="sft", max_tokens_per_turn=200)
    assert res_fail["is_valid"] is False

    # Run with relaxed 500 limit -> Should pass
    res_pass = validate_dataset_file(test_file, dataset_type="sft", max_tokens_per_turn=500)
    assert res_pass["is_valid"] is True


def test_invalid_sft_missing_fields():
    """Verify that missing required fields trigger Tier 1 errors."""
    invalid_sft = {
        "id": "paul_sft_bad_001",
        # missing track, domain, language, messages, metadata
    }
    result = validate_sft_example(invalid_sft)
    assert result.is_valid is False
    assert any("track" in e for e in result.errors)
    assert any("messages" in e for e in result.errors)


def test_invalid_sft_bad_id_and_role():
    """Verify that bad ID patterns and invalid message roles are rejected."""
    bad_sft = {
        "id": "INVALID-UPPERCASE-ID",
        "track": "socratic_tutoring",
        "domain": "biology",
        "language": "en",
        "messages": [
            {"role": "human", "content": "Hello"},  # 'human' is invalid role
            {"role": "assistant", "content": "Hi there."},
        ],
        "metadata": {
            "difficulty": "basic",
            "human_verified": False,
            "benchmark_leakage_checked": False,
        },
    }
    result = validate_sft_example(bad_sft)
    assert result.is_valid is False
    assert any("Invalid ID format" in e for e in result.errors)
    assert any("invalid role" in e for e in result.errors)


def test_socratic_structural_validator():
    """Test the Socratic structural validator on trailing questions vs quotes."""
    good_socratic = (
        "A student once asked: 'Does water stop freezing if we add salt?' "
        "Think about what happens to ice on roads in winter when salt is scattered over it. "
        "How do you think salt particles interfere with water molecules forming an ice lattice?"
    )
    warns, stats = validate_socratic_turn_structure(good_socratic, turn_index=1)
    assert len(warns) == 0
    assert stats["final_paragraph_question_count"] == 1

    no_question_socratic = (
        "Salt lowers the freezing point of water through freezing point depression. "
        "The formula is delta Tf = i * Kf * m. Therefore, the ice melts at lower temperatures."
    )
    warns_no_q, _ = validate_socratic_turn_structure(no_question_socratic, turn_index=1)
    assert any("does not terminate with a student-directed" in w for w in warns_no_q)
    assert any("premature answer disclosure" in w for w in warns_no_q)


def test_clean_translation_whitelist():
    """Test that translation validation respects scientific acronyms, formulas, and units."""
    clean_hindi_translation = (
        "माइटोकॉन्ड्रिया (Mitochondria) कोशिका के लिए ATP के रूप में ऊर्जा उत्पन्न करता है, "
        "जिसमें C6H12O6 और O2 का उपयोग करके CO2 और H2O बनता है।"
    )
    warns, stats = validate_clean_translation_response(
        clean_hindi_translation, target_language="hi"
    )
    assert len(warns) == 0
    assert stats["script_purity"] > 0.60

    wrapped_translation = (
        "Sure! Here is the translation into Hindi: "
        "माइटोकॉन्ड्रिया कोशिका का ऊर्जा घर है। "
        "Transliteration: Mitochondria koshika ka urja ghar hai. "
        "Hope this helps!"
    )
    warns_bad, _ = validate_clean_translation_response(wrapped_translation, target_language="hi")
    assert any("conversational meta-talk" in w for w in warns_bad)


def test_stem_numerical_validator():
    """Test structured STEM calculation screening."""
    good_stem_calc = (
        "### 1. Given & Target Variables\n"
        "- Mass ($m$) = $2\\text{ kg}$\n"
        "- Acceleration ($a$) = $5\\text{ m/s}^2$\n"
        "- Target: Force ($F$)\n\n"
        "### 2. Calculation\n"
        "$$F = m \\cdot a$$\n"
        "$$F = (2\\text{ kg})(5\\text{ m/s}^2) = \\mathbf{10\\text{ N}}$$\n\n"
        "**Final Answer:** Force = $\\mathbf{10\\text{ N}}$"
    )
    warns, stats = validate_stem_numerical_response(good_stem_calc)
    assert len(warns) == 0
    assert stats["has_given_or_target"] is True
    assert stats["has_highlighted_final_answer"] is True

    verbose_calc = (
        "Classical mechanics explores the behavior of macroscopic physical bodies subjected to "
        "forces. Isaac Newton established three foundational laws of motion that govern how "
        "particles interact in our universe. To solve this problem, we must carefully analyze "
        "how force relates to mass and rate of change of momentum. "
        "$$F = ma = (2)(5) = 10$$"
    )
    warns_verbose, _ = validate_stem_numerical_response(verbose_calc)
    assert any("Missing explicit 'Given'" in w for w in warns_verbose)
    assert any("verbose" in w for w in warns_verbose)
    assert any("No bolded or boxed final answer" in w for w in warns_verbose)


def test_valid_dpo_pair():
    """Verify that a well-formed DPO pair passes validation."""
    synthetic_dpo = {
        "id": "paul_dpo_test_calc_001",
        "track": "concise_stem_calc",
        "domain": "physics",
        "language": "en",
        "prompt": "Calculate the kinetic energy of a 2 kg object moving at 3 m/s.",
        "chosen": (
            "### Given: $m = 2\\text{ kg}, v = 3\\text{ m/s}$\n"
            "$$KE = \\frac{1}{2}mv^2 = \\frac{1}{2}(2)(3)^2 = \\mathbf{9\\text{ J}}$$\n"
            "**Final Answer:** $\\mathbf{9\\text{ J}}$"
        ),
        "rejected": (
            "Kinetic energy is the energy of motion. In physics, when an object moves with a "
            "velocity v and has mass m, it possesses energy. The formula was derived from "
            "work-energy principles. The answer is 9 J."
        ),
        "rejection_reason": "preamble_verbosity_truncation",
        "metadata": {
            "difficulty": "basic",
            "human_verified": True,
            "benchmark_leakage_checked": True,
            "review_status": "approved",
            "approved": True,
        },
    }
    res = validate_dpo_pair(synthetic_dpo)
    assert res.is_valid is True
    assert len(res.errors) == 0
    assert res.tier3_review["approved"] is True
