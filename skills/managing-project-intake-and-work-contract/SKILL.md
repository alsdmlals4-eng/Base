---
name: managing-project-intake-and-work-contract
description: Use when routing a project request, closing material ambiguity, defining a work contract, or sequencing approved dependent work.
---

# Managing Project Intake and Work Contracts

> `BASE_CURRENT_OPERATIONAL_BOOTSTRAP` / `PROJECT_WORK_FRESH_BASE_ENTRY`: for **ordinary target-project work** and Base maintenance that need current PM/intake/workflow guidance without project-side preinstallation, read `docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md`. It is a nonpersistent PM/workflow overlay: target-project `AGENTS.md`, product canon, protected paths and adopted Base release retain authority. Do not copy the detailed playbook into this file. Scoped learning and regression provenance: `references/base-current-project-work-bootstrap/LEARNING_LOG.md`.


## Core principle

요청 접수는 `의도 파악 → Work Mode 자동 선택 → Skill 자동 선택 → 필요한 Skill Mode 선택 → 사실 조사 → first-prompt 방향 고정 → 실행 계약 → Grill Me 정합성 확인 → 필요 시 작업 분해·순서화 → 실행 보고`인 하나의 상태 흐름이다.

사용자는 Skill 이름이나 mode를 선언할 필요가 없다. Registry trigger와 현재 작업 단계로 필요한 최소 Skill·Skill Mode만 자동 선택하고, 실제 사용 이유와 얻은 결과를 최종 보고에 남긴다.

모든 L1 이상 지시문 작성은 이 Skill에서 좋은 프롬프트 변환을 수행한 뒤 `Grill Me alignment gate`로 의도·기획·범위가 맞는지 확인한다. 유효한 승인 없이 제품·프로젝트 작업으로 진행하지 않는다.

새 기능 또는 기능 계약·공개 경계를 의미 있게 바꾸는 요청은 작업 크기와 무관하게 이 Skill의 intake를 거친다. 작은 단일 파일·단일 단계라도 L1 intake 대상이며, 작업 분해가 필요하지 않더라도 기능 계약의 정본 owner, 공개·통합 경계, 실제 consumer·의존 방향, 검증·롤백을 기존 실행 계약과 실행계획에 연결한다.

Registry의 승인된 작은 작업 비사용 조건은 이미 승인·정의된 기능 경계를 그대로 구현하는 continuation에만 적용한다. 새 기능 또는 공개 계약·상태 소유권·consumer 연결이 생기거나 바뀌면 작은 변경으로 intake를 우회하지 않는다.

실행자 선택은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 `UNIFIED_WORK_EXECUTION` / `CAPABILITY_BASED_EXECUTOR_SELECTION`을 따른다. 현재 Work가 승인된 저장소 수정·명령·엔진·검증 도구를 실제 사용할 수 있으면 같은 계약으로 구현까지 진행한다. 앱 이름·코드 파일 때문에 역할을 나누거나 강제 인계하지 않는다. `CAPABILITY_IS_NOT_AUTHORIZATION`을 유지하며 부족한 증거만 `NOT_RUN` / `BLOCKED_UNVERIFIED`로 구분한다.

## User-visible approval brief

`VISIBLE_IMPLEMENTATION_BRIEF_BEFORE_APPROVAL`: 새 변경은 실제 수정 전에 다음 내용을 한국어로 보여주고 승인받는다. 이는 내부 first-prompt만 작성하는 것으로 대체되지 않는다.

1. **이해한 의도:** 원 요청과 재구성한 목표, 사실과 가정을 구분한다.
2. **현재 상태:** 구현됨/없음/미확인과 실제 owner·consumer 근거.
3. **변경·보호 범위:** 추가·수정·제외와 유지할 동작.
4. **다음 작업·구현 방법:** 순서·선행 조건·데이터/모듈/UI/자산 연결과 위험한 선택. 승인 전 구현 방향을 숨기지 않는다.
5. **산출물·완료 기준:** 사용자가 무엇을 사용·테스트할 수 있는지와 관찰 가능한 결과.
6. **검증·위험·결정:** 실제 검사 계획, 롤백, 비용·권한·미확정 사항과 이번 승인 대상.

분량은 결정에 필요한 만큼이다. L0 오탈자도 새 변경이면 `현재 → 변경 / 대상 / 확인 방법`의 짧은 승인안을 보여주되 전체 intake·인터뷰·새 문서를 강제하지 않는다. 읽기 전용 조사·설명에는 변경 승인을 만들지 않는다. 단순 요청 자체, 침묵, 조사 허용을 아직 보여주지 않은 실행안의 승인으로 추정하지 않는다.
이미 제시한 동일 계약에 대한 명시적 승인·`진행해`는 승인 참조로 기록해 재사용한다. 같은 범위의 구현·실패 교정·검증·허용된 정상 병합마다 재승인하지 않는다. 새 범위·핵심 의미·비용·보안·파괴적 행위가 생기면 해당 변화만 다시 결정받는다.
승인 전 `implementation_outline`은 방법·의존성·Acceptance를 검토하기 위한 제안이다. `decompose-and-sequence`의 실행 확정은 승인 후다. 구현 준비를 핑계로 수정부터 시작하거나, 상세 코딩 결정을 모두 사용자에게 넘기지 않는다.
기존 `templates/EXECUTABLE_PROMPT.md`를 draft/confirmed 구분으로 재사용한다. 채팅 승인안으로 충분하면 별도 문서를 생성하지 않는다.

