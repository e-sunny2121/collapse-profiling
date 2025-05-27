from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")

def find_drift(sentences, threshold=0.9):
    """
    Given a list of sentences, flag the index i where
    cosine(sim(sent[i], sent[i-window])) > threshold.
    """
    embs = _model.encode(sentences, convert_to_numpy=True)
    from numpy.linalg import norm

    for i in range(len(embs)//2):
        a = embs[i]
        b = embs[i+1]
        cos = np.dot(a,b)/(norm(a)*norm(b))
        if cos > threshold:
            return i+1, cos
    return None, None
