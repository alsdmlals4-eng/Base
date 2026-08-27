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


def policy_digest(paths: list[str]) -> str:
    content = (json.dumps(paths, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return hashlib.sha256(content).hexdigest()


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
        pinned_registry = subprocess.run(
            ["git", "-C", str(self.base), "show", f"{self.evidence_commit}:skills/SKILL_REGISTRY.json"],
            capture_output=True,
            check=True,
        ).stdout
        self.pinned_base_registry_sha = hashlib.sha256(pinned_registry).hexdigest()
        self.candidate_lock = self.base / "base-v9.1.lock.json"
        self.candidate_lock.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "artifact_role": "BASE_V9_1_RELEASE_CANDIDATE_LOCK",
                    "release_line": "v9.1.0",
                    "release_state": "RELEASE_CANDIDATE",
                    "repository": "alsdmlals4-eng/Base",
                    "candidate_release_commit": self.release_commit,
                    "candidate_release_evidence_commit": self.evidence_commit,
                    "candidate_registry": {
                        "hash_definition": "RAW_FILE_BYTES_SHA256",
                        "path": "skills/SKILL_REGISTRY.json",
                        "sha256": self.pinned_base_registry_sha,
                    },
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

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
        (self.project / "evidence").mkdir()
        (self.project / "project.godot").write_text('[application]\nconfig/name="Project"\n', encoding="utf-8")
        (self.project / "docs/CANON.md").write_text("canon\n", encoding="utf-8")
        self.operating_evidence = self.project / "evidence/adapter-installed.txt"
        self.static_evidence = self.project / "evidence/static-contract-check.txt"
        self.operating_evidence.write_text("adapter installed\n", encoding="utf-8")
        self.static_evidence.write_text("static contract passed\n", encoding="utf-8")
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
                    "evidence": {
                        "operating": [
                            {
                                "id": "adapter",
                                "source": "evidence/adapter-installed.txt",
                                "sha256": digest(self.operating_evidence),
                            }
                        ],
                        "product": [],
                        "sheet": [],
                        "gates": {
                            "static": [
                                {
                                    "id": "static",
                                    "source": "evidence/static-contract-check.txt",
                                    "sha256": digest(self.static_evidence),
                                }
                            ],
                            "runtime": [],
                            "device": [],
                            "accessibility": [],
                            "human": [],
                        },
                    },
                    "integrity_verdict": "PASS_WITH_NOT_RUN_GATES",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.legacy_adapter = self.project / "skills/LEGACY_PROJECT_ADAPTER.json"
        self.legacy_adapter.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "base": {"repository": "alsdmlals4-eng/Base", "commit": self.release_commit},
                    "project": {"repository": "example/project", "engine": "Godot 4.7"},
                    "protected_paths": ["project.godot", "game/**", "assets/**"],
                    "validators": [],
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.protected_baseline_commit = commit_all(self.project, "pre-migration protected baseline")
        git(self.project, "update-ref", "refs/remotes/origin/main", self.protected_baseline_commit)
        self.protected_policy_hash = policy_digest(["project.godot", "game/**", "assets/**"])
        self.adapter = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        adapter = self.adapter_data()
        project_registry_blob = subprocess.run(
            ["git", "-C", str(self.project), "show", f"{self.protected_baseline_commit}:skills/SKILL_REGISTRY.json"],
            capture_output=True,
            check=True,
        ).stdout
        adapter["skill_registry"]["project"]["sha256"] = hashlib.sha256(project_registry_blob).hexdigest()
        self.adapter.write_text(json.dumps(adapter, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.project_commit = commit_all(self.project, "install v9.1 adapter")

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
                "base": {
                    "path": "skills/SKILL_REGISTRY.json",
                    "sha256": self.pinned_base_registry_sha,
                    "hash_definition": "RAW_FILE_BYTES_SHA256",
                },
                "project": {
                    "path": "skills/SKILL_REGISTRY.json",
                    "sha256": digest(self.project_registry),
                    "hash_definition": "RAW_FILE_BYTES_SHA256",
                },
            },
            "shared_overrides": {},
            "gdd_sheet": {"role": "USER_FACING_GDD_WORKSPACE", "sync_status": "NOT_CONFIGURED"},
            "protected_baseline": {
                "authority_kind": "REMOTE_TRACKING_REF",
                "authority_ref": "refs/remotes/origin/main",
                "commit": self.protected_baseline_commit,
                "policy_source_type": "FIRST_MIGRATION_LEGACY_SOURCE",
                "policy_source_path": "skills/LEGACY_PROJECT_ADAPTER.json",
                "protected_paths_pointer": "/protected_paths",
                "policy_sha256": self.protected_policy_hash,
            },
            "protected_paths": ["project.godot", "game/**", "assets/**"],
            "validators": [
                "python tools/check_project_operating_contract.py --project-root . --base-repository ../Base --check"
            ],
            "compatibility": {
                "cycle": "ONE_CYCLE",
                "views": [],
                "legacy_inputs": {},
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
                "protected_baseline",
                "protected_paths",
                "validators",
                "compatibility",
            },
        )
        self.assertIn("release_commit", adapter_schema["properties"]["base_release"]["required"])
        self.assertIn("release_evidence_commit", adapter_schema["properties"]["base_release"]["required"])
        self.assertEqual(
            template["protected_baseline"]["policy_source_type"],
            "FIRST_MIGRATION_LEGACY_SOURCE",
        )
        self.assertRegex(template["protected_baseline"]["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(template["protected_baseline"]["policy_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(template["protected_baseline"]["authority_kind"], "REMOTE_TRACKING_REF")
        self.assertEqual(template["protected_baseline"]["authority_ref"], "refs/remotes/origin/main")
        for field in ("base_routes", "project_routes", "inactive_routes", "aliases", "source_registry"):
            self.assertIn(field, snapshot_schema["required"])
        self.assertEqual(health_schema["properties"]["operating_maturity"]["enum"], [f"OM-L{i}" for i in range(6)])
        self.assertEqual(health_schema["properties"]["product_evidence_maturity"]["enum"], [f"PE-{i}" for i in range(6)])

    def test_generation_is_deterministic_and_manual_edits_fail_check(self) -> None:
        legacy_dir = self.project / "legacy"
        legacy_dir.mkdir()
        legacy_shapes = {
            "skills/BASE_V9_ADAPTER.json": {
                "schema_version": 1,
                "adapter_role": "base-v9-adapter",
                "base_route": {"registry": "skills/SKILL_REGISTRY.json"},
            },
            "skills/PROJECT_BASE_SKILL_ADAPTER.json": {
                "schema_version": 1,
                "adapter_role": "base-shared-skill-project-adapter",
                "role_bindings": {"project_agents": "AGENTS.md"},
            },
            "skills/PROJECT_PATH_ADAPTER.json": {
                "schema_version": 1,
                "adapter_role": "project-path-adapter",
                "path_bindings": {"project_file": "project.godot"},
            },
        }
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        for output, data in legacy_shapes.items():
            source = legacy_dir / Path(output).name
            source.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
            adapter["compatibility"]["views"].append(output)
            adapter["compatibility"]["legacy_inputs"][output] = source.relative_to(self.project).as_posix()
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        args = ["--project-root", str(self.project), "--base-repository", str(self.base)]
        first = self.run_tool(BUILD, *args, "--write")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        generated = [
            self.project / "skills/PROJECT_SKILL_SNAPSHOT.json",
            self.project / "docs/PROJECT_OPERATING_DASHBOARD.html",
            self.project / ".agents/skills/project-workflow-router/SKILL.md",
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
        router = generated[2].read_text(encoding="utf-8")
        self.assertIn("PROJECT_BASE_ADAPTER.json", router)
        self.assertIn("PROJECT_SKILL_SNAPSHOT.json", router)
        self.assertNotIn("# Shared", router)
        expected_consumer_fields = ("base_route", "role_bindings", "path_bindings")
        for compatibility_view, consumer_field in zip(generated[3:], expected_consumer_fields):
            data = json.loads(compatibility_view.read_text(encoding="utf-8"))
            self.assertEqual(data["artifact_role"], "GENERATED_COMPATIBILITY_VIEW")
            self.assertEqual(data["lifecycle"], "ONE_CYCLE")
            self.assertIn(consumer_field, data)
            self.assertEqual(data["legacy_source_sha256"], digest(legacy_dir / compatibility_view.name))

        generated[1].write_text(generated[1].read_text(encoding="utf-8") + "<!-- manual -->\n", encoding="utf-8")
        stale = self.run_tool(BUILD, *args, "--check")
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("manual", stale.stderr.lower())

    def test_generation_omits_compatibility_views_that_have_no_real_legacy_input(self) -> None:
        result = self.run_tool(
            BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for relative in self.core.COMPATIBILITY_VIEWS:
            self.assertFalse((self.project / relative).exists(), relative)

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
        project_registry = json.loads(self.project_registry.read_text(encoding="utf-8"))
        project_registry["skills"].append(
            {"skill_id": "copied-shared", "status": "ACTIVE", "path": "skills/shared-skill/SKILL.md"}
        )
        self.project_registry.write_text(json.dumps(project_registry, sort_keys=True) + "\n", encoding="utf-8")
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["project"]["sha256"] = digest(self.project_registry)
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        body_copy = self.run_tool(CHECK, *args)
        self.assertNotEqual(body_copy.returncode, 0)
        self.assertIn("shared skill body", body_copy.stderr.lower())

    def test_validator_uses_clean_tracked_registry_bytes_across_crlf_checkout(self) -> None:
        (self.project / ".gitattributes").write_text("*.json text eol=lf\n", encoding="utf-8")
        commit_all(self.project, "normalize JSON checkout")
        raw = subprocess.run(
            ["git", "-C", str(self.project), "show", "HEAD:skills/SKILL_REGISTRY.json"],
            capture_output=True,
            check=True,
        ).stdout
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["project"]["sha256"] = hashlib.sha256(raw).hexdigest()
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        commit_all(self.project, "pin project Registry Git bytes")
        raw_text = raw.decode("utf-8")
        self.project_registry.write_text(raw_text.replace("\n", "\r\n"), encoding="utf-8", newline="")

        clean = self.run_tool(
            CHECK, "--project-root", str(self.project), "--base-repository", str(self.base)
        )
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

        self.project_registry.write_text(raw_text.replace("local-skill", "changed-local-skill"), encoding="utf-8")
        modified = self.run_tool(
            CHECK, "--project-root", str(self.project), "--base-repository", str(self.base)
        )
        self.assertNotEqual(modified.returncode, 0)
        self.assertIn("uncommitted", modified.stderr.lower())

    def test_shared_skill_duplication_is_detected_by_normalized_body_and_duplicate_provenance(self) -> None:
        shared = subprocess.run(
            ["git", "-C", str(self.base), "show", f"{self.evidence_commit}:skills/shared-skill/SKILL.md"],
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        local = self.project / "skills/local-skill/SKILL.md"
        local.write_text(shared.replace("\n", "\r\n") + "\r\n", encoding="utf-8", newline="")
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["project"]["sha256"] = digest(self.project_registry)
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        duplicate_body = self.run_tool(
            CHECK, "--project-root", str(self.project), "--base-repository", str(self.base)
        )
        self.assertNotEqual(duplicate_body.returncode, 0)
        self.assertIn("normalized", duplicate_body.stderr.lower())

        local.write_text("project-specific\n", encoding="utf-8")
        project_registry = json.loads(self.project_registry.read_text(encoding="utf-8"))
        project_registry["skills"][0]["skill_id"] = "shared-skill"
        self.project_registry.write_text(json.dumps(project_registry, sort_keys=True) + "\n", encoding="utf-8")
        adapter = self.adapter_data()
        adapter["skill_registry"]["project"]["sha256"] = digest(self.project_registry)
        adapter["routing"]["project_routes"][0]["skill_id"] = "shared-skill"
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        duplicate_id = self.run_tool(
            CHECK, "--project-root", str(self.project), "--base-repository", str(self.base)
        )
        self.assertNotEqual(duplicate_id.returncode, 0)
        self.assertIn("provenance", duplicate_id.stderr.lower())

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

    def test_routes_are_status_safe_and_aliases_resolve_to_one_active_effective_route(self) -> None:
        original = json.loads(self.adapter.read_text(encoding="utf-8"))

        inactive_base = json.loads(json.dumps(original))
        inactive_base["routing"]["base_routes"][0]["status"] = "HOLD"
        self.adapter.write_text(json.dumps(inactive_base, sort_keys=True) + "\n", encoding="utf-8")
        result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("active", result.stderr.lower())

        active_inactive = json.loads(json.dumps(original))
        active_inactive["routing"]["inactive_routes"] = [
            {"route_id": "retired", "skill_id": "local-skill", "status": "ACTIVE"}
        ]
        self.adapter.write_text(json.dumps(active_inactive, sort_keys=True) + "\n", encoding="utf-8")
        result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inactive", result.stderr.lower())

        dangling = json.loads(json.dumps(original))
        dangling["routing"]["aliases"] = [{"alias": "old-shared", "target": "missing-route"}]
        self.adapter.write_text(json.dumps(dangling, sort_keys=True) + "\n", encoding="utf-8")
        result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dangling", result.stderr.lower())

        valid = json.loads(json.dumps(original))
        valid["routing"]["aliases"] = [
            {"alias": "legacy-shared", "target": "old-shared"},
            {"alias": "old-shared", "target": "shared-skill"},
        ]
        self.adapter.write_text(json.dumps(valid, sort_keys=True) + "\n", encoding="utf-8")
        built = self.run_tool(BUILD, "--project-root", str(self.project), "--base-repository", str(self.base), "--write")
        self.assertEqual(built.returncode, 0, built.stderr)
        snapshot = json.loads((self.project / "skills/PROJECT_SKILL_SNAPSHOT.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["alias_resolutions"]["legacy-shared"]["target_route_id"], "shared-skill")
        self.assertEqual(snapshot["alias_resolutions"]["legacy-shared"]["source"], "BASE_SHARED")

    def test_router_runs_exact_validator_before_reading_any_routes(self) -> None:
        router = (ROOT / "templates/project-operations/.agents/skills/base-project-router/SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (
            "python tools/check_project_operating_contract.py "
            "--project-root . --base-repository ../Base --check"
        )
        self.assertIn(command, router)
        self.assertIn("nonzero", router.lower())
        self.assertLess(router.index(command), router.index("PROJECT_SKILL_SNAPSHOT.json"))

    def test_generation_fails_closed_when_candidate_release_pins_are_null_or_inconsistent(self) -> None:
        original = json.loads(self.candidate_lock.read_text(encoding="utf-8"))
        for label, release, evidence in (
            ("both-null", None, None),
            ("release-only", self.release_commit, None),
            ("evidence-only", None, self.evidence_commit),
        ):
            with self.subTest(label=label):
                lock = json.loads(json.dumps(original))
                lock["candidate_release_commit"] = release
                lock["candidate_release_evidence_commit"] = evidence
                if release is None:
                    lock["candidate_registry"]["sha256"] = None
                self.candidate_lock.write_text(json.dumps(lock, sort_keys=True) + "\n", encoding="utf-8")
                result = self.run_tool(
                    BUILD,
                    "--project-root",
                    str(self.project),
                    "--base-repository",
                    str(self.base),
                    "--write",
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("candidate", result.stderr.lower())
        self.candidate_lock.write_text(json.dumps(original, sort_keys=True) + "\n", encoding="utf-8")

    def test_adapter_identity_and_pins_must_match_v91_release_lock_exactly(self) -> None:
        original = json.loads(self.adapter.read_text(encoding="utf-8"))
        mutations = {
            "repository": lambda data: data["base_release"].update(repository="wrong/Base"),
            "version": lambda data: data["base_release"].update(version="9.0.0"),
            "release": lambda data: data["base_release"].update(release_commit=self.evidence_commit),
            "evidence": lambda data: data["base_release"].update(release_evidence_commit=self.release_commit),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                data = json.loads(json.dumps(original))
                mutate(data)
                self.adapter.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
                result = self.run_tool(
                    CHECK,
                    "--project-root",
                    str(self.project),
                    "--base-repository",
                    str(self.base),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("lock", result.stderr.lower())

    def test_base_registry_is_validated_from_pinned_git_blob_not_mutable_worktree(self) -> None:
        self.base_registry.write_bytes(self.base_registry.read_bytes() + b" \n")
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["base"]["sha256"] = digest(self.base_registry)
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pinned", result.stderr.lower())
        self.assertIn("registry", result.stderr.lower())

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
            self.protected_baseline_commit,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected", result.stderr.lower())
        self.assertIn("project.godot", result.stderr)

    def test_generator_requires_exact_trusted_baseline_after_remote_ref_advances(self) -> None:
        args = ["--project-root", str(self.project), "--base-repository", str(self.base), "--write"]
        git(self.project, "update-ref", "refs/remotes/origin/main", self.project_commit)

        blocked = self.run_tool(BUILD, *args)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("external protected authority", blocked.stderr.lower())

        trusted = self.run_tool(BUILD, *args, "--protected-base", self.protected_baseline_commit)
        self.assertEqual(trusted.returncode, 0, trusted.stdout + trusted.stderr)

        wrong = self.run_tool(BUILD, *args, "--protected-base", self.project_commit)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn("trusted", wrong.stderr.lower())

    def test_protected_paths_fail_closed_for_bad_baseline_untracked_case_and_policy_weakening(self) -> None:
        args = ["--project-root", str(self.project), "--base-repository", str(self.base)]
        bad_base = self.run_tool(CHECK, *args, "--protected-base", "0" * 40)
        self.assertNotEqual(bad_base.returncode, 0)
        self.assertIn("baseline", bad_base.stderr.lower())

        (self.project / "PROJECT.GODOT").write_text("case variant\n", encoding="utf-8")
        untracked = self.run_tool(CHECK, *args, "--protected-base", self.protected_baseline_commit)
        self.assertNotEqual(untracked.returncode, 0)
        self.assertIn("project.godot", untracked.stderr.lower())
        self.assertTrue(self.core._protected_match("assets/e\u0301/icon.png", ["assets/é/**"]))
        (self.project / "PROJECT.GODOT").unlink()

        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["protected_paths"] = ["docs/CANON.md"]
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        weakened = self.run_tool(CHECK, *args, "--protected-base", self.protected_baseline_commit)
        self.assertNotEqual(weakened.returncode, 0)
        self.assertIn("weaken", weakened.stderr.lower())

        adapter["protected_paths"] = ["**"]
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        nonsensical = self.run_tool(CHECK, *args)
        self.assertNotEqual(nonsensical.returncode, 0)
        self.assertIn("nonsensical", nonsensical.stderr.lower())

    def test_protected_paths_cover_tracked_add_delete_rename_and_untracked_changes(self) -> None:
        args = [
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--protected-base", self.protected_baseline_commit,
        ]
        game = self.project / "game"
        game.mkdir()

        untracked = game / "untracked.gd"
        untracked.write_text("extends Node\n", encoding="utf-8")
        result = self.run_tool(CHECK, *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("game/untracked.gd", result.stderr)
        untracked.unlink()

        added = game / "added.gd"
        added.write_text("extends Node\n", encoding="utf-8")
        git(self.project, "add", "game/added.gd")
        result = self.run_tool(CHECK, *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("game/added.gd", result.stderr)
        git(self.project, "rm", "--cached", "game/added.gd")
        added.unlink()

        original_project = (self.project / "project.godot").read_bytes()
        (self.project / "project.godot").unlink()
        result = self.run_tool(CHECK, *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project.godot", result.stderr)
        (self.project / "project.godot").write_bytes(original_project)

        renamed = self.project / "renamed.godot"
        (self.project / "project.godot").rename(renamed)
        result = self.run_tool(CHECK, *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project.godot", result.stderr)
        renamed.rename(self.project / "project.godot")

    def test_adapter_paths_cannot_escape_roots_or_traverse_symlinks(self) -> None:
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["skill_registry"]["project"]["path"] = "../outside.json"
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        escaped = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(escaped.returncode, 0)
        self.assertIn("unsafe", escaped.stderr.lower())

        outside = self.workspace / "outside"
        outside.mkdir()
        (outside / "SKILL_REGISTRY.json").write_text(self.project_registry.read_text(encoding="utf-8"), encoding="utf-8")
        link = self.project / "linked"
        try:
            os.symlink(outside, link, target_is_directory=True)
        except OSError as error:
            junction = subprocess.run(
                ["cmd", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if junction.returncode:
                self.fail(f"Could not create test reparse point: {error}; {junction.stdout}{junction.stderr}")
        adapter = self.adapter_data()
        adapter["skill_registry"]["project"] = {
            "path": "linked/SKILL_REGISTRY.json",
            "sha256": digest(outside / "SKILL_REGISTRY.json"),
            "hash_definition": "RAW_FILE_BYTES_SHA256",
        }
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        linked = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(linked.returncode, 0)
        self.assertRegex(linked.stderr.lower(), r"symlink|reparse")

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

    def test_health_rejects_inconsistent_verdicts_and_unsupported_maturity_or_sheet_claims(self) -> None:
        health_path = self.project / "docs/PROJECT_OPERATING_HEALTH.json"
        original_health = json.loads(health_path.read_text(encoding="utf-8"))
        original_adapter = json.loads(self.adapter.read_text(encoding="utf-8"))

        cases: list[tuple[str, callable, str]] = []

        def fail_claim(health: dict, adapter: dict) -> None:
            health["critical_gates"]["static"] = "FAIL"
            health["integrity_verdict"] = "PASS"

        def blocked_claim(health: dict, adapter: dict) -> None:
            health["critical_gates"]["runtime"] = "BLOCKED"
            health["integrity_verdict"] = "PASS_WITH_NOT_RUN_GATES"

        def not_run_pass(health: dict, adapter: dict) -> None:
            health["integrity_verdict"] = "PASS"

        def unsupported_om(health: dict, adapter: dict) -> None:
            health["operating_maturity"] = "OM-L5"

        def unsupported_pe(health: dict, adapter: dict) -> None:
            health["product_evidence_maturity"] = "PE-5"

        def unsupported_sheet(health: dict, adapter: dict) -> None:
            adapter["gdd_sheet"]["sync_status"] = "CURRENT"

        cases.extend(
            [
                ("fail", fail_claim, "fail"),
                ("blocked", blocked_claim, "blocked"),
                ("not-run", not_run_pass, "not_run"),
                ("om", unsupported_om, "om-l5"),
                ("pe", unsupported_pe, "pe-5"),
                ("sheet", unsupported_sheet, "current"),
            ]
        )
        for label, mutate, expected in cases:
            with self.subTest(label=label):
                health = json.loads(json.dumps(original_health))
                adapter = json.loads(json.dumps(original_adapter))
                mutate(health, adapter)
                health_path.write_text(json.dumps(health, sort_keys=True) + "\n", encoding="utf-8")
                self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
                result = self.run_tool(
                    CHECK,
                    "--project-root",
                    str(self.project),
                    "--base-repository",
                    str(self.base),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr.lower())

    def test_health_evidence_must_be_unique_existing_confined_and_match_raw_sha256(self) -> None:
        health_path = self.project / "docs/PROJECT_OPERATING_HEALTH.json"
        original = json.loads(health_path.read_text(encoding="utf-8"))
        cases = (
            (
                "missing",
                lambda health: health["evidence"]["operating"][0].update(source="evidence/missing.txt"),
                "does not exist",
            ),
            (
                "fake-hash",
                lambda health: health["evidence"]["operating"][0].update(sha256="f" * 64),
                "hash mismatch",
            ),
            (
                "absolute",
                lambda health: health["evidence"]["operating"][0].update(source=str(self.operating_evidence.resolve())),
                "unsafe",
            ),
            (
                "parent",
                lambda health: health["evidence"]["operating"][0].update(source="../outside.txt"),
                "unsafe",
            ),
            (
                "duplicate-source",
                lambda health: health["evidence"]["product"].append(
                    {
                        "id": "repeated-under-new-id",
                        "source": "evidence/adapter-installed.txt",
                        "sha256": digest(self.operating_evidence),
                    }
                ),
                "duplicate evidence",
            ),
        )
        for label, mutate, expected in cases:
            with self.subTest(label=label):
                health = json.loads(json.dumps(original))
                mutate(health)
                health_path.write_text(json.dumps(health, sort_keys=True) + "\n", encoding="utf-8")
                result = self.run_tool(
                    CHECK,
                    "--project-root",
                    str(self.project),
                    "--base-repository",
                    str(self.base),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr.lower())

        outside = self.workspace / "outside-evidence"
        outside.mkdir()
        outside_file = outside / "runtime.txt"
        outside_file.write_text("runtime evidence\n", encoding="utf-8")
        link = self.project / "evidence-link"
        try:
            os.symlink(outside, link, target_is_directory=True)
        except OSError as error:
            junction = subprocess.run(
                ["cmd", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if junction.returncode:
                self.fail(f"Could not create evidence reparse point: {error}; {junction.stdout}{junction.stderr}")
        linked_health = json.loads(json.dumps(original))
        linked_health["evidence"]["operating"][0] = {
            "id": "linked",
            "source": "evidence-link/runtime.txt",
            "sha256": digest(outside_file),
        }
        health_path.write_text(json.dumps(linked_health, sort_keys=True) + "\n", encoding="utf-8")
        linked_result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
        )
        self.assertNotEqual(linked_result.returncode, 0)
        self.assertRegex(linked_result.stderr.lower(), r"symlink|reparse")

    def test_health_evidence_accepts_clean_autocrlf_checkout_bytes(self) -> None:
        """Tracked evidence must compare against its canonical Git bytes, not CRLF checkout bytes."""
        health_path = self.project / "docs/PROJECT_OPERATING_HEALTH.json"
        health = json.loads(health_path.read_text(encoding="utf-8"))
        canonical = subprocess.run(
            ["git", "-C", str(self.project), "show", f"{self.project_commit}:evidence/adapter-installed.txt"],
            capture_output=True,
            check=True,
        ).stdout
        health["evidence"]["operating"][0]["sha256"] = hashlib.sha256(canonical).hexdigest()
        health_path.write_text(json.dumps(health, sort_keys=True) + "\n", encoding="utf-8")
        git(self.project, "config", "core.autocrlf", "true")
        self.operating_evidence.write_bytes(b"adapter installed\r\n")
        self.assertEqual("", git(self.project, "diff", "--", "evidence/adapter-installed.txt"))

        result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
        )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_standard_check_uses_required_adapter_protected_baseline(self) -> None:
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        protected_baseline = adapter.pop("protected_baseline")
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        missing = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--check",
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("protected_baseline", missing.stderr)

        adapter["protected_baseline"] = protected_baseline
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        (self.project / "project.godot").write_text("[application]\nconfig/name=\"Changed\"\n", encoding="utf-8")
        result = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--check",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected-path changes", result.stderr.lower())

    def test_protected_baseline_policy_source_contract_fails_closed_and_supports_later_canonical_wave(self) -> None:
        canonical_at_baseline = subprocess.run(
            [
                "git",
                "-C",
                str(self.project),
                "cat-file",
                "-e",
                f"{self.protected_baseline_commit}:skills/PROJECT_BASE_ADAPTER.json",
            ],
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(canonical_at_baseline.returncode, 0)
        valid_first_migration = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
        )
        self.assertEqual(valid_first_migration.returncode, 0, valid_first_migration.stderr)

        original = json.loads(self.adapter.read_text(encoding="utf-8"))
        missing_source = json.loads(json.dumps(original))
        missing_source["protected_baseline"]["policy_source_path"] = "skills/MISSING_LEGACY.json"
        self.adapter.write_text(json.dumps(missing_source, sort_keys=True) + "\n", encoding="utf-8")
        missing_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(missing_result.returncode, 0)
        self.assertIn("baseline policy source", missing_result.stderr.lower())

        unsafe_source = json.loads(json.dumps(original))
        unsafe_source["protected_baseline"]["policy_source_path"] = "../LEGACY_PROJECT_ADAPTER.json"
        self.adapter.write_text(json.dumps(unsafe_source, sort_keys=True) + "\n", encoding="utf-8")
        unsafe_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(unsafe_result.returncode, 0)
        self.assertIn("unsafe", unsafe_result.stderr.lower())

        fake_hash = json.loads(json.dumps(original))
        fake_hash["protected_baseline"]["policy_sha256"] = "f" * 64
        self.adapter.write_text(json.dumps(fake_hash, sort_keys=True) + "\n", encoding="utf-8")
        hash_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(hash_result.returncode, 0)
        self.assertIn("policy hash", hash_result.stderr.lower())

        weakened = json.loads(json.dumps(original))
        weakened["protected_paths"] = ["project.godot"]
        self.adapter.write_text(json.dumps(weakened, sort_keys=True) + "\n", encoding="utf-8")
        weakened_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertNotEqual(weakened_result.returncode, 0)
        self.assertIn("weaken", weakened_result.stderr.lower())

        self.adapter.write_text(json.dumps(original, sort_keys=True) + "\n", encoding="utf-8")
        canonical_baseline_commit = commit_all(self.project, "canonical policy baseline")
        later = json.loads(self.adapter.read_text(encoding="utf-8"))
        later["protected_baseline"] = {
            "authority_kind": "REMOTE_TRACKING_REF",
            "authority_ref": "refs/remotes/origin/main",
            "commit": canonical_baseline_commit,
            "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
            "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
            "protected_paths_pointer": "/protected_paths",
            "policy_sha256": policy_digest(later["protected_paths"]),
        }
        git(self.project, "update-ref", "refs/remotes/origin/main", canonical_baseline_commit)
        self.adapter.write_text(json.dumps(later, sort_keys=True) + "\n", encoding="utf-8")
        later_result = self.run_tool(CHECK, "--project-root", str(self.project), "--base-repository", str(self.base))
        self.assertEqual(later_result.returncode, 0, later_result.stderr)

    def test_external_git_authority_prevents_feature_branch_baseline_self_attestation(self) -> None:
        args = ["--project-root", str(self.project), "--base-repository", str(self.base)]
        correct_remote_base = self.run_tool(CHECK, *args)
        self.assertEqual(correct_remote_base.returncode, 0, correct_remote_base.stderr)

        cli_mismatch = self.run_tool(CHECK, *args, "--protected-base", self.project_commit)
        self.assertNotEqual(cli_mismatch.returncode, 0)
        self.assertIn("must equal adapter baseline", cli_mismatch.stderr.lower())

        original = json.loads(self.adapter.read_text(encoding="utf-8"))
        missing_ref = json.loads(json.dumps(original))
        missing_ref["protected_baseline"]["authority_ref"] = "refs/remotes/origin/missing"
        self.adapter.write_text(json.dumps(missing_ref, sort_keys=True) + "\n", encoding="utf-8")
        missing_result = self.run_tool(CHECK, *args)
        self.assertNotEqual(missing_result.returncode, 0)
        self.assertIn("authority ref", missing_result.stderr.lower())

        github_base = json.loads(json.dumps(original))
        github_base["protected_baseline"]["authority_kind"] = "GITHUB_PR_BASE"
        github_base["protected_baseline"]["authority_ref"] = "github.event.pull_request.base.sha"
        self.adapter.write_text(json.dumps(github_base, sort_keys=True) + "\n", encoding="utf-8")
        missing_trusted_input = self.run_tool(CHECK, *args)
        self.assertNotEqual(missing_trusted_input.returncode, 0)
        self.assertIn("requires trusted --protected-base", missing_trusted_input.stderr.lower())
        github_event_base = self.run_tool(
            CHECK, *args, "--protected-base", self.protected_baseline_commit
        )
        self.assertEqual(github_event_base.returncode, 0, github_event_base.stderr)

        self.adapter.write_text(json.dumps(original, sort_keys=True) + "\n", encoding="utf-8")
        git(self.project, "checkout", "-q", "-b", "feature/self-attested-baseline")
        (self.project / "project.godot").write_text("[application]\nconfig/name=\"Attacked\"\n", encoding="utf-8")
        feature_head = commit_all(self.project, "protected product change")
        attacked = json.loads(self.adapter.read_text(encoding="utf-8"))
        attacked["protected_baseline"] = {
            "authority_kind": "REMOTE_TRACKING_REF",
            "authority_ref": "refs/remotes/origin/main",
            "commit": feature_head,
            "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
            "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
            "protected_paths_pointer": "/protected_paths",
            "policy_sha256": policy_digest(attacked["protected_paths"]),
        }
        self.adapter.write_text(json.dumps(attacked, sort_keys=True) + "\n", encoding="utf-8")
        self_attested = self.run_tool(CHECK, *args)
        self.assertNotEqual(self_attested.returncode, 0)
        self.assertIn("external protected authority", self_attested.stderr.lower())

        self.adapter.write_text(json.dumps(original, sort_keys=True) + "\n", encoding="utf-8")
        fixed_old_baseline = self.run_tool(CHECK, *args)
        self.assertNotEqual(fixed_old_baseline.returncode, 0)
        self.assertIn("project.godot", fixed_old_baseline.stderr)

    def test_dashboard_is_static_accessible_and_keeps_maturity_axes_separate(self) -> None:
        adapter = json.loads(self.adapter.read_text(encoding="utf-8"))
        adapter["project"]["repository"] = "example/<script>alert(1)</script>"
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
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
            "9.1.0",
            "RELEASE_CANDIDATE",
            self.release_commit,
            self.evidence_commit,
            "BASE_SHARED: 1",
            "PROJECT_LOCAL: 1",
            "INACTIVE: 0",
            "EFFECTIVE: 2",
            self.pinned_base_registry_sha,
            adapter["skill_registry"]["project"]["sha256"],
            "example/&lt;script&gt;alert(1)&lt;/script&gt;",
        ):
            self.assertIn(term, dashboard)
        self.assertNotIn("<script>alert(1)</script>", dashboard)
        self.assertNotIn("average", dashboard.lower())
        self.assertNotIn("<script", dashboard.lower())
        adapter_raw_hash = digest(self.adapter)
        self.assertEqual(dashboard.count(adapter_raw_hash), 2)
        canonical_hash = hashlib.sha256(self.core.canonical_json(adapter)).hexdigest()
        if canonical_hash != adapter_raw_hash:
            self.assertNotIn(canonical_hash, dashboard)

    def test_migrator_converts_legacy_inputs_without_overwriting_them(self) -> None:
        legacy = self.legacy_adapter
        legacy_before = legacy.read_bytes()
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        missing_pins = self.run_tool(
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
        self.assertNotEqual(missing_pins.returncode, 0)
        self.assertIn("explicit", missing_pins.stderr.lower())

        missing_baseline = self.run_tool(
            MIGRATE,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--legacy-adapter",
            str(legacy),
            "--output",
            str(output),
            "--release-commit",
            self.release_commit,
            "--release-evidence-commit",
            self.evidence_commit,
            "--write",
        )
        self.assertNotEqual(missing_baseline.returncode, 0)
        self.assertIn("baseline", missing_baseline.stderr.lower())

        broken_legacy = self.project / "skills/BROKEN_LEGACY_ADAPTER.json"
        broken_legacy.write_text(
            json.dumps({"project": {"repository": "example/project"}}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        broken_baseline = commit_all(self.project, "legacy source without protected policy")
        git(self.project, "update-ref", "refs/remotes/origin/main", broken_baseline)
        broken_result = self.run_tool(
            MIGRATE,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--legacy-adapter",
            str(broken_legacy),
            "--output",
            str(output),
            "--release-commit",
            self.release_commit,
            "--release-evidence-commit",
            self.evidence_commit,
            "--protected-baseline-commit",
            broken_baseline,
            "--protected-authority-kind",
            "REMOTE_TRACKING_REF",
            "--protected-authority-ref",
            "refs/remotes/origin/main",
            "--write",
        )
        self.assertNotEqual(broken_result.returncode, 0)
        self.assertIn("protected paths", broken_result.stderr.lower())
        git(self.project, "update-ref", "refs/remotes/origin/main", self.protected_baseline_commit)

        same_path = self.run_tool(
            MIGRATE,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--legacy-adapter",
            str(legacy),
            "--output",
            str(legacy),
            "--release-commit",
            self.release_commit,
            "--release-evidence-commit",
            self.evidence_commit,
            "--protected-baseline-commit",
            self.protected_baseline_commit,
            "--protected-authority-kind",
            "REMOTE_TRACKING_REF",
            "--protected-authority-ref",
            "refs/remotes/origin/main",
            "--write",
        )
        self.assertNotEqual(same_path.returncode, 0)
        self.assertIn("same", same_path.stderr.lower())

        head_authority = self.run_tool(
            MIGRATE,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
            "--legacy-adapter",
            str(legacy),
            "--output",
            str(output),
            "--release-commit",
            self.release_commit,
            "--release-evidence-commit",
            self.evidence_commit,
            "--protected-baseline-commit",
            self.protected_baseline_commit,
            "--protected-authority-kind",
            "REMOTE_TRACKING_REF",
            "--protected-authority-ref",
            "HEAD",
            "--write",
        )
        self.assertNotEqual(head_authority.returncode, 0)
        self.assertIn("remote-tracking ref", head_authority.stderr.lower())

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
            "--release-commit",
            self.release_commit,
            "--release-evidence-commit",
            self.evidence_commit,
            "--protected-baseline-commit",
            self.protected_baseline_commit,
            "--protected-authority-kind",
            "REMOTE_TRACKING_REF",
            "--protected-authority-ref",
            "refs/remotes/origin/main",
            "--write",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(legacy_before, legacy.read_bytes())
        migrated = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(migrated["artifact_role"], "PROJECT_BASE_ADAPTER")
        self.assertEqual(migrated["base_release"]["release_commit"], self.release_commit)
        self.assertEqual(migrated["base_release"]["release_evidence_commit"], self.evidence_commit)
        self.assertEqual(migrated["protected_baseline"]["commit"], self.protected_baseline_commit)
        self.assertEqual(migrated["protected_baseline"]["authority_kind"], "REMOTE_TRACKING_REF")
        self.assertEqual(migrated["protected_baseline"]["authority_ref"], "refs/remotes/origin/main")
        self.assertEqual(
            migrated["protected_baseline"]["policy_source_type"],
            "FIRST_MIGRATION_LEGACY_SOURCE",
        )
        self.assertEqual(
            migrated["protected_baseline"]["policy_source_path"],
            "skills/LEGACY_PROJECT_ADAPTER.json",
        )
        self.assertEqual(migrated["protected_baseline"]["policy_sha256"], self.protected_policy_hash)
        self.assertEqual(
            migrated["routing"]["project_routes"],
            [{"route_id": "local-skill", "skill_id": "local-skill", "status": "ACTIVE"}],
        )
        self.adapter.write_bytes(output.read_bytes())
        validates = self.run_tool(
            CHECK,
            "--project-root",
            str(self.project),
            "--base-repository",
            str(self.base),
        )
        self.assertEqual(validates.returncode, 0, validates.stderr)

    def test_migrator_uses_the_legacy_declared_project_registry_path(self) -> None:
        custom_registry = self.project / "docs/planning/SKILL_REGISTRY.json"
        custom_registry.parent.mkdir(parents=True)
        custom_registry.write_bytes(self.project_registry.read_bytes())
        self.project_registry.unlink()
        legacy = json.loads(self.legacy_adapter.read_text(encoding="utf-8"))
        legacy["role_bindings"] = {"skill_registry": "docs/planning/SKILL_REGISTRY.json"}
        self.legacy_adapter.write_text(json.dumps(legacy, sort_keys=True) + "\n", encoding="utf-8")
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        result = self.run_tool(
            MIGRATE,
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--legacy-adapter", str(self.legacy_adapter),
            "--output", str(output),
            "--release-commit", self.release_commit,
            "--release-evidence-commit", self.evidence_commit,
            "--protected-baseline-commit", self.protected_baseline_commit,
            "--protected-authority-kind", "REMOTE_TRACKING_REF",
            "--protected-authority-ref", "refs/remotes/origin/main",
            "--write",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        migrated = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(migrated["skill_registry"]["project"]["path"], "docs/planning/SKILL_REGISTRY.json")
        self.assertEqual(migrated["skill_registry"]["project"]["sha256"], digest(custom_registry))

        legacy["role_bindings"]["skill_registry"] = "../outside/SKILL_REGISTRY.json"
        self.legacy_adapter.write_text(json.dumps(legacy, sort_keys=True) + "\n", encoding="utf-8")
        unsafe = self.run_tool(
            MIGRATE,
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--legacy-adapter", str(self.legacy_adapter),
            "--output", str(output),
            "--release-commit", self.release_commit,
            "--release-evidence-commit", self.evidence_commit,
            "--protected-baseline-commit", self.protected_baseline_commit,
            "--protected-authority-kind", "REMOTE_TRACKING_REF",
            "--protected-authority-ref", "refs/remotes/origin/main",
            "--write",
        )
        self.assertNotEqual(unsafe.returncode, 0)
        self.assertIn("escapes", unsafe.stderr.lower())

    def test_migrator_preserves_registry_identity_and_gdd_contract(self) -> None:
        registry = json.loads(self.project_registry.read_text(encoding="utf-8"))
        registry["project"] = {"repository": "example/actual-project"}
        registry["base_registry_route"] = {
            "project_sheet_id": "sheet-123",
            "project_sheet_role": "USER_FACING_GDD_WORKSPACE",
            "project_sheet_edit_policy": "PROPOSED_SHEET_CHANGE",
            "project_sheet_status": "PROJECT_SHEET_CONFIGURED",
        }
        self.project_registry.write_text(json.dumps(registry, sort_keys=True) + "\n", encoding="utf-8")
        legacy = json.loads(self.legacy_adapter.read_text(encoding="utf-8"))
        legacy["project"]["repository"] = "example/old-project"
        self.legacy_adapter.write_text(json.dumps(legacy, sort_keys=True) + "\n", encoding="utf-8")
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        args = (
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--legacy-adapter", str(self.legacy_adapter),
            "--output", str(output),
            "--release-commit", self.release_commit,
            "--release-evidence-commit", self.evidence_commit,
            "--protected-baseline-commit", self.protected_baseline_commit,
            "--protected-authority-kind", "REMOTE_TRACKING_REF",
            "--protected-authority-ref", "refs/remotes/origin/main",
        )
        written = self.run_tool(MIGRATE, *args, "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        migrated = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(migrated["project"]["repository"], "example/actual-project")
        self.assertEqual(migrated["project"]["legacy_repository_aliases"], ["example/project"])
        self.assertEqual(migrated["gdd_sheet"]["id"], "sheet-123")
        self.assertEqual(migrated["gdd_sheet"]["sync_status"], "BLOCKED")
        self.assertEqual(migrated["gdd_sheet"]["sheet_only_change_policy"], "PROPOSED_SHEET_CHANGE")
        checked = self.run_tool(MIGRATE, *args, "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_project_skill_paths_may_be_relative_to_the_declared_registry(self) -> None:
        registry = self.project / "docs/planning/SKILL_REGISTRY.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "skills": [
                        {
                            "skill_id": "local-skill",
                            "status": "ACTIVE",
                            "path": "../../skills/local-skill/SKILL.md",
                        }
                    ],
                },
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )
        adapter = self.adapter_data()
        adapter["skill_registry"]["project"].update(
            path="docs/planning/SKILL_REGISTRY.json", sha256=digest(registry)
        )
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        self.assertEqual(
            self.core.validation_errors(self.project, self.base, check_generated=False),
            [],
        )

        data = json.loads(registry.read_text(encoding="utf-8"))
        data["skills"][0]["path"] = "../../../outside/SKILL.md"
        registry.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
        adapter["skill_registry"]["project"]["sha256"] = digest(registry)
        self.adapter.write_text(json.dumps(adapter, sort_keys=True) + "\n", encoding="utf-8")
        self.assertTrue(
            any(
                "escapes" in error.lower()
                for error in self.core.validation_errors(self.project, self.base, check_generated=False)
            )
        )

    def test_migrator_initializes_missing_health_without_overwrite(self) -> None:
        health = self.project / "docs/PROJECT_OPERATING_HEALTH.json"
        health.unlink()
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        args = (
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--legacy-adapter", str(self.legacy_adapter),
            "--output", str(output),
            "--release-commit", self.release_commit,
            "--release-evidence-commit", self.evidence_commit,
            "--protected-baseline-commit", self.protected_baseline_commit,
            "--protected-authority-kind", "REMOTE_TRACKING_REF",
            "--protected-authority-ref", "refs/remotes/origin/main",
        )
        result = self.run_tool(MIGRATE, *args, "--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        initial = json.loads(health.read_text(encoding="utf-8"))
        self.assertEqual(initial["operating_maturity"], "OM-L0")
        self.assertEqual(initial["product_evidence_maturity"], "PE-0")
        self.assertEqual(set(initial["critical_gates"].values()), {"NOT_RUN"})

        initial["critical_gates"]["runtime"] = "BLOCKED"
        health.write_text(json.dumps(initial, sort_keys=True) + "\n", encoding="utf-8")
        second = self.run_tool(MIGRATE, *args, "--write")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(
            json.loads(health.read_text(encoding="utf-8"))["critical_gates"]["runtime"],
            "BLOCKED",
        )

    def test_migrator_archives_legacy_adapters_before_generating_compatibility_views(self) -> None:
        legacy_views = {
            "BASE_V9_ADAPTER.json": {"schema_version": 1, "adapter_role": "legacy-base"},
            "PROJECT_BASE_SKILL_ADAPTER.json": {"schema_version": 1, "adapter_role": "legacy-project"},
        }
        for name, content in legacy_views.items():
            (self.project / "skills" / name).write_text(
                json.dumps(content, sort_keys=True) + "\n", encoding="utf-8"
            )
        output = self.project / "skills/MIGRATED_PROJECT_BASE_ADAPTER.json"
        result = self.run_tool(
            MIGRATE,
            "--project-root", str(self.project),
            "--base-repository", str(self.base),
            "--legacy-adapter", str(self.legacy_adapter),
            "--output", str(output),
            "--release-commit", self.release_commit,
            "--release-evidence-commit", self.evidence_commit,
            "--protected-baseline-commit", self.protected_baseline_commit,
            "--protected-authority-kind", "REMOTE_TRACKING_REF",
            "--protected-authority-ref", "refs/remotes/origin/main",
            "--write",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        migrated = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(
            migrated["compatibility"]["views"],
            ["skills/BASE_V9_ADAPTER.json", "skills/PROJECT_BASE_SKILL_ADAPTER.json"],
        )
        for name, content in legacy_views.items():
            archive = self.project / "docs/archive/base-v9-legacy-inputs" / name
            self.assertEqual(json.loads(archive.read_text(encoding="utf-8")), content)

    def test_windows_script_runner_uses_explicit_command_array_without_shell(self) -> None:
        pub_spec = importlib.util.spec_from_file_location("publication_v3", ROOT / "tools/publication_v3.py")
        assert pub_spec and pub_spec.loader
        pub = importlib.util.module_from_spec(pub_spec)
        pub_spec.loader.exec_module(pub)
        exe = pub.safe_executable_command("C:/Poppler/pdftoppm.exe", ["-png", "input.pdf", "page"])
        self.assertEqual(exe[0], "C:/Poppler/pdftoppm.exe")
        self.assertEqual(exe[1:], ["-png", "input.pdf", "page"])
        with tempfile.TemporaryDirectory() as temporary:
            trusted = Path(temporary).resolve()
            wrapper = trusted / "safe-wrapper.cmd"
            wrapper.write_text('@echo off\r\nif "%~1"=="safe value" exit /b 0\r\nexit /b 7\r\n', encoding="utf-8")
            cmd = pub.safe_executable_command(
                str(wrapper), ["safe value"], trusted_wrapper_roots=[trusted]
            )
            self.assertTrue(Path(cmd[0]).name.lower() in {"cmd.exe", "cmd"})
            self.assertEqual(cmd[1:4], ["/d", "/s", "/c"])
            if os.name == "nt":
                executed = subprocess.run(cmd, capture_output=True, check=False)
                self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
            for metacharacter in "&|<>^()%!":
                with self.subTest(metacharacter=metacharacter):
                    with self.assertRaises(ValueError):
                        pub.safe_executable_command(
                            str(wrapper), [f"unsafe{metacharacter}arg"], trusted_wrapper_roots=[trusted]
                        )
            with self.assertRaises(ValueError):
                pub.safe_executable_command(str(wrapper), ["safe"], trusted_wrapper_roots=[trusted / "other"])
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

        project_ci = (
            ROOT / "templates/project-operations/github/validate-project-base-adapter.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}", project_ci)
        self.assertIn('--protected-base "$PR_BASE_SHA"', project_ci)
        self.assertIn("--check", project_ci)

    def test_v91_has_a_separate_candidate_lock_without_rewriting_v90(self) -> None:
        schema = json.loads((ROOT / "schemas/base-v9-1-candidate-lock-v1.schema.json").read_text(encoding="utf-8"))
        candidate = json.loads((ROOT / "base-v9.1.lock.json").read_text(encoding="utf-8"))
        self.assertFalse(list(Draft202012Validator(schema).iter_errors(candidate)))
        self.assertEqual(candidate["artifact_role"], "BASE_V9_1_RELEASE_CANDIDATE_LOCK")
        self.assertEqual(candidate["release_line"], "v9.1.0")
        self.assertEqual(candidate["release_state"], "RELEASE_CANDIDATE")
        self.assertEqual(candidate["github_issue"], 71)
        self.assertEqual(candidate["candidate_release_commit"], "3c158f52cfdad889970aef4d6ce6650a6fea0645")
        self.assertEqual(candidate["candidate_release_evidence_commit"], "dd20ad3852e264d7e337e34d2cb963f71053a6cb")
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
