# collapse_profiling/parse_freq.py
import sys
from collections import Counter
from collapse_profiling.parsers import iterate_deltas

def main(top_n=10):
    tokens = list(iterate_deltas(sys.stdin))
    freqs = Counter(tokens)
    for token, count in freqs.most_common(top_n):
        print(f"{token!r}: {count}")

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--top", type=int, default=10,
                        help="how many top tokens to display")
    args = parser.parse_args()
    main(args.top)