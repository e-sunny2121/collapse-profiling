#!/usr/bin/env python3
import sys, re
from collapse_profiling.full_text import reconstruct
from collapse_profiling.normalize import normalize
from collapse_profiling.refusal import find_refusal
from collapse_profiling.semantic_loop import find_drift

raw = list(sys.stdin)
full = reconstruct(raw)
clean = normalize(full)

print("=== FULL OUTPUT ===")
print(clean[:500] + ("…" if len(clean)>500 else ""))

# refusal
ref = find_refusal(clean)
print("Refusal sentence:", ref or "<none>")

# semantic-drift
sents = re.split(r"[.!?]\s+", clean)
idx, sim = find_drift(sents, threshold=0.95)
print(f"Semantic loop at sentence {idx} (cos={sim})" if idx else "No semantic loop")