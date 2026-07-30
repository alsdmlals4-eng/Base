# Base v9.1 Review Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:systematic-debugging task-by-task. This remediation is executed inline in the existing isolated worktree because the parent request already selected that mode.

**Goal:** Close every verified Issue #71 review blocker without changing product files or rewriting commit `b305531`.

**Architecture:** Treat the v9.1 candidate lock as the authority for release identity and pinned historical Registry content. Validate all paths, Git evidence, health claims, routes, aliases, protected changes, and generated artifacts through one fail-closed contract before any write. Generate explicit snapshot, dashboard, and file-specific legacy projections only from validated inputs.

**Tech Stack:** Python 3 standard library, jsonschema, unittest, Git CLI, GitHub Actions YAML.

## Global Constraints

- Use the mandated Base v9 virtual-environment interpreter for every Python test.
- Preserve `b305531` and create one new follow-up commit; do not amend, push, or open a PR.
- Keep v9.0 release artifacts byte-identical to their declared historical Git blobs.
- Keep all tests inside temporary Git repositories; do not touch Godot product files.
- Record runtime, device, accessibility, and human evidence as `NOT_RUN` unless direct evidence exists.

---

### Task 1: CI provenance and clean-runner dependencies

**Files:** `.github/workflows/*.yml`, `.github/workflows/dependency-review.yml`, `.github/validation-requirements.txt`, `tests/test_v9_1_project_operating_contract.py`

- [ ] Add a failing test for the exact official Action SHA allowlist, pinned validation dependency installation, and common dependency manifest path coverage.
- [ ] Run the focused test and confirm the expected SHA/dependency failures.
- [ ] Replace the setup-node SHA, install the pinned validation requirements before Python imports, and broaden dependency-review paths.
- [ ] Run the focused test to GREEN.

### Task 2: Historical v9.0 immutability and v9.1 release-lock binding

**Files:** `base-v9.1.lock.json`, `schemas/base-v9-1-candidate-lock-v1.schema.json`, `tools/check_base_v9_integrity.py`, `tools/project_operating_contract.py`, templates, tests

- [ ] Add failing temp-repository tests for one-byte frozen-artifact tampering, null candidate pins, inconsistent lock state, wrong identity/pins/ancestry, and pinned Registry hash mismatch.
- [ ] Confirm each failure class is RED for the intended reason.
- [ ] Compare frozen v9.0 files to declared historical Git blobs and bind v9.1 adapters to a populated, internally consistent lock and `git show <pin>:<registry>` bytes.
- [ ] Replace runnable v9.0-pinned v9.1 template values with candidate-safe placeholders and run tests to GREEN.

### Task 3: Health, routing, paths, protected changes, and generator preflight

**Files:** project contract schemas/tooling, router Skill, tests

- [ ] Add counterexample tests for health self-report contradictions, route status/precedence/aliases, unsafe paths/symlinks, invalid protected baselines/patterns/policy weakening, all Git change kinds, and invalid generation inputs.
- [ ] Run focused RED tests one failure class at a time.
- [ ] Implement evidence-derived/capped health, ACTIVE-only effective routing with materialized alias resolution, root-confined paths, fail-closed Git change collection, normalized protected matching, and shared validator preflight for write/check.
- [ ] Make the router invoke the exact validator command and stop before route reads on nonzero; run focused tests to GREEN.

### Task 4: Projections, dashboard, migration, duplication, PDF hardening

**Files:** `tools/project_operating_contract.py`, migration/build scripts, `tools/publication_v3.py`, schemas/templates/tests

- [ ] Add failing consumer-shape tests for each requested legacy view, dashboard content/escaping, explicit migration pins, content-based duplicate detection, and trusted Windows wrapper execution/rejection.
- [ ] Confirm focused RED results.
- [ ] Generate only requested file-specific projections from real legacy inputs, enrich the escaped dashboard from validated adapter/snapshot/health, require explicit migration pins, compare normalized Skill bodies independent of paths, and restrict wrapper fallback to trusted paths and metacharacter-free arguments.
- [ ] Run focused tests to GREEN.

### Task 5: Skill pressure fixtures, schemas, and governance documentation

**Files:** Skill/reference documents, pressure tests, snapshot schema, adapter/routing docs, integrity audit, changelog/documentation map

- [ ] Replace string-only pressure assertions with executable temp-repository fixtures covering body copy, stale pins, route precedence, and hash mismatch.
- [ ] Define concrete route, alias, alias-resolution, effective-route, and source-hash shapes in the snapshot schema.
- [ ] Mark all old adapter paths as generated compatibility/history-only and record the review remediation evidence without premature zero-finding claims.
- [ ] Run Skill pressure and Schema-focused tests to GREEN.

### Task 6: Final evidence and follow-up commit

- [ ] Run all focused tests and the complete unittest suite with the mandated interpreter.
- [ ] Run Base generator/integrity, canonical reference freshness, `git diff --check`, and `git fsck --strict`.
- [ ] Confirm the worktree is scoped and clean after creating a new follow-up commit.
