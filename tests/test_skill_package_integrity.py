from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"
LOCAL_PREFIXES = (
    "skills/",
    "templates/",
    "docs/",
    "tools/",
    "tests/",
    "schemas/",
    ".github/",
    "[수정제안서]/",
)
LOCAL_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".toml", ".txt"}
BACKTICK = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
FIELD = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?P<value>.+?)\s*$", re.MULTILINE)


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def front_matter_fields(text: str) -> dict[str, str]:
    match = FRONT_MATTER.search(text)
    if not match:
        return {}
    return {
        field.group("key"): field.group("value").strip().strip("'\"")
        for field in FIELD.finditer(match.group("body"))
    }


def candidate_local_path(raw: str, skill_path: Path) -> Path | None:
    value = raw.strip().strip(".,;:")
    if not value or value.startswith(("http://", "https://", "mailto:")):
        return None
    value = value.split("#", 1)[0]
    if any(token in value for token in ("<", ">", "*", "{", "}", "|")):
        return None
    suffix = Path(value).suffix.lower()
    if suffix not in LOCAL_SUFFIXES:
        return None
    if value.startswith(("references/", "scripts/")):
        return skill_path.parent / value
    if value.startswith(LOCAL_PREFIXES):
        return ROOT / value
    return None


class SkillPackageIntegrityTests(unittest.TestCase):
    def test_registry_and_skill_packages_are_one_to_one(self) -> None:
        registry = load_registry()
        items = registry["skills"]
        expected_paths = {item["path"] for item in items}
        actual_paths = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(
            actual_paths,
            expected_paths,
            "Registry and active skill package paths differ",
        )
        self.assertEqual(len(items), len(expected_paths), "Duplicate skill paths in Registry")

    def test_each_skill_identity_and_registry_contract_match(self) -> None:
        registry = load_registry()
        seen_ids: set[str] = set()
        for item in registry["skills"]:
            skill_id = item["skill_id"]
            self.assertNotIn(skill_id, seen_ids, f"Duplicate skill_id: {skill_id}")
            seen_ids.add(skill_id)

            path = ROOT / item["path"]
            text = path.read_text(encoding="utf-8")
            fields = front_matter_fields(text)
            self.assertEqual(fields.get("name"), skill_id, f"Front matter name mismatch: {path}")
            self.assertTrue(fields.get("description"), f"Missing description: {path}")
            self.assertEqual(path.parent.name, skill_id, f"Directory and skill_id mismatch: {path}")
            self.assertEqual(item["status"], "ACTIVE", f"Non-active skill in active Registry: {skill_id}")
            self.assertFalse(item["load_by_default"], f"Skill must remain selective: {skill_id}")
            for field in ("trigger_tags", "use_when", "do_not_use_when", "review_triggers"):
                self.assertTrue(item[field], f"Empty Registry field {field}: {skill_id}")
            self.assertTrue((ROOT / item["learning_log"]).is_file(), f"Missing learning log: {skill_id}")

    def test_all_local_artifact_references_from_skills_exist(self) -> None:
        registry = load_registry()
        missing: list[str] = []
        for item in registry["skills"]:
            skill_path = ROOT / item["path"]
            text = skill_path.read_text(encoding="utf-8", errors="replace")
            raw_references = set(BACKTICK.findall(text))
            raw_references.update(MARKDOWN_LINK.findall(text))
            for raw in sorted(raw_references):
                candidate = candidate_local_path(raw, skill_path)
                if candidate is not None and not candidate.is_file():
                    missing.append(
                        f"{skill_path.relative_to(ROOT).as_posix()} -> {raw}"
                    )
        self.assertEqual(
            missing,
            [],
            "Skill documents reference missing local artifacts:\n" + "\n".join(missing),
        )

    def test_every_packaged_reference_or_script_is_linked_from_its_skill(self) -> None:
        registry = load_registry()
        orphaned: list[str] = []
        for item in registry["skills"]:
            skill_path = ROOT / item["path"]
            skill_dir = skill_path.parent
            text = skill_path.read_text(encoding="utf-8", errors="replace")
            for folder_name in ("references", "scripts"):
                folder = skill_dir / folder_name
                if not folder.is_dir():
                    continue
                for artifact in sorted(path for path in folder.rglob("*") if path.is_file()):
                    repo_relative = artifact.relative_to(ROOT).as_posix()
                    skill_relative = artifact.relative_to(skill_dir).as_posix()
                    if repo_relative not in text and skill_relative not in text:
                        orphaned.append(
                            f"{item['skill_id']} -> {repo_relative}"
                        )
        self.assertEqual(
            orphaned,
            [],
            "Packaged references/scripts are not linked from SKILL.md:\n" + "\n".join(orphaned),
        )

    def test_every_active_skill_is_discoverable_from_current_entrypoints(self) -> None:
        registry = load_registry()
        entrypoints = (
            ROOT / "README.md",
            ROOT / "START_HERE.md",
            ROOT / "AGENTS.md",
            ROOT / "docs/OPERATING_MODEL.md",
            ROOT / "docs/DOCUMENTATION_MAP.md",
            ROOT / "templates/project-operations/AI_WORKFLOW.md",
        )
        combined = "\n".join(path.read_text(encoding="utf-8") for path in entrypoints)
        missing = [
            item["skill_id"]
            for item in registry["skills"]
            if item["skill_id"] not in combined
        ]
        self.assertEqual(missing, [], f"Active skills missing from entrypoint routing: {missing}")


if __name__ == "__main__":
    unittest.main()
