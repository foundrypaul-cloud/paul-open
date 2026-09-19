# PAUL Open — H8 DHE V6 Pilot V1 — Blinded Analysis Lock

**Date:** 2026-09-20  
**State:** BLINDED_ANALYSIS_LOCKED  
**Batch:** `HEB1-B6BE09E2D6DB`  
**Partition:** Development Human Evaluation (DHE)  
**SHAE:** sealed / not accessed

## Collection closure

The H8 collection surfaces are closed. The frozen response set contains:

- 12 cases;
- 36 case-level judgments;
- 18 Form submissions;
- 18 canonical V01-side judgments and 18 complementary V02-side judgments;
- 3 judgments per case;
- 12/12 cases with 3-of-3 agreement;
- 0 not-sure judgments;
- 0 required-confidence failures.

No adaptive escalation is required because every case reached unanimous 3-of-3 agreement. Unanimous `NEITHER` and `EQUAL` outcomes are retained as resolved case outcomes rather than converted into a forced model preference.

## Blinded case-level result

Before source identity is consulted:

| Case | Canonical blinded outcome | Agreement |
|---|---|---:|
| H8-DHE-001 | B | 3/3 |
| H8-DHE-002 | Neither | 3/3 |
| H8-DHE-003 | B | 3/3 |
| H8-DHE-004 | Neither | 3/3 |
| H8-DHE-005 | A | 3/3 |
| H8-DHE-006 | A | 3/3 |
| H8-DHE-007 | B | 3/3 |
| H8-DHE-008 | A | 3/3 |
| H8-DHE-009 | A | 3/3 |
| H8-DHE-010 | A | 3/3 |
| H8-DHE-011 | B | 3/3 |
| H8-DHE-012 | About equal | 3/3 |

Blinded summary: canonical A preferred on 5 cases, canonical B on 4, neither good on 2, and about equal on 1.

The A/B labels above are **not model identities**. They are normalized display sides only.

## Durability

The raw Forms response set was snapshotted after closure into a private Drive spreadsheet. The private normalized snapshot contains 36 rows and has aggregate SHA-256:

`132b4ba6fb7107c6f592c456601cc5598dff681b668f13beccac1107b191eed7`

Raw response IDs, Form IDs, respondent links, optional comments, and private collection-control metadata are not committed to the public repository.

The collection surfaces were created through the Forms connector rather than the older Apps Script normalized-plus-backup-ledger runtime. Therefore H8 has a private post-closure durability snapshot, but it does not claim the earlier dual-ledger checksum path.

## Reviewer-independence limitation

Email and reviewer identity collection were intentionally disabled. The instrument therefore cannot technically prove that separate submissions came from distinct people.

The collection is operator-reported complete, but this lock **does not claim identity-level reviewer independence is instrument-verified**. This limitation must remain attached to the H8 interpretation and prevents overstating H8 as strong independent multi-reviewer evidence without an external allocation/attestation record.

## Frozen analysis contract

After controlled unblinding, report:

- case-level V6-preferred / SFT-preferred / equal / neither-good counts;
- raw judgment totals as descriptive evidence only;
- domain/language outcomes;
- critical factual, native-script, instruction-following, or safety failures separately;
- small-sample uncertainty explicitly.

The case remains the primary analysis unit.

No post-unblind case exclusion, outcome recoding, prompt revision, or checkpoint substitution is permitted except correction of a separately documented data-integrity error.

## Next state

The next allowed step is controlled unblinding against the private H8 A/B mapping. Only a safe aggregate may cross the public repository boundary.

SHAE remains sealed and cannot be opened merely because H8 collection is complete.
