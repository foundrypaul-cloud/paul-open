# PAUL Open Model — Phase 3 Pilot Review Matrix (20 SFT + 10 DPO)

This document provides a case-by-case human review matrix for the Phase 3 training-data pilot (30 records total), verifying pedagogical alignment, schema compliance, token limits, and contamination isolation against all 110 held-out evaluation cases.

---

## 1. SFT Pilot Review Matrix (20 Examples)

### Track 1: Socratic Tutoring & Misconception Scaffolding (6 Examples)

#### 1. `paul_sft_pilot_soc_001`
- **Track**: `socratic_tutoring` | **Domain**: `physics` (`fluid_mechanics`) | **Language**: `en`
- **Target Concept**: Pascal's Hydrostatic Paradox (pressure at depth $P = \rho gh$ is independent of container shape/total volume).
- **Intended Behavior**: Validates student's weight intuition, introduces vertical unit column thought experiment, asks **one guiding question**.
- **Why it Teaches Behavior**: Avoids lecturing on $P=\rho gh$; scaffolds attention to force-per-unit-area on a 1 cm² base column.
- **Potential Weakness / Review Note**: Requires student to connect unit column weight to depth.
- **Automated Validation**: Tier 1 Valid (Turn 1: 34 tokens, Turn 2: 74 tokens).
- **Contamination Audit**: Clean (0.20 max similarity vs `SCI-REAS-001`).
- **Review Recommendation**: **APPROVE**.

#### 2. `paul_sft_pilot_soc_002`
- **Track**: `socratic_tutoring` | **Domain**: `chemistry` (`thermodynamics`) | **Language**: `hi`
- **Target Concept**: Evaporation vs Boiling (liquid vaporizes at the surface below $100^\circ\text{C}$).
- **Intended Behavior**: Validates $100^\circ\text{C}$ boiling point intuition, presents drying clothes / spilled water thought experiment, asks **one guiding question** in Hindi.
- **Why it Teaches Behavior**: Uses observable everyday phenomenon to prompt student realization that vaporization occurs at room temperature.
- **Potential Weakness / Review Note**: Simple thought experiment; highly effective for foundational secondary students.
- **Automated Validation**: Tier 1 Valid (Turn 1: 43 tokens, Turn 2: 74 tokens).
- **Contamination Audit**: Clean (0.19 max similarity vs `EMP-HUM-002`).
- **Review Recommendation**: **APPROVE**.

#### 3. `paul_sft_pilot_soc_003`
- **Track**: `socratic_tutoring` | **Domain**: `mathematics` (`arithmetic_fractions`) | **Language**: `en`
- **Target Concept**: Fraction Addition Misconception ($1/2 + 1/3 = 2/5$).
- **Intended Behavior**: Acknowledges component-wise addition intuition, uses concrete pizza slice mental model, asks **one guiding question**.
- **Why it Teaches Behavior**: Shows that $1/2 + 1/3$ must be greater than $1/2$, while $2/5$ is less than $1/2$, without prematurely giving the common denominator algorithm.
- **Potential Weakness / Review Note**: Directs learner to relative magnitude before algebraic technique.
- **Automated Validation**: Tier 1 Valid (Turn 1: 40 tokens, Turn 2: 76 tokens).
- **Contamination Audit**: Clean (0.19 max similarity vs `SCI-EXP-001`).
- **Review Recommendation**: **APPROVE**.

#### 4. `paul_sft_pilot_soc_004`
- **Track**: `socratic_tutoring` | **Domain**: `biology` (`human_circulation`) | **Language**: `bn`
- **Target Concept**: Pulmonary Vessel Role Exception (artery/vein definition based on direction relative to heart, not oxygenation).
- **Intended Behavior**: Validates systemic circulation observation, prompts thought experiment on blood entering the lungs via the pulmonary artery.
- **Why it Teaches Behavior**: Guides student to reconcile the anatomical definition (carrying blood away from heart) with gas exchange exceptions in Bengali.
- **Potential Weakness / Review Note**: Focuses on pulmonary circuit exception.
- **Automated Validation**: Tier 1 Valid (Turn 1: 46 tokens, Turn 2: 72 tokens).
- **Contamination Audit**: Clean (0.09 max similarity vs `EMP-HUM-004`).
- **Review Recommendation**: **APPROVE**.

