# P08 · AI Operations & External Executors

## 목적

P08은 AI instruction/context, model/cost routing, 선택적 외부 executor, worktree 격리와 실행 재수화의 semantic owner다. 역할 판단은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 통합 실행 계약을 따른다.

## 현재 역할 계약

```text
UNIFIED_WORK_EXECUTION
CAPABILITY_BASED_EXECUTOR_SELECTION
CHAT_QUICK_DISCUSSION_DEFAULT
WORK_LONG_MULTISTEP_EXECUTION_DEFAULT
ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
```

현재 승인된 Work 세션은 보유 capability에 따라 기획·조사·벤치마킹·상세 설계·코딩·테스트·검토·정본 갱신·PR 통합까지 수행한다. 제품 코드, Python/JSON 또는 Base 운영 인프라라는 파일 종류만으로 다른 실행자로 전환하지 않는다. capability는 사용자 승인·저장소 권한·보호 경로를 대체하지 않는다.

- 기획·대안 비교·적대적 검토·IRG와 실제 구현의 연결을 같은 승인 계약에서 유지한다.
- Base 정책·Skill·Guide·Template·Learning·허용된 CI/test contract도 승인 범위와 보호 규칙에 따라 처리한다.
- 게임 제품은 project canon이 선택한 engine adapter의 code / Scene / Resource / runtime data / save-load / UI / shader / VFX / build / test를 연결한다.
- 기존 Godot 프로젝트는 `GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER`와 프로젝트가 채택한 버전·저작 권위를 유지한다. 통합 실행은 엔진 변경 권한이 아니다.
- runtime이 없으면 해당 검증은 `NOT_RUN`으로 남긴다. 구현·정적 검사 등 독립적으로 준비된 승인 작업은 계속하며, 필수 runtime 증거가 없는 완료·release 주장은 막는다.

## Chat / Work / 선택적 executor 라우팅

### `CHAT_QUICK_DISCUSSION_DEFAULT`

빠른 질문·설명, 짧은 브레인스토밍·선택지 비교, 사용자 결정이 필요한 단일 쟁점 정리와 실행 전 탐색에 사용한다.

### `WORK_LONG_MULTISTEP_EXECUTION_DEFAULT`

여러 단계의 기획·구현·검증·교정·정본 readback이 필요한 작업은 Work에서 이어간다. Work는 실행 작업면이며 새 정본 저장소가 아니다. 승인 결과와 상태는 current repository owner에 기록하고 readback한다. Notion은 명시된 V4 exception 또는 고유 자료가 남은 legacy migration scope에서만 사용한다.

```text
current repository + approved work contract
→ planning / detailed design
→ implementation with available authorized tools
→ tests / runtime evidence / correction
→ review / canon / permitted PR integration
→ remaining work and evidence readback
```

다른 executor는 사용자 요청, 현재 세션에 실제로 없는 capability, 또는 격리 실행의 구체적인 이점이 있을 때만 선택한다. Codex도 이 조건으로 선택할 수 있는 실행면이며 코드가 있다는 이유로 필수 전환하지 않는다. 별도 handoff 파일을 매 작업 만들지 않는다.

## Shared Work project instruction

프로젝트별 ChatGPT Work의 공용 실행 adapter는 다음 두 파일을 하나의 bundle로 사용한다.

```text
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
```

기본 입력은 **`프로젝트명 + 공용 작업지시문`**이며 Goal은 선택 사항이다. Goal이 없으면 current repository에서 `current stage → active/approved current work → blockers/dependencies → roadmap/accepted frontier → next safe playable slice → current work contract`를 복원한다. 사용자에게 이미 정본에 있는 목표를 다시 묻지 않는다.

본체와 appendix는 planning/reuse/verification, execution-scope, toolchain freshness, local Godot/Fresh Shell, retired-surface, prompt-efficiency 경계를 보존하는 하나의 실행 bundle이다. 다운로드 파일로 결합할 수 있으나 독립 정본을 만들지 않는다.

Default memory는 discovery-only 후보로 사용한다. `skills/SKILL_REGISTRY.json` trigger와 current work contract에 맞는 Skill만 progressive-load하며 최신 Base의 상세 owner와 프로젝트 채택 계약을 구분한다.

