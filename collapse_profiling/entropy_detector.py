import sys
import json
import math
import argparse
from collections import Counter
from collapse_profiling.parsers import iterate_words

def shannon_entropy(counter: Counter) -> float:
    total = sum(counter.values())
    ent = 0.0
    for freq in counter.values():
        p = freq / total
        ent -= p * math.log2(p)
    return ent

def main():
    p = argparse.ArgumentParser(
        description="Watch for low‐entropy (repetitive) windows in word stream"
    )
    p.add_argument(
        "-w", "--window", type=int, default=75,
        help="size of the sliding window (number of tokens)"
    )
    p.add_argument(
        "-t", "--threshold", type=float, default=2.0,
        help="entropy threshold below which to flag repetition"
    )
    args = p.parse_args()

    window = []
    counter = Counter()

    for w in iterate_words(sys.stdin):
        window.append(w)
        counter[w] += 1

        if len(window) > args.window:
            old = window.pop(0)
            counter[old] -= 1
            if counter[old] == 0:
                del counter[old]

        if len(window) == args.window:
            ent = shannon_entropy(counter)
            if ent < args.threshold:
                print(json.dumps({
                    "mode": "low_entropy",
                    "at_token": len(counter) + 1,
                    "entropy": ent,
                    "window": list(window)
                }))
                return

    print(json.dumps({"mode":"ok","entropy": shannon_entropy(counter)}))

if __name__ == "__main__":
    main()
