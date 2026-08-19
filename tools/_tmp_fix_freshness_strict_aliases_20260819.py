from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


checker_path = "tools/check_canonical_reference_freshness.py"
checker = read(checker_path)
anchor = '''def parse_legacy_aliases(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    aliases: set[str] = set()
    first_cell = re.compile(r"^\\|\\s*(.*?)\\|")
    inline_code = re.compile(r"`([^`]+)`")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = first_cell.match(line)
        if not match:
            continue
        for alias in inline_code.findall(match.group(1)):
            alias = alias.strip()
            if alias:
                aliases.add(alias)
    return aliases
'''
replacement = anchor + '''

def parse_strict_legacy_skill_ids(path: Path) -> set[str]:
    """Return only aliases explicitly marked as stale execution Skill IDs.

    The alias table deliberately mixes historical Skill IDs, user-facing compatibility
    names, and current Skill Modes. Bare execution-entrypoint rejection applies only
    to the explicit fourth-column strict IDs; deleted-path detection still uses every
    first-cell alias.
    """
    if not path.is_file():
        return set()
    strict_ids: set[str] = set()
    row = re.compile(r"^\\|\\s*(.*?)\\|\\s*(.*?)\\|\\s*(.*?)\\|\\s*(.*?)\\|\\s*$")
    inline_code = re.compile(r"`([^`]+)`")
    saw_four_column_data = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = row.match(line)
        if not match:
            continue
        fourth = match.group(4).strip()
        if fourth.startswith("---") or "엄격 실행 ID" in fourth:
            continue
        saw_four_column_data = True
        for alias in inline_code.findall(fourth):
            alias = alias.strip()
            if alias:
                strict_ids.add(alias)
    if saw_four_column_data:
        return strict_ids
    return parse_legacy_aliases(path)
'''
if "def parse_strict_legacy_skill_ids" not in checker:
    if anchor not in checker:
        raise SystemExit("parse_legacy_aliases anchor missing")
    checker = checker.replace(anchor, replacement, 1)

old_sig = '''def check_legacy_references(
    root: Path,
    files: list[Path],
    aliases: set[str],
    allowed_globs: list[str],
    strict_id_globs: list[str],
) -> list[str]:'''
new_sig = '''def check_legacy_references(
    root: Path,
    files: list[Path],
    aliases: set[str],
    strict_aliases: set[str],
    allowed_globs: list[str],
    strict_id_globs: list[str],
) -> list[str]:'''
if old_sig in checker:
    checker = checker.replace(old_sig, new_sig, 1)
checker = checker.replace(
    '''        for alias in sorted(aliases):
            old_path = f"skills/{alias}/SKILL.md"
            if old_path in text:
                errors.append(f"Deleted skill path remains in active file: {relative} -> {old_path}")
            if check_bare_id and re.search(
                rf"(?<![a-z0-9-]){re.escape(alias)}(?![a-z0-9-])",
                text,
            ):
                errors.append(f"Legacy skill id remains in execution entrypoint: {relative} -> {alias}")''',
    '''        for alias in sorted(aliases):
            old_path = f"skills/{alias}/SKILL.md"
            if old_path in text:
                errors.append(f"Deleted skill path remains in active file: {relative} -> {old_path}")
        if check_bare_id:
            for alias in sorted(strict_aliases):
                if re.search(
                    rf"(?<![a-z0-9-]){re.escape(alias)}(?![a-z0-9-])",
                    text,
                ):
                    errors.append(f"Legacy skill id remains in execution entrypoint: {relative} -> {alias}")''',
    1,
)
checker = checker.replace(
    '''    aliases_path = str(config.get("legacy_aliases_path", "")).strip()
    aliases = parse_legacy_aliases(root / aliases_path) if aliases_path else set()

    errors: list[str] = []
    errors.extend(check_legacy_references(
        root,
        files,
        aliases,
        [str(item) for item in config.get("allowed_legacy_globs", [])],
        [str(item) for item in config.get("strict_legacy_id_globs", [])],
    ))''',
    '''    aliases_path = str(config.get("legacy_aliases_path", "")).strip()
    aliases = parse_legacy_aliases(root / aliases_path) if aliases_path else set()
    strict_aliases = parse_strict_legacy_skill_ids(root / aliases_path) if aliases_path else set()

    errors: list[str] = []
    errors.extend(check_legacy_references(
        root,
        files,
        aliases,
        strict_aliases,
        [str(item) for item in config.get("allowed_legacy_globs", [])],
        [str(item) for item in config.get("strict_legacy_id_globs", [])],
    ))''',
    1,
)
checker = checker.replace(
    '    print(f"- legacy_aliases: {len(aliases)}")',
    '    print(f"- legacy_aliases: {len(aliases)}")\n    print(f"- strict_legacy_skill_ids: {len(strict_aliases)}")',
    1,
)
write(checker_path, checker)

