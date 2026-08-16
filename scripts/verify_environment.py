#!/usr/bin/env python3
"""Run environment and hardware verification for PAUL Open Model.

Usage:
    uv run python scripts/verify_environment.py
"""

from paul_open_model.utils.hardware import print_environment_report, verify_environment


def main() -> None:
    report = verify_environment()
    print_environment_report(report)


if __name__ == "__main__":
    main()
