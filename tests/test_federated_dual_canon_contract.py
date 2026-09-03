from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
WORKSPACE_POLICY = ROOT / "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md"
MASTER_GDD_POLICY = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"

ACTIVE_ROUTING_SURFACES = (
    "AGENTS.md",
    "README.md",
    "START_HERE.md",
    "docs/OPERATING_MODEL.md",
    "docs/DOCUMENTATION_MAP.md",
    "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md",
    "docs/VISUAL_COLLABORATION_TOOL_POLICY.md",
    "docs/CONFIRMED_DECISION_SYNC_POLICY.md",
    "skills/managing-design-documents/SKILL.md",
    "templates/AGENTS.project.md",
    "templates/copilot-instructions.md",
    "templates/custom-instructions.codex.md",
    "templates/custom-instructions.gpt.md",
    "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md",
    "templates/project-operations/README.md",
    "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md",
    "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md",
)

RETIRED_ACTIVE_TOKENS = (
    "REPOSITORY_PRIMARY_CANON_WITH_DERIVED_HUMAN_PDF",
    "HUMAN_GDD_PDF_DERIVED_VIEW",
    "PDF_IS_DERIVED_SNAPSHOT_NOT_CANON",
)


def text(path: str | Path) -> str:
    candidate = path if isinstance(path, Path) else ROOT / path
    return candidate.read_text(encoding="utf-8")


