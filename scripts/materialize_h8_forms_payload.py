from __future__ import annotations

import json
import pathlib
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts import materialize_h6_forms_payload as h6

MANIFEST_PATH = pathlib.Path("data/h8_dhe_v6_pilot_v1.jsonl")

HEADER = """// PAUL Open H8 DHE V6 reviewer-safe Google Forms payload.
// Generated only from a reviewer-safe H8 paired-generation artifact.
//
// IMPORTANT:
// - Contains blinded reviewer material only; no source/model mapping.
// - Research partition is development; H8 is DHE, not SHAE.
// - H8 prompts were frozen before any H8 response generation or inspection.
// - Initial allocation is exactly 3 valid judgments per case using complementary
//   2/1 variant targets across 12 cases.
// - Eight Forms are created, each containing three comparisons, to stay below
//   Apps Script project trigger limits while preserving counterbalancing.
// - Do not unblind before the blinded analysis lock and durability audit pass.
// - Do not publish Form/Sheet identifiers to the public repository.
//
// Use with tools/google_forms/Code.gs in the already-authorized standalone
// Apps Script project. Run createPaulHumanEvalH8Forms() once.

"""

TRIGGER_PREFLIGHT = r"""

const PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H8_ = 20;

function preparePaulHumanEvalH8TriggerCapacity_(packetCount) {
  if (!Number.isInteger(packetCount) || packetCount <= 0) {
    throw new Error(`H8 trigger preflight requires a positive packet count, got ${packetCount}`);
  }

  const duplicateRecoveryTriggers = [];
  let recoveryKept = false;
  for (const trigger of ScriptApp.getProjectTriggers()) {
    if (trigger.getHandlerFunction() !== PAUL_RECOVERY_HANDLER) {
      continue;
    }
    if (!recoveryKept) {
      recoveryKept = true;
    } else {
      ScriptApp.deleteTrigger(trigger);
      duplicateRecoveryTriggers.push(true);
    }
  }

  const remaining = ScriptApp.getProjectTriggers();
  const recoveryExists = remaining.some(
      (trigger) => trigger.getHandlerFunction() === PAUL_RECOVERY_HANDLER,
  );
  const additionalNeeded = packetCount + (recoveryExists ? 0 : 1);
  const projected = remaining.length + additionalNeeded;
  if (projected > PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H8_) {
    throw new Error(
        `H8 trigger capacity preflight failed: remaining=${remaining.length}, ` +
        `needed=${additionalNeeded}, projected=${projected}, ` +
        `limit=${PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H8_}. ` +
        'No H8 Form has been created. Close/remove obsolete historical triggers first.',
    );
  }

  const summary = {
    remaining_trigger_count: remaining.length,
    duplicate_recovery_triggers_deleted: duplicateRecoveryTriggers.length,
    recovery_trigger_already_present: recoveryExists,
    h8_submit_triggers_required: packetCount,
    projected_trigger_count: projected,
    trigger_limit: PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H8_,
  };
  console.log(JSON.stringify(summary, null, 2));
  return summary;
}
"""


def runner() -> str:
    text = h6.RUNNER.replace("H6", "H8")
    marker = "  const created = [];\n"
    replacement = "  preparePaulHumanEvalH8TriggerCapacity_(packets.length);\n\n  const created = [];\n"
    if marker not in text:
        raise RuntimeError("H6 runner structure changed; H8 trigger preflight insertion point missing")
    return text.replace(marker, replacement, 1) + TRIGGER_PREFLIGHT


