# PAUL Open — Post-H4 Development Plan

**Status:** PLANNED  
**Date:** 2026-09-12  
**Input evidence:** H4 DHE Pilot V1 (`docs/H4_DHE_PILOT_V1_RESULTS.md`)

## Purpose

H4 produced mixed development evidence: DPO V2 Corrective was preferred in the STEM and Hindi cases, while SFT was preferred in the General, Educator, and Bengali cases. H4 is Development Human Evaluation (DHE), not sealed assurance, so its findings may guide development but must not be represented as final superiority evidence.

The next phase is therefore diagnosis and candidate design, not automatic retraining and not SHAE.

## Frozen boundaries

1. Keep SFT as the reference checkpoint.
2. Preserve DPO V2 Corrective as an immutable experimental checkpoint.
3. Do not modify or reinterpret the completed DPO V2 methodology or H4 result.
4. Keep SHAE sealed until a future candidate is frozen.
5. Do not copy evaluator comments directly into training data.
6. Do not use H4 cases as future clean assurance cases.
7. Preserve the observed STEM and Hindi behavior rather than optimizing only for the three weaker H4 strata.

## Development targets

The diagnostic priority strata are:

- General: investigate why all three H4 judgments preferred SFT.
- Educator: investigate usefulness, pedagogical structure, calibration, and the mixed/tie/uncertain judgments before designing any corrective data.
- Bengali: investigate native-language quality, clarity, technical terminology handling, and the mixed/tie/uncertain judgments before designing any corrective data.

The preservation strata are:

- STEM: retain the DPO V2 behavior that produced four DPO preferences and one unable-to-judge judgment.
- Hindi: retain the DPO V2 behavior that produced three DPO preferences.

These are diagnostic directions, not claims that a single H4 prompt represents an entire domain or language.

## Required sequence before any new training

### P1 — Failure analysis

Compare the frozen SFT and DPO V2 outputs for the three weaker H4 cases. Produce structured, case-specific hypotheses about response differences. Keep observations separate from proposed remedies.

### P2 — Corrective-data design

If P1 identifies actionable behaviors, design new development-only examples that target the behavior class without copying H4 prompts or evaluator comments. Include preservation examples for STEM/Hindi behavior where appropriate.

### P3 — Dataset audit

Before training, require checks for duplication, leakage from H4/SHAE, language quality, preference direction, formatting, and intended behavioral coverage. Record dataset hashes and provenance.

### P4 — Candidate training

Only after P1–P3 pass may a new candidate be trained. Use a new experiment identifier; never overwrite DPO V2 artifacts.

### P5 — Automated gates

Run the existing technical, safety, contamination, and regression gates. A failed candidate does not advance to human evaluation.

### P6 — Fresh DHE

Build fresh development prompts that are not the H4 cases and compare the frozen candidate against SFT using the existing blinded/counterbalanced human-evaluation protocol.

### P7 — Candidate freeze and SHAE

Only if a future candidate survives development evaluation should it be frozen for sealed assurance. SHAE prompts remain sealed until that point.

## Current authorization

Authorized now:

- repository and artifact audit;
- H4 failure analysis;
- development-only corrective-data planning;
- accessibility improvements to the evaluator interface that do not alter completed H4 data.

Not authorized yet:

- automatic new DPO training before the diagnostic/data gates are complete;
- changing the H4 methodology after seeing results;
- treating H4 as final assurance;
- opening SHAE;
- promoting DPO V2 over SFT.

## Accessibility requirement for the next evaluator interface

The next evaluator interface must remain keyboard and screen-reader operable and should add optional multilingual text-to-speech assistance where feasible. TTS is supplementary and must not replace semantic labels, logical reading order, focus handling, or standard assistive-technology compatibility.

## Completion condition

This planning gate is complete when P1 failure analysis and, if justified, a separately reviewed corrective-data specification exist in the repository. Training remains a later explicit gate so that H4 findings cannot silently mutate the frozen experiment methodology.
