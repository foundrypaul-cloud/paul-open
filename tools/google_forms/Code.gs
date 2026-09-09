/*
 * PAUL Open Human Evaluation — Google Forms runtime.
 *
 * The evaluation path is anonymous. Reviewer contact details, if collected,
 * live in a separate opt-in reviewer-panel Form. Evaluation submissions are
 * retained in the Google Form, its linked raw response Sheet, a normalized
 * Sheet, and a second backup-ledger spreadsheet. An hourly recovery trigger
 * repairs missing normalized/backup rows from accepted Form responses.
 *
 * This script never receives model/source identities or the H1 private A/B map.
 */

const PAUL_FORM_PROPERTY_PREFIX = 'PAUL_HUMAN_EVAL_FORM_';
const PAUL_PANEL_FORM_PROPERTY = 'PAUL_REVIEWER_PANEL_FORM_ID';
const PAUL_NORMALIZED_SHEET = 'PAUL Normalized';
const PAUL_METADATA_SHEET = 'PAUL Metadata';
const PAUL_BACKUP_SHEET = 'PAUL Backup Ledger';
const PAUL_RECOVERY_HANDLER = 'recoverPaulHumanEvalResponses';

function createPaulHumanEvalSandboxForms() {
  if (typeof PAUL_HUMAN_EVAL_SPEC === 'undefined') {
    throw new Error('PAUL_HUMAN_EVAL_SPEC is missing. Add the generated Payload.gs file.');
  }
  const packets = PAUL_HUMAN_EVAL_SPEC.packets;
  if (!Array.isArray(packets) || packets.length === 0) {
    throw new Error('PAUL_HUMAN_EVAL_SPEC.packets must be a non-empty array.');
  }

  const created = packets.map((packet) => createPaulHumanEvalForm_(packet));
  ensureRecoveryTrigger_();
  console.log(JSON.stringify(created, null, 2));
  return created;
}

function createPaulHumanEvalForm_(packet) {
  validatePacket_(packet);

  // Create unpublished so no respondent can enter while items/settings are incomplete.
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

  form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheet.getId());

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

  // Publish only after the complete form, response destination and trigger exist.
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

function comparisonHelpText_(comparison) {
  return [
    'Question',
    comparison.prompt,
    '',
    'Response A',
    comparison.response_a,
    '',
    'Response B',
    comparison.response_b,
  ].join('\n');
}

function writeMetadataSheet_(sheet, form, packet, itemMap, backupSpreadsheetId) {
  const rows = [
    ['field', 'value'],
    ['packet_id', packet.packet_id],
    ['batch_id', packet.batch_id],
    ['variant_id', packet.variant_id],
    ['environment', packet.environment],
    ['reviewer_cohort', packet.reviewer_cohort],
    ['language', packet.language],
    ['form_id', form.getId()],
    ['backup_spreadsheet_id', backupSpreadsheetId],
    ['form_packet_version', packet.form_packet_version],
    ['protocol_version', packet.protocol_version],
    ['', ''],
    ['choice_item_id', 'comparison_id'],
  ];
  for (const itemId of Object.keys(itemMap).sort()) {
    rows.push([itemId, itemMap[itemId]]);
  }
  sheet.getRange(1, 1, rows.length, 2).setValues(rows);
  sheet.setFrozenRows(1);
}

function onPaulHumanEvalSubmit(event) {
  if (!event || !event.source || !event.response) {
    throw new Error('This function must run from a Google Forms submit trigger.');
  }
  const form = event.source;
  const config = runtimeConfigForForm_(form.getId());
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    persistPaulHumanEvalResponse_(form, event.response, config);
    maybeCloseSandboxForm_(form, config);
  } finally {
    lock.releaseLock();
  }
}

function runtimeConfigForForm_(formId) {
  const propertyKey = PAUL_FORM_PROPERTY_PREFIX + formId;
  const encoded = PropertiesService.getScriptProperties().getProperty(propertyKey);
  if (!encoded) {
    throw new Error(`Missing runtime mapping for form ${formId}.`);
  }
  return JSON.parse(encoded);
}

function persistPaulHumanEvalResponse_(form, response, config) {
  const responseId = response.getId();
  if (!responseId) {
    throw new Error('Submitted FormResponse unexpectedly has no response ID.');
  }

  const payload = responsePayload_(form, response, config);
  ensureBackupLedgerRow_(payload, config);
  ensureNormalizedRows_(payload, config);
}

