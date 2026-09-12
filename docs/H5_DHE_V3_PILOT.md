# H5 DHE V3 Pilot — Final Development Result

**State:** DECISION_RECORDED  
**Partition:** Development Human Evaluation (DHE)  
**Batch:** `HEB1-64CDCC9521D3`  
**Candidate:** DPO V3 Corrective  
**Reference:** SFT  
**Decision:** mixed / no promotion / preservation failure  
**SHAE:** sealed / not started

## Generation and pre-collection gates

GitHub Actions paired-generation run `34692176820` completed successfully. The reviewer-safe generation artifact contained six eligible fresh development cases, two complementary blinded variants per case, and zero identical-pair exclusions.

Pre-form gates passed: paired generation, blinded-batch construction, canonical baseline leakage (6/6 clean), and H4/V3-training development separation. Maximum token-set Jaccard against H4/V3 training was `0.3333333333333333`, below the frozen `< 0.35` threshold.

## Human collection

The frozen initial allocation completed at exactly **18 valid judgments**: three per case with 9 V01 and 9 V02 judgments. All six cases were unanimous after complementary-swap normalization, so no 3→5 adaptive follow-up was authorized.

All twelve forms were closed after reaching their targets.

## Durability and lock

Durability passed before unblinding:

- 18 accepted Form responses;
- 18 normalized rows;
- 18 independent backup rows;
- normalized and backup response-ID sets matched exactly;
- all backup snapshots carried SHA-256 digests.

The blinded analysis was committed in `data/h5_dhe_v3_pilot_v1_blinded_analysis_lock.json` before source identity was consulted.

## Controlled unblinding

Controlled unblinding completed successfully in GitHub Actions run `34699579869`. The private Kaggle mapping remained outside the repository. Only a safe aggregate was emitted.

Final result:

| Case | Preferred checkpoint | Agreement |
|---|---|---:|
| STEM | SFT | 3/3 |
| Educator | SFT | 3/3 |
| Research | DPO V3 | 3/3 |
| Hindi | SFT | 3/3 |
| Bengali | DPO V3 | 3/3 |
| General | DPO V3 | 3/3 |

Aggregate judgments: **9 DPO V3 / 9 SFT / 0 equal / 0 neither / 0 not-sure**. Case-majority split: **3–3**.

## Decision

DPO V3 is **not promoted**. STEM and Hindi were pre-specified preservation strata and both favored SFT unanimously in fresh H5 cases. That preservation failure outweighs any temptation to interpret the aggregate tie as sufficient progress.

SFT remains the reference checkpoint. DPO V2 and DPO V3 remain immutable experimental checkpoints. SHAE remains sealed.

See:

- `docs/H5_DHE_V3_PILOT_V1_ANALYSIS_LOCK.md`
- `docs/H5_DHE_V3_PILOT_V1_RESULTS.md`
- `docs/POST_H5_DEVELOPMENT_PLAN.md`
- `data/h5_dhe_v3_pilot_v1_unblinded_aggregate.json`
