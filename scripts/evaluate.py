#!/usr/bin/env python3
"""Evaluation entry point for PAUL Open Model."""

import argparse
import sys
from pathlib import Path
import torch

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
except ImportError:
    print("Error: Missing required ML dependencies (transformers, peft).", file=sys.stderr)
    sys.exit(1)

try:
    from paul_open_model.models.loader import load_model_config
    from paul_open_model.evaluation.runner import EvaluationRunner
    from paul_open_model.evaluation.benchmark import get_baseline_benchmark_suite
except ImportError:
    print("Error: Could not import internal modules. Check PYTHONPATH.", file=sys.stderr)
    sys.exit(1)

def load_eval_config(path: str) -> dict:
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a Gemma 4 model")
    parser.add_argument("--mode", choices=["base", "sft", "dpo"], default="base", help="Inference mode")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--eval", required=True, help="Path to evaluation config YAML")
    parser.add_argument("--adapter-path", default=None, help="Path to adapter checkpoint")
    parser.add_argument("--output", default="results/evaluation", help="Output directory")
    args = parser.parse_args()

    if args.mode in ["sft", "dpo"] and not args.adapter_path:
        print(f"Error: --adapter-path is required for mode '{args.mode}'", file=sys.stderr)
        sys.exit(1)

    print(f"Loading configuration from {args.model}...")
    try:
        model_cfg = load_model_config(args.model)
        hf_model_id = model_cfg.get("hf_model_id", "google/gemma-4-E4B-it")
    except Exception as e:
        print(f"Error loading model config: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Loading base model: {hf_model_id}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        model = AutoModelForCausalLM.from_pretrained(
            hf_model_id,
            torch_dtype=dtype,
            device_map="auto"
        )
    except Exception as e:
        print(f"Error loading base model: {e}", file=sys.stderr)
        sys.exit(1)

    if args.mode in ["sft", "dpo"]:
        print(f"Loading {args.mode.upper()} adapter from {args.adapter_path}")
        adapter_path = Path(args.adapter_path)
        if not adapter_path.exists():
            print(f"Error: Adapter path does not exist: {adapter_path}", file=sys.stderr)
            sys.exit(1)
        try:
            model = PeftModel.from_pretrained(model, args.adapter_path)
        except Exception as e:
            print(f"Error loading adapter: {e}", file=sys.stderr)
            sys.exit(1)
        
    model.eval()

    import datetime
    now_str = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    experiment_id = f"exp_gemma4_e4b_{args.mode}_{now_str}"
    
    output_dir = Path(args.output) / args.mode
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Initializing EvaluationRunner for {args.mode} mode...")
    runner = EvaluationRunner(
        model=model,
        processor=tokenizer,
        suite=get_baseline_benchmark_suite(),
        model_id=hf_model_id,
        experiment_id=experiment_id,
        output_dir=output_dir,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.9,
        random_seed=42,
        resume=True
    )
    
    print("Starting evaluation...")
    results = runner.run_all(verbose=True)
    print(f"Evaluation complete. Results saved in {output_dir}/{experiment_id}")

if __name__ == "__main__":
    main()
