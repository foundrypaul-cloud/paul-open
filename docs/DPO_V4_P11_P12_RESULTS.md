# PAUL Open — DPO V4 P11/P12 Results

**Status:** P11 COMPLETE / P12 CLEARED FOR FRESH DHE WITH REGRESSION FLAGS  
**Date:** 2026-09-12  
**Candidate:** `paul_e4b_dpo_v4_corrective`  
**Reference:** frozen SFT adapter (`paulfoundry/paul-open-sft`)  
**SHAE:** sealed / not accessed

## P11 — candidate training

DPO V4 production completed successfully on the exact merged source revision:

- source revision: `6bd98c516ed1c4c53251ba4a9bbb6507d4b9cb73`
- GitHub Actions run: `34704441705`
- production artifact: `10301858693`
- artifact digest: `sha256:9932e85b5050ef52124bf5f98c72f847d0b7e57206afc9c8398b3a0bf531f810`
- dataset records: 30
- dataset SHA-256: `1d6b97eb63ab7dd0a52dc12e1b860b67084761668abfe2ab1bdcaa1093ca751c`
- base model revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`
- configured epochs: 4
- trainer global step: 8
- final train loss: `0.62982177734375`
- train runtime: `338.543 s`

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

The validated DPO V2/V3 methodology was preserved: sigmoid DPO, beta `0.1`, learning rate `5e-7`, four epochs, batch size `1`, gradient accumulation `8`, max length `4096`, FP16, gradient checkpointing, `paged_adamw_8bit`, seed `42`, policy on GPU 0 and frozen external SFT reference on GPU 1.

### Final adapter identity

From the production artifact:

- `final-dpo-adapter/dpo/adapter_config.json` SHA-256: `8e601627e6c9a256ed37acffb747c64e675f176ef92950470c6e85f7f09f146e`
- `final-dpo-adapter/dpo/adapter_model.safetensors` SHA-256: `773116e424401dc7009421616c303a0688ce2f1bc7191f2d61b715a447f44b8b`
- adapter weights size: `139602808` bytes

These hashes identify the DPO V4 development candidate for downstream paired generation. The candidate is not promoted or assurance-frozen.

## P12 — automated gates

### Technical gate — PASS

P11 completion and all locked topology/update invariants passed.

### Contamination gate — PASS for V4 training data vs canonical baseline and prior development material

P10 ran the repository-native canonical leakage checker and the additional H4/H5/DPO V1/V2/V3 exact and near-duplicate guards before training. The final V4 dataset was 30/30 clean on the canonical benchmark check, with the frozen dataset digest above. H4/H5 evaluator response text was not used as training data and SHAE remained sealed.

### Safety gate — PASS on the automated 50-case diagnostic run

Both SFT and DPO V4 completed 50/50 cases with zero execution failures. DPO V4 automated anti-anthropomorphism/safety adherence was `100%`.

### Automated regression signal — MIXED / FLAGGED

Matched diagnostic evaluation under the same current runtime:

| Metric | SFT | DPO V4 | Delta |
|---|---:|---:|---:|
| Mean heuristic rubric | 91.14 | 88.99 | -2.15 |
| Safety adherence | 100% | 100% | 0 |
| Human-review flags | 17 | 20 | +3 |

Across 50 paired cases:

- improved: 9
- regressed: 20
- unchanged: 21
- median case delta: 0
- mean case delta: approximately `-2.16`

Selected domain deltas:

| Domain | SFT | DPO V4 | Delta |
|---|---:|---:|---:|
| Empathy / human-centered | 76.80 | 80.00 | +3.20 |
| Multilingual translation | 92.20 | 93.87 | +1.67 |
| Teacher assistance | 94.52 | 94.71 | +0.19 |
| Indic understanding | 93.60 | 93.60 | 0.00 |
| Life sciences | 100.00 | 97.07 | -2.93 |
| Scientific research | 91.47 | 88.27 | -3.20 |
| Socratic tutoring | 77.33 | 74.13 | -3.20 |
| Scientific explanation | 91.47 | 88.27 | -3.20 |
| Science reasoning | 96.80 | 90.67 | -6.13 |
| Student assistance | 97.26 | 89.30 | -7.96 |

Language-level flags include Bengali (`-2.67`), Tamil (`-4.00`), Marathi (`-8.00`), Malayalam (`-8.00`), Punjabi translation (`-8.00`) and Bengali translation (`-6.67`) in small-n diagnostic slices. Hindi was nearly unchanged (`-0.14`), while some translation slices improved, including English-to-Hindi (`+8.00`) and English-to-Kannada (`+15.00`).

The largest case-level negative heuristic deltas included student assistance, a conservation-law science-reasoning case, scientific research, and Bengali Socratic tutoring. The same benchmark also recorded improvements in empathy/human-centered assistance, teacher assistance, several translation cases, one scientific-research case, and one Socratic case.

### Interpretation boundary

The 50-case heuristic suite is a regression detector, not a semantic-quality oracle. No predeclared numeric aggregate threshold exists that would justify converting the observed score after the fact into an automatic promotion or rejection rule. The negative aggregate and specific flags therefore must be carried forward explicitly into fresh blinded human evaluation rather than ignored or retroactively thresholded.

## P12 decision

P12 is **cleared for P13 fresh development human evaluation with explicit regression flags**, not cleared for promotion.

Rationale:

1. technical validity, contamination isolation and automated safety passed;
2. the automated regression signal is materially negative and includes the exact behavior families P8/P9 sought to improve, so those families require fresh blinded qualitative comparison;
3. the existing evaluation framework treats the heuristic suite as a regression signal and requires paired human review for behavioral-quality claims;
4. P13 can test the candidate on fresh prompts that were not used in H4, H5, the 50-case diagnostic suite, prior DPO data, V4 training, or SHAE.

P13 should intentionally cover:

- conservation-law / STEM reasoning;
- diagnostic Socratic tutoring and student assistance;
- scientific-research methodology;
- Hindi scientific calibration / direct completion;
- Bengali scientific fidelity;
- multilingual and evidence-first human-centered usefulness.

## Claim boundary

Supported:

- DPO V4 is a technically valid trained development candidate.
- V4 training data passed the pre-training contamination and separation gates.
- automated safety passed on the 50-case diagnostic run.
- automated regression evidence is mixed and the overall heuristic score is lower than SFT in the matched run.
- P13 fresh DHE is justified to resolve behavioral quality under blinded comparison.

Not supported:

- DPO V4 is superior to SFT.
- DPO V4 has passed human evaluation.
- DPO V4 is assurance-frozen.
- SHAE may be opened.
- the automated aggregate alone proves either superiority or inferiority.
