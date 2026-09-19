from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path
from typing import Any

from tests.test_human_blueprint_progress_projection import valid_projection


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
MASTER_POLICY = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"
REVISION_CONTRACT = (
    ROOT
    / "docs/operations/project-workspace/HUMAN_BLUEPRINT_INCREMENTAL_REVISION_CONTRACT.md"
)
REVISION_TEMPLATE = (
    ROOT
    / "templates/project-operations/HUMAN_BLUEPRINT_INCREMENTAL_REVISION_TEMPLATE.md"
)
PUBLICATION_TOOL = ROOT / "tools/human_blueprint_incremental_publication.py"
SOURCE = "0123456789abcdef0123456789abcdef01234567"
PREDECESSOR_SOURCE = "abcdef0123456789abcdef0123456789abcdef01"


def _collect_list_values(value: Any, key: str) -> set[str]:
    collected: set[str] = set()
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key == key and isinstance(child_value, list):
                collected.update(
                    item for item in child_value if isinstance(item, str) and item
                )
            else:
                collected.update(_collect_list_values(child_value, key))
    elif isinstance(value, list):
        for child in value:
            collected.update(_collect_list_values(child, key))
    return collected


def _status_facts(projection: dict[str, Any]) -> dict[str, str]:
    facts: dict[str, str] = {}
    for record_type, id_key in (
        ("goals", "goal_id"),
        ("systems", "system_id"),
    ):
        for record in projection[record_type]:
            identity = record[id_key]
            facts[f"{identity}:maturity_status"] = record["maturity_status"]
            for check in record["checklist"]:
                facts[f"{identity}:checklist:{check['id']}"] = check["status"]

    for case in projection["cases"]:
        identity = case["case_id"]
        facts[f"{identity}:applicability"] = case["applicability"]
        facts[f"{identity}:maturity_status"] = case["maturity_status"]
        for verification in case["verification"]:
            key = f"{identity}:verification:{verification['level']}"
            facts[key] = verification["status"]

    for work in projection["project_work_kanban"]["work_items"]:
        identity = work["work_item_id"]
        facts[f"{identity}:status"] = work["status"]
        for check in work["checklist"]:
            facts[f"{identity}:checklist:{check['id']}"] = check["status"]
        for verification in work["verification"]:
            key = f"{identity}:verification:{verification['level']}"
            facts[key] = verification["status"]
    return facts


def _successor_inventory(projection: dict[str, Any]) -> dict[str, Any]:
    stable_ids = {
        record[id_key]
        for record_type, id_key in (
            ("goals", "goal_id"),
            ("systems", "system_id"),
            ("cases", "case_id"),
        )
        for record in projection[record_type]
    }
    stable_ids.update(
        work["work_item_id"]
        for work in projection["project_work_kanban"]["work_items"]
    )
    return {
        "stable_ids": sorted(stable_ids),
        "section_ids": [
            "SEC-PROJECT-STATUS",
            "SEC-GOALS",
            "SEC-SYSTEMS",
            "SEC-CASES",
            "SEC-TRACEABILITY",
        ],
        "diagram_ids": ["DGM-GOAL-MAP-01"],
        "approved_asset_ids": ["AST-APPROVED-01"],
        "consumer_refs": sorted(_collect_list_values(projection, "actual_consumers")),
        "evidence_refs": sorted(_collect_list_values(projection, "evidence")),
        "status_facts": _status_facts(projection),
    }


def _empty_inventory() -> dict[str, Any]:
    return {
        "stable_ids": [],
        "section_ids": [],
        "diagram_ids": [],
        "approved_asset_ids": [],
        "consumer_refs": [],
        "evidence_refs": [],
        "status_facts": {},
    }


def _incremental_revision(projection: dict[str, Any]) -> dict[str, Any]:
    successor = _successor_inventory(projection)
    predecessor = copy.deepcopy(successor)
    predecessor["section_ids"].remove("SEC-PROJECT-STATUS")
    return {
        "revision_mode": "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS",
        "publication_status": "READY",
        "predecessor_blueprint_ref": (
            "exports/example_MASTER_PRODUCTION_GDD_20260902.pdf"
        ),
        "predecessor_source_commit": PREDECESSOR_SOURCE,
        "predecessor_inventory": predecessor,
        "successor_inventory": successor,
        "semantic_delta_summary": [
            "Added the integrated goal, system, case, and work-status projection."
        ],
        "removal_or_downgrade_justifications": [],
    }


