# PAUL Open — Current Research Status

**Status date:** 2026-09-10  
**Public research repository:** `foundrypaul-cloud/paul-open`  
**Public website:** https://open.paulfoundry.com/

This document is the concise public status layer for the repository. Detailed historical evidence remains in the experiment-specific documents and immutable artifacts.

## Current position

PAUL Open is currently in the evaluation-hardening stage after a technically successful DPO V2 Corrective run on `google/gemma-4-E4B-it`.

The correct research conclusion remains:

> **The SFT adapter remains the safer reference checkpoint. DPO V2 is technically valid and behaviorally informative, but superiority over SFT has not been established.**

H2 human-evaluation infrastructure is formally complete. H3 is now active as an internal/trusted-reviewer disposable UX and operating-path pilot. H3 does not compare PAUL model checkpoints and does not change the model-comparison conclusion above.

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

See [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md) for the reproducibility record.

## Behavioral evidence

The existing 50-case comparison between SFT and DPO V2 is **diagnostic only**.

Observed heuristic summary:

| Metric | SFT | DPO V2 |
|---|---:|---:|
| Mean heuristic rubric | 90.26 | 89.79 |
| Safety adherence | 100% | 100% |
| Mean latency | 37.60 s | 41.04 s |

The aggregate result is not the main conclusion. Paired review found both improvements and important regressions, including a Punjabi native-script failure and a scientific-mechanism regression.

More importantly, DPO V2 source material overlaps the canonical 50-case suite at exact, content, template, and concept levels. Therefore this comparison is not clean held-out evidence for DPO V2.

See [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md).

## Human evaluation — H2 complete

H2 was formally accepted on **2026-09-10** after repository implementation, live Google-account runtime, genuine respondent submissions, normalized and backup retention, controlled recovery, verifier rerun, closure, and desktop/mobile opening all passed.

H2 remains infrastructure evidence only. It is **not** human preference evidence for SFT versus DPO V2.

See [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md).

## Human evaluation — H3 active

H3 started on **2026-09-10**.

Two live Google Forms have been created for a small internal/trusted reviewer group:

- Form A1: three disposable comparisons;
- Form B1: the same three disposable comparisons with A/B presentation counterbalanced.

Together they exercise six displayed comparison instances across three underlying disposable non-research cases. Email collection is off. The live respondent links are intentionally not committed to the public repository.

Each live UX form also records:

- device class;
- self-reported completion-time bucket;
- readability/navigation friction;
- A/B-format confusion;
- one optional UX comment.

Repository-native H3 durability material is available at [`../tools/google_forms/H3DurabilityPayload.gs`](../tools/google_forms/H3DurabilityPayload.gs) so the previously accepted Apps Script normalization, backup-ledger, checksum and recovery path can be exercised on the same disposable design without introducing model data.

H3 acceptance requires at least 5 trusted-reviewer completions in total with both A1/B1 represented, desktop and mobile coverage, median completion time at or below 4 minutes, no systematic UX confusion/readability issue, correct counterbalancing, and a successful durability-path exercise. Full criteria are in [`HUMAN_EVALUATION_H3_PILOT.md`](HUMAN_EVALUATION_H3_PILOT.md).

H3 is **active but not yet accepted**. DHE and SHAE remain closed.

## Immediate next research steps

1. Collect the H3 trusted-reviewer responses across both counterbalanced live forms.
2. Analyze completion time, device coverage, readability and confusion.
3. Exercise `tools/google_forms/H3DurabilityPayload.gs` through the already-proven Apps Script runtime and verify normalized rows, backup checksums and recovery/idempotency.
4. If all H3 criteria pass, freeze the operating path and open H4 DHE preparation.
5. Preserve SHAE as sealed final assurance only after a future candidate is frozen.

## Public website state

The website is a presentation and participation layer, not a second research database.

Website implementations should consume:

- [`../public/research-status.json`](../public/research-status.json)
- [`../public/human-evaluation.json`](../public/human-evaluation.json)

and follow [`WEBSITE_INTEGRATION.md`](WEBSITE_INTEGRATION.md).

No public human-evaluation round is currently accepting responses. H3 is an internal/trusted-reviewer pilot. The public website must not expose H3 reviewer links, H2 sandbox links, response sheets, private A/B maps, or any future sealed-assurance material.

## Claim boundary

### Supported

- the DPO V2 run is technically valid;
- DPO V2 changed intended trainable parameters;
- mixed behavioral changes were observed;
- the existing 50-case DPO V2 comparison is contaminated and diagnostic;
- SFT remains the reference checkpoint;
- H2 human-evaluation infrastructure is formally accepted;
- H3 internal disposable pilot is active.

### Not supported

- DPO V2 is superior to SFT;
- the current benchmark delta proves progress or regression overall;
- H3 is complete before its acceptance criteria pass;
- DHE may begin before H3 acceptance;
- SHAE may begin during H3;
- H3 responses constitute model-comparison evidence.

## Canonical detail documents

- [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md)
- [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md)
- [`HUMAN_EVALUATION_PROTOCOL.md`](HUMAN_EVALUATION_PROTOCOL.md)
- [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md)
- [`HUMAN_EVALUATION_H3_PILOT.md`](HUMAN_EVALUATION_H3_PILOT.md)
- [`HUMAN_EVALUATION_WORKFLOW.md`](HUMAN_EVALUATION_WORKFLOW.md)
- [`REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md`](REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md)
