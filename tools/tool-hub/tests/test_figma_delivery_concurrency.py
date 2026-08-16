from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import time

import pytest

from test_figma_delivery import png_bytes, registry
from test_projects import make_project
from tool_hub.figma_delivery import FigmaDeliveryService
from tool_hub.projects import ProjectLocator


def test_one_queued_delivery_can_be_claimed_by_only_one_concurrent_bridge_worker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    pairing = service.create_pairing("coc-fiction")
    token = service.pair_by_code(pairing.pairing_code, "bridge-test").token
    job = service.enqueue("expression-studio", "coc-fiction", "run-race", png_bytes(), "image/png")

    original_verify = service._verify_content

    def slow_verify(candidate):
        time.sleep(0.05)
        return original_verify(candidate)

    monkeypatch.setattr(service, "_verify_content", slow_verify)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: service.claim_next(token), range(2)))

    claimed = [result for result in results if result is not None]
    assert len(claimed) == 1
    assert claimed[0].delivery_id == job.delivery_id
    assert service.job_view("coc-fiction", job.delivery_id).state == "CLAIMED"
