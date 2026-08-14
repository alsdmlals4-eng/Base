from __future__ import annotations

import importlib.util
import inspect
import json
import os
from pathlib import Path
import tempfile
import unittest

import tools.loop_a2_runtime.openai_transport as transport
from tools.loop_a2_runtime.integration import compute_worktree_diff_sha256
from tools.loop_a2_runtime.protocol import WorkerResult
from tools.loop_a2_runtime.workspace_registry import WorkspaceOwnershipRegistry
from tests.test_loop_a2_openai_transport import _Client, _git, _repo_and_request


def _require(name: str):
    value = getattr(transport, name, None)
    if value is None:
        raise AssertionError(f"missing adversarial OpenAI transport API: {name}")
    return value


def _worker(request, paths: tuple[str, ...]) -> WorkerResult:
    return WorkerResult.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "role": "BUILDER",
            "status": "COMPLETED",
            "changed_paths": list(paths),
            "summary": "candidate",
            "usage": {"turns": 1},
            "errors": [],
        }
    )


def _owned_worktree(tmp: str):
    source, request = _repo_and_request(tmp)
    runtime_root = Path(tmp) / "runtime"
    workspace = runtime_root / request.project_id / request.run_id
    workspace.parent.mkdir(parents=True)
    completed = _git(source, "worktree", "add", "--detach", str(workspace), request.expected_main_sha)
    del completed
    registry = WorkspaceOwnershipRegistry(repo_root=source, runtime_root=runtime_root)
    registry.claim(
        project_id=request.project_id,
        run_id=request.run_id,
        expected_main_sha=request.expected_main_sha,
        workspace=workspace,
    )
    return source, runtime_root, workspace, request


