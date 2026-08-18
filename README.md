# PAUL Open Model

Research project for specializing [Google Gemma 4](https://ai.google.dev/gemma) open-weight models for Indian/multilingual languages, science education, Socratic tutoring, teacher assistance, human-centered empathy, and life sciences research.

> **Status**: PAUL Open Model training pipeline is implemented.
> * **Reference run ID**: `paul_gemma4_e4b_25d8e53a`
> * **Base model**: `google/gemma-4-E4B-it`
> * **SFT corpus**: 180 records
> * **DPO corpus**: 65 records
> * **DPO training subset**: 55 records
> * **Permanent evaluation holdout**: 10 records
> * **Canonical reproducibility notebook**: `notebooks/paul_open_model_training_colab.ipynb`
> * **Dataset schemas**: `data/schemas/sft_schema.json`, `data/schemas/dpo_schema.json`

## Reproducibility

The committed reproducibility notebook (`notebooks/paul_open_model_training_colab.ipynb`) contains the complete Phase 0–11 workflow. The required datasets and manifest are now permanently committed, ensuring that the training pipeline and evaluation splits can be exactly reproduced.

---

## Google Colab Notebooks

You can run our research notebooks directly on Google Colab using free or dedicated NVIDIA GPUs:

| Notebook | Description | Colab Launch Link |
|---|---|---|
| **01 — Environment Setup** | Verifies Python 3.12, CUDA, GPU VRAM, and pins Gemma 4 ML dependencies. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/foundrypaul-cloud/paul-open/blob/main/notebooks/01_colab_environment_setup.ipynb) |
| **02 — First Model Validation (E4B)** | Quantized 4-bit loading of `google/gemma-4-E4B-it` on Tesla T4 via `AutoModelForMultimodalLM`. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/foundrypaul-cloud/paul-open/blob/main/notebooks/02_first_model_validation_e4b.ipynb) |
| **03 — Baseline Evaluation (E4B)** | Evaluates unmodified `google/gemma-4-E4B-it` across 50 benchmark cases (10 domains, 10 languages). | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/foundrypaul-cloud/paul-open/blob/main/notebooks/03_baseline_evaluation_e4b.ipynb) |

---

## Target Capabilities & Research Scope

1. **Indian Multilingual AI**: Native fluency and reasoning in English, Hindi, Bengali, Assamese, Tamil, Telugu, with extensibility to all 22 scheduled Indian languages.
2. **Multilingual Translation & Code-Switching**: Bidirectional translation (English ↔ Indic, Indic ↔ Indic), transliteration, and conversational code-switching (e.g., Hinglish, Tanglish, Benglish).
3. **Science Education**: Rigorous, curriculum-aligned conceptual explanations across Physics, Chemistry, Biology, Mathematics, and General Science.
4. **Student Tutoring**: Adaptive explanations, Socratic inquiry, misconception detection, step-by-step guidance, and grade-level adaptation (primary to undergraduate).
5. **Teacher Assistance**: Lesson planning (e.g., 5E model), assessment item generation, rubric design, Bloom's taxonomy mapping, and educational material creation.
6. **Empathy & Human-Centered Interaction**: Warm, supportive, and emotionally aware communication guided by the project's **PAUL Human-Centered Interaction / Anti-Anthropomorphism Guideline** (zero false claims of biological feelings, human memories, or physical life).
7. **Scientific Research Assistance**: Scientific literature comprehension, extreme summarization (SciTLDR style), hypothesis formulation, experimental design critique, and technical communication.
8. **Life Sciences & Biomedical Domains**: Genomics, molecular and cellular biology, biochemistry, pharmacology, neuroscience, and biological pathway reasoning.
9. **General Reasoning & Instruction Following**: Multi-step deduction, complex mathematics, and strict structured output adherence.
10. **Multimodal Scientific Capabilities**: Visual reasoning over scientific charts, plots, textbook diagrams, and geometry figures leveraging Gemma 4's native multimodal architecture.

For full mappings of capabilities to candidate resources, licensing, and evaluations, see:
- 📖 [SKILLS.md](SKILLS.md) — Capability & Skill Matrix
- 📊 [DATASET_REGISTRY.md](DATASET_REGISTRY.md) — Dataset Provenance, Licenses & Public Release Audits
- 🧪 [docs/BASELINE_EVALUATION.md](docs/BASELINE_EVALUATION.md) — Phase 2 Baseline Evaluation Framework & Benchmarks

