# PAUL Open — DPO V3 P4/P5 Results

**Status:** P4 COMPLETE / P5 CLEARED FOR FRESH DHE WITH REGRESSION FLAGS  
**Date:** 2026-09-12  
**Candidate:** `paul_e4b_dpo_v3_corrective`  
**Reference:** frozen SFT adapter (`paulfoundry/paul-open-sft`)  
**SHAE:** sealed / not accessed

## P4 — candidate training

DPO V3 production completed successfully on the exact merged source revision:

- source revision: `dff8c34ca148c436bdb0bc06e0ce27ddfb9a821f`
- GitHub Actions run: `34685874589`
- production artifact: `10296611503`
- artifact digest: `sha256:ded01374112482d5e87e6905b2082f390d36e07c368d2bee7a7f7a53a97cce69`
- dataset records: 30
- dataset SHA-256: `5ce4a82f32827a07f339d2b8c437dc4b45ec3f60ac9f5d50f165ea308369c741`
- base model revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`
- configured epochs: 4
- trainer global step: 8
- final train loss: `0.700347900390625`
- train runtime: `275.8702 s`

The production manifest reports `completion_gate: PASS`.

### Technical validity evidence

All intended LoRA tensors changed and remained finite:

- intended trainable tensors: 516
- changed trainable tensors: 516
- finite update evidence: PASS

Post-training invariants:

- adapter topology: PASS
- optimizer membership: PASS
- policy placement: PASS
- frozen reference in evaluation mode: PASS
- policy/reference storage independence: PASS
- external-reference math equivalence: PASS
- maximum absolute reference-math difference: `0.0`
- maximum relative reference-math difference: `0.0`

The locked DPO V2 methodology was preserved: sigmoid DPO, beta `0.1`, learning rate `5e-7`, four epochs, batch size `1`, gradient accumulation `8`, max length `4096`, FP16, gradient checkpointing, `paged_adamw_8bit`, seed `42`, policy on GPU 0 and frozen external SFT reference on GPU 1.

### Final adapter identity

From the production artifact:

- `final-dpo-adapter/dpo/adapter_config.json` SHA-256: `1ccc60a7f99368638a8ececb17aa6060c09a0648c42fdd678463108026ab22c9`
- `final-dpo-adapter/dpo/adapter_model.safetensors` SHA-256: `afcbc55e58aefb4ca72e5c7e3d5ac3362fe6b489477000a77cfa27b53ca76bd3`
- adapter weights size: `139602808` bytes

These hashes identify the DPO V3 development candidate for downstream paired generation. The candidate is not yet promoted or assurance-frozen.

## P5 — automated gates

### Technical gate — PASS

P4 completion and all locked topology/update invariants passed.

### Contamination gate — PASS for V3 training data vs canonical baseline

P3 ran the repository-native `scripts/check_leakage.py`, whose default benchmark is `baseline_suite_v1.json`. The final V3 dataset was reported 30/30 clean with zero contaminated records before training.

This matters because the historical 50-case suite was contaminated for DPO V2 source material, but DPO V3 starts from SFT and was trained on the separately audited V3 dataset. Historical DPO V2 contamination claims remain unchanged and must not be retroactively reinterpreted.

### Safety gate — PASS on the automated 50-case run

Both SFT and DPO V3 completed 50/50 cases with zero execution failures. DPO V3 automated anti-anthropomorphism/safety adherence was `100%`.

### Automated regression signal — MIXED / FLAGGED

Matched diagnostic evaluation under the same current runtime:

| Metric | SFT | DPO V3 | Delta |
|---|---:|---:|---:|
| Mean heuristic rubric | 91.18 | 89.98 | -1.20 |
| Safety adherence | 100% | 100% | 0 |
| Human-review flags | 16 | 18 | +2 |

Across 50 paired cases:

- improved: 12
- regressed: 15
- unchanged: 23
- median case delta: 0
- mean case delta: approximately -1.20

Selected domain deltas:

| Domain | SFT | DPO V3 | Delta |
|---|---:|---:|---:|
| Student assistance | 92.72 | 97.26 | +4.54 |
| Teacher assistance | 91.10 | 95.07 | +3.97 |
| Life sciences | 98.40 | 98.40 | 0.00 |
| Indic understanding | 93.60 | 93.60 | 0.00 |
| Science reasoning | 90.67 | 90.40 | -0.27 |
| Scientific explanation | 91.47 | 90.93 | -0.54 |
| Empathy / human-centered | 80.27 | 78.67 | -1.60 |
| Scientific research | 94.13 | 89.33 | -4.80 |
| Multilingual translation | 95.20 | 90.40 | -4.80 |
| Socratic tutoring | 84.27 | 75.73 | -8.54 |

Language-level regression flags include Bengali (`-4.00`) and Tamil (`-8.00`) in this heuristic run; Hindi was `-1.03`. Other languages improved or were unchanged in small-n slices.

### Response-level interpretation of the regression flags

The heuristic suite is explicitly a regression detector, not a semantic-quality oracle. Response inspection shows both kinds of signal:

- `SOC-TUT-001` is a genuine pedagogical regression: DPO V3 redirects the learner to a car/engine analogy that does not productively test the gravity misconception.
- some other score drops are less clearly behavioral failures. For example, the DPO V3 p-value/effect-size answer remains substantively reasonable despite a lower keyword-based score.
- several Bengali/scientific-explanation score differences are affected by response length/truncation and do not by themselves establish a causal-fidelity failure.

Therefore the automated result is **not** interpreted as either superiority or global failure.

## P5 decision

P5 is **cleared for P6 fresh development human evaluation with explicit regression flags**, not cleared for promotion.

Rationale:

1. technical validity, contamination isolation and automated safety passed;
2. the aggregate automated regression signal is negative and includes a real Socratic concern, so it must be carried forward explicitly;
3. the repository's evaluation framework states that the heuristic rubric is a regression signal and that behavioral quality requires paired qualitative/blinded human review;
4. no predeclared numeric heuristic threshold exists that would justify converting the mixed signal into an automatic promotion or rejection decision after seeing the result.

P6 must therefore use **fresh development prompts**, not H4, the 50-case suite, or training examples, and must intentionally cover Socratic tutoring, Bengali causal explanation, scientific/research assistance, Hindi calibration, STEM preservation and general human-centered usefulness.

## Claim boundary

Supported:

- DPO V3 is a technically valid trained development candidate.
- V3 training data passed the canonical baseline leakage checker before training.
- automated safety passed on the 50-case diagnostic run.
- automated regression evidence is mixed and overall heuristic score is lower than SFT in the matched run.
- P6 fresh DHE is justified to resolve behavioral quality under blinded comparison.

Not supported:

- DPO V3 is superior to SFT.
- DPO V3 has passed human evaluation.
- DPO V3 is assurance-frozen.
- SHAE may be opened.
- the automated aggregate alone proves either superiority or inferiority.
