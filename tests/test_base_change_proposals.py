from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_base_change_proposals",
    ROOT / "tools/check_base_change_proposals.py",
)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class BaseChangeProposalTests(unittest.TestCase):
    def test_current_proposals_validate(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(registry["proposal_root"], "[수정제안서]")

    def test_reallocated_bcp_lineage_keeps_distinct_sources_and_recovery_audit(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entries = {item["proposal_id"]: item for item in registry["proposals"]}
        retained_entry = entries["BCP-2026-023-local-executor-retained-instance-recovery"]
        sandbox_entry = entries["BCP-2026-024-execution-sandbox-authority-split-recovery"]
        retained = (ROOT / retained_entry["path"]).read_text(encoding="utf-8")
        sandbox = (ROOT / sandbox_entry["path"]).read_text(encoding="utf-8")

        self.assertEqual("alsdmlals4-eng/Ten-Paces-Hidden-Moves", retained_entry["source_project"])
        self.assertEqual("alsdmlals4-eng/GRIMOIRE-", sandbox_entry["source_project"])
        self.assertIn("출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`", retained)
        self.assertIn("source_project: alsdmlals4-eng/GRIMOIRE-", sandbox)
        self.assertNotIn("alsdmlals4-eng/Ten-Paces-Hidden-Moves", sandbox)
        for project_only_marker in (
            "alsdmlals4-eng/GRIMOIRE-",
            "GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01",
            "HTTP 525",
            "Star Runtime",
        ):
            self.assertNotIn(project_only_marker, retained)

        self.assertIn("### 충돌 복원 감사", sandbox)
        recovery_audit = sandbox.split("### 충돌 복원 감사", 1)[1].split("## 관찰과 증거", 1)[0]
        chronology = (
            "- PR #293의 초기 BCP-022에는 `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`과 "
            "일시적 external HTTP 525 뒤 동일 exact-head Star Runtime POC 재성공 기록이 모두 있었다.",
            "- PR #295의 BCP-023과 PR #296의 BCP-024에는 Decision ID가 남았지만 "
            "HTTP 525/Star Runtime 기록은 이미 빠져 있었다.",
            "- PR #297의 최종 BCP-024에서는 Decision ID도 빠졌다.",
        )
        for chronology_statement in chronology:
            self.assertIn(chronology_statement, recovery_audit)
        self.assertLess(recovery_audit.index(chronology[0]), recovery_audit.index(chronology[1]))
        self.assertLess(recovery_audit.index(chronology[1]), recovery_audit.index(chronology[2]))
        self.assertEqual("SUBMITTED", sandbox_entry["status"])
        self.assertIsNone(sandbox_entry["approval_ref"])
        self.assertIn("base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE", sandbox)

    def test_grimoire_recovery_evidence_is_not_active_base_policy(self) -> None:
        skill_registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        active_policy_paths = {
            ROOT / "AGENTS.md",
            ROOT / "START_HERE.md",
        }
        allowed_historical_records = {
            ROOT / "docs/audits/2026-08-11-base-structure-and-bcp-conflict-recovery.md",
            ROOT / "docs/superpowers/plans/2026-08-11-base-structure-and-bcp-conflict-recovery.md",
            ROOT / "docs/superpowers/specs/2026-08-11-base-structure-and-bcp-conflict-recovery-design.md",
            ROOT / "docs/superpowers/plans/2026-08-11-one-shot-local-executor-bootstrap.md",
            ROOT / "docs/superpowers/specs/2026-08-11-one-shot-local-executor-bootstrap-design.md",
        }
        non_policy_roots = (ROOT / "docs/archive", ROOT / "docs/evidence")
        for path in (ROOT / "docs").rglob("*.md"):
            if path in allowed_historical_records:
                continue
            if any(path.is_relative_to(non_policy_root) for non_policy_root in non_policy_roots):
                continue
            active_policy_paths.add(path)
        for entry in skill_registry["skills"]:
            if entry["status"] != "ACTIVE":
                continue
            skill_root = (ROOT / entry["path"]).parent
            active_policy_paths.update(skill_root.rglob("*.md"))

        for path in sorted(active_policy_paths):
            policy_text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01", policy_text)
                self.assertNotIn("HTTP 525", policy_text)
                self.assertNotIn("Star Runtime", policy_text)

    def test_merged_continuity_and_diagnostic_proposals_retain_approval_and_implementation_links(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual(errors, [])
        proposal_ids = {
            "BCP-2026-002-actions-node24-compatibility",
            "BCP-2026-013-post-merge-continuation-state-reconciliation",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility",
        }
        approved = {
            item["proposal_id"]: item
            for item in registry["proposals"]
            if item["proposal_id"] in proposal_ids
        }
        self.assertEqual(proposal_ids, set(approved))
        implementation_prs = {
            "BCP-2026-002-actions-node24-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/262",
            "BCP-2026-013-post-merge-continuation-state-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation": "https://github.com/alsdmlals4-eng/Base/pull/261",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/260",
        }
        for proposal_id, item in approved.items():
            self.assertEqual("IMPLEMENTED", item["status"])
            self.assertEqual(
                "docs/superpowers/specs/2026-08-10-approved-base-continuity-diagnostics-actions-design.md",
                item["approval_ref"],
            )
            self.assertEqual(implementation_prs[proposal_id], item["implementation_pr"])

    def test_merged_proposals_have_implemented_lifecycle_states(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entries = {item["proposal_id"]: item for item in registry["proposals"]}
        implemented = {
            "BCP-2026-001-base-skill-map-publication": "https://github.com/alsdmlals4-eng/Base/pull/264",
            "BCP-2026-002-actions-node24-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/262",
            "BCP-2026-013-post-merge-continuation-state-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation": "https://github.com/alsdmlals4-eng/Base/pull/261",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-015-external-runtime-session-same-snapshot-recovery": "https://github.com/alsdmlals4-eng/Base/pull/266",
            "BCP-2026-012-serial-fiction-canon-migration-debt": "https://github.com/alsdmlals4-eng/Base/pull/265",
            "BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard": "https://github.com/alsdmlals4-eng/Base/pull/265",
        }
        for proposal_id, implementation_pr in implemented.items():
            self.assertEqual("IMPLEMENTED", entries[proposal_id]["status"])
            self.assertEqual(implementation_pr, entries[proposal_id]["implementation_pr"])

    def test_implemented_serial_fiction_proposals_retain_closeout_records(self) -> None:
        """Catch a registry closeout that leaves either proposal body stale."""
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entries = {item["proposal_id"]: item for item in registry["proposals"]}
        expected = {
            "BCP-2026-012-serial-fiction-canon-migration-debt": (
                "https://github.com/alsdmlals4-eng/Base/pull/265",
                "0d1cebdec0e1f3b660688ec194dcc27054dcfc2d",
            ),
            "BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard": (
                "https://github.com/alsdmlals4-eng/Base/pull/265",
                "0d1cebdec0e1f3b660688ec194dcc27054dcfc2d",
            ),
        }
        for proposal_id, (implementation_pr, merge_commit) in expected.items():
            with self.subTest(proposal_id=proposal_id):
                self.assertEqual("IMPLEMENTED", entries[proposal_id]["status"])
                self.assertEqual(implementation_pr, entries[proposal_id]["implementation_pr"])
                proposal = (ROOT / entries[proposal_id]["path"]).read_text(encoding="utf-8")
                self.assertIn("- 상태: `IMPLEMENTED`", proposal)
                self.assertIn("### 구현 closeout — PR #265", proposal)
                self.assertIn(implementation_pr, proposal)
                self.assertIn(merge_commit, proposal)

    def test_full_bcp_lifecycle_audit_retains_reconciled_closeout_records(self) -> None:
        """Keep Registry and canonical proposal bodies aligned after full lifecycle audits."""
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entries = {item["proposal_id"]: item for item in registry["proposals"]}
        expected = {
            "BCP-2026-001-base-skill-map-publication": (
                "https://github.com/alsdmlals4-eng/Base/pull/264",
                "381b66bc3619caf7994b0073108fdcba23b30e96",
            ),
            "BCP-2026-008-agentic-spec-design-ui-procurement-integration": (
                "https://github.com/alsdmlals4-eng/Base/pull/192",
                "b96d9dfe09ef33a18e9b31113eb480ad7a919b1f",
            ),
            "BCP-2026-011-game-feature-design-spec-system": (
                "https://github.com/alsdmlals4-eng/Base/pull/231",
                "b37c9def027ecf474be9e5210ba4b5a583591f2a",
            ),
        }
        for proposal_id, (implementation_pr, merge_commit) in expected.items():
            with self.subTest(proposal_id=proposal_id):
                entry = entries[proposal_id]
                self.assertEqual("IMPLEMENTED", entry["status"])
                self.assertEqual(implementation_pr, entry["implementation_pr"])
                proposal = (ROOT / entry["path"]).read_text(encoding="utf-8")
                self.assertIn("- 상태: `IMPLEMENTED`", proposal)
                self.assertIn(implementation_pr, proposal)
                self.assertIn(merge_commit, proposal)

        historical = entries["BCP-2026-008-agentic-spec-design-ui-procurement-integration"]
        self.assertTrue(historical["historical_reconciliation"])
        proposal = (ROOT / historical["path"]).read_text(encoding="utf-8")
        self.assertIn("PR #190은 Draft로 종료되어 병합되지 않았다", proposal)

    def test_explicit_historical_reconciliation_can_backfill_an_implemented_registry_entry(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                dict(CHECKER.HISTORICAL_RECONCILIATION_ENTRY)
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            [
                "[수정제안서]/BCP-2026-008-agentic-spec-design-ui-procurement-integration/PROPOSAL.md",
                "schemas/base-change-proposal-registry-v1.schema.json",
                "tools/check_base_change_proposals.py",
                "tests/test_base_change_proposals.py",
            ],
        )
        self.assertEqual([], errors)

    def test_historical_reconciliation_cannot_be_used_for_an_arbitrary_new_proposal(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                {
                    "proposal_id": "BCP-2026-999-forged-history",
                    "status": "IMPLEMENTED",
                    "historical_reconciliation": True,
                }
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            [
                "[수정제안서]/BCP-2026-999-forged-history/PROPOSAL.md",
                "schemas/base-change-proposal-registry-v1.schema.json",
                "tools/check_base_change_proposals.py",
                "tests/test_base_change_proposals.py",
            ],
        )
        self.assertTrue(any("new proposal must start as SUBMITTED" in error for error in errors))
        self.assertTrue(any("active Base paths" in error for error in errors))

    def test_historical_reconciliation_requires_fixed_bcp008_provenance(self) -> None:
        tampered = dict(CHECKER.HISTORICAL_RECONCILIATION_ENTRY)
        tampered["implementation_pr"] = "https://github.com/alsdmlals4-eng/Base/pull/999"
        self.assertFalse(CHECKER.is_allowed_historical_reconciliation(tampered))

    def test_new_proposal_pr_cannot_change_active_base(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                {
                    "proposal_id": "BCP-2026-999-example",
                    "status": "SUBMITTED",
                }
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md", "AGENTS.md"],
        )
        self.assertTrue(any("active Base paths" in error for error in errors))

    def test_new_proposal_starts_submitted(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                {
                    "proposal_id": "BCP-2026-999-example",
                    "status": "APPROVED_FOR_IMPLEMENTATION",
                }
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md"],
        )
        self.assertTrue(any("must start as SUBMITTED" in error for error in errors))

    def test_bootstrap_pr_is_explicitly_allowed(self) -> None:
        current = {"proposals": [{"proposal_id": "BCP-2026-001-bootstrap", "status": "SUBMITTED"}]}
        self.assertEqual(CHECKER.enforce_proposal_only_diff(current, None, ["AGENTS.md"]), [])

    def test_git_paths_preserve_non_ascii_proposal_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            proposal = root / "[수정제안서]" / "BCP-2026-999-example" / "PROPOSAL.md"
            proposal.parent.mkdir(parents=True)
            proposal.write_text("proposal\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            paths = CHECKER.git_paths(root, "diff", "--cached", "--name-only", "-z")
            self.assertEqual(paths, ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md"])


class ClaimIntentProposalLifecycleTests(unittest.TestCase):
    def test_bcp_027_closeout_binds_green_evidence_and_implementation_pr(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entry = next(
            item
            for item in registry["proposals"]
            if item["proposal_id"] == "BCP-2026-027-claim-and-intent-verification-gate"
        )
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertEqual("https://github.com/alsdmlals4-eng/Base/pull/319", entry["implementation_pr"])
        proposal = (ROOT / entry["path"]).read_text(encoding="utf-8")
        evidence = (ROOT / "docs/evidence/2026-08-13-claim-and-intent-verification-gate.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md").read_text(encoding="utf-8")
        design = (ROOT / "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md").read_text(encoding="utf-8")
        self.assertNotIn("구현 PR: 아직 없음", proposal)
        self.assertNotIn("신규 제안 Registry 상태: `SUBMITTED`", proposal)
        self.assertIn("최종 Registry 상태: `IMPLEMENTED`", proposal)
        self.assertIn("bf0890439cbef96777171cc00a0229c65e852af8", plan + "\n" + design)
        for stale in ('9a4a6e688e993114466e3f25831555b23fcf5912', '8a161eca8d129584aecb3898e8d5622dcfc89efb', '31656590653', '94312314139'):
            self.assertNotIn(stale, plan + "\n" + design)
        for token in (
            "### 구현 closeout — PR #319",
            "eef62df811ae64ff92fa6692a3e91edb8a5e343b",
            "External model behavior run: `NOT_RUN`",
            "post-merge `main` readback",
        ):
            self.assertIn(token, proposal + "\n" + evidence)


    def test_bcp032_implemented_registry_entry_has_proposal_closeout_record(self) -> None:
        """Prevent an IMPLEMENTED registry row from leaving its canonical proposal at approval-only."""
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entry = next(
            item
            for item in registry["proposals"]
            if item["proposal_id"] == "BCP-2026-032-ai-visual-continuity-and-notion-preview-fallback"
        )
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertEqual("https://github.com/alsdmlals4-eng/Base/pull/703", entry["implementation_pr"])
        proposal = (ROOT / entry["path"]).read_text(encoding="utf-8")
        self.assertIn("- 상태: \`IMPLEMENTED\`", proposal)
        self.assertIn("### 구현 closeout — PR #703", proposal)
        self.assertIn("5b241fce6623d4b0a152bff59ad6a257a18704ed", proposal)


if __name__ == "__main__":
    unittest.main()
