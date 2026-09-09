# PAUL Open — Human Evaluation H2 Google Forms Sandbox

**Status:** implementation verified in CI; Google-account sandbox deployment is the remaining H2 acceptance step.  
**Research data:** synthetic/disposable only. No PAUL benchmark, DHE, SHAE, SFT/DPO identity map, or sealed prompt is used here.

## Purpose

H2 verifies the measurement instrument before any real human-evaluation material is exposed. The sandbox should prove that a reviewer can open one short Google Form, compare three response pairs, submit once, and have the answers retained and normalized correctly without seeing model/checkpoint identities.

The Google account is only a presentation/collection surface. Research blinding and A/B assignment are produced upstream by H1.

## Reviewer identity policy

The evaluation Form itself remains anonymous:

- no email collection;
- no name collection;
- no free-text biography;
- no model/checkpoint identity;
- no benchmark/internal case IDs.

Each form may include **one short reviewer-context question after the A/B comparisons**. General-user and educator context is optional. Bilingual and expert forms require a directly relevant self-assessment, including a clear "cannot confidently judge" option.

A separate opt-in `Join the PAUL Open reviewer panel` Form may collect email, broad role, languages, review areas and contact permission. That contact registry is physically separate from evaluation response data and contains no model preference or comparison IDs.

See `docs/REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md`.

## What is verified in CI

The repository verifies the H2 implementation without Google credentials or external API calls:

- H1 and H2 unit tests;
- deterministic packet construction;
- default three-comparison form size and four-comparison hard cap;
- grouping by reviewer cohort and language before form chunking;
- the frozen five pairwise choices;
- technical-term-aware bilingual reviewer instruction;
- one-question reviewer-context budget;
- no evaluation-form email collection, response-summary publication, edit link, or submit-another link;
- refusal to consume known H1 private-map fields;
- synthetic end-to-end CLI packet generation;
- Google Apps Script manifest JSON validity;
- Google Apps Script JavaScript syntax;
- idempotent normalization by Google Form response ID;
- second backup-ledger spreadsheet with SHA-256 integrity checks;
- hourly self-healing recovery from accepted Google Form responses;
- script-lock protection against concurrent duplicate writes;
- sandbox-only submission-count closing;
- separate reviewer-panel registration function.

## Build the disposable sandbox payload

From the repository root:

```bash
PYTHONPATH=src python scripts/build_google_forms_sandbox.py \
  --variant tests/fixtures/human_eval_sandbox_variant.json \
  --output-dir outputs/human_eval/google_forms_sandbox \
  --auto-close-after-submissions 3
```

This creates a gitignored sandbox package including `Payload.gs`. The fixture is synthetic and must never be replaced with a sealed assurance prompt.

## One-time Google Apps Script deployment

Use a standalone Google Apps Script project owned by the research account.

1. Add `tools/google_forms/Code.gs` as `Code.gs`.
2. Add the generated `Payload.gs` as a second script file.
3. Use the OAuth scopes in `tools/google_forms/appsscript.json`.
4. Run `createPaulHumanEvalSandboxForms()` and approve the requested Google Forms, Sheets, and trigger permissions.
5. Optionally run `createPaulReviewerPanelRegistrationForm()` once to create the separate opt-in contact registry.
6. Record returned respondent URLs, form IDs and Sheet URLs in a private sandbox log. Do not commit account-specific IDs, URLs, emails, or reviewer responses.

The runtime creates each evaluation Form unpublished, finishes all questions/settings, creates the primary response spreadsheet and independent backup ledger, links the response destination, installs the submit trigger, installs one hourly recovery trigger, and only then publishes/opens the Form.

## Sandbox reviewer experience

The reviewer should see only:

- a short non-technical introduction;
- three comparisons;
- Question;
- Response A;
- Response B;
- one required preference choice per comparison;
- one short reviewer-context question after the comparisons;
- one optional comment at the end.

The preference choices are exactly:

- Response A is better
- Response B is better
- They are about equally good
- Neither response is good
- I'm not sure / I can't judge this

