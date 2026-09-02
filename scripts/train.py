#!/usr/bin/env python3
"""Training entry point for PAUL Open Model.

Usage:
    uv run python scripts/train.py --model configs/models/gemma4_12b_it.yaml \
                                    --training configs/training/dpo.yaml \
                                    --data data/train/dpo_v2_corrective.jsonl \
                                    --adapter ./results/sft_adapter \
                                    --dry-run
"""

import argparse
import yaml
import json
import os
import sys
import torch
from datasets import Dataset

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_dpo_dataset(data_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")
    
    records = []
    with open(data_path, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    if len(records) != 14:
        raise ValueError(f"Expected exactly 14 records, found {len(records)}")
        
    ids = [r['id'] for r in records]
    if len(set(ids)) != 14:
        raise ValueError("Duplicate IDs found in dataset.")
        
    for r in records:
        if not r.get('prompt') or not r.get('chosen') or not r.get('rejected'):
            raise ValueError(f"Missing required fields (prompt, chosen, rejected) in record {r['id']}")
            
    print(f"Dataset validation passed: {len(records)} records loaded.")
    
    ds = Dataset.from_list([
        {
            "prompt": r["prompt"],
            "chosen": r["chosen"],
            "rejected": r["rejected"]
        }
        for r in records
    ])
    return ds

def main() -> None:
    parser = argparse.ArgumentParser(description="Train a Gemma 4 model")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--training", required=True, help="Path to training config YAML")
    parser.add_argument("--data", required=True, help="Path to data config YAML or JSONL")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--adapter", default=None, help="Path to pre-trained SFT adapter")
    parser.add_argument("--dry-run", action="store_true", help="Perform pre-flight validation without training")
    parser.add_argument("--smoke-test", action="store_true", help="Perform a 1-step training loop to test memory and backward pass")
    args = parser.parse_args()

    print("1. Loading dataset...")
    train_dataset = load_dpo_dataset(args.data)
    
    print("2. Loading configs...")
    train_cfg = load_yaml(args.training)
    model_cfg = load_yaml(args.model).get("model", {})
    
    dpo_cfg = train_cfg.get("training", {}).get("dpo_config", {})
    quant_cfg = model_cfg.get("quantization", {})
    lora_cfg = model_cfg.get("lora", {})

    print(f"Model ID: {model_cfg.get('hf_model_id')}")

    if dpo_cfg.get("bf16"):
        raise ValueError("bf16 is true but T4 GPU requires fp16! Check your config.")
    if not dpo_cfg.get("fp16"):
        raise ValueError("fp16 must be true for T4 GPU.")
        
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import PeftModel, LoraConfig
    from trl import DPOConfig, DPOTrainer
    
    print("3. Configuring quantization...")
    compute_dtype = torch.float16 if dpo_cfg.get("fp16") else torch.bfloat16
    
    has_gpu = torch.cuda.is_available()
    if has_gpu:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=quant_cfg.get("bnb_4bit_quant_type", "nf4"),
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=quant_cfg.get("bnb_4bit_use_double_quant", True)
        )
        print("GPU detected. Using BitsAndBytes 4-bit NF4 configuration.")
    else:
        bnb_config = None
        print("WARNING: No GPU detected. Disabling BitsAndBytes load_in_4bit to prevent crashes during dry-run.")
    
    print("4. Loading model and tokenizer...")
    model_id = model_cfg.get("hf_model_id")
    model_kwargs = {"device_map": "auto"}
    if bnb_config:
        model_kwargs["quantization_config"] = bnb_config
    else:
        model_kwargs["torch_dtype"] = torch.float32

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print(f"Loading {model_id}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        **model_kwargs
    )

    print("5. Loading SFT Adapter...")
    if not args.adapter:
        raise ValueError("--adapter must be specified for DPO V2 training (requires SFT adapter).")
        
    if not os.path.isdir(args.adapter):
        raise FileNotFoundError(f"Real SFT Adapter directory not found at {args.adapter}.")
        
    adapter_config_path = os.path.join(args.adapter, "adapter_config.json")
    if not os.path.exists(adapter_config_path):
        raise FileNotFoundError(f"adapter_config.json not found in {args.adapter}.")
        
    try:
        with open(adapter_config_path, "r") as f:
            adapter_config = json.load(f)
    except Exception as e:
        raise ValueError(f"Could not parse adapter_config.json: {e}")
        
    safetensors_path = os.path.join(args.adapter, "adapter_model.safetensors")
    if not os.path.exists(safetensors_path):
        raise FileNotFoundError(f"adapter_model.safetensors not found in {args.adapter}.")
        
    if os.path.getsize(safetensors_path) == 0:
        raise ValueError(f"adapter_model.safetensors is empty in {args.adapter}.")

    adapter_base_model = adapter_config.get("base_model_name_or_path")
    if not adapter_base_model:
        raise ValueError("base_model_name_or_path missing from adapter_config.json.")
        
    if adapter_base_model != model_id:
        raise ValueError(f"Adapter base model mismatch. Expected {model_id}, found {adapter_base_model}.")
        
    print(f"Loading real adapter from: {args.adapter}")
    try:
        model = PeftModel.from_pretrained(model, args.adapter, is_trainable=True)
    except Exception as e:
        raise RuntimeError(f"Failed to load adapter model with PeftModel.from_pretrained: {e}")

    print("6. Constructing DPOTrainer...")
    training_args = DPOConfig(
        output_dir=dpo_cfg.get("output_dir", "./results/dpo_v2"),
        beta=dpo_cfg.get("beta", 0.1),
        max_length=dpo_cfg.get("max_length", 4096),
        per_device_train_batch_size=dpo_cfg.get("per_device_train_batch_size", 1),
        per_device_eval_batch_size=dpo_cfg.get("per_device_eval_batch_size", 1),
        gradient_accumulation_steps=dpo_cfg.get("gradient_accumulation_steps", 8),
        learning_rate=dpo_cfg.get("learning_rate", 5.0e-7),
        num_train_epochs=dpo_cfg.get("num_train_epochs", 1),
        fp16=dpo_cfg.get("fp16", True),
        bf16=dpo_cfg.get("bf16", False),
        gradient_checkpointing=dpo_cfg.get("gradient_checkpointing", True),
        optim=dpo_cfg.get("optim", "paged_adamw_8bit"),
        seed=dpo_cfg.get("seed", 42),
    )
    
    if args.smoke_test:
        training_args.max_steps = 1
        training_args.num_train_epochs = 1
        print("SMOKE TEST MODE ENABLED: Forcing max_steps=1 to verify forward/backward/memory safely.")

    trainer = DPOTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        processing_class=tokenizer,
    )

    if args.dry_run:
        print("\n=== DRY RUN VALIDATION SUCCESSFUL ===")
        print("DPOTrainer construction: SUCCESS")
        print("Model and Adapter Loaded: SUCCESS")
        print("Configuration parses correctly.")
        print("Training executed: NO")
        sys.exit(0)
        
    print("Starting DPO training...")
    trainer.train()
    
    if args.smoke_test:
        print("\n=== SMOKE TEST SUCCESSFUL ===")
        print("1-step optimization completed successfully.")
        print("This verifies memory, forward, and backward passes.")
        sys.exit(0)

if __name__ == "__main__":
    main()
