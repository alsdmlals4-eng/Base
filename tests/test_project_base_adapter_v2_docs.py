from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_v2_migration_is_discoverable_and_keeps_v1_audit_compatible() -> None:
    migration = (ROOT / "docs" / "operations" / "PROJECT_BASE_ADAPTER_V2_MIGRATION.md").read_text(encoding="utf-8")
    shared = (ROOT / "docs" / "BASE_SHARED_SKILL_ADAPTER_CONTRACT.md").read_text(encoding="utf-8")
    combined = "\n".join((ROOT.joinpath(name).read_text(encoding="utf-8") for name in ("README.md", "START_HERE.md", "docs/DOCUMENTATION_MAP.md")))

    assert "IDENTITY_MIGRATION_REQUIRED" in migration
    assert "must not overwrite" in migration
    assert "never executed" in shared
    assert "PROJECT_BASE_ADAPTER_V2_MIGRATION.md" in combined


def test_v2_tool_requires_explicit_identity_and_non_overwriting_output() -> None:
    tool = (ROOT / "tools" / "migrate_project_base_adapter_v2.py").read_text(encoding="utf-8")

    assert 'parser.add_argument("--project-id", required=True)' in tool
    assert "source == target" in tool
    assert "migrate_adapter_v1_to_v2" in tool
