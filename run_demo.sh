#!/usr/bin/env bash
set -euo pipefail

PROMPT="prompts/base_adversarial.txt"
MODEL="gpt-4o"
OUT="sse_$(date +%s).log"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY not set"; exit 1
fi

curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @<(jq -n --arg p "$(cat "$PROMPT")" --arg m "$MODEL" \
        '{model:$m,stream:true,messages:[{role:"user",content:$p}]}') \
  > "$OUT"

echo "=== Stream saved to $OUT ==="
cat "$OUT" | collapse-depth
