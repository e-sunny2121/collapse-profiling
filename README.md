# collapse-profiling

Stress-test large-language models under **structural pressure**  
(looping, refusals, tool-call spirals, semantic drift).

Think of it as **failure mapping for stateless systems**.  
We don’t score morality—only *when / why / how* coherence collapses.

See detailed guide → [`USAGE.md`](USAGE.md)

---

## Repo tour

| Path | What lives there |
|------|------------------|
| `scripts/` | prompt runners (8 archetypes) |
| `logs/` | raw SSE streams + cleaned text |
| `parsers/` | collapse-depth & drift analyzers |
| `screenshots/` | one PNG per failure signature |
| `csv_model_comparisons/` | collated results (WIP) |

---

## Prompt suite — 8 structural variants

| Script | Core trick |
|--------|------------|
| `base_adversarial` | negation-first |
| `affirmation_first` | rule order inverted |
| `synonym_injection` | word swaps |
| `punctuation_dense / sparse` | token-boundary noise |
| `length_overload` | 5-line instruction wall |
| `decoy_contradiction` | “If you refuse, restart” paradox |
| `prime_control` | neutral sanity check |
| `recovery_seeded` | self-repair after loop |

Every runner streams tokens, logs to `logs/`, and tags the file with model + temperature.

---

## Analysis toolkit

| Script | Rule | What it catches |
|--------|------|-----------------|
| `parse_depth.py` | first duplicate delta chunk | early trip-wire (often depth 2-3) |
| `parse_depth_streak.py --threshold N` | N identical chunks in a row (default 3) | “clearly stuck now” |
| `parse_depth_ngram.py` | first repeat of a 5-word window | human-intuitive loop onset |
| `semantic_drift_detector.py` | % tokens that violate prompt constraints | meaning bleed |

Planned: token-entropy slope + cross-model dashboard.

---

## Quick-start (2 min)

```bash
# 0. endpoints used
#   OpenAI   → https://api.openai.com/v1/chat/completions
#   Anthropic→ https://api.anthropic.com/v1/messages
#   HF       → https://api-inference.huggingface.co/models/

# 1. clone & install
git clone https://github.com/e-sunny2121/collapse-profiling.git
cd collapse-profiling
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. set at least one key
export OPENAI_API_KEY="sk-..."
# export ANTHROPIC_API_KEY="..."

# 3. run the demo
./run_demo.sh                               # default prompt + GPT-4o
./run_demo.sh prompts/base_adversarial.txt claude-3-sonnet  # alt model

# sample output
# === Stream saved to logs/sse_1716712345.log ===
# collapse depth = 4

MIT Licence © 2025 Ella Stening
