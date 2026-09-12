# PAUL Open — Current Research Status

**Status date:** 2026-09-12  
**Public research repository:** `foundrypaul-cloud/paul-open`  
**Public website:** https://open.paulfoundry.com/

This document is the concise public status layer. Detailed evidence remains in experiment-specific documents and immutable artifacts.

## Current position

PAUL Open has completed a full post-H4 development cycle through DPO V3 Corrective and the fresh H5 Development Human Evaluation (DHE).

The current research conclusion is:

> **SFT remains the reference checkpoint. DPO V3 Corrective is technically valid and produced positive fresh H5 signals in Bengali, General and Research, but H5 tied SFT overall and failed the pre-specified STEM/Hindi preservation objective. DPO V3 is therefore not promoted or frozen for SHAE.**

SHAE remains sealed and has not started.

## Experiment lineage

### DPO V2 Corrective

The immutable Step-2 freeze remains:

- branch: `research-freeze/step2-dpo-v2-20260909`
- SHA: `ac899e879f930f25b2081550bd8c5dd5c983df35`

DPO V2 was technically valid but H4 was mixed, so SFT remained the reference.

### Post-H4 development

The repository then completed:

- **P1:** H4 response-level failure analysis;
- **P2:** corrective-data specification;
- **P3:** 30-pair audited DPO V3 corrective dataset;
- **P4:** DPO V3 training with the validated DPO V2 methodology;
- **P5:** automated technical, contamination and regression gates;
- **P6/H5:** fresh blinded DHE against SFT.

The final DPO V3 corrective dataset SHA-256 is `5ce4a82f32827a07f339d2b8c437dc4b45ec3f60ac9f5d50f165ea308369c741`.

## H4 — completed development evidence

H4 compared DPO V2 Corrective with SFT on five eligible development cases and 21 judgments. Aggregate result: DPO V2 7, SFT 9, about equal 2, neither 0, not sure 3. DPO V2 won the STEM and Hindi case majorities; SFT won General, Educator and Bengali. Decision: mixed, no promotion.

See [`H4_DHE_PILOT_V1_RESULTS.md`](H4_DHE_PILOT_V1_RESULTS.md).

## H5 — completed fresh DHE for DPO V3

Batch: `HEB1-64CDCC9521D3`

- eligible fresh cases: 6
- complementary blinded forms: 12
- frozen initial judgments: 18
- adaptive follow-up judgments: 0
- final judgments: **18**
- collection closed: yes
- durability audit: PASS
- blinded analysis lock: committed before unblinding
- controlled unblinding: PASS

All six cases were unanimous 3/3 after complementary display-swap normalization, so the frozen 3→5 adaptive rule was not triggered.

### H5 aggregate result

| Outcome | Count |
|---|---:|
| DPO V3 preferred | 9 |
| SFT preferred | 9 |
| About equal | 0 |
| Neither good | 0 |
| Not sure / unable to judge | 0 |

Case results:

- STEM — SFT
- Educator — SFT
- Research — DPO V3
- Hindi — SFT
- Bengali — DPO V3
- General — DPO V3

Case-majority split: **3 DPO V3 / 3 SFT**. Mean modal-choice agreement: **100%**.

The controlled-unblinding workflow exposed only a safe aggregate. The private A/B mapping, randomization seed, fingerprints and private case identifiers remain outside the public repository.

See:

- [`H5_DHE_V3_PILOT.md`](H5_DHE_V3_PILOT.md)
- [`H5_DHE_V3_PILOT_V1_ANALYSIS_LOCK.md`](H5_DHE_V3_PILOT_V1_ANALYSIS_LOCK.md)
- [`H5_DHE_V3_PILOT_V1_RESULTS.md`](H5_DHE_V3_PILOT_V1_RESULTS.md)

## H5 decision

**Mixed; no DPO V3 promotion. Preservation objective failed.**

The post-H4 plan explicitly designated STEM and Hindi as preservation strata. Both fresh H5 cases favored SFT unanimously. Although DPO V3 won Bengali, General and Research, the aggregate 9–9 tie does not satisfy the pre-specified preservation requirement. Educator also remains a reference win.

Therefore:

- SFT remains the reference checkpoint;
- DPO V2 and DPO V3 remain immutable experimental checkpoints;
- DPO V3 is not frozen for SHAE;
- SHAE remains sealed;
- H4 and H5 remain development evidence only.

## Immediate next research step

The next authorized work is **post-H5 diagnosis**, not DPO V4 training.

`POST_H5_DEVELOPMENT_PLAN.md` requires response-level analysis of the H5 STEM, Educator and Hindi losses while using Bengali, General and Research as preservation controls. Only if that diagnosis identifies actionable behavior classes may a new corrective-data specification be created and separately audited before any new training run.

See [`POST_H5_DEVELOPMENT_PLAN.md`](POST_H5_DEVELOPMENT_PLAN.md).

## Claim boundary

### Supported

- DPO V2 and DPO V3 are technically valid experimental checkpoints;
- H4 and H5 DHE are complete;
- H5 collected 18 judgments across six fresh development cases;
- H5 result was 9 DPO V3 preferences and 9 SFT preferences;
- DPO V3 won Bengali, General and Research H5 cases;
- SFT won STEM, Educator and Hindi H5 cases;
- DPO V3 failed the pre-specified STEM/Hindi preservation objective;
- DPO V3 was not promoted;
- SFT remains the reference checkpoint;
- SHAE remains sealed.

### Not supported

- DPO V3 is broadly superior to SFT;
- the 9–9 H5 result establishes equivalence;
- six unanimous cases establish domain-wide behavior;
- H5 is final assurance;
- SHAE has started or passed;
- H4/H5 cases can later be treated as untouched assurance evidence.

## Public website state

The website is a presentation layer and should consume:

- [`../public/research-status.json`](../public/research-status.json)
- [`../public/human-evaluation.json`](../public/human-evaluation.json)

No public human-evaluation round is accepting responses. Reviewer links, response sheets, private A/B mappings and SHAE material remain non-public.
