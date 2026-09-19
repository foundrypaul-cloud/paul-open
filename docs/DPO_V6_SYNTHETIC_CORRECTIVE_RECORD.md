# DPO V6 Synthetic Corrective — Development Record

Date: 2026-09-19

## Status

DPO V6 is a synthetic corrective-data development iteration. It is **not** a promoted model and it is **not** human-preference training data.

H7 paired generation completed successfully in GitHub Actions run `35437309325` on `main` commit `f702b970a145f407bd5b35d6adbbd3b39a514fe8`. The planned multi-reviewer H7 human evaluation was intentionally not conducted. No H7 blinded response text, hidden candidate/reference mapping, evaluator output, or SHAE material was used to author V6 training examples.

The project owner may act as a single disclosed human evaluator for a development comparison, but such review must be reported as **single-evaluator, non-independent development evidence** and cannot be represented as the precommitted independent-human protocol.

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

Dataset SHA-256:

`eca6b25c27f8c03d221854b2e7aee59f5da0e4f128cd2b9605c10453723dc732`

## Canonical production result

Canonical DPO V6 production completed successfully on 2026-09-19.

- source revision: `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- GitHub Actions run: `35446312134`
- job: `105905727395`
- configured epochs: 4
- global step: 8
- train loss: `0.646148681640625`
- intended trainable tensors changed: 516 / 516
- finite update evidence: PASS
- final adapter safetensors SHA-256: `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`

The matched 50-case production diagnostic completed without execution failures:

- V6 mean heuristic rubric: **90.62**
- SFT mean heuristic rubric: **89.18**
- V6 keyword coverage: **0.765**
- SFT keyword coverage: **0.730**
- automated safety adherence: **100% for both**

This is a positive development diagnostic signal. It is not a promotion or superiority result.

See `docs/DPO_V6_PRODUCTION_DIAGNOSTIC_RESULTS.md` and the permanent sanitized record at `artifacts/public-evidence/dpo-v6-production.json`.

## Boundary rules

1. H7 remains development evaluation material and is not converted into V6 preference labels.
2. SHAE remains sealed.
3. V6 training identity is fixed by the canonical source revision, dataset digest, production run, and final adapter digest.
4. Fresh V6 evaluation must use prompts absent from V6 and prior training/development data.
5. Any owner-only evaluation must disclose the evaluator relationship and cannot be represented as independent or blinded multi-reviewer evidence.
6. A later training iteration must receive a new experiment identity; it cannot replace the frozen V6 candidate inside H8.

## Next evaluation

V6 is development-frozen for H8 DHE.

H8 contains 12 fresh development prompts authored before any H8 response generation or inspection. Its precommit specification is `docs/H8_DHE_V6_PRECOMMIT_SPEC.md`.

H8 generation and human collection have not started.

## Decision semantics

Training validity, diagnostic evidence, fresh held-out development evaluation, candidate promotion, and sealed assurance remain separate stages.

Current decision:

> **Advance DPO V6 to H8 fresh development evaluation; do not promote and do not open SHAE.**
