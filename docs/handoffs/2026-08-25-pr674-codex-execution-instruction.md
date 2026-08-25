# PR #674 · Codex 실행지시문 — 2026-08-25

## 상태

```yaml
instruction_type: CODEX_IMPLEMENTATION_INSTRUCTION
target_repository: alsdmlals4-eng/Base
target_pr: 674
target_branch: workflow/gpt-codex-role-split-20260825
current_phase: CODEX_IMPLEMENTATION_REQUIRED
next_return_state: READY_FOR_GPT_REVIEW
work_instruction_revision: DEFERRED_NOT_IN_SCOPE
notion_instruction: https://app.notion.com/p/3c71b237eb1c812a9ce0dd3610f7ea68?pvs=204
```

이 문서는 PR #674에서 **GPT가 완료한 기획·정본·적대적 검토 결과를 Codex가 실제 repository machine consumer 구현으로 이어받기 위한 실행지시문**이다.

이 문서는 프로젝트 공용 작업지시문 새 revision이 아니다. 해당 revision은 사용자 지시에 따라 별도 후속 작업으로 보류한다.

---

## 0. 현재 역할 계약

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
CODEX_PREFLIGHT_OPTIONAL
```

의미:

- GPT는 기획·조사·벤치마킹·적대적 검토·Notion 사람용 정본·이미지 제작/검수·구현 명세·최종 검수 owner다.
- 실제 code/data/Scene/Resource/config/test/build/runtime 구현은 Codex owner다.
- 구현이 존재하면 별도 `USER_REQUESTED_CODEX_HANDOFF`가 없어도 Codex가 정상 다음 단계다.
- Codex는 구현 전에 current GitHub + relevant Notion을 다시 읽는다.
- Codex는 이미지 생성·생성형 편집을 하지 않는다.
- Codex는 current-use 승인 + Notion upload/attach/readback가 확인된 Visual만 사용한다.
- 이미지가 부족하면 `GPT_VISUAL_REQUEST`로 반환한다.
- GPT→PowerShell→local Codex one-shot launcher는 기본 workflow에서 폐기됐다.
- wrong-target / stale session / process / editor / MCP / runtime freshness safety는 삭제하지 않고 **Codex execution environment owner**로 이동한다.

---

# 1. 시작 전 — `CODEX_REHYDRATE_GITHUB_AND_NOTION`

Handoff 요약을 current truth로 가정하지 않는다.

## GitHub 필수 읽기

1. `AGENTS.md`
2. `START_HERE.md`
3. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
4. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
5. `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
6. `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
7. `docs/handoffs/2026-08-25-gpt-codex-consumer-migration-packet.md`
8. `docs/handoffs/2026-08-25-gpt-codex-role-split-resume-checkpoint.md`
9. `docs/handoffs/2026-08-25-gpt-codex-role-split-codex-handoff.md`
10. `skills/maintaining-project-context-and-handoff/SKILL.md`
11. `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
12. `templates/custom-instructions.codex.md`
13. PR #674 current diff / exact head / current main
14. current open PR inventory

## Notion 필수 읽기

- `Base · 작업 시스템 & Skill 지도`
- `P08 · AI Operations & External Executors`
- `PR #674 · Codex 실행지시문`
- 영향이 있는 경우 P01 / P03 / P05 / P06 / P07 current pages

Notion instruction page:

`https://app.notion.com/p/3c71b237eb1c812a9ce0dd3610f7ea68?pvs=204`

## Freshness Gate

시작 시 반드시 확인:

```text
current main
current PR #674 head
current branch
current changed files
current open PRs
current required checks/workflows
current Notion role contract
current machine consumers
```

과거 SHA·과거 CI PASS·과거 Handoff만으로 진행하지 않는다.

---

# 2. 절대 금지 — 잘못된 GREEN 방지

테스트를 통과시키기 위해 옛 역할 계약을 다시 넣으면 실패다.

다음을 current behavior로 복구하지 않는다.

```text
OPTIONAL_CODEX_EXECUTOR              # implementation owner 의미로 복구 금지
GPT_GODOT_PREPRODUCTION_ALLOWED
GPT가 제품 Godot/code/POC 기본 구현
기획·구현·POC 누적 → USER_REQUESTED_CODEX_HANDOFF가 정상 기본 흐름
USER_REQUESTED_CODEX_HANDOFF가 없으면 구현 Codex 미사용
godot_runtime_files_only            # universal Codex restriction으로 복구 금지
GPT one-copy/paste PowerShell launcher가 기본 local Codex route
Codex image generation
Codex generative image editing
Codex가 임의 AI placeholder 생성
Notion 승인 없는 Visual을 제품 구현에 사용
```

역사 문서·snapshot에서 옛 literal이 존재하는 것은 허용한다. 단 current instruction처럼 보이지 않게 `HISTORICAL_SNAPSHOT`으로 유지한다.

---

# 3. 1단계 — Machine Consumer Inventory & Migration

Repository 전체에서 old-role consumer를 fresh-search한다.

검색 seed:

