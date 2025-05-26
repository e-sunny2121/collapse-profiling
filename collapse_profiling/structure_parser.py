#!/usr/bin/env python3
"""
structural_parser.py

Read an SSE stream, then emit the first structural failure you see:
  - loop: when a chunk repeats over threshold
  - refusal: when a refusal phrase shows up
  - stop: when finish_reason=="stop" with no loops/refusal first
  - drift: when a semantic check fails (hook in your semantic_drift_detector)
  - tool-call: when a "tool" delta appears

Prints a JSON object:
  {"mode":"loop"|"refusal"|...,
   "depth":<num_chunks_seen>,
   "token":<the chunk that triggered it>,
   "extra":{…}}
"""

import sys, json, re, argparse
from collections import Counter

# refusal patterns (you can expand this)
_REFUSAL_RE = re.compile(r"^\s*(i(?:’|')?m sorry|i cannot|i can’t|no,? )", re.IGNORECASE)

def detect_structure(stream, threshold=1):
    seen = set()
    counts = Counter()
    depth = 0

    for line in stream:
        if not line.startswith("data:"):
            continue
        payload = line.removeprefix("data:").strip()
        if payload == "[DONE]":
            return {"mode":"stop","depth":depth,"token":None}

        # parse JSON
        try:
            obj = json.loads(payload)
            choice = obj.get("choices",[{}])[0]
            delta = choice.get("delta",{})
        except:
            continue

        # tool‐call check
        if "tool" in delta:
            return {"mode":"tool-call","depth":depth,"token":delta["tool"]}

        # refusal check
        text = delta.get("content","") or ""
        if _REFUSAL_RE.match(text):
            return {"mode":"refusal","depth":depth,"token":text.strip()}

        # normalize token
        token = re.sub(r"[^\w\s]","", text.strip().lower())
        if not token:
            continue

        # loop check
        counts[token] += 1
        if counts[token] > threshold:
            return {"mode":"loop","depth":depth,"token":token}

        seen.add(token)
        depth += 1

        # semantic drift could go here:
        # if drift_detector.violate(text):
        #     return {"mode":"drift","depth":depth,"token":text.strip()}

    # if we exit the loop without DONE
    return {"mode":"eof","depth":depth,"token":None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-t","--threshold", type=int, default=1)
    args = p.parse_args()

    result = detect_structure(sys.stdin, args.threshold)
    print(json.dumps(result))


if __name__=="__main__":
    main()
