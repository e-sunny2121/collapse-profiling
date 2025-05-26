#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

# sanity
[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "🚨 Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT"      ]] || { echo "🚨 Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

# build payload
PAYLOAD=$(python3 - <<'PY'
import json
p = open("${PROMPT}", "r", encoding="utf-8").read()
print(json.dumps({
  "model": "${MODEL}",
  "stream": True,
  "max_tokens": 64,
  "messages": [{"role":"user","content": p}]
}))
PY
)

echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

# call API
curl -s --max-time 30 --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="

# 1) raw collapse depth
echo -n "Raw collapse depth: "
python3 -m collapse_profiling.parse_depth < "$OUT"

# 2) structural failure detector
echo -n "Structural failure: "
python3 -m collapse_profiling.structure_parser < "$OUT"
