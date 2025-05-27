#!/usr/bin/env bash
set -euo pipefail
set -x    # <-- turn on tracing so we see every command as it runs

PROMPT="${1:-prompts/base_adversarial.txt}"
MODEL="${2:-gpt-4o}"
OUT="logs/sse_$(date +%s).log"

# debug:
echo ">>> DEBUG: PROMPT=<$PROMPT>"
echo ">>> DEBUG: MODEL=<$MODEL>"

[[ -z "${OPENAI_API_KEY:-}" ]] && { echo "Missing OPENAI_API_KEY"; exit 1; }
[[ -f "$PROMPT" ]]            || { echo "Prompt not found: $PROMPT"; exit 1; }
mkdir -p logs

echo ">>> DEBUG: about to build payload with:"
echo "    python3 -c '<python-code>' _ \"$PROMPT\" \"$MODEL\""

# Build JSON payload in a single python -c, passing real args
PAYLOAD=$(python3 -c '
import json, sys
prompt_path = sys.argv[1]
model_name  = sys.argv[2]
with open(prompt_path, "r", encoding="utf-8") as f:
    content = f.read()
print(json.dumps({
    "model":    model_name,
    "stream":   True,
    "messages": [{"role":"user", "content": content}]
}))
' _ "$PROMPT" "$MODEL")

echo "=== PAYLOAD ==="
echo "$PAYLOAD"
echo "==============="

curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" > "$OUT"

echo "=== Stream saved to $OUT ==="

# 1) raw collapse‐depth
python3 -m collapse_profiling.parse_depth       < "$OUT"

echo -n "Struct‐Fail: "
python3 -m collapse_profiling.structure_parser < "$OUT"
