from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
START = ROOT / "START_HERE.md"


class EntrypointOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.agents = AGENTS.read_text(encoding="utf-8")
        cls.start = START.read_text(encoding="utf-8")

    def test_entrypoints_declare_distinct_responsibilities(self) -> None:
        self.assertIn("항상 적용되는 불변 규칙", self.agents)
        self.assertIn("요청별 한 단계 라우터", self.start)
        self.assertIn("## 요청별 라우팅", self.start)
        self.assertNotIn("## 요청별 라우팅", self.agents)
        self.assertIn("완료 보고", self.agents)
        self.assertNotIn("완료 보고", self.start)

    def test_both_entrypoints_delegate_to_canonical_operating_sources(self) -> None:
        for path in ("docs/OPERATING_MODEL.md", "docs/WORK_MODE_AND_SKILL_ROUTING.md", "docs/DOCUMENTATION_MAP.md"):
            with self.subTest(path=path):
                self.assertIn(path, self.agents)
                self.assertIn(path, self.start)

        for path in ("skills/SKILL_REGISTRY.json", "docs/generated/BASE_ACTIVE_SKILLS.md"):
            with self.subTest(path=path):
                self.assertIn(path, self.agents)
                self.assertIn(path, self.start)

    def test_start_here_keeps_one_step_routes_for_high_risk_work(self) -> None:
        for route in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "running-adversarial-review-and-refinement",
            "reviewing-and-validating-project-changes",
            "auditing-canonical-reference-freshness",
            "managing-base-change-proposals",
            "auditing-and-refining-ui-art",
            "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
        ):
            with self.subTest(route=route):
                self.assertIn(route, self.start)

    def test_agents_keeps_always_on_safety_and_authority_boundaries(self) -> None:
        for term in (
            "사용자의 최신 지시",
            "사용자 승인",
            "설치",
            "권한",
            "실행하지 않은",
            "[수정제안서]",
            "별도 구현 PR",
            "released lock",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "PROPOSED_SHEET_CHANGE",
            "정확한 HEAD",
            "소유 경계 없이 병렬",
            "직접 승인한 Base 변경 요청",
            "별도 제안서 없이 작업 계약",
        ):
            with self.subTest(term=term):
                self.assertIn(term, self.agents)

    def test_detailed_contracts_are_not_duplicated_in_entrypoints(self) -> None:
        for term in (
            "lifecycle_status",
            "approval_status",
            "implementation_status",
            "verification_status",
            "publication_status",
            "source_only",
            "milestone_sync",
            "always_sync",
            "review-scope-map",
            "route-findings",
            "refine-approved-findings",
        ):
            with self.subTest(term=term):
                self.assertNotIn(term, self.agents)
                self.assertNotIn(term, self.start)

    def test_every_game_system_first_hop_enters_the_owning_skill(self) -> None:
        routes = [
            line for line in self.start.splitlines()
            if "Game-system routes:" in line
            or line.startswith("| 게임 시스템·난이도·전투 AI |")
        ]
        self.assertEqual(2, len(routes))
        for route in routes:
            with self.subTest(route=route):
                self.assertIn("analyzing-and-refining-game-concepts", route)
                self.assertIn("skills/analyzing-and-refining-game-concepts/SKILL.md", route)
                self.assertNotIn("templates/planning/", route)

        self.assertIn(
            "templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md",
            self.start,
        )

    def test_high_risk_routes_are_derived_from_registry_trigger_metadata(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        high_risk_triggers = {
            "approved-base-change",
            "archive-governance",
            "commercial-plugin",
            "delete-candidate",
            "third-party-license",
            "model-recommendation",
            "prompt-caching",
            "verified-pr-merge",
            "repository-wide-audit",
            "accessibility-review",
            "performance-profile",
        }
        expected_routes = {
            item["skill_id"]
            for item in registry["skills"]
            if high_risk_triggers.intersection(item["trigger_tags"])
        }
        self.assertTrue(expected_routes)
        for skill_id in sorted(expected_routes):
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, self.start)

    def test_every_skill_package_path_declared_in_start_matches_the_registry(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        registered_paths = {item["path"] for item in registry["skills"]}
        declared_paths = set(
            re.findall(r"(?<!\.agents/)skills/[a-z0-9-]+/SKILL\.md", self.start)
        )
        self.assertTrue(declared_paths)
        self.assertEqual(set(), declared_paths - registered_paths)

    def test_active_local_validation_examples_require_an_exact_commit(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name, text in (("AGENTS.md", self.agents), ("README.md", readme)):
            with self.subTest(name=name):
                self.assertNotIn("--trusted-history-commit origin/main", text)
                self.assertRegex(
                    text,
                    re.compile(r"--trusted-history-commit (?:<[a-z0-9-]*sha>|[0-9a-f]{40})"),
                )


if __name__ == "__main__":
    unittest.main()
