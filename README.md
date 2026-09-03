# Jetson Model Zoo

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-NVIDIA%20Jetson%208GB-76B900.svg)
![Models](https://img.shields.io/badge/models-27%20tested-orange.svg)
![Prompts](https://img.shields.io/badge/prompts-12%20across%206%20categories-9cf.svg)
![Scored Rows](https://img.shields.io/badge/scored%20rows-2%2C916-blue.svg)
![Sweeps](https://img.shields.io/badge/sweeps-temp%20%2B%20top__k-blueviolet.svg)
![Champion](https://img.shields.io/badge/champion-hermes3--3b--q5%20(7.8)--gold.svg)
![llama.cpp](https://img.shields.io/badge/engine-llama.cpp%20CUDA-red.svg)
![ARM64](https://img.shields.io/badge/arch-ARM64-aarch64.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

![k=40](https://img.shields.io/badge/top__k-40%20optimal%20(21%2F27)-blueviolet.svg)
![DeepSeek Fix](https://img.shields.io/badge/DeepSeek-chatml%20template%20fix-yellow.svg)
![E2B Fix](https://img.shields.io/badge/E2B-chatml%20template%20fix-yellow.svg)
![Reports](https://img.shields.io/badge/reports-PDF%20%2B%20CSV-success.svg)
![GPU](https://img.shields.io/badge/GPU-full%20offload%20%2B%20flash%20attn-success.svg)
![Categories](https://img.shields.io/badge/categories-HTML%20%7C%20Python%20%7C%20Math%20%7C%20Poetry%20%7C%20Creative%20%7C%20Func%20Calls-purple.svg)

> Systematic evaluation of 27 small LLMs (1B-7B) running on an 8GB NVIDIA Jetson with llama.cpp GPU acceleration. 2,916 scored rows across temperature and top-k sweeps.

---

## Table of Contents

1. [What is this?](#what-is-this)
2. [Key Findings](#key-findings)
3. [Full Leaderboard](#full-leaderboard--all-27-models)
4. [Temperature Sweep Results](#temperature-sweep-results)
5. [Top-K Sweep Results](#top-k-sweep-results)
6. [Chat Template Fixes — DeepSeek & E2B](#chat-template-fixes--deepseek--e2b)
7. [Category Analysis](#category-analysis)
8. [Per-Model Findings](#per-model-findings--all-27-models)
9. [Test Prompts](#test-prompts-12)
10. [Methodology](#methodology)
11. [Quick Start](#quick-start)
12. [Hardware](#hardware)
13. [Project Structure](#project-structure)

---

## What is this?

A benchmark suite that tests 27 quantized language models (Q4_K_M / Q5_K_M) on an 8GB Jetson edge device using llama.cpp with full GPU offload. Each model is evaluated against 12 carefully designed prompts covering HTML generation, Python coding, poetry, mathematical proofs, creative writing, and common Hermes agent function calls.

The benchmark data from this project powers the [LLM Transmission 8GB](https://github.com/drwjkirkpatrick-web/llm-transmission-8gb-202609) routing service, which classifies prompts and routes them to the best local model.

## Key Findings

- **hermes3-3b-q5** is the overall champion (7.8/10 at t=0.3, k=40) - strong across all categories
- **lfm2.5-2.6b** achieves perfect coding & math scores (10.0/10) at 23.8 tok/s
- **gemma3n-e2b** jumped from 1.9 to **7.1** after chatml template fix - excellent creative (9.5) and coding (9.2)
- **gemma4-e2b** jumped from 0.8 to **6.0** after chatml template fix - strong coding (9.2) and creative (9.5)
- **ministral-3b-reasoning** is the best creative writer (9.5/10) but slow at 18.7 tok/s
- **smallthinker-3b** is the best function caller (7.7/10) - the only model that reliably produces valid tool-call JSON
- **k=40** is the universal optimal top_k - wins 21/27 models (78%)
- **No single temperature works** - 7 models peak at t=0.3, 7 at t=1.0. Per-model locked temps are essential
- **DeepSeek R1 distills need chatml template**, not deepseek - using the wrong template caused 43-158% score degradation
- **E2B (MatFormer) models need chatml template**, not gemma - using the wrong template caused 273-650% score degradation
- **Function calls are the hardest category** - no model scores above 7.7/10; most produce prose instead of structured JSON
- **Models under 2B parameters** (gemma3-1b, llama3.2-1b, phi3-3.8b) score below 3.0/10 - not suitable for production use

---

## Full Leaderboard — All 27 Models

Overall score = average across all 12 prompts at each model's best temperature with k=40. Group scores = averages within each category.

| Rank | Model | Overall | Code/Math | Creative | Func Calls | Speed (t/s) | Best Temp | Top-K | Template | Thinking |
|------|-------|---------|-----------|----------|------------|-------------|-----------|-------|----------|----------|
| 1 | hermes3-3b-q5 | 7.8 | 9.8 | 9.0 | 6.2 | 19.4 | 0.3 | 40 | chatml | — |
| 2 | smallthinker-3b | 7.6 | 8.5 | 5.5 | 7.7 | 20.1 | 0.3 | 40 | chatml | ✅ |
| 3 | deepseek-r1-7b | 7.5 | 10.0 | 7.0 | 6.3 | 9.7 | 0.0 | 40 | chatml | ✅ |
| 4 | hermes3-3b-q4 | 7.5 | 9.8 | 6.5 | 6.3 | 19.7 | 0.7 | 40 | chatml | — |
| 5 | qwen2.5-3b | 7.5 | 9.0 | 8.5 | 6.2 | 20.1 | 0.3 | 40 | chatml | — |
| 6 | qwen3.5-2b | 7.5 | 9.8 | 9.0 | 5.5 | 24.9 | 0.1 | 40 | chatml | ✅ |
| 7 | granite4.1-3b | 7.4 | 9.2 | 8.5 | 5.8 | 18.9 | 1.0 | 40 | chatml | — |
| 8 | ministral-3b-reasoning | 7.2 | 9.5 | 9.5 | 5.0 | 18.7 | 0.3 | 40 | chatml | ✅ |
| 9 | qwen3-1.7b | 7.2 | 9.8 | 5.5 | 6.0 | 30.8 | 1.0 | 40 | chatml | — |
| 10 | smollm3 | 7.2 | 9.2 | 7.0 | 5.8 | 20.8 | 1.0 | 40 | chatml | — |
| 11 | gemma3n-e2b | 7.1 | 9.2 | 9.5 | 4.8 | 21.5 | 0.7 | 40 | chatml | ✅ |
| 12 | granite3.2-2b | 7.0 | 9.5 | 7.0 | 5.3 | 26.6 | 0.3 | 40 | chatml | — |
| 13 | granite4.2-3b | 6.9 | 9.5 | 6.5 | 5.3 | 18.9 | 1.0 | 40 | chatml | — |
| 14 | qwen2.5-coder-3b | 6.9 | 9.5 | 8.5 | 4.7 | 20.0 | 0.1 | 40 | chatml | — |
| 15 | granite4-3b | 6.8 | 9.5 | 6.5 | 5.0 | 18.9 | 0.7 | 40 | chatml | — |
| 16 | stablelm-zephyr | 6.8 | 9.8 | 8.0 | 4.3 | 26.4 | 0.3 | 40 | chatml | — |
| 17 | lfm2.5-2.6b | 6.6 | 10.0 | 5.5 | 4.7 | 23.8 | 0.2 | 40 | chatml | — |
| 18 | gemma4-e2b | 6.0 | 9.2 | 9.5 | 2.7 | 23.4 | 0.7 | 40 | chatml | ✅ |
| 19 | deepseek-r1-1.5b | 5.3 | 9.2 | 4.5 | 3.0 | 32.7 | 0.0 | 40 | chatml | ✅ |
| 20 | ministral-3b | 4.9 | 7.2 | 5.5 | 3.2 | 24.7 | 0.5 | 40 | chatml | — |
| 21 | gemma2-2b | 4.5 | 2.8 | 4.0 | 5.8 | 22.3 | 0.1 | 40 | gemma | — |
| 22 | llama3.2-3b | 2.8 | 1.8 | 5.0 | 2.7 | 19.7 | 1.0 | 40 | llama3 | — |
| 23 | gemma3-1b | 2.7 | 2.2 | 3.5 | 2.7 | 31.5 | 1.0 | 40 | gemma | — |
| 24 | phi3-3.8b | 2.5 | 2.2 | 4.0 | 2.2 | 17.7 | 0.2 | 40 | phi3 | — |
| 25 | llama3.2-1b | 2.4 | 1.2 | 4.5 | 2.5 | 42.2 | 0.3 | 40 | llama3 | — |
| 26 | phi4-mini | 2.3 | 2.5 | 3.0 | 2.0 | 16.8 | 1.0 | 40 | phi3 | ✅ |
| 27 | llama3.2-3b-new | 2.2 | 1.5 | 3.5 | 2.2 | 19.7 | 0.0 | 40 | llama3 | — |

---

## Temperature Sweep Results

Each model was tested at 7 temperatures (0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0) with all other parameters held constant (top_k=40, top_p=0.9, repeat_penalty=1.1, max_tokens=2048). Best temp = highest average score across 12 prompts.

**Total: 27 models x 7 temps x 12 prompts = 2,268 runs**

| Best Temp | # Models | Models |
|-----------|----------|--------|
| t=0.0 | 3 | deepseek-r1-7b, deepseek-r1-1.5b, llama3.2-3b-new |
| t=0.1 | 3 | qwen3.5-2b, qwen2.5-coder-3b, gemma2-2b |
| t=0.2 | 2 | lfm2.5-2.6b, phi3-3.8b |
| t=0.3 | 7 | hermes3-3b-q5, smallthinker-3b, qwen2.5-3b, ministral-3b-reasoning, granite3.2-2b, stablelm-zephyr, llama3.2-1b |
| t=0.5 | 1 | ministral-3b |
| t=0.7 | 4 | hermes3-3b-q4, gemma3n-e2b, granite4-3b, gemma4-e2b |
| t=1.0 | 7 | granite4.1-3b, qwen3-1.7b, smollm3, granite4.2-3b, llama3.2-3b, gemma3-1b, phi4-mini |

**Key insight:** There is no single "best" temperature. Reasoning/thinking models (DeepSeek R1, Ministral Reasoning) prefer low temperatures (0.0-0.3), while creative models (Granite 4.1, Qwen 3 1.7B) benefit from high temperatures (1.0). This is why the transmission service stores a per-model locked temperature rather than using a global default.

---

## Top-K Sweep Results

After locking the best temperature per model, we swept top_k across 3 values: 20, 40, and 64. This produced 27 x 3 x 12 = 972 additional scored runs.

| Top-K | # Models Where Best | Percentage | Notes |
|-------|---------------------|------------|-------|
| k=20 | 4 | 15% |  |
| k=40 | 21 | 78% |  |
| k=64 | 2 | 7% |  |

k=40 is the confirmed default. The 4 models that prefer k=20 are still tested at k=40 in the routing table (the difference is typically <0.3 points), and k=40 provides the best balance across all categories.

---

## Chat Template Fixes — DeepSeek & E2B

Two model families were discovered to use the wrong chat template, causing them to ignore prompts entirely and produce garbage or hallucinated output.

### DeepSeek R1 Distills (deepseek -> chatml)

The eval harness was using the `deepseek` chat template, designed for original DeepSeek Coder models. However, DeepSeek R1-Distill models are **Qwen-architecture models** fine-tuned by DeepSeek - they use ChatML format.

| Model | Before (deepseek) | After (chatml) | Improvement |
|-------|-------------------|----------------|-------------|
| deepseek-r1-1.5b | 3.7 | 5.3 | +1.6 (43%) |
| deepseek-r1-7b | 2.4 | 6.2 | +3.8 (158%) |

### E2B MatFormer Models (gemma -> chatml)

Gemma 3n E2B and Gemma 4 E2B are MatFormer models. The `gemma` template caused them to hallucinate about "Gemini 1.5 Pro vs GPT-4 Turbo" or output only `"_4"`. Switching to `chatml` with `--jinja` fixed both.

| Model | Before (gemma) | After (chatml) | Improvement |
|-------|-----------------|----------------|-------------|
| gemma3n-e2b | 1.9 | 7.1 | +5.2 (273%) |
| gemma4-e2b | 0.8 | 6.0 | +5.2 (650%) |

**Lesson:** Always verify the chat template matches the model's architecture, not just its name. A "DeepSeek" model may use chatml, and a "Gemma" model may use chatml too.

---

## Category Analysis

### Coding & Math — Top 10

| Rank | Model | Code/Math | Speed (t/s) | Temp | Thinking |
|------|-------|---------|-------------|------|----------|
| 1 | deepseek-r1-7b | 10.0 | 9.7 | 0.0 | ✅ |
| 2 | lfm2.5-2.6b | 10.0 | 23.8 | 0.2 | — |
| 3 | hermes3-3b-q5 | 9.8 | 19.4 | 0.3 | — |
| 4 | hermes3-3b-q4 | 9.8 | 19.7 | 0.7 | — |
| 5 | qwen3.5-2b | 9.8 | 24.9 | 0.1 | ✅ |
| 6 | qwen3-1.7b | 9.8 | 30.8 | 1.0 | — |
| 7 | stablelm-zephyr | 9.8 | 26.4 | 0.3 | — |
| 8 | ministral-3b-reasoning | 9.5 | 18.7 | 0.3 | ✅ |
| 9 | granite3.2-2b | 9.5 | 26.6 | 0.3 | — |
| 10 | granite4.2-3b | 9.5 | 18.9 | 1.0 | — |

### Creative & Poetry — Top 10

| Rank | Model | Creative | Speed (t/s) | Temp | Thinking |
|------|-------|--------|-------------|------|----------|
| 1 | ministral-3b-reasoning | 9.5 | 18.7 | 0.3 | ✅ |
| 2 | gemma3n-e2b | 9.5 | 21.5 | 0.7 | ✅ |
| 3 | gemma4-e2b | 9.5 | 23.4 | 0.7 | ✅ |
| 4 | hermes3-3b-q5 | 9.0 | 19.4 | 0.3 | — |
| 5 | qwen3.5-2b | 9.0 | 24.9 | 0.1 | ✅ |
| 6 | qwen2.5-3b | 8.5 | 20.1 | 0.3 | — |
| 7 | granite4.1-3b | 8.5 | 18.9 | 1.0 | — |
| 8 | qwen2.5-coder-3b | 8.5 | 20.0 | 0.1 | — |
| 9 | stablelm-zephyr | 8.0 | 26.4 | 0.3 | — |
| 10 | deepseek-r1-7b | 7.0 | 9.7 | 0.0 | ✅ |

### Function Calls — Top 10

| Rank | Model | Func Calls | Speed (t/s) | Temp | Thinking |
|------|-------|----------|-------------|------|----------|
| 1 | smallthinker-3b | 7.7 | 20.1 | 0.3 | ✅ |
| 2 | deepseek-r1-7b | 6.3 | 9.7 | 0.0 | ✅ |
| 3 | hermes3-3b-q4 | 6.3 | 19.7 | 0.7 | — |
| 4 | hermes3-3b-q5 | 6.2 | 19.4 | 0.3 | — |
| 5 | qwen2.5-3b | 6.2 | 20.1 | 0.3 | — |
| 6 | qwen3-1.7b | 6.0 | 30.8 | 1.0 | — |
| 7 | granite4.1-3b | 5.8 | 18.9 | 1.0 | — |
| 8 | smollm3 | 5.8 | 20.8 | 1.0 | — |
| 9 | gemma2-2b | 5.8 | 22.3 | 0.1 | — |
| 10 | qwen3.5-2b | 5.5 | 24.9 | 0.1 | ✅ |

---

## Per-Model Findings — All 27 Models

Each model below includes its ideal settings, per-prompt score breakdown, and observations from the benchmark.


### #1 — hermes3-3b-q5

| Setting | Value |
|---------|-------|
| File | `hermes3-3b-q5.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 19.4 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 10/10 | 19.4 |
| Function Call: Email Draft | Func Call | 7/10 | 19.4 |
| Function Call: Read File | Func Call | 8/10 | 19.5 |
| Function Call: SQLite Query | Func Call | 4/10 | 19.5 |
| Function Call: Terminal Command | Func Call | 8/10 | 19.4 |
| Function Call: Web Search | Func Call | 2/10 | 19.5 |
| Function Call: Write File | Func Call | 8/10 | 19.4 |
| HTML Web Browser Game | HTML | 10/10 | 19.3 |
| HTML Profile Cards Page | HTML | 10/10 | 19.4 |
| Iambic Pentameter Poem | Creative | 8/10 | 19.4 |
| Mathematical Proof | Math | 9/10 | 19.5 |
| Python Data Processing | Python | 10/10 | 19.4 |

- Excellent at coding & math
- Excellent at creative writing & poetry
- ✅ Recommended for production use

### #2 — smallthinker-3b

| Setting | Value |
|---------|-------|
| File | `smallthinker-3b.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 4,096 |
| Generation Speed | 20.1 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 20.3 |
| Function Call: Email Draft | Func Call | 8/10 | 20.1 |
| Function Call: Read File | Func Call | 8/10 | 20.2 |
| Function Call: SQLite Query | Func Call | 10/10 | 20.1 |
| Function Call: Terminal Command | Func Call | 10/10 | 20.3 |
| Function Call: Web Search | Func Call | 4/10 | 20.2 |
| Function Call: Write File | Func Call | 6/10 | 20.0 |
| HTML Web Browser Game | HTML | 8/10 | 19.9 |
| HTML Profile Cards Page | HTML | 9/10 | 20.2 |
| Iambic Pentameter Poem | Creative | 3/10 | 20.1 |
| Mathematical Proof | Math | 9/10 | 20.1 |
| Python Data Processing | Python | 8/10 | 20.0 |

- Strong function-call format compliance
- Reasoning model — produces thinking blocks, needs --jinja flag
- ✅ Recommended for production use

### #3 — deepseek-r1-7b

| Setting | Value |
|---------|-------|
| File | `deepseek-r1-7b.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 2,048 |
| Generation Speed | 9.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 7/10 | 9.7 |
| Function Call: Email Draft | Func Call | 8/10 | 9.7 |
| Function Call: Read File | Func Call | 10/10 | 9.7 |
| Function Call: SQLite Query | Func Call | 4/10 | 9.7 |
| Function Call: Terminal Command | Func Call | 4/10 | 9.7 |
| Function Call: Web Search | Func Call | 4/10 | 9.7 |
| Function Call: Write File | Func Call | 8/10 | 9.7 |
| HTML Web Browser Game | HTML | 10/10 | 9.7 |
| HTML Profile Cards Page | HTML | 10/10 | 9.7 |
| Mathematical Proof | Math | 10/10 | 9.7 |

- Excellent at coding & math
- Slow generation (9.7 tok/s) — may timeout on long prompts
- Reasoning model — produces thinking blocks, needs --jinja flag
- ✅ Recommended for production use

### #4 — hermes3-3b-q4

| Setting | Value |
|---------|-------|
| File | `hermes3-3b-q4.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.7 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 19.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 19.8 |
| Function Call: Email Draft | Func Call | 8/10 | 19.7 |
| Function Call: Read File | Func Call | 8/10 | 19.8 |
| Function Call: SQLite Query | Func Call | 4/10 | 19.8 |
| Function Call: Terminal Command | Func Call | 8/10 | 19.7 |
| Function Call: Web Search | Func Call | 2/10 | 19.8 |
| Function Call: Write File | Func Call | 8/10 | 19.8 |
| HTML Web Browser Game | HTML | 9/10 | 19.7 |
| HTML Profile Cards Page | HTML | 10/10 | 19.7 |
| Iambic Pentameter Poem | Creative | 5/10 | 19.7 |
| Mathematical Proof | Math | 10/10 | 19.7 |
| Python Data Processing | Python | 10/10 | 19.6 |

- Excellent at coding & math
- ✅ Recommended for production use

### #5 — qwen2.5-3b

| Setting | Value |
|---------|-------|
| File | `qwen2.5-3b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 20.1 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 20.2 |
| Function Call: Email Draft | Func Call | 9/10 | 20.1 |
| Function Call: Read File | Func Call | 2/10 | 20.1 |
| Function Call: SQLite Query | Func Call | 8/10 | 20.1 |
| Function Call: Terminal Command | Func Call | 8/10 | 20.1 |
| Function Call: Web Search | Func Call | 2/10 | 20.3 |
| Function Call: Write File | Func Call | 8/10 | 20.2 |
| HTML Web Browser Game | HTML | 10/10 | 20.1 |
| HTML Profile Cards Page | HTML | 9/10 | 20.1 |
| Iambic Pentameter Poem | Creative | 8/10 | 19.9 |
| Mathematical Proof | Math | 8/10 | 20.2 |
| Python Data Processing | Python | 9/10 | 20.1 |

- Excellent at coding & math
- ✅ Recommended for production use

### #6 — qwen3.5-2b

| Setting | Value |
|---------|-------|
| File | `Qwen_Qwen3.5-2B-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.1 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 24.9 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 24.7 |
| Function Call: Email Draft | Func Call | 9/10 | 24.7 |
| Function Call: Read File | Func Call | 2/10 | 24.6 |
| Function Call: SQLite Query | Func Call | 2/10 | 24.7 |
| Function Call: Terminal Command | Func Call | 10/10 | 24.9 |
| Function Call: Web Search | Func Call | 2/10 | 25.4 |
| Function Call: Write File | Func Call | 8/10 | 24.7 |
| HTML Web Browser Game | HTML | 10/10 | 25.1 |
| HTML Profile Cards Page | HTML | 10/10 | 25.1 |
| Iambic Pentameter Poem | Creative | 9/10 | 24.5 |
| Mathematical Proof | Math | 9/10 | 24.9 |
| Python Data Processing | Python | 10/10 | 25.0 |

- Excellent at coding & math
- Excellent at creative writing & poetry
- Reasoning model — produces thinking blocks, needs --jinja flag
- ✅ Recommended for production use

### #7 — granite4.1-3b

| Setting | Value |
|---------|-------|
| File | `granite4.1-3b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 18.9 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 19.0 |
| Function Call: Email Draft | Func Call | 9/10 | 18.8 |
| Function Call: Read File | Func Call | 8/10 | 18.9 |
| Function Call: SQLite Query | Func Call | 2/10 | 18.8 |
| Function Call: Terminal Command | Func Call | 8/10 | 18.9 |
| Function Call: Web Search | Func Call | 2/10 | 19.0 |
| Function Call: Write File | Func Call | 6/10 | 18.9 |
| HTML Web Browser Game | HTML | 10/10 | 18.7 |
| HTML Profile Cards Page | HTML | 9/10 | 18.9 |
| Iambic Pentameter Poem | Creative | 8/10 | 18.9 |
| Mathematical Proof | Math | 8/10 | 19.0 |
| Python Data Processing | Python | 10/10 | 18.9 |

- Excellent at coding & math
- ✅ Recommended for production use

### #8 — ministral-3b-reasoning

| Setting | Value |
|---------|-------|
| File | `Ministral-3-3B-Reasoning-2512-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 18.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 18.6 |
| Function Call: Email Draft | Func Call | 9/10 | 18.6 |
| Function Call: Read File | Func Call | 1/10 | 18.9 |
| Function Call: SQLite Query | Func Call | 2/10 | 18.7 |
| Function Call: Terminal Command | Func Call | 8/10 | 18.8 |
| Function Call: Web Search | Func Call | 2/10 | 18.9 |
| Function Call: Write File | Func Call | 8/10 | 18.6 |
| HTML Web Browser Game | HTML | 10/10 | 18.6 |
| HTML Profile Cards Page | HTML | 10/10 | 18.7 |
| Iambic Pentameter Poem | Creative | 10/10 | 18.7 |
| Mathematical Proof | Math | 8/10 | 18.8 |
| Python Data Processing | Python | 10/10 | 18.7 |

- Excellent at coding & math
- Excellent at creative writing & poetry
- Reasoning model — produces thinking blocks, needs --jinja flag
- ✅ Recommended for production use

### #9 — qwen3-1.7b

| Setting | Value |
|---------|-------|
| File | `Qwen3-1.7B.Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 30.8 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 30.9 |
| Function Call: Email Draft | Func Call | 8/10 | 31.1 |
| Function Call: Read File | Func Call | 8/10 | 31.2 |
| Function Call: SQLite Query | Func Call | 4/10 | 31.0 |
| Function Call: Terminal Command | Func Call | 6/10 | 30.9 |
| Function Call: Web Search | Func Call | 4/10 | 31.1 |
| Function Call: Write File | Func Call | 6/10 | 30.9 |
| HTML Web Browser Game | HTML | 10/10 | 30.1 |
| HTML Profile Cards Page | HTML | 10/10 | 30.7 |
| Iambic Pentameter Poem | Creative | 3/10 | 30.8 |
| Mathematical Proof | Math | 9/10 | 31.0 |
| Python Data Processing | Python | 10/10 | 30.1 |

- Excellent at coding & math
- Fast generation (30.8 tok/s)
- ✅ Recommended for production use

### #10 — smollm3

| Setting | Value |
|---------|-------|
| File | `HuggingFaceTB_SmolLM3-3B-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 20.8 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 20.8 |
| Function Call: Email Draft | Func Call | 9/10 | 20.9 |
| Function Call: Read File | Func Call | 8/10 | 20.8 |
| Function Call: SQLite Query | Func Call | 2/10 | 20.9 |
| Function Call: Terminal Command | Func Call | 10/10 | 20.9 |
| Function Call: Web Search | Func Call | 2/10 | 20.9 |
| Function Call: Write File | Func Call | 4/10 | 20.9 |
| HTML Web Browser Game | HTML | 10/10 | 20.6 |
| HTML Profile Cards Page | HTML | 9/10 | 20.7 |
| Iambic Pentameter Poem | Creative | 5/10 | 20.5 |
| Mathematical Proof | Math | 8/10 | 20.7 |
| Python Data Processing | Python | 10/10 | 20.8 |

- Excellent at coding & math
- ✅ Recommended for production use

### #11 — gemma3n-e2b

| Setting | Value |
|---------|-------|
| File | `gemma-3n-E2B-it-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.7 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 2,048 |
| Generation Speed | 21.5 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 21.3 |
| Function Call: Email Draft | Func Call | 9/10 | 21.1 |
| Function Call: Read File | Func Call | 2/10 | 21.5 |
| Function Call: SQLite Query | Func Call | 2/10 | 20.9 |
| Function Call: Terminal Command | Func Call | 10/10 | 21.6 |
| Function Call: Web Search | Func Call | 4/10 | 21.9 |
| Function Call: Write File | Func Call | 2/10 | 21.5 |
| HTML Web Browser Game | HTML | 10/10 | 21.7 |
| HTML Profile Cards Page | HTML | 9/10 | 21.7 |
| Iambic Pentameter Poem | Creative | 10/10 | 21.5 |
| Mathematical Proof | Math | 8/10 | 21.7 |
| Python Data Processing | Python | 10/10 | 21.7 |

- Excellent at coding & math
- Excellent at creative writing & poetry
- Reasoning model — produces thinking blocks, needs --jinja flag
- ✅ Recommended for production use
- MatFormer (E2B) model — uses chatml template (not gemma), fixed 2026-09-02

### #12 — granite3.2-2b

| Setting | Value |
|---------|-------|
| File | `granite3.2-2b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 26.6 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 7/10 | 26.6 |
| Function Call: Email Draft | Func Call | 8/10 | 26.7 |
| Function Call: Read File | Func Call | 2/10 | 26.6 |
| Function Call: SQLite Query | Func Call | 2/10 | 26.7 |
| Function Call: Terminal Command | Func Call | 8/10 | 26.7 |
| Function Call: Web Search | Func Call | 4/10 | 26.6 |
| Function Call: Write File | Func Call | 8/10 | 26.6 |
| HTML Web Browser Game | HTML | 10/10 | 26.4 |
| HTML Profile Cards Page | HTML | 9/10 | 26.5 |
| Iambic Pentameter Poem | Creative | 7/10 | 26.7 |
| Mathematical Proof | Math | 9/10 | 26.5 |
| Python Data Processing | Python | 10/10 | 26.6 |

- Excellent at coding & math
- Fast generation (26.6 tok/s)
- ✅ Recommended for production use

### #13 — granite4.2-3b

| Setting | Value |
|---------|-------|
| File | `granite-4.2-3b-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 18.9 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 7/10 | 18.7 |
| Function Call: Email Draft | Func Call | 8/10 | 19.1 |
| Function Call: Read File | Func Call | 2/10 | 18.9 |
| Function Call: SQLite Query | Func Call | 10/10 | 18.8 |
| Function Call: Terminal Command | Func Call | 2/10 | 18.8 |
| Function Call: Web Search | Func Call | 4/10 | 18.9 |
| Function Call: Write File | Func Call | 6/10 | 18.9 |
| HTML Web Browser Game | HTML | 10/10 | 18.6 |
| HTML Profile Cards Page | HTML | 10/10 | 18.8 |
| Iambic Pentameter Poem | Creative | 6/10 | 19.0 |
| Mathematical Proof | Math | 8/10 | 18.9 |
| Python Data Processing | Python | 10/10 | 18.8 |

- Excellent at coding & math

### #14 — qwen2.5-coder-3b

| Setting | Value |
|---------|-------|
| File | `qwen2.5-coder-3b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.1 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 20.0 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 10/10 | 20.0 |
| Function Call: Email Draft | Func Call | 9/10 | 20.0 |
| Function Call: Read File | Func Call | 0/10 | 19.5 |
| Function Call: SQLite Query | Func Call | 1/10 | 19.6 |
| Function Call: Terminal Command | Func Call | 8/10 | 20.3 |
| Function Call: Web Search | Func Call | 2/10 | 20.1 |
| Function Call: Write File | Func Call | 8/10 | 20.0 |
| HTML Web Browser Game | HTML | 10/10 | 20.1 |
| HTML Profile Cards Page | HTML | 10/10 | 20.2 |
| Iambic Pentameter Poem | Creative | 7/10 | 20.0 |
| Mathematical Proof | Math | 8/10 | 20.1 |
| Python Data Processing | Python | 10/10 | 20.2 |

- Excellent at coding & math

### #15 — granite4-3b

| Setting | Value |
|---------|-------|
| File | `granite4-3b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.7 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 18.9 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 18.9 |
| Function Call: Email Draft | Func Call | 9/10 | 19.0 |
| Function Call: Read File | Func Call | 2/10 | 18.9 |
| Function Call: SQLite Query | Func Call | 8/10 | 18.8 |
| Function Call: Terminal Command | Func Call | 8/10 | 18.9 |
| Function Call: Web Search | Func Call | 2/10 | 19.0 |
| Function Call: Write File | Func Call | 1/10 | 18.7 |
| HTML Web Browser Game | HTML | 10/10 | 18.8 |
| HTML Profile Cards Page | HTML | 10/10 | 18.8 |
| Iambic Pentameter Poem | Creative | 5/10 | 19.1 |
| Mathematical Proof | Math | 8/10 | 18.9 |
| Python Data Processing | Python | 10/10 | 18.9 |

- Excellent at coding & math

### #16 — stablelm-zephyr

| Setting | Value |
|---------|-------|
| File | `stablelm-zephyr.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 26.4 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 26.4 |
| Function Call: Email Draft | Func Call | 8/10 | 27.3 |
| Function Call: Read File | Func Call | 2/10 | 27.3 |
| Function Call: SQLite Query | Func Call | 2/10 | 27.2 |
| Function Call: Terminal Command | Func Call | 2/10 | 27.0 |
| Function Call: Web Search | Func Call | 4/10 | 26.4 |
| Function Call: Write File | Func Call | 8/10 | 25.8 |
| HTML Web Browser Game | HTML | 10/10 | 25.0 |
| HTML Profile Cards Page | HTML | 10/10 | 24.7 |
| Iambic Pentameter Poem | Creative | 8/10 | 27.2 |
| Mathematical Proof | Math | 9/10 | 26.3 |
| Python Data Processing | Python | 10/10 | 26.0 |

- Excellent at coding & math
- Fast generation (26.4 tok/s)

### #17 — lfm2.5-2.6b

| Setting | Value |
|---------|-------|
| File | `lfm2.5-2.6b.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.2 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 23.8 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 8/10 | 23.7 |
| Function Call: Email Draft | Func Call | 8/10 | 23.8 |
| Function Call: Read File | Func Call | 8/10 | 23.8 |
| Function Call: SQLite Query | Func Call | 6/10 | 23.8 |
| Function Call: Terminal Command | Func Call | 2/10 | 23.9 |
| Function Call: Web Search | Func Call | 2/10 | 24.0 |
| Function Call: Write File | Func Call | 2/10 | 23.9 |
| HTML Web Browser Game | HTML | 10/10 | 23.8 |
| HTML Profile Cards Page | HTML | 10/10 | 23.9 |
| Iambic Pentameter Poem | Creative | 3/10 | 23.9 |
| Mathematical Proof | Math | 10/10 | 23.9 |
| Python Data Processing | Python | 10/10 | 23.7 |

- Excellent at coding & math

### #18 — gemma4-e2b

| Setting | Value |
|---------|-------|
| File | `gemma-4-E2B-it-Q4_K_M.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.7 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 2,048 |
| Generation Speed | 23.4 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 10/10 | 24.2 |
| Function Call: Email Draft | Func Call | 9/10 | 23.0 |
| Function Call: Read File | Func Call | 2/10 | 22.8 |
| Function Call: SQLite Query | Func Call | 1/10 | 22.6 |
| Function Call: Terminal Command | Func Call | 2/10 | 23.5 |
| Function Call: Web Search | Func Call | 2/10 | 23.5 |
| Function Call: Write File | Func Call | 0/10 | 22.3 |
| HTML Web Browser Game | HTML | 10/10 | 23.8 |
| HTML Profile Cards Page | HTML | 9/10 | 23.8 |
| Iambic Pentameter Poem | Creative | 9/10 | 23.2 |
| Mathematical Proof | Math | 8/10 | 23.8 |
| Python Data Processing | Python | 10/10 | 23.9 |

- Excellent at coding & math
- Excellent at creative writing & poetry
- Struggles with function-call JSON — produces prose instead
- Reasoning model — produces thinking blocks, needs --jinja flag
- MatFormer (E2B) model — uses chatml template (not gemma), fixed 2026-09-02

### #19 — deepseek-r1-1.5b

| Setting | Value |
|---------|-------|
| File | `deepseek-r1-1.5b.gguf` |
| Chat Template | chatml |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 0.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 4,096 |
| Generation Speed | 32.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 7/10 | 32.7 |
| Function Call: Email Draft | Func Call | 8/10 | 32.8 |
| Function Call: Read File | Func Call | 2/10 | 31.2 |
| Function Call: SQLite Query | Func Call | 2/10 | 32.5 |
| Function Call: Terminal Command | Func Call | 2/10 | 32.7 |
| Function Call: Web Search | Func Call | 2/10 | 33.1 |
| Function Call: Write File | Func Call | 2/10 | 32.5 |
| HTML Web Browser Game | HTML | 10/10 | 33.1 |
| HTML Profile Cards Page | HTML | 10/10 | 32.8 |
| Iambic Pentameter Poem | Creative | 2/10 | 32.7 |
| Mathematical Proof | Math | 10/10 | 32.9 |
| Python Data Processing | Python | 7/10 | 32.9 |

- Excellent at coding & math
- Struggles with function-call JSON — produces prose instead
- Fast generation (32.7 tok/s)
- Reasoning model — produces thinking blocks, needs --jinja flag

### #20 — ministral-3b

| Setting | Value |
|---------|-------|
| File | `ministral-3b-instruct-q5_k_m.gguf` |
| Chat Template | chatml |
| Thinking Model | No |
| Best Temperature | 0.5 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 24.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 6/10 | 24.6 |
| Function Call: Email Draft | Func Call | 5/10 | 24.7 |
| Function Call: Read File | Func Call | 2/10 | 24.7 |
| Function Call: SQLite Query | Func Call | 2/10 | 24.7 |
| Function Call: Terminal Command | Func Call | 6/10 | 24.7 |
| Function Call: Web Search | Func Call | 2/10 | 24.9 |
| Function Call: Write File | Func Call | 2/10 | 25.0 |
| HTML Web Browser Game | HTML | 7/10 | 24.7 |
| HTML Profile Cards Page | HTML | 6/10 | 24.7 |
| Iambic Pentameter Poem | Creative | 5/10 | 24.7 |
| Mathematical Proof | Math | 8/10 | 24.7 |
| Python Data Processing | Python | 8/10 | 24.7 |

- Struggles with function-call JSON — produces prose instead

### #21 — gemma2-2b

| Setting | Value |
|---------|-------|
| File | `gemma2-2b.gguf` |
| Chat Template | gemma |
| Thinking Model | No |
| Best Temperature | 0.1 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 22.3 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 6/10 | 22.2 |
| Function Call: Email Draft | Func Call | 3/10 | 22.2 |
| Function Call: Read File | Func Call | 6/10 | 22.3 |
| Function Call: SQLite Query | Func Call | 6/10 | 22.3 |
| Function Call: Terminal Command | Func Call | 6/10 | 22.3 |
| Function Call: Web Search | Func Call | 6/10 | 22.2 |
| Function Call: Write File | Func Call | 8/10 | 22.3 |
| HTML Web Browser Game | HTML | 2/10 | 22.3 |
| HTML Profile Cards Page | HTML | 1/10 | 22.3 |
| Iambic Pentameter Poem | Creative | 2/10 | 22.3 |
| Mathematical Proof | Math | 2/10 | 22.4 |
| Python Data Processing | Python | 6/10 | 22.3 |

### #22 — llama3.2-3b

| Setting | Value |
|---------|-------|
| File | `llama3.2-3b-bench.gguf` |
| Chat Template | llama3 |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 19.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 9/10 | 19.9 |
| Function Call: Email Draft | Func Call | 2/10 | 19.8 |
| Function Call: Read File | Func Call | 6/10 | 19.8 |
| Function Call: SQLite Query | Func Call | 2/10 | 19.7 |
| Function Call: Terminal Command | Func Call | 2/10 | 19.6 |
| Function Call: Web Search | Func Call | 2/10 | 19.8 |
| Function Call: Write File | Func Call | 2/10 | 19.7 |
| HTML Web Browser Game | HTML | 2/10 | 19.4 |
| HTML Profile Cards Page | HTML | 1/10 | 19.7 |
| Iambic Pentameter Poem | Creative | 1/10 | 19.7 |
| Mathematical Proof | Math | 1/10 | 19.7 |
| Python Data Processing | Python | 3/10 | 19.7 |

- Struggles with function-call JSON — produces prose instead
- ⚠️ Very poor — not recommended for production use

### #23 — gemma3-1b

| Setting | Value |
|---------|-------|
| File | `gemma3-1b.gguf` |
| Chat Template | gemma |
| Thinking Model | No |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 31.5 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 6/10 | 31.3 |
| Function Call: Email Draft | Func Call | 2/10 | 32.2 |
| Function Call: Read File | Func Call | 4/10 | 31.9 |
| Function Call: SQLite Query | Func Call | 2/10 | 31.4 |
| Function Call: Terminal Command | Func Call | 2/10 | 31.2 |
| Function Call: Web Search | Func Call | 4/10 | 31.3 |
| Function Call: Write File | Func Call | 2/10 | 31.7 |
| HTML Web Browser Game | HTML | 2/10 | 31.5 |
| HTML Profile Cards Page | HTML | 2/10 | 31.5 |
| Iambic Pentameter Poem | Creative | 1/10 | 31.5 |
| Mathematical Proof | Math | 1/10 | 30.6 |
| Python Data Processing | Python | 4/10 | 32.3 |

- Struggles with function-call JSON — produces prose instead
- Fast generation (31.5 tok/s)
- ⚠️ Very poor — not recommended for production use

### #24 — phi3-3.8b

| Setting | Value |
|---------|-------|
| File | `phi3-3.8b.gguf` |
| Chat Template | phi3 |
| Thinking Model | No |
| Best Temperature | 0.2 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 17.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 4/10 | 19.3 |
| Function Call: Email Draft | Func Call | 3/10 | 17.3 |
| Function Call: Read File | Func Call | 2/10 | 18.7 |
| Function Call: SQLite Query | Func Call | 2/10 | 17.2 |
| Function Call: Terminal Command | Func Call | 2/10 | 17.3 |
| Function Call: Web Search | Func Call | 2/10 | 17.3 |
| Function Call: Write File | Func Call | 2/10 | 17.5 |
| HTML Web Browser Game | HTML | 2/10 | 17.3 |
| HTML Profile Cards Page | HTML | 1/10 | 17.2 |
| Iambic Pentameter Poem | Creative | 4/10 | 17.3 |
| Mathematical Proof | Math | 2/10 | 17.3 |
| Python Data Processing | Python | 4/10 | 18.4 |

- Struggles with function-call JSON — produces prose instead
- ⚠️ Very poor — not recommended for production use

### #25 — llama3.2-1b

| Setting | Value |
|---------|-------|
| File | `Llama-3.2-1B-Instruct.Q4_K_M.gguf` |
| Chat Template | llama3 |
| Thinking Model | No |
| Best Temperature | 0.3 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 42.2 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 5/10 | 43.1 |
| Function Call: Email Draft | Func Call | 3/10 | 42.9 |
| Function Call: Read File | Func Call | 4/10 | 40.2 |
| Function Call: SQLite Query | Func Call | 2/10 | 41.2 |
| Function Call: Terminal Command | Func Call | 2/10 | 42.6 |
| Function Call: Web Search | Func Call | 2/10 | 40.6 |
| Function Call: Write File | Func Call | 2/10 | 40.6 |
| HTML Web Browser Game | HTML | 1/10 | 43.2 |
| HTML Profile Cards Page | HTML | 2/10 | 43.4 |
| Iambic Pentameter Poem | Creative | 4/10 | 43.3 |
| Mathematical Proof | Math | 1/10 | 41.6 |
| Python Data Processing | Python | 1/10 | 43.3 |

- Struggles with function-call JSON — produces prose instead
- Fast generation (42.2 tok/s)
- ⚠️ Very poor — not recommended for production use

### #26 — phi4-mini

| Setting | Value |
|---------|-------|
| File | `Phi-4-mini-instruct.Q4_K_M.gguf` |
| Chat Template | phi3 |
| Thinking Model | Yes (requires --jinja) |
| Best Temperature | 1.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 16.8 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 2/10 | 16.7 |
| Function Call: Email Draft | Func Call | 2/10 | 16.7 |
| Function Call: Read File | Func Call | 2/10 | 16.8 |
| Function Call: SQLite Query | Func Call | 2/10 | 17.0 |
| Function Call: Terminal Command | Func Call | 2/10 | 16.8 |
| Function Call: Web Search | Func Call | 2/10 | 16.8 |
| Function Call: Write File | Func Call | 2/10 | 17.0 |
| HTML Web Browser Game | HTML | 1/10 | 16.7 |
| HTML Profile Cards Page | HTML | 1/10 | 16.8 |
| Iambic Pentameter Poem | Creative | 4/10 | 17.2 |
| Mathematical Proof | Math | 5/10 | 16.8 |
| Python Data Processing | Python | 3/10 | 16.8 |

- Struggles with function-call JSON — produces prose instead
- Reasoning model — produces thinking blocks, needs --jinja flag
- ⚠️ Very poor — not recommended for production use

### #27 — llama3.2-3b-new

| Setting | Value |
|---------|-------|
| File | `Llama-3.2-3B-Instruct.Q4_K_M.gguf` |
| Chat Template | llama3 |
| Thinking Model | No |
| Best Temperature | 0.0 |
| Top-K | 40 |
| Top-P | 0.9 |
| Repeat Penalty | 1.1 |
| Max Tokens | 2048 |
| Context Window | 8,192 |
| Generation Speed | 19.7 tok/s |

| Prompt | Category | Score | Speed (t/s) |
|--------|----------|-------|-------------|
| Creative Writing - Short Story | Creative | 3/10 | 19.7 |
| Function Call: Email Draft | Func Call | 3/10 | 19.7 |
| Function Call: Read File | Func Call | 2/10 | 19.8 |
| Function Call: SQLite Query | Func Call | 2/10 | 19.7 |
| Function Call: Terminal Command | Func Call | 2/10 | 19.7 |
| Function Call: Web Search | Func Call | 2/10 | 19.7 |
| Function Call: Write File | Func Call | 2/10 | 19.8 |
| HTML Web Browser Game | HTML | 1/10 | 19.7 |
| HTML Profile Cards Page | HTML | 2/10 | 19.8 |
| Iambic Pentameter Poem | Creative | 4/10 | 19.8 |
| Mathematical Proof | Math | 2/10 | 19.7 |
| Python Data Processing | Python | 1/10 | 19.7 |

- Struggles with function-call JSON — produces prose instead
- ⚠️ Very poor — not recommended for production use

---

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

---

## Methodology

### Scoring System

Each prompt was scored on a 0-10 scale based on task-specific criteria:

| Category | Scoring Criteria |
|----------|------------------|
| HTML | Valid HTML structure, CSS layout (flexbox), responsive design, interactivity |
| Python | Correct algorithm, edge case handling, type hints, docstring, clean code |
| Math | Valid proof structure, logical flow, induction or direct proof |
| Poetry | Correct iambic pentameter meter, rhyme scheme, line count, thematic content |
| Creative | Narrative arc, character development, setting, prose quality |
| Function Calls | Valid JSON tool-call format (not prose), correct tool selection, proper parameters |

### Sweep Methodology

Each model was tested across multiple parameter sweeps, **one variable at a time**. Quality was always evaluated before speed - a model that produces wrong answers quickly is not useful.

| Sweep | Values Tested | Total Runs | Key Finding |
|-------|---------------|------------|-------------|
| Temperature | 0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0 (7 values) | 27 x 7 x 12 = 2,268 | 7 models peak at t=0.3, 7 at t=1.0 |
| Top-K | 20, 40, 64 (3 values) | 27 x 3 x 12 = 972 | k=40 wins 21/27 models (78%) |
| Template Fix - DeepSeek | deepseek vs chatml | DeepSeek R1 1.5B + 7B | chatml fixes DeepSeek - 3.7->5.3, 2.4->6.2 |
| Template Fix - E2B | gemma vs chatml | gemma3n-e2b + gemma4-e2b | chatml fixes E2B - 1.9->7.1, 0.8->6.0 |

### Standard Parameters (held constant)

| Parameter | Value | Notes |
|-----------|-------|-------|
| top_p | 0.9 | Nucleus sampling |
| repeat_penalty | 1.1 | Prevent repetition |
| max_tokens | 2048 | Enough for complete responses |
| GPU layers | 999 (all) | Full GPU offload |
| Flash attention | on | CUDA acceleration |

### Reports

- [`Findings_Report.pdf`](Findings_Report.pdf) - 25-page comprehensive report with all findings, per-model detail, and methodology
- [`scores/all_scores.csv`](scores/all_scores.csv) - Full 2,916-row scored dataset
- [`best_temps.json`](best_temps.json) - Locked best temperature per model

---

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

---

## Hardware

- **Device**: NVIDIA Jetson (8GB unified memory, aarch64)
- **GPU**: NVIDIA GPU with CUDA 12.6
- **RAM**: ~4.3GB available with GUI off
- **Backend**: llama.cpp with CUDA, flash attention on, full GPU offload

---

## Project Structure

```
jetson-model-zoo/
├── run_model.sh              # Model launcher with registry (27 models)
├── test_model.py             # Quick smoke test for a single model
├── eval_harness.py           # Systematic evaluation harness
├── score_results.py          # Automated quality scoring (1-10 rubric)
├── test_prompts.json         # 12 test prompts with scoring rubrics
├── run_all_tests.sh          # Batch runner for all models
├── best_temps.json           # Locked best temperature per model
├── e2b_rerun.sh              # E2B re-benchmark script (chatml fix)
├── Findings_Report.pdf       # 25-page comprehensive findings report
├── docs/
│   └── test_prompts_reference.pdf  # Printable prompt reference
├── results/                  # Raw model outputs (JSON per model)
└── scores/                   # Scored results (CSV)
```

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
- Orca-Mini 3B - quality 2.8/10, refuses tasks
- StarCoder2 3B - base model, not instruction-tuned
- CodeGemma 2B - code completion only

## Related Projects

- [LLM Transmission 8GB](https://github.com/drwjkirkpatrick-web/llm-transmission-8gb-202609) - Routing service built on this benchmark data

## License

MIT