No model names, SFT/DPO labels, benchmark IDs, automated scores, or software terminology should be visible.

## Response durability

A valid evaluation response is retained in four recoverable forms:

1. Google Forms native response store;
2. Google's linked raw response Sheet;
3. `PAUL Normalized` in the primary evaluation spreadsheet;
4. `PAUL Backup Ledger` in a second spreadsheet with a canonical JSON snapshot and SHA-256 checksum.

The native Google Form response is the recovery source of truth. If the submit trigger fails after Google accepts a response, `recoverPaulHumanEvalResponses()` replays accepted Form responses idempotently and repairs missing normalized or backup rows. One hourly installable recovery trigger is created automatically.

A single trigger failure therefore must not silently lose an accepted response.

## Primary Sheet behavior

Each created sandbox form gets a linked spreadsheet. In addition to Google's raw response destination, the script creates:

- `PAUL Metadata` — packet/form metadata and form-item-to-comparison mapping;
- `PAUL Normalized` — one normalized row per comparison judgment.

Normalized fields are:

`response_id`, `submitted_at_utc`, `packet_id`, `batch_id`, `variant_id`, `reviewer_cohort`, `language`, `comparison_id`, `choice`, `reviewer_context`, `optional_comment`.

## Backup ledger behavior

Each evaluation Form also receives an independent backup spreadsheet containing `PAUL Backup Ledger` with:

`response_id`, `submitted_at_utc`, packet metadata, `reviewer_context`, canonical `snapshot_json`, `sha256`, and backup timestamp.

Primary normalization and backup are checked independently. If one exists and the other does not, recovery repairs only the missing representation.

## Reviewer-panel registration

`createPaulReviewerPanelRegistrationForm()` creates a completely separate optional registration Form with its own linked spreadsheet. It may collect:

- email address;
- broad role;
- languages the reviewer can confidently review;
- areas the reviewer can confidently review;
- permission to contact them again;
- optional notes.

The panel registry must never be joined into the human-evaluation judgment table by email. If a future study needs stable pseudonymous reviewer tracking, that must use a separately designed opaque reviewer-token process.

## H2 acceptance test

H2 is complete only after all of the following pass on a disposable Google Form:

1. Form opens correctly on desktop and mobile.
2. Exactly three synthetic comparisons are visible.
3. No model/checkpoint identity or research-internal case ID is visible.
4. Evaluation Form does not collect email or name.
5. Reviewer-context question is short, relevant, and placed after the comparisons.
6. Response summary is not published.
7. Response editing and submit-another links are disabled.
8. Three genuine respondent-link submissions create nine normalized comparison rows with three unique response IDs.
9. The same three response IDs exist in the independent backup ledger with valid SHA-256 checksums.
10. Replaying/duplicating a trigger does not duplicate normalized or backup rows.
11. Temporarily deleting one normalized or backup representation and running `recoverPaulHumanEvalResponses()` repairs it from the Form response.
12. After the configured third submission, the sandbox form stops accepting responses.
13. `verifyPaulHumanEvalSandboxForms()` reports zero missing normalized responses, zero missing backup responses, zero checksum failures, and an installed recovery trigger.
14. `closePaulHumanEvalSandboxForms()` safely closes any remaining sandbox forms.
15. If the reviewer-panel Form is created, its spreadsheet is separate and contains no evaluation comparison IDs.

If any item fails, fix H2 only. Do not expose DHE/SHAE material and do not train a model.

## Important testing note

The acceptance submissions must be genuine submissions through the respondent-facing Google Form URL. Programmatic Apps Script/API submissions do not reliably exercise the same installable form-submit trigger path and therefore cannot substitute for the end-to-end test.

## H3 entry gate

Only after H2 passes may PAUL Open begin H3 with 5–10 disposable non-research comparisons and trusted reviewers to measure completion time, mobile readability, confusion, and mapping integrity.

H3 must still use disposable content. Real DHE begins only after the UX, identity separation, normalization, backup and recovery pipeline are demonstrated to work.
