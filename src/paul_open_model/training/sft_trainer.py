"""Supervised Fine-Tuning via HuggingFace TRL SFTTrainer.

Wraps TRL's SFTTrainer (>= 1.9.0) with Gemma 4-specific handling:
- Custom Gemma4TextCollator for text-only multimodal workaround
- QLoRA configuration via BitsAndBytesConfig
- TensorBoard logging by default, W&B optional via WANDB_ENABLED env var
- Gradient checkpointing for memory efficiency
"""
