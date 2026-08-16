"""Chat template formatting for Gemma 4 models.

Applies Gemma 4 native chat templates and handles the multimodal
input requirements (mm_token_type_ids, token_type_ids) for text-only
fine-tuning.

CRITICAL: Gemma 4 models require mm_token_type_ids even for text-only
input. This module injects zero-filled tensors for these fields and
provides a custom data collator (Gemma4TextCollator) that preserves
them through the training pipeline.

Usage with SFTTrainer requires:
    remove_unused_columns=False  in SFTConfig/TrainingArguments
"""
