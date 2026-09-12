#!/usr/bin/env python3
"""DPO V3 candidate wrapper around the validated DPO V2 E4B training implementation.

This file intentionally does not reimplement trainer/model/topology/optimizer logic.
It materializes the P3-audited dataset, installs the new experiment identity into
DPO V2's fail-closed contract, then delegates to scripts.dpo_v2_e4b_train.main().
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import dpo_v2_e4b_train as v2

SHARDS = (
    Path("data/train/dpo_v3/bengali_causal_direction.jsonl"),
    Path("data/train/dpo_v3/grounded_socratic_tutoring.jsonl"),
    Path("data/train/dpo_v3/evidence_before_hypothesis.jsonl"),
    Path("data/train/dpo_v3/stem_causal_clarity.jsonl"),
    Path("data/train/dpo_v3/hindi_science_calibration.jsonl"),
)
DATASET_PATH = Path("data/train/dpo_v3_corrective.jsonl")
DATASET_SHA256 = "5ce4a82f32827a07f339d2b8c437dc4b45ec3f60ac9f5d50f165ea308369c741"
DATASET_RECORDS = 30
CONFIG_PATH = "configs/training/dpo_v3_e4b_corrective.yaml"


def materialize_dataset() -> Path:
    records: list[dict[str, object]] = []
    for shard in SHARDS:
        if not shard.is_file():
            raise FileNotFoundError(f"DPO V3 shard missing: {shard}")
        for line in shard.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    if len(records) != DATASET_RECORDS:
        raise RuntimeError(f"DPO V3 dataset expected {DATASET_RECORDS} records, found {len(records)}")
    payload = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    if digest != DATASET_SHA256:
        raise RuntimeError(f"DPO V3 assembled dataset SHA-256 mismatch: {digest}")
    DATASET_PATH.write_text(payload, encoding="utf-8")
    return DATASET_PATH


def install_v3_contract() -> dict[str, object]:
    contract = copy.deepcopy(v2.LOCKED_EXPERIMENT)
    experiment = contract["experiment"]
    training = contract["training"]
    assert isinstance(experiment, dict) and isinstance(training, dict)
    experiment.update(
        {
            "id": "paul_e4b_dpo_v3_corrective",
            "name": "PAUL Open E4B DPO V3 Corrective",
            "provenance": "POST-H4 P1/P2/P3 DEVELOPMENT CANDIDATE — DPO V2 METHODOLOGY PRESERVED",
            "dataset_path": str(DATASET_PATH),
            "dataset_sha256": DATASET_SHA256,
            "dataset_records": DATASET_RECORDS,
        }
    )
    dpo_config = training["dpo_config"]
    assert isinstance(dpo_config, dict)
    dpo_config["output_dir"] = "./results/dpo_v3_e4b_corrective"
    v2.LOCKED_EXPERIMENT = contract
    return contract


def main() -> None:
    materialize_dataset()
    install_v3_contract()
    if "--config" not in sys.argv:
        sys.argv.extend(["--config", CONFIG_PATH])
    v2.main()


if __name__ == "__main__":
    main()
