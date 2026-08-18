# Reproducible Training Guide

The PAUL Open Model utilizes a strict two-stage fine-tuning pipeline (SFT followed by DPO), tracked in the canonical reproducibility notebook: `notebooks/paul_open_model_training_colab.ipynb`.

## 1. Hardware and Model Specification
*   **Hardware**: Tesla T4 (or equivalent)
*   **Base Model**: `google/gemma-4-E4B-it`
*   **Quantization**: 4-bit NF4 with double quantization (and FP16 compute where natively configured by the base-model quantization setup).

## 2. Pipeline Architecture (Phases 0-11)

The notebook is structurally divided into 12 distinct phases:

*   **Phase 0**: Environment setup, Colab/Drive authorization, dependencies, and state management.
*   **Phase 1**: Dataset and manifest integrity verification. Enforces strict SHA-256 matching.
*   **Phase 2**: Tesla T4 hardware verification and base-model loading.
*   **Phase 3**: 4-bit NF4 quantization and PEFT/LoRA adapter preparation.
*   **Phase 4**: Forward/backward dry run and gradient/VRAM sanity checks.
*   **Phase 5**: SFT authorization gate.
*   **Phase 6**: Supervised Fine-Tuning (SFT) training execution.
*   **Phase 7**: SFT evaluation preparation, SFT/DPO ID overlap verification, and precise separation of the 10 permanent holdout records.
*   **Phase 8**: DPO authorization gate.
*   **Phase 9**: Direct Preference Optimization (DPO) training initialized from the trained SFT adapter.
*   **Phase 10 & 11**: BASE vs SFT vs DPO evaluation loop and final report generation.

## 3. Training Configurations

### Supervised Fine-Tuning (SFT)
*   **Learning Rate**: `2e-4`
*   **Batch Size**: `1`
*   **Gradient Accumulation Steps**: `16`
*   **Epochs**: `3`
*   **Max Sequence Length**: `4096`
*   **Warmup Ratio**: `0.03`
*   **Scheduler**: Cosine
*   **Weight Decay**: `0.01`
*   **Optimizer**: `paged_adamw_8bit`

### Direct Preference Optimization (DPO)
*   **Learning Rate**: `5e-7`
*   **Batch Size**: `1`
*   **Gradient Accumulation Steps**: `8`
*   **Epochs**: `1`
*   **Max Length**: `2048`
*   *(Note: `max_prompt_length=2048` if present in the final notebook).*
*   **Beta**: `0.1`
*   **Optimizer**: `paged_adamw_8bit`
*   **Precision**: `fp16=False`, `bf16=False`
*   **Gradient Checkpointing**: `True`

## 4. Critical Adapter Lifecycle (Evaluation Requirement)

Because the DPO training process mutates the active SFT adapter (used for DPO initialization), final evaluation must NOT simply re-enable the mutated "default" adapter and call it SFT.

To ensure mathematical correctness and reproducibility, the final evaluation explicitly orchestrates the PEFT adapters:

*   **BASE Evaluation**: All adapters are disabled so the evaluation strictly represents the raw base model.
*   **SFT Evaluation**: The SFT checkpoint is independently loaded from disk into an isolated adapter slot named `sft_eval_adapter`.
*   **DPO Evaluation**: The DPO checkpoint is independently loaded from disk into its own isolated adapter slot named `dpo_adapter`.
