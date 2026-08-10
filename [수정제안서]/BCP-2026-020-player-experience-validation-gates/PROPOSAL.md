# BCP-2026-020 — 플레이어 경험 증거·첫 10분·결정 화면·미니게임 서사 Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base` + 2026-08-10 주간 교차 프로젝트 개선 검토
- 초기 관찰 Base 커밋: `eea83c7a2306265312588894f5f86fe8930e2f72`
- 병합 전 재검증 Base 커밋: `810b01f98bfef9232f4810a3d0006b66e1d296f0`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `패턴 + 검증 전 공용 후보`
- 제안 제출 승인: 사용자 지시 `진행해서 [수정제안서]에 추가해`
- PR 생성·병합 승인: 사용자 지시 `만들고 병합까지 진행해`
- 구현 승인: `미승인`

## 관찰과 증거

현재 Base와 여러 게임 프로젝트는 기술·문서·정본·CI·Vertical Slice 계약이 빠르게 정교해지고 있다. 그러나 자동 테스트·엔진 실행·UI 렌더·문서 승인과 **신규 플레이어가 실제 핵심 경험을 이해하고 기억하는지**는 서로 다른 증거다.

교차 프로젝트에서 반복적으로 다음 공백이 확인된다.

1. 기술·UI 자동 검증이 존재해도 사람 사용성·플레이어 경험은 `NOT_RUN`일 수 있다.
2. 여러 프로젝트가 Vertical Slice 또는 첫 10~15분 흐름을 기획 중이지만, 이를 공용 계약으로 비교할 기준은 분산돼 있다.
3. 핵심 화면이 기능 목록으로 커질수록 플레이어가 지금 내려야 할 결정이 흐려질 수 있다.
4. 미니게임은 독립 재미만으로 채택하면 메인게임·서사와 분리되고, 1인 개발의 콘텐츠·QA 비용을 크게 늘릴 수 있다.
5. Base의 `BCP-2026-004`는 이미 결정 질문 중심 Context 큐레이션과 `context_budget`을 구현했으므로 **Context Budget을 새 규칙으로 중복 승격하면 안 된다.**
6. `BCP-2026-011`의 `GAME_FEATURE_DESIGN_SPEC`는 Experience Intent, Acceptance, Telemetry/Playtest를 포함하므로 새 제안은 기능 상세기획을 복제하지 않고 **증거 단계·초반 경험·결정 화면·미니게임 채택 Gate**만 보완해야 한다.

외부 AI 협업 벤치마크도 같은 방향을 지지한다.

- OpenAI, *How OpenAI uses Codex*: 프롬프트를 GitHub Issue처럼 구조화하고, 지속 컨텍스트는 `AGENTS.md`에 두는 방식을 권장한다.
  - https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*: 하나의 거대한 `AGENTS.md`보다 짧은 지도와 구조화된 저장소 지식을 사용한 경험을 설명한다.
  - https://openai.com/index/harness-engineering/

### 근거 패키지

- 교차 프로젝트 Gap/적대적 검토: `evidence/WEEKLY_RESEARCH_AND_CROSS_PROJECT_GAP_ANALYSIS.md`
- 2026-08-10 주간보고서 정리본: `evidence/WEEKLY_IMPROVEMENT_REPORT_2026-08-10.md`

주간보고서 정리본은 메인게임·미니게임·글쓰기·종합 반영안 전체를 보존하되, 변동성이 큰 수치·순위보다 **Base 승격에 필요한 일반화 가능한 판단과 프로젝트별 적용 후보**를 중심으로 정리한다.

## 일반화 후보

### 1. `PLAYER_EXPERIENCE_EVIDENCE_GATE`

자동·기술·UI 증거와 사람 경험 증거를 분리한다.

