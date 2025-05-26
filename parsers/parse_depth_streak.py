
import json, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--threshold", type=int, default=3,
                    help="number of identical deltas in a row ≡ collapse")
args = parser.parse_args()

streak_text = None
streak_len  = 0
count       = 0      # unique deltas before streak met

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
        return obj["delta"].get("text", "").strip()
    if "choices" in obj:
        return obj["choices"][0]["delta"].get("content", "").strip()
    return ""

for raw in sys.stdin:
    delta = extract(raw.strip())
    if not delta:
        continue

    if delta == streak_text:
        streak_len += 1
    else:
        streak_text = delta
        streak_len  = 1
        count      += 1          # only count the *first* time we see a new delta

    if streak_len >= args.threshold:
        break

print("Collapse depth:", count)
