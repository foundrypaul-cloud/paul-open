"""LoRA/QLoRA adapter management for Gemma 4.

Handles:
- Attaching LoRA adapters via PEFT
- Merging adapters back into base model weights
- Exporting merged models to HuggingFace Hub
- Adapter checkpoint management

IMPORTANT: When targeting modules for LoRA, be aware that Gemma 4's
multimodal layers (Gemma4ClippableLinear) may not be recognized by
older PEFT versions. Use modules_to_save for critical projection layers
if needed.
"""
