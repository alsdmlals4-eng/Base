from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "tools/project_operating_contract.py"
BUILD = ROOT / "tools/build_project_operating_artifacts.py"
CHECK = ROOT / "tools/check_project_operating_contract.py"
MIGRATE = ROOT / "tools/migrate_project_operating_contract.py"
ADAPTER_SCHEMA = ROOT / "schemas/project-base-adapter-v1.schema.json"
SNAPSHOT_SCHEMA = ROOT / "schemas/project-skill-snapshot-v1.schema.json"
HEALTH_SCHEMA = ROOT / "schemas/project-operating-health-v1.schema.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


def commit_all(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "-c", "user.name=Base Tests", "-c", "user.email=base@example.invalid", "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


class BaseV91ProjectOperatingContractTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("project_operating_contract", CORE)
        if not CORE.exists() or spec is None or spec.loader is None:
            raise AssertionError("v9.1 project operating core is missing")
        cls.core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.core)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        self.base = self.workspace / "Base"
        self.project = self.workspace / "Project"
        self.base.mkdir()
        self.project.mkdir()
        git(self.base, "init", "-q")
        git(self.project, "init", "-q")

        (self.base / "skills/shared-skill").mkdir(parents=True)
        (self.base / "skills/shared-skill/SKILL.md").write_text(
            "---\nname: shared-skill\ndescription: Use when shared behavior is required.\n---\n\n# Shared\n",
            encoding="utf-8",
        )
        self.base_registry = self.base / "skills/SKILL_REGISTRY.json"
        self.base_registry.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "skills": [
                        {
                            "skill_id": "shared-skill",
                            "status": "ACTIVE",
                            "path": "skills/shared-skill/SKILL.md",
                        }
                    ],
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.release_commit = commit_all(self.base, "release payload")
        (self.base / "RELEASE_EVIDENCE.md").write_text("verified release evidence\n", encoding="utf-8")
        self.evidence_commit = commit_all(self.base, "release evidence")

        (self.project / "skills/local-skill").mkdir(parents=True)
        (self.project / "skills/local-skill/SKILL.md").write_text(
            "---\nname: local-skill\ndescription: Use when project-only behavior is required.\n---\n\n# Local\n",
            encoding="utf-8",
        )
        self.project_registry = self.project / "skills/SKILL_REGISTRY.json"
        self.project_registry.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "skills": [
                        {
                            "skill_id": "local-skill",
                            "status": "ACTIVE",
                            "path": "skills/local-skill/SKILL.md",
                        }
                    ],
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.project / "docs").mkdir()
        (self.project / "project.godot").write_text('[application]\nconfig/name="Project"\n', encoding="utf-8")
        (self.project / "docs/CANON.md").write_text("canon\n", encoding="utf-8")
        (self.project / "docs/PROJECT_OPERATING_HEALTH.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "artifact_role": "PROJECT_OPERATING_HEALTH",
                    "operating_maturity": "OM-L1",
                    "product_evidence_maturity": "PE-0",
                    "critical_gates": {
                        "static": "PASS",
                        "runtime": "NOT_RUN",
                        "device": "NOT_RUN",
                        "accessibility": "NOT_RUN",
                        "human": "NOT_RUN",
                    },
                    "integrity_verdict": "PASS_WITH_NOT_RUN_GATES",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.adapter = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        self.adapter.write_text(json.dumps(self.adapter_data(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.project_commit = commit_all(self.project, "project baseline")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def adapter_data(self) -> dict:
        return {
            "schema_version": 1,
            "artifact_role": "PROJECT_BASE_ADAPTER",
            "base_release": {
                "repository": "alsdmlals4-eng/Base",
                "version": "9.1.0",
                "release_commit": self.release_commit,
                "release_evidence_commit": self.evidence_commit,
            },
            "project": {
                "repository": "example/project",
                "engine": "Godot 4.7",
                "root": ".",
            },
            "routing": {
                "base_routes": [
                    {"route_id": "shared-skill", "skill_id": "shared-skill", "status": "ACTIVE"}
                ],
                "project_routes": [
                    {"route_id": "local-skill", "skill_id": "local-skill", "status": "ACTIVE"}
                ],
                "inactive_routes": [],
                "aliases": [],
                "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
            },
            "skill_registry": {
                "base": {"path": "skills/SKILL_REGISTRY.json", "sha256": digest(self.base_registry)},
                "project": {"path": "skills/SKILL_REGISTRY.json", "sha256": digest(self.project_registry)},
            },
            "shared_overrides": {},
            "gdd_sheet": {"role": "USER_FACING_GDD_WORKSPACE", "sync_status": "NOT_CONFIGURED"},
            "protected_paths": ["project.godot", "game/**", "assets/**"],
            "validators": [
                "python tools/check_project_operating_contract.py --project-root . --base-repository ../Base --check"
            ],
            "compatibility": {
                "cycle": "ONE_CYCLE",
                "views": [
                    "skills/BASE_V9_ADAPTER.json",
                    "skills/PROJECT_BASE_SKILL_ADAPTER.json",
                    "skills/PROJECT_PATH_ADAPTER.json",
                ],
            },
        }

    def run_tool(self, tool: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(tool), *args],
            cwd=self.project,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def test_schemas_and_template_define_the_canonical_contract(self) -> None:
        adapter_schema = json.loads(ADAPTER_SCHEMA.read_text(encoding="utf-8"))
        snapshot_schema = json.loads(SNAPSHOT_SCHEMA.read_text(encoding="utf-8"))
        health_schema = json.loads(HEALTH_SCHEMA.read_text(encoding="utf-8"))
        template = json.loads((ROOT / "templates/project-operations/PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))

        self.assertFalse(list(Draft202012Validator(adapter_schema).iter_errors(template)))
        self.assertEqual(
            set(adapter_schema["required"]),
            {
                "schema_version",
                "artifact_role",
                "base_release",
                "project",
                "routing",
                "skill_registry",
                "shared_overrides",
                "gdd_sheet",
                "protected_paths",
                "validators",
                "compatibility",
            },
        )
        self.assertIn("release_commit", adapter_schema["properties"]["base_release"]["required"])
        self.assertIn("release_evidence_commit", adapter_schema["properties"]["base_release"]["required"])
        for field in ("base_routes", "project_routes", "inactive_routes", "aliases", "source_registry"):
            self.assertIn(field, snapshot_schema["required"])
        self.assertEqual(health_schema["properties"]["operating_maturity"]["enum"], [f"OM-L{i}" for i in range(6)])
        self.assertEqual(health_schema["properties"]["product_evidence_maturity"]["enum"], [f"PE-{i}" for i in range(6)])

    def test_generation_is_deterministic_and_manual_edits_fail_check(self) -> None:
        args = ["--project-root", str(self.project), "--base-repository", str(self.base)]
        first = self.run_tool(BUILD, *args, "--write")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        generated = [
            self.project / "skills/PROJECT_SKILL_SNAPSHOT.json",
            self.project / "docs/PROJECT_OPERATING_DASHBOARD.html",
            self.project / "skills/BASE_V9_ADAPTER.json",
            self.project / "skills/PROJECT_BASE_SKILL_ADAPTER.json",
            self.project / "skills/PROJECT_PATH_ADAPTER.json",
        ]
        before = {path: digest(path) for path in generated}
        second = self.run_tool(BUILD, *args, "--write")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(before, {path: digest(path) for path in generated})
        checked = self.run_tool(BUILD, *args, "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

        snapshot = json.loads(generated[0].read_text(encoding="utf-8"))
        self.assertEqual(snapshot["source_registry"]["path"], "skills/PROJECT_BASE_ADAPTER.json")
        self.assertEqual(snapshot["source_registry"]["sha256"], digest(self.adapter))
        self.assertEqual(snapshot["base_routes"][0]["route_id"], "shared-skill")
        self.assertEqual(snapshot["project_routes"][0]["route_id"], "local-skill")
        for compatibility_view in generated[2:]:
            data = json.loads(compatibility_view.read_text(encoding="utf-8"))
            self.assertEqual(data["artifact_role"], "GENERATED_COMPATIBILITY_VIEW")
            self.assertEqual(data["lifecycle"], "ONE_CYCLE")

        generated[1].write_text(generated[1].read_text(encoding="utf-8") + "<!-- manual -->\n", encoding="utf-8")
        stale = self.run_tool(BUILD, *args, "--check")
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("manual", stale.stderr.lower())

    def test_validator_fails_closed_for_hashes_aliases_duplicates_and_shared_body_copying(self) -> None:
        args = ["--project-root", str(self.project), "--base-repository", str(self.base), "--check"]
        generated = self.run_tool(BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        clean = self.run_tool(CHECK, *args)
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

        cases: list[tuple[str, callable, str]] = []

        def stale_hash(data: dict) -> None:
            data["skill_registry"]["project"]["sha256"] = "0" * 64

        def alias_cycle(data: dict) -> None:
            data["routing"]["aliases"] = [
                {"alias": "a", "target": "b"},
                {"alias": "b", "target": "a"},
            ]

        def duplicate_id(data: dict) -> None:
            data["routing"]["project_routes"].append(
                {"route_id": "local-skill", "skill_id": "local-skill", "status": "ACTIVE"}
            )

        cases.extend(
            [
                ("hash", stale_hash, "hash"),
                ("alias", alias_cycle, "cycle"),
                ("duplicate", duplicate_id, "duplicate"),
            ]
        )
        original = self.adapter.read_text(encoding="utf-8")
        for label, mutation, expected in cases:
            with self.subTest(label=label):
                data = json.loads(original)
                mutation(data)
                self.adapter.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                result = self.run_tool(CHECK, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr.lower())
        self.adapter.write_text(original, encoding="utf-8")

        copied = self.project / "skills/shared-skill/SKILL.md"
        copied.parent.mkdir(parents=True)
        copied.write_bytes((self.base / "skills/shared-skill/SKILL.md").read_bytes())
        body_copy = self.run_tool(CHECK, *args)
        self.assertNotEqual(body_copy.returncode, 0)
        self.assertIn("shared skill body", body_copy.stderr.lower())

    def test_validator_enforces_pin_ancestry_stale_pin_mismatch_and_project_route_precedence(self) -> None:
        generated = self.run_tool(
            BUILD,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--write",
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        original = json.loads(self.adapter.read_text(encoding="utf-8"))

        precedence = json.loads(json.dumps(original))
        precedence["routing"]["project_routes"] = [
            {"route_id": "shared-skill", "skill_id": "local-skill", "status": "ACTIVE"}
        ]
        self.adapter.write_text(json.dumps(precedence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        built = self.run_tool(BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write")
        self.assertEqual(built.returncode, 0, built.stderr)
        snapshot = json.loads((self.project / "skills/PROJECT_SKILL_SNAPSHOT.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["effective_routes"]["shared-skill"]["source"], "PROJECT_LOCAL")

        stale = json.loads(json.dumps(original))
        stale["base_release"]["release_commit"] = "0" * 40
        self.adapter.write_text(json.dumps(stale, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        stale_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base), "--check")
        self.assertNotEqual(stale_result.returncode, 0)
        self.assertIn("pin", stale_result.stderr.lower())
        self.assertIn("refus", stale_result.stderr.lower())

        unrelated = self.workspace / "Unrelated"
        unrelated.mkdir()
        git(unrelated, "init", "-q")
        (unrelated / "x").write_text("x", encoding="utf-8")
        unrelated_commit = commit_all(unrelated, "unrelated")
        mismatch = json.loads(json.dumps(original))
        mismatch["base_release"]["release_evidence_commit"] = unrelated_commit
        self.adapter.write_text(json.dumps(mismatch, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        mismatch_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base), "--check")
        self.assertNotEqual(mismatch_result.returncode, 0)
        self.assertIn("evidence", mismatch_result.stderr.lower())
        self.assertIn("refus", mismatch_result.stderr.lower())

    def test_validator_detects_protected_path_changes(self) -> None:
        generated = self.run_tool(BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        (self.project / "project.godot").write_text("changed\n", encoding="utf-8")
        result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--check",
            "--protected-base",
            self.project_commit,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected", result.stderr.lower())
        self.assertIn("project.godot", result.stderr)

    def test_validator_rejects_duplicate_registry_ids_and_missing_required_paths(self) -> None:
        project_registry = json.loads(self.project_registry.read_text(encoding="utf-8"))
        project_registry["skills"].append(dict(project_registry["skills"][0]))
        self.project_registry.write_text(json.dumps(project_registry, sort_keys=True) + "\n", encoding="utf-8")
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["project"]["sha256"] = digest(self.project_registry)
        adapter["protected_paths"].append("missing-required.txt")
        self.adapter.write_text(json.dumps(adapter, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--check",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate skill id", result.stderr.lower())
        self.assertIn("missing-required.txt", result.stderr)

    def test_dashboard_is_static_accessible_and_keeps_maturity_axes_separate(self) -> None:
        result = self.run_tool(BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        dashboard = (self.project / "docs/PROJECT_OPERATING_DASHBOARD.html").read_text(encoding="utf-8")
        for term in (
            "lang=\"ko\"",
            "OM-L1",
            "PE-0",
            "critical-gates",
            "NOT_RUN",
            "1280",
            "1920",
            "generated",
        ):
            self.assertIn(term, dashboard)
        self.assertNotIn("average", dashboard.lower())
        self.assertNotIn("<script", dashboard.lower())

    def test_migrator_converts_legacy_inputs_without_overwriting_them(self) -> None:
        legacy = self.project / "skills/PROJECT_BASE_SKILL_ADAPTER.json"
        legacy.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "base": {"repository": "alsdmlals4-eng/Base", "commit": self.release_commit},
                    "project": {"repository": "example/project"},
                    "protected_paths": ["project.godot"],
                    "validators": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        legacy_before = legacy.read_bytes()
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        result = self.run_tool(
            MIGRATE,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--legacy-adapter",
            str(legacy),
            "--output",
            str(output),
            "--write",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(legacy_before, legacy.read_bytes())
        migrated = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(migrated["artifact_role"], "PROJECT_BASE_ADAPTER")
        self.assertEqual(migrated["base_release"]["release_commit"], self.release_commit)
        self.assertEqual(migrated["base_release"]["release_evidence_commit"], self.evidence_commit)

    def test_windows_script_runner_uses_explicit_command_array_without_shell(self) -> None:
        pub_spec = importlib.util.spec_from_file_location("publication_v3", ROOT / "tools/publication_v3.py")
        assert pub_spec and pub_spec.loader
        pub = importlib.util.module_from_spec(pub_spec)
        pub_spec.loader.exec_module(pub)
        exe = pub.safe_executable_command("C:/Poppler/pdftoppm.exe", ["-png", "input.pdf", "page"])
        cmd = pub.safe_executable_command("C:/Tools/pdftoppm.cmd", ["-png", "input.pdf", "page"])
        bat = pub.safe_executable_command("C:/Tools/pdftoppm.bat", ["-png", "input.pdf", "page"])
        self.assertEqual(exe[0], "C:/Poppler/pdftoppm.exe")
        self.assertEqual(exe[1:], ["-png", "input.pdf", "page"])
        self.assertTrue(Path(cmd[0]).name.lower() in {"cmd.exe", "cmd"})
        self.assertEqual(cmd[1:4], ["/d", "/s", "/c"])
        self.assertEqual(bat[1:4], ["/d", "/s", "/c"])
        source = (ROOT / "tools/publication_v3.py").read_text(encoding="utf-8")
        self.assertNotIn("shell=True", source)

    def test_governance_docs_ci_and_router_cover_v91_contract(self) -> None:
        combined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                "docs/operations/BASE_V9_1_SYSTEM_MAP.md",
                "docs/operations/BASE_V9_1_MATURITY_MODEL.md",
                "docs/operations/BASE_V9_1_DASHBOARD_CONTRACT.md",
                "docs/operations/BASE_V9_1_RELEASE_CONTRACT.md",
                "skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md",
                "docs/knowledge/OPEN_SOURCE_GODOT_UI_REFERENCE_CATALOG.md",
            )
        )
        for term in (
            "OM-L0",
            "OM-L5",
            "PE-0",
            "PE-5",
            "never average",
            "Godot 4.7",
            "Control",
            "Container",
            "Theme",
            "focus",
            "long Korean",
            "1280x720",
            "1920x1080",
            "Maaack",
            "MIT",
            "Kenney",
            "CC0",
            "patterns only",
            "DEFERRED_UNTIL_RELEASE_ARTIFACT",
        ):
            self.assertIn(term, combined)

        router = (ROOT / "templates/project-operations/.agents/skills/base-project-router/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT_BASE_ADAPTER.json", router)
        self.assertIn("PROJECT_SKILL_SNAPSHOT.json", router)
        self.assertNotIn("shared Skill body", router)

        workflows = list((ROOT / ".github/workflows").glob("*.yml"))
        action_uses = []
        for workflow in workflows:
            text = workflow.read_text(encoding="utf-8")
            if "uses: actions/" in text:
                self.assertIn("permissions:\n  contents: read", text, workflow.name)
            action_uses.extend(line.strip() for line in text.splitlines() if "uses: actions/" in line)
        for action in action_uses:
            ref = action.rsplit("@", 1)[1].split()[0]
            self.assertRegex(ref, r"^[0-9a-f]{40}$")
        dependency = (ROOT / ".github/workflows/dependency-review.yml").read_text(encoding="utf-8")
        self.assertIn("dependency-review-action", dependency)
        self.assertIn("pull_request", dependency)

    def test_v91_has_a_separate_candidate_lock_without_rewriting_v90(self) -> None:
        schema = json.loads((ROOT / "schemas/base-v9-1-candidate-lock-v1.schema.json").read_text(encoding="utf-8"))
        candidate = json.loads((ROOT / "base-v9.1.lock.json").read_text(encoding="utf-8"))
        self.assertFalse(list(Draft202012Validator(schema).iter_errors(candidate)))
        self.assertEqual(candidate["artifact_role"], "BASE_V9_1_RELEASE_CANDIDATE_LOCK")
        self.assertEqual(candidate["release_line"], "v9.1.0")
        self.assertEqual(candidate["release_state"], "RELEASE_CANDIDATE")
        self.assertEqual(candidate["github_issue"], 71)
        self.assertIsNone(candidate["candidate_release_commit"])
        self.assertIsNone(candidate["candidate_release_evidence_commit"])
        self.assertEqual(candidate["binary_attestation"], "DEFERRED_UNTIL_RELEASE_ARTIFACT")
        self.assertEqual(candidate["compatibility_base"]["release_line"], "v9.0.0")
        self.assertEqual(
            candidate["compatibility_base"]["release_commit"],
            "585a53a25be1b04c543196f5901551deb49c7691",
        )
        v90 = json.loads((ROOT / "base.lock.json").read_text(encoding="utf-8"))
        self.assertEqual(v90["release_line"], "v9.0.0")
        self.assertEqual(v90["release_state"], "BASE_RELEASED")


if __name__ == "__main__":
    unittest.main()
