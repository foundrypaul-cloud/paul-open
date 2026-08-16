#!/usr/bin/env python3
"""Interactive chat / inference demo for Gemma 4 models.

Usage:
    uv run python scripts/chat.py --model configs/models/gemma4_12b_it.yaml
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat with a Gemma 4 model")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--checkpoint", default=None, help="Path to adapter checkpoint")
    args = parser.parse_args()

    print(f"Model config: {args.model}")
    print("Chat not yet implemented — scaffold only.")


if __name__ == "__main__":
    main()
