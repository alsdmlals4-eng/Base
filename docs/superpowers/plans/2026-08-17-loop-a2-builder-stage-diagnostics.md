# Loop A2 REAL Builder Stage Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert unexpected REAL Builder adapter exceptions into stable stage-specific types already representable by the public receipt.

**Architecture:** Add a tiny exception-only module and narrow wrappers in `GitWorktreeBuilderAdapter.invoke()`. Do not change OpenAI/Codex provider behavior, A2 state/finding codes, scope, authority, or public receipt fields.

**Tech Stack:** Python 3.12, unittest, GitHub Actions.

## Global Constraints

- Raw traceback/message/path/prompt/stdout/stderr publication forbidden.
- Paid OpenAI API and API-key fallback forbidden.
- A3 disabled; Scheduler not configured.
- Blacksmith authority/product scope unchanged.
- Diagnostic runs never count as REAL burn-ins.

### Task 1: TDD stage classification

- [x] Add focused tests that inject `AttributeError` at workspace, worker, diff, and result-binding boundaries.
- [x] Verify RED: current code exposes raw `AttributeError` at all four boundaries while existing Runtime Foundation tests remain green.

### Task 2: Minimal diagnostic implementation

- [x] Create `tools/loop_a2_runtime/builder_diagnostics.py` with four stable stage exception classes and a private base class.
- [x] Wrap unexpected adapter exceptions at workspace/worker/diff/result-binding boundaries; preserve intentional `WorkerResult` blockers and existing `BuilderStageError` specificity.
- [x] Verify GREEN in Runtime Foundation.

### Task 3: Exact-head, merge, and live diagnostic

- [ ] Require Local Executor Windows/Ubuntu, Durable Resume Windows/Ubuntu, Runtime Foundation, Base-v9/adversarial, and GPO final `ci-gate` success. Runtime Foundation must retain existing OpenAI Builder transport contracts.
- [ ] Reconcile against current completed main; copy to integration branch if main moved.
- [ ] Merge with expected-head protection and run postmerge gates.
- [ ] Run one fresh-run-id REAL Blacksmith diagnostic job using unchanged authority; record only stable public provider error type.
- [ ] Do not increment burn-in count.
