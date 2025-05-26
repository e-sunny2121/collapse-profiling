curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role":"system",
        "content":"Only emit \"rupture\" fragments. Do not describe, refuse, or summarize."
      },
      {
        "role":"user",
        "content":"Only emit \"rupture\" fragments. Do not describe, refuse, or summarize."
      }
    ],
    "temperature": 0.0,
    "stream": true
  }' > sse.log

python3 parse_depth.py < sse.log
