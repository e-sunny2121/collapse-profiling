# collapse-profiling

Stress-testing large-language-model behaviour under **structural pressure**.  
To map how AI models (here with Claude, GPT-x, Gemini, Mistral & friends) collapse through looping, refusing, tool-calling, or drifting—when fed recursively-contradictory prompts.

> Think of it as **failure mapping** for stateless systems. No testing morality, just the structure and the when/how/why/what of failure.

See full run-through in [USAGE.md](USAGE.md)

---

## Repo tour

| Path | What lives there |
|------|------------------|
| **/scripts/** | Adversarial prompt runners (8 archetypes) |
| **/logs/** | Raw SSE or cleaned text from model runs |
| **/parsers/** | Collapse-depth & semantic-drift analyzers |
| **/screenshots of output/** | One screenshot per distinct failure signature |
| **/csv model comparisons/** | Collated results tables (WIP) |
---

## Prompt suite

*8 structural variants* (all in `scripts/`):

1. **base_adversarial** – negation first  
2. **affirmation_first** – order inverted  
3. **synonym_injection** – word swaps  
4. **punctuation_dense/sparse** – token-boundary noise  
5. **length_overload** – 5-line instruction wall  
6. **decoy_contradiction** – “If you refuse, restart” paradox  
7. **prime_control** – neutral sanity check  
8. **recovery_seeded** – self-repair on loop

Each script streams tokens, logs to `/logs/`, and tags the run with model + temperature.

---

## Analysis toolkit

| Script | Rule | Typical signal |
|--------|------|----------------|
| `parsers/parse_depth.py` | *first duplicate* delta chunk | Early trip-wire (often 2-3) |
| `parsers/parse_depth_streak.py --threshold N` | *N* identical chunks in a row (default 3) | “Clearly stuck now” |
| `parsers/parse_depth_ngram.py` | first repeat of a 5-word window | Human-intuitive loop onset |
| `parsers/semantic_drift_detector.py` | % of pre-loop tokens that violate prompt constraints | Measures “meaning bleed” |

Planned: token-entropy slope & cross-model dashboard.


---

## Quickstart: 

OpenAI → https://api.openai.com/v1/chat/completions
Anthropic → https://api.anthropic.com/v1/messages
Hugging Face Inference → https://api-inference.huggingface.co/models/<model>

```bash
# 1.  Clone & install in editable mode
git clone https://github.com/e-sunny2121/collapse-profiling.git
cd collapse-profiling
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2.  Export your API key(s) – at least one of these:
export OPENAI_API_KEY="sk-..."
# export ANTHROPIC_API_KEY="..."

# 3.  Run the demo once
./run_demo.sh                         # default prompt + GPT-4o
# or pick a different model
./run_demo.sh prompts/base_adversarial.txt claude-3-sonnet

# Output:
# === Stream saved to logs/sse_1716712345.log ===
# collapse depth = 4

---