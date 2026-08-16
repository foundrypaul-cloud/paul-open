#!/usr/bin/env python3
"""Export (merge + push) a fine-tuned Gemma 4 model to HuggingFace Hub.

Usage:
    uv run python scripts/export_model.py --model configs/models/gemma4_12b_it.yaml \
                                           --checkpoint ./results/checkpoint-1000 \
                                           --push
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Export model to HF Hub")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--checkpoint", required=True, help="Path to adapter checkpoint")
    parser.add_argument("--push", action="store_true", help="Push to HuggingFace Hub")
    parser.add_argument(
        "--hf-namespace",
        default=None,
        help="HF namespace (default: from HF_NAMESPACE env var)",
    )
    args = parser.parse_args()

    print(f"Model config: {args.model}")
    print(f"Checkpoint: {args.checkpoint}")
    print(f"Push: {args.push}")
    print("Export not yet implemented — scaffold only.")


if __name__ == "__main__":
    main()
