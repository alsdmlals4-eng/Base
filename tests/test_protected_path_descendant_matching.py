from __future__ import annotations

import unittest

from tools import check_approved_project_operating_contract as approval
from tools import project_operating_contract as contract


class ProtectedDirectoryDescendantMatchingTests(unittest.TestCase):
    def test_directory_pattern_matches_directory_and_descendants(self) -> None:
        for path in ("data", "data/", "data/item.json", "data/vertical_slice/item.json"):
            with self.subTest(path=path):
                self.assertTrue(contract._protected_match(path, ["data/"]))

    def test_directory_pattern_rejects_similarly_prefixed_siblings(self) -> None:
        for path in ("database/item.json", "data_backup/item.json", "data-old/item.json"):
            with self.subTest(path=path):
                self.assertFalse(contract._protected_match(path, ["data/"]))

    def test_normalization_preserves_boundary_safe_matching(self) -> None:
        cases = (
            ("data\\vertical_slice\\item.json", "data/"),
            ("DATA/vertical_slice/item.json", "data/"),
            ("da\u0301ta/item.json", "dáta/"),
            ("scripts/main.gd", "scripts/"),
            ("scenes/main/main.tscn", "scenes/"),
            ("assets/ui/icon.png", "assets/"),
            ("addons/plugin/plugin.gd", "addons/"),
        )
        for path, pattern in cases:
            with self.subTest(path=path, pattern=pattern):
                self.assertTrue(contract._protected_match(path, [pattern]))

    def test_explicit_file_and_wildcard_semantics_remain_compatible(self) -> None:
        self.assertTrue(contract._protected_match("project.godot", ["project.godot"]))
        self.assertFalse(contract._protected_match("project.godot.import", ["project.godot"]))
        self.assertTrue(contract._protected_match("scenes/main/main.tscn", ["scenes/**/*.tscn"]))
        self.assertFalse(contract._protected_match("scripts/main.gd", ["*.tscn"]))

    def test_multiple_nested_approved_paths_reconcile_exactly_once(self) -> None:
        changed = [
            "data/vertical_slice/content_result_contract.json",
            "scripts/vertical_slice/domain/vs_content_result_record.gd",
        ]
        errors = ["Protected-path changes detected: " + ",".join(changed), "unrelated failure"]
        self.assertEqual(
            approval.reconcile_contract_errors(errors, approved_paths=list(reversed(changed))),
            ["unrelated failure"],
        )

    def test_nested_approval_cannot_hide_an_unapproved_path(self) -> None:
        approved = [
            "data/vertical_slice/content_result_contract.json",
            "scripts/vertical_slice/domain/vs_content_result_record.gd",
        ]
        errors = ["Protected-path changes detected: " + ",".join([*approved, "scripts/vertical_slice/domain/unapproved.gd"])]
        self.assertEqual(approval.reconcile_contract_errors(errors, approved_paths=approved), errors)


if __name__ == "__main__":
    unittest.main()
