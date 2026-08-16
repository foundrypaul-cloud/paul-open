#!/usr/bin/env python3
"""Training entry point for PAUL Open Model.

Usage:
    uv run python scripts/train.py --model configs/models/gemma4_12b_it.yaml \
                                    --training configs/training/sft_qlora.yaml \
                                    --data configs/data/indic_languages.yaml
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a Gemma 4 model")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--training", required=True, help="Path to training config YAML")
    parser.add_argument("--data", required=True, help="Path to data config YAML")
    parser.add_argument("--output-dir", default="./results", help="Output directory")
    args = parser.parse_args()

    # TODO: Implement training pipeline
    print(f"Model config: {args.model}")
    print(f"Training config: {args.training}")
    print(f"Data config: {args.data}")
    print("Training not yet implemented — scaffold only.")


if __name__ == "__main__":
    main()
