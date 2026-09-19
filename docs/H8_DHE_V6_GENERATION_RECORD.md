# PAUL Open — H8 DHE V6 Generation Record

**Date:** 2026-09-19  
**State:** GENERATED / READY FOR BLINDED COLLECTION  
**Partition:** Development Human Evaluation (DHE)  
**Candidate:** DPO V6 Synthetic Corrective  
**Reference:** SFT  
**SHAE:** sealed / not accessed

## Canonical generation

The canonical H8 paired-generation workflow completed successfully on the frozen H8 prompt set and frozen V6 development candidate.

- GitHub Actions run: `35457211935`
- job: `105934523360`
- source revision: `854fcf8f9e2d0938d177155f10903b6dba144b44`
- V6 adapter SHA-256: `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`
- reviewer-safe artifact: `10588896454`
- artifact digest: `sha256:79f130d0e20fa612540d3787ffbb13d1327860a5ec6a1ccb9247500187271588`
- artifact expiry: `2026-10-19T17:35:32Z`

The workflow recovered the exact frozen V6 adapter from the completed canonical production kernel, verified its SHA-256 digest, staged only that adapter as a private H8 Kaggle input, and then generated matched SFT/V6 responses under the locked H8 generation contract.

## Reviewer-safe batch

The blinded reviewer bundle reports:

- batch: `HEB1-B6BE09E2D6DB`
- 12 eligible cases
- 0 identical response pairs skipped
- 2 complementary counterbalanced variants
- model/checkpoint identity not exposed

The private A/B source mapping is not present in the reviewer-safe artifact and remains non-public.

## Integrity gates

All pre-collection integrity gates passed:

- blinded batch build: **PASS**
- canonical benchmark leakage: **PASS**, 12/12 clean
- development separation: **PASS**
- maximum Unicode token-set Jaccard against H4–H7 and DPO V1–V6 development/training prompts: `0.3235294117647059`
- required exclusive threshold: `< 0.35`

The closest development/training overlap remained below the precommitted boundary. These checks establish evaluation separation; they do not establish model superiority.

## Collection status

Human collection has **not started**.

The initial protocol remains:

- 3 independent valid judgments per case
- 36 initial case-level judgments total
- escalation to 5 judgments for disagreement, tie, not-sure, or material uncertainty
- exceptional hard cap of 7
- primary analysis unit: case, not individual judgment
- source identity remains blinded until the blinded analysis lock is complete

The grouped H8 Google Forms materializer is available in `scripts/materialize_h8_forms_payload.py`.

## Claim boundary

This record supports saying that fresh H8 matched generation completed successfully and passed the precommitted contamination/separation gates.

It does **not** support saying that:

- DPO V6 is superior to SFT;
- DPO V6 passed H8 human evaluation;
- DPO V6 is promoted or assurance-frozen;
- SHAE has started or may be unsealed.

The next gate is blinded multi-reviewer H8 collection and case-level analysis.
