from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "tools/check_approved_project_operating_contract.py"


class ApprovedProtectedChangeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not GATE.is_file():
            raise AssertionError("approved protected-change gate is missing")
        spec = importlib.util.spec_from_file_location("approved_protected_change_gate", GATE)
        if spec is None or spec.loader is None:
            raise AssertionError("approved protected-change gate cannot be imported")
        cls.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.gate)

    def valid_document(self) -> dict:
        return {
            "schema_version": 1,
            "artifact_role": "PROJECT_PROTECTED_CHANGE_APPROVAL",
            "status": "APPROVED",
            "protected_base_commit": "a" * 40,
            "decision_ids": ["DEC-TEST-001"],
            "approved_paths": ["project.godot", "src/combat.gd"],
            "approval_source": "USER_CURRENT_SESSION_AUTO_APPROVAL",
            "approval_time": "2026-08-06T15:00:00+09:00",
            "scope_summary": "Approved gameplay runtime update.",
        }

    def test_exact_external_approval_allows_only_exact_protected_paths(self) -> None:
        errors = self.gate.validate_approval_document(
            self.valid_document(),
            protected_base="a" * 40,
            changed_paths=["src/combat.gd", "project.godot"],
            externally_approved=True,
        )
        self.assertEqual([], errors)

    def test_missing_external_approval_fails_closed(self) -> None:
        errors = self.gate.validate_approval_document(
            self.valid_document(),
            protected_base="a" * 40,
            changed_paths=["project.godot", "src/combat.gd"],
            externally_approved=False,
        )
        self.assertTrue(any("external" in error.lower() for error in errors), errors)

    def test_extra_or_missing_paths_fail_closed(self) -> None:
        extra = self.gate.validate_approval_document(
            self.valid_document(),
            protected_base="a" * 40,
            changed_paths=["project.godot", "src/combat.gd", "src/unapproved.gd"],
            externally_approved=True,
        )
        self.assertTrue(any("exact" in error.lower() for error in extra), extra)

        missing = self.valid_document()
        missing["approved_paths"] = ["project.godot"]
        errors = self.gate.validate_approval_document(
            missing,
            protected_base="a" * 40,
            changed_paths=["project.godot", "src/combat.gd"],
            externally_approved=True,
        )
        self.assertTrue(any("exact" in error.lower() for error in errors), errors)

    def test_baseline_and_decision_identity_are_required(self) -> None:
        wrong_base = self.valid_document()
        wrong_base["protected_base_commit"] = "b" * 40
        errors = self.gate.validate_approval_document(
            wrong_base,
            protected_base="a" * 40,
            changed_paths=["project.godot", "src/combat.gd"],
            externally_approved=True,
        )
        self.assertTrue(any("baseline" in error.lower() for error in errors), errors)

        no_decision = self.valid_document()
        no_decision["decision_ids"] = []
        errors = self.gate.validate_approval_document(
            no_decision,
            protected_base="a" * 40,
            changed_paths=["project.godot", "src/combat.gd"],
            externally_approved=True,
        )
        self.assertTrue(any("decision" in error.lower() for error in errors), errors)

    def test_only_the_exact_protected_path_error_can_be_reconciled(self) -> None:
        contract_errors = [
            "Protected-path changes detected: project.godot, src/combat.gd",
            "Project Skill Registry hash mismatch",
        ]
        remaining = self.gate.reconcile_contract_errors(
            contract_errors,
            approved_paths=["project.godot", "src/combat.gd"],
        )
        self.assertEqual(["Project Skill Registry hash mismatch"], remaining)

        untouched = self.gate.reconcile_contract_errors(
            ["Protected-path changes detected: project.godot, src/other.gd"],
            approved_paths=["project.godot", "src/combat.gd"],
        )
        self.assertEqual(
            ["Protected-path changes detected: project.godot, src/other.gd"],
            untouched,
        )

    def test_generated_artifact_check_is_replayed_after_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "Project"
            base = Path(temporary) / "Base"
            project.mkdir()
            base.mkdir()
            stale = project / "generated.txt"
            stale.write_text("stale\n", encoding="utf-8")
            protected_error = "Protected-path changes detected: project.godot, src/combat.gd"
            with (
                mock.patch.object(self.gate.contract, "validation_errors", return_value=[protected_error]),
                mock.patch.object(
                    self.gate.contract,
                    "build_artifacts",
                    return_value={stale: b"expected\n"},
                ) as build,
            ):
                errors = self.gate.validate_project_contract(
                    project_root=project,
                    base_repository=base,
                    protected_base="a" * 40,
                    approval_document=self.valid_document(),
                    externally_approved=True,
                    check_generated=True,
                )
            self.assertTrue(any("generated" in error.lower() for error in errors), errors)
            build.assert_called_once_with(project, base, prevalidated=True)


if __name__ == "__main__":
    unittest.main()
