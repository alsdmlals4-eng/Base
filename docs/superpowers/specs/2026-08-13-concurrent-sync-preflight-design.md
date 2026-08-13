# Concurrent Git Sync Preflight Design

## Status

- Date: 2026-08-13
- Baseline: `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- Work Mode: `PLAN → BUILD → REVIEW`
- Existing Solution First: `ABSORB`
- Primary owner: `skills/synchronizing-local-and-github-state/SKILL.md`
- Approval: 사용자의 현재 요청에서 Base 개선·PR·병합까지 명시적으로 승인

## Problem

Base는 `LOOP_ENGINEERING_CONTROL_PLANE`에서 `TASK_LEASE`, path lock, semantic resource lock, exact-SHA freshness를 정의한다. 그러나 일반 Git 동기화 Skill은 로컬·원격 ahead/behind와 dirty/diverged 상태만 검사한다. 여러 ChatGPT/Codex/외부 Agent가 같은 저장소를 동시에 작업할 때 다음 실패를 쓰기 전에 판정하는 공용 절차가 없다.

1. 열린 PR이 이미 소유한 파일을 다른 작업이 수정한다.
2. 파일은 달라도 같은 정본·Schema·생성물·자산 계열을 동시에 수정한다.
3. 동일 Goal을 별도 PR이 중복 구현한다.
4. 조사 시점의 `main` SHA가 쓰기·PR·병합 시점에는 낡아 있다.
5. 열린 PR 목록이나 changed-path 증거를 읽지 못했는데도 충돌 없음으로 보고한다.

현재 사례에서는 열린 PR #312가 `README.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md` 등을 수정 중이다. `README.md`의 활성 Skill 수가 생성 정본과 불일치하지만, 별도 작업이 직접 수정하면 동시작업 충돌을 키운다. 따라서 해당 PR에 조정 요청을 남기고 이 변경은 비중첩 경로만 사용한다.

## Goal

기존 Git 동기화 Skill의 `inspect` 단계에 `CONCURRENT_CHANGE_PREFLIGHT`를 흡수하여, 첫 persistent write·PR 생성·병합 전에 열린/최근 PR, 경로 중첩, 의미 자원 중첩, 동일 Goal, 기준 SHA 이동을 evidence-backed 상태로 판정한다.

## Non-goals

- 새 ACTIVE Skill, 새 Work Mode, 별도 락 서버 또는 scheduler를 만들지 않는다.
- GitHub가 강제하는 실제 mutex나 repository ruleset을 구현했다고 주장하지 않는다.
- PR #312가 소유한 경로를 수정하지 않는다.
- Skill Registry, 생성 파생본, release lock, GitHub workflow, repository settings를 변경하지 않는다.
- 모든 경로 중첩을 자동 merge conflict로 간주하지 않는다.

## Benchmark evidence

| Source | Observed practice | Base decision |
| --- | --- | --- |
| OpenAI Codex | 저장소 `AGENTS.md`의 범위·우선순위·테스트 지시를 따라 작업 환경과 검증을 고정한다. | 현행 AGENTS/Work Mode 구조 유지 |
| GitHub Copilot | 관련 Agent Skill만 선택해 사용하고, branch에서 연구·계획·변경·PR 검토를 분리한다. | 새 Skill 대신 기존 sync owner에 흡수 |
| GitHub rulesets / merge queue | strict required checks는 base 최신성을 요구하며 merge queue는 최신 base와 결합된 `merge_group`을 검증한다. | PR 전뿐 아니라 merge 직전 main freshness 재검사 |
| Anthropic Claude Code | 관련 Skill은 필요할 때만 로드하고 병렬 세션은 worktree로 파일 편집을 격리한다. | Registry 최소 로딩과 격리 branch 원칙 유지 |
| Google Cloud DORA | 작은 독립 변경과 빠른 자동 피드백은 속도·안정성을 함께 높이고 복구를 쉽게 한다. | 비중첩 최소 diff와 짧은 PR 유지 |

Primary references:

- https://openai.com/index/introducing-codex/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/research-plan-iterate
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://code.claude.com/docs/en/how-claude-code-works
- https://code.claude.com/docs/en/worktrees
- https://dora.dev/capabilities/working-in-small-batches/
- https://dora.dev/capabilities/continuous-integration/

## Contract design

### Required evidence

```yaml
source_main_sha:
current_main_sha:
expected_head_sha:
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
open_pr_changed_paths: {}
protected_concurrent_paths: []
repository_and_branch_policy:
credentials_permissions_and_required_checks:
```

### Preflight record

```yaml
CONCURRENT_CHANGE_PREFLIGHT:
  source_main_sha:
  current_main_sha:
  intended_paths: []
  semantic_resource_locks: []
  same_goal_open_and_recent_prs: []
  open_pr_changed_paths: {}
  overlap_classification: NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
  disposition: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
  coordination_action:
```

### Disposition rules

- `CLEAR`: current main equals the fixed source SHA, same-goal duplicate is absent, and no active path/semantic writer collision is verified.
- `STALE_BASE_SHA`: main changed after the source SHA was fixed. Reconcile to the new base and rerun the preflight.
- `WAITING_RESOURCE`: another active PR/task owns an overlapping path or semantic resource. Use a disjoint path, coordinate through its PR, or wait for release.
- `DUPLICATE_WORK`: another open/recent PR already owns the same Goal and expected result. Do not create a competing implementation.
- `BLOCKED_UNVERIFIED`: open PRs, changed paths, current main, or required policy evidence could not be read. Never downgrade this to `CLEAR` by assumption.

Path overlap is a warning, not proof of a textual merge conflict. The decision depends on ownership, intended hunks, generated/source relationships, and semantic authority. Conversely, different files can still collide when they modify the same canonical resource.

### Recheck points

1. Before branch creation or first persistent write.
2. Before PR creation after the final intended path set is known.
3. Before merge using the exact reviewed head SHA and current main.
4. After any observed change to main, the open PR set, or resource ownership.
5. After merge, read the new main and recheck same-goal PR/canon state.

## Files

| Path | Responsibility |
| --- | --- |
| `skills/synchronizing-local-and-github-state/SKILL.md` | Active owner and fail-closed preflight contract |
| `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md` | Step-by-step execution and coordination choices |
| `tests/test_concurrent_git_sync_preflight_contract.py` | Regression contract for required evidence, dispositions, and recheck points |
| `tests/test_v9_machine_contracts.py` | Wires the dedicated contract test into focused Base v9 CI |
| `docs/audits/2026-08-13-base-work-structure-adversarial-audit.md` | Repository structure audit, benchmark comparison, findings, and before/after report |

## Acceptance criteria

1. The existing sync Skill owns `CONCURRENT_CHANGE_PREFLIGHT` without adding a new ACTIVE Skill or Work Mode.
2. The contract requires exact main SHA, intended paths, semantic resources, same-goal PRs, and open PR changed paths.
3. `CLEAR`, `STALE_BASE_SHA`, `WAITING_RESOURCE`, `DUPLICATE_WORK`, and `BLOCKED_UNVERIFIED` are defined fail-closed.
4. First write, PR, merge, and post-merge recheck points are explicit.
5. The test is consumed by the focused Base v9 test topology.
6. PR #312 paths remain untouched; its README drift is handled by a coordination comment.
7. Exact-head CI passes before merge, then new-main readback confirms the merged contract.

## Rollback

Revert the single squash merge for this PR. No schema, Registry, generated artifact, workflow, dependency, repository setting, or project-specific file migration is involved.