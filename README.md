# PAUL Open

**PAUL Open** is Paul Foundry's public, open-source research initiative for building and evaluating reproducible AI systems for multilingual knowledge work, science education, tutoring, teacher assistance, human-centered interaction, and scientific research.

[Website](https://open.paulfoundry.com/) · [Current research status](docs/PROJECT_STATUS.md) · [Public repository boundary](docs/PUBLIC_REPOSITORY_BOUNDARY.md) · [E4B experiment journey](docs/EXPERIMENT_JOURNEY_E4B.md) · [Contributing](CONTRIBUTING.md)

> [!IMPORTANT]
> **Current research state — 19 September 2026**
>
> - Base model: `google/gemma-4-E4B-it`.
> - The historical SFT adapter remains the **reference checkpoint**.
> - DPO V2/H4, DPO V3/H5, and DPO V4/H6 completed development cycles without promotion over SFT.
> - DPO V5 was technically valid; H7 matched generation completed, but the planned H7 multi-reviewer collection was intentionally discontinued without a human result.
> - DPO V6 Synthetic Corrective completed canonical production successfully: 516/516 intended trainable tensors changed.
> - In the matched 50-case diagnostic, V6 scored 90.62 versus 89.18 for SFT, with 100% automated safety adherence for both. This is a positive diagnostic signal, **not proof of superiority**.
> - V6 is development-frozen to the canonical production adapter for a fresh 12-case H8 DHE. Matched SFT/V6 generation completed successfully, all contamination/separation gates passed, and the blinded reviewer batch is ready; human collection has not started.
> - SHAE remains sealed and has not started.
> - Immutable Step 2 research freeze: `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`.

The detailed, evidence-oriented status is maintained in [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md).

---

## Repository is the research source of truth

The public GitHub repository is authoritative for PAUL Open research claims, experiment definitions, datasets that are intended to be public, evaluation protocols, manifests, and reproducibility documentation.

`open.paulfoundry.com` is the public presentation and participation layer. It may render research status, documentation, and human-evaluation entry points, but it must not independently redefine experimental facts. If the website and repository disagree, the versioned repository evidence takes precedence.

For machine-readable website integration, see:

- [`public/research-status.json`](public/research-status.json)
- [`public/human-evaluation.json`](public/human-evaluation.json)
- [`docs/WEBSITE_INTEGRATION.md`](docs/WEBSITE_INTEGRATION.md)

For coding agents and IDEs, start with [`AGENTS.md`](AGENTS.md). For what may and may not cross the public boundary, read [`docs/PUBLIC_REPOSITORY_BOUNDARY.md`](docs/PUBLIC_REPOSITORY_BOUNDARY.md).

---

## Research question

PAUL Open is not a leaderboard-optimization project. The working question is:

> **For the intended user and task, does post-training produce responses that are actually more useful, correct, clear, natural, and appropriately calibrated while preserving existing strengths?**

A higher aggregate score alone is not sufficient evidence that a checkpoint is better.

The project separates four evidence layers:

1. **Technical validity** — did training execute exactly as intended?
2. **Automated regression signal** — what observable indicators changed?
3. **Behavioral quality** — are responses actually better under task-specific review?
4. **Model superiority** — does improvement hold under clean evaluation, preservation checks, robustness testing, and blinded human preference?

DPO V2 through V6 have produced technically valid experimental checkpoints, but model superiority has not been established. V6 is now frozen for fresh H8 development evaluation.

---

## Current E4B experiment

The current research line follows:

`Gemma 4 E4B` → `PAUL SFT reference` → `DPO V2/H4` → `DPO V3/H5` → `DPO V4/H6` → `DPO V5/H7` → `DPO V6` → `H8 DHE`

### DPO V6 Synthetic Corrective

The canonical V6 production run completed successfully on 2026-09-19:

- source revision: `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- training records: 24
- configured epochs: 4
- global step: 8
- train loss: `0.646148681640625`
- intended trainable tensors changed: 516 / 516
- final adapter safetensors SHA-256: `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`

Its matched 50-case diagnostic produced a higher aggregate heuristic signal than SFT (90.62 vs 89.18), with 100% automated safety adherence for both checkpoints. These metrics are development diagnostics, not a clean held-out superiority result.

V6 is development-frozen for H8, a fresh 12-case prompt-frozen SFT-vs-V6 human comparison. Canonical matched generation completed successfully on run `35457211935`; the reviewer batch contains 12 eligible cases with 0 identical pairs, the benchmark-leakage audit is clean 12/12, and development-separation similarity remains below the frozen `<0.35` threshold. Human collection has not started and SHAE remains sealed.

Read the current evidence:

- [`docs/DPO_V6_PRODUCTION_DIAGNOSTIC_RESULTS.md`](docs/DPO_V6_PRODUCTION_DIAGNOSTIC_RESULTS.md)
- [`docs/DPO_V6_CANDIDATE_FREEZE.md`](docs/DPO_V6_CANDIDATE_FREEZE.md)
- [`docs/H8_DHE_V6_PRECOMMIT_SPEC.md`](docs/H8_DHE_V6_PRECOMMIT_SPEC.md)
- [`docs/H8_DHE_V6_GENERATION_RECORD.md`](docs/H8_DHE_V6_GENERATION_RECORD.md)
- [`artifacts/public-evidence/dpo-v6-production.json`](artifacts/public-evidence/dpo-v6-production.json)

### DPO V2 Corrective

The final DPO V2 production run is reproducible and technically validated:

- experiment: `paul_e4b_dpo_v2_corrective`
- corrective dataset: [`data/train/dpo_v2_corrective.jsonl`](data/train/dpo_v2_corrective.jsonl)
- records: 14
- training: DPO sigmoid loss, `beta=0.1`, 4 epochs
- topology: 2 × Tesla T4; policy on GPU 0, frozen external reference on GPU 1
- quantization: 4-bit NF4 base models
- final completion gate: PASS
- intended trainable tensors changed: 516 / 516
- train loss: `0.687744140625`
- train runtime: `238.58 s`

The technically valid run does **not** imply behavioral superiority. The current evidence shows both improvements and meaningful regressions, including multilingual/script fidelity and factual-risk cases.

Read the full evidence chain:

- [`docs/E4B_DPO_V2_CORRECTIVE.md`](docs/E4B_DPO_V2_CORRECTIVE.md)
- [`docs/EXPERIMENT_JOURNEY_E4B.md`](docs/EXPERIMENT_JOURNEY_E4B.md)

---

## Evaluation integrity

PAUL Open treats evaluation contamination as a research failure, not a documentation detail.

The canonical 50-case baseline was later found to overlap with DPO V2 source material at exact, content, template, or concept level. Therefore the current 50-case SFT-vs-DPO V2 comparison is explicitly labeled:

> **Diagnostic / contaminated for DPO V2 — not a clean held-out superiority evaluation.**

Future training datasets must be checked against the full frozen evaluation registry before acceptance. Human review is also being added as a first-class evidence layer rather than using heuristic benchmark numbers as the final judge.

---

## Human evaluation

PAUL Open uses blinded pairwise comparison: reviewers see a prompt and Response A / Response B without model identity, checkpoint identity, score hints, or hidden winner labels.

The research instrument and durability path are versioned in this repository. Google Forms is currently used as a collection surface, with normalized storage and an independent checksum-backed backup ledger.

The public website can provide a more approachable entry point, but the following rules remain fixed:

- reviewer links must be respondent-facing `/viewform` URLs only;
- editor/admin links and response spreadsheets must never be exposed;
- reviewer identity/contact data, private linkage data, blinding seeds, and hidden A/B/source mappings must never be exposed;
- model/checkpoint identity must stay blinded;
- optional comments remain optional;
- the website must not create a second, divergent research protocol;
- when no reviewed evaluation packet is open, the website should show the evaluation as closed/preparing rather than exposing a sandbox instrument.

See [`docs/WEBSITE_INTEGRATION.md`](docs/WEBSITE_INTEGRATION.md), [`docs/HUMAN_EVALUATION_PROTOCOL.md`](docs/HUMAN_EVALUATION_PROTOCOL.md), and [`docs/PUBLIC_REPOSITORY_BOUNDARY.md`](docs/PUBLIC_REPOSITORY_BOUNDARY.md).

---

## Target capabilities

PAUL Open currently explores:

- Indian and multilingual language understanding and generation
- translation, native-script fidelity, transliteration, and code-switching
- science education and rigorous conceptual explanation
- Socratic tutoring and misconception-guided learning
- student and teacher assistance
- human-centered interaction without false anthropomorphic claims
- scientific research assistance
- life-science and biomedical reasoning
- general reasoning and instruction following
- multimodal scientific understanding

Capability and dataset research notes:

- [`SKILLS.md`](SKILLS.md)
- [`DATASET_REGISTRY.md`](DATASET_REGISTRY.md)
- [`docs/BASELINE_EVALUATION.md`](docs/BASELINE_EVALUATION.md)

---

## Reproducing the research

The project uses versioned source, datasets, configs, manifests, and remote GPU execution. Kaggle is the current production GPU environment for the E4B DPO V2 workflow.

Useful entry points:

- [`notebooks/paul_open_model_training_kaggle.ipynb`](notebooks/paul_open_model_training_kaggle.ipynb)
- [`scripts/dpo_v2_e4b_train.py`](scripts/dpo_v2_e4b_train.py)
- [`configs/training/dpo_v2_e4b_corrective.yaml`](configs/training/dpo_v2_e4b_corrective.yaml)
- [`docs/TRAINING_GUIDE.md`](docs/TRAINING_GUIDE.md)

### Local setup

```bash
git clone https://github.com/foundrypaul-cloud/paul-open.git
cd paul-open

uv sync
cp .env.example .env
uv run pytest
```

Never commit tokens, private adapters/checkpoints, private Kaggle outputs, credentials, sealed assurance material, reviewer PII/private mappings, proprietary/confidential material, or third-party content that cannot be redistributed here. New/untracked content under `data/` is private by default; existing tracked datasets are public research evidence.

Before pushing a same-repository branch, run `python scripts/check_public_boundary.py`.

---

## Project map

```text
paul-open/
├── AGENTS.md                  # Agent/IDE operating context and source-of-truth rules
├── public/                    # Machine-readable public status for website consumers
├── configs/                   # Model, training, data, and evaluation configuration
├── data/                      # Intentionally tracked public research; new data is private by default
├── docs/                      # Research protocols, experiment history, and methodology
├── notebooks/                 # Reproducibility notebooks
├── scripts/                   # Training, evaluation, export, and verification entry points
├── src/paul_open_model/       # Core Python research library
├── tests/                     # Test suite
└── artifacts/                 # Versioned manifests and public research artifacts
```

---

## Contributing

PAUL Open welcomes technically rigorous contributions. Research-facing changes have stricter requirements than ordinary application code: provenance, contamination boundaries, experimental claims, reproducibility, and the public/private publication boundary must remain explicit.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request. The repository also provides issue and pull-request templates, a code of conduct, and a security policy.

---

## Research identity and provenance

PAUL Open is an independent research initiative of **Paul Foundry Technologies Private Limited**.

The current model research is derived from Google's Gemma 4 model family. PAUL Open is not an official Google model and is not affiliated with, endorsed by, or developed in collaboration with Google or Google DeepMind.

Website: https://open.paulfoundry.com/  
Repository: https://github.com/foundrypaul-cloud/paul-open

---

## License boundary

The PAUL Open-authored source-code layer is distributed under the **Apache License 2.0**; see [`LICENSE`](LICENSE).

The current `google/gemma-4-E4B-it` model repository identifies the model as Apache-2.0 licensed. Third-party datasets, libraries, benchmarks, models, and other materials retain their own licenses and attribution requirements. Public availability or permission to train does not by itself grant permission to redistribute the underlying content in this repository or release every possible derived artifact.

Apache-2.0 does not relicense third-party content, confidential/proprietary research, or material a contributor lacked permission to submit, and it does not grant trademark rights in Paul Foundry or PAUL Open names or marks.

See [`NOTICE.md`](NOTICE.md), [`docs/DATASET_REGISTRY.md`](docs/DATASET_REGISTRY.md), [`docs/PUBLIC_REPOSITORY_BOUNDARY.md`](docs/PUBLIC_REPOSITORY_BOUNDARY.md), and the applicable upstream terms before redistributing derived artifacts.

---

## Citation

See [`CITATION.cff`](CITATION.cff). A simple project citation is:

```text
Paul Foundry Technologies Private Limited.
"PAUL Open."
Paul Foundry Research Wing, 2026.
https://github.com/foundrypaul-cloud/paul-open
```
