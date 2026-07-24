---
name: reviewing-and-validating-project-changes
description: Use when code, data, documents, assets, configuration, CI workflows, or external AI output must be checked against an approved work contract and verified with repository evidence, reference freshness, cost-aware CI execution, accessibility barriers, performance budgets, runtime behavior, and regression evidence before integration.
---

# Reviewing and Validating Project Changes

## Core principle

변경 주체가 사람이든 AI든 설명보다 실제 diff, 책임 원본, 실행 결과를 우선한다. 승인된 작업 계약과 관찰 가능한 증거가 일치하고, 변경된 정본이 모든 활성 소비자에 전파되며, 적용되는 CI·접근성·성능 기준을 충족하기 전에는 완료로 판정하지 않는다.

## Modes

- `contract-check`: 승인 목표, 범위, 보호 대상과 실제 변경을 대조한다.
- `external-source-review`: 외부 AI·병렬 작업자의 초안과 주장을 독립 검수한다.
- `ci-cost-optimization`: 변경 위험에 따라 GitHub Actions 실행 계층을 분리하고 중복 실행·불필요한 matrix·고비용 설치를 줄이면서 Required Check 증거를 보존한다.
- `reference-freshness`: 변경된 정본·경로·ID·Schema가 활성 참조·템플릿·테스트·파생본에 전파됐는지 감사한다.
- `static-validation`: 코드·데이터·문서·자산·참조·Schema를 정적 검사한다.
- `runtime-validation`: 실행·빌드·렌더·저장·오류 경로를 실제 환경에서 확인한다.
- `accessibility-review`: 핵심 정보·입력·UI·시간·난이도·모션에서 플레이 장벽과 대체 경로를 검수한다.
- `performance-profile`: 목표 플랫폼의 frame time·CPU·GPU·메모리·네트워크·로딩 예산을 재현 가능한 capture로 비교한다.
- `regression`: 대표 정상·경계·반례·기존 기능 회귀를 확인한다.
- `evidence-report`: 통과·실패·미실행·위험·롤백을 증거와 함께 보고한다.

`ci-cost-optimization`은 CI 사용량 증가, 문서 변경의 전체 matrix 중복 실행, workflow·runner·cache·artifact·Required Check 변경, GitHub Actions 사용 불가 상태가 요청이나 diff에 포함될 때 사용한다. 비용 절감을 이유로 필요한 검증을 삭제하지 않고 PR·main·nightly·release의 실행 시점과 위험 계층을 재배치한다.

`reference-freshness`는 파일·경로·Skill ID·문서 ID·Schema·정책·생성기·공개 인터페이스가 추가·이동·통합·삭제·교체되었거나, 영향 파일 누락 가능성이 있는 모든 변경에서 실행한다. 전문 절차는 `auditing-canonical-reference-freshness`를 호출한다.

`accessibility-review`와 `performance-profile`은 모든 L0 변경에 강제하지 않는다. 핵심 플레이·입력·UI·정보 전달·시간 제한·난이도·렌더링·콘텐츠 부하·네트워크·플랫폼 빌드에 영향이 있을 때 적용한다.

## Required inputs

```yaml
approved_work_contract:
baseline_branch_and_commit:
changed_files_or_diff:
current_responsibility_sources:
canonical_sources_and_consumers:
known_renames_aliases_and_replacements:
allowed_and_protected_scope:
acceptance_criteria:
validation_commands_and_tools:
ci_scope:
  workflow_files:
  triggers_and_path_filters:
  jobs_dependencies_and_matrices:
  required_checks_and_branch_protection:
  supported_os_python_and_engine_versions:
  high_cost_dependencies_caches_and_artifacts:
  actions_availability:
  current_or_estimated_duplicate_runs:
runtime_or_capture_targets:
target_platforms_devices_and_hardware:
accessibility_scope:
  target_player_contexts:
  critical_information_channels:
  input_and_ui_paths:
  text_audio_subtitles_motion_time_limits:
performance_budget:
  frame_time_ms:
  cpu_gpu_memory_network:
  loading_streaming:
  representative_and_worst_case_scenes:
  baseline_capture:
rollback_path:
change_producer:
```

## Review order

```text
작업 계약·범위
→ 현행 책임 원본
→ 실제 diff·참조 영향
→ 적용 시 CI 실행·비용 계층 감사
→ 필요 시 reference-freshness
→ 데이터·저장·호환성
→ 정적 검사
→ 런타임·렌더·빌드
→ 필요 시 접근성 장벽 검수
→ 필요 시 목표 플랫폼 성능 프로파일
→ 대표·경계·반례·회귀
→ 증거 보고·최소 수정·롤백
```

## Process

