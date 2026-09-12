# H4 DHE Pilot V1 — Results and Decision

**Partition:** Development Human Evaluation (DHE)  
**Batch:** `HEB1-E928B35C90D7`  
**Analysis state:** DECISION_RECORDED  
**Judgments:** 21 across 5 eligible cases  
**Candidate:** DPO V2 Corrective  
**Reference:** SFT

## Research boundary

These results come from the small H4 development human-evaluation pilot. They are useful for model development and diagnosis, but they are **not sealed assurance** and do not establish overall model superiority.

The 21-judgment set was frozen in `data/h4_dhe_pilot_v1_blinded_analysis_lock.json` before the private A/B mapping was read. The durability audit passed before unblinding. Controlled unblinding then ran against the private mapping retained in the private Kaggle generation output. Only the safe aggregate was released; the private seed, case IDs, fingerprints, and row-level A/B source map remain private.

Private mapping provenance hash:

`3cc28a94f51bed2ca08e110a75b10378b863eb4efec3465a40375a77e95fe8d7`

## Aggregate judgments

| Outcome | Count | Share of all 21 |
|---|---:|---:|
| DPO V2 preferred | 7 | 33.3% |
| SFT preferred | 9 | 42.9% |
| About equal | 2 | 9.5% |
| Neither good | 0 | 0.0% |
| Not sure / unable to judge | 3 | 14.3% |

Among the **16 decisive preference judgments** only, DPO V2 received **43.75%** and SFT received **56.25%**.

## Case-level result

| H4 case | DPO V2 | SFT | Equal | Not sure | Majority |
|---|---:|---:|---:|---:|---|
| General | 0 | 3 | 0 | 0 | SFT |
| STEM | 4 | 0 | 0 | 1 | DPO V2 |
| Educator | 0 | 3 | 1 | 1 | SFT |
| Hindi | 3 | 0 | 0 | 0 | DPO V2 |
| Bengali | 0 | 3 | 1 | 1 | SFT |

DPO V2 wins **2 of 5** case majorities; SFT wins **3 of 5**.

This heterogeneity matters more than the small aggregate difference: DPO V2 performs strongly in the STEM and Hindi cases, while SFT is preferred in General, Educator, and Bengali.

## Inter-rater agreement

Because H4 used adaptive reviewer counts (3 for clear cases, 5 for escalated cases), a simple descriptive agreement statistic is reported rather than treating every rating as an independent identically distributed observation.

The per-case modal-choice agreement proportions are:

- General: 100%
- STEM: 80%
- Educator: 60%
- Hindi: 100%
- Bengali: 60%

Mean modal-choice agreement: **80%**. Two of five cases were unanimous.

The lower agreement in Educator and Bengali is consistent with why those cases triggered the predeclared adaptive escalation.

## Bootstrap uncertainty

The primary uncertainty calculation uses a **cluster bootstrap over the five H4 cases**, sampling cases with replacement so the adaptive 3-vs-5 reviewer allocation does not masquerade as 21 independent cases.

- replicates: 200,000
- deterministic analysis seed: `20260912`
- observed DPO share among decisive judgments: 43.75%
- 95% cluster-bootstrap CI: **0% to 83.3%**
- observed DPO case-majority rate: 40%
- 95% cluster-bootstrap CI: **0% to 80%**

These intervals are intentionally very wide because the independent evaluation unit is only five development cases. They reinforce that H4 is a diagnostic pilot, not a superiority study.

## Decision

**H4 result: mixed; no promotion decision.**

SFT remains the safer reference checkpoint for PAUL Open at this stage. DPO V2 Corrective is technically valid and shows clear positive behavior in some strata, especially the H4 STEM and Hindi cases, but H4 does not demonstrate broad superiority over SFT. The overall judgment-level preference tilts toward SFT (9 vs 7), and SFT wins 3 of 5 case majorities.

Therefore:

1. **Do not promote DPO V2 over SFT on H4 evidence alone.**
2. Preserve DPO V2 as a valid experimental checkpoint with useful domain-specific signals.
3. Treat General, Educator, and Bengali as development areas for diagnosis rather than silently changing evaluation methodology.
4. Retain the accessibility finding (screen-reader compatibility plus optional multilingual TTS assistance) for the next evaluator-interface iteration.
5. Keep SHAE sealed; H4 must not be presented as final assurance.

## Reproducibility trail

- blinded lock: `data/h4_dhe_pilot_v1_blinded_analysis_lock.json`
- analysis-lock record: `docs/H4_DHE_PILOT_V1_ANALYSIS_LOCK.md`
- safe unblinded aggregate: `data/h4_dhe_pilot_v1_unblinded_aggregate.json`
- controlled unblinding workflow: `.github/workflows/h4-dhe-controlled-unblind.yml`
- controlled unblinding run: GitHub Actions run `34683189304`
- safe aggregate artifact: `10294237980`

No private A/B mapping content is committed to the repository.
