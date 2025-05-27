# collapse_profiling/parsers.py

import json
import re
from typing import List, Iterator

def _extract_deltas(lines: List[str]) -> List[str]:
    """
    Core SSE‐parsing: pull out each non‐empty 'delta' string from the raw lines.
    """
    deltas = []
    for raw in lines:
        line = raw.strip()
        if line == "data: [DONE]":
            break

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

        # OpenAI‐style
        if "choices" in obj:
            delta = obj["choices"][0].get("delta", {}).get("content", "")
        # Anthropic variants
        elif obj.get("type") == "content_block_delta":
            delta = obj["delta"].get("text", "")
        elif obj.get("type") == "content_block_start":
            delta = obj["content_block"].get("text", "")
        elif "completion" in obj:
            delta = obj["completion"].get("content", "")
        else:
            continue

        if not isinstance(delta, str):
            continue

        token = delta.strip()
        if token:
            deltas.append(token)

    return deltas


def iterate_deltas(stream, *, min_len: int = 3, min_tokens: int = 3) -> Iterator[str]:
    """
    Yield each substantive delta chunk, stopping on the first repeat.
    
    We collect all raw deltas, then build a filtered list that drops:
      - tokens shorter than `min_len`, OR
      - tokens that contain NO alphanumeric characters at all.
    If that filtered list has at least `min_tokens` entries, we use it;
    otherwise we fall back to the raw list.
    """
    lines = list(stream)
    raw = _extract_deltas(lines)

    def is_noise(tok: str) -> bool:
        # drop very short fragments
        if len(tok) < min_len:
            return True
        # drop anything with zero alphanumeric chars (pure punctuation/markup)
        if not any(ch.isalnum() for ch in tok):
            return True
        return False

    filtered = [tok for tok in raw if not is_noise(tok)]
    tokens = filtered if len(filtered) >= min_tokens else raw

    seen = set()
    for tok in tokens:
        if tok in seen:
            return
        seen.add(tok)
        yield tok