## Context-fit check after routing and consolidation

`CONTEXT_FIT_RECHECK`: 먼저 요청·현재 단계로 후보 Skill을 좁히고, 정본·실제 consumer를 확인한 뒤 각 후보의 trigger/비사용 조건/필수 입력·출력·검증 경계를 다시 맞춘다. 현재 필요한 주 책임과 보조만 선택하고 나머지는 deferred로 둔다.
흡수·통합·reference 이동 뒤에도 이 검사를 한 번 수행해 활성 entrypoint → 선택 Skill → 필요한 reference → 실제 consumer/validator를 따라간다. 통합했다는 이유로 관련 스킬을 전부 재로드하지 않는다. 바뀌지 않은 같은 source의 읽기·승인·검증 근거는 재사용하고 새 범위·실패·정본 변경 시 영향 경로만 다시 읽는다.
새 모듈/Skill은 금지 대상이 아니다. 기존 owner 확장, 조건부 reference/module, 독립 Skill을 비교해 독립 trigger·입출력·권한·검증 경계와 실제 consumer가 있을 때만 만든다. 스킬 수 감소 자체가 목표가 아니며 generic catch-all Skill로 합치지 않는다.
아래 `contract-module` 표시는 저장소 검증용 묶음이다. 실행 때 모든 module을 로드하라는 지시가 아니다. `tools/skill_context.py`는 선택한 reference만 읽고 링크 누락을 검사하며, 승인 강제·도구 권한 또는 앱의 스킬 자동 선택을 대신하지 않는다.

## Mandatory pre-build planning gate

현재 권한·정본·실제 consumer·동일 Goal PR을 먼저 읽는다. 승인 없는 BUILD, 다른 PR 무단 흡수, source 미확인 상태의 사실 확정은 금지한다.
`FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`, `REUSE_FIRST_PREFLIGHT_REQUIRED`, `BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED`는 현재 영향 범위에서 수행한다. 전체 repository/Skill 로드는 요구하지 않는다.
`LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED`: ACTIVE/COMPATIBILITY/ARCHIVE/OBSOLETE/UNKNOWN을 구분하고, 참조·consumer·복구 가능성 없이 삭제하지 않는다.
신규 L1+ preflight에는 [조사·승인·증거 Gate](references/preflight-and-evidence.md)를 읽는다. 같은 범위의 유효한 증거는 `REUSED_EVIDENCE`로 재사용한다.
`PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT`와 `USER_APPROVAL_BEFORE_BUILD`의 사용자-facing 형태는 아래 승인안이다. 구현 후에는 필요한 정본 동기화·검토·exact-head CI·정상 병합·readback을 닫고 `NOT_RUN`을 PASS로 바꾸지 않는다.
<!-- contract-module: references/preflight-and-evidence.md -->

`CONTINUATION_INTENT_ALIASES`는 `[연속작업] 진행해`뿐 아니라 이미 승인된 동일 계약에 대한 `진행해`, `계속해`, `남은 작업 진행` 같은 명확한 계속 실행 의도를 인식한다. 유효한 approval reference가 있을 때만 `APPROVED_CONTRACT_CONTINUATION`으로 [continuous-work-execution.md](references/continuous-work-execution.md)를 적용해 남은 범위에 `CONTINUOUS_WORK_ACTIVE`를 결합한다. 이는 `PLAN / BUILD / REVIEW`를 대체하거나 새 범위를 승인하지 않으며, 사용자 전용 결정·미검증 차단·고위험 외부 행위의 확인 Gate를 제거하지 않는다. blocker가 생기면 즉시 전역 종료하지 않고 `recover → local defer → independent ready work → global stop last` 순서로 처리한다.

명시적인 user-directed 계속 작업에서 `same-goal`의 `in-progress PR`이 이미 있으면 `USER_DIRECTED_PARALLEL_PR`로 라우팅한다. 기존 PR은 read-only overlap evidence로만 확인하고 **do not modify/rebase/update** 하며, **current completed main**에서 **separate branch/PR**을 만든다. ordinary same-workstream coordination에서 허용된 경우 `synchronizing-local-and-github-state`의 concurrent preflight와 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 사용할 수 있다.

그러나 `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 항상 먼저 적용된다. 현재 작업의 더 구체적인 승인 계약이 다른 open/draft/ready PR 또는 다른 workstream을 `read-only / no absorption`으로 지정하면 standing copy-integration보다 우선한다. 그 PR의 material delta를 own 작업으로 가져오려면 **explicit absorption authorization**이 별도로 있어야 하며, 다른 workstream에는 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`을 충족해야 한다. 없으면 overlap 탐지·경로 회피·main의 이미 병합된 결과 재평가만 수행하고 selective copy·재구현·흡수·close·supersede 처리를 하지 않는다.

