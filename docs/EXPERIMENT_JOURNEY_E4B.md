# PAUL Open E4B Experiment Journey — Foundation → DPO V1 → DPO V2

**Status date:** 2026-09-09  
**Model family:** `google/gemma-4-E4B-it`  
**Purpose:** maintain a single evidence-oriented record of how PAUL Open started, what the first preference-tuning round taught us, what the current DPO V2 run achieved, what failed, and what must be improved next.

> **Research principle:** A higher aggregate benchmark number is not sufficient evidence that a model is superior. PAUL Open should be judged by useful behavioral improvement on its intended capabilities, preservation of existing strengths, factual correctness, multilingual quality, human-centered behavior, reproducibility, and clean evaluation methodology.

---

## 1. North star: what PAUL Open is trying to become

PAUL Open is not primarily a score-optimization exercise. The project exists to specialize Gemma 4 for a specific combination of capabilities:

1. Indian and multilingual language understanding/generation.
2. Translation and code-switching, with correct native-script output.
3. Science education and rigorous conceptual explanation.
4. Socratic tutoring and misconception-guided learning.
5. Student assistance and structured learning support.
6. Teacher assistance and educational material generation.
7. Human-centered empathy without false anthropomorphic claims.
8. Scientific research assistance.
9. Life-science/biomedical reasoning.
10. General reasoning, instruction following, and eventually multimodal scientific work.

The optimization objective is therefore **behavioral usefulness under preservation constraints**, not “maximize one composite score.”

---

## 2. How to read this history

There are four distinct evidence layers in the project:

| Layer | Question answered | What counts as evidence |
|---|---|---|
| **Technical validity** | Did training actually happen as intended? | provenance, hashes, optimizer/parameter-change gates, GPU/reference topology, reproducible runtime |
| **Automated regression signal** | Did observable benchmark indicators move? | keyword coverage, script match, safety, length, latency, suite-level scores |
| **Behavioral quality** | Did responses become more useful/correct? | paired qualitative review, factual checks, task-specific rubrics, blinded human preference |
| **Model superiority** | Is the new checkpoint better overall for PAUL Open's goal? | clean held-out evaluation + preservation + human review + robustness across prompts/seeds/languages |

A run may pass the first layer while failing the fourth. DPO V2 is an example: the training run is technically valid, while superiority is **not established**.

---

# STEP 0 — Foundation: base model, benchmark, and SFT starting point

## 3. Base model and initial benchmark design

The project began from the unmodified `google/gemma-4-E4B-it` checkpoint and created an original 50-case baseline benchmark covering 10 capability domains and 10 languages. The benchmark was intended as an anchor before fine-tuning, not as a complete measure of intelligence or usefulness.

The 50-case suite covers:

- science reasoning
- life sciences
- scientific research assistance
- Socratic tutoring
- student assistance
- teacher assistance
- Indic understanding
- multilingual translation
- empathy / human-centered interaction
- scientific explanation

The original evaluation framework uses deterministic checks for keyword coverage, anti-anthropomorphism/safety, native-script match, and output-length compliance, combined into a heuristic rubric score. Subjective domains are explicitly meant to receive human review.

### Important limitation already visible in Step 0

The heuristic rubric is useful as a **regression detector**, but it cannot determine semantic correctness by itself. A response can gain points by including expected keywords while becoming scientifically weaker, and a response can lose points despite being pedagogically better. This matters strongly in the DPO V2 analysis below.

## 4. Training-data design derived from baseline diagnosis

The Phase 3 data specification was designed to improve behavioral deficits while preserving Gemma's existing strengths. The planned corpus was:

- **SFT:** 180 examples.
- **DPO:** 65 preference pairs.
- **DPO training subset:** 55 pairs.
- **Permanent DPO holdout:** 10 pairs.

The SFT design emphasized four adaptation targets:

1. **Socratic tutoring** — avoid premature lecture dumping; scaffold with focused questions.
2. **Concise STEM problem solving** — structured calculation without unnecessary preamble.
3. **Clean multilingual translation** — direct native-script translation with technical notation preserved.
4. **Natural Indic pedagogical tone** — modern classroom register rather than stilted/archaic wording.

