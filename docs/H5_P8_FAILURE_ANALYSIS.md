# PAUL Open — H5 P8 Failure Analysis

**Status:** COMPLETE  
**Date:** 2026-09-12  
**Evidence:** frozen H5 reviewer-facing response pairs plus the reviewer-safe controlled-unblinding aggregate.  
**Scope:** development diagnosis only; SHAE remains sealed.

## Method

Analyze the three H5 cases won by SFT (STEM, Educator, Hindi) and use the three DPO V3 wins (Bengali, General, Research) as preservation controls. Source identity is taken only from the safe aggregate after the blinded lock; the private A/B mapping itself is not exposed or committed.

Observations are kept separate from proposed remedies. H5 prompts, completions and evaluator comments remain evaluation material and must not be copied into later training data.

## Loss 1 — STEM preservation failure

The DPO V3 response correctly mentions decreasing moment of inertia and conservation of angular momentum, but its explanation of the speed increase leans on the claim that the same muscular torque produces greater angular acceleration. That is not the clean causal account requested for the pull-in maneuver. With negligible external torque, the central relationship is conservation of angular momentum as the mass distribution changes.

The response also fails to resolve the prompt's rotational-energy caveat. Rotational kinetic energy can increase as the person pulls the masses inward because the person does internal work; it does not appear from nowhere. An answer that merely says energy is not gained, or leaves the work term unexplained, is physically incomplete.

**Hypothesis:** the corrective optimization preserved concise causal language but did not robustly preserve multi-law physical consistency when the prompt simultaneously requires angular-momentum conservation and energy accounting.

**Actionable behavior class:** conservation-law explanations that explicitly distinguish conserved quantities from quantities changed by internal/external work, without introducing a spurious torque mechanism.

## Loss 2 — Educator preservation failure

The DPO V3 Socratic response acknowledges the learner's misconception but its follow-up comparison becomes physically confused: it frames a solar-eclipse comparison in a way that does not give the learner a clean observation capable of discriminating between the misconception and the correct mechanism.

The SFT response is not an ideal full tutorial either, but it offers a more coherent comparison between lunar and solar eclipse geometry and asks a question that better challenges the claim that Earth's shadow produces the monthly phases.

**Hypothesis:** V3's tutoring behavior can satisfy the surface form of “ask a question” while failing the deeper requirement that the question be diagnostically useful and scientifically coherent.

**Actionable behavior class:** Socratic questions should identify a concrete observation, prediction, diagram, comparison or measurement that would differ if the learner's misconception were true, while avoiding confused analogies or answer leakage.

## Loss 3 — Hindi preservation failure

The DPO V3 Hindi response is fluent at the sentence level but does not complete the requested explanation. It shifts into a sequence of questions/analogies and stops before delivering the temperature-pressure relationship and the requested calibration around the manufacturer's recommended pressure.

The SFT response also ends before fully resolving every requested point, but it supplies substantially more of the requested mechanism: hotter gas particles have greater average kinetic energy and, at approximately fixed tire volume, pressure tends to rise; cooling tends to lower pressure.

**Hypothesis:** V3 over-applied question-first/tutoring behavior into a direct-explanation setting and sacrificed answer completion and instruction coverage. This is a style-transfer/regression problem rather than simply a Hindi-fluency problem.

**Actionable behavior class:** multilingual direct explanations must first satisfy all requested explanatory components; Socratic questioning should not replace a requested explanation unless the user asks for tutoring.

## Preservation control 1 — Bengali gain

The DPO V3 response gives the physically correct wavelength ordering and the expected qualitative dispersion relationship: shorter-wavelength visible light such as violet generally experiences a larger refractive index in ordinary glass and bends more than longer-wavelength red light.

The competing response contains a reversed wavelength statement for red and violet, creating a clear factual defect despite otherwise fluent Bengali.

**Preserve:** multilingual scientific fluency tied to explicit checking of directional scientific invariants.

## Preservation control 2 — General gain

The DPO V3 response is more evidence-first. It asks the user to verify the spreadsheet error, assess its scope and determine whether it can change the conclusion before deciding how to communicate the update. This matches the post-H4 target of distinguishing observations from hypotheses and avoiding invented specifics.

The competing response gives more weight to organizational culture and presentation choices before the factual impact of the error is established.

**Preserve:** immediate evidence triage, uncertainty calibration and practical task decomposition before impression-management advice.

## Preservation control 3 — Research gain

The DPO V3 response foregrounds baseline checks, randomization integrity and, critically, an interaction test for a subgroup-specific treatment effect. This is substantially closer to the correct statistical question than relying on separate within-subgroup significance or ad-hoc robustness manipulations.

The competing response includes weaker diagnostics such as interpreting disappearance of an overall effect as evidence against a subgroup effect and intentionally misclassifying subgroup labels as a robustness check.

**Preserve:** explicit interaction/effect-modification reasoning, randomization-integrity checks and cautious separation of exploratory from pre-specified subgroup analysis.

## Cross-case diagnosis

H5 does not show a global collapse of DPO V3. It shows a tradeoff:

1. **Gains:** evidence-first general assistance, Bengali factual-direction fidelity, and research-methodology reasoning.
2. **Regressions:** conservation-law completeness in STEM, diagnostically useful Socratic questioning, and direct-answer completion in Hindi.
3. **Likely coupling:** the corrective emphasis on question-first tutoring appears capable of leaking into contexts where a direct explanation is requested, while scientific causal training remains vulnerable when multiple constraints/laws must be reconciled at once.

## P8 decision

P8 identifies actionable behavior classes, so P9 corrective-data design is justified.

A future corrective set should target:

- conservation-law consistency and energy accounting;
- discriminating/observable Socratic questions rather than question-shaped paraphrases;
- instruction-mode control: direct explanation versus tutoring;
- answer completion in Hindi and other multilingual direct explanations;
- explicit preservation examples for Bengali scientific fidelity, evidence-first general assistance and interaction-based research reasoning.

No H5 prompt, completion or evaluator comment may be copied into the new training data. DPO V4 training remains blocked until P9 and P10 are separately completed.
