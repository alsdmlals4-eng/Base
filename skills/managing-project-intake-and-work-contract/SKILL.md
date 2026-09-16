---
name: managing-project-intake-and-work-contract
description: Use when routing a project request, closing material ambiguity, defining a work contract, or sequencing approved dependent work.
---

# Managing Project Intake and Work Contracts

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

## 최소 진입과 재개

읽기 전용 조사·설명은 `PLAN`에서 관련 정본·실제 파일·필요한 원출처를 확인하고 근거·권장안·미검증을 보고한다. 파일 변경, 새 실행 receipt, 구현 승인 대기는 만들지 않는다. 이 예외는 이미 승인된 실행 작업을 조사 보고로 축소하는 권한이 아니다.

새 변경은 `route → first-prompt → contract → clarify`로 한 번 접수한다. 같은 승인 범위 재개는 승인 참조·잔여 작업·현재 source 변경분을 복원해 `REUSED_APPROVAL`로 이어간다. 컨텍스트 초기화 자체는 새 인터뷰·계획·승인·전체 검토 예산 초기화 사유가 아니다.

1. 최신 사용자 지시 → 프로젝트 `AGENTS.md`가 지정한 read order → 현재 `main`/작업 브랜치·dirty 상태 → 현재 결정/Active Context → 실제 대상·consumer·테스트 → 같은 Goal PR을 확인한다.
2. 프로젝트의 채택 Base 계약과 원격 최신 Base의 drift를 구분한다. 원격이 새롭다는 이유로 engine·저장·제품 의미·자산 승인을 교체하지 않는다.
3. Registry trigger/use/do-not-use로 현재 단계의 최소 Skill만 고른다. 발행·검증·인계 Skill은 해당 단계까지 deferred다.
4. 기존 구현·승인 자산·관련 Base 근거를 먼저 비교한다. 같은 범위·consumer·freshness의 benchmark는 `REUSED_EVIDENCE`로 재사용한다.
5. 중요한 새 설계·정책 선택에는 실제 대안을 비교한다. 이미 승인된 해법·단일 정답의 결함 수정에 허수 대안이나 새 문서를 만들지 않는다.
6. 승인 범위 안의 구현·교정·검증·정상 PR 병합·readback은 계속한다. 새 범위·비용·보안·핵심 의미·파괴적 변경은 사용자 결정이다.

`OPEN_PR_READ_ONLY_BY_DEFAULT`: 다른 open/draft/ready PR은 조사만 한다. current-task continuation의 좁은 병합 예외는 `docs/GPT_CODEX_WORKFLOW_POLICY.md`를 따른다. 명시적 흡수 승인 없이 다른 작업의 delta를 가져오거나 수정·종료하지 않는다.

필수 source를 읽지 못하면 해당 근거와 의존 작업은 `BLOCKED_UNVERIFIED`다. 원문을 추정하지 않는다. 별도 근거·승인이 있는 독립 작업은 계속할 수 있고, 사용자가 전체 중단을 지시했거나 모든 작업이 그 source에 의존하면 중단한다.

독립 작업으로 전환할 때는 [연속 작업·복구](references/continuous-work-execution.md)의 active-task preflight 재결합 절차를 따른다. 차단된 root preflight를 그대로 통과시키거나 원 source를 PASS로 바꾸지 않는다.

## 조건별 읽기

| 현재 필요한 판단 | 읽을 reference |
|---|---|
| 새 L1+ 설계/제작 preflight 또는 해당 Gate 감사 | [조사·승인·증거](references/preflight-and-evidence.md) |
| L1+ 지시문 작성 | [방향·범위·승인 정합성](references/first-prompt-direction-anchoring.md) |
| 실제 receipt 작성·실행 순서·종료 보고 | [입출력·실행 순서](references/contract-shapes-and-sequencing.md) |
| root receipt 작성·검증 | [전체 JSON 예시](references/work-contract-receipt-example.md) |
| 여러 유효 선택·다분야 분해·라우팅 충돌 또는 L2+ 다중 Task·파일·검증 추적 | [라우팅·의사결정 상세](references/routing-and-decision-details.md) |
| legacy 이관·workspace 예외·PR 중첩·구형 alias | [workspace·호환 상세](references/workspace-and-compatibility.md) |
| 승인된 동일 계약을 계속 실행 | [연속 작업·복구](references/continuous-work-execution.md) |
| 새 기능/공개 계약/상태 소유권/consumer 변경 또는 분해 필요 | [기능별 코드·계약과 순서](references/work-decomposition-and-sequencing.md) |
| 중요한 사용자 의미 결정이 남음 | [Grill Me 정합성](references/grill-me-protocol.md) |
| 공개 영상·새 AI/외부 도구 평가 | [외부 source·도구](references/external-source-and-tool-routing.md) |
| 질문·정본 구별 / 종료 모호성 / 예기치 않은 중단 | [질문·source](references/question-and-source-model.md), [종료](references/ambiguity-and-closure.md), [중단 복구](references/task-recovery-protocol.md) 중 해당 항목만 |
| intake 전체 교정·마감 검사 | [완료·실패 체크](references/intake-completion-checks.md) |