```text
OPTIONAL_CODEX_EXECUTOR
GPT_GODOT_PREPRODUCTION_ALLOWED
ON_DEMAND_CODEX_HANDOFF
USER_REQUESTED_CODEX_HANDOFF
기획·구현·POC 누적
Godot 구현 보조·POC
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
godot_runtime_files_only
PowerShell local Codex launcher
```

각 occurrence를 다음 중 하나로 분류한다.

```yaml
consumer_classification:
  PRESERVE_SEMANTIC:
  MIGRATE_OWNER:
  STALE_EXPECTATION:
  HISTORICAL_SNAPSHOT:
```

## 우선 수정 대상

최소 다음을 fresh-read한다.

### Tests

- `tests/test_gpt_codex_workflow_contract.py`
- `tests/test_p08_ai_operations_contract.py`
- `tests/test_base_long_horizon_work_contract.py`
- `tests/test_pr530_selective_integration_contract.py`
- neutral/adversarial lifecycle 관련 paired tests
- canonical freshness가 지목하는 changed-Skill paired tests

### Machine routing / generated

- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `docs/operations/BASE_PARTITION_MANIFEST.json`
- 필요 시 `.codex-plugin/**` 또는 다른 generated derivative

### Learning / behavior companion

- `skills/SKILL_LEARNING_LOG.md`
- `skills/maintaining-project-context-and-handoff/LEARNING_LOG.md`
- `skills/orchestrating-deepseek-worktrees/LEARNING_LOG.md`
- changed Skill에 필요한 behavior eval / fixture / paired regression

### One-Shot / execution environment

- `.github/workflows/validate-one-shot-local-executor-bootstrap.yml`
- 해당 workflow가 소비하는 tests / contracts / docs

One-Shot의 안전 의미를 지우지 않는다.

```text
wrong project/worktree 방지
stale PID/session 불신
fresh process/transport/server/session identity
editor/runtime/MCP readiness
exact target 확인
실제로 실행하지 않은 것을 PASS로 주장하지 않음
```

이 의미는 `CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED` owner로 이동한다.

---

# 4. MUST_PRESERVE — 역할 변경과 무관하게 유지할 안전 의미

다음 의미가 regression에서 사라지면 실패다.

## Neutral / adversarial

- `동의 편향` 방지
- `반대를 위한 반대` 금지
- 사용자안과 AI 최초안을 같은 기준으로 평가
- 결정·권장안 없는 설명형 칭찬/균형 요약만 full adversarial exclusion
- L1+ 중요한 결정은 PLAN 사전 적대검토
- finding은 먼저 validate
- approved finding은 실제 owner BUILD에서 한 번만 구현
- 구현 뒤 `regression-recheck → decision-report`
- 이미 구현된 finding을 review owner가 중복 수정하지 않음
- 최소 5회 full-scope loop + 이후 clean exit

## Continuous work

`기술적 단일 최소 안전 finding이면 자동 승인`의 의미는 유지하되 execution owner를 분리한다.

```text
GPT finding validation
→ 동일 승인 범위면 추가 사용자 승인 없이
→ Codex BUILD
→ GPT regression review
```

## Git / state

- exact-head validation
- remote HEAD 확인
- other open/draft/ready PR read-only
- force push / history rewrite 금지
- rollback
- post-merge main readback
- PRE_MERGE_SNAPSHOT과 LIVE_CONTINUATION_STATE 구분
- stale PID/session historical evidence 구분

---

# 5. TDD 순서

## 5.1 RED

새 역할을 검증하는 regression을 먼저 작성/교정해 old current behavior에서 실패하는지 확인한다.

