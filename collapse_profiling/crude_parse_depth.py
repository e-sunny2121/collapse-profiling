#!/usr/bin/env python3
"""
Enhanced collapse-depth parser for SSE streams.

Reads from stdin, normalizes each assistant "content" chunk,
counts unique non-empty tokens until a repeat threshold is hit,
then prints a summary.
"""

import sys
import json
import re
import argparse
from collections import Counter

def collapse_depth(stream, threshold=1):
    seen = set()
    counts = Counter()
    depth = 0
    first_dup = None

    for line in stream:
        if not line.startswith("data:"):
            continue

        payload = line.removeprefix("data:").strip()
        if payload == "[DONE]":
            break

        try:
            delta = json.loads(payload)["choices"][0]["delta"]
        except Exception:
            continue

        # skip pure role announcements
        if "role" in delta and not delta.get("content"):
            continue

        text = delta.get("content", "")
        # normalize: lowercase, strip whitespace, drop punctuation
        norm = re.sub(r"[^\w\s]", "", text.strip().lower())
        if not norm:
            continue

        counts[norm] += 1
        if counts[norm] > threshold:
            first_dup = norm
            break

        seen.add(norm)
        depth += 1

    return depth, first_dup, counts

def main():
    parser = argparse.ArgumentParser(
        description="Compute collapse depth from an SSE stream.")
    parser.add_argument(
        "-t", "--threshold", type=int, default=1,
        help="how many repeats trigger collapse (default=1)")
    parser.add_argument(
        "--json", action="store_true",
        help="output full metrics as JSON")
    args = parser.parse_args()

    depth, dup, counts = collapse_depth(sys.stdin, args.threshold)

    if args.json:
        out = {"depth": depth, "first_duplicate": dup, "counts": dict(counts)}
        print(json.dumps(out))
    else:
        msg = f"collapse depth = {depth}"
        if dup is not None:
            msg += f" (first_dup='{dup}' @ {counts[dup]}×)"
        print(msg)

if __name__ == "__main__":
    main()
