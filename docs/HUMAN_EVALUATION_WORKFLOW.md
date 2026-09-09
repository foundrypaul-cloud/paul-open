# PAUL Open — Human Evaluation Workflow v1

**Status:** engineered research protocol; implementation follows after review  
**Applies after:** Step 2 research freeze (`ac899e879f930f25b2081550bd8c5dd5c983df35`)

## 1. Objective

PAUL Open uses human evaluation to answer a narrow question that automated metrics cannot answer reliably:

> **For the intended user and task, which valid response is actually better?**

The reviewer-facing experience must remain simple. Reviewers do not need to know about SFT, DPO, adapters, checkpoints, benchmark names, inference infrastructure, or training methodology.

A reviewer should only need to:

1. open a link;
2. read a prompt;
3. read Response A and Response B;
4. choose the response they prefer, or indicate a tie / neither / uncertainty;
5. submit.

The target completion time for a normal form is **2–4 minutes**.

---

## 2. Research principles

### 2.1 Human preference is one evidence layer, not the only metric

Human preference is combined with technical validity, factual/safety gates, capability-preservation checks, and clean held-out evaluation. A model is not promoted merely because it wins a popularity vote.

### 2.2 Reviewer blinding

Reviewers must not be told:

- model/checkpoint identity;
- SFT/DPO/base labels;
- automated scores;
- which response is the newer model;
- which response the research team expects to win.

Response A/B assignment must be counterbalanced.

### 2.3 Development evaluation and final assurance evaluation are different assets

PAUL Open uses two human-evaluation partitions.

#### A. Development Human Evaluation (DHE)

Purpose: diagnose weaknesses and decide what future training should target.

DHE cases **may influence future model development**. Once a DHE case is used to design training examples, tune prompts, select hyperparameters, or otherwise influence the next model, that case is permanently marked **development-exposed** and cannot later serve as clean final superiority evidence.

#### B. Sealed Human Assurance Evaluation (SHAE)

Purpose: make a final promotion/release decision on a candidate that has already been frozen.

SHAE prompts must remain outside the public repository and outside normal training/development data access. The candidate model artifact, adapter hash, source revision, and evaluation configuration must be frozen **before** SHAE prompts are used.

If SHAE results are used to change the model, the candidate is no longer the same candidate and that SHAE batch is considered **burned/retired**. A new sealed batch is required for the next assurance decision.

This separation is essential to prevent human evaluation from becoming another source of benchmark contamination.

### 2.4 Current Step 2 baseline suite status

The existing 50-case SFT-vs-DPO V2 comparison remains useful for diagnosis, but because DPO V2 corrective data overlaps with parts of that suite, it must not be relabeled as a clean SHAE set.

---

## 3. Reviewer cohorts

Do not ask one general reviewer to judge every capability. Route each form to people who can reasonably judge that content.

| Cohort | Appropriate tasks |
|---|---|
| General learner / user | clarity, helpfulness, basic explanations, student assistance, tone |
| Teacher / educator | Socratic tutoring, lesson/rubric quality, classroom usefulness |
| Bilingual reviewer | English→Indic translation, Indic naturalness, terminology, script appropriateness |
| STEM-capable reviewer | physics/chemistry/biology/math factuality and mechanism |
| Research/domain expert | scientific research assistance, advanced life-science or technical reasoning |

For v1, use separate short forms or separate links per cohort/language instead of adding a long demographic routing questionnaire.

---

## 4. Reviewer-facing form design

### 4.1 Intro text

Keep the introduction short and non-technical. Suggested text:

> **Help us compare two AI responses.**  
> For each question, read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so. There are no right or wrong preferences.

For bilingual translation forms, add one sentence:

> Standard scientific terms, formulas, units and abbreviations may stay in their familiar English or standard notation when that is clearer or more accurate.

### 4.2 Number of comparisons

Default: **3 research comparisons per form**.

- For short responses, a form may contain 4 comparisons if the estimated completion time stays below 4 minutes.
- For long teacher/research responses, reduce to 2 comparisons.
- Avoid large all-domain forms. Cognitive switching and scrolling reduce completion quality.

### 4.3 Required answer choices

Each research comparison uses one required multiple-choice answer:

- **Response A is better**
- **Response B is better**
- **They are about equally good**
- **Neither response is good**
- **I’m not sure / I can’t judge this**

Do not ask reviewers to assign many 1–10 scores for every answer. Pairwise preference is the primary signal; detailed rubrics are reserved for expert adjudication.

### 4.4 Optional comment

One optional final free-text question only:

> **Anything important you noticed? (optional)**

Do not require written justification for every pair in the normal user form.

### 4.5 Google Forms presentation settings

Recommended defaults:

