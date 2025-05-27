# collapse_profiling/parse_depth_streak.py

import sys
import json
import argparse
from collapse_profiling.parsers import all_deltas

def main():
    p = argparse.ArgumentParser(
        description="Detect collapse when the same delta repeats N times in a row"
    )
    p.add_argument(
        "-t", "--threshold",
        type=int,
        default=3,
        help="number of identical deltas in a row to declare a collapse"
    )
    args = p.parse_args()

    streak_text = None
    streak_len  = 0
    count       = 0  # number of deltas seen before the streak threshold

    # iterate the *entire* stream, not stopping on first repeat
    for delta in all_deltas(sys.stdin):
        # start a new streak when delta changes
        if delta != streak_text:
            streak_text = delta
            streak_len  = 1
            count      += 1
        else:
            # same as last time, extend the streak
            streak_len += 1

        # once we've seen `threshold` in a row, bail out
        if streak_len >= args.threshold:
            break

    print(f"Collapse depth (streak): {count}")

if __name__ == "__main__":
    main()
