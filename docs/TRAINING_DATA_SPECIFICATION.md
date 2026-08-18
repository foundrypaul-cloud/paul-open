# PAUL Open Model — Phase 3 Training Data Specification & Pilot Design

> [!IMPORTANT]
> **TRAINING / EVALUATION CONTAMINATION PREVENTION PROTOCOL**
> The 110 held-out evaluation cases across the Canonical Baseline (`50`), Capability Preservation (`30`), and Held-Out Behavioral (`30`) suites are **strictly held out** and must not be used as source material, templates, or references for model development.
> The repository enforces a multi-tier contamination-prevention protocol combining exact-match string search, n-gram lexical overlap calculation, numerical parameter collision detection, conceptual isolation screening, and expert human review to drastically minimize data leakage risk.

---

## 1. Executive Summary & Target Corpus Architecture

The Phase 3 training corpus is designed to instill the four behavioral adaptation capabilities identified in the baseline diagnostic analysis while safeguarding Gemma 4's strong baseline performance.

| Dataset Track | Target Quantity | Primary Behavioral Purpose | Modality / Format |
|---|---|---|---|
| **SFT Full Corpus** | **180 Examples** | High-fidelity behavioral demonstrations and multi-turn scaffolding | Multi-turn and single-turn JSONL (`sft_schema.json`) |
| **DPO Full Corpus** | **65 Pairs** | Contrastive preference pairs suppressing realistic model failure modes | Preference pairs JSONL (`dpo_schema.json`) |
| **SFT Initial Pilot** | **20 Examples** | Calibration pilot covering all target behaviors | JSONL subset for human review |
| **DPO Initial Pilot** | **10 Pairs** | Calibration pilot contrastive pairs | JSONL subset for human review |

---

## 2. SFT Corpus Allocation (180 Examples)

Priority is allocated to **Socratic Tutoring** (27.8% of SFT) as it exhibited the largest behavioral deficit during baseline diagnostics (premature solution dumping).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SFT ALLOCATION BREAKDOWN (180 EXAMPLES)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  [1] Socratic Tutoring (Misconceptions & Scaffolding)        : 50 (27.8%)   │
│  [2] Concise Numerical & STEM Problem Solving                : 35 (19.4%)   │
│  [3] Clean Direct Multilingual Translation                   : 30 (16.7%)   │
│  [4] Natural Indic Pedagogical Tone & Classroom Register     : 35 (19.4%)   │
│  [5] Capability Preservation (Teacher Tools, Life Sciences)  : 30 (16.7%)   │
│                                                                             │
│  TOTAL SFT EXAMPLES                                          : 180 (100%)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed SFT Category Specifications

