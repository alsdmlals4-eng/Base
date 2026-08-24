from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = (
    ROOT
    / "docs"
    / "knowledge"
    / "serial-fiction"
    / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md"
)


class StoryCraftPlanningNormalizationTests(unittest.TestCase):
    def test_story_planning_lenses_are_explicit_and_bounded(self) -> None:
        guide = GUIDE_PATH.read_text(encoding="utf-8")

        for token in (
            "EMMA_COATS_STORYBASICS_NOT_OFFICIAL_PIXAR_POLICY",
            "HERO_JOURNEY_12_IS_VOGLER_ADAPTATION",
            "HERO_JOURNEY_OPTIONAL_12_STAGE_LENS",
            "STORY_PLANNING_MINIMUM",
            "OPTIONAL_STORY_PLANNING_FIELDS",
            "FOCAL_AGENT_DECISION_OWNER",
            "WANT_NEED_STAKES",
            "CAUSE_BEFORE_SEQUENCE",
            "CAUSAL_BEAT_CHAIN",
            "COINCIDENCE_CAN_START_NOT_SOLVE",
            "AUDIENCE_PERCEPTION_ORDER",
            "END_BACKWARD_PLANNING",
            "PROMISE_PROGRESS_PAYOFF",
            "DRAFT_FEEDBACK_REWRITE",
            "IDEA_DIVERGENCE_BEFORE_COMMIT",
            "NEGATIVE_NEXT_BEAT_LIST",
            "IDEA_PARKING_LOT",
            "SYMBOL_MOTIF_METAPHOR_OPTIONAL",
            "VOICE_TONE_CONTINUITY",
            "PARAGRAPH_SCREEN_BLOCK_PREFERENCE",
        ):
            self.assertIn(token, guide)

        lowered = guide.lower()
        self.assertIn("optional", lowered)
        self.assertIn("universal", lowered)
        self.assertIn("framework_overfit", lowered)

    def test_normalization_rejects_false_universal_rules(self) -> None:
        guide = GUIDE_PATH.read_text(encoding="utf-8")

        for token in (
            "MULTI_POV_IS_NOT_AUTOMATIC_FAILURE",
            "TRAGEDY_OR_VILLAIN_NOT_REQUIRED",
            "THREE_TO_FIVE_LINES_NOT_UNIVERSAL",
            "FEEDBACK_IS_EVIDENCE_NOT_CANON",
        ):
            self.assertIn(token, guide)

        self.assertNotIn("픽사의 공식 22가지 법칙", guide)
        self.assertNotIn("캠벨의 12단계 영웅의 여정", guide)

    def test_external_craft_claims_have_traceable_primary_or_near_primary_links(self) -> None:
        guide = GUIDE_PATH.read_text(encoding="utf-8")

        for token in (
            "https://www.khanacademy.org/computing/pixar/storytelling",
            "https://www.pixartouchbook.com/blog/2011/5/15/pixar-story-rules-one-version.html",
            "https://www.open.edu/openlearn/mod/oucontent/view.php?id=101090&section=_unit4.2",
            "https://chrisvogler.wordpress.com/tag/the-heros-journey/",
            "https://www.youtube.com/watch?v=ihd76ijy9LU",
        ):
            self.assertIn(token, guide)


if __name__ == "__main__":
    unittest.main()