Godot authority·Godot addon 평가는 **실제 Godot 엔진·저작·씬·리소스 consumer가 있는 도구 작업**에만 추가한다. 일반 Base 문서·Skill·비-Godot 도구 요청에는 분야 owner와 Existing Solution First를 사용한다.

새 기능·공개 계약·상태 소유권·consumer 변경은 작업 분해가 필요하지 않은 작은 기능을 포함해 [work-decomposition-and-sequencing.md](references/work-decomposition-and-sequencing.md)를 읽는다. 단일 파일이라는 이유로 기능 계약을 생략하지 않는다.

`contract-module`은 저장소 검증용 합집합이다. 실행 시 모든 reference를 읽는 지시가 아니다.
<!-- contract-module: references/preflight-and-evidence.md -->
<!-- contract-module: references/contract-shapes-and-sequencing.md -->
<!-- contract-module: references/external-source-and-tool-routing.md -->
<!-- contract-module: references/intake-completion-checks.md -->
<!-- contract-module: references/routing-and-decision-details.md -->
<!-- contract-module: references/workspace-and-compatibility.md -->

## Skill Modes

- `route`: 요청 의도·현재 단계·위험을 파악하고 Work Mode, 작업 수준, 변경 유형, 주 책임 분야와 최소 Skill 집합을 자동 판정한다. `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 계속 실행 의도와 기존 approval reference를 함께 감지한다.
- `first-prompt`: 핵심 방향 문장을 지시문 가장 앞에 배치하고 Task·Context·Source·Constraints·Output·Validation을 순서화한 뒤 전체 계약과 충돌하지 않는지 검사한다. 상세 절차는 [first-prompt-direction-anchoring.md](references/first-prompt-direction-anchoring.md)를 사용한다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환하고, opt-in이 있으면 현재 승인 범위에 `continuous_work_state`를 결합한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다. 모든 L1 이상 지시문은 실행 전 `Grill Me alignment gate`를 거치며, 프로젝트 방향을 바꾸는 핵심 결정은 [grill-me-protocol.md](references/grill-me-protocol.md)를 사용한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.
- `execution-report`: 실제 실행한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다.

하나의 호출에서 필요한 Skill Mode만 순서대로 실행한다. L1 이상 지시문 작성의 기본 순서는 `route → first-prompt → contract → clarify`다. 이미 exact contract already approved 상태이고 유효한 approval reference가 있으면 `clarify`는 승인 재사용을 기록하고 중복 질문하지 않는다. `CONTINUATION_INTENT_ALIASES`는 미승인 계약을 임의 승인하지 않으며, `CONFIRMED` 또는 `REUSED_APPROVAL` 이후 현재 승인 범위에 연속 실행 상태를 적용한다. `decompose-and-sequence`는 `CONFIRMED` 이후에만 실행한다. L1 이상 작업 종료 시 `execution-report`를 실행하되 짧은 작업에서는 최종 답변의 한 섹션으로 압축할 수 있다.

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

## Output contract

새 변경: 사용자-facing 승인안 + `AWAITING_USER_CONFIRMATION`. 승인/동일 계약: `CONFIRMED | REUSED_APPROVAL` + approval reference + 다음 미완료 작업. 실제 receipt·실행 보고의 필드는 [입출력·실행 순서 계약](references/contract-shapes-and-sequencing.md)에 있다.

## Definition of Done

의도·범위·구현 개요·완료 기준을 사용자에게 보여줬고 필요한 승인이 있는가? 적용 source·consumer·Skill/reference가 연결됐는가? 기존 승인·안전·실행 증거를 보존했는가? 실행하지 않은 것을 완료라고 하지 않는가?
전체 intake 교정·마감 검사에는 [완료·실패 체크](references/intake-completion-checks.md)를 사용한다.
<!-- contract-module: references/intake-completion-checks.md -->

## Failure conditions

승인 없이 새 변경을 실행하거나, 같은 승인에 질문을 반복하거나, 관련 없는 Skill/reference를 전부 읽거나, 선택한 필수 지침을 부분 읽기해 생략하면 실패다. 사용자 원문·보호 범위·반대 근거·미검증을 잃는 축약도 실패다.
