from __future__ import annotations

import os

import pytest


_POSIX_ONLY_TESTS = frozenset(
    {
        "test_engine_frame_handle_prevents_leaf_symlink_swap_escape",
        "test_export_handoff_uses_logical_paths_across_independent_directory_handles",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Skip only tests whose mechanism requires POSIX directory descriptors or /proc aliases."""
    if os.name != "nt":
        return
    marker = pytest.mark.skip(
        reason="POSIX-only probe requires os.O_DIRECTORY and/or directory-handle symlink aliases"
    )
    for item in items:
        if item.name in _POSIX_ONLY_TESTS:
            item.add_marker(marker)
