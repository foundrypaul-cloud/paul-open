# PAUL Open Evaluation Methodology

PAUL Open treats evaluation as a **multi-layer research process**, not as a single-score ranking exercise. A higher aggregate number is supporting evidence only; it is not sufficient to claim that one checkpoint is superior.

## Current evaluation layers

1. **Technical validity** — did the intended training/update actually occur with correct provenance, topology, parameter changes, and reproducible runtime?
2. **Automated regression signals** — keyword coverage, safety/anti-anthropomorphism checks, script checks, length/structure checks, latency, and domain summaries.
3. **Behavioral quality** — factual correctness, pedagogical usefulness, task fitness, multilingual naturalness, and paired qualitative review.
4. **Superiority / release decision** — clean held-out evaluation, capability preservation, robustness, and blinded human preference.

The current historical 50-case anchor is documented in [BASELINE_EVALUATION.md](BASELINE_EVALUATION.md). The Base → SFT → DPO V1 → DPO V2 research history and present limitations are documented in [EXPERIMENT_JOURNEY_E4B.md](EXPERIMENT_JOURNEY_E4B.md).

## Translation-specific interpretation

English → Indic scientific translation must **not** be scored as if every token should be converted into an Indic script.

Standard formulas, equations, SI units, scientific notation, acronyms, gene/protein symbols, software/API names, and established technical terms may correctly remain in their conventional Latin/English form. In these cases, a lower legacy script or keyword score can occasionally represent a **better and more technically faithful translation**.

At the same time, broad romanization of ordinary target-language prose remains a genuine failure when native script is expected. The evaluator therefore needs to distinguish:

- protected technical spans that should not incur a script penalty; and
- romanization of the surrounding natural-language text.

The full policy and proposed scoring revision are defined in [TRANSLATION_EVALUATION_POLICY.md](TRANSLATION_EVALUATION_POLICY.md).

## Current research limitations

- The existing heuristic rubric is a regression signal, not a semantic correctness judge.
- `scripts/evaluate.py --eval` must be made authoritative before the next clean comparison; the current CLI path still needs evaluation-suite/config enforcement.
- DPO V2's current 50-case comparison is diagnostic rather than clean held-out superiority evidence because the corrective dataset is not fully isolated from the canonical evaluation suite.
- Translation results should be reinterpreted under the technical-term-aware policy above rather than using raw script percentage alone.

## Next evaluation revision

Before another preference-training round, PAUL Open should:

1. freeze a machine-readable registry of all held-out evaluation prompts;
2. enforce exact, lexical, template, semantic, and numerical-overlap checks against every training dataset;
3. make evaluation configuration and suite selection authoritative and provenance-tracked;
4. separate task-specific metrics rather than collapsing them into one headline score;
5. add protected-span-aware translation scoring;
6. run deterministic regression tests plus multi-seed stochastic evaluation where appropriate;
7. use blinded bilingual/subject-matter human review for release decisions.

## Canonical evaluation references

- [BASELINE_EVALUATION.md](BASELINE_EVALUATION.md)
- [TRANSLATION_EVALUATION_POLICY.md](TRANSLATION_EVALUATION_POLICY.md)
- [EXPERIMENT_JOURNEY_E4B.md](EXPERIMENT_JOURNEY_E4B.md)
- [EVALUATION_SUITES_GUIDE.md](EVALUATION_SUITES_GUIDE.md)
- [TRAINING_DATA_SPECIFICATION.md](TRAINING_DATA_SPECIFICATION.md)
