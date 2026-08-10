from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_CHECKERS = (
    ROOT / "tools/check_base_v9_4_1_release.py",
    ROOT / "tools/check_base_v9_4_2_release.py",
    ROOT / "tools/check_base_v9_4_3_release.py",
)


class HistoricalRegistryEvolutionTests(unittest.TestCase):
    def test_historical_release_pins_do_not_freeze_current_registry(self) -> None:
        for path in RELEASE_CHECKERS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("current Registry raw bytes do not match", text)
                self.assertNotIn("current Registry bytes do not match", text)
                self.assertIn("Registry blob at", text)
                self.assertIn("wrong SHA-256", text)


if __name__ == "__main__":
    unittest.main()
