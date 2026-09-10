# PAUL Open — Current Research Status

**Status date:** 2026-09-10  
**Public research repository:** `foundrypaul-cloud/paul-open`  
**Public website:** https://open.paulfoundry.com/

This document is the concise public status layer for the repository. Detailed historical evidence remains in the experiment-specific documents and immutable artifacts.

## Current position

PAUL Open is currently in the evaluation-hardening stage after a technically successful DPO V2 Corrective run on `google/gemma-4-E4B-it`.

The correct research conclusion remains:

> **The SFT adapter remains the safer reference checkpoint. DPO V2 is technically valid and behaviorally informative, but superiority over SFT has not been established.**

The human-evaluation infrastructure milestone H2 is formally complete. The next human-evaluation stage is H3, a disposable non-research UX pilot. H2 completion does not change the model-comparison conclusion above.

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

H2 was formally accepted on **2026-09-10** after the repository implementation, live Google-account runtime, respondent path, durability mechanisms, recovery behavior, and closure behavior were checked.

Acceptance evidence includes:

- genuine respondent submissions through Google Forms;
- 6 native Form responses retained;
- 18 normalized comparison rows retained, representing 6 unique submissions;
- 6 independent backup-ledger rows retained;
- snapshot JSON and SHA-256 fields populated;
- anonymous evaluation path with email collection off;
- optional reviewer context and optional comments;
- blinded synthetic A/B comparisons;
- controlled recovery drill passed after an intentionally removed normalized representation was restored from the native Form response;
- verifier rerun passed on the patched live runtime;
- sandbox closure passed;
- respondent-facing Form opening on both desktop and mobile explicitly confirmed.

During H2, Google Forms accepted `setAcceptingResponses(false)` but could throw `Exception: Invalid data updating form` when the script subsequently attempted to set a custom closed-form message. Repository fix PR #12, merged as `49e7bc0a893b988519f8b65d793230b5246fd89b`, made the cosmetic closed-message update best-effort while preserving mandatory form closure. CI passed and the patched runtime subsequently passed recovery and closure acceptance.

H2 is infrastructure evidence only. It is **not** human preference evidence for SFT versus DPO V2.

See [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md).

## Human evaluation — H3 ready

The H3 entry gate is now open.

H3 is a dry-run human pilot using **5–10 disposable non-research comparisons** with a small internal/trusted reviewer group. It is intended to measure:

- median completion time;
- desktop/mobile readability;
- reviewer confusion;
- duplicate-response handling;
- Sheets normalization correctness;
- A/B mapping integrity.

Target: median completion time at or below 4 minutes with no systematic UX confusion.

H3 must not use DHE or SHAE cases. Real DHE begins only after H3 passes. SHAE remains sealed final assurance and must not be exposed during this stage.

## Immediate next research steps

1. Run and accept H3 using disposable non-research material and trusted reviewers.
2. Freeze the proven human-evaluation operating path after H3 acceptance.
3. Repair and preserve the clean evaluation boundary and contamination checks before further model training.
4. Build clean DHE material and reserve SHAE as sealed final assurance.
5. Compare checkpoints using task-specific metrics plus blinded human preference rather than one aggregate score.

## Public website state

The website is a presentation and participation layer, not a second research database.

Website implementations should consume:

- [`../public/research-status.json`](../public/research-status.json)
- [`../public/human-evaluation.json`](../public/human-evaluation.json)

and follow [`WEBSITE_INTEGRATION.md`](WEBSITE_INTEGRATION.md).

No public human-evaluation round is currently accepting responses. H3 is an internal/trusted-reviewer pilot. The public website must not expose H2 sandbox links, response sheets, private A/B maps, or any future sealed assurance material.

## Claim boundary

### Supported

- the DPO V2 run is technically valid;
- DPO V2 changed intended trainable parameters;
- mixed behavioral changes were observed;
- the existing 50-case DPO V2 comparison is contaminated and diagnostic;
- SFT remains the reference checkpoint;
- H2 human-evaluation infrastructure is formally accepted;
- H3 disposable UX-pilot work may begin.

### Not supported

- DPO V2 is superior to SFT;
- the current benchmark delta proves progress or regression overall;
- the H2 sandbox constitutes a model comparison result;
- H3 is complete before its trusted-reviewer pilot acceptance criteria pass;
- DHE or SHAE evidence exists merely because the collection infrastructure works;
- a future checkpoint will be better merely because it trains successfully.

## Canonical detail documents

- [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md)
- [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md)
- [`HUMAN_EVALUATION_PROTOCOL.md`](HUMAN_EVALUATION_PROTOCOL.md)
- [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md)
- [`HUMAN_EVALUATION_WORKFLOW.md`](HUMAN_EVALUATION_WORKFLOW.md)
- [`REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md`](REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md)
