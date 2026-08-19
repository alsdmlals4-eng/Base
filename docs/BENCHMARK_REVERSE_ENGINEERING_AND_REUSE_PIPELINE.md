# Benchmark Reverse Engineering & Reuse Pipeline

## 목적

벤치마킹을 단순 참고에서 끝내지 않고, **검증된 장르 문법·메커닉·시스템·콘텐츠 구조·데이터 구조·UI/UX·도구·자동화·에셋/이미지 재료·작업구조·Skill/Eval·QA 패턴을 재사용 가능한 계약으로 추출**해 프로젝트별 제작비와 시행착오를 줄인다.

이 문서는 외부 작품의 코드·아트·문구·고유 표현을 복제하기 위한 절차가 아니다. 관찰 가능한 문제 해결 구조를 추상화하고, 라이선스가 허용된 기존 해결책은 직접 재사용하며, 프로젝트 코어에 맞게 변형·검증하는 공용 작업구조다.

## 핵심 파이프라인

```text
PROJECT_CANON_FIRST
→ REPEATED_COST_AND_BOTTLENECK_MAP
→ PROJECT_REUSE_OPPORTUNITY_SCAN
→ SOURCE_AND_RIGHTS_PRECHECK
→ MULTI_SOURCE_REVERSE_ENGINEERING
→ REUSABLE_UNIT_DISCOVERY
→ REUSABLE_CONTRACT_EXTRACTION
→ EXISTING_SOLUTION_FIRST
→ PROJECT_FIT_DISCOVERY
→ REUSE_MODE_DECISION
→ NOVELTY_DELTA
→ REUSE_OWNER_ROUTING
→ PROJECT_SPECIFIC_SYNTHESIS
→ FIT_FOR_UNIT_VALIDATION
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

## 1. PROJECT_CANON_FIRST

사용자가 든 예시나 장르 이름부터 시작하지 않는다. 대상 프로젝트의 최신 Notion/GitHub 정본과 실제 코드·데이터·Scene·Resource·자산·테스트에서 다음을 먼저 확인한다.

- 핵심 플레이어 약속과 Core Loop.
- 의미 있는 선택과 핵심 감정.
- 세계관·스토리·시각적 불변조건.
- 현재 시스템·데이터·씬 구조.
- 현재 도구·자동화·검증 흐름.
- 반복 제작되는 UI·아트·콘텐츠·데이터.
- GPT/Codex 작업에서 반복 설명·검수되는 절차.
- 일정·인력·성능·플랫폼·비용·권리 제약.

`EXAMPLE_IS_NOT_SCOPE_LIMIT`: 테트리스류, 선택형 비주얼노벨/텍스트 로그라이크, 덱빌딩, 서바이버라이크는 탐색 seed일 뿐 고정 목록이 아니다.

## 2. PROJECT_REUSE_OPPORTUNITY_SCAN

프로젝트마다 다음 두 종류의 병목을 먼저 만든다.

### 플레이어 병목

- 반복 피로.
- 선택 의미 부족.
- 정보 과부하·가독성·입력 마찰.
- 난이도·공정성·보상·진행 문제.
- 실패 후 복구·재도전 마찰.

### 제작 병목

- 프로젝트마다 반복 구현하는 시스템.
- 반복 데이터 입력·콘텐츠 조립·밸런스 작업.
- 반복 UI 화면·아이콘·배경·타일·VFX·레이어 제작.
- 수동 변환·임포트·검수·캡처·증거 수집.
- 반복 QA·회귀·극단값 확인.
- 반복되는 작업지시·Skill·검토 구조.

각 병목에서 역으로 후보를 찾는다.

```text
프로젝트 내부 기존 요소
→ Base/다른 프로젝트에서 검증된 공용 요소
→ 직접 장르
→ 인접 장르
→ 비게임 제품·인터랙션
→ 오픈소스·Godot addon·공개 에셋
→ 제작·QA·분석 도구
→ 아트/이미지 제작 파이프라인
→ Workflow·Skill·Eval
→ 실패·혼합 사례
```

## 3. REUSABLE_UNIT_DISCOVERY

| 단위 | 추출 대상 |
|---|---|
| `GENRE_FOUNDATION_REFERENCE` | 장르에서 반복되는 최소 플레이 문법과 기대 |
| `MECHANIC_PATTERN` | 입력·상태·규칙·결과·피드백 |
| `SYSTEM_PATTERN` | 전투·경제·진행·생성·상태관리 등 복합 구조 |
| `CONTENT_PATTERN` | 이벤트·적·카드·퀘스트·스테이지 생산 문법 |
| `DATA_SCHEMA_PATTERN` | 콘텐츠·상태 관계와 데이터 경계 |
| `UI_UX_PATTERN` | 정보 우선순위·조작·피드백·오류 복구 |
| `TOOL_PATTERN` | 반복 제작·검증 비용을 줄이는 입력/처리/출력 계약 |
| `ASSET_MATERIAL_PATTERN` | 레이어·모듈 파츠·타일·아이콘군·배경재료·마스크·VFX 파츠 |
| `WORKFLOW_PATTERN` | 조사→기획→구현→검증 등의 반복 작업구조 |
| `SKILL_PATTERN` | trigger·정본·절차·산출물·검증이 반복되는 AI/사람 작업 |
| `TEST_QA_PATTERN` | seed·snapshot·golden case·stress matrix·replay 등 검증 구조 |

“유명 게임이 쓴다” 또는 “화면이 비슷하다”만으로는 재사용 단위가 아니다.

## 4. MULTI_SOURCE_REVERSE_ENGINEERING

공용 패턴으로 일반화할 때는 가능한 경우 서로 다른 구현·전제를 가진 **3개 이상의 materially distinct 사례**를 비교한다.

```yaml
problem_solved:
source_a:
source_b:
source_c:
shared_invariant:
implementation_variants:
failure_or_mixed_cases:
signature_expression_to_exclude:
```

세 사례를 확보하기 어렵다면 `SINGLE_SOURCE_HYPOTHESIS`로 유지한다. 한 작품의 고유 조합을 장르 공식처럼 승격하지 않는다.

## 5. SOURCE_AND_RIGHTS_PRECHECK

- 공개적으로 관찰 가능한 동작, 공식 문서, 개발자 발표, 합법적으로 확보한 자료를 근거로 삼는다.
- 라이선스가 허용된 코드·도구·에셋은 역공학 재구현보다 직접 재사용/래핑이 나은지 먼저 비교한다.
- 코드, 아트, 사운드, 문구, 고유 명칭, 고유 UI 표현, 고유 수치표를 권한 없이 복사하지 않는다.
- 접근통제 우회, 비공개 데이터 추출, 보안 우회는 이 파이프라인의 범위가 아니다.
- 라이선스·상표·특허·계약·플랫폼 정책 검토가 필요하면 `RIGHTS_REVIEW_REQUIRED`로 둔다.

## 6. REUSABLE_CONTRACT_EXTRACTION

후보를 작품 이름과 표현에서 분리해 다음 계약으로 적는다.

```yaml
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
```

## 7. EXISTING_SOLUTION_FIRST

재현하기 전에 다음 순서로 확인한다.

1. 프로젝트 내부에 이미 있는가.
2. Base 또는 다른 프로젝트의 검증된 공용 요소를 흡수할 수 있는가.
3. 공식/오픈소스/Asset Library에 라이선스가 명확한 해결책이 있는가.
4. 설정·래핑·부분 수정으로 해결 가능한가.
5. 그래도 부족할 때만 패턴 추출 또는 독립 재구현을 검토한다.

판정:

- `DIRECT_LICENSED_REUSE`
- `ADAPT_LICENSED`
- `PATTERN_EXTRACT`
- `CLEAN_ROOM_REIMPLEMENTATION`
- `REJECT`

`CLEAN_ROOM_REIMPLEMENTATION`은 독립적으로 정리한 관찰 계약과 테스트를 기반으로 새 구현을 작성하는 엔지니어링 경계일 뿐, 법적 면책이나 라이선스 적합성을 자동 보장하지 않는다.

## 8. PROJECT_FIT_DISCOVERY

후보는 다음 기준으로 평가한다.

- 플레이어/사용자 가치.
- Core Loop와 의미 있는 선택 적합성.
- 세계관·스토리·시각언어 적합성.
- 제작시간 절감과 반복 빈도.
- 통합·유지 비용.
- 성능·플랫폼·접근성 적합성.
- 권리·라이선스·보안 위험.
- 증거 강도와 검증 가능성.
- Rollback 난이도.

인기가 높아도 프로젝트 코어를 약하게 만들면 제외한다.

## 9. NOVELTY_DELTA

`PATTERN_EXTRACT`와 `CLEAN_ROOM_REIMPLEMENTATION`은 다음을 기록한다.

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
```

