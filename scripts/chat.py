#!/usr/bin/env python3
"""Interactive chat / inference demo for Gemma 4 models."""

import argparse
import sys
import yaml
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def main() -> None:
    parser = argparse.ArgumentParser(description="Chat with a Gemma 4 model")
    parser.add_argument("--model", required=True, help="Path to model config YAML")
    parser.add_argument("--mode", choices=["base", "sft", "dpo"], default="base")
    parser.add_argument("--adapter-path", default=None, help="Path to adapter checkpoint")
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()

    if args.mode in ["sft", "dpo"] and not args.adapter_path:
        print(f"Error: --adapter-path is required for mode '{args.mode}'", file=sys.stderr)
        sys.exit(1)

    with open(args.model, "r") as f:
        config = yaml.safe_load(f)
    hf_model_id = config.get("hf_model_id")

    print(f"Loading configuration from {args.model}...")
    print(f"Loading base model: {hf_model_id}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
        # Using bfloat16 for GPU, fallback to float16
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        
        model = AutoModelForCausalLM.from_pretrained(
            hf_model_id,
            torch_dtype=dtype,
            device_map="auto"
        )
        
        if args.mode in ["sft", "dpo"]:
            print(f"Loading {args.mode.upper()} adapter from {args.adapter_path}...")
            model = PeftModel.from_pretrained(model, args.adapter_path)
            
        model.eval()
            
        if args.smoke_test:
            print("Running deterministic smoke test generation...")
            messages = [{"role": "user", "content": "Hello."}]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False)
            response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)
            print(f"Smoke test successful. Output: {response}")
            sys.exit(0)
            
    except Exception as e:
        print(f"Error during inference/loading: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