class FederatedDualCanonContractTests(unittest.TestCase):
    def test_machine_contract_declares_federated_dual_canon(self) -> None:
        contract = json.loads(text(V4))

        self.assertEqual(
            "FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER",
            contract["authority_model"],
        )
        self.assertEqual(
            "FEDERATED_REPOSITORY_AND_APPROVED_PDF_CANON",
            contract["project_canon"],
        )
        self.assertEqual(
            "REPOSITORY_EXECUTION_DATA_CANON",
            contract["repository_canon"],
        )
        self.assertEqual(
            "APPROVED_HUMAN_BLUEPRINT_PDF_CANON",
            contract["human_pdf_canon"],
        )
        self.assertEqual(
            "ONE_EDITABLE_OWNER_PER_ATOMIC_FACT",
            contract["single_fact_owner"],
        )
        self.assertEqual(
            "APPROVED_PDF_IS_HUMAN_VISUAL_CANON",
            contract["pdf_policy"],
        )
        self.assertEqual(
            "CANDIDATE_PDF_NOT_CANON",
            contract["candidate_pdf_policy"],
        )

    def test_current_authority_amendment_and_consumer_route_are_explicit(self) -> None:
        contract = json.loads(text(V4))

        self.assertEqual("2026-09-04", contract["authority_model_effective_date"])
        self.assertEqual(
            "current-user-message:2026-09-04:앞으로-둘-다-정본",
            contract["authority_model_approval_ref"],
        )
        self.assertEqual(
            "APPROVED_PDF_CANON_MANIFEST_AND_HASH_READBACK",
            contract["codex_blueprint_rehydration"],
        )
        self.assertEqual(
            "NO_MASS_BACKFILL_PROJECT_ADOPTS_ON_EXPLICIT_SYNC_OR_NEXT_BLUEPRINT_REVISION",
            contract["dual_canon_adoption_policy"],
        )

    def test_pdf_canon_requires_approval_registration_and_immutable_supersession(self) -> None:
        contract = json.loads(text(V4))
        pdf = contract["human_pdf_canon_contract"]

        self.assertEqual(
            "USER_APPROVED_AND_MANIFEST_REGISTERED",
            pdf["activation"],
        )
        self.assertEqual(
            "PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION",
            pdf["structured_content"],
        )
        self.assertEqual(
            "PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION",
            pdf["annotation_policy"],
        )
        self.assertTrue(pdf["immutable_after_approval"])
        self.assertEqual(
            "APPROVED_PDF_IMMUTABLE_NEW_VERSION_REQUIRED",
            pdf["immutability_policy"],
        )
        self.assertEqual(
            "NEW_VERSION_NEW_HASH_KEEP_HISTORY",
            pdf["supersession_policy"],
        )
        self.assertEqual(
            "PROJECT_CONTROLLED_REPOSITORY_OR_GITHUB_RELEASE_LOCATOR_WITH_HASH",
            pdf["storage_policy"],
        )
        self.assertEqual(
            "CANON_CONFLICT_BLOCKS_COMPLETION_AND_RELEASE",
            pdf["conflict_gate"],
        )

        required_registration = {
            "source_commit",
            "pdf_sha256",
            "approval_ref",
            "approved_at",
            "canonical_status",
            "supersedes_pdf_ref",
            "pdf_canon_manifest_ref",
        }
        self.assertTrue(
            required_registration.issubset(set(pdf["required_registration_fields"]))
        )
        self.assertTrue(
            required_registration.issubset(
                set(contract["human_pdf_required_metadata"])
            )
        )

    def test_alignment_states_and_domain_ownership_are_explicit(self) -> None:
        contract = json.loads(text(V4))
        pdf = contract["human_pdf_canon_contract"]

        self.assertEqual(
            [
                "CANON_ALIGNED",
                "REPOSITORY_ADVANCED_PDF_REVIEW_REQUIRED",
                "PDF_FEEDBACK_PENDING_REPOSITORY_REFLECTION",
                "CANON_CONFLICT",
                "SUPERSEDED",
            ],
            pdf["alignment_states"],
        )
        self.assertIn("USER_APPROVED_VISUAL_HIERARCHY", pdf["owned_domains"])
        self.assertIn("HUMAN_REVIEW_BASELINE", pdf["owned_domains"])
        self.assertIn("CODE_AND_RUNTIME", pdf["repository_owned_domains"])
        self.assertIn("STRUCTURED_DATA_AND_IDS", pdf["repository_owned_domains"])
        self.assertIn("WORK_STATUS_AND_EVIDENCE", pdf["repository_owned_domains"])

    def test_core_policies_define_dual_canon_without_duplicate_editability(self) -> None:
        combined = "\n".join((text(WORKSPACE_POLICY), text(MASTER_GDD_POLICY)))
        for token in (
            "FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER",
            "REPOSITORY_EXECUTION_DATA_CANON",
            "APPROVED_HUMAN_BLUEPRINT_PDF_CANON",
            "ONE_EDITABLE_OWNER_PER_ATOMIC_FACT",
            "CANDIDATE_PDF_NOT_CANON",
            "USER_APPROVED_AND_MANIFEST_REGISTERED",
            "PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION",
            "PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION",
            "APPROVED_PDF_IMMUTABLE_NEW_VERSION_REQUIRED",
            "CANON_CONFLICT_BLOCKS_COMPLETION_AND_RELEASE",
        ):
            with self.subTest(token=token):
                self.assertIn(token, combined)

        self.assertIn(
            "PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION",
            text(MASTER_GDD_POLICY),
        )
        self.assertIn(
            "NO_PARALLEL_BLUEPRINT_STATUS_CANON",
            text(MASTER_GDD_POLICY),
        )

    def test_active_routes_use_new_model_without_derived_pdf_semantics(self) -> None:
        derived_same_line = re.compile(
            r"APPROVED_HUMAN_BLUEPRINT_PDF_CANON[^\n]{0,180}(?:derived|파생)",
            re.IGNORECASE,
        )

        for path in ACTIVE_ROUTING_SURFACES:
            with self.subTest(path=path):
                source = text(path)
                self.assertIn("FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER", source)
                self.assertIn("APPROVED_HUMAN_BLUEPRINT_PDF_CANON", source)
                self.assertIsNone(
                    derived_same_line.search(source),
                    f"{path} still describes the approved PDF canon as derived",
                )
                for retired in RETIRED_ACTIVE_TOKENS:
                    self.assertNotIn(retired, source)

    def test_codex_and_gpt_consumers_read_back_the_approved_pdf_manifest(self) -> None:
        for path in (
            "templates/custom-instructions.codex.md",
            "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md",
        ):
            with self.subTest(path=path):
                source = text(path)
                self.assertIn(
                    "APPROVED_PDF_CANON_MANIFEST_AND_HASH_READBACK",
                    source,
                )
                self.assertIn("pdf_canon_manifest_ref", source)
                self.assertIn("pdf_sha256", source)

        master_instruction = text(
            "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md"
        )
        self.assertIn("PDF_CANON_MANIFEST_REGISTRATION", master_instruction)
        self.assertIn(
            "USER_APPROVED_AND_MANIFEST_REGISTERED",
            master_instruction,
        )

    def test_project_templates_track_pdf_canon_identity_and_approval(self) -> None:
        decisions = text(
            "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md"
        )
        for field in (
            "pdf_source_commit:",
            "pdf_sha256:",
            "pdf_approval_ref:",
            "pdf_approved_at:",
            "pdf_canonical_status:",
            "supersedes_pdf_ref:",
            "pdf_canon_manifest_ref:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, decisions)

        project_readme = text("templates/project-operations/README.md")
        self.assertIn("USER_APPROVED_AND_MANIFEST_REGISTERED", project_readme)
        self.assertIn("pdf_sha256", project_readme)
        self.assertIn("pdf_canon_manifest_ref", project_readme)

    def test_historical_v3_contract_remains_compatibility_only(self) -> None:
        legacy = json.loads(
            text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json")
        )
        self.assertEqual(3, legacy["schema_version"])
        self.assertEqual("V3_COMPATIBILITY_AND_HISTORY_ONLY", legacy["status"])
        self.assertFalse(legacy["active_route_for_new_work"])
        self.assertEqual("NOTION_DEFAULT_PROJECT_WORKSPACE", legacy["project_workspace"])


if __name__ == "__main__":
    unittest.main()
