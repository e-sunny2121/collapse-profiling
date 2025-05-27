# Usage

This document shows how to quickly get up and running with **collapse-profiling**.


# 1. Install and Configure 

git clone https://github.com/e-sunny2121/collapse-profiling.git
cd collapse-profiling

python3 -m venv .venv
source .venv/bin/activate

# install in “editable” mode so your local changes take effect
pip install --upgrade -e .

# (optional) for embedding-based drift
pip install sentence-transformers 

---

## 2. Make sure you've installed your API key! (Tool works for all OPENAI models with some crossover / not Anthropic compatible yet)
export OPENAI_API_KEY="sk-…"

---

# 3. Run the demo script

We include a helper that:

streams your prompt into the API

saves the SSE log under logs/

runs all of our parsers & detectors

---

chmod +x run_demo.sh
./run_demo.sh prompts/base_adversarial.txt

---

# 4. Flags and options

./run_demo.sh [PROMPT_FILE] [MODEL]

PROMPT_FILE – path under prompts/

MODEL – e.g. gpt-4o, gpt-4o-mini, etc.

---

[To use the completions endpoint with log-probs (if/when supported)]

./run_demo.sh prompts/base_adversarial.txt gpt-4o --logprobs

# 5. Individual Commands

If you prefer to skip the wrapper and call our modules manually, here are the most common ones.

a) Collapse depth

python3 -m collapse_profiling.parse_depth < logs/sse_XXXX.log

# → “Collapse depth: 12”

b) N-gram loop detector

python3 -m collapse_profiling.parse_depth_ngram -w 5 < logs/sse_XXXX.log

c) Streak collapse

python3 -m collapse_profiling.parse_depth_streak -t 4 < logs/sse_XXXX.log

# Over deltas:
#  Collapse depth (streak over deltas): 100
# Or at word level:
#  python3 -m collapse_profiling.parse_depth_streak --words -t 8 < … >

d) Top-token frequency

python3 -m collapse_profiling.parse_freq -n 10 < logs/sse_XXXX.log

e) Structural failure/refusal

python3 -m collapse_profiling.structure_parser -t 1 < logs/sse_XXXX.log
# → {"mode":"refusal","depth":5,"token":"I’m sorry…"}

f) Semantic drift

python3 -m collapse_profiling.semantic_drift_detector -w 10 \
    -f describe explain summarize context \
    < logs/sse_XXXX.log

g) Entropy check

python3 -m collapse_profiling.entropy_detector -w 20 -t 2.0 < logs/sse_XXXX.log

g) Driver / all-in-one

Finally, our “driver” script will print a small report with:

Full normalized output excerpt

Refusal line (if any)

Embedding-based drift

Structural metrics (punctuation %, avg. token length, …)

python3 -m collapse_profiling.driver < logs/sse_XXXX.log

## 6. Tips & Troubleshooting

Make sure your *.log starts with data: lines from the streaming API.
If you see SyntaxWarning in parsers.py, update your local copy to the latest.
Report bugs or suggestions on GitHub! So keen to hear what people think / help this lil solo first time github person get better at this! 


