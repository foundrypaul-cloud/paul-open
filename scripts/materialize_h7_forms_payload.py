from __future__ import annotations

import json
import pathlib
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts import materialize_h6_forms_payload as h6

H5_LOCKED_BATCH_ID = "HEB1-64CDCC9521D3"
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
//
// Trigger-safety note:
// H5 previously hit the Apps Script project trigger ceiling because obsolete
// per-Form triggers from earlier evaluations and a failed H5 materialization were
// still installed. This H7 runner performs a fail-closed preflight before creating
// any Form. It removes only provably obsolete triggers from locked H5/H6 batches,
// deduplicates the shared recovery trigger, and can clean a zero-response partial
// H7 attempt without deleting any Form, Sheet, response, or backup ledger.

'''

TRIGGER_PREFLIGHT = r'''

const PAUL_H5_LOCKED_BATCH_ID_FOR_H7_ = 'HEB1-64CDCC9521D3';
const PAUL_H6_LOCKED_BATCH_ID_FOR_H7_ = 'HEB1-5AE2CE4166CD';
const PAUL_APPS_SCRIPT_TRIGGER_LIMIT_FOR_H7_ = 20;
const PAUL_OBSOLETE_HISTORICAL_HANDLERS_FOR_H7_ = new Set([
  'monitorH4AdaptiveFollowup',
]);

function h7TriggerSourceId_(trigger) {
  try {
    return trigger.getTriggerSourceId() || null;
  } catch (error) {
    return null;
  }
}

function h7ParseRuntimeConfig_(properties, formId) {
  const key = PAUL_FORM_PROPERTY_PREFIX + formId;
  const raw = properties.getProperty(key);
  if (!raw) {
    throw new Error(`H7 trigger preflight found an unmapped PAUL Form trigger for Form ${formId}.`);
  }
  try {
    const config = JSON.parse(raw);
    if (!config || !config.batch_id) {
      throw new Error('runtime mapping has no batch_id');
    }
    return config;
  } catch (error) {
    throw new Error(`H7 trigger preflight could not parse runtime mapping for Form ${formId}: ${error}`);
  }
}

function h7TargetBatchId_(packets) {
  if (!Array.isArray(packets) || packets.length === 0) {
    throw new Error('H7 trigger preflight requires a non-empty packet list.');
  }
  const batchIds = [...new Set(packets.map((packet) => packet.batch_id))];
  if (batchIds.length !== 1 || !batchIds[0]) {
    throw new Error(`H7 packets must contain exactly one non-empty batch_id; got ${batchIds}`);
  }
  return batchIds[0];
}

function h7InspectTargetBatchRuntime_(properties, targetBatchId) {
  const values = properties.getProperties();
  const staleZeroResponseForms = new Set();
  const targetRuntimeFormIds = [];

  for (const key of Object.keys(values).sort()) {
    if (!key.startsWith(PAUL_FORM_PROPERTY_PREFIX)) {
      continue;
    }
    let config;
    try {
      config = JSON.parse(values[key]);
    } catch (error) {
      // Historical malformed properties are preserved; an attached PAUL trigger
      // will still fail closed later because its mapping cannot be parsed.
      continue;
    }
    if (!config || config.batch_id !== targetBatchId) {
      continue;
    }

    const formId = key.slice(PAUL_FORM_PROPERTY_PREFIX.length);
    const form = FormApp.openById(formId);
    const responseCount = form.getResponses().length;
    targetRuntimeFormIds.push(formId);

    if (form.isAcceptingResponses()) {
      throw new Error(
          `H7 trigger preflight found an already-live H7 Form ${formId}. ` +
          'Refusing to rerun materialization and create duplicates.',
      );
    }
    if (responseCount > 0) {
      throw new Error(
          `H7 trigger preflight found an existing H7 Form ${formId} with ${responseCount} responses. ` +
          'Refusing to remove its runtime mapping or rerun materialization.',
      );
    }

    // A closed, zero-response target-batch Form can be left behind when a prior
    // creation attempt fails before publish (for example at trigger creation).
    // It is safe to detach that abandoned runtime mapping and retry. The Form,
    // response Sheet and backup ledger themselves are deliberately preserved.
    staleZeroResponseForms.add(formId);
  }

  return {staleZeroResponseForms, targetRuntimeFormIds};
}

