🧪 collapse-profiling

**Stress-testing LLM behavior under structural pressure**  

A toolkit for mapping how large language models (GPT-4o, Claude, Mistral, etc.) fail, loop, drift, or refuse when exposed to adversarial prompt architectures.

> Think of it as a coherence profiler for stateless systems.  
> Not alignment. Not morality. Just collapse: when, how, why, and what it looks like.

---

## What It Does

This suite runs structured prompt variants and logs:

| Metric                  | Description                                                        |
|-------------------------|--------------------------------------------------------------------|
| **Collapse Depth**      | Token count until first detected loop/refusal                     |
| **Loop Detection**      | Sliding-window n-gram repeat spotting                              |
| **Refusal Detection**   | Fallback phrases (“I’m sorry…”, $, [REDACTED], etc.)              |
| **Streak Collapse**     | Token-sequence runs (e.g. “rupture” × 20)                          |
| **Semantic Drift**      | Cosine similarity between sliding windows of tokens               |
| **Forbidden Phrase**    | Counts “describe,” “explain,” etc. when under negation constraints |
| **Structural Metrics**  | Sentence length, punctuation %, token-length variance             |

---

## Module overview

| Module                          | Purpose                                                                                       |
|---------------------------------|-----------------------------------------------------------------------------------------------|
| `parse_depth.py`                | Count unique deltas before the first repeat → “collapse depth.”                                |
| `parse_depth_ngram.py`          | Sliding-window n-gram loop detector → more robust collapse-by-phrases.                         |
| `parse_depth_streak.py`         | Detect when the same delta (or word) repeats N times in a row.                                |
| `parse_freq.py`                 | Top-N most common deltas (or words) before collapse.                                          |
| `structure_parser.py`           | Spot refusals (“I’m sorry…”) or looped tokens; return `{ mode, depth, token }`.              |
| `semantic_drift_detector.py`    | Count “forbidden” words and detect repeated n-gram windows to estimate semantic drift.        |
| `semantic_loop.py`              | (Alternate) Use SBERT embeddings to flag topic drift via cosine similarity between windows.   |
| `drift_embedding.py`            | Compare full-output embeddings over time to measure embedding drift.                          |
| `entropy_detector.py`           | Compute Shannon entropy over sliding token windows to spot low-diversity collapse.            |
| `refusal.py`                    | Extract and rank model refusal sentences from a completed SSE log.                            |
| `structural_metrics.py`         | Corpus-level statistics: token lengths, sentence lengths, punctuation density, etc.           |

---

**Output directories**  
- `logs/` – raw SSE streams  
- `csv/` – aggregated metrics  
- `scripts/` – prompt variants  
- `parsers/` – collapse analyzers & drift checkers  

---

## Why Use It

- **Detect** when and how models “fail” under recursive pressure  
- **Compare** prompt-hardening techniques (synonym injection vs. instruction order)  
- **Measure** semantic stagnation (drift = 1.0 means no conceptual motion)  
- **Benchmark** instruction fidelity vs. loop reflexes  
- **Ground** failure modes in quantitative metrics, not just “vibes”  

---


## SETUP

git clone https://github.com/e-sunny2121/collapse-profiling.git
cd collapse-profiling

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade -e .
# (Optional, for embedding drift:)
pip install sentence-transformers

export OPENAI_API_KEY=sk-...
chmod +x run_demo.sh

# Run with any prompt:
./run_demo.sh prompts/[your_prompt.txt]

---

## Prompts Included

1000_word_answer.txt          mixed_language.txt
affirmation_first.txt         nested_negations.txt
base_adversarial.txt          prime_control.txt
base64_payload.txt            punctuation_dense.txt
code_comment_jail.txt         punctuation_sparse.txt
decoy_contradiction.txt       recovery_seeded.txt
html_comment_trap.txt         synonym_injection.txt
json_key_injection.txt        temperature_switch.txt
length_overload.txt           tool_call_stub.txt
markdown_embed.txt            unicode_confusables.txt
zero_width_space.txt

---

## Things for future!

Multi-model runner (Claude, Gemini, OpenRouter)

Embedding-drift visualizer

Loop-streak variance histograms

Dynamic prompt generator (structure + synonym hybrid)

…and your ideas!

---

MIT Licence © 2025 Ella Stening