- progress bar: **on**;
- collect email: **off** by default;
- show response summary: **off**;
- allow response editing: **off**;
- “submit another response” link: **off**;
- confirmation message: brief thank-you;
- no model names in title, description, URL text, section titles, or choices.

A sign-in/one-response requirement should be enabled only when duplicate-response risk is more important than participation friction. The default v1 research mode is a curated/invited reviewer link rather than an unrestricted public poll.

---

## 5. Blinding and randomization

### 5.1 A/B counterbalancing

For each comparison, generate at least two display variants:

- Variant X: A = reference, B = candidate
- Variant Y: A = candidate, B = reference

Across reviewers, assignment should be approximately balanced.

### 5.2 Case-order randomization

Google Forms can shuffle individual questions, but PAUL comparisons contain a prompt plus two response blocks that must remain together. Therefore the production system should **generate multiple form variants programmatically** with seeded case ordering instead of relying on global question shuffling.

The randomization seed and A/B mapping belong in a private batch manifest, not in the reviewer-facing form.

### 5.3 No answer-option shuffling

Do not shuffle the answer options “Response A is better” and “Response B is better”; stable option order reduces reviewer mistakes. Position bias is handled by swapping the displayed response content across variants.

---

## 6. Quality controls without burdening users

Quality-control items should be sparse, not one per short form.

Recommended v1 control injection rate: **~20% of forms** receive one non-research control comparison whose expected preference is clear to an appropriately qualified reviewer.

Controls are never included in model win-rate calculations. They are used only to detect careless/random participation.

Other low-cost quality signals:

- implausibly fast completion;
- repeated identical response pattern across many forms;
- failure on a control item;
- excessive “not sure” responses for a cohort that claimed the required expertise.

No single behavioral signal should automatically invalidate a reviewer without inspection.

---

## 7. Adaptive review allocation

Do not collect a large fixed number of votes on every case.

1. Collect **3 independent valid judgments** per case.
2. If there is strong agreement, close the case.
3. If judgments conflict, include “not sure”, or the case is critical, collect **2 additional judgments** (5 total).
4. Only exceptional unresolved cases escalate to **7** and/or expert adjudication.

This concentrates human effort on ambiguous cases instead of wasting reviewer time on obvious ones.

---

## 8. Translation-specific human evaluation

English→Indic translation must be judged on technical usefulness, not raw script percentage.

Bilingual reviewers should consider:

- semantic fidelity;
- natural modern target-language prose;
- correct native script for ordinary prose;
- appropriate preservation of formulas, SI units, acronyms, names and established technical terms;
- terminology familiar to the intended educational context;
- absence of unnecessary meta-talk or duplicate transliteration.

A few conventional Latin/English technical spans are **not** a failure. Broad romanization of the target-language prose remains a failure when native script is expected.

See `docs/TRANSLATION_EVALUATION_POLICY.md`.

---

## 9. Google Forms / Sheets automation architecture

The workflow should be automated with Google Forms + Google Sheets + Apps Script (or the Google Forms API), while the reviewer only sees the form link.

```text
frozen model outputs
        ↓
automated validity / safety / contamination gates
        ↓
human-eval batch builder
        ↓
private blind-map + seeded variants
        ↓
Google Forms generator
        ↓
short responder links
        ↓
Google Sheets response destination
        ↓
form-submit normalization
        ↓
review-count / disagreement monitor
        ↓
auto-close batch at target
        ↓
locked analysis snapshot
        ↓
unblind model identities
        ↓
research decision
```

Google Apps Script supports programmatic form creation/modification, multiple-choice questions, page breaks, progress settings, response destinations, response-collection state, and form-submit triggers. Google Forms responses can be linked to Google Sheets for analysis.

### Why programmatic form generation

Programmatic generation gives us:

- deterministic A/B swapping;
- deterministic case-order variants;
- repeatable titles/descriptions/settings;
- automatic mapping to a batch manifest;
- automatic closing when enough valid responses arrive;
- far less manual copying/pasting, reducing accidental unblinding and transcription errors.

---

## 10. Data model

### 10.1 Public/repository batch metadata

The public repository may contain:

- protocol version;
- batch ID after completion;
- model artifact hashes after unblinding/publication decision;
- counts by domain/language;
- aggregate results;
- hashes of sealed case manifests if appropriate.

### 10.2 Private batch manifest

The private manifest contains:

- `batch_id`
- `protocol_version`
- `evaluation_partition` (`development` or `sealed_assurance`)
- `candidate_artifact_hash`
- `reference_artifact_hash`
- `case_id`
- `domain`
- `language`
- `cohort`
- `form_variant`
- A/B source mapping
- randomization seed
- control-item flag
- case lifecycle state

For sealed assurance, **prompt text and candidate/reference outputs must not be committed to the public repository before the evaluation is retired/published according to the research plan.**

### 10.3 Normalized judgment record

