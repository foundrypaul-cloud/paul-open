# PAUL OPEN — DPO v2 CORRECTIVE DATASET AUDIT

> **POST-RUN RESEARCH-INTEGRITY NOTE (2026-09-09):** The original audit below correctly checked the 14 corrective pairs against the 10-case permanent DPO holdout, but that scope was insufficient for the repository's broader contamination-prevention contract. Subsequent post-run analysis found reuse/overlap with the canonical 50-case baseline suite. The DPO V2 50-case SFT-vs-DPO comparison must therefore be treated as **diagnostic/contaminated for DPO V2, not as a clean held-out superiority evaluation**. See `docs/EXPERIMENT_JOURNEY_E4B.md` and Section 12 below.

## 1. DPO v1 Bias Summary
The forensic analysis of DPO v1 revealed a strong bias toward conciseness, with 78.5% of chosen responses shorter than their rejected counterparts. This caused regressions in cases where depth, structure, or emotional warmth was explicitly required (e.g., scientific explanations, detailed plans, and empathy).

## 2. DPO v2 Design Rationale
**Length is not being used as the preference target.**
The DPO v2 dataset injects exactly 14 corrective pairs designed to teach **Contextual Response Calibration**. The pairs explicitly penalize inappropriate brevity, robotic coldness, and lack of structure where verbosity and detail are necessary, while simultaneously penalizing unhelpful rambling, irrelevant tangents, and unnecessary complexity where brevity and simplicity are requested. The final dataset reflects a balanced distribution of response lengths so the model learns task fitness rather than a length shortcut.

## 3. All 14 Pair IDs
paul_dpo_v2_sci_exp_001, paul_dpo_v2_sci_exp_002, paul_dpo_v2_sci_exp_003, paul_dpo_v2_sci_exp_004, paul_dpo_v2_emp_001, paul_dpo_v2_emp_002, paul_dpo_v2_emp_003, paul_dpo_v2_emp_004, paul_dpo_v2_plan_001, paul_dpo_v2_plan_002, paul_dpo_v2_tch_001, paul_dpo_v2_tch_002, paul_dpo_v2_ind_001, paul_dpo_v2_ind_002

## 4. Category Distribution
- Scientific explanation: 4
- Empathy / human-centered: 4
- Structured planning: 2
- Teacher assistance: 2
- Indic detailed explanation: 2

## 5. Language Distribution
{
  "en": 11,
  "hi": 1,
  "bn": 1,
  "ta": 1
}

## 6. Domain Distribution
{
  "biology": 3,
  "physics": 4,
  "chemistry": 2,
  "mathematics": 2,
  "computer_science": 2,
  "astronomy": 1
}

## 7. Rejection Reason Distribution
{
  "technically_impressive_but_unnecessarily_complicated": 1,
  "scientifically_misleading_and_rambling": 1,
  "excessive_brevity_removing_reasoning": 1,
  "irrelevant_historical_and_advanced_tangent": 1,
  "unhelpful_lecture_lacking_empathy": 1,
  "excessive_emotional_verbosity_without_actionable_help": 1,
  "brief_but_emotionally_dismissive": 1,
  "unsolicited_and_stressful_generic_advice": 1,
  "too_concise_lacking_actionable_structure": 1,
  "excessively_verbose_without_actionable_technical_structure": 1,
  "concise_but_missing_evaluation_dimensions": 1,
  "lacks_structured_guidance_and_scientific_rigor": 1,
  "excessively_brief_lacking_educational_depth": 1,
  "irrelevant_rambling_and_unrelated_tangent": 1
}

## 8. Chosen/Rejected Length Statistics (10% diff margin for equality)
- Chosen shorter than rejected: 4 (28.6%)
- Chosen longer than rejected: 5 (35.7%)
- Approximately equal length: 5 (35.7%)
- Average Chosen/Rejected length ratio: 2.35

## 9. Validation Results
The dataset successfully neutralizes the unidirectional brevity bias of v1 (where 78.5% were shorter) by balancing the length distribution (5 longer, 4 shorter, 5 equal). Chosen responses are rewarded for task fitness (accuracy, empathy, actionable structure) rather than simply token length. The JSONL conforms to the canonical DPO schema.

## 10. Original Holdout-Overlap Check
Verified at the time of the original audit: 0% overlap with the **10-case DPO holdout IDs** (`paul_dpo_ind_001`, `paul_dpo_soc_005`, etc.) or their semantic content. None of those 10 DPO-holdout prompts were reused.

This statement must not be interpreted as proof of isolation from the canonical baseline, capability-preservation, or held-out-behavioral suites.

## 11. Original Pair-Ambiguity Review
The preference direction was judged decoupled from raw length; for example, `paul_dpo_v2_sci_exp_004` rewards brevity because the rejected response includes irrelevant history, whereas `paul_dpo_v2_tch_001` rewards length because a full rubric inherently requires details. No pair was intentionally designed with length alone as the preference target.

## 12. Post-run contamination correction

The repository's `docs/TRAINING_DATA_SPECIFICATION.md` defines a stricter boundary: the 110 cases across the canonical baseline (50), capability-preservation (30), and held-out behavioral (30) suites are strictly held out and must not be used as source material, templates, or references for model development.

Post-run inspection found that DPO V2 did not satisfy that broader boundary:

1. **Exact prompt reuse:** `paul_dpo_v2_tch_001` uses the same enzyme-catalysis four-level analytic-rubric prompt as canonical baseline case `TCH-ASST-003`.
2. **Direct content reuse:** `paul_dpo_v2_emp_004` contains the same Hindi math-stress user statement embedded in baseline empathy case `EMP-HUM-002`.
3. **Template-level overlap:** `paul_dpo_v2_plan_001` uses the same structured three-day revision-plan task pattern as baseline `STU-ASST-001`, with subject matter changed.
4. **Concept/template overlap:** `paul_dpo_v2_sci_exp_002` is a sky-color/Rayleigh-scattering explanation task closely related to a canonical scientific-explanation case.

### Research consequence

The successful DPO V2 training run remains technically valid, but its 50-case canonical-baseline evaluation is **not a clean held-out generalization test for DPO V2**. The scores remain useful for regression discovery and paired behavioral analysis, but they must not support a superiority claim.

Before a future DPO dataset is trained, contamination auditing must cover the complete frozen evaluation registry, not only the 10 DPO holdout IDs. Exact, lexical/n-gram, template/structural, semantic, and numerical-collision checks should be recorded against the accepted training-dataset hash.
