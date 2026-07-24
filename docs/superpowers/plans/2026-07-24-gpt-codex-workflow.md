# GPT–Codex Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base가 Grill Me 의사결정부터 GPT 비-Godot 완료, Codex 읽기 전용 Plan 재검수, 단계별 Godot 구현 인계와 비용 최적화 CI까지 일관되게 운영하도록 만든다.

**Architecture:** 기존 통합 Skill을 유지하고 Grill Me는 intake Skill의 `clarify` Mode에, 단계별 구현 인계는 context/handoff Skill의 전용 Mode에 추가한다. 공용 정책과 Template을 별도 정본으로 두고 정적 계약 테스트와 실제 GitHub Actions로 연결한다.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions YAML, GitHub Branch·Issue·PR.

## Global Constraints

- 새 독립 Skill은 기존 Skill Mode로 책임을 보존할 수 없을 때만 만든다.
- GPT는 기획·비-Godot 파일·GitHub 계약을 완료한다.
- Codex Plan은 읽기 전용이다.
- Codex Build는 지정 Branch의 Godot 런타임 파일만 수정·Commit·Push한다.
- 프로젝트 코어·플레이 규칙·MVP·호환성 변경은 `CHANGE_PROPOSAL`로 반환한다.
- PR 병합은 사용자 명시적 승인 전 금지한다.
- GitHub Actions 결과를 확인하기 전 통과를 주장하지 않는다.

---

### Task 1: Canonical workflow policy and templates

**Files:**
- Create: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Create: `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- Create: `templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md`
- Create: `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md`
- Create: `templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md`

**Interfaces:**
- Consumes: approved design in `docs/superpowers/specs/2026-07-24-gpt-codex-workflow-design.md`.
- Produces: canonical role, status, approval, Git and handoff contracts used by Skills and tests.

- [ ] Write the canonical policy with GPT, Codex Plan, Codex Build, user approval and change-authority boundaries.
- [ ] Write Grill Me decision ledger template.
- [ ] Write master implementation plan and package contract templates.
- [ ] Write read-only Codex Plan report template.
- [ ] Verify no placeholder text or contradictory authority remains.
- [ ] Commit with `docs: add GPT Codex workflow policy and templates`.

### Task 2: Integrate Grill Me and implementation handoff into existing Skills

**Files:**
- Create: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Modify: `skills/managing-project-intake-and-work-contract/references/ambiguity-and-closure.md`
- Create: `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
- Modify: `skills/maintaining-project-context-and-handoff/SKILL.md`

**Interfaces:**
- Consumes: canonical workflow policy and templates.
- Produces: automatic `clarify/grill-me` and `implementation-package-handoff` procedures without new duplicate Skill IDs.

- [ ] Add one-question-at-a-time Grill Me protocol with repository-first checks and termination conditions.
- [ ] Route Grill Me from ambiguity-and-closure reference.
- [ ] Add handoff Skill Modes for context refresh and implementation package handoff.
- [ ] Define Codex read-only Plan, technical changes, `CHANGE_PROPOSAL`, package status and Git guardrails.
- [ ] Commit with `skills: integrate Grill Me and Codex package handoff`.

### Task 3: Update Base routing and coverage maps

**Files:**
- Modify: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `skills/SKILL_COVERAGE.json`
- Modify: `docs/SKILL_COVERAGE_MAP.md`

**Interfaces:**
- Consumes: Task 1 and Task 2 paths and modes.
- Produces: cold-start routing, canonical lookup and machine-readable responsibility coverage.

- [ ] Add GPT → Codex Plan → GPT gate → Codex Build → GPT review → user merge flow.
- [ ] Add Grill Me and implementation package rows to Documentation Map.
- [ ] Add coverage responsibilities for Grill Me decision interviews and GPT–Codex package handoff.
- [ ] Keep existing Skill IDs and active count unchanged.
- [ ] Commit with `docs: route GPT Codex workflow through Base skills`.

### Task 4: Add regression tests

**Files:**
- Modify: `tests/test_deep_interview_contract.py`
- Create: `tests/test_gpt_codex_workflow_contract.py`
- Create: `tests/test_ci_workflow_cost_policy.py`

**Interfaces:**
- Consumes: policy, Skill references, templates and workflow.
- Produces: static evidence that required terms, paths, statuses, modes and CI gates remain present.

- [ ] Extend interview tests for `grill-me`, one-question rule, recommendation and decision ledger.
- [ ] Test GPT/Codex authority and package templates.
- [ ] Test CI concurrency, classifier, conditional Windows, `ci-gate`, main/nightly/full triggers and no unconditional heavy dependency installation.
- [ ] Run the focused tests in GitHub Actions.
- [ ] Commit with `test: cover GPT Codex workflow and CI policy`.

### Task 5: Implement cost-aware GitHub Actions

**Files:**
- Modify: `.github/workflows/validate-game-project-operating-system.yml`

**Interfaces:**
- Consumes: `docs/CI_EXECUTION_COST_POLICY.md` and Task 4 tests.
- Produces: change classification, minimal PR jobs, full main/nightly jobs, concurrency cancellation and stable `ci-gate`.

- [ ] Add PR, main push, nightly schedule and dispatch inputs.
- [ ] Add concurrency cancellation.
- [ ] Add `classify-changes` outputs with safe escalation.
- [ ] Run low-cost docs validation without LibreOffice, Poppler, Node or Windows.
- [ ] Run Ubuntu contract checks for canonical changes.
- [ ] Run publication dependencies and Windows smoke only for code/high-risk/full tiers.
- [ ] Add always-terminating `ci-gate` that rejects required job failures or omissions.
- [ ] Commit with `ci: tier validation by change risk`.

### Task 6: Changelog, issue and PR validation

**Files:**
- Modify: `docs/CHANGELOG.md`
- Update: GitHub Issue `#32`
- Create: Draft PR from `gpt/gpt-codex-workflow-20260724` to `main`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: reviewable diff and actual Actions evidence.

- [ ] Record the workflow, Skill Mode, templates and CI changes in `Unreleased`.
- [ ] Compare branch against latest `main` and confirm no unrelated Godot/runtime files.
- [ ] Open Draft PR and trigger Actions.
- [ ] Inspect workflow runs, jobs and logs.
- [ ] Fix failures on the same branch and rerun through a new commit.
- [ ] Report actual passing, failed or unverified checks without merging.
