import hashlib
from pathlib import Path

from PIL import Image
import pytest

from base_tool_contracts import StagingViolation
from expression_studio.exporter import export_selected_candidate


def test_expression_export_hashes_the_verified_output_bytes_without_reopening_final_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    candidates = tmp_path / "candidates"
    exports = tmp_path / "exports"
    candidates.mkdir()
    exports.mkdir()
    candidate = candidates / "candidate-000.png"
    Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(candidate)
    expected = (hashlib.sha256(candidate.read_bytes()).hexdigest(),)
    monkeypatch.setattr(Path, "read_bytes", lambda self: (_ for _ in ()).throw(AssertionError(f"lexical output read: {self}")))

    result = export_selected_candidate(
        exports,
        [candidate],
        0,
        "wink",
        candidate_sha256=expected,
        engine={"provenance": "test"},
        anchor_sha256="0" * 64,
        anchor_verification="ANCHOR_EVIDENCE_VERIFIED",
        anchor_evidence={},
    )

    assert result.manifest.is_file()


def test_expression_export_rejects_candidate_symlink_swap_after_generation_hashing(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates"
    exports = tmp_path / "exports"
    candidates.mkdir()
    exports.mkdir()
    candidate = candidates / "candidate-000.png"
    Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(candidate)
    expected = (hashlib.sha256(candidate.read_bytes()).hexdigest(),)
    outside = tmp_path / "outside.png"
    Image.new("RGBA", (8, 8), (0, 255, 0, 255)).save(outside)
    candidate.unlink()
    candidate.symlink_to(outside)

    with pytest.raises(StagingViolation, match="regular file"):
        export_selected_candidate(
            exports,
            [candidate],
            0,
            "wink",
            candidate_sha256=expected,
            engine={"provenance": "test"},
            anchor_sha256="0" * 64,
            anchor_verification="ANCHOR_EVIDENCE_VERIFIED",
            anchor_evidence={},
        )
