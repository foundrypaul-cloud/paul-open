#!/usr/bin/env python3
"""Fail-closed checks for material that must not cross PAUL Open's public boundary.

The guard intentionally scans only Git-tracked files. It is designed for:
  * local/pre-push use before a same-repository branch becomes public, and
  * CI on pull requests and main.

It complements, but cannot replace, GitHub rulesets/branch protection and secret scanning.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_TEXT_SCAN_BYTES = 10 * 1024 * 1024

FORBIDDEN_EXACT_PATHS = {".env", "kaggle.json", ".kaggle/kaggle.json"}
FORBIDDEN_DIR_SEGMENTS = {
    "private", "sealed", "reviewer-private", "reviewer_private", "kaggle-private",
    "kaggle_private", "credentials", "checkpoints",
}
FORBIDDEN_WEIGHT_SUFFIXES = {".safetensors", ".ckpt", ".pt", ".pth", ".gguf"}

SENSITIVE_NAME_PATTERNS = (
    re.compile(r"(^|[-_.])(raw[-_.]?reviewer|reviewer[-_.]?export)([-_.]|$)", re.I),
    re.compile(r"(^|[-_.])(blind(?:ing)?[-_.]?seed)([-_.]|$)", re.I),
    re.compile(r"(^|[-_.])(?:a[-_.]?b|ab)[-_.]?(?:mapping|map)([-_.]|$)", re.I),
    re.compile(r"(^|[-_.])(?:source|candidate)[-_.]?(?:mapping|map)([-_.]|$)", re.I),
    re.compile(r"(^|[-_.])service[-_.]?account(?:[-_.]|$)", re.I),
    re.compile(r"(^|[-_.])oauth[-_.]?(?:token|credentials)([-_.]|$)", re.I),
)

SECRET_PATTERNS = {
    "Hugging Face access token": re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    "GitHub classic token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    "Kaggle API token": re.compile(r"\bKGAT_[A-Za-z0-9_-]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "PEM private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

PUBLIC_JSON_FORBIDDEN_KEYS = {
    "form_id", "sheet_id", "edit_url", "form_edit_url", "admin_url", "reviewer_email",
    "reviewer_phone", "reviewer_identity", "blinding_seed", "blind_seed", "source_mapping",
    "candidate_mapping", "ab_mapping", "a_b_mapping",
}

UNSAFE_ARTIFACT_PATH_FRAGMENTS = {
    "kaggle-output", "kaggle-v2-output", "kaggle-v3-preflight-output",
    "kaggle-v3-production-output", "kaggle-v4-preflight-output",
    "kaggle-v4-production-output", "kaggle-v5-preflight-output",
    "kaggle-v5-production-output", "production-output", "preflight-output",
    "evaluation-results", "checkpoint", "checkpoints", "adapter_model.safetensors",
    "final-dpo-adapter",
}


def tracked_files() -> list[Path]:
    proc = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
    return [ROOT / p.decode("utf-8") for p in proc.stdout.split(b"\0") if p]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str | None:
    """Best-effort UTF-8 scan for any reasonably sized tracked file.

    Do not rely on filename extensions: credentials commonly live in dotfiles or
    extensionless files such as .npmrc, .pypirc, id_rsa, or netrc-style files.
    """
    try:
        if path.stat().st_size > MAX_TEXT_SCAN_BYTES:
            return None
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192]:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def walk_json_keys(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{prefix}.{key}" if prefix else key
            yield key, here
            yield from walk_json_keys(child, here)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk_json_keys(child, f"{prefix}[{idx}]")


def walk_json_strings(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{prefix}.{key}" if prefix else key
            yield from walk_json_strings(child, here)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk_json_strings(child, f"{prefix}[{idx}]")
    elif isinstance(value, str):
        yield value, prefix


def public_value_issue(value: str) -> str | None:
    lower = value.lower()
    if "docs.google.com/spreadsheets/" in lower:
        return "Google Sheets URLs are private/admin surfaces and must not appear in public manifests"
    if "docs.google.com/forms/" in lower and "/viewform" not in lower:
        return "Google Forms public links must be respondent-facing /viewform URLs only"
    if "script.google.com/home/" in lower or "script.google.com/d/" in lower:
        return "Google Apps Script editor/admin URLs must not appear in public manifests"
    return None


def check_paths(files: list[Path], errors: list[str]) -> None:
    for path in files:
        rp = rel(path)
        lower = rp.lower()
        parts = {p.lower() for p in Path(rp).parts}
        if lower in FORBIDDEN_EXACT_PATHS:
            errors.append(f"{rp}: tracked never-public credential/config path")
        if parts & FORBIDDEN_DIR_SEGMENTS:
            errors.append(f"{rp}: tracked file under a never-public namespace")
        if path.suffix.lower() in FORBIDDEN_WEIGHT_SUFFIXES:
            errors.append(f"{rp}: tracked model/checkpoint weight file")
        if any(pattern.search(path.name.lower()) for pattern in SENSITIVE_NAME_PATTERNS):
            errors.append(f"{rp}: filename resembles private mapping/reviewer/credential material")


def check_secrets(files: list[Path], errors: list[str]) -> None:
    for path in files:
        text = read_text(path)
        if text is None:
            continue
        rp = rel(path)
        if rp == "scripts/check_public_boundary.py":
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{rp}: likely {label}")
        if path.suffix.lower() == ".json":
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, dict) and parsed.get("type") == "service_account":
                errors.append(f"{rp}: Google service-account JSON must never be public")


def check_public_json(files: list[Path], errors: list[str]) -> None:
    for path in files:
        rp = rel(path)
        if not rp.startswith("public/") or path.suffix.lower() != ".json":
            continue
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        for key, where in walk_json_keys(parsed):
            if str(key).lower() in PUBLIC_JSON_FORBIDDEN_KEYS:
                errors.append(f"{rp}: public manifest contains forbidden key {where!r}")
        for value, where in walk_json_strings(parsed):
            issue = public_value_issue(value)
            if issue:
                errors.append(f"{rp}: public manifest value {where!r}: {issue}")


def artifact_blocks(text: str):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "uses:" in line and "actions/upload-artifact@" in line:
            yield i + 1, "\n".join(lines[i : min(i + 18, len(lines))])


def check_workflows(files: list[Path], errors: list[str]) -> None:
    for path in files:
        rp = rel(path)
        if not rp.startswith(".github/workflows/") or path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        if "pull_request_target:" in lower:
            errors.append(f"{rp}: pull_request_target is prohibited without an explicit security exception")
        if re.search(r"(^|\n)\s*set\s+-[a-z]*x[a-z]*\b", text):
            errors.append(f"{rp}: shell xtrace can expose secrets")
        if re.search(r"(^|\n)\s*(?:printenv|env)\s*(?:$|[>|])", text):
            errors.append(f"{rp}: broad environment dump can expose secrets")
        for lineno, block in artifact_blocks(text):
            for path_line in [ln.strip() for ln in block.lower().splitlines() if ln.strip().startswith("path:")]:
                value = path_line.split(":", 1)[1].strip().strip("'\"")
                if value in {".", "./", "${{ github.workspace }}"}:
                    errors.append(f"{rp}:{lineno}: upload-artifact path is the whole workspace")
                if any(fragment in value for fragment in UNSAFE_ARTIFACT_PATH_FRAGMENTS):
                    errors.append(f"{rp}:{lineno}: upload-artifact path appears to be raw/private output ({value})")


def main() -> int:
    files = tracked_files()
    errors: list[str] = []
    check_paths(files, errors)
    check_secrets(files, errors)
    check_public_json(files, errors)
    check_workflows(files, errors)
    if errors:
        print("PUBLIC REPOSITORY SAFETY CHECK: FAIL")
        for error in sorted(set(errors)):
            print(f" - {error}")
        print("\nDo not push or merge. Keep private source material private, then publish only explicitly allowlisted/sanitized evidence.")
        return 1
    print(f"PUBLIC REPOSITORY SAFETY CHECK: PASS ({len(files)} tracked files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
