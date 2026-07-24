# GitHub Pro Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GitHub Pro의 private repository 보호 기능과 자동 병합을 Base 공용 정책·Template·회귀 테스트로 만들고 `omenward` 시범 적용 계약을 준비한다.

**Architecture:** 기존 Skill ID를 늘리지 않고 GitHub 저장소 거버넌스는 문서·Template·기존 검증 흐름에 연결한다. 병합 권한은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 차단 상태를 통해 관리하고, Repository 설정을 직접 변경할 수 없는 도구 환경에서는 UI 적용과 미검증 상태를 명시한다.

**Tech Stack:** Markdown, JSON, Python unittest, GitHub Actions, GitHub Rulesets, GitHub Pull Requests.

## Global Constraints

- 기본 적용 순서는 Base → `omenward` → 다른 활성 프로젝트다.
- Required Check 기본 이름은 `ci-gate`다.
- 필수 승인 리뷰 수는 1인 저장소에서 `0`이다.
- `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `REVISE`, `BLOCKED`, `UNVERIFIED`는 자동 병합 금지다.
- 비공개 Push ruleset은 GitHub Pro 범위에 포함하지 않는다.
- Repository 설정을 실제 확인하지 못하면 통과로 주장하지 않는다.

---

### Task 1: Add canonical GitHub Pro policy and templates

**Files:**
- Create: `docs/GITHUB_PRO_OPERATING_POLICY.md`
- Create: `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`
- Create: `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`
- Create: `templates/project-operations/github/rulesets/solo-main-safety.json`

**Interfaces:**
- Consumes: approved design spec and official GitHub plan/ruleset/auto-merge contracts.
- Produces: reusable repository governance contract and importable ruleset.

- [ ] Write the policy with public/private Actions differences, Pro-supported protections, exclusions and rollout order.
- [ ] Add a repository profile template covering visibility, default branch, required checks, auto-merge and Ruleset state.
- [ ] Add an Actions/Packages/Codespaces budget evidence template.
- [ ] Add an importable branch ruleset targeting `~DEFAULT_BRANCH` with PR, `ci-gate`, linear history, force-push and deletion protection.
- [ ] Validate JSON syntax and required keys.

### Task 2: Replace mandatory user merge approval with gated auto-merge

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Modify: `skills/maintaining-project-context-and-handoff/SKILL.md`
- Modify: `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
- Modify: `templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md`
- Modify: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

**Interfaces:**
- Consumes: `AUTO_MERGE_AFTER_REQUIRED_CHECKS` policy.
- Produces: one consistent merge gate across policy, Skill, reference and package contract.

- [ ] Add `MANUAL_USER_APPROVAL` and `AUTO_MERGE_AFTER_REQUIRED_CHECKS` merge modes.
- [ ] Set automatic gated merge as the default selected policy for this workspace.
- [ ] Add `AUTO_MERGE_ELIGIBLE`, `AUTO_MERGE_ENABLED`, `AUTO_MERGE_BLOCKED` states.
- [ ] Keep user review mandatory for player-experience and planning decisions, not routine PR merge clicks.
- [ ] Remove absolute statements that every PR needs final user merge approval.

### Task 3: Add regression tests and routing

**Files:**
- Create: `tests/test_github_pro_operating_policy.py`
- Modify: `tests/test_gpt_codex_workflow_contract.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: static evidence and discoverability.

- [ ] Test the policy, template and Ruleset JSON.
- [ ] Test auto-merge eligibility and blocking statuses.
- [ ] Run the new test in lightweight and Ubuntu contract jobs.
- [ ] Route GitHub Pro governance from Documentation Map.
- [ ] Record the change in Unreleased changelog.

### Task 4: Open PR, validate Actions and enable auto-merge

**Files:**
- Create: Pull Request from `gpt/github-pro-governance-20260724` to `main`.
- Create: `omenward` pilot issue.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: actual CI evidence and rollout tracking.

- [ ] Compare the branch with latest `main` and verify no unrelated Godot runtime files.
- [ ] Open a non-draft PR.
- [ ] Confirm `classify-changes`, `docs-validation`, `ubuntu-contract` and `ci-gate` outcomes.
- [ ] Enable PR auto-merge if Repository setting permits it.
- [ ] If repository-level auto-merge is disabled and no available tool can change it, record `UNVERIFIED_REPOSITORY_SETTING` with exact UI path.
- [ ] Create `omenward` pilot issue with Ruleset import, auto-merge, Required Check and rollback checklist.
