# BCP-2026-020 Evidence — 2026-08-10 주간 조사·교차 프로젝트 Gap 분석

## 1. 목적

이 문서는 다음 주간 개선 후보를 Base 공용 원리와 프로젝트 전용 적용안으로 분리하기 위한 증거 메모다.

- 플레이어 경험 증거 Gate
- 첫 10분 경험 계약
- 결정 중심 화면 원칙
- 미니게임 서사 기능 Gate
- Context Budget의 기존 Base 책임과 중복 여부

이 문서는 외부 사례를 정본으로 사용하지 않는다. Base 현행 owner와 실제 프로젝트 계약을 우선하고 외부 자료는 보조 벤치마크로만 사용한다.

## 2. Base 중복·책임 감사

### BCP-2026-004 — 이미 구현된 책임

`BCP-2026-004-ai-instruction-context-ui-motion`은 이미 다음을 구현했다.

- 결정 질문 중심 Context 큐레이션
- `context_budget`
- `include_criteria / exclude_criteria`
- progressive load / refresh trigger
- Artifact-first 전달
- 게임 UI의 상태·입력·모션 검증

따라서 이번 주 조사에서 도출된 `Context Budget`은 신규 BCP 후보가 아니라 **기존 BCP-2026-004를 프로젝트에 적용·강화할 항목**이다.

### BCP-2026-011 — 합성해야 하는 책임

`BCP-2026-011-game-feature-design-spec-system`은 다음 필드를 포함한다.

- Player Problem
- Experience Intent
- Player Verbs
- Feedback
- Success / Failure / Recovery
- UX/UI & Accessibility
- Benchmark Decision
- Risk & Prototype
- Acceptance
- Telemetry / Playtest

따라서 이번 제안은 새 기능 상세기획 Template을 만들지 않고 다음 **횡단 Gate**만 보완해야 한다.

1. `TECH / UI / HUMAN_USABILITY / PLAYER_EXPERIENCE` 증거 단계 분리
2. 첫 10분 대표 경험 계약
3. 핵심 화면의 현재 결정 중심 정보 계층
4. 독립 미니게임의 본편 연결·실패 학습·재사용성 채택 Gate

## 3. 외부 AI 협업 벤치마크

### OpenAI — How OpenAI uses Codex

공식 가이드는 다음을 권장한다.

- 프롬프트를 GitHub Issue처럼 구조화
- 파일 경로·컴포넌트·참조 구현 등 구체적 컨텍스트 제공
- 지속 컨텍스트는 `AGENTS.md` 사용
- 큰 작업을 한 번에 끝내려 하기보다 작업 큐와 작은 단위 활용

Source:
https://openai.com/business/guides-and-resources/how-openai-uses-codex/

### OpenAI — Harness engineering

OpenAI는 큰 단일 `AGENTS.md`가 다음 문제를 만들었다고 설명한다.

- 관련 코드·작업 컨텍스트를 밀어냄
- 모든 지시가 중요해져 우선순위가 사라짐
- stale rule 누적
- 기계적 freshness/ownership 검사 어려움

대신 짧은 `AGENTS.md`를 저장소 지식으로 이동하는 지도처럼 사용하고, 구조화된 `docs/`를 system of record로 유지한다.

Source:
https://openai.com/index/harness-engineering/

### Base 판정

이 외부 사례는 BCP-2026-004의 Context 큐레이션 방향을 재확인하지만 새 Context Skill을 요구하지 않는다.

## 4. 교차 프로젝트 실제 Gap

### `urban-legend`

현행 계약에서 확인되는 사항:

- 조사·회수·괴이 규칙·미니게임·서사 책임 원본이 분리돼 있다.
- 시나리오당 대표 미니게임은 조사 마지막 규칙 검증이며 이후 안정화·회수로 연결한다.
- 요원·아카·장비·자동행동은 핵심 정답을 대신하지 않는다.
- 1280×720 / 1920×1080에서 한국어 줄바꿈·포커스·첫 선택 노출을 확인한다.

Gap:

- UI/자동 QA와 실제 신규 플레이어의 `핵심 질문·추론·결과 기억`을 별도 Evidence state로 관리할 공용 Gate가 필요하다.
- `MINIGAME_SYSTEM_SPEC`에 본편 단서 사용·실패 학습·재사용성·서사 결과를 더 명확히 프로젝트 값으로 연결할 가치가 높다.

권장 적용:

- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: 직접 적용
- `FIRST_10_MINUTES_CONTRACT`: 직접 적용
- `DECISION_SCREEN_RULE`: 직접 적용
- `MINIGAME_NARRATIVE_FUNCTION_GATE`: 직접 적용
- 글쓰기: 첫 장면의 정보 권한은 프로젝트 Narrative/Dialogue 책임 원본에 구체화

### `omenward`

현행 `AGENTS.md`의 다음 Decision이 이미:

