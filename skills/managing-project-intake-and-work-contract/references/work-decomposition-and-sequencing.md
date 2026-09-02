# 작업 분해·의존성·실행 순서 모델

> `BASE_CURRENT_OPERATIONAL_BOOTSTRAP`: when current scope requires **Base-only maintenance** and future project sessions to fresh-read current Base without project-side preinstallation, read `docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md`. It is a nonpersistent PM/workflow overlay: target-project `AGENTS.md`, product canon, protected paths and adopted Base release retain authority. Do not copy the detailed playbook into this file.


이 문서는 `managing-project-intake-and-work-contract`의 `decompose-and-sequence` mode가 사용하는 상세 모델이다. 큰 요청을 체크박스 목록으로 잘게 자르는 것이 아니라, **각 단계가 검증 가능한 결과를 만들고 다음 단계를 안전하게 여는 실행 구조**를 만든다.

## 1. 입력 계약

```yaml
confirmed_work_contract:
current_stage_and_gate:
actual_repository_state:
protected_paths_and_behavior:
available_people_tools_and_permissions:
known_dependencies_and_blockers:
external_deliveries:
milestone_or_deadline:
validation_environment:
rollback_constraints:
benchmark_preflight_receipt:
context_configuration_hygiene:
project_work_kanban:
```

요구가 확정되지 않았거나 중요한 사용자 결정이 남아 있으면 실행 순서를 확정하지 않는다.

## 1.1 분해 전 누락·충돌 감사

분해 전에 최신 main, 현재 Decision, 관련 분야 정본, 동일 Goal의 열린·최근 병합 PR, 실제 구현과 개별 프로젝트 Sheet를 비교한다. `DUPLICATE_WORK`, `DUPLICATE_QUESTION`, `MISSING_CANON`, `MISSING_CONSUMER`, `CANON_CONFLICT`, `IMPLEMENTATION_CONFLICT`, `STALE_REFERENCE`, `MISSING_SYNC`가 있으면 새 작업 목록보다 복원과 정리를 먼저 배치한다. Base 저장소 자체의 Sheet 상태는 `BASE_EXCLUDED`다.

### 1.2 필수 benchmark·역공학 preflight, 범위 한정 hygiene와 PM 실행 Gate

`MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT` / `BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED`: Base·프로젝트의 모든 L1+ 작업은 분해·작성·구현보다 먼저 exact repository revision의 같은 책임·실제 consumer를 비교하고, task-appropriate current Base 사례·승인 Reference/Benchmark·직접 관련 유사 구현·필요한 공식 원출처를 조사한다. 결과는 repository-owned root receipt의 `benchmark_preflight_receipt`에 `state: PASS | REUSED_EVIDENCE | NOT_APPLICABLE | BLOCKED_UNVERIFIED`, entry별 `source_and_evidence`, `observed_pattern`, `project_fit_and_difference`, `disposition: ADOPT | ADAPT | REJECT`로 남긴다. `PASS`/`REUSED_EVIDENCE`는 최소 한 entry, `BLOCKED_UNVERIFIED`는 unreadable source/blocker, `NOT_APPLICABLE`은 L0의 이유를 요구한다. benchmark는 프로젝트의 장르·세계관·화면·버튼·시각 구도를 고정하는 catalog가 아니라, 현재 consumer와 계약에 맞는 더 효율적인 방향을 찾는 evidence다.

`LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED`: 시작 시 이번 scope의 context·설정·entrypoint·문서·생성물을 같은 root receipt의 `context_configuration_hygiene` scoped `inventory`에 `ACTIVE_OWNER | COMPATIBILITY | ARCHIVE | OBSOLETE_CANDIDATE | UNKNOWN_UNVERIFIED`로 분류하고, 각 항목에 path·owner/provenance·references/consumers readback을 남긴다. `NO_BROAD_SWEEP_WITHOUT_SCOPE`와 `NO_DELETION_BY_AGE_OR_NAME`을 지킨다. `OBSOLETE_CANDIDATE`를 실제 제거할 때만 receipt validator가 `REFERENCES_AND_CONSUMERS_ZERO_BEFORE_REMOVAL` 및 `GIT_RECOVERABLE_REMOVAL_AND_READBACK`을 요구하게 하고, 연결 문서·생성물·검증을 다시 확인한다. source나 consumer가 불명확하면 `UNKNOWN_UNVERIFIED`로 보존하고 entrypoint의 오인만 최소 교정한다.

