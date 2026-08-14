from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import tools.loop_a2_runtime.openai_transport as transport
from tools.loop_a2_runtime.provider_gate import real_provider_gate
from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tests.test_loop_a2_protocol import valid_request


class _Usage:
    input_tokens = 17
    output_tokens = 23
    total_tokens = 40


class _Response:
    def __init__(self, payload: dict[str, object] | str) -> None:
        self.output_text = payload if isinstance(payload, str) else json.dumps(payload)
        self.usage = _Usage()


class _Responses:
    def __init__(self, payload: dict[str, object] | str) -> None:
        self.payload = payload
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response(self.payload)


class _Client:
    def __init__(self, payload: dict[str, object] | str) -> None:
        self.responses = _Responses(payload)


class _MaterialSource:
    def __init__(self, material) -> None:
        self.material = material
        self.calls = 0

    def collect(self, request: RunRequest, worker_result: WorkerResult):
        self.calls += 1
        return self.material


def _require(name: str):
    value = getattr(transport, name, None)
    if value is None:
        raise AssertionError(f"missing OpenAI transport API: {name}")
    return value


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )
    return completed.stdout.strip()


def _write_contracts(root: Path) -> None:
    loop = root / "docs" / "operations" / "loop"
    loop.mkdir(parents=True, exist_ok=True)
    (loop / "PROJECT_EXECUTION_CAPSULE.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "contract_role": "LOOP_PROJECT_EXECUTION_CAPSULE",
                "project_id": "BLACKSMITH",
                "planning_lock_path": "PLANNING_LOCK.json",
                "visual_lock_path": "VISUAL_LOCK.json",
                "runtime_adapter_path": "RUNTIME_ADAPTER.json",
                "implementation_package_path": "IMPLEMENTATION_PACKAGE.json",
                "coverage_ledger_path": "REQUIREMENT_COVERAGE_LEDGER.json",
            }
        ),
        encoding="utf-8",
    )
    (loop / "IMPLEMENTATION_PACKAGE.json").write_text(
        json.dumps({"package_id": "PACKAGE_001", "requirements": ["REQ_001"]}),
        encoding="utf-8",
    )
    (loop / "PLANNING_LOCK.json").write_text(
        json.dumps({"status": "PLANNING_LOCKED"}), encoding="utf-8"
    )
    (loop / "VISUAL_LOCK.json").write_text(
        json.dumps({"status": "VISUAL_NOT_APPLICABLE"}), encoding="utf-8"
    )
    (loop / "RUNTIME_ADAPTER.json").write_text(
        json.dumps({"provider": "TEST"}), encoding="utf-8"
    )
    (loop / "REQUIREMENT_COVERAGE_LEDGER.json").write_text(
        json.dumps({"requirements": ["REQ_001"]}), encoding="utf-8"
    )


