# PAUL Open — DPO V5 P11/P12 Results

**Status:** P11 COMPLETE / P12 CLEARED FOR PRECOMMITTED H7 DHE WITH REGRESSION FLAGS  
**Date:** 2026-09-13  
**Candidate:** `paul_e4b_dpo_v5_corrective`  
**Reference:** frozen SFT adapter (`paulfoundry/paul-open-sft`)  
**SHAE:** sealed / not accessed

## P11 — candidate training

DPO V5 production completed successfully on the exact merged source revision:

- source revision: `08a0857bbd5a93d58b8ca64a61625e69f68bf442`
- GitHub Actions run: `34737466097`
- production artifact: `10311949786`
- artifact digest: `sha256:baf68e48dbd3bb8c8a901265e9bbb2ff1e0899092789dc8a6c9c541c25145973`
- dataset records: 30
- dataset SHA-256: `1584705bf332137ade1ee24873e5d463653a2b26e26c63f6dc9c87515618bbd4`
- base model revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`
- configured epochs: 4
- trainer global step: 8
- final train loss: `0.682159423828125`
- final AMP scale: `32768.0`

The production manifest reports `completion_gate: PASS`.

### Technical validity evidence

All intended LoRA tensors changed and remained finite:

- intended trainable tensors: 516
- changed trainable tensors: 516
- finite update evidence: PASS

Post-training invariants all passed:

- adapter topology: PASS
- optimizer membership: PASS
- policy placement: PASS
- frozen reference in evaluation mode: PASS
- policy/reference storage independence: PASS
- external-reference math equivalence: PASS

The validated DPO V2/V3/V4 methodology was preserved: sigmoid DPO, beta `0.1`, learning rate `5e-7`, four epochs, batch size `1`, gradient accumulation `8`, max length `4096`, FP16, gradient checkpointing, `paged_adamw_8bit`, seed `42`, policy on GPU 0 and frozen external SFT reference on GPU 1.

### Final adapter identity

Recovered from the completed private Kaggle production kernel and independently re-hashed in the H7 binding audit:

- `final-dpo-adapter/dpo/adapter_config.json` SHA-256: `2edf45ffe03f0f026acfd4c7ecb35df23275cd9edc3509e7e091115d6a9cd023`
- `final-dpo-adapter/dpo/adapter_model.safetensors` SHA-256: `9a5e26985ad85226dc67c6e056dd0856b721d084da4213f1d6fe3f4af19f549c`
- adapter config size: `14707` bytes
- adapter weights size: `139602808` bytes

These hashes identify the DPO V5 development candidate for downstream paired generation. The candidate is not promoted or assurance-frozen.

## P12 — automated gates

### Technical gate — PASS

P11 completion, authentic parameter updates, locked topology and runtime invariants passed. The separate V5 contract-verification workflow also passed and confirmed no optimizer/model/adapter/tokenizer/runtime methodology drift from V4.

### Contamination gate — PASS

The P10 gate audited all 30 V5 preference records before training:

- exact reuse from prior development/training material: absent;
- maximum prior-data Unicode token-set Jaccard: `0.2857142857142857`, below the frozen exclusive `0.35` threshold;
- canonical benchmark leakage: `0 / 30` detected;
- independent non-human record audit: all 30 exact dataset IDs covered and passed;
- H4/H5/H6 raw response text: not accessed for V5 training data;
- SHAE: not accessed.

### Automated 50-case diagnostic — SUCCESS / MIXED

Both SFT and DPO V5 completed all 50 cases with zero execution failures and `100%` automated safety / anti-anthropomorphism adherence.

| Metric | SFT | DPO V5 | Delta |
|---|---:|---:|---:|
| Mean heuristic rubric | 90.66 | 89.53 | -1.13 |
| Mean keyword coverage | 0.767 | 0.738 | -0.029 |
| Safety adherence | 100% | 100% | 0 |
| Human-review flags | 17 | 16 | -1 |

Selected domain rubric means:

| Domain | SFT | DPO V5 | Delta |
|---|---:|---:|---:|
| Empathy / human-centered | 78.40 | 84.53 | +6.13 |
| Indic understanding | 92.00 | 93.60 | +1.60 |
| Life sciences | 98.67 | 98.67 | 0.00 |
| Scientific research | 89.60 | 89.87 | +0.27 |
| Multilingual translation | 93.87 | 90.67 | -3.20 |
| Science reasoning | 95.20 | 92.27 | -2.93 |
| Scientific explanation | 90.93 | 86.93 | -4.00 |
| Socratic tutoring | 77.33 | 72.53 | -4.80 |
| Student assistance | 96.11 | 93.18 | -2.93 |
| Teacher assistance | 94.52 | 93.07 | -1.45 |

### Interpretation boundary

The 50-case suite is an automated regression detector, not a semantic-quality oracle and not a human-preference study. Its mixed signal therefore does not establish either superiority or inferiority of V5. In particular, the lower aggregate heuristic score and the Socratic/science/explanation flags must be carried into fresh blinded human review rather than hidden, while the empathy/Indic gains likewise require human confirmation.

H7 prompts were frozen and merged to `main` at `d890fdbbaa224ad9cdfbe38440b01e0a4bc8ed2d` **before V5 outputs were inspected**, so the next human gate is not selected post hoc around these diagnostic results.

## P12 decision

P12 is **cleared for the precommitted H7 development human evaluation with explicit regression flags**, not cleared for promotion.

Rationale:

1. technical validity, authentic update evidence, contamination isolation and automated safety passed;
2. automated behavioral evidence is mixed and the aggregate heuristic score is modestly below SFT;
3. the evaluation framework treats these metrics as diagnostic signals rather than final behavioral judgments;
4. H7 was independently precommitted on fresh prompts before candidate output inspection and is therefore the appropriate next development gate.

## Claim boundary

Supported:

- DPO V5 is a technically valid trained development candidate.
- V5 training data passed the frozen P10 contamination/separation gates.
- automated safety passed on the 50-case matched diagnostic run.
- automated diagnostic evidence is mixed and the aggregate heuristic score is lower than SFT in this run.
- precommitted H7 blinded DHE is justified and required before any promotion claim.

Not supported:

- DPO V5 is superior to SFT.
- DPO V5 has passed human evaluation.
- DPO V5 is assurance-frozen.
- SHAE may be opened.
- the automated aggregate alone proves superiority or inferiority.
