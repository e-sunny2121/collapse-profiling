#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

PAYLOAD=$(python3 - <<PY
import json
p = open("$PROMPT","r").read()
print(json.dumps({
  "model":"$MODEL",
  "stream": True,
  "messages":[{"role":"user","content":p}]
}))
PY
)

echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="
python3 collapse_profiling/parse_depth.py < "$OUT"
python3 -m collapse_profiling.parse_depth       < "$OUT"

