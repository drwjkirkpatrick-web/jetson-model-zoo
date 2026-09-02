# Jetson Model Zoo — Temperature Sweep Results

Generated: 2026-09-02 07:12

## Overview

- **Models tested:** 27
- **Temperatures:** 0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0
- **Prompts per condition:** 12 (6 categories: creative, function_call, html, math, poetry, python)
- **Total scored rows:** 2268

## Full Score Matrix (sorted by best score)

| Model | t=0.0 | t=0.1 | t=0.2 | t=0.3 | t=0.5 | t=0.7 | t=1.0 | BEST | TPS |
|-------|-------|-------|-------|-------|-------|-------|-------|------|-----|
| hermes3-3b-q5 | 7.4* | 7.4* | 7.4* | **7.8* | 7.7* | 7.8* | 7.1* | **7.8**@t=0.3 | 19 |
| smallthinker-3b | 6.9* | 7.4* | 6.7* | **7.6* | 7.4* | 6.7* | 6.8* | **7.6**@t=0.3 | 20 |
| hermes3-3b-q4 | 7.2* | 7.3* | 7.3* | 7.1* | 7.2* | **7.5* | 7.4* | **7.5**@t=0.7 | 20 |
| qwen2.5-3b | 7.0* | 7.2* | 7.3* | **7.5* | 7.2* | 7.1* | 7.2* | **7.5**@t=0.3 | 20 |
| qwen3.5-2b | 7.2* | **7.5* | 7.1* | 6.8* | 6.8* | 6.5* | 7.1* | **7.5**@t=0.1 | 25 |
| granite4.1-3b | 7.0* | 6.9* | 6.6* | 7.2* | 7.2* | 7.1* | **7.4* | **7.4**@t=1.0 | 19 |
| ministral-3b-reasoning | 6.7* | 6.9* | 6.8* | **7.2* | 6.7* | 6.8* | 7.0* | **7.2**@t=0.3 | 19 |
| qwen3-1.7b | 7.0* | 6.2* | 7.0* | 6.4* | 7.1* | 7.1* | **7.2* | **7.2**@t=1.0 | 31 |
| smollm3 | 7.0* | 6.6* | 7.0* | 6.6* | 6.8* | 6.5* | **7.2* | **7.2**@t=1.0 | 21 |
| granite3.2-2b | 6.8* | 6.8* | 6.7* | **7.0* | 6.6* | 6.8* | 6.8* | **7.0**@t=0.3 | 27 |
| granite4.2-3b | 5.5* | 5.5* | 6.4* | 6.5* | 6.5* | 6.0* | **6.9* | **6.9**@t=1.0 | 19 |
| qwen2.5-coder-3b | 6.8* | **6.9* | 6.7* | 6.1* | 6.5* | 6.5* | 6.5* | **6.9**@t=0.1 | 20 |
| granite4-3b | 6.2* | 6.2* | 6.4* | 6.2* | 6.2* | **6.8* | 5.8* | **6.8**@t=0.7 | 19 |
| stablelm-zephyr | 6.3* | 6.2* | 6.2* | **6.8* | 6.2* | 6.3* | 6.4* | **6.8**@t=0.3 | 26 |
| lfm2.5-2.6b | 6.2* | 6.3* | **6.6* | 5.8* | 5.8* | 5.8* | 5.5* | **6.6**@t=0.2 | 24 |
| ministral-3b | 4.2* | 3.6* | 4.8* | 4.4* | **4.9* | 4.7* | 3.8* | **4.9**@t=0.5 | 25 |
| gemma2-2b | 4.0* | **4.5* | 3.4* | 2.5* | 2.2* | 3.7* | 3.0* | **4.5**@t=0.1 | 22 |
| deepseek-r1-1.5b | **3.7* | 1.7* | 2.5* | 2.6* | 2.5* | 2.3* | 3.1* | **3.7**@t=0.0 | 33 |
| llama3.2-3b | 2.2* | 2.2* | 1.9* | 2.5* | 2.2* | 2.2* | **2.8* | **2.8**@t=1.0 | 20 |
| gemma3-1b | 2.1* | 2.0* | 2.2* | 1.8* | 2.1* | 1.6* | **2.7* | **2.7**@t=1.0 | 32 |
| phi3-3.8b | 2.2* | 1.9* | **2.5* | 1.7* | 1.8* | 2.1* | 2.1* | **2.5**@t=0.2 | 18 |
| deepseek-r1-7b | **2.4* | 1.7* | 1.0* | 0.9* | 1.2* | 0.9* | 0.8* | **2.4**@t=0.0 | 10 |
| llama3.2-1b | 2.0* | 1.8* | 1.9* | **2.4* | 1.9* | 2.3* | 2.0* | **2.4**@t=0.3 | 42 |
| phi4-mini | 1.8* | 1.7* | 1.9* | 2.1* | 1.9* | 2.1* | **2.3* | **2.3**@t=1.0 | 17 |
| gemma3n-e2b | 2.2* | 1.9* | 2.0* | 1.9* | 1.5* | **2.2* | 1.6* | **2.2**@t=0.7 | 21 |
| llama3.2-3b-new | **2.2* | 1.9* | 1.9* | 2.1* | 2.2* | 1.9* | 2.1* | **2.2**@t=0.0 | 20 |
| gemma4-e2b | 0.3* | 0.7* | 0.7* | 0.8* | **1.2* | 0.7* | 1.0* | **1.2**@t=0.5 | 20 |