def _repo_and_request(tmp: str) -> tuple[Path, RunRequest]:
    root = Path(tmp) / "project"
    root.mkdir()
    _git(root, "init")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Loop Test")
    _write_contracts(root)
    target = root / "scripts" / "feature"
    target.mkdir(parents=True)
    (target / "existing.gd").write_text("extends Node\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "baseline")
    value = valid_request()
    value["provider_mode"] = "REAL"
    value["expected_main_sha"] = _git(root, "rev-parse", "HEAD")
    return root, RunRequest.from_dict(value)


class OpenAITransportContractTests(unittest.TestCase):
    def test_bounded_openai_transport_module_exists(self) -> None:
        self.assertIsNotNone(transport)

    def test_real_gate_requires_explicit_distinct_builder_and_critic_models(self) -> None:
        keys = (
            "LOOP_A2_REAL_PROVIDER_APPROVED",
            "OPENAI_API_KEY",
            "LOOP_A2_BUILDER_MODEL",
            "LOOP_A2_CRITIC_MODEL",
        )
        previous = {key: os.environ.get(key) for key in keys}
        try:
            os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = "1"
            os.environ["OPENAI_API_KEY"] = "test-only-redacted-placeholder"
            os.environ.pop("LOOP_A2_BUILDER_MODEL", None)
            os.environ.pop("LOOP_A2_CRITIC_MODEL", None)
            missing = real_provider_gate()
            self.assertEqual(missing["status"], "USER_DECISION_REQUIRED")
            self.assertEqual(missing["code"], "REAL_PROVIDER_MODELS_NOT_SELECTED")

            os.environ["LOOP_A2_BUILDER_MODEL"] = "MODEL_A"
            os.environ["LOOP_A2_CRITIC_MODEL"] = "MODEL_A"
            same = real_provider_gate()
            self.assertEqual(same["status"], "USER_DECISION_REQUIRED")
            self.assertEqual(same["code"], "REAL_PROVIDER_MODELS_NOT_INDEPENDENT")

            os.environ["LOOP_A2_CRITIC_MODEL"] = "MODEL_B"
            ready = real_provider_gate()
            self.assertEqual(ready["status"], "READY")
            self.assertEqual(ready["code"], "REAL_PROVIDER_GATE_PASS")
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_builder_uses_structured_responses_and_applies_only_local_write_plan(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "add bounded feature",
                    "writes": [
                        {"path": "scripts/feature/new.gd", "content": "extends Node\n"}
                    ],
                    "blocked_reason": "",
                }
            )
            builder = Builder(client=client, model="builder-model", max_output_tokens=512)
            result = builder.invoke(request, worktree_path=root, repair_cycle=0)

            self.assertEqual(result.status, "COMPLETED")
            self.assertEqual(result.changed_paths, ("scripts/feature/new.gd",))
            self.assertEqual((root / "scripts/feature/new.gd").read_text(encoding="utf-8"), "extends Node\n")
            self.assertEqual(len(client.responses.calls), 1)
            call = client.responses.calls[0]
            self.assertEqual(call["model"], "builder-model")
            self.assertIs(call["store"], False)
            self.assertEqual(call["timeout"], request.budgets.timeout_seconds)
            self.assertEqual(call["max_output_tokens"], 512)
            self.assertNotIn("tools", call)
            fmt = call["text"]["format"]
            self.assertEqual(fmt["type"], "json_schema")
            self.assertIs(fmt["strict"], True)
            self.assertEqual(fmt["name"], "loop_a2_builder_write_plan")
            usage = builder.usage_snapshot()
            self.assertEqual(usage["request_count"], 1)
            self.assertEqual(usage["input_tokens"], 17)
            self.assertEqual(usage["output_tokens"], 23)
            self.assertEqual(usage["total_tokens"], 40)

    def test_builder_blocks_out_of_scope_write_without_touching_workspace(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "bad proposal",
                    "writes": [{"path": "README.md", "content": "not allowed\n"}],
                    "blocked_reason": "",
                }
            )
            builder = Builder(client=client, model="builder-model")
            result = builder.invoke(request, worktree_path=root, repair_cycle=0)
            self.assertEqual(result.status, "BLOCKED")
            self.assertIn("BUILDER_WRITE_SCOPE_VIOLATION", [item.code for item in result.errors])
            self.assertFalse((root / "README.md").exists())
            self.assertEqual(_git(root, "status", "--porcelain"), "")

    def test_builder_fails_closed_before_api_when_context_exceeds_budget(self) -> None:
        Builder = _require("OpenAIWorkspaceBuilder")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            (root / "docs/operations/loop/PLANNING_LOCK.json").write_text(
                json.dumps({"status": "PLANNING_LOCKED", "blob": "x" * 2048}),
                encoding="utf-8",
            )
            client = _Client({"status": "BLOCKED", "summary": "unused", "writes": [], "blocked_reason": "unused"})
            builder = Builder(client=client, model="builder-model", max_context_bytes=256)
            result = builder.invoke(request, worktree_path=root, repair_cycle=0)
            self.assertEqual(result.status, "BLOCKED")
            self.assertIn("BUILDER_CONTEXT_LIMIT", [item.code for item in result.errors])
            self.assertEqual(client.responses.calls, [])

    def test_critic_is_read_only_and_returns_identity_bound_review(self) -> None:
        ReviewMaterial = _require("ReviewMaterial")
        Critic = _require("OpenAIWorktreeCritic")
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            before = _git(root, "status", "--porcelain")
            material = ReviewMaterial(
                diff_text="diff --git a/scripts/feature/a.gd b/scripts/feature/a.gd\n+pass\n",
                diff_sha256="a" * 64,
                changed_paths=("scripts/feature/a.gd",),
            )
            client = _Client(
                {
                    "verdict": "PASS",
                    "findings": [],
                    "checked_requirement_ids": ["REQ_001"],
                }
            )
            critic = Critic(
                client=client,
                model="critic-model",
                material_source=_MaterialSource(material),
                max_output_tokens=384,
            )
            worker = WorkerResult.from_dict(
                {
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_WORKER_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "BUILDER",
                    "status": "COMPLETED",
                    "changed_paths": ["scripts/feature/a.gd"],
                    "summary": "candidate",
                    "usage": {"turns": 1},
                    "errors": [],
                }
            )
            review = critic.review(request, worker)
            after = _git(root, "status", "--porcelain")

            self.assertEqual(review.verdict, "PASS")
            self.assertEqual(review.project_id, request.project_id)
            self.assertEqual(review.expected_main_sha, request.expected_main_sha)
            self.assertEqual(review.checked_requirement_ids, ("REQ_001",))
            self.assertEqual(before, after)
            call = client.responses.calls[0]
            self.assertEqual(call["model"], "critic-model")
            self.assertIs(call["store"], False)
            self.assertNotIn("tools", call)
            self.assertIn("a" * 64, json.dumps(call, default=str))
            self.assertEqual(call["text"]["format"]["name"], "loop_a2_critic_review")


if __name__ == "__main__":
    unittest.main()
