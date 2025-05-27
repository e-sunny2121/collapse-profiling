#!/usr/bin/env bash
set -euo pipefail
set -x   # trace commands

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

echo ">>> DEBUG: PROMPT=<$PROMPT>"
echo ">>> DEBUG: MODEL=<$MODEL>"

[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

# —— build JSON payload via unquoted here-doc —— 
PAYLOAD=$(python3 <<EOF2
import json
with open("$PROMPT", "r", encoding="utf-8") as f:
    text = f.read()
print(json.dumps({
    "model": "$MODEL",
    "stream": True,
    "messages": [{"role": "user", "content": text}]
}))
EOF2
)

echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="

python3 -m collapse_profiling.parse_depth       < "$OUT"
echo -n "Struct-Fail: "
python3 -m collapse_profiling.structure_parser < "$OUT"
EOF