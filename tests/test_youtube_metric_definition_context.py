from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "templates/game-development-youtube/EPISODE_PACKET.md"


class YouTubeMetricDefinitionContextTests(unittest.TestCase):
    def test_episode_packet_separates_shorts_view_definitions(self) -> None:
        text = PACKET_PATH.read_text(encoding="utf-8")
        for token in (
            "content_type: LONG_FORM | SHORT | LIVE | OTHER",
            "youtube_metric_definition_checked_at:",
            "shorts_views_basis: NOT_APPLICABLE | PUBLIC_VIEWS | ENGAGED_VIEWS | BOTH_RECORDED | BLOCKED_UNVERIFIED",
            "shorts_public_views:",
            "shorts_engaged_views:",
            "2025-03-31",
            "Do not join public views and Engaged views into one longitudinal metric",
            "metric-definition changes as confounders",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
