# DPO V6 Synthetic Corrective Dataset — Development Record

Date: 2026-09-19

## Status

DPO V6 is a synthetic corrective-data development iteration. It is **not** a promoted model and it is **not** human-preference data.

H7 paired generation completed successfully in GitHub Actions run 35437309325 on `main` commit `f702b970a145f407bd5b35d6adbbd3b39a514fe8`. The planned multi-reviewer H7 human evaluation was intentionally not conducted. No H7 blinded response text, hidden candidate/reference mapping, evaluator output, or SHAE material was used to author V6 training examples.

The project owner may act as a single disclosed human evaluator for a later development comparison. Such a review must be reported as **single-evaluator, non-independent development evidence** and must not be described as the precommitted H7 independent-human protocol.

## Dataset

Path: `data/train/dpo_v6/synthetic_corrective_v6.jsonl`

Records: 24.

Each record uses the existing preference schema: `prompt`, `chosen`, `rejected`, `domain`, `language`, `track`, `rejection_reason`, and provenance metadata.

All records are explicitly marked:
- `synthetic: true`
- `human_verified: false`
- `development_only: true`
- `h7_content_used: false`

The dataset targets conditional science reasoning, scientific explanation, research methodology, evidence-first uncertainty, Socratic tutoring, instruction completion, and multilingual precision in English, Hindi, Bengali, and Spanish.

## Boundary rules

1. H7 remains development evaluation material and is not converted into V6 preference labels.
2. SHAE remains sealed.
3. V6 examples must pass repository boundary, schema, contamination, and benchmark-leakage checks before any canonical training run.
4. A future V6 evaluation must use fresh held-out prompts not present in V6 training data.
5. Any owner-only evaluation must disclose the evaluator relationship and cannot be represented as independent or blinded multi-reviewer evidence.

## Decision semantics

This dataset authorizes dataset auditing only. It does not by itself authorize a promotion claim. Training, candidate binding, held-out evaluation, and a documented decision remain separate stages.
