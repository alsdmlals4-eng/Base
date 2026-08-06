from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
ADOPTION_PATH = ROOT / "templates/project-operations/HIGODOT_ADOPTION_RECORD.json"
GODOT_SKILL_PATH = (
    ROOT
    / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
)
POLICY_RELATIVE = "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
OWNER_PATHS = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
    ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md",
    ROOT / "skills/evolving-project-discipline-skills/SKILL.md",
    ROOT / "skills/managing-game-project-operating-system/SKILL.md",
)


class HiGodotSingleAuthorityPolicyTests(unittest.TestCase):
    def test_global_entrypoints_require_existing_solution_first(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        for marker in (
            "Existing Solution First Gate",
            "REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW",
            POLICY_RELATIVE,
        ):
            self.assertIn(marker, agents)
        self.assertIn("신규 MCP·addon·CLI·framework·Skill·Mode", start)
        self.assertIn(POLICY_RELATIVE, start)

    def test_canonical_policy_names_one_provider_and_keeps_destructive_features(self) -> None:
        self.assertTrue(POLICY_PATH.is_file())
        policy = POLICY_PATH.read_text(encoding="utf-8")
        for marker in (
            "hi-godot/godot-ai",
            "SOLE_GODOT_EXECUTION_AUTHORITY",
            "authority_count: 1",
            "Node deletion",
            "file creation, modification, move, or deletion",
            "project settings",
            "autoload",
            "L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE",
            "L3_HIGH_IMPACT_CHANGE",
        ):
            self.assertIn(marker, policy)
        self.assertIn("Base custom MCP", policy)
        self.assertIn("STOP_AND_ARCHIVE", policy)
        self.assertIn("Hera", policy)
        self.assertIn("BENCHMARK_REFERENCE_ONLY", policy)

    def test_policy_mitigates_tool_context_identity_transport_and_update_risks(self) -> None:
        policy = POLICY_PATH.read_text(encoding="utf-8")
        for marker in (
            "progressive schema discovery",
            "one primary domain",
            "DeepSeek Analysis",
            "MCP registration: absent",
            "credential: absent",
            "LOOPBACK_ONLY",
            "LAN_FORBIDDEN",
            "PUBLIC_URL_FORBIDDEN",
            "PORT_FORWARDING_FORBIDDEN",
            "REMOTE_TUNNEL_FORBIDDEN",
            "exact release or commit",
            "destructive canary",
            "project regression",
            "rollback",
            "production readiness",
        ):
            self.assertIn(marker, policy)

    def test_existing_solution_gate_is_owned_by_existing_skills(self) -> None:
        for path in OWNER_PATHS:
            self.assertTrue(path.is_file(), str(path))
            body = path.read_text(encoding="utf-8")
            self.assertIn(POLICY_RELATIVE, body, str(path))

        evaluation = OWNER_PATHS[0].read_text(encoding="utf-8")
        for marker in (
            "inventory-current-environment",
            "REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW",
            "connected MCP",
            "open and recently merged PR",
        ):
            self.assertIn(marker, evaluation)

        intake = OWNER_PATHS[1].read_text(encoding="utf-8")
        self.assertIn("existing_solution_disposition", intake)
        self.assertIn("BUILD_NEW", intake)

        evolution = OWNER_PATHS[2].read_text(encoding="utf-8")
        self.assertIn("external solution", evolution)
        self.assertIn("BUILD_NEW", evolution)

        operating = OWNER_PATHS[3].read_text(encoding="utf-8")
        for marker in ("HiGodot", "exact pin", "canary", "rollback"):
            self.assertIn(marker, operating)

    def test_project_godot_skill_routes_only_to_higodot(self) -> None:
        self.assertTrue(GODOT_SKILL_PATH.is_file())
        skill = GODOT_SKILL_PATH.read_text(encoding="utf-8")
        for marker in (
            "HiGodot",
            "SOLE_GODOT_EXECUTION_AUTHORITY",
            "L0_OBSERVE",
            "L1_REVERSIBLE_WRITE",
            "L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE",
            "L3_HIGH_IMPACT_CHANGE",
            "Node deletion",
            "file write",
            "project settings",
            "autoload",
            "DeepSeek",
            "LOOPBACK_ONLY",
        ):
            self.assertIn(marker, skill)
        self.assertNotIn("canonical addon을 복사", skill)
        self.assertNotIn("base_live_editor_adapter/", skill)

    def test_adoption_record_is_exact_pinned_and_fail_closed(self) -> None:
        self.assertTrue(ADOPTION_PATH.is_file())
        payload = json.loads(ADOPTION_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["artifact_role"], "HIGODOT_ADOPTION_RECORD")
        self.assertEqual(payload["provider"], "hi-godot/godot-ai")
        self.assertEqual(payload["host_clients"]["deepseek"], "FORBIDDEN")
        self.assertEqual(payload["network_mode"], "LOOPBACK_ONLY")
        self.assertEqual(payload["exact_release_or_commit"], "NOT_CONFIGURED")
        self.assertEqual(payload["rollback_release_or_commit"], "NOT_CONFIGURED")
        self.assertEqual(payload["runtime_status"], "NOT_RUN")
        self.assertEqual(payload["regression_status"], "NOT_RUN")
        self.assertFalse(payload["production_readiness"])

    def test_no_active_shared_mcp_configuration_is_committed(self) -> None:
        for path in (
            ROOT / ".vscode/mcp.json",
            ROOT / ".codex/config.toml",
            ROOT / "templates/project-operations/.vscode/mcp.json",
            ROOT / "templates/project-operations/.codex/config.toml",
        ):
            self.assertFalse(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
