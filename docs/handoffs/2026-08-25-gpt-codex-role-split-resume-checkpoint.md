# 2026-08-25 GPT–Codex 역할 분리 · Resume Checkpoint

## 상태

```yaml
workstream: GPT_CODEX_ROLE_SPLIT
pull_request: 674
branch: workflow/gpt-codex-role-split-20260825
work_instruction_revision: DRAFT_DEFERRED_NOT_CURRENT_CANON
resume_main: 6f8ca83efbb34862bd8cdceb38321090734a57ba
pre_resume_head: bf7473fd60d748b03330eb5ef74341ad681772f7
latest_main_merge_commit: 8cb30e35315fccd7eb5e62c8f2c0f767cde5d61c
checkpoint_head_after_doc_corrections: 9ac19045c76f30cc90ddbfa8e2536bf2a215290e
current_status: PARTIAL_CODEX_CONSUMER_MIGRATION_REQUIRED
clean_review_exit: false
```

## 사용자 최신 범위

- Base + Notion의 GPT/Codex 역할 분리 교정은 계속한다.
- 프로젝트 공용 작업지시문 revision 작성/승격은 **나중 별도 작업**으로 보류한다.
- GPT는 기획·조사·검수·이미지·Notion/운영 정본·구현 명세·최종 검수를 담당한다.
- 실제 code/data/Scene/Resource/config/test/build/runtime 구현은 Codex가 담당한다.
- Codex는 이미지를 생성·생성형 편집하지 않으며, current-use 승인 + Notion upload/attach/readback된 Visual만 소비한다.

## 재개 시 최신 main reconciliation

중단 뒤 Base main이 전진해 `6f8ca83efbb34862bd8cdceb38321090734a57ba`가 current main으로 관측됐다.

특히 merged PR #698 `docs: strengthen handoff resumability and learning promotion`이 다음을 강화했다.

- GitHub + Notion 종료/readback
- fresh-chat resumability
- Notion Visual delivery audit
- 문제→교훈→Base write/readback

#698은 본문에서 #674를 concurrent open workstream으로 명시하고 #674가 수정 중인 handoff Skill 파일을 건드리지 않았다. path overlap audit에서도 #698/latest-main 10개 변경과 #674 변경 파일의 직접 overlap은 0이었다.

따라서 force/rebase/history rewrite 없이 두 부모 merge commit `8cb30e35315fccd7eb5e62c8f2c0f767cde5d61c`으로 latest main을 #674 branch에 흡수했다.

```text
parent 1 = old #674 head bf7473fd...
parent 2 = main 6f8ca83e...
force update = false
result = #674 ahead of main, behind 0 at reconciliation readback
```

## 이번 재개에서 교정한 실제 비퇴행 finding

### NR-01 · Workspace schema 호환성

문제:
- 역할 분리에 필요하지 않은 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` schema `3 → 4` 변경이 들어가 있었다.
- `cross_domain_sync: SYNC_BEFORE_IMPLEMENTATION`도 새 문구로 덮여 기존 consumer 호환성을 불필요하게 깨뜨릴 수 있었다.

교정:
- `schema_version: 3` 유지
- `cross_domain_sync: SYNC_BEFORE_IMPLEMENTATION` 유지
- 새 역할 계약은 additive fields/invariants로 추가
- `codex_role`과 planning/implementation owner는 current 역할 의미로 갱신

결과:
- Workspace 데이터 계약 자체를 새 역할 분리 때문에 불필요하게 breaking-change하지 않는다.

### NR-02 · AI 활용 Guide active conflict

문제:
- `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`가 current rule로 `OPTIONAL_CODEX_EXECUTOR`, GPT 직접 Godot 구현, “GPT 다음은 Codex가 아님”을 사용하고 있었다.

교정:
- planning/research/review/visual = GPT
- actual implementation/coding/runtime = Codex
- Codex는 GitHub + relevant Notion fresh-read
- Codex image generation/editing 금지
- 승인 Notion Visual만 소비
- missing visual = `GPT_VISUAL_REQUEST`
- planning-only 작업에는 Codex를 강제하지 않지만 implementation이 존재하면 Codex BUILD를 생략하지 않음

보존:
- Eval, Prompt/Context, 보안, Prompt Injection, 개인정보, 권리/라이선스, 비용, 독립 검수, Golden Set, retry/rollback 기준은 유지

## 이전 비퇴행 finding 중 이미 복원된 항목

첫 역할분리 교정이 기존 정책을 지나치게 축약한 문제를 적대적 검토에서 발견했고 다음 capability를 복원했다.

- `CONTINUOUS_WORK_EXECUTOR_HANDOFF`
- `DEFERRED_EXTERNAL_EXECUTOR`
- Global Progress Queue / recover-defer-continue
- HiGodot/persistent authoring authority 보존
- `CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED`
- wrong-target / stale PID/session / project-session-version readiness
- destructive reset/restore/clean 금지
- Codex Plan read-only / 금지항목
- Master Implementation Plan / package contract
- Push 전후 VCS guard
- exact remote HEAD
- `PRE_MERGE_SNAPSHOT` / `LIVE_CONTINUATION_STATE` 분리
- `OBSERVE_POST_MERGE_TRUTH`
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`
- current repository required-check/ruleset discovery

