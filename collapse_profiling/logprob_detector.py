import json, sys
from collections import deque
import statistics

def detect_logprob_anomalies(raw_sse_lines, window=50, sigma_thresh=3.0):
    buf = deque()
    for raw in raw_sse_lines:
        line = raw.strip()
        if not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        obj = json.loads(payload)
        choice = obj["choices"][0]
        delta = choice.get("delta", {})
        tok = delta.get("content", "").strip()
        lp = delta.get("logprobs", {}).get("token_logprobs", [None])[0]
        if tok and lp is not None:
            buf.append(lp)
            if len(buf) > window:
                buf.popleft()
            if len(buf) == window:
                mu = statistics.mean(buf)
                sigma = statistics.pstdev(buf)
                if lp < mu - sigma_thresh * sigma:
                    print(f"  anomaly: {tok!r} lp={lp:.2f} (μ={mu:.2f},σ={sigma:.2f})")
