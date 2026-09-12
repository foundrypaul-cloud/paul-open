# PAUL Open — DPO V5 P10 Corrective Data Audit

**Date:** 2026-09-13  
**State:** P10 PASS  
**Candidate dataset:** DPO V5 corrective, development-only  
**Record count:** 30  
**SHAE:** sealed / not accessed

## Decision

The DPO V5 corrective preference dataset passes the frozen P10 pre-training data gate. Training may proceed only under the unchanged validated DPO methodology and from the frozen SFT reference adapter.

## Frozen identity

Assembled dataset SHA-256:

`1584705bf332137ade1ee24873e5d463653a2b26e26c63f6dc9c87515618bbd4`

Track allocation:

| Track | Records |
|---|---:|
| Conditional physical reasoning | 6 |
| Confounding-aware research reasoning | 6 |
| Instruction-complete Socratic tutoring | 6 |
| Bengali scientific fidelity V5 | 4 |
| Evidence-first uncertainty | 4 |
| Multilingual precision/completion | 4 |
| **Total** | **30** |

## Machine validity and separation

The P10 workflow verified schema completeness, unique IDs/prompts/chosen/rejected completions, exact 30-record allocation, metadata constraints, and the frozen assembled digest.

Exact prompt/completion reuse against H4, H5, H6, DPO V1/V2, and all DPO V3/V4 shards was absent.

The near-duplicate check used the established Unicode tokenizer `unicode_letter_mark_word_v1`: NFKC normalization, casefolding, and contiguous Unicode Letter/Number/Mark tokens. The exclusive Jaccard threshold remained **0.35**.

Maximum prior-data prompt token Jaccard: **0.2857142857142857**.  
Nearest prior source: `data/train/dpo_v4/direct_explanation_multilingual.jsonl` for `paul_dpo_v5_030`.

Result: **PASS**.

## Canonical benchmark leakage

The repository's canonical leakage checker audited all 30 records.

- total audited: **30**
- leakage-free: **30**
- leakage detected: **0**
- clean: **true**
- benchmark version: `1.0.0`

Highest reported benchmark similarity among the 30 records was **0.2513**, still classified clean by the canonical checker.

Result: **PASS**.

## Independent non-human content audit

An independent Gemini CLI review evaluated every record without editing the dataset. For every one of the 30 records it required all of the following to pass:

- chosen response is clearly preferable for the stated prompt and defect;
- factual/scientific/research-methodological correctness;
- natural and intelligible declared-language prose, including Bengali, Hindi and Spanish;
- explicit instruction completion;
- coherent hard-negative quality without accidentally making the rejected answer preferable.

All five booleans were **true for all 30 records** and `overall_pass` was **true**.

Result: **PASS**.

## Development-separation safeguards

The machine audit records:

- `h4_h5_h6_raw_response_text_accessed: false`
- `shae_material_accessed: false`

The dataset was authored from abstracted H6 failure classes rather than the exact H6 examples. H6 remains development-exposed and must not be reused as clean evaluation evidence. SHAE remains sealed.

## Training boundary

P10 approval does not authorize a methodology change. DPO V5 must:

1. start from the same frozen SFT adapter used by the prior corrective runs;
2. preserve the validated dual-T4 policy/reference topology;
3. preserve 4-bit NF4 loading, LoRA contract, optimizer, beta, learning rate, epochs, seed and fail-closed preflight unless separately reviewed;
4. remain a development candidate after training;
5. pass automated diagnostic gates and a fresh non-overlapping DHE before SHAE can be considered.

## Evidence provenance

P10 workflow run: `34723501502`  
Audit artifact: `dpo-v5-p10-audit-evidence` / artifact id `10306554359`  
Artifact digest: `sha256:4c7e84611ea3912c098d16590fc4e1807c60d71131dc2c06707b6e5b41ab892b`

The artifact contains the machine summary, canonical leakage report, and independent audit. No SHAE material is included.
