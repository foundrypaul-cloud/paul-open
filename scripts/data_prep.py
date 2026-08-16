#!/usr/bin/env python3
"""Download and preprocess datasets for PAUL Open Model.

Usage:
    uv run python scripts/data_prep.py --config configs/data/indic_languages.yaml
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare training datasets")
    parser.add_argument("--config", required=True, help="Path to data config YAML")
    parser.add_argument("--output-dir", default="./data/processed", help="Output directory")
    args = parser.parse_args()

    print(f"Data config: {args.config}")
    print("Data preparation not yet implemented — scaffold only.")


if __name__ == "__main__":
    main()
