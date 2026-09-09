"""Google Forms packet construction for PAUL Open human evaluation.

This module is deliberately provider-bound only at the specification layer.
It converts a blinded H1 public variant into small, cohort-consistent form
packets suitable for Google Forms. It never consumes the H1 private A/B map and
therefore cannot reveal checkpoint identities.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

FORM_PACKET_VERSION = "1.1"
DEFAULT_MAX_COMPARISONS = 3
DEFAULT_CHOICES = (
    "Response A is better",
    "Response B is better",
    "They are about equally good",
    "Neither response is good",
    "I'm not sure / I can't judge this",
)
_ALLOWED_ENVIRONMENTS = {"sandbox", "development", "sealed_assurance"}
_PRIVATE_KEYS = {
    "case_id",
    "response_a_source",
    "response_b_source",
    "sources",
    "seed",
    "fingerprint",
    "left_label",
    "right_label",
}


class HumanEvalFormBuildError(ValueError):
    """Raised when a reviewer-facing form packet cannot be built safely."""


@dataclass(frozen=True)
class GoogleFormPacketBundle:
    """Reviewer-facing Google Forms packets and a non-secret routing manifest."""

    manifest: dict[str, Any]
    packets: tuple[dict[str, Any], ...]


def _digest(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise HumanEvalFormBuildError(f"{field} must be text")
    cleaned = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not cleaned:
        raise HumanEvalFormBuildError(f"{field} cannot be empty")
    return cleaned


def _reject_private_keys(value: Any, *, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in _PRIVATE_KEYS:
                raise HumanEvalFormBuildError(
                    f"private H1 field {key!r} is not allowed in Google Forms input ({path})"
                )
            _reject_private_keys(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_private_keys(child, path=f"{path}[{index}]")


def _validated_comparisons(variant: dict[str, Any]) -> list[dict[str, str]]:
    comparisons = variant.get("comparisons")
    if not isinstance(comparisons, list) or not comparisons:
        raise HumanEvalFormBuildError("variant comparisons must be a non-empty array")

    required = {
        "comparison_id",
        "domain",
        "language",
        "reviewer_cohort",
        "prompt",
        "response_a",
        "response_b",
    }
    validated: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(comparisons, start=1):
        if not isinstance(raw, dict):
            raise HumanEvalFormBuildError(f"comparison {index} must be an object")
        missing = sorted(required - raw.keys())
        if missing:
            raise HumanEvalFormBuildError(
                f"comparison {index} missing fields: {', '.join(missing)}"
            )
        row = {
            field: _require_text(raw[field], field=f"comparison {index}.{field}")
            for field in sorted(required)
        }
        if row["comparison_id"] in seen_ids:
            raise HumanEvalFormBuildError(
                f"duplicate comparison_id {row['comparison_id']!r} in variant"
            )
        seen_ids.add(row["comparison_id"])
        if row["response_a"] == row["response_b"]:
            raise HumanEvalFormBuildError(
                f"comparison {row['comparison_id']!r} contains identical responses"
            )
        validated.append(row)
    return validated


def _intro_text(*, reviewer_cohort: str) -> str:
    base = (
        "Read each question and the two responses. Choose the response you would rather "
        "receive based on accuracy, clarity, usefulness and naturalness. If they are equally "
        "good, both poor, or you are unsure, you can say so."
    )
    if reviewer_cohort == "bilingual":
        return (
            base
            + " Standard scientific terms, formulas, units and abbreviations may stay in their "
            "familiar English or standard notation when that is clearer or more accurate."
        )
    return base


def _reviewer_context_question(reviewer_cohort: str) -> dict[str, Any]:
    """Return one low-friction reviewer-context question for the cohort."""

    if reviewer_cohort == "general_user":
        return {
            "enabled": True,
            "title": "Optional: Which best describes you?",
            "choices": [
                "Student",
                "Teacher / educator",
                "Researcher / scientist / engineer",
                "Other working professional",
                "General user",
                "Prefer not to say",
            ],
            "required": False,
        }
    if reviewer_cohort == "educator":
        return {
            "enabled": True,
            "title": "Optional: Which best describes your teaching experience?",
            "choices": [
                "I currently teach",
                "I have taught before",
                "I work in education but not as a classroom teacher",
                "I am training to teach",
                "Other",
                "Prefer not to say",
            ],
            "required": False,
        }
    if reviewer_cohort == "bilingual":
        return {
            "enabled": True,
            "title": "How comfortable are you reading and writing this language?",
            "choices": [
                "Native / near-native",
                "Fluent",
                "Conversational",
                "Limited",
                "I cannot confidently judge this language",
                "Prefer not to say",
            ],
            "required": True,
        }
    if reviewer_cohort in {"stem_capable", "domain_expert"}:
        return {
            "enabled": True,
            "title": "How comfortable are you judging the topics in this form?",
            "choices": [
                "Strong background",
                "Some background",
                "General familiarity",
                "I cannot confidently judge these topics",
                "Prefer not to say",
            ],
            "required": True,
        }
    raise HumanEvalFormBuildError(f"unsupported reviewer cohort {reviewer_cohort!r}")


def _chunked(values: list[dict[str, str]], size: int) -> list[list[dict[str, str]]]:
    return [values[start : start + size] for start in range(0, len(values), size)]


def build_google_form_packets(
    public_variant: dict[str, Any],
    *,
    max_comparisons: int = DEFAULT_MAX_COMPARISONS,
    environment: str = "sandbox",
    auto_close_after_submissions: int | None = None,
) -> GoogleFormPacketBundle:
    """Convert one H1 blinded variant into short Google Forms packets.

    Packets are grouped by reviewer cohort and language before chunking. This
    avoids long routing questionnaires and reduces cognitive switching. The
    function never accepts or emits model/checkpoint identities.
    """

    if not isinstance(public_variant, dict):
        raise HumanEvalFormBuildError("public_variant must be an object")
    _reject_private_keys(public_variant)

    if environment not in _ALLOWED_ENVIRONMENTS:
        expected = sorted(_ALLOWED_ENVIRONMENTS)
        raise HumanEvalFormBuildError(
            f"unsupported environment {environment!r}; expected one of {expected}"
        )
    if not isinstance(max_comparisons, int) or not 1 <= max_comparisons <= 4:
        raise HumanEvalFormBuildError("max_comparisons must be an integer from 1 to 4")
    if auto_close_after_submissions is not None:
        if not isinstance(auto_close_after_submissions, int) or auto_close_after_submissions < 1:
            raise HumanEvalFormBuildError(
                "auto_close_after_submissions must be a positive integer or null"
            )
        if environment != "sandbox":
            raise HumanEvalFormBuildError(
                "automatic submission-count closing is sandbox-only; "
                "research closing is analysis-driven"
            )

    protocol_version = _require_text(
        public_variant.get("protocol_version"), field="protocol_version"
    )
    batch_id = _require_text(public_variant.get("batch_id"), field="batch_id")
    variant_id = _require_text(public_variant.get("variant_id"), field="variant_id")
    partition = _require_text(public_variant.get("partition"), field="partition")
    comparisons = _validated_comparisons(public_variant)

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for comparison in comparisons:
        key = (comparison["reviewer_cohort"], comparison["language"])
        grouped.setdefault(key, []).append(comparison)

    packets: list[dict[str, Any]] = []
    for reviewer_cohort, language in sorted(grouped):
        group = grouped[(reviewer_cohort, language)]
        for chunk_index, chunk in enumerate(_chunked(group, max_comparisons), start=1):
            packet_id = "HEF1-" + _digest(
                FORM_PACKET_VERSION,
                batch_id,
                variant_id,
                reviewer_cohort,
                language,
                str(chunk_index),
            )[:12].upper()
            count = len(chunk)
            packet_comparisons: list[dict[str, Any]] = []
            for ordinal, comparison in enumerate(chunk, start=1):
                packet_comparisons.append(
                    {
                        "ordinal": ordinal,
                        "comparison_id": comparison["comparison_id"],
                        "display_title": f"Comparison {ordinal} of {count}",
                        "prompt": comparison["prompt"],
                        "response_a": comparison["response_a"],
                        "response_b": comparison["response_b"],
                        "question": "Which response would you rather receive?",
                        "choices": list(DEFAULT_CHOICES),
                        "required": True,
                        "domain": comparison["domain"],
                    }
                )

            packets.append(
                {
                    "form_packet_version": FORM_PACKET_VERSION,
                    "protocol_version": protocol_version,
                    "environment": environment,
                    "packet_id": packet_id,
                    "batch_id": batch_id,
                    "variant_id": variant_id,
                    "partition": partition,
                    "reviewer_cohort": reviewer_cohort,
                    "language": language,
                    "title": "Help us compare AI responses",
                    "description": _intro_text(reviewer_cohort=reviewer_cohort),
                    "settings": {
                        "collect_email": False,
                        "allow_response_edits": False,
                        "limit_one_response_per_user": False,
                        "progress_bar": True,
                        "publish_response_summary": False,
                        "show_submit_another_response_link": False,
                        "shuffle_questions": False,
                        "accepting_responses": True,
                    },
                    "comparisons": packet_comparisons,
                    "reviewer_context": _reviewer_context_question(reviewer_cohort),
                    "optional_comment": {
                        "enabled": True,
                        "title": "Optional: Anything else you want to tell us?",
                        "required": False,
                    },
                    "confirmation_message": "Thank you — your response has been recorded.",
                    "sandbox_auto_close_after_submissions": auto_close_after_submissions,
                }
            )

    manifest = {
        "form_packet_version": FORM_PACKET_VERSION,
        "protocol_version": protocol_version,
        "environment": environment,
        "batch_id": batch_id,
        "variant_id": variant_id,
        "partition": partition,
        "source_comparison_count": len(comparisons),
        "packet_count": len(packets),
        "max_comparisons_per_packet": max_comparisons,
        "grouping": "reviewer_cohort_then_language",
        "reviewer_context_policy": "one_post_comparison_question_max",
        "model_identity_exposed": False,
        "private_mapping_consumed": False,
    }
    return GoogleFormPacketBundle(manifest=manifest, packets=tuple(packets))


def bundle_fingerprint(bundle: GoogleFormPacketBundle) -> str:
    """Return a stable fingerprint for an exact form-packet bundle."""

    payload = {"manifest": bundle.manifest, "packets": bundle.packets}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
