# PAUL Open H4 DHE — Kaggle Execution Handoff

**Status:** ready for paired generation  
**Partition:** development (DHE)  
**Frozen case manifest:** `data/h4_dhe_pilot_v1.jsonl`  
**Frozen generation contract:** `configs/evaluation/h4_dhe_pilot_v1.yaml`

## Objective

Generate matched responses for the six frozen H4 development cases from:

1. historical SFT reference adapter; and
2. frozen DPO V2 Corrective adapter produced by `paul_e4b_dpo_v2_corrective`.

Do not train, modify, merge, repair, or otherwise change either adapter.

## Source of truth

Use current `main` and preserve the Step 2 immutable freeze:

`research-freeze/step2-dpo-v2-20260909` @ `ac899e879f930f25b2081550bd8c5dd5c983df35`

The DPO production trainer emitted its final adapter at:

`<training output dir>/final-dpo-adapter`

as recorded by `scripts/dpo_v2_e4b_train.py` and the production `training_manifest.json`.

The historical SFT adapter is the same authoritative adapter used to initialize and reference the successful DPO V2 run.

## Non-negotiable methodology

- use `google/gemma-4-E4B-it` with the exact model revision recorded in the successful DPO V2 training manifest when available;
- use the same tokenizer/chat template for both checkpoints;
- use identical prompt bytes and identical generation settings for both checkpoints;
- use the repository E4B 4-bit NF4 loading convention already exercised by the DPO V2 workflow;
- do not regenerate a prompt selectively because one model's answer looks weak;
- do not manually edit generated responses;
- preserve raw generations before any human-facing conversion.

Generation settings are frozen in `configs/evaluation/h4_dhe_pilot_v1.yaml`:

- `max_new_tokens: 256`
- `temperature: 0.7`
- `top_p: 0.9`
- `random_seed: 42`
- tokenizer chat template with `add_generation_prompt=true`

## Required pre-generation audit

Run the repository leakage checker against the frozen manifest and persist its JSON report:

```bash
python scripts/check_leakage.py data/h4_dhe_pilot_v1.jsonl \
  --json-output outputs/h4_dhe/private/leakage_report.json \
  --verbose
```

A leakage failure blocks generation/collection. Do not waive it.

Also inspect `docs/H4_DHE_PILOT_V1_CONTAMINATION_AUDIT.md`. One candidate (the Earth/Sun seasons misconception) was already rejected because it matched SFT training material.

## Required output schema

Write one JSONL file per checkpoint. Every row must contain exactly the fields expected by the human-evaluation batch loader:

```json
{
  "case_id": "H4-DHE-001",
  "prompt": "...",
  "response": "...",
  "domain": "science_reasoning",
  "language": "en",
  "reviewer_cohort": "stem_capable"
}
```

Required paths:

- `outputs/h4_dhe/private/sft_reference.jsonl`
- `outputs/h4_dhe/private/dpo_v2_corrective.jsonl`
- `outputs/h4_dhe/private/generation_manifest.json`

The generation manifest must record at minimum:

- repo commit SHA;
- base model ID and resolved model revision;
- tokenizer/chat-template provenance if available;
- SFT adapter provenance/path and hashes if available;
- DPO V2 adapter provenance/path and hashes if available;
- generation settings;
- CUDA/GPU information;
- package versions;
- six case IDs for each checkpoint;
- success/failure per case;
- output file SHA-256 values.

## Hard gates before human-batch construction

For all six cases and both checkpoints verify:

- generation completed;
- response is non-empty;
- no generation exception/traceback leaked into response;
- no obviously malformed output;
- safety gate passes;
- case IDs/prompts/domain/language/cohort match exactly between the two source JSONLs;
- partition remains `development`;
- no SHAE material was accessed.

If a checkpoint produces an identical response for a case, leave it unchanged. The existing batch builder will skip identical pairs rather than manufacturing a difference.

## Build blinded H4 bundle

After all gates pass, use the existing batch builder. Supply a fresh private deterministic seed via a secret/environment variable; do not commit the seed.

```bash
python scripts/build_human_eval_batch.py \
  --left outputs/h4_dhe/private/sft_reference.jsonl \
  --right outputs/h4_dhe/private/dpo_v2_corrective.jsonl \
  --left-label sft_reference \
  --right-label dpo_v2_corrective \
  --seed "$PAUL_H4_DHE_SEED" \
  --variant-count 2 \
  --partition development \
  --public-output-dir outputs/human_eval/public/h4_dhe_pilot_v1 \
  --private-mapping .human-eval-private/h4_dhe_pilot_v1_mapping.json
```

Never publish `.human-eval-private/h4_dhe_pilot_v1_mapping.json` or expose it to reviewers.

## After generation

Stop before collecting reviewer judgments if any hard gate fails.

If all gates pass:

1. convert the blinded variants into the existing Google Forms packet format;
2. use the established Apps Script normalization/backup/recovery runtime;
3. package default groups of three comparisons per Form;
4. assign reviewers so each eligible case gets 3 initial valid judgments;
5. escalate only disagreement cases to 5, with exceptional hard cap 7;
6. keep public website participation disabled unless separately authorized in the canonical manifest;
7. lock analysis before unblinding.

H4 is development evidence only and cannot, by itself, establish final superiority. SHAE remains untouched.
