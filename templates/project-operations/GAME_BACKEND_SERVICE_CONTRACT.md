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
requested_action:
target_resource:
target_property:
target_owner_or_tenant:
authorization_context:
authorization_decision:
authorization_failure_semantics:
allowed_read_properties:
allowed_write_properties:
unknown_or_sensitive_property_policy: REJECT
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
authentication_authorization_boundary: AUTHENTICATION_IS_NOT_AUTHORIZATION
default_authorization_decision: DENY_BY_DEFAULT
authorization_enforcement: SERVER_SIDE_AUTHORIZATION_EVERY_REQUEST
authorization_policy_model: OBJECT_ACTION_PROPERTY_CONTEXT_POLICY
function_level_authorization:
object_level_authorization:
property_level_authorization:
client_identifier_policy: UNTRUSTED_SELECTOR
ui_visibility_policy: NOT_ENFORCEMENT
public_client_endpoints:
private_service_endpoints:
administrator_routes:
least_privilege_review:
environment_separation:
```

## Authorization, session, and denial-path evidence

Use this section only when the project has an actual protected online operation.
An offline-only project may record `ONLINE_IDENTITY_NOT_REQUIRED` and remain
`SERVER_NOT_REQUIRED` rather than inventing authentication or a backend.

```yaml
online_identity_requirement: ONLINE_IDENTITY_NOT_REQUIRED | ONLINE_IDENTITY_REQUIRED
identity_management_policy: MANAGED_IDP_PREFERRED | SELF_MANAGED_JUSTIFIED
transport_policy: TLS_REQUIRED_FOR_ENTIRE_PROTECTED_SESSION
privileged_credential_policy: DEFAULT_OR_SHARED_PRIVILEGED_CREDENTIALS_FORBIDDEN
common_or_breached_password_policy: COMMON_OR_BREACHED_PASSWORD_BLOCKING
generic_authentication_failure: generic authentication failure
login_abuse_control: login abuse control
privileged_authentication: privileged MFA or reauthentication
account_recovery_assurance: account recovery
password_storage_policy: MANAGED_BY_IDP | ARGON2ID_PREFERRED | SCRYPT_FALLBACK | PBKDF2_FIPS_REQUIRED | LEGACY_BCRYPT_ONLY
session_secret_storage_threat_model: SESSION_SECRET_STORAGE_THREAT_MODEL_REQUIRED
session_secret_storage:
browser_cookie_policy_if_applicable: SECURE_HTTPONLY_SAMESITE
browser_web_storage_policy: FORBID_BEARER_SESSION_SECRETS
browser_csrf_and_origin_controls:
native_secure_storage_if_applicable:
token_url_policy: FORBIDDEN
token_log_policy: REDACT
access_token_lifetime:
refresh_or_session_rotation:
revocation_strategy:
session_storage_and_transport:
idle_timeout: idle timeout
absolute_timeout: absolute timeout
server_side_logout_invalidation: server-side invalidation
explicit_revocation_invalidation: server-side invalidation
privilege_change_invalidation: privilege change
session_rotation_or_reauthentication: session rotation
websocket_session_revalidation: WebSocket session revalidation
websocket_message_authorization: per-message authorization
websocket_origin_policy: EXPLICIT_ALLOWLIST_FOR_BROWSER_CLIENTS
authorization_negative_matrix: AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED
matrix:
  - case_id:
    actor_identity:
    requested_action:
    target_resource:
    target_property:
    target_owner_or_tenant:
    authorization_context:
    expected_decision: DENY
    expected_error_class:
    expected_state_delta: NONE
    expected_external_side_effects: NONE
    expected_audit_event:
