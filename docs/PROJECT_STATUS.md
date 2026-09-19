# PAUL Open — Current Research Status

**Status date:** 2026-09-19  
**Public research repository:** `foundrypaul-cloud/paul-open`

## Current position

PAUL Open has completed successive development cycles through DPO V4/H6 and has trained and technically validated DPO V5 Corrective. The historical SFT checkpoint remains the reference.

DPO V5 passed the P10 corrective-data audit and P11 production validity gates. P12 automated evidence was mixed: safety and technical gates passed, while the 50-case diagnostic showed both positive signals and regression flags. P12 therefore cleared V5 only for the already-precommitted H7 Development Human Evaluation (DHE), not for promotion.

Six fresh H7 cases were frozen before V5 output inspection and matched generation completed successfully. On 2026-09-19 the planned multi-reviewer H7 human collection was intentionally discontinued to shorten the development loop; therefore H7 has no human preference result and cannot support a V5 promotion claim. A separate DPO V6 synthetic corrective-data iteration has begun without using H7 blinded responses or mappings. SHAE remains sealed and has not started.

## Experiment lineage

- **DPO V2 / H4:** technically valid; H4 mixed; no promotion.
- **DPO V3 / H5:** technically valid; H5 ended 9–9 in judgments and failed the pre-specified STEM/Hindi preservation objective; no promotion.
- **DPO V4 / H6:** H6 collected 18 judgments. SFT was preferred on five cases (15 judgments); all three Educator judgments selected neither response; no promotion.
- **DPO V5 / P10–P12:** 30-record corrective dataset passed P10; production completed with 516/516 intended LoRA tensors changed and completion gate PASS. Automated P12 evidence was mixed and cleared V5 only for H7 DHE.
- **H7:** matched generation completed; planned multi-reviewer human collection intentionally discontinued on 2026-09-19; no H7 human result and no promotion decision.
- **DPO V6:** synthetic corrective-data development iteration initiated with fresh training prompts; not yet trained or promoted.

The immutable Step-2 freeze remains `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`.

## DPO V5 technical evidence

Canonical P11 production evidence records source revision `08a0857bbd5a93d58b8ca64a61625e69f68bf442`, 30 dataset records, four configured epochs, global step 8, final train loss `0.682159423828125`, and 516/516 intended trainable tensors changed.

The P12 matched 50-case automated diagnostic completed without execution failures and with 100% automated safety / anti-anthropomorphism adherence. Its aggregate heuristic signal was lower for V5 than SFT (89.53 vs 90.66), while some domain signals improved and others regressed. These metrics are diagnostic, not a human-preference or superiority result.

See [DPO_V5_P10_AUDIT.md](DPO_V5_P10_AUDIT.md) and [DPO_V5_P11_P12_RESULTS.md](DPO_V5_P11_P12_RESULTS.md).

## Current development gate

H7 remains development evidence, not final assurance. Its matched generation completed, but the precommitted multi-reviewer collection was not completed, so H7 provides no human preference result. Development has moved to the separately documented DPO V6 synthetic corrective-data track. V6 must pass data gates, training validity, and a fresh held-out evaluation before any development decision. Any project-owner-only evaluation must be disclosed as single-evaluator, non-independent evidence. SHAE remains sealed.

## Claim boundary

Supported: DPO V2–V5 are technically valid experimental/development checkpoints; H4–H6 are completed DHE rounds; DPO V5 passed P10/P11 technical and contamination gates; P12 was mixed; H7 matched generation completed but human collection was discontinued without a result; DPO V6 synthetic corrective development has begun; SFT remains the reference; SHAE remains sealed.

Not supported: DPO V5 is superior to SFT; DPO V5 passed H7 human evaluation; DPO V5 is assurance-frozen; DPO V6 has been trained, evaluated, or promoted; SHAE may be opened, has started, or has passed.

## Operational boundary

The 2026-09-13 accidental duplicate V4/V5 Kaggle launches are documented non-canonical operational side effects and must not be substituted for canonical experiment evidence. Research-significant Kaggle production workflows are now manual-dispatch only.

## Public website state

The website is a presentation layer and should consume the machine-readable files under `public/`. No public human-evaluation round is accepting responses. Reviewer links, response sheets, private A/B mappings and SHAE material remain non-public.