def projection_with_revision() -> dict[str, Any]:
    projection = valid_projection()
    projection["blueprint_revision"] = _incremental_revision(projection)
    return projection


class HumanBlueprintIncrementalRevisionContractTests(unittest.TestCase):
    def test_v4_routes_incremental_revision_contract_and_publication_gate(self) -> None:
        contract = json.loads(WORKSPACE_CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(
            contract["human_blueprint_incremental_revision_contract"],
            (
                "docs/operations/project-workspace/"
                "HUMAN_BLUEPRINT_INCREMENTAL_REVISION_CONTRACT.md"
            ),
        )
        self.assertEqual(
            contract["human_blueprint_incremental_revision_template"],
            (
                "templates/project-operations/"
                "HUMAN_BLUEPRINT_INCREMENTAL_REVISION_TEMPLATE.md"
            ),
        )
        self.assertEqual(
            contract["human_blueprint_incremental_publication_validator"],
            "tools/human_blueprint_incremental_publication.py",
        )
        self.assertEqual(
            contract["blueprint_revision_contract"]["mode"],
            "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS",
        )
        self.assertIn(
            "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS",
            contract["blueprint_revision_contract"]["forbidden_modes"],
        )
        for metadata in (
            "predecessor_blueprint_ref",
            "predecessor_source_commit",
            "revision_mode",
            "semantic_delta_summary",
        ):
            self.assertIn(metadata, contract["human_pdf_required_metadata"])

    def test_contract_preserves_existing_two_artifact_policy(self) -> None:
        policy = MASTER_POLICY.read_text(encoding="utf-8")
        self.assertIn("EXACTLY_TWO_DELIVERABLES", policy)
        self.assertIn("NO_SEPARATE_BLUEPRINT_ARTIFACT", policy)
        self.assertIn(
            "REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION",
            policy,
        )
        self.assertIn("NO_MASS_BLUEPRINT_BACKFILL", policy)

    def test_revision_contract_and_template_define_lossless_update(self) -> None:
        for path in (REVISION_CONTRACT, REVISION_TEMPLATE):
            text = path.read_text(encoding="utf-8")
            for token in (
                "EXISTING_BLUEPRINT_INCREMENTAL_REVISION_REQUIRED",
                "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS",
                "PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY",
                "STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION",
                "SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED",
                "UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN",
                "BLUEPRINT_LOSS_REGRESSION_GATE",
                "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED",
                "INITIAL_CREATION_NO_VALID_PREDECESSOR",
            ):
                self.assertIn(token, text)


class HumanBlueprintIncrementalRevisionValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PUBLICATION_TOOL.exists():
            raise AssertionError(f"publication validator must exist: {PUBLICATION_TOOL}")
        spec = importlib.util.spec_from_file_location(
            "human_blueprint_incremental_publication",
            PUBLICATION_TOOL,
        )
        if spec is None or spec.loader is None:
            raise AssertionError("publication validator could not be loaded")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_valid_incremental_revision_passes_and_renders_delta(self) -> None:
        projection = projection_with_revision()
        self.assertEqual(
            self.module.validate_publication_projection(
                projection,
                expected_source_sha=SOURCE,
            ),
            [],
        )
        rendered = self.module.render_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        for token in (
            "Blueprint 증분 수정·보존",
            "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS",
            PREDECESSOR_SOURCE,
            "BLUEPRINT_LOSS_REGRESSION_GATE: PASS",
            "Added the integrated goal, system, case, and work-status projection.",
            "프로젝트 작업 현황",
        ):
            self.assertIn(token, rendered)

    def test_revision_receipt_is_mandatory_for_current_publication(self) -> None:
        errors = self.module.validate_publication_projection(
            valid_projection(),
            expected_source_sha=SOURCE,
        )
        self.assertTrue(any("blueprint_revision" in error for error in errors))

    def test_successor_inventory_must_cover_current_projection(self) -> None:
        projection = projection_with_revision()
        projection["blueprint_revision"]["successor_inventory"][
            "stable_ids"
        ].remove("GOAL-01")
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        self.assertTrue(any("GOAL-01" in error for error in errors))

    def test_unexplained_stable_id_loss_fails_closed(self) -> None:
        projection = projection_with_revision()
        projection["blueprint_revision"]["predecessor_inventory"][
            "stable_ids"
        ].append("SYS-LEGACY")
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        self.assertTrue(
            any("stable_ids:SYS-LEGACY" in error for error in errors)
        )

    def test_explicit_replacement_allows_stable_id_transition(self) -> None:
        projection = projection_with_revision()
        revision = projection["blueprint_revision"]
        revision["predecessor_inventory"]["stable_ids"].append("SYS-LEGACY")
        revision["removal_or_downgrade_justifications"] = [
            {
                "change_key": "stable_ids:SYS-LEGACY",
                "change_type": "REPLACED",
                "reason": "The legacy system ID was consolidated into the active system.",
                "replacement_refs": ["SYS-01"],
                "affected_consumers": ["scenes/combat/combat.tscn"],
                "verification_impact": "Re-run the linked system and case checks.",
                "evidence": ["DEC-REPLACE-001"],
            }
        ]
        self.assertEqual(
            self.module.validate_publication_projection(
                projection,
                expected_source_sha=SOURCE,
            ),
            [],
        )

    def test_unexplained_evidence_status_downgrade_fails_closed(self) -> None:
        projection = projection_with_revision()
        runtime = projection["cases"][0]["verification"][1]
        runtime["status"] = "NOT_RUN"
        runtime["evidence"] = []
        revision = projection["blueprint_revision"]
        revision["successor_inventory"] = _successor_inventory(projection)
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        expected_key = "status_facts:CASE-01:verification:E3_RUNTIME"
        self.assertTrue(any(expected_key in error for error in errors))

    def test_initial_creation_requires_search_evidence_and_no_predecessor(self) -> None:
        projection = valid_projection()
        projection["blueprint_revision"] = {
            "revision_mode": "INITIAL_CREATION_NO_VALID_PREDECESSOR",
            "publication_status": "READY",
            "predecessor_blueprint_ref": None,
            "predecessor_source_commit": None,
            "predecessor_inventory": _empty_inventory(),
            "successor_inventory": _successor_inventory(projection),
            "predecessor_search_evidence": [
                "Repository, Library, and legacy Blueprint search found no valid predecessor."
            ],
            "semantic_delta_summary": [
                "Created the initial Blueprint after predecessor discovery."
            ],
            "removal_or_downgrade_justifications": [],
        }
        self.assertEqual(
            self.module.validate_publication_projection(
                projection,
                expected_source_sha=SOURCE,
            ),
            [],
        )

        projection["blueprint_revision"]["predecessor_search_evidence"] = []
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        self.assertTrue(any("predecessor_search_evidence" in error for error in errors))

        projection["blueprint_revision"]["predecessor_search_evidence"] = [
            "Search completed."
        ]
        projection["blueprint_revision"]["predecessor_blueprint_ref"] = (
            "exports/existing.pdf"
        )
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        self.assertTrue(
            any(
                "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS" in error
                for error in errors
            )
        )

    def test_unreadable_predecessor_blocks_publication(self) -> None:
        projection = projection_with_revision()
        revision = projection["blueprint_revision"]
        revision["revision_mode"] = "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED"
        revision["publication_status"] = "BLOCKED_UNVERIFIED"
        revision["predecessor_source_commit"] = None
        revision["predecessor_access_blockers"] = [
            "The predecessor PDF bytes or source revision could not be read."
        ]
        errors = self.module.validate_publication_projection(
            projection,
            expected_source_sha=SOURCE,
        )
        self.assertTrue(
            any(
                "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED" in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
