import sys
import json
import re
import argparse
from collections import Counter
from collapse_profiling.parsers import iterate_deltas

# refusal pattern (expand as needed)
_REFUSAL_RE = re.compile(
    r"^\s*(i(?:’|')?m sorry|i cannot|i can’t|no,? )",
    re.IGNORECASE
)

def detect_structure(stream, threshold=1):
    counts = Counter()
    depth = 0

    for token in iterate_deltas(stream):
        # refusal
        if _REFUSAL_RE.match(token):
            return {"mode": "refusal", "depth": depth, "token": token.strip()}

        # loop
        counts[token] += 1
        if counts[token] > threshold:
            return {"mode": "loop", "depth": depth, "token": token}

        depth += 1

    # finished with no repeat/refusal
    return {"mode": "stop", "depth": depth, "token": None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=1,
        help="how many times to allow the same token before declaring a loop"
    )
    args = parser.parse_args()

    result = detect_structure(sys.stdin, args.threshold)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
