import sys
import json
import argparse
from collapse_profiling.parsers import iterate_deltas

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
    count       = 0  # number of unique deltas before the streak threshold

    for delta in iterate_deltas(sys.stdin):
        # New delta starts a fresh streak
        if delta != streak_text:
            streak_text = delta
            streak_len  = 1
            count      += 1
        else:
            # Same as previous, extend the streak
            streak_len += 1

        # If we’ve seen this delta `threshold` times in a row, stop
        if streak_len >= args.threshold:
            break

    print(f"Collapse depth (streak): {count}")

if __name__ == "__main__":
    main()
