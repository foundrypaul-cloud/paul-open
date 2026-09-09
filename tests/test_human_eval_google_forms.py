from __future__ import annotations

import json
from pathlib import Path

import pytest

from paul_open_model.evaluation.human_eval_forms import (
    DEFAULT_CHOICES,
    HumanEvalFormBuildError,
    build_google_form_packets,
    bundle_fingerprint,
)


def _comparison(
    index: int,
    *,
    cohort: str = "general_user",
    language: str = "en",
) -> dict[str, object]:
    return {
        "comparison_id": f"HEV1-{index:012d}",
        "domain": "synthetic_science",
        "language": language,
        "reviewer_cohort": cohort,
        "prompt": f"Explain synthetic concept number {index} to a learner.",
        "response_a": f"Synthetic response A number {index}.",
        "response_b": f"Synthetic response B number {index}.",
    }


def _variant(comparisons: list[dict[str, object]]) -> dict[str, object]:
    return {
        "protocol_version": "1.0",
        "batch_id": "HEB1-SYNTHETIC001",
        "partition": "development",
        "variant_id": "V01",
        "comparisons": comparisons,
    }


def test_default_packets_are_short_and_use_frozen_choices() -> None:
    bundle = build_google_form_packets(_variant([_comparison(i) for i in range(1, 8)]))

    assert bundle.manifest["packet_count"] == 3
    assert [len(packet["comparisons"]) for packet in bundle.packets] == [3, 3, 1]
    assert all(len(packet["comparisons"]) <= 3 for packet in bundle.packets)
    for packet in bundle.packets:
        for comparison in packet["comparisons"]:
            assert comparison["choices"] == list(DEFAULT_CHOICES)
            assert comparison["required"] is True


def test_forms_are_grouped_by_cohort_and_language_before_chunking() -> None:
    comparisons = [
        _comparison(1, cohort="general_user", language="en"),
        _comparison(2, cohort="general_user", language="en"),
        _comparison(3, cohort="bilingual", language="pa"),
        _comparison(4, cohort="bilingual", language="pa"),
        _comparison(5, cohort="bilingual", language="hi"),
    ]
    bundle = build_google_form_packets(_variant(comparisons))

    keys = [
        (packet["reviewer_cohort"], packet["language"], len(packet["comparisons"]))
        for packet in bundle.packets
    ]
    assert keys == [
        ("bilingual", "hi", 1),
        ("bilingual", "pa", 2),
        ("general_user", "en", 2),
    ]


def test_bilingual_instruction_preserves_technical_term_policy() -> None:
    bilingual = build_google_form_packets(
        _variant([_comparison(1, cohort="bilingual", language="pa")])
    ).packets[0]
    general = build_google_form_packets(_variant([_comparison(2)])).packets[0]

    assert "scientific terms, formulas, units and abbreviations may stay" in bilingual[
        "description"
    ]
    assert "scientific terms, formulas, units and abbreviations may stay" not in general[
        "description"
    ]


def test_packet_settings_are_low_friction_and_anonymous() -> None:
    packet = build_google_form_packets(_variant([_comparison(1)])).packets[0]
    settings = packet["settings"]

    assert settings == {
        "collect_email": False,
        "allow_response_edits": False,
        "limit_one_response_per_user": False,
        "progress_bar": True,
        "publish_response_summary": False,
        "show_submit_another_response_link": False,
        "shuffle_questions": False,
        "accepting_responses": True,
    }
    assert packet["optional_comment"]["required"] is False


def test_same_public_variant_produces_identical_bundle_and_fingerprint() -> None:
    variant = _variant([_comparison(i) for i in range(1, 5)])

    first = build_google_form_packets(variant)
    second = build_google_form_packets(json.loads(json.dumps(variant)))

    assert first == second
    assert bundle_fingerprint(first) == bundle_fingerprint(second)


def test_private_h1_fields_fail_closed() -> None:
    variant = _variant([_comparison(1)])
    variant["seed"] = "PRIVATE-SEED-DO-NOT-ACCEPT"

    with pytest.raises(HumanEvalFormBuildError, match="private H1 field"):
        build_google_form_packets(variant)


def test_identical_responses_fail_before_a_form_is_built() -> None:
    comparison = _comparison(1)
    comparison["response_b"] = comparison["response_a"]

    with pytest.raises(HumanEvalFormBuildError, match="identical responses"):
        build_google_form_packets(_variant([comparison]))


def test_submission_count_auto_close_is_sandbox_only() -> None:
    variant = _variant([_comparison(1)])

    with pytest.raises(HumanEvalFormBuildError, match="sandbox-only"):
        build_google_form_packets(
            variant,
            environment="development",
            auto_close_after_submissions=3,
        )

    sandbox = build_google_form_packets(
        variant,
        environment="sandbox",
        auto_close_after_submissions=3,
    )
    assert sandbox.packets[0]["sandbox_auto_close_after_submissions"] == 3


def test_four_comparisons_is_hard_cap() -> None:
    variant = _variant([_comparison(i) for i in range(1, 6)])

    with pytest.raises(HumanEvalFormBuildError, match="1 to 4"):
        build_google_form_packets(variant, max_comparisons=5)


def test_reviewer_facing_fields_do_not_display_internal_comparison_ids() -> None:
    packet = build_google_form_packets(_variant([_comparison(1), _comparison(2)])).packets[0]

    for comparison in packet["comparisons"]:
        internal_id = comparison["comparison_id"]
        visible = json.dumps(
            {
                "display_title": comparison["display_title"],
                "prompt": comparison["prompt"],
                "response_a": comparison["response_a"],
                "response_b": comparison["response_b"],
                "question": comparison["question"],
                "choices": comparison["choices"],
            }
        )
        assert internal_id not in visible


def test_apps_script_runtime_keeps_frozen_privacy_and_lifecycle_settings() -> None:
    source = Path("tools/google_forms/Code.gs").read_text(encoding="utf-8")

    required_fragments = [
        "FormApp.create(packet.title, false)",
        ".setCollectEmail(false)",
        ".setAllowResponseEdits(false)",
        ".setLimitOneResponsePerUser(false)",
        ".setPublishingSummary(false)",
        ".setShowLinkToRespondAgain(false)",
        ".setShuffleQuestions(false)",
        "ScriptApp.newTrigger('onPaulHumanEvalSubmit')",
        "normalizedResponseExists_",
        "response.getId()",
        "form.setPublished(true).setAcceptingResponses(true)",
    ]
    for fragment in required_fragments:
        assert fragment in source
    assert "setCollectEmail(true)" not in source
    assert "getRespondentEmail" not in source


def test_apps_script_manifest_requests_only_required_workspace_scopes() -> None:
    manifest = json.loads(Path("tools/google_forms/appsscript.json").read_text(encoding="utf-8"))

    assert manifest["timeZone"] == "Etc/UTC"
    assert set(manifest["oauthScopes"]) == {
        "https://www.googleapis.com/auth/forms",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/script.scriptapp",
    }
