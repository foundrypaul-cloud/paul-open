# PAUL Open — H6 DHE V4 Pilot V1 — Blinded Analysis Lock

**Date:** 2026-09-13  
**State:** BLINDED_ANALYSIS_LOCKED  
**Batch:** `HEB1-5AE2CE4166CD`  
**Partition:** Development Human Evaluation (DHE)  
**SHAE:** sealed / not accessed

## Collection closure

The frozen initial allocation completed exactly at **18 valid judgments**: three independent judgments per case across six cases, with the complementary display variants balanced at 9 submissions for V01 and 9 for V02.

All twelve H6 forms were closed to further responses immediately after the frozen allocation was confirmed. No additional judgments were collected beyond the initial target.

The frozen adaptive rule did not authorize escalation to five judgments because every case was unanimous at three judgments. There were no tie judgments and no `I'm not sure / I can't judge this` judgments.

For the five strata with a required confidence check (STEM, Research, Hindi, Bengali and Spanish), every submitted judgment selected `Yes — confidently`. The Educator stratum used the protocol's optional teaching/tutoring-context question instead of a confidence gate.

## Durability

The accepted H6 response set reconciles across all three retained collection layers:

- 18 Google Form responses;
- 18 normalized response rows;
- 18 independent backup-ledger rows;
- normalized and backup response-ID sets match packet-by-packet;
- every backup row contains a SHA-256 snapshot digest.

The SHA-256 of the newline-delimited, lexicographically sorted normalized response-ID set (with a trailing newline) is:

`1f4cf378771881833c9d112cff6108fb7eba57c795a84813e1d4a12fcc2cfe14`

Durability status: **PASS**.

## Blinded result

The table below is expressed only in the canonical V01 display orientation. No model/source identity was consulted when this lock was written.

| Case | Canonical V01 judgment | Agreement |
|---|---|---:|
| STEM | Response A preferred | 3/3 |
| Educator | Neither response is good | 3/3 |
| Research | Response A preferred | 3/3 |
| Hindi | Response B preferred | 3/3 |
| Bengali | Response A preferred | 3/3 |
| Spanish | Response B preferred | 3/3 |

All six cases were unanimous at the initial three-judgment stage. Mean modal agreement is therefore 100%, but the Educator result is explicitly a unanimous rejection of both displayed responses rather than a preference for one side.

## Interpretation boundary

H6 is a **development** human-evaluation batch. These results may guide diagnosis and future development, but they are not clean final superiority evidence and must not be relabeled as SHAE.

The unanimous `Neither response is good` Educator result is a substantive development signal and should be preserved as such rather than converted into a forced A/B win.

## Lock rule

This record freezes the blinded H6 result **before** any private A/B source mapping is consulted. Controlled unblinding may proceed only from this locked state. SHAE remains sealed.
