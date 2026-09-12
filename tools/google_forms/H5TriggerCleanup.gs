/*
 * PAUL Open H5 one-time trigger-capacity cleanup.
 *
 * Run preparePaulHumanEvalH5TriggerCapacity() once before rerunning
 * createPaulHumanEvalH5Forms(). This helper deletes only obsolete PAUL
 * human-evaluation triggers and stale H5 runtime properties left by failed H5
 * creation attempts. It does not delete Forms, Sheets, responses, or unrelated
 * Apps Script triggers.
 */

const PAUL_H5_BATCH_ID = 'HEB1-64CDCC9521D3';

function preparePaulHumanEvalH5TriggerCapacity() {
  const triggers = ScriptApp.getProjectTriggers();
  const deletedTriggers = [];
  const preservedTriggers = [];

  for (const trigger of triggers) {
    const handler = trigger.getHandlerFunction();

    // H4 is complete, so its per-Form PAUL submit triggers and adaptive watcher
    // are obsolete. Failed H5 attempts use the same submit handler.
    if (handler === 'onPaulHumanEvalSubmit' || handler === 'monitorH4AdaptiveFollowup') {
      ScriptApp.deleteTrigger(trigger);
      deletedTriggers.push({
        handler: handler,
        source_id: safeTriggerSourceId_(trigger),
      });
      continue;
    }

    // Preserve the single recovery trigger and every unrelated project trigger.
    preservedTriggers.push({
      handler: handler,
      source_id: safeTriggerSourceId_(trigger),
    });
  }

  // Remove only runtime mappings from failed attempts for this exact H5 batch.
  // H4 mappings remain intact as historical evidence.
  const properties = PropertiesService.getScriptProperties();
  const values = properties.getProperties();
  const deletedPropertyKeys = [];
  for (const key of Object.keys(values).sort()) {
    if (!key.startsWith(PAUL_FORM_PROPERTY_PREFIX)) {
      continue;
    }
    try {
      const config = JSON.parse(values[key]);
      if (config && config.batch_id === PAUL_H5_BATCH_ID) {
        properties.deleteProperty(key);
        deletedPropertyKeys.push(key);
      }
    } catch (error) {
      // Do not touch malformed or unrelated historical properties here.
      console.warn(`Skipped unreadable property ${key}: ${error}`);
    }
  }

  const remainingTriggers = ScriptApp.getProjectTriggers().map((trigger) => ({
    handler: trigger.getHandlerFunction(),
    source_id: safeTriggerSourceId_(trigger),
  }));

  const result = {
    h5_batch_id: PAUL_H5_BATCH_ID,
    deleted_trigger_count: deletedTriggers.length,
    deleted_triggers: deletedTriggers,
    deleted_h5_runtime_property_count: deletedPropertyKeys.length,
    deleted_h5_runtime_property_keys: deletedPropertyKeys,
    remaining_trigger_count: remainingTriggers.length,
    remaining_triggers: remainingTriggers,
    next_step: 'Run createPaulHumanEvalH5Forms() once.',
  };

  console.log(JSON.stringify(result, null, 2));
  return result;
}

function safeTriggerSourceId_(trigger) {
  try {
    return trigger.getTriggerSourceId() || null;
  } catch (error) {
    return null;
  }
}
