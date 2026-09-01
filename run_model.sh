#!/usr/bin/env bash
#==============================================================================
# run_model.sh — Launch any model in the Jetson Model Zoo via llama-server
#==============================================================================
#
# Usage:
#   ./run_model.sh <name> [port]    Start a model
#   ./run_model.sh list             List all available models
#   ./run_model.sh stop [port]      Stop running server
#
# All models run on GPU (-ngl 999) with flash attention on.
# Context is tuned per-model for 8GB Jetson unified memory.
# Thinking models automatically get --jinja flag.
#
set -euo pipefail

MODEL_DIR="${MODEL_DIR:-$HOME/models/new-zoo}"
LLAMA_SERVER="$HOME/llama.cpp/build/bin/llama-server"
PORT="${PORT:-8082}"
THREADS="${THREADS:-6}"

# ── Model registry ──────────────────────────────────────────────────────
# format: "filename|chat_template|context|thinking|display_name"
# thinking=1 adds --jinja flag
declare -A MODELS

# ── 1B class ──
MODELS[gemma3-1b]="gemma3-1b.gguf|gemma|32768|0|Gemma 3 1B"
MODELS[llama3.2-1b]="Llama-3.2-1B-Instruct.Q4_K_M.gguf|llama3|32768|0|Llama 3.2 1B (new)"

# ── 1.5B class ──
MODELS[deepseek-r1-1.5b]="deepseek-r1-1.5b.gguf|deepseek|8192|1|DeepSeek R1 1.5B"
MODELS[qwen3-1.7b]="Qwen3-1.7B.Q4_K_M.gguf|chatml|32768|0|Qwen3 1.7B (new)"
MODELS[qwen3.5-2b]="Qwen_Qwen3.5-2B-Q4_K_M.gguf|chatml|16384|1|Qwen3.5 2B (new)"

# ── 2B class ──
MODELS[granite3.2-2b]="granite3.2-2b.gguf|chatml|16384|0|Granite 3.2 2B"
MODELS[gemma2-2b]="gemma2-2b.gguf|gemma|16384|0|Gemma 2 2B"
MODELS[stablelm-zephyr]="stablelm-zephyr.gguf|chatml|16384|0|StableLM Zephyr"
MODELS[lfm2.5-2.6b]="lfm2.5-2.6b.gguf|chatml|16384|0|LFM 2.5 2.6B"

# ── 3B class ──
MODELS[qwen2.5-3b]="qwen2.5-3b.gguf|chatml|16384|0|Qwen 2.5 3B"
MODELS[qwen2.5-coder-3b]="qwen2.5-coder-3b.gguf|chatml|16384|0|Qwen2.5-Coder 3B"
MODELS[llama3.2-3b]="llama3.2-3b-bench.gguf|llama3|16384|0|Llama 3.2 3B"
MODELS[llama3.2-3b-new]="Llama-3.2-3B-Instruct.Q4_K_M.gguf|llama3|16384|0|Llama 3.2 3B (new)"
MODELS[hermes3-3b-q4]="hermes3-3b-q4.gguf|chatml|16384|0|Hermes 3 3B Q4"
MODELS[hermes3-3b-q5]="hermes3-3b-q5.gguf|chatml|16384|0|Hermes 3 3B Q5"
MODELS[granite4-3b]="granite4-3b.gguf|chatml|16384|0|Granite 4 3B"
MODELS[granite4.1-3b]="granite4.1-3b.gguf|chatml|16384|0|Granite 4.1 3B"
MODELS[granite4.2-3b]="granite-4.2-3b-Q4_K_M.gguf|chatml|16384|0|Granite 4.2 3B (new)"
MODELS[smollm3]="HuggingFaceTB_SmolLM3-3B-Q4_K_M.gguf|chatml|16384|0|SmolLM3 3B (new)"
MODELS[phi3-3.8b]="phi3-3.8b.gguf|phi3|16384|0|Phi-3 3.8B"
MODELS[phi4-mini]="Phi-4-mini-instruct.Q4_K_M.gguf|phi3|16384|1|Phi-4-mini (new)"
MODELS[smallthinker-3b]="smallthinker-3b.gguf|chatml|8192|1|SmallThinker 3B"
MODELS[ministral-3b]="ministral-3b-instruct-q5_k_m.gguf|chatml|16384|0|Ministral-3B Instruct"

# ── 7B class ──
MODELS[deepseek-r1-7b]="deepseek-r1-7b.gguf|deepseek|2048|1|DeepSeek R1 7B"

