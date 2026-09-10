# PAUL Open H4 DHE Pilot v1 — Contamination Audit

**Audit date:** 2026-09-11  
**Partition:** development (DHE)  
**Case manifest:** `data/h4_dhe_pilot_v1.jsonl`  
**Status:** pre-generation screen passed; automated benchmark leakage check still required in execution environment before Forms generation.

## Scope

This audit screens candidate H4 prompts against PAUL Open's public repository before model generation. It is intentionally conservative: a candidate is rejected when a materially similar training/evaluation concept is found, even if the wording is not identical.

Repositories/material explicitly treated as contamination sources include:

- `data/train/sft_train.jsonl`
- `data/train/dpo_train.jsonl`
- `data/train/dpo_v2_corrective.jsonl`
- the canonical 50-case baseline/evaluation material
- H3 disposable pilot material
- documented DPO holdout material
- any other development/evaluation content discoverable in the repository

SHAE material is outside the public repository and was not inspected or exposed for this audit.

## Screening method

For every candidate, distinctive wording and the underlying task concept were searched across `foundrypaul-cloud/paul-open`. Exact/no-hit search is not treated as sufficient by itself; broader concept searches were also used where overlap risk was plausible.

Before H4 collection, the execution environment must additionally run the repository's existing leakage checker against the frozen manifest and preserve the report alongside generation provenance.

## Rejected candidate

An initial Socratic candidate based on the misconception that summer occurs because Earth is closer to the Sun was **rejected**. Broader repository search found the same misconception in SFT Socratic training material (`paul_sft_soc_v2_029`). It was removed before the H4 manifest was frozen.

This rejection is evidence that the screen is being used as a gate rather than as documentation after the fact.

## Frozen accepted cases

### H4-DHE-001 — pressure/temperature reasoning

A capped flexible bottle dents inward after warm enclosed air cools.

Repository searches for the bottle/cooling/pressure concept returned no matching PAUL Open material.

### H4-DHE-002 — Socratic dissolution/mass misconception

A student believes dissolved salt disappears and therefore lowers total mass.

Repository searches for salt/dissolution/mass/Socratic overlap returned no matching PAUL Open material.

### H4-DHE-003 — research troubleshooting/outlier handling

A six-reading lab measurement contains one unusually large value; the assistant must propose a principled troubleshooting path rather than delete the observation.

Repository searches for the distinctive graph/readings/troubleshooting concept returned no matching PAUL Open material.

### H4-DHE-004 — Hindi lithium-ion charging explanation

Explain the practical rationale and limits of the 20–80% battery-charging heuristic in natural Hindi.

Repository searches for the lithium-ion/20–80/Hindi concept returned no matching PAUL Open material.

### H4-DHE-005 — Bengali pressure-cooker explanation

Explain pressure, boiling point and cooking temperature in Bengali for a higher-secondary learner.

Repository searches for pressure-cooker/boiling-point/Bengali overlap returned no matching PAUL Open material.

### H4-DHE-006 — human-centered research setback

A user has had three failed experiment attempts and must give an honest supervisor update the next day.

Repository searches for the failed-experiment/presentation/overwhelm concept returned no matching PAUL Open material.

## Important limits

A repository search cannot prove universal non-exposure. The conclusion is narrower: no matching or materially overlapping PAUL Open repository material was found for the six frozen cases during the pre-generation screen, while one overlapping candidate was detected and rejected.

These cases are explicitly **development-exposed** from the moment they are committed. They must never be reclassified as sealed-assurance (SHAE) material.

## Required execution-time checks

Before reviewer Forms are generated:

1. run `scripts/check_leakage.py data/h4_dhe_pilot_v1.jsonl` against the canonical baseline suite;
2. preserve the machine-readable leakage report;
3. confirm all six paired generations are complete and non-empty;
4. reject malformed or safety-gate failures before human-batch construction;
5. ensure SFT and DPO V2 prompts/metadata match case-for-case;
6. build with `scripts/build_human_eval_batch.py --partition development`;
7. keep the source-identity mapping outside reviewer-facing artifacts.

A failed contamination check blocks H4 collection; it is not a warning-only condition.
