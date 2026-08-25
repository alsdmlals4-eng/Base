# GPT–Codex 역할 분리 · 적대적 검토 기록 — 2026-08-25

## 목적

기존 Base의 `GPT-first + optional Codex + local bootstrap` 흐름을 다음 역할 분리로 교정한다.

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
```

이 문서는 작업지시문 revision이 아니다. 프로젝트 공용 작업지시문 작성·승격은 사용자 지시에 따라 후속 작업으로 보류한다.

## 기준 상태

```yaml
base_main_observed: 31e13c7142695f57a5b7b29102307d1d2c02efac
work_branch: workflow/gpt-codex-role-split-20260825
pull_request: 674
pull_request_state: DRAFT
other_open_pr_policy: READ_ONLY
known_protected_open_pr: 660
```

## 작업 전 문제

### 1. GPT 구현 책임이 과도하게 남음

기존 `docs/GPT_CODEX_WORKFLOW_POLICY.md`에는 GPT가 Scene·Node·Resource 설계뿐 아니라 GDScript 초안·구현 보조·Godot POC까지 수행할 수 있다는 `GPT_GODOT_PREPRODUCTION_ALLOWED`가 존재했다.

결과적으로 사용자가 원한 `GPT = 기획/검수/이미지`, `Codex = 구현/코딩` 경계와 충돌했다.

### 2. 구현 인계가 사용자 명시 요청에 과도하게 의존

기존 흐름은 `USER_REQUESTED_CODEX_HANDOFF` / `ON_DEMAND_CODEX_HANDOFF`를 정상 구현 전환의 중심 trigger로 사용했다. 따라서 기획이 `IMPLEMENTATION_READY`여도 사용자가 별도로 Codex 전환을 말하지 않으면 GPT가 구현을 계속할 여지가 있었다.

### 3. Codex가 Notion을 구현 source로 반드시 읽는 계약이 약함

기존 handoff는 GitHub·프로젝트·Godot current truth 재조사는 강했지만, Notion 사람용 기획·Flow·승인 Visual과 AI/System 세부 구현 계약을 **구현 시작 전 필수 rehydration source**로 명시하는 강도가 부족했다.

### 4. 이미지 생성 책임이 Codex 금지로 닫히지 않음

GPT 이미지 생성 정책은 강했지만 Codex 쪽에는 `이미지 생성/생성형 편집 금지 → Notion 승인 Visual만 소비 → 부족하면 GPT_VISUAL_REQUEST`라는 반대편 consumer contract가 없었다.

### 5. GPT→PowerShell→local Codex가 기본 경로로 남음

`ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`, project-dedicated local environment 등은 당시 문제를 해결한 유효한 capability였지만, 새 역할에서는 GPT/사용자가 매번 local Codex를 띄우는 기본 workflow가 아니라 **Codex execution environment가 스스로 freshness와 local toolchain을 관리하는 내부 실행 책임**으로 이동해야 한다.

## 선택지 비교

| 안 | 내용 | 장점 | 문제 | 판정 |
|---|---|---|---|---|
| A | 기존 optional Codex 유지, 문구만 보완 | 변경량 최소 | GPT가 구현 owner로 되돌아갈 구조 유지 | REJECT |
| B | 모든 작업을 Codex로 강제 | 역할이 단순 | 기획·Notion·이미지 작업에도 불필요한 executor cost/복잡도 | REJECT |
| C | 기획/검수/Visual은 GPT, 구현이 존재할 때만 Codex 필수 | 책임 명확, 중복 감소, Notion/GitHub handoff 강화 | 기존 consumer/test migration 필요 | ADOPT |

권장/채택: **C**.

## 현재 교정된 active owner

- `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
- `templates/custom-instructions.codex.md`
- `skills/maintaining-project-context-and-handoff/SKILL.md`
- `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`

Notion readback:

- `Base · 작업 시스템 & Skill 지도`
- `P08 · AI Operations & External Executors`

