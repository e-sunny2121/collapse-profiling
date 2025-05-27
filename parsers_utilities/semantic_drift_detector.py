# collapse_profiling/semantic_drift.py

import sys
import re
import json
import argparse
from collapse_profiling.parsers import iterate_deltas
from typing import List

def tokenize(text: str) -> List[str]:
    """Split text into lowercase word tokens, stripping punctuation."""
    return re.findall(r"\b\w+\b", text.lower())

def detect_loop(tokens: List[str], window: int) -> int:
    """
    Return the index at which a repeated window of length `window` first occurs.
    If no loop is found, return -1.
    """
    for i in range(len(tokens) - 2 * window):
        if tokens[i : i + window] == tokens[i + window : i + 2 * window]:
            return i + window
    return -1

def compute_semantic_drift(output: str, forbidden: List[str], window: int) -> dict:
    """
    Compute drift metrics:
      - tokens_before_loop: number of tokens before the first repeated window
      - forbidden_count: number of forbidden tokens in that prefix
      - semantic_drift: forbidden_count / tokens_before_loop (0 if no tokens)
    """
    tokens = tokenize(output)
    loop_idx = detect_loop(tokens, window)
    if loop_idx == -1:
        loop_idx = len(tokens)

    pre_loop = tokens[:loop_idx]
    forbidden_count = sum(1 for t in pre_loop if t in forbidden)
    drift_score = forbidden_count / len(pre_loop) if pre_loop else 0.0

    return {
        "tokens_before_loop": loop_idx,
        "forbidden_count": forbidden_count,
        "semantic_drift": drift_score
    }

def main():
    p = argparse.ArgumentParser(
        description="Compute semantic drift from an LLM SSE log."
    )
    p.add_argument(
        "-w", "--window",
        type=int,
        default=10,
        help="ngram window size for detecting repeated sequences"
    )
    p.add_argument(
        "-f", "--forbidden",
        nargs="+",
        default=["describe","explain","summarize","context","meaning","interpret"],
        help="list of tokens considered 'forbidden' under prompt constraints"
    )
    args = p.parse_args()

    # Reconstruct the full streamed output
    full_output = "".join(iterate_deltas(sys.stdin))

    result = compute_semantic_drift(full_output, args.forbidden, args.window)
    # Print as JSON for easy downstream parsing
    print(json.dumps(result))

if __name__ == "__main__":
    main()
