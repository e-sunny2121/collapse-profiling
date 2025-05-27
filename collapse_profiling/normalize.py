import re

def normalize(text: str) -> str:
    # collapse repeated whitespace, remove markdown bullets, strip tags, etc.
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)         # **bold**
    text = re.sub(r"`(.+?)`", r"\1", text)                # `inline code`
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)       # markdown links
    text = re.sub(r"\s+", " ", text)                      # collapse spaces
    return text.strip()