function preparePaulHumanEvalH7TriggerCapacity_(packets) {
  const targetBatchId = h7TargetBatchId_(packets);
  const packetCount = packets.length;
  const properties = PropertiesService.getScriptProperties();
  const targetInspection = h7InspectTargetBatchRuntime_(properties, targetBatchId);
  const staleTargetForms = targetInspection.staleZeroResponseForms;

  const deletedHistoricalSubmitTriggers = [];
  const deletedStaleTargetSubmitTriggers = [];
  const deletedHistoricalHandlers = [];
  const deletedDuplicateRecoveryTriggers = [];

  let recoveryKept = false;
  for (const trigger of ScriptApp.getProjectTriggers()) {
    const handler = trigger.getHandlerFunction();

    if (PAUL_OBSOLETE_HISTORICAL_HANDLERS_FOR_H7_.has(handler)) {
      ScriptApp.deleteTrigger(trigger);
      deletedHistoricalHandlers.push({handler: handler, source_id: h7TriggerSourceId_(trigger)});
      continue;
    }

    if (handler === PAUL_RECOVERY_HANDLER) {
      if (!recoveryKept) {
        recoveryKept = true;
      } else {
        ScriptApp.deleteTrigger(trigger);
        deletedDuplicateRecoveryTriggers.push(h7TriggerSourceId_(trigger));
      }
      continue;
    }

    if (handler !== 'onPaulHumanEvalSubmit') {
      continue;
    }

    const sourceId = h7TriggerSourceId_(trigger);
    if (!sourceId) {
      throw new Error('H7 trigger preflight found a PAUL submit trigger without a source Form ID.');
    }
    const config = h7ParseRuntimeConfig_(properties, sourceId);
    const batchId = config.batch_id;

    if (batchId === PAUL_H5_LOCKED_BATCH_ID_FOR_H7_ || batchId === PAUL_H6_LOCKED_BATCH_ID_FOR_H7_) {
      const form = FormApp.openById(sourceId);
      if (form.isAcceptingResponses()) {
        throw new Error(
            `H7 trigger preflight refuses to delete a still-open historical PAUL Form ${sourceId}; ` +
            `batch=${batchId}`,
        );
      }
      ScriptApp.deleteTrigger(trigger);
      deletedHistoricalSubmitTriggers.push({form_id: sourceId, batch_id: batchId});
      continue;
    }

    if (batchId === targetBatchId && staleTargetForms.has(sourceId)) {
      ScriptApp.deleteTrigger(trigger);
      deletedStaleTargetSubmitTriggers.push(sourceId);
      continue;
    }

    throw new Error(
        `H7 trigger preflight found a PAUL submit trigger that is not safe to remove: ` +
        `Form ${sourceId}, batch=${batchId}. No H7 Form has been created.`,
    );
  }

  const deletedStaleTargetRuntimeProperties = [];
  for (const formId of [...staleTargetForms].sort()) {
    const key = PAUL_FORM_PROPERTY_PREFIX + formId;
    properties.deleteProperty(key);
    deletedStaleTargetRuntimeProperties.push(key);
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
    target_h7_batch_id: targetBatchId,
    h5_locked_batch_id: PAUL_H5_LOCKED_BATCH_ID_FOR_H7_,
    h6_locked_batch_id: PAUL_H6_LOCKED_BATCH_ID_FOR_H7_,
    deleted_obsolete_historical_submit_trigger_count: deletedHistoricalSubmitTriggers.length,
    deleted_obsolete_historical_submit_triggers: deletedHistoricalSubmitTriggers,
    deleted_obsolete_historical_handler_count: deletedHistoricalHandlers.length,
    deleted_obsolete_historical_handlers: deletedHistoricalHandlers,
    deleted_duplicate_recovery_trigger_count: deletedDuplicateRecoveryTriggers.length,
    deleted_stale_h7_submit_trigger_count: deletedStaleTargetSubmitTriggers.length,
    deleted_stale_h7_runtime_property_count: deletedStaleTargetRuntimeProperties.length,
    historical_h5_h6_runtime_properties_deleted: 0,
    stale_h7_forms_sheets_or_responses_deleted: 0,
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
    replacement = "  preparePaulHumanEvalH7TriggerCapacity_(packets);\n\n  const created = [];\n"
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
    if len({p["batch_id"] for p in packets}) != 1:
        raise SystemExit("H7 packets must all share one batch_id")

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
