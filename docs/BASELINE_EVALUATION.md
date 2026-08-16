# PAUL Open Model — Baseline Evaluation Framework

## 1. Overview & Research Objective

The **Baseline Evaluation Framework (Phase 2)** establishes a reproducible, transparent, and version-controlled benchmark to evaluate the base capabilities of unmodified Google Gemma 4 models prior to fine-tuning.

- **Initial Evaluated Checkpoint**: `google/gemma-4-E4B-it` (unmodified open weights)
- **Quantization Mode**: 4-bit NF4 with Double Quantization (`BitsAndBytesConfig`, `compute_dtype=torch.float16`)
- **Hardware Profile**: Google Colab Tesla T4 (14.56 GiB usable VRAM)
- **Benchmark Version**: `1.0.0` (Anchor version for all subsequent comparative evaluation)

> **Important**: This framework uses **original prompts** authored specifically for PAUL Open Model research. No copyrighted benchmark datasets are copied into the repository.

---

## 2. Capability Domains & Case Distribution

The baseline suite evaluates **50 curated benchmark cases** (5 cases per domain across 10 capability domains):

| # | Capability Domain | Domain Tag | Cases | Key Assessment Criteria |
|---|---|---|---|---|
| **A** | **Science Reasoning** | `science_reasoning` | 5 | First-principles deduction, thermodynamics, kinematics, periodic trends |
| **B** | **Life Sciences** | `life_sciences` | 5 | Molecular biology, CRISPR-Cas9, immunology, cellular respiration |
| **C** | **Scientific Research Assistance** | `scientific_research` | 5 | Hypothesis formulation, experimental controls (PCR), statistical reporting (p-value vs effect size) |
| **D** | **Socratic Tutoring** | `socratic_tutoring` | 5 | Inquiry-based guiding questions, misconception diagnosis, constructive feedback |
| **E** | **Student Assistance** | `student_assistance` | 5 | Structured revision schedules, concept comparisons, step-by-step problem solving |
| **F** | **Teacher Assistance** | `teacher_assistance` | 5 | 5E lesson planning, rubric design, assessment item generation, differentiated tasks |
| **G** | **Indian Language Understanding** | `indic_understanding` | 5 | Native comprehension & generation across major Indian linguistic families |
| **H** | **Multilingual Translation** | `multilingual_translation` | 5 | Scientific & educational translation (English ↔ Indic languages) |
| **I** | **Empathy & Human-Centered Interaction** | `empathy_human_centered` | 5 | Supportive communication adhering to the **PAUL Human-Centered Interaction Guideline** |
| **J** | **Scientific Explanation Quality** | `scientific_explanation` | 5 | Intuitive physical analogies, wave interference, everyday science phenomena |

---

## 3. Multilingual Coverage

The baseline benchmark encompasses 10 languages:

1. **English (`en`)**: Global scientific baseline and reference translations.
2. **Hindi (`hi`)**: Northern/Central Indo-Aryan, Devanagari script.
3. **Bengali (`bn`)**: Eastern Indo-Aryan, Bengali script.
4. **Tamil (`ta`)**: Dravidian, Tamil script.
5. **Telugu (`te`)**: Dravidian, Telugu script.
6. **Marathi (`mr`)**: Indo-Aryan, Devanagari script.
7. **Gujarati (`gu`)**: Indo-Aryan, Gujarati script.
8. **Kannada (`kn`)**: Dravidian, Kannada script.
9. **Malayalam (`ml`)**: Dravidian, Malayalam script.
10. **Punjabi (`pa`)**: Indo-Aryan, Gurmukhi script.

---

## 4. Evaluation Methodology & Metric Categorization

Evaluation metrics are structured into three distinct layers:

