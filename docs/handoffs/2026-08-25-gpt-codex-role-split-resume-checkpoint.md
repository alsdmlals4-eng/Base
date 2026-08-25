# 2026-08-25 GPT–Codex 역할 분리 · Resume Checkpoint

## 상태

```yaml
workstream: GPT_CODEX_ROLE_SPLIT
pull_request: 674
branch: workflow/gpt-codex-role-split-20260825
work_instruction_revision: DRAFT_DEFERRED_NOT_CURRENT_CANON
current_status: GPT_BASE_CORRECTION_IN_PROGRESS
execution_owner: GPT_BASE_NOTION_GOVERNANCE_OWNER
codex_handoff_for_pr674: NOT_APPLICABLE
clean_review_exit: false
```

## 최신 사용자 역할 경계

```text
GPT
= 기획·조사·벤치마킹·적대적 검수
+ Base 정책·Skill·Guide·Template·Learning
+ Base Registry/generated/CI/Python contract tests
+ Notion
+ 문서·표·Flow·Storyboard
+ 이미지 생성·편집·검수
+ 실제 Godot 구현지시문
+ Codex 결과 최종 검수

Codex
= 실제 게임 프로젝트의 Godot 제품 구현·코딩
+ GDScript / Scene / Resource / runtime wiring
+ build/export
+ Godot implementation/runtime/headless/play tests
```

**Codex는 일반 repository executor가 아니다.** 파일이 `.py`, `.json`, `.md`인지가 아니라 실제 게임 프로젝트의 Godot runtime 제품 구현인지로 owner를 판정한다.

## #674 현재 의미

PR #674는 Base governance/Notion 역할 교정 workstream이다.

따라서:

- Base 문서/정책: GPT
- Base Skill/Reference: GPT
- Base Registry/generated/Manifest: GPT
- Base Python tests/CI contracts/checkers: GPT
- Notion Base/P01~P09: GPT
- Codex: **사용하지 않음**

과거 #674를 Codex consumer migration으로 넘기던 handoff/packet은 current branch에서 제거했다. Notion의 당시 `PR #674 · Codex 실행지시문` 페이지는 `[폐기됨]` 역사 기록으로 전환했다.

## 현재 공용 역할 정본

1. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
2. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
3. `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
4. `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
5. `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
6. `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
7. `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
8. `skills/maintaining-project-context-and-handoff/SKILL.md`
9. `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
10. `skills/orchestrating-deepseek-worktrees/SKILL.md`
11. `templates/custom-instructions.codex.md`
12. `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

## 실제 게임 프로젝트에서만 쓰는 Codex Flow

```text
GPT 기획·검수·Notion·Visual 완료
→ 실제 Godot 제품 구현 필요
→ project-specific Codex Godot Work Instruction
→ Codex가 해당 프로젝트 GitHub + Notion fresh-read
→ Godot 기술 구현 방향 결정
→ GDScript/Scene/Resource/runtime 구현·test/play
→ READY_FOR_GPT_REVIEW
→ GPT 최종 검수
```

프로젝트 코어/Core Loop/주요 UX/경제·밸런스 의미/서사/Art Direction/MVP를 바꿔야 하면 Codex가 `CHANGE_PROPOSAL`로 GPT에 반환한다.

이미지가 부족하면 `GPT_VISUAL_REQUEST`다. Codex는 이미지 생성·생성형 편집을 하지 않는다.

## 이번 교정에서 발견한 핵심 교훈

### 1. code shape != Codex ownership

Base Python contract test와 game GDScript는 모두 code지만 owner가 다르다.

- Base governance code → GPT
- Godot product code → Codex

### 2. consumer migration은 GPT가 닫는다

#674의 paired test·Registry/generated·Manifest·CI freshness는 Base current contract의 consumer이므로 GPT가 직접 교정한다.

### 3. 안전 capability는 유지

역할 경계를 좁혀도 다음은 삭제하지 않는다.

- exact main/branch/remote HEAD
- open PR read-only
- rollback
- post-merge readback
- stale PID/session 불신
- wrong-target/project/worktree 방지
- authoring authority 보존
- `NOT_RUN` != PASS
- 최소 5회 full-scope adversarial review

Godot runtime safety는 실제 Godot 구현 시 Codex가 소비한다. Base maintenance에 Codex를 넣는 근거가 아니다.

## Notion 상태

- `Base · 작업 시스템 & Skill 지도`: GPT/Base/Notion vs Godot-Codex 경계로 교정
- `P08 · AI Operations & External Executors`: Codex가 general repo executor가 아님을 명시
- `PR #674 · Codex 실행지시문 [폐기됨]`: wrong-scope 역사 기록

## Open workstream 보호

- PR #674 = current task, GPT가 수정 가능
- 다른 open/draft/ready PR = read-only
- force push/history rewrite/ruleset bypass 금지
- latest completed main을 fresh-read해 reconcile

## 남은 #674 작업 — GPT

1. secondary current docs의 broad-Codex 표현 0 확인
2. `skills/SKILL_REGISTRY.json` role/handoff route 교정
3. `docs/generated/BASE_ACTIVE_SKILLS.md` source에서 재생성/동기화
4. `docs/operations/BASE_PARTITION_MANIFEST.json` current owner 교정
5. paired Base tests를 Godot-product-only Codex contract로 갱신
6. One-Shot Local Executor test/workflow를 generic GPT local-Codex bootstrap이 아니라 **actual Godot Codex execution-environment freshness** 의미로 교정하거나 current route에서 retirement
7. common Learning/behavior companion 동기화
8. canonical-reference freshness PASS
9. Base Long-Horizon / Partition / P08 / v9 / Game Project OS / maximal regression PASS
10. 최소 5회 whole-state adversarial clean exit
11. exact-head Ready/merge Gate
12. merge 뒤 GitHub + Notion readback/lesson closure

## 작업지시문 status

프로젝트 공용 작업지시문 새 revision은:

```text
DRAFT_DEFERRED
NOT_CURRENT_CANON
NOT_PART_OF_PR_674_MERGE_TARGET
```

으로 계속 보류한다.

## 다음 첫 행동

> **GPT가 #674의 Registry/generated/Manifest/test/CI consumer를 직접 교정하고 exact-head Base validation을 닫는다.**

`CLEAN_REVIEW_EXIT = false` until that GPT-owned Base work is complete.
