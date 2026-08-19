# Project Reuse Opportunity Scan

## 0. Identity
```yaml
project:
baseline_commit_or_canon_revision:
scan_date:
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

## 2. Repeated cost & bottleneck map
| 병목 ID | 플레이어/제작 문제 | 반복 빈도 | 현재 비용·마찰 | 현재 우회법 | 코어 영향 | 근거 |
|---|---|---:|---|---|---|---|
| B-001 |  |  |  |  |  |  |

## 3. Candidate discovery matrix
| 후보 ID | Candidate family | 해결 대상 병목 | 참고 사례/Source | 공통 원리 | 예상 절감/가치 | 적합성 | 상태 |
|---|---|---|---|---|---|---|---|
| C-001 | Genre foundation | | | | | | DISCOVERED |
| C-002 | Mechanic / system | | | | | | DISCOVERED |
| C-003 | Content / data schema | | | | | | DISCOVERED |
| C-004 | UI / UX | | | | | | DISCOVERED |
| C-005 | Tool / automation | | | | | | DISCOVERED |
| C-006 | Asset / image material | | | | | | DISCOVERED |
| C-007 | Workflow / work structure | | | | | | DISCOVERED |
| C-008 | Skill / evaluation | | | | | | DISCOVERED |
| C-009 | Testing / QA | | | | | | DISCOVERED |

## 4. Multi-source reverse engineering
```yaml
candidate_id:
problem_solved:
source_a:
source_b:
source_c:
shared_invariant:
implementation_variants:
failure_or_mixed_cases:
signature_expression_to_exclude:
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
판정값:
- `DIRECT_LICENSED_REUSE`
- `ADAPT_LICENSED`
- `PATTERN_EXTRACT`
- `CLEAN_ROOM_REIMPLEMENTATION`
- `REJECT`

## 7. Fit / cost / risk
| 후보 | 플레이어/사용자 가치 | Core fit | 제작시간 절감 | 반복 빈도 | 통합 비용 | 유지 비용 | 권리·보안 위험 | 증거 | Rollback | 우선순위 |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |

## 8. NOVELTY_DELTA
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

## 9. Reuse owner routing
| 후보군 | 최종 owner | 필요한 검증 | 승격 상태 |
|---|---|---|---|
| 게임 규칙/시스템/콘텐츠 | 프로젝트 기획 정본 | PoC + 필요 시 Vertical Slice | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| UI / UX | UI/UX owner | 실제 해상도·입력·가독성 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Tool / automation | Tool/Existing Solution owner | 대표 입력·반복·실패복구 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Asset / image material | Asset Vault / Reusable Visual Harvest | 실제 화면·출처·권리·재사용성 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Workflow / work structure | 기존 운영 policy/reference/mode | 실제 작업 전후 비교 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Skill / evaluation | AI Skill adoption/evolution owner | positive/negative/non-route eval | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |
| Testing / QA | validation owner | 재현성·회귀·극단값 | PROJECT_ONLY / BASE_PROMOTION_CANDIDATE |

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

## 12. Decision & promotion
- `PROJECT_ONLY`:
- `BASE_PROMOTION_CANDIDATE`:
- `REJECTED`:
- 다음 검증:
- Revisit condition:
- Rollback:
