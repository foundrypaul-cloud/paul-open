# PAUL Open — Current Research Status

**Status date:** 2026-09-10  
**Public research repository:** `foundrypaul-cloud/paul-open`  
**Public website:** https://open.paulfoundry.com/

This document is the concise public status layer for the repository. Detailed historical evidence remains in the experiment-specific documents and immutable artifacts.

## Current position

PAUL Open is currently in the evaluation-hardening stage after a technically successful DPO V2 Corrective run on `google/gemma-4-E4B-it`.

The correct research conclusion is:

> **The SFT adapter remains the safer reference checkpoint. DPO V2 is technically valid and behaviorally informative, but superiority over SFT has not been established.**

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

## Human evaluation — H2 status

The human-evaluation architecture is being validated before any model-superiority claim or broader reviewer recruitment.

What has been demonstrated in the sandbox:

- genuine respondent submissions through Google Forms;
- 6 native Form responses retained;
- 18 normalized comparison rows retained;
- 6 independent backup-ledger rows retained;
- snapshot JSON and SHA-256 fields populated;
- anonymous evaluation path with email collection off;
- optional reviewer context and optional comments;
- blinded synthetic A/B comparisons;
- verifier execution passed against the live sandbox state.

A live Apps Script issue was isolated during the remaining acceptance checks: Google Forms accepted `setAcceptingResponses(false)` but threw `Exception: Invalid data updating form` when the script subsequently attempted to set a custom closed-form message. The same cosmetic-message failure caused both the close helper and recovery helper to report failure after the safety-critical closure/persistence work.

Repository fix PR #12 was merged into `main` as commit:

`49e7bc0a893b988519f8b65d793230b5246fd89b`

The fix makes the custom closed message best-effort while keeping form closure mandatory.

### H2 is not yet declared complete

The live standalone Apps Script project still needs to be synchronized with the repository patch and the remaining recovery/closure acceptance checks must be rerun successfully. A previous controlled recovery drill was abandoned and manually restored; it does not count as proof of hourly self-healing.

Until those checks are complete:

- do not mark H2 fully accepted;
- do not start SHAE;
- do not claim human preference evidence for SFT vs DPO V2;
- do not expose the sandbox Form as a public research instrument.

## Immediate next research steps

1. Finish H2 runtime synchronization and controlled recovery/closure acceptance.
2. Freeze a clean human-evaluation path.
3. Repair the evaluation boundary and contamination checks before further model training.
4. Build clean DHE material and reserve SHAE as sealed final assurance.
5. Compare checkpoints using task-specific metrics plus blinded human preference rather than one aggregate score.

## Public website state

The website is a presentation and participation layer, not a second research database.

Website implementations should consume:

- [`../public/research-status.json`](../public/research-status.json)
- [`../public/human-evaluation.json`](../public/human-evaluation.json)

and follow [`WEBSITE_INTEGRATION.md`](WEBSITE_INTEGRATION.md).

When there is no approved live human-evaluation packet, the website should display an evaluation-preparing/closed state rather than a sandbox respondent link.

## Claim boundary

### Supported

- the DPO V2 run is technically valid;
- DPO V2 changed intended trainable parameters;
- mixed behavioral changes were observed;
- the existing 50-case DPO V2 comparison is contaminated and diagnostic;
- SFT remains the reference checkpoint;
- human-evaluation infrastructure is actively being validated.

### Not supported

- DPO V2 is superior to SFT;
- the current benchmark delta proves progress or regression overall;
- the present human-evaluation sandbox constitutes a model comparison result;
- H2 is fully accepted before the remaining runtime checks pass;
- a future checkpoint will be better merely because it trains successfully.

## Canonical detail documents

- [`EXPERIMENT_JOURNEY_E4B.md`](EXPERIMENT_JOURNEY_E4B.md)
- [`E4B_DPO_V2_CORRECTIVE.md`](E4B_DPO_V2_CORRECTIVE.md)
- [`HUMAN_EVALUATION_PROTOCOL.md`](HUMAN_EVALUATION_PROTOCOL.md)
- [`HUMAN_EVALUATION_H2_SANDBOX.md`](HUMAN_EVALUATION_H2_SANDBOX.md)
- [`REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md`](REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md)
