# GAME_BACKEND_SERVICE_CONTRACT

- Capability Pack: `GAME_BACKEND_CLOUD_RUN`
- Project-owned artifact: yes
- Base Guide: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
- Current state: `CANDIDATE`
- Static document evidence must not be promoted to runtime or production evidence.

## Lifecycle

```text
NOT_REQUIRED
→ CANDIDATE
→ SELECTED
→ CONFIGURED
→ STATIC_VERIFIED
→ RUNTIME_VERIFIED
→ LOAD_AND_FAILURE_VERIFIED
→ PRODUCTION_READY
```

단계를 건너뛰지 않는다. 미실행 증거는 `NOT_RUN`으로 남긴다.
`PRODUCTION_READY`는 프로젝트별 배포·런타임·부하·실패·비용·보안 증거가 있을 때만 선언한다.

## Player value and server feature

```yaml
project:
decision_id:
player_value:
server_feature:
critical_play_flow:
server_required_reason:
server_not_required_alternative:
current_state: CANDIDATE
owner:
```

## Fit decision and rejected alternatives

```yaml
decision: CLOUD_RUN_RECOMMENDED | CLOUD_RUN_CONDITIONAL | ALTERNATIVE_ARCHITECTURE_REQUIRED | SERVER_NOT_REQUIRED | BLOCKED_UNVERIFIED
latency_and_tick_requirement:
connection_model:
expected_traffic_and_burst:
selected_architecture:
rejected_alternatives:
rejection_reasons:
assumptions:
review_date:
```

## Authority and persistent state

```yaml
authoritative_state:
client_claims:
request_scoped_state:
durable_player_state:
external_persistent_datastore:
cache:
instance_local_state_policy: NON_AUTHORITATIVE
filesystem_policy: EPHEMERAL_ONLY
```

## API and request lifecycle

```yaml
operation_id:
actor_identity:
authorization_scope:
request_schema:
request_version:
resource_version_or_precondition:
idempotency_key:
rate_limit_class:
timeout_budget:
domain_result:
error_codes:
retry_policy:
audit_fields:
sensitive_log_redaction:
```

```text
authenticate
→ authorize
→ validate
→ bind actor/version/precondition
→ check idempotency/replay
→ transaction
→ durable result
→ stable response
```

## Identity and authorization

```yaml
service_identity:
service_account:
end_user_identity:
identity_provider:
domain_authorization:
public_client_endpoints:
private_service_endpoints:
administrator_routes:
least_privilege_review:
environment_separation:
```

## Data model and migration

```yaml
schema_version:
source_of_truth:
required_fields:
constraints:
migration_from:
migration_to:
backup_before_migration:
restore_test:
corruption_handling:
data_export:
provider_exit:
```

## Idempotency, replay, transaction, and retry

```yaml
mutation:
idempotency_scope:
idempotency_ttl:
duplicate_response:
replay_guard:
transaction_boundary:
double_submit_test:
retryable_errors:
non_retryable_errors:
dead_letter_or_manual_recovery:
```

## Realtime and connection model

```yaml
realtime_required:
websocket_or_stream:
request_timeout:
client_reconnect:
external_state_sync:
duplicate_handling:
out_of_order_handling:
session_affinity_assumption: BEST_EFFORT_ONLY
degraded_mode:
minimum_instances:
maximum_instances:
connection_cost:
```

## Async tasks and events

```yaml
task_or_event:
durable_identity:
delivery_semantics:
idempotency:
retry_limit:
dead_letter:
manual_recovery:
scheduler:
finite_job:
```

## AI proxy and provider limits

```yaml
ai_proxy_required:
bounded_game_intent:
provider:
model:
quota:
rate_limit:
privacy:
retention:
output_validation:
safety_filter:
provider_failure:
budget_fallback:
non_ai_degraded_mode:
```

LLM 출력만으로 결제·보상·제재·영구 저장을 확정하지 않는다.

## Secrets and service identity

```yaml
secret_manager:
secret_versions:
rotation:
rollback:
client_export_scan:
repository_scan:
log_redaction_test:
service_account:
iam_roles:
least_privilege_evidence:
```

실제 secret 값이나 unredacted credential을 이 파일에 기록하지 않는다.

## Privacy, retention, and region

```yaml
personal_data:
purpose:
minimum_fields:
region:
retention:
deletion:
access_control:
provider_transfer:
log_policy:
incident_owner:
```

## Capacity, cost, quota, and alerts

```yaml
traffic_assumptions:
peak_rps:
concurrent_connections:
request_duration:
cpu_memory:
minimum_instances:
maximum_instances:
concurrency:
database_connections:
egress:
datastore_calls:
ai_provider_calls:
logging_volume:
quota:
budget_alert:
load_test_result: NOT_RUN
cost_per_active_user_or_match: NOT_RUN
```

## Failure, degradation, backup, and rollback

```yaml
dependency_failure:
timeout:
retry_and_backoff:
read_only_mode:
queued_mutations:
temporary_block:
backup:
restore:
rollback:
data_export:
provider_exit:
service_sunset:
support_owner:
```

## Runtime, load, failure, and cost evidence

```yaml
deployment:
  status: NOT_RUN
  evidence:
runtime_persistence:
  status: NOT_RUN
  evidence:
load:
  status: NOT_RUN
  evidence:
connection_storm:
  status: NOT_RUN
  evidence:
dependency_failure:
  status: NOT_RUN
  evidence:
cost:
  status: NOT_RUN
  evidence:
security_review:
  status: NOT_RUN
  evidence:
rollback:
  status: NOT_RUN
  evidence:
```

## Current readiness and remaining gates

```yaml
current_state: CANDIDATE
static_validation: NOT_RUN
runtime_validation: NOT_RUN
load_and_failure_validation: NOT_RUN
production_readiness: NOT_READY
remaining_gates:
rollback_owner:
last_verified_commit:
```

완료 보고에는 문서 상태와 실제 프로젝트 증거를 분리한다.
