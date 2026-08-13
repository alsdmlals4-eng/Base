from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_completion_claim_gate_has_required_surfaces() -> None:
    required = (
        "tools/check_completion_claim_contract.py",
        "schemas/completion-claim-contract-v1.schema.json",
        "schemas/completion-claim-evidence-v1.schema.json",
        "templates/quality/COMPLETION_CLAIM_CONTRACT.json",
    )
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing, f"missing completion-claim surfaces: {missing}"