## 현재 Base 정본 변경

현재 #674 branch가 직접 소유하는 핵심 current role 문서:

1. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
2. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
3. `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
4. `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
5. `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
6. `skills/maintaining-project-context-and-handoff/SKILL.md`
7. `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
8. `templates/custom-instructions.codex.md`

Review/Handoff evidence:

- `docs/reviews/2026-08-25-gpt-codex-role-split-adversarial-review.md`
- `docs/reviews/2026-08-25-gpt-codex-role-split-non-regression-followup.md`
- `docs/handoffs/2026-08-25-gpt-codex-role-split-codex-handoff.md`
- this checkpoint

## Notion current alignment

이미 destination readback된 중앙 페이지:

- `Base · 작업 시스템 & Skill 지도`
- `P01 · Project Planning, Operations & Notion`
- `P03 · Adversarial Quality, Refactoring & Git Integrity`
- `P05 · Art, UX/UI & Visual Assets`
- `P06 · Godot, Runtime & Technical Toolchain`
- `P07 · Platform, Release & Execution Validation`
- `P08 · AI Operations & External Executors`

핵심 의미:

```text
GPT PLAN/REVIEW/VISUAL
→ Implementation Ready
→ Codex GitHub + Notion rehydrate
→ Codex BUILD / test / runtime
→ missing visual? GPT_VISUAL_REQUEST
→ GPT image/review → Notion approved upload/readback
→ Codex resume
→ GPT final review
```

## 아직 남은 repository consumer migration

### Codex 구현/기계 consumer 영역

Codex가 fresh inventory 후 교정해야 한다.

- tests asserting old GPT preproduction / optional Codex behavior
- `skills/SKILL_REGISTRY.json`
- generated derivatives such as `docs/generated/BASE_ACTIVE_SKILLS.md`
- machine Manifest consumers that encode old role literal
- One-Shot Local Executor workflow/tests: 안전 capability는 삭제하지 않고 Codex execution-environment owner로 migration
- exact-head maximal regression

최소 새 regression contract:

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
```

### 추가 active 문서 rescan

다음 old literal consumer는 historical/test/generated인지 current doc인지 fresh 분류를 계속한다.

- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- `skills/orchestrating-deepseek-worktrees/SKILL.md`
- `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`

Evidence/history 문서의 과거 `OPTIONAL_CODEX_EXECUTOR` literal은 당시 상태를 설명하면 보존한다.

## Open workstream 보호

- PR #674 = current task, 수정 허용
- PR #660 및 다른 독립 open/draft/ready PR = read-only
- merged main만 follow-up source로 흡수
- force push / history rewrite / ruleset bypass 금지

## 작업지시문 status

이 작업 중 먼저 생성됐던 r6 draft는 사용자의 최신 범위 변경에 따라:

```text
DRAFT_DEFERRED
NOT_CURRENT_CANON
NOT_PART_OF_PR_674_MERGE_TARGET
```

작업지시문 revision은 Base/Notion 역할 교정과 repository consumer migration이 안정된 뒤 별도 작업에서 최신 main을 baseline으로 다시 작성한다.

## 다음 첫 행동

1. exact current #674 head에서 CI/workflow 결과 fresh-read
2. old-role active consumer rescan
3. GPT-owned 운영/기획 문서 conflict 최소 교정
4. code/test/Registry/generated/automation 영역은 Codex implementation handoff 유지
5. Codex consumer migration 뒤 exact-head full/maximal verification
6. whole-state adversarial review 최소 5회 + clean까지
7. Ready/merge Gate 판단
8. merge 뒤 #698 방식의 GitHub+Notion/fresh-chat/Visual/Lesson closure 수행

`CLEAN_REVIEW_EXIT = false` until consumer migration and fresh exact-head evidence close all active conflicts.