function responsePayload_(form, response, config) {
  const answersByItem = {};
  for (const itemResponse of response.getItemResponses()) {
    const itemId = String(itemResponse.getItem().getId());
    const raw = itemResponse.getResponse();
    answersByItem[itemId] = Array.isArray(raw) ? raw.join(' | ') : String(raw || '');
  }

  let reviewerContext = '';
  if (config.reviewer_context_item_id) {
    reviewerContext = answersByItem[config.reviewer_context_item_id] || '';
  }
  let optionalComment = '';
  if (config.optional_comment_item_id) {
    optionalComment = answersByItem[config.optional_comment_item_id] || '';
  }

  const timestamp = response.getTimestamp();
  const submittedAtUtc = timestamp ? timestamp.toISOString() : new Date().toISOString();
  const responseId = response.getId();

  const orderedAnswers = {};
  for (const itemId of Object.keys(answersByItem).sort()) {
    orderedAnswers[itemId] = answersByItem[itemId];
  }
  const snapshotObject = {
    response_id: responseId,
    submitted_at_utc: submittedAtUtc,
    form_id: form.getId(),
    packet_id: config.packet_id,
    batch_id: config.batch_id,
    variant_id: config.variant_id,
    reviewer_cohort: config.reviewer_cohort,
    language: config.language,
    reviewer_context: reviewerContext,
    answers_by_item_id: orderedAnswers,
  };
  const snapshotJson = JSON.stringify(snapshotObject);

  return {
    response_id: responseId,
    submitted_at_utc: submittedAtUtc,
    answers_by_item_id: answersByItem,
    reviewer_context: reviewerContext,
    optional_comment: optionalComment,
    snapshot_json: snapshotJson,
    sha256: sha256Hex_(snapshotJson),
  };
}

function ensureBackupLedgerRow_(payload, config) {
  const spreadsheet = SpreadsheetApp.openById(config.backup_spreadsheet_id);
  const backup = spreadsheet.getSheetByName(PAUL_BACKUP_SHEET);
  if (!backup) {
    throw new Error(`Missing ${PAUL_BACKUP_SHEET} sheet.`);
  }
  if (sheetContainsResponseId_(backup, payload.response_id)) {
    return;
  }
  backup.appendRow([
    payload.response_id,
    payload.submitted_at_utc,
    config.packet_id,
    config.batch_id,
    config.variant_id,
    config.reviewer_cohort,
    config.language,
    payload.reviewer_context,
    payload.snapshot_json,
    payload.sha256,
    new Date().toISOString(),
  ]);
}

function ensureNormalizedRows_(payload, config) {
  const spreadsheet = SpreadsheetApp.openById(config.spreadsheet_id);
  const normalized = spreadsheet.getSheetByName(PAUL_NORMALIZED_SHEET);
  if (!normalized) {
    throw new Error(`Missing ${PAUL_NORMALIZED_SHEET} sheet.`);
  }
  if (sheetContainsResponseId_(normalized, payload.response_id)) {
    return;
  }

  const rows = [];
  for (const itemId of Object.keys(config.choice_item_to_comparison)) {
    const comparisonId = config.choice_item_to_comparison[itemId];
    const choice = payload.answers_by_item_id[itemId];
    if (!choice) {
      throw new Error(`Required comparison ${comparisonId} has no recorded choice.`);
    }
    rows.push([
      payload.response_id,
      payload.submitted_at_utc,
      config.packet_id,
      config.batch_id,
      config.variant_id,
      config.reviewer_cohort,
      config.language,
      comparisonId,
      choice,
      payload.reviewer_context,
      payload.optional_comment,
    ]);
  }

  if (rows.length > 0) {
    normalized.getRange(normalized.getLastRow() + 1, 1, rows.length, rows[0].length)
        .setValues(rows);
  }
}

function sheetContainsResponseId_(sheet, responseId) {
  const lastRow = sheet.getLastRow();
  if (lastRow <= 1) {
    return false;
  }
  const responseIds = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  return responseIds.some((row) => row[0] === responseId);
}

function sha256Hex_(value) {
  const digest = Utilities.computeDigest(
      Utilities.DigestAlgorithm.SHA_256,
      value,
      Utilities.Charset.UTF_8,
  );
  return digest.map((byte) => {
    const unsigned = (byte + 256) % 256;
    return unsigned.toString(16).padStart(2, '0');
  }).join('');
}

function ensureRecoveryTrigger_() {
  const exists = ScriptApp.getProjectTriggers().some(
      (trigger) => trigger.getHandlerFunction() === PAUL_RECOVERY_HANDLER,
  );
  if (!exists) {
    ScriptApp.newTrigger(PAUL_RECOVERY_HANDLER).timeBased().everyHours(1).create();
  }
}

