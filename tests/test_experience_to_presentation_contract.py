"""Documentation-route regressions only; not runtime or agent-behavior tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path("docs/knowledge/game-development/EXPERIENCE_TO_PRESENTATION_GUIDE.md")
SKILL = Path("skills/auditing-and-refining-ui-art/SKILL.md")
CONCEPT = Path("skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md")
ADAPTER = Path("skills/auditing-and-refining-ui-art/references/project-adapter-contract.md")


class ExperienceToPresentationContractTests(unittest.TestCase):
    def text(self, path=REFERENCE):
        self.assertTrue((ROOT / path).is_file(), f"missing documentation: {path}")
        return (ROOT / path).read_text(encoding="utf-8")

    def clauses(self, *clauses):
        text = self.text()
        for clause in clauses:
            with self.subTest(clause=clause):
                self.assertIn(clause, text)

    def test_existing_owners_route_to_one_conditional_reference(self):
        # Keep the established Skill entrypoint; follow its existing adapter link.
        # This avoids an unnecessary public Skill-contract/registry change.
        for owner, target in ((SKILL, ADAPTER), (CONCEPT, REFERENCE),
                              (ADAPTER, REFERENCE)):
            with self.subTest(owner=str(owner), target=str(target)):
                links = re.findall(r"\]\(([^)]+)\)", self.text(owner))
                resolved = [
                    (ROOT / owner.parent / link.split("#", 1)[0]).resolve()
                    for link in links if "://" not in link
                ]
                self.assertEqual(resolved.count((ROOT / target).resolve()), 1,
                                 "one real link per existing-owner route required")
                self.assertTrue((ROOT / target).is_file())

    def test_gameplay_and_presentation_effects_have_different_owners(self):
        self.clauses("GAMEPLAY_EFFECT", "PRESENTATION_EFFECT", "state_owner",
                     "중첩", "지속", "동일 거래", "확정 결과", "장식")

    def test_specification_maps_intent_to_real_consumers_and_existing_sources(self):
        self.clauses("requirement_id", "source_id + path + section", "runtime_consumer",
                     "GAME_UX_UI_SYSTEM", "GAME_FEATURE_DESIGN_SPEC", "FEATURE_SPEC_TRACEABILITY_PACKET",
                     "PLANNED", "Theme", "Control", "Container", "Signal", "AnimationPlayer", "Tween")

    def test_ui_states_preserve_input_recovery_and_orthogonal_state_meanings(self):
        self.clauses("focused + selected", "disabled", "locked", "loading", "error",
                     "취소", "복귀", "터치", "긴 한국어", "정답", "정보 공개")

    def test_feedback_assets_and_limits_are_project_specific(self):
        self.clauses("반복 빈도", "동시", "장식", "reduced motion", "mute", "haptic-off",
                     "HYPOTHESIS", "아트 방향", "SHA-256", "GENERATED_CANDIDATE",
                     "USER_APPROVED", "CANON_REGISTERED", "이미지 모델")

    def test_examples_cover_noncombat_experience_without_claiming_implementation(self):
        self.clauses("EXAMPLE_ONLY", "FX-01", "VIS-01", "UI-01", "STORY-01", "DECOR-01",
                     "상처", "단서", "꾸미기", "counterevidence", "NOT_RUN")

    def test_scope_adoption_and_evidence_ceilings_are_not_collapsed(self):
        self.clauses("L0", "L1", "L2", "REUSED_EVIDENCE", "DOC", "MACHINE", "RUNTIME", "HUMAN",
                     "FUN_PASS", "에이전트", "PENDING_PROJECT_ADOPTION", "USER_DECISION_REQUIRED")
        self.assertIn("PROJECT_PRESENTATION_BINDING", self.text(ADAPTER))

    def test_guide_stays_in_shared_knowledge_without_a_packaged_orphan(self):
        self.assertEqual(REFERENCE.parent, Path("docs/knowledge/game-development"))
        self.assertFalse((ROOT / "skills/auditing-and-refining-ui-art/references/experience-to-presentation-contract.md").exists())
        for artifact in (ROOT / ADAPTER.parent).glob("*.md"):
            self.assertIn(artifact.relative_to(ROOT / SKILL.parent).as_posix(),
                          self.text(SKILL), "package sources require a direct Skill route")

    def test_existing_domain_and_fun_boundaries_survive(self):
        self.assertIn("도메인 규칙", self.text(SKILL))
        self.assertIn("NO_UNIVERSAL_FUN_SCORE", self.text(CONCEPT))
        self.assertIn("SLICE_BUILD_READY", self.text(CONCEPT))
        self.assertIn("새 schema를 강제하지 않는다", self.text(ADAPTER))


if __name__ == "__main__":
    unittest.main()