# ── E2B (MatFormer, needs reduced context) ──
MODELS[gemma3n-e2b]="gemma-3n-E2B-it-Q4_K_M.gguf|gemma|8192|1|Gemma 3n E2B (new)"
MODELS[gemma4-e2b]="gemma-4-E2B-it-Q4_K_M.gguf|gemma|2048|1|Gemma 4 E2B"

# ── Commands ────────────────────────────────────────────────────────────
if [[ "${1:-}" == "list" ]]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║          JETSON MODEL ZOO — Available Models                       ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    printf "  %-22s %-26s %6s  %6s  %5s  %s\n" "KEY" "MODEL" "SIZE" "CTX" "JINJA" "STATUS"
    echo "  ────────────────────────────────────────────────────────────────────────"
    
    for key in $(echo "${!MODELS[@]}" | tr ' ' '\n' | sort); do
        IFS='|' read -r filename template ctx thinking display <<< "${MODELS[$key]}"
        filepath="$MODEL_DIR/$filename"
        
        if [[ -f "$filepath" ]]; then
            # Follow symlinks for size
            real_size=$(du -h --dereference "$filepath" 2>/dev/null | cut -f1)
            [[ -z "$real_size" || "$real_size" == "0" ]] && real_size=$(du -hL "$filepath" 2>/dev/null | cut -f1)
            jinja_flag="no"
            [[ "$thinking" == "1" ]] && jinja_flag="yes"
            printf "  %-22s %-26s %6s  %6s  %5s  ✓\n" "$key" "$display" "$real_size" "$ctx" "$jinja_flag"
        else
            printf "  %-22s %-26s %6s  %6s  %5s  ✗ missing\n" "$key" "$display" "?" "$ctx" "?"
        fi
    done
    echo ""
    echo "  Usage: ./run_model.sh <key> [port]"
    echo "  Default port: $PORT"
    echo ""
    exit 0
fi

if [[ "${1:-}" == "stop" ]]; then
    stop_port="${2:-$PORT}"
    pid=$(pgrep -f "llama-server.*:$stop_port" 2>/dev/null || true)
    if [[ -n "$pid" ]]; then
        echo "Stopping llama-server on port $stop_port (PID $pid)..."
        kill "$pid"; sleep 1; echo "Stopped."
    else
        echo "No llama-server found on port $stop_port."
    fi
    exit 0
fi

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <model-key> [port]"
    echo "       $0 list"
    echo "       $0 stop [port]"
    echo ""
    echo "Run '$0 list' to see available models."
    exit 1
fi

MODEL_KEY="$1"
PORT="${2:-$PORT}"

if [[ -z "${MODELS[$MODEL_KEY]:-}" ]]; then
    echo "Error: Unknown model '$MODEL_KEY'"
    echo "Run '$0 list' to see available models."
    exit 1
fi

IFS='|' read -r FILENAME TEMPLATE CONTEXT THINKING DISPLAY <<< "${MODELS[$MODEL_KEY]}"
MODEL_PATH="$MODEL_DIR/$FILENAME"

if [[ ! -f "$MODEL_PATH" ]]; then
    echo "Error: Model file not found: $MODEL_PATH"
    exit 1
fi

# Stop existing server on this port
existing_pid=$(pgrep -f "llama-server.*:$PORT" 2>/dev/null || true)
if [[ -n "$existing_pid" ]]; then
    echo "Stopping existing server on port $PORT (PID $existing_pid)..."
    kill "$existing_pid" 2>/dev/null || true; sleep 1
fi

# Build command
JINJA_FLAG=""
[[ "$THINKING" == "1" ]] && JINJA_FLAG="--jinja"

echo "Starting: $DISPLAY"
echo "  File:     $FILENAME"
echo "  Size:     $(du -hL "$MODEL_PATH" | cut -f1)"
echo "  Port:     $PORT"
echo "  Context:  $CONTEXT"
echo "  Template: $TEMPLATE"
echo "  Jinja:    $([[ -n "$JINJA_FLAG" ]] && echo "yes (thinking model)" || echo "no")"
echo "  GPU:      all layers (-ngl 999)"
echo "  Flash:    on"
echo ""

exec "$LLAMA_SERVER" \
    -m "$MODEL_PATH" \
    --host 0.0.0.0 \
    --port "$PORT" \
    -c "$CONTEXT" \
    -t "$THREADS" \
    --chat-template "$TEMPLATE" \
    -ngl 999 \
    -fa on \
    $JINJA_FLAG \
    2>&1