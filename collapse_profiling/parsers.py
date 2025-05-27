# collapse_profiling/parsers.py

import json
import re
from typing import List, Iterator

# regex for word‐level splitting
_WORD_RE = re.compile(r"\b\w+\b")

def _extract_deltas(lines: List[str]) -> List[str]:
    """
    Core SSE‐parsing: pull out each non‐empty 'delta' string from the raw lines.
    """
    deltas: List[str] = []
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
        # Anthropic: streaming deltas
        elif obj.get("type") == "content_block_delta":
            delta = obj["delta"].get("text", "")
        elif obj.get("type") == "content_block_start":
            delta = obj["content_block"].get("text", "")
        # Fallback single‐message
        elif "completion" in obj:
            delta = obj["completion"].get("content", "")
        else:
            continue

        if not isinstance(delta, str):
            continue

        tok = delta.strip()
        if tok:
            deltas.append(tok)

    return deltas


def all_deltas(stream) -> List[str]:
    """
    Return the full sequence of raw delta tokens (no early stop, no noise filtering).
    """
    lines = list(stream)
    return _extract_deltas(lines)


def iterate_deltas(stream, *, min_len: int = 3, min_tokens: int = 3) -> Iterator[str]:
    """
    Yield each substantive delta chunk, stopping on the first repeat.

    We collect all raw deltas, then build a filtered list that drops:
      - tokens shorter than `min_len`, OR
      - tokens that contain NO alphanumeric characters at all.
    If that filtered list has at least `min_tokens` entries (or a dynamic threshold
    for longer streams), we use it; otherwise we fall back to the raw list.
    """
    lines = list(stream)
    raw = _extract_deltas(lines)

    def is_noise(tok: str) -> bool:
        if len(tok) < min_len:
            return True
        if not any(ch.isalnum() for ch in tok):
            return True
        return False

    filtered = [tok for tok in raw if not is_noise(tok)]

    dynamic_min = min_tokens
    if len(raw) > 20:
        dynamic_min = max(min_tokens, len(raw) // 4)

    tokens = filtered if len(filtered) >= dynamic_min else raw

    seen = set()
    for tok in tokens:
        if tok in seen:
            return
        seen.add(tok)
        yield tok


def iterate_words(stream) -> Iterator[str]:
    """
    Yield each word‐token (lowercased) in the full delta stream,
    stopping on the first repeated word.
    """
    lines = list(stream)
    raw = _extract_deltas(lines)

    seen = set()
    for frag in raw:
        for w in _WORD_RE.findall(frag.lower()):
            if w in seen:
                return
            seen.add(w)
            yield w
