#!/usr/bin/env bash
set -euo pipefail

# —— Config ——  
PROMPT="prompts/base_adversarial.txt"
MODEL="${1:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

# —— Sanity checks ——  
[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "🚨 OPENAI_API_KEY not set"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "🚨 Prompt file not found: $PROMPT"; exit 1; }
command -v collapse-depth >/dev/null 2>&1 || { echo "🚨 collapse-depth not installed"; exit 1; }

mkdir -p logs

# —— Build JSON payload via Python ——  
PAYLOAD=$(python3 - <<PY
import json, sys
prompt = open("$PROMPT", "r").read()
obj = {"model": "$MODEL", "stream": True, "messages": [{"role": "user", "content": prompt}]}
sys.stdout.write(json.dumps(obj))
PY
)

# —— Fire the request ——  
curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  > "$OUT"

echo "=== Stream saved to $OUT ==="

# —— Parse collapse depth ——  
collapse-depth < "$OUT"
