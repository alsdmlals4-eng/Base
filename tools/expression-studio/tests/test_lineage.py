import json
from pathlib import Path

from expression_studio.catalog import resolve_expression
from expression_studio.lineage import write_lineage
from expression_studio.models import ExpressionRequest
from tests.test_models import valid_payload


def test_lineage_records_anchor_hash_and_resolved_phrase(tmp_path: Path) -> None:
    request = ExpressionRequest.model_validate(valid_payload())
    target = write_lineage(request, resolve_expression(request), b"anchor", tmp_path)

    record = json.loads(target.read_text(encoding="utf-8"))

    assert record["anchor"]["sha256"] == "79bfb0e2ba76b9d447606ddbcc494834f05a4c11deb052e74b49ea307a3c5bcd"
    assert record["resolved_expression"]["movement_phrases"] == ["wink the left eye"]
    assert record["requested_expression"]["controls"] == [{"code": "AU46", "intensity": "C", "side": "left"}]
    assert record["generation_instruction"] is None