`PROJECT_WORK_KANBAN_CHECKLIST` / `PM_EXECUTION_GATE_REQUIRED`: 위 두 기록만으로는 실행 권한이 생기지 않는다. 같은 repository-owned root receipt에 현재 승인 Goal의 필수 작업을 나타내는 `project_work_kanban`을 형제 필드로 두고, 기존 Issue·카드·owner를 재사용한다. 세 필드를 모두 기록한 뒤 다음 실제 실행 명령을 통과해야 한다.

```text
python <resolved-Base-root-at-current-Base-or-project-adapter-pin>/tools/validate_work_contract_receipt.py --receipt <receipt.json> --phase start --expected-source-sha <fresh-read-project-source-sha> --render-markdown
```

다음 승인 작업으로 전환할 때는 먼저 그 작업을 `IN_PROGRESS`와 `active_work_item_ref`로 기록하고 `--phase resume`으로 재검사한다. 승인 범위 마감은 모든 필수 작업의 evidence를 같은 최종 HEAD에서 다시 확인한 뒤 `--phase closeout --expected-source-sha <fresh-read-project-source-sha> --expected-head-sha <fresh-read-final-head-sha> --render-markdown`으로 검사한다. `TRUSTED_VERIFICATION_TARGET_HEAD`: receipt 안의 SHA를 기대값으로 되돌려 쓰지 않고 신뢰한 caller가 source와 final HEAD를 별도로 fresh-read한다. root 예시와 DONE 증거 계약은 `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md` §12.1과 `PROJECT_WORK_ITEM_CHECKLIST.md` §10을 따른다. 빈 PM 보드·미완료 작업 삭제·history-only `validate_receipt()` 호출로 실행 Gate를 우회하지 않는다.

## 2. 분해 단위

하나의 작업 항목은 다음을 모두 가져야 한다.

