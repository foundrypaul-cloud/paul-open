# PAUL Open — Human Evaluation H3 Dry-Run Pilot

**Status:** live pilot instruments created; trusted-reviewer responses pending.  
**Started:** 2026-09-10  
**Research material:** disposable non-research content only. No PAUL benchmark, DHE, SHAE, SFT/DPO identity map, or sealed prompt is used here.

## Purpose

H3 validates the reviewer experience and operating path after H2 infrastructure acceptance, before any real development or sealed-assurance human-evaluation material is exposed.

H3 is not a model-quality experiment. Its outputs must not be used to claim that SFT, DPO V2, or any other checkpoint is better.

## Pilot design

The live H3 pilot uses two short counterbalanced Google Forms:

- **Form A1:** three disposable comparisons in the primary A/B presentation;
- **Form B1:** the same three disposable comparisons with A/B responses swapped.

Across the two forms, H3 exercises six displayed comparison instances while retaining only three underlying disposable cases. This is intentional: H3 is testing presentation, counterbalancing, reviewer comprehension and data handling, not estimating model preference.

Each form contains:

1. exactly three pairwise comparisons;
2. the frozen five response choices from protocol v1;
3. a required device question;
4. a required completion-time bucket;
5. a required readability/navigation question;
6. a required A/B-confusion question;
7. one optional free-text UX comment.

Email collection is off. The forms are published and accepting responses only for a small trusted-reviewer pilot. Respondent URLs are intentionally not stored in the public repository.

## Disposable cases

### H3-DISP-001 — thermal-conduction explanation

Prompt asks why a metal spoon can feel colder than a wooden spoon at the same room temperature. One response correctly explains faster heat conduction from the hand; the alternate response incorrectly attributes the sensation to metal simply being at a lower indoor temperature.

### H3-DISP-002 — short study-planning advice

Prompt asks how to use 90 minutes before a quiz. One response proposes targeted active recall, practice, error review and a final summary; the alternate response recommends rereading the full chapter and highlighting.

### H3-DISP-003 — polite rewrite

Prompt asks for a polite rewrite of a short scheduling message. Both alternatives are acceptable but differ slightly in tone and wording, giving a deliberately less-obvious preference case.

These cases are disposable and must never be promoted into DHE or SHAE evidence.

## Counterbalancing map

The H3 mapping is non-secret because the content is disposable and non-research:

| Case | Form A1 | Form B1 |
|---|---|---|
| H3-DISP-001 | A = technically correct; B = incorrect | A = incorrect; B = technically correct |
| H3-DISP-002 | A = active-recall plan; B = rereading plan | A = rereading plan; B = active-recall plan |
| H3-DISP-003 | A = concise polite rewrite; B = more apologetic rewrite | A = more apologetic rewrite; B = concise polite rewrite |

The H3 acceptance analysis should verify that any preference-pattern interpretation is invariant to which response happened to be displayed as A or B.

## H3 acceptance criteria

H3 passes only when all of the following are satisfied:

1. At least **5 trusted-reviewer form completions** are collected in total, with both A1 and B1 represented.
2. At least one genuine completion is from a desktop/laptop and at least one from a mobile phone.
3. Median self-reported completion time is **4 minutes or less**.
4. No systematic readability/navigation problem is observed. A single isolated minor-friction response may be inspected rather than treated as automatic failure.
5. No systematic A/B-format confusion is observed. Any `Yes` response or repeated `A little` response requires comment review and, if necessary, a UX correction before H3 is accepted.
6. All three preference questions are required and use exactly the frozen five-choice vocabulary.
7. Email collection remains off and no model/checkpoint/research identity is exposed.
8. Counterbalancing integrity is verified: the A1/B1 content swap matches the table above with no accidental prompt/response mismatch.
9. Duplicate-response behavior is inspected. Duplicate submissions must remain identifiable as separate native Form responses; downstream normalization must not accidentally duplicate a single response ID.
10. The established H2 durability path is exercised for H3 before final acceptance: native response retention, normalized rows, backup-ledger representation, checksum population and idempotent recovery must still behave correctly on disposable H3 material.
11. No H3 material is treated as DHE or SHAE evidence.

## Two-layer execution note

The connected Google Forms API was used to create the live A1/B1 UX instruments directly. This is useful for immediate reviewer UX testing, but that API path does not attach the repository Apps Script normalization/backup runtime by itself.

Therefore H3 acceptance is intentionally split into two evidence layers:

- **UX evidence:** live A1/B1 reviewer submissions, device coverage, completion time, readability and confusion;
- **durability evidence:** the same disposable H3 design exercised through the established repository Apps Script/Sheets path before H3 is declared complete.

This distinction prevents a convenient provider shortcut from being mistaken for end-to-end acceptance.

## Decision rule

If all acceptance criteria pass, mark H3 complete and open H4 DHE preparation. If any UX or durability criterion fails, fix only the human-evaluation operating path and rerun H3 with disposable material. Do not expose DHE/SHAE prompts and do not train a new model merely to resolve an evaluation-infrastructure issue.

## Claim boundary

Supported while H3 is collecting:

- H2 is complete;
- H3 live disposable pilot instruments exist and are accepting trusted-reviewer responses;
- H3 is testing UX, counterbalancing and data handling only.

Not supported until acceptance:

- H3 is complete;
- DHE may begin;
- SHAE may begin;
- any H3 response demonstrates model superiority.
