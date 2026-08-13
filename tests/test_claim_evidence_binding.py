from pathlib import Path


def test_review_script_exposes_entrypoint() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "skills/reviewing-and-validating-project-changes/scripts/verify_evidence.py").read_text(encoding="utf-8")
    assert "def validate_evidence(" in text
