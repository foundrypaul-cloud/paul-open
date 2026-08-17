# PAUL Open Model — Evaluation Suites Guide

This document describes the three evaluation suites supporting the PAUL Open Model research program, their architectural roles, and strict isolation protocols.

> [!IMPORTANT]
> **IMMUTABLE EVALUATION ASSET NOTICE**
> These evaluation suites are held out and must not be used as model-development data.
> Both `preservation_suite_v1.json` and `behavioral_suite_v1.json` are frozen at version **`v1.0.0`** and serve as immutable benchmarks for regression detection and behavioral verification.

---

## 1. Overview of the Three Evaluation Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PAUL OPEN MODEL THREE EVALUATION LAYERS                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [LAYER 1: CANONICAL BASELINE BENCHMARK v1.0.0] (50 Cases)                  │
│  • Location: src/paul_open_model/evaluation/data/baseline_suite_v1.json      │
│  • Role: Immutable research anchor (Audited mean score: 90.5/100).           │
│  • Status: FROZEN & IMMUTABLE.                                              │
│                                                                             │
│  [LAYER 2: CAPABILITY PRESERVATION SUITE v1.0.0] (30 Cases)                 │
│  • Location: src/paul_open_model/evaluation/data/preservation_suite_v1.json  │
│  • Role: Monitors regression across baseline Gemma 4 strengths.             │
│  • Covers: Teacher Assistance (6), Scientific Explanation (6),              │
│    Life Sciences (6), Indic Understanding (6), Safety & Interaction (6).    │
│  • Status: FROZEN & IMMUTABLE.                                              │
│                                                                             │
│  [LAYER 3: HELD-OUT BEHAVIORAL SUITE v1.0.0] (30 Cases)                     │
│  • Location: src/paul_open_model/evaluation/data/behavioral_suite_v1.json    │
│  • Role: Measures whether fine-tuning acquired the 4 target behaviors.      │
│  • Covers: Guided Socratic Tutoring (8), Concise STEM Calculation (8),      │
│    Clean Direct Translation (7), Natural Indic Pedagogical Tone (7).         │
│  • Status: FROZEN & IMMUTABLE.                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Suite Details & Specifications

### Layer 1 — Canonical Baseline Benchmark (`baseline_suite_v1.json`)
- **Case Count**: 50 cases across 10 capability domains.
- **Version**: `1.0.0` (Frozen)
- **Languages**: English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi.
- **Role**: Provides the primary anchor to compare unmodified `google/gemma-4-E4B-it` with fine-tuned checkpoints under identical sampling parameters ($T=0.7, \text{top\_p}=0.9, \text{max\_tokens}=256$).

---

### Layer 2 — Capability Preservation Suite (`preservation_suite_v1.json`)
- **Case Count**: 30 cases (`PRES-TCH-001..006`, `PRES-EXP-001..006`, `PRES-LIF-001..006`, `PRES-IND-001..006`, `PRES-SAF-001..006`).
- **Version**: `1.0.0` (Frozen)
- **Domain Coverage**:
  1. *Teacher Assistance (6)*: Formative assessment design, tiered rubrics, lesson planning, lab practical guides.
  2. *Scientific Explanation (6)*: Photoelectric effect, Bernoulli's principle, Coriolis deflection, acid rain, semiconductor doping, geothermal energy.
  3. *Life Sciences (6)*: Krebs cycle, action potential propagation, natural selection vs genetic drift, transpiration cohesion, recombinant plasmids, antibody specificity.
  4. *Indic Understanding (6)*: 10% ecological energy rule, states of matter, chemical bonding, small intestine digestion, series/parallel circuits, universal gravitation.
  5. *Appropriate AI Interaction & Safety (6)*: Anti-anthropomorphism boundaries, refusal of live exam cheating, mental health support, hazardous home remedy warnings, AI role boundaries.
- **Purpose**: Detects catastrophic forgetting or capability regression in areas where the base model already demonstrates high competence.

---

### Layer 3 — Held-Out Behavioral Suite (`behavioral_suite_v1.json`)
- **Case Count**: 30 cases (`BEH-SOC-001..008`, `BEH-NUM-001..008`, `BEH-TRN-001..007`, `BEH-IND-001..007`).
- **Version**: `1.0.0` (Frozen)
- **Target Behavioral Tracks**:
  1. *Guided Socratic Tutoring (8)*: Assesses misconception identification, validation of intuition, avoidance of premature lecture dumping, and single trailing guiding probes.
  2. *Concise Numerical/STEM Problem Solving (8)*: Assesses concise Given/Target blocks, immediate formula application, step-by-step arithmetic without verbose preambles, and boxed answers with units.
  3. *Clean Direct Translation (7)*: Assesses direct target-language scientific output, zero conversational English pleasantries (*"Here is the translation..."*), and zero unsolicited transliteration across Indic languages.
  4. *Natural Indic Pedagogical Tone (7)*: Assesses natural classroom register, NCERT-aligned bilingual technical terms (*"गतिज ऊर्जा (Kinetic Energy)"*), and absence of archaic Sanskritization.

---

## 3. Strict Evaluation Isolation Protocols

> [!CAUTION]
> **TRAINING CONTAMINATION PROHIBITION**
> Under no circumstances may any case from `baseline_suite_v1.json`, `preservation_suite_v1.json`, or `behavioral_suite_v1.json` be included in, paraphrased for, or referenced during SFT or DPO dataset generation. These evaluation suites are held out and must not be used as model-development data.

1. **Pre-Training Leakage Audit**: Every proposed training batch must pass `scripts/check_leakage.py` with zero exact matches, zero parameter collisions, and $< 35\%$ n-gram overlap.
2. **Immutable Versioning**: The evaluation suites are frozen at version `1.0.0`.
3. **Execution Tooling**:
   ```bash
   # Run baseline benchmark evaluation
   uv run python scripts/run_evaluation.py configs/evaluation/baseline_e4b.yaml

   # Run capability preservation evaluation
   uv run python scripts/run_evaluation.py configs/evaluation/preservation_e4b.yaml

   # Run held-out behavioral evaluation
   uv run python scripts/run_evaluation.py configs/evaluation/behavioral_e4b.yaml
   ```
