"""Source-identity adversarial regressions; structure-only, never source-authenticity proof."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/validate_player_surface_plan.py"
FIXTURE_FILE = ROOT / "tests/test_player_surface_plan.py"
PACKET_CONTRACT = ROOT / "docs/knowledge/game-development/BENCHMARK_FIRST_MODULAR_UI_PRODUCTION_PACKET_CONTRACT.md"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PlayerSurfacePlanReviewRound4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = _load(CHECKER, "surface_plan_checker_round4")
        cls.fixtures = _load(FIXTURE_FILE, "surface_plan_fixtures_round4")

    def rejected(self, packet, code: str):
        errors = self.checker.validate_packet(packet)
        self.assertTrue(any(code in error for error in errors), (code, errors))

    def test_project_repository_rejects_dot_segments(self):
        for identity in ["../fixture-game", "owner/.", "owner/..", "./.", "owner/..git"]:
            with self.subTest(identity=identity):
                packet = self.fixtures.packet()
                packet["repository"] = identity
                self.rejected(packet, "SOURCE_IDENTITY")

    def test_github_self_repository_detection_normalizes_dot_segments(self):
        for source in [
            "https://github.com/other/../example/fixture-game/blob/main/ui.md",
            "https://github.com/other/%2e%2e/example/fixture-game/blob/main/ui.md",
            "https://raw.githubusercontent.com/other/../example/fixture-game/main/ui.md",
            "https://api.github.com/repos/other/../example/fixture-game/contents/ui.md",
        ]:
            with self.subTest(source=source):
                packet = self.fixtures.packet()
                packet["references"][0]["source"] = source
                self.rejected(packet, "EXTERNAL_BENCHMARK_REQUIRED")

    def test_legacy_ipv4_loopback_and_private_hosts_are_rejected(self):
        for source in [
            "https://127.1/example",
            "https://0177.0.0.1/example",
            "https://2130706433/example",
            "https://0300.0250.0001.0001/example",
            "https://0x7f000001/example",
        ]:
            with self.subTest(source=source):
                packet = self.fixtures.packet()
                packet["references"][0].update(
                    source=source,
                    source_repository="other/reference-game",
                )
                self.rejected(packet, "REFERENCE_ORIGIN")

    def test_non_github_repository_source_requires_source_repository_identity(self):
        packet = self.fixtures.packet()
        packet["references"][0].update(
            evidence_kind="SOURCE_CODE",
            source="https://gitlab.com/example/fixture-game/-/blob/main/ui.gd",
        )
        packet["references"][0].pop("source_repository", None)
        self.rejected(packet, "REFERENCE_ORIGIN")

    def test_non_github_repository_identity_must_differ_from_project(self):
        packet = self.fixtures.packet()
        packet["references"][0].update(
            evidence_kind="SOURCE_CODE",
            source="https://gitlab.com/example/fixture-game/-/blob/main/ui.gd",
            source_repository="example/fixture-game",
        )
        self.rejected(packet, "EXTERNAL_BENCHMARK_REQUIRED")

    def test_non_github_repository_source_with_distinct_identity_is_valid(self):
        packet = self.fixtures.packet()
        packet["references"][0].update(
            evidence_kind="SOURCE_CODE",
            source="https://gitlab.com/other/reference-game/-/blob/main/ui.gd",
            source_repository="other/reference-game",
        )
        self.assertEqual(self.checker.validate_packet(packet), [])

    def test_public_product_observation_does_not_invent_repository_identity(self):
        packet = self.fixtures.packet()
        packet["references"][0].update(
            evidence_kind="PRODUCT_OBSERVATION",
            source="https://factorio.com/blog/post/fff-246",
        )
        packet["references"][0].pop("source_repository", None)
        self.assertEqual(self.checker.validate_packet(packet), [])

    def test_packet_contract_records_source_identity_hardening(self):
        text = PACKET_CONTRACT.read_text(encoding="utf-8")
        for token in [
            "URL_DOT_SEGMENTS_NORMALIZED_BEFORE_REPOSITORY_IDENTITY",
            "LEGACY_NUMERIC_IP_NORMALIZED_OR_REJECTED",
            "NON_GITHUB_SOURCE_CODE_REQUIRES_SOURCE_REPOSITORY",
            "PRODUCT_OBSERVATION_DOES_NOT_REQUIRE_REPOSITORY_IDENTITY",
        ]:
            with self.subTest(token=token):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
