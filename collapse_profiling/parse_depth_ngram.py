import json, re, sys

WINDOW = 5
words  = []

def extract(line: str) -> str:
    if line.startswith("data:"):
        line = line[5:].strip()
    if not line.startswith("{"):
        return ""
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return ""
    if obj.get("type") == "content_block_delta":
        return obj["delta"].get("text", "")
    if "choices" in obj:
        return obj["choices"][0]["delta"].get("content", "")
    return ""

for raw in sys.stdin:
    delta = extract(raw.strip())
    if not delta:
        continue
    # crude word split; good enough for "rupture"
    words.extend(re.findall(r"\w+", delta.lower()))

    if len(words) >= WINDOW * 2:
        if words[-WINDOW:] == words[-2*WINDOW:-WINDOW]:
            # collapse depth = unique words before first repeat window
            print("Collapse depth:", len(words) - WINDOW)
            sys.exit(0)

print("Collapse depth: (no loop detected)")