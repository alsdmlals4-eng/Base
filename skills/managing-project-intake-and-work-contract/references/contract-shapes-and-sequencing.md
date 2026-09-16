# Contract Shapes and Execution Sequencing

실제 L1+ receipt·실행 계약·세부 작업 순서를 작성하거나 검증할 때 읽는다. 단순 분류·짧은 승인안에 빈 필드 전체를 복제하지 않는다. 승인 전에는 구현 방향·의존성·검증의 개요를 제안하고, 승인 후 같은 범위의 세부 실행 순서를 확정한다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
current_confirmed_decisions:
  project_notion_exception_or_legacy_source:
project_asset_reference_benchmark_surfaces:
google_sheet_compatibility_source:
related_open_and_recent_prs:
documentation_map:
design_document_registry:
skill_registry:
current_stage_and_gate:
current_issue_or_approved_request:
actual_code_data_assets_tests:
delivery_constraints:
known_dependencies_and_blockers:
available_people_tools_permissions:
external_deliveries:
milestone_or_deadline:
validation_environment:
rollback_constraints:
approval_reference:
continuous_work_trigger:
continuation_intent:
continuous_work_state: CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE
copy_integration_standing_authorization: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
reuse_handoff:
reuse_preflight_state: NOT_RUN | COMPLETE | REUSED_EVIDENCE | NOT_APPLICABLE
reuse_preflight_evidence: []
reuse_disposition:
reuse_learning_handoff:
existing_solution_inventory:
  existing_solution_disposition:
  existing_solution_evidence:
    existing_solution_user_approval:
benchmark_preflight_receipt:
context_configuration_hygiene:
project_work_kanban:
```

Execution trust/CLI and the directly linked root receipt example remain in the parent SKILL.md; do not create a second receipt owner.

`EXTERNAL_OPERATOR_CASE_RECONSTRUCTION`: 외부 사용자의 운용 사례가 workflow/tool/Skill/evaluation/QA/content-pipeline 결정을 실제로 바꿀 때만, 그 benchmark entry에 선택적 `operator_case_reconstruction`을 붙인다. `input_anchor_and_source`, `staged_execution_and_handoffs`, `human_decision_and_approval_boundary`, `observable_outcome_and_evidence_ceiling`, `nontransferable_or_unobserved`, `project_trial_and_acceptance_gate`을 모두 기록한다. 직접 원출처·입력 anchor를 우선하고, public card·vendor report·unreadable source는 ceiling을 명시한다. 이 기록은 추가 PM board·agent·approval status가 아니며 project adoption을 자동 승인하지 않는다. 실행 관찰·failure·fallback은 `skills/optimizing-ai-model-and-prompt-costs/references/model-stack-routing.md`의 기존 `execution_strategy`로 연결한다.

### 6. Produce the executable contract

```md
# 작업 제목
## Direction Anchor
## 목적
## Work Mode
## Continuous Work State
## 맥락·정본·실제 근거
## 목표 사용자·플레이어 경험
## Reuse-First Preflight and Disposition
## Existing Solution Inventory and Disposition
## 작업 범위
## 제약·제외·보호 범위
## 자동 선택 Skill·Skill Mode
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성·롤백
## Grill Me 정합성·승인 근거
## 작업 후 Skill 실행 보고
```

### 7. Decompose and sequence

승인 계약을 활동 목록이 아니라 검증 가능한 결과 단위로 나눈다.

```yaml
step_id:
outcome:
why_now:
work_mode:
inputs:
files_or_systems:
owner_or_skill:
skill_mode:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

의존성은 `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES / OPTIONAL_FOLLOWUP`으로 구분한다.

```text
환경·권한·입력 선행 조건
→ 정본·인터페이스·Schema 계약
→ 가장 위험한 가설·기술 불확실성
→ 핵심 사용자·플레이어 경로
→ 데이터·자산·인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 사용자 체감 검수·통합·인수인계
```

순서는 의존성 해소, 위험 감소, 사용자 가치, 피드백 속도, 되돌리기 난이도, 자원 충돌로 결정한다. 일정 숫자를 근거 없이 발명하지 않는다. 병렬화는 입력·출력 경계가 고정되고 같은 파일·Schema·자산을 경쟁적으로 수정하지 않으며 독립 검증이 가능할 때만 허용한다. `CONTINUOUS_WORK_ACTIVE`에서는 이 순서에서 다음 미완료 결과를 자동 선택하되 승인 범위를 넘어 새 결과를 추가하지 않는다.

### 8. Report execution

실제로 실행한 항목마다 다음을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
trigger_and_reason:
work_performed:
result:
evidence:
status: PASS/PARTIAL/FAIL/UNVERIFIED
```

최종 사용자 보고에는 최소한 다음이 있어야 한다.

```text
사용한 Work Mode·Skill·Skill Mode
→ 사용한 이유
→ 얻은 결과·증거
```

`CONTINUOUS_WORK_ACTIVE`였다면 완료한 작업, deferred 작업, blocker recovery, 적대 검토 finding, 자동 승인해 반영한 기술 권장안, 검증 증거, 종료 상태를 최종 보고에 함께 남긴다.

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음` 중 하나로 이유를 기록한다. 모든 Registry 항목을 나열하지 않는다.

템플릿: `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## Output contract

```yaml
work_mode:
work_level:
change_types: []
primary_discipline:
affected_disciplines: []
foundation_skills: []
discipline_skills: []
deferred_skills: []
read_first: []
actual_paths: []
reuse_preflight_state: NOT_RUN | COMPLETE | REUSED_EVIDENCE | NOT_APPLICABLE
reuse_preflight_evidence: []
reuse_candidates: []
reuse_disposition:
reuse_learning_handoff:
existing_solution_inventory: []
existing_solution_disposition:
existing_solution_evidence: []
existing_solution_user_approval:
direction_anchor:
prompt_contract:
prompt_conflict_scan:
requirement_status:
approval_state:
approval_reference:
user_confirmation_ref:
continuous_work_trigger:
continuous_work_state: CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE
work_contract_path:
execution_sequence_path:
steps: []
dependencies: []
parallel_batches: []
gates: []
validation: []
skill_execution_report: []
remaining_unknowns: []
```
