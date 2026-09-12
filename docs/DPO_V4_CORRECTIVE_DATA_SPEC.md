# PAUL Open — DPO V4 Corrective Data Specification

**Stage:** P9 COMPLETE / DATASET AUTHORING PENDING  
**Date:** 2026-09-12  
**Upstream evidence:** `docs/H5_P8_FAILURE_ANALYSIS.md`  
**Reference checkpoint:** SFT  
**Prior experimental checkpoints:** DPO V2 Corrective and DPO V3 Corrective (immutable)

## Objective

Design a small development-only preference dataset that corrects the H5 preservation failures without erasing the behavior gains observed in Bengali, General and Research. This specification is a development instrument, not evaluation evidence.

## Proposed dataset identity

After authoring: `data/train/dpo_v4_corrective.jsonl`.

Use the existing preference schema (`prompt`, `chosen`, `rejected` plus identifying/provenance metadata). Never overwrite DPO V1/V2/V3 data.

## Initial size and allocation

Author **30 preference pairs**:

| Track | Pairs | Role |
|---|---:|---|
| Conservation-law consistency and energy accounting | 6 | corrective |
| Diagnostically useful Socratic questioning | 6 | corrective |
| Direct-explanation mode + multilingual completion | 6 | corrective |
| Bengali scientific-fidelity preservation | 4 | preservation |
| Evidence-first general-assistance preservation | 4 | preservation |
| Research-methodology preservation | 4 | preservation |
| **Total** | **30** | |

Expansion requires a separate audit finding; training volume alone is not a reason to add examples.

## Track A — conservation-law consistency (6)

Use fresh STEM scenarios structurally distinct from H4/H5. Favor problems where more than one physical quantity matters, for example momentum versus kinetic energy, angular momentum versus rotational energy, electrical energy versus charge conservation, or thermodynamic state variables versus heat/work.

Chosen responses must:
- identify the relevant conserved quantity and the conditions for its conservation;
- distinguish it from quantities that may change;
- account explicitly for work/energy transfer when required;
- avoid invoking a spurious external force/torque to explain a constraint-driven change;
- satisfy all explicit caveats in the prompt.

Rejected responses should be plausible but contain one specific conservation-law, work/energy, or causal-mechanism defect.

## Track B — diagnostic Socratic questioning (6)

Use new misconceptions unrelated to salt dissolution or lunar phases.

Chosen responses must:
- start with one focused observation, prediction, comparison, measurement or diagram-based question when requested;
- make the question discriminate between the misconception and an alternative mechanism;
- remain scientifically coherent;
- avoid merely rephrasing the learner's belief;
- avoid embedding the entire answer in the opening question.

Rejected responses should look tutor-like on the surface but fail diagnostically through a confused comparison, question-shaped lecture, irrelevant question, or non-discriminating paraphrase.

## Track C — direct explanation and multilingual completion (6)

Use fresh direct-explanation prompts, with at least four non-English examples and at least two in Hindi. Do not reuse tire pressure, batteries, pressure cookers, prisms, or other H4/H5 prompts.

Chosen responses must:
- recognize that the user requested an explanation rather than a Socratic lesson;
- answer every requested component before optional elaboration;
- remain complete within the expected output length;
- use natural target-language prose and calibrated scientific wording;
- use questions only when they support rather than replace the requested answer.

Rejected responses should be fluent but drift into excessive questioning, terminate before required components, or substitute an analogy for the actual mechanism.

## Track D — Bengali scientific-fidelity preservation (4)

Use fresh Bengali scientific explanations with directional or comparative facts that can be checked explicitly. Preserve natural Bengali and correct scientific invariants. Rejected responses should be fluent enough that the preference depends on factual fidelity rather than obvious language corruption.

## Track E — evidence-first general assistance preservation (4)

Use fresh time-pressured work or life scenarios. Chosen responses should establish what is known, what can be verified now, and what remains uncertain before giving communication or presentation advice. Avoid invented specifics and impression-management-first framing.

## Track F — research-methodology preservation (4)

Use fresh experimental/statistical reasoning tasks. Chosen responses should distinguish the actual estimand/hypothesis from tempting but weaker analyses, preserve randomization/provenance reasoning, and use interaction/effect-modification logic when appropriate. Avoid p-value folklore and ad-hoc robustness rituals.

## Hard exclusions

The dataset must not:
- reuse or lightly paraphrase H4 or H5 prompts;
- copy H4/H5 model responses;
- quote or paraphrase evaluator comments;
- include SHAE prompts or material derived from sealed assurance assets;
- silently reuse DPO V1/V2/V3 pairs;
- claim `human_verified: true` before actual verification;
- claim `benchmark_leakage_checked: true` before P10 passes.

## Required metadata

Each record must include:
- unique `id` with `paul_dpo_v4_` prefix;
- `track`;
- `domain`;
- `language`;
- `rejection_reason`;
- `prompt`;
- `chosen`;
- `rejected`;
- metadata including `difficulty`, `source: "post_h5_p9_authored"`, `human_verified: false`, `benchmark_leakage_checked: false`, and a concise `corrective_category`.

## P10 acceptance gates

Before training, all records must pass:

1. valid JSONL/schema and unique IDs;
2. no internal exact duplicates;
3. no exact or near-duplicate prompts against H4, H5, DPO V1/V2/V3, or accessible sealed-assurance fingerprints/material;
4. canonical benchmark leakage check;
5. no copied H4/H5 response spans beyond unavoidable generic language;
6. preference direction independently verified;
7. multilingual language-quality review;
8. scientific/research factual review for relevant tracks;
9. provenance metadata complete;
10. final dataset SHA-256 recorded.

Any failed gate blocks training.

## Training boundary

P9 does **not** authorize DPO V4 training. Training may begin only after a concrete dataset exists and P10 is recorded as PASS. The validated DPO training machinery should be reused unless a methodology change is separately proposed, justified and reviewed.

SHAE remains sealed.
