# GitHub Work Item Lifecycle Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Issue·Goal·Branch·PR·Actions Run·Artifact·Release의 책임과 보존 기간을 분리해 기록을 잃지 않으면서 Base와 프로젝트의 현재 작업 화면을 간결하게 유지한다.

**Architecture:** `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`가 생명주기의 단일 공용 정본이다. 기존 GitHub Pro 정책은 Repository 보호·병합 설정, CI 비용 정책은 실행 계층을 계속 책임진다. Documentation Map과 Base·프로젝트 PR Template이 새 정본으로 라우팅하며, 새 unittest는 기존 CI 계약 테스트가 import해 Workflow 파일을 추가 수정하지 않고 실행한다.

**Tech Stack:** Markdown, Python 3.12 `unittest`, GitHub Actions, GitHub Pull Requests.

## Global Constraints

- 기존 열린 PR을 자동 종료·삭제하지 않는다.
- 하나의 Issue·Goal에는 하나의 활성 PR을 기본값으로 사용한다.
- 전체 열린 PR은 권장 최대 3개다.
- 기본 병합 방식은 Squash merge다.
- 병합된 head Branch는 삭제할 수 있지만 기본·Release Branch는 보존한다.
- 중요한 판단은 PR에 남기고 Run·Artifact는 기간 제한이 가능한 임시 증거로 취급한다.
- Repository 설정을 실제 확인·변경하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 기록한다.
- Changelog 전체 교체 위험을 피하기 위해 이번 PR에서는 `docs/CHANGELOG.md`를 변경하지 않는다.

---

### Task 1: Add the canonical lifecycle policy

**Files:**
- Create: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`

**Interfaces:**
- Consumes: `docs/GITHUB_PRO_OPERATING_POLICY.md`, `docs/CI_EXECUTION_COST_POLICY.md`, approved user request.
- Produces: Issue·Goal·Branch·PR·Run·Artifact·Release responsibility and retention contract.

- [x] Define object responsibilities and long-term versus temporary evidence.
- [x] Define one active PR per Goal and required search before PR creation.
- [x] Define WIP defaults: active 1, review 1, blocked/hold 1, total open PR recommended maximum 3.
- [x] Define squash merge, merged Branch deletion conditions and unmerged close records.
- [x] Define retention targets: success Run 14 days, failed Run 30 days, diagnostic Artifact 14 days, development build 7 days, release candidate 30 days.
- [x] Define `KEEP_UNRESOLVED`, `UNVERIFIED_REPOSITORY_SETTING`, lossless cleanup and rollback.

### Task 2: Add Base and project PR lifecycle templates

**Files:**
- Create: `.github/pull_request_template.md`
- Modify: `templates/pull_request_template.md`

**Interfaces:**
- Consumes: Task 1 policy.
- Produces: reviewable evidence for PR reuse, scope, validation, retention and post-merge cleanup.

- [x] Add original Issue·Goal and current status fields.
- [x] Add existing PR·Branch search and new PR justification.
- [x] Add include/exclude scope and responsibility-source table.
- [x] Add verification, unverified state and resume condition.
- [x] Add Run·Artifact retention and GitHub Release handoff.
- [x] Add merge method and Branch handling.
- [x] Keep project-only `docs/BASE_RULES_VERSION.md` in the project Template.
- [x] Remove legacy `docs/AI_SHARED_WORK_RULES.md` from the project Template.
- [x] Exclude project-only Base version tracking from the Base repository Template.

### Task 3: Route the policy from the Documentation Map

**Files:**
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: cold-start discovery for lifecycle questions.

- [x] Add the policy to the public canonical responsibility table.
- [x] Add project responsibility routing for work-item lifecycle and PR Templates.
- [x] Add the question route for PR·Run·Artifact accumulation.
- [x] Verify the diff is additive only.

### Task 4: Add regression tests without changing the Workflow

**Files:**
- Create: `tests/test_github_work_item_lifecycle_policy.py`
- Modify: `tests/test_ci_workflow_cost_policy.py`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: standard-library checks loaded by the existing lightweight and Ubuntu CI suites.

- [x] Test required policy terms and WIP defaults.
- [x] Test retention targets.
- [x] Test Base and project PR Template responsibilities and stale-reference removal.
- [x] Test Documentation Map registration.
- [x] Import the lifecycle TestCase from `test_ci_workflow_cost_policy.py` so existing Workflow commands discover it.
- [x] Keep `.github/workflows/validate-game-project-operating-system.yml` unchanged to avoid a redundant Workflow edit.

### Task 5: Protect existing history and open the PR

**Files:**
- Preserve unchanged: `docs/CHANGELOG.md`
- Create: Pull Request from `agent/github-work-item-lifecycle-policy` to `main`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: reviewable Base implementation without altering pre-existing PRs.

- [x] Search existing open PRs and confirm no matching Goal exists.
- [x] Leave PR #31, #30, #29, #28, #18 and #5 unchanged.
- [x] Detect the accidental partial Changelog replacement during diff review.
- [x] Restore `docs/CHANGELOG.md` exactly to the `main` blob using a Git tree commit.
- [x] Confirm the final diff contains no Changelog change and no game/runtime files.
- [x] Open Draft PR #44 while verification is in progress.

### Task 6: Verify and finalize review state

**Files:**
- Verify: all eight changed files and PR #44 Actions evidence.

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: evidence-backed Ready-for-review state or explicit blocked status.

- [x] Confirm `main...branch` reports only eight intended files.
- [x] Confirm `docs-validation` succeeds.
- [x] Confirm `ubuntu-contract` succeeds, including syntax, reference freshness and regression tests.
- [ ] Confirm `publication-validation`, `platform-smoke-windows` and `ci-gate` final outcomes.
- [ ] Update PR body with final HEAD, checks, retained settings gaps and Branch treatment.
- [ ] Mark PR Ready for review only if all required checks succeed.

## Verification Commands and Evidence

The repository Workflow executes the effective commands:

```bash
python -m unittest \
  tests/test_gpt_codex_workflow_contract.py \
  tests/test_ci_workflow_cost_policy.py \
  -v
```

Because `tests/test_ci_workflow_cost_policy.py` imports `GithubWorkItemLifecyclePolicyTests`, the new lifecycle tests are loaded by the existing command.

Ubuntu contract validation additionally performs Python syntax checks, Base proposal checks, canonical reference freshness and the full contract regression list. Final evidence is the PR HEAD Actions Run and `ci-gate`; local full-checkout verification is not claimed in the connector-only environment.
