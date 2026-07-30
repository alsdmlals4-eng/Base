# Base v9.1 operating dashboard contract

`docs/PROJECT_OPERATING_DASHBOARD.html` is a deterministic generated view, never a new source of truth.

## Inputs and output

- Adapter input: `skills/PROJECT_BASE_ADAPTER.json` and its SHA-256.
- Route input: generated `skills/PROJECT_SKILL_SNAPSHOT.json`.
- State input: `docs/PROJECT_OPERATING_HEALTH.json`.
- Output: static UTF-8 HTML with no script, network dependency, timestamp, environment-specific path, or writable control.

## Required presentation

The dashboard exposes the project/release pins, independent OM and PE axes, every critical gate, integrity verdict, route counts, source hash, and generated status. The axes never average. Critical failures remain separate and visible.

Use semantic headings, landmarks, lists, native focus behavior, sufficient contrast, overflow-safe long Korean strings, and responsive layouts. Static layout inspection targets 1280x720 and 1920x1080. Those target labels do not constitute device, accessibility, runtime, or human validation.

`--check` performs byte comparison and reports a manual modification or stale output. Regenerate from canonical inputs; never repair the HTML directly.
