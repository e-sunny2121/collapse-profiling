import json
from typing import List, Iterable

def extract_deltas(lines: Iterable[str]) -> List[str]:
    """Exactly your _extract_deltas, but returns the raw strings."""
    deltas = []
    for raw in lines:
        line = raw.strip()
        if line == "data: [DONE]": break
        if   line.startswith("data:"):
            payload = line[len("data:"):].strip()
        elif line.startswith("{"):
            payload = line
        else:
            continue

        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue

        # your existing branching for choices/content_block_…
        chunk = (
            obj.get("choices",[{}])[0]
               .get("delta",{}).get("content", "")
            if "choices" in obj else
            obj.get("delta",{}).get("text", "")   # etc…
        )
        if isinstance(chunk,str) and chunk.strip():
            deltas.append(chunk)
    return deltas

def reconstruct(lines: Iterable[str]) -> str:
    """Stitch all deltas into one continuous string."""
    deltas = extract_deltas(lines)
    return "".join(deltas)
