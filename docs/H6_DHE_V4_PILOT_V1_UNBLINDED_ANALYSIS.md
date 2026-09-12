# PAUL Open — H6 DHE V4 Pilot V1 — Unblinded Development Analysis

**Date:** 2026-09-13  
**State:** UNBLINDED_DEVELOPMENT_ANALYSIS_COMPLETE  
**Batch:** `HEB1-5AE2CE4166CD`  
**Partition:** Development Human Evaluation (DHE)  
**Candidate:** `dpo_v4_corrective`  
**Reference:** `sft_reference`  
**SHAE:** sealed / not accessed

## Preconditions

This analysis was produced only after the blinded H6 lock was merged. The controlled unblinding workflow verified the lock, downloaded the private Kaggle mapping, created a safe aggregate, asserted that private mapping content was absent, and completed successfully.

The private A/B mapping, random seed, fingerprints and private case IDs are not published here.

## Human-evaluation result

H6 collected exactly 18 valid judgments: three independent judgments on each of six development cases. Every case was unanimous at the initial three-judgment stage, so the frozen adaptive rule did not require escalation to five.

| Development stratum | DPO V4 preferred | SFT preferred | Neither good | Agreement |
|---|---:|---:|---:|---:|
| STEM | 0 | 3 | 0 | 3/3 |
| Educator | 0 | 0 | 3 | 3/3 |
| Research | 0 | 3 | 0 | 3/3 |
| Hindi | 0 | 3 | 0 | 3/3 |
| Bengali | 0 | 3 | 0 | 3/3 |
| Spanish | 0 | 3 | 0 | 3/3 |
| **Total** | **0** | **15** | **3** | **18/18 modal agreement** |

There were no tie judgments and no `I'm not sure / I can't judge this` judgments. All required confidence checks were answered `Yes — confidently`.

## Interpretation

On these six frozen H6 development cases, DPO V4 did **not** produce a human-preference improvement over the SFT reference. The SFT response was unanimously preferred on five cases; on the Educator case, all three reviewers rejected both responses.

This is a strong diagnostic signal for this development batch, but it is **not** a final superiority or release claim. H6 contains only six curated development cases and is explicitly not SHAE. The correct conclusion is therefore that DPO V4 has not earned promotion on the basis of H6 and should be treated as a development candidate requiring further corrective work.

## Qualitative diagnostic observations

The reviewer-visible outputs indicate several concrete failure modes worth targeting in future development:

- **STEM:** the candidate response inferred equal speeds from equal-and-opposite momenta even though the prompt did not state equal cart masses. Equal momentum magnitudes do not imply equal speeds unless the masses are equal.
- **Research methodology:** the candidate proposed randomly shuffling day/plate labels while retaining treatment labels as a way to resolve confounding. That destroys the observed batch structure rather than identifying a treatment effect and is not a valid remedy for strong treatment-day confounding.
- **Educator:** both systems failed the requested pedagogical structure. Neither gave a concrete current measurement in the actual series circuit followed by a complete explanation; the responses stopped at analogies/questions. This is a shared capability gap rather than a candidate-only regression.
- **Hindi:** both responses were broadly on-task and scientifically plausible, but reviewers unanimously preferred the SFT response. This should be treated as a quality/precision/naturalness gap unless a later targeted audit identifies a harder factual distinction.
- **Bengali:** the candidate contained scientifically weak language around molecular collisions/instability as the mechanism of the spark and showed awkward Bengali phrasing. This is both a scientific-explanation and language-quality target.
- **Spanish:** the candidate response did not provide a sufficiently concrete sensor-validation sequence before public communication. It relied more on contextual plausibility than on direct checks such as corroborating nearby sensors/official monitors, calibration/QC history, time-series behavior and relevant environmental conditions.

These observations are development diagnoses, not new evaluation labels.

## Development decision

1. **Do not promote DPO V4 on H6 evidence.** Preserve the V4 artifact and hashes for reproducibility, but keep it as a non-promoted development candidate.
2. **Use H6 only for diagnosis.** The exact H6 cases are now development-exposed and must never be reused as clean evidence for a later candidate.
3. **Target the next corrective iteration** at the observed failure classes: physical constraints, confounding-aware research reasoning, instruction-complete Socratic tutoring, Bengali scientific naturalness/accuracy, and evidence-first uncertainty handling.
4. **Evaluate the next candidate on fresh, non-overlapping development cases.** A new DHE batch should test the same capability families without reusing H6 prompts or near-duplicates.
5. **Keep SHAE sealed.** Final assurance should remain untouched until a future candidate is frozen and has first passed fresh development evaluation and the existing automated validity/safety/contamination gates.

## Reproducibility

The safe unblinded aggregate is stored in `data/h6_dhe_v4_pilot_v1_unblinded_aggregate.json`.

The private mapping used for controlled unblinding is bound by SHA-256:

`f05f51524dc6e24e7d658ecf1ff7321e6db6b8d97af39a633aca348d4e825fdb`

The mapping content itself remains private.
