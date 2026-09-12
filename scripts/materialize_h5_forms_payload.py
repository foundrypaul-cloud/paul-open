from __future__ import annotations

import json
import pathlib
import sys

BASE_DESC = (
    "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. "
    "Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so."
)
BILINGUAL_DESC = BASE_DESC + (
    " Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation when that is clearer or more accurate."
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

CASE_SPECS = [
    {
        "key": ("stem_capable", "en", "science_reasoning"),
        "slug": "STEM",
        "title": "Stem",
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
            "title": "Can you confidently judge the Hindi language and scientific explanation in this response pair?",
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
            "title": "Can you confidently judge the Bengali language and scientific explanation in this response pair?",
            "choices": CONFIDENCE,
            "required": True,
        },
    },
    {
        "key": ("general_user", "en", "empathy_human_centered"),
        "slug": "GENERAL",
        "title": "General",
        "targets": {"V01": 1, "V02": 2},
        "context": {
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
        },
    },
]

HEADER = '''// PAUL Open H5 DHE V3 reviewer-safe Google Forms payload.
// Generated only from GitHub Actions reviewer-safe artifact 10297811566.
// Batch: HEB1-64CDCC9521D3
//
// IMPORTANT:
// - This file contains blinded reviewer material only; it contains no source/model mapping.
// - `environment: "sandbox"` is required by the existing H2/H3/H4 Forms runtime validator.
//   The research partition is explicitly `development`; H5 remains DHE, not SHAE.
// - Initial allocation is exactly 3 judgments/case with alternating 2/1 complementary
//   variant targets, giving 9 submissions per display variant across six cases.
// - Do not unblind before the blinded analysis lock and durability audit pass.
//
// Use with the existing tools/google_forms/Code.gs runtime in the already-authorized
// standalone Apps Script project. Run createPaulHumanEvalH5Forms() once.

'''

RUNNER = r'''

// H5-specific resilient launcher.
// Use this instead of createPaulHumanEvalSandboxForms() for H5 collection.
// It preserves the existing runtime/data model but retries the Google Forms
// response-destination link, which can fail transiently immediately after a
// new Spreadsheet is created.
function createPaulHumanEvalH5Forms() {
  if (typeof PAUL_HUMAN_EVAL_SPEC === 'undefined') {
    throw new Error('PAUL_HUMAN_EVAL_SPEC is missing. Add H5Payload.gs.');
  }
  const packets = PAUL_HUMAN_EVAL_SPEC.packets;
  if (!Array.isArray(packets) || packets.length === 0) {
    throw new Error('PAUL_HUMAN_EVAL_SPEC.packets must be a non-empty array.');
  }

  const created = [];
  for (const packet of packets) {
    created.push(createPaulHumanEvalH5Form_(packet));
  }
  ensureRecoveryTrigger_();
  console.log(JSON.stringify(created, null, 2));
  return created;
}

function createPaulHumanEvalH5Form_(packet) {
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
    'response_id',
    'submitted_at_utc',
    'packet_id',
    'batch_id',
    'variant_id',
    'reviewer_cohort',
    'language',
    'comparison_id',
    'choice',
    'reviewer_context',
    'optional_comment',
  ]);

  const backupSpreadsheet = SpreadsheetApp.create(
      `PAUL Human Eval — ${packet.packet_id} — Backup Ledger`,
  );
  const backupSheet = backupSpreadsheet.getSheets()[0];
  backupSheet.setName(PAUL_BACKUP_SHEET);
  backupSheet.appendRow([
    'response_id',
    'submitted_at_utc',
    'packet_id',
    'batch_id',
    'variant_id',
    'reviewer_cohort',
    'language',
    'reviewer_context',
    'snapshot_json',
    'sha256',
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

  setH5ResponseDestinationWithRetry_(form, spreadsheet.getId(), packet.packet_id);

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
      metadataSheet,
      form,
      packet,
      choiceItemToComparison,
      backupSpreadsheet.getId(),
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

function setH5ResponseDestinationWithRetry_(form, spreadsheetId, packetId) {
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
          `H5 ${packetId}: response destination attempt ${attempt}/${maxAttempts} failed: ${error}`,
      );
      if (attempt < maxAttempts) {
        Utilities.sleep(1500 * attempt);
      }
    }
  }
  throw new Error(
      `H5 ${packetId}: failed to set response destination after ${maxAttempts} attempts. ` +
      `Spreadsheet ID: ${spreadsheetId}. Last error: ${lastError}`,
  );
}
'''


def load_variant(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_key(variant):
    out = {}
    for comparison in variant["comparisons"]:
        key = (
            comparison["reviewer_cohort"],
            comparison["language"],
            comparison["domain"],
        )
        if key in out:
            raise SystemExit(f"duplicate H5 reviewer key: {key}")
        out[key] = comparison
    return out


def make_packet(spec, variant, comparison):
    letter = "A" if variant["variant_id"] == "V01" else "B"
    description = (
        BILINGUAL_DESC
        if comparison["language"] in {"hi", "bn"}
        else BASE_DESC
    )
    return {
        "form_packet_version": "1.1",
        "protocol_version": "1.0",
        "environment": "sandbox",
        "packet_id": f"HEF1-H5-{spec['slug']}-{letter}-20260912",
        "batch_id": variant["batch_id"],
        "variant_id": variant["variant_id"],
        "partition": "development",
        "reviewer_cohort": comparison["reviewer_cohort"],
        "language": comparison["language"],
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
        "comparisons": [
            {
                "ordinal": 1,
                "comparison_id": comparison["comparison_id"],
                "display_title": "Comparison 1 of 1",
                "prompt": comparison["prompt"],
                "response_a": comparison["response_a"],
                "response_b": comparison["response_b"],
                "question": "Which response would you rather receive?",
                "choices": CHOICES,
                "required": True,
                "domain": comparison["domain"],
            }
        ],
        "reviewer_context": spec["context"],
        "optional_comment": OPTIONAL,
        "confirmation_message": CONFIRM,
        "sandbox_auto_close_after_submissions": spec["targets"][variant["variant_id"]],
    }


def generate(bundle_dir: pathlib.Path):
    v01 = load_variant(bundle_dir / "variant_v01.json")
    v02 = load_variant(bundle_dir / "variant_v02.json")
    if v01["batch_id"] != "HEB1-64CDCC9521D3" or v02["batch_id"] != v01["batch_id"]:
        raise SystemExit("unexpected H5 batch")

    maps = {"V01": by_key(v01), "V02": by_key(v02)}
    packets = []
    for spec in CASE_SPECS:
        for variant in (v01, v02):
            comparison = maps[variant["variant_id"]].get(spec["key"])
            if not comparison:
                raise SystemExit(
                    f"missing H5 reviewer case {spec['key']} in {variant['variant_id']}"
                )
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
            "usage: materialize_h5_forms_payload.py <reviewer_bundle_dir> <output.gs>"
        )
    bundle_dir = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    output_path.write_text(generate(bundle_dir), encoding="utf-8")
