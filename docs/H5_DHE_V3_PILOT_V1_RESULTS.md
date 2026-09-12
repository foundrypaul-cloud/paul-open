# PAUL Open — H5 DHE V3 Pilot V1 Results

**Date:** 2026-09-12  
**Partition:** Development Human Evaluation (DHE)  
**Batch:** `HEB1-64CDCC9521D3`  
**Candidate:** DPO V3 Corrective  
**Reference:** SFT  
**Decision:** MIXED — NO PROMOTION / PRESERVATION FAILURE  
**SHAE:** sealed / not started

## Collection and durability

The frozen initial allocation completed exactly at 18 valid judgments: three judgments for each of six fresh development cases. All six cases were unanimous after complementary A/B display normalization, so the frozen adaptive rule did not authorize escalation to five judgments.

The collection was closed before unblinding. Durability passed with 18 accepted responses, 18 normalized rows, 18 independent backup-ledger rows, exact normalized/backup response-ID agreement, and SHA-256 snapshot coverage for every backup row.

The blinded analysis was committed before the private A/B mapping was consulted. Controlled unblinding ran in GitHub Actions and emitted only a reviewer-safe aggregate. The private mapping, seed, fingerprints and private case identifiers remain uncommitted.

## Aggregate result

| Outcome | Judgments |
|---|---:|
| DPO V3 Corrective preferred | 9 |
| SFT preferred | 9 |
| About equal | 0 |
| Neither good | 0 |
| Not sure | 0 |

The decisive preference share is therefore 50% DPO V3 and 50% SFT. This small DHE pilot is not a superiority study.

## Case results

| Case | Human result | Agreement |
|---|---|---:|
| STEM | SFT preferred | 3/3 |
| Educator | SFT preferred | 3/3 |
| Research | DPO V3 preferred | 3/3 |
| Hindi | SFT preferred | 3/3 |
| Bengali | DPO V3 preferred | 3/3 |
| General | DPO V3 preferred | 3/3 |

Case-majority split: DPO V3 wins 3/6 and SFT wins 3/6. Mean modal agreement is 100%.

## Research interpretation

H5 provides encouraging case-specific evidence that the post-H4 corrective work improved behavior on the fresh Bengali, General and Research cases. However, the candidate lost the fresh STEM and Hindi cases unanimously. Those two strata were explicitly designated preservation targets before V3 training. Educator also remains a reference win.

The preservation requirement therefore failed. The 9–9 aggregate tie does not override that pre-specified development objective.

## Decision

**Do not promote or freeze DPO V3 for SHAE.**

- SFT remains the reference checkpoint.
- DPO V2 and DPO V3 remain immutable experimental checkpoints.
- H5 remains development evidence and cannot be reclassified as sealed assurance evidence.
- SHAE remains sealed.
- No DPO V4 training is authorized merely from this result.

The next development stage is a post-H5 diagnosis of the tradeoff: preserve the newly positive Bengali/General/Research behavior while investigating the fresh STEM/Hindi preservation regressions and the persistent Educator weakness. Any new corrective dataset must pass a separate design and audit gate before another training run.

## Controlled-unblinding evidence

GitHub Actions controlled-unblinding run: `34699579869`  
Safe artifact: `h5-dhe-unblinded-safe-aggregate` / artifact ID `10300165925`  
Artifact digest: `sha256:11e162c93965521404bb5b38f224588d3b3e531be29d80be9a598e3f246135dc`

The safe aggregate records the SHA-256 of the private mapping without exposing its contents.
