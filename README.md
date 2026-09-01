# Jetson Model Zoo

> Systematic evaluation of 27 small LLMs (1B–7B) running on an 8GB NVIDIA Jetson with llama.cpp GPU acceleration.

## What is this?

A benchmark suite that tests 27 quantized language models (Q4_K_M / Q5_K_M) on an 8GB Jetson edge device using llama.cpp with full GPU offload. Each model is evaluated against 12 carefully designed prompts covering HTML generation, Python coding, poetry, mathematical proofs, creative writing, and common Hermes agent function calls.

## Models Tested (27)

| Size Class | Models |
|------------|--------|
| **1B** | Gemma 3 1B, Llama 3.2 1B |
| **1.5B** | DeepSeek R1 1.5B (thinking) |
| **1.7B** | Qwen3 1.7B |
| **2B** | Qwen3.5 2B (thinking), Granite 3.2 2B, Gemma 2 2B, StableLM Zephyr, LFM 2.5 2.6B |
| **3B** | Qwen 2.5 3B, Qwen2.5-Coder 3B, Llama 3.2 3B, Hermes 3 3B (Q4/Q5), Granite 4/4.1/4.2 3B, SmolLM3 3B, Phi-3 3.8B, Phi-4-mini (thinking), SmallThinker 3B (thinking), Ministral 3B, Ministral 3B Reasoning (thinking) |
| **7B** | DeepSeek R1 7B (thinking) |
| **E2B** | Gemma 4 E2B (thinking), Gemma 3n E2B (thinking) |

### Excluded (poor performers)
- Orca-Mini 3B — quality 2.8/10, refuses tasks
- StarCoder2 3B — base model, not instruction-tuned
- CodeGemma 2B — code completion only

## Test Prompts (12)

| # | ID | Category | Description |
|---|-----|----------|-------------|
| 1 | html_profiles | HTML | Profile cards page with flexbox, hover, responsive |
| 2 | html_game | HTML | Click-the-target game with canvas, scoring, timer |
| 3 | python_code | Python | Grade processing function with type hints, docstring |
| 4 | iambic_pentameter | Poetry | 6-line poem in strict iambic pentameter |
| 5 | math_proof | Math | Induction proof: sum of first n naturals = n(n+1)/2 |
| 6 | creative_writing | Creative | 200-word short story about a memory-playing guitar |
| 7 | func_web_search | Function call | Web search for renewable energy news |
| 8 | func_terminal | Function call | Check disk usage via terminal |
| 9 | func_write_file | Function call | Create todo.txt file |
| 10 | func_read_file | Function call | Read /etc/hostname |
| 11 | func_sqlite | Function call | Query clinic database for recent patients |
| 12 | func_email | Function call | Draft professional rescheduling email |

See [`docs/test_prompts_reference.pdf`](docs/test_prompts_reference.pdf) for full prompt text and scoring rubrics.

## Quick Start

### Prerequisites
- NVIDIA Jetson (8GB RAM, CUDA support)
- llama.cpp built with CUDA: `~/llama.cpp/build/bin/llama-server`
- Python 3.10+
- ~30GB disk for model weights

### Install models

Models are stored in `~/models/new-zoo/`. Download via HuggingFace:

```python
from huggingface_hub import hf_hub_download
hf_hub_download("ibm-granite/granite-4.2-3b-GGUF", "granite-4.2-3b-Q4_K_M.gguf", local_dir="~/models/new-zoo/")
```

### Run a model

```bash
cd ~/projects/jetson-model-zoo
./run_model.sh list                    # list all available models
./run_model.sh granite4.2-3b           # start model on port 8082
./run_model.sh deepseek-r1-1.5b 9090   # start on custom port
./run_model.sh stop                    # stop running server
```

### Run the evaluation suite

```bash
# Single model
python3 eval_harness.py --model granite4.2-3b --max-tokens 2048

# All models (batch)
python3 eval_harness.py --batch --max-tokens 2048

# Custom parameters
python3 eval_harness.py --model qwen3.5-2b --temp 0.7 --top-k 80 --max-tokens 2048

# Score results
python3 score_results.py --all
```

### Default Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Temperature | 0.3 | Low for deterministic output |
| Top-k | 40 | Standard sampling |
| Top-p | 0.9 | Nucleus sampling |
| Repeat penalty | 1.1 | Prevent repetition |
| Max tokens | 2048 | Enough for complete responses |
| GPU layers | 999 (all) | Full GPU offload |
| Flash attention | on | CUDA acceleration |

## Hardware

- **Device**: NVIDIA Jetson (8GB unified memory, aarch64)
- **GPU**: NVIDIA GPU with CUDA 12.6
- **RAM**: ~4.3GB available with GUI off
- **Backend**: llama.cpp with CUDA, flash attention on, full GPU offload

## Project Structure

```
jetson-model-zoo/
├── run_model.sh              # Model launcher with registry (27 models)
├── test_model.py             # Quick smoke test for a single model
├── eval_harness.py           # Systematic evaluation harness
├── score_results.py          # Automated quality scoring (1-10 rubric)
├── test_prompts.json         # 12 test prompts with scoring rubrics
├── run_all_tests.sh          # Batch runner for all models
├── docs/
│   └── test_prompts_reference.pdf  # Printable prompt reference
├── results/                  # Raw model outputs (JSON per model)
└── scores/                   # Scored results (CSV)
```

## License

MIT