흡수가 명시적으로 허용된 ordinary coordination에서만 `PROVISIONAL_INTEGRATION`을 사용한다. owner PR branches는 read-only로 보존하고 필요한 material delta만 selective copy·재구현한 뒤 semantic reconciliation과 exact-head 검증을 수행한다. `absorbed_owner_deltas`와 `residual_owner_deltas`로 coverage를 증명한다. `scheduled/periodic` repository-writing automation도 unrelated open PR 존재 자체를 전역 blocker로 사용하지 않고 실제 path/semantic overlap만 국소 조정한다. 상세 경계는 [continuous-work-execution.md](references/continuous-work-execution.md)와 `synchronizing-local-and-github-state`를 따른다.

공개 영상의 source 복구, 새 AI/MCP/addon/CLI/framework/Skill/Mode 평가가 필요하면 [외부 source·도구 라우팅](references/external-source-and-tool-routing.md)을 읽는다. 외부 용어 발견은 설치·비용·권한·신규 제작의 승인이 아니다.
<!-- contract-module: references/external-source-and-tool-routing.md -->

## Terminology

- `Work Mode`: AI의 현재 작업 자세·권한·증거 기준. `PLAN / BUILD / REVIEW` 중 한 시점에 하나를 주로 사용한다.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 전문 작업 계약.
- `Skill Mode`: 한 Skill 안에서 선택하는 세부 절차. 이 문서의 `route`, `first-prompt`, `clarify` 등이 해당한다.
- `Prompt`: 사용자의 현재 목표·제약·산출물. Skill 선언문이 아니다.
- `Direction anchor`: 지시문 가장 앞에서 핵심 행동·결과·지배 기준을 고정하는 1~2문장. 배치 순서는 권한을 만들지 않는다.
- `Continuous Work`: 유효한 승인 계약과 `CONTINUATION_INTENT_ALIASES`가 함께 있을 때 `APPROVED_CONTRACT_CONTINUATION`으로 활성화되는 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 상태. Work Mode가 아니라 승인된 계약 안에서 다음 미완료 작업으로 계속 이동하는 orchestration flag다.

상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

승인 결정 복원·중복 질문 방지·Repository/Notion 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

프로젝트 workspace 권위: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` (`DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`, `REPOSITORY_PRIMARY_CANON`, `HUMAN_GDD_PDF_DERIVED_VIEW`, legacy Notion/Google Sheets migration boundary). V3 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`은 `V3_COMPATIBILITY_AND_HISTORY_ONLY`이며 신규 project work route가 아니다.

legacy Google Sheets 해석·이관이 필요한 경우에만 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 compatibility 계약을 참고한다. 이는 신규 입력이나 active workspace 권위를 만들지 않는다. 기존 consumer가 사용하는 legacy literal `project_google_sheet`는 `google_sheet_compatibility_source`의 호환 alias일 뿐이며 신규 Sheet·active sync·정본 권위를 뜻하지 않는다.

연속작업 활성화·자동 승인·blocker recovery·종료 경계: [continuous-work-execution.md](references/continuous-work-execution.md)

예기치 않은 실행 중단의 Retry/Resume·Watchdog 신호·중복 실행 방지: [task-recovery-protocol.md](references/task-recovery-protocol.md)

## Skill Modes

