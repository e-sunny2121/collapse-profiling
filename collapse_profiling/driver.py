#!/usr/bin/env python3
import sys, re, json
from collapse_profiling.full_text   import reconstruct
from collapse_profiling.normalize    import normalize
from collapse_profiling.refusal      import find_refusal
from collapse_profiling.semantic_loop import find_drift
from collapse_profiling.drift_embedding import detect_embedding_drift
from collapse_profiling.structural_metrics import all_structural_metrics

# 1) Reconstruct & normalize
raw   = list(sys.stdin)
full  = reconstruct(raw)
clean = normalize(full)

print("=== FULL OUTPUT ===")
print(clean[:500] + ("…" if len(clean)>500 else ""))

# 2) Refusal
ref = find_refusal(clean)
print("Refusal sentence:", ref or "<none>")

# 3) Semantic n-gram loop
sents = re.split(r"[.!?]\s+", clean)
idx, sim = find_drift(sents, threshold=0.95)
if idx:
    print(f"Semantic loop at sentence {idx} (cos={sim:.3f})")
else:
    print("No semantic loop")

# 4) SBERT-style embedding drift
#    (prints any windowed cosine drops below your chosen cutoff)
print("\n=== Embedding Drift ===")
detect_embedding_drift(full, window_tokens=100, cos_thresh=0.80)

print("=== Structural Metrics ===")
print(json.dumps(all_structural_metrics(clean), indent=2))