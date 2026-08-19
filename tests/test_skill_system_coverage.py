from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "check_skill_system_coverage",
    ROOT / "tools/check_skill_system_coverage.py",
)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


def package_text(skill_id: str) -> str:
    skill_dir = ROOT / "skills" / skill_id
    paths = [skill_dir / "SKILL.md"]
    references = skill_dir / "references"
    if references.is_dir():
        paths.extend(sorted(path for path in references.rglob("*") if path.is_file()))
    return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in paths)


def load_archive_validator():
    path = ROOT / "templates/project-operations/github/check_archive_governance.py"
    module_spec = importlib.util.spec_from_file_location("check_archive_governance", path)
    module = importlib.util.module_from_spec(module_spec)
    assert module_spec.loader is not None
    module_spec.loader.exec_module(module)
    return module


class SkillSystemCoverageTests(unittest.TestCase):
    def test_source_responsibilities_are_mapped_to_active_skills(self) -> None:
        self.assertEqual(checker.validate(), [])

    def test_requested_independent_skills_remain_distinct_and_optional(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        required = {
            "refactoring-with-contract-preservation",
            "simplifying-skill-bodies",
            "pruning-stale-and-nonfunctional-material",
            "synchronizing-local-and-github-state",
            "maintaining-long-running-task-continuity",
            "governing-game-user-research-coverage",
            "creating-user-learning-notes",
            "building-project-visual-dashboards",
            "diagnosing-game-engine-runtime-failures",
            "governing-legacy-retention-and-archives",
        }
        self.assertTrue(required.issubset(by_id))
        for skill_id in required:
            self.assertEqual(by_id[skill_id]["status"], "ACTIVE")
            self.assertFalse(by_id[skill_id]["load_by_default"], skill_id)
            self.assertTrue(by_id[skill_id]["trigger_tags"], skill_id)
            self.assertTrue(by_id[skill_id]["use_when"], skill_id)
            self.assertTrue(by_id[skill_id]["do_not_use_when"], skill_id)

    def test_github_sync_routes_missing_optional_cli_to_connector(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "synchronizing-local-and-github-state"
        )

        self.assertTrue(
            {
                "github-cli-missing",
                "gh-auth-missing",
                "github-connector-fallback",
            }.issubset(entry["trigger_tags"])
        )
        self.assertTrue(any("connector" in value and "gh" in value for value in entry["use_when"]))

        skill = package_text("synchronizing-local-and-github-state")
        for token in (
            "GITHUB_CAPABILITY_FALLBACK",
            "MISSING_OPTIONAL_CLI",
            "BLOCKED_UNVERIFIED",
            "update_ref(force=false)",
            "PROVISIONAL_INTEGRATION",
            "owner_pr_head_shas",
            "provisional_overlap_paths",
            "provisional_semantic_resources",
            "explicit user authorization",
            "owner PR branches",
            "semantic reconciliation",
            "must not merge",
        ):
            self.assertIn(token, skill)

    def test_games_user_research_contract_has_exactly_eleven_domains(self) -> None:
        text = (ROOT / "skills/governing-game-user-research-coverage/SKILL.md").read_text(encoding="utf-8")
        numbered = [
            line for line in text.splitlines()
            if re.match(r"^(?:[1-9]|10|11)\. ", line)
        ]
        self.assertEqual(len(numbered), 11)
        self.assertTrue(numbered[0].startswith("1. "))
        self.assertTrue(numbered[-1].startswith("11. "))

    def test_optimized_existing_skills_preserve_legacy_capabilities(self) -> None:
        required_terms = {
            "identifying-project-core": (
                "PROJECT_CORE", "CORE_SUPPORT", "MVP_SUPPORT", "CONTENT_VARIANT",
                "PRESENTATION_SHELL", "TECHNICAL_FOUNDATION", "candidate:",
                "dependents:", "CORE", "BOTH", "LATER", "IDENTIFIED", "PARTIAL",
                "CONFLICTED", "UNVERIFIED", "저장·호환성", "읽기 전용",
            ),
            "establishing-project-core": (
                "CORE_SEED", "CORE_PROPOSED", "CORE_STRESS_TESTED", "CORE_CONFIRMED",
                "CORE_REVISE", "CORE_REJECTED", "CORE_RECORDED", "INVARIANT",
                "CHANGEABLE", "REQUIRES_REAPPROVAL", "OUT_OF_SCOPE", "사용자 승인",
                "PoC·플레이테스트", "마이그레이션",
            ),
            "running-adversarial-review-and-refinement": (
                "작성자·블루팀", "레드팀", "검증자", "개선자", "회귀 검토자",
                "finding_id", "MUST_FIX", "SHOULD_FIX", "DEFER", "REJECT",
                "UNVERIFIED", "PASS_WITH_FOLLOWUP", "REVISE_AGAIN", "REJECT_CHANGE",
                "CRITICAL", "Schema", "롤백",
            ),
            "evolving-project-discipline-skills": (
                "Consolidation-first", "기존 통합 Skill의 mode", "load_all_skills",
                "automatic_selection", "require_trigger_match", "max_primary_discipline_skills",
                "max_foundation_skills", "LEGACY_SKILL_ALIASES.md", "OBSERVATION",
                "HYPOTHESIS", "PATTERN", "VERIFIED", "PROMOTION_CANDIDATE",
                "untouched 소비자",
            ),
            "analyzing-and-refining-game-concepts": (
                "`frame`", "`constrain`", "`sharpen`", "`structure`",
                "`benchmark-and-player-research`", "`playtest-and-experiment`",
                "`poc-contract`", "`recalibrate`", "`production-gate`", "BIG BLIND",
                "AMPLIFY", "SUPPORT", "NEUTRAL", "CONFLICT", "UNPROVEN",
                "Action-feedback latency", "Reward legibility", "Reward ladder",
                "Fatigue and inflation", "feedback_channel", "telemetry_events",
                "funnel_steps", "control_and_variants", "ADOPT", "ADAPT", "AVOID",
                "TEST", "IGNORE", "KEEP", "REMOVE", "RETEST", "PRODUCTION_READY",
                "REPEAT_VERTICAL_SLICE", "TECHNICAL_SPIKE_INTERNAL_ONLY",
                "RELEASE_NEAR_VERTICAL_SLICE_FIRST", "HOLD", "STOP",
            ),
        }
        for skill_id, terms in required_terms.items():
            text = package_text(skill_id)
            for term in terms:
                self.assertIn(term, text, f"{skill_id} lost contract term: {term}")

    def test_optimization_report_and_machine_coverage_exist(self) -> None:
        self.assertTrue((ROOT / "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md").is_file())
        self.assertTrue((ROOT / "docs/SKILL_COVERAGE_MAP.md").is_file())
        self.assertTrue((ROOT / "skills/SKILL_COVERAGE.json").is_file())

    def test_base_v94_ai_operations_have_distinct_registry_boundaries(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        model = by_id["optimizing-ai-model-and-prompt-costs"]
        self.assertEqual("skills/optimizing-ai-model-and-prompt-costs/SKILL.md", model["path"])
        self.assertEqual("ACTIVE", model["status"])
        self.assertFalse(model["load_by_default"])
        self.assertTrue({"model-recommendation", "prompt-caching", "provider-profile"}.issubset(model["trigger_tags"]))

        intake = by_id["managing-project-intake-and-work-contract"]
        simplifying = by_id["simplifying-skill-bodies"]
        ui = by_id["auditing-and-refining-ui-art"]
        self.assertIn("instruction-authority", intake["trigger_tags"])
        self.assertIn("example-as-fixture", simplifying["trigger_tags"])
        self.assertIn("ui-motion-design", ui["trigger_tags"])
        self.assertNotIn("designing-ai-instructions", by_id)
        self.assertNotIn("designing-ui-motion", by_id)

    def test_bcp008_uses_existing_owners_without_new_active_skill(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        self.assertNotIn("managing-feature-traceability", by_id)
        self.assertNotIn("procuring-external-ui", by_id)
        for skill_id in (
            "managing-project-intake-and-work-contract",
            "managing-design-documents",
            "reviewing-and-validating-project-changes",
            "running-adversarial-review-and-refinement",
            "auditing-and-refining-ui-art",
        ):
            self.assertEqual("ACTIVE", by_id[skill_id]["status"])
        self.assertEqual([], checker.validate())



class LegacyRetentionArchiveGovernanceTests(unittest.TestCase):
    def test_archive_contract_files_exist(self) -> None:
        required = (
            "skills/governing-legacy-retention-and-archives/references/archive-contract.md",
            "schemas/archive-retention-adapter-v1.schema.json",
            "schemas/archive-manifest-v1.schema.json",
            "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",
            "templates/project-operations/ARCHIVE_MANIFEST.json",
            "templates/project-operations/ARCHIVE_README.md",
            "templates/project-operations/github/check_archive_governance.py",
        )
        self.assertEqual([], [path for path in required if not (ROOT / path).is_file()])

    def test_archive_skill_preserves_body_and_removes_authority(self) -> None:
        skill = package_text("governing-legacy-retention-and-archives")
        for token in (
            "원문을 비우지 않는다",
            "CURRENT_AUTHORITY",
            "COMPATIBILITY_ONLY",
            "EVIDENCE_RETENTION",
            "GENERATED_DERIVATIVE",
            "DELETE_PROHIBITED_SECRET",
            "active_authority: false",
            "implementation_authority: NONE",
            "unique commit 감사",
        ):
            self.assertIn(token, skill)
        simplifying = package_text("simplifying-skill-bodies")
        for term in ("줄 수", "문자 수", "분량 상한", "내용 보존", "한 단계 발견성"):
            self.assertIn(term, simplifying)

    def test_shared_route_declares_archive_roles_schemas_and_templates(self) -> None:
        routes = json.loads((ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json").read_text(encoding="utf-8"))
        legacy = next(
            item for item in routes["shared_skills"]
            if item["skill_id"] == "governing-legacy-retention-and-archives"
        )
        for role in ("archive_readme", "archive_manifest", "generated_derivative_roots", "protected_evidence_roots"):
            self.assertIn(role, legacy["project_adapter_roles"])
        self.assertEqual(
            legacy["schemas"],
            ["schemas/archive-retention-adapter-v1.schema.json", "schemas/archive-manifest-v1.schema.json"],
        )
        self.assertIn("templates/project-operations/ARCHIVE_README.md", legacy["templates"])

    def test_adapter_and_manifest_templates_match_schemas(self) -> None:
        for schema_path, instance_path in (
            ("schemas/archive-retention-adapter-v1.schema.json", "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json"),
            ("schemas/archive-manifest-v1.schema.json", "templates/project-operations/ARCHIVE_MANIFEST.json"),
        ):
            with self.subTest(instance=instance_path):
                schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
                instance = json.loads((ROOT / instance_path).read_text(encoding="utf-8"))
                errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
                self.assertEqual([], [error.message for error in errors])

    def test_adapter_schema_rejects_blank_and_secret_archival(self) -> None:
        schema = json.loads((ROOT / "schemas/archive-retention-adapter-v1.schema.json").read_text(encoding="utf-8"))
        adapter = json.loads((ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
        adapter["policies"]["blank_placeholders_allowed"] = True
        adapter["policies"]["secrets_may_be_archived"] = True
        self.assertGreaterEqual(len(list(Draft202012Validator(schema).iter_errors(adapter))), 2)

    def test_manifest_schema_rejects_authoritative_archive_record(self) -> None:
        schema = json.loads((ROOT / "schemas/archive-manifest-v1.schema.json").read_text(encoding="utf-8"))
        manifest = {
            "schema_version": 1,
            "manifest_role": "project-archive-retention-index",
            "records": [{
                "archive_id": "old-plan",
                "classification": "ARCHIVE_HISTORY",
                "original_path": "docs/old-plan.md",
                "current_path": "docs/archive/old-plan.md",
                "content_sha256": "a" * 64,
                "archived_at": "2026-07-25",
                "superseded_by": ["docs/current-plan.md"],
                "reason": "superseded",
                "active_authority": True,
                "implementation_authority": "CURRENT",
                "compatibility_consumers": [],
                "rollback_ref": "a" * 40,
                "validation_status": "PASS",
            }],
        }
        self.assertGreaterEqual(len(list(Draft202012Validator(schema).iter_errors(manifest))), 2)

    def test_validator_passes_template_mode_and_requires_project_pin(self) -> None:
        validator = load_archive_validator()
        adapter = ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json"
        manifest = ROOT / "templates/project-operations/ARCHIVE_MANIFEST.json"
        self.assertEqual([], validator.validate_archive_governance(ROOT, adapter, manifest, require_pinned_commit=False))
        self.assertIn(
            "project adapter must pin an exact 40-character Base commit",
            validator.validate_archive_governance(ROOT, adapter, manifest),
        )

    def test_validator_rejects_empty_archived_markdown(self) -> None:
        validator = load_archive_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "docs/archive").mkdir(parents=True)
            for name in ("archive-retention-adapter-v1.schema.json", "archive-manifest-v1.schema.json"):
                (root / "schemas" / name).write_text((ROOT / "schemas" / name).read_text(encoding="utf-8"), encoding="utf-8")
            for relative, text in (
                ("AGENTS.md", "agents"),
                ("docs/DOCUMENTATION_MAP.md", "map"),
                ("docs/ACTIVE_CONTEXT.md", "context"),
                ("skills/SKILL_REGISTRY.json", "{}"),
                ("docs/current.md", "current"),
                ("docs/archive/README.md", "archive"),
                ("docs/archive/empty.md", "---\narchive_metadata: true\n---\n"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            adapter = json.loads((ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
            adapter["base"]["commit"] = "a" * 40
            adapter["project"]["repository"] = "owner/test"
            adapter["paths"].update({
                "documentation_map": "docs/DOCUMENTATION_MAP.md",
                "active_context": "docs/ACTIVE_CONTEXT.md",
                "canonical_sources": ["docs/current.md"],
                "archive_root": "docs/archive",
                "archive_readme": "docs/archive/README.md",
                "archive_manifest": "docs/archive/MANIFEST.json",
                "legacy_search_roots": ["docs"],
                "protected_evidence_roots": [],
            })
            manifest = {
                "schema_version": 1,
                "manifest_role": "project-archive-retention-index",
                "records": [{
                    "archive_id": "empty",
                    "classification": "ARCHIVE_HISTORY",
                    "original_path": "docs/empty.md",
                    "current_path": "docs/archive/empty.md",
                    "content_sha256": "a" * 64,
                    "archived_at": "2026-07-25",
                    "superseded_by": ["docs/current.md"],
                    "reason": "test",
                    "active_authority": False,
                    "implementation_authority": "NONE",
                    "compatibility_consumers": [],
                    "rollback_ref": "a" * 40,
                    "validation_status": "NOT_RUN",
                }],
            }
            adapter_path = root / "adapter.json"
            manifest_path = root / "docs/archive/MANIFEST.json"
            adapter_path.write_text(json.dumps(adapter), encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertIn(
                "archived Markdown body is empty: docs/archive/empty.md",
                validator.validate_archive_governance(root, adapter_path, manifest_path),
            )


if __name__ == "__main__":
    unittest.main()
