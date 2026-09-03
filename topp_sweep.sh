#!/usr/bin/env bash
#==============================================================================
# topp_sweep.sh — Systematic top_p sweep at 0.8 across all models × all prompts
#
# Methodology: one variable at a time (top_p). Temperature is LOCKED per model
# (see best_temps.json). top_k=40 (confirmed optimal in topk sweep). All other
# params held at baseline: repeat_penalty=1.1, max_tokens=2048.
#
# top_p=0.8 chosen to tighten the nucleus from the 0.9 baseline, targeting
# improved function_call (structured JSON) scores — the universal weakest
# category across all top-10 models.
#
# Features:
#   - Uses per-model locked temperature from best_temps.json
#   - Skips already-completed model+top_p combinations (resumable)
#   - Kills lingering llama-cli processes between runs
#   - Logs all progress to results/topp_sweep.log
#   - Auto-scores after completion
#==============================================================================
set -euo pipefail

cd "$(dirname "$0")"

# All models in the zoo (alphabetical, matches eval_harness.py registry)
MODELS=(
    deepseek-r1-1.5b
    deepseek-r1-7b
    gemma2-2b
    gemma3-1b
    gemma3n-e2b
    gemma4-e2b
    granite3.2-2b
    granite4-3b
    granite4.1-3b
    granite4.2-3b
    hermes3-3b-q4
    hermes3-3b-q5
    lfm2.5-2.6b
    llama3.2-1b
    llama3.2-3b
    llama3.2-3b-new
    ministral-3b
    ministral-3b-reasoning
    phi3-3.8b
    phi4-mini
    qwen2.5-3b
    qwen2.5-coder-3b
    qwen3-1.7b
    qwen3.5-2b
    smallthinker-3b
    smollm3
    stablelm-zephyr
)

# top_p value to test (0.9 is the existing baseline — already scored)
TOP_P=0.8

# Fixed params
TOP_K=40
MAX_TOKENS=2048
PARAM_SUFFIX="k${TOP_K}"

LOGFILE="results/topp_sweep.log"
mkdir -p results scores

TOTAL_MODELS=${#MODELS[@]}

echo "============================================" | tee "$LOGFILE"
echo "  TOP_P SWEEP" | tee -a "$LOGFILE"
echo "  Models: $TOTAL_MODELS" | tee -a "$LOGFILE"
echo "  top_p: $TOP_P (baseline 0.9 already scored)" | tee -a "$LOGFILE"
echo "  Total runs: $TOTAL_MODELS (each = 12 prompts)" | tee -a "$LOGFILE"
echo "  Temperature: LOCKED per model (best_temps.json)" | tee -a "$LOGFILE"
echo "  Fixed: top_k=$TOP_K repeat_penalty=1.1 max_tokens=$MAX_TOKENS" | tee -a "$LOGFILE"
echo "  Started: $(date)" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"

COMPLETED=0
FAILED=0
SKIPPED=0

for MODEL in "${MODELS[@]}"; do
    # Get locked temperature for this model
    TEMP=$(python3 -c "import json; d=json.load(open('best_temps.json')); print(d['models']['$MODEL'])" 2>/dev/null || echo "0.3")

    OUTFILE="results/${MODEL}_t${TEMP}_k${TOP_K}_p${TOP_P}.json"

    # Skip if already completed with all 12 prompts
    if [ -f "$OUTFILE" ]; then
        COUNT=$(python3 -c "import json; d=json.load(open('$OUTFILE')); print(len(d.get('results',[])))" 2>/dev/null || echo "0")
        if [ "$COUNT" = "12" ]; then
            echo "  SKIP: $MODEL p=$TOP_P t=$TEMP k=$TOP_K (already has 12 results)" | tee -a "$LOGFILE"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
    fi

    echo "  >>> RUN: $MODEL p=$TOP_P t=$TEMP k=$TOP_K [$(date +%H:%M:%S)]" | tee -a "$LOGFILE"

    # Run the evaluation with locked temp + top_p=0.8
    python3 eval_harness.py \
        --model "$MODEL" \
        --temp "$TEMP" \
        --top-k "$TOP_K" \
        --top-p "$TOP_P" \
        --max-tokens "$MAX_TOKENS" \
        >> "$LOGFILE" 2>&1

    if [ $? -eq 0 ]; then
        COMPLETED=$((COMPLETED + 1))
        echo "  DONE: $MODEL p=$TOP_P t=$TEMP ($COMPLETED done, $SKIPPED skipped, $FAILED failed)" | tee -a "$LOGFILE"
    else
        FAILED=$((FAILED + 1))
        echo "  FAILED: $MODEL p=$TOP_P t=$TEMP" | tee -a "$LOGFILE"
    fi

    # Kill any lingering llama processes
    pkill -9 -f "llama-cli" 2>/dev/null || true
    sleep 3

    # Progress report
    PROGRESS=$((COMPLETED + SKIPPED + FAILED))
    echo "  PROGRESS: $PROGRESS/$TOTAL_MODELS ($COMPLETED done, $SKIPPED skipped, $FAILED failed)" | tee -a "$LOGFILE"
done

echo "" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"
echo "  TOP_P SWEEP COMPLETE" | tee -a "$LOGFILE"
echo "  Completed: $COMPLETED" | tee -a "$LOGFILE"
echo "  Skipped: $SKIPPED" | tee -a "$LOGFILE"
echo "  Failed: $FAILED" | tee -a "$LOGFILE"
echo "  Finished: $(date)" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"

# Final scoring pass
python3 score_results.py --all 2>&1 | tee -a "$LOGFILE"
echo "All results scored. CSV at: scores/all_scores.csv" | tee -a "$LOGFILE"