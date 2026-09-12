#!/usr/bin/env python3
"""Generate matched SFT and DPO V4 responses for frozen H6 DHE development cases.

Generation only. This script never trains or modifies either adapter.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import torch
import yaml
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from paul_open_model.evaluation.metrics import check_anti_anthropomorphism, detect_script


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise RuntimeError(f"no records in {path}")
    seen: set[str] = set()
    for row in rows:
        required = {"case_id", "partition", "domain", "language", "reviewer_cohort", "prompt"}
        missing = required - row.keys()
        if missing:
            raise RuntimeError(f"{row.get('case_id', '?')}: missing {sorted(missing)}")
        if row["partition"] != "development":
            raise RuntimeError(f"{row['case_id']}: H6 requires development partition")
        if row["case_id"] in seen:
            raise RuntimeError(f"duplicate case_id: {row['case_id']}")
        seen.add(row["case_id"])
    return rows


def resolve_adapter(path: Path) -> Path:
    candidates = [path, path / "dpo", path / "final-dpo-adapter", path / "final-dpo-adapter" / "dpo"]
    for candidate in candidates:
        if (candidate / "adapter_config.json").is_file() and (candidate / "adapter_model.safetensors").is_file():
            return candidate
    matches = [p.parent for p in path.rglob("adapter_config.json") if (p.parent / "adapter_model.safetensors").is_file()]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one adapter payload below supplied input, found {len(matches)}")
    return matches[0]


def generate_source(
    rows: list[dict[str, Any]],
    *,
    adapter: Path,
    model_id: str,
    revision: str,
    generation: dict[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    quant = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    base = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        device_map={"": 0},
        quantization_config=quant,
    )
    model = PeftModel.from_pretrained(base, adapter, is_trainable=False)
    model.eval()

    records: list[dict[str, Any]] = []
    gate_details: list[dict[str, Any]] = []
    expected_scripts = {"hi": "Devanagari", "bn": "Bengali", "es": "Latin"}
    start = time.time()

    for index, row in enumerate(rows):
        seed = int(generation["random_seed"]) + index
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        messages = [{"role": "user", "content": row["prompt"]}]
        rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(rendered, return_tensors="pt").to(model.device)
        with torch.no_grad():
            generated = model.generate(
                **inputs,
                max_new_tokens=int(generation["max_new_tokens"]),
                do_sample=True,
                temperature=float(generation["temperature"]),
                top_p=float(generation["top_p"]),
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(
            generated[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
        ).strip()
        if not response:
            raise RuntimeError(f"{row['case_id']}: empty generation")
        if "Traceback (most recent call last)" in response:
            raise RuntimeError(f"{row['case_id']}: malformed generation contains traceback")

        safety_clean, _ = check_anti_anthropomorphism(response)
        if not safety_clean:
            raise RuntimeError(f"{row['case_id']}: automated safety gate failed")

        script = detect_script(response)
        expected_script = expected_scripts.get(row["language"])
        if expected_script and script != expected_script:
            raise RuntimeError(
                f"{row['case_id']}: native-script gate failed; expected {expected_script}, got {script}"
            )

        records.append({
            "case_id": row["case_id"],
            "prompt": row["prompt"],
            "response": response,
            "domain": row["domain"],
            "language": row["language"],
            "reviewer_cohort": row["reviewer_cohort"],
        })
        gate_details.append({
            "case_id": row["case_id"],
            "nonempty": True,
            "malformed": False,
            "anti_anthropomorphism_safety": "PASS",
            "detected_script": script,
            "expected_script": expected_script,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    elapsed = time.time() - start

    del model, base, quant
    gc.collect()
    torch.cuda.empty_cache()
    return {
        "records": len(records),
        "elapsed_seconds": elapsed,
        "sha256": sha256(output_path),
        "gates": gate_details,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--training-config", default="configs/training/dpo_v4_e4b_corrective.yaml")
    parser.add_argument("--sft-adapter", required=True)
    parser.add_argument("--dpo-adapter", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    config_path = Path(args.config)
    training_config_path = Path(args.training_config)
    rows = load_jsonl(manifest_path)
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))["h6_dhe_v4_pilot"]
    train_cfg = yaml.safe_load(training_config_path.read_text(encoding="utf-8"))["experiment"]
    if cfg["status"] != "frozen_pre_generation" or cfg["partition"] != "development":
        raise RuntimeError("H6 config is not frozen_pre_generation/development")

    model_id = train_cfg["model_id"]
    revision = train_cfg["model_revision"]
    generation = cfg["generation"]
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sft_path = out / "sft_reference.jsonl"
    dpo_path = out / "dpo_v4_corrective.jsonl"

    sft_adapter = resolve_adapter(Path(args.sft_adapter))
    dpo_adapter = resolve_adapter(Path(args.dpo_adapter))

    sft = generate_source(
        rows,
        adapter=sft_adapter,
        model_id=model_id,
        revision=revision,
        generation=generation,
        output_path=sft_path,
    )
    dpo = generate_source(
        rows,
        adapter=dpo_adapter,
        model_id=model_id,
        revision=revision,
        generation=generation,
        output_path=dpo_path,
    )

    if sft["records"] != len(rows) or dpo["records"] != len(rows):
        raise RuntimeError("generation count mismatch")

    try:
        source_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        source_revision = "unknown"
    manifest = {
        "experiment": "H6_DHE_V4_PILOT_V1",
        "partition": "development",
        "source_revision": source_revision,
        "case_manifest_sha256": sha256(manifest_path),
        "generation_config_sha256": sha256(config_path),
        "model_id": model_id,
        "model_revision": revision,
        "generation": generation,
        "case_count": len(rows),
        "sft": sft,
        "dpo_v4": dpo,
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "gates": {
            "generation_completed": "PASS",
            "nonempty_output": "PASS",
            "automated_safety_gate": "PASS",
            "malformed_output_gate": "PASS",
            "evaluation_partition_integrity": "PASS",
        },
    }
    (out / "generation_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "case_count": len(rows), "output_dir": str(out)}, indent=2))


def _failure_output_dir(argv: list[str]) -> Path | None:
    try:
        idx = argv.index("--output-dir")
        return Path(argv[idx + 1])
    except (ValueError, IndexError):
        return None


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        out = _failure_output_dir(sys.argv)
        if out is not None:
            out.mkdir(parents=True, exist_ok=True)
            message = str(exc)
            for sensitive in ("sft_reference", "dpo_v4_corrective"):
                message = message.replace(sensitive, "checkpoint")
            failure = {
                "status": "FAIL",
                "exception_type": type(exc).__name__,
                "message": message[:1000],
            }
            (out.parent / "failure_summary.json").write_text(
                json.dumps(failure, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        raise
