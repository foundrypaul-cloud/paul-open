# Architecture

See the project README for the current architecture overview.

## Config-Driven Design

All variation is controlled by YAML configs in `configs/`:
- `configs/models/` — per-model settings (HF ID, quantization, LoRA rank)
- `configs/training/` — training recipes (SFT QLoRA, SFT full, DPO)
- `configs/data/` — dataset pipeline configs
- `configs/evaluation/` — benchmark configs

The same training script works for all model sizes by pointing to different configs.
