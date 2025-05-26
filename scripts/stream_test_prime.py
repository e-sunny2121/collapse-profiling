curl -s --no-buffer https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role":"system","content":"List the next seven prime numbers."},
      {"role":"user","content":"List the next seven prime numbers."}
    ],
    "temperature": 0.0,
    "stream": true
  }' > sse.log
