from __future__ import annotations

import json
import pathlib
import re
import sys

BASE_DESC = (
    "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. "
    "Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, "
    "you can say so. There are no right or wrong preferences. This is a development research evaluation. "
    "Please do not include personal or sensitive information in the optional comment."
)
BILINGUAL_DESC = BASE_DESC + (
    " Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation "
    "when that is clearer or more accurate."
)
CHOICES = [
    "Response A is better",
    "Response B is better",
    "They are about equally good",
    "Neither response is good",
    "I'm not sure / I can't judge this",
]
CONFIRM = "Thank you — your PAUL Open evaluation response has been recorded."
OPTIONAL = {
    "enabled": True,
    "title": "Anything important you noticed? (optional)",
    "required": False,
}
CONFIDENCE = [
    "Yes — confidently",
    "Mostly — with minor uncertainty",
    "No — I can’t confidently judge this",
]

QUESTION_BY_LANG = {
    "en": "Which response would you rather receive?",
    "hi": "आप कौन-सा उत्तर प्राप्त करना पसंद करेंगे? / Which response would you rather receive?",
    "bn": "আপনি কোন উত্তরটি পেতে বেশি পছন্দ করবেন? / Which response would you rather receive?",
    "es": "¿Qué respuesta preferirías recibir? / Which response would you rather receive?",
}

