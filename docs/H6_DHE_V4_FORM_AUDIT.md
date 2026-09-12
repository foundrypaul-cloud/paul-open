# H6 DHE V4 Form Audit — 2026-09-13

**State:** AUDIT_HOLD / REGENERATION_REQUIRED  
**Partition:** Development Human Evaluation (DHE)  
**Candidate:** DPO V4 Corrective  
**Reference:** SFT  
**SHAE:** sealed / not accessed  
**Original reviewer bundle:** `HEB1-10BFFE4FEDE6`

## Executive finding

The first H6 reviewer bundle passed contamination, blinding, counterbalancing, and basic generation gates, but it is **not admissible for human preference collection**. A post-generation form audit found that the 256-token generation ceiling produced reviewer-visible truncation in multiple model outputs, and the direct Google Forms API construction path did not reproduce the H5 durability/normalization/auto-close controls.

The 12 first-pass H6 forms were therefore unpublished and retired from research collection. Any accidental/test submission to those forms is inadmissible and must not enter H6 analysis.

No model training methodology, checkpoint, adapter, prompt set, or source mapping is changed by this audit amendment.

## What passed

- Candidate and reference identities remained hidden from reviewers.
- The reviewer-safe bundle contained six eligible cases and two complementary variants.
- A/B assignment was correctly reversed between V01 and V02 for every case.
- No identical output pair was admitted.
- Canonical baseline leakage passed 6/6 clean.
- Development separation passed with maximum token-set Jaccard `0.34`, below the frozen `<0.35` threshold.
- Reviewer-facing preference choices matched the five-option PAUL protocol.
- Email collection was disabled.
- Evaluation content was presented as selectable text rather than images, improving compatibility with screen readers and browser/device text-to-speech.
- Reviewer cohort prompts were present for STEM, research, Hindi, Bengali and Spanish; educator context remained optional as intended.

## Critical finding 1 — generation truncation

The original frozen H6 generation spec used `max_new_tokens: 256` but had no gate that checked whether generation ended naturally or merely hit the ceiling.

Manual inspection of the reviewer-safe bundle found clear mid-sentence or mid-structure truncation in **9 of 12 unique source responses**:

| H6 stratum | Truncation finding |
|---|---|
| STEM conservation | one of two source responses visibly cut at the display boundary |
| Socratic tutoring | neither response visibly cut by the token ceiling |
| Research methodology | both responses cut mid-structure |
| Hindi scientific explanation | both responses cut mid-sentence |
| Bengali scientific explanation | both responses cut mid-sentence |
| Spanish evidence-first usefulness | both responses cut mid-sentence |

This is a hard validity failure for a pairwise preference study. A reviewer could prefer the response that happened to finish before the ceiling rather than the response that would otherwise be better. The truncation mechanism is external to the intended model-quality comparison.

### Remediation

H6 evaluation config v1.1:

- raises the **matched** ceiling for both checkpoints to `768` new tokens;
- preserves temperature `0.7`, top-p `0.9`, seed `42`, base revision, prompts, adapters and runtime path;
- adds `require_eos_before_limit: true`;
- adds a fail-closed `no_generation_truncation_gate`;
- records generated token count, EOS state and token-limit state per case/source;
- refuses to build reviewer material if any response reaches the configured ceiling without EOS.

## Critical finding 2 — collection durability and stopping controls

The first-pass H6 forms were created directly through the Google Forms API. The reviewer surface was valid, but that route did **not** reproduce the collection controls proven in H5:

- linked Google Sheets response destination;
- form-submit normalization;
- independent backup ledger with digest-bearing snapshots;
- explicit batch/comparison/variant metadata in the collection data model;
- review-count/disagreement monitor;
- automatic close at per-variant target;
- pre-unblinding durability audit.

The PAUL human-evaluation protocol requires those controls before a result can be locked and unblinded. H6 collection must therefore return to the H5-style Forms + Sheets + Apps Script runtime (or an equivalently durable implementation) rather than relying on the first-pass direct forms alone.

## Important finding 3 — reviewer assignment independence

The initial design requires three **independent** valid judgments per case. With complementary A/B variants, the same reviewer should not judge both variants of the same case. Because email collection is intentionally disabled, reviewer assignment must be controlled outside the form or by a pseudonymous assignment token that does not reveal model identity.

For H6 collection:

- distribute only one variant of a given case to any one reviewer;
- do not publish the complete A/B link set as an unrestricted poll;
- retain the 2/1 complementary allocation per case and 9/9 aggregate variant balance;
- escalate 3→5 only under the frozen disagreement/uncertainty rules.

## Important finding 4 — multilingual and accessibility presentation

Text-native presentation is an improvement over image-based response blocks, but the first-pass forms still have two usability issues:

1. generated Markdown markers such as `**`, `###`, and backticks are displayed as literal characters in Google Forms rather than rendered formatting;
2. the preference and reviewer-confidence UI remains English-only on Hindi, Bengali and Spanish forms.

The regenerated form material should:

- strip Markdown formatting markers while preserving response wording and paragraph structure;
- keep `Response A` / `Response B` labels stable for mapping, but provide bilingual/localized question wording for Hindi, Bengali and Spanish reviewers;
- keep all response text selectable and screen-reader accessible;
- avoid image-only text;
- preserve formulas, units and established technical notation as text.

## Protocol-level observations

The following are not blockers on their own, but should be locked before collection:

- Progress bar, response editing, response summary, submit-another-response behavior and confirmation message should be explicitly controlled through the Apps Script runtime rather than left to defaults.
- The protocol recommends sparse quality-control items (~20% of forms). If controls are used in H6, they must be clearly marked non-research internally and excluded from model preference statistics.
- Form IDs, respondent URLs, Sheet IDs and private A/B source mappings remain operational/private data and must not be committed to the public repository.
- A private operational manifest should map `form_id → batch_id → comparison_id → variant_id → target_count` while the public repository retains only non-sensitive batch metadata permitted by policy.

## Retired first-pass form set

The 12 first-pass forms are unpublished and audit-retired. Their identifiers are intentionally omitted from the public repository in accordance with `docs/REVIEWER_IDENTITY_AND_RESPONSE_DURABILITY.md`. They must not be reused for H6 research collection.

## Authorization to resume collection

H6 human collection may resume only when all of the following are true:

1. regenerated SFT and V4 outputs pass the new no-truncation gate;
2. leakage and development-separation gates pass again;
3. a fresh two-variant reviewer bundle is built;
4. form text is checked against the fresh bundle after Markdown sanitation/localization;
5. H5-equivalent response normalization, independent backup, target monitoring and auto-close are active;
6. the private operational form manifest is frozen before links are distributed;
7. source identities remain blinded.

Until then, H6 remains `AUDIT_HOLD` and SHAE remains sealed.
