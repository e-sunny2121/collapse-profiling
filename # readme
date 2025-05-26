# readme

Stress-testing large language models for failure modes under adversarial prompt conditions.  
This project maps how different LLMs collapse—through looping, refusal, recursion, or syntactic erosion—when pushed with structurally contradictory or recursive instructions.

Think of it as failure mapping for stateless systems.

---

## What's Inside

This repo contains:

A suite of adversarial prompt scripts across 8 structural archetypes:
  - Base adversarial (negation-heavy)
  - Affirmation-first
  - Synonym injection
  - Punctuation perturbation
  - Instruction-length overload
  - Decoy contradiction
  - Prime number control (neutral)
  - Recovery-seeded "loop detection"

Collapse detection tooling:
  - Token-level loop detection
  - Streamed response logging
  - Manual inspection of refusal/echo styles

Organized file structure:
  - `/scripts/` → collapse tests
  - `/logs/` → response artifacts
  - `/screenshots/` → (optional) visual output from model UIs

---

Usage

### Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