```yaml
TECH_EVIDENCE:
  proves:
    - 코드·데이터·Schema·엔진 실행의 기술적 상태

UI_EVIDENCE:
  proves:
    - 렌더·입력·포커스·해상도·시각 상태의 관찰 가능한 상태

HUMAN_USABILITY_EVIDENCE:
  proves:
    - 처음 보는 사람이 조작·정보 구조·다음 행동을 이해하는지

PLAYER_EXPERIENCE_EVIDENCE:
  proves:
    - 의도한 고민·감정·선택·보상·기억이 실제 플레이에서 발생하는지
```

규칙:

- 앞 단계 PASS는 뒤 단계 PASS를 의미하지 않는다.
- 실제 사람 검증이 없으면 `HUMAN_USABILITY_EVIDENCE=NOT_RUN`, `PLAYER_EXPERIENCE_EVIDENCE=NOT_RUN`을 유지한다.
- 재미·이해도·몰입·제품 완성도 주장은 실제 근거 단계의 상한을 넘지 않는다.
- 작은 내부 테스트도 관찰 대상·참가 조건·질문·결과·한계를 기록한다.

### 2. `FIRST_10_MINUTES_CONTRACT`

첫 10분은 전체 시스템 설명이 아니라 **대표 경험의 축소판**으로 설계한다.

기본 점검 질문:

```text
대표 문제를 보았는가
→ 대표 행동을 해보았는가
→ 의미 있는 첫 선택을 했는가
→ 선택의 결과를 확인했는가
→ 다음에는 무엇을 바꾸고 싶은지 질문이 생겼는가
```

권장 기본값:

- 첫 10분 안에 `대표 문제 / 대표 행동 / 첫 선택 / 첫 결과 / 다음 질문` 중 핵심 흐름을 최소 한 번 경험하게 한다.
- 정확한 분 단위는 장르·세션 길이·의도한 불투명성에 따라 프로젝트가 조정한다.
- 튜토리얼·세계관·시스템 전체를 첫 10분에 노출하는 것을 목표로 하지 않는다.
- 공포·미스터리처럼 의도적인 불확실성이 중요한 작품도 **행동 목적까지 불명확하게 만드는 것**과 구분한다.

### 3. `DECISION_SCREEN_RULE`

핵심 화면은 기능 목록보다 **현재 플레이어가 내려야 할 결정**을 중심으로 설계한다.

가능하면 한 화면에서 다음 네 질문에 답한다.

```text
현재 상황은 무엇인가
무엇을 선택할 수 있는가
선택에 필요한 정보는 무엇인가
선택하면 어떤 비용·위험·결과가 예상되는가
```

적용 예:

- 메인 화면: 세계관 정체성 + 현재 상태 + 다음 핵심 행동.
- 전투/퍼즐 화면: 현재 질문 + 선택 가능한 행동 + 관련 자원/정보.
- 휴식/편성 화면: 모든 기능 버튼보다 이번 구간의 핵심 trade-off.
- 결과 화면: 변화 + 원인 + 다음 선택에 미치는 영향.

이 규칙은 특정 UI 레이아웃·색·컴포넌트를 Base에서 강제하지 않는다.

### 4. `MINIGAME_NARRATIVE_FUNCTION_GATE`

미니게임을 별도 시스템으로 채택하기 전에 다음을 검사한다.

```yaml
main_game_information_used:
player_decision_tested:
narrative_or_system_result_changed:
failure_learning:
rule_learning_time:
reusability:
content_cost:
flow_interrupt_cost:
```

채택 기본 조건:

1. 메인게임 또는 직전 장면에서 얻은 정보·규칙을 실제로 사용한다.
2. 플레이어 판단을 단순 클릭·반사신경이 아니라 의미 있는 결과로 시험한다.
3. 성공·실패가 인물·사건·자원·기록·다음 선택 중 하나 이상을 바꾼다.
4. 실패가 오답 이유·새 정보·위험 사례 등 학습을 남긴다.
5. 공통 프레임·데이터 변형으로 재사용 가능한지 먼저 검토한다.
6. 선택지·짧은 공통 인터랙션만으로 같은 경험을 낼 수 있다면 독립 미니게임을 만들지 않는다.