#### 5. `paul_sft_pilot_soc_005` *(Multi-Turn: 2 User Turns, 2 Assistant Turns)*
- **Track**: `socratic_tutoring` | **Domain**: `astronomy` (`celestial_mechanics`) | **Language**: `en`
- **Target Concept**: Moon Phases vs Lunar Eclipses (changing angle of illuminated hemisphere vs Earth's shadow).
- **Intended Behavior**: Turn 1 clarifies eclipse vs monthly phase + asks lamp/ball rotating probe; Turn 2 synthesizes student's correct observation and confirms monthly orbital geometry.
- **Why it Teaches Behavior**: Full end-to-end multi-turn demonstration of Socratic scaffolding from misconception to successful student discovery and affirmation.
- **Potential Weakness / Review Note**: Multi-turn dialogue requires model to remember context across turns.
- **Automated Validation**: Tier 1 Valid (Turn 1: 34 tkn, Turn 2: 78 tkn, Turn 3: 31 tkn, Turn 4: 67 tkn).
- **Contamination Audit**: Clean (0.16 max similarity vs `TRANS-004`).
- **Review Recommendation**: **APPROVE**.

#### 6. `paul_sft_pilot_soc_006`
- **Track**: `socratic_tutoring` | **Domain**: `physics` (`ray_optics`) | **Language**: `ta`
- **Target Concept**: Plane Mirror Field of View (stepping back from a vertical plane mirror does not reveal more of one's height).
- **Intended Behavior**: Validates perspective intuition, prompts reflection geometry ($\theta_i = \theta_r$) and proportional visual field subtended by mirror.
- **Why it Teaches Behavior**: Uses similar triangles / ray geometry scaffolding in Tamil without giving the geometric proof prematurely.
- **Potential Weakness / Review Note**: Requires student to understand that ray subtended angle and apparent mirror size scale together.
- **Automated Validation**: Tier 1 Valid (Turn 1: 40 tokens, Turn 2: 78 tokens).
- **Contamination Audit**: Clean (0.00 max similarity).
- **Review Recommendation**: **APPROVE**.

---

### Track 2: Concise Numerical STEM Problem Solving (4 Examples)

#### 7. `paul_sft_pilot_num_001`
- **Track**: `concise_stem_calc` | **Domain**: `physics` (`mechanics`) | **Language**: `en`
- **Target Concept**: Kinetic energy calculation ($m=1200\text{ kg}, v=20\text{ m/s}$).
- **Intended Behavior**: Structured `Given` $\to$ `Formula` $\to$ `Calculation` $\to$ `Boxed Answer` ($2.4 \times 10^5\text{ J}$ / $240\text{ kJ}$).
- **Why it Teaches Behavior**: Zero introductory meta-talk; clean algebraic substitution and explicit SI units.
- **Potential Weakness / Review Note**: None; ideal standard template.
- **Automated Validation**: Tier 1 Valid (Turn 1: 27 tokens, Turn 2: 120 tokens).
- **Contamination Audit**: Clean (0.12 max similarity vs `TRANS-001`).
- **Review Recommendation**: **APPROVE**.

#### 8. `paul_sft_pilot_num_002`
- **Track**: `concise_stem_calc` | **Domain**: `physics` (`electricity`) | **Language**: `hi`
- **Target Concept**: Electrical resistance from resistivity ($R = \rho L / A$).
- **Intended Behavior**: Devanagari structured problem solving with scientific notation exponents ($1.7 \times 10^{-8} \times 2 / 10^{-6} = 0.034\text{ }\Omega$).
- **Why it Teaches Behavior**: Teaches concise STEM layout in Hindi with proper mathematical notation and SI units ($\Omega$).
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 52 tokens, Turn 2: 135 tokens).
- **Contamination Audit**: Clean (0.06 max similarity vs `SCI-REAS-003`).
- **Review Recommendation**: **APPROVE**.

#### 9. `paul_sft_pilot_num_003`
- **Track**: `concise_stem_calc` | **Domain**: `chemistry` (`gas_laws`) | **Language**: `en`
- **Target Concept**: Ideal Gas Law Pressure ($P = nRT / V$).
- **Intended Behavior**: Multi-variable algebra with universal gas constant $R=8.314\text{ J/(mol K)}$, yielding $1.25 \times 10^5\text{ Pa}$ ($124.71\text{ kPa}$).
- **Why it Teaches Behavior**: Explicit algebraic rearrangement before substitution; clear SI unit cancellation.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 49 tokens, Turn 2: 125 tokens).
- **Contamination Audit**: Clean (0.11 max similarity vs `TRANS-002`).
- **Review Recommendation**: **APPROVE**.

