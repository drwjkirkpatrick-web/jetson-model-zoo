#!/usr/bin/env bash
# run_all_tests.sh — Run all 27 models through all 12 prompts at 2048 max tokens
# Saves results to results/ directory, one JSON per model

cd /home/walker/projects/jetson-model-zoo

MODELS=(
    gemma3-1b
    llama3.2-1b
    deepseek-r1-1.5b
    qwen3-1.7b
    qwen3.5-2b
    granite3.2-2b
    gemma2-2b
    stablelm-zephyr
    lfm2.5-2.6b
    qwen2.5-3b
    qwen2.5-coder-3b
    llama3.2-3b
    llama3.2-3b-new
    hermes3-3b-q4
    hermes3-3b-q5
    granite4-3b
    granite4.1-3b
    granite4.2-3b
    smollm3
    phi3-3.8b
    phi4-mini
    smallthinker-3b
    ministral-3b
    ministral-3b-reasoning
    deepseek-r1-7b
    gemma4-e2b
    gemma3n-e2b
)

TOTAL=${#MODELS[@]}
echo "=== STARTING FULL BATCH: $TOTAL models x 12 prompts, 2048 max tokens ==="
echo "=== Estimated time: ~3-4 hours ==="
echo ""

COMPLETED=0
FAILED=0

for i in "${!MODELS[@]}"; do
    MODEL="${MODELS[$i]}"
    NUM=$((i + 1))
    echo ""
    echo "### MODEL $NUM/$TOTAL: $MODEL ###"
    
    # Check if results already exist (skip completed)
    PARAM_TAG="t0.3_k40_p0.9"
    OUTFILE="results/${MODEL}_${PARAM_TAG}.json"
    
    if [ -f "$OUTFILE" ]; then
        # Check if it has all 12 prompts
        COUNT=$(python3 -c "import json; d=json.load(open('$OUTFILE')); print(len(d.get('results',[])))" 2>/dev/null)
        if [ "$COUNT" = "12" ]; then
            echo "  SKIP — already has 12 results"
            COMPLETED=$((COMPLETED + 1))
            continue
        fi
    fi
    
    # Run the model
    python3 eval_harness.py --model "$MODEL" --temp 0.3 --top-k 40 --top-p 0.9 --max-tokens 2048 2>&1
    
    if [ $? -eq 0 ]; then
        COMPLETED=$((COMPLETED + 1))
        echo "  ✓ DONE ($COMPLETED/$TOTAL completed)"
    else
        FAILED=$((FAILED + 1))
        echo "  ✗ FAILED"
    fi
    
    # Kill any lingering processes between models
    pkill -9 -f "llama-cli" 2>/dev/null
    sleep 3
done

echo ""
echo "=== BATCH COMPLETE ==="
echo "  Completed: $COMPLETED/$TOTAL"
echo "  Failed: $FAILED"
echo ""
echo "=== Scoring all results ==="
python3 score_results.py --all