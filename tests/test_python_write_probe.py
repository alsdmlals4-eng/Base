from pathlib import Path


def test_review_script_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "skills/reviewing-and-validating-project-changes/scripts/verify_evidence.py").is_file()
