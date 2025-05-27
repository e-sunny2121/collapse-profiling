#!/usr/bin/env bash
set -euo pipefail
set -x   # trace commands

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]] || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

# — build JSON payload via here-doc —
PAYLOAD=$(python3 <<EOF
import json
with open("$PROMPT","r",encoding="utf-8") as f:
    text = f.read()
print(json.dumps({
    "model": "$MODEL",
    "stream": True,
    "messages": [{"role":"user","content": text}]
}))
EOF
)

# call the API
curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="
echo

# 1) Collapse depth
echo -n "Collapse depth: "
python3 -m collapse_profiling.parse_depth < "$OUT"
echo

# 2) Structural failure
echo -n "Struct-Fail: "
python3 -m collapse_profiling.structure_parser < "$OUT"
echo

# 3) Top-token frequency
echo "Top tokens:"
python3 -m collapse_profiling.parse_freq -n 5 < "$OUT"
echo

# 4) N-gram streak collapse
echo -n "Streak-collapse (4 in a row): "
python3 -m collapse_profiling.parse_depth_streak -t 4 < "$OUT"
echo

# 5) Semantic drift
echo "Semantic drift:"
python3 -m collapse_profiling.semantic_drift_detector -w 5 \
    -f describe explain interpret summarize meaning context \
    < "$OUT"
echo

# 6) Driver Analysis
echo
echo "=== Driver analysis ==="
python3 -m collapse_profiling.driver < "$OUT"