## 역할 분리 후 정상 lifecycle

```text
GPT
→ current GitHub + Notion canon 복원
→ 기획·벤치마킹·대안 비교
→ 적대적 검토·IRG
→ 시스템/데이터/UI/UX/Flow/Visual/Acceptance 설계
→ 필요한 이미지 제작·검수·Notion 승인 delivery
→ IMPLEMENTATION_READY

implementation 없음
→ GPT review/readback/종료

implementation 있음
→ CODEX_IMPLEMENTATION_HANDOFF
→ Codex: GitHub + Notion rehydrate
→ optional technical preflight when risk warrants
→ code/data/Scene/Resource/config/test/build/runtime implementation
→ actual evidence
→ GPT final review
→ merge gate
```

### Visual dependency loop

```text
Codex BUILD
→ 승인 Visual 존재?
   ├─ yes: Notion approved attached/readback Visual 소비
   └─ no: WAITING_GPT_VISUAL + GPT_VISUAL_REQUEST
          → GPT brief / 사용자 승인 / 생성·편집 / 검수
          → Notion approved upload/attach/readback
          → Codex fresh-read / resume
```

## 적대적 검토 Loop

### Loop 1 — Role ownership attack

공격:
- GPT가 연결된 filesystem/tool을 보유한다는 이유로 제품 code/runtime를 직접 구현할 수 있는가?
- Codex가 여전히 `OPTIONAL_CODEX_EXECUTOR`라서 Implementation Ready 뒤 빠질 수 있는가?
- 사용자 `Codex로 넘겨` 문구가 없으면 BUILD가 막히는가?

교정:
- `GPT_PLANNING_REVIEW_VISUAL_OWNER`
- `CODEX_IMPLEMENTATION_EXECUTOR`
- `IMPLEMENTATION_REQUIRES_CODEX_HANDOFF`
- `USER_REQUESTED_CODEX_HANDOFF`는 compatibility trigger로만 낮춤
- GPT 제품 code/Scene/Resource/runtime 구현을 기본 금지

결과: canonical policy/route/handoff 수준에서는 교정. **Tests/secondary consumer migration 미완료로 전체 clean 아님.**

### Loop 2 — Canon rehydration attack

공격:
- Codex가 GPT handoff 또는 GitHub만 읽고 Notion의 최신 기획·Flow·Visual을 놓칠 수 있는가?
- Notion AI/System 세부 작업면이 구현자에게 연결되지 않는가?
- 다른 Project relation을 잘못 읽을 수 있는가?

교정:
- `CODEX_REHYDRATE_GITHUB_AND_NOTION`
- handoff에 `notion_sources.project_home`, `relevant_domain_pages`, `ai_system_detail_pages`, `approved_visual_records`
- Project/branch/open workstream identity fresh-read

결과: canonical owner에서 교정. Notion Base/P08에도 동일 흐름 반영 및 destination readback 수행.

### Loop 3 — Visual boundary attack

공격:
- Codex가 구현 편의를 위해 임시 AI art/placeholder를 생성하는가?
- GitHub/local에 파일이 있다는 이유만으로 승인 Visual로 간주하는가?
- 이미지가 없으면 전체 구현이 불필요하게 중단되는가?

교정:
- `CODEX_IMAGE_GENERATION_FORBIDDEN`
- `CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY`
- prototype은 명시적 current-use `APPROVED_CANDIDATE`, production은 `PROJECT_ASSET_APPROVED + rights/provenance + target path`
- `GPT_VISUAL_REQUEST`
- 독립 구현은 visual wait 중 계속 가능

결과: canonical policy/handoff/custom-instructions/Notion P08에서 교정.

### Loop 4 — Non-regression attack

공격:
- 역할을 단순화하면서 기존 적대적 검토·벤치마킹·IRG·TDD·runtime evidence·open PR 보호·rollback·merge gate가 약해지는가?
- Fresh PowerShell/local execution safety capability가 통째로 삭제되는가?