- `route`: 요청 의도·현재 단계·위험을 파악하고 Work Mode, 작업 수준, 변경 유형, 주 책임 분야와 최소 Skill 집합을 자동 판정한다. `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 계속 실행 의도와 기존 approval reference를 함께 감지한다.
- `first-prompt`: 핵심 방향 문장을 지시문 가장 앞에 배치하고 Task·Context·Source·Constraints·Output·Validation을 순서화한 뒤 전체 계약과 충돌하지 않는지 검사한다. 상세 절차는 [first-prompt-direction-anchoring.md](references/first-prompt-direction-anchoring.md)를 사용한다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환하고, opt-in이 있으면 현재 승인 범위에 `continuous_work_state`를 결합한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다. 모든 L1 이상 지시문은 실행 전 `Grill Me alignment gate`를 거치며, 프로젝트 방향을 바꾸는 핵심 결정은 [grill-me-protocol.md](references/grill-me-protocol.md)를 사용한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.
- `execution-report`: 실제 실행한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다.

하나의 호출에서 필요한 Skill Mode만 순서대로 실행한다. L1 이상 지시문 작성의 기본 순서는 `route → first-prompt → contract → clarify`다. 이미 exact contract already approved 상태이고 유효한 approval reference가 있으면 `clarify`는 승인 재사용을 기록하고 중복 질문하지 않는다. `CONTINUATION_INTENT_ALIASES`는 미승인 계약을 임의 승인하지 않으며, `CONFIRMED` 또는 `REUSED_APPROVAL` 이후 현재 승인 범위에 연속 실행 상태를 적용한다. `decompose-and-sequence`는 `CONFIRMED` 이후에만 실행한다. L1 이상 작업 종료 시 `execution-report`를 실행하되 짧은 작업에서는 최종 답변의 한 섹션으로 압축할 수 있다.

## Work Mode selection

### `PLAN`

- 요구·근거·설계·정본·작업 순서를 확정한다.
- 읽기·조사·제안이 기본이며 승인 전 제품 동작·구조를 변경하지 않는다.

### `BUILD`

- 승인된 계약 범위의 코드·데이터·문서·자산을 구현한다.
- 단계별 검증·롤백을 유지한다.

### `REVIEW`

- 결과를 적대적으로 검토하고 반례·회귀·증거를 찾는다.
- 기본 읽기 전용이다. 수정까지 요청되거나 승인된 finding이 있으면 `BUILD`로 전환해 최소 수정하고 다시 `REVIEW`로 검증한다.

복합 작업은 `PLAN → BUILD → REVIEW`로 전환할 수 있지만 한 시점의 주 Work Mode는 하나다. `CONTINUOUS_WORK_ACTIVE`에서도 이 규칙은 동일하다.

## Automatic selection policy

- 사용자가 Skill·Skill Mode를 언급하지 않아도 현재 요청과 Registry trigger를 비교한다.
- `load_by_default=false`는 자동 선택 금지가 아니라 trigger 불일치 시 읽지 않는다는 뜻이다.
- trigger가 일치하고 `do_not_use_when`에 걸리지 않는 최소 집합만 사용한다.
- 새 기능 또는 기능 계약·공개 경계의 의미 변경은 trigger가 일치한 것으로 보고, 작업 크기·단계 수와 무관하게 intake와 기능 계약 reference를 사용한다.
- 주 책임 분야 Skill은 최대 하나다. Foundation·검증·발행·Handoff는 현재 단계에 필요한 것만 추가한다.
- 사용자에게 “어떤 Skill을 쓸까요?”라고 선택을 전가하지 않는다.
- 사용자가 Skill을 지정해도 trigger·권한·비사용 조건과 충돌하면 그대로 실행하지 않고 이유를 설명한다.
- 새 범위·실패·정본 변경이 생기면 Work Mode와 Skill 라우팅을 다시 계산한다.
- Skill 파일을 읽은 것과 Skill 절차를 실제 실행한 것을 구분한다.
- 실제 capability gap·사용자 지정 인계 등 workflow owner의 조건으로 다른 실행자에게 넘길 때는 `first-prompt → contract → clarify`의 유효한 동일 계약과 승인 참조를 재사용한다. 인계 때문에 같은 질문·계획을 다시 만들지 않는다.
- 신규 실행 기술 제작 압력이 감지되면 설계 Skill보다 기존 대안 평가 Skill을 먼저 호출하고 `existing_solution_disposition`을 계약 입력으로 요구한다.
- 유효한 approval reference 또는 명확한 계속 실행 의도 중 하나라도 없으면 `CONTINUOUS_WORK_INACTIVE`로 유지하고 기존 승인·Grill Me 흐름을 바꾸지 않는다.

## Use when

- 새 L1 이상 요청 또는 여러 분야에 걸친 요청을 접수한다.
- 기능·게임 경험·아트 방향·아키텍처·워크플로·Base 변경을 결정한다.
- 새 기능 또는 기능 계약·공개 경계·상태 소유권·consumer 연결을 만들거나 의미 있게 바꾼다. 단일 파일·단일 단계의 작은 기능도 포함한다.
- 요청이 짧거나 모호하거나 여러 파일·산출물에 영향을 준다.
- 승인된 요구를 Issue·Goal·Plan 또는 실행 프롬프트로 넘긴다.
- GPT·Codex·외부 AI용 작업 지시문을 작성하거나 개선한다.
- 큰 작업을 단계·의존성·병렬 묶음·게이트로 분해한다.
- 범위가 바뀌어 분야·Skill·검증·실행 순서를 다시 계산한다.
- 새 MCP·addon·CLI·framework·Skill·Mode 또는 기존 실행 권위와 겹칠 수 있는 도구를 제안한다.
- 사용자가 `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 등으로 현재 승인된 동일 계약의 연속 실행을 명시적으로 요청한다.

## Do not use when

- 새 기능·기능 계약·공개 경계 변경이 없는 오탈자나 명확한 단일 파일 기계 수정인 L0 작업은 전체 intake 예외다. 새 변경의 짧은 승인안·승인 경계까지 면제하지 않는다.
- 입력과 판정 기준이 동일한 검사를 재실행한다.
- 승인된 Plan에 분야·범위·완료·검증·실행 순서가 이미 확정됐고 기능 계약·공개 경계·상태 소유권·consumer가 변하지 않았다. 이때 기존 approval reference를 재사용한다.
- 저장소 변경·결정·검증이 없는 단순 설명이다.
- 요구가 확정되지 않았는데 구현 세부 순서부터 고정하려 한다.

## Required inputs

