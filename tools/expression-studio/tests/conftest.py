from __future__ import annotations

import os

import pytest


_WINDOWS_POSIX_ONLY_TESTS = {
    "test_engine_candidate_handle_prevents_leaf_symlink_swap_escape",
}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Keep POSIX fd/proc attacks on POSIX; Windows uses portable staging contracts."""
    if os.name != "nt":
        return
    marker = pytest.mark.skip(
        reason="POSIX directory-handle /proc semantics; Windows uses PortableStableStagingTree contracts"
    )
    for item in items:
        if item.name in _WINDOWS_POSIX_ONLY_TESTS:
            item.add_marker(marker)
