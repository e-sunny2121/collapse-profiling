"""
Tiny parser: read an SSE stream from stdin,
count how many chunks arrive before the first exact repeat,
print that number.

Usage:
    cat sse.log | collapse-depth
"""
import sys
import json

def collapse_depth(stream):
    seen = set()
    depth = 0
    for line in stream:
        if not line.startswith("data:"):          # skip pings etc.
            continue
        payload = line.removeprefix("data:").strip()
        if payload == "[DONE]":
            break
        text = json.loads(payload)["choices"][0]["delta"].get("content", "")
        if text in seen:
            break
        seen.add(text)
        depth += 1
    return depth

def main():
    depth = collapse_depth(sys.stdin)
    print(f"collapse depth = {depth}")

if __name__ == "__main__":
    main()
