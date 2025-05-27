#!/usr/bin/env python3
import sys, json, argparse
from collections import deque
import statistics

def parse_sse(stream):
    """
    Yield (token:str, logprob:float) for each delta chunk.
    """
    for raw in stream:
        line = raw.strip()
        if not (line.startswith("data:") or line.startswith("{")):
            continue
        payload = line[len("data:"):].strip() if line.startswith("data:") else line
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue
        # each chunk has .choices[0].delta.content and .choices[0].delta.logprobs
        choice = obj.get("choices", [{}])[0]
        delta = choice.get("delta", {})
        token = delta.get("content")
        lp = delta.get("logprobs", {}).get("token_logprobs", [None])[0]
        if token is not None and lp is not None:
            yield token, lp

def main():
    p = argparse.ArgumentParser(
      description="Flag any token whose logprob is >Mσ below the rolling mean of the last N tokens"
    )
    p.add_argument("-w","--window", type=int, default=50,
                   help="rolling window size")
    p.add_argument("-s","--sigmas", type=float, default=3.0,
                   help="threshold in σ below the mean")
    args = p.parse_args()

    buf = deque(maxlen=args.window)
    for i, (tok, lp) in enumerate(parse_sse(sys.stdin), 1):
        # initialize
        if len(buf) < args.window:
            buf.append(lp)
            continue

        μ = statistics.mean(buf)
        σ = statistics.pstdev(buf)
        if lp < μ - args.sigmas * σ:
            print(f"[{i:4d}] OUTLIER token={tok!r}  logprob={lp:.3f}  (μ={μ:.3f}, σ={σ:.3f})")
        buf.append(lp)

if __name__=="__main__":
    main()
