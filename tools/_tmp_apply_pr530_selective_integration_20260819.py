from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "origin/feat/gpt-first-notion-poc-retirement-20260819"


def old_text(path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{OLD}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(f"cannot read {path} from #530 branch: {proc.stderr}")
    return proc.stdout


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


# 1. Unique retirement policy, narrowed so specialist validation tools are not
#    confused with retired project-management/local visual surfaces.
retirement = '''# 폐기 프로젝트 작업면 흡수·제거 정책

이 문서는 더 이상 기본 프로젝트 작업면으로 사용하지 않는 **프로젝트 관리용 user-facing local/HTML/visual surface, Figma, Google Sheets**를 마지막으로 감사하고 고유 정보만 현행 owner로 옮긴 뒤 active routing에서 제거하는 방법을 정의한다.

## Machine contract

```text
DEPRECATED_PROJECT_SURFACE_ABSORB_THEN_REMOVE
PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED
EXTERNAL_HTML_WORKSPACE_RETIRED
GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL
FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY
QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED
GIT_HISTORY_IS_ROLLBACK_NOT_ACTIVE_CANON
NO_DEFAULT_READ_OF_RETIRED_SURFACE
```

## 1. 기본 작업면

```text
GPT
→ planning / research / review

Notion
→ human-facing Project Home / visual / asset / flow / confirmed human tables

GitHub repository
→ structured data / code / scene / resource / tracked assets / tests / runtime evidence

Codex
→ optional implementation/runtime executor when actually useful
```

프로젝트 기획·자산·UX·정본을 관리하기 위해 새 localhost/browser/desktop app 또는 standalone HTML dashboard를 기본 작업면으로 만들지 않는다.

## 2. 폐기 대상

### `PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED`

과거의 Tool Hub, Expression/Sprite 계열 프로젝트 관리·시각 작업면처럼 Notion/Repository로 대체된 user-facing local management surface는 신규 기본 경로가 아니다. 고유 capability가 남아 있는지 한 번 감사하고 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다.

### `EXTERNAL_HTML_WORKSPACE_RETIRED`

독립 HTML dashboard/catalog/기획 UI를 프로젝트 정본·기본 discovery surface로 유지하지 않는다. 단, 실제 game/runtime web asset, 문서 빌드 derived artifact, test fixture, 배포 산출물은 consumer가 다르므로 자동 삭제 대상이 아니다.

### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`

Google Sheets는 신규 기획·승인·상태관리의 입력면이 아니다.

```text
legacy Sheet
→ UNIQUE / DUPLICATE / OBSOLETE
→ UNIQUE human-facing meaning → exact Project Notion owner
→ UNIQUE structured/runtime meaning → repository owner
→ provenance / source locator 보존
→ destination readback
→ active consumer/reference count 확인
→ migrated unique material = 0
→ active Sheet routing/template/reference 제거
→ archive/trash/delete decision
```

고유 정보 여부를 확인하지 못하면 `BLOCKED_UNVERIFIED`이고 먼저 삭제하지 않는다.

### `FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY`

Figma는 신규 active visual workspace가 아니다. 과거 링크/asset에 UNIQUE provenance가 있으면 현재 Project Notion/Repository owner로 이관·readback한 뒤 active reference를 제거한다.

## 3. QA Evidence Studio는 폐기 프로젝트 작업면과 다르다

`QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED`

QA Evidence Studio는 프로젝트 기획·정본·Visual workspace가 아니라 **실제 PC 빌드의 체크리스트·화면 증거·PASS/FAIL/BLOCKED/NOT_RUN 판정을 exact Git commit에 묶는 specialist validation utility**다.

따라서 다음 조건을 유지하는 동안 retirement 대상에 포함하지 않는다.

- repository 안에 실제 implementation과 automated contract tests가 존재
- 프로젝트 정본/asset/runtime를 자동 수정하지 않음
- evidence ceiling을 넘는 PASS를 만들지 않음
- 외부 AI/API나 별도 유료 서비스가 필요 없음
- 실제 validation consumer가 존재

향후 이 조건이 사라지거나 repository-native/GitHub artifact만으로 동일 기능을 더 단순하게 완전히 대체할 수 있다는 검증된 증거가 생기면 그때 별도 retirement review를 수행한다.

## 4. 흡수 기준

흡수 가능:
- 현재 승인 결정과 충돌하지 않는 UNIQUE 기획 의미
- 다른 곳에 없는 provenance
- 재사용 가능한 workflow 원리
- evidence vocabulary / fail-closed rule
- 실제 소비 중인 schema/contract/test 원리

흡수 금지:
- 이미 Notion/repository에 있는 중복 표현
- superseded/rejected 결정
- tool-specific layout/port/session metadata
- 폐기 프로그램에만 필요한 helper state
- 과거 임시 snapshot

## 5. 삭제 Gate

```text
inventory exact surface
→ identify consumers
→ UNIQUE / DUPLICATE / OBSOLETE
→ migrate UNIQUE
→ destination readback
→ replace active references/tests
→ adversarial review
→ remove active surface
→ regression
→ exact-head PR gate
→ merge
→ postmerge search confirms active consumer/reference = 0
```

Git history는 rollback/audit history이지 active canon이 아니다. 역사 조사 필요성이 없는 한 삭제된 surface를 매 작업마다 다시 후보로 올리지 않는다.

## 6. 비용

현재 기본 유료 플랜은 `GPT_PRO` 하나다. Notion은 Free 범위를 먼저 사용한다. 추가 유료 기능은 실제 blocker·무료 대안·비용·장기 효과를 비교한 뒤 사용자 명시 승인이 있어야 한다.

## 7. 완료 판정

```yaml
retired_surface:
  unique_material_absorbed: true | false
  notion_readback: PASS | BLOCKED | NOT_APPLICABLE
  repository_readback: PASS | BLOCKED | NOT_APPLICABLE
  active_references_remaining: []
  files_removed: []
  retained_specialist_utilities: []
  rollback: Git history
  result: REMOVED | BLOCKED_UNVERIFIED | PARTIAL_RETIREMENT
```

`PARTIAL_RETIREMENT`에서 완료를 주장하지 않는다.
'''
write("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md", retirement)

# 2. Reuse #530's good planning rewrite, but reconcile it to current canonical
#    workflow names, current single-chat PR policy, and self-contained Home.
planning = old_text("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
planning = planning.replace(
    "프로젝트 기본 역할은 `docs/GPT_FIRST_PROJECT_WORKFLOW.md`, 승인 결정 동기화는",
    "프로젝트 기본 역할은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`와 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, 승인 결정 동기화는",
    1,
)
planning = planning.replace(
    "→ same-goal open/recent PRs read-only classification",
    "→ same-goal open/recent PR backlog classification (`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`)",
)
planning = planning.replace(
    "→ exact Project Notion Home and relevant filtered surfaces",
    "→ exact Project Notion Home and relevant filtered surfaces (`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`)",
)
planning = planning.replace(
    "Google Sheets\n→ RETIRED_MIGRATION_ONLY\n→ GOOGLE_SHEETS_MIGRATE_THEN_REMOVE",
    "Google Sheets\n→ `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`",
)
planning = planning.replace("GOOGLE_SHEETS_MIGRATE_THEN_REMOVE", "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL")
# Explicitly tie to the merged Home policy.
if "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN" not in planning.split("## 2. 내용 보존")[0]:
    planning = planning.replace(
        "독립 HTML dashboard/catalog와 user-facing localhost project apps도 새 기획 surface가 아니다.",
        "독립 HTML dashboard/catalog와 프로젝트 관리용 user-facing localhost apps도 새 기획 surface가 아니다. Project Home은 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`에 따라 핵심 방향·Core Loop·시스템·UX/Visual·구현·검증·blocker를 본문에서 직접 설명한다.",
        1,
    )
# Current PR policy: open state is not automatic read-only ownership.
planning = planning.replace(
    "same-goal open/recent PRs read-only classification",
    "same-goal open/recent PR backlog classification",
)
write("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md", planning)

# 3. Workspace authority schema v3 from current v2, without duplicate GPT-first canon.
workspace_path = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
workspace = json.loads(workspace_path.read_text(encoding="utf-8"))
workspace["schema_version"] = 3
workspace["workflow_policy"] = "docs/GPT_CODEX_WORKFLOW_POLICY.md"
workspace["planning_owner"] = "GPT_FIRST_PLANNING_AND_REVIEW"
workspace["final_review_owner"] = "GPT_PRIMARY_REVIEWER"
workspace["codex_role"] = "OPTIONAL_CODEX_EXECUTOR"
workspace["visual_poc_gate"] = "VISUALIZED_POC_BEFORE_DEMO_TEST"
workspace["human_home_policy"] = "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN"
workspace["human_home_policy_path"] = "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md"
workspace["retirement_policy"] = "docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md"
workspace["project_management_local_surface"] = "RETIRED"
workspace["html_project_surface"] = "RETIRED"
workspace["google_sheets"] = "MIGRATION_ONLY_UNTIL_REMOVAL"
workspace["figma"] = "DEPRECATED_NOT_ACTIVE_AUTHORITY"
workspace["qa_evidence_studio"] = "QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED"
workspace["default_paid_plans"] = ["GPT_PRO"]
workspace["notion_paid"] = "ON_REQUEST_ONLY_AFTER_COST_BENEFIT_EVIDENCE"
workspace["human_home_required_sections"] = [
    "PROJECT_DEFINITION_AND_VALUE",
    "CONFIRMED_DIRECTION_AND_PROTECTED_ELEMENTS",
    "CORE_LOOP_AND_FLOW",
    "CORE_SYSTEMS",
    "UX_UI_VISUAL_DIRECTION",
    "IMPLEMENTATION_STATUS",
    "VALIDATION_EVIDENCE_CEILING",
    "BLOCKERS_AND_NEXT_WORK",
    "IMPORTANT_DECISIONS",
    "RISKS_AND_REVISIT_CONDITIONS",
]
# Replace stale Google-Sheets-only invariant if present, append new invariants once.
workspace["invariants"] = [
    item for item in workspace.get("invariants", [])
    if "Google Sheets" not in item and "Business-only query_data_sources" not in item
]
for invariant in (
    "The default Notion workflow stays within ZERO_INCREMENTAL_COST and must not require paid-only Notion features; Project-filtered views plus search/fetch and destination readback are the baseline fallback.",
    "GPT is the default planning/review owner; Codex is optional and used only when actual repository/runtime execution benefits from it.",
    "When visuals materially affect PoC/demo judgment, representative UX/UI states and approved visual inputs are reviewed in Notion before implementation and runtime validation remains separate.",
    "Project Home is self-contained for core human understanding; child pages are drilldown/evidence, not a substitute for the Home explanation.",
    "Project-management local/HTML surfaces, Figma, and Google Sheets are retired or migration-only; QA Evidence Studio remains a specialist validation utility while its tested evidence role remains unique and useful.",
):
    if invariant not in workspace["invariants"]:
        workspace["invariants"].append(invariant)
workspace_path.write_text(json.dumps(workspace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 4. Retire HTML dashboard Skill from active routing; keep a compatibility locator.
dashboard = old_text("skills/building-project-visual-dashboards/SKILL.md")
dashboard = dashboard.replace(
    "→ reviewing-and-validating-project-changes\n→ REPOSITORY_NATIVE_QA_EVIDENCE",
    "→ reviewing-and-validating-project-changes\n→ QA Evidence Studio when specialist PC visual evidence capture is actually useful",
)
dashboard = dashboard.replace(
    "기존 HTML surface의 고유 데이터 이관·삭제는 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`를 따른다.",
    "기존 HTML surface의 고유 데이터 이관·삭제는 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`를 따른다. QA Evidence Studio는 이 HTML project-management surface와 다른 specialist validation utility다.",
)
write("skills/building-project-visual-dashboards/SKILL.md", dashboard)

# Add a local learning record for the disposition.
log_path = ROOT / "skills/building-project-visual-dashboards/LEARNING_LOG.md"
existing_log = log_path.read_text(encoding="utf-8") if log_path.is_file() else "# Learning Log\n"
entry_marker = "2026-08-19 · retire HTML dashboard routing, retain QA validation"
if entry_marker not in existing_log:
    existing_log = existing_log.rstrip() + f'''\n\n## {entry_marker}\n\n- standalone HTML project dashboard는 Notion Project Home/Visual Map으로 대체되어 active routing 가치가 없어졌다.\n- QA Evidence Studio는 project-management dashboard가 아니라 tested specialist validation utility이므로 같은 retirement로 삭제하지 않는다.\n- disposition: `REMOVAL_CANDIDATE` compatibility locator until material consumer count reaches zero.\n- reuse_scope: BASE_PROMOTION_CANDIDATE\n'''
write("skills/building-project-visual-dashboards/LEARNING_LOG.md", existing_log)

# 5. Registry normalization.
registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
rows = {row["skill_id"]: row for row in registry["skills"]}
stale_tags = {
    "google-sheets-sync",
    "project-sheet-semantic-tabs",
    "project-sheet-workbook",
    "project-gdd-sheet",
    "gdd-workspace",
    "proposed-sheet-change",
}
replacements = {
    "managing-project-intake-and-work-contract": {
        "add_tags": ["notion-project-workspace", "project-home", "legacy-sheet-migration"],
        "use_when": "새 요청과 중요 기획 질문을 라우팅할 때 최신 main·CURRENT_CONFIRMED_DECISIONS·분야 정본·동일 Goal의 open/recent PR backlog와 정확한 Project Notion Home을 비교하고 기술 기본값과 사용자 결정 사항을 분리해 실행 계약으로 만든다. Google Sheets는 UNIQUE 미이관 정보가 있는 migration scope에서만 읽는다.",
        "review": ["main·PR·Project Notion 사전 대조 누락", "Notion/repository sync 누락", "legacy Sheet를 active workspace로 되살림"],
    },
    "managing-game-project-operating-system": {
        "add_tags": ["notion-project-workspace", "project-home", "legacy-sheet-migration"],
        "use_when": "프로젝트 운영체계를 설치·감사·마이그레이션·검증하면서 CURRENT_CONFIRMED_DECISIONS, open/recent PR backlog, 분야 정본, GitHub main과 정확한 Project Notion Home의 결정·구현·human-facing sync를 복원한다. Google Sheets는 migration-only legacy source다.",
        "review": ["Project Notion Home readback 누락", "repository/human-facing authority drift", "legacy Sheet active authority 부활"],
    },
    "managing-design-documents": {
        "add_tags": ["notion-project-workspace", "project-home", "legacy-sheet-migration"],
        "use_when": "등록된 기획 책임 원본을 작성·갱신·재구조화하고 발행 정책에 따라 파생본을 검수하며, 질문 전 기존 Decision·open/recent PR backlog·Project Notion을 대조하고 승인 결정을 repository 정본과 필요한 Notion human-facing Home/detail에 동기화한다. Google Sheets는 migration-only source다.",
        "review": ["Notion/repository 결정 sync 누락", "Project Home human-facing 설명 누락", "legacy Sheet active authority 부활"],
    },
}
for skill_id, config in replacements.items():
    row = rows[skill_id]
    row["trigger_tags"] = [tag for tag in row.get("trigger_tags", []) if tag not in stale_tags]
    for tag in config["add_tags"]:
        if tag not in row["trigger_tags"]:
            row["trigger_tags"].append(tag)
    row["use_when"] = [config["use_when"]]
    row["review_triggers"] = [
        trigger for trigger in row.get("review_triggers", [])
        if "Google Sheets" not in trigger and "Sheet" not in trigger and "SYNCED" not in trigger
    ]
    for trigger in config["review"]:
        if trigger not in row["review_triggers"]:
            row["review_triggers"].append(trigger)
    row["last_reviewed_at"] = "2026-08-19"
    row["last_reviewed_commit"] = "PENDING_PR530_SELECTIVE_INTEGRATION"

rows["building-project-visual-dashboards"]["status"] = "REMOVAL_CANDIDATE"
rows["building-project-visual-dashboards"]["use_when"] = [
    "과거 consumer가 이 Skill ID를 참조할 때 replacement owner를 찾기 위한 compatibility locator로만 사용한다. 새 standalone HTML project dashboard는 만들지 않는다."
]
rows["building-project-visual-dashboards"]["do_not_use_when"] = [
    "새 프로젝트 계획·시각·상태 작업에는 Notion Project Home/Visual Map과 repository owner를 사용한다."
]
rows["building-project-visual-dashboards"]["last_reviewed_at"] = "2026-08-19"
rows["building-project-visual-dashboards"]["last_reviewed_commit"] = "PENDING_PR530_SELECTIVE_INTEGRATION"
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

# 6. Partition active-Skill owner map follows Registry ACTIVE state.
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
if "building-project-visual-dashboards" in p05["owned_skill_ids"]:
    p05["owned_skill_ids"].remove("building-project-visual-dashboards")
# Keep the package path under P05 for compatibility cleanup ownership.
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 7. Permanent CI actually consumes the new focused regression.
workflow_path = ROOT / ".github/workflows/base-partition-contract.yml"
workflow = workflow_path.read_text(encoding="utf-8")
path_line = "      - 'tests/test_pr530_selective_integration_contract.py'"
if path_line not in workflow:
    anchor = "      - 'tests/test_human_home_self_contained_contract.py'"
    workflow = workflow.replace(anchor, anchor + "\n" + path_line, 1)
    # second push block occurrence
    workflow = workflow.replace(anchor, anchor + "\n" + path_line, 1)
run_anchor = "          tests.test_human_home_self_contained_contract"
if "tests.test_pr530_selective_integration_contract" not in workflow:
    workflow = workflow.replace(
        run_anchor,
        run_anchor + "\n          tests.test_pr530_selective_integration_contract",
        1,
    )
compile_anchor = "          tests/test_human_home_self_contained_contract.py"
if "tests/test_pr530_selective_integration_contract.py" not in workflow.split("Run partition and source-learning")[0]:
    workflow = workflow.replace(
        compile_anchor,
        compile_anchor + "\n          tests/test_pr530_selective_integration_contract.py",
        1,
    )
workflow_path.write_text(workflow, encoding="utf-8", newline="\n")

print("PR530_SELECTIVE_INTEGRATION_APPLIED")
