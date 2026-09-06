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