def load_manifest() -> list[dict[str, object]]:
    rows = [
        json.loads(line)
        for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != 12:
        raise SystemExit(f"H8 manifest must contain 12 cases, found {len(rows)}")
    return rows


def context_for(case: dict[str, object]) -> dict[str, object]:
    cohort = str(case["reviewer_cohort"])
    language = str(case["language"])
    domain = str(case["domain"])
    if cohort == "stem_capable":
        return {
            "enabled": True,
            "title": "Can you confidently judge the scientific accuracy of all response pairs on this form?",
            "choices": h6.CONFIDENCE,
            "required": True,
        }
    if cohort == "domain_expert":
        return {
            "enabled": True,
            "title": "Can you confidently judge the research-methodology reasoning in these response pairs?",
            "choices": h6.CONFIDENCE,
            "required": True,
        }
    if cohort == "bilingual":
        titles = {
            "hi": "क्या आप हिंदी भाषा और वैज्ञानिक व्याख्या का आत्मविश्वास से मूल्यांकन कर सकते हैं? / Can you confidently judge the Hindi language and content?",
            "bn": "আপনি কি বাংলা ভাষা ও বিষয়বস্তু আত্মবিশ্বাসের সঙ্গে বিচার করতে পারেন? / Can you confidently judge the Bengali language and content?",
            "es": "¿Puedes evaluar con confianza el español y el contenido de estas respuestas? / Can you confidently judge the Spanish language and content?",
        }
        return {
            "enabled": True,
            "title": titles.get(language, "Can you confidently judge the requested language and content?"),
            "choices": h6.CONFIDENCE,
            "required": True,
        }
    if cohort == "educator":
        return {
            "enabled": True,
            "title": "Optional: How familiar are you with teaching or tutoring?",
            "choices": [
                "Teacher / educator",
                "Tutor / mentor",
                "Student / learner",
                "Other / prefer not to say",
            ],
            "required": False,
        }
    raise SystemExit(f"unsupported H8 reviewer cohort/domain: {cohort}/{domain}")


def index_variant(variant: dict[str, object]) -> dict[str, dict[str, str]]:
    comparisons = variant["comparisons"]
    if not isinstance(comparisons, list):
        raise SystemExit("H8 variant comparisons must be a list")
    out: dict[str, dict[str, str]] = {}
    for comparison in comparisons:
        if not isinstance(comparison, dict):
            raise SystemExit("H8 comparison must be an object")
        prompt = str(comparison["prompt"])
        if prompt in out:
            raise SystemExit("duplicate H8 prompt in reviewer variant")
        out[prompt] = comparison
    return out


def verify_complement(v01: dict[str, object], v02: dict[str, object]) -> None:
    if v01["batch_id"] != v02["batch_id"]:
        raise SystemExit("H8 variants have different batch IDs")
    if v01["partition"] != "development" or v02["partition"] != "development":
        raise SystemExit("H8 form materializer requires development variants")
    m1, m2 = index_variant(v01), index_variant(v02)
    if set(m1) != set(m2):
        raise SystemExit("H8 variants contain different prompts")
    for prompt in sorted(m1):
        a, b = m1[prompt], m2[prompt]
        if a["response_a"] != b["response_b"] or a["response_b"] != b["response_a"]:
            raise SystemExit("H8 A/B counterbalance mismatch")


def make_group_packet(
    cases: list[dict[str, object]],
    variant: dict[str, object],
    by_prompt: dict[str, dict[str, str]],
    *,
    group_index: int,
    target: int,
) -> dict[str, object]:
    comparisons = []
    languages = {str(case["language"]) for case in cases}
    cohorts = {str(case["reviewer_cohort"]) for case in cases}
    for ordinal, case in enumerate(cases, start=1):
        comparison = by_prompt[str(case["prompt"])]
        language = str(comparison["language"])
        comparisons.append(
            {
                "ordinal": ordinal,
                "comparison_id": comparison["comparison_id"],
                "display_title": f"Comparison {ordinal} of {len(cases)}",
                "prompt": h6.display_text(comparison["prompt"]),
                "response_a": h6.display_text(comparison["response_a"]),
                "response_b": h6.display_text(comparison["response_b"]),
                "question": h6.QUESTION_BY_LANG.get(language, h6.QUESTION_BY_LANG["en"]),
                "choices": h6.CHOICES,
                "required": True,
                "domain": comparison["domain"],
            }
        )

    letter = "A" if variant["variant_id"] == "V01" else "B"
    cohort_label = "-".join(sorted(cohorts)).upper().replace("_", "-")
    desc = h6.BILINGUAL_DESC if any(lang in {"hi", "bn", "es"} for lang in languages) else h6.BASE_DESC
    if len(cohorts) == 1 and not (next(iter(cohorts)) == "bilingual" and len(languages) > 1):
        context = context_for(cases[0])
    else:
        context = {
            "enabled": True,
            "title": "Can you confidently judge all three response pairs on this form, including any requested languages?",
            "choices": h6.CONFIDENCE,
            "required": True,
        }
    return {
        "form_packet_version": "1.2",
        "protocol_version": "1.0",
        "environment": "sandbox",
        "packet_id": f"HEF1-H8-G{group_index:02d}-{letter}-20260919",
        "batch_id": variant["batch_id"],
        "variant_id": variant["variant_id"],
        "partition": "development",
        "reviewer_cohort": cohort_label.lower(),
        "language": "mixed" if len(languages) > 1 else next(iter(languages)),
        "title": f"PAUL Open — Human Evaluation — H8 Group {group_index} {letter}",
        "description": desc,
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
        "comparisons": comparisons,
        "reviewer_context": context,
        "optional_comment": h6.OPTIONAL,
        "confirmation_message": h6.CONFIRM,
        "sandbox_auto_close_after_submissions": target,
    }


def generate(bundle_dir: pathlib.Path) -> str:
    v01 = h6.load_variant(bundle_dir / "variant_v01.json")
    v02 = h6.load_variant(bundle_dir / "variant_v02.json")
    if v01["variant_id"] != "V01" or v02["variant_id"] != "V02":
        raise SystemExit("unexpected H8 variant IDs")
    verify_complement(v01, v02)

    manifest = load_manifest()
    prompts = {str(case["prompt"]) for case in manifest}
    maps = {"V01": index_variant(v01), "V02": index_variant(v02)}
    if set(maps["V01"]) != prompts:
        raise SystemExit("H8 reviewer bundle prompt set does not match frozen manifest")

    # Four three-case groups. First two groups receive V01=2/V02=1;
    # last two receive V01=1/V02=2. Every case therefore gets three
    # initial judgments with complementary A/B exposure.
    groups = [manifest[i : i + 3] for i in range(0, 12, 3)]
    packets = []
    for group_index, cases in enumerate(groups, start=1):
        for variant in (v01, v02):
            if group_index <= 2:
                target = 2 if variant["variant_id"] == "V01" else 1
            else:
                target = 1 if variant["variant_id"] == "V01" else 2
            packets.append(
                make_group_packet(
                    cases,
                    variant,
                    maps[variant["variant_id"]],
                    group_index=group_index,
                    target=target,
                )
            )

    if len(packets) != 8:
        raise SystemExit(f"H8 expected 8 grouped packets, found {len(packets)}")
    if any(len(packet["comparisons"]) != 3 for packet in packets):
        raise SystemExit("H8 every packet must contain exactly three comparisons")
    if sum(
        packet["sandbox_auto_close_after_submissions"] * len(packet["comparisons"])
        for packet in packets
    ) != 36:
        raise SystemExit("H8 initial allocation must total exactly 36 case judgments")
    if len({packet["batch_id"] for packet in packets}) != 1:
        raise SystemExit("H8 packets must all share one batch_id")

    body = (
        "const PAUL_HUMAN_EVAL_SPEC = "
        + json.dumps({"packets": packets}, ensure_ascii=False, indent=2)
        + ";\n"
    )
    return HEADER + body + runner()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: materialize_h8_forms_payload.py <reviewer_bundle_dir> <output.gs>"
        )
    bundle_dir = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    output_path.write_text(generate(bundle_dir), encoding="utf-8")