예외:

- 미니게임 자체가 메인 코어인 퍼즐·액션 게임에는 이 Gate를 `CORE_INTERACTION_EVIDENCE`로 변형하며, 메인게임을 미니게임으로 오분류하지 않는다.

### 5. 새 광역 Skill을 만들지 않는다

이번 후보는 새 `player-experience-management` 같은 ACTIVE Skill을 추가하지 않는다.

승인 후 연결 후보:

- 핵심 경험·Vertical Slice·Playtest: `analyzing-and-refining-game-concepts`
- 기능 세부기획: `GAME_FEATURE_DESIGN_SPEC`와 `managing-design-documents`
- 화면 결정·시각 검증: 기존 UX/UI 설계·감사 owner
- 반례·claim ceiling 공격: `running-adversarial-review-and-refinement`
- Context Budget: 이미 구현된 `BCP-2026-004` owner를 그대로 사용

`Consolidation First`를 적용해 같은 질문의 owner를 늘리지 않는다.

## 프로젝트 전용으로 남길 내용

아래 항목은 공용 Base에 넣지 않고 **해당 프로젝트의 현행 책임 원본·Decision·테스트 계약**으로 적용하는 것이 적합하다.

### A. 메인게임 적용 후보

| 프로젝트 | 우선도 | 적용하면 좋은 내용 | 적용 위치 후보 | Base에 올리지 않을 프로젝트 값 |
|---|---:|---|---|---|
| `urban-legend` | 매우 높음 | `PLAYER_EXPERIENCE_EVIDENCE_GATE`, 첫 10분 조사 경험, 관제실/조사 화면의 `DECISION_SCREEN_RULE` | `docs/planning/PROJECT_DIRECTION.md`, `docs/GAME_DESIGN_DOCUMENT.md`, `docs/GODOT_NATIVE_UI_ARCHITECTURE.md`, `TEST_CHECKLIST.md` | 괴이 기록국·아카·괴이 매뉴얼·사건 규칙·실제 UI 배치 |
| `omenward` | 매우 높음 | 다음 Decision인 `FIRST-10-15-MINUTES-FLOW`에 첫 경험 계약과 사람 증거 Gate 직접 적용 | `docs/PROJECT_CORE.md`, `docs/OMENWARD_GDD_CURRENT_CANON.md`, 현재/다음 Decision 책임 원본, `docs/CURRENT_IMPLEMENTATION_STATUS.md` | 병종·마력탑·상인·골드/마력 수치·실제 전투 규칙 |
| `Ten-Paces-Hidden-Moves` | 높음 | `VERTICAL_SLICE_APP_FLOW_SHELL`의 Main→Route→Combat→Result에서 첫 결정·결과가 읽히는지 검증 | `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`, 현재 화면/앱플로 Decision 책임 원본, 제품 검증 계약 | 10칸·3/3/4·무공/절초·행동 슬롯·실제 카드 UI |
| `Blacksmith` | 높음 | 강화의 `멈춤/추가 도전` 고민이 첫 세션에서 실제로 발생하는지 Player Evidence로 분리 검증 | `CURRENT_CONFIRMED_DECISIONS.md`, `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`, Vertical Slice Decision/검증 계약 | 강화 수치·등급·예술성·재료·실제 Workshop UI |
| `ninja-survival-godot` | 높음 | 단계형 MVP에서 첫 전투→결과→휴식/가방 선택까지 첫 경험 계약 적용 | `docs/CURRENT_CONFIRMED_DECISIONS.md`, `MVP_ROADMAP.md`, MVP-3/4 Goal·검증 계약 | 4개 닌자 유파·20분 런·배낭 모양·운명 선택·실제 수치 |
| `Switchy-Express-Cargo-Puzzle` | 높음 | 튜토리얼 1~10과 Vertical Slice에서 `현재 배송 문제 → 선로/적재/분기 결정 → 결과`가 읽히는지 검증 | `기획서/10_경험/CORE_GAMEPLAY.md`, `기획서/40_표현/VISUAL_DIRECTION.md`, `기획서/50_제작_검증/VERTICAL_SLICE_CONTRACT.md` | LIFO·선로비·별 조건·튜토리얼 맵·실제 퍼즐 데이터 |

