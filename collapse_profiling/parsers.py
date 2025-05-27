# collapse_profiling/parsers.py

import json
import re
from typing import List, Iterator

_PUNCT_SPACE = set('.,!?-–—*#[]()_`"\'\n\r\t ')

def _extract_deltas(lines: List[str]) -> List[str]:
    """
    Core SSE-parsing: pull out each non-empty 'delta' string from the raw lines.
    """
    deltas: List[str] = []
    for raw in lines:
        line = raw.strip()
        if line == "data: [DONE]":
            break

        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
        elif line.startswith("{"):
            payload = line
        else:
            continue

        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue

        # OpenAI-style
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


def all_deltas(stream) -> List[str]:
    """
    Return the full sequence of raw delta tokens (no early stop, no noise filter).
    """
    lines = list(stream)
    return _extract_deltas(lines)


def iterate_deltas(stream, *, min_len: int = 3, min_tokens: int = 3) -> Iterator[str]:
    """
    Yield each substantive delta chunk, stopping on the first repeat.

    We collect all raw deltas, then build a filtered list that drops:
      - tokens shorter than `min_len`, OR
      - tokens that contain NO alphanumeric characters at all.

    If the filtered list has at least `min_tokens` entries (or a dynamic threshold
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

    # dynamic minimum for long streams
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


_WORD_RE = re.compile(r"\b\w+\b")

def iterate_words(stream) -> Iterator[str]:
    """
    Yield every word‐token in the full delta stream, in order
    (no early stop).  Splits on \w+.
    """
    lines = list(stream)
    deltas = _extract_deltas(lines)
    for delta in deltas:
        for w in _WORD_RE.findall(delta.lower()):
            yield w
