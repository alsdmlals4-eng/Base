import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def load_validator():
    path = ROOT / "tools/validate_external_ui_procurement_receipt.py"
    spec = importlib.util.spec_from_file_location("procurement_validator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_behavior_eval_adds_positive_negative_and_boundary_pressure() -> None:
    evals = load_json("skills/SKILL_BEHAVIOR_EVALS.json")
    cases = {case["case_id"]: case for case in evals["cases"]}
    required = {"SBE-901", "SBE-902", "SBE-903", "SBE-904"}
    assert required <= cases.keys()
    assert cases["SBE-901"]["expected_primary_skill"] == "managing-project-intake-and-work-contract"
    assert cases["SBE-902"]["case_type"] == "negative"
    assert "auditing-and-refining-ui-art" in cases["SBE-903"]["expected_supporting_skills"]
    assert "auditing-and-refining-ui-art" in cases["SBE-904"]["forbidden_skills"]
    assert evals["model_run_status"] == "NOT_RUN"


def test_actual_shadcn_procurement_receipt_is_evidence_backed_and_fail_closed() -> None:
    receipt = load_json(
        "docs/evidence/external-ui-procurement/BCP008_SHADCN_BUTTON_PILOT.json"
    )
    assert receipt["source_repo"] == "shadcn-ui/ui"
    assert receipt["source_commit"] == "b1c580c637f4666890b25c69cdc315c93a892c5d"
    assert receipt["registry_item"] == "button"
    assert receipt["source_acquisition"] == "PASS"
    assert receipt["license"] == "MIT"
    assert receipt["license_blob_sha"] == "fad4d887a681dd49233e5ed01ee2c7a1513089a0"
    assert receipt["source_package_declared_version"] == "4.16.2"
    assert receipt["source_package_published_status"] == "NOT_PUBLISHED_ETARGET"
    assert receipt["published_cli_version"] == "4.16.1"
    assert receipt["procurement_execution"] == "PASS_DISPOSABLE_WEB_FIXTURE"
    assert receipt["disposable_fixture"]["procurement"] == "PASS"
    assert receipt["disposable_fixture"]["build"] == "PASS"
    assert receipt["disposable_fixture"]["generated_component_sha256"] == "9ce417985b97956fbb3a73c84b0eb60230fd0a9844c5111df92e061731440a3f"
    assert receipt["installation"] == "NOT_RUN"
    assert receipt["target_project_installation"] == "NOT_RUN"
    assert receipt["actual_render_review"] == "NOT_RUN"
    assert receipt["decision"] == "BLOCKED_UNVERIFIED"
    assert "SOURCE_PACKAGE_VERSION_NOT_PUBLISHED" in receipt["reason_codes"]
    assert receipt["component_sha256"] == "cc36af0f8b5019c33cc039fbf03bb952a513072b15b55b53c592b78af3e5f4c4"

    validator = load_validator()
    result = validator.validate_receipt(receipt)
    assert result["valid"] is True
    assert result["decision"] == "BLOCKED_UNVERIFIED"
    assert result["errors"] == []
