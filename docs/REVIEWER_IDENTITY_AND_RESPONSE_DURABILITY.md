# PAUL Open — Reviewer Identity and Response Durability Policy

**Status:** protocol extension for H2/H3 human evaluation.  
**Scope:** Google Forms human evaluation only.  
**Research principle:** collect only reviewer information that improves interpretation of judgments, and keep contact identity separate from evaluation data.

## 1. Identity separation

The evaluation Form remains anonymous by default:

- do not collect respondent email;
- do not collect name;
- do not ask for a free-text biography;
- do not expose model/checkpoint identities, benchmark IDs, automated scores, or internal case IDs.

If PAUL Open maintains a recurring reviewer panel, contact details are collected in a **separate opt-in reviewer registration Form**. That registry is operational contact data, not evaluation data. Evaluation records must not contain a reviewer email or registration-form response ID.

This separation prevents contact identity from becoming part of the model-comparison dataset and reduces unnecessary personally identifiable information in research exports.

## 2. Minimal reviewer context

Reviewer context is collected only when it improves interpretation of the task and should be one short multiple-choice question at most. It is placed **after the A/B comparisons** to reduce priming.

- **general_user:** optional broad role category;
- **educator:** optional teaching-experience category;
- **bilingual:** required self-assessed ability in the requested language, including an explicit "cannot confidently judge" option;
- **stem_capable / domain_expert:** required self-assessed topic-judging confidence, including a "cannot confidently judge" option.

Do not use job title as a proxy for language competence or scientific expertise. The metadata should describe the competence relevant to the actual judgment.

## 3. Separate reviewer-panel registration

A reviewer may voluntarily join a recurring PAUL Open review panel through a different Form. The panel Form may collect:

- email address;
- broad role;
- languages the reviewer can confidently evaluate;
- areas the reviewer can confidently evaluate;
- permission to be contacted for future studies;
- optional notes.

The panel Form must not ask which model a reviewer preferred and must not contain evaluation comparison IDs. Its response spreadsheet must remain separate from evaluation response spreadsheets.

## 4. Response durability architecture

No software system can guarantee literal zero-loss under every possible account, provider, or deletion failure. PAUL Open therefore uses redundant, recoverable storage so a single trigger or normalization failure cannot silently erase a valid human judgment.

For every evaluation Form submission, the system retains four recoverable representations:

1. **Google Form response store** — provider-native source response;
2. **linked Google response Sheet** — provider-generated raw response destination;
3. **PAUL Normalized sheet** — one structured row per comparison judgment;
4. **PAUL Backup ledger spreadsheet** — a second spreadsheet containing an append-only canonical response snapshot and SHA-256 checksum.

The Form response itself is the recovery source of truth. If a submit trigger fails after Google accepted the Form, an hourly recovery job re-reads Form responses and repairs missing normalized or backup rows idempotently.

## 5. Idempotency and concurrency

Normalization and backup use the Google Forms `FormResponse` ID as the immutable submission key.

- repeated trigger execution must not duplicate a submission;
- a script lock protects concurrent writes;
- primary normalization and backup are checked independently, so one destination can be repaired even if the other already contains the response;
- the backup ledger stores a canonical JSON snapshot and SHA-256 digest for integrity checking;
- recovery is allowed to replay accepted Form responses but never invents a submission.

## 6. Monitoring and repair

The Apps Script runtime provides:

- `verifyPaulHumanEvalSandboxForms()` — compares Form response count, normalized response IDs and backup response IDs;
- `recoverPaulHumanEvalResponses()` — repairs missing normalized/backup representations from Form responses;
- an hourly installable recovery trigger created once per Apps Script project;
- `closePaulHumanEvalSandboxForms()` — closes remaining disposable sandbox Forms safely.

A sandbox cannot be considered complete while any accepted Form response is missing from either normalized storage or the backup ledger.

## 7. Data-handling rules

- Never commit respondent URLs, Form IDs, Sheet IDs, emails, raw comments, or reviewer-panel contact data to the public repository.
- Human comments are development evidence, not direct training examples.
- If a DHE judgment influences training design, associated cases are development-exposed.
- Sealed assurance prompts and outputs remain outside the public repository.
- Contact registry exports and evaluation exports remain physically separate.

## 8. UX budget

The default evaluation remains three A/B comparisons plus at most one short reviewer-context question and one optional final comment. Reviewer metadata must never turn the evaluation into a demographic survey.

The target remains a normal completion time of roughly 2–4 minutes on mobile or desktop.
