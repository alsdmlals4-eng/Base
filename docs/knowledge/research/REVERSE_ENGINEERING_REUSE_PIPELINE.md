# Reverse Engineering & Reuse Pipeline

이 Reference는 벤치마킹 작업에서 **장르·메커닉뿐 아니라 시스템, 콘텐츠 구조, 데이터 구조, UI/UX, 도구, 자동화, 에셋·이미지 재료, 작업구조, Skill/Eval, QA 패턴까지 재사용 후보를 능동적으로 발굴**할 때 사용한다.

상위 원칙은 `docs/BENCHMARKING_REFERENCE_GUIDE.md`의 `BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE`를 따른다. 실행 기록은 `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`를 사용한다. 새 후보를 추출하기 전에 `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`에서 이미 정의된 공용/프로젝트-seed 모듈을 먼저 확인하고, 같은 문제를 해결하는 계약이 있으면 새 모듈보다 재사용·변형·project adapter를 우선한다.

Context에서 아직 존재하지 않는 공용 구조를 설계하는 두 번째 origin 경로는 `docs/knowledge/research/CONTEXT_DRIVEN_REUSE_SYNTHESIS.md`가 정의한다.

## 핵심 계약

`PROJECT_REUSE_OPPORTUNITY_SCAN`은 사용자가 이미 알고 있는 예시 목록을 확장하는 절차가 아니다. **대상 프로젝트의 최신 정본과 실제 병목·roadmap·책임 구조를 먼저 읽고, 증거에서 패턴을 추출하거나 아직 없는 더 나은 구조를 context hypothesis로 설계하는 절차**다.

