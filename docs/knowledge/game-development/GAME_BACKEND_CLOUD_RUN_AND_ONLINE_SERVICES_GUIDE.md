# Cloud Run Game Backend and Online Services Guide

Capability Pack: `GAME_BACKEND_CLOUD_RUN`
Approved BCP: `BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity`
New active Skill: none
Cloud resources created: none

Evidence ceiling:
- deployment: NOT_RUN
- runtime: NOT_RUN
- load: NOT_RUN
- failure: NOT_RUN
- cost: NOT_RUN
- security: NOT_RUN
- `PRODUCTION_READY is project evidence only`

## Decision lifecycle

```text
SERVER_FEATURE_DETECTED
-> CLOUD_RUN_DEFAULT_CANDIDATE
-> FIT_AND_RISK_ASSESSMENT
-> PROJECT_OWNED_SERVICE_CONTRACT
-> implementation
-> static / runtime / load / failure / cost validation
```

Allowed decisions: `CLOUD_RUN_RECOMMENDED`, `CLOUD_RUN_CONDITIONAL`,
`ALTERNATIVE_ARCHITECTURE_REQUIRED`, `SERVER_NOT_REQUIRED`, or
`BLOCKED_UNVERIFIED`. Start with player value, authority, latency, connection,
data, privacy, failure, cost, rollback, and service-sunset requirements.

## Fit boundary

Good default candidates: authenticated HTTPS APIs, profile, cloud save,
leaderboard, achievement, async turns/results, webhooks, admin APIs, finite jobs,
and a bounded AI proxy. WebSocket lobby, presence, chat, and soft realtime are
conditional.

Default exclusions:
- high-frequency authoritative realtime
- UDP
- indefinite worker
- instance-local durable authority
- fixed dedicated-server lifecycle
- offline-only features that do not need a server

Small projects start with a `modular monolith` and future split seams.
Durable state belongs in an `external persistent datastore`; instance memory and
writable filesystem are non-authoritative. Measure `scale-to-zero` cold start
and minimum-instance cost instead of assuming suitability.

## API and mutation contract

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
authenticate -> authorize -> validate schema/version
-> bind actor and precondition -> check idempotency and replay
-> apply transaction -> write durable result -> return stable response
```

Paid, competitive, currency, reward, and trade state is not finalized from a
client claim alone.

## Demo and test-double service contract

A project may validate a service-backed flow before the real provider is ready,
but it must not fork consumer behavior into a separate demo-only API. Use
`ONE_CONSUMER_INTERFACE`: the same consumer-facing operation contract is
implemented by a `REAL_ADAPTER` and, when useful, a `FAKE_ADAPTER`.

```text
consumer
-> ONE_CONSUMER_INTERFACE
   -> REAL_ADAPTER -> real provider
   -> FAKE_ADAPTER -> deterministic synthetic fixture