class OpenAITransportAdversarialTests(unittest.TestCase):
    def test_api_key_value_in_allowed_text_is_redacted_before_builder_prompt(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        previous = os.environ.get("OPENAI_API_KEY")
        secret = "sk-test-super-secret-never-send-123456789"
        try:
            os.environ["OPENAI_API_KEY"] = secret
            with tempfile.TemporaryDirectory() as tmp:
                root, request = _repo_and_request(tmp)
                (root / "scripts/feature/existing.gd").write_text(
                    f"# accidental local text {secret}\nextends Node\n", encoding="utf-8"
                )
                client = _Client(
                    {
                        "status": "COMPLETED",
                        "summary": "safe",
                        "writes": [{"path": "scripts/feature/new.gd", "content": "extends Node\n"}],
                        "blocked_reason": "",
                    }
                )
                builder = Builder(client=client, model="builder-model")
                builder.invoke(request, worktree_path=root, repair_cycle=0)
                serialized = json.dumps(client.responses.calls, default=str)
                self.assertNotIn(secret, serialized)
                self.assertIn("[REDACTED]", serialized)
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous

    def test_builder_rejects_symlink_write_target_before_mutation(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            outside = Path(tmp) / "outside.txt"
            outside.write_text("outside\n", encoding="utf-8")
            target = root / "scripts/feature/link.gd"
            try:
                target.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "try link",
                    "writes": [{"path": "scripts/feature/link.gd", "content": "pwned\n"}],
                    "blocked_reason": "",
                }
            )
            result = Builder(client=client, model="builder-model").invoke(
                request, worktree_path=root, repair_cycle=0
            )
            self.assertEqual(result.status, "BLOCKED")
            self.assertIn("BUILDER_WRITE_PATH_UNSAFE", [error.code for error in result.errors])
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")

    def test_builder_rejects_oversized_structured_output(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        if "max_response_bytes" not in inspect.signature(Builder).parameters:
            self.fail("OpenAIWorkspaceBuilder lacks a bounded max_response_bytes contract")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            output = json.dumps(
                {
                    "status": "COMPLETED",
                    "summary": "x" * 2048,
                    "writes": [],
                    "blocked_reason": "",
                }
            )
            client = _Client(output)
            builder = Builder(
                client=client,
                model="builder-model",
                max_response_bytes=256,
            )
            result = builder.invoke(request, worktree_path=root, repair_cycle=0)
            self.assertEqual(result.status, "BLOCKED")
            self.assertIn("BUILDER_PROVIDER_OUTPUT_LIMIT", [error.code for error in result.errors])

    def test_git_review_material_is_bound_to_owned_worktree_and_actual_diff(self) -> None:
        Source = _require("GitReviewMaterialSource")
        with tempfile.TemporaryDirectory() as tmp:
            source_repo, runtime_root, workspace, request = _owned_worktree(tmp)
            file_path = workspace / "scripts/feature/existing.gd"
            file_path.write_text("extends Node\nvar verified = true\n", encoding="utf-8")
            worker = _worker(request, ("scripts/feature/existing.gd",))
            material = Source(repo_root=source_repo, runtime_root=runtime_root).collect(request, worker)
            self.assertEqual(material.changed_paths, ("scripts/feature/existing.gd",))
            self.assertIn("var verified = true", material.diff_text)
            self.assertEqual(material.diff_sha256, compute_worktree_diff_sha256(workspace))

    def test_git_review_material_rejects_declared_diff_mismatch(self) -> None:
        Source = _require("GitReviewMaterialSource")
        Error = _require("OpenAITransportError")
        with tempfile.TemporaryDirectory() as tmp:
            source_repo, runtime_root, workspace, request = _owned_worktree(tmp)
            (workspace / "scripts/feature/existing.gd").write_text(
                "extends Node\nvar changed = true\n", encoding="utf-8"
            )
            worker = _worker(request, ("scripts/feature/not-the-file.gd",))
            with self.assertRaises(Error) as caught:
                Source(repo_root=source_repo, runtime_root=runtime_root).collect(request, worker)
            self.assertEqual(caught.exception.code, "CRITIC_DIFF_ATTESTATION_MISMATCH")

    def test_git_review_material_rejects_oversized_diff_before_critic(self) -> None:
        Source = _require("GitReviewMaterialSource")
        Error = _require("OpenAITransportError")
        with tempfile.TemporaryDirectory() as tmp:
            source_repo, runtime_root, workspace, request = _owned_worktree(tmp)
            (workspace / "scripts/feature/existing.gd").write_text(
                "extends Node\n" + ("x" * 4096), encoding="utf-8"
            )
            worker = _worker(request, ("scripts/feature/existing.gd",))
            with self.assertRaises(Error) as caught:
                Source(repo_root=source_repo, runtime_root=runtime_root, max_diff_bytes=256).collect(
                    request, worker
                )
            self.assertEqual(caught.exception.code, "CRITIC_DIFF_LIMIT")

    def test_critic_must_fix_is_available_to_next_builder_repair_turn(self) -> None:
        Mailbox = _require("RepairMailbox")
        ReviewMaterial = _require("ReviewMaterial")
        Critic = _require("OpenAIWorktreeCritic")
        Builder = _require("OpenAIWorkspaceBuilder")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            mailbox = Mailbox()
            material = ReviewMaterial(
                diff_text="diff --git a/scripts/feature/a.gd b/scripts/feature/a.gd\n+bad\n",
                diff_sha256="b" * 64,
                changed_paths=("scripts/feature/a.gd",),
            )

            class Material:
                def collect(self, request, worker_result):
                    return material

            critic_client = _Client(
                {
                    "verdict": "MUST_FIX",
                    "findings": [
                        {
                            "code": "FIX_FIRST",
                            "severity": "P1",
                            "message": "fix the approved requirement",
                            "paths": ["scripts/feature/a.gd"],
                            "requirement_ids": ["REQ_001"],
                        }
                    ],
                    "checked_requirement_ids": ["REQ_001"],
                }
            )
            critic = Critic(
                client=critic_client,
                model="critic-model",
                material_source=Material(),
                repair_mailbox=mailbox,
            )
            critic.review(request, _worker(request, ("scripts/feature/a.gd",)))

            builder_client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "repair",
                    "writes": [{"path": "scripts/feature/existing.gd", "content": "extends Node\n# repaired\n"}],
                    "blocked_reason": "",
                }
            )
            builder = Builder(
                client=builder_client,
                model="builder-model",
                repair_mailbox=mailbox,
            )
            builder.invoke(request, worktree_path=root, repair_cycle=1)
            self.assertIn("FIX_FIRST", str(builder_client.responses.calls[0]["input"]))

    def test_real_component_factory_fails_closed_before_client_construction(self) -> None:
        Factory = _require("build_real_provider_components")
        Error = _require("OpenAITransportError")
        called = 0

        def client_factory():
            nonlocal called
            called += 1
            raise AssertionError("client must not be constructed before provider gate")

        keys = (
            "LOOP_A2_REAL_PROVIDER_APPROVED",
            "OPENAI_API_KEY",
            "LOOP_A2_BUILDER_MODEL",
            "LOOP_A2_CRITIC_MODEL",
        )
        previous = {key: os.environ.pop(key, None) for key in keys}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                repo, _request = _repo_and_request(tmp)
                with self.assertRaises(Error) as caught:
                    Factory(
                        repo_root=repo,
                        runtime_root=Path(tmp) / "runtime",
                        client_factory=client_factory,
                    )
                self.assertEqual(caught.exception.code, "REAL_PROVIDER_GATE_CLOSED")
                self.assertEqual(called, 0)
        finally:
            for key, value in previous.items():
                if value is not None:
                    os.environ[key] = value

    def test_pinned_openai_sdk_exposes_responses_create_without_network_call(self) -> None:
        if importlib.util.find_spec("openai") is None:
            self.skipTest("optional OpenAI provider SDK is not installed in core A2 environment")
        from openai import OpenAI

        client = OpenAI(api_key="sk-test-placeholder-never-used")
        self.assertTrue(callable(client.responses.create))


if __name__ == "__main__":
    unittest.main()