```text
PROJECT_CANON_FIRST
→ CORE_EXPERIENCE_AND_CONSTRAINT_MAP
→ REPEATED_COST_AND_BOTTLENECK_MAP
→ CANDIDATE_ORIGIN_GATE
   ├─ EVIDENCE_DERIVED
   │  → BOTTLENECK_TO_CANDIDATE_SEARCH
   │  → CREATIVE_BENCHMARK_FRONTIER
   │  → SOURCE_AND_RIGHTS_PRECHECK
   │  → MULTI_SOURCE_REVERSE_ENGINEERING
   └─ CONTEXT_SYNTHESIZED
      → CONTEXT_DRIVEN_REUSE_SYNTHESIS
      → FALSIFICATION_AND_SMALLEST_PILOT
   EVIDENCE_DERIVED + CONTEXT_SYNTHESIZED → HYBRID
→ REUSABLE_CONTRACT_EXTRACTION
→ EXISTING_SOLUTION_FIRST
→ PROJECT_FIT_AND_NOVELTY_DELTA
→ ORIGINALITY_FUN_CREATIVITY_REVIEW
→ REUSE_OWNER_ROUTING
→ PROJECT_SPECIFIC_SYNTHESIS
→ FIT_FOR_UNIT_VALIDATION
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

```text
SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS
CONTEXT_SYNTHESIS_IS_NOT_VALIDATION
EVIDENCE_REQUIRED_FOR_PROMOTION
```

외부 Source나 반복 구현 기록이 없어도 context candidate를 `HYPOTHESIS` 또는 `MODULE_CONTRACT_DEFINED`로 설계할 수 있다. 반대로 context 추론만으로 reference implementation, project adoption, runtime proof, player value를 주장할 수 없다.

`EXAMPLE_IS_NOT_SCOPE_LIMIT`: 테트리스류, 선택형 비주얼노벨/텍스트 로그라이크, 덱빌딩, 서바이버라이크 등 사용자가 직접 든 사례는 **탐색 seed**일 뿐 고정 범위가 아니다. 프로젝트의 실제 문제와 제작 비용을 더 잘 줄이는 후보가 있으면 다른 장르·제품·툴·오픈소스·에셋·제작 파이프라인·QA 방식까지 조사한다.

## 1. PROJECT_CANON_FIRST

역공학 또는 Context-Synthesis 후보를 찾기 전에 다음을 최신 프로젝트 정본과 실제 코드·데이터·Scene·Resource·자산·테스트·승인 roadmap에서 확인한다.

```yaml
project:
core_player_promise:
core_loop:
meaningful_choices:
world_story_visual_invariants:
current_systems:
current_tools_and_automation:
current_asset_reuse_structure:
current_workflow_and_skill_routes:
planned_consumers:
production_capacity:
platform_and_performance_constraints:
rights_cost_security_constraints:
current_poc_or_vertical_slice_state:
```

프로젝트 정본을 읽지 않고 “이 장르면 보통 이것을 쓴다”는 이유만으로 후보를 밀어 넣지 않는다.

## 2. 반복 비용·병목 지도

`REPEATED_COST_AND_BOTTLENECK_MAP`은 플레이어 문제와 제작 문제를 구분한다. 실제 반복 기록뿐 아니라 승인된 roadmap에서 구조적으로 반복이 예정되는 비용도 구분해서 기록할 수 있다.

### 플레이어 측

- 반복적으로 지루해지는 구간.
- 선택의 의미가 약한 구간.
- 정보 과부하·가독성·입력 마찰.
- 보상·진행·난이도·공정성 문제.
- 실패 후 복구와 재도전 마찰.
- 장르 기대는 있으나 프로젝트 고유 경험과 충돌하는 부분.

### 제작 측

- 프로젝트마다 다시 만드는 동일/유사 시스템.
- 반복 데이터 입력·콘텐츠 조립·밸런스 작업.
- 반복 UI 화면·아이콘·배경·VFX·타일·레이어 제작.
- 수동 변환·임포트·검수·캡처·증거 수집.
- 반복되는 버그 탐색·QA·회귀 테스트.
- GPT/Codex에 매번 다시 설명하는 작업 규칙·검토 방식.
- 같은 판단을 여러 문서/도구에서 반복하는 중복 작업.
- 아직 반복되지 않았지만 실제 planned consumers 때문에 곧 같은 작업이 반복될 구조.

## 3. CANDIDATE_ORIGIN_GATE

각 후보는 먼저 origin을 명시한다.

```yaml
candidate_origin: EVIDENCE_DERIVED | CONTEXT_SYNTHESIZED | HYBRID
```

### `EVIDENCE_DERIVED`

실제 구현·반복 병목·benchmark·실패·운영 기록에서 공통 불변원리를 추출한다. 이 경로는 아래 `BOTTLENECK_TO_CANDIDATE_SEARCH`와 `MULTI_SOURCE_REVERSE_ENGINEERING`을 사용한다.

### `CONTEXT_SYNTHESIZED`

아직 반복 evidence가 없어도 실제 project canon, 승인 roadmap, planned consumer, 책임 결합, 예상 반복비용을 근거로 새 bounded contract를 설계한다. 세부 trigger, `falsification_test`, `smallest_pilot`, rollback 규칙은 `CONTEXT_DRIVEN_REUSE_SYNTHESIS.md`를 따른다.

### `HYBRID`

Context hypothesis를 외부/내부 evidence로 공격하거나, evidence-derived pattern을 현재 project 구조와 새로 재조합할 때 사용한다.

origin은 validation state가 아니다. `CONTEXT_SYNTHESIZED` 또는 `HYBRID`라고 해서 증거 수준이 자동 상승하지 않는다.

## 4. BOTTLENECK_TO_CANDIDATE_SEARCH

Evidence-derived 병목마다 후보 검색 범위를 단계적으로 확장한다.

```text
A. 프로젝트 내부 기존 구현·자산·도구
B. Base와 다른 사용자 프로젝트의 검증된 공용 후보
C. 직접 장르의 반복 문법
D. 인접 장르의 동일 문제 해결 방식
E. 비게임 제품·인터랙션·생산 도구
F. 오픈소스 / Godot addon / 공개 데이터·에셋
G. 아트·이미지의 모듈 재료와 제작 파이프라인
H. QA·테스트·관찰·분석 도구와 실무 프로세스
I. AI 작업구조·Skill·Eval 패턴
J. 실패·혼합 사례와 폐기된 접근
```

후보는 유명세보다 **현재 병목을 얼마나 줄이는지**로 평가한다.

## 5. `CREATIVE_BENCHMARK_FRONTIER`

중요한 게임 기획은 직접 장르의 대표작만 보면 동질화 위험이 커진다. 같은 문제를 서로 다르게 푸는 다음 다섯 집합을 결정 직전까지 탐색한다.

```text
DIRECT_GENRE_BEST_IN_CLASS
ADJACENT_GENRE_BEST_IN_CLASS
DISTINCTIVE_OR_INNOVATIVE_WORK
FAILURE_OR_MIXED_CASE
PROJECT_INTERNAL_STRENGTH
```

```yaml
creative_frontier:
  player_promise:
  design_question:
  direct_genre_best_in_class: []
  adjacent_genre_best_in_class: []
  distinctive_or_innovative_work: []
  failure_or_mixed_case: []
  project_internal_strength: []
  transferable_principles: []
  expressions_not_to_copy: []
  recombination_candidates: []
