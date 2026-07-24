# GPT–Codex 역할 분리와 단계별 구현 인계 설계

## 1. 목표

GPT가 저장소 조사, Grill Me 의사결정 인터뷰, 총기획, 벤치마킹, 시스템·데이터·UX 설계, 비-Godot 파일, GitHub 운영, 검증 계약과 구현 인계까지 완료한다. Codex에는 최종적으로 승인된 설계를 Godot에서 구현하는 작업만 전달한다.

## 2. 역할 경계

### GPT 책임

- 저장소·대화·책임 원본 감사
- Grill Me 질문과 결정 원장 관리
- 프로젝트 코어·Core Loop·MVP·PoC·Vertical Slice 확정
- 벤치마킹·시장·플레이어 근거 조사
- 시스템·데이터 계약·UI·UX·콘텐츠 규칙 설계
- Skill·Registry·Documentation Map·Schema·Template·CI·검증 도구
- 기획 Branch·Issue·PR·PDF·Manifest
- 마스터 구현계획과 패키지 구현 계약
- Codex Plan 보고서 검수와 패키지 Plan 갱신
- Codex 구현 diff의 기획 일치·회귀 검수

### Codex Plan 책임

- 최신 `main`과 실제 Godot 구현 상태 재조사
- 파일·의존성·위험·테스트·롤백 재검수
- 더 나은 기술 구현안 제안
- 파일 수정·Commit·Push 없이 읽기 전용 보고서 제출

### Codex Build 책임

- 지정된 패키지 Branch에서 GDScript, Scene, Resource, Autoload, Godot 프로젝트 설정, 런타임 데이터 연결, 저장·마이그레이션, Godot 테스트, 셰이더·플러그인·빌드 설정 구현
- Godot 런타임 파일만 Stage·Commit·지정 Branch Push
- Commit SHA, 원격 HEAD, 실행한 테스트와 미실행 검증 보고

## 3. 변경 권한

### Codex 자동 반영 가능

동일한 플레이어 결과를 유지하는 리팩터링, 성능·메모리·안정성 개선, Godot Node·Scene·Resource·Signal 구조 개선, 테스트 가능성 향상, 중복 제거, 방어 코드와 오류 처리다.

### `CHANGE_PROPOSAL` 필요

프로젝트 코어, Core Loop, 플레이어 규칙·보상·실패 결과, 신규 시스템, MVP 범위, 주요 UI·UX 흐름, 콘텐츠 의미, 승인 기능 제거, 저장 호환성을 깨는 Schema 변경이다.

## 4. 구현 패키지

전체 설계는 하나의 통합 명세와 마스터 구현계획으로 유지한다. 실제 구현은 검증 가능한 결과 단위의 패키지로 순차 진행한다.

```text
상위 구현 Issue
├─ Package 0: 기반·테스트 하네스
├─ Package 1: 핵심 상태·데이터
├─ Package 2: 핵심 플레이 행동
├─ Package 3: 성공·실패·복구
├─ Package 4: UI·피드백
├─ Package 5: 저장·불러오기
├─ Package 6: 콘텐츠 연결
├─ Package 7: Vertical Slice 통합
└─ Package 8: 회귀·성능·접근성·마감
```

프로젝트 특성에 따라 패키지 수와 이름은 조정하되 파일 수가 아니라 플레이 가능 결과 또는 검증 가능한 기반으로 나눈다.

## 5. Branch·PR 구조

- 전체 구현은 상위 Issue 하나에서 추적한다.
- 패키지마다 독립 Branch와 PR을 사용한다.
- 기본은 순차 진행이다.
- 완전히 독립적인 도구·자산 파이프라인만 병렬 허용한다.
- GPT가 Branch·Issue·PR 계약을 준비한다.
- Codex는 지정 Branch를 생성·변경하지 않는다.
- Codex는 `main` 직접 Push, force push, amend, PR 생성·병합을 하지 않는다.
- PR 병합은 사용자 명시적 승인 후 수행한다.

## 6. Plan 구조

### 마스터 구현계획

전체 목표, 불변 프로젝트 코어, 패키지 의존성, 데이터·저장·Schema 보호 조건, 공통 수정 금지, 테스트 전략, Vertical Slice 완료 기준과 승인 게이트를 관리한다.

### 패키지 Plan

각 패키지 시작 전 최신 `main`을 기준으로 실제 경로, 현재 구현 상태, 선행 패키지 결과, Red → Green → Refactor, 테스트, 위험과 롤백을 최신화한다. 마스터 계약 변경은 직접 반영하지 않고 `CHANGE_PROPOSAL`로 반환한다.

## 7. 승인 게이트

- `PACKAGE_APPROVED`: 승인 명세와 일치하고 검증 통과
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`: 기술 개선만 포함하고 플레이 계약 유지
- `USER_REVIEW_REQUIRED`: 조작감·난이도·보상 체감·UI·UX·아트·연출·사운드·Vertical Slice 판단 필요
- `CHANGE_PROPOSAL`: 승인 기획이나 호환성 변경 필요
- `REVISE`: 계약 또는 검증 실패
- `BLOCKED`: 환경·권한·선행 조건 차단
- `UNVERIFIED`: 필요한 증거 미확보

## 8. Grill Me 계약

Grill Me는 독립 Skill을 중복 생성하지 않고 `managing-project-intake-and-work-contract`의 `clarify` Skill Mode에 정식 프로토콜로 통합한다.

- 저장소에서 답할 수 있는 질문은 묻지 않는다.
- 이미 답했거나 최신 결정으로 대체된 질문은 반복하지 않는다.
- 프로젝트 방향을 바꾸는 사용자 결정만 한 번에 하나씩 묻는다.
- 질문마다 중요 이유, 확인된 상태, 선택지, 장단점, GPT 권장안, 확정 영향을 제시한다.
- 사용자의 답을 즉시 결정 원장과 책임 원본에 반영한다.
- 핵심 결정 분기가 해소되면 질문 수를 채우지 않고 종료한다.

## 9. 성공 기준

1. GPT 단계 종료 시 Codex에 남은 작업이 Godot 구현 패키지뿐이다.
2. Codex Plan은 읽기 전용이며 실제 저장소 재검수 증거를 제공한다.
3. 기술 개선과 기획 변경이 구분된다.
4. 패키지마다 독립 Branch·PR·테스트·롤백이 있다.
5. 사용자 결정이 필요한 지점만 작업을 중단한다.
6. Base Skill·문서·Template·CI가 이 구조를 자동 라우팅하고 검증한다.
