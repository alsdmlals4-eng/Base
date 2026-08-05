# Game Entitlement, Integrity, and DRM Guide

Capability Pack: `GAME_ENTITLEMENT_INTEGRITY_AND_DRM`
Approved BCP: `BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity`
Official-source check date: `2026-08-05`
New active Skill: none
Platform accounts, credentials, signing keys, and secrets created: none

Evidence ceiling:
- platform_sdk_integration: NOT_RUN
- steam_sandbox: NOT_RUN
- play_integrity_sandbox: NOT_RUN
- stove_capability_review: NOT_RUN
- human_false_positive_recovery: HUMAN_NOT_RUN
- legal_clearance: NOT_PERFORMED
- platform_approval: NOT_PERFORMED
- production_readiness: NOT_READY

This Guide does not provide `PERFECT_ANTI_PIRACY_GUARANTEE`,
`ZERO_FALSE_POSITIVES_GUARANTEE`, `AUTOMATIC_LEGAL_CLEARANCE`, or
`AUTOMATIC_PLATFORM_APPROVAL`.

## Core policy

```text
PLATFORM_NATIVE_FIRST
-> NO_CUSTOM_DRM_DEFAULT
-> SERVER_AUTHORITY_FOR_HIGH_VALUE_STATE
-> REQUEST_BINDING_AND_REPLAY_CONTROL
-> TIERED_REMEDIATION
-> OFFLINE_AND_OUTAGE_POLICY
-> PLAYER_HARM_REVIEW
```

DRM is a layered practice, not a perfect piracy-prevention claim. Separate:
- entitlement: the right to use a product, DLC, or feature;
- integrity: evidence about app, build, device/environment, or request state;
- server authority: project-owned domain validation for high-value state;
- tamper resistance: optional cost-raising local protection;
- evidence state: what was actually verified.

## Trust tiers

```text
Tier 0: client claim
Tier 1: platform entitlement signal
Tier 2: app/build integrity signal
Tier 3: request-bound integrity/replay protection
Tier 4: server-authoritative domain validation
Tier 5: audit, anomaly, human/multi-signal review
```

Higher-value actions require stronger evidence, but no tier removes the need for
recovery, proportionality, privacy, and support.

## Platform adapter

```yaml
platform:
account_identity:
product_identity:
package_or_app_identity:
entitlement_verdict:
app_integrity_verdict:
device_or_environment_verdict:
request_binding:
issued_at:
expiry:
replay_status:
raw_signal_storage_policy:
normalized_decision:
remediation_options:
```

Preserve `UNKNOWN`, `UNVERIFIED`, and `NOT_APPLICABLE`. Apply
`NO_UNIVERSAL_PLATFORM_VERDICT`: unsupported fields and platform-specific
meaning must not be fabricated or flattened.

## Steam

Use platform-native ownership verification and Steam launch integration where
appropriate. The `Steam DRM Wrapper` is optional shallow protection and launch
integration. It is `NOT_A_PIRACY_SOLUTION` and is removable by a determined attacker. Prefer legitimate player value from Steamworks features, graceful
offline behavior, account recovery, and support over escalating custom DRM.

Official source to re-check before release:
- https://partner.steamgames.com/doc/features/drm

## Google Play

Evaluate `Play App Signing` and `Play Integrity` for the actual app and request.
Important requests use `requestHash` or the current official binding mechanism.
The server performs backend verification, recomputes the binding, verifies app
and account context, and applies domain policy. Standard requests provide
automatic replay protection, but quota, error handling, token freshness,
provider outage, and remediation must still be designed.

`ONE_VERDICT_PERMANENT_PUNISHMENT_PROHIBITED`: one unavailable or negative
verdict cannot directly cause irreversible ban, purchase denial, or save
deletion.

Official sources to re-check before implementation:
- https://developer.android.com/google/play/integrity
- https://developer.android.com/google/play/integrity/standard
- https://developer.android.com/guide/publishing/app-signing

## STOVE and unsupported platforms

For `STOVE` and every unsupported platform, official SDK and account evidence required before capability claims. Until the exact current SDK, contract screen,
sandbox account, offline behavior, and recovery path are checked, use
`PLATFORM_CAPABILITY_UNVERIFIED` and
`NO_STEAM_GOOGLE_PLAY_PARITY_ASSUMPTION`.

Reference entrypoint to re-check without assuming feature parity:
- https://studio-docs.onstove.com

## Server authority for high-value state

`SERVER_AUTHORITY_FOR_HIGH_VALUE_STATE` applies to:
- purchase-linked entitlement
- currency and trade
- competitive score and rank
- reward-bearing achievement
- asynchronous battle result
- online inventory
- limited event claim

```yaml
authoritative_input:
server_recomputation:
allowed_ranges:
resource_version:
transaction:
double_spend_guard:
idempotency:
replay_guard:
audit_record:
rollback:
support_and_appeal:
```

A client claim, local checksum, Wrapper, obfuscation, or one platform signal is
not sufficient authority for paid or competitive mutation.

## Optional local protection

Possible supporting controls include binary signing, package encryption where
supported, obfuscation, save checksum/signature, and debugger/tamper detection.
Assume client secrets are extractable. Local protection raises attack cost but
must be challenged when single-player modification has no external harm to
other players, economy, competition, or paid entitlement.

## Offline, outage, recovery, and sunset

`OFFLINE_AND_OUTAGE_POLICY` requires explicit decisions:

```yaml
offline_play_allowed:
first_launch_online_required:
cached_entitlement:
cache_ttl:
clock_tamper_handling:
grace_period:
platform_outage:
backend_outage:
account_recovery:
device_change:
refund_or_revocation:
save_export:
sunset_mode:
support_and_appeal:
```

A legitimate single-player session should not be permanently locked by a
temporary provider outage. High-value online mutation may retry, degrade to
read-only, queue safely, or block temporarily. Service sunset requires an
offline fallback or an explicit save/data export decision where feasible.

## Tiered remediation

```text
signal unavailable -> retry/backoff or degraded mode
weak anomaly -> telemetry and low-risk limits
entitlement mismatch -> reauthentication and platform remediation
request binding mismatch -> reject high-value mutation, preserve account/save
repeated multi-signal abuse -> temporary restriction and review
confirmed severe abuse -> evidence-backed project action with support/appeal
```

`TIERED_REMEDIATION` prohibits irreversible punishment from one weak or
unavailable signal.

## Privacy and signal retention

```yaml
signal_purpose:
minimum_fields:
raw_signal_retention:
retention_ttl:
deletion:
access_control:
provider_transfer:
```

Minimize device, account, and integrity data. Raw signals require a documented
purpose, access boundary, and TTL. `RAW_SIGNAL_WITHOUT_PURPOSE_OR_TTL_BLOCKED`.

## Evidence state

Static CI verifies document structure, routes, and safeguards. It does not prove
platform SDK integration, sandbox verdicts, false-positive recovery, legal
clearance, platform approval, or production readiness.
