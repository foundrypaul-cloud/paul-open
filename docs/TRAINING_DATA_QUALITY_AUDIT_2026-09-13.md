# Training Data Quality Audit — 2026-09-13

Scope: current remote `main` at the start of the audit (`28c3531c037b9788a7ade1a8794db366951284a3`), with frozen historical research preserved unchanged.

This report records defects and existing quality controls. It does not rewrite any dataset that has already been used by a frozen experiment.

## Confirmed SFT semantic mismatches

Two concrete prompt/response mismatches are present in `data/train/sft_train.jsonl`:

1. `paul_sft_soc_v2_001`
   - Prompt: asks why a heavy bowling ball and a light tennis ball fall at the same speed.
   - Response: switches to an unrelated thought experiment about falling through the centre of the Earth.
   - Classification: semantic supervision mismatch; high-confidence data-quality defect.

2. `paul_sft_soc_v2_007`
   - Prompt: asks whether friction is always bad and whether a frictionless world would be better.
   - Response: switches to a vacuum heavy-ball/feather falling example.
   - Classification: semantic supervision mismatch; high-confidence data-quality defect.

Both records are already marked `human_verified: false`, `review_status: pending`, and `approved: false`. Their metadata therefore does not falsely claim human approval, but the records are still poor supervision if included in training.

## Scientific handling

Do **not** edit these records in place if they belong to already executed/frozen training evidence. Historical datasets, hashes, checkpoints, and negative/ambiguous results must remain reproducible.

For any future SFT version:

- create a new versioned dataset rather than modifying the frozen file;
- correct or replace the two affected examples through explicit review;
- mark verification/approval metadata only after actual review;
- record the parent dataset/hash and a machine-readable correction manifest;
- rerun leakage and duplicate checks before training.

## DPO V2–V5 controls

The repository contains progressively stronger corrective-data verification workflows. Current V5 verification requires, among other controls:

- required schema and non-empty prompt/chosen/rejected fields;
- `chosen != rejected`;
- unique IDs, prompts, chosen completions, and rejected completions;
- exact prior-prompt and prior-completion non-reuse checks;
- a token-Jaccard near-duplicate guard against H4/H5/H6 and earlier DPO data;
- a canonical benchmark leakage checker;
- an independent 30-record audit covering preference direction, factuality, language, completeness, and hard-negative quality;
- an exact dataset SHA-256 gate.

Those controls materially reduce duplicate, leakage, malformed-structure, and obvious preference-direction risk. They do not prove that every training example is ideal; semantic review remains required when a defect is found.

## Evaluation-contamination boundary

Development-exposed evaluation (DHE) may be used for development analysis only where the protocol explicitly permits it. SHAE remains sealed assurance material and must not be used to construct corrective training data or failure-analysis examples before legitimate unsealing.

No historical dataset should be silently edited to improve apparent results. New corrective data must preserve an explicit lineage to the failure or development signal it addresses without copying sealed assurance material or private reviewer responses.

## Current disposition

- SFT: **known semantic defects recorded; historical file preserved**.
- DPO V2–V5: **preserve frozen evidence; continue using version-specific structural/leakage/semantic gates**.
- Future SFT: **requires a new reviewed version before relying on the two affected records as supervision**.