```

최고의 작품은 단순 판매량 순위가 아니라 **현재 설계 질문에서 무엇을 가장 잘 해결하는지**로 선정한다. 하나의 작품을 통째로 모사하지 않고, 여러 사례의 장점·실패조건을 분리해 프로젝트 고유 조합으로 재설계한다.

시장 성과·리뷰·수상·다운로드 수는 discovery 신호일 수 있지만, 현재 프로젝트의 재미·시장성·기술 적합성을 자동 증명하지 않는다.

## 6. 재사용 후보 분류

한 사례 또는 context packet에서 여러 종류를 동시에 추출할 수 있다.

| Candidate family | 추출 대상 | 예시 |
|---|---|---|
| Genre foundation | 익숙한 최소 장르 문법 | 낙하 블록, 선택형 사건 진행, 덱 순환, 자동공격+성장 선택 |
| Mechanic / system | 입력·상태·규칙·결과 | 콤보, 상태효과, 어그로, 드래프트, 리롤, 위험/보상 |
| Content / data schema | 콘텐츠 생성·표현 구조 | 이벤트 노드, 카드 정의, 적 역할, loot table, encounter budget |
| UI / UX | 정보·입력·피드백 패턴 | telegraph, compare view, lock/continue, preview, undo/recovery |
| Tool / automation | 반복 작업 절감 계약 | 에셋 전처리, 콘텐츠 검증, 밸런스 시뮬레이션, repository-native evidence capture |
| Asset / image material | 분해·재조합 가능한 시각 재료 | 타일, 프레임, 아이콘군, 실루엣, 배경 모듈, 마스크, VFX 파츠 |
| Workflow / work structure | 생산·handoff 절차 | research→spec→slice→evidence, batch review, content assembly |
| Skill / evaluation | 반복 판단·검수 계약 | trigger, inputs, canon, output, negative case, regression eval |
| Testing / QA | 실패 탐지·재현 패턴 | deterministic seed, snapshot, golden case, stress matrix, replay |

## 7. MULTI_SOURCE_REVERSE_ENGINEERING

외부 사례의 반복 불변원리를 주장하는 후보는 가능한 경우 서로 다른 구현·전제를 가진 3개 이상의 사례를 비교한다.

```yaml
candidate_id:
problem_solved:
source_a:
source_b:
source_c:
shared_invariant:
implementation_variants:
failure_cases:
project_relevant_constraints:
```

단일 작품의 고유 조합을 그대로 “장르 공식”으로 승격하지 않는다. 반복되는 불변 원리와 작품별 표현을 분리한다.

Pure `CONTEXT_SYNTHESIZED` hypothesis에는 Source 3개가 선행 조건이 아니다. 대신 `context_basis`, 실명 가능한 `planned_consumers`, `falsification_test`, `smallest_pilot`이 필수다. 이후 external invariant를 주장하려면 그 시점부터 evidence 경계를 적용한다.

## 8. REUSABLE_CONTRACT_EXTRACTION

재사용 후보는 최소 다음 계약으로 추상화한다.

```yaml
candidate_origin:
context_basis:
planned_consumers: []
unit_type:
problem_or_player_need:
production_problem:
inputs:
state:
rules_or_process:
outputs:
feedback:
tunable_parameters:
dependencies:
failure_and_recovery:
content_or_asset_interfaces:
test_or_validation_interface:
source_observations:
rights_and_license_boundary:
falsification_test:
smallest_pilot:
rollback_or_discard_condition:
maturity:
validation_state:
```

도구·Workflow·Skill 후보는 `player_need` 대신 `production_problem`을 중심으로 써도 된다. Evidence-derived 후보는 context-only 필드를 `not_applicable`로 명시할 수 있지만, 현재 project fit과 consumer는 항상 기록한다.

## 9. EXISTING_SOLUTION_FIRST

새로 재현하기 전에 다음을 비교한다.

1. 프로젝트 내부에 이미 있는가.
2. Base 또는 다른 프로젝트에서 검증된 공용 요소를 흡수할 수 있는가.
3. 공식/오픈소스/에셋 라이브러리에 라이선스가 명확한 해결책이 있는가.
4. 설정·래핑·부분 수정으로 해결 가능한가.
5. 여러 기존 모듈의 composition으로 해결 가능한가.
6. 그래도 충족되지 않을 때만 새 `PATTERN_EXTRACT`, bounded reference implementation 또는 `CLEAN_ROOM_REIMPLEMENTATION`을 검토한다.

재사용 모드:

- `DIRECT_LICENSED_REUSE`
- `ADAPT_LICENSED`
- `PATTERN_EXTRACT`
- `CLEAN_ROOM_REIMPLEMENTATION`
- `REJECT`

직접 재사용 가능한 검증된 해결책을 불필요하게 역공학해서 다시 만드는 것은 작업 절감 목표와 충돌한다. Context-Synthesis도 새 구조를 발명했다는 이유만으로 Existing Solution First를 건너뛰지 않는다.

## 10. PROJECT_FIT_AND_NOVELTY_DELTA

다음 축으로 후보를 공격한다.

```yaml
player_or_user_value:
core_loop_fit:
world_story_visual_fit:
production_time_saved:
repeat_frequency:
integration_cost:
maintenance_cost:
performance_and_platform_fit:
rights_license_security_risk:
evidence_strength:
rollback_difficulty:
```

`NOVELTY_DELTA`:

```yaml
keep:
remove:
invert:
combine:
add:
changed_player_decision:
changed_feedback_or_pacing:
changed_production_result:
project_identity_gain:
```

장르 table-stakes를 의도적으로 유지하는 경우에도 프로젝트의 고유 선택·감정·피드백·세계관·시각 언어 중 무엇이 달라지는지 기록한다.

## 11. `ORIGINALITY_FUN_CREATIVITY_REVIEW`

재조합 후보는 실제 구현 전에 다음으로 다시 본다.

```yaml
originality_fun_creativity:
  originality_delta:
  fun_hypothesis:
  creativity_recombination:
  familiar_anchor:
  meaningful_choice:
  tension_or_tradeoff:
  feedback_and_pacing:
  world_story_fit:
  visual_identity_fit:
  avoid_gimmick_complexity:
  player_evidence_status:
