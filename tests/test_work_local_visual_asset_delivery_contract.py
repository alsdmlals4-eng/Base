from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"
LOCAL_STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
LOCAL_PROFILE = ROOT / "templates/project-operations/WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md"
START_CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
IMAGE_POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
VAULT_POLICY = ROOT / "docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md"
CASE = ROOT / "docs/knowledge/cases/PROJECT_LOCAL_VISUAL_ASSET_WITHOUT_NOTION_BINARY_CASE.md"


class WorkLocalVisualAssetDeliveryContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_existing_starter_routes_the_compatibility_appendix_and_start_checklist(self) -> None:
        text = self._read(STARTER)
        self.assertIn("CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md", text)
        self.assertIn("WORK_PROJECT_START_CANON_CHECKLIST.md", text)
        self.assertIn("PROJECT_START_CANON_CHECKLIST_REQUIRED", text)

    def test_thin_local_visual_starter_reuses_current_owners_and_carries_delegation(self) -> None:
        text = self._read(LOCAL_STARTER)
        for token in (
            "WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "PROJECT_LOCAL_VISUAL_BINARY_FIRST",
            "NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY",
            "NO_NOTION_BINARY_UPLOAD_REQUIRED",
            "Human usability",
            "Player Experience",
        ):
            self.assertIn(token, text)

    def test_appendix_routes_explicit_project_local_visual_binary_profile(self) -> None:
        appendix = self._read(APPENDIX)
        for token in (
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "PROJECT_LOCAL_VISUAL_BINARY_FIRST",
            "NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY",
            "NO_NOTION_BINARY_UPLOAD_REQUIRED",
            "NOTION_BINARY_DELIVERY_OPTIONAL_BY_EXPLICIT_PROJECT_POLICY",
            "NOTION_UPLOAD_NOT_RUN",
            "NO_FALSE_NOTION_UPLOAD_CLAIM",
        ):
            self.assertIn(token, appendix)

    def test_local_profile_composes_existing_visual_and_vault_owners(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for token in (
            "COMPOSE_PROJECT_LOCAL_ASSET_VAULT_NOT_SECOND_CANON",
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            "docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
        ):
            self.assertIn(token, text)
        self.assertIn("PROJECT_LOCAL_ASSET_VAULT_POLICY.md", self._read(IMAGE_POLICY))
        self.assertIn(".asset-vault/library/", self._read(VAULT_POLICY))

    def test_local_gpt_can_write_candidates_but_codex_requires_durable_promotion(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for token in (
            "LOCAL_GPT_DIRECT_PROJECT_WRITE_WHEN_CALLABLE",
            ".asset-vault/library/work-generated/",
            "LOCAL_CANDIDATE_NOT_CODEX_DURABLE_INPUT",
            "PROJECT_ASSET_APPROVED",
            "ASSET_MANIFEST.yml",
            "COMMIT_AND_REMOTE_READBACK_BEFORE_REMOTE_CODEX",
        ):
            self.assertIn(token, text)

    def test_visual_packet_records_local_paths_hash_manifest_and_durable_identity(self) -> None:
        text = self._read(LOCAL_PROFILE)
        visual_section = text.split("### 4.1 Visual production packet override", 1)[1].split(
            "### 4.2 Manifest 최소 필드", 1
        )[0]
        for field in (
            "project_local_candidate_path:",
            "project_owned_tracked_path:",
            "asset_manifest_path:",
            "sha256:",
            "durable_commit_or_artifact:",
            "notion_reference_surface:",
        ):
            self.assertIn(field, visual_section)
        self.assertNotIn("notion_destination:", visual_section)

    def test_candidate_and_runtime_promotion_are_separate_and_freshness_is_exact(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for token in (
            "LOCAL_VISUAL_CANDIDATE",
            "RUNTIME_PROMOTED",
            "EXACT_CANDIDATE_FRESHNESS",
            "EXACT_RUNTIME_CANDIDATE_FRESHNESS",
            "HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE",
            "TOOLING_TEST_DOC_ONLY_DOES_NOT_INVALIDATE_CANDIDATE",
        ):
            self.assertIn(token, text)

    def test_godot_import_cache_is_not_product_source_and_tracking_is_discovered(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for token in (
            "IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF",
            "NEVER_STAGE_GENERATED_IMPORT_NOISE",
            "PROJECT_ENGINE_POLICY_DISCOVERY_REQUIRED",
            ".godot/",
            "*.import",
            "*.uid",
        ):
            self.assertIn(token, text)
        self.assertIn("일괄 금지", text)

    def test_startup_receipt_extension_records_visual_route_and_distinct_sha_meanings(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for field in (
            "product_implementation_baseline:",
            "latest_router_or_canon_sync:",
            "visual_asset_binary_owner:",
            "project_local_candidate_root:",
            "tracked_asset_root:",
            "asset_manifest:",
            "notion_visual_reference_surface:",
            "visual_asset_durability_gap:",
        ):
            self.assertIn(field, text)
        self.assertIn("visual_audio_asset_state", text)
        self.assertIn("PROJECT_START_CANON_CHECKLIST", self._read(START_CHECKLIST))

    def test_ci_package_candidate_and_optional_heartbeat_evidence_are_separate(self) -> None:
        text = self._read(LOCAL_PROFILE)
        for token in (
            "TEST_LOGIC_PASS != CI_GATE_PASS",
            "CI_WORKFLOW_AND_ARTIFACT_CONTRACT_REQUIRED",
            "EXACT_RUNTIME_CANDIDATE_FRESHNESS",
            "COMPLETED_PR_HEARTBEAT_CLEANUP_WHEN_PRESENT",
        ):
            self.assertIn(token, text)

    def test_project_neutral_case_is_linked_without_absorbing_project_values(self) -> None:
        local_profile = self._read(LOCAL_PROFILE)
        case = self._read(CASE)
        self.assertIn(CASE.name, local_profile)
        for token in (
            "NOTION_BINARY_IS_NOT_REQUIRED_FOR_PROJECT_OWNED_VISUAL_BYTES",
            "LOCAL_ONLY_IS_NOT_DURABLE_HANDOFF",
            "CANDIDATE_FRESHNESS_FOLLOWS_PLAYER_FACING_BYTES",
        ):
            self.assertIn(token, case)
        for project_only in (
            "PR #19",
            "PR #196",
            "Task9",
            "Cheonsul",
            "HANDPAINTED_STORYBOOK_3D_DIORAMA",
            "C+강아지",
            "960×540",
        ):
            self.assertNotIn(project_only, case)

    def test_minimum_transition_and_evidence_boundaries_are_not_regressed(self) -> None:
        combined = "\n".join(
            (self._read(STARTER), self._read(LOCAL_STARTER), self._read(PROFILE), self._read(LOCAL_PROFILE))
        )
        for token in (
            "PROJECT_START_CANON_CHECKLIST_REQUIRED",
            "WORK_PREP_COMPLETION_BEFORE_CODEX",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "AUTO_LAUNCH_GODOT_WHEN_CALLABLE",
            "MACHINE_QA_FIRST",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "SCOPE_BOUNDED_REQUIRED_WORK_ZERO",
            "DO_NOT_AUTO_ADVANCE_TO_NEXT_SLICE_BEFORE_USER_VALIDATION",
        ):
            self.assertIn(token, combined)


if __name__ == "__main__":
    unittest.main()
