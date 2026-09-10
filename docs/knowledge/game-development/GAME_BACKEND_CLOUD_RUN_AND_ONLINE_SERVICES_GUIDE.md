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
-> static / runtime / load / failure / cost / security validation
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
requested_action:
target_resource:
target_property:
target_owner_or_tenant:
authorization_context:
authorization_decision:
authorization_failure_semantics:
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

## Authorization, session, and authentication boundary

`APPLIES_ONLY_TO_PROTECTED_ONLINE_OPERATIONS`: use this contract only when a
project actually exposes protected online data or actions. An offline-only project
with no account, shared state, remote entitlement, or administrator surface records
`ONLINE_IDENTITY_NOT_REQUIRED`; this Guide does not create a server requirement.

`AUTHENTICATION_IS_NOT_AUTHORIZATION`: a valid identity proves who is making a
request; it does not grant implicit access to every object, property, or
function. Static wording is also not executed protection:
`STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE`.

### Authorization enforcement

Every protected operation uses `DENY_BY_DEFAULT` at a trusted server, gateway,
or serverless boundary and applies `SERVER_SIDE_AUTHORIZATION_EVERY_REQUEST`.
Each decision follows `OBJECT_ACTION_PROPERTY_CONTEXT_POLICY` by binding:

- the actor and effective privileges derived from trusted server-side state;
- the requested action or function, including alternate methods and routes;
- the target resource or object and requested property set; and
- ownership, tenant, relationship, entitlement, and relevant environment or
  domain context.

A path, query, header, or body identifier is a
`CLIENT_IDENTIFIER_IS_UNTRUSTED_SELECTOR`. Random or unpredictable identifiers
reduce guessing but do not replace object-level authorization. A
`client-supplied role`, owner or tenant, entitlement, balance, reward, or
administrator flag is an untrusted caller claim. A verified identity-provider
claim may be an input to policy, but it is not the final game-domain
authorization decision. `UI_VISIBILITY_IS_NOT_ENFORCEMENT`: hiding a button, screen,
route, or administrator menu may improve UX, but the direct request must still be
rejected at the trusted enforcement point.

Apply function-level authorization, object-level authorization, and
property-level authorization. Use explicit read and write property allowlists;
reject unknown or sensitive properties so mass assignment cannot change
ownership, role, moderation, currency, reward, entitlement, or other
server-owned state.

### Authorization negative proof

`AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED` uses at least two distinct actors and
separate resources of the same type. Test applicable cases including:

- unauthenticated, expired, revoked, or stale identity;
- actor A requests another actor's resource, including cross-actor read, update, and delete;
- the same role crosses a tenant or relationship boundary;
- an ordinary actor calls an administrator function;
- HTTP method, route, RPC, or operation substitution;
- sensitive property injection; and
- a bulk, list, or export operation that could mix authorized and unauthorized
  objects.

Every denial must prove both:

- `DENIED_RESPONSE_IS_STABLE_AND_NON_DISCLOSING`: the response uses the approved
  stable error class without revealing private object or policy details; and
- `DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT`: authoritative state is unchanged, no
  queue, event, webhook, reward, charge, email, or equivalent external effect
  is emitted, and the redacted audit event is attributable.

These checks include `NO_DURABLE_SIDE_EFFECT`, `NO_PRIVATE_DATA_DISCLOSURE`,
`NO_PRIVILEGE_ELEVATION`, and `SANITIZED_AUDIT_READBACK`.
`POSITIVE_PATH_IS_NOT_AUTHORIZATION_PROOF`: successful allowed requests do not
prove forbidden requests fail. A managed identity provider establishes identity,
not game-domain permissions;
`THIRD_PARTY_IDENTITY_IS_NOT_DOMAIN_AUTHORIZATION_PROOF`.

### Session and long-lived connection lifecycle

Define an idle timeout and an absolute timeout according to project risk and UX,
and enforce both at the session host. Browser timers or client token deletion alone
are `CLIENT_ONLY_TIMEOUT_IS_NOT_ENFORCEMENT`. Require server-side invalidation on
logout, expiry, explicit revocation, suspected compromise, account disablement, and
privilege change. Use session rotation or reauthentication after authentication-boundary
changes and before high-risk operations when the threat model requires it.

