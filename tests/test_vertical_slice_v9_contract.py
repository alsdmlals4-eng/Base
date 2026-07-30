from __future__ import annotations

import unittest
import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class VerticalSliceV9ContractTests(unittest.TestCase):
    def test_active_contract_declares_reconciliation_only_first_wave(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        for term in (
            'contract_version: "9.0"',
            "active_authority: true",
            "APPLICATION_BINDING",
            "RECONCILIATION_PLANNING_PROFILE",
            "금지: 게임 코드·Scene·데이터·에셋 수정",
            "Google Sheet 쓰기",
            "제품 범위 PR 병합",
        ):
            self.assertIn(term, prompt)

    def test_legacy_contracts_are_classified_without_auto_replacement(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        migration = read("docs/knowledge/VERTICAL_SLICE_V8_TO_V9_MIGRATION.md")
        for term in (
            "LEGACY_REFERENCE_INPUT",
            "SUPERSEDED_COMPATIBILITY",
            "CORE_POC",
            "SLICE_VALIDATION",
            "VERTICAL_SLICE_FULL_PROFILE",
            "CANON_CONFLICT",
            "STALE_REFERENCE",
        ):
            self.assertIn(term, prompt)
            self.assertIn(term, migration)

    def test_visual_checkpoint_requires_canon_and_never_claims_delivery(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        for term in (
            "한 화면 흐름",
            "Screen Brief",
            "DRAFT_VISUAL",
            "Screen Interpretation Review",
            "MISSING_CANON",
            "VISUAL_CANONICAL_CONFLICT",
            "TECHNICAL_REVIEW_PROPOSAL",
            "최종 게임 리소스",
            "Godot 구현 완료",
            "사용자 Decision 없이는",
        ):
            self.assertIn(term, prompt)

    def test_project_application_and_packet_are_thin_and_auditable(self) -> None:
        application = read("templates/project-operations/VERTICAL_SLICE_PROJECT_APPLICATION_v9.md")
        packet = read("templates/project-operations/VERTICAL_SLICE_RECONCILIATION_PACKET_v9.md")
        for term in (
            "REFERENCE_ONLY_NO_COPY",
            "origin/main",
            "Base release commit",
            "보호 경로",
            "기본 중간 시각화 시나리오",
        ):
            self.assertIn(term, application)
        for term in (
            "Baseline Recovery Record",
            "Legacy Requirement Traceability",
            "Source / Consumer / Propagation Map",
            "Finding Ledger",
            "Readiness / Critical Gate",
            "Approval Bundle / Change Plan",
        ):
            self.assertIn(term, packet)

    def test_finalized_lock_binds_the_trusted_payload_and_evidence(self) -> None:
        lock = json.loads((ROOT / "base-v9.2.lock.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["release_line"], "v9.2.0")
        self.assertEqual(lock["release_state"], "BASE_RELEASED")
        self.assertEqual(lock["candidate_release_commit"], "648b9f60e53c4dbc7780d463be8d1bbd3a5a5e88")
        self.assertEqual(lock["candidate_release_evidence_commit"], "839154eca628084b023776f4ccf91770c344d7e6")
        self.assertEqual(
            lock["candidate_registry"]["sha256"],
            hashlib.sha256((ROOT / "skills/SKILL_REGISTRY.json").read_bytes()).hexdigest(),
        )
        release_contract = read("docs/operations/BASE_V9_2_RELEASE_CONTRACT.md")
        self.assertIn("must not self-attest", release_contract)
        self.assertIn("Projects may now pin Base v9.2", release_contract)

        core = read("tools/project_operating_contract.py")
        self.assertIn('"9.2.0": Path("base-v9.2.lock.json")', core)
        self.assertIn("release_lock_path(str(adapter[\"base_release\"][\"version\"]))", core)
        self.assertIn("candidate release/evidence pins are null or inconsistent", core)

    def test_release_evidence_records_the_merged_payload_without_finalizing_pins(self) -> None:
        lock = json.loads((ROOT / "base-v9.2.lock.json").read_text(encoding="utf-8"))
        evidence = json.loads(
            (ROOT / "docs/operations/BASE_V9_2_RELEASE_EVIDENCE.json").read_text(encoding="utf-8")
        )
        self.assertEqual(evidence["release_payload_commit"], "648b9f60e53c4dbc7780d463be8d1bbd3a5a5e88")
        self.assertEqual(evidence["candidate_registry"], lock["candidate_registry"])
        self.assertEqual(evidence["product_evidence"]["godot_runtime"], "NOT_RUN")
        self.assertEqual(evidence["release_payload_commit"], lock["candidate_release_commit"])
        self.assertTrue((ROOT / "schemas/base-v9-2-release-evidence-v1.schema.json").is_file())

    def test_visual_policy_and_skill_share_the_checkpoint_boundary(self) -> None:
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        for term in ("Intermediate visual checkpoint", "MISSING_CANON", "DRAFT_VISUAL"):
            self.assertIn(term, policy)
        for term in ("`intermediate-visual-checkpoint`", "Screen Interpretation Review", "사용자 Decision 없이"):
            self.assertIn(term, skill)


if __name__ == "__main__":
    unittest.main()
