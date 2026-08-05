from __future__ import annotations

import json
from pathlib import Path

GUIDE = "docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"
RECORD = "templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md"
TEST = "tests/test_game_entitlement_integrity_drm_capability.py"

GUIDE_CONTENT = r'''# Game Entitlement, Integrity, and DRM Guide

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
integration. It is `NOT_A_PIRACY_SOLUTION` and can be removable by a determined
attacker. Prefer legitimate player value from Steamworks features, graceful
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

For `STOVE` and every unsupported platform, official SDK and account evidence
required before capability claims. Until the exact current SDK, contract screen,
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
'''

RECORD_CONTENT = r'''# GAME_ENTITLEMENT_AND_INTEGRITY_RECORD

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
'''


def append_block(path: str, marker: str, block: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    if marker in text:
        return
    target.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def package() -> None:
    Path(GUIDE).write_text(GUIDE_CONTENT, encoding="utf-8")
    Path(RECORD).write_text(RECORD_CONTENT, encoding="utf-8")


def route_and_harden() -> None:
    append_block(
        "docs/knowledge/game-development/README.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## 9. 게임 권한·무결성·DRM Capability Pack

- 권한·앱/요청 무결성·DRM·오프라인 라이선스·고가치 서버 권위 질문은 `{GUIDE}`를 사용한다.
- 프로젝트별 신호·복구·개인정보·서비스 종료 증거는 `{RECORD}`가 소유한다.
- `PLATFORM_NATIVE_FIRST`, `NO_CUSTOM_DRM_DEFAULT`, `PLAYER_HARM_REVIEW`를 유지하며 플랫폼별 미확인 기능은 `PLATFORM_CAPABILITY_UNVERIFIED`로 남긴다.
""",
    )
    append_block(
        "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## 게임 권한·무결성·DRM 기술 경로

플랫폼 entitlement, app/build/request integrity, replay, server-authoritative value, offline/outage, false-positive recovery, privacy와 service sunset은 `{GUIDE}`를 사용하고 프로젝트 증거는 `{RECORD}`에 기록한다. Cloud Run Guide는 백엔드 적합성을, 이 Guide는 보호 신호와 플레이어 피해 경계를 소유한다.
""",
    )
    append_block(
        "docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## Entitlement·integrity·DRM handoff

등급·스토어 설문·자산 권리와 별도로 플랫폼 entitlement, app/build/request integrity, server authority, offline/outage와 false-positive remediation은 `{GUIDE}`가 소유한다. 출시 증거는 `{RECORD}`를 링크하되 자산 권리 provenance와 합치지 않는다.
""",
    )
    append_block(
        "docs/DOCUMENTATION_MAP.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## 게임 권한·무결성 Capability Pack

| 질문 | 책임 원본 |
|---|---|
| 플랫폼 권한·앱/요청 무결성·DRM·오프라인·오탐·서비스 종료 | `{GUIDE}` |
| 프로젝트별 플랫폼 신호·서버 권위·복구·개인정보·sandbox 증거 | `{RECORD}` |
""",
    )
    append_block(
        "START_HERE.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## 게임 권한·무결성·DRM 진입

entitlement, Play Integrity, Steam DRM Wrapper, STOVE 기능, anti-tamper, offline license 또는 고가치 서버 권위 질문은 `{GUIDE}`에서 시작한다. 프로젝트 상태는 `{RECORD}`에 두며 platform sandbox와 사람 복구 증거 전에는 `PRODUCTION_READY`를 선언하지 않는다.
""",
    )
    append_block(
        "skills/managing-game-project-operating-system/SKILL.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## Entitlement and integrity capability handoff

`{GUIDE}`가 선택된 프로젝트는 `{RECORD}`를 `PROJECT_OWNED_ENTITLEMENT_INTEGRITY_RECORD`로 설치한다. 실제 platform account, product/package ID, SDK, signing, backend, privacy, recovery와 sandbox evidence는 프로젝트가 소유한다.
""",
    )
    append_block(
        "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## Platform-native entitlement and integrity evaluation

Steam·Google Play·STOVE SDK 또는 보호 도구를 도입하기 전에 `{GUIDE}`의 `PLATFORM_NATIVE_FIRST`와 `NO_CUSTOM_DRM_DEFAULT`를 적용한다. 공식 기능·계정·sandbox 근거가 없으면 `PLATFORM_CAPABILITY_UNVERIFIED`이며 다른 플랫폼과 동일하다고 추정하지 않는다.
""",
    )
    append_block(
        "skills/designing-vertical-slices/SKILL.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## Entitlement and integrity representative flow

`{GUIDE}`를 소비하는 Vertical Slice는 정상 entitlement, offline/grace, provider outage, device/account recovery, request replay와 false-positive remediation을 대표 흐름으로 검증한다. 실제 sandbox 근거가 있을 때만 `PLATFORM_SANDBOX_VERIFIED`를 선언한다.
""",
    )
    append_block(
        "skills/reviewing-and-validating-project-changes/SKILL.md",
        "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
        f"""
## Entitlement and integrity validation route

`{GUIDE}`와 `{RECORD}`의 platform signal, request binding, server authority, replay/double spend, privacy, outage, false positive와 sunset 증거를 분리해 검증한다. 사람의 실제 복구 세션이 없으면 `HUMAN_RECOVERY_VERIFIED`를 선언하지 않는다.
""",
    )
    append_block(
        "templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md",
        "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md",
        f"""
## Entitlement and integrity release evidence

- 프로젝트 Record: `{RECORD}`
- `PLATFORM_NATIVE_FIRST`, platform-specific signal meaning, offline/outage, support/appeal, privacy, save access와 service sunset 상태를 링크한다.
- 자산 권리 provenance와 합치지 않으며 sandbox·사람 복구·법률·플랫폼 승인 미실행 상태를 보존한다.
""",
    )
    append_block(
        "templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md",
        "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md",
        f"""
## 20. Entitlement·integrity·DRM 특화 증빙

- 공용 Guide: `{GUIDE}`
- 프로젝트 Record: `{RECORD}`
- 플랫폼별 entitlement·integrity 신호, server authority, request binding/replay, offline/outage, false-positive, privacy와 sunset 증거를 연결한다.
""",
    )

    governance_path = Path("templates/project-operations/github/documentation-governance.json")
    governance = json.loads(governance_path.read_text(encoding="utf-8"))
    roles = governance.setdefault("release_compliance_evidence_roles", [])
    if not any(item.get("role") == "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD" for item in roles):
        roles.append(
            {
                "role": "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD",
                "template": RECORD,
                "project_owned": True,
                "base_template_is_project_truth": False,
                "default_policy": "PLATFORM_NATIVE_FIRST",
                "unknown_platform_state": "PLATFORM_CAPABILITY_UNVERIFIED",
                "human_recovery_required_for_production": True,
            }
        )
    governance_path.write_text(json.dumps(governance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    append_block(
        GUIDE,
        "## Adversarial decision fixtures",
        """
## Adversarial decision fixtures

```text
Steam single-player entitlement with graceful offline behavior -> PLATFORM_NATIVE_FIRST
Google Play competitive score submit with request-bound backend verification -> REQUEST_BINDING_AND_REPLAY_CONTROL
client-only currency or inventory mutation -> BLOCKED_UNVERIFIED
one unavailable or negative integrity signal -> ONE_VERDICT_PERMANENT_PUNISHMENT_PROHIBITED
repeated multi-signal abuse -> temporary restriction and review
platform outage -> retry, degraded/read-only, or grace path required
service sunset -> offline fallback or save/data export decision required
raw device/integrity signal retained without purpose or TTL -> RAW_SIGNAL_WITHOUT_PURPOSE_OR_TTL_BLOCKED
STOVE capability copied from Steam or Google without official evidence -> PLATFORM_CAPABILITY_UNVERIFIED
Wrapper or obfuscation described as perfect anti-piracy -> BLOCKED_UNVERIFIED
local single-player modding with no external harm -> excessive DRM challenged
```
""",
    )

    test_path = Path(TEST)
    test_text = test_path.read_text(encoding="utf-8")
    if "def test_adversarial_platform_and_player_harm_fixtures" not in test_text:
        method = '''
    def test_adversarial_platform_and_player_harm_fixtures(self) -> None:
        guide = read(GUIDE)
        expectations = {
            "Steam single-player entitlement with graceful offline behavior": "PLATFORM_NATIVE_FIRST",
            "Google Play competitive score submit with request-bound backend verification": "REQUEST_BINDING_AND_REPLAY_CONTROL",
            "client-only currency or inventory mutation": "BLOCKED_UNVERIFIED",
            "one unavailable or negative integrity signal": "ONE_VERDICT_PERMANENT_PUNISHMENT_PROHIBITED",
            "repeated multi-signal abuse": "temporary restriction and review",
            "platform outage": "retry, degraded/read-only, or grace path required",
            "service sunset": "offline fallback or save/data export decision required",
            "raw device/integrity signal retained without purpose or TTL": "RAW_SIGNAL_WITHOUT_PURPOSE_OR_TTL_BLOCKED",
            "STOVE capability copied from Steam or Google without official evidence": "PLATFORM_CAPABILITY_UNVERIFIED",
            "Wrapper or obfuscation described as perfect anti-piracy": "BLOCKED_UNVERIFIED",
            "local single-player modding with no external harm": "excessive DRM challenged",
        }
        for scenario, decision in expectations.items():
            self.assertIn(f"{scenario} -> {decision}", guide)
'''
        marker = '\n\nif __name__ == "__main__":'
        if marker not in test_text:
            raise RuntimeError("entitlement test footer marker not found")
        test_path.write_text(test_text.replace(marker, "\n" + method.rstrip() + marker), encoding="utf-8")

    freshness_path = Path(".github/reference-freshness.json")
    freshness = json.loads(freshness_path.read_text(encoding="utf-8"))
    canonical = freshness.setdefault("canonical_reference_rules", [])
    if not any(rule.get("name") == "game-entitlement-integrity-capability-entrypoints" for rule in canonical):
        canonical.append(
            {
                "name": "game-entitlement-integrity-capability-entrypoints",
                "canonical_path": GUIDE,
                "reference_tokens": [GUIDE, "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"],
                "required_consumers": [
                    "START_HERE.md",
                    "docs/DOCUMENTATION_MAP.md",
                    "docs/knowledge/game-development/README.md",
                    "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
                    "docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
                    "skills/managing-game-project-operating-system/SKILL.md",
                    "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
                    "skills/designing-vertical-slices/SKILL.md",
                    "skills/reviewing-and-validating-project-changes/SKILL.md",
                ],
            }
        )
    coupled = freshness.setdefault("coupled_change_rules", [])
    if not any(rule.get("name") == "game-entitlement-integrity-capability-sync" for rule in coupled):
        coupled.append(
            {
                "name": "game-entitlement-integrity-capability-sync",
                "when_changed": [GUIDE, RECORD],
                "exclude_when_changed": [],
                "require_all_changed": [
                    TEST,
                    "tests/test_platform_review_asset_rights_reference_production.py",
                    "tests/test_base_v9_5_skill_operating_refinement.py",
                    "skills/managing-game-project-operating-system/LEARNING_LOG.md",
                    "docs/CHANGELOG.md",
                ],
                "require_any_changed": [
                    "docs/knowledge/game-development/README.md",
                    "templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md",
                ],
            }
        )
    freshness_path.write_text(json.dumps(freshness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    platform_test = Path("tests/test_platform_review_asset_rights_reference_production.py")
    platform_text = platform_test.read_text(encoding="utf-8")
    if "def test_entitlement_integrity_capability_remains_distinct_and_routed" not in platform_text:
        method = '''
    def test_entitlement_integrity_capability_remains_distinct_and_routed(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"
        )
        record_path = (
            "templates/project-operations/"
            "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md"
        )
        for path in (
            "docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
            "skills/reviewing-and-validating-project-changes/SKILL.md",
        ):
            self.assertIn(guide_path, read(path), path)
        release_pack = read(RELEASE_PACK)
        self.assertIn(record_path, release_pack)
        self.assertIn("PLATFORM_NATIVE_FIRST", release_pack)
        self.assertNotIn("GAME_ENTITLEMENT_AND_INTEGRITY_RECORD", read("skills/SKILL_REGISTRY.json"))
        self.assertNotIn("GAME_ENTITLEMENT_AND_INTEGRITY_RECORD", read("skills/BASE_SHARED_SKILL_ROUTES.json"))
'''
        marker = '\n\nif __name__ == "__main__":'
        platform_test.write_text(platform_text.replace(marker, "\n" + method.rstrip() + marker), encoding="utf-8")

    v95_test = Path("tests/test_base_v9_5_skill_operating_refinement.py")
    v95_text = v95_test.read_text(encoding="utf-8")
    if "def test_entitlement_integrity_routes_through_existing_owners_without_new_skill" not in v95_text:
        method = '''
    def test_entitlement_integrity_routes_through_existing_owners_without_new_skill(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"
        )
        expectations = {
            "skills/managing-game-project-operating-system/SKILL.md": "PROJECT_OWNED_ENTITLEMENT_INTEGRITY_RECORD",
            "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md": "PLATFORM_CAPABILITY_UNVERIFIED",
            "skills/designing-vertical-slices/SKILL.md": "PLATFORM_SANDBOX_VERIFIED",
            "skills/reviewing-and-validating-project-changes/SKILL.md": "HUMAN_RECOVERY_VERIFIED",
        }
        for skill_path, token in expectations.items():
            skill = read(skill_path)
            self.assertIn(guide_path, skill, skill_path)
            self.assertIn(token, skill, skill_path)
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn("GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md", registry)
        self.assertNotIn("GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md", registry)
'''
        marker = '\n\nif __name__ == "__main__":'
        v95_test.write_text(v95_text.replace(marker, "\n" + method.rstrip() + marker), encoding="utf-8")

    append_block(
        "skills/managing-game-project-operating-system/LEARNING_LOG.md",
        "## 2026-08-05 — 게임 entitlement·integrity·DRM Capability Pack",
        """
## 2026-08-05 — 게임 entitlement·integrity·DRM Capability Pack

- **상태:** `PATTERN_CANDIDATE`
- **Decision:** 새 활성 Skill과 shared route를 추가하지 않고 기존 운영·플랫폼 도입 평가·Vertical Slice·통합 검증 owner에 Guide와 프로젝트 Record를 연결했다.
- **Boundary:** `PLATFORM_NATIVE_FIRST`, `NO_CUSTOM_DRM_DEFAULT`, 플랫폼별 의미 보존, 단일 신호 영구 제재 금지, offline/outage·지원/이의제기·save access·sunset·privacy 결정이 필수다.
- **Evidence:** 정적 테스트는 계약·라우팅·반례만 증명한다. Steam/Google Play/STOVE sandbox, 사람 오탐 복구, 법률 검토, 플랫폼 승인과 production readiness는 실행하지 않았다.
- **Not run:** platform SDK integration `NOT_RUN`, human false-positive recovery `HUMAN_NOT_RUN`, legal/platform approval `NOT_PERFORMED`.
""",
    )
    append_block(
        "docs/CHANGELOG.md",
        "## 2026-08-05 - 게임 entitlement·integrity·DRM Capability Pack PR B",
        """
## 2026-08-05 - 게임 entitlement·integrity·DRM Capability Pack PR B

- 플랫폼 entitlement·app/build/request integrity·server authority·offline/outage·오탐 복구·privacy·service sunset Guide와 프로젝트 Record를 추가했다.
- Steam Wrapper의 한계, Google Play request-bound backend verification, STOVE 미확인 상태를 플랫폼별로 분리했다.
- 단일 신호 영구 제재, false platform parity, client-authoritative high-value state, replay/double spend, outage lockout, 무기한 raw-signal 보존과 no-sunset 설계를 차단했다.
- 새 활성 Skill·shared route·플랫폼 계정·SDK credential·signing key·secret은 추가하지 않았다.
""",
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("package", "route-harden"))
    args = parser.parse_args()
    if args.phase == "package":
        package()
    else:
        route_and_harden()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
