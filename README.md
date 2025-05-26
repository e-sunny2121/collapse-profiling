# collapse-profiling

Stress-testing large-language-model behaviour under **structural pressure**.  
To map how AI models (here with Claude, GPT-x, Gemini, Mistral & friends) collapse through looping, refusing, tool-calling, or drifting—when fed recursively-contradictory prompts.

> Think of it as **failure mapping** for stateless systems. No testing morality, just the structure and the when/how/why/what of failure.

---

## Repo tour

| Path | What lives there |
|------|------------------|
| **/scripts/** | Adversarial prompt runners (8 archetypes) |
| **/logs/** | Raw SSE or cleaned text from model runs |
| **/parsers/** | Collapse-depth & semantic-drift analyzers |
| **/screenshots of output/** | One screenshot per distinct failure signature |
| **/csv model comparisons/** | Collated results tables (WIP) |
| **/requirements/** | `requirements.txt` for one-shot install |

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

## Analysis tools

| Parser | Metric |
|--------|--------|
| **collapse_depth/** | Counts tokens to first loop/refusal |
| **semantic_drift/** | % of pre-loop tokens violating prompt constraints |

Planned: entropy-slope tracker & cross-model dashboard.

---

## Quick start

```bash
# clone & install
git clone https://github.com/e-sunny2121/collapse-profiling.git
cd collapse-profiling
pip install -r requirements/requirements.txt

# run a test
export OPENAI_API_KEY=sk-…
python scripts/stream_test_base_adversarial.py
# output lands in logs/…