---

## Model Strategy & Target Tiers

The project targets the Gemma 4 open-weights model family (Apache 2.0) with an extensible dynamic registry in `src/paul_open_model/models/loader.py`:

| Role / Tier | Model Name | Hugging Face ID | Architecture | Parameter Count | Context | Typical QLoRA VRAM |
|---|---|---|---|---|---|---|
| **Primary Target** ⭐ | **Gemma 4 26B A4B IT** | `google/gemma-4-26B-A4B-it` | `gemma4` (MoE) | 26B total (~4B active) | 256K | ~22 GB |
| **Development / Fallback** 🛠️ | **Gemma 4 12B IT** | `google/gemma-4-12B-it` | `gemma4_unified` (June 2026) | 12B dense | 256K | ~14 GB |
| **Maximum Capability** 🚀 | **Gemma 4 31B IT** | `google/gemma-4-31B-it` | `gemma4` | 31B dense | 256K | ~28 GB |
| **Edge / Lightweight** 📱 | **Gemma 4 E4B IT** | `google/gemma-4-E4B-it` | `gemma4` | 4.5B dense | 128K | ~6 GB |
| **Ultra-Lightweight** ⚡ | **Gemma 4 E2B IT** | `google/gemma-4-E2B-it` | `gemma4` | 2.3B dense | 128K | ~3.5 GB |

⭐ **Primary Target**: Gemma 4 26B A4B IT provides near-30B quality with ~4B active inference compute.  
🛠️ **Development / Fallback**: Gemma 4 12B IT (June 2026 Unified release) features an encoder-free unified multimodal architecture for fast iteration.  
🚀 **Maximum Capability**: Gemma 4 31B IT establishes the dense scaling ceiling.

See [docs/MODELS.md](docs/MODELS.md) for full architectural details and memory profiles.

---

## Quick Start

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.12 (managed automatically by uv in `.venv`)
- NVIDIA GPU with CUDA (for remote training — local development works on any workstation)

### Setup

```bash
# Clone the repository
git clone https://github.com/foundrypaul-cloud/paul-open.git
cd paul-open

# Create virtual environment and install core dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your HF_TOKEN and preferred HF_NAMESPACE

# Verify installation
uv run python -c "import paul_open_model; print(paul_open_model.__version__)"
```

### Install Optional Dependency Groups

```bash
uv sync --extra eval        # Evaluation benchmarks (sacrebleu, etc.)
uv sync --extra notebooks   # Jupyter & plotting tools
uv sync --extra wandb       # Weights & Biases (optional)
uv sync --extra dev         # Testing, linting, formatting
uv sync --extra all         # Full environment
```

---

## Project Structure

```
paul-open/
├── SKILLS.md                 # Full capability-to-resource-to-eval matrix
├── DATASET_REGISTRY.md       # Dataset licensing, provenance & release audits
├── configs/                  # Modular YAML configurations
│   ├── models/               # Model configs (26B-A4B, 12B Unified, 31B, E4B, E2B)
│   ├── training/             # Recipes: SFT QLoRA, SFT Full, DPO
│   ├── data/                 # Data pipelines for all 10 capability domains
│   └── evaluation/           # Standardized & custom benchmark configs
├── src/paul_open_model/      # Core research library
│   ├── models/               # Dynamic registry, loader, quantization, PEFT adapters
│   ├── data/                 # Registry, formatters, Indic & science loaders
│   ├── training/             # SFT & DPO training loops, custom callbacks
│   ├── evaluation/           # Benchmark harnesses, translation & empathy metrics
│   └── utils/                # Config validation, logging, hardware planning
├── scripts/                  # CLI entry points (train, evaluate, export, chat)
├── notebooks/                # Google Colab & Jupyter notebooks
├── tests/                    # Test suite
├── docs/                     # Detailed architectural guides and documentation
└── results/                  # Experiment outputs & checkpoints (gitignored)
```

---

## Development & Verification

```bash
# Run test suite
uv run pytest

# Linting
uv run ruff check .

# Code formatting
uv run ruff format .

# Type checking
uv run mypy src/
```

---

## License

This project's original code and configuration are licensed under the **Apache License 2.0** (see [LICENSE](LICENSE)). Third-party models and datasets remain subject to their respective original licenses.