필수 positive assertion:

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
CODEX_PREFLIGHT_OPTIONAL
```

필수 negative assertion:

```text
GPT product BUILD owner 부활 금지
implementation이 있는데 Codex optional 처리 금지
Codex image generation/editing 금지
unapproved Notion Visual substitution 금지
GPT default PowerShell/local-Codex launcher 부활 금지
```

## 5.2 GREEN

source → Registry → generated → Manifest → Learning/behavior → tests를 같은 semantic contract로 맞춘다.

Assertion을 단순 삭제하거나 테스트를 skip해서 GREEN 만들지 않는다.

## 5.3 REFACTOR

- compatibility alias와 current authority 분리
- history snapshot 보존
- duplicate current owner 제거
- generated artifact는 source에서 재생성

---

# 6. 이미지 규칙

이번 consumer migration은 원칙적으로 새 이미지가 필요하지 않다.

그래도 구현 중 별도 이미지 필요성이 생기면:

```text
Codex 생성 금지
→ GPT_VISUAL_REQUEST
→ GPT brief / 사용자 승인 / 생성·편집 / 검수
→ Notion current-use Approved
→ upload/attach/readback
→ Codex fresh-read
→ BUILD resume
```

Codex는 임시 AI 이미지나 placeholder를 생성하지 않는다.

---

# 7. Open PR / 동시작업 보호

현재 수정 허용 workstream은 PR #674뿐이다.

현재 관측된 다른 open PR은 전부 read-only:

- #696
- #693
- #689
- #679
- #678
- #660
- #658
- #650

새 open PR이 생기면 동일하게 read-only로 취급한다.

금지:

```text
checkout/write/rebase/close/merge/absorb/selective-copy of other open PRs
force push
history rewrite
destructive reset/clean
```

current main이 이동하면 force하지 말고 current main을 fresh-read해 안전하게 reconcile하고 다시 전체 검증한다.

---

# 8. 2단계 — 필수 검증

실제 current repository에서 commands/workflows를 discovery하고 실행한다. 특정 과거 check 이름이나 과거 PASS를 재사용하지 않는다.

최소 닫아야 할 범위:

```text
canonical-reference freshness
Skill Routing Precision
Evidence-Based Game Development Knowledge
Base Long-Horizon Work Contract
Base Partition Contract
Integrated Vertical Slice Prompt
Base v9 Operating Contracts
Game Project Operating System
One-Shot → Codex Execution Environment freshness replacement contract
Registry → generated sync
JSON/syntax/static validation
maximal available core regression
PR #674 exact-head validation
open PR overlap audit
unresolved review threads
```

`NOT_RUN`, `SKIPPED`, `BLOCKED_UNVERIFIED`는 PASS로 승격하지 않는다.

환경상 legitimate skip이면 environment와 이유를 기록한다.

---

# 9. Codex 적대적 self-check — 최소 5회

Codex는 구현 결과에 대해 다음 whole-state loop를 최소 5회 수행한다.

1. **Role ownership** — GPT product BUILD 또는 optional Codex implementation이 다시 생겼는가.
2. **Consumer completeness** — Registry/generated/test/Manifest/Learning/behavior consumer가 누락됐는가.
3. **Safety non-regression** — neutral/adversarial/continuous/Git/session safety가 약화됐는가.
4. **Visual boundary** — Codex image generation 또는 unapproved Visual path가 생겼는가.
5. **Freshness/concurrency/evidence** — stale head, stale Notion, other open PR 침범, NOT_RUN 과장이 있는가.

각 회차는 **전체 결과를 다시 읽는 full loop**다. 다섯 lens를 한 번씩 본 것을 5 loops라고 세지 않는다.

finding이 있으면 수정·검증 후 Loop 1부터 다시 current state를 공격한다. 최소 5회 후에도 finding이 남으면 계속한다.

---

# 10. 3단계 — GPT REVIEW 반환

Codex가 구현과 검증을 끝내도 직접 최종 승인하지 않는다.

최종 상태를 다음 중 하나로 반환한다.

```text
READY_FOR_GPT_REVIEW
BLOCKED
WAITING_GPT_VISUAL
```

반환 packet:

```yaml
codex_result:
  repository: alsdmlals4-eng/Base
  pr: 674
  branch: workflow/gpt-codex-role-split-20260825
  baseline_main:
  final_head:
  changed_files_and_reasons: []
  consumer_inventory:
    preserve_semantic: []
    migrate_owner: []
    stale_expectation_removed: []
    historical_snapshot_kept: []
  active_conflicts_removed: []
  preserved_safety_semantics: []
  one_shot_safety_migration:
  registry_generated_sync:
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_environment_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  adversarial_loops:
  open_pr_protection:
  remaining_risks: []
  rollback:
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

GPT는 이 결과를 current GitHub + Notion + actual CI와 다시 대조한다.

GPT가 `REVISE`를 반환하면 해당 finding만 Codex가 수정하고 다시 검증한다.

---

# 11. 4단계 — PR #674 병합 Gate

Codex는 GPT review를 생략해 PR을 독자적으로 final-approved 처리하지 않는다.

GPT가 `PACKAGE_APPROVED` 또는 동등 final review 상태를 선언한 뒤에만:

```text
current main fresh-read
→ PR #674 current exact HEAD
→ required checks PASS
→ unresolved review threads 0
→ current ruleset / merge method 확인
→ P0/P1 / CHANGE_PROPOSAL / WAITING_GPT_VISUAL 0
→ Ready 전환
→ 허용된 merge method로 merge
→ post-merge main readback
→ GitHub + Notion status reconcile
→ final GPT post-merge adversarial review
```

현재 repository/PR 정책을 그 시점에 다시 확인한다. 과거 merge method 또는 check 이름을 고정 가정하지 않는다.

---

# 12. 완료 정의

다음이 모두 충족되어야 #674 역할분리 작업이 완료다.

- machine consumer migration 완료
- stale current role assertion 0
- Registry/generated/Manifest/Learning/behavior consumer sync
- One-Shot safety의 Codex execution-environment owner migration 완료
- neutral/adversarial/continuous/Git/session safety 회귀 0
- Codex image generation/editing path 0
- unapproved Visual consumption path 0
- canonical-reference freshness PASS
- required/focused CI PASS
- maximal core regression 결과 확인
- 다른 open PR 침범 0
- Codex `READY_FOR_GPT_REVIEW`
- GPT final review PASS
- PR #674 merge
- post-merge main + Notion readback
- final `CLEAN_REVIEW_EXIT`

그 전에는 `COMPLETE`, `READY`, `CLEAN_REVIEW_EXIT=true`를 주장하지 않는다.