```

`CONTRACT_PARITY_REQUIRED` means both adapters preserve the same operation IDs,
request shape and version, response/domain-result shape, stable error classes,
and mutation semantics that the consumer is expected to handle. A fake adapter
may replace infrastructure and external side effects, but it must not silently
invent a friendlier contract than the real provider.

Unknown fake operations use `FAIL_CLOSED_UNKNOWN_OPERATION`. Missing handlers,
unsupported request versions, schema mismatches, or unseeded required state must
return an explicit test/demo failure or `BLOCKED_UNVERIFIED`; they must not fall
through to `null`, `{ok: true}`, or another fabricated success.

Demo fixtures use `DETERMINISTIC_FIXTURE` and `RESETTABLE_STATE` when repeatable
validation benefits from a known starting state. A reset must restore the same
approved seed and must not mutate project canon, production data, or a real
provider. Public or shareable demo data uses `SYNTHETIC_DATA_ONLY`.

`PUBLIC_DEMO_SANITIZATION` requires the demo boundary to exclude real secrets,
private records, and real identity data unless a specific field is both necessary
and explicitly approved for public use. Replace identities, customer/player
records, credentials, approval recipients, and other private operational values
with synthetic equivalents. Never copy production credentials or private data
into a fixture merely to make the demo realistic.

Fake execution has evidence ceiling `SIMULATED_ONLY`. It may prove consumer flow,
UI/UX behavior, deterministic state transitions, error handling, and contract
expectations inside the fake boundary. It does not satisfy real-provider
`RUNTIME_VERIFIED`, load, dependency-failure, cost, security, persistence,
rollback, or `PRODUCTION_READY` evidence. Provider contract verification and real
runtime evidence remain separate gates.

## Identity, privilege, and secret boundary

```text
service identity -> Cloud Run IAM and service account
end-user identity -> project identity provider
domain authorization -> project game rules
```

Separate public endpoints, private service calls, and each `administrator route`.
Use a user-managed service account and `least privilege` per environment.
Keep keys and credentials in `Secret Manager` or an equivalent server-side
boundary, never in `client export` or the `repository`. Apply
`sensitive log redaction`, rotation, and rollback.

## WebSocket and soft realtime

```yaml
request timeout:
client reconnect:
external state:
duplicate:
out-of-order:
session_affinity_assumption: BEST_EFFORT_ONLY
degraded mode:
connection cost:
minimum_instances:
maximum_instances:
```

Test reconnect to another instance, duplicate and out-of-order messages,
instance termination, external-state delay, connection storm, quota, dependency
failure, and degraded mode. A single connection or instance must not own the
authoritative session state.

## Capacity, cost, and provider exit

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
load_test_result:
cost_per_active_user_or_match:
provider_exit:
```

Bound maximum instances and database_connections together. Connect rate limits,
quota, and budget alerts to failure policy. `provider_exit` covers data export,
API seams, migration, rollback, and service sunset.

## Bounded AI proxy

```text
game client -> bounded game intent -> authentication/policy/quota
-> provider request -> output validation -> safe game response
```

Define privacy, minimum data, retention, provider failure, safety filter,
`budget fallback`, and a non-AI degraded mode.

Forbidden claims:
- `LLM_ONLY_PAYMENT_AUTHORITY`
- `LLM_ONLY_REWARD_AUTHORITY`
- `LLM_ONLY_SANCTION_AUTHORITY`
- `LLM_ONLY_PERMANENT_SAVE_AUTHORITY`

## Evidence and official sources

Static CI validates files, routes, terms, and forbidden boundaries. It does not
prove deployment, runtime persistence, load, failure recovery, cost, security,
or production readiness. Fake/demo adapter execution remains `SIMULATED_ONLY`
until the corresponding real-provider contract and runtime evidence are actually
verified.

Re-check current official documentation before implementation:
- https://cloud.google.com/run/docs
- https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run
- https://docs.cloud.google.com/run/docs/triggering/websockets
- https://docs.cloud.google.com/run/docs/configuring/request-timeout
- https://docs.cloud.google.com/run/docs/configuring/session-affinity
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service
- https://docs.cloud.google.com/run/docs/configuring/services/secrets

## Adversarial decision fixtures

```text
async leaderboard API -> CLOUD_RUN_RECOMMENDED
turn-based asynchronous battle -> CLOUD_RUN_RECOMMENDED
WebSocket lobby and presence -> CLOUD_RUN_CONDITIONAL
60 Hz authoritative action battle / UDP -> ALTERNATIVE_ARCHITECTURE_REQUIRED
offline-only feature with no shared state -> SERVER_NOT_REQUIRED
retrying reward mutation without idempotency -> BLOCKED_UNVERIFIED
provider key in client or repository -> BLOCKED_UNVERIFIED
unlimited AI proxy without quota/cost -> BLOCKED_UNVERIFIED
instance-local durable save -> BLOCKED_UNVERIFIED
static documents presented as runtime/load/cost proof -> BLOCKED_UNVERIFIED
```
