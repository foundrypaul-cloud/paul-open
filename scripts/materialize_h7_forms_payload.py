from __future__ import annotations

import json
import pathlib
import sys

from scripts import materialize_h6_forms_payload as h6

H6_LOCKED_BATCH_ID = "HEB1-5AE2CE4166CD"

HEADER = '''// PAUL Open H7 DHE V5 reviewer-safe Google Forms payload.
// Generated only from a reviewer-safe H7 paired-generation artifact.
//
// IMPORTANT:
// - Contains blinded reviewer material only; no source/model mapping.
// - Research partition is development; H7 is DHE, not SHAE.
// - H7 prompts were frozen before DPO V5 output inspection.
// - Initial allocation is exactly 3 valid judgments/case with complementary
//   2/1 variant targets, giving 9 submissions per display variant across six cases.
// - Do not unblind before the blinded analysis lock and durability audit pass.
// - Do not publish Form/Sheet identifiers to the public repository.
//
// Use with tools/google_forms/Code.gs in the already-authorized standalone
// Apps Script project. Run createPaulHumanEvalH7Forms() once.
// The runner first removes only obsolete, closed H6 per-Form submit triggers;
// H6 Forms, Sheets, responses, backups and runtime metadata are preserved.

'''

TRIGGER_PREFLIGHT = r'''

const PAUL_H6_LOCKED_BATCH_ID_FOR_H7_ = 'HEB1-5AE2CE4166CD';
const PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H7_ = 20;

function h7TriggerSourceId_(trigger) {
  try {
    return trigger.getTriggerSourceId() || null;
  } catch (error) {
    return null;
  }
}

function preparePaulHumanEvalH7TriggerCapacity_(packetCount) {
  if (!Number.isInteger(packetCount) || packetCount <= 0) {
    throw new Error(`H7 trigger preflight requires a positive packet count, got ${packetCount}`);
  }

  const properties = PropertiesService.getScriptProperties();
  const deleted = [];

  // H6 is blinded-analysis locked and all H6 Forms are closed. Remove only
  // submit triggers whose persisted runtime mapping proves they belong to that
  // exact locked H6 batch. Preserve the runtime mappings as historical evidence.
  for (const trigger of ScriptApp.getProjectTriggers()) {
    if (trigger.getHandlerFunction() !== 'onPaulHumanEvalSubmit') {
      continue;
    }
    const sourceId = h7TriggerSourceId_(trigger);
    if (!sourceId) {
      throw new Error('H7 trigger preflight found a PAUL submit trigger without a source Form ID.');
    }
    const raw = properties.getProperty(PAUL_FORM_PROPERTY_PREFIX + sourceId);
    if (!raw) {
      throw new Error(`H7 trigger preflight found an unmapped PAUL submit trigger for Form ${sourceId}.`);
    }
    let config;
    try {
      config = JSON.parse(raw);
    } catch (error) {
      throw new Error(`H7 trigger preflight could not parse runtime mapping for Form ${sourceId}: ${error}`);
    }
    if (!config || config.batch_id !== PAUL_H6_LOCKED_BATCH_ID_FOR_H7_) {
      throw new Error(
          `H7 trigger preflight refuses to delete non-H6 submit trigger for Form ${sourceId}; ` +
          `batch=${config && config.batch_id}`,
      );
    }
    const form = FormApp.openById(sourceId);
    if (form.isAcceptingResponses()) {
      throw new Error(`H7 trigger preflight refuses to delete trigger for still-open H6 Form ${sourceId}.`);
    }
    ScriptApp.deleteTrigger(trigger);
    deleted.push(sourceId);
  }

  const remaining = ScriptApp.getProjectTriggers();
  const recoveryExists = remaining.some(
      (trigger) => trigger.getHandlerFunction() === PAUL_RECOVERY_HANDLER,
  );
  const additionalNeeded = packetCount + (recoveryExists ? 0 : 1);
  const projected = remaining.length + additionalNeeded;
  if (projected > PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H7_) {
    throw new Error(
        `H7 trigger capacity preflight failed: remaining=${remaining.length}, ` +
        `needed=${additionalNeeded}, projected=${projected}, ` +
        `limit=${PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H7_}. No H7 Form has been created.`,
    );
  }

  const summary = {
    h6_locked_batch_id: PAUL_H6_LOCKED_BATCH_ID_FOR_H7_,
    deleted_obsolete_h6_submit_trigger_count: deleted.length,
    h6_runtime_properties_deleted: 0,
    remaining_trigger_count: remaining.length,
    recovery_trigger_already_present: recoveryExists,
    h7_submit_triggers_required: packetCount,
    projected_trigger_count: projected,
    trigger_limit: PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H7_,
  };
  console.log(JSON.stringify(summary, null, 2));
  return summary;
}
'''