function recoverPaulHumanEvalResponses() {
  const properties = PropertiesService.getScriptProperties().getProperties();
  const recovered = [];
  for (const key of Object.keys(properties).sort()) {
    if (!key.startsWith(PAUL_FORM_PROPERTY_PREFIX)) {
      continue;
    }
    const formId = key.slice(PAUL_FORM_PROPERTY_PREFIX.length);
    const config = JSON.parse(properties[key]);
    const form = FormApp.openById(formId);
    const lock = LockService.getScriptLock();
    lock.waitLock(30000);
    try {
      for (const response of form.getResponses()) {
        persistPaulHumanEvalResponse_(form, response, config);
      }
      maybeCloseSandboxForm_(form, config);
    } finally {
      lock.releaseLock();
    }
    recovered.push({
      packet_id: config.packet_id,
      form_id: formId,
      response_count: form.getResponses().length,
    });
  }
  console.log(JSON.stringify(recovered, null, 2));
  return recovered;
}

function maybeCloseSandboxForm_(form, config) {
  const target = config.sandbox_auto_close_after_submissions;
  if (config.environment !== 'sandbox' || target === null || target === undefined) {
    return;
  }
  if (!Number.isInteger(target) || target < 1) {
    throw new Error('Invalid sandbox auto-close target in runtime config.');
  }
  if (form.getResponses().length >= target) {
    form
        .setAcceptingResponses(false)
        .setCustomClosedFormMessage(
            'This sandbox form has reached its test response target. Thank you.',
        );
  }
}

function verifyPaulHumanEvalSandboxForms() {
  const properties = PropertiesService.getScriptProperties().getProperties();
  const results = [];
  for (const key of Object.keys(properties).sort()) {
    if (!key.startsWith(PAUL_FORM_PROPERTY_PREFIX)) {
      continue;
    }
    const config = JSON.parse(properties[key]);
    if (config.environment !== 'sandbox') {
      continue;
    }
    const formId = key.slice(PAUL_FORM_PROPERTY_PREFIX.length);
    const form = FormApp.openById(formId);
    const responseIds = form.getResponses().map((response) => response.getId());

    const spreadsheet = SpreadsheetApp.openById(config.spreadsheet_id);
    const normalized = spreadsheet.getSheetByName(PAUL_NORMALIZED_SHEET);
    const normalizedIds = uniqueResponseIds_(normalized);

    const backupSpreadsheet = SpreadsheetApp.openById(config.backup_spreadsheet_id);
    const backup = backupSpreadsheet.getSheetByName(PAUL_BACKUP_SHEET);
    const backupIds = uniqueResponseIds_(backup);

    const missingNormalized = responseIds.filter((id) => !normalizedIds.includes(id));
    const missingBackup = responseIds.filter((id) => !backupIds.includes(id));
    const checksumFailures = backupChecksumFailures_(backup);

    results.push({
      packet_id: config.packet_id,
      form_id: formId,
      published: form.isPublished(),
      accepting_responses: form.isAcceptingResponses(),
      collects_email: form.collectsEmail(),
      allows_response_edits: form.canEditResponse(),
      response_count: responseIds.length,
      normalized_unique_responses: normalizedIds.length,
      backup_unique_responses: backupIds.length,
      normalized_rows: Math.max(0, normalized.getLastRow() - 1),
      missing_normalized_count: missingNormalized.length,
      missing_backup_count: missingBackup.length,
      backup_checksum_failures: checksumFailures,
      recovery_trigger_installed: recoveryTriggerInstalled_(),
    });
  }
  console.log(JSON.stringify(results, null, 2));
  return results;
}

function uniqueResponseIds_(sheet) {
  if (!sheet || sheet.getLastRow() <= 1) {
    return [];
  }
  const values = sheet.getRange(2, 1, sheet.getLastRow() - 1, 1).getValues();
  return [...new Set(values.map((row) => row[0]).filter((value) => value))];
}

function backupChecksumFailures_(sheet) {
  if (!sheet || sheet.getLastRow() <= 1) {
    return 0;
  }
  const rows = sheet.getRange(2, 9, sheet.getLastRow() - 1, 2).getValues();
  let failures = 0;
  for (const row of rows) {
    const snapshotJson = String(row[0] || '');
    const checksum = String(row[1] || '');
    if (!snapshotJson || !checksum || sha256Hex_(snapshotJson) !== checksum) {
      failures += 1;
    }
  }
  return failures;
}

function recoveryTriggerInstalled_() {
  return ScriptApp.getProjectTriggers().some(
      (trigger) => trigger.getHandlerFunction() === PAUL_RECOVERY_HANDLER,
  );
}

function closePaulHumanEvalSandboxForms() {
  const properties = PropertiesService.getScriptProperties().getProperties();
  const closed = [];
  for (const key of Object.keys(properties).sort()) {
    if (!key.startsWith(PAUL_FORM_PROPERTY_PREFIX)) {
      continue;
    }
    const config = JSON.parse(properties[key]);
    if (config.environment !== 'sandbox') {
      continue;
    }
    const formId = key.slice(PAUL_FORM_PROPERTY_PREFIX.length);
    const form = FormApp.openById(formId);
    form
        .setAcceptingResponses(false)
        .setCustomClosedFormMessage('This sandbox evaluation is closed. Thank you.');
    closed.push({packet_id: config.packet_id, form_id: formId});
  }
  console.log(JSON.stringify(closed, null, 2));
  return closed;
}

