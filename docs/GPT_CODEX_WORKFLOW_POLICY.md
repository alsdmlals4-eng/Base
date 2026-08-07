# GPT–Codex 역할·구현 인계 정책

이 문서는 Base를 사용하는 게임 프로젝트에서 GPT와 Codex의 책임, 사용자 요청 기반 인계, 선택적 Plan preflight, Godot 구현 패키지, GitHub 게시와 병합 자동화 경계를 정의하는 공용 정본이다.

## 1. 기본 원칙

```text
GPT 평상시 작업
→ 기획·조사·설계·구현 보조·Godot POC/사전 제작 누적
→ USER_REQUESTED_CODEX_HANDOFF
→ GPT가 현재 의도·실제 상태·보호 범위·Acceptance Criteria를 실행 명세로 압축
→ Codex가 실제 GitHub 저장소·프로젝트 파일·Godot 상태를 직접 재조사
→ 필요할 때만 CODEX_PREFLIGHT_OPTIONAL 읽기 전용 Plan
→ Codex Build가 지정 Branch에서 구현·테스트·Commit·Push
→ GPT가 diff·테스트·기획 일치를 적대적으로 검수
→ 필수 게이트 통과 시 담당 에이전트가 허용된 방식으로 즉시 병합
```

이 기본 흐름의 상태 이름은 `ON_DEMAND_CODEX_HANDOFF`다. Codex 사용은 모든 작업의 의무 단계가 아니라 사용자가 “Codex로 넘기자”, “Codex 작업 명세 만들어줘”, “Codex에서 점검·개선하자”처럼 전환을 요청한 시점의 집중 구현·통합·검증 단계다.

`GPT_GODOT_PREPRODUCTION_ALLOWED`: GPT는 기획만 담당하는 문서 전용 역할로 제한되지 않는다. 현재 도구와 승인 범위 안에서 Scene·Node·Resource/Data 구조 설계, GDScript 초안·구현 보조, HiGodot 기반 국소 구현, POC와 직접 플레이를 통한 재설계까지 진행할 수 있다. 다만 실제로 실행하지 않은 Godot 런타임·렌더·빌드·테스트를 완료로 보고하지 않는다.

Codex는 GPT의 하위 단순 실행기가 아니다. 인계 명세는 의도와 예상 상태를 전달하지만 **실제 구현 사실의 source of truth는 현재 GitHub 저장소, 프로젝트 파일, Godot 프로젝트 상태와 실행 증거**다. 명세와 실제가 충돌하면 Codex는 임의로 덮어쓰지 않고 원인·영향·가장 안전한 개선안을 보고한다.

기본 병합 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다. 별도 사용자 병합 승인은 필요하지 않는다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 사용자의 **명시적 승인이 완료된 항목**은 그 승인 범위의 구현·검증·PR에 병합 권한도 함께 부여된 것으로 간주한다. 이후 동일 범위에 대해 추가 확인·재승인·병합 승인 요청 없이 exact HEAD, Required Check, unresolved thread, 차단 상태를 확인한 뒤 즉시 병합한다. 단, 새 `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, P0/P1, 범위 확대 또는 승인 이후 생긴 새로운 사용자 결정은 기존 승인으로 덮지 않는다.

## 2. GPT 책임

GPT는 평상시 작업과 Codex 인계 준비를 담당한다.

- 현재 대화·저장소·책임 원본·Issue·Branch·PR 감사
- Grill Me 의사결정 인터뷰와 결정 원장
- WHY / HOW / WHAT, 프로젝트 코어, Core Loop, MVP, PoC, Vertical Slice
- 벤치마킹, 시장·플레이어 근거, SWOT·VRIO
- 시스템 규칙, 데이터 계약, UI·UX 흐름, 콘텐츠 제작 문법
- Scene·Node·Resource/Data·Signal·상태 구조 설계와 GDScript 초안·구현 보조
- 승인 범위 안의 Godot POC·사전 제작과 직접 실행 가능한 경우의 재설계
- `AGENTS.md`, Skill, Registry, Documentation Map, Schema, Template
- HTML·Python 기반 기획·검증·발행 도구
- GitHub Actions, 정적 검사, PDF·Manifest
- 기획 Branch·Issue·PR와 필요 시 마스터 구현계획
- `USER_REQUESTED_CODEX_HANDOFF` 시 Codex 실행 명세 작성
- 선택적 Codex Plan 결과 검수와 구현 계약 갱신
- Codex 구현 결과의 기획 일치·회귀·증거 검수
- 자동 병합 적격성 판정과 Repository 설정 검증

Codex 실행 명세에는 최소한 다음을 포함한다.

```yaml
handoff_mode: ON_DEMAND_CODEX_HANDOFF
trigger: USER_REQUESTED_CODEX_HANDOFF
intent_and_current_behavior:
actual_state_verification_required: true
repositories_and_paths_to_inspect: []
godot_scenes_scripts_resources_to_inspect: []
known_problems_and_improvement_goals: []
protected_behavior_and_data_contracts: []
priority_order: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
performance_size_structure_checks: []
forbidden_or_high_risk_changes: []
completion_report_required:
  - changed_files_and_reasons
  - tests_run_failed_not_run
  - remaining_risks