### B. 미니게임 적용 후보

| 프로젝트 | 판정 | 적용 제안 |
|---|---|---|
| `urban-legend` | **직접 적용** | `docs/MINIGAME_SYSTEM_SPEC.md`에 본편 단서 사용·실패 학습·사건/기록 결과·재사용성 Gate를 프로젝트 값으로 구체화한다. 조사 마지막 규칙 검증이라는 기존 불변 조건을 유지한다. |
| `Blacksmith` | **조건부 적용** | 강화·정밀강화를 별도 미니게임으로 확장하려는 경우에만 Gate를 사용한다. 현재 한 입력 한 결과 코어를 불필요한 조작 미니게임으로 바꾸는 근거로 사용하지 않는다. |
| `omenward` | **조건부 적용** | 룰렛·상인·전술 선택을 별도 미니게임화할 때만 적용한다. 전투 코어 자체는 미니게임으로 취급하지 않는다. |
| `ninja-survival-godot` | **조건부/비적용** | 배낭 정리·휴식은 메인 런 루프의 핵심 상호작용이므로 미니게임으로 낮추지 않는다. 부가 이벤트가 별도 미니게임화될 때만 적용한다. |
| `Ten-Paces-Hidden-Moves` | **비적용 기본** | 비무·무공 배치는 메인 코어다. `MINIGAME_NARRATIVE_FUNCTION_GATE`를 전투 코어에 강제하지 않는다. |
| `Switchy-Express-Cargo-Puzzle` | **비적용 기본** | 퍼즐 자체가 메인게임이므로 미니게임 Gate 대신 `CORE_INTERACTION_EVIDENCE`로 변형한다. |

### C. 글쓰기 적용 후보

이번 BCP는 새 글쓰기 Skill을 만들지 않는다. 공용 글쓰기 방법은 이미 `BCP-2026-004`의 Context 큐레이션과 `BCP-2026-009`의 연재소설 Discipline을 우선 사용한다.

| 프로젝트 | 적용하면 좋은 프로젝트 전용 내용 | 적용 위치 후보 |
|---|---|---|
| `urban-legend` | 첫 장면에서 `현재 질문 / 플레이어가 아는 정보 / 화자가 아는 정보 / 공개 금지 정보 / 다음 행동`을 프로젝트 장면 계약으로 구체화. 첫 선택이 실제 UI에서 읽히는지 Player Evidence와 연결 | `docs/planning/NARRATIVE_CONTENT_PLAN.md`, `docs/DIALOGUE_AUTHORING_WORKFLOW.md`, 대표 에피소드 데이터/장면 Spec |
| `Coc-Fiction` | Context Budget·Canon/화자 정보 권한·장면 목적은 기존 BCP-004/009/012/017 계열에서 적용. 이번 BCP를 이유로 게임식 첫 10분·미니게임 Gate를 소설에 강제하지 않음 | 현행 Canon·집필·퇴고 책임 원본 |
| `Ten-Paces-Hidden-Moves` | 비무 전후 대사·복기는 `첫 10분 계약`보다 `결정 결과를 설명하고 다음 빌드 판단을 만드는가`로 변형 | 전투 결과·복기·서사 책임 원본 |
| `Blacksmith` | 제작 결과 문구·사건·연대기는 강화 결과의 원인과 작품 기억을 보강하되 수치 설명을 반복하지 않음 | Game Bible과 작품/연대기 서사 책임 원본 |
| `omenward` | 전술·상인·전장 안내 문구는 플레이어의 다음 결정을 명확히 하고 세계관 설명을 과도하게 앞세우지 않음 | GDD 및 UI/서사 관련 Decision 책임 원본 |
| `ninja-survival-godot` | 결과·휴식·운명 선택 텍스트는 전투 결과를 해석하고 다음 빌드 고민을 생성하는 역할로 제한 | MVP-3/4/5 기획·결과 화면 책임 원본 |
| `Switchy-Express-Cargo-Puzzle` | 튜토리얼 문구는 퍼즐 규칙을 설명하기보다 현재 배송 문제·가능 행동·실패 이유를 짧게 전달 | Core Gameplay·Vertical Slice·튜토리얼 책임 원본 |