The analysis table should contain only what is necessary:

- `batch_id`
- `comparison_id`
- `cohort`
- `domain`
- `language`
- `variant_id`
- `displayed_choice`
- mapped preference after unblinding
- timestamp
- control status
- optional comment

Avoid collecting unnecessary personally identifiable information.

---

## 11. Human-evaluation state machine

```text
CANDIDATE_FROZEN
      ↓
AUTO_EVAL_PASSED
      ↓
HUMAN_BATCH_BUILT
      ↓
FORMS_GENERATED
      ↓
COLLECTING
      ↓
TARGET_REACHED
      ↓
FORMS_CLOSED
      ↓
ANALYSIS_LOCKED
      ↓
UNBLINDED
      ↓
DECISION_RECORDED
      ↓
RETIRED
```

No stage should silently skip forward.

For sealed assurance, `CANDIDATE_FROZEN` is mandatory before prompt material is released to forms.

---

## 12. Analysis rules

Report the human data transparently rather than compressing everything into one number.

At minimum report:

- candidate preferred;
- reference preferred;
- about equal;
- neither acceptable;
- unable to judge;
- results by domain;
- results by language;
- reviewer cohort;
- inter-rater agreement;
- confidence intervals for preference rates.

For a simple two-model comparison, raw paired preference rates plus bootstrap confidence intervals are sufficient as the primary summary. If future studies compare many models, a Bradley–Terry-style preference model may be added.

“Neither response is good” is a failure signal and must not be silently folded into a tie.

Disagreement is information. It can indicate ambiguous prompts, plural legitimate preferences, insufficient reviewer expertise, or a model trade-off that aggregate metrics hide.

---

## 13. Contamination safeguards

These are hard research rules.

1. **No sealed assurance prompts in public GitHub before use.**
2. **No sealed prompts in training datasets, prompt-development notebooks, synthetic-data generation context, or DPO pair construction.**
3. Candidate artifact/hash is frozen before sealed forms are generated.
4. DHE cases that influence model development are marked development-exposed and cannot later become SHAE cases.
5. SHAE cases that influence a subsequent model are immediately retired/burned.
6. Human comments are not copied directly into training data. Any lesson extracted from comments must go through a new development-data process, and the associated assurance cases are retired.
7. Reviewer-facing forms never reveal benchmark IDs or model identities.
8. A final result should always state whether the human evidence came from DHE or SHAE.

---

## 14. Resource-efficiency rules

- No human form is generated for outputs that fail automated hard gates.
- No reviewer is asked to judge more cases than necessary.
- No new model training is triggered by a form-system or analysis-system failure.
- Human evaluation operates on immutable saved model outputs/artifacts.
- Ambiguous cases receive more reviewers; clear cases stop early.
- Long responses get shorter forms.
- Domain/language specialists receive only tasks they can reasonably judge.

---

## 15. Implementation sequence

### Milestone H0 — protocol freeze

- merge this workflow specification;
- freeze the machine-readable v1 config;
- do not create production forms yet.

### Milestone H1 — local batch builder

Build/test code that takes two frozen model-output files and creates:

- eligibility report;
- blinded comparison bundle;
- private A/B map;
- deterministic variant manifests.

Use synthetic test cases only.

### Milestone H2 — Google Forms generator

Implement Apps Script / Forms API generation for a **sandbox form**:

- 3 comparisons;
- correct settings;
- variant generation;
- linked response Sheet;
- form-submit normalization;
- automatic closing test.

No real research prompts yet.

### Milestone H3 — dry-run human pilot

Use 5–10 disposable non-research comparisons with a small internal/trusted reviewer group to measure:

- median completion time;
- mobile readability;
- confusion rate;
- duplicate-response handling;
- Sheets normalization correctness;
- A/B mapping integrity.

Target: median completion ≤ 4 minutes and no systematic UX confusion.

### Milestone H4 — DHE pilot

Only after H3 passes, run a small development human-evaluation batch on fresh non-assurance cases.

### Milestone H5 — SHAE capability

Create the private/sealed case storage and one-way batch-release process. SHAE is used only after a future candidate has been fully frozen.

---

## 16. External methodology references

The protocol draws on several established ideas rather than treating Google Forms as merely a survey tool:

- Google AI’s Responsible Generative AI guidance distinguishes **development evaluations** used during model iteration from **assurance evaluations** used at key milestones.
- Google DeepMind’s work on double-blind evaluation emphasizes protecting test material from model-development contamination.
- Google DeepMind research on pairwise human preferences highlights that different annotators can legitimately have heterogeneous preferences, so disagreement and multiple raters should be modeled rather than erased.
- Google Forms/Apps Script officially support programmatic form creation/modification, response destinations, progress controls, and form-submit automation.

The implementation should retain these principles even if the user-facing interface remains only a few clicks long.
