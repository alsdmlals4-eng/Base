from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from .evidence import canonical_receipt


_IDENTIFIER = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")


class WorkspaceOwnershipError(RuntimeError):
    pass


def _identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise WorkspaceOwnershipError(f"{label} is not a closed identifier")
    return value


def _sha(value: str) -> str:
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise WorkspaceOwnershipError("expected_main_sha is invalid")
    return value


def _verify_digest(value: Mapping[str, Any]) -> dict[str, Any]:
    receipt = dict(value)
    digest = receipt.pop("receipt_digest", None)
    if not isinstance(digest, str):
        raise WorkspaceOwnershipError("ownership receipt digest is missing")
    expected = canonical_receipt(receipt)["receipt_digest"]
    if digest != expected:
        raise WorkspaceOwnershipError("ownership receipt digest mismatch")
    receipt["receipt_digest"] = digest
    return receipt


class WorkspaceOwnershipRegistry:
    """Durable, fail-closed ownership receipts for external A2 worktrees."""

    def __init__(self, *, repo_root: Path | str, runtime_root: Path | str) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self.runtime_root = Path(runtime_root).resolve(strict=False)
        if self.runtime_root == self.repo_root or self.repo_root in self.runtime_root.parents:
            raise WorkspaceOwnershipError("runtime_root must remain outside the source repository")
        self.ownership_root = self.runtime_root / ".loop-ownership"

    def _assert_safe_tree(self, path: Path, *, allow_missing: bool) -> None:
        runtime = self.runtime_root
        candidate = path.resolve(strict=False)
        if candidate != runtime and runtime not in candidate.parents:
            raise WorkspaceOwnershipError("path escapes runtime_root")
        try:
            relative = path.relative_to(runtime)
        except ValueError as exc:
            raise WorkspaceOwnershipError("path is not lexically runtime-bound") from exc
        current = runtime
        if current.is_symlink():
            raise WorkspaceOwnershipError("runtime_root must not be a symlink")
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise WorkspaceOwnershipError("path traverses a symlink")
            if not allow_missing and not current.exists():
                raise WorkspaceOwnershipError("path is missing")

    def _safe_mkdir(self, directory: Path) -> None:
        try:
            relative = directory.relative_to(self.runtime_root)
        except ValueError as exc:
            raise WorkspaceOwnershipError("ownership directory escapes runtime_root") from exc
        current = self.runtime_root
        if current.is_symlink():
            raise WorkspaceOwnershipError("runtime_root must not be a symlink")
        current.mkdir(parents=True, exist_ok=True)
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise WorkspaceOwnershipError("ownership directory traverses a symlink")
            if current.exists() and not current.is_dir():
                raise WorkspaceOwnershipError("ownership path component is not a directory")
            current.mkdir(exist_ok=True)
        self._assert_safe_tree(directory, allow_missing=False)

    def receipt_path(self, project_id: str, run_id: str) -> Path:
        project = _identifier(project_id, "project_id")
        run = _identifier(run_id, "run_id")
        path = self.ownership_root / project / f"{run}.json"
        self._assert_safe_tree(path, allow_missing=True)
        return path

    def validate_workspace_path(
        self,
        *,
        project_id: str,
        run_id: str,
        workspace: Path | str,
    ) -> Path:
        project = _identifier(project_id, "project_id")
        run = _identifier(run_id, "run_id")
        lexical = self.runtime_root / project / run
        supplied = Path(workspace)
        try:
            supplied.relative_to(self.runtime_root)
        except ValueError as exc:
            raise WorkspaceOwnershipError("workspace is not lexically runtime-bound") from exc
        if supplied != lexical:
            raise WorkspaceOwnershipError("workspace path does not match the closed project/run namespace")
        self._assert_safe_tree(supplied, allow_missing=True)
        canonical = supplied.resolve(strict=False)
        if canonical == self.runtime_root or self.runtime_root not in canonical.parents:
            raise WorkspaceOwnershipError("workspace escapes runtime_root")
        return canonical

    def _payload(
        self,
        *,
        project_id: str,
        run_id: str,
        expected_main_sha: str,
        workspace: Path | str,
    ) -> dict[str, Any]:
        project = _identifier(project_id, "project_id")
        run = _identifier(run_id, "run_id")
        expected = _sha(expected_main_sha)
        canonical_workspace = self.validate_workspace_path(
            project_id=project,
            run_id=run,
            workspace=workspace,
        )
        return {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKSPACE_OWNERSHIP",
            "project_id": project,
            "run_id": run,
            "expected_main_sha": expected,
            "source_repo": str(self.repo_root),
            "workspace": str(canonical_workspace),
        }

    def preflight_claim(
        self,
        *,
        project_id: str,
        run_id: str,
        expected_main_sha: str,
        workspace: Path | str,
    ) -> None:
        self._payload(
            project_id=project_id,
            run_id=run_id,
            expected_main_sha=expected_main_sha,
            workspace=workspace,
        )
        path = self.receipt_path(project_id, run_id)
        if path.exists() or path.is_symlink():
            raise WorkspaceOwnershipError("ownership receipt already exists")

    def claim(
        self,
        *,
        project_id: str,
        run_id: str,
        expected_main_sha: str,
        workspace: Path | str,
    ) -> dict[str, Any]:
        self.preflight_claim(
            project_id=project_id,
            run_id=run_id,
            expected_main_sha=expected_main_sha,
            workspace=workspace,
        )
        payload = self._payload(
            project_id=project_id,
            run_id=run_id,
            expected_main_sha=expected_main_sha,
            workspace=workspace,
        )
        receipt = canonical_receipt(payload)
        path = self.receipt_path(project_id, run_id)
        self._safe_mkdir(path.parent)
        try:
            with path.open("x", encoding="utf-8") as handle:
                json.dump(receipt, handle, ensure_ascii=False, sort_keys=True, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError as exc:
            raise WorkspaceOwnershipError("ownership receipt already exists") from exc
        return receipt

    def read(self, project_id: str, run_id: str) -> dict[str, Any]:
        path = self.receipt_path(project_id, run_id)
        self._assert_safe_tree(path, allow_missing=False)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkspaceOwnershipError("ownership receipt is unreadable") from exc
        if not isinstance(value, dict):
            raise WorkspaceOwnershipError("ownership receipt is not an object")
        return _verify_digest(value)

    def verify(
        self,
        *,
        project_id: str,
        run_id: str,
        expected_main_sha: str,
        workspace: Path | str,
    ) -> dict[str, Any]:
        expected = self._payload(
            project_id=project_id,
            run_id=run_id,
            expected_main_sha=expected_main_sha,
            workspace=workspace,
        )
        receipt = self.read(project_id, run_id)
        for key, value in expected.items():
            if receipt.get(key) != value:
                raise WorkspaceOwnershipError(f"ownership receipt {key} mismatch")
        if set(receipt) != set(expected) | {"receipt_digest"}:
            raise WorkspaceOwnershipError("ownership receipt has an unexpected field")
        return receipt

    def remove(
        self,
        *,
        project_id: str,
        run_id: str,
        expected_main_sha: str,
        workspace: Path | str,
    ) -> None:
        self.verify(
            project_id=project_id,
            run_id=run_id,
            expected_main_sha=expected_main_sha,
            workspace=workspace,
        )
        path = self.receipt_path(project_id, run_id)
        path.unlink()
        try:
            path.parent.rmdir()
        except OSError:
            pass
