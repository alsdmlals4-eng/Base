# Reverse Engineering & Reuse Pipeline

이 Reference는 `analyzing-and-refining-game-concepts`의 벤치마킹 작업에서 **장르·메커닉뿐 아니라 시스템, 콘텐츠 구조, 데이터 구조, UI/UX, 도구, 자동화, 에셋·이미지 재료, 작업구조, Skill/Eval, QA 패턴까지 재사용 후보를 능동적으로 발굴**할 때 사용한다.

상위 원칙은 `docs/BENCHMARKING_REFERENCE_GUIDE.md`의 `BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE`를 따른다.

## 핵심 계약

`PROJECT_REUSE_OPPORTUNITY_SCAN`은 사용자가 이미 알고 있는 예시 목록을 확장하는 절차가 아니다. **대상 프로젝트의 최신 정본과 실제 병목을 먼저 읽고, 그 문제를 해결할 재사용 후보를 외부 사례와 기존 내부 자산에서 역으로 찾는 절차**다.

```text
PROJECT_CANON_FIRST
→ CORE_EXPERIENCE_AND_CONSTRAINT_MAP
→ REPEATED_COST_AND_BOTTLENECK_MAP
→ BOTTLENECK_TO_CANDIDATE_SEARCH
→ SOURCE_AND_RIGHTS_PRECHECK
→ MULTI_SOURCE_REVERSE_ENGINEERING
→ REUSABLE_CONTRACT_EXTRACTION
→ EXISTING_SOLUTION_FIRST
→ PROJECT_FIT_AND_NOVELTY_DELTA
→ REUSE_OWNER_ROUTING
→ PROJECT_SPECIFIC_SYNTHESIS
→ FIT_FOR_UNIT_VALIDATION
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

`EXAMPLE_IS_NOT_SCOPE_LIMIT`: 테트리스류, 선택형 비주얼노벨/텍스트 로그라이크, 덱빌딩, 서바이버라이크 등 사용자가 직접 든 사례는 **탐색 seed**일 뿐 고정 범위가 아니다. 프로젝트의 실제 문제와 제작 비용을 더 잘 줄이는 후보가 있으면 다른 장르·제품·툴·오픈소스·에셋·제작 파이프라인·QA 방식까지 조사한다.

## 1. PROJECT_CANON_FIRST

역공학 후보를 찾기 전에 다음을 최신 프로젝트 정본과 실제 코드·데이터·Scene·Resource·자산·테스트에서 확인한다.

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
production_capacity:
platform_and_performance_constraints:
rights_cost_security_constraints:
current_poc_or_vertical_slice_state:
```

프로젝트 정본을 읽지 않고 “이 장르면 보통 이것을 쓴다”는 이유만으로 후보를 밀어 넣지 않는다.

## 2. 반복 비용·병목 지도

`REPEATED_COST_AND_BOTTLENECK_MAP`은 플레이어 문제와 제작 문제를 구분한다.

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

## 3. BOTTLENECK_TO_CANDIDATE_SEARCH

병목마다 후보 검색 범위를 단계적으로 확장한다.

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

## 4. 재사용 후보 분류

한 사례에서 여러 종류를 동시에 추출할 수 있다.

| Candidate family | 추출 대상 | 예시 |
|---|---|---|
| Genre foundation | 익숙한 최소 장르 문법 | 낙하 블록, 선택형 사건 진행, 덱 순환, 자동공격+성장 선택 |
| Mechanic / system | 입력·상태·규칙·결과 | 콤보, 상태효과, 어그로, 드래프트, 리롤, 위험/보상 |
| Content / data schema | 콘텐츠 생성·표현 구조 | 이벤트 노드, 카드 정의, 적 역할, loot table, encounter budget |
| UI / UX | 정보·입력·피드백 패턴 | telegraph, compare view, lock/continue, preview, undo/recovery |
| Tool / automation | 반복 작업 절감 계약 | 에셋 전처리, 콘텐츠 검증, 밸런스 시뮬레이션, 증거 캡처 |
| Asset / image material | 분해·재조합 가능한 시각 재료 | 타일, 프레임, 아이콘군, 실루엣, 배경 모듈, 마스크, VFX 파츠 |
| Workflow / work structure | 생산·handoff 절차 | research→spec→slice→evidence, batch review, content assembly |
| Skill / evaluation | 반복 판단·검수 계약 | trigger, inputs, canon, output, negative case, regression eval |
| Testing / QA | 실패 탐지·재현 패턴 | deterministic seed, snapshot, golden case, stress matrix, replay |