```

## 3. Codex Plan 책임 — 선택적 preflight

`CODEX_PREFLIGHT_OPTIONAL`: Codex Plan은 모든 인계의 의무 단계가 아니다. 다음처럼 실제 구현 전 별도 재검수가 비용 대비 가치가 큰 경우에만 사용한다.

- 저장·Schema·마이그레이션·플랫폼 설정처럼 되돌리기 어려운 고위험 변경
- GPT 명세와 실제 저장소가 크게 어긋날 가능성이 높음
- 여러 패키지·Scene·공용 Resource가 얽혀 경쟁 수정 위험이 큼
- 구현 전에 기술 대안 비교나 별도 `CHANGE_PROPOSAL` 분리가 필요함
- 사용자가 명시적으로 Codex Plan 검토를 요청함

낮은 위험의 명확한 구현 패키지는 실행 명세가 충분하고 실제 저장소 선조사가 가능하면 Codex Build에서 바로 조사→구현으로 진행할 수 있다.

Codex Plan을 사용하는 경우에는 읽기 전용이다.

### 수행

- 최신 `main`, 지정 패키지 Branch, 실제 Godot 파일 재조사
- 예상 파일과 실제 파일 대조
- 선행 패키지 결과와 의존성 확인
- 기술 위험, 데이터·저장 영향, 테스트와 롤백 분석
- Red → Green → Refactor 작업 단위 제안
- 더 나은 Godot 구조·성능·안정성·테스트 개선안 제안
- `CHANGE_PROPOSAL`과 `USER_DECISION_REQUIRED` 분리

### 금지

- 파일 생성·수정·삭제·이동
- Commit·Push·PR·Issue 변경
- 마스터 구현계획 직접 덮어쓰기
- 프로젝트 코어·MVP·플레이 규칙의 암묵 변경
- 존재하지 않는 파일 경로·Godot API·테스트 명령 추측

### 종료 상태

- `PLAN_REVIEW_COMPLETE`
- `PLAN_REVIEW_WITH_TECHNICAL_IMPROVEMENTS`
- `CHANGE_PROPOSAL`
- `USER_DECISION_REQUIRED`
- `BLOCKED`
- `UNVERIFIED`

## 4. Codex Build 책임

Codex Build는 지정된 구현 범위의 실제 저장소·프로젝트·Godot 상태를 먼저 조사한 뒤 구현한다. 별도 Codex Plan을 생략했더라도 이 runtime-truth 조사 의무는 생략되지 않는다.

### 허용 파일

- GDScript
- Scene·Resource·Autoload
- Godot 프로젝트 설정
- 런타임 게임 데이터의 최종 연결
- 저장·불러오기와 마이그레이션 구현
- Godot headless·런타임 테스트
- 셰이더·Godot 플러그인·빌드 설정

### 기본 금지 파일

- 기획 책임 원본
- Base Skill·Registry·Documentation Map
- 비-Godot Schema·Template·CI 정책
- Issue·PR 설명·Active Context
- GPT가 관리하는 마스터·패키지 계약 문서

구현에 필수인 비-Godot 파일 변경이 발견되면 직접 수정하지 않고 GPT에 반환한다.

## 5. 영향도 기반 이중 변경 권한

### Codex 자동 반영 가능

다음은 플레이어 결과와 승인된 데이터 계약을 유지하는 기술 변경이다.

- 동작 보존 리팩터링
- 성능·메모리·안정성 개선
- 더 적합한 Godot Node·Scene·Resource·Signal 구조
- 테스트 가능성 개선
- 중복 제거·내부 파일 분리
- 오류 처리·방어 코드
- 승인 결과를 더 정확히 구현하는 내부 세부 변경

기술 변경은 구현 보고에 이유·영향·검증을 기록한다. 선택적 Codex Plan을 사용했다면 Plan에도 기록한다.

### `CHANGE_PROPOSAL` 필수

- 프로젝트 코어·Core Loop 변경
- 플레이어 규칙·보상·실패 결과 변경
- 신규 시스템·기능 추가
- MVP 포함·제외 범위 변경
- 주요 UI·UX 흐름 변경
- 콘텐츠·내러티브 의미 변경
- 승인 기능 제거
- 저장 호환성을 깨는 Schema 변경
- 제작 범위·일정·의존성의 중대한 변경

`CHANGE_PROPOSAL`은 구현과 분리한다. 승인 계약을 갱신하기 전에는 관련 구현을 시작하지 않는다.

## 6. 구현 패키지

대규모 작업은 하나의 통합 설계 명세와 마스터 구현계획을 유지하고 검증 가능한 결과 단위로 분해한다. 소규모·국소 작업에는 불필요한 패키지 문서를 강제하지 않는다.

기본 예시:

```text
PKG-00 기반·테스트 하네스
PKG-01 핵심 상태·데이터
PKG-02 핵심 플레이 행동
PKG-03 성공·실패·복구
PKG-04 UI·피드백
PKG-05 저장·불러오기
PKG-06 콘텐츠 연결
PKG-07 Vertical Slice 통합
PKG-08 회귀·성능·접근성·마감
```

패키지는 파일 수가 아니라 다음 조건으로 나눈다.

- 독립된 플레이 가능 결과 또는 검증 가능한 기반
- 명확한 입력·출력·선행 조건
- 독립 테스트·검수·롤백 가능
- 같은 파일·Schema·Scene의 경쟁 수정 최소화

## 7. 마스터 구현계획과 선택적 패키지 Plan

### 마스터 구현계획

L2 이상 또는 다중 패키지 작업에서 GPT가 관리한다.

- 전체 구현 목표와 플레이어 가치
- 승인된 프로젝트 코어와 불변 조건
- 패키지 순서와 의존성
- 공통 수정 금지 범위
- 데이터·저장·ID·Schema 보호 조건
- 공통 테스트 전략
- Vertical Slice 완료 기준
- 승인 게이트·롤백·기획 반환 조건

### 패키지 Plan

`CODEX_PREFLIGHT_OPTIONAL`이 선택된 경우 Codex가 최신 저장소를 읽기 전용 재검수하고 GPT가 문서에 반영한다.

- 기준 Branch·Commit
- 현재 구현 상태
- 예상·실제 파일 영향도
- Red → Green → Refactor
- 회귀 테스트와 실패 반례
- 기술 개선과 `CHANGE_PROPOSAL`
- 독립 Commit 계획
- 롤백·중단 조건

패키지 Plan은 마스터 구현계획을 직접 덮어쓰지 않는다.

## 8. 승인 게이트

패키지 구현 후 GPT가 다음 중 하나로 판정한다.

- `PACKAGE_APPROVED`: 승인 계약과 일치하고 필수 검증 통과
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`: 기술 개선만 포함하고 플레이어 계약 유지
- `USER_REVIEW_REQUIRED`: 조작감·난이도·보상·UI·UX·아트·연출·사운드·Vertical Slice 체감 판단 필요
- `CHANGE_PROPOSAL`: 승인 기획 또는 호환성 변경 필요
- `REVISE`: 구현·계약·테스트 불일치
- `BLOCKED`: 권한·환경·선행 조건 차단
- `UNVERIFIED`: 필수 증거 미확보

