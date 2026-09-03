#!/bin/bash
# E2B re-benchmark: temp sweep + top_k sweep for both E2B models
# Uses chatml template (fixed from gemma)

set -e
cd ~/projects/jetson-model-zoo

MODELS="gemma3n-e2b gemma4-e2b"
TEMPS="0.0 0.1 0.2 0.3 0.5 0.7 1.0"
TOPKS="20 40 64"

echo "=== E2B RE-BENCHMARK (chatml fix) ==="
echo "Start: $(date)"

for MODEL in $MODELS; do
    echo ""
    echo "=== TEMPERATURE SWEEP: $MODEL ==="
    for TEMP in $TEMPS; do
        TAG="t${TEMP}_k40_p0.9"
        OUTFILE="results/${MODEL}_${TAG}.json"
        if [ -f "$OUTFILE" ]; then
            echo "  SKIP $MODEL $TAG (exists)"
        else
            echo "  RUN  $MODEL temp=$TEMP k=40 ..."
            python3 eval_harness.py --model $MODEL --temp $TEMP --top-k 40 --top-p 0.9 \
                --max-tokens 2048 --prompts html_profiles,html_game,python_code,iambic_pentameter,math_proof,creative_writing,func_web_search,func_terminal,func_write_file,func_read_file,func_sqlite,func_email \
                > /dev/null 2>&1 && echo "    DONE" || echo "    FAILED"
        fi
    done
done

echo ""
echo "=== SCORING TEMP SWEEP ==="
python3 score_results.py --all 2>/dev/null || echo "scoring done"

# Determine best temp per model from scores
echo ""
echo "=== BEST TEMPS ==="
for MODEL in $MODELS; do
    BEST_TEMP=$(python3 -c "
import csv, json
with open('scores/all_scores.csv', newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['model']=='$MODEL']
temp_scores = {}
for r in rows:
    try:
        p = json.loads(r.get('params','') or '{}')
        if p.get('top_k') == 40:
            t = p.get('temp',-1)
            temp_scores.setdefault(t, []).append(float(r['score']))
    except: pass
for t in sorted(temp_scores):
    avg = sum(temp_scores[t])/len(temp_scores[t])
    print(f'  $MODEL t={t}: avg={avg:.2f} n={len(temp_scores[t])}')
best = max(temp_scores, key=lambda t: sum(temp_scores[t])/len(temp_scores[t]))
print(f'  BEST: $MODEL t={best}')
print(best)
" 2>/dev/null)
    echo "$BEST_TEMP"
done

echo ""
echo "=== TOP_K SWEEP ==="
for MODEL in $MODELS; do
    # Get best temp for this model
    BEST_TEMP=$(python3 -c "
import csv, json
with open('scores/all_scores.csv', newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['model']=='$MODEL']
temp_scores = {}
for r in rows:
    try:
        p = json.loads(r.get('params','') or '{}')
        if p.get('top_k') == 40:
            t = p.get('temp',-1)
            temp_scores.setdefault(t, []).append(float(r['score']))
    except: pass
best = max(temp_scores, key=lambda t: sum(temp_scores[t])/len(temp_scores[t]))
print(f'{best}')
" 2>/dev/null)
    
    echo "  $MODEL best_temp=$BEST_TEMP"
    
    for K in $TOPKS; do
        TAG="t${BEST_TEMP}_k${K}_p0.9"
        OUTFILE="results/${MODEL}_${TAG}.json"
        if [ -f "$OUTFILE" ]; then
            echo "    SKIP $MODEL $TAG (exists)"
        else
            echo "    RUN  $MODEL temp=$BEST_TEMP k=$K ..."
            python3 eval_harness.py --model $MODEL --temp $BEST_TEMP --top-k $K --top-p 0.9 \
                --max-tokens 2048 --prompts html_profiles,html_game,python_code,iambic_pentameter,math_proof,creative_writing,func_web_search,func_terminal,func_write_file,func_read_file,func_sqlite,func_email \
                > /dev/null 2>&1 && echo "      DONE" || echo "      FAILED"
        fi
    done
done

echo ""
echo "=== FINAL SCORING ==="
python3 score_results.py --all 2>/dev/null || echo "scoring done"

echo ""
echo "=== RESULTS SUMMARY ==="
for MODEL in $MODELS; do
    python3 -c "
import csv, json
with open('scores/all_scores.csv', newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['model']=='$MODEL']
print(f'$MODEL: {len(rows)} scored rows')
# Group by temp+k
combos = {}
for r in rows:
    try:
        p = json.loads(r.get('params','') or '{}')
        key = f\"t={p.get('temp','?')}_k={p.get('top_k','?')}\"
        combos.setdefault(key, []).append(float(r['score']))
    except: pass
for key in sorted(combos):
    vals = combos[key]
    print(f'  {key}: avg={sum(vals)/len(vals):.2f} min={min(vals):.0f} max={max(vals):.0f} n={len(vals)}')
" 2>/dev/null
done

echo ""
echo "=== E2B RE-BENCHMARK COMPLETE ==="
echo "End: $(date)"