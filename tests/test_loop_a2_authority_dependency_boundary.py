from __future__ import annotations

import builtins
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from tools.loop_a2_runtime.authority_snapshot import (
    AuthoritySnapshotError,
    validate_bundle,
)


class LoopA2AuthorityDependencyBoundaryTests(unittest.TestCase):
    def test_missing_schema_validator_dependency_is_wrapped_as_authority_snapshot_error(self) -> None:
        real_import = builtins.__import__
        removed: dict[str, object] = {}
        for name in (
            "tools.loop_contracts.bundle_validation",
            "tools.loop_contracts.schema_validation",
            "jsonschema",
        ):
            if name in sys.modules:
                removed[name] = sys.modules.pop(name)

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "jsonschema":
                raise ModuleNotFoundError("simulated missing schema validator")
            return real_import(name, globals, locals, fromlist, level)

        try:
            with patch("builtins.__import__", side_effect=guarded_import):
                try:
                    validate_bundle(Path("unused-capsule.json"))
                except Exception as exc:  # assert the boundary converts the import failure
                    self.assertIsInstance(exc, AuthoritySnapshotError)
                else:
                    self.fail("missing schema validator dependency must fail closed")
        finally:
            for name in (
                "tools.loop_contracts.bundle_validation",
                "tools.loop_contracts.schema_validation",
                "jsonschema",
            ):
                sys.modules.pop(name, None)
            sys.modules.update(removed)


if __name__ == "__main__":
    unittest.main()