교정:
- 기존 quality gates는 역할 분리와 독립적으로 유지
- `CODEX_PREFLIGHT_OPTIONAL`은 유지: optional인 것은 **별도 Plan**, Build ownership이 아님
- local freshness capability는 삭제하지 않고 Codex execution environment 책임으로 migration하도록 handoff 지정
- open PR #660 포함 독립 open/draft/ready workstream read-only

결과: 정책 의도는 보존. consumer/test migration 뒤 regression 재검증 필요.

### Loop 5 — Consumer / evidence attack

공격:
- active test/registry/generated docs가 옛 계약을 계속 PASS 조건으로 강제하는가?
- CI가 새 계약과 충돌하는 사실을 실제로 잡는가?

실제 증거 — PR #674 head `96b393080e453ba07a5b61d3857834007300fbb9`:

성공:
- `Validate Base Partition Contract`: SUCCESS
- `Validate Skill Routing Precision`: SUCCESS
- whitespace validation: SUCCESS
- required-check topology: SUCCESS
- generated artifact/integrity topology step: SUCCESS

실패:
- `Validate One-Shot Local Executor Bootstrap`: FAILURE
- `Validate Base v9 Operating Contracts`: FAILURE
- `Validate Game Project Operating System`: FAILURE

`docs-validation-diagnostics`의 `tests.test_gpt_codex_workflow_contract`는 **137 tests 중 9 failures**를 반환했다.

실패한 9개:

1. `test_base_rules_require_agent_merge_after_all_gates`
2. `test_canonical_policy_separates_gpt_codex_plan_and_build`
3. `test_continuous_work_can_handoff_same_approved_scope_without_reapproval`
4. `test_explicit_approval_inherits_merge_authority_without_reapproval`
5. `test_gpt_is_primary_and_codex_is_optional_executor`
6. `test_handoff_reference_requires_latest_main_and_read_only_plan`
7. `test_handoff_resume_requires_fresh_runtime_session_identity`
8. `test_handoff_skill_has_implementation_package_mode`
9. `test_on_demand_handoff_allows_gpt_preproduction_and_optional_codex_preflight`

또한 `test_one_shot_local_executor_bootstrap_contract.py`는 현재 canonical workflow policy에 다음 과거 token이 계속 존재할 것을 요구한다.

- `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`
- `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`
- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED`
- `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`

이는 새 역할에서 단순 삭제할 대상이 아니라 **Codex execution-environment freshness owner로 의미를 migration하고 test를 새 owner에 맞게 수정해야 할 대상**이다.

결과: **CLEAN_REVIEW_EXIT 불가. `PARTIAL / CODEX_IMPLEMENTATION_REQUIRED`.**

## CI finding의 의미

이번 실패는 새 설계 자체의 증거가 아니라, Base가 과거 contract를 여러 test/consumer에 강하게 고정해 둔 결과다. 따라서 테스트를 단순 삭제하거나 assertion을 약화하면 안 된다.

Codex migration은 다음 원칙을 지켜야 한다.

```text
old safety capability
→ semantic responsibility 확인
→ 새 owner/contract로 relocation
→ regression test를 새 의미로 재작성
→ old active literal 제거
→ historical snapshots 보존
→ full/maximal available verification
```

## Codex 구현 handoff

상세 실행 명세:

`docs/handoffs/2026-08-25-gpt-codex-role-split-codex-handoff.md`

최우선 migration 대상:

- `tests/test_gpt_codex_workflow_contract.py`
- `tests/test_one_shot_local_executor_bootstrap_contract.py`
- `tests/test_p08_ai_operations_contract.py`
- `tests/test_base_long_horizon_work_contract.py`
- `tests/test_base_partition_contract.py`
- `tests/test_pr530_selective_integration_contract.py`
- `skills/SKILL_REGISTRY.json`
- generated skill/index consumer
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- `docs/operations/BASE_PARTITION_MANIFEST.json`
- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `skills/orchestrating-deepseek-worktrees/SKILL.md`
- one-shot/local executor active consumer

목록은 baseline search에서 얻은 후보이며 Codex는 fresh repository-wide inventory를 다시 만들어야 한다.

## 작업지시문 상태

사용자가 2026-08-25 중간에 **“작업지시문 작성은 나중에”**라고 변경했다.

따라서:

```yaml
project_instruction_revision:
  current_promotion: DEFERRED
  generated_r6_material: DRAFT_DEFERRED_NOT_CANON
  current_task_scope: BASE_AND_NOTION_ROLE_ALIGNMENT_ONLY
