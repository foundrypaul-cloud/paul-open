# PAUL Open — DPO V3 Corrective Data Specification

**Stage:** P2 COMPLETE / DATASET AUTHORING PENDING  
**Date:** 2026-09-12  
**Upstream evidence:** `docs/H4_P1_FAILURE_ANALYSIS.md`  
**Reference checkpoint:** SFT  
**Prior experimental checkpoint:** DPO V2 Corrective (immutable)

## Objective

Design a small development-only preference dataset that targets behavior classes identified in H4 P1 without copying H4 prompts, responses, or evaluator comments. The dataset is a candidate-development instrument, not evaluation evidence.

## Dataset identity

Proposed path after authoring: `data/train/dpo_v3_corrective.jsonl`.

Use the existing DPO preference schema (`prompt`, `chosen`, `rejected` plus identifying and provenance metadata). Never overwrite `dpo_train.jsonl` or `dpo_v2_corrective.jsonl`.

## Size and allocation

Author **30 preference pairs** initially:

| Track | Pairs | Role |
|---|---:|---|
| Bengali causal-direction science | 8 | corrective |
| Grounded Socratic tutoring | 6 | corrective |
| Evidence-before-hypothesis assistance | 6 | corrective |
| STEM causal-clarity preservation | 5 | preservation |
| Hindi calibrated science preservation | 5 | preservation |
| **Total** | **30** | |

This is intentionally small. Expansion requires a separate audit finding; do not scale merely to increase training volume.

## Track A — Bengali causal-direction science (8)

Create Bengali explanations in which the key challenge is preserving the direction of a causal scientific relationship. Use topics structurally distinct from the H4 pressure-cooker prompt, for example vapor pressure/humidity, altitude and boiling, gas compression, thermal expansion, diffusion, circuits, concentration gradients, or heat transfer.

Chosen responses must:
- be fluent, natural Bengali suitable for the requested audience;
- state the relevant causal direction explicitly;
- avoid internally contradictory mechanism statements;
- distinguish approximations from universal rules;
- explain enough mechanism to make the conclusion understandable.

Rejected responses should be plausible and fluent but contain one identifiable directional, causal, or calibration defect. Avoid cartoonishly false negatives.

## Track B — Grounded Socratic tutoring (6)

Use new misconceptions unrelated to salt dissolution. The chosen response should begin with one focused question that lets the learner inspect, measure, compare, predict, or test something relevant before explanation.

Chosen responses must:
- honor requests for a question-first Socratic style;
- prefer an observable/testable question over merely restating the misconception;
- avoid giving away the answer in the first question;
- scaffold further only when the prompt requests or permits it.

Rejected responses should remain superficially helpful but exhibit a specific defect such as paraphrasing the misconception, immediately lecturing, asking several unfocused questions, or embedding the answer in the question.

## Track C — Evidence before hypothesis (6)

Use new human-centered research/work situations unrelated to the failed-experiment presentation prompt. Examples may involve inconsistent observations, a debugging update, an unexpected survey result, a failed prototype, or a confusing measurement series.

Chosen responses must:
- acknowledge emotional or practical urgency briefly when present;
- separate known observations from unknown causes;
- avoid inventing measurements, variables, outcomes, or motives;
- give concrete immediate organization/troubleshooting steps;
- label hypotheses as hypotheses;
- provide communication language only after grounding it in known evidence.

Rejected responses should be plausible but prematurely invent a cause, fabricate specifics, overpromise, or optimize appearance to a supervisor/client before establishing evidence.

## Track D — STEM causal-clarity preservation (5)

Use fresh English STEM prompts requiring a compact causal chain. Chosen responses should preserve the useful DPO V2 behavior seen in H4-DHE-001: name the changing variable, connect it to the mechanism, and state the resulting observable effect without unnecessary jargon.

Rejected responses should remain factually adjacent but use a confused variable relationship, omit the mechanism, or substitute vague language for the causal chain.

## Track E — Hindi calibrated science preservation (5)

Use fresh Hindi science/technology explanations unrelated to phone battery charging. Chosen responses must be simple and natural while preserving scientific calibration: heuristics are not cliffs, risk factors are not certainties, and analogies must not introduce false mechanisms.

Rejected responses may be fluent but should contain a specific overstatement, misleading analogy, false threshold, or invented mechanism.

## Hard exclusions

The authored dataset must not:
- reuse or lightly paraphrase any H4 prompt;
- quote or paraphrase evaluator comments;
- include SHAE prompts or material derived from sealed assurance assets;
- use H4 responses as chosen/rejected completions;
- claim `human_verified: true` before actual human verification;
- set `benchmark_leakage_checked: true` before P3 passes;
- silently reuse an existing pair from DPO V1/V2.

## Required metadata

Each record should include at minimum:
- unique `id` with `paul_dpo_v3_` prefix;
- `track`;
- `domain`;
- `language`;
- `rejection_reason`;
- `prompt`;
- `chosen`;
- `rejected`;
- metadata containing `difficulty`, `source: "post_h4_p2_authored"`, `human_verified: false`, `benchmark_leakage_checked: false`, and a concise `corrective_category`.

## P3 acceptance gates

Before training, all 30 records must pass:

1. valid JSONL/schema and unique IDs;
2. no exact duplicate prompts or completions internally;
3. no exact or near-duplicate prompts against H4, SHAE-accessible hashes/material, DPO V1, or DPO V2;
4. no copied H4 response spans beyond unavoidable generic phrases;
5. chosen/rejected preference direction manually or independently verified;
6. Bengali and Hindi language-quality review;
7. scientific factual review for science tracks;
8. provenance metadata complete;
9. SHA-256 recorded for the final dataset;
10. dataset remains development-only and H4/SHAE remain evaluation-only.

If any gate fails, training is blocked until the dataset is corrected and re-audited.

## Training boundary

P2 does **not** authorize training by itself. Candidate training begins only after a concrete 30-pair dataset exists and P3 is recorded as PASS. The existing DPO V2 training machinery should be reused with a new experiment/candidate identifier rather than introducing a new training methodology.
