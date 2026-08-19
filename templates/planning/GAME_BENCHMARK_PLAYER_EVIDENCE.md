# 게임 벤치마크·플레이어 근거·개선안

> 비교 게임의 표면 기능을 복제하지 않고, 현재 결정 질문과 Evidence ID·원출처·플레이어 행동·자기보고·실패 사례·Case Card를 연결한다. 더 넓은 분야 횡단 조사는 `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`를 사용한다.

## 메타데이터

```yaml
research_id:
project:
baseline_commit:
created_at:
updated_at:
owner:
related_evidence_pack:
status: DRAFT | IN_RESEARCH | READY_FOR_DECISION | DECIDED | VALIDATED | SUPERSEDED
```

## 결정 질문

- 현재 결정:
- 현재 가설:
- 결정을 바꿀 근거:
- 보호할 프로젝트 코어:
- 대상 플레이어·플랫폼·지역·언어:
- 조사 기간·버전:
- 비교 차원:
- 조사 제외:
- 성공·실패·중단 조건:

## CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY

중요한 L1+ 결정은 하나의 해법을 먼저 정한 뒤 벤치마크를 근거로 붙이지 않는다. 현재 상태와 기존 해법을 먼저 확인한 뒤 **`MINIMUM_VIABLE_ALTERNATIVES: 3`**의 materially distinct 실질 대안을 만든다. 숫자를 채우기 위한 허수 대안은 금지한다.

| 대안 | 접근 방식 | 플레이어 가치 | 정확성·근거 | 제작·유지 비용 | AI Context 비용 | 충돌·위험 | Rollback | 검증 가능성 | 장기 확장성 | 관련 Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 현행 유지·현행 해법 재사용 | | | | | | | | | |
| B | 최소 수정·흡수 | | | | | | | | | |
| C | 책임 경계 재구성·다른 실행 경로 | | | | | | | | | |
| D+ | 조사에서 발견한 더 나은 대안 | | | | | | | | | |

- 유효 대안 수:
- 3개 미만이면 추가 조사·추상화가 필요한 이유:
- 임시 권장안:
- 탈락안과 탈락 이유:
- 핵심 trade-off:

### BETTER_ALTERNATIVE_SEARCH

임시 권장안을 선택한 뒤에도 새 Evidence·실패·플레이테스트·적대적 검토 finding이 나오면 더 나은 대안이 생겼는지 다시 탐색한다.

```yaml
better_alternative_search:
  new_candidates_considered: []
  stronger_option_found: false
  selected_option_after_recheck:
  replacement_reason:
```

### LONG_TERM_PLAN_FIT_REQUIRED

단기 구현량만이 아니라 플레이어 가치, 정확성·기획 충실도, 위험, 수명주기 비용, 유지보수성, rollback, 재사용·모듈성, 증거 강도와 현재 비용 경계를 비교한다.

```yaml
long_term_fit:
  player_value:
  design_fidelity:
  maintenance_and_lifecycle_cost:
  rollback_difficulty:
  reuse_and_modularity:
  evidence_strength:
  current_cost_boundary:
revisit_condition:
```

## 비교 대상

| 대상 | 유형 | 비교 차원 | 버전·기간 | 선정 이유 | Case Card |
|---|---|---|---|---|---|
|  | 직접 경쟁/인접 장르/실패 사례/혼합 사례/비게임 참고 |  |  |  | `templates/research/GAME_DEVELOPMENT_CASE_CARD.md` |

성공 사례만 선택하지 않고 최소한 실패 사례 또는 혼합 반응 사례를 함께 검토한다.

## BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE

벤치마크의 목적이 “좋은 사례를 참고”하는 수준을 넘어 **재사용 가능한 설계·제작 단위를 찾아 작업량을 줄이는 것**이라면 이 섹션을 실행한다. `표현·자산·코드`를 권한 없이 복사하지 않고, 관찰 가능한 계약과 라이선스된 재사용 가능 범위를 분리한다.

### PROJECT_FIT_DISCOVERY

사용자가 예로 든 작품·장르만 검색하지 않는다. 먼저 현재 프로젝트 정본에서 병목과 플레이어 가치를 읽고, 그 문제를 해결할 후보를 능동적으로 확장한다.

