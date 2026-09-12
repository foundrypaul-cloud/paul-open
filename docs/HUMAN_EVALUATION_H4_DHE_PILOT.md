# PAUL Open Human Evaluation — H4 DHE Pilot

**Status:** DECISION_RECORDED  
**Stage:** H4 — Development Human Evaluation (DHE)  
**Protocol:** `docs/HUMAN_EVALUATION_WORKFLOW.md` + `configs/evaluation/human_eval_v1.yaml`  
**Precondition:** H3 formally accepted on 2026-09-11

## Purpose and research boundary

H4 is PAUL Open's first real development human-evaluation pilot after the H2 infrastructure validation and H3 UX/durability pilot. H4 is **development evidence**, not sealed final-assurance evidence. Its cases are development-exposed and cannot later be represented as untouched SHAE evidence.

The H4 research question was whether blinded reviewers preferred responses from the frozen SFT reference checkpoint or DPO V2 Corrective checkpoint on a small set of fresh development cases.

H4 is not authorized to establish overall model superiority by itself.

## Frozen checkpoints

- reference: SFT
- candidate: DPO V2 Corrective
- base model: `google/gemma-4-E4B-it`
- Step 2 immutable freeze: `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`

No retraining or checkpoint repair was performed for this pilot.

## Blinding and allocation

The existing deterministic human-evaluation builder was used with complementary A/B variants and a private A/B source mapping. Model identity remained hidden from reviewers.

Frozen reviewer allocation:

- initial valid judgments per case: 3
- disagreement/uncertainty escalation: 5 total judgments
- exceptional hard cap: 7 judgments
- no extra judgments solely to increase sample size

Allowed reviewer cohorts remained `general_user`, `educator`, `bilingual`, `stem_capable`, and `domain_expert`.

## Collection result

Batch `HEB1-E928B35C90D7` contained five eligible cases after one identical response pair was excluded. Ten complementary reviewer-facing variants were generated.

The initial round produced 15 judgments. STEM, Educator, and Bengali triggered the predeclared adaptive rule and each received two additional judgments.

Final case totals:

- General: 3
- STEM: 5
- Educator: 5
- Hindi: 3
- Bengali: 5
- **Total: 21 judgments**

The exceptional seven-judgment cap was not required.

## Data integrity

Before unblinding, the full H4 response path was audited across all ten variants:

- raw response rows: 21
- `PAUL Normalized` response IDs: 21
- independent `PAUL Backup Ledger` response IDs: 21
- normalized/backup IDs: exact match
- backup SHA-256: present for all 21
- backup-write timestamp: present for all 21

Durability result: **PASS**.

The blinded judgment set was then frozen in:

- `data/h4_dhe_pilot_v1_blinded_analysis_lock.json`
- `docs/H4_DHE_PILOT_V1_ANALYSIS_LOCK.md`

The private A/B mapping was not read until after this lock.

## Controlled unblinding

Controlled unblinding used the private mapping retained in the private Kaggle generation output. The join used the exact comparison IDs recovered from the live form metadata. Only a safe aggregate was exported; the private seed, case IDs, fingerprints, and row-level A/B mapping remain uncommitted.

Safe aggregate:

- `data/h4_dhe_pilot_v1_unblinded_aggregate.json`

Full analysis and decision:

- `docs/H4_DHE_PILOT_V1_RESULTS.md`

## H4 result

Across all 21 judgments:

- DPO V2 preferred: **7**
- SFT preferred: **9**
- about equal: **2**
- neither good: **0**
- not sure / unable to judge: **3**

Among 16 decisive preference judgments, DPO V2 received **43.75%** and SFT **56.25%**.

Case majorities:

- General: SFT
- STEM: DPO V2
- Educator: SFT
- Hindi: DPO V2
- Bengali: SFT

DPO V2 therefore wins 2 of 5 case majorities; SFT wins 3 of 5.

Mean descriptive modal-choice agreement across the five cases is **80%**. A cluster bootstrap over the five cases produces very wide uncertainty intervals, consistent with H4 being a small development pilot rather than a superiority study.

## Decision

**Mixed result; no DPO V2 promotion.**

SFT remains the safer reference checkpoint. DPO V2 Corrective remains a technically valid experimental checkpoint with meaningful positive signals in STEM and Hindi, but H4 does not demonstrate broad superiority. General, Educator, and Bengali remain development areas for diagnosis.

Do not claim that H4 establishes DPO V2 superiority over SFT.

## Accessibility finding

A reviewer identified that the text-only Google Forms experience is not sufficiently self-evident for evaluators with poor or no vision. Future evaluator-interface work should preserve keyboard and screen-reader compatibility and evaluate optional multilingual text-to-speech assistance without making TTS the sole accessibility path.

This remains a future-interface DHE finding and did not alter the H4 collection or analysis.

## Current boundary

As of 2026-09-12, H4 is **DECISION_RECORDED**. Collection, durability verification, analysis lock, controlled unblinding, aggregate analysis, and the H4 development decision are complete.

SHAE remains sealed and has **not** started. Any next model-development work based on H4 is DHE follow-up and must not retroactively convert H4 into final assurance.