function createPaulReviewerPanelRegistrationForm() {
  const properties = PropertiesService.getScriptProperties();
  const existingId = properties.getProperty(PAUL_PANEL_FORM_PROPERTY);
  if (existingId) {
    const existing = FormApp.openById(existingId);
    return reviewerPanelDescriptor_(existing);
  }

  const form = FormApp.create('Join the PAUL Open reviewer panel', false);
  form
      .setDescription(
          'Optional: join our reviewer panel for future short AI-response evaluations. ' +
          'This registration is kept separate from your evaluation judgments.',
      )
      .setCollectEmail(false)
      .setAllowResponseEdits(false)
      .setLimitOneResponsePerUser(false)
      .setPublishingSummary(false)
      .setShowLinkToRespondAgain(false)
      .setShuffleQuestions(false)
      .setConfirmationMessage('Thank you. We will only contact you for PAUL Open reviews.')
      .setAcceptingResponses(false);

  form.addTextItem()
      .setTitle('Email address')
      .setRequired(true);
  form.addMultipleChoiceItem()
      .setTitle('Which best describes you?')
      .setChoiceValues([
        'Student',
        'Teacher / educator',
        'Researcher / scientist / engineer',
        'Other working professional',
        'General user',
        'Prefer not to say',
      ])
      .setRequired(true);
  form.addCheckboxItem()
      .setTitle('Which languages could you confidently review?')
      .setChoiceValues([
        'English',
        'Hindi',
        'Bengali',
        'Assamese',
        'Punjabi',
        'Tamil',
        'Telugu',
        'Kannada',
        'Malayalam',
        'Gujarati',
        'Marathi',
        'Odia',
        'Other',
      ])
      .setRequired(true);
  form.addCheckboxItem()
      .setTitle('Which areas could you confidently review?')
      .setChoiceValues([
        'General clarity and helpfulness',
        'Teaching and tutoring',
        'Physics',
        'Chemistry',
        'Biology',
        'Mathematics',
        'Research / technical writing',
        'Translation',
        'Other',
      ])
      .setRequired(true);
  form.addMultipleChoiceItem()
      .setTitle('May we contact you for future PAUL Open evaluation studies?')
      .setChoiceValues(['Yes', 'No'])
      .setRequired(true);
  form.addParagraphTextItem()
      .setTitle('Optional: Anything else about the kinds of reviews you can help with?')
      .setRequired(false);

  const spreadsheet = SpreadsheetApp.create('PAUL Open Reviewer Panel — Registration');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheet.getId());
  properties.setProperty(PAUL_PANEL_FORM_PROPERTY, form.getId());
  form.setPublished(true).setAcceptingResponses(true);
  return reviewerPanelDescriptor_(form);
}

function reviewerPanelDescriptor_(form) {
  return {
    form_id: form.getId(),
    respondent_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    note: 'Keep this contact registry separate from evaluation response data.',
  };
}

function validatePacket_(packet) {
  if (!packet || packet.environment !== 'sandbox') {
    throw new Error('H2 runtime accepts sandbox packets only.');
  }
  if (!Array.isArray(packet.comparisons) || packet.comparisons.length < 1) {
    throw new Error('Packet must contain at least one comparison.');
  }
  if (packet.comparisons.length > 4) {
    throw new Error('Packet exceeds the four-comparison UX hard cap.');
  }
  if (packet.settings.collect_email !== false ||
      packet.settings.allow_response_edits !== false ||
      packet.settings.limit_one_response_per_user !== false ||
      packet.settings.publish_response_summary !== false ||
      packet.settings.show_submit_another_response_link !== false ||
      packet.settings.shuffle_questions !== false ||
      packet.settings.progress_bar !== true) {
    throw new Error('Packet settings violate the frozen low-friction/blinding protocol.');
  }
  if (!packet.reviewer_context || packet.reviewer_context.enabled !== true) {
    throw new Error('Packet must define exactly one reviewer-context question.');
  }
  if (!Array.isArray(packet.reviewer_context.choices) ||
      packet.reviewer_context.choices.length < 2) {
    throw new Error('Reviewer-context question must contain multiple-choice options.');
  }
  for (const comparison of packet.comparisons) {
    if (!Array.isArray(comparison.choices) || comparison.choices.length !== 5) {
      throw new Error('Each comparison must expose exactly five frozen preference choices.');
    }
    if (comparison.required !== true) {
      throw new Error('Each preference question must be required.');
    }
  }
}