CASE_SPECS = [
    {
        "key": ("stem_capable", "en", "science_reasoning"),
        "slug": "STEM",
        "title": "STEM",
        "targets": {"V01": 2, "V02": 1},
        "context": {
            "enabled": True,
            "title": "Can you confidently judge the scientific accuracy of this response pair?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
    {
        "key": ("educator", "en", "socratic_tutoring"),
        "slug": "EDUCATOR",
        "title": "Educator",
        "targets": {"V01": 1, "V02": 2},
        "context": {
            "enabled": True,
            "title": "Optional: How familiar are you with teaching or tutoring?",
            "choices": [
                "Teacher / educator",
                "Tutor / mentor",
                "Student / learner",
                "Other / prefer not to say",
            ],
            "required": False,
        },
    },
    {
        "key": ("domain_expert", "en", "scientific_research_assistance"),
        "slug": "RESEARCH",
        "title": "Research",
        "targets": {"V01": 2, "V02": 1},
        "context": {
            "enabled": True,
            "title": "Can you confidently judge the research-methodology and statistical reasoning in this response pair?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
    {
        "key": ("bilingual", "hi", "scientific_explanation"),
        "slug": "HI",
        "title": "Hindi",
        "targets": {"V01": 1, "V02": 2},
        "context": {
            "enabled": True,
            "title": "क्या आप हिंदी भाषा और वैज्ञानिक व्याख्या का आत्मविश्वास से मूल्यांकन कर सकते हैं? / Can you confidently judge the Hindi language and scientific explanation?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
    {
        "key": ("bilingual", "bn", "scientific_explanation"),
        "slug": "BN",
        "title": "Bengali",
        "targets": {"V01": 2, "V02": 1},
        "context": {
            "enabled": True,
            "title": "আপনি কি বাংলা ভাষা ও বৈজ্ঞানিক ব্যাখ্যাটি আত্মবিশ্বাসের সঙ্গে বিচার করতে পারেন? / Can you confidently judge the Bengali language and scientific explanation?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
    {
        "key": ("bilingual", "es", "evidence_first_human_centered"),
        "slug": "ES",
        "title": "Spanish",
        "targets": {"V01": 1, "V02": 2},
        "context": {
            "enabled": True,
            "title": "¿Puedes evaluar con confianza el español, el manejo de la evidencia y la comunicación de la incertidumbre? / Can you confidently judge this response pair?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
]

HEADER = '''// PAUL Open H6 DHE V4 reviewer-safe Google Forms payload.
// Generated only from a reviewer-safe H6 paired-generation artifact.
//
// IMPORTANT:
// - Contains blinded reviewer material only; no source/model mapping.
// - Research partition is development; H6 is DHE, not SHAE.
// - Initial allocation is exactly 3 valid judgments/case with complementary
//   2/1 variant targets, giving 9 submissions per display variant across six cases.
// - Do not unblind before the blinded analysis lock and durability audit pass.
// - Do not publish Form/Sheet identifiers to the public repository.
//
// Use with tools/google_forms/Code.gs in the already-authorized standalone
// Apps Script project. Run createPaulHumanEvalH6Forms() once.

'''

RUNNER = r'''

function createPaulHumanEvalH6Forms() {
  if (typeof PAUL_HUMAN_EVAL_SPEC === 'undefined') {
    throw new Error('PAUL_HUMAN_EVAL_SPEC is missing. Add the generated H6Payload.gs.');
  }
  const packets = PAUL_HUMAN_EVAL_SPEC.packets;
  if (!Array.isArray(packets) || packets.length === 0) {
    throw new Error('PAUL_HUMAN_EVAL_SPEC.packets must be a non-empty array.');
  }

  const created = [];
  for (const packet of packets) {
    created.push(createPaulHumanEvalH6Form_(packet));
  }
  ensureRecoveryTrigger_();
  console.log(JSON.stringify(created, null, 2));
  return created;
}

function createPaulHumanEvalH6Form_(packet) {
  validatePacket_(packet);

  const form = FormApp.create(packet.title, false);
  form
      .setDescription(packet.description)
      .setCollectEmail(false)
      .setAllowResponseEdits(false)
      .setLimitOneResponsePerUser(false)
      .setProgressBar(true)
      .setPublishingSummary(false)
      .setShowLinkToRespondAgain(false)
      .setShuffleQuestions(false)
      .setConfirmationMessage(packet.confirmation_message)
      .setAcceptingResponses(false);

  const spreadsheet = SpreadsheetApp.create(
      `PAUL Human Eval — ${packet.packet_id} — Responses`,
  );
  const metadataSheet = spreadsheet.getSheets()[0];
  metadataSheet.setName(PAUL_METADATA_SHEET);
  const normalizedSheet = spreadsheet.insertSheet(PAUL_NORMALIZED_SHEET);
  normalizedSheet.appendRow([
    'response_id', 'submitted_at_utc', 'packet_id', 'batch_id', 'variant_id',
    'reviewer_cohort', 'language', 'comparison_id', 'choice', 'reviewer_context',
    'optional_comment',
  ]);

  const backupSpreadsheet = SpreadsheetApp.create(
      `PAUL Human Eval — ${packet.packet_id} — Backup Ledger`,
  );
  const backupSheet = backupSpreadsheet.getSheets()[0];
  backupSheet.setName(PAUL_BACKUP_SHEET);
  backupSheet.appendRow([
    'response_id', 'submitted_at_utc', 'packet_id', 'batch_id', 'variant_id',
    'reviewer_cohort', 'language', 'reviewer_context', 'snapshot_json', 'sha256',
    'backup_written_at_utc',
  ]);

  const choiceItemToComparison = {};
  for (const comparison of packet.comparisons) {
    form.addSectionHeaderItem()
        .setTitle(comparison.display_title)
        .setHelpText(comparisonHelpText_(comparison));
    const choiceItem = form.addMultipleChoiceItem()
        .setTitle(comparison.question)
        .setChoiceValues(comparison.choices)
        .setRequired(true);
    choiceItemToComparison[String(choiceItem.getId())] = comparison.comparison_id;
  }

  let reviewerContextItemId = null;
  if (packet.reviewer_context && packet.reviewer_context.enabled) {
    const contextItem = form.addMultipleChoiceItem()
        .setTitle(packet.reviewer_context.title)
        .setChoiceValues(packet.reviewer_context.choices)
        .setRequired(packet.reviewer_context.required === true);
    reviewerContextItemId = String(contextItem.getId());
  }

  let optionalCommentItemId = null;
  if (packet.optional_comment && packet.optional_comment.enabled) {
    const commentItem = form.addParagraphTextItem()
        .setTitle(packet.optional_comment.title)
        .setRequired(false);
    optionalCommentItemId = String(commentItem.getId());
  }

  setH6ResponseDestinationWithRetry_(form, spreadsheet.getId(), packet.packet_id);

  const runtimeConfig = {
    environment: packet.environment,
    packet_id: packet.packet_id,
    batch_id: packet.batch_id,
    variant_id: packet.variant_id,
    reviewer_cohort: packet.reviewer_cohort,
    language: packet.language,
    spreadsheet_id: spreadsheet.getId(),
    backup_spreadsheet_id: backupSpreadsheet.getId(),
    choice_item_to_comparison: choiceItemToComparison,
    reviewer_context_item_id: reviewerContextItemId,
    optional_comment_item_id: optionalCommentItemId,
    sandbox_auto_close_after_submissions: packet.sandbox_auto_close_after_submissions,
  };
  PropertiesService.getScriptProperties().setProperty(
      PAUL_FORM_PROPERTY_PREFIX + form.getId(),
      JSON.stringify(runtimeConfig),
  );

  writeMetadataSheet_(
      metadataSheet, form, packet, choiceItemToComparison, backupSpreadsheet.getId(),
  );
  ScriptApp.newTrigger('onPaulHumanEvalSubmit').forForm(form).onFormSubmit().create();
  form.setPublished(true).setAcceptingResponses(true);

  return {
    packet_id: packet.packet_id,
    form_id: form.getId(),
    respondent_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    spreadsheet_id: spreadsheet.getId(),
    spreadsheet_url: spreadsheet.getUrl(),
    backup_spreadsheet_id: backupSpreadsheet.getId(),
    backup_spreadsheet_url: backupSpreadsheet.getUrl(),
  };
}

function setH6ResponseDestinationWithRetry_(form, spreadsheetId, packetId) {
  const maxAttempts = 5;
  let lastError = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      SpreadsheetApp.openById(spreadsheetId);
      SpreadsheetApp.flush();
      Utilities.sleep(1000 * attempt);
      form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheetId);
      return;
    } catch (error) {
      lastError = error;
      console.warn(
          `H6 ${packetId}: response destination attempt ${attempt}/${maxAttempts} failed: ${error}`,
      );
      if (attempt < maxAttempts) {
        Utilities.sleep(1500 * attempt);
      }
    }
  }
  throw new Error(
      `H6 ${packetId}: failed to set response destination after ${maxAttempts} attempts. ` +
      `Spreadsheet ID: ${spreadsheetId}. Last error: ${lastError}`,
  );
}
'''


def load_variant(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def display_text(text: str) -> str:
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*[\*\-]\s+", "• ", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return text.strip()


def by_key(variant):
    out = {}
    for comparison in variant["comparisons"]:
        key = (
            comparison["reviewer_cohort"],
            comparison["language"],
            comparison["domain"],
        )
        if key in out:
            raise SystemExit(f"duplicate H6 reviewer key: {key}")
        out[key] = comparison
    return out


def verify_complement(v01, v02):
    if v01["batch_id"] != v02["batch_id"]:
        raise SystemExit("H6 variants have different batch IDs")
    if v01["partition"] != "development" or v02["partition"] != "development":
        raise SystemExit("H6 form materializer requires development variants")
    m1, m2 = by_key(v01), by_key(v02)
    if set(m1) != set(m2):
        raise SystemExit("H6 variants contain different case keys")
    for key in sorted(m1):
        a, b = m1[key], m2[key]
        if a["prompt"] != b["prompt"]:
            raise SystemExit(f"H6 prompt mismatch across variants: {key}")
        if a["response_a"] != b["response_b"] or a["response_b"] != b["response_a"]:
            raise SystemExit(f"H6 A/B counterbalance mismatch: {key}")


def make_packet(spec, variant, comparison):
    letter = "A" if variant["variant_id"] == "V01" else "B"
    language = comparison["language"]
    description = BILINGUAL_DESC if language in {"hi", "bn", "es"} else BASE_DESC
    return {
        "form_packet_version": "1.1",
        "protocol_version": "1.0",
        "environment": "sandbox",
        "packet_id": f"HEF1-H6-{spec['slug']}-{letter}-20260913",
        "batch_id": variant["batch_id"],
        "variant_id": variant["variant_id"],
        "partition": "development",
        "reviewer_cohort": comparison["reviewer_cohort"],
        "language": language,
        "title": f"PAUL Open — Human Evaluation — {spec['title']} {letter}",
        "description": description,
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
        "comparisons": [{
            "ordinal": 1,
            "comparison_id": comparison["comparison_id"],
            "display_title": "Comparison 1 of 1",
            "prompt": display_text(comparison["prompt"]),
            "response_a": display_text(comparison["response_a"]),
            "response_b": display_text(comparison["response_b"]),
            "question": QUESTION_BY_LANG.get(language, QUESTION_BY_LANG["en"]),
            "choices": CHOICES,
            "required": True,
            "domain": comparison["domain"],
        }],
        "reviewer_context": spec["context"],
        "optional_comment": OPTIONAL,
        "confirmation_message": CONFIRM,
        "sandbox_auto_close_after_submissions": spec["targets"][variant["variant_id"]],
    }


def generate(bundle_dir: pathlib.Path):
    v01 = load_variant(bundle_dir / "variant_v01.json")
    v02 = load_variant(bundle_dir / "variant_v02.json")
    if v01["variant_id"] != "V01" or v02["variant_id"] != "V02":
        raise SystemExit("unexpected H6 variant IDs")
    verify_complement(v01, v02)

    maps = {"V01": by_key(v01), "V02": by_key(v02)}
    expected_keys = {spec["key"] for spec in CASE_SPECS}
    if set(maps["V01"]) != expected_keys:
        missing = expected_keys - set(maps["V01"])
        extra = set(maps["V01"]) - expected_keys
        raise SystemExit(f"unexpected H6 reviewer keys; missing={missing}, extra={extra}")

    packets = []
    for spec in CASE_SPECS:
        for variant in (v01, v02):
            comparison = maps[variant["variant_id"]][spec["key"]]
            packets.append(make_packet(spec, variant, comparison))

    body = (
        "const PAUL_HUMAN_EVAL_SPEC = "
        + json.dumps({"packets": packets}, ensure_ascii=False, indent=2)
        + ";\n"
    )
    return HEADER + body + RUNNER


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: materialize_h6_forms_payload.py <reviewer_bundle_dir> <output.gs>"
        )
    bundle_dir = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    output_path.write_text(generate(bundle_dir), encoding="utf-8")
