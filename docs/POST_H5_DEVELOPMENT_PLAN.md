# PAUL Open — Post-H5 Development Gate

**Status:** PLANNED  
**Date:** 2026-09-12  
**Input:** H5 DHE V3 Pilot V1

## Evidence boundary

H5 is development evidence, not sealed assurance. DPO V3 tied SFT 9–9 at the judgment level and 3–3 at the case-majority level. DPO V3 won the fresh Bengali, General and Research cases; SFT won STEM, Educator and Hindi. All six cases were unanimous.

The pre-specified V3 preservation targets were STEM and Hindi. Both were lost in H5, so DPO V3 is not eligible for promotion or SHAE freeze.

## Frozen boundaries

1. Keep SFT as the reference checkpoint.
2. Preserve DPO V2 and DPO V3 as immutable experimental checkpoints.
3. Do not reinterpret H4 or H5 as final assurance.
4. Keep SHAE sealed until a future candidate passes development gates and is explicitly frozen.
5. Do not copy H5 prompts, responses, or evaluator comments into training data.
6. H4 and H5 cases cannot become future clean assurance cases.
7. Preserve the newly positive H5 Bengali, General and Research behavior rather than optimizing only the losing strata.
8. Do not start another DPO training run before the diagnostic and dataset gates below are complete.

## P8 — post-H5 failure analysis

Compare the frozen SFT and DPO V3 outputs for the three H5 cases won by SFT: STEM, Educator and Hindi. Produce case-specific observations and hypotheses. Keep observations separate from proposed remedies.

Also inspect the three DPO V3 wins (Bengali, General, Research) as preservation controls so proposed fixes do not erase the gains that motivated V3.

## P9 — corrective-data design

Only if P8 identifies actionable behavior classes, define a small development-only preference-data specification. It must use new prompts that are structurally distinct from H4, H5, prior DPO data and sealed SHAE material.

The specification must include both corrective examples for P8 weaknesses and preservation examples for the H5 wins.

## P10 — dataset audit

Before any training, require:

- schema and unique-ID checks;
- exact and near-duplicate checks against H4/H5 and prior DPO datasets;
- canonical benchmark leakage checking;
- multilingual language-quality review where applicable;
- scientific/research factual review where applicable;
- chosen/rejected preference-direction verification;
- provenance completeness;
- final dataset SHA-256.

A failed audit blocks training.

## P11 — future candidate training

Only after P8–P10 pass, train a new candidate under a separately recorded experiment identity. Reuse the validated training methodology unless a methodology change is explicitly proposed and independently justified. Never overwrite DPO V2 or DPO V3.

## P12 — automated gates

Apply the existing technical, contamination, safety and regression checks before human evaluation.

## P13 — fresh DHE

Use fresh development prompts not used in H4, H5 or training. Compare the future candidate against SFT using the existing blinded, complementary, durability-audited protocol.

## P14 — candidate freeze / SHAE decision

Only a candidate that survives P12 and P13 may be explicitly frozen for sealed assurance. SHAE remains sealed until that decision is recorded.

## Authorized now

- H5 result recording and publication-safe status updates;
- post-H5 response-level diagnosis;
- development-only corrective-data planning after diagnosis.

## Not authorized now

- DPO V4 training;
- opening or inspecting SHAE material;
- changing H4/H5 methodology retrospectively;
- claiming DPO V3 superiority;
- promoting DPO V3 over SFT.

## Completion condition for the next gate

P8 is complete when a response-level diagnosis exists for STEM, Educator and Hindi and preservation observations exist for Bengali, General and Research. P9 may begin only if P8 identifies actionable behavior classes.
