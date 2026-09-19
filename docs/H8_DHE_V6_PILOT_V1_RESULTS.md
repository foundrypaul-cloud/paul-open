# PAUL Open — H8 DHE V6 Pilot V1 — Results

**Date:** 2026-09-20  
**State:** UNBLINDED DEVELOPMENT ANALYSIS COMPLETE  
**Batch:** `HEB1-B6BE09E2D6DB`  
**Candidate:** DPO V6 Synthetic Corrective  
**Reference:** SFT  
**SHAE:** sealed / not accessed  
**Decision:** RETAIN SFT REFERENCE / DO NOT PROMOTE V6

## Controlled unblinding

Controlled unblinding ran only after the blinded analysis lock was merged.

- GitHub Actions run: `35462516736`
- safe artifact: `h8-dhe-unblinded-safe-aggregate`
- artifact ID: `10591050193`
- artifact digest: `sha256:d2b3b31d6334f0bce3eb3f59e292a125dde86f226eb6f830783f1f8deb208222`
- private mapping SHA-256: `00cfd5ce446423a0674314f6f3a7dc2f8cc44d348212e4a8266bab0c0f6a6de9`
- private mapping content exposed publicly: no
- SHAE accessed: no

The safe aggregate is permanently copied to:

`artifacts/public-evidence/h8-dhe-v6-unblinded-aggregate.json`

## Case-level result

The case is the primary unit of analysis.

| Outcome | Cases |
|---|---:|
| V6 preferred | 3 |
| SFT preferred | 6 |
| About equal | 1 |
| Neither good | 2 |
| Not sure | 0 |

The 12 case outcomes were unanimous within the collected 3 judgments per case.

Directional cases only: V6 was preferred on 3 of 9 cases and SFT on 6 of 9. A two-sided exact binomial test against 50/50 gives `p = 0.5078125`; the exact 95% interval for the V6 directional-win fraction is approximately `0.0749–0.7007`. With only nine directional cases, this is not a precise estimate and must not be treated as a statistically definitive superiority test.

## Per-case outcomes

| Case | Domain / language | Outcome |
|---|---|---|
| H8-DHE-001 | science reasoning / English | SFT preferred |
| H8-DHE-002 | science reasoning / English | Neither good |
| H8-DHE-003 | Socratic tutoring / English | V6 preferred |
| H8-DHE-004 | Socratic tutoring / English | Neither good |
| H8-DHE-005 | scientific research assistance / English | SFT preferred |
| H8-DHE-006 | scientific research assistance / English | SFT preferred |
| H8-DHE-007 | scientific explanation / Hindi | SFT preferred |
| H8-DHE-008 | scientific explanation / Bengali | SFT preferred |
| H8-DHE-009 | evidence-first human-centered / Spanish | V6 preferred |
| H8-DHE-010 | multilingual precision / Spanish | V6 preferred |
| H8-DHE-011 | teacher assistance / English | SFT preferred |
| H8-DHE-012 | student assistance / English | About equal |

The pattern is mixed rather than uniformly negative: V6 wins the English Socratic spacecraft case and both Spanish cases, while SFT is preferred on both research-assistance cases, Hindi, Bengali, one science-reasoning case, and teacher assistance. Two cases were judged poor on both sides.

## Raw judgments

Raw judgments are descriptive only because repeated judgments on one case are not independent test examples.

| Outcome | Judgments |
|---|---:|
| V6 preferred | 9 |
| SFT preferred | 18 |
| About equal | 3 |
| Neither good | 6 |
| Not sure | 0 |

## Decision against the precommitted H8 gate

The H8 precommit allowed V6 to advance for assurance-candidate consideration only if the case-level evidence was directionally favorable **and** no material preservation/safety regression was found.

That gate is not met:

- SFT is preferred on twice as many cases as V6, 6 versus 3;
- SFT wins both scientific-research-assistance cases;
- SFT wins both Hindi and Bengali scientific-explanation cases;
- one science-reasoning case and the teacher-assistance case also favor SFT;
- two additional cases are judged poor for both checkpoints.

Therefore:

> **DPO V6 is not promoted. The historical SFT adapter remains the reference checkpoint.**

H8 does not justify opening SHAE for V6. There is no assurance-candidate freeze for V6.

## Reviewer-independence limitation

The H8 Forms intentionally did not collect email or reviewer identity. The stored response set therefore cannot technically prove that separate submissions came from distinct people.

The collection was operator-reported complete and all submitted reviewer-confidence answers were "Yes — confidently", but identity-level independence remains unverified. This limitation prevents H8 from being represented as fully verified independent multi-reviewer evidence.

Importantly, the no-promotion decision does not depend on claiming stronger reviewer independence than the instrument can verify.

## Research interpretation

The positive 50-case automated diagnostic for V6 and the H8 human preference result point in different directions.

This is exactly why PAUL Open separates automated regression signal from behavioral preference evidence: the V6 diagnostic improved from 89.18 to 90.62 relative to matched SFT, yet the fresh H8 case-level human comparison preferred SFT more often.

The appropriate conclusion is not that V6 is universally worse or that the automated evaluation is useless. It is that V6 does not satisfy the project's promotion standard and exposes remaining capability-preservation problems.

## Next allowed development state

- Archive V6 as a valid but non-promoted development checkpoint.
- Keep SFT as the reference checkpoint.
- Keep SHAE sealed.
- Any V7 work must use a new experiment identity and a new precommitted evaluation round.
- H8 outputs and results may inform future corrective-data design because H8 is development evaluation, but they must never be represented as untouched assurance evidence later.