```yaml
project_fit_discovery:
  player_promise:
  core_loop:
  meaningful_choices:
  target_emotions_and_memory:
  content_bottleneck:
  balance_or_validation_bottleneck:
  ui_ux_friction:
  art_or_image_repetition_bottleneck:
  data_scene_resource_repetition:
  developer_manual_work_bottleneck:
  ai_collaboration_or_skill_bottleneck:
  platform_performance_accessibility_constraints:
  cost_and_schedule_constraints:
  rights_constraints:
  search_rings:
    - DIRECT_GENRE
    - ADJACENT_GENRE_OR_SYSTEM
    - NON_GAME_INTERACTION_OR_PRODUCT
    - TOOL_ASSET_WORKFLOW_SKILL
    - FAILURE_AND_COUNTEREXAMPLE
```

### REUSABLE_UNIT_DISCOVERY

후보 유형은 하나로 제한하지 않는다.

- `GENRE_FOUNDATION_REFERENCE`: 장르의 반복되는 최소 문법과 플레이어 기대.
- `MECHANIC_PATTERN_LIBRARY`: 입력·상태·규칙·결과·피드백 단위.
- `SYSTEM_PATTERN`: 전투·경제·진행·생성·상태 관리 등 결합 시스템.
- `CONTENT_PATTERN`: 이벤트·적·방·퀘스트·카드·스테이지 생산 문법.
- `DATA_SCHEMA_PATTERN`: 데이터 관계·상태·콘텐츠 표현 구조.
- `UI_UX_PATTERN`: 정보 우선순위·조작 흐름·피드백·오류 복구.
- `TOOL_PATTERN`: 반복 제작/검증을 줄이는 도구 입력→처리→출력 계약.
- `ASSET_MATERIAL_PATTERN`: 파츠·레이어·타일·아이콘 계열·마스크·배경 재료·구조 재료.
- `WORKFLOW_PATTERN`: 작업 순서·handoff·승인·검증·복구 구조.
- `SKILL_PATTERN`: 반복 판단 작업의 trigger·입력·정본·절차·산출물·검증 계약.

| Candidate ID | Source/Evidence | Unit type | 해결 문제 | Inputs/State | Rule/Process | Outputs/Feedback | 조절 변수 | Dependency | Rights/License | Project fit | 검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RU-001 |  | SYSTEM_PATTERN |  |  |  |  |  |  |  |  |  |

### MULTI_SOURCE_EXTRACTION

공용 패턴 승격은 가능한 경우 서로 다른 전제를 가진 3개 이상의 사례에서 불변 구조를 찾는다. 단일 작품에서만 확인되면 `SINGLE_SOURCE_HYPOTHESIS`다.

| Source | 같은 문제 | 공통 불변 구조 | 작품별 가변 요소 | 실패/한계 | 추출 Evidence |
|---|---|---|---|---|---|
| A |  |  |  |  |  |
| B |  |  |  |  |  |
| C |  |  |  |  |  |

- 공통으로 유지할 계약:
- 특정 작품에만 남길 표현:
- 일반화하면 안 되는 요소:
- 실패 조건:

### MECHANIC_PATTERN_LIBRARY

```yaml
pattern_id:
problem_or_player_need:
input:
state:
decision:
rule:
dynamics:
feedback_and_payoff:
parameters:
dependencies:
failure_and_recovery:
source_observations: []
do_not_copy: []
known_variations: []
project_fit:
validation:
```

### GENRE_FOUNDATION_REFERENCE

아래는 **탐색 seed**이지 고정 장르 목록이나 구현 명세가 아니다. 실제 프로젝트의 `PROJECT_FIT_DISCOVERY`에서 더 맞는 사례·시스템·도구·자산·작업구조를 계속 추가한다.

