# Behavior Eval Integrity

이 Reference는 Skill·Workflow 변경이 단순 라우팅을 넘어 **작업 정확도, 실제 수정 품질, 변경 범위 감소 또는 메커니즘 선택 개선**을 주장할 때 적용하는 선택적 functional-eval 계약이다. `skills/SKILL_BEHAVIOR_EVALS.json`의 라우팅 coverage를 대체하지 않고, 결정론적 behavioral oracle을 만들 수 있는 경우에만 추가한다.

## 적용 조건

다음 중 하나를 주장하려면 이 계약을 검토한다.

- Skill 적용으로 실제 실패를 더 자주 고친다.
- 동일한 성공률을 유지하면서 더 작은 patch·더 적은 불필요한 변경으로 해결한다.
- 특정 진단·도구·reference routing이 실제 작업 결과를 개선한다.
- 새 규칙이 관찰된 agent failure를 예방한다.

순수한 trigger/Skill-selection 정확도만 평가하는 경우 기존 behavior-eval 계약이 정본이며 이 Reference를 억지로 적용하지 않는다.

## Oracle integrity pair

functional fixture는 먼저 평가기 자체가 유효한지 증명한다.

```yaml
BROKEN_BASELINE:
  expected: FAIL_FOR_REGISTERED_REASON
REFERENCE_SOLUTION:
  expected: PASS_SAME_ORACLE
UNCHANGED_ORACLE_REQUIRED: true
```

1. `BROKEN_BASELINE`은 후보 수정 없이 의도한 불변식 때문에 실패해야 한다.
2. `REFERENCE_SOLUTION`은 알려진 올바른 최소 해법을 적용해 **같은 oracle**을 통과해야 한다.
3. reference solution을 통과시키려고 assertion, threshold, fixture, expected output을 약화하지 않는다.
4. 둘 중 하나라도 성립하지 않으면 `BLOCKED_INVALID_ORACLE`이다. 그 fixture는 Skill 효능 비교에 사용하지 않는다.

이 pair가 증명하는 것은 **fixture와 oracle이 의도한 실패/성공을 구분할 수 있다는 것**뿐이다. `FIXTURE_VALIDITY_NOT_SKILL_EFFICACY`: 이 상태만으로 agent가 Skill을 발견·적용하거나 더 좋은 결과를 만든다고 주장하지 않는다.

## Grader visibility

behavioral grader나 verifier source를 읽는 것만으로 원인 API, 필요한 flag, 정답 구조, exact repair가 노출될 수 있다면 비교 실행에서 agent workspace 밖에 둔다.

```yaml
HIDDEN_GRADER_WHEN_CAUSAL_LEAKAGE: required
visible_grader_ceiling: GRADER_VISIBLE_CEILING
```

- agent는 사용자 증상, 허용 범위, anti-cheating 제약과 필요한 실행 surface만 본다.
- root evaluator 또는 독립 runner가 agent 종료 뒤 oracle을 실행할 수 있다.
- grader를 숨길 수 없고 causal detail이 노출된다면 그 결과는 `GRADER_VISIBLE_CEILING`으로 기록한다. 블라인드 비교와 같은 강도로 취급하지 않는다.
- grader가 단순 public contract이고 정답 구현을 유출하지 않는다면 숨김 자체를 의식적으로 목표화하지 않는다. 중요한 것은 **causal leakage 여부**다.

## Same-harness comparative run

oracle이 유효해도 Skill 효능은 별도 비교가 필요하다.

```yaml
SAME_HARNESS_AB:
  candidate_arm: WITH_CANDIDATE_SKILL_OR_WORKFLOW
  baseline_arm: WITHOUT_SKILL_OR_PREVIOUS_RELEASE
  fresh_workspace_per_arm: true
  same_model_and_version: true
  same_tools_and_permissions: true
  same_fixture_and_user_task: true
  same_time_or_budget: true
  independent_oracle_execution: true
```

