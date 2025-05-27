#!/usr/bin/env python3
import sys
import json
import argparse
from collections import deque
import statistics

def parse_sse(stream):
    """
    Yield (token: str, logprob: float) for each delta chunk.
    Only considers lines starting with `data:` or raw JSON (`{…}`).
    """
    for raw in stream:
        line = raw.strip()

        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
        elif line.startswith("{"):
            payload = line
        else:
            continue

        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue

        choice = obj.get("choices", [{}])[0]
        delta  = choice.get("delta", {})

        token = delta.get("content")
        # try delta.logprobs first, then choice.logprobs
        lp = (delta.get("logprobs") or {}).get("token_logprobs", [None])[0]
        if lp is None:
            lp = (choice.get("logprobs") or {}).get("token_logprobs", [None])[0]

        if token is not None and lp is not None:
            yield token, lp

def detect_logprob_anomalies(lines, window=50, sigma_thresh=3.0):
    """
    Scan the raw SSE lines (with logprobs) and print any token
    whose logprob is more than `sigma_thresh` below the rolling mean.
    """
    buf = deque(maxlen=window)
    for i, (tok, lp) in enumerate(parse_sse(lines), start=1):
        # warm up the buffer until we have `window` values
        if len(buf) < window:
            buf.append(lp)
            continue

        μ = statistics.mean(buf)
        σ = statistics.pstdev(buf)
        if lp < μ - sigma_thresh * σ:
            print(f"[{i:4d}] OUTLIER token={tok!r}  "
                  f"logprob={lp:.3f}  (μ={μ:.3f}, σ={σ:.3f})")
        buf.append(lp)

def main():
    p = argparse.ArgumentParser(
        description="Flag tokens whose logprob is >Mσ below the rolling mean of the last N tokens"
    )
    p.add_argument("-w","--window", type=int, default=50,
                   help="rolling window size")
    p.add_argument("-s","--sigmas", type=float, default=3.0,
                   help="threshold in σ below the mean")
    args = p.parse_args()

    # run over stdin
    detect_logprob_anomalies(sys.stdin, window=args.window, sigma_thresh=args.sigmas)

if __name__ == "__main__":
    main()
