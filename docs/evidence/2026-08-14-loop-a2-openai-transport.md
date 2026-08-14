# Loop A2 OpenAI Transport Evidence — 2026-08-14

## Scope

Issue #364. Implement bounded real OpenAI Responses API transport without making a live or paid API request.

## RED 1

Test-only head starts with:

- missing `tools/loop_a2_runtime/openai_transport.py` must fail;
- REAL provider gate must require explicit, distinct Builder and Critic model IDs in addition to approval and an API-key presence check.

No live API call, model selection, key value, project product mutation, A3, or Scheduler activation is part of this RED.