#### 10. `paul_sft_pilot_num_004`
- **Track**: `concise_stem_calc` | **Domain**: `physics` (`gravitation`) | **Language**: `te`
- **Target Concept**: Acceleration due to gravity at altitude ($g' = g \frac{R^2}{(R+h)^2}$).
- **Intended Behavior**: Telugu structured calculation showing inverse square law scaling by factor of 4, yielding $2.45\text{ m/s}^2$.
- **Why it Teaches Behavior**: Direct Telugu STEM calculation template with exact algebraic simplification.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 52 tokens, Turn 2: 122 tokens).
- **Contamination Audit**: Clean (0.00 max similarity).
- **Review Recommendation**: **APPROVE**.

---

### Track 3: Clean Direct Multilingual Translation (4 Examples)

#### 11. `paul_sft_pilot_trn_001`
- **Track**: `clean_translation` | **Domain**: `biology` (`molecular_genetics`) | **Language**: `hi`
- **Target Concept**: DNA helicase unzipping and replication fork.
- **Intended Behavior**: Direct Devanagari translation preserving technical acronyms (`DNA`, `DNA helicase`, `replication fork`).
- **Why it Teaches Behavior**: Starts immediately in Hindi without conversational intro (*"यहाँ अनुवाद है"*); retains essential biochemical loan words.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 43 tokens, Turn 2: 54 tokens).
- **Contamination Audit**: Clean (0.12 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 12. `paul_sft_pilot_trn_002`
- **Track**: `clean_translation` | **Domain**: `physics` (`nuclear_physics`) | **Language**: `bn`
- **Target Concept**: Nuclear reactor control rods (cadmium/boron neutron absorption).
- **Intended Behavior**: Clean Bengali translation starting directly with scientific text; includes standard Bengali terms (`নিয়ন্ত্রক দণ্ড`, `বিভাজন শৃঙ্খল বিক্রিয়া`).
- **Why it Teaches Behavior**: Teaches zero meta-talk and natural technical terminology in Bengali.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 39 tokens, Turn 2: 45 tokens).
- **Contamination Audit**: Clean (0.10 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 13. `paul_sft_pilot_trn_003`
- **Track**: `clean_translation` | **Domain**: `chemistry` (`chemical_equilibrium`) | **Language**: `ta`
- **Target Concept**: Le Chatelier's dynamic equilibrium principle.
- **Intended Behavior**: Pure Tamil translation starting directly with principle statement.
- **Why it Teaches Behavior**: Demonstrates direct translation without phonetic transliteration or English wrappers.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 38 tokens, Turn 2: 48 tokens).
- **Contamination Audit**: Clean (0.08 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 14. `paul_sft_pilot_trn_004`
- **Track**: `clean_translation` | **Domain**: `physics` (`optics`) | **Language**: `mr`
- **Target Concept**: Total internal reflection and critical angle.
- **Intended Behavior**: Marathi translation starting immediately with optical density conditions.
- **Why it Teaches Behavior**: Clean Marathi scientific prose with zero English chatter.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 43 tokens, Turn 2: 52 tokens).
- **Contamination Audit**: Clean (0.06 max similarity).
- **Review Recommendation**: **APPROVE**.