### 1. Contract check

1. 요청한 문제·산출물·완료 기준을 재진술한다.
2. 변경 파일을 `필수 / 허용 / 범위 밖`으로 분류한다.
3. 사용자 기존 변경과 승인되지 않은 구조 변경을 찾는다.
4. 삭제·이동·이름 변경은 모든 참조와 대체 경로를 확인한다.
5. CI·접근성·성능·플랫폼 기준이 적용되는 변경인지 판정한다.

### 2. Source review

1. 새 책임 원본을 만들기 전에 같은 책임의 현행 원본이 있는지 찾는다.
2. 구현 사실, 외부 근거, 추정, 제안을 분리한다.
3. 외부 설명보다 실제 파일·diff·명령 결과를 우선한다.
4. 확인할 수 없는 경로·명령·함수·필드를 승인하지 않는다.

### 2A. CI cost optimization

`docs/CI_EXECUTION_COST_POLICY.md`를 정본으로 사용한다.

1. 모든 workflow의 event, `paths`, concurrency, Job 의존성, OS·Python·엔진 matrix, 설치 단계, cache, artifact, Required Check를 인벤토리화한다.
2. 각 Job이 제공하는 검증 증거와 실패 시 막아야 하는 통합 위험을 연결한다. 목적을 설명할 수 없는 중복 Job·matrix 축은 후보로 분리한다.
3. 변경을 `DOCS_ONLY / CANONICAL_CONTRACT / CODE_OR_ENGINE / CI_TOOLCHAIN_HIGH_RISK / FULL_MATRIX`로 분류하고, 알 수 없는 파일은 더 높은 계층으로 승격한다.
4. 기본 실행을 다음처럼 설계한다.

```text
문서 전용 PR
→ Ubuntu·기준 Python 1개·문서 validator

정본·Skill·Registry 변경 PR
→ Ubuntu·기준 Python 1개·전체 계약·reference freshness

코드·도구·Godot 변경 PR
→ Ubuntu 전체 계약·관련 테스트·적용 시 Godot

main·nightly·release·명시적 full
→ 지원 OS × 선언된 Python 전체 matrix × 전체 계약·적용 시 Godot
```

5. feature branch `push`와 `pull_request`가 같은 SHA의 전체 검증을 중복 실행하지 않게 하고, PR workflow에는 기본적으로 다음 concurrency 계약을 둔다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

6. 조건부 Job을 Branch protection에 직접 여러 개 요구하기보다, 선택된 Job의 성공·실패·취소·누락을 판정하는 안정된 `ci-gate`를 둔다.
7. LibreOffice·Poppler·브라우저·Node·Godot·Windows runner처럼 고비용인 의존성과 플랫폼은 실제 필요 Job에서만 설치·실행한다.
8. GitHub Actions를 사용할 수 없으면 로컬·정적 검사만 실제 결과로 기록하고 다음 상태를 사용한다.

```text
BLOCKED_BY_GITHUB_ACTIONS
판정: UNVERIFIED
```

9. 보류 보고에는 workflow, event 또는 dispatch 입력, 실행할 Job, 기대 Required Check, 확인할 log·artifact, 재개 조건, 미검증 위험을 남긴다.
10. 사용자가 Actions 사용 가능 상태를 알리면 최신 branch·SHA·workflow diff를 다시 확인하고 아직 필요한 보류 Job만 실행한다.

### 3. Reference freshness

다음 중 하나라도 해당하면 `auditing-canonical-reference-freshness`를 호출한다.

- 파일·폴더·Skill ID·문서 ID·Schema·명령·공개 인터페이스를 변경했다.
- Registry·Documentation Map·START_HERE·AGENTS·운영 모델·템플릿을 변경했다.
- 통합·삭제·마이그레이션·발행 정책·생성기 변경이 있다.
- 하나의 정본 변경이 여러 소비자·테스트·Workflow·파생본에 영향을 줄 수 있다.

검사 결과에서 활성 파일의 오래된 참조, untouched 소비자, 허용된 Legacy·Change Log·과거 case, 정책·상태 drift, PDF·Manifest·해시 불일치를 구분한다.

Base 자동 검사:

```text
python tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base <base-sha> --head <head-sha>
```

### 4. Static validation

- 코드: 호출 관계, 타입, 오류 처리, 공개 인터페이스.
- 데이터: ID, Schema, 기본값, 마이그레이션, 저장 호환성.
- 문서: 책임 중복, 경로, 상태, 명령, 구현과의 일치.
- 자산: 참조 경로, import 설정, 형식, 승인 상태.
- 구성: 플랫폼별 경로, 환경 변수, 잠금 파일, CI와 로컬 차이.
- CI: YAML 구문, 변경 분류 fallback, Job `if`·`needs`, concurrency, stable gate, main·nightly 전체 matrix 경로.