```yaml
step_id:
outcome:
why_now:
inputs:
files_or_systems:
owner_or_skill:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

위험·가치·불확실성을 검증하는 단계에는 다음 `Build-Measure-Learn` 계약을 추가한다.

```yaml
hypothesis:
minimum_test_unit:
element_purpose:
observation_method:
success_threshold:
failure_threshold:
integration_interface:
evidence_decision: KEEP / REVISE / REDUCE / REMOVE / RETEST
learning_destination: BASE_CANDIDATE / PROJECT_ONLY / NO_PROMOTION
```

- `Build`: 가설을 판정하는 데 필요한 `minimum_test_unit`만 만든다.
- `Measure`: 해석이 아니라 `observation_method`와 사전 선언한 성공·실패 기준으로 결과를 수집한다.
- `Learn`: 결과에 따라 `KEEP / REVISE / REDUCE / REMOVE / RETEST` 중 하나를 선택한다.
- 실제 결과가 없으면 `evidence_decision`을 비워 두거나 `RETEST`로 유지하며 성공으로 승격하지 않는다.

## 2.1 복합 작업의 요소 분해·통합

UI·시스템·데이터·이미지/아트·문서/Skill처럼 여러 요소가 맞물린 작업은 다음 순서로 분해한다.

```text
전체 목표·실패 가설
→ element_purpose별 구성 요소
→ 요소별 입력·출력·불변조건·최소 초안
→ 적용 가능한 다관점 검토
→ integration_interface와 결합 순서
→ 통합 결과
→ Golden Path·Edge·Regression
→ 회고와 재사용 경계
```

요소를 나눈 뒤 각각을 독립 제품처럼 최적화하지 않는다. 모든 요소는 상위 플레이어·사용자 경험과 `integration_interface`에 다시 연결돼야 하며, 통합 뒤에만 드러나는 상태·순서·소유권·피드백 충돌을 별도 검증한다.

좋은 단계는 “코딩하기”, “문서 수정하기”가 아니라 다음처럼 관찰 가능한 결과를 만든다.

- 저장 Schema와 마이그레이션 계약을 확정한다.
- 최소 정상·실패 fixture가 통과하는 파서를 구현한다.
- 대표 플레이 흐름이 목표 플랫폼에서 끝까지 실행된다.
- 변경된 정본의 모든 소비자와 파생본이 동기화된다.

## 2.2 기능별 코드·계약 모듈화

새 기능을 만들거나 기능·계약을 의미 있게 바꿀 때 **기능별 코드와 기능 계약은 같은 책임 경계로 설계한다.** Base의 Python·자동화 코드와 프로젝트 제품 코드 모두에 적용한다. 기존 모듈·계약·테스트를 먼저 재사용한다. 여기서 모듈은 독립적으로 설명·변경·검증할 수 있는 기능 책임 단위이며, 파일 수나 배포 패키지 수를 뜻하지 않는다.

프로젝트의 최신 `AGENTS.md`·채택 계약·기존 구조를 우선한다. Base 최신 버전으로 프로젝트 lock을 자동 교체하지 않는다. 기존 프로젝트를 일괄 재구성하지 않는다. 이번 승인 기능에 필요한 경계만 보완하고, 행동 보존 리팩터링은 baseline·consumer·회귀 증거가 있을 때만 포함한다. 새 프레임워크·패키지·유료 도구를 기본 요구하지 않는다.

### 경계와 크기

- 기능의 목적·비목표·공개 사용 방법·의존성을 내부 구현을 읽지 않고도 설명할 수 있게 한다. 함수마다 파일·클래스·인터페이스를 만들지 않는다. 작은 기능은 한 파일 또는 기존 문서의 한 절로 유지할 수 있다.
- 책임·변경 이유·상태 소유권·검증 경계가 달라질 때 분리를 검토한다. 늘 함께 바뀌고 별도 소비·검증 가치가 없는 조각은 합친다. 모듈별 검증 뒤에도 상위 플레이 흐름의 통합 검증을 생략하지 않는다.
- 코드·계약·데이터·테스트는 같은 기능 경계로 연결하되 물리적으로 같은 폴더에 둘 의무는 없다. 기존 저장소 경로와 문서 owner를 유지하며 상호 참조한다. 파일 이동이 필요하면 Scene/Resource 참조·NodePath·외부 consumer·저장 호환성과 롤백을 먼저 확인한다.

### 소프트 코딩과 고정 경계

프로젝트·장르·벤치마크·플랫폼·난이도·표현·화면 흐름처럼 달라질 수 있는 값은 명시된 데이터·구성·Resource·계약 입력 또는 project-local 설정 owner에서 한 번만 정의한다. 코드는 그 owner의 유효한 입력을 해석하고 적용하며, 동일한 가변 값을 조건문·문서·Scene·테스트 fixture에 따로 하드코딩해 두 번째 정본을 만들지 않는다.

보안 경계, 프로토콜 식별자, 저장 키, 공개 호환 계약처럼 고정이 필요한 값은 하드코딩을 허용하는 이유·owner·변경/마이그레이션 경로와 함께 기록한다. 이 고정 경계는 임의의 프로젝트 취향·밸런스·화면 버튼·벤치마크 결론을 대신하지 않는다. 가변 값의 초기값, 허용 범위, fallback, version, consumer 영향과 정상·경계·잘못된 구성 fixture를 계약에 연결한다. 구성값이 누락되거나 유효하지 않으면 추측으로 기본 동작을 발명하지 않고 명시된 fallback 또는 `BLOCKED_UNVERIFIED` 처리로 남긴다.

모든 값을 추상화하거나 범용 configuration framework를 새로 만들지 않는다. 한 번만 쓰이고 프로젝트 의미가 변하지 않는 내부 구현 상수는 가까운 책임 코드에 둘 수 있다. 반대로 같은 값을 둘 이상의 consumer가 해석하거나 프로젝트별로 바뀔 가능성이 있으면 기존 data/resource/config owner 또는 얇은 project adapter에 올린다. external JSON, Resource, Scene metadata, environment/config, 코드 상수 중 무엇을 쓸지는 현재 프로젝트의 엔진·저장·검증·배포 제약과 실제 consumer를 비교해 정하며, Base가 하나의 형식을 강제하지 않는다.

### 기존 작업 계약에 연결할 정보

별도 Registry·추적표·문서 세트를 의무 생성하지 않는다. 다음 정보는 위 작업 항목과 현재 기능 계약의 기존 필드·절·링크에 담는다. 아래 표는 새 공용 Schema가 아니다. 적용되지 않는 항목은 이유를 기록하고, 아직 없는 구현은 계획 상태로 구분한다.

| 기존 위치 | 기능별로 연결할 내용 |
|---|---|
| `step_id / outcome` | 작업 ID와 구별되는 기존 기능 ID 또는 이름, 사용자 가치, 책임·비목표. 작업 단계와 기능 모듈을 일대일로 강제하지 않는다. |
| `files_or_systems / owner_or_skill` | 기능 계약의 정본 owner, 실제 구현·데이터·테스트 위치, 변경 책임. 계획 경로는 실제 존재하는 consumer로 표시하지 않는다. |
| `inputs / output / integration_interface` | 입력·출력 타입, 공개 함수·signal/event, 상태 소유권·전이, 불변조건. 적용되는 오류·취소·재시도·중복 실행의 의미와 부작용·초기화/종료 조건도 포함한다. |
| `dependencies / parallel_with` | 의존 방향과 실제 consumer 경로를 기록한다. 공유 상태·자원, 연결 지점과 병렬 수정 금지 경계를 확인한다. |
| `variation_owner / fixed_boundary` | 프로젝트별 변동 값의 단일 data/config/Resource/adapter owner, 초기값·허용 범위·fallback·version과 consumer를 기록한다. 하드코딩한 불변 보안·호환 경계는 이유·owner·변경/마이그레이션 경로를 기록한다. |
| `acceptance_criteria / validation` | 정상·경계·실패 fixture, 공개 계약 일치 검사, consumer 통합 검사와 해당 실행 명령·환경·결과·증거. |
| `rollback` | 실패 시 복원 방법, 영향을 받는 공개 계약·저장 형식의 호환성, 필요한 이관·백업·복구 검증. |

기능 계약의 정본 owner는 하나만 둔다. 공용 불변조건은 기존 owner를 참조하고 기능별 차이만 해당 계약이 소유한다. 같은 수치·규칙·Schema를 코드·문서·JSON에 중복 정본으로 만들지 않는다. 구현 세부를 문서에 전사하지 않고 권위 있는 선언·데이터·테스트를 참조한다. 책임 원본을 여러 계약에서 사용하는 것과 같은 사실을 여러 곳에서 따로 관리하는 것은 구별한다.

다른 기능의 내부 상태를 직접 수정하거나 내부 구현 경로에 결합하지 않는다. 필요한 상호작용은 좁은 공개 함수·데이터·signal/event 또는 명시적 연결 지점으로 표현한다. 순환 의존·숨은 전역 상태·소유권 충돌을 검토한다. 단순 연결에 불필요한 인터페이스 클래스·범용 manager·추상 계층을 추가하지 않는다.

### Godot 연결

구체적인 엔진 책임은 `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`를 재사용한다. 프로젝트가 채택한 엔진 버전에서 Scene·Node·Resource·Script·Autoload의 실제 역할과 consumer를 확인한다. 정적 정의·런타임 상태·저장 상태·표현 상태의 owner를 구분하고, 상위 Scene 또는 명시적인 연결 지점이 필요한 의존성을 제공하도록 설계한다. 모든 기능을 Autoload 또는 전역 event bus로 만들지 않는다. 이미 승인된 구조가 같은 경계를 충족하면 그 구조를 유지한다.

### 변경·인계·검증

계약·코드·영향 consumer·테스트를 같은 승인 변경 단위로 갱신한다. 호환성 파괴 여부와 영향 consumer를 먼저 확인한다. 저장 Schema에 영향이 있으면 마이그레이션·복구 fixture를 검증한다. 승인된 공개 동작은 보존하고, 의미 변경은 해당 프로젝트의 결정 Gate를 따른다.

Work 준비와 Codex 구현이 분리된 경우 이 단위는 하나의 승인된 기능 범위를 뜻하며, 모든 산출물이 같은 시점에 구현됐다는 뜻은 아니다. Work는 현재 owner·공개 계약·구현 예정 위치·consumer·검증·롤백을 exact repository revision에 연결하고, Codex는 그 revision과 현재 drift를 fresh-read하여 실제 구현·테스트 상태를 반환한다. 준비 문서만으로 구현 완료를 주장하지 않는다. Base Python·운영 계약의 GPT 실행 책임은 기존 Work Mode 라우팅대로 유지한다.

문서 검사 PASS는 실제 모듈 동작·runtime·UX·사용자 승인 PASS가 아니다. 실행하지 않은 검증은 NOT_RUN으로 남긴다. 실제 기능 변경에서는 적용되는 단위·공개 계약·consumer 통합 검사를 실행하고, 엔진 연결은 해당 Godot 런타임 증거로 검증한다. 화면·시각 상태가 바뀌는 경우 실제 인게임 캡처를 화면/상태·consumer·exact revision·검증 결과에 연결한다. 사람의 체감·최종 승인과 출시 검증은 별도 Gate로 유지한다.

### 구조 예시와 재사용 경계

아래는 구조 설명 예시이며 프로젝트의 새 규칙·경로·구현 사실이 아니다.

```text
피해 계산: 공격 정보 + 대상 상태 snapshot → DamageResult
전투 실행: DamageResult를 받아 자신이 소유하는 체력·상태에 적용
HUD: 공개된 표시 정보·signal을 받아 화면 갱신
```

계산 규칙 변경은 계산 계약·구현·fixture와 영향 consumer를 함께 확인한다. 표시 방식만 바꾸는 경우 계산 규칙까지 복제하거나 변경하지 않는다. 공개 결과 형식이 바뀌면 전투 실행과 HUD의 사용 계약을 다시 검사한다.

프로젝트 고유 규칙·수치·경로는 프로젝트에 남긴다. 공용화는 기존 reuse handoff와 `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`의 검증·승격 경계를 따른다. 기능 계약 작성은 Base 공용 구현·프로젝트 채택 완료를 뜻하지 않는다. 새 재사용 증거가 없으면 기존 `NO_NEW_REUSE_LEARNING`으로 종료하고 등록 건수를 늘리지 않는다.

## 3. 분해 원칙

- 하나의 단계는 하나의 주 결과와 하나의 완료 판정을 가진다.
- 서로 다른 승인 경계·도구·실패 복구가 있으면 분리한다.
- 같은 파일을 여러 단계가 동시에 수정해야 하면 순차화하거나 경계를 재설계한다.
- 구현과 대규모 리팩터링, 원본 변경과 발행, 자동 검증과 사용자 체감 검수는 필요에 따라 분리한다.
- 단계가 너무 커 독립 검증이 불가능하면 더 분해한다.
- 단계가 너무 작아 독립 가치·검증·인수인계가 없으면 합친다.

Scrum Guide는 선택된 작업을 더 작고 정밀한 작업 항목으로 분해하며, 실제 작업자가 수행 방법을 결정하도록 설명한다. Base는 이를 고정 시간 추정 규칙으로 강제하지 않고 **작고 투명하며 검증 가능한 결과**라는 원칙으로 사용한다.

## 4. 의존성 지도

각 관계를 명시적으로 구분한다.

- `BLOCKS`: 완료 전 다음 작업을 시작할 수 없다.
- `INFORMS`: 결과가 다음 결정의 입력이지만 병렬 탐색은 가능하다.
- `USES_OUTPUT`: 생성 파일·Schema·자산·API를 소비한다.
- `SHARES_RESOURCE`: 같은 사람·파일·환경 때문에 충돌할 수 있다.
- `VALIDATES`: 다른 작업 결과를 독립 검증한다.
- `OPTIONAL_FOLLOWUP`: 핵심 완료를 막지 않는 후속이다.

GitHub Issues의 sub-issue와 dependency는 큰 목표를 작은 작업으로 나누고 blocked-by·blocking 관계를 표시하는 데 사용할 수 있다. Milestone은 여러 Issue·PR의 진행을 한 게이트로 묶는 데 사용한다.

## 5. 실행 순서

기본 정렬 기준:

```text
보안·권한·환경 선행 조건
→ 정본·인터페이스·Schema 계약
→ 가장 위험한 가설·기술 불확실성
→ 핵심 사용자·플레이어 경로
→ 데이터·자산·인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 사용자 체감 검수·통합·인수인계
```

다음 기준을 함께 사용한다.

1. `dependency`: 다른 작업을 여는 선행 작업인가?
2. `risk`: 실패했을 때 전체 방향을 바꾸는가?
3. `value`: 가장 빨리 사용자·플레이어 가치를 증명하는가?
4. `reversibility`: 되돌리기 어려운 결정을 너무 일찍 고정하는가?
5. `feedback speed`: 짧은 주기로 실제 결과를 볼 수 있는가?
6. `resource conflict`: 같은 파일·사람·환경을 동시에 요구하는가?

## 6. 병렬화

병렬 작업은 다음을 모두 만족할 때만 허용한다.

- 입력과 책임 원본이 고정됐다.
- 출력 경계와 통합 지점이 명확하다.
- 같은 파일·Schema·자산을 경쟁적으로 수정하지 않는다.
- 각각 독립적으로 검증할 수 있다.
- 한 작업 실패가 다른 작업의 대규모 재작업을 만들지 않는다.

병렬화가 가능한 예:

- 확정된 데이터 계약을 기준으로 코드와 문서 fixture 작성
- 독립된 아트 자산 제작과 테스트 harness 구축
- 대표 정상 경로와 별도 실패·경계 테스트 작성

## 7. 게이트와 재계획

각 묶음 끝에 다음을 둔다.

```yaml
gate:
entry_conditions:
exit_evidence:
if_passed:
if_failed:
if_unverified:
replan_trigger:
```

새 사실·실패·범위 변경이 생기면 이후 단계를 무조건 유지하지 않는다. Sprint Backlog처럼 계획은 목표를 향해 적응 가능해야 하며, 완료 기준과 보호 범위는 추적 가능하게 유지한다.

## 7.1 Approval Bundle

같은 플레이어 경험·시스템·정본·후속 구현에 영향을 주는 결정을 분야별 `Approval Bundle`로 묶는다. 각 Bundle은 현재 Decision, 누락·충돌 판정, Evidence ID, GPT 권장안, 사용자 승인, 영향받는 정본·소비처·Sheet tab, 검증 Gate를 가진다. 기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분리한다.

승인 묶음의 기본 분야 순서는 `00 기반 → 10 제품 방향 → 20 코어 경험·데모 목표 → 30 데모 범위·품질·제작 기반 → 40 시스템·성장·경제 → 50 메인 콘텐츠 → 51 미니게임 → 52 글쓰기·서사 → 60 UX·UI·접근성 → 70 아트·오디오·에셋 → 80 데모 Vertical Slice·플레이테스트 → 90 본제작·출시 → 98 Base 후보 → 99 회고`다. 프로젝트에 없는 분야는 건너뛴다.

## 8. 출력 형식

```text
목표·완료 기준
→ 단계 목록
→ 의존성 그래프
→ 병렬 작업 묶음
→ 게이트·검증
→ 위험·롤백
→ 다음 단계 진입 조건
```

가설 검증이 포함되면 `hypothesis → minimum_test_unit → observation_method → success/failure_threshold → evidence_decision`을 함께 보고한다. 회고에서는 재사용 조건이 반복 증거를 갖춘 공용 판단인지, 프로젝트 고유 수치·세계관·경로·자산인지 구분해 `BASE_CANDIDATE / PROJECT_ONLY / NO_PROMOTION`으로 판정한다.

## 9. 실패 조건

- 동사만 있는 체크리스트를 만든다.
- 요구 확정 전에 세부 구현 순서를 고정한다.
- 파일·데이터·승인·환경 의존성을 기록하지 않는다.
- 위험한 가설을 뒤로 미루고 쉬운 장식 작업부터 한다.
- 모든 작업을 병렬화해 같은 파일과 정본을 충돌시킨다.
- 테스트·문서·발행을 마지막 한 단계에 몰아넣는다.
- 일정 숫자를 근거 없이 발명한다.
- 선행 단계 실패 후에도 이후 계획을 그대로 실행한다.
- 측정 전 가설을 성공으로 기록하거나, 결과와 무관하게 원안을 유지한다.
- 요소별 결과는 통과했지만 `integration_interface`와 통합 E2E를 검증하지 않는다.

## 공식 참고 자료

- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- GitHub Docs — About issues, sub-issues and dependencies: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues
- GitHub Docs — Planning and tracking work: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project
- GitHub Docs — Milestones: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
