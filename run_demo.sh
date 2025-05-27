#!/usr/bin/env bash
set -euo pipefail
set -x

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).jsonl"

[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]] || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

# Build our chat‐style payload
read -r -d '' PAYLOAD <<EOF
$(
  python3 - <<PYCODE
import json
p = open("$PROMPT", "r", encoding="utf-8").read()
print(json.dumps({
  "model": "$MODEL",
  "stream": true,
  "messages": [{"role":"user","content": p}]
}))
PYCODE
)
EOF

# Fire off the Chat completion
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
python3 -m collapse_profiling.semantic_drift_detector \
    -w 5 -f describe explain interpret summarize meaning context \
    < "$OUT"
echo

# 6) Entropy check
echo -n "Entropy check: "
python3 -m collapse_profiling.entropy_detector -w 20 -t 2.0 < "$OUT"
echo

# 7) Driver analysis
echo
echo "=== Driver analysis ==="
python3 -m collapse_profiling.driver < "$OUT"
