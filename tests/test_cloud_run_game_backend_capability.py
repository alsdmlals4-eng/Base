from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md"
)
CONTRACT = (
    ROOT
    / "templates"
    / "project-operations"
    / "GAME_BACKEND_SERVICE_CONTRACT.md"
)
EVIDENCE_PACK = ROOT / "templates" / "research" / "GAME_DEVELOPMENT_EVIDENCE_PACK.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
SHARED_ROUTES = ROOT / "skills" / "BASE_SHARED_SKILL_ROUTES.json"


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class CloudRunGameBackendCapabilityTests(unittest.TestCase):
    maxDiff = None

    def test_required_artifacts_exist(self) -> None:
        required = (GUIDE, CONTRACT)
        missing = [
            str(path.relative_to(ROOT))
            for path in required
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_cloud_run_fit_lifecycle_is_conditional(self) -> None:
        guide = read(GUIDE)
        for term in (
            "SERVER_FEATURE_DETECTED",
            "CLOUD_RUN_DEFAULT_CANDIDATE",
            "FIT_AND_RISK_ASSESSMENT",
            "PROJECT_OWNED_SERVICE_CONTRACT",
            "CLOUD_RUN_RECOMMENDED",
            "CLOUD_RUN_CONDITIONAL",
            "ALTERNATIVE_ARCHITECTURE_REQUIRED",
            "SERVER_NOT_REQUIRED",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, guide)
        self.assertNotIn("CLOUD_RUN_REQUIRED", guide)

    def test_unsuitable_realtime_and_state_assumptions_are_rejected(self) -> None:
        guide = read(GUIDE)
        for term in (
            "high-frequency authoritative realtime",
            "UDP",
            "indefinite worker",
            "instance-local durable authority",
            "external persistent datastore",
            "modular monolith",
            "scale-to-zero",
        ):
            self.assertIn(term, guide)

    def test_api_mutation_and_identity_contract(self) -> None:
        guide = read(GUIDE)
        for field in (
            "operation_id:",
            "actor_identity:",
            "authorization_scope:",
            "requested_action:",
            "target_resource:",
            "target_property:",
            "target_owner_or_tenant:",
            "authorization_context:",
            "authorization_decision:",
            "authorization_failure_semantics:",
            "request_schema:",
            "request_version:",
            "resource_version_or_precondition:",
            "idempotency_key:",
            "rate_limit_class:",
            "timeout_budget:",
            "error_codes:",
            "retry_policy:",
            "audit_fields:",
            "sensitive_log_redaction:",
        ):
            self.assertIn(field, guide)
        for term in (
            "service identity",
            "end-user identity",
            "domain authorization",
            "authenticate",
            "authorize",
            "idempotency",
            "replay",
            "transaction",
            "durable result",
        ):
            self.assertIn(term, guide)

    def test_demo_test_double_contract_is_interface_compatible_and_fail_closed(self) -> None:
        guide = read(GUIDE)
        contract = read(CONTRACT)
        required_terms = (
            "ONE_CONSUMER_INTERFACE",
            "REAL_ADAPTER",
            "FAKE_ADAPTER",
            "CONTRACT_PARITY_REQUIRED",
            "FAIL_CLOSED_UNKNOWN_OPERATION",
        )
        for term in required_terms:
            self.assertIn(term, guide)
            self.assertIn(term, contract)
        for field in (
            "consumer_interface:",
            "real_adapter:",
            "fake_adapter:",
            "contract_version:",
            "unknown_operation_policy: FAIL_CLOSED_UNKNOWN_OPERATION",
            "provider_contract_verification: NOT_RUN",
        ):
            self.assertIn(field, contract)

    def test_demo_fixtures_are_deterministic_synthetic_resettable_and_simulated_only(self) -> None:
        guide = read(GUIDE)
        contract = read(CONTRACT)
        for term in (
            "DETERMINISTIC_FIXTURE",
            "RESETTABLE_STATE",
            "SYNTHETIC_DATA_ONLY",
            "PUBLIC_DEMO_SANITIZATION",
            "SIMULATED_ONLY",
        ):
            self.assertIn(term, guide)
            self.assertIn(term, contract)
        for phrase in (
            "real secrets",
            "private records",
            "real identity",
        ):
            self.assertIn(phrase, guide)
        self.assertIn("## Demo, test-double, and public-demo boundary", contract)

    def test_secrets_and_privileged_routes_stay_server_side(self) -> None:
        guide = read(GUIDE)
        for term in (
            "Secret Manager",
            "service account",
            "least privilege",
            "administrator route",
            "client export",
            "repository",
            "sensitive log redaction",
        ):
            self.assertIn(term, guide)

    def test_authorization_denial_path_is_project_consumable_and_evidence_bounded(self) -> None:
        guide = read(GUIDE)
        contract = read(CONTRACT)
        evidence = read(EVIDENCE_PACK)
        shared_terms = (
            "AUTHENTICATION_IS_NOT_AUTHORIZATION",
            "DENY_BY_DEFAULT",
            "SERVER_SIDE_AUTHORIZATION_EVERY_REQUEST",
            "AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED",
            "DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT",
            "STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE",
        )
        for term in shared_terms:
            self.assertIn(term, guide, term)
            self.assertIn(term, contract, term)
        for term in (
            "ONLINE_IDENTITY_NOT_REQUIRED",
            "cross_user_object_id_test: NOT_RUN",
            "ordinary_user_admin_function_test: NOT_RUN",
            "sensitive_property_injection_test: NOT_RUN",
            "denial_state_readback: NOT_RUN",
            "denial_side_effect_readback: NOT_RUN",
            "authorization_negative_tests: NOT_RUN",
            "security_runtime_evidence: NOT_RUN",
        ):
            self.assertIn(term, contract, term)
        for term in (
            "AUTHENTICATION_IS_NOT_AUTHORIZATION",
            "AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED",
            "DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT",
            "STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE",
            "ONLINE_IDENTITY_NOT_REQUIRED",
        ):
            self.assertIn(term, evidence, term)

    def test_websocket_contract_requires_recovery_and_cost_evidence(self) -> None:
        guide = read(GUIDE)
        for term in (
            "request timeout",
            "client reconnect",
            "external state",
            "duplicate",
            "out-of-order",
            "BEST_EFFORT_ONLY",
            "degraded mode",
            "connection cost",
        ):
            self.assertIn(term, guide)

    def test_capacity_cost_and_provider_exit_are_explicit(self) -> None:
        guide = read(GUIDE)
        for field in (
            "minimum_instances:",
            "maximum_instances:",
            "concurrency:",
            "database_connections:",
            "quota:",
            "budget_alert:",
            "load_test_result:",
            "cost_per_active_user_or_match:",
            "provider_exit:",
        ):
            self.assertIn(field, guide)

    def test_ai_proxy_is_bounded_and_not_domain_authority(self) -> None:
        guide = read(GUIDE)
        for term in (
            "bounded game intent",
            "quota",
            "output validation",
            "privacy",
            "provider failure",
            "safety filter",
            "budget fallback",
            "LLM_ONLY_PAYMENT_AUTHORITY",
            "LLM_ONLY_REWARD_AUTHORITY",
            "LLM_ONLY_SANCTION_AUTHORITY",
            "LLM_ONLY_PERMANENT_SAVE_AUTHORITY",
        ):
            self.assertIn(term, guide)

    def test_project_contract_has_required_sections_and_fields(self) -> None:
        contract = read(CONTRACT)
        for heading in (
            "## Player value and server feature",
            "## Fit decision and rejected alternatives",
            "## Authority and persistent state",
            "## API and request lifecycle",
            "## Identity and authorization",
            "## Authorization, session, and denial-path evidence",
            "## Data model and migration",
            "## Idempotency, replay, transaction, and retry",
            "## Realtime and connection model",
            "## Async tasks and events",
            "## AI proxy and provider limits",
            "## Secrets and service identity",
            "## Privacy, retention, and region",
            "## Capacity, cost, quota, and alerts",
            "## Failure, degradation, backup, and rollback",
            "## Demo, test-double, and public-demo boundary",
            "## Runtime, load, failure, and cost evidence",
            "## Current readiness and remaining gates",
        ):
            self.assertIn(heading, contract)
        for term in (
            "NOT_REQUIRED",
            "CANDIDATE",
            "SELECTED",
            "CONFIGURED",
            "STATIC_VERIFIED",
            "RUNTIME_VERIFIED",
            "LOAD_AND_FAILURE_VERIFIED",
            "PRODUCTION_READY",
            "NOT_RUN",
        ):
            self.assertIn(term, contract)

    def test_official_sources_and_evidence_ceiling_are_explicit(self) -> None:
        guide = read(GUIDE)
        for domain in (
            "cloud.google.com/run/docs",
            "docs.cloud.google.com/run/docs",
            "cheatsheetseries.owasp.org",
            "owasp.org/API-Security",
            "pages.nist.gov/800-63-4",
        ):
            self.assertIn(domain, guide)
        for term in (
            "deployment: NOT_RUN",
            "runtime: NOT_RUN",
            "load: NOT_RUN",
            "failure: NOT_RUN",
            "cost: NOT_RUN",
            "security: NOT_RUN",
            "PRODUCTION_READY is project evidence only",
        ):
            self.assertIn(term, guide)

    def test_existing_owners_and_discovery_surfaces_route_the_capability(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md"
        )
        contract_path = "templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md"

        for path in (
            "docs/knowledge/game-development/README.md",
            "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "docs/DOCUMENTATION_MAP.md",
            "START_HERE.md",
        ):
            self.assertIn(guide_path, read(path), path)

        owner_expectations = {
            "skills/analyzing-and-refining-game-concepts/SKILL.md": (
                guide_path,
                "SERVER_FEATURE_DETECTED",
            ),
            "skills/managing-game-project-operating-system/SKILL.md": (
                guide_path,
                contract_path,
                "PROJECT_OWNED_SERVICE_CONTRACT",
            ),
            "skills/designing-vertical-slices/SKILL.md": (
                guide_path,
                "RUNTIME_VERIFIED",
            ),
            "skills/reviewing-and-validating-project-changes/SKILL.md": (
                guide_path,
                "LOAD_AND_FAILURE_VERIFIED",
            ),
            "skills/optimizing-ai-model-and-prompt-costs/SKILL.md": (
                guide_path,
                "bounded AI proxy",
            ),
        }
        for path, terms in owner_expectations.items():
            text = read(path)
            for term in terms:
                self.assertIn(term, text, path)

        evidence = read(EVIDENCE_PACK)
        self.assertIn(contract_path, evidence)
        for term in (
            "AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED",
            "DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT",
            "STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE",
        ):
            self.assertIn(term, evidence)
        governance = json.loads(
            read("templates/project-operations/github/documentation-governance.json")
        )
        serialized = json.dumps(governance, ensure_ascii=False, sort_keys=True)
        for term in (
            "GAME_BACKEND_SERVICE_CONTRACT",
            "CLOUD_RUN_DEFAULT_CANDIDATE",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, serialized)

    def test_no_active_skill_or_shared_project_route_is_added(self) -> None:
        registry = read(REGISTRY)
        shared_routes = read(SHARED_ROUTES)
        for token in (
            "cloud-run-game-backend",
            "game-backend-cloud-run",
            "GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md",
            "GAME_BACKEND_SERVICE_CONTRACT.md",
        ):
            self.assertNotIn(token, registry)
            self.assertNotIn(token, shared_routes)

    def test_adversarial_decision_fixtures(self) -> None:
        guide = read(GUIDE)
        fixtures = {
            "async leaderboard API": "CLOUD_RUN_RECOMMENDED",
            "turn-based asynchronous battle": "CLOUD_RUN_RECOMMENDED",
            "WebSocket lobby and presence": "CLOUD_RUN_CONDITIONAL",
            "60 Hz authoritative action battle / UDP": "ALTERNATIVE_ARCHITECTURE_REQUIRED",
            "offline-only feature with no shared state": "SERVER_NOT_REQUIRED",
            "retrying reward mutation without idempotency": "BLOCKED_UNVERIFIED",
            "provider key in client or repository": "BLOCKED_UNVERIFIED",
            "unlimited AI proxy without quota/cost": "BLOCKED_UNVERIFIED",
            "instance-local durable save": "BLOCKED_UNVERIFIED",
            "static documents presented as runtime/load/cost proof": "BLOCKED_UNVERIFIED",
            "authenticated user reads another user's save by changing an object ID": "BLOCKED_UNVERIFIED",
            "hidden admin button but direct admin operation succeeds": "BLOCKED_UNVERIFIED",
            "denied mutation still changes balance or emits a reward": "BLOCKED_UNVERIFIED",
            "positive-only authorization tests presented as security proof": "BLOCKED_UNVERIFIED",
            "logout clears only the client token while the server session remains valid": "BLOCKED_UNVERIFIED",
            "bearer session secret stored in browser localStorage or sessionStorage or written to a URL or raw log": "BLOCKED_UNVERIFIED",
        }
        for scenario, decision in fixtures.items():
            self.assertIn(f"{scenario} -> {decision}", guide)


if __name__ == "__main__":
    unittest.main()
