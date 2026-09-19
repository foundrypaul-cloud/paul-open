# PAUL Open — H8 DHE V6 Precommit Specification

**Date:** 2026-09-19  
**State:** PROMPT-FROZEN DEVELOPMENT EVALUATION / GENERATION NOT STARTED  
**Partition:** development  
**Cases:** 12  
**Reference:** historical PAUL SFT adapter  
**Candidate:** DPO V6 development freeze in `docs/DPO_V6_CANDIDATE_FREEZE.md`  
**SHAE:** sealed / not accessed

## Purpose

H8 is the fresh held-out development comparison for DPO V6. The prompts are frozen after V6 production completion but before any H8 candidate/reference response generation or inspection.

At authoring time, the public aggregate V6 production/diagnostic evidence was known. H8 was authored without access to V6 case-level diagnostic responses, H7 hidden A/B mappings, reviewer output, or SHAE material.

H8 is development evidence. It is not final assurance and cannot by itself establish broad model superiority.

The case manifest is `data/h8_dhe_v6_pilot_v1.jsonl`.

## Case allocation

| Case | Domain | Language | Reviewer cohort |
|---|---|---|---|
| H8-DHE-001 | science_reasoning | en | stem_capable |
| H8-DHE-002 | science_reasoning | en | stem_capable |
| H8-DHE-003 | socratic_tutoring | en | educator |
| H8-DHE-004 | socratic_tutoring | en | educator |
| H8-DHE-005 | scientific_research_assistance | en | domain_expert |
| H8-DHE-006 | scientific_research_assistance | en | domain_expert |
| H8-DHE-007 | scientific_explanation | hi | bilingual |
| H8-DHE-008 | scientific_explanation | bn | bilingual |
| H8-DHE-009 | evidence_first_human_centered | es | bilingual |
| H8-DHE-010 | multilingual_precision | es | bilingual |
| H8-DHE-011 | teacher_assistance | en | educator |
| H8-DHE-012 | student_assistance | en | educator |

The expansion from six to twelve cases reduces dependence on any single prompt while keeping the development-human-review burden tractable.

## Prompt-freeze gates

Before H8 generation is permitted, CI must verify:

1. exactly twelve unique case IDs and prompts with the frozen allocation above;
2. every case is `partition: development` and `development_exposed: true`;
3. no exact prompt reuse from H4, H5, H6, H7, or DPO V1–V6 training data;
4. Unicode-aware token-set Jaccard separation remains strictly below `0.35` against all of those development/training prompts;
5. the repository canonical benchmark leakage checker reports clean against Canonical Benchmark v1.0.0.

The separation tokenizer is `unicode_letter_mark_word_v1`: NFKC normalization, casefolding, and contiguous Unicode Letter/Number/Mark tokens.

## Candidate identity gate

Generation must use the exact V6 development candidate identified by:

- source revision `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- production run `35446312134`
- final adapter safetensors SHA-256 `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`

and the established SFT reference adapter.

A different adapter, later training run, repaired checkpoint, or prompt-tuned variant cannot be substituted under the H8/V6 identity.

## Generation contract

Reference and candidate generation must be matched.

Unless a separately reviewed methodology change is merged before generation, H8 should reuse the established H7/H6 safeguards:

- identical generation settings between SFT and V6;
- `max_new_tokens: 768`;
- EOS required before the hard limit;
- neutral response-length instruction;
- native-script checks for Hindi/Bengali/Spanish where applicable;
- malformed-output and automated-safety gates;
- deterministic recorded seed and A/B mapping kept private.

The generation manifest must record the exact base revision, SFT adapter hashes, V6 adapter digest, source revision, generation settings, and prompt-manifest hash.

## Human-review protocol

Initial collection:

- 3 independent valid judgments per case;
- disagreement, tie, not-sure, or material uncertainty may escalate to 5;
- exceptional hard cap 7;
- a reviewer must not see complementary A/B variants of the same case;
- source/model identity and mapping remain hidden until blinded analysis is locked.

Reviewers should judge correctness, usefulness, clarity, naturalness, instruction adherence, and domain-specific quality. Bilingual cases require reviewers competent in the requested language.

## Statistical and reporting plan

The primary unit of analysis is the **case**, not the individual judgment. Multiple judgments on one case are repeated ratings used to resolve that case and must not be treated as independent test examples.

Report:

- case-level V6-preferred / SFT-preferred / tie-or-unresolved counts;
- raw judgment counts as descriptive supporting evidence;
- per-domain and per-language outcomes;
- critical factual, safety, native-script, or instruction-following failures separately from preference totals;
- uncertainty using a case-level bootstrap or exact/binomial analysis where appropriate, with the small sample size stated explicitly.

H8 must not be converted into a single opaque leaderboard score.

## Decision semantics

H8 may support one of three development decisions:

- **advance V6 for assurance-candidate consideration** if the case-level evidence is directionally favorable and no material preservation/safety regression is found;
- **retain SFT as reference and continue research** if evidence is mixed or weak;
- **reject V6 for promotion** if material regressions are found.

No H8 outcome automatically opens SHAE. A separate assurance-candidate freeze and explicit SHAE authorization are required.

## Prohibitions

H8 must not:

- reuse H4–H7 prompts or DPO V1–V6 training prompts;
- use V6 case-level diagnostic outputs to choose or revise H8 prompts;
- use H7 response text or hidden mappings as prompt material;
- access SHAE material;
- change the V6 candidate after H8 response inspection;
- represent owner-only review as independent multi-reviewer evidence;
- represent H8 as final assurance or proof of broad superiority.
