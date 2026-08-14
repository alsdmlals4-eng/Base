from __future__ import annotations

from pathlib import Path

import pytest

from base_tool_contracts import ProjectFigmaTarget
from tool_hub.figma_bridge import BridgeError, DeliveryReceipt, FigmaBridgeStore


PNG_BYTES = b"\x89PNG\r\n\x1a\nfixture-image-bytes"


def target(project_id: str = "urban-legend", file_key: str = "Z7J3eLeavEytKN20H4HfoP") -> ProjectFigmaTarget:
    return ProjectFigmaTarget(
        project_id=project_id,
        display_name=project_id,
        figma_file_key=file_key,
        figma_url=f"https://www.figma.com/design/{file_key}/fixture?node-id=0-1",
        delivery_page="Sprite Animation Studio",
        generation_area="Generated Assets",
        delivery_page_node_id="11:2",
        generation_area_node_id="11:3",
    )


def write_export(root: Path, name: str = "candidate.png", content: bytes = PNG_BYTES) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def receipt_for(job, *, node_id: str = "99:1", artifact_sha256: str | None = None) -> DeliveryReceipt:
    return DeliveryReceipt(
        delivery_id=job.delivery_id,
        project_id=job.project_id,
        figma_file_key=job.figma_file_key,
        generation_area_node_id=job.generation_area_node_id,
        created_node_id=node_id,
        artifact_sha256=artifact_sha256 or job.artifact_sha256,
        artifact_byte_length=job.artifact_byte_length,
        width=32,
        height=32,
    )


def test_job_binds_exact_export_hash_and_route(tmp_path: Path) -> None:
    export = write_export(tmp_path / "project")
    store = FigmaBridgeStore(tmp_path / "private")

    job = store.enqueue(
        tool_id="expression-studio",
        project_id="urban-legend",
        run_id="run-001",
        export_path=export,
        target=target(),
        media_type="image/png",
    )

    assert job.project_id == "urban-legend"
    assert job.figma_file_key == "Z7J3eLeavEytKN20H4HfoP"
    assert job.generation_area_node_id == "11:3"
    assert job.artifact_byte_length == len(PNG_BYTES)
    assert len(job.artifact_sha256) == 64
    assert str(export.resolve()) not in str(job.public_view())


def test_pairing_code_is_one_time_and_project_scoped(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "private")
    pairing = store.create_pairing(project_id="urban-legend", target=target())

    capability = store.exchange_pairing(
        code=pairing.pairing_code,
        current_file_key="Z7J3eLeavEytKN20H4HfoP",
    )

    assert capability.project_id == "urban-legend"
    assert capability.capability_token
    with pytest.raises(BridgeError, match="pairing"):
        store.exchange_pairing(
            code=pairing.pairing_code,
            current_file_key="Z7J3eLeavEytKN20H4HfoP",
        )


def test_expired_pairing_is_rejected(tmp_path: Path) -> None:
    clock = [1000.0]
    store = FigmaBridgeStore(tmp_path / "private", now=lambda: clock[0])
    pairing = store.create_pairing(project_id="urban-legend", target=target(), ttl_seconds=5)
    clock[0] = 1006.0

    with pytest.raises(BridgeError, match="expired"):
        store.exchange_pairing(
            code=pairing.pairing_code,
            current_file_key="Z7J3eLeavEytKN20H4HfoP",
        )


def test_wrong_project_token_cannot_claim_job(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "private")
    export = write_export(tmp_path / "project-a")
    store.enqueue(
        tool_id="expression-studio",
        project_id="urban-legend",
        run_id="run-a",
        export_path=export,
        target=target(),
        media_type="image/png",
    )
    other_target = target("omenward", "IhxUJaS6ik6MpBzdxt6o8D")
    pairing = store.create_pairing(project_id="omenward", target=other_target)
    capability = store.exchange_pairing(
        code=pairing.pairing_code,
        current_file_key=other_target.figma_file_key,
    )

    assert store.claim_next(
        capability_token=capability.capability_token,
        current_file_key=other_target.figma_file_key,
    ) is None


def test_served_artifact_rehash_detects_tampering(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "private")
    export = write_export(tmp_path / "project")
    job = store.enqueue(
        tool_id="expression-studio",
        project_id="urban-legend",
        run_id="run-001",
        export_path=export,
        target=target(),
        media_type="image/png",
    )
    pairing = store.create_pairing(project_id="urban-legend", target=target())
    capability = store.exchange_pairing(
        code=pairing.pairing_code,
        current_file_key="Z7J3eLeavEytKN20H4HfoP",
    )
    export.write_bytes(PNG_BYTES + b"tampered")

    with pytest.raises(BridgeError, match="changed"):
        store.artifact_bytes(
            capability_token=capability.capability_token,
            delivery_id=job.delivery_id,
        )


def test_identical_receipt_is_idempotent_but_conflict_is_rejected(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "private")
    export = write_export(tmp_path / "project")
    job = store.enqueue(
        tool_id="expression-studio",
        project_id="urban-legend",
        run_id="run-001",
        export_path=export,
        target=target(),
        media_type="image/png",
    )
    pairing = store.create_pairing(project_id="urban-legend", target=target())
    capability = store.exchange_pairing(
        code=pairing.pairing_code,
        current_file_key="Z7J3eLeavEytKN20H4HfoP",
    )
    store.claim_next(
        capability_token=capability.capability_token,
        current_file_key="Z7J3eLeavEytKN20H4HfoP",
    )
    receipt = receipt_for(job)

    first = store.accept_receipt(
        capability_token=capability.capability_token,
        receipt=receipt,
    )
    second = store.accept_receipt(
        capability_token=capability.capability_token,
        receipt=receipt,
    )

    assert first == second
    assert first.status == "FIGMA_DELIVERED_VERIFIED"
    with pytest.raises(BridgeError, match="conflict"):
        store.accept_receipt(
            capability_token=capability.capability_token,
            receipt=receipt_for(job, node_id="99:2"),
        )
