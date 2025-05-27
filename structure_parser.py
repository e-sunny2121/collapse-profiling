# collapse_profiling/structure_parser.py

import sys
import json
import re
import argparse
from collections import Counter
from collapse_profiling.parsers import iterate_deltas

# refusal patterns (word‐only, anchored)
_REFUSAL_RE = re.compile(
    r"^(?:"
    r"i(?:’|'|m)?m sorry|"          # i'm sorry, i’m sorry
    r"i cannot|i can(?:’|'| not)?t|" # i cannot, i can't
    r"no\b|cannot\b|decline\b|refuse\b"
    r")",
    re.IGNORECASE
)

def detect_structure(stream, threshold=1):
    counts = Counter()
    depth = 0

    for raw_token in iterate_deltas(stream):
        token = raw_token.strip()
        if not token:
            continue

        # strip leading/trailing punctuation and lowercase
        cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", token).lower()

        # refusal check
        if _REFUSAL_RE.match(cleaned):
            return {"mode": "refusal", "depth": depth, "token": token}

        # loop detection
        depth += 1
        counts[token] += 1
        if counts[token] > threshold:
            return {"mode": "loop", "depth": depth, "token": token}

    return {"mode": "stop", "depth": depth, "token": None}


def main():
    p = argparse.ArgumentParser(
        description="Detect refusal or looping in an LLM SSE stream"
    )
    p.add_argument(
        "-t", "--threshold",
        type=int,
        default=1,
        help="how many times to allow the same token before declaring a loop"
    )
    args = p.parse_args()

    result = detect_structure(sys.stdin, args.threshold)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
