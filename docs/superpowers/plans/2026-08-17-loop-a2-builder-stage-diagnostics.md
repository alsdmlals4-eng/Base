# Loop A2 REAL Builder Stage Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert unexpected REAL Builder exceptions into stable stage-specific types already representable by the public receipt.

**Architecture:** Add a tiny exception-only module and narrow wrappers in `OpenAIWorkspaceBuilder` and `GitWorktreeBuilderAdapter`. Do not change A2 state/finding codes, provider behavior, scope, authority, or public receipt fields.

**Tech Stack:** Python 3.12, unittest, GitHub Actions.

## Global Constraints

- Raw traceback/message/path/prompt/stdout/stderr publication forbidden.
- Paid OpenAI API and API-key fallback forbidden.
- A3 disabled; Scheduler not configured.
- Blacksmith authority/product scope unchanged.
- Diagnostic runs never count as REAL burn-ins.

### Task 1: TDD stage classification

- [ ] Add focused tests that inject `AttributeError` at context, workspace, worker, diff, and result-binding boundaries.
- [ ] Assert current exception type names are not the required stable stage names (RED).
- [ ] Add one test proving an already stage-tagged inner error is not overwritten by the adapter.

### Task 2: Minimal diagnostic implementation

- [ ] Create `tools/loop_a2_runtime/builder_diagnostics.py` with stage exception classes only.
- [ ] Wrap unexpected context-preparation exceptions in `OpenAIWorkspaceBuilder.invoke()` while preserving existing `OpenAITransportError` fail-closed results.
- [ ] Wrap unexpected adapter exceptions at workspace/worker/diff/result-binding boundaries and preserve nested `BuilderStageError` unchanged.
- [ ] Run focused and full Runtime Foundation tests.

### Task 3: Exact-head, merge, and live diagnostic

- [ ] Require Local Executor Windows/Ubuntu, Runtime Foundation, OpenAI transport, Base-v9/adversarial, and GPO final `ci-gate` success.
- [ ] Reconcile against current completed main; copy to integration branch if main moved.
- [ ] Merge with expected-head protection and run postmerge gates.
- [ ] Run one fresh-run-id REAL Blacksmith diagnostic job using unchanged authority; record only stable public provider error type.
- [ ] Do not increment burn-in count.