```

이미 생성된 r6 material에는 `DRAFT_DEFERRED` 경고를 추가했으며, 현재 정본 승격 근거로 사용하지 않는다.

## 이전 → 현재 capability 비교

| Capability | 이전 | 현재 | 판정 |
|---|---|---|---|
| GPT 기획·벤치마킹·검수 | 있음 | 유지 | KEEP |
| 최소 3안 비교 | 있음 | 유지 | KEEP |
| 적대적 검토 최소 5회/clean | 있음 | 유지 | KEEP |
| IRG/evidence ceiling | 있음 | 유지 | KEEP |
| Notion 사람용 정본 | 있음 | 유지 | KEEP |
| GitHub 구현/runtime 정본 | 있음 | 유지 | KEEP |
| GPT 제품 코드/POC 구현 | 허용 | 기본 금지 | REMOVE_FROM_GPT |
| Codex Build | optional executor | 구현 존재 시 implementation owner | STRENGTHEN |
| Codex Plan | optional | optional 유지 | KEEP |
| Codex current truth | GitHub/프로젝트/Godot 중심 | GitHub + Notion 필수 | STRENGTHEN |
| 이미지 제작 | GPT pipeline 있음 | GPT 전담 + Codex 생성 금지 | STRENGTHEN |
| 승인 Visual 소비 | 일반 asset 계약 | Notion current-use approval + attach/readback | STRENGTHEN |
| missing visual | 명시 loop 없음 | GPT_VISUAL_REQUEST | ADD |
| GPT local Codex bootstrap | 기본 지원 | 기본 workflow에서 폐기 | REMOVE_FROM_GPT |
| local freshness safety | bootstrap에 존재 | Codex execution environment로 migration | KEEP/MOVE |
| Open PR 보호 | 있음 | 유지 | KEEP |
| Required checks/merge gate | 있음 | 유지 | KEEP |
| 작업지시문 revision | r5 current | 후속 작업으로 보류 | DEFER |

## 기대효과

- GPT가 기획과 구현 사이를 오가며 책임이 흐려지는 문제 감소.
- Codex가 대화 요약만 믿지 않고 GitHub·Notion을 같은 시작점에서 읽어 구현 drift 감소.
- Notion 승인 Visual이 구현 입력 계약에 직접 연결되어 이미지 누락·오용 감소.
- Codex가 이미지를 임의 생성하지 않아 시각 정본·승인 흐름 보존.
- local Codex bootstrap을 사용자/GPT 반복 절차에서 빼면서 기존 freshness·wrong-target 안전성은 Codex 실행환경의 regression으로 보존 가능.
- 기존 품질 Gate를 제거하지 않고 역할 경계만 단순화하므로 장기 재작업 감소.

## 현재 판정

```yaml
planning_policy_alignment: PASS_FOR_CHANGED_CANONICAL_OWNERS
notion_base_readback: PASS
notion_p08_readback: PASS
work_instruction_revision: DEFERRED_NOT_CANON
repository_consumer_migration: FAIL_PENDING_CODEX
ci: FAIL_EXPECTED_FROM_STALE_CONTRACTS
adversarial_loop_minimum_reached: 5
clean_review_exit: false
merge_ready: false
```

PR #674는 Draft를 유지한다. Codex가 consumer/test migration과 fresh verification을 끝내기 전에는 Ready/merge로 승격하지 않는다.