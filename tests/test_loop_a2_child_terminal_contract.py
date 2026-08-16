from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "loop_a2.py"


class LoopA2ChildTerminalContractTests(unittest.TestCase):
    def test_blocked_helper_owns_explicit_machine_terminal_contract(self) -> None:
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        blocked = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "_blocked"
        )
        constants = {
            node.value
            for node in ast.walk(blocked)
            if isinstance(node, ast.Constant) and isinstance(node.value, (str, int))
        }

        self.assertIn(1, constants)
        self.assertIn("schema_version", constants)
        self.assertIn("contract_role", constants)
        self.assertIn("LOOP_A2_CHILD_TERMINAL", constants)
        self.assertIn("status", constants)
        self.assertIn("code", constants)
        self.assertIn("message", constants)

    def test_contract_construction_failure_routes_through_blocked_helper(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn('code="A2_CONTRACT_INVALID"', source)
        self.assertNotIn(
            'print(json.dumps({"status": "CONTRACT_INVALID", "message": str(exc)}, sort_keys=True))',
            source,
        )


if __name__ == "__main__":
    unittest.main()
