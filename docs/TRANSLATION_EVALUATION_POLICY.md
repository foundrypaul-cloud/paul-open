# PAUL Open — English → Indic Scientific Translation Evaluation Policy

**Status:** research policy for the next evaluation revision  
**Scope:** English → Indic scientific, educational, technical, and classroom translation

## 1. Core principle

PAUL Open should evaluate whether a translation is **useful, faithful, natural, and technically correct**, not whether every visible token has been converted into an Indic script.

A lower legacy script/keyword score can occasionally correspond to a **better translation** when the model correctly preserves technical material that should remain in its conventional form.

Therefore:

> **Native-script fidelity applies primarily to the surrounding natural-language prose. It must not become a blanket requirement to translate, transliterate, or script-convert every technical token.**

This is especially important in science and technical education, where forced localization can make an otherwise correct answer less precise, less familiar to students, or actively misleading.

## 2. Technical spans that may legitimately remain in Latin/standard notation

The evaluator should identify and protect, where appropriate:

- mathematical formulas and symbols (`F=ma`, `E=mc^2`, `ΔT`, `λ`)
- chemical formulae and equations (`H2O`, `CO2`, `NaCl`, `2H2 + O2 → 2H2O`)
- SI units and standard unit symbols (`kg`, `m/s`, `Pa`, `J`, `mol`, `K`)
- scientific notation (`1.0 × 10^-6 m^2`)
- established scientific acronyms (`DNA`, `RNA`, `ATP`, `PCR`, `pH`)
- gene, protein, receptor, and pathway symbols where conventional spelling matters
- software, programming, API, framework, database, and protocol names
- internationally standardized instrument or model names
- technical terms that are conventionally taught or used in English in the target-language educational context

These spans should not automatically lower a native-script score.

## 3. Context-sensitive terminology policy

This policy does **not** mean “never translate technical terms.”

For many concepts, a natural and widely understood Indic term exists and should be used. In other cases, the English term is the standard classroom or professional form. A third common pattern is bilingual terminology on first use, for example:

`गतिज ऊर्जा (Kinetic Energy)`

The preferred form should be determined by:

1. semantic accuracy,
2. target-language educational convention,
3. likely learner comprehension,
4. consistency within the response,
5. avoidance of artificial or archaic terminology.

A model should not receive extra credit merely for replacing an established technical term with a less familiar Indic coinage.

## 4. What remains a genuine script failure

Preserving a technical span is different from romanizing the target-language sentence itself.

For example, an English → Punjabi answer in which ordinary Punjabi prose is emitted primarily as Latin-script romanization is still a failure when Gurmukhi was requested or expected. This remains true even though technical acronyms, formulas, or conventional English scientific terms inside the same response may legitimately stay in Latin script.

The DPO V2 `TRANS-005` observation should therefore be interpreted as a genuine regression because the natural-language Punjabi was romanized, not because a small number of protected technical tokens remained in Latin script.

## 5. Revised translation evaluation dimensions

Future evaluation should report separate dimensions instead of compressing translation quality into one script-heavy score:

### A. Semantic adequacy
Does the target text preserve the source meaning, causal relations, quantities, and constraints?

### B. Natural-language script fidelity
After excluding protected technical spans, is the ordinary target-language prose written in the expected native script?

### C. Technical-term preservation
Are formulas, symbols, acronyms, units, names, and established technical terms preserved or localized appropriately?

### D. Terminology quality
Are translated/localized technical terms standard, comprehensible, and appropriate for the educational context?

### E. Fluency and classroom naturalness
Does the answer sound like natural modern educational language rather than literal, archaic, or machine-translated prose?

### F. Translation cleanliness
Does the output avoid unwanted meta-talk, explanatory wrappers, duplicate transliteration, and unsolicited commentary?

### G. Human bilingual preference
For release decisions, bilingual reviewers should compare outputs for correctness, naturalness, technical precision, and usefulness.

## 6. Recommended script-scoring implementation

The next evaluator should use a protected-span-aware process:

1. identify technical spans before script analysis;
2. exclude those spans from the native-script denominator;
3. measure script coverage only over remaining natural-language tokens/characters;
4. separately detect widespread romanization of target-language prose;
5. separately score technical-term preservation;
6. flag ambiguous terminology decisions for bilingual human review.

A single Unicode-block percentage is insufficient for scientific translation quality.

## 7. Interpretation of historical scores

Existing PAUL Open translation scores remain useful as diagnostic evidence, but they should be interpreted cautiously:

- a low score caused by broad romanization of normal Indic prose is a meaningful regression;
- a low score caused mainly by correctly preserved formulas, acronyms, units, or technical terms may be a false negative;
- a high score obtained by force-translating technical vocabulary into unnatural or inaccurate terminology is not evidence of superior translation.

Historical comparisons should therefore preserve the raw outputs and be re-scored under the revised translation policy where practical.

## 8. Release principle

PAUL Open should prefer a translation that is **technically faithful and educationally natural** over one that merely maximizes target-script coverage.

The release gate should reject severe natural-language romanization, semantic distortion, and terminology errors, while explicitly allowing correct conventional technical material to remain in its standard form.
