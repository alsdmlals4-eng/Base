from __future__ import annotations

import unittest
import json
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class VerticalSliceV9ContractTests(unittest.TestCase):
    def test_active_contract_restores_the_single_attachment_integrated_route(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        for term in (
            'contract_version: "9.1"',
            'release_line: "Base v9.3"',
            "active_authority: true",
            "SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION",
            "이 파일 하나만 첨부하면 저장소 우선 인터뷰부터 기획·Codex 인계·구현·검수·병합 후 Notion/repository readback까지",
            "APPLICATION_BINDING",
            "REPOSITORY_FIRST_INTERVIEW",
            "INTEGRATED_DELIVERY_PROFILE",
            "RECONCILIATION_PLANNING_PROFILE",
            "CONDITIONAL_RECONCILIATION",
            "모든 첨부의 기본값이 아니라",
            "PLAN_AND_CODEX_HANDOFF",
            "CANONICAL_UPDATE_AND_IMPLEMENTATION",
            "MERGE_AND_SYNC",
            "병합된 main을 기준으로만",
            "금지: 게임 코드·Scene·데이터·에셋 수정",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "LEGACY_SHEET_COMPATIBILITY_MIGRATION",
            "요청·승인·Issue/Goal 없이 제품 범위를 발명하는 구현",
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
        registry_blob = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                f"{lock['candidate_release_commit']}:skills/SKILL_REGISTRY.json",
            ],
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(lock["candidate_registry"]["sha256"], hashlib.sha256(registry_blob).hexdigest())
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

    def test_v93_candidate_preserves_v92_and_declares_the_compatibility_fix(self) -> None:
        candidate = json.loads((ROOT / "base-v9.3.lock.json").read_text(encoding="utf-8"))
        v92 = json.loads((ROOT / "base-v9.2.lock.json").read_text(encoding="utf-8"))
        contract = read("docs/operations/BASE_V9_3_RELEASE_CONTRACT.md")

        self.assertEqual(candidate["release_line"], "v9.3.0")
        self.assertEqual(candidate["release_state"], "BASE_RELEASED")
        self.assertEqual(candidate["github_issue"], 107)
        self.assertEqual(candidate["candidate_release_commit"], "30ca6c7b5f93521f0eb0eed42d01437cd43c50ae")
        self.assertEqual(candidate["candidate_release_evidence_commit"], "462a86db192d23d0f386281a1eb54b0a8cbad62e")
        self.assertEqual(v92["release_state"], "BASE_RELEASED")
        self.assertIn("does not rewrite\nthe v9.2 payload", contract)
        self.assertIn("single-attachment integrated execution behavior", contract)
        self.assertIn('"9.3.0": Path("base-v9.3.lock.json")', read("tools/project_operating_contract.py"))
        core = read("tools/project_operating_contract.py")
        self.assertIn("def latest_released_base_version", core)
        self.assertIn("selected_base_version = base_version or latest_released_base_version(base_repository)", core)
        self.assertIn("newest locally available lock with usable release and evidence pins", read("tools/migrate_project_operating_contract.py"))
        registry_blob = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                f"{candidate['candidate_release_commit']}:skills/SKILL_REGISTRY.json",
            ],
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(candidate["candidate_registry"]["sha256"], hashlib.sha256(registry_blob).hexdigest())
        self.assertTrue((ROOT / "schemas/base-v9-3-candidate-lock-v1.schema.json").is_file())
        self.assertTrue((ROOT / "schemas/base-v9-3-release-evidence-v1.schema.json").is_file())

        integrity = read("tools/check_base_v9_integrity.py")
        self.assertIn("def v93_evidence_record_errors", integrity)
        self.assertIn("def v93_release_lock_errors", integrity)
        self.assertIn("def v94_release_lock_errors", integrity)
        self.assertIn("v9.3 release evidence candidate Issue does not match the candidate lock", integrity)

    def test_visual_policy_and_skill_share_the_checkpoint_boundary(self) -> None:
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        for term in ("Intermediate visual checkpoint", "MISSING_CANON", "DRAFT_VISUAL"):
            self.assertIn(term, policy)
        for term in ("`intermediate-visual-checkpoint`", "Screen Interpretation Review", "사용자 Decision 없이"):
            self.assertIn(term, skill)

    def test_merged_main_uses_notion_and_repository_readback_not_normal_sheet_sync(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        for term in (
            "Project Notion Home",
            "Notion destination readback",
            "Google Sheets와 Figma는 migration-only historical surface",
            "병합된 **뒤에만**",
        ):
            self.assertIn(term, prompt)

        for forbidden in (
            "Google Sheet 쓰기",
            "병합 후 Google Sheet 동기화",
            "Google Sheet 구성·마지막 동기화 SHA·쓰기 권한",
        ):
            self.assertNotIn(forbidden, prompt)

    def test_user_approval_is_binding_while_nonapproval_changes_use_review_loop(self) -> None:
        prompt = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        for term in (
            "승인 요청에서 사용자가 확정한 선택은 그대로 집행한다",
            "승인 외 변경은 벤치마킹·현업 비교·충돌·누락 조사와 적대적 검토",
        ):
            self.assertIn(term, prompt)


if __name__ == "__main__":
    unittest.main()
