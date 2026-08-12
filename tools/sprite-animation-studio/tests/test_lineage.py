import hashlib
import json
from pathlib import Path

from sprite_animation_studio.lineage import write_lineage
from tests.test_models import valid_payload
from sprite_animation_studio.models import SpriteAnimationRequest


def test_lineage_records_figma_url_and_anchor_sha256(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())

    record = write_lineage(request, b"anchor", tmp_path, engine={"provenance": "test"})
    data = json.loads(record.read_text(encoding="utf-8"))

    assert data["anchor"]["sha256"] == hashlib.sha256(b"anchor").hexdigest()
    assert data["anchor"]["figma_node_url"].endswith("node-id=1-2")