가능하면 중요한 실패 사례는 한 번의 운 좋은 출력으로 결론 내리지 않고 반복한다. 자동 activation을 주장하려면 Prompt에서 Skill 이름을 직접 지정하지 않은 별도 실행이 필요하다.

## Correctness와 efficiency 분리

같은 oracle PASS라도 작업 비용과 위험은 다를 수 있다. 따라서 다음을 가능한 범위에서 분리 기록한다.

```yaml
correctness:
  oracle_pass_rate:
  unsupported_completion_claims:
efficiency:
  changed_file_count:
  unnecessary_edit_count:
  references_or_context_loaded:
  extra_diagnostic_or_tool_calls:
  elapsed_or_budget_measurement:
```

`EFFICIENCY_METRICS_SEPARATE_FROM_CORRECTNESS`: 두 arm의 correctness가 같으면 correctness uplift를 주장하지 않는다. 대신 동일 성공률에서 반복적으로 patch scope, 불필요한 수정, context/tool 비용이 줄었을 때만 그 범위의 efficiency 개선으로 표현한다.

정확한 elapsed time이나 token 비용을 같은 환경에서 측정하지 못했다면 추정값을 실제 측정처럼 기록하지 않는다.

## Evidence states와 claim ceiling

```yaml
BLOCKED_INVALID_ORACLE:
  meaning: broken baseline 또는 reference solution이 unchanged oracle 계약을 충족하지 못함
VALID_ORACLE_MODEL_RUN_NOT_RUN:
  meaning: evaluator validity는 확인했지만 fresh-agent candidate-vs-baseline 비교는 미실행
GRADER_VISIBLE_CEILING:
  meaning: causal detail을 노출할 수 있는 grader를 agent가 볼 수 있어 비교 강도가 제한됨
COMPARATIVE_EVAL_COMPLETE:
  meaning: same-harness 비교와 독립 oracle 결과가 기록됨
```

- 문서·fixture·schema·reference solution 존재는 실제 모델 행동 PASS가 아니다.
- 한 model/client의 결과를 다른 client나 자동 activation 성능으로 일반화하지 않는다.
- correctness PASS는 플레이어 가치, 사람 이해도, 프로젝트 runtime 전체의 production readiness를 자동 증명하지 않는다.

## 최소 산출물

```yaml
functional_eval_artifact:
  current_failure_or_claim:
  candidate_skill_or_workflow_version:
  baseline_identity:
  model_client_version:
  tools_permissions_budget:
  fixture_identity:
  broken_baseline_result:
  reference_solution_result:
  oracle_identity_and_hash:
  oracle_unchanged: true | false
  grader_visibility: HIDDEN | VISIBLE_NONCAUSAL | VISIBLE_CAUSAL_CEILING
  repetitions:
  candidate_results:
  baseline_results:
  correctness_comparison:
  efficiency_comparison:
  unsupported_claims_observed:
  independent_evaluator:
  evidence_state:
  rollback_or_revisit_condition:
```

## 실패와 복구

- baseline이 실패하지 않으면 fixture를 더 어렵게 만드는 것이 아니라 **실패 가설이 실제로 재현되는지** 먼저 재검토한다.
- reference solution이 실패하면 solution 또는 oracle의 실제 불일치를 조사한다. oracle을 약화해 green으로 만들지 않는다.
- both arms가 모두 통과하면 더 많은 규칙을 추가해 억지 차이를 만들지 않는다. 반복적으로 관찰된 scope/context/tool-cost 차이만 최소 개선 후보로 삼는다.
- 비교 환경이 달라졌으면 모델/Skill 효과와 harness drift를 분리할 수 없으므로 재실행하거나 `PARTIALLY_VERIFIED`로 낮춘다.
- 개선이 재현되지 않으면 `REFERENCE_ONLY`, `TEST`, 프로젝트 전용 또는 rollback으로 되돌린다.