Capability-preservation examples were also included for teacher assistance, scientific explanation, life sciences, empathy, and safety.

## 5. SFT foundation checkpoint

The historical SFT adapter is the authoritative starting point for the DPO work:

- logical source: `paulfoundry/paul-open-sft`
- base: `google/gemma-4-E4B-it`
- LoRA rank: 16
- LoRA alpha: 32
- LoRA dropout: 0.05
- task type: `CAUSAL_LM`
- bias: none

The repository's canonical SFT/QLoRA recipe specifies 3 epochs, batch size 1, gradient accumulation 16, learning rate `2e-4`, sequence length 4096, gradient checkpointing, and paged 8-bit AdamW. The current repository does **not** contain the original SFT run's complete immutable training manifest, so these recipe values should be distinguished from artifact-verified historical runtime values.

### Current re-evaluation of the SFT checkpoint

During the final DPO V2 production workflow, the historical SFT adapter was re-evaluated on the 50-case baseline suite:

- 50/50 cases completed
- 0 failures
- mean heuristic rubric: **90.26**
- safety / anti-anthropomorphism adherence: **100%**
- mean latency: **37.60 s**
- 17 cases flagged for human review

This is the present comparison anchor for DPO V2.

### Evidence gap to preserve in the history

The repository currently preserves the baseline framework and SFT provenance, but not the original numeric **base-model baseline result artifact** nor the complete historical SFT run manifest. Those should be added later if recovered from the original experiment storage. They must not be reconstructed from memory or inferred.

---

# STEP 1 — First preference round: DPO V1

## 6. What DPO V1 attempted

The first preference round followed the original DPO design: contrast desirable educational behavior against plausible but inferior outputs. The original corpus architecture allocated preference data to Socratic tutoring, concise STEM, clean translation, and natural Indic tone, with a permanent 10-record holdout.

## 7. What we learned from DPO V1

The later forensic audit identified a major bias in the DPO V1 preference construction:

- **78.5% of chosen responses were shorter than rejected responses.**
- The preference signal therefore risked teaching a shortcut: “shorter is better.”
- Regressions appeared where depth, structure, or emotional warmth were actually required, particularly scientific explanations, detailed plans, and empathy.

This is an important research result. The failure was not simply that a score moved down. It showed that the **preference dataset encoded an unintended latent objective**.

### Step 1 conclusion

DPO V1 demonstrated that preference optimization can successfully move behavior, but that the model can learn the easiest statistical shortcut in the pair construction rather than the intended abstract principle. This motivated DPO V2.

### Evidence gap for Step 1

The repository contains the forensic DPO V1 bias summary but does not currently contain a complete immutable DPO V1 training/evaluation manifest in `results/`. If the original DPO V1 artifact is recovered, this document should be updated with its exact source revision, run parameters, checkpoint hashes, and evaluation numbers.

---

# STEP 2 — Current round: DPO V2 Corrective

## 8. Why DPO V2 was created

DPO V2 introduced 14 corrective preference pairs intended to teach **contextual response calibration** rather than a global brevity preference.

The 14-pair audit describes the distribution as:

- scientific explanation: 4
- empathy / human-centered: 4
- structured planning: 2
- teacher assistance: 2
- Indic detailed explanation: 2

Language distribution is heavily English-skewed:

- English: 11
- Hindi: 1
- Bengali: 1
- Tamil: 1

That distribution is itself important when interpreting multilingual outcomes: DPO V2 contains **no Punjabi, Telugu, Malayalam, Kannada, Gujarati, Marathi, or Assamese corrective pair**.

## 9. DPO V2 technical training result

The final successful production run is technically valid.

### Provenance

