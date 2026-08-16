#!/usr/bin/env python3
"""Evaluation entry point for PAUL Open Model.

Usage:
    uv run python scripts/evaluate.py --model configs/models/gemma4_12b_it.yaml \
                                       --eval configs/evaluation/mmlu_science.yaml
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a Gemma 4 model")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--eval", required=True, help="Path to evaluation config YAML")
    parser.add_argument("--checkpoint", default=None, help="Path to adapter checkpoint")
    args = parser.parse_args()

    print(f"Model config: {args.model}")
    print(f"Eval config: {args.eval}")
    print("Evaluation not yet implemented — scaffold only.")


if __name__ == "__main__":
    main()
