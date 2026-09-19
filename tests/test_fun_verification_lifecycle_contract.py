"""Guard fun-verification documentation routes, not player enjoyment or AI execution.

These tests detect missing contract clauses and broken owner links. A green result
is documentation-contract evidence only; human play and project adoption remain
independent, explicitly evidenced activities.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OWNER = Path("skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md")
PROJECT = Path("templates/AGENTS.project.md")
PACKET = Path("templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md")


class FunVerificationLifecycleContractTests(unittest.TestCase):
    def text(self, path: Path) -> str:
        self.assertTrue((ROOT / path).is_file(), f"missing contract: {path}")
        return (ROOT / path).read_text(encoding="utf-8")

    def section(self, path: Path, title: str) -> str:
        text = self.text(path)
        heading = f"## {title}\n"
        self.assertTrue(heading in text, f"missing section in {path}: {title}")
        return text.split(heading, 1)[1].split("\n## ", 1)[0]

    def require(self, text: str, *clauses: str) -> None:
        for clause in clauses:
            with self.subTest(clause=clause):
                self.assertIn(clause, text)

    def test_existing_technical_and_production_evidence_boundaries_survive(self):
        self.require(self.text(OWNER), "TECHNICAL_SPIKE_INTERNAL_ONLY",
                     "SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE",
                     "SLICE_BUILD_READY", "RELEASE_NEAR_VERTICAL_SLICE_FIRST",
                     "PRODUCTION_READY", "REPEAT_VERTICAL_SLICE")

    def test_common_contract_scopes_work_without_a_new_approval_or_director(self):
        text = self.section(OWNER, "Fun verification lifecycle")
        self.require(text, "FUN_VERIFICATION_LIFECYCLE", "L1", "L0",
                     "REUSED_EVIDENCE", "NOT_APPLICABLE", "USER_DECISION_REQUIRED",
                     "runtime Director", "새 독립 Skill")

    def test_common_contract_connects_all_feature_phases_to_existing_owners(self):
        text = self.section(OWNER, "Fun verification lifecycle")
        self.require(text, "PLAN", "DESIGN", "IMPLEMENT", "VERIFY", "LEARN",
                     "GAME_FEATURE_DESIGN_SPEC.md", "FEATURE_SPEC_TRACEABILITY_PACKET.md",
                     "runtime_consumer", "counterevidence", "KEEP / CHANGE / DEFER / RETEST")

    def test_common_contract_keeps_human_evidence_and_genre_specificity(self):
        text = self.section(OWNER, "Fun verification lifecycle")
        self.require(text, "NO_UNIVERSAL_FUN_SCORE", "관찰", "자기보고", "로그",
                     "첫 플레이", "반복 플레이", "서사", "표현", "NOT_RUN",
                     "빌드", "표본", "DOC", "MACHINE", "RUNTIME", "HUMAN", "RELEASE")

    def test_project_template_uses_current_canon_and_explicit_adoption(self):
        text = self.section(PROJECT, "Project-specific fun verification")
        self.require(text, "PROJECT_FUN_PROFILE_BINDING", "source_id + path + section",
                     "핵심 경험", "보조 경험", "금지 방향", "승인",
                     "docs/BASE_RULES_VERSION.md", "PENDING_PROJECT_ADOPTION",
                     "기능 기획", "설계", "구현", "L0", "L1", "L2")

    def test_project_and_packet_routes_resolve_to_the_same_owner(self):
        for path, title in ((PROJECT, "Project-specific fun verification"),
                            (PACKET, "8. Player-experience verification linkage")):
            with self.subTest(path=str(path)):
                text = self.section(path, title)
                targets = re.findall(r"\]\(([^)]+#fun-verification-lifecycle)\)", text)
                self.assertEqual(len(targets), 1, "one explicit shared-owner link required")
                target, anchor = targets[0].split("#", 1)
                self.assertEqual((ROOT / path.parent / target).resolve(), (ROOT / OWNER).resolve())
                self.assertIn(f'id="{anchor}"', self.text(OWNER))

    def test_packet_preserves_scope_and_separates_machine_from_human_verification(self):
        text = self.section(PACKET, "8. Player-experience verification linkage")
        self.require(text, "L2 이상", "L0·L1", "requirement_id", "implementation_paths",
                     "verification_id", "MACHINE", "RUNTIME", "HUMAN", "NOT_RUN",
                     "CONVERGED", "GAP", "BLOCKED_UNVERIFIED", "FUN_PASS")

    def test_existing_packet_authority_and_evidence_rows_survive(self):
        self.require(self.text(PACKET), "별도 책임 원본이 아니다", "## 3. Traceability matrix",
                     "## 4. Verification evidence", "## 5. Coverage gaps",
                     "coverage_status: GAP | BLOCKED_UNVERIFIED | CONVERGED",
                     "NOT_RUN / PASSED / FAILED / BLOCKED_UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
