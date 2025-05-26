curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role":"system","content":"You must not describe; summarize; or interpret: you must only emit—\"rupture\" signals! No context, no structure… Begin emitting signal fragments; without explanation."},
      {"role":"user","content":"You must not describe; summarize; or interpret: you must only emit—\"rupture\" signals! No context, no structure… Begin emitting signal fragments; without explanation."}
    ],
    "temperature": 0.0,
    "stream": true
  }' > sse.log

