from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = "tests/test_game_design_difficulty_workflow.py"
RULE_NAMES = {
    "local-skill-contract-registry-learning-sync",
    "registry-structure-test-sync",
}


def main() -> None:
    path = ROOT / ".github" / "reference-freshness.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    matched: set[str] = set()
    for rule in data["coupled_change_rules"]:
        name = rule.get("name")
        if name not in RULE_NAMES:
            continue
        matched.add(name)
        companions = rule.setdefault("require_any_changed", [])
        if TEST_PATH not in companions:
            companions.append(TEST_PATH)

    missing = RULE_NAMES - matched
    if missing:
        raise RuntimeError(f"freshness rules not found: {sorted(missing)}")

    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
