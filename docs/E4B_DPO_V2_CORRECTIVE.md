# PAUL Open E4B DPO V2 Corrective

> **RECONSTRUCTED CANDIDATE — REVALIDATED FROM REVIEWED EXPERIMENT DESIGN**

This experiment continues `google/gemma-4-E4B-it` at pinned revision
`ee0ef6023621cff504d758262d4e04895a5af4a2` from the genuine historical SFT
adapter in private dataset `paulfoundry/paul-open-sft`. Its corrective corpus is
the 14 records in `data/train/dpo_v2_corrective.jsonl`.

The historical adapter is authoritative: LoRA rank 16, alpha 32, dropout 0.05,
`CAUSAL_LM`, no bias, and no modules to save. The policy loads a byte-copied
adapter named `dpo` as trainable on GPU 0. A separate base and original frozen
adapter named `sft` form the evaluation-mode reference on GPU 1. Both bases use
4-bit NF4, double quantization, and FP16 compute.

## External reference compatibility

TRL 1.10.0 prepares a supplied reference through Accelerate. Accelerate 1.14.0
rejects a quantized GPU-1 model when the accelerator device is GPU 0 even with
`device_placement=False`. The dedicated subclass instead passes `ref_model=None`
during upstream construction, verifies the PEFT-policy branch created no
implicit reference, and then installs the exact frozen external reference.

Only the reference-log-probability boundary is specialized: reference-forward
tensors are copied to GPU 1 without mutating the policy batch; shifted labels,
completion masking, `selective_log_softmax`, and chosen/rejected splitting match
TRL. Only chosen/rejected sequence log-probabilities return to GPU 0. Upstream
TRL retains policy forward, log-ratio, beta, sigmoid loss, reward, and metrics.

## Zero-step command

```bash
python scripts/dpo_v2_e4b_smoke.py \
  --config configs/training/dpo_v2_e4b_corrective.yaml \
  --adapter "$SFT_ADAPTER_DIRECTORY" \
  --manifest /kaggle/working/paul_e4b_dpo_v2_corrective_smoke.json
```

The entry point has no training or weight-save mode. It requires exactly two
Tesla T4 GPUs, constructs and validates the trainer, requires `global_step == 0`
and no optimizer, writes a non-sensitive manifest, and exits. There is no
held-out corrective evaluation split; optimizer execution requires separate
authorization.

## Production training path

The production entry point is `scripts/dpo_v2_e4b_train.py`; the disposable
three-update v4 notebook was validation instrumentation and is not the training
implementation. The production entry point reuses the validated external-reference
boundary above, pins the policy to GPU 0 and the independently loaded, frozen,
evaluation-mode reference to GPU 1, and audits the 516 FP32 `dpo` LoRA tensors and
their optimizer membership before training. It requires the exact package versions
recorded in the corrective configuration and `uv.lock`.

Mixed precision is owned by Trainer, Accelerate, and the native GradScaler. Do not
set an initial scale in a wrapper: the bounded v4 validation observed safe overflow
skips and natural backoff from 65536 through 1024, with three authentic updates at
4096, 2048, and 1024. A skipped boundary may advance `TrainerState.global_step` in
the pinned runtime even though the underlying optimizer and scheduler do not step;
therefore `global_step` alone is not proof of a parameter update.

Run the non-training production preflight with a downloaded, hash-verified copy of
the historical adapter:

```bash
uv sync --frozen
uv run python scripts/dpo_v2_e4b_train.py \
  --config configs/training/dpo_v2_e4b_corrective.yaml \
  --adapter /kaggle/input/paul-open-sft \
  --output-dir /kaggle/working/paul_e4b_dpo_v2_corrective \
  --preflight-only
```

`--adapter` may name either the adapter directory itself or its Kaggle dataset
mount root. The production resolver accepts files directly at that path;
otherwise it accepts exactly one qualifying immediate child containing both
`adapter_config.json` and `adapter_model.safetensors`. It fails closed on zero
or multiple matches and does not recursively search unrelated directories. The
logical adapter identity remains `paulfoundry/paul-open-sft`, independently of
the resolved runtime path.

After separate authorization, remove only `--preflight-only`. Checkpoints use the
epoch save strategy under the output directory, with one retained checkpoint. A
normal completion writes `final-dpo-adapter/` plus `training_manifest.json`. Resume
only from a checkpoint produced by the same experiment, source revision, package
lock, model revision, dataset hash, and historical-adapter hashes:

```bash
uv run python scripts/dpo_v2_e4b_train.py \
  --config configs/training/dpo_v2_e4b_corrective.yaml \
  --adapter /kaggle/input/paul-open-sft \
  --output-dir /kaggle/working/paul_e4b_dpo_v2_corrective \
  --resume-from-checkpoint /kaggle/working/paul_e4b_dpo_v2_corrective/checkpoint-N
```

Every production checkpoint contains `checkpoint_provenance.json`, written by the
Trainer save callback. Before resume, the entry point requires that record to
exactly match the current source revision, resolved output lineage, complete
experiment/runtime lock, adapter topology, dataset, and historical-adapter
provenance. Missing, malformed, stale, or foreign provenance fails before
`Trainer.train`; Trainer remains solely responsible for restoring model,
optimizer, scheduler, scaler, and Trainer state after validation.

After training, verify that the saved adapter is still named `dpo`, remains rank
16 with alpha 32 and dropout 0.05, contains no `default` or `ref` adapter, and was
not merged. Re-run the zero-step topology/reference checks against the final
adapter before publication. Never interpret a checkpoint containing only skipped
AMP boundaries as evidence of a successful optimizer update.

## Bounded full-run accounting and completion gate

The committed corpus gives 14 dataloader microbatches per epoch at policy batch
size 1. Gradient accumulation is 8, so the pinned Trainer forms two attempted
update boundaries per epoch: one complete eight-microbatch group and one six-item
end-of-epoch remainder. The effective complete-cycle policy batch is 8.

The bounded production budget is four epochs: 56 example presentations, 56
dataloader batches, four complete eight-microbatch groups, four six-microbatch
remainders, and eight attempted Trainer boundaries. This is the smallest budget
with reasonable margin beyond the four overflow boundaries observed before the
first v4 update. If the validated trajectory repeats, boundaries 5 and 7 apply
updates while boundaries 6 and 8 may still overflow. One or two epochs cannot
reach the observed first finite boundary; three epochs has only one boundary of
margin and only one empirically expected update. An explicit `max_steps` budget
would count Trainer boundaries rather than authentic optimizer updates and is
therefore less clear and no more data-efficient for this pinned runtime.

A run is successful only if the underlying optimizer executes at least once,
the final trainable digest differs from the initial digest, applied gradients and
updated LoRA values are finite, and all policy/reference topology, placement,
freezing, optimizer-membership, and cross-device checks pass. In particular,
`TrainerState.global_step == 8` does not by itself prove learning. The final
adapter must not be published until the established external-reference probe and
mathematical-equivalence gate have passed against it.

The production completion gate directly checks all 516 intended final `dpo` LoRA
tensors for finite values and requires at least one per-tensor value digest to
change before saving. The manifest records the exact lock and source revision,
checkpoint provenance when resumed, initial/final aggregate digests, intended and
changed tensor counts, finite-value success, and the consolidated gate result.
