# collapse_profiling/parse_freq.py

import sys
from collections import Counter
import argparse

from collapse_profiling.parsers import iterate_deltas

# a minimal stop-word list; feel free to expand
_STOP_WORDS = {
    "the","and","in","to","of","a","is","it","that","for","on",
    "with","as","was","at","by","an","be","are","this","or","from"
}

def main(top_n: int, min_count: int):
    # gather all substantive tokens up to first repeat
    tokens = [tok for tok in iterate_deltas(sys.stdin) if tok.lower() not in _STOP_WORDS]

    freqs = Counter(tokens)
    # only keep those that meet the minimum count
    common = [(tok, cnt) for tok, cnt in freqs.most_common(top_n) if cnt >= min_count]

    if not common:
        print(f"No tokens repeated at least {min_count} times.")
    else:
        for token, count in common:
            print(f"{token!r}: {count}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Show top repeated tokens (excluding stop words)")
    p.add_argument(
        "-n","--top",
        type=int, default=10,
        help="how many top tokens to display"
    )
    p.add_argument(
        "-m","--min-count",
        type=int, default=5,
        help="minimum repetition count to include"
    )
    args = p.parse_args()

    main(args.top, args.min_count)