## 5. MULTI_SOURCE_REVERSE_ENGINEERING

일반화할 후보는 가능한 경우 서로 다른 구현·전제를 가진 3개 이상의 사례를 비교한다.

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

## 6. REUSABLE_CONTRACT_EXTRACTION

재사용 후보는 최소 다음 계약으로 추상화한다.

```yaml
unit_type:
problem_or_player_need:
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
```

도구·Workflow·Skill 후보는 `player_need` 대신 `production_problem`을 중심으로 써도 된다.

## 7. EXISTING_SOLUTION_FIRST

새로 재현하기 전에 다음을 비교한다.

1. 프로젝트 내부에 이미 있는가.
2. Base 또는 다른 프로젝트에서 검증된 공용 요소를 흡수할 수 있는가.
3. 공식/오픈소스/에셋 라이브러리에 라이선스가 명확한 해결책이 있는가.
4. 설정·래핑·부분 수정으로 해결 가능한가.
5. 그래도 충족되지 않을 때만 `PATTERN_EXTRACT` 또는 `CLEAN_ROOM_REIMPLEMENTATION`을 검토한다.

재사용 모드:

- `DIRECT_LICENSED_REUSE`
- `ADAPT_LICENSED`
- `PATTERN_EXTRACT`
- `CLEAN_ROOM_REIMPLEMENTATION`
- `REJECT`

직접 재사용 가능한 검증된 해결책을 불필요하게 역공학해서 다시 만드는 것은 작업 절감 목표와 충돌한다.

## 8. PROJECT_FIT_AND_NOVELTY_DELTA

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

## 9. REUSE_OWNER_ROUTING

이 Reference는 후보를 **발굴하고 추상화하는 owner**다. 최종 권위는 기존 owner에 넘긴다.

- 게임 규칙·시스템·콘텐츠 → 프로젝트 기획 정본과 해당 설계 Skill.
- UI/UX → 현재 UI/UX 설계 owner와 실제 화면/입력 검증.
- Asset/Image material → 프로젝트 Asset Vault / Reusable Visual Harvest owner.
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
```

## 10. PROJECT_SPECIFIC_SYNTHESIS

최종 목표는 벤치마크를 닮는 것이 아니라 **프로젝트 코어를 더 싸고 빠르게 구현하면서 고유 경험을 강화하는 것**이다.

```text
reusable foundation
+ project-specific rules
+ project-specific content
+ project-specific visual language
+ project-specific tuning
= project implementation candidate
```

재사용 foundation이 프로젝트 코어보다 커지면 기각한다.

## 11. 검증 증거 ceiling

- 규칙·시스템 PoC는 구현 가능성과 규칙 동작을 증명하지만 재미·몰입을 자동 증명하지 않는다.
- `VERTICAL_SLICE_EVIDENCE_CEILING`: 플레이어 경험을 주장하려면 실제 UI/UX·아트·대표 콘텐츠가 포함된 release-near Vertical Slice와 플레이 증거가 필요하다.
- Tool은 실제 대표 입력, 반복 실행, 실패·복구, 성능·의존성 검증이 필요하다.
- Asset/Image material은 실제 화면에서의 가독성·일관성·재사용성·출처·권리 검토가 필요하다.
- Workflow/Skill은 대표 성공 사례뿐 아니라 실패·비선택·오라우팅 사례를 포함한 전후 Eval이 필요하다.

## 12. 프로젝트별 결과 저장

Base에는 공용 방법만 둔다. 실제 프로젝트 스캔 결과는 각 프로젝트의 Notion/GitHub 정본에 둔다.

- `PROJECT_ONLY`: 해당 프로젝트에서만 유효하거나 아직 1회 검증.
- `BASE_PROMOTION_CANDIDATE`: 서로 다른 프로젝트에서 반복 가치가 확인되어 공용화 검토 가치가 있음.
- `REJECTED`: 권리·비용·품질·적합성·유지보수 문제로 탈락.

공용 승격은 “좋아 보임”이 아니라 반복 소비자와 검증 증거가 생겼을 때만 한다.