cross_user_object_id_test: NOT_RUN
cross_tenant_or_relationship_test: NOT_RUN
ordinary_user_admin_function_test: NOT_RUN
method_path_operation_substitution_test: NOT_RUN
sensitive_property_injection_test: NOT_RUN
bulk_list_export_test: NOT_RUN
property_allowlist_test: NOT_RUN
expired_or_revoked_session_test: NOT_RUN
logout_invalidation_test: NOT_RUN
privilege_change_invalidation_test: NOT_RUN
websocket_session_revalidation_test: NOT_RUN
websocket_message_authorization_test: NOT_RUN
websocket_origin_validation_test: NOT_RUN
browser_session_secret_storage_test: NOT_RUN
browser_csrf_origin_test: NOT_RUN
native_session_secret_storage_review: NOT_RUN
token_url_and_log_scan: NOT_RUN
revocation_strategy_test: NOT_RUN
default_or_shared_privileged_credential_scan: NOT_RUN
common_or_breached_password_test: NOT_RUN
protected_session_tls_test: NOT_RUN
denied_response_policy: DENIED_RESPONSE_IS_STABLE_AND_NON_DISCLOSING
denial_side_effect_policy: DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT
denial_state_readback: NOT_RUN
denial_side_effect_readback: NOT_RUN
denial_private_data_readback: NOT_RUN
denial_privilege_readback: NOT_RUN
redacted_audit_readback: NOT_RUN
authorization_negative_tests: NOT_RUN
security_runtime_evidence: NOT_RUN
```

Required boundaries:

- `AUTHENTICATION_IS_NOT_AUTHORIZATION`, `DENY_BY_DEFAULT`,
  `SERVER_SIDE_AUTHORIZATION_EVERY_REQUEST`, and
  `OBJECT_ACTION_PROPERTY_CONTEXT_POLICY` apply at the trusted enforcement point.
- Client identifiers are selectors, not grants; use
  `client_identifier_policy: UNTRUSTED_SELECTOR`. Hidden UI is not enforcement;
  use `ui_visibility_policy: NOT_ENFORCEMENT`.
- A denial passes only with `DENIED_RESPONSE_IS_STABLE_AND_NON_DISCLOSING` and
  `DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT`, supported by state, external-effect,
  private-data, privilege, and redacted-audit readback.
- Idle and absolute timeouts are server-enforced.
  `CLIENT_ONLY_TIMEOUT_IS_NOT_ENFORCEMENT`; logout, revocation, expiry,
  disablement, and privilege change require server-side invalidation.
- Long-lived connections require WebSocket session revalidation and per-message
  authorization, then close when the identity or session becomes invalid. Browser
  handshakes validate `Origin` against an explicit allowlist of trusted origins and
  apply the selected
  CSWSH or CSRF handshake control when cookies carry identity.
- `SESSION_SECRET_STORAGE_THREAT_MODEL_REQUIRED` records browser and native risks.
  Do not use persistent JavaScript-readable browser storage for bearer session
  secrets in `localStorage` or `sessionStorage`. Cookie sessions require Secure,
  HttpOnly, and SameSite attributes when
  applicable; native clients use platform-protected storage where supported. Never
  place session secrets in URLs or logs. Record access-token lifetime, refresh or
  session rotation, and a server-verifiable revocation or invalidation strategy.
- Protect the complete authenticated path with
  `TLS_REQUIRED_FOR_ENTIRE_PROTECTED_SESSION`, not only the login request. Do not
  deploy default, test, or shared privileged credentials;
  `DEFAULT_OR_SHARED_PRIVILEGED_CREDENTIALS_FORBIDDEN` applies to administrator
  and service identities.
- Self-managed password registration and change apply
  `COMMON_OR_BREACHED_PASSWORD_BLOCKING` using a current blocklist of common,
  expected, context-specific, and compromised complete values. This does not add
  arbitrary composition or periodic-rotation requirements.
- For self-managed passwords, current guidance prefers Argon2id, uses scrypt
  when Argon2id is unavailable, uses PBKDF2 when FIPS validation is required,
  and states that bcrypt is legacy-only. Plain SHA-256 or another fast general hash
  violates `FAST_GENERAL_HASH_IS_NOT_PASSWORD_STORAGE`.
- Positive-only tests, client UI, unpredictable IDs, and identity-provider login
  are not domain-authorization evidence.
- `STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE`. Keep execution fields
  `NOT_RUN` until the project performs and reads back the corresponding test.

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
