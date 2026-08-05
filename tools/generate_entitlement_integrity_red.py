from __future__ import annotations

from pathlib import Path

TEST_PATH = Path("tests/test_game_entitlement_integrity_drm_capability.py")
LOCAL_VALIDATION = Path("tests/test_local_validation.py")
V9_MACHINE = Path("tests/test_v9_machine_contracts.py")

TEST_CONTENT = r'''from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"
)
RECORD = (
    ROOT
    / "templates"
    / "project-operations"
    / "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md"
)
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
SHARED_ROUTES = ROOT / "skills" / "BASE_SHARED_SKILL_ROUTES.json"


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class GameEntitlementIntegrityDrmCapabilityTests(unittest.TestCase):
    maxDiff = None

    def test_required_artifacts_exist(self) -> None:
        required = (GUIDE, RECORD)
        missing = [
            str(path.relative_to(ROOT))
            for path in required
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_core_layered_protection_contract(self) -> None:
        guide = read(GUIDE)
        for token in (
            "PLATFORM_NATIVE_FIRST",
            "NO_CUSTOM_DRM_DEFAULT",
            "SERVER_AUTHORITY_FOR_HIGH_VALUE_STATE",
            "REQUEST_BINDING_AND_REPLAY_CONTROL",
            "TIERED_REMEDIATION",
            "OFFLINE_AND_OUTAGE_POLICY",
            "PLAYER_HARM_REVIEW",
            "PLATFORM_CAPABILITY_UNVERIFIED",
        ):
            self.assertIn(token, guide)
        for forbidden in (
            "PERFECT_ANTI_PIRACY_GUARANTEE",
            "ZERO_FALSE_POSITIVES_GUARANTEE",
            "AUTOMATIC_LEGAL_CLEARANCE",
            "AUTOMATIC_PLATFORM_APPROVAL",
        ):
            self.assertIn(forbidden, guide)

    def test_trust_tiers_preserve_evidence_strength(self) -> None:
        guide = read(GUIDE)
        for tier in (
            "Tier 0: client claim",
            "Tier 1: platform entitlement signal",
            "Tier 2: app/build integrity signal",
            "Tier 3: request-bound integrity/replay protection",
            "Tier 4: server-authoritative domain validation",
            "Tier 5: audit, anomaly, human/multi-signal review",
        ):
            self.assertIn(tier, guide)

    def test_platform_adapter_preserves_unknown_and_platform_specific_meaning(self) -> None:
        guide = read(GUIDE)
        for field in (
            "platform:",
            "account_identity:",
            "product_identity:",
            "package_or_app_identity:",
            "entitlement_verdict:",
            "app_integrity_verdict:",
            "device_or_environment_verdict:",
            "request_binding:",
            "issued_at:",
            "expiry:",
            "replay_status:",
            "raw_signal_storage_policy:",
            "normalized_decision:",
            "remediation_options:",
        ):
            self.assertIn(field, guide)
        for state in ("UNKNOWN", "UNVERIFIED", "NOT_APPLICABLE"):
            self.assertIn(state, guide)
        self.assertIn("NO_UNIVERSAL_PLATFORM_VERDICT", guide)

    def test_steam_wrapper_limitations_are_explicit(self) -> None:
        guide = read(GUIDE)
        for term in (
            "Steam DRM Wrapper",
            "ownership verification",
            "Steam launch integration",
            "NOT_A_PIRACY_SOLUTION",
            "removable by a determined attacker",
            "legitimate player value",
        ):
            self.assertIn(term, guide)

    def test_google_play_integrity_requires_backend_binding_and_recovery(self) -> None:
        guide = read(GUIDE)
        for term in (
            "Play App Signing",
            "Play Integrity",
            "requestHash",
            "backend verification",
            "automatic replay protection",
            "quota",
            "error handling",
            "remediation",
            "ONE_VERDICT_PERMANENT_PUNISHMENT_PROHIBITED",
        ):
            self.assertIn(term, guide)

    def test_stove_and_unsupported_platforms_remain_unverified(self) -> None:
        guide = read(GUIDE)
        for term in (
            "STOVE",
            "official SDK and account evidence required",
            "PLATFORM_CAPABILITY_UNVERIFIED",
            "NO_STEAM_GOOGLE_PLAY_PARITY_ASSUMPTION",
            "studio-docs.onstove.com",
        ):
            self.assertIn(term, guide)

    def test_high_value_state_requires_server_authority(self) -> None:
        guide = read(GUIDE)
        for term in (
            "purchase-linked entitlement",
            "currency and trade",
            "competitive score and rank",
            "reward-bearing achievement",
            "asynchronous battle result",
            "online inventory",
            "limited event claim",
        ):
            self.assertIn(term, guide)
        for field in (
            "authoritative_input:",
            "server_recomputation:",
            "allowed_ranges:",
            "resource_version:",
            "transaction:",
            "double_spend_guard:",
            "idempotency:",
            "replay_guard:",
            "audit_record:",
            "rollback:",
            "support_and_appeal:",
        ):
            self.assertIn(field, guide)

    def test_offline_outage_recovery_and_sunset_are_mandatory_decisions(self) -> None:
        guide = read(GUIDE)
        for field in (
            "offline_play_allowed:",
            "first_launch_online_required:",
            "cached_entitlement:",
            "cache_ttl:",
            "clock_tamper_handling:",
            "grace_period:",
            "platform_outage:",
            "backend_outage:",
            "account_recovery:",
            "device_change:",
            "refund_or_revocation:",
            "save_export:",
            "sunset_mode:",
            "support_and_appeal:",
        ):
            self.assertIn(field, guide)

    def test_privacy_and_raw_signal_retention_are_minimized(self) -> None:
        guide = read(GUIDE)
        for field in (
            "signal_purpose:",
            "minimum_fields:",
            "raw_signal_retention:",
            "retention_ttl:",
            "deletion:",
            "access_control:",
            "provider_transfer:",
        ):
            self.assertIn(field, guide)
        self.assertIn("RAW_SIGNAL_WITHOUT_PURPOSE_OR_TTL_BLOCKED", guide)

    def test_project_record_has_required_sections_and_evidence_states(self) -> None:
        record = read(RECORD)
        for heading in (
            "## Platform and product identity",
            "## Protected player value",
            "## Threat and abuse model",
            "## Entitlement source",
            "## App/build integrity source",
            "## Request binding and replay protection",
            "## Server-authoritative state",
            "## Local tamper resistance",
            "## Offline, outage, and grace policy",
            "## False-positive remediation",
            "## Privacy and signal retention",
            "## Service sunset and save access",
            "## Platform-specific evidence",
            "## Adversarial findings",
            "## Current readiness and remaining gates",
        ):
            self.assertIn(heading, record)
        for state in (
            "UNKNOWN",
            "UNVERIFIED",
            "NOT_APPLICABLE",
            "CONFIGURED",
            "STATIC_VERIFIED",
            "PLATFORM_SANDBOX_VERIFIED",
            "HUMAN_RECOVERY_VERIFIED",
            "PRODUCTION_READY",
            "NOT_RUN",
            "HUMAN_NOT_RUN",
        ):
            self.assertIn(state, record)

    def test_existing_owners_and_release_surfaces_route_the_capability(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md"
        )
        record_path = (
            "templates/project-operations/"
            "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md"
        )
        for path in (
            "docs/knowledge/game-development/README.md",
            "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
            "docs/DOCUMENTATION_MAP.md",
            "START_HERE.md",
        ):
            self.assertIn(guide_path, read(path), path)

        expectations = {
            "skills/managing-game-project-operating-system/SKILL.md": (
                guide_path,
                record_path,
                "PROJECT_OWNED_ENTITLEMENT_INTEGRITY_RECORD",
            ),
            "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md": (
                guide_path,
                "PLATFORM_CAPABILITY_UNVERIFIED",
            ),
            "skills/designing-vertical-slices/SKILL.md": (
                guide_path,
                "PLATFORM_SANDBOX_VERIFIED",
            ),
            "skills/reviewing-and-validating-project-changes/SKILL.md": (
                guide_path,
                "HUMAN_RECOVERY_VERIFIED",
            ),
        }
        for path, terms in expectations.items():
            text = read(path)
            for term in terms:
                self.assertIn(term, text, path)

        for path in (
            "templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md",
            "templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md",
        ):
            self.assertIn(record_path, read(path), path)

        governance = json.loads(
            read("templates/project-operations/github/documentation-governance.json")
        )
        serialized = json.dumps(governance, ensure_ascii=False, sort_keys=True)
        for term in (
            "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD",
            "PLATFORM_NATIVE_FIRST",
            "PLATFORM_CAPABILITY_UNVERIFIED",
        ):
            self.assertIn(term, serialized)

    def test_no_active_skill_shared_route_or_universal_verdict_is_added(self) -> None:
        registry = read(REGISTRY)
        shared_routes = read(SHARED_ROUTES)
        for token in (
            "game-entitlement-integrity-drm",
            "GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md",
            "GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md",
            "UNIVERSAL_PLATFORM_VERDICT",
        ):
            self.assertNotIn(token, registry)
            self.assertNotIn(token, shared_routes)

    def test_evidence_ceiling_and_official_source_boundaries_are_explicit(self) -> None:
        guide = read(GUIDE)
        for term in (
            "platform_sdk_integration: NOT_RUN",
            "steam_sandbox: NOT_RUN",
            "play_integrity_sandbox: NOT_RUN",
            "stove_capability_review: NOT_RUN",
            "human_false_positive_recovery: HUMAN_NOT_RUN",
            "legal_clearance: NOT_PERFORMED",
            "platform_approval: NOT_PERFORMED",
            "production_readiness: NOT_READY",
            "partner.steamgames.com",
            "developer.android.com/google/play/integrity",
        ):
            self.assertIn(term, guide)


if __name__ == "__main__":
    unittest.main()
'''

IMPORT_BLOCK = '''from tests.test_game_entitlement_integrity_drm_capability import (
    GameEntitlementIntegrityDrmCapabilityTests
    as _GameEntitlementIntegrityDrmCapabilityTests,
)
'''


def insert_before(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "test_game_entitlement_integrity_drm_capability" in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker}")
    path.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")


def main() -> int:
    TEST_PATH.write_text(TEST_CONTENT, encoding="utf-8")
    insert_before(LOCAL_VALIDATION, "from tools import run_local_validation as runner\n", IMPORT_BLOCK)
    insert_before(V9_MACHINE, "\n\nROOT = Path(__file__).resolve().parents[1]\n", "\n" + IMPORT_BLOCK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
