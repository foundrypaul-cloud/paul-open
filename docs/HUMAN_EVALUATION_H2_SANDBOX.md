# PAUL Open — Human Evaluation H2 Google Forms Sandbox

**Status:** implementation verified; Google-account sandbox deployment is the remaining H2 acceptance step.  
**Research data:** synthetic/disposable only. No PAUL benchmark, DHE, SHAE, SFT/DPO identity map, or sealed prompt is used here.

## Purpose

H2 verifies the *measurement instrument* before any real human-evaluation material is exposed. The sandbox should prove that a reviewer can open one short Google Form, compare three response pairs, submit once, and have the answers normalized correctly without seeing model/checkpoint identities.

The Google account is only a presentation/collection surface. Research blinding and A/B assignment are produced upstream by H1.

## What is already verified in CI

The repository verifies the H2 implementation without Google credentials or external API calls:

- H1 and H2 unit tests;
- deterministic packet construction;
- default three-comparison form size and four-comparison hard cap;
- grouping by reviewer cohort and language before form chunking;
- the frozen five pairwise choices;
- technical-term-aware bilingual reviewer instruction;
- no email collection, no response-summary publication, no edit link, no submit-another link;
- refusal to consume known H1 private-map fields;
- synthetic end-to-end CLI packet generation;
- Google Apps Script manifest JSON validity;
- Google Apps Script JavaScript syntax;
- duplicate form-submit normalization protection;
- sandbox-only submission-count closing.

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
5. Record the returned respondent URL, form ID, linked Sheet URL, and packet ID in a private sandbox log. Do not commit account-specific IDs or URLs.

The runtime creates the Form unpublished, finishes all questions/settings, links the Sheet, installs the submit trigger, and only then publishes/opens the Form.

## Sandbox reviewer experience

The reviewer should see only:

- a short non-technical introduction;
- three comparisons;
- Question;
- Response A;
- Response B;
- one required preference choice per comparison;
- one optional comment at the end.

The preference choices are exactly:

- Response A is better
- Response B is better
- They are about equally good
- Neither response is good
- I'm not sure / I can't judge this

No model names, SFT/DPO labels, benchmark IDs, automated scores, or software terminology should be visible.

## Linked Sheet behavior

Each created sandbox form gets a linked spreadsheet. In addition to Google's raw response destination, the script creates:

- `PAUL Metadata` — packet/form metadata and form-item-to-comparison mapping;
- `PAUL Normalized` — one normalized row per comparison judgment.

Normalized fields are:

`response_id`, `submitted_at_utc`, `packet_id`, `batch_id`, `variant_id`, `reviewer_cohort`, `language`, `comparison_id`, `choice`, `optional_comment`.

The form-submit trigger uses the Google Form response ID to make normalization idempotent: a repeated trigger execution must not duplicate the same submission.

### Why the trigger test needs real respondent submissions

Google Apps Script explicitly documents that script executions and API requests do **not** fire installable triggers; calling `FormResponse.submit()` programmatically therefore does not exercise the real Forms submit trigger. H2 must use genuine submissions through the respondent URL for its final trigger/normalization acceptance test. This is intentional and prevents a false-positive sandbox validation.

## H2 acceptance test

H2 is complete only after all of the following pass on a disposable Google Form:

1. Form opens correctly on desktop and mobile.
2. Exactly three synthetic comparisons are visible.
3. No model/checkpoint identity or research-internal case ID is visible.
4. Email is not collected.
5. Response summary is not published.
6. Response editing and submit-another links are disabled.
7. Three real respondent submissions create nine normalized comparison rows with three unique response IDs.
8. Replaying/duplicating a trigger does not duplicate normalized rows.
9. After the configured third submission, the sandbox form stops accepting responses.
10. `verifyPaulHumanEvalSandboxForms()` reports the expected state.
11. `closePaulHumanEvalSandboxForms()` safely closes any remaining sandbox forms.

If any item fails, fix H2 only. Do not expose DHE/SHAE material and do not train a model.

## H3 entry gate

Only after H2 passes may PAUL Open begin H3 with 5–10 disposable non-research comparisons and trusted reviewers to measure completion time, mobile readability, confusion, and mapping integrity.

H3 must still use disposable content. Real DHE begins only after the UX and normalization pipeline are demonstrated to work.