스킨·명칭·색만 바뀌고 판단이나 제작 계약이 사실상 같다면 재가공이 부족한지 재검토한다. 반대로 장르 table-stakes를 의도적으로 유지하면 익숙함을 유지할 이유와 프로젝트 고유 차별점을 분리한다.

## 10. REUSE_OWNER_ROUTING

이 파이프라인은 발굴·추상화·라우팅 owner다. 최종 권위는 기존 owner에 둔다.

- 게임 규칙·시스템·콘텐츠 → 프로젝트 기획 정본.
- UI/UX → UI/UX 설계 owner와 실제 화면/입력 검증.
- Tool/addon → Existing Solution First와 도구/Godot addon 평가 owner.
- Asset/Image material → Asset Vault / Reusable Visual Harvest.
- Workflow → 기존 운영 policy/reference/mode에 우선 흡수.
- Skill/Eval → 기존 Skill adoption/evolution owner.
- Testing/QA → 기존 validation owner.

```text
discovery != PROJECT_ASSET_APPROVED
discovery != NEW_SKILL_APPROVED
discovery != RUNTIME_PROOF
discovery != RIGHTS_CLEARANCE
```

## 11. PROJECT_SPECIFIC_SYNTHESIS

```text
REUSABLE FOUNDATION
+ PROJECT-SPECIFIC RULES
+ PROJECT-SPECIFIC CONTENT
+ PROJECT-SPECIFIC VISUAL LANGUAGE
+ PROJECT-SPECIFIC TUNING
= IMPLEMENTATION CANDIDATE
```

