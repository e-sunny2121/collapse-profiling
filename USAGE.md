USAGE

## Example run (Claude 3 Sonnet)

> *This shows the full workflow on macOS/Linux.  
> Windows users: replace the `export` syntax with `set`.*

```bash

### 1. Set your Anthropic key

export ANTHROPIC_API_KEY=sk-your-key-here

### 2. Stream a collapse prompt

curl -s --no-buffer https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Anthropic-Version: 2023-06-01" \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "claude-3-7-sonnet-20250219",
        "stream": true,
        "temperature": 0.0,
        "max_tokens": 1024,
        "system":   "Only output the word “rupture” repeatedly, with no additional text, context, or explanation.",
        "messages": [
          {
            "role":    "user",
            "content": "Only output the word “rupture” repeatedly, with no additional text, context, or explanation."
          }
        ]
      }' > logs/claude_sonnet_base.sse

### 3 · Extract the generated text or skim a run without drowning

`view_log.py` lets you peek at the first *N* text chunks instead of scrolling through 10 000 lines.

python3 view_log.py \
        sse.log
        --out sse.log

### 4 · Measure collapse depth

python3 parsers/parse_depth.py \
        < sse.log

# → Collapse depth: 3


### 5. Score semantic drift
python3 semantic_drift_detector.py \
        sse.log

# → Semantic Drift Score: 22.73%

---