## Tier Rankings

- **Tier 1 (7.0+):** hermes3-3b-q5, smallthinker-3b, hermes3-3b-q4, qwen2.5-3b, qwen3.5-2b, granite4.1-3b, ministral-3b-reasoning, qwen3-1.7b, smollm3, granite3.2-2b
- **Tier 2 (5.0–6.9):** granite4.2-3b, qwen2.5-coder-3b, granite4-3b, stablelm-zephyr, lfm2.5-2.6b
- **Tier 3 (3.0–4.9):** ministral-3b, gemma2-2b, deepseek-r1-1.5b
- **Tier 4 (<3.0):** llama3.2-3b, gemma3-1b, phi3-3.8b, deepseek-r1-7b, llama3.2-1b, phi4-mini, gemma3n-e2b, llama3.2-3b-new, gemma4-e2b

## Category Breakdown at Best Temperature

| Model | Best T | Creative | Func Call | HTML | Math | Poetry | Python | AVG |
|-------|--------|----------|-----------|------|------|--------|--------|-----|
| hermes3-3b-q5 | 0.3 | 10.0 | 6.2 | 10.0 | 9.0 | 8.0 | 10.0 | **7.8** |
| smallthinker-3b | 0.3 | 8.0 | 7.7 | 8.5 | 9.0 | 3.0 | 8.0 | **7.6** |
| hermes3-3b-q4 | 0.7 | 8.0 | 6.3 | 9.5 | 10.0 | 5.0 | 10.0 | **7.5** |
| qwen2.5-3b | 0.3 | 9.0 | 6.2 | 9.5 | 8.0 | 8.0 | 9.0 | **7.5** |
| qwen3.5-2b | 0.1 | 9.0 | 5.5 | 10.0 | 9.0 | 9.0 | 10.0 | **7.5** |
| granite4.1-3b | 1.0 | 9.0 | 5.8 | 9.5 | 8.0 | 8.0 | 10.0 | **7.4** |
| ministral-3b-reasoning | 0.3 | 9.0 | 5.0 | 10.0 | 8.0 | 10.0 | 10.0 | **7.2** |
| qwen3-1.7b | 1.0 | 8.0 | 6.0 | 10.0 | 9.0 | 3.0 | 10.0 | **7.2** |
| smollm3 | 1.0 | 9.0 | 5.8 | 9.5 | 8.0 | 5.0 | 10.0 | **7.2** |
| granite3.2-2b | 0.3 | 7.0 | 5.3 | 9.5 | 9.0 | 7.0 | 10.0 | **7.0** |
| granite4.2-3b | 1.0 | 7.0 | 5.3 | 10.0 | 8.0 | 6.0 | 10.0 | **6.9** |
| qwen2.5-coder-3b | 0.1 | 10.0 | 4.7 | 10.0 | 8.0 | 7.0 | 10.0 | **6.9** |
| granite4-3b | 0.7 | 8.0 | 5.0 | 10.0 | 8.0 | 5.0 | 10.0 | **6.8** |
| stablelm-zephyr | 0.3 | 8.0 | 4.3 | 10.0 | 9.0 | 8.0 | 10.0 | **6.8** |
| lfm2.5-2.6b | 0.2 | 8.0 | 4.7 | 10.0 | 10.0 | 3.0 | 10.0 | **6.6** |
| ministral-3b | 0.5 | 6.0 | 3.2 | 6.5 | 8.0 | 5.0 | 8.0 | **4.9** |
| gemma2-2b | 0.1 | 6.0 | 5.8 | 1.5 | 2.0 | 2.0 | 6.0 | **4.5** |
| deepseek-r1-1.5b | 0.0 | 5.0 | 3.8 | 2.0 | 5.0 | 3.0 | 4.0 | **3.7** |
| llama3.2-3b | 1.0 | 9.0 | 2.7 | 1.5 | 1.0 | 1.0 | 3.0 | **2.8** |
| gemma3-1b | 1.0 | 6.0 | 2.7 | 2.0 | 1.0 | 1.0 | 4.0 | **2.7** |
| phi3-3.8b | 0.2 | 4.0 | 2.2 | 1.5 | 2.0 | 4.0 | 4.0 | **2.5** |
| deepseek-r1-7b | 0.0 | 3.0 | 3.7 | 0.0 | 0.0 | 3.0 | 1.0 | **2.4** |
| llama3.2-1b | 0.3 | 5.0 | 2.5 | 1.5 | 1.0 | 4.0 | 1.0 | **2.4** |
| phi4-mini | 1.0 | 2.0 | 2.0 | 1.0 | 5.0 | 4.0 | 3.0 | **2.3** |
| gemma3n-e2b | 0.7 | 4.0 | 2.3 | 0.0 | 1.0 | 3.0 | 5.0 | **2.2** |
| llama3.2-3b-new | 0.0 | 3.0 | 2.2 | 1.5 | 2.0 | 4.0 | 1.0 | **2.2** |
| gemma4-e2b | 0.5 | 1.0 | 1.3 | 0.0 | 0.0 | 6.0 | 0.0 | **1.2** |

