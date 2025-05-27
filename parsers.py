# collapse_profiling/parsers.py
import json, sys

def iterate_deltas(stream):
    """
    Yield each non-empty 'delta' chunk from an SSE log.
    Stops when it sees the first repeated delta.
    """
    seen = set()
    for raw in stream:
        line = raw.strip()
        if line == "data: [DONE]":
            return
        if     line.startswith("data:"):   payload = line[len("data:"):].strip()
        elif   line.startswith("{"):       payload = line
        else:                              continue

        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue

        # OpenAI-style
        delta = ""
        if "choices" in obj:
            delta = obj["choices"][0].get("delta", {}).get("content", "")
        # Anthropic variants
        elif obj.get("type") == "content_block_delta":
            delta = obj.get("delta", {}).get("text", "")
        elif obj.get("type") == "content_block_start":
            delta = obj.get("content_block", {}).get("text", "")
        elif "completion" in obj:
            delta = obj["completion"].get("content", "")

        if not isinstance(delta, str):
            continue
        token = delta.strip()
        if not token:
            continue

        # first repeat = stop‐depth
        if token in seen:
            return
        seen.add(token)
        yield token
