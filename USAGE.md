USAGE

## Example run (Claude 3 Sonnet)

> *This shows the full workflow on macOS/Linux.  
> Windows users: replace the `export` syntax with `set`.*

### 1. Set your Anthropic key

```bash
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

### 3 · Extract the generated text

python3 parsers/semantic_drift/extract_claude_output.py \
        logs/claude_sonnet_base.sse \
        --out logs/claude_sonnet_base.txt

### 4 · Measure collapse depth

python3 parsers/collapse_depth/parse_depth.py \
        < logs/claude_sonnet_base.sse

# → Collapse depth: 3


### 5. Score semantic drift
python3 parsers/semantic_drift/semantic_drift_detector.py \
        logs/claude_sonnet_base.txt

# → Semantic Drift Score: 22.73%