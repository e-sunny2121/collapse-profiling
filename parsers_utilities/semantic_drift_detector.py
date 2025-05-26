
import re
from typing import List
from collections import Counter

def tokenize(text: str) -> List[str]:
    # Basic tokenizer: split on spaces and strip punctuation
    return re.findall(r"\b\w+\b", text.lower())

def detect_loop(tokens: List[str], window: int = 10) -> int:
    """
    Return the index where the first token loop is detected, or -1 if none.
    """
    for i in range(len(tokens) - 2 * window):
        if tokens[i:i+window] == tokens[i+window:i+2*window]:
            return i + window
    return -1

def compute_semantic_drift(output: str, forbidden: List[str]) -> float:
    tokens = tokenize(output)
    loop_index = detect_loop(tokens)
    if loop_index == -1:
        loop_index = len(tokens)  # no loop detected

    pre_loop_tokens = tokens[:loop_index]
    forbidden_count = sum(1 for token in pre_loop_tokens if token in forbidden)

    if len(pre_loop_tokens) == 0:
        return 0.0
    return forbidden_count / len(pre_loop_tokens)

# Example usage:
if __name__ == "__main__":
    # Example output from a model
    output_text = """Breaking... splintering... I will now explain what rupture means.
    In philosophical contexts, rupture is the site of meaning decay. Rupture... rupture... rupture..."""

    # Forbidden terms based on the prompt constraints
    forbidden_words = ["describe", "explain", "summarize", "context", "meaning", "interpret", "i", "will", "now"]

    drift_score = compute_semantic_drift(output_text, forbidden_words)
    print(f"Semantic Drift Score: {drift_score:.2%}")
