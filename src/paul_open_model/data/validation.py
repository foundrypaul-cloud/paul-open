"""Validation and linting framework for PAUL Open Model Phase 3 training datasets.

Implements the Tri-Tier validation architecture:
- Tier 1: Hard validity constraints (syntax, schema, non-empty, token budget).
- Tier 2: Heuristic screening signals (Socratic probe, translation cleanliness, STEM structure).
- Tier 3: Human review metadata structure and tracking.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ============================================================================
# Tier 1 & 2 Constants and Whitelists
# ============================================================================

MAX_SINGLE_TURN_TOKENS = 350
MAX_PREAMBLE_WORDS_STEM = 25
MAX_SOCRATIC_TURN1_WORDS = 200

# Universal scientific acronyms and entities allowed in translation without penalty
SCIENTIFIC_ACRONYMS_WHITELIST = {
    "DNA",
    "RNA",
    "MRNA",
    "TRNA",
    "RRNA",
    "CDNA",
    "ATP",
    "ADP",
    "AMP",
    "NADP",
    "NADPH",
    "NADH",
    "FADH2",
    "PCR",
    "QPCR",
    "RT-PCR",
    "CRISPR",
    "CAS9",
    "PAM",
    "SGRNA",
    "CO2",
    "H2O",
    "O2",
    "N2",
    "CH4",
    "NH3",
    "H2SO4",
    "HCL",
    "NAOH",
    "C6H12O6",
    "SI",
    "PH",
    "KE",
    "PE",
    "EMF",
    "AC",
    "DC",
    "UV",
    "IR",
    "NMR",
    "MRI",
    "CT",
    "GFP",
    "ELISA",
    "NCERT",
    "CBSE",
    "ICSE",
    "IIT",
    "NEET",
    "AIIMS",
}

# Standard SI Units whitelist
SI_UNITS_WHITELIST = {
    "m",
    "cm",
    "mm",
    "um",
    "nm",
    "pm",
    "km",
    "kg",
    "g",
    "mg",
    "ug",
    "s",
    "ms",
    "us",
    "ns",
    "min",
    "h",
    "hr",
    "A",
    "mA",
    "uA",
    "K",
    "C",
    "mol",
    "mmol",
    "umol",
    "cd",
    "N",
    "kN",
    "J",
    "kJ",
    "MJ",
    "W",
    "kW",
    "MW",
    "Pa",
    "kPa",
    "MPa",
    "Hz",
    "kHz",
    "MHz",
    "GHz",
    "V",
    "mV",
    "kV",
    "ohm",
    "F",
    "uF",
    "nF",
    "pF",
    "T",
    "G",
    "Wb",
    "lx",
    "Bq",
    "Gy",
    "Sv",
    "m/s",
    "m/s^2",
    "m/s2",
    "km/h",
    "km/hr",
    "g/cm^3",
    "kg/m^3",
    "mol/L",
    "M",
    "mM",
    "uM",
    "J/K",
    "J/(mol*K)",
    "kJ/mol",
    "N*m",
    "N/m",
}

# Forbidden conversational meta-talk in translation outputs
TRANSLATION_META_TALK_PATTERNS = [
    r"^(here is|here's|sure|certainly|below is|let me translate|this translates to)\b",
    r"\b(depending on the desired nuance|here are a few ways to translate|formal translation:)\b",
    r"\b(transliteration|pronunciation guide|word-by-word|breakdown:)\b",
    r"\b(hope this helps|let me know if you need)\b",
]

# Premature answer disclosure phrases in Socratic Turn 1
SOCRATIC_PREMATURE_GIVEAWAYS = [
    "the correct answer is",
    "the formula is",
    "in conclusion,",
    "therefore, the answer is",
    "this is because",
    "the actual reason is that",
    "to explain why you are wrong",
    "as a matter of fact, the principle is",
]


def estimate_token_count(text: str) -> int:
    """Estimate token count from raw text (repository heuristic: 4 chars/token)."""
    clean_text = text.strip()
    if not clean_text:
        return 0
    return max(1, len(clean_text) // 4)


@dataclass
class ValidationResult:
    """Outcome of validating an SFT or DPO data entry across all three tiers."""

    id: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tier3_review: dict[str, Any] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "tier3_review": self.tier3_review,
            "stats": self.stats,
        }


# ============================================================================
# Tier 2 Specialized Linting / Screening Helpers
# ============================================================================


def validate_socratic_turn_structure(
    content: str, turn_index: int = 1
) -> tuple[list[str], dict[str, Any]]:
    """Screening check for Socratic inquiry structure."""
    warnings: list[str] = []
    stats: dict[str, Any] = {}

    words = re.findall(r"\b\w+\b", content)
    stats["word_count"] = len(words)

    if len(words) < 40:
        warnings.append(f"Socratic response word count ({len(words)}) is suspiciously low (< 40 words) — potentially underdeveloped.")

    if turn_index == 1 and len(words) > MAX_SOCRATIC_TURN1_WORDS:
        msg = (
            f"Socratic Turn 1 word count ({len(words)}) exceeds recommended max "
            f"({MAX_SOCRATIC_TURN1_WORDS}) — potential lecture dumping."
        )
        warnings.append(msg)

    content_lower = content.lower()
    for phrase in SOCRATIC_PREMATURE_GIVEAWAYS:
        if phrase in content_lower:
            warnings.append(f"Potential premature answer disclosure detected: '{phrase}'")

    paragraphs = [p.strip() for p in content.strip().split("\n") if p.strip()]
    if not paragraphs:
        warnings.append("Socratic response content is empty.")
        return warnings, stats

    last_paragraph = paragraphs[-1]
    cleaned_last_para = re.sub(r"[\*_>`\s]+$", "", last_paragraph)

    if not cleaned_last_para.endswith("?"):
        msg = "Socratic turn does not terminate with a student-directed question (missing '?')."
        warnings.append(msg)

    # Strip quoted material before counting probing questions
    unquoted_last_para = re.sub(r"\'[^\']*\'|\"[^\"]*\"", "", last_paragraph)
    question_count_in_final = len(re.findall(r"\?", unquoted_last_para))
    stats["final_paragraph_question_count"] = question_count_in_final
    if question_count_in_final > 1:
        msg = (
            f"Multiple questions ({question_count_in_final}) detected in final paragraph — "
            "risk of multi-question firing."
        )
        warnings.append(msg)

    return warnings, stats


def validate_clean_translation_response(
    content: str, target_language: str
) -> tuple[list[str], dict[str, Any]]:
    """Screening check for clean, direct translation output."""
    warnings: list[str] = []
    stats: dict[str, Any] = {}

    content_clean = content.strip()
    for pat in TRANSLATION_META_TALK_PATTERNS:
        if re.search(pat, content_clean, re.IGNORECASE):
            warnings.append(f"Translation contains conversational meta-talk matching: '{pat}'")

    text_without_formulas = re.sub(r"\$\$.*?\$\$|\$.*?\$", " ", content_clean, flags=re.DOTALL)
    words = re.findall(r"[^\s\d\.,;:!\?\"'()\[\]{}]+", text_without_formulas)

    total_alpha_chars = 0
    target_script_chars = 0
    latin_chars = 0

    script_map = {
        "hi": "DEVANAGARI",
        "mr": "DEVANAGARI",
        "bn": "BENGALI",
        "ta": "TAMIL",
        "te": "TELUGU",
        "gu": "GUJARATI",
        "kn": "KANNADA",
        "ml": "MALAYALAM",
        "pa": "GURMUKHI",
        "or": "ORIYA",
    }

    t_lang = target_language.split("-")[-1].lower()
    expected_script = script_map.get(t_lang)

    for word in words:
        word_upper = word.upper()
        if word_upper in SCIENTIFIC_ACRONYMS_WHITELIST or word in SI_UNITS_WHITELIST:
            continue

        for ch in word:
            if ch.isalpha():
                total_alpha_chars += 1
                try:
                    name = unicodedata.name(ch)
                    if expected_script and expected_script in name:
                        target_script_chars += 1
                    elif "LATIN" in name:
                        latin_chars += 1
                except ValueError:
                    pass

    if total_alpha_chars > 0 and expected_script:
        script_purity = target_script_chars / total_alpha_chars
        latin_ratio = latin_chars / total_alpha_chars
        stats["script_purity"] = round(script_purity, 3)
        stats["latin_ratio"] = round(latin_ratio, 3)

        if script_purity < 0.60 and latin_ratio > 0.30:
            msg = (
                f"Low target script purity ({script_purity:.1%}) with high Latin ratio "
                f"({latin_ratio:.1%}) for '{target_language}' — possible English commentary."
            )
            warnings.append(msg)

    return warnings, stats


def validate_stem_numerical_response(content: str) -> tuple[list[str], dict[str, Any]]:
    """Screening check for concise, structured STEM numerical problem solving."""
    warnings: list[str] = []
    stats: dict[str, Any] = {}

    content_lower = content.lower()
    has_given = any(k in content_lower for k in ["given", "known", "givens", "data:"])
    has_target = any(k in content_lower for k in ["target", "find", "calculate", "goal", "unknown"])
    stats["has_given_or_target"] = has_given or has_target

    if not (has_given or has_target):
        warnings.append("Missing explicit 'Given' or 'Target variables' setup block.")

    first_eq_pos = content.find("$")
    if first_eq_pos != -1:
        preamble_text = content[:first_eq_pos]
        preamble_words = re.findall(r"\b\w+\b", preamble_text)
        stats["preamble_words_before_eq"] = len(preamble_words)
        if len(preamble_words) > MAX_PREAMBLE_WORDS_STEM:
            msg = (
                f"Preamble before equation is verbose ({len(preamble_words)} > "
                f"{MAX_PREAMBLE_WORDS_STEM} words) — risk of token exhaustion."
            )
            warnings.append(msg)
    else:
        first_num_match = re.search(r"\d", content)
        if first_num_match:
            preamble_words = re.findall(r"\b\w+\b", content[: first_num_match.start()])
            stats["preamble_words_before_eq"] = len(preamble_words)
            if len(preamble_words) > MAX_PREAMBLE_WORDS_STEM:
                msg = (
                    f"Preamble before calculation is verbose ({len(preamble_words)} > "
                    f"{MAX_PREAMBLE_WORDS_STEM} words) — risk of token exhaustion."
                )
                warnings.append(msg)
        else:
            stats["preamble_words_before_eq"] = 0
            warnings.append("No mathematical equation ($ or $$) found in numerical response.")

    has_final_box = any(
        k in content for k in ["\\mathbf{", "\\boxed{", "**Final Answer", "**Answer:"]
    )
    stats["has_highlighted_final_answer"] = has_final_box
    if not has_final_box:
        warnings.append("No bolded or boxed final answer block detected.")

    return warnings, stats


# ============================================================================
# Main SFT and DPO Validators (Tier 1 + Tier 2 + Tier 3)
# ============================================================================


def validate_sft_example(
    data: dict[str, Any],
    schema_path: Path | None = None,
    max_tokens_per_turn: int = MAX_SINGLE_TURN_TOKENS,
) -> ValidationResult:
    """Validate a single SFT training example across Tiers 1, 2, and 3."""
    example_id = str(data.get("id", "UNKNOWN_ID"))
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, Any] = {}

    if not isinstance(data, dict):
        return ValidationResult(
            id=example_id, is_valid=False, errors=["Data entry is not a JSON object."]
        )

    required_fields = ["id", "track", "domain", "language", "messages", "metadata"]
    for field_name in required_fields:
        if field_name not in data:
            errors.append(f"Missing required field: '{field_name}'")

    if "id" in data and not re.match(r"^paul_sft_[a-z0-9_]+$", str(data["id"])):
        errors.append(f"Invalid ID format '{data['id']}': must match pattern ^paul_sft_[a-z0-9_]+$")

    valid_tracks = {
        "socratic_tutoring",
        "concise_stem_calc",
        "clean_translation",
        "indic_pedagogical_tone",
        "preservation_core",
    }
    if "track" in data and data["track"] not in valid_tracks:
        errors.append(f"Invalid track '{data['track']}': must be one of {sorted(valid_tracks)}")

    messages = data.get("messages")
    if not isinstance(messages, list) or len(messages) < 2:
        errors.append("'messages' must be a list with at least 2 turn objects.")
    else:
        total_tokens = 0
        for idx, turn in enumerate(messages):
            if not isinstance(turn, dict):
                errors.append(f"Turn {idx} is not a valid JSON object.")
                continue
            role = str(turn.get("role", "unknown"))
            if role not in ["system", "user", "assistant"]:
                errors.append(f"Turn {idx} has invalid role: '{role}'.")
            content = str(turn.get("content", "")).strip()
            if not content:
                errors.append(f"Turn {idx} has empty or missing 'content'.")
            else:
                turn_tokens = estimate_token_count(content)
                total_tokens += turn_tokens
                if turn_tokens > max_tokens_per_turn:
                    errors.append(
                        f"Turn {idx} ({role}) exceeds max token budget "
                        f"({turn_tokens} > {max_tokens_per_turn} tokens)."
                    )
        stats["approx_token_count"] = total_tokens

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("'metadata' must be a JSON object.")
    else:
        for meta_field in ["difficulty", "human_verified", "benchmark_leakage_checked"]:
            if meta_field not in metadata:
                errors.append(f"Missing required metadata field: '{meta_field}'")

    is_valid = len(errors) == 0

    if is_valid and isinstance(messages, list):
        track = data.get("track")
        language = data.get("language", "en")

        assistant_turns = [m for m in messages if m.get("role") == "assistant"]
        if assistant_turns:
            final_turn_content = str(assistant_turns[-1].get("content", ""))

            if track == "socratic_tutoring":
                soc_warns, soc_stats = validate_socratic_turn_structure(
                    final_turn_content, turn_index=len(assistant_turns)
                )
                warnings.extend(soc_warns)
                stats.update(soc_stats)

            elif track == "clean_translation":
                trans_warns, trans_stats = validate_clean_translation_response(
                    final_turn_content, target_language=language
                )
                warnings.extend(trans_warns)
                stats.update(trans_stats)

            elif track == "concise_stem_calc":
                stem_warns, stem_stats = validate_stem_numerical_response(final_turn_content)
                warnings.extend(stem_warns)
                stats.update(stem_stats)

    tier3_info: dict[str, Any] = {}
    if isinstance(metadata, dict):
        tier3_info = {
            "reviewer_id": metadata.get("reviewer_id", "UNASSIGNED"),
            "review_status": metadata.get("review_status", "pending"),
            "review_notes": metadata.get("review_notes", ""),
            "review_timestamp": metadata.get("review_timestamp", None),
            "approved": metadata.get("approved", False),
            "human_verified": metadata.get("human_verified", False),
        }

    return ValidationResult(
        id=example_id,
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        tier3_review=tier3_info,
        stats=stats,
    )


def validate_dpo_pair(
    data: dict[str, Any],
    schema_path: Path | None = None,
    max_tokens_per_turn: int = MAX_SINGLE_TURN_TOKENS,
) -> ValidationResult:
    """Validate a single DPO preference pair across Tiers 1, 2, and 3."""
    pair_id = str(data.get("id", "UNKNOWN_ID"))
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, Any] = {}

    if not isinstance(data, dict):
        return ValidationResult(
            id=pair_id, is_valid=False, errors=["Data entry is not a JSON object."]
        )

    required_fields = [
        "id",
        "track",
        "domain",
        "language",
        "prompt",
        "chosen",
        "rejected",
        "rejection_reason",
        "metadata",
    ]
    for field_name in required_fields:
        if field_name not in data:
            errors.append(f"Missing required field: '{field_name}'")

    if "id" in data and not re.match(r"^paul_dpo_[a-z0-9_]+$", str(data["id"])):
        errors.append(f"Invalid ID format '{data['id']}': must match pattern ^paul_dpo_[a-z0-9_]+$")

    valid_tracks = {
        "socratic_tutoring",
        "concise_stem_calc",
        "clean_translation",
        "indic_pedagogical_tone",
    }
    if "track" in data and data["track"] not in valid_tracks:
        errors.append(f"Invalid track '{data['track']}': must be one of {sorted(valid_tracks)}")

    for text_field in ["prompt", "chosen", "rejected"]:
        if text_field in data:
            val = str(data[text_field]).strip()
            if not isinstance(data[text_field], str) or len(val) < 5:
                errors.append(f"Field '{text_field}' must be a non-empty string (>= 5 chars).")
            else:
                field_tokens = estimate_token_count(val)
                if field_tokens > max_tokens_per_turn:
                    errors.append(
                        f"Field '{text_field}' exceeds max token budget "
                        f"({field_tokens} > {max_tokens_per_turn} tokens)."
                    )

    if (
        "chosen" in data
        and "rejected" in data
        and str(data["chosen"]).strip() == str(data["rejected"]).strip()
    ):
        errors.append("'chosen' and 'rejected' completions cannot be identical.")

    valid_reasons = {
        "lecture_dumping_in_socratic_mode",
        "preamble_verbosity_truncation",
        "conversational_meta_talk_in_translation",
        "unnatural_or_archaic_indic_register",
        "multi_question_firing",
        "missing_units_or_incomplete_calculation",
        "unsolicited_transliteration",
    }
    if "rejection_reason" in data and data["rejection_reason"] not in valid_reasons:
        errors.append(f"Invalid rejection_reason '{data['rejection_reason']}'.")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("'metadata' must be a JSON object.")
    else:
        for meta_field in ["difficulty", "human_verified", "benchmark_leakage_checked"]:
            if meta_field not in metadata:
                errors.append(f"Missing required metadata field: '{meta_field}'")

    is_valid = len(errors) == 0

    if is_valid:
        track = data.get("track")
        chosen = str(data.get("chosen", ""))
        rejected = str(data.get("rejected", ""))

        stats["chosen_words"] = len(re.findall(r"\b\w+\b", chosen))
        stats["rejected_words"] = len(re.findall(r"\b\w+\b", rejected))

        if track == "socratic_tutoring":
            soc_warns, _ = validate_socratic_turn_structure(chosen, turn_index=1)
            warnings.extend(soc_warns)
            
            # Enforce substantive pedagogical scaffolding for chosen responses
            chosen_words = stats["chosen_words"]
            if chosen_words < 20 or (len(re.split(r"[.!?]+", chosen)) <= 2 and "?" in chosen):
                errors.append("DPO chosen response lacks substantive pedagogical scaffolding or is question-only.")
        elif track == "clean_translation":
            trans_warns, _ = validate_clean_translation_response(
                chosen, target_language=str(data.get("language", "en"))
            )
            warnings.extend(trans_warns)
        elif track == "concise_stem_calc":
            stem_warns, _ = validate_stem_numerical_response(chosen)
            warnings.extend(stem_warns)

    tier3_info: dict[str, Any] = {}
    if isinstance(metadata, dict):
        tier3_info = {
            "reviewer_id": metadata.get("reviewer_id", "UNASSIGNED"),
            "review_status": metadata.get("review_status", "pending"),
            "review_notes": metadata.get("review_notes", ""),
            "review_timestamp": metadata.get("review_timestamp", None),
            "approved": metadata.get("approved", False),
            "human_verified": metadata.get("human_verified", False),
        }

    return ValidationResult(
        id=pair_id,
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        tier3_review=tier3_info,
        stats=stats,
    )


def validate_dataset_file(
    filepath: Path | str,
    dataset_type: str = "sft",
    max_tokens_per_turn: int = MAX_SINGLE_TURN_TOKENS,
) -> dict[str, Any]:
    """Validate an entire JSON or JSONL dataset file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    items: list[dict[str, Any]] = []
    content = path.read_text(encoding="utf-8")

    if path.suffix == ".jsonl":
        for line_num, line in enumerate(content.splitlines(), start=1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                items.append(json.loads(line_str))
            except json.JSONDecodeError as e:
                return {
                    "file": str(path),
                    "is_valid": False,
                    "total_records": 0,
                    "valid_records": 0,
                    "invalid_records": 1,
                    "errors": [f"JSONL parse error on line {line_num}: {e}"],
                    "warnings": [],
                    "results": [],
                }
    else:
        try:
            loaded = json.loads(content)
            items = loaded if isinstance(loaded, list) else [loaded]
        except json.JSONDecodeError as e:
            return {
                "file": str(path),
                "is_valid": False,
                "total_records": 0,
                "valid_records": 0,
                "invalid_records": 1,
                "errors": [f"JSON parse error: {e}"],
                "warnings": [],
                "results": [],
            }

    results: list[ValidationResult] = []
    for item in items:
        res = (
            validate_dpo_pair(item, max_tokens_per_turn=max_tokens_per_turn)
            if dataset_type == "dpo"
            else validate_sft_example(item, max_tokens_per_turn=max_tokens_per_turn)
        )
        results.append(res)

    total = len(results)
    valid_count = sum(1 for r in results if r.is_valid)
    invalid_count = total - valid_count
    all_warnings = [w for r in results for w in r.warnings]
    all_errors = [e for r in results for e in r.errors]

    approved_count = sum(1 for r in results if r.tier3_review.get("approved", False))
    pending_count = sum(1 for r in results if r.tier3_review.get("review_status") == "pending")

    return {
        "file": str(path),
        "dataset_type": dataset_type,
        "max_tokens_per_turn": max_tokens_per_turn,
        "is_valid": invalid_count == 0,
        "total_records": total,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "total_warnings": len(all_warnings),
        "tier3_approved_records": approved_count,
        "tier3_pending_records": pending_count,
        "errors": all_errors,
        "warnings": all_warnings,
        "results": [r.to_dict() for r in results],
    }