| 사례군 | 역공학할 공통 문법 예 | 그대로 가져오지 않을 것 | 변형 질문 |
|---|---|---|---|
| 낙하 블록 퍼즐·테트리스류 | 낙하/배치 → 공간 압박 → 선/패턴 해소 → 속도·난도 상승 → 즉시 점수/콤보 피드백 | 고유 블록 표현, 브랜드 규칙 명칭, 특정 회전/점수/시각 시그니처를 검증 없이 동일 복제 | 라인·체인·기술·잠금/진행 같은 현재 프로젝트의 의미 있는 선택과 어떻게 결합할까? |
| 텍스트 선택형 이벤트·내러티브 로그라이크·비주얼노벨 계열(서울 2033 같은 사례군) | 상태/조건 → 상황 제시 → 제한된 선택 → 즉시/지연 결과 → 상태·자원·관계 변화 → 다음 이벤트 조건 | 원문 문구, 사건, 등장인물, 세계관, 고유 선택지·UI 표현 | 같은 선택 구조로 더 강한 정보 부족·위험·기억·세계관 반응을 만들 수 있는가? |
| 덱빌딩 로그라이크·슬더슬류 | 드로우/손패/비용 → 제한된 행동 선택 → 적 의도/상태와 상호작용 → 덱 변화 → 보상 선택 → 빌드 진화 | 카드 문구·아트·수치·유물·적·맵 구성·고유 조합 | 카드가 아닌 기술·행동·부품·룬 등 다른 단위로 의사결정 문법을 옮길 수 있는가? |
| 서바이버라이크·뱀서류 | 이동/위치 선정 → 자동·간소 공격 → 시간 기반 압박/스폰 → 경험치 회수 → 레벨업 다지선다 → 빌드 시너지 | 무기·진화 조합·적·스테이지·수치·시각 효과의 고유 표현 | 조작 부담은 낮추되 위치·빌드·리스크 판단을 어떻게 프로젝트 고유 선택으로 만들까? |
| Push-your-luck | 확보한 가치 → 더 진행할 유혹 → 위험 증가 → 현금화/계속 선택 | 특정 테마·확률표·보상표 | 무엇을 잃을 위험이 플레이어에게 실제로 의미 있는가? |
| Hidden-information / Telegraph | 불완전 정보 → 예측 → 행동 선택 → 정보 갱신 → 대응 | 특정 아이콘·표시 언어 | 정보의 양과 확실성을 어떻게 조절해 공정한 긴장을 만들까? |
| Branching route / Map choice | 여러 경로 → 미래 보상·위험 추정 → 경로 선택 → 이후 선택공간 변화 | 특정 맵 형태·노드 명칭 | 경로가 단순 메뉴가 아니라 장기 전략이 되려면 무엇을 기억시켜야 하는가? |
| Modular inventory / Crafting | 모듈 획득 → 조합/배치 → 속성 상호작용 → 빌드 변화 | 아이템 세트·레시피·UI | 공간/순서/인접/재료 중 무엇이 핵심 선택인가? |
| Procedural encounter/event grammar | 조건·태그·풀 → 후보 필터 → 가중 선택 → 변형 → 결과 상태 갱신 | 사건 원문·고유 데이터 | 적은 콘텐츠로 반복감 없이 조합 가능한 최소 문법은 무엇인가? |
| Meta progression | 런 결과 → 영구 자원/해금 → 다음 런 선택공간 변화 | 해금표·경제 수치 | 실패가 단순 누적 노동이 아니라 새로운 선택을 열도록 할 수 있는가? |
| Objective/quest state machine | 조건 → 목표 상태 → 진행 이벤트 → 분기/실패/복구 → 보상/후속 상태 | 퀘스트 문구·세계관 | 서사/시스템 상태를 중복 데이터 없이 연결할 수 있는가? |
| Grid/chain/line puzzle | 공간 상태 → 패턴 생성 → 해소/연쇄 → 보드 변화 → 압박/보상 | 특정 블록·보드·점수 규칙 | 라인/체인/콤보가 서로 다른 전략 모드가 되게 할 수 있는가? |

### TOOL / ASSET / WORKFLOW / SKILL 후보

게임 규칙 밖의 생산성도 같은 방식으로 역공학한다.