`PROJECT_WORK_KANBAN_CHECKLIST`: `benchmark_preflight_receipt`, `context_configuration_hygiene`, `project_work_kanban`은 위 `request` metadata나 `existing_solution_evidence`의 하위 필드가 아니다. L1+ 작업에서 project/Base repository가 소유하는 **같은 root receipt JSON의 형제 필드**다. 별도 빈 PM 보드나 두 번째 상태 정본을 만들지 않는다. 아래 예시는 `validate_work_contract_receipt.py`의 실제 start 실행 Gate에 전달할 수 있는 최소 구조이며, 실제 작업에서는 예시 값을 fresh-read evidence, 현재 승인 Goal과 그 Goal의 모든 필수 작업으로 바꾼다.

WORK_CONTRACT_RECEIPT_ROOT_JSON_EXAMPLE: root receipt를 작성·검증할 때 [실행 가능한 전체 JSON 예시](references/work-contract-receipt-example.md)를 읽는다. 접수 분류만 할 때 예시 전문을 미리 로드하지 않는다.

실행 경로는 `python <resolved-Base-root-at-current-Base-or-project-adapter-pin>/tools/validate_work_contract_receipt.py --receipt <repository-owned-json-receipt> --phase start --expected-source-sha <fresh-read-project-source-sha> --render-markdown`이다. Base root·adapter pin·receipt를 해석하지 못하거나 nonzero이면 `BLOCKED_UNVERIFIED`이며 새 설계·제작·구현을 시작하지 않는다. 작업 전환은 다음 승인 작업을 먼저 active로 기록한 뒤 같은 trusted source와 `--phase resume`으로 검사한다. 마감은 모든 필수 작업을 같은 최종 HEAD에서 다시 검증하고 `--phase closeout --expected-source-sha <fresh-read-project-source-sha> --expected-head-sha <fresh-read-final-head-sha> --render-markdown`을 실행한다. `TRUSTED_VERIFICATION_TARGET_HEAD`: receipt의 `verified_head_sha`를 기대값으로 복사하지 않고 신뢰한 caller가 final HEAD를 별도로 읽는다.

현재 요청, 확인한 정본·실제 consumer, 범위/제외/보호, 승인 참조, 산출물·검증을 우선 복원한다. 해당하지 않는 외부 도구·migration·workspace 입력은 만들지 않는다.
L1+ root receipt를 작성·검증할 때 [입출력·실행 순서 계약](references/contract-shapes-and-sequencing.md)을 읽는다. source SHA·benchmark·hygiene·PM gate를 생략하지 않는다.
<!-- contract-module: references/contract-shapes-and-sequencing.md -->

