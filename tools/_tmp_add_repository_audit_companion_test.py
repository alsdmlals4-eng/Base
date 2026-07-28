from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tests/test_consolidated_skill_references.py"


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    anchor = '\nif __name__ == "__main__":\n    unittest.main()\n'
    method = '''\n    def test_repository_wide_audit_is_an_integrated_mode_with_consumers(self) -> None:\n        adversarial = skill_package_text("running-adversarial-review-and-refinement")\n        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")\n        doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")\n        prompt = (ROOT / "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md").read_text(encoding="utf-8")\n\n        for term in (\n            "`repository-wide-audit`",\n            "references/repository-wide-audit-protocol.md",\n            "CURRENT_AUTHORITY",\n            "UNTOUCHED_CONSUMER",\n            "ALLOWED_LEGACY",\n            "STALE_PROMPT_CONTRACT",\n        ):\n            self.assertIn(term, adversarial)\n\n        for tag in (\n            "repository-wide-audit",\n            "full-file-audit",\n            "stale-file-audit",\n            "untouched-consumer-audit",\n            "prompt-drift",\n        ):\n            self.assertIn(tag, registry)\n\n        self.assertIn("repository-wide-audit", doc_map)\n        self.assertIn("repository-wide-audit", prompt)\n        self.assertNotIn('"skill_id":"repository-wide-adversarial-audit"', registry)\n'''
    if "def test_repository_wide_audit_is_an_integrated_mode_with_consumers" in text:
        return
    if text.count(anchor) != 1:
        raise RuntimeError("test file footer anchor not found exactly once")
    PATH.write_text(text.replace(anchor, method + anchor, 1), encoding="utf-8")


if __name__ == "__main__":
    main()
