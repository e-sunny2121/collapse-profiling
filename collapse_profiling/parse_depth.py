# collapse_profiling/parse_depth.py

import sys
from collapse_profiling.parsers import iterate_deltas

def main():
    """
    Read an SSE log from stdin, count how many unique 'delta' tokens
    appear before the first repeat, and print the collapse depth.
    """
    count = sum(1 for _ in iterate_deltas(sys.stdin))
    print("Collapse depth:", count)

if __name__ == "__main__":
    main()
