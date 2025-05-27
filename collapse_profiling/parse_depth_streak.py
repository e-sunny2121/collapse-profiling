# collapse_profiling/parse_depth_streak.py

import sys
import argparse
from collapse_profiling.parsers import all_deltas, iterate_words

def main():
    p = argparse.ArgumentParser(
        description="Detect collapse when the same token repeats N times in a row"
    )
    p.add_argument(
        "-t", "--threshold",
        type=int,
        default=3,
        help="number of identical tokens in a row to declare a collapse"
    )
    p.add_argument(
        "--words",
        action="store_true",
        help="run streak detection at the word level instead of the raw delta level"
    )
    args = p.parse_args()

    streak_text = None
    streak_len  = 0
    count       = 0

    iterator = iterate_words if args.words else all_deltas

    for token in iterator(sys.stdin):
        if token != streak_text:
            streak_text = token
            streak_len  = 1
            count      += 1
        else:
            streak_len += 1

        if streak_len >= args.threshold:
            break

    label = "words" if args.words else "deltas"
    print(f"Collapse depth (streak over {label}): {count}")

if __name__ == "__main__":
    main()
