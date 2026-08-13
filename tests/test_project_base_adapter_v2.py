import copy
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).parents[1]
V1_SCHEMA = ROOT / "schemas" / "project-base-adapter-v1.schema.json"
V2_SCHEMA = ROOT / "schemas" / "project-base-adapter-v2.schema.json"
V1_TEMPLATE = ROOT / "templates" / "project-operations" / "PROJECT_BASE_ADAPTER.json"
V2_TEMPLATE = ROOT / "templates" / "project-operations" / "PROJECT_BASE_ADAPTER_V2.json"


def load_contract_module():
    spec = importlib.util.spec_from_file_location(
        "project_operating_contract_v2_test", ROOT / "tools" / "project_operating_contract.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def errors(schema_path: Path, payload: dict) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return [error.message for error in Draft202012Validator(schema).iter_errors(payload)]


def test_v2_requires_one_canonical_kebab_case_project_id() -> None:
    template = json.loads(V2_TEMPLATE.read_text(encoding="utf-8"))

    assert errors(V2_SCHEMA, template) == []
    for invalid in ("Ten-Paces", "ten_paces", "-ten-paces", "ten--paces", ""):
        payload = copy.deepcopy(template)
        payload["project"]["project_id"] = invalid
        assert errors(V2_SCHEMA, payload), invalid

    payload = copy.deepcopy(template)
    del payload["project"]["project_id"]
    assert errors(V2_SCHEMA, payload)


def test_v1_contract_is_unchanged_and_blocked_for_hub_identity() -> None:
    v1 = json.loads(V1_TEMPLATE.read_text(encoding="utf-8"))
    module = load_contract_module()

    assert errors(V1_SCHEMA, v1) == []
    assert module.hub_identity_state(v1) == "IDENTITY_MIGRATION_REQUIRED"
    assert module.adapter_schema(v1)[0] == V1_SCHEMA


def test_explicit_v1_to_v2_migration_is_deterministic_and_non_mutating() -> None:
    v1 = json.loads(V1_TEMPLATE.read_text(encoding="utf-8"))
    original = copy.deepcopy(v1)
    module = load_contract_module()

    migrated = module.migrate_adapter_v1_to_v2(v1, project_id="ten-paces-hidden-moves")

    assert v1 == original
    assert migrated["schema_version"] == 2
    assert migrated["project"]["project_id"] == "ten-paces-hidden-moves"
    assert module.hub_identity_state(migrated) == "IDENTITY_VERIFIED"
    assert module.adapter_schema(migrated)[0] == V2_SCHEMA
    assert errors(V2_SCHEMA, migrated) == []


def test_version_dispatch_rejects_an_unknown_adapter_version() -> None:
    module = load_contract_module()

    try:
        module.adapter_schema({"schema_version": 3})
    except module.ContractError as error:
        assert "Unsupported" in str(error)
    else:
        raise AssertionError("unknown project adapter version was accepted")


def test_migration_rejects_inferred_or_invalid_identity_and_v2_input() -> None:
    v1 = json.loads(V1_TEMPLATE.read_text(encoding="utf-8"))
    module = load_contract_module()

    for invalid in ("", "Ten-Paces", "ten_paces"):
        try:
            module.migrate_adapter_v1_to_v2(v1, project_id=invalid)
        except module.ContractError as error:
            assert "project_id" in str(error)
        else:
            raise AssertionError(f"accepted invalid project_id {invalid!r}")

    v2 = copy.deepcopy(v1)
    v2["schema_version"] = 2
    try:
        module.migrate_adapter_v1_to_v2(v2, project_id="demo")
    except module.ContractError as error:
        assert "v1" in str(error)
    else:
        raise AssertionError("accepted a non-v1 migration source")