### 5. Runtime validation

- 가능한 경우 사용자가 실제로 겪는 시작점에서 증상을 재현한다.
- 빌드·실행·렌더·저장·불러오기·오류 경로를 확인한다.
- 엔진이 Edit Mode·Play Mode·target player 테스트를 구분하면 각 층을 별도 증거로 남긴다.
- CI 변경은 적용 가능한 경우 PR·`workflow_dispatch`·main 또는 nightly 실제 실행 결과와 Required Check를 확인한다.
- UI 전문 시각 감사가 필요하면 `auditing-and-refining-ui-art`를 별도 호출한다.
- 필요한 실행 환경이 없으면 통과 처리하지 않고 미실행 사유와 확인 방법을 기록한다.

### 6. Accessibility review

Microsoft Xbox Accessibility Guidelines처럼 접근성을 설계·개발·테스트 가드레일로 사용하되 법적 준수 인증으로 표현하지 않는다.

다음을 핵심 플레이 경로와 설정 경로 양쪽에서 확인한다.

- 텍스트 크기·간격·배경·실제 플레이 거리와 대비.
- 색만이 아닌 아이콘·텍스트·음향·진동 등 핵심 정보의 다중 채널.
- 자막·화자·대사와 중요한 효과음 구분, 개별 오디오 제어.
- 키·버튼 재지정, 홀드·연타·복합 입력 대안, 장치 전환.
- 난이도·도움 옵션과 실패 후 학습·복구.
- 일관된 UI 탐색·포커스·탈출·오류·파괴 행동 확인.
- 읽기·판단·입력 시간과 일시정지·연장·비활성 대안.
- 화면 흔들림·깜빡임·과도한 모션의 감소·비활성 옵션.

각 장벽은 `BLOCKING / MAJOR / MODERATE / MINOR`로 판정하고 대상 플레이어 맥락, 트리거, 막히는 행동, 대안, 검증 시나리오를 기록한다. 옵션이 존재해도 실제 게임에 적용되지 않으면 통과가 아니다.

### 7. Performance profile

목표 플랫폼·빌드·대표 장면·최악 장면과 예산을 먼저 고정한다.

```text
baseline 반복 측정
→ frame time·CPU·GPU·메모리·네트워크·로딩 병목 분리
→ 최소 수정
→ 같은 조건 재측정
→ 품질·기능·접근성 회귀 확인
```

- 평균 FPS만 보지 않고 frame time(ms), 일관성, hitch·spike와 하위 구간을 확인한다.
- 에디터보다 실제 target build·hardware에 가까운 환경을 우선한다.
- profiler·debugger 오버헤드와 측정 반복의 변동을 기록한다.
- 재현 가능한 장면·입력·빌드 설정을 고정한다.
- 병목을 측정하기 전에 추측으로 최적화하지 않는다.
- 변경 전후 capture는 같은 조건에서 비교한다.
- 대표 장면뿐 아니라 최대 콘텐츠·긴 세션·저사양·메모리 누적을 필요에 따라 확인한다.

상세 축은 `references/accessibility-and-performance-validation.md`를 따른다.

### 8. Regression

1. 대표 정상 경로.
2. 최소·최대·빈 값·누락 입력 같은 경계 경로.
3. 원래 실패를 재현하는 반례.
4. 변경과 인접한 기존 기능.
5. 실패 후 복구·롤백 경로.
6. 최신 정본과 이전 참조가 다시 공존하지 않는지 확인한다.
7. CI 최적화가 필요한 검증을 누락하거나 Required Check를 영구 대기 상태로 만들지 않는지 확인한다.
8. 접근성·성능 개선이 핵심 규칙·가독성·아트·입력 약속을 훼손하지 않는지 확인한다.

### 9. Decision

- `ACCEPT`: 계약과 적용 검증을 충족하고 참조 최신성 누락이 없다.
- `ACCEPT_WITH_FOLLOWUP`: 핵심 기준은 통과했지만 비차단 후속 작업이 있다.
- `REVISE`: 수정 뒤 같은 검증을 다시 실행해야 한다.
- `REJECT`: 범위·사실·호환성·정본·핵심 품질 계약 위반으로 폐기한다.
- `UNVERIFIED`: 필요한 환경·입력이 없거나 GitHub Actions가 사용 불가해 완료 판정할 수 없다.

## Output contract