def runner() -> str:
    text = h6.RUNNER.replace("H6", "H7")
    marker = "  const created = [];\n"
    replacement = "  preparePaulHumanEvalH7TriggerCapacity_(packets.length);\n\n  const created = [];\n"
    if marker not in text:
        raise RuntimeError("H6 runner structure changed; H7 trigger preflight insertion point missing")
    return text.replace(marker, replacement, 1) + TRIGGER_PREFLIGHT


def make_packet(spec, variant, comparison):
    packet = h6.make_packet(spec, variant, comparison)
    packet["packet_id"] = packet["packet_id"].replace("HEF1-H6-", "HEF1-H7-", 1)
    return packet


def verify_complement(v01, v02):
    if v01["batch_id"] != v02["batch_id"]:
        raise SystemExit("H7 variants have different batch IDs")
    if v01["partition"] != "development" or v02["partition"] != "development":
        raise SystemExit("H7 form materializer requires development variants")
    m1, m2 = h6.by_key(v01), h6.by_key(v02)
    if set(m1) != set(m2):
        raise SystemExit("H7 variants contain different case keys")
    for key in sorted(m1):
        a, b = m1[key], m2[key]
        if a["prompt"] != b["prompt"]:
            raise SystemExit(f"H7 prompt mismatch across variants: {key}")
        if a["response_a"] != b["response_b"] or a["response_b"] != b["response_a"]:
            raise SystemExit(f"H7 A/B counterbalance mismatch: {key}")


def generate(bundle_dir: pathlib.Path) -> str:
    v01 = h6.load_variant(bundle_dir / "variant_v01.json")
    v02 = h6.load_variant(bundle_dir / "variant_v02.json")
    if v01["variant_id"] != "V01" or v02["variant_id"] != "V02":
        raise SystemExit("unexpected H7 variant IDs")
    verify_complement(v01, v02)

    maps = {"V01": h6.by_key(v01), "V02": h6.by_key(v02)}
    expected_keys = {spec["key"] for spec in h6.CASE_SPECS}
    if set(maps["V01"]) != expected_keys:
        missing = expected_keys - set(maps["V01"])
        extra = set(maps["V01"]) - expected_keys
        raise SystemExit(f"unexpected H7 reviewer keys; missing={missing}, extra={extra}")

    packets = []
    for spec in h6.CASE_SPECS:
        for variant in (v01, v02):
            comparison = maps[variant["variant_id"]][spec["key"]]
            packets.append(make_packet(spec, variant, comparison))

    if len(packets) != 12:
        raise SystemExit(f"H7 expected 12 one-comparison packets, found {len(packets)}")
    if sum(p["sandbox_auto_close_after_submissions"] for p in packets) != 18:
        raise SystemExit("H7 initial allocation must total exactly 18 judgments")

    body = (
        "const PAUL_HUMAN_EVAL_SPEC = "
        + json.dumps({"packets": packets}, ensure_ascii=False, indent=2)
        + ";\n"
    )
    return HEADER + body + runner()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: materialize_h7_forms_payload.py <reviewer_bundle_dir> <output.gs>"
        )
    bundle_dir = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    output_path.write_text(generate(bundle_dir), encoding="utf-8")
