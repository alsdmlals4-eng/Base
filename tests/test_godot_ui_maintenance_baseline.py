from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md"


class GodotUiMaintenanceBaselineTests(unittest.TestCase):
    def test_maintenance_reference_is_dated_and_project_pin_preserving(self) -> None:
        text = CONTRACT.read_text(encoding="utf-8")

        for marker in (
            "Godot 4.7 UI maintenance baseline — dated reference",
            "target project's adopted Godot version remains authoritative",
            "Do not silently replace a project engine pin",
            "https://docs.godotengine.org/en/stable/about/release_policy.html",
            "https://godotengine.org/download/archive/",
            "Godot 4.7.2-stable (2026-08-18)",
            "https://godotengine.org/article/maintenance-release-godot-4-7-2/",
            "dated Base reference, not a floating `current` claim",
            "not project runtime evidence",
        ):
            self.assertIn(marker, text)

        self.assertNotIn(
            "Use Godot 4.7.1-stable as the current 4.7 maintenance reference",
            text,
        )


if __name__ == "__main__":
    unittest.main()
