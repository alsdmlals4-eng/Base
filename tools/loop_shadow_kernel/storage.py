from __future__ import annotations

import json
import os
import re
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

from .canonical import digest_json


_IDENTIFIER = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")


class ReceiptExistsError(FileExistsError):
    pass


class ReceiptCorruptError(ValueError):
    pass


class UnsafeStateTreeError(ValueError):
    pass


class LeaseLedgerBusyError(RuntimeError):
    pass


class LeaseLedgerCorruptError(ValueError):
    pass


def _validate_identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"{label} is not a safe identifier")
    return value


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReceiptCorruptError(f"invalid JSON at {path}: {error}") from error


class StateStorage:
    def __init__(self, state_root: Path) -> None:
        self.state_root = state_root

    def _assert_inside_state_root(self, path: Path) -> None:
        root = self.state_root.resolve(strict=False)
        candidate = path.resolve(strict=False)
        if candidate != root and root not in candidate.parents:
            raise UnsafeStateTreeError(f"state path escapes reserved root: {path}")

        try:
            relative = path.relative_to(self.state_root)
        except ValueError as error:
            raise UnsafeStateTreeError(f"state path is not lexically confined: {path}") from error
        current = self.state_root
        if current.is_symlink():
            raise UnsafeStateTreeError(f"state root is a symlink: {current}")
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise UnsafeStateTreeError(f"state path traverses a symlink: {current}")

    def _safe_mkdir(self, directory: Path) -> None:
        try:
            relative = directory.relative_to(self.state_root)
        except ValueError as error:
            raise UnsafeStateTreeError(f"directory escapes state root: {directory}") from error

        current = self.state_root
        if current.is_symlink():
            raise UnsafeStateTreeError(f"state root is a symlink: {current}")
        if not current.exists():
            current.mkdir()
        elif not current.is_dir():
            raise UnsafeStateTreeError(f"state root is not a directory: {current}")

        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise UnsafeStateTreeError(f"state directory is a symlink: {current}")
            if current.exists():
                if not current.is_dir():
                    raise UnsafeStateTreeError(f"state path component is not a directory: {current}")
            else:
                current.mkdir()
        self._assert_inside_state_root(directory)

    def project_root(self, project_id: str) -> Path:
        safe_project = _validate_identifier(project_id, "project_id")
        return self.state_root / "projects" / safe_project

    def receipt_path(self, project_id: str, run_id: str) -> Path:
        safe_run = _validate_identifier(run_id, "run_id")
        return self.project_root(project_id) / "runs" / safe_run / "receipt.json"

    def receipt_exists(self, project_id: str, run_id: str) -> bool:
        path = self.receipt_path(project_id, run_id)
        self._assert_inside_state_root(path)
        return path.is_file()

    def _write_json_exclusive(self, path: Path, value: Any) -> None:
        self._safe_mkdir(path.parent)
        self._assert_inside_state_root(path)
        data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError as error:
                raise ReceiptExistsError(str(path)) from error
            except OSError as error:
                if path.exists():
                    raise ReceiptExistsError(str(path)) from error
                raise
        finally:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass

    def _atomic_replace_json(self, path: Path, value: Any) -> None:
        self._safe_mkdir(path.parent)
        self._assert_inside_state_root(path)
        data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()

    def write_receipt(self, receipt: dict[str, Any]) -> dict[str, Any]:
        unsigned = dict(receipt)
        unsigned.pop("receipt_digest", None)
        signed = dict(unsigned)
        signed["receipt_digest"] = digest_json(unsigned)
        self._write_json_exclusive(
            self.receipt_path(str(signed["project_id"]), str(signed["run_id"])),
            signed,
        )
        return signed

    def read_receipt(self, project_id: str, run_id: str) -> dict[str, Any]:
        path = self.receipt_path(project_id, run_id)
        self._assert_inside_state_root(path)
        value = _read_json(path)
        if not isinstance(value, dict):
            raise ReceiptCorruptError(f"receipt is not an object: {path}")
        digest = value.get("receipt_digest")
        if not isinstance(digest, str):
            raise ReceiptCorruptError(f"receipt digest is missing: {path}")
        unsigned = dict(value)
        unsigned.pop("receipt_digest", None)
        if digest_json(unsigned) != digest:
            raise ReceiptCorruptError(f"receipt digest mismatch: {path}")
        return value

    def iter_receipts(self, project_id: str) -> Iterable[dict[str, Any]]:
        runs_root = self.project_root(project_id) / "runs"
        self._assert_inside_state_root(runs_root)
        if not runs_root.is_dir():
            return ()
        receipts: list[dict[str, Any]] = []
        for path in sorted(runs_root.glob("*/receipt.json")):
            receipts.append(self.read_receipt(project_id, path.parent.name))
        return tuple(receipts)

    def leases_path(self, project_id: str) -> Path:
        return self.project_root(project_id) / "leases.json"

    def lease_lock_path(self, project_id: str) -> Path:
        return self.project_root(project_id) / "leases.lock"

    def read_leases(self, project_id: str) -> list[dict[str, str]]:
        path = self.leases_path(project_id)
        self._assert_inside_state_root(path)
        if not path.is_file():
            return []
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise UnsafeStateTreeError(f"invalid lease ledger: {path}: {error}") from error
        if not isinstance(value, list):
            raise UnsafeStateTreeError(f"lease ledger is not a list: {path}")
        leases: list[dict[str, str]] = []
        seen_resources: set[str] = set()
        for item in value:
            if not isinstance(item, dict):
                raise UnsafeStateTreeError(f"lease ledger item is invalid: {path}")
            resource = item.get("resource")
            run_id = item.get("run_id")
            if not isinstance(resource, str) or not resource or not isinstance(run_id, str):
                raise UnsafeStateTreeError(f"lease ledger item is incomplete: {path}")
            _validate_identifier(run_id, "lease run_id")
            resource_key = resource.casefold()
            if resource_key in seen_resources:
                raise LeaseLedgerCorruptError(
                    f"duplicate normalized lease resource: {resource}"
                )
            seen_resources.add(resource_key)
            leases.append({"resource": resource, "run_id": run_id})
        return sorted(leases, key=lambda item: (item["resource"].casefold(), item["run_id"]))

    def _write_leases_unlocked(self, project_id: str, leases: list[dict[str, str]]) -> None:
        self._atomic_replace_json(
            self.leases_path(project_id),
            sorted(leases, key=lambda item: (item["resource"].casefold(), item["run_id"])),
        )

    @contextmanager
    def _lease_guard(self, project_id: str) -> Iterator[None]:
        lock = self.lease_lock_path(project_id)
        self._safe_mkdir(lock.parent)
        self._assert_inside_state_root(lock)
        descriptor: int | None = None
        for _ in range(20):
            try:
                descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                break
            except FileExistsError:
                time.sleep(0.01)
        if descriptor is None:
            raise LeaseLedgerBusyError(f"lease ledger guard is already held: {lock}")
        try:
            os.write(descriptor, b"LOCKED\n")
            os.fsync(descriptor)
            yield
        finally:
            os.close(descriptor)
            try:
                lock.unlink()
            except FileNotFoundError:
                pass

    def acquire_leases(
        self,
        project_id: str,
        run_id: str,
        resources: tuple[str, ...],
    ) -> tuple[dict[str, str], ...]:
        _validate_identifier(run_id, "run_id")
        with self._lease_guard(project_id):
            existing = self.read_leases(project_id)
            by_resource = {item["resource"].casefold(): item for item in existing}
            conflicts = tuple(
                by_resource[resource.casefold()]
                for resource in resources
                if resource.casefold() in by_resource
                and by_resource[resource.casefold()]["run_id"] != run_id
            )
            if conflicts:
                return conflicts
            merged = list(existing)
            for resource in sorted(resources, key=str.casefold):
                if resource.casefold() not in by_resource:
                    item = {"resource": resource, "run_id": run_id}
                    merged.append(item)
                    by_resource[resource.casefold()] = item
            self._write_leases_unlocked(project_id, merged)
            return ()

    def release_leases(self, project_id: str, run_id: str) -> None:
        _validate_identifier(run_id, "run_id")
        with self._lease_guard(project_id):
            existing = self.read_leases(project_id)
            retained = [item for item in existing if item["run_id"] != run_id]
            if retained != existing:
                self._write_leases_unlocked(project_id, retained)
