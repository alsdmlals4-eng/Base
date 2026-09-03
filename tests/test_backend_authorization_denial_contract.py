from __future__ import annotations

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str, next_heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = text.find(next_heading, start + len(heading))
    return text[start:] if end < 0 else text[start:end]


class BackendAuthorizationDenialContractTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.guide = read(GUIDE)
        cls.contract = read(CONTRACT)
        cls.guide_authz = section(
            cls.guide,
            "## Authorization, session, and authentication boundary",
            "## WebSocket and soft realtime",
        )
        cls.contract_authz = section(
            cls.contract,
            "## Identity and authorization",
            "## Data model and migration",
        )

    def assert_contains_all(
        self, text: str, terms: tuple[str, ...], source: Path | str
    ) -> None:
        missing = [term for term in terms if term not in text]
        self.assertEqual([], missing, f"missing from {source}: {missing}")

    def test_authentication_is_separate_and_authorization_fails_closed(self) -> None:
        shared_terms = (
            "AUTHENTICATION_IS_NOT_AUTHORIZATION",
            "DENY_BY_DEFAULT",
            "SERVER_SIDE_AUTHORIZATION_EVERY_REQUEST",
            "OBJECT_ACTION_PROPERTY_CONTEXT_POLICY",
        )
        self.assert_contains_all(self.guide_authz, shared_terms, GUIDE)
        self.assert_contains_all(self.contract_authz, shared_terms, CONTRACT)

    def test_api_contract_binds_the_complete_authorization_decision(self) -> None:
        fields = (
            "actor_identity:",
            "authorization_scope:",
            "requested_action:",
            "target_resource:",
            "target_property:",
            "target_owner_or_tenant:",
            "authorization_context:",
            "authorization_decision:",
            "authorization_failure_semantics:",
        )
        self.assert_contains_all(self.guide, fields, GUIDE)
        self.assert_contains_all(self.contract, fields, CONTRACT)

    def test_client_ui_identifiers_and_privilege_claims_are_not_authority(self) -> None:
        self.assert_contains_all(
            self.guide_authz,
            (
                "CLIENT_IDENTIFIER_IS_UNTRUSTED_SELECTOR",
                "UI_VISIBILITY_IS_NOT_ENFORCEMENT",
                "Random or unpredictable identifiers",
                "client-supplied role",
            ),
            GUIDE,
        )
        self.assert_contains_all(
            self.contract_authz,
            (
                "client_identifier_policy: UNTRUSTED_SELECTOR",
                "ui_visibility_policy: NOT_ENFORCEMENT",
            ),
            CONTRACT,
        )

    def test_negative_matrix_covers_horizontal_vertical_property_bulk_and_session_cases(self) -> None:
        self.assert_contains_all(
            self.guide_authz,
            (
                "AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED",
                "two distinct actors",
                "another actor's resource",
                "cross-actor read, update, and delete",
                "sensitive property injection",
                "bulk, list, or export operation",
                "ordinary actor calls an administrator function",
            ),
            GUIDE,
        )
        self.assert_contains_all(
            self.contract_authz,
            (
                "cross_user_object_id_test: NOT_RUN",
                "cross_tenant_or_relationship_test: NOT_RUN",
                "ordinary_user_admin_function_test: NOT_RUN",
                "method_path_operation_substitution_test: NOT_RUN",
                "sensitive_property_injection_test: NOT_RUN",
                "bulk_list_export_test: NOT_RUN",
                "expired_or_revoked_session_test: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_denial_requires_stable_non_disclosing_response_and_no_effect(self) -> None:
        shared_terms = (
            "DENIED_RESPONSE_IS_STABLE_AND_NON_DISCLOSING",
            "DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT",
        )
        self.assert_contains_all(self.guide_authz, shared_terms, GUIDE)
        self.assert_contains_all(self.contract_authz, shared_terms, CONTRACT)
        self.assert_contains_all(
            self.contract_authz,
            (
                "expected_state_delta: NONE",
                "expected_external_side_effects: NONE",
                "denial_state_readback: NOT_RUN",
                "denial_side_effect_readback: NOT_RUN",
                "denial_private_data_readback: NOT_RUN",
                "denial_privilege_readback: NOT_RUN",
                "redacted_audit_readback: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_properties_use_explicit_read_and_write_allowlists(self) -> None:
        self.assert_contains_all(
            self.guide_authz,
            (
                "explicit read and write property allowlists",
                "mass assignment",
                "unknown or sensitive properties",
            ),
            GUIDE,
        )
        self.assert_contains_all(
            self.contract,
            (
                "allowed_read_properties:",
                "allowed_write_properties:",
                "unknown_or_sensitive_property_policy: REJECT",
                "property_allowlist_test: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_sessions_are_invalidated_server_side_and_long_connections_reauthorize(self) -> None:
        shared_terms = (
            "idle timeout",
            "absolute timeout",
            "server-side invalidation",
            "privilege change",
            "session rotation",
            "WebSocket session revalidation",
            "per-message authorization",
            "explicit allowlist of trusted origins",
            "CLIENT_ONLY_TIMEOUT_IS_NOT_ENFORCEMENT",
        )
        self.assert_contains_all(self.guide_authz, shared_terms, GUIDE)
        self.assert_contains_all(self.contract_authz, shared_terms, CONTRACT)
        self.assert_contains_all(
            self.contract_authz,
            (
                "logout_invalidation_test: NOT_RUN",
                "privilege_change_invalidation_test: NOT_RUN",
                "websocket_session_revalidation_test: NOT_RUN",
                "websocket_message_authorization_test: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_session_secret_storage_and_revocation_strategy_are_explicit(self) -> None:
        self.assert_contains_all(
            self.guide_authz,
            (
                "SESSION_SECRET_STORAGE_THREAT_MODEL_REQUIRED",
                "JavaScript-readable browser Web Storage",
                "`localStorage`",
                "`sessionStorage`",
                "Secure, HttpOnly, and SameSite",
                "origin and CSRF controls",
                "platform-protected storage",
                "session secrets in URLs or logs",
                "server-verifiable",
                "revocation or invalidation strategy",
                "access-token lifetime",
                "refresh or session rotation",
            ),
            GUIDE,
        )
        self.assert_contains_all(
            self.contract_authz,
            (
                "session_secret_storage:",
                "browser_cookie_policy_if_applicable: SECURE_HTTPONLY_SAMESITE",
                "browser_web_storage_policy: FORBID_BEARER_SESSION_SECRETS",
                "browser_csrf_and_origin_controls:",
                "websocket_origin_policy: EXPLICIT_ALLOWLIST_FOR_BROWSER_CLIENTS",
                "websocket_origin_validation_test: NOT_RUN",
                "native_secure_storage_if_applicable:",
                "access_token_lifetime:",
                "refresh_or_session_rotation:",
                "revocation_strategy:",
                "token_url_policy: FORBIDDEN",
                "token_log_policy: REDACT",
                "browser_session_secret_storage_test: NOT_RUN",
                "browser_csrf_origin_test: NOT_RUN",
                "native_session_secret_storage_review: NOT_RUN",
                "token_url_and_log_scan: NOT_RUN",
                "revocation_strategy_test: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_authentication_abuse_recovery_and_password_storage_are_bounded(self) -> None:
        shared_terms = (
            "MANAGED_IDP_PREFERRED",
            "TLS_REQUIRED_FOR_ENTIRE_PROTECTED_SESSION",
            "DEFAULT_OR_SHARED_PRIVILEGED_CREDENTIALS_FORBIDDEN",
            "COMMON_OR_BREACHED_PASSWORD_BLOCKING",
            "generic authentication failure",
            "login abuse control",
            "privileged MFA or reauthentication",
            "account recovery",
            "Argon2id",
            "scrypt",
            "PBKDF2",
            "bcrypt is legacy-only",
            "FAST_GENERAL_HASH_IS_NOT_PASSWORD_STORAGE",
        )
        self.assert_contains_all(self.guide_authz, shared_terms, GUIDE)
        self.assert_contains_all(self.contract_authz, shared_terms, CONTRACT)
        self.assertIn("Argon2id is the preferred new-system default", self.guide_authz)
        self.assertIn("current guidance prefers Argon2id", self.contract_authz)
        self.assert_contains_all(
            self.contract_authz,
            (
                "transport_policy: TLS_REQUIRED_FOR_ENTIRE_PROTECTED_SESSION",
                "privileged_credential_policy: DEFAULT_OR_SHARED_PRIVILEGED_CREDENTIALS_FORBIDDEN",
                "common_or_breached_password_policy: COMMON_OR_BREACHED_PASSWORD_BLOCKING",
                "default_or_shared_privileged_credential_scan: NOT_RUN",
                "common_or_breached_password_test: NOT_RUN",
                "protected_session_tls_test: NOT_RUN",
            ),
            CONTRACT,
        )

    def test_security_contract_is_conditional_and_preserves_evidence_ceiling(self) -> None:
        self.assert_contains_all(
            self.guide_authz,
            (
                "APPLIES_ONLY_TO_PROTECTED_ONLINE_OPERATIONS",
                "ONLINE_IDENTITY_NOT_REQUIRED",
                "offline-only project",
                "POSITIVE_PATH_IS_NOT_AUTHORIZATION_PROOF",
                "THIRD_PARTY_IDENTITY_IS_NOT_DOMAIN_AUTHORIZATION_PROOF",
                "AUTHORIZATION_RUNTIME_EVIDENCE_REQUIRED",
                "STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE",
            ),
            GUIDE,
        )
        self.assert_contains_all(
            self.contract_authz,
            (
                "online_identity_requirement: ONLINE_IDENTITY_NOT_REQUIRED | ONLINE_IDENTITY_REQUIRED",
                "authorization_negative_tests: NOT_RUN",
                "security_runtime_evidence: NOT_RUN",
                "STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE",
            ),
            CONTRACT,
        )

    def test_primary_sources_are_present_once(self) -> None:
        sources = (
            "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html",
            "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
            "https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/",
            "https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/",
            "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
            "https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/",
            "https://cornucopia.owasp.org/taxonomy/asvs-5.0/06-authentication/02-password-security",
            "https://pages.nist.gov/800-63-4/sp800-63b.html",
            "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html",
            "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html",
            "https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html",
            "https://mas.owasp.org/MASWE/MASVS-STORAGE/MASWE-0001/",
        )
        for source in sources:
            self.assertEqual(1, self.guide.count(source), source)

    def test_adversarial_fixtures_reject_common_shortcuts(self) -> None:
        fixtures = (
            "authenticated user reads another user's save by changing an object ID -> BLOCKED_UNVERIFIED",
            "hidden admin button but direct admin operation succeeds -> BLOCKED_UNVERIFIED",
            "random UUID used without object authorization -> BLOCKED_UNVERIFIED",
            "denied mutation still changes balance or emits a reward -> BLOCKED_UNVERIFIED",
            "positive-only authorization tests presented as security proof -> BLOCKED_UNVERIFIED",
            "logout clears only the client token while the server session remains valid -> BLOCKED_UNVERIFIED",
            "WebSocket authenticates once but does not authorize each message -> BLOCKED_UNVERIFIED",
            "self-managed passwords use plain SHA-256 without an adaptive password hash -> BLOCKED_UNVERIFIED",
            "default or shared privileged credential remains enabled -> BLOCKED_UNVERIFIED",
            "self-managed password accepts a common or breached value -> BLOCKED_UNVERIFIED",
            "login uses TLS but an authenticated session later falls back to plaintext -> BLOCKED_UNVERIFIED",
            "bearer session secret stored in browser localStorage or sessionStorage or written to a URL or raw log -> BLOCKED_UNVERIFIED",
        )
        self.assert_contains_all(self.guide, fixtures, GUIDE)


if __name__ == "__main__":
    unittest.main()
