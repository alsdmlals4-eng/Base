from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from tools.loop_a2_runtime.openai_transport import OpenAIWorkspaceBuilder
from tests.test_loop_a2_openai_transport import _Client, _repo_and_request


class OpenAITransportAuthorityTests(unittest.TestCase):
    def test_builder_never_writes_capsule_or_lock_files_even_with_overbroad_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            request = replace(
                request,
                allowed_paths=("scripts/feature/**", "docs/operations/loop/**"),
            )
            planning = root / "docs/operations/loop/PLANNING_LOCK.json"
            original = planning.read_text(encoding="utf-8")
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "attempt authority mutation",
                    "writes": [
                        {"path": "scripts/feature/should_not_land.gd", "content": "extends Node\n"},
                        {"path": "docs/operations/loop/PLANNING_LOCK.json", "content": "{}\n"},
                    ],
                    "blocked_reason": "",
                }
            )
            result = OpenAIWorkspaceBuilder(client=client, model="builder-model").invoke(
                request,
                worktree_path=root,
                repair_cycle=0,
            )
            self.assertEqual(result.status, "BLOCKED")
            self.assertIn(
                "BUILDER_AUTHORITY_WRITE_FORBIDDEN",
                [error.code for error in result.errors],
            )
            self.assertEqual(planning.read_text(encoding="utf-8"), original)
            self.assertFalse((root / "scripts/feature/should_not_land.gd").exists())


if __name__ == "__main__":
    unittest.main()
