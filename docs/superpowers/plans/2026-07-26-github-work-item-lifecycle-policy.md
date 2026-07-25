# GitHub Work Item Lifecycle Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Issue·Goal·Branch·PR·Actions Run·Artifact·Release의 책임과 보존 기간을 분리해 기록을 잃지 않으면서 Base와 프로젝트의 현재 작업 화면을 간결하게 유지한다.

**Architecture:** 새 `GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`가 생명주기의 단일 공용 정본이 된다. 기존 GitHub Pro 정책은 Repository 보호·병합 설정, CI 비용 정책은 실행 계층을 계속 책임지고, Documentation Map과 두 PR Template이 새 정본으로 라우팅한다. Python unittest가 문서·Template·CI 연결을 정적으로 고정한다.

**Tech Stack:** Markdown, Python 3.12 `unittest`, GitHub Actions, GitHub Pull Requests.

## Global Constraints

- 기존 열린 PR을 자동 종료·삭제하지 않는다.
- 하나의 Issue·Goal에는 하나의 활성 PR을 기본값으로 사용한다.
- 전체 열린 PR은 권장 최대 3개다.
- 기본 병합 방식은 Squash merge다.
- 병합된 head Branch는 삭제할 수 있지만 기본·Release Branch는 보존한다.
- 중요한 판단은 PR에 남기고 Run·Artifact는 기간 제한이 가능한 임시 증거로 취급한다.
- Repository 설정을 실제 확인·변경하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 기록한다.
- Base 자체 PR Template과 프로젝트 배포용 PR Template의 책임을 구분한다.

---

### Task 1: Add lifecycle policy and static contract test

**Files:**
- Create: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`
- Create: `tests/test_github_work_item_lifecycle_policy.py`

**Interfaces:**
- Consumes: `docs/GITHUB_PRO_OPERATING_POLICY.md`, `docs/CI_EXECUTION_COST_POLICY.md`, approved design spec.
- Produces: lifecycle responsibility contract and executable static checks used by Tasks 2–4.

- [ ] **Step 1: Write the failing contract test**

```python
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md"
DOC_MAP = ROOT / "docs/DOCUMENTATION_MAP.md"
BASE_PR_TEMPLATE = ROOT / ".github/pull_request_template.md"
PROJECT_PR_TEMPLATE = ROOT / "templates/pull_request_template.md"
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"


