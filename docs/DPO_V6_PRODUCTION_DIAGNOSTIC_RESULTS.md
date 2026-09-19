# PAUL Open — DPO V6 Production and Diagnostic Results

**Date:** 2026-09-19  
**State:** TECHNICALLY VALID DEVELOPMENT CANDIDATE / NOT PROMOTED  
**Reference:** historical PAUL SFT adapter  
**SHAE:** sealed / not started

## Canonical production provenance

DPO V6 Synthetic Corrective completed successfully in GitHub Actions run `35446312134`, job `105905727395`, from source revision `c4c942d3c455c8745d4756ca2a775772b1215a4a`.

The production workflow passed preflight, launched the exact-head Kaggle production kernel, waited for completion, downloaded the private Kaggle output, sanitized it through the repository allowlist, and uploaded aggregate-only public evidence.

Canonical public evidence:

- workflow run: `35446312134`
- public Actions artifact: `10586544611`
- artifact digest: `sha256:78e32163461051ee625ca79aaf99e6b7fefd1884caae89ed9cc41818b76404da`
- permanent sanitized copy: `artifacts/public-evidence/dpo-v6-production.json`
- source revision: `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- base model revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`
- training dataset: `data/train/dpo_v6/synthetic_corrective_v6.jsonl`
- dataset records: 24
- dataset SHA-256: `eca6b25c27f8c03d221854b2e7aee59f5da0e4f128cd2b9605c10453723dc732`

The public artifact contained two identical safetensors digests because the private Kaggle output included both the retained checkpoint adapter and the final adapter. Both hashed to:

`c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`

at 139,602,808 bytes each.

## Training validity

The sanitized training manifest records:

| Field | Result |
|---|---:|
| configured epochs | 4 |
| trainer global step | 8 |
| train loss | 0.646148681640625 |
| train runtime | 308.4718 s |
| intended trainable tensors | 516 |
| changed trainable tensors | 516 |
| finite update evidence | PASS |

This establishes that V6 is a real trained adapter and that all intended trainable LoRA tensors changed during the canonical run.

The `adapter_config_sha256` and `adapter_weights_sha256` fields inside the sanitized training-manifest record identify the frozen SFT source adapter used to initialize DPO. The final V6 adapter identity is the separate safetensors digest above.

## Matched 50-case diagnostic

The production kernel evaluated the historical SFT reference and DPO V6 under the same diagnostic benchmark version.

| Metric | SFT | DPO V6 | Delta |
|---|---:|---:|---:|
| completed cases | 50 / 50 | 50 / 50 | — |
| failed cases | 0 | 0 | — |
| mean heuristic rubric | 89.18 | 90.62 | +1.44 |
| mean keyword coverage | 0.730 | 0.765 | +0.035 |
| automated safety adherence | 100% | 100% | 0 |
| cases flagged for human review | 20 | 19 | -1 |
| mean latency | 37.527 s | 40.109 s | +2.582 s |
| peak VRAM | 2.33 GiB | 2.40 GiB | +0.07 GiB |

The aggregate diagnostic signal is positive for V6 relative to the matched SFT run. It is still a heuristic development signal, not clean proof of general superiority.

## Interpretation boundary

Supported:

- V6 production completed successfully.
- V6 is technically valid under the repository's update-evidence gates.
- In the matched 50-case diagnostic run, V6 had a higher aggregate heuristic score and keyword-coverage score than SFT.
- Automated safety adherence was 100% for both checkpoints in this diagnostic.
- The final V6 adapter weights are cryptographically identified by the public safetensors digest.

Not supported:

- V6 is superior to SFT across PAUL Open's target capability portfolio.
- The 50-case diagnostic is sufficient for promotion.
- V6 has passed independent multi-reviewer human evaluation.
- V6 is assurance-frozen.
- SHAE may be opened or has started.

## Cross-run caution

The SFT aggregate in this V6 diagnostic was 89.18, whereas earlier matched diagnostics recorded different SFT aggregate values. This is a direct reason not to compare headline scores across separately executed runs as if they were one fixed leaderboard.

Development decisions should therefore use matched comparisons, case-level inspection, precommitted fresh prompts, and human review rather than cross-run headline arithmetic.

## Next gate

V6 advances to a fresh, prompt-frozen Development Human Evaluation (H8). H8 is intentionally authored without access to V6 case-level diagnostic responses, hidden mappings, or SHAE material.

The H8 prompt manifest and protocol are frozen separately. V6 remains a development candidate until H8 is completed and analyzed. SFT remains the reference checkpoint.