ref_path = "tests/test_reference_freshness.py"
ref = read(ref_path)
ref = ref.replace(
    '"| 이전 Skill ID | 새 Skill ID | Mode |\\n"\n            "|---|---|---|\\n"\n            "| `old-skill` | `new-skill` | `run` |\\n",',
    '"| 이전 Skill ID·호환 이름 | 새 Skill ID | Mode | 엄격 실행 ID |\\n"\n            "|---|---|---|---|\\n"\n            "| `old-skill` | `new-skill` | `run` | `old-skill` |\\n",',
    1,
)
main_marker = '\n\nif __name__ == "__main__":'
if "test_strict_alias_column_distinguishes_compatibility_name_from_legacy_id" not in ref:
    method = r'''

    def test_strict_alias_column_distinguishes_compatibility_name_from_legacy_id(self) -> None:
        aliases = self.root / "skills/LEGACY_SKILL_ALIASES.md"
        aliases.write_text(
            "| 이전 Skill ID·호환 이름 | 새 Skill ID | Mode | 엄격 실행 ID |\n"
            "|---|---|---|---|\n"
            "| `friendly label`, `old-two`, `old-three` | `new-skill` | `run` | `old-two`, `old-three` |\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text(
            "See docs/OPERATING_MODEL.md and friendly label.\n",
            encoding="utf-8",
        )
        allowed = self._run()
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        (self.root / "README.md").write_text(
            "See docs/OPERATING_MODEL.md and old-three.\n",
            encoding="utf-8",
        )
        blocked = self._run()
        self.assertNotEqual(0, blocked.returncode)
        self.assertIn("Legacy skill id remains in execution entrypoint", blocked.stdout)

    def test_parse_strict_legacy_skill_ids_reads_nonfirst_strict_alias(self) -> None:
        from tempfile import TemporaryDirectory
        from tools.check_canonical_reference_freshness import parse_strict_legacy_skill_ids

        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "aliases.md"
            path.write_text(
                "| 이전 Skill ID·호환 이름 | 새 Skill ID | Mode | 엄격 실행 ID |\n"
                "|---|---|---|---|\n"
                "| `label`, `old-two`, `old-three` | `new` | `run` | `old-two`, `old-three` |\n",
                encoding="utf-8",
            )
            self.assertEqual({"old-two", "old-three"}, parse_strict_legacy_skill_ids(path))
'''
    if main_marker not in ref:
        raise SystemExit("reference freshness main marker missing")
    ref = ref.replace(main_marker, method + main_marker, 1)
write(ref_path, ref)

gpt_test_path = "tests/test_gpt_codex_workflow_contract.py"
gpt_test = read(gpt_test_path)
if "test_adversarial_registry_uses_workspace_neutral_authority_drift_terms" not in gpt_test:
    method = r'''

    def test_adversarial_registry_uses_workspace_neutral_authority_drift_terms(self) -> None:
        registry_text = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        self.assertNotIn("google-sheets-drift", registry_text)
        self.assertNotIn("GitHub·Google Sheets 불일치", registry_text)
        self.assertIn("configured-workspace-authority-drift", registry_text)
        self.assertIn("configured workspace/repository authority 불일치", registry_text)
'''
    if main_marker not in gpt_test:
        raise SystemExit("gpt codex test main marker missing")
    gpt_test = gpt_test.replace(main_marker, method + main_marker, 1)
write(gpt_test_path, gpt_test)

# Legacy alias table changes are semantically owned by the freshness parser/test,
# so require that actual consumer instead of an unrelated consolidated-reference test.
config_path = ROOT / ".github/reference-freshness.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
for rule in config.get("coupled_change_rules", []):
    if rule.get("name") == "legacy-alias-test-sync":
        rule["require_all_changed"] = ["tests/test_reference_freshness.py"]
        rule["require_any_changed"] = []
        rule["semantic_note"] = "Legacy alias table strict-ID semantics are parsed and regression-tested by tests/test_reference_freshness.py."
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("STRICT_ALIAS_AND_REGISTRY_REGRESSIONS_FIXED")
