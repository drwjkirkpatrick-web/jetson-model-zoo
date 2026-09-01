#!/usr/bin/env python3
"""Quick smoke test for a model served by llama-server.

Sends a simple prompt and prints the response + timing.

Usage:
    python3 test_model.py granite         # test on default port 8082
    python3 test_model.py granite 9090    # test on custom port
"""
import sys
import time
import urllib.request
import urllib.error
import json

def test_model(port: int = 8082, prompt: str = "What is 2+2? Explain in one sentence."):
    url = f"http://localhost:{port}/v1/chat/completions"
    payload = json.dumps({
        "model": "test",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Be concise."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 256,
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    print(f"Sending prompt to port {port}...")
    print(f"  Prompt: {prompt}")
    print()

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"Error: Cannot connect to port {port} - {e}")
        print("Is the model server running? Start it with: ./run_model.sh <model-name>")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

    elapsed = time.time() - t0
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    usage = data.get("usage", {})

    print(f"Response ({elapsed:.1f}s):")
    print(f"  {content}")
    print()
    print(f"Tokens: {usage.get('prompt_tokens', '?')} prompt, "
          f"{usage.get('completion_tokens', '?')} completion, "
          f"{usage.get('total_tokens', '?')} total")
    if elapsed > 0 and usage.get("completion_tokens"):
        tps = usage["completion_tokens"] / elapsed
        print(f"Speed: {tps:.1f} tokens/sec")
    print()
    return True

if __name__ == "__main__":
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8082
    prompt = sys.argv[3] if len(sys.argv) > 3 else "What is 2+2? Explain in one sentence."
    model = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    print(f"=== Testing {model} ===")
    test_model(port, prompt)