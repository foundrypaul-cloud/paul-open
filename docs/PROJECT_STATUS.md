# PAUL Open — Current Research Status

**Status date:** 2026-09-18  
**Public research repository:** `foundrypaul-cloud/paul-open`

## Current position

PAUL Open has completed successive development cycles through DPO V4/H6 and has trained and technically validated DPO V5 Corrective. The historical SFT checkpoint remains the reference.

DPO V5 passed the P10 corrective-data audit and P11 production validity gates. P12 automated evidence was mixed: safety and technical gates passed, while the 50-case diagnostic showed both positive signals and regression flags. P12 therefore cleared V5 only for the already-precommitted H7 Development Human Evaluation (DHE), not for promotion.

Six fresh H7 cases were frozen before V5 output inspection. The repository contains H7 generation, verification, candidate-binding and Forms-materialization machinery, but no completed H7 human-evaluation result is currently recorded. SHAE remains sealed and has not started.

## Experiment lineage

- **DPO V2 / H4:** technically valid; H4 mixed; no promotion.
- **DPO V3 / H5:** technically valid; H5 ended 9–9 in judgments and failed the pre-specified STEM/Hindi preservation objective; no promotion.
- **DPO V4 / H6:** H6 collected 18 judgments. SFT was preferred on five cases (15 judgments); all three Educator judgments selected neither response; no promotion.
- **DPO V5 / P10–P12:** 30-record corrective dataset passed P10; production completed with 516/516 intended LoRA tensors changed and completion gate PASS. Automated P12 evidence was mixed and cleared V5 only for H7 DHE.
- **H7:** six fresh development prompts precommitted before V5 output inspection; human evaluation remains the next required gate.

The immutable Step-2 freeze remains `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`.

## DPO V5 technical evidence

Canonical P11 production evidence records source revision `08a0857bbd5a93d58b8ca64a61625e69f68bf442`, 30 dataset records, four configured epochs, global step 8, final train loss `0.682159423828125`, and 516/516 intended trainable tensors changed.

The P12 matched 50-case automated diagnostic completed without execution failures and with 100% automated safety / anti-anthropomorphism adherence. Its aggregate heuristic signal was lower for V5 than SFT (89.53 vs 90.66), while some domain signals improved and others regressed. These metrics are diagnostic, not a human-preference or superiority result.

See [DPO_V5_P10_AUDIT.md](DPO_V5_P10_AUDIT.md) and [DPO_V5_P11_P12_RESULTS.md](DPO_V5_P11_P12_RESULTS.md).

## H7 next gate

H7 is development evidence, not final assurance. Its six prompts were frozen before V5 output inspection under [H7_DHE_V5_PRECOMMIT_SPEC.md](H7_DHE_V5_PRECOMMIT_SPEC.md). The required sequence is matched SFT/V5 generation, hard-gate verification, blinded collection, durability audit, blinded analysis lock, controlled unblinding, and a recorded development decision. No promotion claim is permitted before those steps are evidenced.

## Claim boundary

Supported: DPO V2–V5 are technically valid experimental/development checkpoints; H4–H6 are completed DHE rounds; DPO V5 passed P10/P11 technical and contamination gates; P12 is mixed and cleared V5 only for H7; SFT remains the reference; H7 is the next development gate; SHAE remains sealed.

Not supported: DPO V5 is superior to SFT; DPO V5 has passed human evaluation; DPO V5 is assurance-frozen; H7 is complete; SHAE may be opened, has started, or has passed.

## Operational boundary

The 2026-09-13 accidental duplicate V4/V5 Kaggle launches are documented non-canonical operational side effects and must not be substituted for canonical experiment evidence. Research-significant Kaggle production workflows are now manual-dispatch only.

## Public website state

The website is a presentation layer and should consume the machine-readable files under `public/`. No public human-evaluation round is accepting responses. Reviewer links, response sheets, private A/B mappings and SHAE material remain non-public.