목표는 벤치마크를 닮는 것이 아니라 **프로젝트 코어를 더 적은 비용으로 구현하면서 고유 경험을 강화하는 것**이다.

## 12. 단위별 검증

- 장르·메커닉·시스템·콘텐츠: PoC는 규칙/기술 증거. 플레이 경험은 대표 UI/UX·아트·콘텐츠가 있는 Vertical Slice와 실제 플레이 증거가 필요하다.
- 데이터 구조: 샘플·직렬화·무결성·극단값·마이그레이션 검증.
- UI/UX: 실제 해상도·입력·오류복구·가독성 검증.
- Tool: 대표 입력·반복 실행·실패/복구·성능·의존성·보안 검증.
- Asset/Image material: 실제 화면 품질·출처·권리·유사성·재사용성 검토.
- Workflow/Skill: 정상 사례뿐 아니라 실패·비선택·오라우팅 사례의 전후 Eval.

유명 작품의 성공 자체는 현재 프로젝트에서의 PASS가 아니다.

## 13. 저장과 승격

실제 프로젝트 스캔 결과는 각 프로젝트 정본에 둔다.

- `PROJECT_ONLY`: 해당 프로젝트에서만 유효하거나 1회 검증.
- `BASE_PROMOTION_CANDIDATE`: 서로 다른 프로젝트에서 반복 가치가 확인됨.
- `REJECTED`: 권리·비용·품질·적합성·유지보수 문제로 탈락.

공용 승격은 반복 소비자와 검증 증거가 생겼을 때만 한다.

## 실행 산출물

프로젝트별 스캔은 `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`를 사용한다. 게임 기획 벤치마킹에서 상세 후보를 발굴할 때는 `skills/analyzing-and-refining-game-concepts/references/reverse-engineering-reuse-pipeline.md`를 함께 사용한다.
