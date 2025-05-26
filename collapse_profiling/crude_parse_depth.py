"""
Tiny parser: read an SSE stream from stdin,
count how many *non-empty* content chunks arrive
before the first repeat, then print that number.

Usage:
    cat sse.log | collapse-depth
"""
import sys
import json

def collapse_depth(stream):
    seen = set()
    depth = 0

    for line in stream:
        if not line.startswith("data:"):
            continue

        payload = line.removeprefix("data:").strip()
        if payload == "[DONE]":
            break

        # parse JSON safely
        try:
            delta = json.loads(payload)["choices"][0]["delta"]
        except (json.JSONDecodeError, KeyError, IndexError):
            continue

        text = delta.get("content", "")
        norm = text.strip()
        if not norm:
            # skip empty or whitespace-only chunks
            continue

        if norm in seen:
            # we’ve seen this exact chunk before → collapse
            break

        seen.add(norm)
        depth += 1

    return depth

def main():
    depth = collapse_depth(sys.stdin)
    print(f"collapse depth = {depth}")

if __name__ == "__main__":
    main()