## Read first

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, repository-owned Asset/Reference/Benchmark와 exact-SHA derived PDF; V4 exception/legacy source는 적용 조건이 기록됐을 때만
4. `docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json`, current adoption profile/matrix, `REUSABLE_MODULE_REGISTRY.md`
5. 현재 결정과 관련된 기존 Base knowledge/case/reference owner
6. Registry/profile/current bottleneck이 가리키는 경우에만 직접 관련 다른 프로젝트의 검증된 implementation/pattern evidence
7. legacy Sheet에 UNIQUE 미이관 material이 실제 있을 때만 `google_sheet_compatibility_source`
8. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
9. 현재 Issue·Plan·책임 원본과 실제 파일
10. `SKILL_REGISTRY.json`
11. 신규 MCP·addon·CLI·framework·Skill·Mode이면 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`와 Godot 평가 Skill
12. L1 이상 지시문 작성 시 [first-prompt-direction-anchoring.md](references/first-prompt-direction-anchoring.md)
13. 필요한 경우 [question-and-source-model.md](references/question-and-source-model.md)
14. 종료 판정이 필요한 경우 [ambiguity-and-closure.md](references/ambiguity-and-closure.md)
15. Grill Me 정합성 확인과 핵심 결정 인터뷰가 필요한 경우 [grill-me-protocol.md](references/grill-me-protocol.md)
16. `CONTINUATION_INTENT_ALIASES`와 유효한 승인 계약이 함께 있으면 [continuous-work-execution.md](references/continuous-work-execution.md)
17. 새 기능 또는 기능 계약·공개 경계를 만들거나 의미 있게 바꾸는 경우에는 작업 분해가 필요하지 않은 작은 기능을 포함해 [work-decomposition-and-sequencing.md](references/work-decomposition-and-sequencing.md); 그 밖에는 작업 분해·순서화가 필요할 때만 읽는다.

## Workflow

### 1. Route automatically once

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

새 기능 또는 기능 계약·공개 경계의 의미 변경은 크기가 작아도 `L1` 이상으로 분류한다. 이미 승인된 기능 경계를 그대로 구현하는 작은 continuation만 기존 approval reference로 intake 재작성을 생략할 수 있다.

최종 결정을 소유하는 `primary_discipline`은 하나만 지정한다. 실제 입력·산출물·검증이 바뀌는 분야만 `affected_disciplines`에 추가한다.

```text
요청 의도·현재 단계·위험
→ PLAN / BUILD / REVIEW
→ Registry trigger·do_not_use_when
→ 최소 Skill 집합
→ 각 Skill의 필요한 Skill Mode
→ CONTINUATION_INTENT_ALIASES와 approval reference 존재 여부
→ CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE 후보
```

발행·검증 Skill은 해당 단계에 도달할 때까지 `deferred_skills`에 둔다. Handoff Skill은 실제 인계가 필요할 때만 선택하며 같은 Work에서 직접 구현하는 경로의 필수 단계가 아니다. 연속작업 후보는 승인 상태가 확인되기 전 실행 권한이 아니다.

### 1.5 Existing Solution First Gate

신규 MCP·addon·CLI·framework·Skill·Mode·execution layer 요청이면 다음을 `PLAN`의 첫 blocker로 둔다.

```text
current environment inventory
→ connected MCP·enabled addon·dependency·existing implementation
→ open/recent PR
→ maintained external solution
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
→ adversarial review
→ user-visible approval state
```

`existing_solution_disposition`이 없으면 `AWAITING_EXISTING_SOLUTION_REVIEW`다. `BUILD_NEW`는 대안으로 해결할 수 없는 차단 결함과 사용자 승인이 모두 있어야 하며, 없으면 custom design·code·PR을 만들지 않는다.

### 1.6 Reuse-First Project Preflight

새로 만들거나 의미 있게 바꾸는 시스템·메커닉·데이터/콘텐츠 구조·UI/UX·시각/Asset·도구/자동화·workflow·Skill/Eval·QA/Test는 tool-only Existing Solution First보다 넓은 `REUSE_FIRST_PREFLIGHT_REQUIRED`를 적용한다.

```text
current project authority + actual implementation/assets/tests
→ Project Asset/Reference/Benchmark already approved or collected
→ PROJECT_WORK_REUSE_HANDOFF + adoption profile/matrix + REUSABLE_MODULE_REGISTRY
→ Base accumulated knowledge/case/reference relevant to this decision
→ targeted cross-project verified evidence only when directly pointed to
→ decision-relevant external benchmark/professional practice/success-failure cases
→ owner-specific reuse/adapt/reference/no-reuse disposition
→ new creation only for the unresolved gap
```

`NOT_RUN`은 신규 제작·`BUILD_NEW`를 차단한다. `REUSED_EVIDENCE`는 동일 승인 범위·같은 consumer·freshness 확인을 만족할 때만 쓴다. `NOT_APPLICABLE`은 새 설계 판단이 없는 기계적 변경에만 이유와 함께 사용한다. 재사용 때문에 프로젝트 고유 규칙·표현·플레이어 경험을 평준화하지 않는다.

### 2. Inspect repository facts

최신 `main`, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본과 실제 repository 파일에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. Notion은 `V4_NOTION_EXCEPTION_ONLY`에 해당할 때만 그 scope를 읽고 exception 또는 migration provenance를 별도로 기록한다. legacy Sheet는 `google_sheet_compatibility_source`에 UNIQUE 미이관 material이 있을 때만 migration evidence로 읽는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

### 3. Build one requirement model

```text
원 요청
→ 문제·목적
→ 사용자·플레이어 경험
→ 범위·비목표
→ 제약·보호 대상
→ 산출물
→ 완료 기준
→ 검증
→ 미검증·보류
```

### 3.1 Build the first prompt

모든 L1 이상 지시문 작성은 [first-prompt-direction-anchoring.md](references/first-prompt-direction-anchoring.md)를 사용한다.

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
→ conflict scan
```

- 핵심 행동·의도한 결과·지배 기준을 1~2문장으로 압축해 지시문 가장 앞에 둔다.
- Task, Context, Source, Constraints, Output, Validation을 명확히 분리한다.
- 정석안·파격안·통합안은 설계·결정 탐색에 실제 가치가 있을 때만 같은 기준으로 비교한다.
- 앞 문장이 전체 계약을 좁히거나 과장하거나 뒤의 `HARD_CONSTRAINT`와 충돌하면 전체 지시문을 다시 작성한다.
- first-prompt는 초안이며 아직 실행 권한이 없다.

### 3.5 Apply the neutral-recommendation-gate

권장안·판정·설계 선택이 있으면 사용자안과 AI 최초안을 같은 기준으로 비교한다.

```yaml
evaluation_criteria: []
alternatives: []
counterevidence: []
benefits_costs_and_risks: []
reversibility:
unknowns_and_evidence_limits: []
recommended_conclusion:
agreement_or_disagreement_reason:
```

- 사용자안이 검토를 통과하면 근거와 함께 동의한다.
- 다른 안이 더 강하면 차이를 만드는 증거와 함께 권장한다.
- 반대를 위한 반대를 만들지 않는다.
- 증거 부족은 `BLOCKED_UNVERIFIED`로 남긴다.
- L1 이상 기능·설계·아키텍처·정책·방향 결정은 `running-adversarial-review-and-refinement`의 `attack → validate-critique → decision-report`를 PLAN 사전판정 지원 Skill로 실행한다.
- 이 판정의 승인 finding은 `refine-approved-findings`에서 주 책임 분야 Skill BUILD로 한 번만 구현·수정하고, `regression-recheck → decision-report`로 복귀한다.