#### Track 1: Socratic Tutoring & Misconception Scaffolding (50 Examples)
- **Target Topics**: Physics (Pascal's hydrostatic paradox, ray optics reflection, momentum vs force), Chemistry (evaporation vs boiling, conservation of mass in open/closed systems, endothermic phase changes), Biology (blood vessel roles, photosynthesis dark reactions, natural selection mechanisms), Mathematics (fraction addition, distributive property, negative number operations).
- **Format**:
  - 30 Multi-turn examples (2 to 3 turns: Student misconception $\to$ Assistant Socratic probe $\to$ Student partial response $\to$ Assistant synthesis/reinforcement).
  - 20 Single-turn examples (Turn 1 response: Validate intuition + ask 1 guiding question).
- **Key Behavioral Invariants**:
  - Zero lecture dumping on Turn 1.
  - Terminate with exactly ONE focused guiding question.
  - Use accessible physical analogies or thought experiments.
  - Token budget: $< 220$ tokens per turn.

#### Track 2: Concise Numerical & STEM Problem Solving (35 Examples)
- **Target Topics**: Kinematics ($v=u+at, s=ut+\frac{1}{2}at^2$), Work/Energy ($W=Fd, KE=\frac{1}{2}mv^2, PE=mgh$), Electromagnetism ($R=\rho L/A, V=IR, P=VI$), Chemistry stoichiometry ($n=m/M, PV=nRT, M_1V_1=M_2V_2$), Waves & Thermodynamics ($Q=mc\Delta T, c=f\lambda$).
- **Format**: Single-turn.
- **Key Behavioral Invariants**:
  - Clean structure: `Given` $\to$ `Formula` $\to$ `Calculation` $\to$ `Boxed Answer with SI Units`.
  - Zero conversational preambles (*"Let's solve this step by step..."*).
  - Explicit arithmetic without skipping critical algebraic substitutions.
  - Token budget: $< 200$ tokens.

#### Track 3: Clean Direct Multilingual Translation (30 Examples)
- **Target Languages**: Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese.
- **Target Topics**: Core secondary and senior secondary science terminology and conceptual paragraphs (genetics, nuclear physics, organic chemistry, thermodynamics).
- **Format**: Single-turn.
- **Key Behavioral Invariants**:
  - Direct target-language translation in native script.
  - Zero unsolicited conversational commentary (*"Sure, here is the translation:"*).
  - Zero unsolicited romanized transliteration.
  - **Technical notation preservation**: Standard formulas, chemical equations, scientific notation ($1.0 \times 10^{-6}\text{ m}^2$), and established scientific acronyms (`DNA`, `RNA`, `ATP`, `pH`, `CO2`) are preserved without artificial script penalties.

#### Track 4: Natural Indic Pedagogical Tone & Classroom Register (35 Examples)
- **Target Languages**: Hindi (8), Bengali (6), Tamil (6), Telugu (5), Marathi (4), Gujarati (3), Kannada (1), Malayalam (1), Punjabi (1).
- **Target Topics**: Explaining foundational scientific concepts using native idioms and natural classroom registers.
- **Format**: Single-turn and 2-turn dialogue.
- **Key Behavioral Invariants**:
  - Natural modern educational register aligned with standard secondary classroom instruction.
  - Judicious inclusion of English technical terms in parentheses where pedagogically helpful: e.g., *"गतिज ऊर्जा (Kinetic Energy)"* or *"অপবর্তন (Diffraction)"*.
  - Strict avoidance of hyper-archaic, artificially Sanskritized or classical vocabulary that obscures comprehension.

#### Track 5: Capability Preservation & Instructional Quality (30 Examples)
- **Target Topics**: Teacher assistance (formative checks, rubrics, tiered quiz generation), complex scientific explanations, life science processes, human empathy and ethical boundaries.
- **Format**: Single-turn.
- **Key Behavioral Invariants**:
  - Structured, clear pedagogical outputs matching Gemma 4's strong baseline performance.
  - Maintains strict anti-anthropomorphism and academic integrity boundaries.

---

## 3. DPO Corpus Allocation & Negative-Response Design

DPO pairs reinforce the distinction between optimal educational behavior and realistic model failure modes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DPO PREFERENCE PAIRS ALLOCATION (65 PAIRS)               │
├─────────────────────────────────────────────────────────────────────────────┤
│  [1] Socratic Tutoring (Guiding Probe vs Premature Lecture)   : 22 (33.8%)   │
│  [2] Concise Numerical (Direct Calculation vs Verbose Essay)  : 15 (23.1%)   │
│  [3] Clean Translation (Direct Output vs Meta-talk / Wrappers): 14 (21.5%)   │
│  [4] Natural Indic Tone (Classroom Register vs Archaic/Stilted): 14 (21.5%) │
│                                                                             │
│  TOTAL DPO PAIRS                                             : 65 (100%)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Contrastive Pair Design & Token Constraints

> [!IMPORTANT]
> **DPO NEGATIVE RESPONSE VALIDITY CONSTRAINTS**
> All non-preferred responses ($y_l$) must strictly satisfy:
> 1. **Schema validity**: Fully valid JSON and UTF-8 string encoding.
> 2. **Token hard limit**: Must remain **strictly below the 350-token limit** per turn (typically 200–300 tokens).
> 3. **Behavioral inferiority**: Must represent realistic, plausible model failures (e.g., unnecessary conversational preambles, lecture dumping, or meta-talk wrappers) rather than synthetic corruption, gibberish, or token overflow.

| Track | Prompt Characteristic | Preferred Response ($y_w$) | Non-Preferred Response ($y_l$) | Key Distinguishing Failure Mode |
|---|---|---|---|---|
| **Socratic** | Student expresses conceptual misconception | Validates intuition, offers 1 concrete analogy, asks **single guiding question** ($<150$ tokens) | Delivers a well-written 250-word comprehensive lecture explaining the full concept immediately ($<320$ tokens) | **Lecture Dumping**: Destroys active student discovery |
| **Numerical** | Multi-step STEM calculation with numerical values | Given $\to$ Formula $\to$ Step-by-step arithmetic $\to$ **Boxed SI unit answer** ($<180$ tokens) | 260-word verbose essay explaining historical background and unnecessary preambles before giving the answer ($<320$ tokens) | **Excessive Verbosity**: Wastes token budget and obscures numerical result |
| **Translation** | "Translate this science text into Tamil/Hindi..." | Starts **immediately** in native script with faithful scientific translation | Opens with conversational filler (*"Certainly! Here is the Hindi translation for your text:"*) plus romanized transliteration ($<280$ tokens) | **Conversational Meta-talk & Wrappers**: Pollutes pure translation outputs |
| **Indic Tone** | Explain a physics/biology concept in Hindi/Bengali | Fluid, modern classroom register with standard textbook terms and bilingual keywords | Grammatically valid but overly literal translation using archaic Sanskritized/classical terms ($<280$ tokens) | **Unnatural / Archaic Register**: Obstructs student accessibility |

---

## 4. Linguistic, Domain & Difficulty Distribution

### A. Language Distribution (SFT 180 / DPO 65)

| Language | ISO Code | SFT Target (180) | DPO Target (65) | Combined Examples | Share (%) |
|---|---|---|---|---|---|
| **English** | `en` | 68 | 26 | 94 | 38.4% |
| **Hindi** | `hi` | 36 | 13 | 49 | 20.0% |
| **Bengali** | `bn` | 24 | 8 | 32 | 13.1% |
| **Tamil** | `ta` | 18 | 6 | 24 | 9.8% |
| **Telugu** | `te` | 14 | 5 | 19 | 7.8% |
| **Marathi** | `mr` | 8 | 3 | 11 | 4.5% |
| **Gujarati** | `gu` | 6 | 2 | 8 | 3.3% |
| **Kannada** | `kn` | 2 | 1 | 3 | 1.2% |
| **Malayalam** | `ml` | 2 | 1 | 3 | 1.2% |
| **Punjabi** | `pa` | 2 | 1 | 3 | 1.2% |
| **Total** | | **180** | **65** | **245** | **100.0%** |

### B. STEM Domain Distribution
- **Physics**: 32% (Fluid Mechanics, Optics, Electromagnetism, Thermodynamics, Motion)
- **Chemistry**: 24% (Atomic Structure, Chemical Bonding, Stoichiometry, Gas Laws, Acids/Bases)
- **Life Sciences & Biology**: 24% (Cell Biology, Physiology, Genetics, Plant Nutrition, Synaptic Transmission)
- **Mathematics**: 12% (Algebra, Fractions, Coordinate Systems, Trigonometry)
- **Earth & Environmental Science**: 8% (Hydrology, Atmospheric Systems, Energy Cycles)

### C. Difficulty Level Distribution
- **Beginner (Foundation)**: 25% (Introductory definitions, basic single-step calculations, foundational misconceptions)
- **Intermediate (Core Secondary)**: 60% (Multi-step problems, conceptual explanations, multi-turn dialogues)
- **Advanced (Senior Secondary / Applied)**: 15% (Rigorous multi-parameter physics, complex biochemical pathways)

---

## 5. Single-Turn vs Multi-Turn Strategy

- **Multi-Turn (44 SFT examples / 24.4%)**:
  - Allocated strictly to **Socratic Tutoring** (30 examples) and **Indic Pedagogical Dialogues** (14 examples).
  - *Socratic Multi-turn Flow*: Turn 1 (Scaffold probe) $\to$ Turn 2 (Evaluate student attempt & narrow probe) $\to$ Turn 3 (Affirm correct reasoning & synthesize 2-sentence takeaway).
- **Single-Turn (136 SFT examples / 75.6%)**:
  - Allocated to Concise Numerical STEM, Clean Translation, and Capability Preservation tasks where single-turn economy is required.

---

## 6. Finalized Dataset Specification

The finalized training corpus covers all target behaviors and uses concepts that have been thoroughly audited to remain distinct from all frozen evaluation cases.

### SFT Corpus
- **180 total records** used for supervised fine-tuning.

### DPO Corpus
- **65 total records**
- **55 records** used for DPO training.
- **10 records** permanently held out for deterministic evaluation.

#### Permanent Evaluation Holdout IDs
The DPO training subset is formed by strictly excluding these 10 exact record IDs, which are permanently reserved for final evaluation:
- `paul_dpo_ind_001`
- `paul_dpo_ind_007`
- `paul_dpo_ind_013`
- `paul_dpo_ind_019`
- `paul_dpo_soc_005`
- `paul_dpo_soc_011`
- `paul_dpo_soc_017`
- `paul_dpo_stem_003`
- `paul_dpo_stem_009`
- `paul_dpo_stem_015`

The pipeline explicitly verifies zero overlap between SFT IDs and DPO IDs before preparing the DPO split.

### Dataset Integrity Verification
The training pipeline enforces strict SHA-256 integrity checks (Phase 1) on the reproducibility assets prior to loading any data:
- **SFT SHA-256**: `4c48d5077a5a6df0da7fed592c17dfd00f172da0f4a00ece0c7b682d7e2ef875`
- **DPO SHA-256**: `a613e476cb161ffaddd1638bbd302d8b63c4534e4dabc33936756278cebd245e`
- **Manifest SHA-256**: `36414ac115f075bc8845f274303705c806e33962529624a1d567d774f9473caa`

The manifest is located at `data/train/generation_progress_v2.json`.

## 7. Data-Quality Pipeline & Contamination Prevention Protocol

Every example in the pilot and full corpus must pass a 3-tier validation gate:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       3-TIER DATA QUALITY PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  [TIER 1: HARD VALIDITY]                                                    │
│  • JSON/JSONL syntax and UTF-8 validity.                                    │
│  • Schema compliance (sft_schema.json / dpo_schema.json).                   │
│  • Strict token limit: < 350 tokens per single turn (both SFT and DPO).     │
│  • Disjoint, unique ID naming convention.                                   │
│                                                                             │
│  [TIER 2: HEURISTIC SCREENING]                                              │
│  • Socratic: Verify non-empty and presence of trailing question mark.       │
│  • Numerical: Verify presence of numeric value and SI unit.                 │
│  • Translation: Whitelist check (zero conversational English preambles).     │
│  • Indic: Script validation matching target language code.                  │
│                                                                             │
│  [TIER 3: CONTAMINATION PREVENTION & ISOLATION AUDIT]                       │
│  • 0 Exact prompt matches against 110 evaluation cases.                     │
│  • < 35% 3-gram lexical cosine similarity against eval testbeds.            │
│  • 0 Numerical parameter collisions against eval testbeds.                  │
│  • Expert human qualitative review for semantic independence.               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Contamination Prevention Protocol & Methodological Guardrails

To prevent evaluation leakage and maintain clean scientific benchmarks:
1. **Multi-Faceted Audit**: The contamination prevention protocol combines automated exact-match string search, n-gram lexical overlap measurement, numerical parameter collision detection, conceptual mapping, and expert human review. While no automated tool provides mathematical proof of conceptual independence, this protocol drastically suppresses empirical overlap.
2. **Pre-Commit Isolation Audit**: Run `scripts/check_leakage.py` against both pilot and full datasets before human review.
3. **Execution Guard**: Dataset generation scripts must write exclusively to `data/training/` and must never modify `src/paul_open_model/evaluation/data/` or any baseline evaluation artifacts.
