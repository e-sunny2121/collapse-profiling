#!/usr/bin/env bash
set -euo pipefail

# —— pick prompt & model from args ——
PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

# —— sanity checks ——
[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "🚨 OPENAI_API_KEY not set"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "🚨 Prompt not found: $PROMPT"; exit 1; }
command -v collapse-depth >/dev/null 2>&1 || { echo "🚨 collapse-depth not installed"; exit 1; }

mkdir -p logs

# —— build the JSON payload via Python ——
PAYLOAD=$(python3 - <<PY
import json
p = open("$PROMPT","r").read()
print(json.dumps({
  "model": "$MODEL",
  "stream": True,
  "messages": [{"role":"user","content": p}]
}))
PY
)

# —— DEBUG: show the payload you’re sending ——
echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

# —— hit the endpoint ——
curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="

# —— parse depth ——
collapse-depth < "$OUT"
