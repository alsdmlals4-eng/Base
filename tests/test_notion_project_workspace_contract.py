import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_machine_workspace_authority_is_notion_and_project_scoped() -> None:
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert contract["schema_version"] == 1
    assert contract["project_workspace"] == "NOTION_DEFAULT_PROJECT_WORKSPACE"
    assert contract["project_relation"] == "PROJECT_RELATION_REQUIRED"
    assert contract["work_master"] == "WORK_MASTER"
    assert contract["asset_master"] == "ASSET_KNOWLEDGE_MASTER"
    assert contract["visual_map"] == "VISUAL_MAP_DERIVED"
    assert contract["runtime_truth"] == "REPOSITORY_RUNTIME_TRUTH"


def test_canon_authority_is_split_by_human_visual_and_structured_runtime_domains() -> None:
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert contract["authority_model"] == "DOMAIN_SPLIT_CANON"
    assert contract["human_facing_canon"] == "NOTION_HUMAN_FACING_CANON"
    assert contract["repository_structured_canon"] == "REPOSITORY_STRUCTURED_CANON"
    assert {
        "PROJECT_OVERVIEW",
        "VISUAL_DIRECTION",
        "VISUAL_ASSET_CATALOG",
        "BUDGET_TABLE",
        "TIER_TABLE",
        "HUMAN_EDITABLE_FLOW_MAP",
        "STORYBOARD",
    }.issubset(set(contract["notion_priority_domains"]))
    assert {
        "MARKDOWN_SPEC",
        "JSON_DATA",
        "GAME_DATA",
        "CODE",
        "SCENE",
        "RESOURCE",
        "TEST",
        "RUNTIME_EVIDENCE",
    }.issubset(set(contract["repository_priority_domains"]))
    assert contract["cross_domain_sync"] == "SYNC_BEFORE_IMPLEMENTATION"


def test_active_visual_policy_absorbs_tool_principles_without_figma_authority() -> None:
    policy = text("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
    required = (
        "NOTION_DEFAULT_PROJECT_WORKSPACE",
        "PROJECT_RELATION_REQUIRED",
        "ASSET_KNOWLEDGE_MASTER",
        "VISUAL_MAP_DERIVED",
        "Record Type",
        "ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE",
        "source provenance",
        "version",
        "readback",
        "human",
        "AI / System",
    )
    for token in required:
        assert token in policy
    assert "FIGMA_DEFAULT_VISUAL_WORKSPACE" not in policy
    assert "Figma Bridge" not in policy


def test_deprecated_visual_execution_surfaces_are_absent() -> None:
    deleted = (
        "tools/figma-bridge",
        "tools/expression-studio",
        "tools/sprite-animation-studio",
        "tools/tool-hub",
        "docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json",
        "docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json",
        "docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json",
        "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md",
        "templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md",
        "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md",
    )
    for path in deleted:
        assert not (ROOT / path).exists(), path


def test_qa_evidence_studio_remains_independent_runtime_evidence_tool() -> None:
    readme = text("tools/qa-evidence-studio/README.md")
    assert "QA Evidence Studio" in readme
    assert "DEVELOPER_OWNER" in readme
    assert "DEFERRED_NOT_CONNECTED" in readme
    assert "Figma" not in readme


def test_google_sheets_is_compatibility_only_not_default_workspace() -> None:
    policy = text("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
    assert "COMPATIBILITY_ONLY" in policy
    assert "NOTION_DEFAULT_PROJECT_WORKSPACE" in policy
    assert "FIGMA_DEFAULT_VISUAL_WORKSPACE" not in policy


def test_active_paid_plan_contract_does_not_require_figma() -> None:
    agents = text("AGENTS.md")
    assert "CURRENT_PAID_PLANS: GPT_PRO" in agents
    assert "PAID_PLAN_COUNT: 1" in agents
    assert "CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO" not in agents
