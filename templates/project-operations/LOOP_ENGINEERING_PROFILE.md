# Loop Engineering Project Profile

이 Template은 Base의 `LOOP_ENGINEERING_CONTROL_PLANE`을 프로젝트에 채택할 때 **프로젝트별 값만** 선언한다. Base 공용 규칙을 복제하거나 프로젝트 정본보다 높은 권한을 만들지 않는다.

## 기본 Profile

```yaml
loop_engineering_profile:
  status: DISABLED_UNTIL_PROJECT_ADOPTION
  planning_lock_source: ""
  planning_gate_required: PLANNING_LOCKED
  default_autonomy: A2_EXECUTE_ISOLATED

  allowed_executors: []
  resource_lock_domains: []

  a3_auto_merge_allowlist: []
  a4_protected_surfaces:
    - AGENTS.md
    - security_and_secret_policy
    - permission_and_repository_governance
    - skill_registry_authority
    - loop_control_authority
    - project_core
    - player_experience_direction
    - major_ux_meaning
    - content_meaning
    - destructive_data_migration
    - release_or_paid_external_action

  budgets:
    max_agents: 2
    max_parallel_agents: 1
    max_model_calls: 24
    max_repair_cycles: 3
    max_ci_runs: 4

  required_evidence_levels:
    contract: E0_CONTRACT
    static: E1_STATIC
    automated_test: E2_TEST
    runtime_when_applicable: E3_RUNTIME
    visual_when_applicable: E4_VISUAL
    play_when_player_experience_changes: E5_PLAY
    human_playtest_when_required: E6_HUMAN_PLAYTEST

  merge_policy_reference: docs/GPT_CODEX_WORKFLOW_POLICY.md
  scheduler_runtime_provider: NOT_CONFIGURED
```

## 채택 규칙

- `PLANNING_LOCKED`는 사용자와 GPT가 전체 기획·시장/벤치마크 근거·적대적 검토·완료 기준을 닫고 사용자가 최종 검수를 완료한 범위만 뜻한다.
- `default_autonomy: A2_EXECUTE_ISOLATED`가 초기 안전 기본값이다. Agent는 격리 Branch/Worktree에서 구현·검증·PR까지 수행할 수 있지만 A3 allowlist가 없으면 자동 병합 권한을 새로 만들지 않는다.
- `a3_auto_merge_allowlist: []`는 의도적인 fail-closed 기본값이다. 프로젝트가 반복 검증된 저위험 변경 범주를 명시적으로 채택하기 전에는 비어 있어야 한다.
- `resource_lock_domains`는 파일 경로만이 아니라 save schema, combat runtime, scene, asset family 같은 의미적 소유 영역을 선언한다. 서로 다른 파일이어도 같은 의미적 자원을 변경하면 동시 writer를 허용하지 않는다.
- `a4_protected_surfaces`는 AI가 자동으로 권한을 확대하거나 제품 방향을 바꾸지 못하게 하는 프로젝트별 보호면이다. Base의 더 엄격한 권한·보안·정본 Gate를 완화할 수 없다.
- 예산은 무한 retry·agent fan-out·CI churn을 막는 상한이다. 프로젝트 특성에 맞게 더 낮게 시작하고 실제 이득이 검증된 경우에만 확대한다.
- `scheduler_runtime_provider: NOT_CONFIGURED`는 이 Template 자체가 scheduler, webhook, daemon, 24/7 runtime을 설치하지 않는다는 뜻이다. 실제 지속 실행기는 별도 Existing Solution First 조사·보안·비용·권한·복구 검증 뒤 프로젝트 Adapter로 채택한다.

## A3 Auto-Merge Allowlist 작성 기준

A3는 범주를 비워 두는 것이 기본이다. 추가하려면 다음을 모두 만족해야 한다.

```text
반복 발생
+ 결과가 deterministic 또는 강하게 검증 가능
+ 작은 blast radius
+ project core / player experience / major UX / security / permission / governance 비영향
+ rollback 용이
+ exact HEAD 및 Required Check 가능
+ 독립 검토 가능
```

예시 후보는 프로젝트가 실제로 반복 검증한 경우에만 채택한다.

```yaml
a3_auto_merge_allowlist:
  - deterministic_generated_reference_refresh
  - approved_scope_test_hardening
```

명백한 문서·generated freshness라 해도 정본 의미, 보안, 권한, 제품 방향이 바뀌면 A3가 아니다.

## 자율화 성숙 단계

프로젝트는 아래 단계를 건너뛰어 높은 자율도로 시작하지 않는다.

### `SHADOW`

- Agent가 작업 발견·분해·라우팅·예상 검증만 기록한다.
- 실제 persistent 변경은 하지 않는다.
- 사람이 선택했을 작업과 Agent 제안의 정합성을 측정한다.

### `ISOLATED_AGENT`

- `A2_EXECUTE_ISOLATED`가 기본이다.
- 승인된 Task를 격리 Branch/Worktree에서 구현·테스트·PR까지 진행한다.
- 제품/거버넌스 보호면은 그대로 사용자·기존 Gate에 남긴다.

### `MULTI_AGENT`

- 독립 Task에만 ORCHESTRATOR/SCOUT/BUILDER/VERIFIER/CRITIC 역할을 분리한다.
- `TASK_LEASE`와 `RESOURCE_LOCK` 충돌이 0임을 증명한다.
- 병렬화가 단일 Agent 대비 시간/품질/비용에서 실제 이득이 있을 때만 유지한다.

### `BOUNDED_AUTONOMOUS`

- 검증된 A3 allowlist에서만 안전 Gate 후 자동 병합을 허용한다.
- false merge, rollback, regression escape, human intervention 지표를 추적한다.

### `CONTINUOUS_OPERATIONS`

- 검증된 scheduler/runtime provider가 프로젝트별로 채택된 경우에만 이벤트·주기 실행을 연결한다.
- Base의 권한·Evidence·PR·exact-head Gate를 그대로 소비한다.

### `SELF_IMPROVEMENT`

- 실행 실패·비용·중복·회귀 데이터를 `IMPROVEMENT_CANDIDATE`로 축적한다.
- Learning은 직접 정책을 고치지 않는다. 공용 규칙은 기존 Learning/BCP/승인/구현 경계를 거친다.

## 승격·강등 Gate

다음 단계로 승격하려면 최소한 최근 실행에서 목표 drift, resource collision, 무한 retry, 검증 누락, 잘못된 자동 병합이 통제되고 생산성 또는 품질 이득이 관찰되어야 한다.

회귀·비용 폭증·중복 작업·오판 증가가 발생하면 즉시 이전의 더 낮은 단계로 rollback한다. 단계 승격은 Agent 수 증가 자체가 목적이 아니라 **검증된 업무 처리량과 품질 향상**을 목적으로 한다.
