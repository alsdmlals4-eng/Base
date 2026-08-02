#!/usr/bin/env python3
"""Canonical compatible Base release-lock index for project operating CLIs."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType


RELEASE_LOCK_PATHS = {
    "9.1.0": Path("base-v9.1.lock.json"),
    "9.2.0": Path("base-v9.2.lock.json"),
    "9.3.0": Path("base-v9.3.lock.json"),
    "9.4.0": Path("base-v9.4.lock.json"),
    "9.4.1": Path("base-v9.4.1.lock.json"),
}


def install_release_lock_paths(contract_module: ModuleType) -> None:
    """Install the canonical release map into the legacy contract module.

    The project operating implementation predates the v9.4 release line. Keeping
    the evolving release index in this small module avoids rewriting that large,
    security-sensitive implementation while all official CLIs share one exact map.
    """

    contract_module.RELEASE_LOCK_PATHS.clear()
    contract_module.RELEASE_LOCK_PATHS.update(RELEASE_LOCK_PATHS)