### 프로젝트 적용 우선순위

```text
P0: urban-legend / omenward
P1: Ten-Paces-Hidden-Moves / Blacksmith / ninja-survival-godot / Switchy-Express-Cargo-Puzzle
SEPARATE_WRITING_TRACK: Coc-Fiction
```

이 우선순위는 Base 구현 승인이나 각 프로젝트 구현 승인을 의미하지 않는다. 각 프로젝트의 현재 Gate·Decision·보호 경계를 따라 별도 제안·Issue·PR에서 적용한다.

## 적용 조건과 비사용 조건

### 적용

- Vertical Slice·First Playable·첫 10~15분 흐름을 평가한다.
- 기술 테스트는 충분하지만 신규 플레이어 이해·재미 근거가 없다.
- 핵심 화면에 기능·정보가 늘어 현재 결정이 흐려졌다.
- 메인게임과 별도 미니게임의 연결 가치·제작비를 판단해야 한다.
- 신규 시스템 추가 전에 현재 루프의 플레이어 체감부터 확인해야 한다.

### 비사용 또는 변형

- 오탈자·링크·단순 문서 정리처럼 플레이 경험이 변하지 않는 L0 작업.
- 백엔드·빌드·CI·라이선스 등 플레이어 경험과 직접 무관한 변경.
- 퍼즐·전투 자체가 메인 코어인데 이를 미니게임으로 오분류하는 경우.
- 의도적으로 느리고 불투명한 첫 구간이 작품 핵심인 경우: `FIRST_10_MINUTES_CONTRACT`의 시간을 그대로 강제하지 않고 대표 경험·행동 목적 기준으로 변형한다.
- 사람 검증이 불가능한 상태에서 자동 점수로 `PLAYER_EXPERIENCE_PASS`를 대체하는 경우.

## 반례와 위험

1. **첫 10분 공식화 과잉**
   - 위험: 모든 장르가 동일한 템포를 갖게 됨.
   - 대응: 시간은 기본값이며 장르별 `ADAPT` 허용. 핵심은 대표 문제·행동·선택·결과·다음 질문의 존재다.

2. **사람 검증의 의식화**
   - 위험: 실제 관찰 없이 체크박스만 채움.
   - 대응: 참가 조건·관찰 질문·실제 답변/행동·한계를 evidence로 남긴다.

3. **Decision Screen의 정보 과소화**
   - 위험: 분위기·세계관·탐색성을 해칠 수 있음.
   - 대응: 모든 정보를 제거하는 규칙이 아니라 현재 결정의 계층을 가장 명확히 하는 규칙으로 사용한다.

4. **미니게임 Gate의 코어게임 오적용**
   - 위험: 퍼즐·전투 핵심을 부가 기능처럼 취급.
   - 대응: `CORE_INTERACTION_EVIDENCE` 예외를 명시한다.

5. **BCP-2026-004 중복**
   - 위험: Context Budget·큐레이션 정본이 두 개가 됨.
   - 대응: 새 Context 규칙을 만들지 않고 BCP-004를 dependency로 참조한다.

6. **BCP-2026-011 중복**
   - 위험: Feature Spec의 Experience/Playtest 필드와 새 Template이 경쟁.
   - 대응: 새 광역 Template을 만들지 않고 기존 Feature Spec·Playtest 계약에 증거 Gate와 선택적 Checklist만 합성한다.

