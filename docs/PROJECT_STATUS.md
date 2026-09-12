# PAUL Open — Current Research Status

**Status date:** 2026-09-12  
**Public research repository:** `foundrypaul-cloud/paul-open`  
**Public website:** https://open.paulfoundry.com/

This document is the concise public status layer for the repository. Detailed historical evidence remains in the experiment-specific documents and immutable artifacts.

## Current position

PAUL Open has completed the H4 Development Human Evaluation (DHE) pilot for the frozen SFT reference checkpoint versus DPO V2 Corrective on `google/gemma-4-E4B-it`.

The current research conclusion is:

> **SFT remains the safer reference checkpoint. DPO V2 Corrective is technically valid and shows meaningful positive signals in some H4 strata, but H4 is mixed and does not establish broad superiority. DPO V2 is not promoted over SFT on H4 evidence alone.**

H2 infrastructure, H3 UX/durability, and H4 DHE are complete. SHAE remains sealed and has not started.

## Step 2 — DPO V2 Corrective

Immutable experiment freeze:

- branch: `research-freeze/step2-dpo-v2-20260909`
- SHA: `ac899e879f930f25b2081550bd8c5dd5c983df35`

The final DPO V2 production run established technical validity, including:

- 14-record corrective preference dataset;
- two-GPU policy/reference topology on Tesla T4;
- 4-bit NF4 base models;
- 516 / 516 intended trainable tensors changed;
- optimizer/placement/reference gates passed;
- external-reference mathematical equivalence passed at the validated boundary;
- final train loss `0.687744140625`;
- runtime `238.58 s`.

See [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md).

## Earlier behavioral evidence

The existing 50-case SFT-vs-DPO V2 comparison remains **diagnostic only** because DPO V2 source material overlaps the canonical suite at exact, content, template, and concept levels.

Its heuristic aggregate therefore is not clean held-out evidence and cannot establish superiority.

See [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md).

## Human evaluation milestones

### H2 — complete

H2 formally validated the live Google Forms infrastructure, linked raw responses, normalized rows, independent backup ledgers, checksums, idempotent recovery, and desktop/mobile opening. H2 is infrastructure evidence, not model-preference evidence.

### H3 — complete

H3 validated the trusted-reviewer UX and durability path using disposable non-research material. It passed the frozen acceptance criteria before H4 opened.

### H4 — DHE complete; decision recorded

Batch: `HEB1-E928B35C90D7`

- source cases: 6
- eligible cases: 5
- identical pair excluded: 1
- complementary reviewer-facing forms: 10
- initial judgments: 15
- adaptive follow-up judgments: 6
- final judgments: **21**

Final case reviewer totals:

- General: 3
- STEM: 5
- Educator: 5
- Hindi: 3
- Bengali: 5

The response-durability audit passed before unblinding: 21 raw responses, 21 normalized response IDs, and 21 matching independent backup-ledger IDs, with SHA-256 and backup-write timestamps present for every response.

The judgment set was analysis-locked before the private A/B mapping was read. Controlled unblinding used the private mapping retained in the private Kaggle generation output; the private mapping itself is not committed.

### H4 aggregate result

| Outcome | Count |
|---|---:|
| DPO V2 preferred | 7 |
| SFT preferred | 9 |
| About equal | 2 |
| Neither good | 0 |
| Not sure / unable to judge | 3 |

Among 16 decisive preference judgments, DPO V2 received **43.75%** and SFT **56.25%**.

Case majorities:

- General — SFT
- STEM — DPO V2
- Educator — SFT
- Hindi — DPO V2
- Bengali — SFT

SFT wins 3 of 5 case majorities; DPO V2 wins 2 of 5. Mean descriptive modal-choice agreement is 80%.

A cluster bootstrap over the five cases produces wide intervals, as expected for such a small DHE pilot. H4 therefore remains diagnostic/development evidence rather than a superiority study.

See:

- [`H4_DHE_PILOT_V1_ANALYSIS_LOCK.md`](H4_DHE_PILOT_V1_ANALYSIS_LOCK.md)
- [`H4_DHE_PILOT_V1_RESULTS.md`](H4_DHE_PILOT_V1_RESULTS.md)
- [`HUMAN_EVALUATION_H4_DHE_PILOT.md`](HUMAN_EVALUATION_H4_DHE_PILOT.md)

## H4 decision

**Mixed; no DPO V2 promotion.**

SFT remains the reference checkpoint. DPO V2 remains a valid experimental checkpoint with positive STEM and Hindi signals, while General, Educator, and Bengali are development areas for diagnosis.

The H4 accessibility finding is also retained: future evaluator-interface work should preserve keyboard/screen-reader compatibility and evaluate optional multilingual text-to-speech assistance.

## Immediate next research steps

H4 itself has no remaining blocker. The next work should be explicitly chosen as one of two paths:

1. **DHE follow-up/model development:** use H4 findings to diagnose and improve the experimental checkpoint, with new development material and a new evaluation cycle; or
2. **future assurance preparation:** freeze a future candidate first, then separately design SHAE without exposing or contaminating sealed assurance material.

Do not start SHAE merely because H4 is complete. SHAE requires its own frozen-candidate and sealed-assurance boundary.

## Public website state

The website is a presentation layer, not a second research database. It should consume:

- [`../public/research-status.json`](../public/research-status.json)
- [`../public/human-evaluation.json`](../public/human-evaluation.json)

No public human-evaluation round is accepting responses. Reviewer links, response sheets, private A/B maps, and SHAE material must remain non-public.

## Claim boundary

### Supported

- DPO V2 is technically valid;
- the earlier 50-case comparison is contaminated and diagnostic;
- H2, H3, and H4 are complete;
- H4 DHE produced 21 judgments across five eligible development cases;
- H4 aggregate result was 7 DPO-preferred, 9 SFT-preferred, 2 equal, 0 neither, 3 unable-to-judge;
- DPO V2 won the STEM and Hindi H4 case majorities;
- SFT won General, Educator, and Bengali;
- H4 result is mixed and no DPO V2 promotion was made;
- SFT remains the safer reference checkpoint.

### Not supported

- DPO V2 is broadly superior to SFT;
- H4 is final assurance;
- the earlier contaminated 50-case delta proves overall progress or regression;
- SHAE has started or passed;
- H4 development cases can later be reclassified as untouched assurance evidence.

## Canonical detail documents

- [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md)
- [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md)
- [`HUMAN_EVALUATION_PROTOCOL.md`](HUMAN_EVALUATION_PROTOCOL.md)
- [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md)
- [`HUMAN_EVALUATION_H3_PILOT.md`](HUMAN_EVALUATION_H3_PILOT.md)
- [`HUMAN_EVALUATION_H4_DHE_PILOT.md`](HUMAN_EVALUATION_H4_DHE_PILOT.md)
- [`H4_DHE_PILOT_V1_ANALYSIS_LOCK.md`](H4_DHE_PILOT_V1_ANALYSIS_LOCK.md)
- [`H4_DHE_PILOT_V1_RESULTS.md`](H4_DHE_PILOT_V1_RESULTS.md)
- [`HUMAN_EVALUATION_WORKFLOW.md`](HUMAN_EVALUATION_WORKFLOW.md)
