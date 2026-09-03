#!/usr/bin/env python3
"""
Systematic model evaluation harness for Jetson Model Zoo.

Runs each model against all 12 test prompts with configurable parameters.
Saves results as JSON for quality scoring.

Usage:
    python3 eval_harness.py --model granite4.2-3b
    python3 eval_harness.py --model granite4.2-3b --temp 0.3 --top-k 40
    python3 eval_harness.py --batch  # all models with defaults
    python3 eval_harness.py --model granite4.2-3b --prompts html_profiles,python_code
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROMPTS_FILE = PROJECT_DIR / "test_prompts.json"
RESULTS_DIR = PROJECT_DIR / "results"
ZOO_DIR = Path(os.environ.get("ZOO_DIR", os.path.expanduser("~/models/new-zoo")))
LLAMA_CLI = os.environ.get("LLAMA_CLI", os.path.expanduser("~/llama.cpp/build/bin/llama-cli"))

# Model configs (mirrors run_model.sh registry)
# format: (filename, template, context, thinking)
MODEL_CONFIGS = {
    "gemma3-1b":            ("gemma3-1b.gguf", "gemma", 8192, False),
    "llama3.2-1b":          ("Llama-3.2-1B-Instruct.Q4_K_M.gguf", "llama3", 8192, False),
    "deepseek-r1-1.5b":     ("deepseek-r1-1.5b.gguf", "chatml", 4096, True),
    "qwen3-1.7b":           ("Qwen3-1.7B.Q4_K_M.gguf", "chatml", 8192, False),
    "qwen3.5-2b":           ("Qwen_Qwen3.5-2B-Q4_K_M.gguf", "chatml", 8192, True),
    "granite3.2-2b":        ("granite3.2-2b.gguf", "chatml", 8192, False),
    "gemma2-2b":            ("gemma2-2b.gguf", "gemma", 8192, False),
    "stablelm-zephyr":      ("stablelm-zephyr.gguf", "chatml", 8192, False),
    "lfm2.5-2.6b":          ("lfm2.5-2.6b.gguf", "chatml", 8192, False),
    "qwen2.5-3b":           ("qwen2.5-3b.gguf", "chatml", 8192, False),
    "qwen2.5-coder-3b":     ("qwen2.5-coder-3b.gguf", "chatml", 8192, False),
    "llama3.2-3b":          ("llama3.2-3b-bench.gguf", "llama3", 8192, False),
    "llama3.2-3b-new":      ("Llama-3.2-3B-Instruct.Q4_K_M.gguf", "llama3", 8192, False),
    "hermes3-3b-q4":        ("hermes3-3b-q4.gguf", "chatml", 8192, False),
    "hermes3-3b-q5":        ("hermes3-3b-q5.gguf", "chatml", 8192, False),
    "granite4-3b":          ("granite4-3b.gguf", "chatml", 8192, False),
    "granite4.1-3b":        ("granite4.1-3b.gguf", "chatml", 8192, False),
    "granite4.2-3b":        ("granite-4.2-3b-Q4_K_M.gguf", "chatml", 8192, False),
    "smollm3":              ("HuggingFaceTB_SmolLM3-3B-Q4_K_M.gguf", "chatml", 8192, False),
    "phi3-3.8b":            ("phi3-3.8b.gguf", "phi3", 8192, False),
    "phi4-mini":            ("Phi-4-mini-instruct.Q4_K_M.gguf", "phi3", 8192, True),
    "smallthinker-3b":      ("smallthinker-3b.gguf", "chatml", 4096, True),
    "ministral-3b":         ("ministral-3b-instruct-q5_k_m.gguf", "chatml", 8192, False),
    "ministral-3b-reasoning": ("Ministral-3-3B-Reasoning-2512-Q4_K_M.gguf", "chatml", 8192, True),
    "deepseek-r1-7b":       ("deepseek-r1-7b.gguf", "chatml", 2048, True),
    "gemma4-e2b":           ("gemma-4-E2B-it-Q4_K_M.gguf", "chatml", 2048, True),
    "gemma3n-e2b":          ("gemma-3n-E2B-it-Q4_K_M.gguf", "chatml", 2048, True),
}

def load_prompts():
    with open(PROMPTS_FILE) as f:
        data = json.load(f)
    return data["prompts"]

def build_command(model_key, prompt_text, params):
    filename, template, ctx, thinking = MODEL_CONFIGS[model_key]
    model_path = ZOO_DIR / filename

    if not model_path.exists():
        return None, None

    cmd = [
        LLAMA_CLI,
        "-m", str(model_path),
        "-p", prompt_text,
        "-n", str(params.get("max_tokens", 1024)),
        "-c", str(params.get("context", ctx)),
        "-ngl", "999",
        "-fa", "on",
        "--no-conversation",
        "--no-display-prompt",
        "-st",
        "--temp", str(params.get("temp", 0.3)),
        "--top-k", str(params.get("top_k", 40)),
        "--top-p", str(params.get("top_p", 0.9)),
        "--repeat-penalty", str(params.get("repeat_penalty", 1.1)),
        "--chat-template", template,
    ]

    if thinking:
        cmd.append("--jinja")

    return cmd, str(model_path)

def run_single(model_key, prompt_obj, params):
    cmd, model_path = build_command(model_key, prompt_obj["prompt"], params)
    if cmd is None:
        return {
            "model": model_key,
            "prompt_id": prompt_obj["id"],
            "category": prompt_obj["category"],
            "output": "",
            "error": "model file not found",
            "elapsed": 0,
            "params": params,
        }

    t0 = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        elapsed = time.time() - t0
        output = result.stdout

        # Strip llama.cpp banner/build info/loading artifacts from stdout
        # llama-cli prints build info, model info, then the prompt/output, then stats
        import re

        # Remove backspace characters and their following chars
        output = re.sub(r'\x08.', '', output)

        # Remove "Loading model..." with trailing spinner chars
        output = re.sub(r'Loading model\.\.\..*', '', output)

        # Remove build info header (lines starting with "build :", "model :", "ftype :", etc.)
        lines = output.split('\n')
        clean_lines = []
        in_header = True
        for line in lines:
            stripped = line.strip()
            # Skip header lines (build/model/ftype/system_info/etc.)
            if in_header:
                if re.match(r'^(build|model|ftype|system_info|params|sampling|prompt|dialog|add_\w+|general|modalities|available)\s*:', stripped, re.I):
                    continue
                if stripped.startswith('ggml_cuda') or stripped.startswith('device') or stripped.startswith('compute'):
                    continue
                if stripped in ('', 'Loading...', 'model loaded', 'Exiting...'):
                    continue
                # Skip the "available commands:" section
                if stripped.lower().startswith('available commands'):
                    continue
                if stripped.startswith('/exit') or stripped.startswith('/regen') or stripped.startswith('/clear') or stripped.startswith('/read') or stripped.startswith('/glob'):
                    continue
                # Check for ASCII art logo lines
                if stripped and all(c in '▄▀█ _|/\\-' for c in stripped) and any(c in '▄▀█' for c in stripped):
                    continue
                if stripped in ('|', '/', '\\', '-', '||', '//'):
                    continue
                # Skip the "> prompt" marker line
                if stripped.startswith('>'):
                    continue
                # Once we hit real content, stop header filtering
                if stripped and not stripped.startswith('log_') and not stripped.startswith('llama_'):
                    in_header = False

            # Skip the stats line and exit message in the output body
            if re.match(r'^\s*\[\s*Prompt:.*Generation:.*t/s\s*\]', stripped):
                continue
            if stripped == 'Exiting...':
                continue

            clean_lines.append(line)

        output = '\n'.join(clean_lines).lstrip('\n').strip()

        # Extract generation stats from STDOUT (not stderr)
        # Format: "[ Prompt: 39.5 t/s | Generation: 18.1 t/s ]"
        gen_tps = None
        prompt_tps = None
        full_output = result.stdout + result.stderr
        for line in full_output.split("\n"):
            if "Generation:" in line and "t/s" in line:
                m = re.search(r'Generation:\s*([\d.]+)\s*t/s', line)
                if m:
                    gen_tps = float(m.group(1))
            if "Prompt:" in line and "t/s" in line:
                m = re.search(r'Prompt:\s*([\d.]+)\s*t/s', line)
                if m:
                    prompt_tps = float(m.group(1))

        return {
            "model": model_key,
            "prompt_id": prompt_obj["id"],
            "category": prompt_obj["category"],
            "prompt_name": prompt_obj["name"],
            "output": output.strip(),
            "error": None,
            "elapsed": round(elapsed, 2),
            "gen_tps": gen_tps,
            "prompt_tps": prompt_tps,
            "params": params,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return {
            "model": model_key,
            "prompt_id": prompt_obj["id"],
            "category": prompt_obj["category"],
            "prompt_name": prompt_obj["name"],
            "output": "",
            "error": "timeout (180s)",
            "elapsed": round(elapsed, 2),
            "params": params,
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "model": model_key,
            "prompt_id": prompt_obj["id"],
            "category": prompt_obj["category"],
            "prompt_name": prompt_obj["name"],
            "output": "",
            "error": str(e),
            "elapsed": round(elapsed, 2),
            "params": params,
        }

def run_model(model_key, prompts, params, save=True):
    """Run all prompts for a single model."""
    print(f"\n{'='*60}")
    print(f"  MODEL: {model_key}")
    print(f"  Params: temp={params.get('temp',0.3)} top_k={params.get('top_k',40)} "
          f"top_p={params.get('top_p',0.9)} repeat={params.get('repeat_penalty',1.1)}")
    print(f"  Prompts: {len(prompts)}")
    print(f"{'='*60}")

    results = []
    for i, p in enumerate(prompts):
        print(f"\n  [{i+1}/{len(prompts)}] {p['id']} ({p['category']})... ", end="", flush=True)
        result = run_single(model_key, p, params)
        results.append(result)

        if result["error"]:
            print(f"ERROR: {result['error']}")
        else:
            out_len = len(result["output"])
            tps = result.get("gen_tps", "?")
            print(f"OK ({out_len} chars, {tps} t/s, {result['elapsed']}s)")

    if save:
        RESULTS_DIR.mkdir(exist_ok=True)
        param_tag = f"t{params.get('temp',0.3)}_k{params.get('top_k',40)}_p{params.get('top_p',0.9)}"
        outfile = RESULTS_DIR / f"{model_key}_{param_tag}.json"
        with open(outfile, "w") as f:
            json.dump({"model": model_key, "params": params, "results": results}, f, indent=2)
        print(f"\n  Saved to: {outfile}")

    return results

def main():
    parser = argparse.ArgumentParser(description="Jetson Model Zoo Evaluation Harness")
    parser.add_argument("--model", help="Single model key to test")
    parser.add_argument("--batch", action="store_true", help="Test all models")
    parser.add_argument("--prompts", help="Comma-separated prompt IDs (default: all)")
    parser.add_argument("--temp", type=float, default=0.3, help="Temperature (default: 0.3)")
    parser.add_argument("--top-k", type=int, default=40, help="Top-k (default: 40)")
    parser.add_argument("--top-p", type=float, default=0.9, help="Top-p (default: 0.9)")
    parser.add_argument("--repeat-penalty", type=float, default=1.1, help="Repeat penalty (default: 1.1)")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Max output tokens (default: 1024)")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    if args.list_models:
        print("Available models:")
        for key in sorted(MODEL_CONFIGS.keys()):
            filename, template, ctx, thinking = MODEL_CONFIGS[key]
            model_path = ZOO_DIR / filename
            exists = "✓" if model_path.exists() else "✗"
            think = " [thinking]" if thinking else ""
            print(f"  {exists} {key:25s} ctx={ctx:5d}{think}")
        return

    prompts = load_prompts()

    # Filter prompts if specified
    if args.prompts:
        ids = args.prompts.split(",")
        prompts = [p for p in prompts if p["id"] in ids]
        print(f"Filtered to {len(prompts)} prompts: {[p['id'] for p in prompts]}")

    params = {
        "temp": args.temp,
        "top_k": args.top_k,
        "top_p": args.top_p,
        "repeat_penalty": args.repeat_penalty,
        "max_tokens": args.max_tokens,
    }

    if args.batch:
        # Run all models
        all_results = {}
        for i, model_key in enumerate(sorted(MODEL_CONFIGS.keys())):
            print(f"\n{'#'*60}")
            print(f"# MODEL {i+1}/{len(MODEL_CONFIGS)}: {model_key}")
            print(f"{'#'*60}")
            results = run_model(model_key, prompts, params)
            all_results[model_key] = results
        # Summary
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE: {len(all_results)} models x {len(prompts)} prompts")
        print(f"{'='*60}")
    elif args.model:
        if args.model not in MODEL_CONFIGS:
            print(f"Error: Unknown model '{args.model}'")
            print(f"Available: {', '.join(sorted(MODEL_CONFIGS.keys()))}")
            sys.exit(1)
        run_model(args.model, prompts, params)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()