---

### Track 4: Natural Indic Pedagogical Tone (3 Examples)

#### 15. `paul_sft_pilot_ind_001`
- **Track**: `indic_pedagogical_tone` | **Domain**: `physics` (`acoustics`) | **Language**: `hi`
- **Target Concept**: Closed Organ Pipe fundamental mode ($L = \lambda/4$).
- **Intended Behavior**: Modern NCERT Hindi educational register; clear breakdown of Node (निस्पंद) and Antinode (प्रस्पंद) with parenthetical English keywords.
- **Why it Teaches Behavior**: Natural classroom tone without hyper-archaic Sanskritization; easy for secondary school students to follow.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 29 tokens, Turn 2: 135 tokens).
- **Contamination Audit**: Clean (0.14 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 16. `paul_sft_pilot_ind_002`
- **Track**: `indic_pedagogical_tone` | **Domain**: `chemistry` (`periodic_properties`) | **Language**: `bn`
- **Target Concept**: Periodic trends in electronegativity across a period.
- **Intended Behavior**: Flowing Bengali instructional register explaining effective nuclear charge and constant shell number.
- **Why it Teaches Behavior**: Clean, step-by-step educational flow matching secondary textbook pedagogy in West Bengal / Bangladesh.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 34 tokens, Turn 2: 128 tokens).
- **Contamination Audit**: Clean (0.11 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 17. `paul_sft_pilot_ind_003`
- **Track**: `indic_pedagogical_tone` | **Domain**: `biology` (`neurobiology`) | **Language**: `te`
- **Target Concept**: Synaptic transmission and chemical neurotransmitters.
- **Intended Behavior**: Engaging, sequential Telugu pedagogical explanation covering action potential arrival, vesicle release, and receptor binding.
- **Why it Teaches Behavior**: Natural classroom tone in Telugu with bilingual technical anchors (`సినాప్స్ (Synapse)`, `న్యూరోట్రాన్స్‌మిటర్లు`).
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 26 tokens, Turn 2: 132 tokens).
- **Contamination Audit**: Clean (0.00 max similarity).
- **Review Recommendation**: **APPROVE**.

---

### Track 5: Capability Preservation (3 Examples)

#### 18. `paul_sft_pilot_prs_001`
- **Track**: `preservation_core` | **Domain**: `education` (`teacher_formative_assessment`) | **Language**: `en`
- **Target Concept**: Formative 3-item assessment on enzyme specificity and denaturation.
- **Intended Behavior**: High-quality teacher resource: 3 well-crafted MCQs with explicit keys and pedagogical distractor rationales ($<240$ tokens).
- **Why it Teaches Behavior**: Preserves Gemma 4's strong teacher assistance capability while strictly respecting the 350-token hard limit.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 33 tokens, Turn 2: 236 tokens).
- **Contamination Audit**: Clean (0.16 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 19. `paul_sft_pilot_prs_002`
- **Track**: `preservation_core` | **Domain**: `physics` (`wave_mechanics`) | **Language**: `hi`
- **Target Concept**: Doppler effect in acoustics (approaching vs receding sound sources).
- **Intended Behavior**: Comprehensive, clear scientific explanation in Hindi covering wavefront compression and apparent frequency shift.
- **Why it Teaches Behavior**: Retains strong baseline scientific exposition capability in Indic languages.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 37 tokens, Turn 2: 175 tokens).
- **Contamination Audit**: Clean (0.15 max similarity).
- **Review Recommendation**: **APPROVE**.

#### 20. `paul_sft_pilot_prs_003`
- **Track**: `preservation_core` | **Domain**: `education` (`ethics_academic_integrity`) | **Language**: `en`
- **Target Concept**: Academic integrity refusal and constructive educational scaffolding.
- **Intended Behavior**: Politely refuses to write student's graded homework essay; offers conceptual outline (Mitosis vs Meiosis) and invites student collaboration.
- **Why it Teaches Behavior**: Reinforces ethical boundaries without being robotic or dismissive.
- **Potential Weakness / Review Note**: None.
- **Automated Validation**: Tier 1 Valid (Turn 1: 42 tokens, Turn 2: 152 tokens).
- **Contamination Audit**: Clean (0.14 max similarity).
- **Review Recommendation**: **APPROVE**.

