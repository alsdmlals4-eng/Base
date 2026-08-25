#!/usr/bin/env python3
"""Canonical compatible Base release-lock index for project operating CLIs."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any, Callable


RELEASE_LOCK_PATHS = {
    "9.1.0": Path("base-v9.1.lock.json"),
    "9.2.0": Path("base-v9.2.lock.json"),
    "9.3.0": Path("base-v9.3.lock.json"),
    "9.4.0": Path("base-v9.4.lock.json"),
    "9.4.1": Path("base-v9.4.1.lock.json"),
    "9.4.2": Path("base-v9.4.2.lock.json"),
    "9.4.3": Path("base-v9.4.3.lock.json"),
    "9.4.4": Path("base-v9.4.4.lock.json"),
}

# Historical release locks bind payload and evidence. Compatibility releases are
# promoted by a later immutable finalization commit, which project adapters also
# pin. Keep that post-lock identity in the release index rather than rewriting a
# released lock file. v9.4.4 is intentionally absent until its pin-finalization
# PR has merged and that immutable merge commit can be recorded truthfully.
RELEASE_FINALIZATION_COMMITS = {
    "9.4.3": "0b7c94f38d959efc0fc9442274c60b2e268a3c97",
}


def _install_finalization_pin_validation(contract_module: ModuleType) -> None:
    """Extend the legacy release validator with immutable finalization identity."""

    if getattr(contract_module, "_base_finalization_validation_installed", False):
        return

    original: Callable[..., tuple[list[str], dict[str, Any] | None, bytes | None]] = (
        contract_module._release_lock_contract
    )

    def release_lock_contract(
        adapter: dict[str, Any], base_repository: Path
    ) -> tuple[list[str], dict[str, Any] | None, bytes | None]:
        errors, lock, pinned_registry = original(adapter, base_repository)
        base_release = adapter.get("base_release", {})
        if not isinstance(base_release, dict):
            return errors, lock, pinned_registry
        finalization_commit = base_release.get("finalization_commit")
        if finalization_commit is None:
            return errors, lock, pinned_registry

        version = base_release.get("version")
        if not isinstance(version, str):
            return errors, lock, pinned_registry
        expected = RELEASE_FINALIZATION_COMMITS.get(version)
        if expected is None:
            errors.append(
                f"Adapter finalization_commit is unsupported for Base v{version}: "
                "no canonical finalization identity is indexed"
            )
            return errors, lock, pinned_registry
        if finalization_commit != expected:
            errors.append(
                f"Adapter finalization_commit does not match Base v{version} release index: "
                f"expected {expected!r}, got {finalization_commit!r}"
            )
            return errors, lock, pinned_registry
        if not contract_module._commit_exists(base_repository, expected):
            errors.append(f"Base v{version} finalization commit is absent: {expected}")
            return errors, lock, pinned_registry

        evidence_commit = base_release.get("release_evidence_commit")
        if (
            isinstance(evidence_commit, str)
            and contract_module._commit_exists(base_repository, evidence_commit)
            and not contract_module._is_ancestor(base_repository, evidence_commit, expected)
        ):
            errors.append(
                f"Base v{version} release evidence is not an ancestor of finalization commit"
            )
        return errors, lock, pinned_registry

    contract_module._release_lock_contract = release_lock_contract
    contract_module._base_finalization_validation_installed = True


def _install_protected_baseline_ancestry(contract_module: ModuleType) -> None:
    """Authenticate canonical historical remote baselines without shortening the diff."""

    if getattr(contract_module, "_base_protected_baseline_ancestry_installed", False):
        return

    original: Callable[..., tuple[str | None, list[str]]] = (
        contract_module._trusted_protected_base
    )

    def trusted_protected_base(
        project_root: Path,
        baseline: dict[str, Any],
        protected_base_override: str = "",
    ) -> tuple[str | None, list[str]]:
        if (
            protected_base_override
            or baseline.get("authority_kind") != "REMOTE_TRACKING_REF"
            or baseline.get("policy_source_type") != "CANONICAL_ADAPTER_SOURCE"
        ):
            return original(project_root, baseline, protected_base_override)

        adapter_commit = baseline["commit"]
        authority_ref = baseline["authority_ref"]
        resolved = contract_module._resolve_commit(project_root, authority_ref)
        if resolved is None:
            return None, [
                f"Protected authority ref cannot be resolved to a commit: {authority_ref}"
            ]
        if not contract_module._commit_exists(project_root, adapter_commit):
            return None, [f"Protected baseline commit is absent: {adapter_commit}"]
        if not contract_module._is_ancestor(project_root, adapter_commit, resolved):
            return None, [
                "External protected authority requires adapter baseline ancestry: "
                f"{adapter_commit} is not an ancestor of {authority_ref} ({resolved})"
            ]
        return adapter_commit, []

    contract_module._trusted_protected_base = trusted_protected_base
    contract_module._base_protected_baseline_ancestry_installed = True


def install_release_lock_paths(contract_module: ModuleType) -> None:
    """Install canonical release identities into the legacy contract module.

    The project operating implementation predates the v9.4 release line. Keeping
    the evolving release index in this small module avoids rewriting that large,
    security-sensitive implementation while all official CLIs share one exact map.
    """

    contract_module.RELEASE_LOCK_PATHS.clear()
    contract_module.RELEASE_LOCK_PATHS.update(RELEASE_LOCK_PATHS)
    _install_finalization_pin_validation(contract_module)
    _install_protected_baseline_ancestry(contract_module)
