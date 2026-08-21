# GAME_BACKEND_SERVICE_CONTRACT

Capability Pack: `GAME_BACKEND_CLOUD_RUN`
Project-owned artifact: yes
Base Guide: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
Current state: `CANDIDATE`
Static document evidence must not be promoted to runtime or production evidence.

## Lifecycle

```text
NOT_REQUIRED
-> CANDIDATE
-> SELECTED
-> CONFIGURED
-> STATIC_VERIFIED
-> RUNTIME_VERIFIED
-> LOAD_AND_FAILURE_VERIFIED
-> PRODUCTION_READY
```

Do not skip stages. Record unexecuted evidence as `NOT_RUN`.
`PRODUCTION_READY` requires project deployment, runtime, load, failure, cost,
and security evidence.

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
authenticate -> authorize -> validate -> bind actor/version/precondition
-> check idempotency/replay -> transaction -> durable result -> stable response
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

LLM output alone must not authorize payment, reward, sanction, or permanent save.

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

Do not place real secret values or unredacted credentials in this file.

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

## Demo, test-double, and public-demo boundary

Use this section only when the project actually needs a fake/demo service path.
The consumer-facing service contract remains one interface; a fake path is an
adapter, not a second product API.

```yaml
consumer_interface:
consumer_interface_policy: ONE_CONSUMER_INTERFACE
real_adapter: REAL_ADAPTER
fake_adapter: FAKE_ADAPTER
contract_version:
contract_parity_policy: CONTRACT_PARITY_REQUIRED
parity_operations:
parity_request_schema:
parity_response_or_domain_result:
parity_error_classes:
parity_mutation_semantics:
unknown_operation_policy: FAIL_CLOSED_UNKNOWN_OPERATION
fixture_policy: DETERMINISTIC_FIXTURE
fixture_seed:
reset_policy: RESETTABLE_STATE
reset_target:
synthetic_data_policy: SYNTHETIC_DATA_ONLY
public_demo_policy: PUBLIC_DEMO_SANITIZATION
real_secrets_policy: FORBIDDEN
private_records_policy: FORBIDDEN
real_identity_policy: REPLACE_WITH_SYNTHETIC_UNLESS_EXPLICITLY_PUBLIC_APPROVED
provider_contract_verification: NOT_RUN
provider_contract_evidence:
fake_evidence_ceiling: SIMULATED_ONLY
```

Required boundaries:

- `REAL_ADAPTER` and `FAKE_ADAPTER` implement the same approved consumer contract.
- Unknown operations, unsupported versions, missing required fixture state, and schema mismatches fail closed; they never fabricate success.
- Reset restores the approved deterministic seed and does not mutate production or project canon.
- Public/shareable fixtures contain synthetic records and no production credentials, private user/customer/project records, or unapproved real identities.
- `SIMULATED_ONLY` may support consumer-flow and error-handling evidence but never satisfies real provider `RUNTIME_VERIFIED`, load, dependency-failure, cost, security, persistence, rollback, or `PRODUCTION_READY` evidence.

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

Completion reports must separate document status from project runtime evidence.
