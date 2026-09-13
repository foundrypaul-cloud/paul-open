# PAUL Open — H7 DHE V5 Precommit Specification

**Date:** 2026-09-13  
**State:** PROMPT-ONLY PRECOMMIT / CANDIDATE NOT YET BOUND  
**Partition:** development  
**Cases:** 6  
**SHAE:** sealed / not accessed

## Purpose

Freeze the next development human-evaluation prompts before DPO V5 production outputs are inspected. This prevents post-hoc prompt selection based on candidate behavior and keeps H7 independent of the results it will later measure.

The case manifest is `data/h7_dhe_v5_pilot_v1.jsonl`.

## Case allocation

H7 preserves the six-case capability structure used for the prior development rounds while using fresh concepts and wording:

| Case | Domain | Language | Reviewer cohort |
|---|---|---|---|
| H7-DHE-001 | science_reasoning | en | stem_capable |
| H7-DHE-002 | socratic_tutoring | en | educator |
| H7-DHE-003 | scientific_research_assistance | en | domain_expert |
| H7-DHE-004 | scientific_explanation | hi | bilingual |
| H7-DHE-005 | scientific_explanation | bn | bilingual |
| H7-DHE-006 | evidence_first_human_centered | es | bilingual |

All cases are development-exposed. H7 is not final assurance evidence.

## Prompt-freeze gates

Before the manifest can be used for generation, CI must verify:

1. exactly six unique case IDs and prompts with the frozen allocation above;
2. all cases are marked `partition: development` and `development_exposed: true`;
3. no exact prompt reuse from H4, H5, H6, or DPO V1–V5 training data;
4. Unicode-aware token-set Jaccard separation remains strictly below `0.35` against all of those development/training prompts;
5. the repository canonical benchmark leakage checker reports clean.

The separation tokenizer is the established `unicode_letter_mark_word_v1` contract: NFKC normalization, casefolding, and contiguous Unicode Letter/Number/Mark tokens.

## Candidate binding boundary

This precommit does **not** contain DPO V5 adapter hashes, production artifact IDs, or generated model responses. Those fields may be added only after the already-launched V5 production run completes and its adapter is recovered and hashed.

When candidate binding occurs, H7 generation must reuse the H6 v1.2 response-length/truncation safeguards and matched generation settings unless a separately reviewed evaluation-methodology change is proposed.

## Review protocol

The intended human-review protocol remains:

- 3 independent valid judgments per case initially;
- disagreement, tie, not-sure, or material uncertainty may escalate to 5;
- exceptional hard cap 7;
- the same reviewer must not see complementary A/B variants of the same case;
- source/model identity and private mapping remain hidden from reviewers;
- unblinding occurs only after the blinded analysis and durability lock.

## Prohibitions

H7 must not:

- reuse H4, H5, or H6 evaluation prompts;
- reuse DPO V1–V5 training prompts;
- use H4/H5/H6 model response text or evaluator comments as evaluation content;
- inspect V5 responses to choose or revise H7 prompts after this freeze;
- access SHAE material;
- be represented as sealed or final assurance evidence.
