# GAME_ENTITLEMENT_AND_INTEGRITY_RECORD

Capability Pack: `GAME_ENTITLEMENT_INTEGRITY_AND_DRM`
Project-owned artifact: yes
Base Guide: `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`
Current state: `UNVERIFIED`

Evidence states:

```text
UNKNOWN
UNVERIFIED
NOT_APPLICABLE
CONFIGURED
STATIC_VERIFIED
PLATFORM_SANDBOX_VERIFIED
HUMAN_RECOVERY_VERIFIED
PRODUCTION_READY
NOT_RUN
HUMAN_NOT_RUN
```

Do not skip evidence stages. A document is not platform, human, legal, or
production evidence.

## Platform and product identity

```yaml
project:
decision_id:
platform:
account_identity:
product_identity:
package_or_app_identity:
platform_sdk_version:
official_source_checked_at:
capability_state: UNVERIFIED
owner:
```

## Protected player value

```yaml
product_or_dlc_access:
paid_rewards:
currency_and_trade:
competitive_score_and_rank:
reward_achievement:
asynchronous_battle_result:
online_inventory:
limited_event_claim:
legitimate_player_value:
```

## Threat and abuse model

```yaml
threat:
protected_value:
attacker_capability:
expected_harm:
legitimate_player_harm:
likelihood:
selected_controls:
rejected_controls:
remaining_risk:
```

## Entitlement source

```yaml
platform_entitlement_source:
ownership_or_license_signal:
issued_at:
expiry:
cached_entitlement:
refund_or_revocation:
reauthentication:
remediation:
state: UNVERIFIED
```

## App/build integrity source

```yaml
app_signing:
app_integrity_verdict:
device_or_environment_verdict:
build_identity:
local_integrity_support:
unsupported_fields: UNKNOWN
state: UNVERIFIED
```

## Request binding and replay protection

```yaml
operation_id:
request_binding:
request_hash_or_nonce:
actor_identity:
resource_version:
idempotency_key:
replay_status:
transaction:
double_spend_guard:
retry_policy:
audit_record:
state: UNVERIFIED
```

## Server-authoritative state

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
state: UNVERIFIED
```

## Local tamper resistance

```yaml
binary_signing:
package_encryption:
obfuscation:
save_checksum_or_signature:
debugger_or_tamper_detection:
extractable_client_secret_assumption: true
external_harm_if_modified:
player_harm_review:
state: NOT_APPLICABLE
```

## Offline, outage, and grace policy

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
read_only_or_queued_mode:
state: UNVERIFIED
```

## False-positive remediation

```yaml
signal_unavailable:
weak_anomaly:
entitlement_mismatch:
request_binding_mismatch:
repeated_multi_signal_abuse:
severe_action_evidence:
temporary_restriction:
permanent_action_approval:
support_and_appeal:
human_recovery_test: HUMAN_NOT_RUN
```

## Privacy and signal retention

```yaml
signal_purpose:
minimum_fields:
raw_signal_retention:
retention_ttl:
deletion:
access_control:
provider_transfer:
incident_owner:
state: UNVERIFIED
```

## Service sunset and save access

```yaml
sunset_mode:
offline_fallback:
save_export:
data_export:
license_cache_after_sunset:
support_end_date:
player_notice:
rollback_owner:
state: UNVERIFIED
```

## Platform-specific evidence

```yaml
steam_sandbox:
  status: NOT_RUN
  evidence:
play_integrity_sandbox:
  status: NOT_RUN
  evidence:
stove_capability_review:
  status: NOT_RUN
  evidence:
other_platform:
  status: NOT_APPLICABLE
  evidence:
```

## Adversarial findings

```yaml
perfect_anti_piracy_claim:
false_platform_parity:
client_authoritative_value:
replay_or_double_spend_gap:
one_signal_irreversible_punishment:
outage_lockout:
excessive_signal_retention:
missing_sunset_or_save_access:
local_modding_overprotection:
open_findings:
```

## Current readiness and remaining gates

```yaml
current_state: UNVERIFIED
static_validation: NOT_RUN
platform_sandbox_validation: NOT_RUN
human_false_positive_recovery: HUMAN_NOT_RUN
legal_clearance: NOT_PERFORMED
platform_approval: NOT_PERFORMED
production_readiness: NOT_READY
remaining_gates:
rollback_owner:
last_verified_commit:
```
