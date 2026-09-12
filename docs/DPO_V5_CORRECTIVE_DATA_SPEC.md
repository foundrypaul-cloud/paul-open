# PAUL Open — DPO V5 Corrective Data Specification

**Stage:** POST-H6 CORRECTIVE DATASET AUTHORED / P10 VERIFICATION REQUIRED  
**Date:** 2026-09-13  
**Upstream evidence:** `docs/H6_DHE_V4_PILOT_V1_UNBLINDED_ANALYSIS.md`  
**Reference checkpoint:** frozen SFT adapter  
**Prior candidates:** DPO V2/V3/V4 immutable  
**SHAE:** sealed / not accessed

## Objective

Create a small development-only preference dataset that targets the failure classes exposed by H6 without reusing H6 prompts or changing the validated DPO training methodology.

H6 showed five unanimous SFT preferences and one unanimous `Neither response is good` result. The development diagnoses were: missing physical conditions, confounding-insensitive research reasoning, incomplete Socratic instruction following, Bengali scientific/language weakness, and evidence-first uncertainty gaps. Hindi and Spanish also favored SFT and therefore receive preservation/precision coverage.

## Data-design change relative to V4

V5 uses **near-miss hard negatives** more deliberately. The rejected answer should often look plausible and fluent while containing a specific conditional, causal, methodological, factual, or instruction-following defect. This is a data-design hypothesis motivated by H6; it is not an evaluation conclusion about why V4 failed.

No optimizer, topology, quantization, adapter source, or DPO hyperparameter change is authorized by this specification.

## Dataset identity

The six source shards live under `data/train/dpo_v5/` and are assembled deterministically into `data/train/dpo_v5_corrective.jsonl` by the training wrapper.

Frozen assembled SHA-256:

`634a507ffc63e731f48887f8a471bf08807ca94b600ad88d703ccfd9875ce364`

Total records: **30**.

| Track | Pairs | Purpose |
|---|---:|---|
| Conditional physical reasoning | 6 | Correct missing assumptions, system boundaries, momentum/energy distinctions |
| Confounding-aware research reasoning | 6 | Correct identifiability and design errors under batch/day/site confounding |
| Instruction-complete Socratic tutoring | 6 | Require a discriminating concrete test followed by an actual explanation |
| Bengali scientific fidelity V5 | 4 | Improve scientific accuracy and natural explanatory Bengali |
| Evidence-first uncertainty | 4 | Verify measurements and communicate uncertainty before narrative/accusation |
| Multilingual precision/completion | 4 | Preserve/improve Hindi and Spanish complete scientific explanations |
| **Total** | **30** | |

## Authoring rules

Chosen responses must be correct, complete for the prompt, concise, and explicit about material assumptions. Rejected responses must remain useful as preference negatives: generally fluent and plausible, but with a localized defect that explains the preference direction.

The dataset must not:
- reuse or lightly paraphrase H4, H5, or H6 evaluation prompts;
- copy any human-evaluation model response or evaluator comment;
- use H6 outcomes as labels for the exact H6 examples;
- access or derive from sealed SHAE material;
- silently reuse DPO V1/V2/V3/V4 pairs;
- claim `human_verified: true` before actual verification;
- claim `benchmark_leakage_checked: true` before the canonical leakage gate passes.

## Required metadata

Each record contains `id`, `track`, `domain`, `language`, `rejection_reason`, `prompt`, `chosen`, `rejected`, and metadata. IDs use the `paul_dpo_v5_` prefix. Metadata includes `difficulty`, `source: post_h6_v5_authored`, `human_verified: false`, `benchmark_leakage_checked: false`, `development_only: true`, and `corrective_category`.

## P10 acceptance gates

Training is blocked until all gates pass:

1. valid JSONL/schema, exact 30-record allocation, unique IDs/prompts/completions;
2. frozen assembled SHA-256 match;
3. no exact prior prompt or completion reuse;
4. prompt near-duplicate guard against H4, H5, H6, DPO V1/V2/V3/V4;
5. canonical benchmark leakage checker PASS;
6. independent preference-direction audit PASS for all records;
7. independent factual/methodological audit PASS for all records;
8. independent Hindi/Bengali/Spanish language audit PASS;
9. completion/instruction-following audit PASS;
10. SHAE remains sealed.

## Training boundary

After P10 passes, V5 must reuse the validated DPO V2/V3/V4 machinery and start from the same frozen SFT adapter. The existing dual-T4 topology, 4-bit NF4 model loading, LoRA contract, optimizer, beta, learning rate, epochs, seed, and fail-closed preflight remain unchanged unless a separate methodology change is proposed and reviewed.

V5 will be a development candidate only. It must pass automated diagnostic evaluation and a fresh, non-overlapping DHE before any consideration of SHAE.