| 영역 | 관찰할 것 | 추출 계약 | 승격 전 검증 |
|---|---|---|---|
| Tool | 반복 입력, 자동화 단계, 실패 복구, batch 처리 | input → transform → output → evidence/error | 대표 프로젝트 입력, 실패/복구, 반복 실행, 보안·의존성 |
| Asset/Image | 반복 파츠, 레이어, 타일, 마스크, 재질, 아이콘 계열 | source/provenance → reusable material → variant rules → use context | 권리·유사성·실사용 품질·Project Asset 승인 |
| Workflow | 단계, handoff, approval, state transition | trigger → authority → steps → handoff → verification → rollback | 실제 작업 사례에서 누락/중복/오버헤드 비교 |
| Skill | 반복 판단, source of truth, output, failure | trigger → inputs → canon → reasoning contract → output → eval | 기존 Skill/Mode와 중복 비교 + `EVAL_BEFORE_PROMOTION` |

### 재사용 모드

```yaml
reuse_mode: DIRECT_LICENSED_REUSE | ADAPT_LICENSED | PATTERN_EXTRACT | CLEAN_ROOM_REIMPLEMENTATION | REJECT
source_license:
security_or_supply_chain_review:
dependency_cost:
direct_copy_allowed:
independent_contract_written:
implementation_or_asset_owner:
```

`CLEAN_ROOM_REIMPLEMENTATION`은 직접 원본 코드·에셋·문구를 복사하지 않고 관찰 계약과 테스트에서 새 구현을 만드는 Base의 엔지니어링 격리 방식이다. 법적 면책을 뜻하지 않는다.

### NOVELTY_DELTA

```yaml
NOVELTY_DELTA:
  keep:
  remove:
  invert:
  combine:
  add:
  changed_player_decision:
  changed_feedback_or_pacing:
  changed_production_result:
  project_identity_gain:
  insufficient_if_only_skin_or_names_change: true
```

장르의 익숙한 table-stakes를 유지하는 것은 허용한다. 다만 “익숙한 기반”과 “이 프로젝트를 선택할 이유가 되는 차별점”을 구분한다.

### 승격·라우팅

- 장르/메커닉/시스템/콘텐츠/UI 패턴 → 프로젝트 기획 정본 + 검증된 Base Case 후보.
- Tool → Existing Solution First 및 실제 소비 경로 검증 뒤 기존 Tool owner.
- Asset/Image material → `PROJECT_LOCAL_ASSET_VAULT_POLICY.md`의 Harvest/명시적 승격. 발견만으로 product asset 승인이 아니다.
- Workflow/Skill → `AI_SKILL_ADOPTION_GUIDE.md`; 기존 Instruction/Template/Mode/Skill/Tool 중 최소 적절 owner에 흡수한다.
- 외부 프로세스 → `CAPABILITY_COMPOSITION_MAP.md`의 overlay 경계.
- 프로젝트 특화 결과 → Base에 억지로 일반화하지 않고 프로젝트 전용 유지.

## Evidence 체계

근거 층:

- `T1_PRIMARY_OFFICIAL`
- `T2_PROFESSIONAL_PRACTICE`
- `T3_PLAYER_BEHAVIOR`
- `T4_PLAYER_SELF_REPORT`
- `T5_SYNTHESIS`
- `T6_AI_INFERENCE`

근거 상태:

- `VERIFIED_SOURCE`
- `PARTIALLY_VERIFIED`
- `CONTEXT_LIMITED`
- `STALE_RECHECK_REQUIRED`
- `CONFLICTING_EVIDENCE`
- `UNVERIFIED`

| Evidence ID | 대상 | 원출처 | 게시일·버전 | 확인일 | 근거 층 | 근거 상태 | 확인된 사실 | 사용 한계 |
|---|---|---|---|---|---|---|---|---|
| EVD-001 |  |  |  |  |  |  |  |  |

`T6_AI_INFERENCE`는 원출처와 실제 프로젝트 증거 없이 공식 사실로 승격하지 않는다.

## 제품 사실

| 대상 | 실제 규칙·흐름 | Evidence ID | 공식 근거 | 우리와 같은 점 | 다른 점 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

제품 사실, 개발자 의도, 플레이어 반응과 분석자의 해석을 같은 칸에 합치지 않는다.

## 현업·개발자 사례

| 대상 | 해결하려던 문제 | 접근 방식 | 관찰된 결과 | 적용 조건 | 실패·비복제 요소 | Evidence ID |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 플레이어 반응 클러스터