### 4. Run the Grill Me alignment gate

좋은 프롬프트 변환과 실행 계약 작성 뒤, 실행 전 `Grill Me alignment gate`로 의도·기획 정합성을 확인한다.

- 결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다.
- 기존 Decision이 유효하면 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부·초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.
- 상세 요청은 처음부터 다시 인터뷰하지 않고 direction anchor와 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.
- 계약이 완전하지만 승인되지 않았다면 direction anchor·범위·보호 대상·산출물·검증을 한 번 보여 주고 명시적 승인을 받는다.
- exact contract already approved 상태이면 approval reference를 기록하고 중복 질문 없이 `REUSED_APPROVAL`로 통과한다.
- 중대한 승인 또는 확인이 없으면 `AWAITING_USER_CONFIRMATION`을 유지하고 BUILD·위임·실행으로 이동하지 않는다.

### 5. Closure and confirmation

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

확인 결과는 `CONFIRMED` 또는 `REUSED_APPROVAL`과 approval reference로 기록한다.

### 5.5 Activate bounded continuous work for an approved contract

`[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 `CONTINUATION_INTENT_ALIASES`가 있고 현재 계약이 `CONFIRMED` 또는 `REUSED_APPROVAL`이면 `APPROVED_CONTRACT_CONTINUATION`으로 [continuous-work-execution.md](references/continuous-work-execution.md)를 적용해 `CONTINUOUS_WORK_ACTIVE`로 전환한다.

```text
현재 승인된 작업 계약
→ ready task 선택
→ BUILD
→ REVIEW attack → validate-critique
→ 범위 안의 기술적 단일 최소 안전 권장안이면 자동 승인 간주
→ BUILD 최소 반영
→ REVIEW regression-recheck
→ blocker가 있으면 recovery ladder
→ 당장 해결 불가한 국소 task는 defer
→ 독립 ready task 계속
→ 상태 변화 뒤 deferred task 재평가
→ 완료 또는 GLOBAL_TERMINAL_BLOCKER까지 반복
```

`USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위는 자동 승인하지 않는다. 그러나 그 상태가 국소적이거나 복구 가능하면 전체 루프를 즉시 종료하지 않는다. `RECOVERABLE_VERIFICATION_BLOCKER`와 `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`는 재조회·대체 증거·authorized alternate executor를 먼저 시도하고, 당장 풀리지 않으면 해당 task만 defer한다. `GLOBAL_TERMINAL_BLOCKER`는 recovery path를 소진하고 실행 가능한 독립 task가 없을 때만 사용한다. 유효한 계약이나 계속 실행 의도가 없는 요청은 `CONTINUOUS_WORK_INACTIVE`다.

### 6. Produce, sequence and report the approved contract

승인된 범위의 실행 계약·의존성·세부 작업·실제 수행 보고는 [입출력·실행 순서 계약](references/contract-shapes-and-sequencing.md)을 사용한다. 기존 Plan/receipt의 참조를 재사용하며 새 빈 추적표를 만들지 않는다. 승인 전 사용자에게 구현 개요를 보여주는 것은 이 단계의 BUILD·실행 확정과 다르다.

## Project workspace handling

`NO_NEW_NOTION_WRITE_BY_DEFAULT`: Notion/Sheets는 아래 명시적 예외·이관 조건 외 기본 쓰기 대상이 아니다. 승인된 변경은 `REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK`로 repository owner와 적용되는 사람용 view에 반영한다.

```yaml
workspace_authority: DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
project_canon: REPOSITORY_PRIMARY_CANON
human_facing_view: HUMAN_GDD_PDF_DERIVED_VIEW
notion: LEGACY_OPTIONAL_READ_ONLY_MIGRATION_SOURCE
google_sheets: MIGRATION_COMPATIBILITY_ONLY
google_sheet_compatibility_source: OPTIONAL_LEGACY_MIGRATION_INPUT
```

- 최신 repository 정본·실제 파일을 현재 계획·결정·구조화·runtime truth로 읽고, 사람용 PDF에는 exact source SHA와 evidence ceiling을 기록한다.
- `CURRENT_CODEX_HANDOFF.md`는 실제 인계가 있을 때만 사용하는 조건부 경로다. 같은 Work의 재개 정보는 기존 Active Context·작업 계약에 유지하며 별도 handoff 문서 생성을 요구하지 않는다.
- Base 채택은 승인된 운영 규칙에 한정한다. 프로젝트의 engine/version·저장 호환성·제품 의미·자산 승인·보안 계약은 최신 Base를 관찰했다는 이유로 조용히 교체하지 않는다.
- Base 자체 작업처럼 project-scoped migration surface가 적용되지 않으면 목적지를 발명하지 않는다.
- 기존 Notion 또는 Google Sheet가 실제 존재하면 고유 사용자 자료를 `UNIQUE / DUPLICATE / OBSOLETE`로 판정한다. `UNIQUE`만 repository 또는 명시적 non-canon 보관소로 이관 → readback/Test → consumer/reference 확인한다.
- Notion과 Sheet는 신규 입력·active Decision sync·완료 판정에 필요하지 않으며 신규 프로젝트에 생성하지 않는다. V4 예외는 explicit user approval, owner, scope, measurable value, revisit/exit 조건이 있을 때만 적용한다.

