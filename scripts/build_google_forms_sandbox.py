#!/usr/bin/env python3
"""Build short Google Forms sandbox packets from one blinded H1 variant."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paul_open_model.evaluation.human_eval_forms import (
    HumanEvalFormBuildError,
    build_google_form_packets,
    bundle_fingerprint,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert an H1 reviewer-facing variant into short Google Forms sandbox packets. "
            "This command never accepts the private A/B mapping."
        )
    )
    parser.add_argument("--variant", required=True, help="H1 public variant JSON file")
    parser.add_argument(
        "--output-dir",
        default="outputs/human_eval/google_forms_sandbox",
        help="Gitignored sandbox packet directory",
    )
    parser.add_argument(
        "--max-comparisons",
        type=int,
        default=3,
        help="Maximum comparisons per form (default: 3; hard cap: 4)",
    )
    parser.add_argument(
        "--auto-close-after-submissions",
        type=int,
        default=None,
        help="Sandbox-only lifecycle test: close each form after this many submissions",
    )
    return parser


def _load_variant(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise HumanEvalFormBuildError(f"variant file does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HumanEvalFormBuildError(f"invalid variant JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise HumanEvalFormBuildError("variant JSON must contain one object")
    return payload


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _write_apps_script_payload(path: Path, packets: tuple[dict[str, object], ...]) -> None:
    payload = {"packets": packets}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "// Generated sandbox payload. Contains blinded synthetic/reviewer-facing text only.\n"
        f"const PAUL_HUMAN_EVAL_SPEC = {encoded};\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = _parser()
    args = parser.parse_args()

    try:
        variant = _load_variant(Path(args.variant))
        bundle = build_google_form_packets(
            variant,
            max_comparisons=args.max_comparisons,
            environment="sandbox",
            auto_close_after_submissions=args.auto_close_after_submissions,
        )
    except HumanEvalFormBuildError as exc:
        parser.error(str(exc))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "manifest.json", bundle.manifest)
    packet_paths: list[str] = []
    for packet in bundle.packets:
        packet_id = str(packet["packet_id"]).lower()
        path = output_dir / f"{packet_id}.json"
        _write_json(path, packet)
        packet_paths.append(str(path))
    payload_path = output_dir / "Payload.gs"
    _write_apps_script_payload(payload_path, bundle.packets)

    summary = {
        "manifest": str(output_dir / "manifest.json"),
        "packet_paths": packet_paths,
        "apps_script_payload": str(payload_path),
        "packet_count": len(bundle.packets),
        "fingerprint": bundle_fingerprint(bundle),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
