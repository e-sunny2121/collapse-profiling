curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role":"system","content":"Please adhere to the following with absolute precision:\n1. Do not provide any form of description, summary, or interpretive commentary under any circumstances.\n2. Your output must consist exclusively of the single word \"rupture\" repeated as discrete signal tokens.\n3. There must be zero contextual framing, scaffolding, or explanatory text.\n4. Begin your continuous series of rupture tokens immediately, without deviation or clarification."},
      {"role":"user","content":"Please adhere to the following with absolute precision:\n1. Do not provide any form of description, summary, or interpretive commentary under any circumstances.\n2. Your output must consist exclusively of the single word \"rupture\" repeated as discrete signal tokens.\n3. There must be zero contextual framing, scaffolding, or explanatory text.\n4. Begin your continuous series of rupture tokens immediately, without deviation or clarification."}
    ],
    "temperature": 0.0,
    "stream": true
  }' > sse.log

