import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_machine_workspace_authority_is_notion_and_project_scoped() -> None:
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert contract["schema_version"] == 3
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


def test_gpt_is_primary_planning_review_owner_and_codex_is_optional_sub_executor() -> None:
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert contract["planning_owner"] == "GPT_PRIMARY_PLANNING_REVIEW"
    assert contract["final_review_owner"] == "GPT_FINAL_REVIEW_AUTHORITY"
    assert contract["codex_role"] == "CODEX_OPTIONAL_SUB_EXECUTOR"
    assert contract["visual_poc_gate"] == "NOTION_VISUAL_CHECKPOINT_BEFORE_POC"
    assert contract["workflow_policy"] == "docs/GPT_FIRST_PROJECT_WORKFLOW.md"


def test_managing_design_documents_uses_notion_for_human_canon_and_repo_for_structured_canon() -> None:
    skill = text("skills/managing-design-documents/SKILL.md")
    for token in (
        "NOTION_HUMAN_FACING_CANON",
        "REPOSITORY_STRUCTURED_CANON",
        "PROPOSED_NOTION_CHANGE",
        "SYNC_BEFORE_IMPLEMENTATION",
    ):
        assert token in skill
    assert "USER_FACING_GDD_WORKSPACE" not in skill
    assert "프로젝트 Google Sheets까지 같은 승인 단위에서 동기화" not in skill


def test_confirmed_decision_sync_uses_notion_human_surface_and_repository_structured_truth() -> None:
    policy = text("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
    for token in (
        "DOMAIN_SPLIT_CANON",
        "NOTION_HUMAN_FACING_CANON",
        "REPOSITORY_STRUCTURED_CANON",
        "PROPOSED_NOTION_CHANGE",
        "SYNC_BEFORE_IMPLEMENTATION",
        "NOTION_UPDATED",
    ):
        assert token in policy
    assert "USER_FACING_GDD_WORKSPACE" not in policy
    assert "Google Sheets가 갱신되고 재조회 결과가 일치했다" not in policy


def test_active_visual_policy_absorbs_tool_principles_without_deprecated_authority() -> None:
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


def test_deprecated_user_facing_visual_and_qa_surfaces_are_absent() -> None:
    deleted = (
        "tools/figma-bridge",
        "tools/expression-studio",
        "tools/sprite-animation-studio",
        "tools/tool-hub",
        "tools/qa-evidence-studio",
        "docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json",
        "docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json",
        "docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json",
        "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md",
        "templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md",
        "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md",
    )
    for path in deleted:
        assert not (ROOT / path).exists(), path


def test_repository_native_qa_evidence_absorbs_the_useful_fail_closed_rules() -> None:
    retirement = text("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md")
    for token in (
        "REPOSITORY_NATIVE_QA_EVIDENCE",
        "PASS / FAIL / BLOCKED / NOT_RUN",
        "exact Git commit/PR head",
        "DEFERRED_NOT_CONNECTED",
        "screenshot/video/log",
    ):
        assert token in retirement


def test_google_sheets_is_migration_only_then_removed() -> None:
    policy = text("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert "RETIRED_MIGRATION_ONLY" in policy
    assert "GOOGLE_SHEETS_MIGRATE_THEN_REMOVE" in policy
    assert contract["google_sheets"] == "MIGRATION_ONLY_THEN_REMOVE"
    assert "FIGMA_DEFAULT_VISUAL_WORKSPACE" not in policy


def test_paid_plan_contract_is_gpt_pro_only_and_notion_paid_is_opt_in() -> None:
    agents = text("AGENTS.md")
    contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
    assert "CURRENT_PAID_PLANS: GPT_PRO" in agents
    assert "PAID_PLAN_COUNT: 1" in agents
    assert "CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO" not in agents
    assert contract["default_paid_plans"] == ["GPT_PRO"]
    assert contract["notion_paid"] == "ON_REQUEST_ONLY_AFTER_COST_BENEFIT_EVIDENCE"
