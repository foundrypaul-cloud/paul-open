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

import torch
from transformers import BitsAndBytesConfig
from typing import Any

def get_quantization_config(quant_cfg: dict[str, Any] | None, compute_dtype: torch.dtype) -> BitsAndBytesConfig | None:
    if not quant_cfg or quant_cfg.get("method") != "qlora" or quant_cfg.get("bits") != 4:
        return None
        
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for BitsAndBytes 4-bit quantization, but no GPU was detected.")

    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type=quant_cfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=quant_cfg.get("bnb_4bit_use_double_quant", True)
    )