`OMW-DEC-20260805-PLANNING-FIRST-10-15-MINUTES-FLOW-V1`

이다.

현재 제품 코드는 승인되지 않은 `TOTAL_PLANNING` 단계이며, PC/Android 플랫폼 구조와 핵심 전술·마력·상인 설계가 정본화되고 있다.

Gap:

- 첫 10~15분에 어떤 시스템을 보여줄지보다 `플레이어가 무엇을 고민하고 어떤 결과를 확인해야 하는지`를 명시할 공용 계약이 직접 필요하다.

권장 적용:

- `FIRST_10_MINUTES_CONTRACT`: **최우선 Pilot**
- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: 직접 적용
- `DECISION_SCREEN_RULE`: 전술·마력탑·상인 화면에 적용
- 미니게임 Gate: 룰렛/부가 이벤트가 독립 미니게임화될 때만 조건부 적용

### `Ten-Paces-Hidden-Moves`

현행 상태:

- `product_stage: VERTICAL_SLICE_APP_FLOW_PLANNING`
- 다음 패키지: `VERTICAL_SLICE_APP_FLOW_SHELL`
- Main → 시작 무공 선택 → Route·Node·Briefing → Combat → Result·Reward·Retry
- 화면 계약: 메인 / 비무 / 무공 구성·자원 / 결과·복기·보상
- 자동 검증은 실제 Windows 렌더·Android 실기기·사람 플레이를 대체하지 않는다.

Gap:

- App Flow가 기술적으로 연결되는 것과 첫 플레이어가 `무공 선택 → 전투 계획 → 복기`의 판단 루프를 이해하는 것을 구분할 Evidence Gate가 필요하다.

권장 적용:

- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: 직접 적용
- `FIRST_10_MINUTES_CONTRACT`: App Flow Pilot에 적용
- `DECISION_SCREEN_RULE`: 메인·무공 구성·복기 화면에 적용
- `MINIGAME_NARRATIVE_FUNCTION_GATE`: **비적용**. 비무는 메인 코어다.

### `Blacksmith`

현행 상태:

- 일반 제품 구현은 `BLOCKED`
- 승인된 Vertical Slice namespace만 제한 구현 가능
- 코어는 `강화 성공·실패 + 멈춤·추가 도전`의 즉각 반복 재미
- 실제 Android·접근성·성능·사람 플레이는 `NOT_RUN`

Gap:

- 자동/기술 검증과 실제 `멈출지 더 도전할지`라는 감정·판단의 재미를 분리해야 한다.

권장 적용:

- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: 매우 적합
- `FIRST_10_MINUTES_CONTRACT`: 강화 코어 Vertical Slice에 적용
- `DECISION_SCREEN_RULE`: Workshop/강화 결과 화면에 적용
- 미니게임 Gate: 정밀강화 등을 별도 조작 미니게임으로 확장할 때만 조건부. 현재 `한 입력 한 결과` 코어를 훼손하지 않는다.

### `ninja-survival-godot`

현행 상태:

- Godot rebuild
- staged planning MVP
- MVP-0 전투 기초 → MVP-1 Combat DDD → MVP-2 유파 → MVP-3 결과/휴식 → MVP-4 배낭 → MVP-5 최종 런/메타
- 휴식 단계에 전투 요약·전리품·배낭 정리·조합 힌트·상점/강화·운명 선택·다음 스테이지 예고가 존재

Gap:

- 단계별 기능이 많아질수록 첫 런에서 모든 시스템을 설명하는 위험과 휴식 화면의 결정 중심 계층 문제가 커진다.

권장 적용:

- `FIRST_10_MINUTES_CONTRACT`: 전투 DDD와 첫 결과까지 적용
- `DECISION_SCREEN_RULE`: 휴식/배낭/결과 화면에 높은 가치
- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: MVP별 Human/Player pass 분리
- 미니게임 Gate: 배낭·휴식은 메인 코어이므로 기본 비적용

### `Switchy-Express-Cargo-Puzzle`

현행 상태:

- 수작업 유한 배송 퍼즐
- 튜토리얼 1~10
- Core Gameplay / Visual Direction / Vertical Slice Contract 책임 원본 존재
- 퍼즐 자체가 선로·LIFO·적재·분기·배송 판단의 메인 코어

Gap:

- 튜토리얼이 규칙 설명 목록이 되지 않고 플레이어가 `배송 문제 → 선로/적재/분기 판단 → 결과`를 실제로 이해하는지 검증해야 한다.

권장 적용:

- `FIRST_10_MINUTES_CONTRACT`: 튜토리얼 1~10 감사에 적용
- `DECISION_SCREEN_RULE`: 현재 배송 문제와 선택 정보 계층에 적용
- `PLAYER_EXPERIENCE_EVIDENCE_GATE`: Vertical Slice에 적용
- `MINIGAME_NARRATIVE_FUNCTION_GATE`: **비적용**. 퍼즐이 메인게임이므로 `CORE_INTERACTION_EVIDENCE`로 변형

