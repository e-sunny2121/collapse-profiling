#!/usr/bin/env python3
"""
view_log.py  —  skim an SSE log without drowning

Usage
-----
    python view_log.py [log_file] [max_chunks]

    log_file    Path to .sse / .log file (default: ./sse.log)
    max_chunks  How many text chunks to print (default: 150)

Works with:
  • Anthropic streams  (content_block_delta → delta.text)
  • OpenAI streams     (choices[].delta.content)
  • Any newline-JSON file that has .content or .text fields
"""

import json, itertools, pathlib, re, sys

# --------------------------------------------------------------------------- CLI
log_path   = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("sse.log")
max_chunks = int(sys.argv[2])          if len(sys.argv) > 2 else 150

# -------------------------------------------------------------------- extractors
def extract_text(payload: dict) -> str:
    """
    Return the human text from a streaming payload, or "" if none.
    Supports Anthropic + OpenAI formats.
    """
    # Anthropic — content_block_delta
    if payload.get("type") == "content_block_delta":
        return payload.get("delta", {}).get("text", "")

    # OpenAI — chat completion chunk
    if "choices" in payload:
        return payload["choices"][0].get("delta", {}).get("content", "")

    # Generic — plain delta.content or content
    return (
        payload.get("delta", {}).get("content")
        or payload.get("content")
        or ""
    )

# ---------------------------------------------------------------------- display
try:
    with log_path.open() as f:
        printed = 0
        for line in f:
            if not line.startswith("data:"):
                continue                         # skip 'event:' lines etc.

            raw = re.sub(r"^data:\s*", "", line)
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue                         # malformed chunk → ignore

            text = extract_text(payload)
            if text:
                print(text, end="", flush=True)
                printed += 1
                if printed >= max_chunks:
                    break

except FileNotFoundError:
    sys.exit(f"✘ No such log file: {log_path}")
