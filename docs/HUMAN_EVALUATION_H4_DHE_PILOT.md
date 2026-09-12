# PAUL Open Human Evaluation — H4 DHE Pilot

**Status:** collecting  
**Stage:** H4 — Development Human Evaluation (DHE)  
**Protocol:** `docs/HUMAN_EVALUATION_WORKFLOW.md` + `configs/evaluation/human_eval_v1.yaml`  
**Precondition:** H3 formally accepted on 2026-09-11

## Purpose

H4 is the first real PAUL Open development human-evaluation pilot after the H2 infrastructure validation and H3 UX/durability pilot passed.

H4 is **development evidence**, not sealed final-assurance evidence. Its results may inform future training or data work, so H4 cases become development-exposed and must never later be represented as untouched SHAE evidence.

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

Every H4 case must be fresh development-evaluation material and pass the pre-form gates already frozen in `configs/evaluation/human_eval_v1.yaml`:

1. generation completed;
2. output non-empty;
3. automated safety gate passed;
4. malformed-output gate passed;
5. evaluation partition integrity passed;
6. contamination gate passed.

Exclude:

- all H3 disposable cases;
- any case used in SFT/DPO training;
- the canonical 50-case baseline suite and close paraphrases/templates derived from it;
- the DPO V2 corrective training prompts or close derivatives;
- the permanent DPO holdout;
- any material reserved for SHAE;
- any prompt whose provenance cannot be established well enough to clear contamination review.

## Pilot size

The protocol specifies a **small DHE pilot** but does not freeze a numeric case count. Do not invent a fixed number merely for convenience. Select the smallest coherent fresh set that exercises the intended PAUL Open capability mix while remaining practical for blinded review.

Form packaging remains protocol-controlled:

- default: 3 comparisons per form;
- maximum short-response comparisons: 4;
- maximum long-response comparisons: 2;
- target completion time: about 4 minutes.

## Reviewer-facing judgment

Each comparison uses the fixed five-choice vocabulary:

- Response A is better
- Response B is better
- They are about equally good
- Neither response is good
- I'm not sure / I can't judge this

Model/checkpoint identity and automated scores must remain hidden from reviewers.

## Blinding and counterbalancing

Use the existing deterministic batch builder:

`scripts/build_human_eval_batch.py`

Required behavior:

- partition=`development`;
- deterministic secret/research seed;
- complementary A/B variants;
- private model-identity mapping stored outside reviewer-facing artifacts;
- no hidden mapping exposed in Google Forms, website bundles, or reviewer instructions.

## Review allocation

Use the frozen allocation policy from `configs/evaluation/human_eval_v1.yaml`:

- initial valid judgments per case: 3;
- escalate disagreement to 5 total judgments;
- exceptional hard cap: 7 judgments;
- control-injection form rate: 0.20;
- control items are excluded from model win-rate calculations.

Do not collect more judgments merely to increase sample size when the protocol does not require them.

## Reviewer cohorts

Use only the cohort categories already declared in the protocol:

- general_user
- educator
- bilingual
- stem_capable
- domain_expert

Route cases to appropriate cohorts when domain/language competence is necessary. Reviewer contact identity must remain separate from judgments.

## Generation and pairing workflow

1. Freeze the H4 case manifest before model generation.
2. Generate SFT and DPO V2 outputs independently using matched inference settings.
3. Preserve raw generated outputs and generation metadata outside reviewer-facing material.
4. Run all hard pre-form gates.
5. Build blinded A/B variants with `scripts/build_human_eval_batch.py --partition development`.
6. Store the private A/B source mapping only in the gitignored/private mapping path.
7. Convert reviewer-facing variants to the established Google Forms packet format.
8. Use the proven Apps Script response-normalization/backup/recovery path.
9. Distribute only `/viewform` respondent links to assigned reviewers.
10. Close forms when the protocol target is reached.
11. Lock analysis before unblinding.
12. Unblind only after judgments and exclusions are frozen.

## Data integrity

Retain the H2/H3 durability architecture:

1. native Google Form response;
2. linked raw response sheet;
3. `PAUL Normalized` rows;
4. independent `PAUL Backup Ledger`;
5. canonical snapshot JSON + SHA-256;
6. idempotent recovery from native Form responses.

No manual spreadsheet editing should be part of the normal analysis path.

## Analysis

Report at minimum:

- candidate preferred;
- reference preferred;
- about equal;
- neither good;
- not sure;
- inter-rater agreement;
- domain/language/reviewer-cohort strata where sample size permits.

Use bootstrap confidence intervals where appropriate under the frozen analysis configuration.

Do not count control items in model win-rate calculations.

Do not translate a small H4 pilot result into an overall model-superiority claim.

## Contamination consequence

Once an H4 case or reviewer finding is used to change training data, prompts, model weights, preference data, generation strategy, or evaluation design, that material is development-exposed. It remains useful as DHE evidence but cannot be reclassified as sealed final assurance.

SHAE stays outside this workflow.

## H4 preparation acceptance gate

Preparation is complete only when all of the following are true:

- H3 formal acceptance is recorded;
- fresh DHE case manifest exists;
- contamination audit passes;
- SFT and DPO V2 generation inputs/settings are frozen;
- paired outputs are complete and non-empty;
- safety/malformed gates pass;
- deterministic blinded variants are built;
- private A/B mapping is separated from reviewer-facing artifacts;
- Google Forms packets are generated using the established pipeline;
- no SHAE material has been exposed.

Only then may H4 collection move to `COLLECTING`.

## Accessibility finding

During H4 collection, a reviewer identified that the text-only Google Forms experience is not sufficiently self-evident for evaluators with poor or no vision. Future evaluator-interface work should explicitly preserve keyboard and screen-reader compatibility and evaluate multilingual text-to-speech assistance without making TTS the sole accessibility path.

This is a DHE interface finding for future iterations; do not modify the active H4 forms in a way that changes this collection round after distribution.

## Current boundary

As of 2026-09-12, H4 is **COLLECTING**. The five eligible cases have each reached the initial three-judgment coverage target (15 judgments total). Under the frozen adaptive allocation policy, cases containing disagreement or a `not_sure` judgment escalate to five total judgments before closure. Public participation remains disabled, reviewer links remain private, and no SHAE material has been exposed.