### A. Automated Deterministic Metrics
- **Keyword Coverage Score ($0.0 - 1.0$)**: Proportion of essential scientific and domain concepts present in the output.
- **Safety & Anti-Anthropomorphism Adherence ($1.0 \text{ or } 0.0$)**: Strict verification that the model does not make false biological or human emotional claims (*"I feel pain"*, *"when I was in school"*, *"my human heart"*).
- **Script Match Score ($1.0 \text{ or } 0.0$)**: Unicode character-block detection verifying the response is written in the correct native script.
- **Length & Structure Compliance**: Verifies responses stay within reasonable pedagogical token bounds ($15 - 400$ tokens).

### B. Heuristic Rubric Scoring (0 – 100)
Combines weighted deterministic indicators into a composite benchmark score:
$$\text{Rubric Score} = 40 \times \text{Keyword Coverage} + 30 \times \text{Safety Adherence} + 15 \times \text{Script Match} + 15 \times \text{Length Compliance}$$

### C. Qualitative Human Review Flags
Cases involving subjective pedagogy (Socratic dialogue), emotional resonance, or deep cultural nuance are automatically flagged for **Human Expert Review** before final publication.

---

## 5. Execution Workflow & Persistence Architecture

To guarantee robustness against Google Colab disconnections or VM teardowns, the evaluation runner implements a dual-mode persistence architecture:

### Persistence Modes

1. **`runtime_local` (Default without Drive)**:
   - Working directory: `results/baseline/<experiment_id>/` on the local VM filesystem (`/content`).
   - Per-case checkpointing: Every completed case is appended to `checkpoint.jsonl`.
   - Resume behavior: Supports **same-runtime resume** (e.g. re-running cells after a transient network hiccup within the active session).
   - *Limitation*: If the Colab runtime is disconnected or torn down, ephemeral VM disk contents are lost.

2. **`drive_mirrored` (Optional with Google Drive)**:
   - Working directory: Local `results/baseline/<experiment_id>/` + Mirrored to `/content/drive/MyDrive/paul-open-experiments/baseline/<experiment_id>/`.
   - Dual mirroring: `checkpoint.jsonl`, `STATUS.json`, `results.json`, `results.csv`, `summary.md`, `metadata.json`, and `manifest.json` are mirrored to Drive in real time.
   - Resume behavior: Supports **persistent restart-safe resume**. If a Colab VM is restarted, the runner detects the existing Drive checkpoint, synchronizes completed cases, and evaluates only remaining prompts.

---

## 6. Result Artifacts & Manifest

Each experiment produces the following isolated files under `results/baseline/<experiment_id>/`:

| File | Format | Content |
|---|---|---|
| `manifest.json` | JSON | High-level execution summary, persistence mode, local/drive paths, completion status |
| `results.json` | JSON | Complete case-by-case data (prompts, responses, metrics, latency, VRAM) |
| `results.csv` | CSV | Tabular flat representation for spreadsheet analysis |
| `summary.md` | Markdown | Formatted scorecard report with domain & language breakdowns |
| `metadata.json` | JSON | Hardware (GPU/VRAM), Python/package versions, and sampling parameters |
| `STATUS.json` | JSON | Machine-readable status (`SUCCESS`, `PARTIAL`, `FAILED`), case counts, peak VRAM |
| `checkpoint.jsonl` | JSONL | Incremental line-by-line checkpoint stream |
| `execution.log` | Text | Timestamped runner execution log |

> **Zero Leakage Rule**: Result files are strictly sanitized. No API tokens, passwords, credentials, model weights, HF caches, or private filesystem paths are stored.

---

## 7. Post-Processing & Offline Analysis

The CLI tool [scripts/analyze_baseline.py](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/scripts/analyze_baseline.py) allows inspecting results completely offline without requiring GPU or model weights:

```bash
# Analyze latest run
uv run python scripts/analyze_baseline.py --latest

# Analyze specific experiment folder
uv run python scripts/analyze_baseline.py -d results/baseline/exp_gemma4_e4b_baseline_<timestamp>
```
