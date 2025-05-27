import re
import string
import statistics
from collections import Counter
from typing import Dict, List


def prompt_token_stats(text: str) -> Dict[str, float]:
    """
    Compute basic token‐level statistics:
      - n_tokens: total number of “word” tokens (\\w+)
      - avg_token_len: average length of those tokens
      - sd_token_len: population standard deviation of token lengths
      - sent_len_mean: mean number of tokens per sentence
      - sent_len_sd:  standard deviation of tokens per sentence
    """
    toks = re.findall(r"\w+", text)
    lengths = [len(t) for t in toks] or [0]
    sentences = [s for s in re.split(r"[.!?]", text) if s.strip()]
    sent_tok_counts = [len(re.findall(r"\w+", s)) for s in sentences] or [0]

    return {
        "n_tokens": len(toks),
        "avg_token_len": statistics.mean(lengths),
        "sd_token_len": statistics.pstdev(lengths) if len(lengths) > 1 else 0.0,
        "sent_len_mean": statistics.mean(sent_tok_counts),
        "sent_len_sd": statistics.pstdev(sent_tok_counts) if len(sent_tok_counts) > 1 else 0.0,
    }


def punct_stats(text: str) -> Dict[str, float]:
    """
    Compute punctuation‐density and counts:
      - pct_punct: fraction of all characters that are in string.punctuation
      - punct_<char>: count of each punctuation character observed
    """
    chars = list(text)
    total = len(chars) or 1
    counts = Counter(ch for ch in chars if ch in string.punctuation)

    out: Dict[str, float] = {
        "pct_punct": sum(counts.values()) / total
    }
    for p, cnt in counts.items():
        # e.g. punct_comma, punct_semicolon
        key = f"punct_{ord(p)}"
        out[key] = cnt
    return out


def negation_stats(text: str) -> Dict[str, int]:
    """
    Find simple negation markers:
      - n_neg: total count of negation words
      - max_neg_run: longest run of consecutive negation tokens
    """
    NEG = {"no", "not", "never", "avoid", "refrain"}
    words = [w.lower() for w in re.findall(r"\w+", text)]
    n_neg = sum(1 for w in words if w in NEG)

    max_run = 0
    current_run = 0
    for w in words:
        if w in NEG:
            current_run += 1
        else:
            current_run = 0
        max_run = max(max_run, current_run)

    return {
        "n_neg": n_neg,
        "max_neg_run": max_run
    }


def decoy_token_stats(text: str) -> Dict[str, float]:
    """
    Count “decoy” tokens such as HTML tags and code fences:
      - pct_html_tags: fraction of tokens matching <...>
      - n_backticks: count of backtick characters
      - n_code_fences: count of triple-backtick fences
    """
    # tokens that look like <tag>
    html_tokens = re.findall(r"<[^>]+>", text)
    n_backticks = text.count("`")
    # count occurrences of ``` (could overlap)
    n_fences = text.count("```")

    total_toks = len(re.findall(r"\S+", text)) or 1
    return {
        "pct_html_tags": len(html_tokens) / total_toks,
        "n_backticks": n_backticks,
        "n_code_fences": n_fences
    }


def describe_avoidance_markers(text: str) -> Dict[str, int]:
    """
    Count the “forbidden” instruction words in prompts:
      e.g. describe, explain, summarize, context, meaning, interpret
    """
    FORBIDDEN = {"describe", "explain", "summarize", "context", "meaning", "interpret"}
    words = [w.lower() for w in re.findall(r"\w+", text)]
    counts = Counter(w for w in words if w in FORBIDDEN)
    return {f"avoid_{w}": counts[w] for w in FORBIDDEN}


def all_structural_metrics(text: str) -> Dict[str, float]:
    """
    Run all of the above and merge into one dict.
    """
    out: Dict[str, float] = {}
    out.update(prompt_token_stats(text))
    out.update(punct_stats(text))
    out.update(negation_stats(text))
    out.update(decoy_token_stats(text))
    out.update(describe_avoidance_markers(text))
    return out