## State model

```text
RECEIVED
→ ROUTED
→ AWAITING_REUSE_PREFLIGHT | AWAITING_EXISTING_SOLUTION_REVIEW | PROMPT_DRAFTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED | REUSED_APPROVAL
→ CONTRACT_READY
→ EXECUTION_PLAN_READY
→ EXECUTED
→ REPORTED
→ SUPERSEDED | ABANDONED
```

연속작업은 위 상태 머신을 대체하지 않는 직교 실행 flag다.

```text
CONTINUOUS_WORK_INACTIVE
→ (CONTINUATION_INTENT_ALIASES + CONFIRMED/REUSED_APPROVAL)
→ CONTINUOUS_WORK_ACTIVE
→ COMPLETE | STOPPED_USER_DECISION | GLOBAL_TERMINAL_BLOCKER | STOPPED_BY_USER
```

`BLOCKED_UNVERIFIED`, `EVIDENCE_TRANSPORT_INCOMPLETE`, `DEFERRED_EXTERNAL_EXECUTOR`는 개별 task/evidence 상태가 될 수 있으며 자동으로 전역 종료 상태가 되지 않는다.

## Output contract

새 변경: 사용자-facing 승인안 + `AWAITING_USER_CONFIRMATION`. 승인/동일 계약: `CONFIRMED | REUSED_APPROVAL` + approval reference + 다음 미완료 작업. 실제 receipt·실행 보고의 필드는 [입출력·실행 순서 계약](references/contract-shapes-and-sequencing.md)에 있다.

## Definition of Done

의도·범위·구현 개요·완료 기준을 사용자에게 보여줬고 필요한 승인이 있는가? 적용 source·consumer·Skill/reference가 연결됐는가? 기존 승인·안전·실행 증거를 보존했는가? 실행하지 않은 것을 완료라고 하지 않는가?
전체 intake 교정·마감 검사에는 [완료·실패 체크](references/intake-completion-checks.md)를 사용한다.
<!-- contract-module: references/intake-completion-checks.md -->

## Failure conditions

승인 없이 새 변경을 실행하거나, 같은 승인에 질문을 반복하거나, 관련 없는 Skill/reference를 전부 읽거나, 선택한 필수 지침을 부분 읽기해 생략하면 실패다. 사용자 원문·보호 범위·반대 근거·미검증을 잃는 축약도 실패다.

## Legacy aliases

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `grill-me`, `grillme`, `Grill Me` → `clarify` + [grill-me-protocol.md](references/grill-me-protocol.md)
- `transforming-requests-into-prompts` → `first-prompt` + `contract` + `clarify`
- `[좋은 프롬프트]`, `좋은 프롬프트`, `퍼스트 프롬프트`, `first prompt` → `first-prompt` + `contract` + `clarify`
- `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` → 유효한 현재 승인 계약 + [continuous-work-execution.md](references/continuous-work-execution.md)

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## Base v9.4 지시 권위·Context 큐레이션

L1 이상 Prompt 계약에서 강한 지시를 추가하기 전에 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 권위를 분류한다. 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 완화하지 않는다.

입력·출력·불변조건·실패조건·검증을 예시보다 먼저 정의하는 Interface-first 계약을 사용한다. 예시는 정상·실패·경계·회귀 Fixture 또는 Golden Set으로 보존한다.

Direction anchor와 first-prompt 순서화는 [first-prompt-direction-anchoring.md](references/first-prompt-direction-anchoring.md)를 따른다. Context 큐레이션은 현재 `decision_question`을 고정한 뒤 권위·freshness·representation·deduplication·known conflicts·반대 근거·`progressive_load_trigger`·`refresh_trigger`를 기록한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.

## BCP-008 L2+ 명세 추적성

`L2 이상` 작업에서 승인된 요구가 여러 Task·파일·검증으로 분산되면 `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`를 사용한다. 이 Packet은 **별도 책임 원본이 아니다**. intake는 Decision·Requirement·Acceptance ID와 범위를 연결하고, 분야 정본·실제 구현·검증의 내용을 복제하지 않는다.

```text
Decision
→ Requirement
→ Acceptance Criteria
→ Task
→ Implementation Path
→ Verification Evidence
```

- `L0·L1`에는 기본 적용하지 않는다. 다만 실제 영향이 여러 시스템·파일로 확장되면 작업 수준을 다시 판정한다.
- Packet 생성 자체를 완료로 보지 않고 `coverage_status`, `unmapped_items`, `BLOCKED_UNVERIFIED`를 기록한다.
- 문서 정본 연결은 `managing-design-documents`, 실제 diff·테스트 증거 대조는 `reviewing-and-validating-project-changes`가 소유한다.
- 같은 ID를 새 문서마다 재정의하거나 별도 Spec 정본을 만들지 않는다.
