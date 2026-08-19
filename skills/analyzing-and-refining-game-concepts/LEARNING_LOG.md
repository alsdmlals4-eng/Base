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

## 2026-08-19 — 핵심 규칙은 Skill에서 끝내지 않고 실제 기획 consumer까지 닫는다

### Trigger

PR #539의 P04 규칙을 최신 completed main 위 독립 workstream으로 복사해 재검증하자, Skill에는 존재하지만 실제 작성 템플릿이 소비하지 않는 규칙과 폐기된 작업면 권위가 남아 있었다.

### Evidence reviewed

- `VERTICAL_SLICE_PLAN.md`, `GAME_CONCEPT_DIRECTION_REVIEW.md`, `GAME_BENCHMARK_PLAYER_EVIDENCE.md`, `TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`, `GAME_FEATURE_DESIGN_SPEC.md`, `GAME_UX_UI_SYSTEM.md`
- P04 Context Pack의 `WORLD_STORYLINE_FIT_REQUIRED`, 3대안, Better Alternative Search, long-term fit 요구
- Required Check가 실제로 실행하는 `tests/test_game_design_difficulty_workflow.py`
- P05 `test_game_ux_ui_system.py`의 semantic `usage_context` 계약

### Lesson

- `WORLD_STORYLINE_FIT_REQUIRED`는 세계관이 없는 게임에 억지 서사를 추가하는 규칙이 아니라, 세계관·핵심 스토리·플레이어 판타지가 실제로 관련될 때 기능/코어가 이를 훼손하지 않는지 보는 조건부 Gate다.
- 최소 3대안·Better Alternative Search·장기계획 적합성은 전역 정책에만 있으면 실제 벤치마크 작성에서 누락될 수 있으므로 의사결정 consumer가 직접 필드를 가져야 한다.
- 폐기된 도구 이름을 지울 때도 `usage_context`처럼 도구와 독립적인 의미 필드는 보존하고 현재 Notion/repository 값으로 치환해야 한다.
- 새 테스트 파일을 만들었다는 사실보다 Required CI가 실제 그 테스트를 소비하는지가 더 중요하다.

### Base change

- `analyzing-and-refining-game-concepts`와 컨셉/Vertical Slice consumer에 world/story/player-fantasy fit을 연결했다.
- benchmark template에 실질 대안·trade study·better-alternative recheck·long-term fit·revisit condition을 연결했다.
- active planning templates의 Google Sheets/Figma 권위를 Notion/repository current authority로 교체했다.
- 별도 연구/튜토리얼/trace Skill은 추가하지 않았다.

### Guardrail

프로젝트가 세계관·핵심 스토리와 무관하면 `NOT_APPLICABLE` 근거를 기록하고 억지 narrative 작업을 만들지 않는다. repository CI PASS는 human usability/player experience PASS가 아니다. 다른 Part가 소유한 companion test나 freshness rule은 P04가 우회 수정하지 않는다.

### Revisit

P04 planning templates의 ownership이 바뀌거나, Notion/repository authority 정책이 다시 변경되거나, Required CI에서 focused P04 regression 소비 경로가 바뀌면 재검토한다.

## 2026-08-20 — 플레이어 경험 검증은 완성형 짧은 Vertical Slice에서 한다

### Trigger

시스템만 작동하는 PoC를 먼저 플레이하면 UI·이미지·사운드·연출이 빠져 실제 게임의 몰입·가독성·첫인상·감정·기억을 판단하기 어렵다는 사용자 제작 원칙이 확정됐다.

### Evidence reviewed

- 기존 `DEMO_FIRST_VERTICAL_SLICE`와 Vertical Slice quality/pipeline/playtest 계약
- `VISUALIZED_POC_BEFORE_DEMO_TEST`가 시각 요소 비중이 낮은 PoC에 예외를 허용하던 기존 정책
- `PLAYER_VALUE_TRACE_REQUIRED`의 human evidence ceiling
- 현재 Notion + repository authority와 Existing Solution First 원칙
- exact-head CI에서 실제로 소비되는 Vertical Slice 및 visual-workflow 회귀 테스트

### Lesson

`SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`: 시스템-only PoC는 알고리즘·성능·호환성 같은 좁은 기술 질문을 푸는 내부 Spike로는 유효하지만, 재미·몰입·전체 UX를 판정하는 제품 단계로 취급하면 증거 상한을 넘는다. 플레이어 경험 검증은 짧더라도 shipping-intent UI/UX, 이미지·아트, 대표 사운드, VFX/피드백, 핵심 시스템·데이터·콘텐츠가 연결된 완성형 Vertical Slice에서 해야 한다.

### Base change

- 기존 Vertical Slice Skill을 유지하고 새 광역 Skill을 만들지 않았다.
- `RELEASE_NEAR_VERTICAL_SLICE_FIRST`, `GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE`, `SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED`를 공용 정책·Skill·Gate·작성 템플릿에 연결했다.
- `PLAYER_APPEAL_QUALITY_GATE`에 독창성, DDD, 일관성, 복잡성, 난이도, 개성·기억을 포함했다.
- 기존 자산·UI·오디오·도구를 먼저 조사하고 `ADOPT / ADAPT / REJECT`하는 `EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`를 보존했다.

### Guardrail

완성형 Slice 원칙은 모든 기술 질문을 고비용 완성 자산으로 검증하라는 뜻이 아니다. 기술 Spike는 허용하지만 플레이어 경험 PASS로 승격하지 않는다. 자동 테스트·정적 문서·렌더만으로 재미·몰입을 PASS 처리하지 않으며 실제 인간 플레이 전에는 해당 경험 축을 `NOT_RUN`으로 남긴다.

### Revisit

특정 장르에서 shipping-intent audiovisual presentation 자체가 핵심 가설을 오염시키거나, 반복 실험 비용이 학습 속도를 심각하게 저해한다는 실제 프로젝트 증거가 누적될 때 재검토한다.