7. **1인 개발 비용 증가**
   - 위험: 사람 테스트 문서가 구현보다 무거워짐.
   - 대응: 대표 Vertical Slice에 작은 테스트를 우선하고 전체 콘텐츠에 동일 규모 테스트를 강제하지 않는다.

## 영향 범위와 검증

### 승인 후 영향 후보

- `skills/analyzing-and-refining-game-concepts/`의 Vertical Slice·playtest reference
- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md`가 존재하는 경우 Acceptance/Telemetry와 연결
- UX/UI 설계·감사 책임 원본의 `DECISION_SCREEN_RULE` reference
- `running-adversarial-review-and-refinement`의 claim ceiling·사람 증거 반례
- 프로젝트 운영 Template의 `TECH / UI / HUMAN_USABILITY / PLAYER_EXPERIENCE` 상태 표기
- 필요 시 작은 `FIRST_10_MINUTES` / `MINIGAME_NARRATIVE_GATE` checklist reference

### 구현 전 검증 계획

1. BCP-2026-004 Context 큐레이션과 owner 중복 검사.
2. BCP-2026-011 Feature Spec의 Experience/Playtest와 중복·합성 경계 검사.
3. 공포·미스터리·전투·퍼즐·클리커/제작 등 최소 4개 장르 반례 테스트.
4. `urban-legend`, `omenward`, `Ten-Paces-Hidden-Moves`, `Blacksmith`, `ninja-survival-godot`, `Switchy-Express-Cargo-Puzzle` 적용 예를 통해 공용 원리와 프로젝트 값 분리 검사.
5. 사람 검증 `NOT_RUN` 상태가 자동 테스트로 PASS 전환되지 않는 contract test.
6. `MINIGAME_NARRATIVE_FUNCTION_GATE`가 메인 퍼즐/전투 코어에 오적용되지 않는 비사용 시나리오.
7. Registry·Documentation Map·reference freshness·Base integrity·`git diff --check`.
8. 실제 프로젝트 Pilot 전에는 재미·유지율·판매 성과를 검증됐다고 주장하지 않는다.

## 필요한 도구·파일·권한

- 필요 항목: Base·프로젝트 GitHub read, Base `[수정제안서]` write, 승인 후 별도 구현 PR 권한, 프로젝트별 사람 플레이테스트 환경
- 필요한 이유: 기존 owner 중복 검사, 교차 프로젝트 적용성 검증, Proposal Registry 추적
- 설치·적용 방법: 신규 외부 MCP·Plugin·CLI 설치 없음. 기존 Base Skill·Template·프로젝트 문서 체계에 합성한다.
- 설치 후 확인 명령: 승인 전 `해당 없음`; 구현 시 Base 필수 contract/integrity/reference-freshness 검증을 따른다.
- 최소 권한: 제안 제출 단계에서는 `[수정제안서]/**` 쓰기만 필요. 활성 Base 파일 변경 권한은 구현 승인 전 사용하지 않는다.

## 승인과 구현

- 제안 제출 승인 근거: 2026-08-10 사용자 지시 `진행해서 [수정제안서]에 추가해`
- PR 생성·병합 승인 근거: 2026-08-10 사용자 지시 `만들고 병합까지 진행해`
- 구현 승인 근거: `미승인`
- 구현 PR: `없음`
- 제안 등록 PR: `https://github.com/alsdmlals4-eng/Base/pull/273`
- 현재 허용 범위: `[수정제안서]/**`의 제안·증거·Registry 등록 및 해당 제안 PR 병합
- 활성 Base Skill·Method·Template·Test 변경: `금지`
- 프로젝트 직접 반영: `금지`; 위 표는 적용 후보와 위치 제안일 뿐 각 프로젝트 승인·Decision을 대체하지 않는다.
- 롤백: 제안 PR을 revert하거나 Proposal 상태를 `DEFERRED / REJECTED`로 변경해 이력을 보존한다. 활성 Base와 프로젝트 파일은 이번 제안 등록으로 변경하지 않는다.