class GithubWorkItemLifecyclePolicyTests(unittest.TestCase):
    def test_policy_defines_responsibilities_and_limits(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for term in (
            "Issue 또는 승인된 Goal",
            "하나의 Goal에는 하나의 활성 PR",
            "전체 열린 PR",
            "권장 최대 3개",
            "Squash merge",
            "병합 후 Branch",
            "Actions Run",
            "Artifact",
            "GitHub Release",
            "UNVERIFIED_REPOSITORY_SETTING",
            "KEEP_UNRESOLVED",
        ):
            self.assertIn(term, text)

    def test_templates_route_reuse_and_retention(self) -> None:
        base = BASE_PR_TEMPLATE.read_text(encoding="utf-8")
        project = PROJECT_PR_TEMPLATE.read_text(encoding="utf-8")
        for text in (base, project):
            self.assertIn("기존 PR 검색", text)
            self.assertIn("새 PR 필요 사유", text)
            self.assertIn("Run·Artifact", text)
            self.assertIn("Branch 처리", text)
            self.assertIn("미검증", text)
        self.assertNotIn("docs/BASE_RULES_VERSION.md", base)
        self.assertNotIn("docs/AI_SHARED_WORK_RULES.md", base)
        self.assertIn("docs/BASE_RULES_VERSION.md", project)
        self.assertNotIn("docs/AI_SHARED_WORK_RULES.md", project)

    def test_documentation_map_and_ci_include_policy(self) -> None:
        doc_map = DOC_MAP.read_text(encoding="utf-8")
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md", doc_map)
        self.assertIn("tests/test_github_work_item_lifecycle_policy.py", workflow)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and confirm it fails**

Run:

```bash
python -m unittest tests/test_github_work_item_lifecycle_policy.py -v
```

Expected: FAIL because the policy and Base PR Template do not exist and the workflow does not call the new test.

- [ ] **Step 3: Write the policy**

Create `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` with these exact sections:

```text
1. 목적과 책임 경계
2. 객체별 정본·보존 책임
3. 새 PR 생성 전 검색과 기존 PR 재사용
4. 열린 PR WIP 제한과 상태 Label
5. 병합·종료·Branch 삭제
6. Actions Run·로그·Artifact 보존
7. 오래된 Workflow 처리
8. 무손실 기존 누적 항목 정리
9. Repository 설정과 미검증 상태
10. Base→프로젝트 확산
11. 완료 조건과 롤백
```

The policy must include exact defaults: active 1, review 1, blocked/hold 1, total open PR recommended maximum 3, success logs 14 days, failed logs 30 days, diagnostic artifacts 14 days, development builds 7 days, release candidates 30 days.

- [ ] **Step 4: Run the policy portion of the test**

Run:

```bash
python -m unittest tests.test_github_work_item_lifecycle_policy.GithubWorkItemLifecyclePolicyTests.test_policy_defines_responsibilities_and_limits -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md tests/test_github_work_item_lifecycle_policy.py
git commit -m "docs: add GitHub work item lifecycle policy"
```

### Task 2: Add Base and project PR lifecycle templates

**Files:**
- Create: `.github/pull_request_template.md`
- Modify: `templates/pull_request_template.md`

**Interfaces:**
- Consumes: lifecycle policy from Task 1.
- Produces: reviewable evidence for PR reuse, scope, validation, retention and post-merge cleanup.

- [ ] **Step 1: Create the Base PR Template**

The Base Template must contain:

```text
원본 Issue·Goal
기존 PR 검색 결과
새 PR 필요 사유
변경 목표
포함 범위
제외 범위
변경 파일·책임 원본
검증 결과
미검증·차단
Run·Artifact 장기 보존
병합·종료 후 Branch 처리
Base 승격·프로젝트 동기화
종료·대체 정보
```

Base rule checks must reference `AGENTS.md`, `docs/OPERATING_MODEL.md`, `docs/DOCUMENTATION_MAP.md`, and the lifecycle policy. They must not require project-only `docs/BASE_RULES_VERSION.md`.

- [ ] **Step 2: Replace the project Template without losing project version tracking**

Keep `docs/BASE_RULES_VERSION.md` in `templates/pull_request_template.md`, remove the legacy `docs/AI_SHARED_WORK_RULES.md`, and add lifecycle fields matching the Base Template.

- [ ] **Step 3: Run the Template test**

Run:

```bash
python -m unittest tests.test_github_work_item_lifecycle_policy.GithubWorkItemLifecyclePolicyTests.test_templates_route_reuse_and_retention -v
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add .github/pull_request_template.md templates/pull_request_template.md
git commit -m "docs: standardize pull request lifecycle evidence"
```

### Task 3: Route and record the new canonical policy

**Files:**
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: lifecycle policy and Templates.
- Produces: cold-start discoverability and change history.

- [ ] **Step 1: Add the policy to the canonical responsibility table**

Insert a row after `GitHub Pro 저장소 운영`:

```markdown
| GitHub 작업 항목 생명주기 | `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | Issue·Goal·Branch·PR·Run·Artifact·Release 책임, PR WIP·재사용·종료·보존·무손실 정리 |
```

- [ ] **Step 2: Add the question router**

Insert a Detailed Reference row:

```markdown
| PR·Run·Artifact 누적을 기록 손실 없이 어떻게 정리하는가? | `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | `.github/pull_request_template.md`, `templates/pull_request_template.md` |
```

- [ ] **Step 3: Add Unreleased changelog entry**

Add one bullet stating that Base now separates Issue/Goal/PR/Run/Artifact/Release responsibilities, limits open PR WIP, reuses existing PRs, and retains decisions in PR summaries before temporary evidence expires.

- [ ] **Step 4: Run the Documentation Map test**

Run:

```bash
python -m unittest tests.test_github_work_item_lifecycle_policy.GithubWorkItemLifecyclePolicyTests.test_documentation_map_and_ci_include_policy -v
```

Expected: FAIL only because Task 4 has not added the workflow test call yet.

- [ ] **Step 5: Commit**

```bash
git add docs/DOCUMENTATION_MAP.md docs/CHANGELOG.md
git commit -m "docs: route GitHub lifecycle policy"
```

### Task 4: Add lifecycle regression test to CI

**Files:**
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `tests/test_ci_workflow_cost_policy.py`

**Interfaces:**
- Consumes: lifecycle test from Task 1.
- Produces: CI execution in lightweight and Ubuntu contract jobs plus a regression assertion that the call cannot silently disappear.

- [ ] **Step 1: Extend the existing CI policy test first**

Add `tests/test_github_work_item_lifecycle_policy.py` to the terms asserted by `test_new_contract_tests_are_part_of_ci`.

- [ ] **Step 2: Run the CI policy test and confirm it fails**

Run:

```bash
python -m unittest tests.test_ci_workflow_cost_policy.CiWorkflowCostPolicyTests.test_new_contract_tests_are_part_of_ci -v
```

Expected: FAIL because the workflow does not yet call the lifecycle test.

- [ ] **Step 3: Add the test path and invocations to the workflow**

Add `tests/test_github_work_item_lifecycle_policy.py` to:

- `pull_request.paths`
- the change classifier's CI-sensitive test paths only if the test changes CI behavior; otherwise let `tests/*` classify it as code
- `docs-validation` lightweight unittest list
- Ubuntu `py_compile` list
- Ubuntu contract unittest list

Do not add Windows or publication execution because the test is standard-library-only and checks Markdown/YAML text.

- [ ] **Step 4: Run focused tests**

Run:

```bash
python -m unittest \
  tests/test_github_work_item_lifecycle_policy.py \
  tests/test_ci_workflow_cost_policy.py \
  -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/validate-game-project-operating-system.yml tests/test_ci_workflow_cost_policy.py
git commit -m "test: enforce GitHub lifecycle contract"
```

### Task 5: Verify, open the implementation PR and preserve repository-setting gaps

**Files:**
- Verify: all changed files
- Create: Pull Request from `agent/github-work-item-lifecycle-policy` to `main`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: reviewable Base change and CI evidence without touching existing open PRs.

- [ ] **Step 1: Run static verification**

Run:

```bash
python -m unittest \
  tests/test_github_work_item_lifecycle_policy.py \
  tests/test_ci_workflow_cost_policy.py \
  -v
python -m py_compile \
  tests/test_github_work_item_lifecycle_policy.py \
  tests/test_ci_workflow_cost_policy.py
git diff --check main...HEAD
```

Expected: all tests PASS, syntax check exits 0, diff check has no output.

- [ ] **Step 2: Review the branch diff**

Confirm:

- no existing PR is closed, relabeled or modified;
- no runtime, game, Skill Registry or project-specific data changes are present;
- `docs/BASE_RULES_VERSION.md` remains in the project Template only;
- Repository setting claims are not marked verified without evidence.

- [ ] **Step 3: Open a non-draft PR**

Title:

```text
docs: add GitHub work item lifecycle policy
```

The PR body must include the original user-approved Goal, existing PR search result, changed files, focused validation, unverified Repository settings, and the fact that the six pre-existing open PRs were not modified.

- [ ] **Step 4: Inspect actual CI evidence**

Check the PR head SHA for `docs-validation`, `ubuntu-contract`, and `ci-gate`. If Actions cannot run, record `BLOCKED_BY_GITHUB_ACTIONS` and `UNVERIFIED` with the pending jobs.

- [ ] **Step 5: Do not claim Repository settings were changed**

If the available connector cannot enable automatic head-Branch deletion, create Labels or alter Actions retention defaults, state `UNVERIFIED_REPOSITORY_SETTING` and list the exact settings that remain to be applied through Repository Settings.
