from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def archived_body(text: str) -> str:
    if not text.startswith("---\n"):
        raise AssertionError("Archive document must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError("Archive document frontmatter is not closed")
    return parts[2].lstrip("\n")


class V9GovernanceDocumentTests(unittest.TestCase):
    def test_ui_reference_card_covers_open_source_adoption_and_godot_contract(self) -> None:
        card = read("templates/research/UX_UI_REFERENCE_CARD.md")
        for field in (
            "license",
            "commercial_use",
            "attribution",
            "modification_and_redistribution",
            "godot_compatibility",
            "maintenance",
            "dependency_removal",
            "copying_prohibited",
            "transformation_and_validation",
        ):
            self.assertIn(field, card)
        godot = read("skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md")
        for term in ("Control", "Container", "Theme", "Signal", "focus", "Korean", "resolution"):
            self.assertIn(term, godot)

    def test_common_project_adoption_order_is_explicitly_held(self) -> None:
        order = read("templates/prompts/BASE_V9_COMMON_PROJECT_ADOPTION_WORK_ORDER.md")
        for project in ("Ten Paces: Hidden Moves", "Blacksmith", "OMENWARD", "urban-legend", "GRIMOIRE"):
            self.assertIn(project, order)
        for prerequisite in ("Base v9.0.0 lock", "repository audit", "Sheet access", "user approval", "verification environment"):
            self.assertIn(prerequisite, order)
        self.assertIn("[보류]", order)
        self.assertIn("No Sheet write", order)

    def test_release_design_plan_and_integrity_audit_keep_dispositions_and_evidence_visible(self) -> None:
        design = read("docs/operations/BASE_V9_RELEASE_DESIGN.md")
        implementation = read("docs/operations/BASE_V9_IMPLEMENTATION_PLAN.md")
        audit = read("docs/operations/BASE_V9_INTEGRITY_AUDIT.md")
        for term in ("Registry", "frontmatter", "generated", "Base Adapter", "project-specific"):
            self.assertIn(term, design)
        self.assertIn("POST_RELEASE_PROJECT_ADOPTION_WAVE", implementation)
        for disposition in ("KEEP", "CONSOLIDATE", "ARCHIVE", "RETIRE", "BLOCKED"):
            self.assertIn(disposition, audit)
        for check in ("link", "orphan", "cycle", "provenance", "template consumer"):
            self.assertIn(check, audit)

    def test_v9_focused_workflow_preserves_contract_and_adversarial_evidence(self) -> None:
        workflow = read(".github/workflows/validate-base-v9-rc.yml")
        for term in (
            "docs/**",
            "tools/**",
            ".github/workflows/**",
            "base-v9-contract:",
            "adversarial-gate:",
        ):
            self.assertIn(term, workflow)
        self.assertNotIn("\n  ci-gate:", workflow)
        self.assertIn("check_base_v9_integrity.py", workflow)

    def test_cross_project_handoff_is_archived_without_active_authority(self) -> None:
        archive_path = "docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md"
        manifest_path = "docs/archive/ARCHIVE_MANIFEST.json"
        audit_path = "docs/operations/BASE_REPOSITORY_INTEGRITY_AUDIT_2026-07-30.md"
        stub = read("docs/ACTIVE_HANDOFF.md")
        archive_file = ROOT / archive_path

        self.assertTrue(archive_file.is_file(), archive_path)
        self.assertTrue((ROOT / "docs/archive/README.md").is_file())
        self.assertTrue((ROOT / manifest_path).is_file(), manifest_path)
        self.assertTrue((ROOT / audit_path).is_file(), audit_path)
        archive = archive_file.read_text(encoding="utf-8")
        archive_readme = read("docs/archive/README.md")
        manifest = json.loads(read(manifest_path))
        documentation_map = read("docs/DOCUMENTATION_MAP.md")
        audit = read(audit_path)

        for term in ("COMPATIBILITY_ONLY", archive_path, "프로젝트 저장소"):
            self.assertIn(term, stub)
        self.assertNotIn("| `Blacksmith` |", stub)

        for term in (
            "status: SUPERSEDED",
            "original_path: docs/ACTIVE_HANDOFF.md",
            "active_authority: false",
            "implementation_authority: NONE",
            "rollback_ref: dc98a666563b1f0f87b665eac97dbd8a8be37576",
            "# UX/UI 공용 체계 확산 Active Handoff",
        ):
            self.assertIn(term, archive)

        for term in ("기본 콜드 스타트", "active_authority: false", "ARCHIVE_MANIFEST.json"):
            self.assertIn(term, archive_readme)

        self.assertEqual(manifest["schema_version"], 1)
        record = manifest["records"][0]
        self.assertEqual(record["archive_id"], "BASE-ARCHIVE-2026-07-29-UX-UI-HANDOFF")
        self.assertEqual(record["classification"], "ARCHIVE_HISTORY")
        self.assertEqual(record["original_path"], "docs/ACTIVE_HANDOFF.md")
        self.assertEqual(record["current_path"], archive_path)
        self.assertFalse(record["active_authority"])
        self.assertEqual(record["implementation_authority"], "NONE")
        self.assertEqual(record["rollback_ref"], "dc98a666563b1f0f87b665eac97dbd8a8be37576")

        actual_hash = hashlib.sha256(archived_body(archive).encode("utf-8")).hexdigest()
        self.assertEqual(record["content_sha256"], actual_hash)
        self.assertIn(f"content_sha256: {actual_hash}", archive)
        for consumer in record["compatibility_consumers"]:
            consumer_text = read(consumer)
            self.assertIn(archive_path, consumer_text)
            self.assertIn("COMPATIBILITY_ONLY", consumer_text)

        self.assertIn(archive_path, documentation_map)
        self.assertIn("COMPATIBILITY_ONLY", documentation_map)
        for term in ("DEC-2026-07-30-001", archive_path, "ARCHIVE_HISTORY", "PR #72"):
            self.assertIn(term, audit)

    def test_schema_v3_audits_are_archived_as_non_authoritative_evidence(self) -> None:
        manifest = json.loads(read("docs/archive/ARCHIVE_MANIFEST.json"))
        records = {record["archive_id"]: record for record in manifest["records"]}
        expected = {
            "base-archive-2026-07-19-schema-v3-read-only-audit": (
                "docs/audits/2026-07-19-base-schema-v3-read-only-audit.md",
                "docs/archive/audits/2026-07-19-base-schema-v3-read-only-audit.md",
            ),
            "base-archive-2026-07-19-schema-v3-final-audit": (
                "docs/audits/2026-07-19-base-schema-v3-final-audit.md",
                "docs/archive/audits/2026-07-19-base-schema-v3-final-audit.md",
            ),
        }

        for archive_id, (original_path, archive_path) in expected.items():
            with self.subTest(archive_id=archive_id):
                self.assertFalse((ROOT / original_path).exists(), original_path)
                archived = ROOT / archive_path
                self.assertTrue(archived.is_file(), archive_path)
                record = records[archive_id]
                self.assertEqual(record["classification"], "EVIDENCE_RETENTION")
                self.assertEqual(record["original_path"], original_path)
                self.assertEqual(record["current_path"], archive_path)
                self.assertFalse(record["active_authority"])
                self.assertEqual(record["implementation_authority"], "NONE")
                body = archived_body(archived.read_text(encoding="utf-8"))
                self.assertEqual(
                    record["content_sha256"],
                    hashlib.sha256(body.encode("utf-8")).hexdigest(),
                )

    def test_skills_readme_is_a_registry_router_not_a_manual_legacy_skill_table(self) -> None:
        readme = read("skills/README.md")

        for term in (
            "skills/SKILL_REGISTRY.json",
            "docs/generated/BASE_ACTIVE_SKILLS.md",
            "skills/LEGACY_SKILL_ALIASES.md",
            "load_all_skills",
            "automatic-trigger-match",
        ):
            self.assertIn(term, readme)

        self.assertNotIn("| 스킬 | Trigger |", readme)
        for legacy_id in (
            "conducting-deep-requirement-interviews",
            "transforming-requests-into-prompts",
            "writing-game-design-documents",
            "reviewing-external-ai-drafts",
            "promoting-project-knowledge",
            "reviewing-and-implementing-base-change-proposals",
        ):
            self.assertNotIn(f"| `{legacy_id}` |", readme)

    def test_agent_metadata_lives_under_the_active_integrated_skill_package(self) -> None:
        active_path = ROOT / "skills/managing-project-intake-and-work-contract/agents/openai.yaml"
        legacy_path = ROOT / "skills/conducting-deep-requirement-interviews/agents/openai.yaml"

        self.assertTrue(active_path.is_file(), active_path.relative_to(ROOT).as_posix())
        self.assertFalse(legacy_path.exists(), legacy_path.relative_to(ROOT).as_posix())

        metadata = active_path.read_text(encoding="utf-8")
        for term in (
            "프로젝트 요청·결정 계약",
            "$managing-project-intake-and-work-contract",
            "저장소 사실",
            "사용자 결정",
            "실행 계약",
        ):
            self.assertIn(term, metadata)
        self.assertNotIn("$conducting-deep-requirement-interviews", metadata)

    def test_pre_release_integrity_audit_is_marked_as_historical_after_release(self) -> None:
        audit = read("docs/operations/BASE_V9_INTEGRITY_AUDIT.md")
        for term in (
            "HISTORY_ONLY",
            "release_evidence_snapshot",
            "docs/BASE_RULES_VERSION.md",
            "docs/operations/BASE_V9_RELEASE_CONTRACT.md",
            "BASE_RELEASED",
            "Status before final verification",
        ):
            self.assertIn(term, audit)


if __name__ == "__main__":
    unittest.main()