GPT는 기술 구현과 승인 명세가 일치하고 자동·Godot 검증이 통과한 경우 다음 패키지를 준비할 수 있다. 사용자 체감·취향·코어·범위 판단은 사용자에게 반환한다.

## 9. 병합 정책

### `AUTO_MERGE_AFTER_REQUIRED_CHECKS`

기본 정책이다.

`AGENT_MERGE_REQUIRED`: 자동 병합 설정이 있으면 이를 활성화하고, 없으면 저장소가 허용한 직접 병합을 실행한다. 모든 게이트를 통과한 PR을 별도 사용자 승인 대기로 남기지 않는다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 명시적으로 승인된 항목은 동일 승인 범위의 구현 PR이 검증을 통과하면 추가 확인·재승인·병합 승인 요청 없이 병합한다.

자동 병합 허용 조건:

- PR이 Draft가 아님
- 검수 기준 HEAD SHA와 현재 HEAD SHA가 일치
- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- 저장소 Required Check 성공
- unresolved review thread 없음
- 허용된 병합 방식과 active Ruleset 또는 동등한 branch protection 확인

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

다음 상태는 자동 병합을 차단한다.

- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

## 10. GitHub 구조

L2 이상 다중 패키지 작업의 기본 구조:

```text
상위 구현 Issue
├─ 패키지 0 Branch / PR
├─ 패키지 1 Branch / PR
├─ 패키지 2 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

- 패키지마다 독립 Branch와 PR을 사용한다.
- 기본은 순차 진행이다.
- GPT가 Issue·Branch 이름·PR 계약과 체크리스트를 관리한다.
- Codex는 지정 Branch를 생성·변경하지 않는다.
- Codex는 지정 Branch에서 Godot 파일만 Stage·Commit·Push할 수 있다.
- `main` 직접 Push, force push, amend, PR 생성·병합은 금지한다.
- 사용자의 기존 변경과 무관한 파일을 포함하지 않는다.
- GPT가 자동 병합 적격성을 판정하고, `AGENT_MERGE_REQUIRED`에 따라 GitHub auto-merge 또는 허용된 직접 병합을 실행한다.

## 11. Codex Push 전후 가드레일

### Push 전

- `git status` 확인
- 기준 Branch·Commit 확인
- 변경 파일 목록 제출
- 비-Godot 파일 혼입 검사
- 승인 범위 밖 변경 검사
- Godot 정적·headless·런타임 테스트
- 실패·미실행 검사 명시

### Push 후

- Commit SHA 제출
- 원격 HEAD 일치 확인
- 실행 명령·결과 제출
- 기술 변경 목록 제출
- `CHANGE_PROPOSAL`·미검증·남은 위험 제출

## 12. 작업 중단과 반환

다음은 구현을 중단하고 GPT 기획 단계로 반환한다.

- 실제 저장소가 승인 계약의 핵심 전제와 다름
- 데이터·저장 호환성을 유지할 수 없음
- 프로젝트 코어 또는 플레이어 규칙을 변경해야 함
- 필수 자산·엔진 버전·플러그인·권한이 없음
- 패키지 독립 검증이 불가능함
- 사용자 기존 변경과 충돌하며 안전한 보존 경로가 없음

## 13. 완료 조건

- GPT 평상시 단계에서 필요한 기획·설계·POC가 현재 범위에 맞게 진행됐다.
- `USER_REQUESTED_CODEX_HANDOFF`이면 실행 명세가 현재 의도·보호 범위·Acceptance Criteria를 전달한다.
- Codex가 실제 저장소·프로젝트·Godot 상태를 직접 확인했다.
- `CODEX_PREFLIGHT_OPTIONAL`을 사용한 경우 Plan 보고서가 최신 실제 저장소를 근거로 한다.
- 구현이 지정 Branch와 승인 범위에 한정됐다.
- 기술 개선과 기획 변경이 구분됐다.
- 필수 Godot·회귀 검증 결과가 있다.
- GPT가 승인 명세와 diff를 대조했다.
- 병합 정책과 Required Check가 선언됐다.
- 자동 병합이면 Repository 설정·HEAD SHA·차단 상태를 확인했다.
- 사용자 결정이 필요한 상태에서는 자동 병합하지 않았다.
