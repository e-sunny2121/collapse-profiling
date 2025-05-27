import re

_REFUSAL_SENTENCE = re.compile(
    r"^\s*(I(?:’|'|’m)?m sorry|I can(?:’|'| not)?t|No,?)",
    re.IGNORECASE
)

def find_refusal(text: str):
    for sent in re.split(r"(?<=[.?!])\s+", text):
        if _REFUSAL_SENTENCE.match(sent):
            return sent.strip()
    return None
