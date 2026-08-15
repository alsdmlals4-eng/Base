from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from base_tool_contracts import ApprovedAnchorRegistry
from PIL import Image
import pytest

from expression_studio.delivery import ProjectFigmaRegistry
from expression_studio.engine import FakeExpressionEngine
from expression_studio.imports import validate_imported_image
from expression_studio.models import ExpressionRequest
from expression_studio.service import ExpressionStudioService, RunNotFoundError
from tests.test_delivery import write_registry
from tests.test_import_api import png
from tests.test_models import valid_payload


def handoff_service(project_root: Path) -> ExpressionStudioService:
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    (project_root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
    (project_root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")

    approved = project_root / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    approved.parent.mkdir(parents=True, exist_ok=True)
    approved.write_text(
        json.dumps(
            {
                "version": 1,
                "entries": [
                    {
                        "project_id": "demo",
                        "source_path": "art/source/hero.png",
                        "figma_node_url": "https://www.figma.com/design/abc123/demo?node-id=1-2",
                        "source_sha256": hashlib.sha256(anchor.read_bytes()).hexdigest(),
                        "approval_state": "APPROVED",
                        "evidence": {
                            "kind": "EXPORTED_SNAPSHOT",
                            "ref": "handoff-service-test",
                            "checked_at": "2026-08-15T00:00:00Z",
                        },
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", str(project_root)], check=True)
    subprocess.run(["git", "-C", str(project_root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(project_root), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(project_root), "add", ".gitignore", "art", "docs"], check=True)
    subprocess.run(["git", "-C", str(project_root), "commit", "-qm", "approved handoff anchor"], check=True)

    return ExpressionStudioService(
        project_root,
        FakeExpressionEngine(project_root),
        registry=ProjectFigmaRegistry.load(write_registry(project_root)),
        project_id="demo",
        anchor_registry=ApprovedAnchorRegistry.load(approved),
        run_mode="subscription_handoff_import",
    )


def imported_candidates():
    return (
        validate_imported_image(png((220, 30, 30, 255)), declared_source="CHATGPT_INCLUDED", order=0),
        validate_imported_image(png((30, 30, 220, 255)), declared_source="CHATGPT_INCLUDED", order=1),
    )


def test_prepare_subscription_handoff_is_server_issued_and_copy_ready(tmp_path: Path) -> None:
    service = handoff_service(tmp_path)
    request = ExpressionRequest.model_validate(valid_payload())

    pending = service.prepare_subscription_handoff(request)

    assert len(pending.run_id) == 32
    assert pending.packet.run_id == pending.run_id
    assert pending.packet.generation_surface == "CHATGPT_PRO_SUBSCRIPTION"
    assert pending.packet.import_run_mode == "subscription_handoff_import"
    assert pending.packet.import_declared_source == "CHATGPT_INCLUDED"
    assert pending.packet.provider_call_made is False
    assert pending.packet.requires_additional_payment is False
    assert pending.packet.source_filename == "hero.png"
    assert pending.packet.source_sha256 == hashlib.sha256((tmp_path / "art/source/hero.png").read_bytes()).hexdigest()
    assert pending.run_id in pending.prompt
    assert "https://www.figma.com/" not in pending.prompt
    assert str(tmp_path) not in pending.prompt


@pytest.mark.parametrize(
    ("edit_mode", "edit_prompt"),
    [
        ("outfit", "dark navy field coat with brass fasteners"),
        ("scene", "rainy neon alley at night"),
    ],
)
def test_prepare_subscription_handoff_supports_reviewed_character_edit_modes(
    tmp_path: Path,
    edit_mode: str,
    edit_prompt: str,
) -> None:
    service = handoff_service(tmp_path)
    request = ExpressionRequest.model_validate(
        valid_payload(
            edit_mode=edit_mode,
            edit_prompt=edit_prompt,
            controls=[],
            gaze="center",
            head_pose="neutral",
            preset=None,
        )
    )

    pending = service.prepare_subscription_handoff(request)

    assert pending.packet.workflow == "character_edit"
    assert edit_prompt in pending.packet.instruction
    assert edit_prompt in pending.prompt
    assert pending.packet.provider_call_made is False
    assert pending.packet.requires_additional_payment is False
    assert "https://www.figma.com/" not in pending.prompt
    assert str(tmp_path) not in pending.prompt


def test_subscription_handoff_import_preserves_exact_pending_run_and_consumes_once(tmp_path: Path) -> None:
    service = handoff_service(tmp_path)
    pending = service.prepare_subscription_handoff(ExpressionRequest.model_validate(valid_payload()))

    record = service.import_subscription_handoff(pending.run_id, imported_candidates())

    assert record.run_id == pending.run_id
    assert record.run_mode == "subscription_handoff_import"
    assert record.provider_call_made is False
    assert record.status == "generated"
    assert record.public_view()["declared_source"] == "CHATGPT_INCLUDED"
    with pytest.raises(RunNotFoundError):
        service.import_subscription_handoff(pending.run_id, imported_candidates())


def test_invalid_handoff_import_does_not_consume_pending_run(tmp_path: Path) -> None:
    service = handoff_service(tmp_path)
    pending = service.prepare_subscription_handoff(ExpressionRequest.model_validate(valid_payload()))
    first = imported_candidates()[0]

    with pytest.raises(ValueError, match="expected 2"):
        service.import_subscription_handoff(pending.run_id, (first,))

    record = service.import_subscription_handoff(pending.run_id, imported_candidates())
    assert record.run_id == pending.run_id


def test_anchor_change_between_prepare_and_import_fails_closed_and_remains_retryable(tmp_path: Path) -> None:
    service = handoff_service(tmp_path)
    pending = service.prepare_subscription_handoff(ExpressionRequest.model_validate(valid_payload()))
    anchor = tmp_path / "art" / "source" / "hero.png"
    original = anchor.read_bytes()
    anchor.write_bytes(png((10, 20, 30, 255)))

    with pytest.raises(ValueError, match="anchor|SHA-256|changed"):
        service.import_subscription_handoff(pending.run_id, imported_candidates())

    anchor.write_bytes(original)
    record = service.import_subscription_handoff(pending.run_id, imported_candidates())
    assert record.run_id == pending.run_id


def test_unknown_subscription_handoff_run_fails_without_creating_asset_vault_run(tmp_path: Path) -> None:
    service = handoff_service(tmp_path)

    with pytest.raises(RunNotFoundError):
        service.import_subscription_handoff("f" * 32, imported_candidates())

    generated = tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio"
    assert not generated.exists()
