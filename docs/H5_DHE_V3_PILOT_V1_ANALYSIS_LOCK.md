# PAUL Open — H5 DHE V3 Pilot V1 — Blinded Analysis Lock

**Date:** 2026-09-12  
**State:** BLINDED_ANALYSIS_LOCKED  
**Batch:** `HEB1-64CDCC9521D3`

## Collection closure

The frozen initial allocation was completed exactly at 18 valid judgments: three per case across six cases, balanced across the complementary blinded variants. No case produced conflicting judgments, a tie, or a not-sure vote, so the frozen adaptive rule did not authorize escalation to five judgments.

All twelve H5 forms were then closed to further responses.

## Durability

The accepted response set reconciles across the three retained layers:

- 18 Form responses;
- 18 normalized rows;
- 18 independent backup-ledger rows;
- normalized and backup response-ID sets match exactly;
- every backup row contains a SHA-256 snapshot digest.

The SHA-256 of the newline-delimited sorted response-ID set is:

`20d1f8fc33eb52d6782ab562d4468ea68b57e6fc4d0fdac79e13012f2850b7fb`

Durability status: **PASS**.

## Blinded result

After normalizing the complementary display swaps, all six cases were unanimous (3/3) for one underlying response. Model/source identity was not used.

| Case | Canonical V01 side preferred | Agreement |
|---|---|---:|
| STEM | B | 3/3 |
| Educator | A | 3/3 |
| Research | B | 3/3 |
| Hindi | A | 3/3 |
| Bengali | A | 3/3 |
| General | A | 3/3 |

Mean modal agreement is 100%. There were zero tie judgments and zero not-sure judgments.

## Lock rule

This record freezes the blinded H5 analysis before any private A/B source mapping is consulted. Controlled unblinding may proceed only from this locked state. SHAE remains sealed.
