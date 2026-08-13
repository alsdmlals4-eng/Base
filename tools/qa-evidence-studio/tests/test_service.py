import json
from pathlib import Path
import subprocess

import pytest
from PIL import Image

from qa_evidence_studio.models import ChecklistItem, CreateSessionRequest
from qa_evidence_studio.service import QaEvidenceError, QaEvidenceService


def make_project(root: Path) -> Path:
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True)
    (root / "project.godot").write_text("[application]\nconfig/name=\"QA Fixture\"\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", ".gitignore", "project.godot"], check=True)
    subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=QA", "-c", "user.email=qa@example.invalid", "commit", "-qm", "fixture"],
        check=True,
    )
    return root


def request(project: Path) -> CreateSessionRequest:
    return CreateSessionRequest(
        title="Main menu image and UX review",
        build_commit=subprocess.check_output(["git", "-C", str(project), "rev-parse", "HEAD"], text=True).strip(),
        checklist=[
            ChecklistItem(item_id="visual-readability", label="Image readability"),
            ChecklistItem(item_id="keyboard-flow", label="Keyboard UX"),
        ],
    )


def png_bytes(tmp_path: Path) -> bytes:
    path = tmp_path / "sample.png"
    Image.new("RGBA", (16, 16), (20, 40, 80, 255)).save(path)
    return path.read_bytes()


def test_new_session_is_pc_first_and_cannot_claim_human_validation(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    session = QaEvidenceService(project, "demo-game").create_session(request(project))

    assert session["stage"] == "PREPARING_VISUAL_UX"
    assert session["reviewer"] == {"role": "DEVELOPER_OWNER", "count": 1}
    assert session["external_tester_status"] == "NOT_AVAILABLE_NOT_REQUIRED_FOR_PHASE_1"
    assert session["platforms"]["pc"]["status"] == "NOT_RUN"
    assert session["platforms"]["android"] == {
        "status": "DEFERRED_NOT_CONNECTED",
        "gate": "AFTER_PC_IMPLEMENTATION_BEFORE_RELEASE",
    }
    assert session["overall_result"] == "NOT_RUN"


def test_results_are_blocked_until_visual_and_ux_placement_is_complete(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session = service.create_session(request(project))

    with pytest.raises(QaEvidenceError, match="image and UX placement"):
        service.record_result(session["session_id"], "visual-readability", "PASS", "looks clear")
    with pytest.raises(QaEvidenceError, match="acknowledgement"):
        service.mark_visual_ux_ready(session["session_id"], "")


def test_developer_can_record_pc_results_and_finalize_hashed_packet(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session = service.create_session(request(project))
    session_id = session["session_id"]

    ready = service.mark_visual_ux_ready(
        session_id,
        "I confirm the planned images and UX elements are placed in this PC build.",
    )
    first = service.record_result(session_id, "visual-readability", "PASS", "Readable at 1280x720")
    service.record_result(session_id, "keyboard-flow", "PASS", "Completed by developer")
    evidence = service.add_image_evidence(session_id, "screen.png", "image/png", png_bytes(tmp_path))
    final = service.finalize(session_id)

    assert ready["stage"] == "READY_FOR_DEVELOPER_PC_REVIEW"
    assert first["stage"] == "DEVELOPER_PC_REVIEW_IN_PROGRESS"
    assert len(evidence["sha256"]) == 64
    assert final["stage"] == "DEVELOPER_PC_REVIEW_COMPLETE"
    assert final["overall_result"] == "PASS"
    assert final["platforms"]["android"]["status"] == "DEFERRED_NOT_CONNECTED"
    packet = json.loads(Path(final["packet_path"]).read_text(encoding="utf-8"))
    assert packet["session_id"] == session_id
    assert packet["evidence"][0]["sha256"] == evidence["sha256"]
    assert str(project.resolve()) not in json.dumps(packet)


def test_finalize_blocks_missing_result_or_image_evidence(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session_id = service.create_session(request(project))["session_id"]
    service.mark_visual_ux_ready(session_id, "Images and UX are placed for PC review.")

    with pytest.raises(QaEvidenceError, match="required checklist"):
        service.finalize(session_id)
    service.record_result(session_id, "visual-readability", "PASS", "clear")
    service.record_result(session_id, "keyboard-flow", "PASS", "works")
    with pytest.raises(QaEvidenceError, match="image evidence"):
        service.finalize(session_id)


def test_fail_and_blocked_results_cannot_be_misreported_as_pass(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session_id = service.create_session(request(project))["session_id"]
    service.mark_visual_ux_ready(session_id, "Images and UX are placed for PC review.")
    service.record_result(session_id, "visual-readability", "FAIL", "text clips")
    service.record_result(session_id, "keyboard-flow", "BLOCKED", "gamepad unavailable")
    service.add_image_evidence(session_id, "screen.png", "image/png", png_bytes(tmp_path))

    final = service.finalize(session_id)

    assert final["overall_result"] == "FAIL"
    assert final["platforms"]["pc"]["status"] == "FAIL"


def test_evidence_rejects_wrong_media_and_oversized_content(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session_id = service.create_session(request(project))["session_id"]

    with pytest.raises(QaEvidenceError, match="PNG, JPEG, or WebP"):
        service.add_image_evidence(session_id, "note.txt", "text/plain", b"not an image")
    with pytest.raises(QaEvidenceError, match="25 MiB"):
        service.add_image_evidence(session_id, "huge.png", "image/png", b"x" * (25 * 1024 * 1024 + 1))


def test_session_rejects_a_commit_that_does_not_exist_in_the_project(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    payload = request(project).model_copy(update={"build_commit": "f" * 40})

    with pytest.raises(QaEvidenceError, match="build commit"):
        QaEvidenceService(project, "demo-game").create_session(payload)


def test_session_rejects_a_tag_object_sha_in_the_build_commit_field(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    subprocess.run(
        [
            "git",
            "-C",
            str(project),
            "-c",
            "user.name=QA",
            "-c",
            "user.email=qa@example.invalid",
            "tag",
            "-a",
            "fixture-tag",
            "-m",
            "fixture tag",
        ],
        check=True,
    )
    tag_object = subprocess.check_output(
        ["git", "-C", str(project), "rev-parse", "fixture-tag^{tag}"], text=True
    ).strip()
    payload = request(project).model_copy(update={"build_commit": tag_object})

    with pytest.raises(QaEvidenceError, match="build commit"):
        QaEvidenceService(project, "demo-game").create_session(payload)


def test_evidence_rejects_a_replaced_symlink_directory(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    service = QaEvidenceService(project, "demo-game")
    session_id = service.create_session(request(project))["session_id"]
    evidence_directory = (
        project / ".asset-vault" / "library" / "generated" / "qa-evidence-studio" / session_id / "evidence"
    )
    outside = tmp_path / "outside"
    outside.mkdir()
    evidence_directory.rmdir()
    evidence_directory.symlink_to(outside, target_is_directory=True)

    with pytest.raises(QaEvidenceError, match="link, reparse point, or non-directory"):
        service.add_image_evidence(session_id, "screen.png", "image/png", png_bytes(tmp_path))
    assert list(outside.iterdir()) == []
