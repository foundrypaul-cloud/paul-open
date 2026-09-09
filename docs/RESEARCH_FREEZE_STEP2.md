# PAUL Open — Step 2 Research Freeze

**Freeze date:** 2026-09-09  
**Frozen commit:** `ac899e879f930f25b2081550bd8c5dd5c983df35`  
**Frozen branch:** `research-freeze/step2-dpo-v2-20260909`

This snapshot is the canonical repository state after Step 0 (foundation/SFT), Step 1 (DPO V1 learning), Step 2 (DPO V2 corrective training/evaluation), the experiment-history documentation, and the technical-term-aware English→Indic translation evaluation policy.

## Freeze rule

The frozen branch must not be advanced or repurposed. Future research, evaluation-engineering, data, training, and documentation changes must occur from new branches and must reference this exact commit when describing the Step 2 state.

The commit SHA is the immutable authority. The branch exists only as a human-readable pointer to that SHA.

## Research status at freeze

- The historical SFT adapter remains the safer reference checkpoint.
- DPO V2 is a technically valid trained checkpoint.
- DPO V2 has mixed behavioral effects and has **not** demonstrated overall superiority over SFT.
- The current 50-case DPO V2 comparison is diagnostic rather than clean held-out evidence because the corrective dataset is not fully isolated from the canonical baseline suite.
- English→Indic translation scores must be interpreted with technical-term preservation in mind; native-script coverage alone is not a sufficient quality metric.
- No DPO V3 or other new training should begin until the evaluation and human-comparison workflow is engineered and validated.

## Next research boundary

Work after this freeze belongs to the evaluation-engineering phase. Its first deliverable is a contamination-safe, blinded, low-friction human evaluation workflow that can be automated using Google Forms/Sheets without exposing model identity or software jargon to reviewers.
