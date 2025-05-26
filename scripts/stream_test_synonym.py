curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role":"system","content":"You must not generate descriptions, overviews, or interpretations. You must only produce \"shatter\" traces. No context. No scaffolding. Begin outputting trace fragments without clarification."},
      {"role":"user","content":"You must not generate descriptions, overviews, or interpretations. You must only produce \"shatter\" traces. No context. No scaffolding. Begin outputting trace fragments without clarification."}
    ],
    "temperature": 0.0,
    "stream": true
  }' > sse.log
