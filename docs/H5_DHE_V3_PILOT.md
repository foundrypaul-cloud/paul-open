# H5 DHE V3 Pilot — Generation and Collection Freeze

**State:** GENERATED_READY_FOR_COLLECTION  
**Partition:** Development Human Evaluation (DHE)  
**Batch:** `HEB1-64CDCC9521D3`  
**Candidate:** DPO V3 Corrective  
**Reference:** SFT  
**SHAE:** sealed / not started

## Generation result

GitHub Actions run `34692176820` completed successfully at source revision
`36b525486dfe8e4cee5785f082186e77efe9d550`.

Reviewer-safe artifact:

- artifact ID: `10297811566`
- name: `h5-dhe-v3-reviewer-safe-bundle`
- digest: `sha256:19ec31d93516f312fa339aa8e1a4e287ef1c4b1c9d36a8a50aff950905423f54`
- six eligible cases
- two complementary blinded variants
- zero identical response pairs skipped

The reviewer-safe artifact contains only the public blinded bundle and safe gate reports. The private
A/B source mapping remains outside the reviewer-safe artifact and is **not authorized for reading before
the blinded analysis lock**.

## Pre-form gates

- paired generation workflow: **PASS**
- blinded batch build: **PASS**
- canonical baseline leakage audit: **PASS (6/6 clean)**
- H4/V3-training development separation: **PASS**
- maximum token-set Jaccard against H4/V3 training: `0.3333333333333333`
- frozen threshold: `< 0.35`

## Frozen initial review allocation

H5 follows the existing protocol: three independent valid judgments per case initially, disagreement or
uncertainty escalation to five, and exceptional hard cap seven.

The initial 18 judgments are counterbalanced at the display-variant level: nine submissions to V01 and
nine to V02. Per case, the initial split alternates between 2/1 and 1/2. Exact packet targets and
comparison IDs are frozen in `data/h5_dhe_v3_pilot_v1_collection_plan.json`.

The Google Forms payload was generated only from the reviewer-safe artifact. Its SHA-256 is
`1e56484d2bb4da1a4a93aeaae2860ca91e04cf775e51f15c7c261fbfa49d37ab`. The response text payload is deliberately **not committed** to the public repository
before collection.

## Interpretation boundary

H5 is fresh DHE for the frozen V3 candidate. It may inform later development and therefore cannot become
sealed assurance evidence. H5 cannot by itself establish broad model superiority or authorize promotion.

No SHAE prompts have been opened or used.
