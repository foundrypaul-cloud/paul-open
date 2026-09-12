# H4 DHE Pilot V1 — Analysis Lock

**State:** ANALYSIS_LOCKED  
**Partition:** development (DHE)  
**Batch:** `HEB1-E928B35C90D7`  
**Lock time:** 2026-09-12 08:14 UTC  
**Unblinded at lock:** no

## Lock boundary

This document freezes the H4 human-evaluation judgment set before the private A/B source mapping is read for analysis. No candidate/reference interpretation was used to decide which judgments to retain.

All **21 accepted judgments** are included. No post-unblind exclusion changes are permitted for this H4 analysis except correction of a demonstrable data-integrity error, which must be separately documented rather than silently changing the lock.

The machine-readable blinded snapshot is `data/h4_dhe_pilot_v1_blinded_analysis_lock.json`.

## Collection size

- eligible cases: 5
- reviewer-facing complementary variants: 10
- initial judgments: 15
- adaptive follow-up judgments: 6
- final judgments: **21**
- General: 3
- STEM: 5
- Educator: 5
- Hindi: 3
- Bengali: 5

The adaptive allocation followed the frozen 3 → 5 policy. The exceptional seven-judgment cap was not required before this lock.

## Durability audit

The live Google Forms response system was audited immediately before lock.

Across all ten H4 variants:

- native raw response rows: **21**
- `PAUL Normalized` response IDs: **21**
- independent `PAUL Backup Ledger` response IDs: **21**
- normalized and backup response IDs: exact match
- backup SHA-256: present for every response
- backup-written timestamp: present for every response

Result: **PASS**.

No manual spreadsheet editing was used to repair or reinterpret the judgment set.

## Frozen blinded observations

These are raw reviewer-facing A/B labels only. Because complementary variants counterbalance the response positions, these numbers **must not** be interpreted as SFT-vs-DPO outcomes before unblinding.

| Variant | n | A better | B better | Equal | Neither | Not sure |
|---|---:|---:|---:|---:|---:|---:|
| GENERAL-A | 2 | 2 | 0 | 0 | 0 | 0 |
| GENERAL-B | 1 | 0 | 1 | 0 | 0 | 0 |
| STEM-A | 2 | 0 | 1 | 0 | 0 | 1 |
| STEM-B | 3 | 3 | 0 | 0 | 0 | 0 |
| EDUCATOR-A | 3 | 2 | 0 | 0 | 0 | 1 |
| EDUCATOR-B | 2 | 0 | 1 | 1 | 0 | 0 |
| HI-A | 1 | 1 | 0 | 0 | 0 | 0 |
| HI-B | 2 | 0 | 2 | 0 | 0 | 0 |
| BN-A | 2 | 0 | 1 | 1 | 0 | 0 |
| BN-B | 3 | 2 | 0 | 0 | 0 | 1 |
| **Total** | **21** | **10** | **6** | **2** | **0** | **3** |

## Frozen analysis contract

The post-unblind analysis must retain the protocol already declared in `configs/evaluation/human_eval_v1.yaml`:

- report candidate preferred;
- report reference preferred;
- report about equal;
- report neither good;
- report not sure;
- report inter-rater agreement;
- stratify by domain, language, and reviewer cohort where the small sample permits;
- use bootstrap confidence intervals where appropriate;
- do not use Bradley-Terry for this two-model comparison;
- exclude any declared control items from model win-rate calculations;
- do not turn this small DHE pilot into an overall model-superiority claim.

## Accessibility finding

The multilingual text-to-speech/accessibility suggestion collected during Hindi evaluation is retained as a future evaluator-interface finding. It does not change the H4 judgment set or analysis contract.

## Next step

The next allowed state is **UNBLINDED**: read the private gitignored A/B mapping, map each frozen judgment to SFT reference versus DPO V2 Corrective, calculate the frozen metrics, and then record the H4 development-evaluation decision.

SHAE remains sealed and is not part of this transition.
