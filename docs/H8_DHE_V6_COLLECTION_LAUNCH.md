# PAUL Open — H8 DHE V6 Collection Launch Record

**Date:** 2026-09-19  
**State:** BLINDED COLLECTION OPEN / RESULT NOT RECORDED  
**Partition:** Development Human Evaluation (DHE)  
**Batch:** `HEB1-B6BE09E2D6DB`  
**Candidate:** DPO V6 Synthetic Corrective  
**Reference:** SFT  
**SHAE:** sealed / not accessed

## Launch basis

H8 matched generation completed successfully before collection opened. The canonical reviewer-safe bundle is bound to:

- generation run: `35457211935`
- generation job: `105934523360`
- reviewer-safe artifact: `10588896454`
- artifact digest: `sha256:79f130d0e20fa612540d3787ffbb13d1327860a5ec6a1ccb9247500187271588`
- batch: `HEB1-B6BE09E2D6DB`
- eligible cases: 12
- identical pairs skipped: 0
- canonical benchmark leakage: PASS, 12/12 clean
- development separation: PASS
- max Unicode token-set Jaccard: `0.3235294117647059 < 0.35`

See `docs/H8_DHE_V6_GENERATION_RECORD.md`.

## Collection surface

Private Google Forms respondent surfaces were provisioned from the canonical reviewer-safe variants.

Operational constraints:

- respondent URLs are private and are not committed to the public repository;
- editor/admin URLs and form IDs are not committed;
- email collection is disabled;
- source/model identity is not displayed;
- the private A/B mapping is not available to reviewers;
- complementary variants of the same cases must not be shown to the same reviewer;
- bilingual cases require reviewers competent in the requested language;
- collection remains development research, not SHAE.

A private collection-control spreadsheet is maintained outside the public repository for reviewer allocation and response-count tracking.

## Initial allocation

The frozen H8 protocol remains unchanged:

- 3 independent valid judgments per case;
- 12 cases;
- 36 initial case-level judgments;
- disagreement, tie, not-sure, or material uncertainty may escalate a case to 5 judgments;
- exceptional hard cap: 7 judgments per case;
- the case is the primary analysis unit.

The display variants remain complementary and counterbalanced.

## Analysis boundary

No H8 preference result exists at collection launch.

Before source identity can be consulted:

1. close the relevant forms after the frozen allocation target is satisfied;
2. export/snapshot accepted responses and preserve response provenance;
3. verify collection integrity and reviewer-competence exclusions;
4. freeze the blinded case-level analysis dataset;
5. commit the blinded analysis lock;
6. only then use the private A/B mapping for controlled unblinding.

## Claim boundary

Supported:

- H8 matched generation completed;
- H8 contamination/separation gates passed;
- the blinded reviewer batch was provisioned for private collection;
- H8 collection is open to recruited reviewers.

Not supported:

- H8 human evaluation is complete;
- DPO V6 is preferred to SFT;
- DPO V6 is broadly superior to SFT;
- DPO V6 is assurance-frozen or promoted;
- SHAE has started or may be opened.

SHAE remains sealed.