## 조건부 Handoff

```text
explicit user request / missing capability / justified isolated executor
→ exact repository SHA + approved scope + actual remaining work
→ selected executor fresh-read
→ project engine adapter / approved asset / permission checks
→ bounded implementation or verification
→ actual evidence returned and reviewed
```

기존 파일명 `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`는 Codex가 선택된 경우의 호환 Template로 유지한다. 같은 세션에서 실행할 수 있으면 기존 Plan·Acceptance·checkpoint를 재사용한다. 엔진 baseline/adapter owner는 `docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md`다.

## 외부 AI

DeepSeek 등 외부 AI는 대량 초안·분류·비교·독립 반례에 선택적으로 사용할 수 있다. 결과는 `REVIEW_PENDING`이며 current canon과 실제 산출물에 대조해 검수한다. 외부 AI를 선택했다는 사실은 권한·비용·검증의 자동 승인이 아니다.

## Rehydration

현재 또는 인계받은 executor는 변경 전에 다음을 fresh-read한다.

1. exact project/repository/worktree와 source SHA
2. project AGENTS/Active Context와 승인 계약
3. current GitHub product/operation paths와 실제 consumer
4. relevant repository human projection/Domain/AI-System surface; 명시된 V4 Notion exception은 적용 범위만
5. 승인 Visual의 repository path / SHA-256 / manifest
6. current open workstream과 보호 범위
7. 실제 runtime/test evidence와 `NOT_RUN`
8. selected engine adapter / stable engine baseline

## 이미지

```text
IMAGE_TOOL_REQUIRED_FOR_GENERATION_AND_EDITING
GENERATED_CANDIDATE_IS_NOT_APPROVED_ASSET
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
```

이미지 생성·생성형 편집은 실제 이미지 도구로 수행한다. 필요한 후보는 consumer·brief·현재 승인 범위에 맞게 만들며, 사용자 승인 전에는 후보로 유지한다. 승인 뒤 repository binary·SHA-256·consumer·provenance·manifest를 확인하고 runtime에 연결한다. 실행자 이름만으로 생성 기능을 금지하지 않는다. 이미지 도구나 승인이 없으면 해당 의존 작업을 보류하고 독립 작업은 계속한다.

## 비용과 Open PR 보호

`ZERO_INCREMENTAL_COST_REQUIRED`, `CURRENT_PAID_PLANS: GPT_PRO`를 유지한다. 별도 API/SaaS/compute 비용은 사용자 승인 없이 기본 경로로 만들지 않는다.

다른 open/draft/ready PR은 기본 read-only다. current-task continuation의 허용 범위에서도 exact HEAD, required checks, review, unresolved thread, ruleset과 postmerge readback을 확인한다. force push, direct main push, admin/ruleset bypass, history rewrite, destructive reset을 하지 않는다.

## 실패 조건

- 앱 이름이나 코드 파일 종류만으로 필수 인계 또는 실행 금지를 만듦
- capability를 사용자 승인·저장소 권한으로 오인함
- runtime `NOT_RUN`을 PASS로 표시하거나 독립 구현 전체를 자동 중단함
- Work 대화 상태를 repository 정본 대신 사용함
- project canon의 engine adapter 또는 승인 자산을 임의 변경함
- 이미지 도구 없이 생성하거나 candidate를 승인 자산으로 승격함
- stale repository/asset/권한 정보로 실행함
- external AI 결과를 검수 없이 current canon으로 승격함
- 별도 Goal이 없다는 이유로 current canon 조회 전 사용자의 목표를 다시 질문함

## 완료 기준

같은 승인 후보 계보의 공유 검토 예산은 전체 정확히 2회다. Part·Final Integration별로 초기화하지 않는다. 이후 결함별 교정·검증만 계속한다. 정본: `docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md`.

> **현재 승인된 Work는 보유 capability로 기획부터 구현·검증·검토·허용된 통합까지 이어가며, 실제로 필요한 경우에만 다른 실행자로 인계한다. 완료 상태는 실행자 이름이 아니라 실제 증거로 판정한다.**
