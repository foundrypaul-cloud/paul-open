# Gemma 4 Model Strategy & Registry

## Project Target Tiers

To balance computational efficiency with research capability across fine-tuning experiments, the project structures model targets into four tiers:

| Tier / Role | Model Name | HF Model ID | Architecture | Parameter Count | Context | Primary Use Case |
|---|---|---|---|---|---|---|
| **Primary Target** ⭐ | **Gemma 4 26B A4B IT** | `google/gemma-4-26B-A4B-it` | `gemma4` (MoE) | ~26B total (~4B active) | 256K | **Core research, specialization, and primary evaluation target.** Delivers ~30B quality with the compute speed and inference footprint of ~4B active parameters. |
| **Development / Fallback** 🛠️ | **Gemma 4 12B IT** | `google/gemma-4-12B-it` | `gemma4_unified` (June 2026) | ~12B dense | 256K | **Development, rapid pipeline testing, dataset debugging, and local fallback.** Uses the June 2026 encoder-free unified multimodal architecture. |
| **Maximum Capability** 🚀 | **Gemma 4 31B IT** | `google/gemma-4-31B-it` | `gemma4` | ~31B dense | 256K | **Upper-bound benchmark ceiling and large-scale runs.** Highest density dense reasoning. |
| **Edge / Mobile** 📱 | **Gemma 4 E4B IT** | `google/gemma-4-E4B-it` | `gemma4` | ~4.5B dense | 128K | On-device deployment testing and rapid prototyping. |
| **Ultra-Lightweight** ⚡ | **Gemma 4 E2B IT** | `google/gemma-4-E2B-it` | `gemma4` | ~2.3B dense | 128K | Edge testing on highly resource-constrained devices. |

---

## Architectural Distinctions: `gemma4` vs `gemma4_unified`

### 1. `gemma4` (Standard Multimodal Architecture)
- Models: `26B-A4B-it`, `31B-it`, `E4B-it`, `E2B-it`.
- Multimodal projection towers for vision and audio.
- Requires `mm_token_type_ids` and `token_type_ids` even during text-only fine-tuning.
- Supported via `transformers >= 5.5.2` and `peft >= 0.18.0`.

### 2. `gemma4_unified` (June 2026 Unified Release)
- Model: `12B-it`.
- **Encoder-free unified multimodal architecture** that processes audio, vision, and text in a shared token space without discrete heavyweight encoder towers.
- Significantly lowers latency and memory overhead on workstation and laptop execution.
- Supported via `transformers >= 5.15.0` and `trl >= 1.9.0`.

---

## Dynamic Model Registry (`GemmaModelRegistry`)

The codebase includes an extensible, dynamic model registry in `src/paul_open_model/models/loader.py`.

```python
from paul_open_model.models.loader import GemmaModelRegistry

# Fetch primary target
primary = GemmaModelRegistry.get_primary_target()
print(primary.hf_model_id)  # "google/gemma-4-26B-A4B-it"

# Fetch development fallback
fallback = GemmaModelRegistry.get_development_fallback()
print(fallback.hf_model_id)  # "google/gemma-4-12B-it"

# Fetch maximum capability
maximum = GemmaModelRegistry.get_maximum_capability()
print(maximum.hf_model_id)  # "google/gemma-4-31B-it"

# Flexible alias lookups
spec = GemmaModelRegistry.get("primary")  # resolves to 26B-A4B
spec = GemmaModelRegistry.get("12b-unified")  # resolves to 12B Unified
```

---

## Memory & Training Requirements (QLoRA 4-bit)

| Model | Weights VRAM (4-bit) | Training VRAM (QLoRA, Batch 4, Seq 4096) | Recommended Hardware |
|---|---|---|---|
| **Gemma 4 E2B IT** | ~1.8 GB | ~3.5 GB | Single 8 GB GPU (RTX 3060/4060) |
| **Gemma 4 E4B IT** | ~3 GB | ~6 GB | Single 12 GB GPU (RTX 3060/4070) |
| **Gemma 4 12B IT (Unified)** | ~8 GB | ~14 GB | Single 16–24 GB GPU (RTX 4080/4090/A5000) |
| **Gemma 4 26B A4B IT (MoE)** ⭐ | ~16 GB | ~22 GB | Single 24 GB GPU (RTX 3090/4090/A5000) or A100 |
| **Gemma 4 31B IT** | ~20 GB | ~28 GB | Single 48 GB GPU (A6000/A40) or 2x 24 GB GPUs or A100 80GB |
