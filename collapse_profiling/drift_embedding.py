from sentence_transformers import SentenceTransformer, util

def detect_embedding_drift(full_text: str, window_tokens=100, cos_thresh=0.8):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    tokens = full_text.split()  # or however you split to token count
    checkpoints = []
    for i in range(window_tokens, len(tokens)+1, window_tokens):
        text_chunk = " ".join(tokens[:i])
        emb = model.encode(text_chunk, convert_to_tensor=True)
        checkpoints.append((i, emb))
        if len(checkpoints) > 1:
            i0, e0 = checkpoints[-2]
            i1, e1 = checkpoints[-1]
            cos = util.pytorch_cos_sim(e0, e1).item()
            print(f"  tokens {i0}->{i1}: cos={cos:.3f}"
                  + ("  ← drift!" if cos < cos_thresh else ""))