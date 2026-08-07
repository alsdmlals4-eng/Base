from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
LOCAL_REFERENCE_DOC = ROOT / "docs" / "knowledge" / "godot" / "LOCAL_GODOT_REFERENCE_LIBRARY.md"
SOURCE_CATALOG = (
    ROOT
    / "skills"
    / "evaluating-godot-assets-and-plugins-before-creation"
    / "references"
    / "source-catalog.md"
)


class LocalGodotReferenceLibraryTests(unittest.TestCase):
    def test_official_demo_corpus_is_explicitly_registered(self) -> None:
        local_reference = LOCAL_REFERENCE_DOC.read_text(encoding="utf-8")
        source_catalog = SOURCE_CATALOG.read_text(encoding="utf-8")

        for text in (local_reference, source_catalog):
            self.assertIn("godot-demo-projects-master", text)
            self.assertIn("REFERENCE_ONLY", text)

        self.assertIn("Official_Demos", local_reference)
        self.assertIn("godotengine/godot-demo-projects", local_reference)


if __name__ == "__main__":
    unittest.main()
