# BCP-2026-037 · Work-native Project Execution Instruction

## 상태
`APPROVED_FOR_IMPLEMENTATION`

## approval_ref
`USER_CHAT_2026-08-26_WORK_NATIVE_PROJECT_INSTRUCTION`

사용자는 2026-08-26 현재 대화에서 앞으로 게임 프로젝트 작업을 ChatGPT Work에서 진행하고, 기존 `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL`의 기능을 누락 없이 Work에 맞게 교정·개선한 공용 지시문을 Base에 반영하고 다운로드 파일로 제공하도록 명시 승인했다.

최종 진입 요구는 **`프로젝트명 + 공용 작업지시문`만으로 정상 시작 가능**하게 하는 것이다. 별도 Goal은 사용자가 특정 작업을 명시적으로 우선하고 싶을 때만 선택적으로 주며 정상 시작 조건이 아니다. Goal이 없으면 Work가 GitHub/Notion/Base를 fresh-read하여 `current stage → active/approved current work → blockers/dependencies → roadmap/accepted frontier → next safe playable slice → current work contract`를 복원한다. Default memory는 연결 후보 탐색용 보조 기억으로만 사용한다.

## 문제
r5.4는 광범위한 capability를 보존하지만 다음 최신 Base 계약보다 먼저 작성됐다.

- Chat = 빠른 논의, Work = 긴 multi-step GPT-owned 비코딩 작업, Codex = 실제 게임 제품 구현.
- `ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE`와 project-canon-selected engine adapter. 기존 프로젝트는 Godot adapter 유지.
- `STABLE_ENGINE_BASELINE` / `NO_AUTOMATIC_LATEST_FOLLOW` / canary 기반 엔진 승격.
- production information은 text/table/DB/flow 우선, 생성 이미지는 `ACTUAL_CONSUMER_REQUIRED`.
- Default memory는 Work/reuse 후보 발견에 유용하지만 current project canon보다 낮은 authority.
- 사용자가 매번 별도 Goal·AGENTS/Notion/GitHub/Base/Memory 충돌검사를 반복 지시하지 않아도 되는 self-starting Work bootstrap이 필요하다.

짧은 재작성만 하면 r5.4가 여러 non-regression 교정에서 복원한 Slice, traceability, Visual, IRG, PR/CI, recovery, completion 기능이 다시 누락될 위험이 있다.

## 승인 구현안
`templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`와 compatibility appendix를 하나의 공용 Work 실행 bundle로 추가하고 regression contract를 둔다.

핵심 원칙:

```text
PROJECT_PLUS_INSTRUCTION_IS_DEFAULT_SUFFICIENT_INPUT
SEPARATE_GOAL_NOT_REQUIRED_BY_DEFAULT
PROJECT_PLUS_INSTRUCTION_PLUS_OPTIONAL_GOAL_IS_SUFFICIENT_INPUT
WORK_SELF_STARTING_FRESH_READ_BOOTSTRAP
DEFAULT_MEMORY_DISCOVERY_ONLY_NOT_CANON
MEMORY_CONFLICT_CURRENT_PROJECT_CANON_WINS
WORK_LONG_MULTISTEP_NONCODING_DEFAULT
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER
ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE
ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER_FOR_EXISTING_PROJECTS
STABLE_ENGINE_BASELINE
NO_AUTOMATIC_LATEST_FOLLOW
REUSE_FIRST_PREFLIGHT_REQUIRED
CURRENT_SKILL_REGISTRY_COVERAGE_GATE
PRODUCTION_INFORMATION_TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY
IMPLEMENTATION_REALITY_GATE
ADVERSARIAL_REVIEW_UNTIL_CLEAN
FULL_LOOP_COUNT_MINIMUM: 5
DOMAIN_SPLIT_CANON
OPEN_PR_READ_ONLY_BY_DEFAULT
CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE
REQUIRED_WORK_REMAINING_0_IS_COMPLETION_CANDIDATE
```

## r5.4 non-regression
다음은 근거 없이 삭제하지 않는다: Authority Recovery, Fresh-Read, Entry Reconciliation, Skill coverage, Whole Project Audit, Requirement Traceability, bounded decisions, core/pointed fun, creative quality, world/story, balance, benchmark, >=3 alternatives, Existing Solution First, partial absorption, Superpowers/TDD/debug/verification, Visual Delete Test/coverage/style lock, explicit image approval, Notion image readback, IRG, player evidence, first-session, localization/responsive, decision-screen comprehension, multi-platform shared core, Implementation Ready, Playable Slice, A/V POC, canonical reflection, Codex handoff, user-runnable play, Case Lookup, recovery ladder, Incident/Solution/Lesson, >=5 full adversarial loops until clean, PR/CI/readback, Notion↔GitHub sync, provenance/performance, Base reuse gate, completion rescan, NOT_RUN ceiling, user-learning report.

## 대안
- A `r5.4 그대로`: 최신 Work/Memory/engine/image 정책과 drift → REJECT.
- B `짧은 프롬프트 전면 재작성`: context는 작지만 edge gate 회귀 위험 큼 → canonical replacement로 REJECT.
- C `r5.4 capability superset + Work-native bootstrap + Base progressive load`: 기능 보존과 장기 적응성 균형 → RECOMMENDED/APPROVED.

## Skill routing
이번 Base 변경 자체에는 intake, skill audit, design-doc, adversarial review, change validation, reference freshness, long-running continuity, model/effort routing, Base change proposal owner를 적용한다. 프로젝트 실행에서는 Registry 전체를 inventory한 뒤 **복원된 current work contract 또는 사용자가 예외적으로 지정한 특정 작업**의 trigger와 맞는 Skill만 progressive-load한다. 모든 게임/UI/Visual/Godot Skill을 항상 호출하는 고정 목록을 만들지 않는다.

## 범위 제외
- 기존 게임 Unity migration 없음.
- runtime 변경 없음.
- 새 Skill 없음.
- Notion IA 재구축 없음.
- 새 유료 API/SaaS 없음.

## 동시성
기존 open/draft/ready PR은 read-only. PR #660 소유 경로와 PR #678의 `[수정제안서]/PROPOSAL_REGISTRY.json`은 수정하지 않는다. Proposal Registry reconciliation은 해당 concurrent ownership 종료 뒤 별도 current-main 작업으로 남긴다.

## 검증
구현 PR에서 r5.4 capability markers, default project+instruction entry, no-separate-Goal reconstruction, Work/Chat/Codex owner, memory authority, self-start bootstrap, Skill Registry progressive routing, engine adapter, stable baseline, image consumer, PR/CI/completion/evidence ceiling을 계약 테스트하고 최소 5회의 full-scope adversarial review 후 clean exit를 요구한다.
