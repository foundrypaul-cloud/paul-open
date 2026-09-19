#!/usr/bin/env python3
"""DPO V6 wrapper around the validated DPO V2/V5 E4B implementation."""
from __future__ import annotations
import copy, json, subprocess, sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import dpo_v2_e4b_train as v2

DATASET_PATH=Path("data/train/dpo_v6/synthetic_corrective_v6.jsonl")
DATASET_GIT_BLOB_SHA="0dba7994d7de0fc80e2778e053648ab124545074"
DATASET_RECORDS=24
DATASET_SHA256="eca6b25c27f8c03d221854b2e7aee59f5da0e4f128cd2b9605c10453723dc732"
CONFIG_PATH="configs/training/dpo_v6_e4b_synthetic_corrective.yaml"

def validate_dataset() -> None:
    if not DATASET_PATH.is_file(): raise FileNotFoundError(DATASET_PATH)
    blob=subprocess.check_output(["git","hash-object",str(DATASET_PATH)],text=True).strip()
    if blob != DATASET_GIT_BLOB_SHA: raise RuntimeError(f"V6 dataset blob mismatch: {blob}")
    rows=[json.loads(x) for x in DATASET_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows)!=DATASET_RECORDS: raise RuntimeError(f"V6 expected {DATASET_RECORDS} records, found {len(rows)}")
    for r in rows:
        if not (r["prompt"].strip() and r["chosen"].strip() and r["rejected"].strip()): raise RuntimeError(f"empty V6 field: {r.get('id')}")
        if r["chosen"]==r["rejected"]: raise RuntimeError(f"identical preference pair: {r.get('id')}")
        m=r.get("metadata",{})
        if not (m.get("synthetic") is True and m.get("development_only") is True and m.get("human_verified") is False and m.get("h7_content_used") is False):
            raise RuntimeError(f"V6 provenance boundary failed: {r.get('id')}")

def install_contract():
    contract=copy.deepcopy(v2.LOCKED_EXPERIMENT)
    e=contract["experiment"]; t=contract["training"]
    e.update({"id":"paul_e4b_dpo_v6_synthetic_corrective","name":"PAUL Open E4B DPO V6 Synthetic Corrective","provenance":"POST-H7 ABBREVIATED DEVELOPMENT — SYNTHETIC CORRECTIVE DATA; V5 TRAINING METHODOLOGY PRESERVED","dataset_path":str(DATASET_PATH),"dataset_sha256":DATASET_SHA256,"dataset_records":DATASET_RECORDS})
    t["dpo_config"]["output_dir"]="./results/dpo_v6_synthetic_corrective"
    v2.LOCKED_EXPERIMENT=contract

def main():
    validate_dataset(); install_contract()
    if "--config" not in sys.argv: sys.argv.extend(["--config",CONFIG_PATH])
    v2.main()
if __name__=="__main__": main()