| 클러스터 | 상황·트리거 | 긍정·부정·혼합 | 플레이어 맥락 | 빈도 신호 | 영향 | Evidence ID | 신뢰도 |
|---|---|---|---|---|---|---|---|
|  |  |  | 플랫폼·언어·플레이타임·패치 |  |  |  | HIGH/MEDIUM/LOW |

플레이어 자기보고는 실제 행동과 분리한다.

## 기대와 실제 경험

| 약속·기대 | 실제 플레이어 행동 | 플레이어 자기보고 | 일치 여부 | 원인 가설 | Evidence ID | 추가 검증 |
|---|---|---|---|---|---|---|
|  |  |  | MATCH/GAP/UNKNOWN |  |  |  |

## 행동·퍼널 근거

| 이벤트·단계 | 대상 집단 | 통과·이탈·시간 | 빌드·버전 | Evidence ID | 해석 한계 | 개선 후보 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

퍼널은 무엇이 일어났는지를 보여 주지만 감정과 원인을 자동으로 증명하지 않는다.

## 실패 사례·혼합 사례

### 실패 사례

| 대상·Case Card | 실패한 약속·흐름 | 관찰 결과 | 원인 가설 | 우리 프로젝트가 피할 요소 | 추가 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 혼합 사례

| 대상·Case Card | 잘된 부분 | 나빠진 부분 | 조건별 차이 | ADAPT 후보 | 추가 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 상충 근거

| 충돌 ID | Evidence A | Evidence B | 충돌 내용 | 조건 차이 | 현재 해석 | 추가 검증 |
|---|---|---|---|---|---|---|
| CONFLICT-001 |  |  |  |  |  |  |

신뢰 가능한 근거가 충돌하면 하나를 숨기지 않고 `CONFLICTING_EVIDENCE`로 유지한다.

## 플레이테스트·실험 계약

```yaml
hypothesis:
decision_if_supported:
decision_if_refuted:
build_and_version:
tester_segment:
prior_exposure:
recruitment_and_access:
tasks_or_play_window:
observation_points:
feedback_questions:
feedback_channel:
telemetry_events:
funnel_steps:
control_and_variants:
primary_metric:
guardrail_metrics:
accessibility_checks:
performance_budget:
success_failure_stop:
bias_and_validity_risks:
```

## 개선 판정

판정:

- `ADOPT`
- `ADAPT`
- `TEST`
- `AVOID`
- `IGNORE`
- `REFERENCE_ONLY`

| 발견 | 핵심 컨셉 정렬 | 플레이어 가치 | 제작 비용·위험 | 접근성·성능 | Evidence ID | 판정 | 변경 후보 | 검증 |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | ADOPT/ADAPT/TEST/AVOID/IGNORE/REFERENCE_ONLY |  |  |

`REFERENCE_ONLY`는 현재 적용하지 않지만 실패·반례·역사·향후 비교를 위해 보존할 때 사용한다.

## 편향·한계

- 표본 편향:
- 리뷰 폭탄·오프토픽:
- 버전·패치 차이:
- 플랫폼·지역·언어 차이:
- 플레이타임·숙련도 차이:
- 행동과 자기보고 불일치:
- 개발자·마케팅 이해관계:
- 성공 사례 선택 편향:
- 확인하지 못한 원출처:
- AI 추론·환각 위험:
- 현재 프로젝트와 다른 제작 규모:

## Case Card 연결

| Case Card | 분류 | 공용 원리 | 적용 조건 | 그대로 복제하지 않을 요소 | 프로젝트 판정 |
|---|---|---|---|---|---|
|  | SUCCESS/FAILURE/MIXED |  |  |  |  |

Case Card Template: `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`

## 최종 반영

- 유지:
- 강화:
- 수정:
- 제거:
- `ADOPT`:
- `ADAPT`:
- `TEST`:
- `AVOID`:
- `IGNORE`:
- `REFERENCE_ONLY`:
- 별도 PoC·Vertical Slice·A/B·Concept Test:
- 프로젝트 Notion·repository canonical owner 갱신:
- 실제 코드·데이터·자산 영향:
- 미검증·재검증 조건:
- Base 승격 후보:
- 프로젝트 전용 유지:
