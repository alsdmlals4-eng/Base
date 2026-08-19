# Project Reuse Opportunity Scan

이 Template은 프로젝트마다 **재사용 가능한 장르 문법·메커닉·시스템·콘텐츠/데이터 구조·UI/UX·도구·자동화·에셋/이미지 재료·작업구조·Skill/Eval·QA 패턴**을 찾고, 역공학·재사용·재구현 여부를 결정할 때 사용한다.

## 0. Scan identity

```yaml
project:
baseline_commit_or_canon_revision:
scan_date:
owner:
trigger:
status: DRAFT | IN_RESEARCH | READY_FOR_DECISION | VALIDATED | SUPERSEDED
```

## 1. Project canon first

- 핵심 플레이어 약속:
- Core Loop:
- 의미 있는 선택:
- 세계관·스토리·시각적 불변조건:
- 현재 시스템·데이터·Scene/Resource 구조:
- 현재 도구·자동화:
- 현재 Asset/Image 재사용 구조:
- 현재 작업구조·Skill/Eval:
- 플랫폼·성능·접근성:
- 일정·비용·인력 제약:
- 권리·라이선스·보안 제약:
- 현재 PoC / Vertical Slice 상태:

## 2. Repeated cost & bottleneck map

| 병목 ID | 사용자/플레이어 문제 또는 제작 문제 | 반복 빈도 | 현재 비용·마찰 | 현재 우회법 | 영향을 받는 코어 | 근거 |
|---|---|---:|---|---|---|---|
| B-001 |  |  |  |  |  |  |

## 3. Candidate discovery matrix

사용자가 예시로 든 장르에만 한정하지 않는다. 프로젝트 병목을 해결할 가능성이 있는 후보를 내부 → Base → 직접 장르 → 인접 장르 → 비게임 제품/도구 → 오픈소스/에셋 → 실패사례 순으로 넓혀 찾는다.

| 후보 ID | Candidate family | 해결 대상 병목 | 참고 사례/Source | 공통 원리 | 예상 절감/가치 | 현재 프로젝트 적합성 | 상태 |
|---|---|---|---|---|---|---|---|
| C-001 | Genre foundation |  |  |  |  |  | DISCOVERED |
| C-002 | Mechanic / system |  |  |  |  |  | DISCOVERED |
| C-003 | Content / data schema |  |  |  |  |  | DISCOVERED |
| C-004 | UI / UX |  |  |  |  |  | DISCOVERED |
| C-005 | Tool / automation |  |  |  |  |  | DISCOVERED |
| C-006 | Asset / image material |  |  |  |  |  | DISCOVERED |
| C-007 | Workflow / work structure |  |  |  |  |  | DISCOVERED |
| C-008 | Skill / evaluation |  |  |  |  |  | DISCOVERED |
| C-009 | Testing / QA |  |  |  |  |  | DISCOVERED |

## 4. Multi-source reverse engineering

일반화하는 후보는 가능한 경우 materially distinct 사례 3개 이상을 비교한다. 세 사례를 확보하지 못하면 `SINGLE_SOURCE_HYPOTHESIS`로 유지한다.

```yaml
candidate_id:
problem_solved:
source_a:
source_b:
source_c:
shared_invariant:
implementation_variants:
failure_or_mixed_cases:
what_is_signature_expression_not_pattern:
source_and_rights_notes:
```

## 5. Reusable contract

```yaml
candidate_id:
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

## 6. Existing Solution First

| 후보 | 프로젝트 내부 | Base/다른 프로젝트 검증 요소 | 공식/오픈소스/Asset 해결책 | 설정·래핑 가능 | 신규 재현 필요 | 판정 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

판정값:

- `DIRECT_LICENSED_REUSE`
- `ADAPT_LICENSED`
- `PATTERN_EXTRACT`
- `CLEAN_ROOM_REIMPLEMENTATION`
- `REJECT`

`CLEAN_ROOM_REIMPLEMENTATION`은 독립적으로 정리한 관찰 계약과 테스트에서 새 구현을 작성하는 엔지니어링 경계이며, 권리·라이선스 적합성을 자동 보장하지 않는다.

## 7. Fit / cost / risk

| 후보 | 플레이어/사용자 가치 | Core fit | 제작시간 절감 | 반복 빈도 | 통합 비용 | 유지 비용 | 권리·보안 위험 | 증거 | Rollback | 우선순위 |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |

우선순위는 유명세가 아니라 **프로젝트 가치 + 반복 절감 + 낮은 통합/권리 위험 + 검증 가능성**으로 정한다.

## 8. NOVELTY_DELTA

`PATTERN_EXTRACT` 또는 `CLEAN_ROOM_REIMPLEMENTATION` 후보마다 기록한다.

```yaml
candidate_id:
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

장르의 익숙한 table-stakes를 유지하는 경우에는 유지 이유와 프로젝트 고유 차별점을 별도로 적는다.

## 9. Reuse owner routing

| 후보 | 최종 owner | 저장 위치 | 필요한 검증 | 승격 상태 |
|---|---|---|---|---|
| 게임 규칙/시스템/콘텐츠 | 프로젝트 기획 정본 |  | PoC + 필요 시 Vertical Slice | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| UI / UX | UI/UX owner |  | 실제 해상도·입력·가독성 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Tool / automation | Tool/Existing Solution owner |  | 대표 입력·반복·실패복구 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Asset / image material | Asset Vault / Reusable Visual Harvest |  | 실제 화면·출처·권리·재사용성 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Workflow / work structure | 기존 운영 policy/reference/mode |  | 실제 작업 전후 비교 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Skill / evaluation | AI Skill adoption/evolution owner |  | positive/negative/non-route eval | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Testing / QA | 현재 validation owner |  | 재현성·회귀·극단값 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |

발견만으로 권위가 상승하지 않는다.

```text
discovery != PROJECT_ASSET_APPROVED
discovery != NEW_SKILL_APPROVED
discovery != RUNTIME_PROOF
```

## 10. Project-specific synthesis

```text
REUSABLE FOUNDATION
+ PROJECT-SPECIFIC RULES
+ PROJECT-SPECIFIC CONTENT
+ PROJECT-SPECIFIC VISUAL LANGUAGE
+ PROJECT-SPECIFIC TUNING
= IMPLEMENTATION CANDIDATE
```

- 유지할 장르/시스템 관습:
- 제거할 요소:
- 프로젝트 고유 결합:
- 플레이어 판단이 달라지는 지점:
- 제작비가 줄어드는 지점:
- 새로운 의존성/위험:

## 11. Validation contract

- 기술/규칙 PoC:
- 대표 Vertical Slice 필요 여부:
- Tool 대표 입력/실패/복구 테스트:
- Asset/Image 실제 화면 검증:
- 데이터/Schema 무결성·극단값:
- Workflow/Skill 전후 Eval:
- 권리·라이선스 확인:
- 성능·플랫폼 확인:
- 사용자/플레이어 실제 증거:
- 미검증:

## 12. Decision

| 후보 | 결정 | 이유 | 다음 행동 | Revisit condition |
|---|---|---|---|---|
|  | ADOPT / ADAPT / TEST / REJECT / DEFER |  |  |  |

## 13. Promotion

- `PROJECT_ONLY`:
- `BASE_PROMOTION_CANDIDATE`:
- `REJECTED`:
- 공용 승격에 필요한 추가 프로젝트/증거:
- 프로젝트 정본 갱신 위치:
- 롤백:
