"""Quantization utilities for Gemma 4 models.

Supports:
- BitsAndBytes QLoRA (4-bit NF4) — primary method for consumer GPUs
- GPTQ — for pre-quantized model weights
- AWQ — alternative quantization scheme

Note on Gemma 4 ClippableLinear:
Gemma 4 uses Gemma4ClippableLinear layers in its multimodal projection
towers. These do NOT inherit from nn.Linear in older PEFT versions.
Ensure peft >= 0.18.0 or exclude these layers from LoRA targeting.
"""
