from __future__ import annotations

import json
import pathlib
import subprocess

INTEGRATION_BRANCH = "integrate/pr66-game-design-difficulty"
REGISTRY_PATH = pathlib.Path("skills/SKILL_REGISTRY.json")
FRESHNESS_PATH = pathlib.Path(".github/reference-freshness.json")


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout.strip()


def merge_values(first, second, *, prefer_second: bool):
    if first == second:
        return first
    if isinstance(first, dict) and isinstance(second, dict):
        result = {}
        for key in dict.fromkeys([*first.keys(), *second.keys()]):
            if key not in first:
                result[key] = second[key]
            elif key not in second:
                result[key] = first[key]
            else:
                result[key] = merge_values(
                    first[key], second[key], prefer_second=prefer_second
                )
        return result
    if isinstance(first, list) and isinstance(second, list):
        result = []
        for item in [*first, *second]:
            if item not in result:
                result.append(item)
        return result
    return second if prefer_second else first


def dedupe_keyed(items: list[dict], key: str, prefer_second_ids: set[str]) -> list[dict]:
    order: list[str] = []
    merged: dict[str, dict] = {}
    duplicate_counts: dict[str, int] = {}

    for item in items:
        item_id = item[key]
        if item_id not in merged:
            order.append(item_id)
            merged[item_id] = item
            duplicate_counts[item_id] = 1
            continue
        duplicate_counts[item_id] += 1
        merged[item_id] = merge_values(
            merged[item_id],
            item,
            prefer_second=item_id in prefer_second_ids,
        )

    duplicates = {item_id: count for item_id, count in duplicate_counts.items() if count > 1}
    print(f"DEDUPLICATED {key}: {json.dumps(duplicates, ensure_ascii=False, sort_keys=True)}")
    return [merged[item_id] for item_id in order]


def normalize_registry() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["skills"] = dedupe_keyed(
        registry["skills"],
        "skill_id",
        {"analyzing-and-refining-game-concepts"},
    )

    ids = [item["skill_id"] for item in registry["skills"]]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate skill_id remains after normalization")

    skills = {item["skill_id"]: item for item in registry["skills"]}
    game_design = skills["analyzing-and-refining-game-concepts"]
    for required in (
        "game-system-design",
        "difficulty-design",
        "combat-ai-design",
        "attack-budget",
        "threat-budget",
        "tension-pacing",
    ):
        if required not in game_design["trigger_tags"]:
            raise RuntimeError(f"Missing game design trigger: {required}")

    ui = skills["auditing-and-refining-ui-art"]
    for required in ("ui-polishing", "microinteraction", "motion-feedback"):
        if required not in ui["trigger_tags"]:
            raise RuntimeError(f"Missing UI polishing trigger: {required}")

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def normalize_freshness() -> None:
    config = json.loads(FRESHNESS_PATH.read_text(encoding="utf-8"))
    config["canonical_reference_rules"] = dedupe_keyed(
        config["canonical_reference_rules"], "name", set()
    )
    config["coupled_change_rules"] = dedupe_keyed(
        config["coupled_change_rules"], "name", set()
    )

    names = [item["name"] for item in config["coupled_change_rules"]]
    if len(names) != len(set(names)):
        raise RuntimeError("Duplicate coupled-change rule remains after normalization")

    rules = {item["name"]: item for item in config["coupled_change_rules"]}
    for rule_name in (
        "local-skill-contract-registry-learning-sync",
        "registry-structure-test-sync",
    ):
        required = rules[rule_name]["require_any_changed"]
        if "tests/test_game_design_difficulty_workflow.py" not in required:
            raise RuntimeError(f"Game design test missing from {rule_name}")

    ui_rule = rules["game-ux-ui-skill-sync"]
    for required in (
        "skills/SKILL_REGISTRY.json",
        "skills/SKILL_LEARNING_LOG.md",
        "tests/test_game_ux_ui_system.py",
    ):
        if required not in ui_rule["require_all_changed"]:
            raise RuntimeError(f"UI coupled-change contract missing: {required}")

    FRESHNESS_PATH.write_text(
        json.dumps(config, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    normalize_registry()
    normalize_freshness()

    git("add", str(REGISTRY_PATH), str(FRESHNESS_PATH))
    git("diff", "--cached", "--check")
    if not git("diff", "--cached", "--quiet", check=False):
        git("commit", "-m", "chore: normalize integrated skill contracts")
        git("push", "origin", f"HEAD:{INTEGRATION_BRANCH}")
    else:
        print("No normalization changes required")


if __name__ == "__main__":
    main()
