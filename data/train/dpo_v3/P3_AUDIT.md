# DPO V3 Corrective Dataset — P3 Audit

**Status:** PASS  
**Date:** 2026-09-12  
**Dataset:** 30 development-only preference pairs across the five P2 shards  
**Verification run:** GitHub Actions `34685252231`  
**Verified source head:** `6f1864db6d47bf274b93654eba0b2cbebcfdfef6`

## Frozen assembly order

1. `bengali_causal_direction.jsonl` — 8
2. `grounded_socratic_tutoring.jsonl` — 6
3. `evidence_before_hypothesis.jsonl` — 6
4. `stem_causal_clarity.jsonl` — 5
5. `hindi_science_calibration.jsonl` — 5

The CI verification assembles these records deterministically with sorted JSON keys before hashing.

**Assembled dataset SHA-256:** `5ce4a82f32827a07f339d2b8c437dc4b45ec3f60ac9f5d50f165ea308369c741`

## Gate results

| P3 gate | Result | Evidence |
|---|---|---|
| 30 valid JSONL records | PASS | CI schema/count assertion |
| unique IDs | PASS | CI uniqueness assertion |
| unique prompts/chosen/rejected | PASS | CI uniqueness assertion |
| exact H4 prompt reuse | PASS — none | CI exact-set comparison |
| exact prior DPO V1/V2 prompt reuse | PASS — none | CI exact-set comparison |
| near-H4 prompt sanity check | PASS | maximum token-set Jaccard `0.3333333333333333`, `paul_dpo_v3_bn_008` vs `H4-DHE-005`, below predeclared `0.35` guard |
| canonical benchmark leakage audit | PASS CLEAN | `scripts/check_leakage.py`: 30/30 clean, 0 contaminated |
| strongest canonical-benchmark similarity | PASS | 27.91% (`paul_dpo_v3_soc_001` vs `SOC-TUT-001`), below checker threshold |
| provenance metadata | PASS | all records use `source: post_h4_p2_authored` |
| source verification flags | PASS | source records remain `human_verified: false` and `benchmark_leakage_checked: false`; the audit result is recorded here instead of mutating the hashed source data |
| preference direction | PASS — independent review | chosen responses implement the P2 target behavior; rejected responses contain the declared, plausible defect |
| science factuality | PASS — independent review | causal direction and calibration checked across Bengali, STEM, and Hindi science tracks |
| Bengali/Hindi language quality | PASS — independent non-human review | native-script, intelligible, audience-appropriate wording; no broad romanization detected |
| SHAE isolation | PASS | sealed assurance material was not accessed, opened, copied, or used in authoring/audit |

## Audit corrections caught before PASS

The guard worked as intended. Earlier CI attempts rejected P2 records whose wording was too close to H4, including an altitude/boiling Bengali example and Hindi battery-adjacent/structurally similar examples. Those records were rewritten into distinct development scenarios rather than weakening the threshold. The final passing run therefore represents the corrected dataset, not a bypassed check.

## Verification boundary

This is a repository/independent model-assisted data audit, **not human verification**. The per-record `human_verified` flag remains false. No claim is made that a human expert reviewed all 30 records.

`benchmark_leakage_checked` also remains false inside source records because changing those fields after the passing hash would create a different dataset. The immutable audit evidence for the assembled digest is this record plus GitHub Actions run `34685252231`.

## P3 decision

P3 passes for the frozen 30-pair development dataset identified by SHA-256 above. P4 candidate-training preparation is authorized under `docs/POST_H4_DEVELOPMENT_PLAN.md`, subject to preserving the validated DPO V2 training methodology and using a new experiment/candidate identity. DPO V2 artifacts must remain immutable and SHAE remains sealed.