Long-lived connections do not inherit permanent permission from the initial
handshake. Require WebSocket session revalidation, per-message authorization,
and closure when the session expires or is revoked. Browser WebSocket handshakes
validate `Origin` against an explicit allowlist of trusted origins and apply the
project's CSWSH or CSRF handshake control when cookies carry identity. Reconnect
repeats current authentication and authorization checks.

`SESSION_SECRET_STORAGE_THREAT_MODEL_REQUIRED`: document the browser, native,
desktop, console, and device-compromise assumptions before choosing storage. Do not
store bearer session secrets in JavaScript-readable browser Web Storage such as
`localStorage` or `sessionStorage`.
For browser cookie sessions, apply Secure, HttpOnly, and SameSite attributes plus
the required origin and CSRF controls. Native and desktop clients minimize local
secrets and use platform-protected storage where supported by the target platform
and threat model. Never place session secrets in URLs or logs. Record the
access-token lifetime, refresh or session rotation, and a server-verifiable
revocation or invalidation strategy.

### Authentication abuse, recovery, and credential storage

Prefer a current platform or managed identity provider when cost, privacy,
portability, and provider exit fit the project: `MANAGED_IDP_PREFERRED`.
Self-managed identity requires explicit justification and a project threat model.
Use `TLS_REQUIRED_FOR_ENTIRE_PROTECTED_SESSION`; protecting only login while later
authenticated traffic can downgrade is not sufficient. Use a
`generic authentication failure` response where account enumeration is a risk,
bounded login abuse control,
privileged MFA or reauthentication where the risk requires it, and account recovery
that is not weaker than the normal authentication path.

Do not ship default, test, or shared privileged credentials.
`DEFAULT_OR_SHARED_PRIVILEGED_CREDENTIALS_FORBIDDEN` applies to administrator and
service identities; each privileged principal must be attributable and limited to the
least privilege required by its role. A documented, monitored break-glass path is a
separate emergency control, not a reusable default account.

When a project manages passwords itself, registration and change flows use
`COMMON_OR_BREACHED_PASSWORD_BLOCKING`: compare the complete candidate against a
current blocklist of common, expected, context-specific, and compromised values.
This complements login abuse limits; it does not justify arbitrary composition rules
or periodic rotation as a substitute for compromise response. Re-check current OWASP
and NIST guidance at implementation time.

Argon2id is the preferred new-system default, scrypt is the fallback when
Argon2id is unavailable, PBKDF2 is the FIPS-required option, and bcrypt is legacy-only.
Plaintext, reversible storage, or a fast general hash such as
SHA-256 alone violates `FAST_GENERAL_HASH_IS_NOT_PASSWORD_STORAGE`. Do not copy
work factors or blocklist sizes into Base as timeless constants; record the current
official parameters in the project evidence at implementation time.

`AUTHORIZATION_RUNTIME_EVIDENCE_REQUIRED`: a project security claim needs the
exact tested revision, configured policy and environment, executable negative
tests, and state, side-effect, and audit readback. Base static tests prove only
that this reusable contract exists.

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
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/
- https://cornucopia.owasp.org/taxonomy/asvs-5.0/06-authentication/02-password-security
- https://pages.nist.gov/800-63-4/sp800-63b.html
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html
- https://mas.owasp.org/MASWE/MASVS-STORAGE/MASWE-0001/

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
authenticated user reads another user's save by changing an object ID -> BLOCKED_UNVERIFIED
hidden admin button but direct admin operation succeeds -> BLOCKED_UNVERIFIED
random UUID used without object authorization -> BLOCKED_UNVERIFIED
denied mutation still changes balance or emits a reward -> BLOCKED_UNVERIFIED
positive-only authorization tests presented as security proof -> BLOCKED_UNVERIFIED
logout clears only the client token while the server session remains valid -> BLOCKED_UNVERIFIED
WebSocket authenticates once but does not authorize each message -> BLOCKED_UNVERIFIED
self-managed passwords use plain SHA-256 without an adaptive password hash -> BLOCKED_UNVERIFIED
default or shared privileged credential remains enabled -> BLOCKED_UNVERIFIED
self-managed password accepts a common or breached value -> BLOCKED_UNVERIFIED
login uses TLS but an authenticated session later falls back to plaintext -> BLOCKED_UNVERIFIED
bearer session secret stored in browser localStorage or sessionStorage or written to a URL or raw log -> BLOCKED_UNVERIFIED
```
