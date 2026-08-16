from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.test_api import client_for
from tests.test_import_api import png
from tests.test_models import valid_payload


@pytest.mark.parametrize(
    ("edit_mode", "edit_prompt", "instruction_fragment"),
    (
        ("outfit", "navy field coat with brass fasteners", "Change only clothing, costume, and wearable accessories"),
        ("scene", "rainy neon alley at night", "Change only the environment, location, and background"),
    ),
)
def test_character_edit_import_writes_real_sample_candidates_inside_project(
    tmp_path: Path,
    edit_mode: str,
    edit_prompt: str,
    instruction_fragment: str,
) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    request = valid_payload(
        edit_mode=edit_mode,
        edit_prompt=edit_prompt,
        controls=[],
        preset=None,
        gaze="center",
        head_pose="neutral",
    )
    files = [
        ("candidates", ("candidate-red.png", png((220, 30, 30, 255)), "image/png")),
        ("candidates", ("candidate-blue.png", png((30, 30, 220, 255)), "image/png")),
    ]

    response = client.post(
        "/api/import-runs",
        data={
            "request_json": json.dumps(request),
            "declared_source": "CHATGPT_INCLUDED",
        },
        files=files,
    )

    assert response.status_code == 201
    run = response.json()
    assert run["status"] == "generated"
    assert run["candidate_count"] == 2
    assert instruction_fragment in run["generation_instruction"]
    assert edit_prompt in run["generation_instruction"]
    assert run["provider_call_made"] is False

    first = client.get(f"/api/runs/{run['run_id']}/candidates/0")
    second = client.get(f"/api/runs/{run['run_id']}/candidates/1")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.content != second.content

    generated = list(
        (tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio").rglob(
            "candidate-*.png"
        )
    )
    assert len(generated) == 2
    assert all(tmp_path.resolve() in path.resolve().parents for path in generated)