```

`fun_hypothesis`는 “재밌어 보인다”가 아니라 **무슨 행동·선택·위험·보상·피드백 때문에 어떤 감정/고민이 생길 것인지**를 적는다.

```text
PLAYER_EVIDENCE_REQUIRED_FOR_FUN_PASS
```

실제 사람 플레이 증거 전에는 `FUN_HYPOTHESIS` 이상의 상태로 올리지 않는다. 독창성도 새 요소 개수로 평가하지 않고 familiar anchor와 project-specific recombination이 학습비용 대비 새로운 플레이 의미를 만드는지 본다.

## 12. REUSE_OWNER_ROUTING

이 Reference는 후보를 **발굴하고 추상화하는 owner**다. 최종 권위는 기존 owner에 넘긴다.

- 게임 규칙·시스템·콘텐츠 → 프로젝트 기획 정본과 해당 설계 Skill.
- UI/UX → 현재 UI/UX 설계 owner와 실제 화면/입력 검증.
- Asset/Image material → Project Notion Asset/Visual workflow + repository implementation owner.
- Tool/addon → Existing Solution First, 도구 계약, Godot addon/plugin 평가 owner.
- Workflow → 기존 Base 운영 정책·reference·Mode에 먼저 흡수.
- Skill/Eval → `AI_SKILL_ADOPTION_GUIDE.md`의 재사용·흡수·평가 절차.
- 프로젝트 고유 후보 → 프로젝트에만 저장.
- 여러 프로젝트에서 반복 검증된 일반 원리 → `BASE_PROMOTION_CANDIDATE`.

권위 경계:

```text
discovery != PROJECT_ASSET_APPROVED
discovery != NEW_SKILL_APPROVED
discovery != RUNTIME_PROOF
discovery != COPYRIGHT_OR_LICENSE_CLEARANCE
context synthesis != validation
```

## 13. PROJECT_SPECIFIC_SYNTHESIS

최종 목표는 벤치마크를 닮는 것이 아니라 **프로젝트 코어를 더 싸고 빠르게 구현하면서 고유 경험을 강화하는 것**이다.

```text
reusable foundation
+ project-specific rules
+ project-specific content
+ project-specific visual language
+ project-specific tuning
+ evidence-derived learning
+ context-driven invention
= project implementation candidate
```

재사용 foundation이 프로젝트 코어보다 커지면 기각한다.

## 14. 검증 증거 ceiling

- 규칙·시스템 PoC는 구현 가능성과 규칙 동작을 증명하지만 재미·몰입을 자동 증명하지 않는다.
- `VERTICAL_SLICE_EVIDENCE_CEILING`: 플레이어 경험을 주장하려면 실제 UI/UX·아트·대표 콘텐츠가 포함된 release-near Vertical Slice와 플레이 증거가 필요하다.
- Tool은 실제 대표 입력, 반복 실행, 실패·복구, 성능·의존성 검증이 필요하다.
- Asset/Image material은 실제 화면에서의 가독성·일관성·재사용성·출처·권리 검토가 필요하다.
- Workflow/Skill은 대표 성공 사례뿐 아니라 실패·비선택·오라우팅 사례를 포함한 전후 Eval이 필요하다.
- benchmark가 강해도 실제 project fit·runtime·player evidence를 대신하지 않는다.
- Context-Synthesized 후보는 실제 `smallest_pilot`을 통과하기 전 `VALIDATION_NOT_RUN` 또는 직접 실행된 좁은 검증 수준 이상으로 올라가지 않는다.

## 15. 프로젝트별 결과 저장

Base에는 공용 방법만 둔다. 실제 프로젝트 스캔 결과는 각 프로젝트의 Notion/GitHub 정본에 둔다.

- `PROJECT_ONLY`: 해당 프로젝트에서만 유효하거나 아직 1회 검증.
- `BASE_PROMOTION_CANDIDATE`: 서로 다른 프로젝트에서 반복 가치가 확인되어 공용화 검토 가치가 있음.
- `REJECTED`: 권리·비용·품질·적합성·유지보수 문제로 탈락.

공용 승격은 “좋아 보임” 또는 “구조적으로 그럴듯함”이 아니라 실제 consumer와 검증 증거가 생겼을 때만 한다.
