from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from tools.project_integration_capsule import (
    _git,
    _is_rfc3339,
    _safe_child,
    validate_capsule,
)
from tools.base_release_index import (
    RELEASE_FINALIZATION_COMMITS,
    install_release_lock_paths,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/project-integration-capsule-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/PROJECT_INTEGRATION_CAPSULE.json"
CLI = ROOT / "tools/check_project_integration_capsule.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


class ProjectIntegrationCapsuleContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name)
        run_git(self.project, "init", "-b", "main")
        run_git(self.project, "config", "user.email", "capsule@example.invalid")
        run_git(self.project, "config", "user.name", "Capsule Test")
        run_git(
            self.project,
            "remote",
            "add",
            "origin",
            "https://github.com/owner/capsule-test.git",
        )
        base_lock = json.loads((ROOT / "base-v9.4.3.lock.json").read_text(encoding="utf-8"))
        (self.project / "project.godot").write_text(
            '[application]\nconfig/name="Capsule Test"\n',
            encoding="utf-8",
        )
        (self.project / "docs").mkdir()
        (self.project / "docs/CURRENT_CONFIRMED_DECISIONS.md").write_text(
            "# Decisions\n\n"
            "- DEC-INTEGRATION-001 — APPROVED\n"
            "- Approval: https://github.com/owner/capsule-test/issues/1\n"
            "- Project ID: capsule-test\n"
            "- Repository: owner/capsule-test\n"
            "- Notion Project Key: CAPSULE_TEST\n"
            "- Notion Record Key: CAPSULE_TEST::SYSTEM::INTEGRATION_CANARY\n",
            encoding="utf-8",
        )
        (self.project / "skills").mkdir()
        (self.project / "skills/PROJECT_BASE_ADAPTER.json").write_text(
            json.dumps(
                {
                    "artifact_role": "PROJECT_BASE_ADAPTER",
                    "base_release": {
                        "finalization_commit": RELEASE_FINALIZATION_COMMITS["9.4.3"],
                        "release_commit": base_lock["candidate_release_commit"],
                        "release_evidence_commit": base_lock[
                            "candidate_release_evidence_commit"
                        ],
                        "repository": base_lock["repository"],
                        "version": "9.4.3",
                    },
                    "compatibility": {"cycle": "ONE_CYCLE", "legacy_inputs": {}, "views": []},
                    "gdd_sheet": {
                        "role": "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
                        "sync_status": "NOT_CONFIGURED",
                        "workspace_status": "MIGRATION_COMPATIBILITY_SURFACE",
                    },
                    "project": {
                        "engine": "Godot 4.5.1",
                        "project_id": "capsule-test",
                        "repository": "owner/capsule-test",
                        "root": ".",
                    },
                    "protected_baseline": {
                        "authority_kind": "REMOTE_TRACKING_REF",
                        "authority_ref": "refs/remotes/origin/main",
                        "commit": "1" * 40,
                        "policy_sha256": "1" * 64,
                        "policy_source_path": "skills/LEGACY_PROJECT_ADAPTER.json",
                        "policy_source_type": "FIRST_MIGRATION_LEGACY_SOURCE",
                        "protected_paths_pointer": "/protected_paths",
                    },
                    "protected_paths": ["project.godot", "**/*.gd", "**/*.tscn"],
                    "routing": {
                        "aliases": [],
                        "base_routes": [],
                        "inactive_routes": [],
                        "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
                        "project_routes": [],
                    },
                    "schema_version": 2,
                    "shared_overrides": {},
                    "skill_registry": {
                        "base": {
                            **base_lock["candidate_registry"],
                        },
                        "project": {
                            "hash_definition": "RAW_FILE_BYTES_SHA256",
                            "path": "skills/SKILL_REGISTRY.json",
                            "sha256": "1" * 64,
                        },
                    },
                    "validators": [
                        "python tools/check_project_operating_contract.py --project-root . --base-repository ../Base --check"
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.project / "docs/operations").mkdir()
        (self.project / "docs/operations/HIGODOT_ADOPTION_RECORD.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "artifact_role": "HIGODOT_ADOPTION_RECORD",
                    "provider": "hi-godot/godot-ai",
                    "exact_release_or_commit": "0123456789abcdef0123456789abcdef01234567",
                    "godot_version": "4.5.1",
                    "host_clients": {
                        "codex": "CONFIGURED",
                        "gpt_vscode": "NOT_CONFIGURED",
                        "deepseek": "FORBIDDEN",
                    },
                    "network_mode": "LOOPBACK_ONLY",
                    "enabled_domains": ["EDITOR_READ"],
                    "unverified_domains": [],
                    "last_verified_at": "2026-08-20T00:00:00Z",
                    "verification_evidence": ["evidence/writer-canary.json"],
                    "rollback_release_or_commit": "fedcba9876543210fedcba9876543210fedcba98",
                    "connection_status": "PASS",
                    "runtime_status": "NOT_RUN",
                    "regression_status": "NOT_RUN",
                    "production_readiness": False,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.project / "evidence").mkdir()
        (self.project / "evidence/notion-readback.json").write_text(
            '{"access_mode":"SEARCH_FETCH_ONLY","existing_page_write":"FORBIDDEN",'
            '"last_edited":"2026-08-20T00:00:00Z","project":"CAPSULE_TEST",'
            '"project_relation_count":1,'
            '"record_key":"CAPSULE_TEST::SYSTEM::INTEGRATION_CANARY",'
            '"revision":1,"source":"NOTION_OFFICIAL_MCP_SEARCH_FETCH",'
            '"status":"PASS"}\n',
            encoding="utf-8",
        )
        (self.project / "evidence/writer-canary.json").write_text(
            '{"attempted_actor":"CODEX","attempted_path":"project.godot",'
            '"authoring_provider":"hi-godot/godot-ai",'
            '"blocked_paths":["project.godot","**/*.gd","**/*.tscn","**/*.tres",'
            '"**/*.res","**/*.scn"],"observed":"BLOCKED",'
            '"operation_level":"L0_OBSERVE","second_writer_blocked":true,'
            '"status":"PASS"}\n',
            encoding="utf-8",
        )
        run_git(
            self.project,
            "add",
            "project.godot",
            "skills/PROJECT_BASE_ADAPTER.json",
            "docs/CURRENT_CONFIRMED_DECISIONS.md",
            "docs/operations/HIGODOT_ADOPTION_RECORD.json",
            "evidence/notion-readback.json",
            "evidence/writer-canary.json",
        )
        run_git(self.project, "commit", "-m", "test: seed integration fixture")
        self.head = run_git(self.project, "rev-parse", "HEAD")
        run_git(self.project, "update-ref", "refs/remotes/origin/main", self.head)
        self.capsule = self._ready_capsule()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _ready_capsule(self) -> dict[str, object]:
        godot_hash = sha256(self.project / "project.godot")
        notion_evidence_hash = sha256(self.project / "evidence/notion-readback.json")
        writer_evidence_hash = sha256(self.project / "evidence/writer-canary.json")
        base_adapter_hash = sha256(self.project / "skills/PROJECT_BASE_ADAPTER.json")
        adoption_record_hash = sha256(
            self.project / "docs/operations/HIGODOT_ADOPTION_RECORD.json"
        )
        return {
            "schema_version": 1,
            "artifact_role": "PROJECT_INTEGRATION_CAPSULE",
            "authority": "READ_ONLY_BINDING_NOT_CANON",
            "status": "READ_ONLY_BINDING_VERIFIED",
            "project": {
                "project_id": "capsule-test",
                "repository": "owner/capsule-test",
                "base_branch": "main",
                "worktree_branch": "main",
                "base_sha": self.head,
                "result_sha": self.head,
                "worktree_relative_root": ".",
            },
            "decision": {
                "decision_id": "DEC-INTEGRATION-001",
                "approval_status": "APPROVED",
                "approval_ref": "https://github.com/owner/capsule-test/issues/1",
                "decision_record_path": "docs/CURRENT_CONFIRMED_DECISIONS.md",
            },
            "authority_refs": {
                "workspace": "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",
                "notion_isolation": "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md",
                "gpt_codex": "docs/GPT_CODEX_WORKFLOW_POLICY.md",
                "godot": "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
            },
            "base_adapter": {
                "path": "skills/PROJECT_BASE_ADAPTER.json",
                "sha256": base_adapter_hash,
            },
            "notion": {
                "access_mode": "SEARCH_FETCH_ONLY",
                "project_relation_count": 1,
                "project_key": "CAPSULE_TEST",
                "record_key": "CAPSULE_TEST::SYSTEM::INTEGRATION_CANARY",
                "revision": 1,
                "last_edited": "2026-08-20T00:00:00Z",
                "readback_status": "PASS",
                "existing_page_write": "FORBIDDEN",
            },
            "codex": {
                "workspace_access": "LOCAL_WORKTREE_NATIVE",
                "godot_direct_write": "FORBIDDEN",
                "mutation_authority": "NONE_READ_ONLY",
                "external_connectors_during_mutation": "DISABLED",
            },
            "godot": {
                "engine": "GODOT",
                "authoring_provider": "hi-godot/godot-ai",
                "writer_authority": "SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY",
                "adoption_record_path": "docs/operations/HIGODOT_ADOPTION_RECORD.json",
                "adoption_record_sha256": adoption_record_hash,
                "network_mode": "LOOPBACK_ONLY",
                "operation_level": "L0_OBSERVE",
                "editor_project_root": ".",
                "project_godot_sha256": godot_hash,
                "direct_filesystem_write_enforcement": "PASS",
            },
            "change_boundary": {
                "write_allowlist": [],
                "codex_forbidden_godot_paths": [
                    "project.godot",
                    "**/*.gd",
                    "**/*.tscn",
                    "**/*.tres",
                    "**/*.res",
                    "**/*.scn",
                ],
                "unexpected_tracked_diff": "PASS",
            },
            "cost_surface": {
                "boundary": "ZERO_INCREMENTAL_COST_REQUIRED",
                "allowed_service_classes": [
                    "GPT_PRO",
                    "NOTION_FREE",
                    "LOCAL_OPEN_SOURCE_TOOLS",
                ],
                "prohibited_metered_services": [
                    "OPENAI_API_PAYG",
                    "PAID_CI_RUNNER",
                    "PAID_NOTION_AI",
                    "PAID_REMOTE_HOSTING",
                ],
                "status": "DECLARED_ZERO_INCREMENTAL_COST_POLICY",
            },
            "acceptance": [
                {
                    "acceptance_id": "ACC_READ_ONLY_BINDING",
                    "statement": "Bind one exact project across Git, Notion, and Godot without product-file mutation.",
                    "status": "PASS",
                    "evidence_ids": ["EVID_NOTION_READBACK", "EVID_WRITER_EXCLUSIVITY"],
                }
            ],
            "evidence": [
                {
                    "evidence_id": "EVID_NOTION_READBACK",
                    "level": "E3_RUNTIME",
                    "kind": "NOTION_READBACK",
                    "path": "evidence/notion-readback.json",
                    "sha256": notion_evidence_hash,
                },
                {
                    "evidence_id": "EVID_WRITER_EXCLUSIVITY",
                    "level": "E2_TEST",
                    "kind": "WRITER_EXCLUSIVITY_CANARY",
                    "path": "evidence/writer-canary.json",
                    "sha256": writer_evidence_hash,
                }
            ],
            "rollback": {
                "rollback_ref": self.head,
                "procedure": "Restore rollback_ref in an isolated worktree and rerun the capsule check.",
                "drill_status": "NOT_APPLICABLE",
            },
            "reality_gate": {
                "exact_head": "PASS",
                "notion_readback": "PASS",
                "godot_import": "NOT_APPLICABLE",
                "writer_exclusivity": "PASS",
                "rollback_drill": "NOT_APPLICABLE",
                "final_status": "READ_ONLY_BINDING_VERIFIED",
            },
            "evidence_ceiling": "LOCAL_RECEIPT_BINDING_ONLY",
        }

    def _write_capsule(self, payload: dict[str, object]) -> Path:
        path = self.project / "PROJECT_INTEGRATION_CAPSULE.json"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _commit_fixture_changes(self, payload: dict[str, object], *paths: str) -> None:
        run_git(self.project, "add", *paths)
        run_git(self.project, "commit", "-m", "test: update integration fixture")
        self.head = run_git(self.project, "rev-parse", "HEAD")
        run_git(self.project, "update-ref", "refs/remotes/origin/main", self.head)
        payload["project"]["base_sha"] = self.head  # type: ignore[index]
        payload["project"]["result_sha"] = self.head  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = self.head  # type: ignore[index]

    def test_ready_capsule_binds_exact_git_notion_godot_and_evidence(self) -> None:
        path = self._write_capsule(self.capsule)

        findings = validate_capsule(path, project_root=self.project)

        self.assertEqual(findings, [])

    def test_only_canonical_adapter_path_is_accepted(self) -> None:
        copied = self.project / "PROJECT_BASE_ADAPTER.json"
        copied.write_bytes(
            (self.project / "skills/PROJECT_BASE_ADAPTER.json").read_bytes()
        )
        payload = deepcopy(self.capsule)
        payload["base_adapter"]["path"] = "PROJECT_BASE_ADAPTER.json"  # type: ignore[index]
        payload["base_adapter"]["sha256"] = sha256(copied)  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("NONCANONICAL_BASE_ADAPTER_PATH", codes)

    def test_canonical_v1_adapter_remains_read_only_binding_compatible(self) -> None:
        payload = deepcopy(self.capsule)
        adapter_path = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        adapter["schema_version"] = 1
        del adapter["project"]["project_id"]
        adapter["gdd_sheet"]["role"] = "USER_FACING_GDD_WORKSPACE"
        adapter_path.write_text(json.dumps(adapter, indent=2) + "\n", encoding="utf-8")
        payload["base_adapter"]["sha256"] = sha256(adapter_path)  # type: ignore[index]
        self._commit_fixture_changes(payload, "skills/PROJECT_BASE_ADAPTER.json")
        path = self._write_capsule(payload)

        findings = validate_capsule(path, project_root=self.project)

        self.assertEqual(findings, [])

    def test_exact_higodot_release_tags_are_accepted_but_floating_refs_are_not(self) -> None:
        payload = deepcopy(self.capsule)
        adoption_path = self.project / "docs/operations/HIGODOT_ADOPTION_RECORD.json"
        adoption = json.loads(adoption_path.read_text(encoding="utf-8"))
        adoption["exact_release_or_commit"] = "v1.2.3"
        adoption["rollback_release_or_commit"] = "v1.2.2"
        adoption_path.write_text(json.dumps(adoption, indent=2) + "\n", encoding="utf-8")
        payload["godot"]["adoption_record_sha256"] = sha256(adoption_path)  # type: ignore[index]
        self._commit_fixture_changes(payload, "docs/operations/HIGODOT_ADOPTION_RECORD.json")
        path = self._write_capsule(payload)

        self.assertEqual(validate_capsule(path, project_root=self.project), [])

        adoption["exact_release_or_commit"] = "latest"
        adoption_path.write_text(json.dumps(adoption, indent=2) + "\n", encoding="utf-8")
        payload["godot"]["adoption_record_sha256"] = sha256(adoption_path)  # type: ignore[index]
        path = self._write_capsule(payload)
        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("HIGODOT_ADOPTION_UNVERIFIED", codes)

    def test_nul_in_any_relative_path_fails_closed(self) -> None:
        mutations = (
            ("project", "worktree_relative_root"),
            ("decision", "decision_record_path"),
            ("base_adapter", "path"),
            ("godot", "adoption_record_path"),
            ("godot", "editor_project_root"),
        )
        for section, field in mutations:
            with self.subTest(section=section, field=field):
                payload = deepcopy(self.capsule)
                payload[section][field] = "bad\x00path"  # type: ignore[index]
                path = self._write_capsule(payload)
                codes = {
                    finding.code
                    for finding in validate_capsule(path, project_root=self.project)
                }
                self.assertIn("SCHEMA_INVALID", codes)

        payload = deepcopy(self.capsule)
        payload["evidence"][0]["path"] = "bad\x00receipt.json"  # type: ignore[index]
        path = self._write_capsule(payload)
        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}
        self.assertIn("SCHEMA_INVALID", codes)
        self.assertIsNone(_safe_child(self.project, "bad\x00path"))

    def test_invalid_utf8_decision_record_returns_a_finding(self) -> None:
        payload = deepcopy(self.capsule)
        decision_path = self.project / "docs/CURRENT_CONFIRMED_DECISIONS.md"
        decision_path.write_bytes(b"\xff")
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("DECISION_RECORD_UNREADABLE", codes)

    def test_git_wrapper_surrogateescapes_non_utf8_output(self) -> None:
        raw_name = b"non-utf8-\xff.txt"
        raw_path = bytes(self.project) + b"/" + raw_name
        descriptor = os.open(raw_path, os.O_CREAT | os.O_WRONLY)
        os.close(descriptor)
        run_git(self.project, "add", raw_name.decode("utf-8", errors="surrogateescape"))

        completed = _git(self.project, "ls-files", "-z")

        self.assertEqual(completed.returncode, 0)
        self.assertIn("\udcff", completed.stdout)

    def test_git_wrapper_returns_a_structured_failure_when_git_cannot_start(self) -> None:
        with patch(
            "tools.project_integration_capsule.subprocess.run",
            side_effect=OSError("git executable unavailable"),
        ):
            completed = _git(self.project, "status", "--porcelain")

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("git executable unavailable", completed.stderr)

    def test_git_wrapper_disables_lazy_fetch_locks_and_fsmonitor(self) -> None:
        completed = subprocess.CompletedProcess(["git"], 0, "", "")
        with patch.dict(
            os.environ,
            {
                "GIT_DIR": "/tmp/alternate.git",
                "GIT_WORK_TREE": "/tmp/alternate-worktree",
                "GIT_INDEX_FILE": "/tmp/alternate-index",
            },
        ):
            with patch(
                "tools.project_integration_capsule.subprocess.run",
                return_value=completed,
            ) as run:
                _git(self.project, "rev-parse", "HEAD")

        command = run.call_args.args[0]
        environment = run.call_args.kwargs["env"]
        self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
        self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
        self.assertNotIn("GIT_DIR", environment)
        self.assertNotIn("GIT_WORK_TREE", environment)
        self.assertNotIn("GIT_INDEX_FILE", environment)
        self.assertIn("core.fsmonitor=false", command)

    def test_ambient_git_repository_selection_cannot_redirect_validation(self) -> None:
        path = self._write_capsule(self.capsule)
        with tempfile.TemporaryDirectory() as alternate_directory:
            alternate = Path(alternate_directory)
            run_git(alternate, "init", "-b", "main")
            run_git(alternate, "config", "user.email", "alternate@example.invalid")
            run_git(alternate, "config", "user.name", "Alternate Test")
            (alternate / "alternate.txt").write_text("other repository\n", encoding="utf-8")
            run_git(alternate, "add", "alternate.txt")
            run_git(alternate, "commit", "-m", "test: seed alternate repository")

            with patch.dict(
                os.environ,
                {
                    "GIT_DIR": str(alternate / ".git"),
                    "GIT_WORK_TREE": str(self.project),
                    "GIT_INDEX_FILE": str(alternate / ".git/index"),
                },
            ):
                findings = validate_capsule(path, project_root=self.project)

        self.assertEqual(findings, [])

    def test_rfc3339_gate_rejects_iso8601_superset_spellings(self) -> None:
        self.assertTrue(_is_rfc3339("2026-08-20T00:00:00Z"))
        self.assertTrue(_is_rfc3339("2026-08-20t00:00:00.123+09:30"))
        for non_rfc3339 in (
            "2026-08-20 00:00:00+00:00",
            "2026-08-20T00:00:00+0000",
            "2026-08-20T00:00:00",
        ):
            with self.subTest(value=non_rfc3339):
                self.assertFalse(_is_rfc3339(non_rfc3339))

    def test_template_is_schema_valid_but_cannot_claim_runtime_readiness(self) -> None:
        self.assertTrue(SCHEMA.is_file())
        self.assertTrue(TEMPLATE.is_file())
        self.assertEqual(validate_capsule(TEMPLATE, schema_only=True), [])

        codes = {finding.code for finding in validate_capsule(TEMPLATE)}

        self.assertIn("CAPSULE_NOT_CONFIGURED", codes)

    def test_blocked_status_cannot_pass_the_readiness_gate(self) -> None:
        payload = deepcopy(self.capsule)
        payload["status"] = "BLOCKED_UNVERIFIED"
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("CAPSULE_STATUS_NOT_READY", codes)

    def test_read_only_binding_rejects_commit_delta_and_dirty_tracked_files(self) -> None:
        original_head = self.head
        (self.project / "notes.txt").write_text("committed mutation\n", encoding="utf-8")
        run_git(self.project, "add", "notes.txt")
        run_git(self.project, "commit", "-m", "test: create forbidden observation delta")
        mutated_head = run_git(self.project, "rev-parse", "HEAD")
        payload = deepcopy(self.capsule)
        payload["project"]["base_sha"] = original_head  # type: ignore[index]
        payload["project"]["result_sha"] = mutated_head  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = original_head  # type: ignore[index]
        path = self._write_capsule(payload)

        delta_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("READ_ONLY_COMMIT_DELTA", delta_codes)

        payload["project"]["base_sha"] = mutated_head  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = mutated_head  # type: ignore[index]
        (self.project / "project.godot").write_text("dirty tracked mutation\n", encoding="utf-8")
        path = self._write_capsule(payload)

        dirty_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("TRACKED_WORKTREE_DIRTY", dirty_codes)

    @unittest.skipIf(os.name == "nt", "POSIX executable bits are not portable on Windows")
    def test_tracked_executable_mode_drift_is_rejected(self) -> None:
        payload = deepcopy(self.capsule)
        path = self._write_capsule(payload)
        project_file = self.project / "project.godot"
        os.chmod(project_file, project_file.stat().st_mode | 0o111)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("TRACKED_FILE_MODE_MISMATCH", codes)
        self.assertIn("TRACKED_WORKTREE_DIRTY", codes)

    def test_repository_and_base_branch_identity_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        payload["project"]["repository"] = "other-owner/other-project"  # type: ignore[index]
        payload["project"]["base_branch"] = "missing-branch"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("REPOSITORY_IDENTITY_MISMATCH", codes)
        self.assertIn("BASE_BRANCH_UNRESOLVABLE", codes)

    def test_decision_and_cross_system_project_identity_are_verified(self) -> None:
        payload = deepcopy(self.capsule)
        payload["decision"]["approval_status"] = "NOT_CONFIGURED"  # type: ignore[index]
        payload["decision"]["decision_record_path"] = "docs/MISSING.md"  # type: ignore[index]
        payload["notion"]["project_key"] = "OTHER_PROJECT"  # type: ignore[index]
        payload["notion"]["record_key"] = (  # type: ignore[index]
            "OTHER_PROJECT::SYSTEM::INTEGRATION_CANARY"
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("DECISION_UNAPPROVED", codes)
        self.assertIn("DECISION_RECORD_MISSING", codes)

        payload["decision"]["approval_status"] = "APPROVED"  # type: ignore[index]
        payload["decision"]["decision_record_path"] = (  # type: ignore[index]
            "docs/CURRENT_CONFIRMED_DECISIONS.md"
        )
        path = self._write_capsule(payload)
        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("CROSS_SYSTEM_PROJECT_MISMATCH", codes)

    def test_nested_directory_cannot_impersonate_the_git_worktree_root(self) -> None:
        nested = self.project / "nested"
        nested.mkdir()
        (nested / "project.godot").write_bytes((self.project / "project.godot").read_bytes())
        payload = deepcopy(self.capsule)
        payload["project"]["worktree_relative_root"] = "nested"  # type: ignore[index]
        payload["godot"]["editor_project_root"] = "nested"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("WORKTREE_ROOT_MISMATCH", codes)

    def test_notion_timestamp_and_receipt_semantics_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        payload["notion"]["last_edited"] = "not-a-timestamp"  # type: ignore[index]
        (self.project / "evidence/notion-readback.json").write_text(
            '{}\n', encoding="utf-8"
        )
        payload["evidence"][0]["sha256"] = sha256(  # type: ignore[index]
            self.project / "evidence/notion-readback.json"
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("NOTION_LAST_EDITED_INVALID", codes)
        self.assertIn("NOTION_EVIDENCE_MISMATCH", codes)

    def test_writer_canary_receipt_semantics_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        (self.project / "evidence/writer-canary.json").write_text(
            '{"second_writer_blocked":true,"status":"PASS"}\n',
            encoding="utf-8",
        )
        payload["evidence"][1]["sha256"] = sha256(  # type: ignore[index]
            self.project / "evidence/writer-canary.json"
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("WRITER_CANARY_EVIDENCE_MISMATCH", codes)

    def test_untracked_evidence_cannot_support_readiness(self) -> None:
        payload = deepcopy(self.capsule)
        untracked = self.project / "evidence/untracked-notion-readback.json"
        untracked.write_bytes((self.project / "evidence/notion-readback.json").read_bytes())
        payload["evidence"][0]["path"] = "evidence/untracked-notion-readback.json"  # type: ignore[index]
        payload["evidence"][0]["sha256"] = sha256(untracked)  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("EVIDENCE_NOT_AT_RESULT_SHA", codes)

    def test_cost_allowlist_blocks_reclassified_metered_service(self) -> None:
        payload = deepcopy(self.capsule)
        payload["cost_surface"]["allowed_service_classes"] = [  # type: ignore[index]
            "GPT_PRO",
            "NOTION_FREE",
            "LOCAL_OPEN_SOURCE_TOOLS",
            "OPENAI_API_PAYG",
        ]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("SCHEMA_INVALID", codes)

    def test_cost_surface_is_a_declared_policy_not_billing_evidence(self) -> None:
        payload = deepcopy(self.capsule)
        payload["cost_surface"]["status"] = "SUBSCRIPTION_INCLUDED"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("SCHEMA_INVALID", codes)

    def test_base_adapter_and_higodot_adoption_are_bound_not_duplicated(self) -> None:
        payload = deepcopy(self.capsule)
        adapter_path = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        adapter["project"]["repository"] = "other-owner/other-project"
        adapter_path.write_text(json.dumps(adapter, indent=2) + "\n", encoding="utf-8")
        payload["base_adapter"]["sha256"] = sha256(adapter_path)  # type: ignore[index]

        adoption_path = self.project / "docs/operations/HIGODOT_ADOPTION_RECORD.json"
        adoption = json.loads(adoption_path.read_text(encoding="utf-8"))
        adoption["exact_release_or_commit"] = "NOT_CONFIGURED"
        adoption_path.write_text(json.dumps(adoption, indent=2) + "\n", encoding="utf-8")
        payload["godot"]["adoption_record_sha256"] = sha256(adoption_path)  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("BASE_ADAPTER_PROJECT_MISMATCH", codes)
        self.assertIn("HIGODOT_ADOPTION_UNVERIFIED", codes)

    def test_required_second_writer_paths_cannot_be_omitted(self) -> None:
        payload = deepcopy(self.capsule)
        payload["change_boundary"]["codex_forbidden_godot_paths"] = [  # type: ignore[index]
            "project.godot"
        ]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("CHANGE_BOUNDARY_INCOMPLETE", codes)

    def test_untracked_and_ignored_godot_authoring_files_are_rejected(self) -> None:
        payload = deepcopy(self.capsule)
        path = self._write_capsule(payload)
        (self.project / "rogue.gd").write_text("extends Node\n", encoding="utf-8")

        untracked_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("UNTRACKED_PROJECT_FILE", untracked_codes)

        (self.project / "rogue.gd").unlink()
        (self.project / ".git/info/exclude").write_text(
            "*.gdshader\n", encoding="utf-8"
        )
        (self.project / "hidden.gdshader").write_text(
            "shader_type canvas_item;\n", encoding="utf-8"
        )

        ignored_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("IGNORED_GODOT_AUTHORING_FILE", ignored_codes)

    def test_failed_untracked_and_ignored_scans_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        (self.project / "evil.gd").write_text("extends Node\n", encoding="utf-8")
        run_git(self.project, "config", "core.excludesFile", str(self.project))
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("UNTRACKED_SCAN_UNREADABLE", codes)
        self.assertIn("IGNORED_SCAN_UNREADABLE", codes)

    def test_corrupt_index_makes_every_index_probe_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        index_path = self.project / ".git/index"
        index_path.unlink()
        index_path.mkdir()
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("INDEX_TREE_UNREADABLE", codes)
        self.assertIn("INDEX_VISIBILITY_SCAN_UNREADABLE", codes)

    def test_git_index_visibility_overrides_cannot_hide_mutation(self) -> None:
        payload = deepcopy(self.capsule)
        path = self._write_capsule(payload)
        run_git(self.project, "update-index", "--skip-worktree", "project.godot")
        (self.project / "project.godot").write_text("hidden mutation\n", encoding="utf-8")
        payload["godot"]["project_godot_sha256"] = sha256(  # type: ignore[index]
            self.project / "project.godot"
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("GIT_INDEX_VISIBILITY_OVERRIDE", codes)

    def test_remote_tracking_base_must_match_the_recorded_base(self) -> None:
        payload = deepcopy(self.capsule)
        remote_commit = run_git(
            self.project,
            "commit-tree",
            f"{self.head}^{{tree}}",
            "-p",
            self.head,
            "-m",
            "remote-only commit",
        )
        run_git(self.project, "update-ref", "refs/remotes/origin/main", remote_commit)
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("REMOTE_BASE_SHA_MISMATCH", codes)

    def test_acceptance_evidence_and_rollback_claims_are_coherent(self) -> None:
        payload = deepcopy(self.capsule)
        payload["acceptance"][0]["evidence_ids"] = ["EVID_NOTION_READBACK"]  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = "1" * 40  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("ORPHAN_REQUIRED_EVIDENCE", codes)
        self.assertIn("ROLLBACK_BASE_MISMATCH", codes)

    def test_decision_record_must_be_tracked_at_result_sha(self) -> None:
        payload = deepcopy(self.capsule)
        copied = self.project / "docs/UNTRACKED_DECISION.md"
        copied.write_bytes(
            (self.project / "docs/CURRENT_CONFIRMED_DECISIONS.md").read_bytes()
        )
        payload["decision"]["decision_record_path"] = "docs/UNTRACKED_DECISION.md"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("DECISION_RECORD_NOT_AT_RESULT_SHA", codes)

    def test_notion_record_key_requires_project_type_and_local_id(self) -> None:
        payload = deepcopy(self.capsule)
        payload["notion"]["record_key"] = "CAPSULE_TEST::ONLY_TYPE"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("NOTION_RECORD_KEY_INVALID", codes)

    def test_git_clean_filter_cannot_hide_raw_worktree_byte_mutation(self) -> None:
        (self.project / ".gitattributes").write_text(
            "project.godot filter=hidechanges\n", encoding="utf-8"
        )
        run_git(self.project, "add", ".gitattributes")
        run_git(self.project, "commit", "-m", "test: configure adversarial clean filter")
        filtered_head = run_git(self.project, "rev-parse", "HEAD")
        run_git(self.project, "update-ref", "refs/remotes/origin/main", filtered_head)
        run_git(
            self.project,
            "config",
            "filter.hidechanges.clean",
            "git show HEAD:project.godot",
        )
        payload = deepcopy(self.capsule)
        payload["project"]["base_sha"] = filtered_head  # type: ignore[index]
        payload["project"]["result_sha"] = filtered_head  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = filtered_head  # type: ignore[index]
        (self.project / "project.godot").write_text("filter-hidden mutation\n", encoding="utf-8")
        payload["godot"]["project_godot_sha256"] = sha256(  # type: ignore[index]
            self.project / "project.godot"
        )
        path = self._write_capsule(payload)

        self.assertEqual(run_git(self.project, "diff", "--name-only"), "")
        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("TRACKED_FILE_BYTES_MISMATCH", codes)

    def test_validator_never_executes_repository_clean_filters(self) -> None:
        payload = deepcopy(self.capsule)
        marker = self.project / ".git/validator-executed"
        (self.project / ".gitattributes").write_text(
            "project.godot filter=sidefx\n", encoding="utf-8"
        )
        self._commit_fixture_changes(payload, ".gitattributes")
        run_git(
            self.project,
            "config",
            "filter.sidefx.clean",
            f"touch {marker}; cat",
        )
        path = self._write_capsule(payload)

        findings = validate_capsule(path, project_root=self.project)

        self.assertEqual(findings, [])
        self.assertFalse(marker.exists())

    def test_all_tracked_files_use_raw_bytes_without_clean_filters(self) -> None:
        payload = deepcopy(self.capsule)
        marker = self.project / ".git/noncritical-filter-executed"
        (self.project / "notes.txt").write_text("canonical\n", encoding="utf-8")
        (self.project / ".gitattributes").write_text(
            "notes.txt filter=sidefx\n", encoding="utf-8"
        )
        self._commit_fixture_changes(payload, ".gitattributes", "notes.txt")
        run_git(
            self.project,
            "config",
            "filter.sidefx.clean",
            f"touch {marker}; cat",
        )
        (self.project / "notes.txt").write_text("hidden mutation\n", encoding="utf-8")
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("TRACKED_FILE_BYTES_MISMATCH", codes)
        self.assertFalse(marker.exists())

    def test_index_tree_mismatch_cannot_hide_behind_head_matching_worktree_bytes(self) -> None:
        payload = deepcopy(self.capsule)
        notes = self.project / "notes.txt"
        notes.write_text("canonical\n", encoding="utf-8")
        self._commit_fixture_changes(payload, "notes.txt")
        notes.write_text("staged mutation\n", encoding="utf-8")
        run_git(self.project, "add", "notes.txt")
        notes.write_text("canonical\n", encoding="utf-8")
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("INDEX_TREE_MISMATCH", codes)

    def test_gitlinks_are_rejected_from_read_only_snapshot_binding(self) -> None:
        payload = deepcopy(self.capsule)
        run_git(
            self.project,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.head},addons/ext",
        )
        run_git(self.project, "commit", "-m", "test: add unsupported gitlink")
        self.head = run_git(self.project, "rev-parse", "HEAD")
        run_git(self.project, "update-ref", "refs/remotes/origin/main", self.head)
        payload["project"]["base_sha"] = self.head  # type: ignore[index]
        payload["project"]["result_sha"] = self.head  # type: ignore[index]
        payload["rollback"]["rollback_ref"] = self.head  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("GITLINK_UNSUPPORTED", codes)

    def test_ignored_godot_script_cannot_hide_as_generated_cache(self) -> None:
        payload = deepcopy(self.capsule)
        (self.project / ".gitignore").write_text(".godot/\n", encoding="utf-8")
        (self.project / "project.godot").write_text(
            '[application]\nconfig/name="Capsule Test"\n'
            '[autoload]\nEvil="*res://.godot/evil.gd"\n',
            encoding="utf-8",
        )
        payload["godot"]["project_godot_sha256"] = sha256(  # type: ignore[index]
            self.project / "project.godot"
        )
        self._commit_fixture_changes(payload, ".gitignore", "project.godot")
        (self.project / ".godot").mkdir()
        (self.project / ".godot/evil.gd").write_text(
            "extends Node\n", encoding="utf-8"
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("IGNORED_GODOT_AUTHORING_FILE", codes)

    def test_known_generated_godot_editor_cache_remains_allowed(self) -> None:
        payload = deepcopy(self.capsule)
        (self.project / ".gitignore").write_text(".godot/\n", encoding="utf-8")
        self._commit_fixture_changes(payload, ".gitignore")
        (self.project / ".godot/editor").mkdir(parents=True)
        (self.project / ".godot/editor/filesystem_cache8").write_text(
            "generated\n", encoding="utf-8"
        )
        path = self._write_capsule(payload)

        self.assertEqual(validate_capsule(path, project_root=self.project), [])

    def test_tracked_symlinks_are_rejected_instead_of_followed(self) -> None:
        payload = deepcopy(self.capsule)
        os.symlink("project.godot", self.project / "linked-project.godot")
        self._commit_fixture_changes(payload, "linked-project.godot")
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("SYMLINK_UNSUPPORTED", codes)

    def test_human_playtest_or_other_evidence_cannot_exceed_v1_ceiling(self) -> None:
        payload = deepcopy(self.capsule)
        payload["acceptance"][0]["statement"] = (  # type: ignore[index]
            "Human playtest and production delivery passed."
        )
        payload["evidence"].append(  # type: ignore[union-attr]
            {
                "evidence_id": "EVID-HUMAN-001",
                "level": "E6_HUMAN_PLAYTEST",
                "kind": "OTHER",
                "path": "evidence/playtest.json",
                "sha256": "1" * 64,
            }
        )
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("SCHEMA_INVALID", codes)

    def test_rollback_drill_state_cannot_contradict_not_applicable_reality(self) -> None:
        payload = deepcopy(self.capsule)
        payload["rollback"]["drill_status"] = "FAIL"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("ROLLBACK_DRILL_STATE_INVALID", codes)

    def test_adapter_release_identity_must_match_the_canonical_lock(self) -> None:
        payload = deepcopy(self.capsule)
        adapter_path = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        adapter["base_release"]["release_commit"] = run_git(ROOT, "rev-parse", "HEAD^")
        adapter_path.write_text(json.dumps(adapter, indent=2) + "\n", encoding="utf-8")
        payload["base_adapter"]["sha256"] = sha256(adapter_path)  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("BASE_RELEASE_UNVERIFIED", codes)

    def test_base_release_git_checks_use_the_fail_closed_capsule_runner(self) -> None:
        payload = deepcopy(self.capsule)
        path = self._write_capsule(payload)
        real_run = subprocess.run
        base_git_environments: list[dict[str, str]] = []

        def observe_run(command: list[str], *args: object, **kwargs: object):
            if command and command[0] == "git" and str(ROOT) in command:
                environment = kwargs.get("env")
                self.assertIsInstance(environment, dict)
                base_git_environments.append(environment)  # type: ignore[arg-type]
            return real_run(command, *args, **kwargs)

        with patch(
            "tools.project_integration_capsule.subprocess.run",
            side_effect=observe_run,
        ):
            findings = validate_capsule(path, project_root=self.project)

        self.assertEqual(findings, [])
        self.assertTrue(base_git_environments)
        for environment in base_git_environments:
            self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
            self.assertNotIn("GIT_DIR", environment)

    def test_base_release_git_start_failure_becomes_a_local_finding(self) -> None:
        payload = deepcopy(self.capsule)
        path = self._write_capsule(payload)
        real_run = subprocess.run

        def fail_base_git(command: list[str], *args: object, **kwargs: object):
            if command and command[0] == "git" and str(ROOT) in command:
                raise OSError("Base Git unavailable")
            return real_run(command, *args, **kwargs)

        with patch(
            "tools.project_integration_capsule.subprocess.run",
            side_effect=fail_base_git,
        ):
            codes = {
                finding.code
                for finding in validate_capsule(path, project_root=self.project)
            }

        self.assertIn("BASE_RELEASE_UNVERIFIED", codes)

    def test_release_index_preserves_legacy_two_argument_validator_calls(self) -> None:
        legacy = ModuleType("legacy_project_operating_contract")
        legacy.RELEASE_LOCK_PATHS = {}  # type: ignore[attr-defined]
        observed: list[tuple[dict[str, object], Path]] = []

        def legacy_release_lock_contract(
            adapter: dict[str, object], base_repository: Path
        ) -> tuple[list[str], dict[str, object], None]:
            observed.append((adapter, base_repository))
            return [], {}, None

        legacy._release_lock_contract = legacy_release_lock_contract  # type: ignore[attr-defined]
        legacy._trusted_protected_base = lambda *args: (None, [])  # type: ignore[attr-defined]
        legacy._git = lambda *args: subprocess.CompletedProcess([], 1, "", "")  # type: ignore[attr-defined]
        legacy._resolve_commit = lambda *args: None  # type: ignore[attr-defined]
        legacy._commit_exists = lambda *args: False  # type: ignore[attr-defined]
        legacy._is_ancestor = lambda *args: False  # type: ignore[attr-defined]
        install_release_lock_paths(legacy)
        adapter: dict[str, object] = {"base_release": {}}

        result = legacy._release_lock_contract(adapter, self.project)  # type: ignore[attr-defined]

        self.assertEqual(result, ([], {}, None))
        self.assertEqual(observed, [(adapter, self.project)])

    def test_malformed_nested_adapter_object_fails_as_a_finding(self) -> None:
        payload = deepcopy(self.capsule)
        adapter_path = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        adapter["project"] = []
        adapter_path.write_text(json.dumps(adapter, indent=2) + "\n", encoding="utf-8")
        payload["base_adapter"]["sha256"] = sha256(adapter_path)  # type: ignore[index]
        path = self._write_capsule(payload)

        adapter_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("BASE_ADAPTER_INVALID", adapter_codes)

    def test_malformed_nested_adoption_object_fails_as_a_finding(self) -> None:
        payload = deepcopy(self.capsule)
        adoption_path = self.project / "docs/operations/HIGODOT_ADOPTION_RECORD.json"
        adoption = json.loads(adoption_path.read_text(encoding="utf-8"))
        adoption["host_clients"] = []
        adoption_path.write_text(json.dumps(adoption, indent=2) + "\n", encoding="utf-8")
        payload["godot"]["adoption_record_sha256"] = sha256(adoption_path)  # type: ignore[index]
        path = self._write_capsule(payload)

        adoption_codes = {
            finding.code for finding in validate_capsule(path, project_root=self.project)
        }

        self.assertIn("HIGODOT_ADOPTION_UNVERIFIED", adoption_codes)

    def test_malformed_writer_receipt_fails_as_a_finding(self) -> None:
        payload = deepcopy(self.capsule)
        receipt_path = self.project / "evidence/writer-canary.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["blocked_paths"] = [{}]
        receipt_path.write_text(json.dumps(receipt) + "\n", encoding="utf-8")
        payload["evidence"][1]["sha256"] = sha256(receipt_path)  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("WRITER_CANARY_EVIDENCE_MISMATCH", codes)

    def test_dual_writer_metered_cost_and_notion_identity_fail_closed(self) -> None:
        payload = deepcopy(self.capsule)
        payload["codex"]["godot_direct_write"] = "ALLOWED"  # type: ignore[index]
        payload["cost_surface"]["status"] = "POLICY_NOT_ADOPTED"  # type: ignore[index]
        payload["notion"]["record_key"] = "OTHER_PROJECT::SYSTEM::INTEGRATION_CANARY"  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertTrue(
            {"SECOND_GODOT_WRITER", "COST_GATE_BLOCKED", "NOTION_PROJECT_MISMATCH"}.issubset(codes)
        )

    def test_stale_head_and_godot_fingerprint_are_rejected(self) -> None:
        payload = deepcopy(self.capsule)
        payload["project"]["result_sha"] = "1" * 40  # type: ignore[index]
        payload["godot"]["project_godot_sha256"] = "2" * 64  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("STALE_RESULT_SHA", codes)
        self.assertIn("PROJECT_GODOT_FINGERPRINT_MISMATCH", codes)

    def test_missing_or_tampered_evidence_is_rejected(self) -> None:
        payload = deepcopy(self.capsule)
        payload["evidence"][0]["sha256"] = "3" * 64  # type: ignore[index]
        path = self._write_capsule(payload)

        codes = {finding.code for finding in validate_capsule(path, project_root=self.project)}

        self.assertIn("EVIDENCE_HASH_MISMATCH", codes)

    def test_cli_emits_machine_readable_findings(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(CLI),
                str(TEMPLATE),
                "--format",
                "json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 1)
        findings = json.loads(completed.stdout)
        self.assertIn("CAPSULE_NOT_CONFIGURED", {item["code"] for item in findings})

    def test_cli_output_stays_utf8_with_non_utf8_git_filenames(self) -> None:
        path = self._write_capsule(self.capsule)
        raw_path = bytes(self.project) + b"/untracked-\xff.tscn"
        descriptor = os.open(raw_path, os.O_CREAT | os.O_WRONLY)
        os.close(descriptor)
        control_path = bytes(self.project) + b"/untracked-\x1b.tscn"
        descriptor = os.open(control_path, os.O_CREAT | os.O_WRONLY)
        os.close(descriptor)

        for output_format in ("json", "text"):
            with self.subTest(output_format=output_format):
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(CLI),
                        str(path),
                        "--project-root",
                        str(self.project),
                        "--format",
                        output_format,
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    check=False,
                )
                decoded = completed.stdout.decode("utf-8")
                self.assertEqual(completed.returncode, 1)
                self.assertNotIn("\x1b", decoded)
                if output_format == "json":
                    findings = json.loads(decoded)
                    self.assertIn(
                        "UNTRACKED_PROJECT_FILE",
                        {item["code"] for item in findings},
                    )


if __name__ == "__main__":
    unittest.main()