```md
# 프로젝트 변경 검증
## 판정
## 승인된 목표·범위와 실제 diff
## 확인한 책임 원본·파일
## CI 변경 분류·실행 계층·중복 제거
## Actions 사용 가능 상태·실행 결과·보류 Job·재개 조건
## 정본·참조 최신성·변경 전파
## 정적 검사
## 런타임·렌더·빌드 검증
## 접근성 장벽·대안·심각도
## 성능 예산·baseline·profile·변경 후 비교
## 대표·경계·반례·회귀 결과
## 외부 산출물 독립 검수
## 실패·미실행·남은 위험
## 필요한 최소 수정
## 롤백·복구
## 증거 경로·명령·캡처
```

## Definition of Done

- 승인된 계약과 실제 변경 범위를 대조했다.
- 변경된 책임과 참조 경로를 확인했다.
- CI 최적화가 적용되면 변경 분류, PR·main·nightly 실행 계층, concurrency, `ci-gate`, Required Check 계약을 확인했다.
- GitHub Actions 사용 불가 시 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`, 보류 Job, 재개 조건과 위험을 남겼다.
- 정본·경로·ID·Schema 변경이 있으면 영향 지도와 reference freshness 결과가 있다.
- 변경됐어야 하지만 untouched인 파일의 갱신 필요 여부를 판정했다.
- 가능한 정적·런타임·회귀 검증을 실제 실행했다.
- 적용되는 경우 핵심 정보·입력·UI·시간·난이도·모션 장벽을 실제 경로에서 확인했다.
- 적용되는 경우 목표 플랫폼·대표·최악 장면에서 성능 예산과 baseline을 같은 조건으로 비교했다.
- 실행하지 못한 검증을 성공으로 표시하지 않았다.
- 판정과 증거, 남은 위험, 롤백을 연결했다.
- 외부 산출물은 독립 검수 없이 정본에 반영하지 않았다.

## Failure conditions

- 실제 파일을 읽지 않고 완료를 주장한다.
- 원래 증상을 재현하지 못한 테스트만으로 수정 완료를 주장한다.
- 사용자 승인 없이 범위 밖 구조 변경·삭제·마이그레이션을 수행한다.
- 테스트 없이 저장 형식·공개 인터페이스를 바꾼다.
- 확인할 수 없는 경로·명령·함수·데이터 필드·실행 결과를 만든다.
- 기존 사용자 변경을 덮어쓴다.
- 새 정본 파일만 확인하고 이전 참조·untouched 소비자·파생본을 검사하지 않는다.
- Git 이력·Change Log·Alias의 역사 참조를 활성 stale reference와 구분하지 않는다.
- 비용 절감을 이유로 검증 Job을 삭제하고 동일한 증거를 다른 계층에서 보존하지 않는다.
- 문서 전용 변경에 전체 OS·Python·Godot matrix를 관성적으로 실행한다.
- 조건부 Job을 Required Check로 묶어 영구 대기 상태를 만들거나 `ci-gate`가 필요한 실패를 숨긴다.
- Actions가 사용 불가한데 workflow 존재만으로 통과를 주장하거나 반복 재실행한다.
- 접근성을 자막·색약 모드 하나로 축소하거나 옵션 존재만 확인한다.
- 접근성 검수를 법적 준수 인증처럼 보고한다.
- 평균 FPS 하나나 에디터의 빈 장면만으로 성능 통과를 주장한다.
- baseline·장면·빌드·하드웨어 조건이 다른 수치를 직접 비교한다.
- 측정 없이 추측으로 최적화하고 기능·가독성·품질 회귀를 생략한다.

## Related skills

- `auditing-canonical-reference-freshness`: 정본 영향 지도, 오래된 참조, content drift, 파생본 최신성과 변경 전파 누락을 전문 감사한다.
- `refactoring-with-contract-preservation`: workflow 중복·구조 복잡성을 기존 검증 계약을 보존하며 줄인다.
- `synchronizing-local-and-github-state`: 기준 branch·SHA·PR·Actions 상태를 대조한다.
- `managing-design-documents`: 등록된 문서 정본과 정책별 발행·Manifest 검증을 담당한다.
- `managing-game-project-operating-system`: 시작 문서·Registry·Skill·자동화·콜드 스타트 전체 연결을 검증한다.
- `auditing-and-refining-ui-art`: 실제 Godot·Web UI 렌더의 전문 시각 감사를 담당한다.
- `analyzing-and-refining-game-concepts`: 접근성·성능 목표가 기획 제약과 플레이어 약속에 미치는 영향을 정의한다.

## Legacy mode mapping

- `reviewing-external-ai-drafts` → `external-source-review`, `static-validation`, `regression`, `evidence-report`

References and templates:

- `docs/CI_EXECUTION_COST_POLICY.md`
- `references/accessibility-and-performance-validation.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md`
- `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md` (legacy-compatible input)