---

## 2. DPO Pilot Review Matrix (10 Preference Pairs)

| ID | Track / Language | Concept | Chosen ($y_w$) Behavioral Merit | Rejected ($y_l$) Behavioral Flaw | Token Counts ($y_w / y_l$) | Contam. Audit | Recommendation |
|---|---|---|---|---|---|---|---|
| **`paul_dpo_pilot_soc_001`** | `socratic_tutoring` / `en` | Sound speed in steel vs air | Marble line thought experiment + 1 question | Accurate 85-word lecture dumping formula $v=\sqrt{E/\rho}$ | 57 w / 81 w (both $<200$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_soc_002`** | `socratic_tutoring` / `hi` | Pendulum energy at peak | Validates $v=0$ + asks about height potential energy | Correct but premature Hindi lecture on $KE+PE=\text{const}$ | 99 w / 111 w (both $<220$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_soc_003`** | `socratic_tutoring` / `bn` | Plant nutrition from soil vs air | Scaffolds leaf photosynthesis role with 1 probe | Accurate 125-word lecture explaining autotrophic biology | 117 w / 125 w (both $<230$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_soc_004`** | `socratic_tutoring` / `en` | Thermal heat vs temperature | Iceberg mass vs teacup thought experiment | Scientifically defensible lecture on Kelvin, internal energy $U$, mass $m$ | 57 w / 92 w (both $<180$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_num_001`** | `concise_stem_calc` / `en` | Step-down transformer ($V_s=12\text{ V}$) | Given $\to$ Formula $\to$ Calculation $\to$ Boxed ($12\text{ V}$) | Verbose essay detailing Faraday's history before math | 53 w / 96 w (both $<180$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_num_002`** | `concise_stem_calc` / `hi` | Specific heat heating ($Q=336\text{ kJ}$) | दिया है $\to$ सूत्र $\to$ गणना $\to$ उत्तर ($3.36 \times 10^5\text{ J}$) | Conversational essay in Hindi explaining calorie background | 118 w / 140 w (both $<240$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_trn_001`** | `clean_translation` / `ta` | Mitochondria ATP synthase | 100% direct Tamil translation text | Opens with *"Sure! Here is the translation:"* + transliteration | 113 w / 68 w (both $<180$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_trn_002`** | `clean_translation` / `te` | Newton's third law of motion | Direct Telugu translation starting immediately | Meta-talk wrapper (*"Certainly! Here is..."* + *"Hope this helps"*) | 71 w / 69 w (both $<150$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_ind_001`** | `indic_pedagogical_tone` / `hi` | Right-hand thumb rule | Modern classroom Hindi with NCERT keywords | Grammatically valid but hyper-archaic Sanskritized register | 135 w / 91 w (both $<220$ tkn) | Clean | **APPROVE** |
| **`paul_dpo_pilot_ind_002`** | `indic_pedagogical_tone` / `mr` | Calvin cycle in stroma | Flowing Marathi classroom instructional register | Stilted, hyper-classical phrasing avoiding standard terms | 155 w / 56 w (both $<230$ tkn) | Clean | **APPROVE** |

---

## 3. Automated Validation & Quality Gate Summary

- **Total Pilot Records**: **30 records** (20 SFT examples, 10 DPO pairs).
- **Tier 1 Hard Validity**: **30 / 30 Passed (100%)** — All records conform to JSON Schema, UTF-8 validity, unique IDs, non-empty fields, and single-turn token budgets $< 350$ tokens.
- **Tier 3 Contamination Audit**: **30 / 30 Clean (100%)** — Audited against all 110 evaluation cases across `baseline_suite_v1.json`, `preservation_suite_v1.json`, and `behavioral_suite_v1.json`.
- **Review Recommendation**: **APPROVE ALL 30 RECORDS**.
