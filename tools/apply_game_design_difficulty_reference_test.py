from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def update_consolidated_test() -> None:
    path = "tests/test_consolidated_skill_references.py"
    text = read(path)
    method = '''    def test_game_system_difficulty_modes_are_integrated_not_new_skills(self) -> None:
        concepts = skill_package_text("analyzing-and-refining-game-concepts")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")

        for term in (
            "`system-design`",
            "`difficulty-and-combat-ai`",
            "game-system-difficulty-and-combat-ai.md",
            "GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md",
            "공격 예산",
            "위협 예산",
            "동적 난이도 조절",
        ):
            self.assertIn(term, concepts)

        for tag in (
            "game-system-design",
            "difficulty-design",
            "combat-ai-design",
            "adaptive-difficulty",
            "attack-budget",
            "threat-budget",
            "tension-pacing",
        ):
            self.assertIn(tag, registry)

        for path_name in (
            "skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md",
            "templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md",
        ):
            self.assertTrue((ROOT / path_name).is_file(), path_name)
            self.assertIn(path_name, start + "\\n" + doc_map)

        self.assertNotIn('"skill_id":"designing-game-difficulty"', registry)
        self.assertNotIn('"skill_id":"designing-combat-ai"', registry)

'''
    if "def test_game_system_difficulty_modes_are_integrated_not_new_skills" not in text:
        marker = 'if __name__ == "__main__":\n'
        if marker not in text:
            raise RuntimeError("consolidated test insertion marker missing")
        text = text.replace(marker, method + marker, 1)
        write(path, text)


def update_evidence_workflow() -> None:
    path = ".github/workflows/validate-evidence-knowledge.yml"
    text = read(path)

    replacements = (
        (
            '      - "tests/test_game_design_difficulty_workflow.py"\n',
            '      - "tests/test_game_design_difficulty_workflow.py"\n'
            '      - "tests/test_consolidated_skill_references.py"\n',
        ),
        (
            '              tests/test_game_design_difficulty_workflow.py \\\n',
            '              tests/test_game_design_difficulty_workflow.py \\\n'
            '              tests/test_consolidated_skill_references.py \\\n',
        ),
        (
            '            tests/test_game_design_difficulty_workflow.py\n',
            '            tests/test_game_design_difficulty_workflow.py\n'
            '            tests/test_consolidated_skill_references.py\n',
        ),
    )

    for old, new in replacements:
        if new in text:
            continue
        if old not in text:
            raise RuntimeError(f"evidence workflow marker missing: {old!r}")
        text = text.replace(old, new, 1)

    write(path, text)


def main() -> None:
    update_consolidated_test()
    update_evidence_workflow()


if __name__ == "__main__":
    main()
