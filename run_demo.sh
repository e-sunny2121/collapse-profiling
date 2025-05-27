#!/usr/bin/env bash
set -euo pipefail
set -x    # show each command

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

# debug params
echo ">>> DEBUG: PROMPT=<$PROMPT>"
echo ">>> DEBUG: MODEL=<$MODEL>"

# sanity checks for me
[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

# ——— build JSON payload via unquoted here-doc ———
PAYLOAD=$(python3 <<EOF
import json
# Bash has already substituted $PROMPT and $MODEL
with open("$PROMPT", "r", encoding="utf-8") as f:
    text = f.read()
print(json.dumps({
    "model": "$MODEL",
    "stream": True,
    "messages": [{"role": "user", "content": text}]
}))
EOF
)

echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

# fire the API
curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="

# parse outputs
python3 -m collapse_profiling.parse_depth       < "$OUT"
echo -n "Struct-Fail: "
python3 -m collapse_profiling.structure_parser < "$OUT"
