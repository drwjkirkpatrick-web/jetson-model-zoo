#!/usr/bin/env bash
#==============================================================================
# topk_sweep.sh — Systematic top_k sweep across all models × all prompts
#
# Methodology: one variable at a time (top_k). Temperature is now LOCKED per
# model (see best_temps.json). All other params held at baseline:
# top_p=0.9, repeat_penalty=1.1, max_tokens=2048.
#
# top_k values tested: 20, 64
#   - top_k=20: Qwen official recommendation (Qwen3/Qwen3.5 model cards)
#   - top_k=64: Gemma official recommendation (Gemma 3/4 model cards)
#   - top_k=40: existing baseline (already scored in temp sweep)
#
# Features:
#   - Uses per-model locked temperature from best_temps.json
#   - Skips already-completed model+top_k combinations (resumable)
#   - Kills lingering llama-cli processes between runs
#   - Logs all progress to results/topk_sweep.log
#   - Auto-scores after each top_k value completes
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

# top_k values to test (40 is the existing baseline — already scored)
TOPK_VALUES=(20 64)

# Fixed params
TOP_P=0.9
MAX_TOKENS=2048
PARAM_SUFFIX="p${TOP_P}"

LOGFILE="results/topk_sweep.log"
mkdir -p results scores

TOTAL_MODELS=${#MODELS[@]}
TOTAL_KS=${#TOPK_VALUES[@]}
TOTAL_RUNS=$((TOTAL_MODELS * TOTAL_KS))

echo "============================================" | tee "$LOGFILE"
echo "  TOP_K SWEEP" | tee -a "$LOGFILE"
echo "  Models: $TOTAL_MODELS" | tee -a "$LOGFILE"
echo "  top_k values: ${TOPK_VALUES[*]}" | tee -a "$LOGFILE"
echo "  Total runs: $TOTAL_RUNS (each = 12 prompts)" | tee -a "$LOGFILE"
echo "  Temperature: LOCKED per model (best_temps.json)" | tee -a "$LOGFILE"
echo "  Fixed: top_p=$TOP_P max_tokens=$MAX_TOKENS" | tee -a "$LOGFILE"
echo "  Started: $(date)" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"

COMPLETED=0
FAILED=0
SKIPPED=0

for TOPK in "${TOPK_VALUES[@]}"; do
    echo "" | tee -a "$LOGFILE"
    echo "########## TOP_K: $TOPK ##########" | tee -a "$LOGFILE"
    echo "Started: $(date)" | tee -a "$LOGFILE"

    for MODEL in "${MODELS[@]}"; do
        # Get locked temperature for this model
        TEMP=$(python3 -c "import json; d=json.load(open('best_temps.json')); print(d['models']['$MODEL'])" 2>/dev/null || echo "0.3")

        OUTFILE="results/${MODEL}_t${TEMP}_k${TOPK}_${PARAM_SUFFIX}.json"

        # Skip if already completed with all 12 prompts
        if [ -f "$OUTFILE" ]; then
            COUNT=$(python3 -c "import json; d=json.load(open('$OUTFILE')); print(len(d.get('results',[])))" 2>/dev/null || echo "0")
            if [ "$COUNT" = "12" ]; then
                echo "  SKIP: $MODEL k=$TOPK t=$TEMP (already has 12 results)" | tee -a "$LOGFILE"
                SKIPPED=$((SKIPPED + 1))
                continue
            fi
        fi

        echo "  >>> RUN: $MODEL k=$TOPK t=$TEMP [$(date +%H:%M:%S)]" | tee -a "$LOGFILE"

        # Run the evaluation with locked temp
        python3 eval_harness.py \
            --model "$MODEL" \
            --temp "$TEMP" \
            --top-k "$TOPK" \
            --top-p "$TOP_P" \
            --max-tokens "$MAX_TOKENS" \
            >> "$LOGFILE" 2>&1

        if [ $? -eq 0 ]; then
            COMPLETED=$((COMPLETED + 1))
            echo "  DONE: $MODEL k=$TOPK t=$TEMP ($COMPLETED done, $SKIPPED skipped)" | tee -a "$LOGFILE"
        else
            FAILED=$((FAILED + 1))
            echo "  FAILED: $MODEL k=$TOPK t=$TEMP" | tee -a "$LOGFILE"
        fi

        # Kill any lingering llama processes
        pkill -9 -f "llama-cli" 2>/dev/null || true
        sleep 3

        # Progress report
        PROGRESS=$((COMPLETED + SKIPPED + FAILED))
        echo "  PROGRESS: $PROGRESS/$TOTAL_RUNS runs ($COMPLETED done, $SKIPPED skipped, $FAILED failed)" | tee -a "$LOGFILE"
    done

    # Score this top_k value's results
    echo "" | tee -a "$LOGFILE"
    echo "  Scoring top_k=$TOPK results..." | tee -a "$LOGFILE"
    python3 score_results.py --all >> "$LOGFILE" 2>&1 || true
    echo "  Scoring complete for top_k=$TOPK" | tee -a "$LOGFILE"
done

echo "" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"
echo "  TOP_K SWEEP COMPLETE" | tee -a "$LOGFILE"
echo "  Completed: $COMPLETED" | tee -a "$LOGFILE"
echo "  Skipped: $SKIPPED" | tee -a "$LOGFILE"
echo "  Failed: $FAILED" | tee -a "$LOGFILE"
echo "  Finished: $(date)" | tee -a "$LOGFILE"
echo "============================================" | tee -a "$LOGFILE"

# Final scoring pass
python3 score_results.py --all 2>&1 | tee -a "$LOGFILE"
echo "All results scored. CSV at: scores/all_scores.csv" | tee -a "$LOGFILE"