## Key Findings

### Temperature
- Most models peak at **t=0.3** (7 models) or **t=1.0** (7 models)
- Average score across all models is nearly flat across temps (4.69–4.84)
- Low-temperature (t=0.0) favors deterministic output models (deepseek-r1, llama3.2-3b-new)
- Higher temps (t=1.0) favor creative/poetry-strong models (granite4.1-3b, qwen3-1.7b, smollm3)
- **hermes3-3b-q4** is the most temperature-stable (CV=1.8%)

### Top Performers
- **hermes3-3b-q5** wins overall (7.8 @ t=0.3) — strongest in creative(10), html(10), python(10)
- **smallthinker-3b** is best function caller (7.6 @ t=0.3) — only model scoring 10 on func_sqlite
- **qwen3.5-2b** fastest Tier 1 (25 TPS) with excellent creative/poetry (7.5 @ t=0.1)
- **qwen3-1.7b** fastest overall Tier 1 (30.8 TPS, 7.2 @ t=1.0)

### Universal Weaknesses
- **func_web_search** is hardest prompt (avg 2.28/10) — nearly all models fail
- **func_sqlite** (avg 2.78) — only smallthinker-3b masters it (10/10)
- **func_read_file** (avg 3.24) — inconsistent; half of Tier 1 scores 1-2
- **Poetry/iambic** (avg 4.34) — smallthinker-3b and qwen3-1.7b collapse to 3.0

### Best by Category (at best temp)

- **creative**: hermes3-3b-q5 (10.0/10)
- **function_call**: smallthinker-3b (7.7/10)
- **html**: granite4-3b (10.0/10)
- **math**: hermes3-3b-q4 (10.0/10)
- **poetry**: ministral-3b-reasoning (10.0/10)
- **python**: granite3.2-2b (10.0/10)

### Speed vs Quality

| Model | Score | TPS | Notes |
|-------|-------|-----|-------|
| hermes3-3b-q5 | 7.8 | 19 | Moderate, Tier 1 |
| smallthinker-3b | 7.6 | 20 | Moderate, Tier 1 |
| hermes3-3b-q4 | 7.5 | 20 | Moderate, Tier 1 |
| qwen2.5-3b | 7.5 | 20 | Moderate, Tier 1 |
| qwen3.5-2b | 7.5 | 25 | Fast, Tier 1 |
| granite4.1-3b | 7.4 | 19 | Moderate, Tier 1 |
| ministral-3b-reasoning | 7.2 | 19 | Moderate, Tier 1 |
| qwen3-1.7b | 7.2 | 31 | Very fast, Tier 1 |
| smollm3 | 7.2 | 21 | Moderate, Tier 1 |
| granite3.2-2b | 7.0 | 27 | Fast, Tier 1 |
| granite4.2-3b | 6.9 | 19 | Moderate |
| qwen2.5-coder-3b | 6.9 | 20 | Moderate |
| granite4-3b | 6.8 | 19 | Moderate |
| stablelm-zephyr | 6.8 | 26 | Fast |
| lfm2.5-2.6b | 6.6 | 24 | Fast |