- experiment: `paul_e4b_dpo_v2_corrective`
- source revision used by the final run: `3e564d95e72c5f83220179dca6dcd7520b5c03d8`
- base model revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`
- dataset: `data/train/dpo_v2_corrective.jsonl`
- dataset records: 14
- dataset SHA-256: `046f9c74aefc4491cb14c769d8c94c4bdedd83b223d23476b4ba30a535269a73`
- historical adapter: `paulfoundry/paul-open-sft`

### Locked training configuration

- method: DPO sigmoid loss
- beta: `0.1`
- learning rate: `5e-7`
- epochs: `4`
- batch size: `1`
- gradient accumulation: `8`
- max length: `4096`
- FP16: enabled
- optimizer: `paged_adamw_8bit`
- gradient checkpointing: enabled

### Runtime topology

- required GPUs: 2 × Tesla T4
- policy: GPU 0
- frozen external reference: GPU 1
- policy adapter: `dpo`
- reference adapter: `sft`
- both base models: 4-bit NF4

### Completion evidence

The final `training_manifest.json` reports:

- completion gate: **PASS**
- 516 intended trainable tensors
- **516/516 trainable tensors changed**
- finite parameter-update evidence: PASS
- adapter topology: PASS
- optimizer membership: PASS
- placement: PASS
- frozen-reference evaluation: PASS
- policy/reference storage independence: PASS
- external-reference math equivalence: PASS
- max absolute math difference: **0.0**
- max relative math difference: **0.0**
- global step: 4
- train loss: **0.687744140625**
- train runtime: **238.58 s**

This establishes that DPO V2 is a real trained adapter, not a no-op or skipped-optimizer artifact.

---

# STEP 2 EVALUATION — SFT vs DPO V2

## 10. Automated comparison

Both checkpoints completed 50/50 baseline cases with zero execution failures.

| Metric | SFT | DPO V2 | Change |
|---|---:|---:|---:|
| Mean heuristic rubric | 90.26 | 89.79 | **-0.47** |
| Safety adherence | 100% | 100% | 0 |
| Mean latency | 37.60 s | 41.04 s | +3.44 s |

Across the 50 paired cases:

- **11 improved** by the heuristic score
- **16 regressed**
- **23 were unchanged**
- median case delta: **0**
- mean case delta: **-0.464**

### Domain-level deltas

| Domain | SFT | DPO V2 | Delta |
|---|---:|---:|---:|
| Scientific research | 92.80 | 95.47 | **+2.67** |
| Teacher assistance | 93.38 | 95.67 | **+2.29** |
| Scientific explanation | 89.60 | 91.47 | **+1.87** |
| Science reasoning | 92.27 | 93.87 | **+1.60** |
| Empathy / human-centered | 78.40 | 81.60 | **+3.20** |
| Life sciences | 98.40 | 98.67 | +0.27 |
| Student assistance | 93.18 | 92.72 | -0.46 |
| Socratic tutoring | 75.73 | 73.87 | **-1.87** |
| Indic understanding | 95.20 | 92.00 | **-3.20** |
| Multilingual translation | 93.60 | 82.60 | **-11.00** |

These values are diagnostic, not proof of superiority.

---

# 11. Paired qualitative analysis

## A. Clear regression: Punjabi translation / script fidelity

`TRANS-005` is the strongest failure.

- SFT: 84
- DPO V2: 45
- expected script: Gurmukhi
- SFT detected script: Gurmukhi
- DPO detected script: **Latin**

The DPO response produced romanized Punjabi (`Paani di ...`) instead of Punjabi in Gurmukhi. This is a direct violation of one of PAUL Open's core multilingual goals. It is more important than the aggregate -0.47 point change because it is a **capability regression on a declared target behavior**.

## B. Clear semantic regression: elevator/Newtonian mechanics

`SCI-REAS-002` fell from 100 to 84. More importantly, the DPO answer introduced a physically misleading explanation that the elevator floor moves away “at a faster rate than gravity pulls” the person. The correct relation is about the reduced normal force under downward acceleration, e.g. `N = m(g-a)` for downward acceleration magnitude `a`.

This case demonstrates why keyword-based scoring is insufficient: the important issue is not only missing words, but the introduction of an incorrect physical mechanism.

## C. Apparent improvement that is probably real: teacher-rubric completeness

`TCH-ASST-003` rose from 88.57 to 100. The DPO answer includes all four requested performance levels and is structurally more complete than the truncated/incomplete SFT rubric.

However, this case **cannot be treated as clean evidence of generalization**, because the exact evaluation prompt appears in the DPO V2 corrective training data. See the contamination section below.

## D. Apparent improvement that is contaminated: Hindi empathy

`EMP-HUM-002` rose from 60 to 84. The DPO answer is more actionable and gives concrete study strategies. But the core Hindi user statement from the held-out benchmark appears directly in a DPO V2 training prompt. This improvement is therefore useful as an illustration of learned behavior, but not as unbiased held-out evidence.

## E. Likely meaningful improvement: Malayalam scientific explanation

`SCI-EXP-004` rose from 68 to 92. The DPO response includes a clearer photosynthesis mechanism, chloroplast/chlorophyll context, the reaction components, glucose, and oxygen. This looks qualitatively stronger than the SFT response, although expert language review is still needed.

## F. Metric improvement that needs scientific expert review

`SCI-RES-001` rose from 80 to 93.33 because the DPO response includes more expected concepts such as diffusion. The first hypothesis is plausible. The second hypothesis (“bacterial mobility/environment requirement”) is more speculative and its proposed experiment is not obviously a strong discriminating test. This should not be called a scientific-quality improvement solely because the keyword rubric increased.

## G. Socratic tutoring remains unresolved

Socratic tutoring declined slightly in aggregate. Some DPO responses are arguably more conversational or exploratory, but several use multiple guiding questions, simulation scaffolds, or meta-framing that may not match the project's intended “single focused probe” behavior. Since all five Socratic cases are qualitative by design, this domain requires blinded human review rather than score chasing.

---

# 12. Critical evaluation-integrity finding: DPO V2 contaminated the 50-case baseline suite

This is the most important methodological finding from the current analysis.

The Phase 3 data specification states that the 110 evaluation cases — including the canonical 50-case baseline — are strictly held out and must **not** be used as source material, templates, or references for model development.

The DPO V2 dataset audit only documents a check against the **10-case DPO holdout**. It does not establish isolation from the canonical 50-case baseline suite.

Direct inspection shows baseline leakage / template overlap in DPO V2:

1. **Exact prompt reuse:** the teacher-assistance enzyme-catalysis rubric prompt in `paul_dpo_v2_tch_001` is the same prompt as baseline case `TCH-ASST-003`.
2. **Direct content reuse:** the Hindi math-stress sentence in `paul_dpo_v2_emp_004` appears inside baseline empathy case `EMP-HUM-002`.
3. **Template-level reuse:** `paul_dpo_v2_plan_001` asks for a “structured 3-day revision schedule,” closely mirroring baseline `STU-ASST-001`, changing the subject matter but retaining the benchmark task template.
4. **Concept/template overlap:** `paul_dpo_v2_sci_exp_002` asks “Why is the sky blue? Keep it simple,” while the baseline scientific-explanation suite contains a Rayleigh-scattering sky-color case.

This conflicts with the project's stated contamination-prevention standard.

### Consequence

The current SFT-vs-DPO V2 50-case comparison must be labeled:

> **Diagnostic / contaminated for DPO V2 — not a clean held-out superiority evaluation.**

It can still tell us where behavior changed and reveal regressions, but it must **not** be used to claim that DPO V2 is better than SFT.

This also means the current apparent gains in teacher assistance, empathy, planning, and some explanation tasks must be interpreted conservatively when they resemble corrective training examples.

---

# 13. Second evaluation-method issue: `--eval` is not currently authoritative

`scripts/evaluate.py` accepts an `--eval` configuration path, but the runner currently instantiates `get_baseline_benchmark_suite()` directly. The loaded evaluation config does not determine the suite used by the CLI.

Therefore, the successful run proves evaluation on the repository's 50-case baseline suite, but not that every setting or suite selection in `configs/evaluation/baseline_e4b.yaml` was honored.

This should be fixed before the next research comparison.

---

# 14. What we started with vs where we are now

| Stage | Model state | Main learning |
|---|---|---|
| **Start / base** | Generic Gemma 4 E4B | Strong general capabilities, but target behavioral gaps motivated specialization |
| **SFT foundation** | 180-example behavioral SFT adapter | Established PAUL-specific instructional/multilingual behavior and became the reference checkpoint |
| **DPO V1** | First preference-tuned continuation | Preference data encoded a concision shortcut; “shorter” became an unintended latent objective |
| **DPO V2** | 14-pair corrective DPO continuation | Training is technically sound; response calibration improved in some cases, but multilingual/Socratic regressions remain and the current benchmark comparison is contaminated |

The correct present status is therefore:

> **SFT remains the safer reference checkpoint. DPO V2 is a technically valid research checkpoint with mixed behavioral effects, not a demonstrated superior model.**

---

# 15. What has been established so far

## Established with strong evidence

- The PAUL Open training/reproducibility pipeline can execute a real two-GPU DPO run on Kaggle.
- The custom external-reference topology works and is mathematically equivalent at the validated boundary.
- DPO V2 changed all intended LoRA tensors and passed the final completion gates.
- Preference-pair construction strongly influences learned shortcuts.
- DPO V1 had a measurable brevity bias.
- DPO V2 can improve some desired response-calibration behaviors.
- DPO V2 can also regress core multilingual and factual behavior.
- The current 50-case heuristic score alone is insufficient to judge superiority.
- The DPO V2 corrective dataset is not cleanly isolated from the canonical 50-case baseline suite.

## Not established

- That DPO V2 is superior to SFT.
- That the +domain scores represent generalization rather than prompt/template exposure or sampling variance.
- That the current 50-case suite is statistically sufficient for release decisions.
- That the historical base → SFT → DPO V1 → DPO V2 improvement chain is monotonic.
- That multilingual quality is preserved across low-resource languages.
- That one stochastic response per prompt is stable enough for model ranking.

---

# 16. Step 3 plan — improve the science before doing more training

The next phase should begin with **evaluation repair and data isolation**, not immediately with another DPO run.

## Priority 1 — Restore a truly clean evaluation boundary

Create a single machine-readable registry of all permanent evaluation prompts across:

- canonical baseline 50
- capability-preservation 30
- held-out behavioral 30
- permanent DPO holdout 10

Before any training dataset is accepted, enforce:

1. exact normalized prompt match = fail
2. high n-gram/lexical overlap = fail/review
3. template/structural similarity = review
4. semantic similarity above a conservative threshold = review
5. numerical-parameter collision where relevant = review
6. explicit audit artifact committed with dataset hash

The contamination check must cover **all 110 held-out benchmark cases plus the 10 DPO holdout cases**, not only the 10 DPO IDs.

## Priority 2 — Fix the evaluation harness

- Make `scripts/evaluate.py --eval` actually load and honor the requested suite/configuration.
- Record the exact model revision, adapter hash, evaluation-config hash, suite hash, and source revision in every evaluation manifest.
- Capture actual GPU/device information correctly.
- Add deterministic evaluation (`temperature=0`) for regression testing.
- Keep stochastic evaluation separately and run multiple seeds/samples per prompt.

## Priority 3 — Separate automated metrics by purpose

Do not collapse everything into one headline number.

Track at least:

### Translation
- native-script correctness as a hard gate
- adequacy / semantic fidelity
- terminology preservation
- unwanted romanization/meta-talk
- human bilingual preference

### Science reasoning
- final-answer correctness
- reasoning validity
- factual/mechanistic errors
- unit/numerical correctness
- expert review on ambiguous cases

### Socratic tutoring
- does not dump the solution prematurely
- asks a focused diagnostic question
- identifies the misconception
- adapts to the learner's response
- human teacher preference

### Empathy
- acknowledges difficulty without overclaiming emotion
- actionable next step
- avoids manipulative/dependent framing
- preserves academic integrity
- human preference

### Teacher/student assistance
- completeness
- usability
- structure
- constraint adherence
- factual/curricular validity

## Priority 4 — Build a clean DPO V3 dataset only after evaluation is frozen

DPO V3 should be **concept-disjoint and template-disjoint** from all frozen benchmarks.

Dataset changes should include:

- substantially more multilingual representation
- explicit Punjabi/Gurmukhi, Telugu, Malayalam, Kannada, Gujarati, Marathi, Assamese/Odia coverage as appropriate
- preservation pairs for scientific correctness
- preservation pairs for native-script output
- Socratic pairs where “one focused next question” is the actual preference dimension
- examples where longer is better, shorter is better, and equal-length is better for reasons unrelated to length
- adversarial pairs designed to prevent shortcut learning

The current 14-pair DPO V2 set is too small and too English-heavy to serve as a robust multilingual corrective dataset.

## Priority 5 — Evaluate Base vs SFT vs DPO V1 vs DPO V2 vs future DPO V3 on the same clean protocol

When artifacts are available, compare all checkpoints under the same:

- exact base revision
- tokenizer
- inference precision
- generation parameters
- evaluation prompts
- random seeds
- hardware class where practical

This is necessary to distinguish real model progress from runtime/sampling differences.

## Priority 6 — Add blinded human pairwise review

For the capabilities central to PAUL Open, automated metrics should be a filter, not the final judge.

Use blinded A/B comparisons with reviewers unaware of which checkpoint produced the response. At minimum review:

- all Socratic cases
- all empathy cases
- all translation cases with bilingual reviewers
- all material science/factual disagreements
- a stratified sample of teacher and student assistance

Record win / tie / loss plus structured reasons.

---

# 17. Proposed release / superiority gate

A future checkpoint should be called “better” only if it passes **all** of the following:

1. **Technical validity:** provenance and training gates pass.
2. **Zero evaluation leakage:** no benchmark/source/template contamination.
3. **Safety non-regression:** no deterioration in hard safety/anti-anthropomorphism constraints.
4. **Native-script hard gate:** no severe translation-script failures such as the Punjabi DPO V2 case.
5. **Factuality preservation:** no new critical scientific errors relative to SFT.
6. **Target-domain improvement:** meaningful improvement in the behaviors we explicitly trained for.
7. **Capability preservation:** no material regression in strong SFT domains.
8. **Human preference:** blinded reviewers prefer the new model on the target behaviors with a meaningful margin.
9. **Robustness:** result persists across prompt paraphrases and multiple decoding seeds.
10. **Aggregate score:** treated as supporting evidence only after the above conditions are satisfied.

---

# 18. Immediate research decision

Do **not** discard DPO V2. It is valuable evidence:

- it proves the production DPO implementation works;
- it demonstrates that contextual calibration can be moved;
- it exposes multilingual preservation problems;
- it exposes factual regression risk;
- it exposes a benchmark-leakage flaw in the data-audit process.

But do **not** promote DPO V2 as the new preferred PAUL Open checkpoint based on the present benchmark. Keep the SFT adapter as the reference while the evaluation boundary is repaired and a clean next experiment is designed.

---

# 19. Evidence still to recover and attach

To complete the historical record, recover if available:

- original base-model baseline `results.json` / `manifest.json`
- original SFT training manifest and adapter hashes
- DPO V1 training manifest/checkpoint hashes
- DPO V1 full evaluation output
- any human-review notes that motivated the DPO V2 corrective examples

These should be appended as evidence; missing values should remain explicitly marked as missing rather than inferred.

---

## Canonical repository references

- `README.md`
- `docs/BASELINE_EVALUATION.md`
- `docs/TRAINING_DATA_SPECIFICATION.md`
- `docs/PILOT_REVIEW_MATRIX.md`
- `docs/E4B_DPO_V2_CORRECTIVE.md`
- `results/dpo/dpo_v2_dataset_audit.md`
- `data/train/dpo_v2_corrective.jsonl`
- `configs/training/sft_qlora.yaml`
- `configs/training/dpo_v2_e4b_corrective.yaml`
- `scripts/dpo_v2_e4b_train.py`
- `scripts/evaluate.py`
- final GitHub Actions production artifact from run `34324528349`