### `Coc-Fiction`

이 프로젝트는 게임 플레이 Gate의 직접 Pilot 대상이 아니다.

현재 관련 Base 이력:

- BCP-2026-009 연재소설 집필·퇴고 Discipline
- BCP-2026-012 Canon Migration Debt
- BCP-2026-017 Reconciliation Frontier / Derived Continuity Guard
- BCP-2026-004 Context Budget·큐레이션

권장:

- Context Budget, 장면 정보 권한, Canon 경계는 기존 글쓰기·정본 owner에서 적용
- `FIRST_10_MINUTES_CONTRACT`, `DECISION_SCREEN_RULE`, `MINIGAME_NARRATIVE_FUNCTION_GATE`를 소설에 억지로 일반화하지 않음
- 이번 BCP 구현 범위에서 Coc-Fiction 전용 변경 없음

## 5. 프로젝트별 적용 우선순위

### P0 Pilot

1. `omenward`
   - 다음 Decision 자체가 첫 10~15분 흐름이므로 가장 직접적인 Pilot.
2. `urban-legend`
   - 메인게임·미니게임·서사 세 축을 동시에 검증할 수 있음.

### P1 Pilot

3. `Ten-Paces-Hidden-Moves`
   - Vertical Slice App Flow와 사람 제품 검증 경계.
4. `Blacksmith`
   - 기술 PASS와 실제 강화 재미를 분리하기 적합.
5. `ninja-survival-godot`
   - 첫 런과 휴식/배낭의 정보 계층 검증.
6. `Switchy-Express-Cargo-Puzzle`
   - 튜토리얼 1~10과 퍼즐 Core Interaction 검증.

### Separate Writing Track

- `Coc-Fiction`
  - 기존 글쓰기/Canon BCP 계열 사용.

## 6. 적대적 검토

### 공격 1 — `FIRST_10_MINUTES`가 장르를 획일화한다

판정: 위험 있음.

대응:

- 시간은 default heuristic으로만 사용.
- 공포·미스터리·슬로우번 장르는 `대표 문제 / 행동 목적 / 선택 / 결과 / 다음 질문` 구조를 유지하면서 시간값을 프로젝트가 조정한다.

### 공격 2 — 사람 테스트가 또 하나의 문서 의식이 된다

판정: 가장 큰 운영 위험.

대응:

- PASS 문구보다 실제 행동·답변·관찰 결과를 evidence로 요구.
- 참가자 수가 적으면 `SMALL_SAMPLE` 한계를 함께 기록.
- 실행하지 않으면 `NOT_RUN`.

### 공격 3 — Decision Screen 때문에 분위기 UI가 도구 화면처럼 된다

판정: 잘못 적용하면 가능.

대응:

- 모든 정보를 숫자/버튼으로 노출하는 규칙이 아님.
- 시각적 분위기와 세계관 안에서 **현재 질문의 우선순위만 명확하게** 한다.

### 공격 4 — 미니게임 Gate가 모든 부가 놀이를 제거한다

판정: 과잉 YAGNI 위험.

대응:

- 감정 완충·캐릭터 표현 같은 명확한 역할도 `narrative_or_system_result_changed`로 인정 가능.
- 단, 반복 제작비가 큰 독립 시스템은 역할과 비용을 증명해야 한다.

### 공격 5 — BCP-2026-004 / 011과 owner 충돌

판정: 신규 Skill/Template을 만들면 충돌 가능성이 높음.

대응:

- Context는 BCP-004를 참조만 한다.
- Feature Spec은 BCP-011 owner를 유지한다.
- 이번 제안은 작은 Gate/reference/checklist 합성만 후보로 둔다.

## 7. 제안 판정

```yaml
Context_Budget_New_Rule: REJECT_DUPLICATE
Player_Experience_Evidence_Gate: SUBMIT
First_10_Minutes_Contract: SUBMIT_WITH_ADAPTATION
Decision_Screen_Rule: SUBMIT_WITH_ADAPTATION
Minigame_Narrative_Function_Gate: SUBMIT_WITH_CORE_GAME_EXCEPTION
New_Broad_Skill: AVOID
Project_Direct_Implementation: NOT_AUTHORIZED
```

## 8. 구현 전 필수 조건

- 사용자 `APPROVED_FOR_IMPLEMENTATION` 결정과 재현 가능한 approval_ref
- BCP-2026-004 / 011 owner overlap 최종 확인
- 최소 2개 서로 다른 장르 Pilot 설계
- 메인 코어를 미니게임으로 오분류하지 않는 비사용 테스트
- `NOT_RUN` claim ceiling contract
- 프로젝트 고유 값이 Base 공용 문구에 섞이지 않았는지 적대적 감사
