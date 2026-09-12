# PAUL Open Human Evaluation — H4 DHE Pilot

**Status:** ANALYSIS_LOCKED  
**Stage:** H4 — Development Human Evaluation (DHE)  
**Protocol:** `docs/HUMAN_EVALUATION_WORKFLOW.md` + `configs/evaluation/human_eval_v1.yaml`  
**Precondition:** H3 formally accepted on 2026-09-11

## Purpose

H4 is the first real PAUL Open development human-evaluation pilot after the H2 infrastructure validation and H3 UX/durability pilot passed. H4 is **development evidence**, not sealed final-assurance evidence. Its results may inform future training or data work, so H4 cases are development-exposed and must never later be represented as untouched SHAE evidence.

## Research question

For fresh, non-assurance prompts that have not been used in PAUL Open training or the contaminated 50-case comparison, how do blinded reviewers compare the frozen SFT reference checkpoint and DPO V2 Corrective checkpoint on response usefulness and quality?

H4 is not authorized to establish final model superiority by itself.

## Checkpoints

- reference checkpoint: historical SFT adapter
- experimental checkpoint: DPO V2 Corrective
- base model: `google/gemma-4-E4B-it`
- Step 2 immutable experiment freeze: `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`

Do not retrain, modify, or silently repair either checkpoint for this pilot.

## Case eligibility

Every H4 case must be fresh development-evaluation material and pass the frozen pre-form gates: generation complete, non-empty output, automated safety gate, malformed-output gate, evaluation-partition integrity, and contamination gate.

Exclude H3 disposable cases, SFT/DPO training material, the contaminated canonical 50-case suite and close derivatives, the DPO V2 corrective prompts and close derivatives, the permanent DPO holdout, SHAE material, and material without sufficient provenance.

## Reviewer-facing judgment

Each comparison uses the fixed five-choice vocabulary:

- Response A is better
- Response B is better
- They are about equally good
- Neither response is good
- I'm not sure / I can't judge this

Model/checkpoint identity and automated scores remain hidden from reviewers.

## Blinding and counterbalancing

Use `scripts/build_human_eval_batch.py` with partition=`development`, deterministic secret/research seed, complementary A/B variants, and a private model-identity mapping stored only in the gitignored/private mapping path. The private mapping must not appear in Google Forms, website bundles, reviewer instructions, or the blinded analysis lock.

## Review allocation

The frozen allocation policy is unchanged:

- initial valid judgments per case: 3
- disagreement/uncertainty escalation: 5 total judgments
- exceptional hard cap: 7 judgments
- control-injection form rate: 0.20
- control items excluded from model win-rate calculations

Do not collect more judgments merely to increase sample size when the protocol does not require them.

## Reviewer cohorts

Allowed cohorts remain `general_user`, `educator`, `bilingual`, `stem_capable`, and `domain_expert`. Reviewer contact identity remains separate from judgments.

## H4 collection result

Batch `HEB1-E928B35C90D7` contained five eligible cases after one identical pair was excluded. Ten complementary reviewer-facing variants were generated.

The initial round produced 15 judgments. STEM, Educator, and Bengali met the frozen escalation rule and each received two additional judgments. Final case totals are:

- General: 3
- STEM: 5
- Educator: 5
- Hindi: 3
- Bengali: 5
- **Total: 21 judgments**

The exceptional seven-judgment cap was not invoked before analysis lock.

## Data integrity and durability audit

The H2/H3 durability architecture was retained: native Google Form responses, linked raw response sheets, `PAUL Normalized`, independent `PAUL Backup Ledger`, canonical snapshot JSON + SHA-256, and idempotent recovery.

Immediately before analysis lock on 2026-09-12, all ten variants were audited. Results:

- raw response rows: 21
- normalized response IDs: 21
- backup response IDs: 21
- normalized/backup response IDs: exact match
- backup SHA-256: present for all 21 responses
- backup-write timestamp: present for all 21 responses
- durability audit: **PASS**

No manual spreadsheet editing was used to repair or reinterpret the H4 judgment set.

## Analysis lock

The blinded judgment set is frozen in:

- `data/h4_dhe_pilot_v1_blinded_analysis_lock.json`
- `docs/H4_DHE_PILOT_V1_ANALYSIS_LOCK.md`

The lock was created **before** reading the private A/B source mapping. All 21 accepted judgments are frozen. Post-unblind exclusion changes are prohibited except correction of a separately documented, demonstrable data-integrity error.

## Frozen analysis contract

Post-unblind reporting must include candidate preferred, reference preferred, about equal, neither good, not sure, and inter-rater agreement. Stratify by domain/language/reviewer cohort where the small sample permits and use bootstrap confidence intervals where appropriate under the frozen configuration. Bradley-Terry is for multi-model use only and is not the primary analysis for this two-model H4 comparison.

Do not count declared controls in model win-rate calculations. Do not translate this small H4 DHE pilot into an overall model-superiority claim.

## Accessibility finding

During H4 collection, a reviewer identified that the text-only Google Forms experience is not sufficiently self-evident for evaluators with poor or no vision. Future evaluator-interface work should preserve keyboard and screen-reader compatibility and evaluate multilingual text-to-speech assistance without making TTS the sole accessibility path.

This remains a future-interface DHE finding and does not alter the frozen H4 judgments.

## Contamination consequence

Once an H4 case or reviewer finding is used to change training data, prompts, model weights, preference data, generation strategy, or evaluation design, that material remains development-exposed and cannot be reclassified as sealed final assurance. SHAE remains outside this workflow.

## Current boundary

As of 2026-09-12, H4 is **ANALYSIS_LOCKED** with 21 frozen judgments and a passing durability audit. The next permitted transition is **UNBLINDED**: use the private gitignored mapping to convert the frozen reviewer-facing A/B judgments into SFT-reference versus DPO-V2-Corrective outcomes, calculate the predeclared H4 metrics, and record the development-evaluation decision.

Public participation remains disabled. Reviewer links, response sheets, private A/B mappings, and SHAE material remain non-public.
