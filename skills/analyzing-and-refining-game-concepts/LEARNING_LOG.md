# Analyzing and Refining Game Concepts Learning Log

## 2026-08-05 — PC·Android 동시 목표는 조건부 기획 제약으로 다룬다

### Trigger

조작이 단순하고 턴제·저시간압박인 게임을 Windows PC와 Android 모바일에 처음부터 대응시키고, STOVE·Google Play를 우선 검토한 뒤 Steam으로 확장하려는 반복 프로젝트 요구가 발생했다.

### Evidence reviewed

- Godot의 다중 해상도·stretch 설정과 모바일 가로형 시작점
- Android의 터치 목표, Activity lifecycle, 상태 저장, 실제 기기 성능·메모리·발열 검증
- Steam Direct 비용, Google Play 등록비와 신규 개인 계정 closed test gate
- STOVE Studio의 프로젝트·Game ID·Application Key·PC SDK·출시 절차
- Into the Breach, Slay the Spire, Dicey Dungeons, Balatro의 PC·모바일 적응 및 단계 출시 사례

### Lesson

- 적합한 프로젝트에서는 `공용 게임 코어 하나 + 입력·레이아웃·lifecycle·품질·상점 서비스 어댑터`가 실무적인 기본 구조다.
- 조작 수가 적다는 이유만으로 PC UI를 축소하거나 모바일 UI·중단 복구·실기기 QA를 생략해서는 안 된다.
- 두 플랫폼을 처음부터 실행 가능하게 유지하는 결정과 같은 날 공개하는 결정은 분리한다.
- Steam 비용 하나만으로 Google Play 우선순위를 자동 결정하지 않는다. 신규 개인 계정의 테스터·기간 gate와 팀의 지원 역량이 더 큰 병목일 수 있다.
- 코드 공유율을 목표로 삼지 않고 규칙 정본·저장 Schema·결정론이 하나인지와 플랫폼 경계의 교체 가능성을 검증한다.

### Base change

- 새 광역 Skill을 추가하지 않았다.
- 기존 `analyzing-and-refining-game-concepts`의 `constrain`, `poc-contract`, `production-gate`에서만 조건부 Guide와 Profile을 소비한다.
- 프로젝트는 `DUAL_TARGET_APPROVED`, `DUAL_TARGET_CONDITIONAL`, `SINGLE_TARGET_FIRST`, `BLOCKED_UNVERIFIED` 중 하나로 판정한다.

### Guardrail

이 학습은 모든 프로젝트에 Windows+Android 동시 개발이나 STOVE+Google Play 동시 공개를 강제하지 않는다. 정밀·고속 입력, 모바일에서 손실되는 정보 구조, 성능 위험, 실기기·테스터·QA·지원 역량 부족이 있으면 단일 플랫폼 우선 또는 보류가 맞다.

### Validation state

```yaml
base_contract_test: IMPLEMENTED
existing_skill_companion_test: IMPLEMENTED
actual_project_pilot: NOT_RUN
physical_android_device: DEVICE_NOT_RUN
human_usability: HUMAN_NOT_RUN
store_submission: NOT_RUN
```

프로젝트 Pilot이 반복 성공하기 전에는 이 패턴을 보편적 성공 공식이나 강제 기본값으로 승격하지 않는다.

## 2026-08-19 — 플레이어 가치에서 증거 상한까지 하나의 추적으로 유지한다

### Trigger

P04 독립 최적화에서 컨셉 연구, 11영역 Games User Research coverage, Vertical Slice 판정이 각각 플레이어 가치를 다루지만 한 결정 추적으로 명시 연결되지 않은 상태와, 튜토리얼 mode의 폐기된 Google Sheets 활성 입력 문구가 확인됐다.

### Evidence reviewed

- `GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`의 플레이어 약속과 `PLAYER_EXPERIENCE_EVIDENCE_GATE`
- `analyzing-and-refining-game-concepts`, `governing-game-user-research-coverage`, `designing-vertical-slices`의 실제 책임 경계
- 기존 `identifying-project-core`와 `establishing-project-core`의 existing-project 판정 / new-or-redefined-core 승인 분리
- MDA의 설계·개발·연구 반복 연결
- Games User Research의 research-question-first 방법 선택
- Vertical Slice를 production readiness 판단에 쓰는 실무 자료

### Lesson

`player_promise → meaningful_choice → expected_experience → research_question → observable_signal → evidence_ceiling → slice_acceptance`를 하나의 추적으로 유지하면 기능·화면 완료를 플레이어 가치의 대리 지표로 쓰는 오류를 줄이고, 연구 방법 선택과 Vertical Slice의 다음 결정을 같은 질문에 연결할 수 있다.

### Base change

- 새 Skill을 만들지 않고 기존 P04 5개 Skill의 책임 수를 유지했다.
- `analyzing-and-refining-game-concepts`는 `DECISION_SPECIFIC_RESEARCH`, `governing-game-user-research-coverage`는 `RESEARCH_QUESTION_FIRST`와 `DECISION_RELEVANT_COVERAGE`, `designing-vertical-slices`는 `PLAYER_VALUE_TRACE_REQUIRED`를 소유한다.
- 튜토리얼 선감사는 프로젝트 Notion/GitHub 정본을 기본으로 하고 폐기된 Sheets는 명시적 migration/read-only evidence에만 한정한다.

### Guardrail

11개 연구 영역을 `11/11` 채우기 목표로 바꾸지 않는다. 자동 테스트·정적 문서·UI 렌더가 사람의 이해·감정·고민·기억을 직접 증명한다고 승격하지 않는다. 기존 코어 판정과 새 코어 확정 Skill을 합쳐 lifecycle authority를 흐리지 않는다.

### Revisit

시뮬레이션처럼 고전적 polished Vertical Slice가 대표성을 왜곡하는 프로젝트가 반복되거나, P04 연구 실행 Skill이 새로 생겨 coverage/execution 경계가 바뀔 때 재검토한다.
