# collapse_profiling/parse_depth_ngram.py

import sys
import json
import re
import argparse
from typing import List

from collapse_profiling.parsers import _extract_deltas

def tokenize_deltas(lines: List[str]) -> List[str]:
    """
    Pull out all raw delta strings and split them into cleaned word tokens.
    """
    deltas = _extract_deltas(lines)
    words = []
    for delta in deltas:
        words.extend(re.findall(r"\w+", delta.lower()))
    return words

def detect_ngram_loop(tokens: List[str], window: int) -> int:
    """
    Return the index where the first exact repeated n-gram of length `window`
    occurs (i.e. tokens[i:i+window] == tokens[i+window:i+2*window]).
    If none, return -1.
    """
    for i in range(len(tokens) - 2 * window + 1):
        if tokens[i : i + window] == tokens[i + window : i + 2 * window]:
            return i + window
    return -1

def main():
    p = argparse.ArgumentParser(
        description="Detect n-gram collapse in an SSE log"
    )
    p.add_argument(
        "-w", "--window", type=int, default=5,
        help="size of the n-gram (number of tokens)"
    )
    p.add_argument(
        "--min-len", type=int, default=3,
        help="minimum token length to keep (drops shorter tokens)"
    )
    p.add_argument(
        "--min-tokens", type=int, default=10,
        help="minimum number of tokens after filtering before trusting the filtered list"
    )
    args = p.parse_args()

    lines = list(sys.stdin)
    raw_tokens = tokenize_deltas(lines)

    # apply noise filter
    filtered = [t for t in raw_tokens if len(t) >= args.min_len]
    tokens = filtered if len(filtered) >= args.min_tokens else raw_tokens

    idx = detect_ngram_loop(tokens, args.window)
    if idx >= 0:
        print("Collapse depth (ngram):", idx)
    else:
        print("Collapse depth (ngram): (no loop detected)")

if __name__ == "__main__":
    main()
