/*
 * PAUL Open H4 adaptive follow-up controller.
 *
 * Recovery-only helper for the 2026-09-12 H4 DHE collection round.
 * Reopens only the three predeclared follow-up variants that each currently
 * have one response and closes each again at exactly three responses. Combined
 * with the complementary variant's two responses, this yields five judgments
 * per escalated H4 case as required by the frozen adaptive allocation policy.
 *
 * Run startH4AdaptiveFollowup() once from the SAME Apps Script project that
 * owns the PAUL Open human-evaluation Forms runtime. No model/source identity,
 * reviewer identity, A/B mapping, or SHAE material is handled here.
 */

const PAUL_H4_ADAPTIVE_FOLLOWUP = [
  {
    packet_id: 'HEF1-H4-STEM-B-20260911',
    form_id: '1m2QWa4tirdEa_UREVcUof6GWCLqCSfj6672EXNh_poA',
    expected_start_count: 1,
    target_count: 3,
  },
  {
    packet_id: 'HEF1-H4-EDUCATOR-A-20260911',
    form_id: '1TVE8gRQLtCGofVdBAq1qRZEi9OGFYZcoXeWYo8bZVFg',
    expected_start_count: 1,
    target_count: 3,
  },
  {
    packet_id: 'HEF1-H4-BN-B-20260911',
    form_id: '1OjQONnK-xofMK9u7Y7K0GtRRjCnzBk075EcICsoaj3U',
    expected_start_count: 1,
    target_count: 3,
  },
];

const PAUL_H4_ADAPTIVE_HANDLER = 'monitorH4AdaptiveFollowup';

function startH4AdaptiveFollowup() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const result = [];

    // Fail closed: inspect every target before reopening any of them.
    for (const target of PAUL_H4_ADAPTIVE_FOLLOWUP) {
      const form = FormApp.openById(target.form_id);
      const count = form.getResponses().length;
      if (count !== target.expected_start_count) {
        throw new Error(
            `${target.packet_id}: expected ${target.expected_start_count} existing ` +
            `response(s) before recovery, found ${count}. Nothing was reopened.`,
        );
      }
      result.push({
        packet_id: target.packet_id,
        form_id: target.form_id,
        response_count: count,
      });
    }

    for (const target of PAUL_H4_ADAPTIVE_FOLLOWUP) {
      const form = FormApp.openById(target.form_id);
      form
          .setPublished(true)
          .setAcceptingResponses(true);
    }

    ensureH4AdaptiveMonitorTrigger_();
    console.log(JSON.stringify({status: 'reopened', forms: result}, null, 2));
    return result;
  } finally {
    lock.releaseLock();
  }
}

function monitorH4AdaptiveFollowup() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const states = [];
    let allComplete = true;

    for (const target of PAUL_H4_ADAPTIVE_FOLLOWUP) {
      const form = FormApp.openById(target.form_id);
      const count = form.getResponses().length;

      if (count >= target.target_count) {
        if (form.isAcceptingResponses()) {
          form.setAcceptingResponses(false);
          try {
            form.setCustomClosedFormMessage(
                'This evaluation form has reached its review target. Thank you.',
            );
          } catch (error) {
            console.warn(
                `${target.packet_id}: closed at target but could not set closed message: ${error}`,
            );
          }
        }
      } else {
        allComplete = false;
        if (!form.isAcceptingResponses()) {
          // Recovery guard: an unrelated close should not silently strand a
          // predeclared follow-up before its target is reached.
          form.setAcceptingResponses(true);
        }
      }

      states.push({
        packet_id: target.packet_id,
        response_count: count,
        target_count: target.target_count,
        accepting_responses: form.isAcceptingResponses(),
      });
    }

    if (allComplete) {
      removeH4AdaptiveMonitorTriggers_();
    }

    console.log(JSON.stringify({all_complete: allComplete, forms: states}, null, 2));
    return states;
  } finally {
    lock.releaseLock();
  }
}

function ensureH4AdaptiveMonitorTrigger_() {
  const exists = ScriptApp.getProjectTriggers().some(
      (trigger) => trigger.getHandlerFunction() === PAUL_H4_ADAPTIVE_HANDLER,
  );
  if (!exists) {
    ScriptApp.newTrigger(PAUL_H4_ADAPTIVE_HANDLER)
        .timeBased()
        .everyMinutes(1)
        .create();
  }
}

function removeH4AdaptiveMonitorTriggers_() {
  for (const trigger of ScriptApp.getProjectTriggers()) {
    if (trigger.getHandlerFunction() === PAUL_H4_ADAPTIVE_HANDLER) {
      ScriptApp.deleteTrigger(trigger);
    }
  }
}

function verifyH4AdaptiveFollowup() {
  const states = PAUL_H4_ADAPTIVE_FOLLOWUP.map((target) => {
    const form = FormApp.openById(target.form_id);
    return {
      packet_id: target.packet_id,
      response_count: form.getResponses().length,
      target_count: target.target_count,
      accepting_responses: form.isAcceptingResponses(),
      respondent_url: form.getPublishedUrl(),
    };
  });
  console.log(JSON.stringify(states, null, 2));
  return states;
}
