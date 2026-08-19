from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write(path, text)


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise SystemExit(f"missing anchor in {path}: {old[:100]!r}")
    text = text.replace(old, new, 1)
    write(path, text)


# ---------------------------------------------------------------------------
# Partition manifest: one coordinator chat, semantic ownership, current CP0 fixes.
# ---------------------------------------------------------------------------
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["version"] = "2.0.0"
manifest["selected_strategy"] = "ONE_BASE_STABLE_PARTITIONS_SEQUENTIAL_COORDINATOR"
manifest["ownership_policy"] = "PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER"
manifest["independent_workstream_policy"] = "ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED"
manifest["unassigned_path_policy"] = "COORDINATOR_REVIEW_WITH_SEMANTIC_OWNER_ATTRIBUTION"
manifest["cross_part_protocol"] = "CROSS_PART_CHANGE_DEFAULT_REQUEST_ONLY_FOR_REAL_BLOCKERS"
manifest["coordinator_execution"] = {
    "policy": "SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS",
    "chat": "CURRENT_COORDINATOR_CHAT",
    "part_order": [f"P{i:02d}" for i in range(1, 10)],
    "required_new_worker_chats": 0,
    "one_part_checkpoint_at_a_time": True,
    "repin_latest_main_between_parts": True,
    "default_pr_model": "ONE_PART_PR_AT_A_TIME",
    "cross_part_fix_policy": "FIX_VALIDATED_FINDINGS_IN_CURRENT_COORDINATOR_WORK_WITH_SEMANTIC_ATTRIBUTION",
    "active_independent_workstreams": "READ_ONLY_UNLESS_EXPLICIT_USER_TAKEOVER",
}
manifest["review_contract"]["FULL_LOOP_IS_NOT_A_REVIEW_LENS"] = True
manifest["control_plane"]["write_authority"] = "COORDINATOR_OR_INTEGRATION"
manifest["validation_evidence_policy"] = {
    "contract": "TEST_FILE_EXISTENCE_IS_NOT_EXECUTION_EVIDENCE",
    "required_for_ci_claim": "NAME_ACTUAL_CONSUMING_WORKFLOW_OR_COMMAND",
    "main_advance_policy": "REVALIDATE_MERGE_READINESS_AGAINST_CURRENT_MAIN",
}

iso = manifest.get("collaboration_isolation", {})
iso["worker_model"] = "SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS"
gh = iso.get("github", {})
gh["one_branch_per_part"] = True
gh["one_pr_per_part"] = True
gh["branch_template"] = "opt/base-part-{PART_ID}-{slug}"
gh["other_part_branches_prs"] = "SEMANTIC_OWNER_REFERENCE_ONLY_NOT_WRITE_BARRIER"
gh["control_plane_write"] = "COORDINATOR_ALLOWED_WITH_ATTRIBUTION"
gh["active_independent_workstreams"] = "READ_ONLY_UNLESS_EXPLICIT_USER_TAKEOVER"
iso["github"] = gh
notion = iso.get("notion", {})
notion["hub_write"] = "COORDINATOR"
notion["shared_visual_write"] = "COORDINATOR"
notion["part_page_write"] = "COORDINATOR_CURRENT_OR_AFFECTED_PART"
notion["other_part_pages"] = "COORDINATOR_MAY_UPDATE_WHEN_VALIDATED_CHANGE_AFFECTS_PAGE"
notion["cross_part_change"] = "CROSS_PART_CHANGE"
iso["notion"] = notion
manifest["collaboration_isolation"] = iso

for group in manifest.get("parallel_execution_groups", []):
    group["can_run_with_other_groups"] = False
    group["execution_role"] = "REFERENCE_CLUSTER_ONLY_SEQUENTIAL_COORDINATOR_IS_DEFAULT"

for part in manifest["parts"]:
    part["chat_ownership"] = "CURRENT_COORDINATOR_CHAT_SEQUENTIAL_CHECKPOINT"
    part["notion_write_authority"] = "COORDINATOR_CURRENT_OR_AFFECTED_PART"
    if "notion_read_only_pages" in part:
        part["notion_related_pages"] = part.pop("notion_read_only_pages")

p01 = next(p for p in manifest["parts"] if p["part_id"] == "P01")
if "docs/PROJECT_WORKSPACE_AUTHORITY_POLICY.md" in p01["owned_write_paths"]:
    p01["owned_write_paths"].remove("docs/PROJECT_WORKSPACE_AUTHORITY_POLICY.md")
for actual in (
    "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",
    "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md",
):
    if actual not in p01["owned_write_paths"]:
        p01["owned_write_paths"].append(actual)

p02 = next(p for p in manifest["parts"] if p["part_id"] == "P02")
paths = p02["owned_write_paths"]
if "proposals/**" in paths:
    paths[paths.index("proposals/**")] = "[수정제안서]/**"

p07 = next(p for p in manifest["parts"] if p["part_id"] == "P07")
dep = "P01 project-operation evidence templates: templates/project-operations/** (read-only semantic dependency)"
if dep not in p07["read_only_dependencies"]:
    p07["read_only_dependencies"].append(dep)

p09 = next(p for p in manifest["parts"] if p["part_id"] == "P09")
paths = p09["owned_write_paths"]
replacements = {
    "docs/knowledge/writing/**": "docs/knowledge/serial-fiction/**",
    "templates/game-dev-youtube/**": "templates/game-development-youtube/**",
}
for old, new in replacements.items():
    if old in paths:
        paths[paths.index(old)] = new
if "templates/writing/**" in paths:
    paths.remove("templates/writing/**")

integration = manifest.get("integration", {})
integration["worker_chat_count"] = 0
integration["total_new_gpt_chats_after_task_1"] = 0
integration["integration_chat"] = "CURRENT_COORDINATOR_CHAT"
integration["new_integration_chat_count"] = 0
integration["final_confirmation_chat"] = "CURRENT_COORDINATOR_CHAT"
integration["ordered_steps"] = [
    "Run P01 through P09 sequentially in CURRENT_COORDINATOR_CHAT",
    "Repin latest main between Part checkpoints",
    "Fix validated cross-Part/CP0 findings directly when no protected active-workstream blocker exists",
    "Record CROSS_PART_CHANGE semantic attribution",
    "Deduplicate only real CROSS_PART_CHANGE_REQUEST blockers",
    "Rebuild Registry/generated artifacts when affected",
    "Reconcile self-contained Notion Base/Project Homes from merged facts",
    "Run repository-wide regression and required CI",
    "Run at least 5 true full-scope adversarial loops and continue until CLEAN_REVIEW_EXIT",
    "Exact-head merge",
    "Post-merge main and Notion readback",
]
manifest["integration"] = integration
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Context Packs: make the new semantic boundary explicit and remove hard-barrier language.
for path in sorted((ROOT / "docs/operations/base-partitions").glob("P*.md")):
    text = path.read_text(encoding="utf-8")
    contract = (
        "## 현재 실행 계약\n"
        "`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · "
        "`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`\n\n"
        "이 Part는 semantic responsibility / learning / validation checkpoint다. "
        "현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 "
        "다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. "
        "단, 다른 독립 open/draft/ready PR·branch·worktree는 "
        "`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.\n\n"
    )
    if "## 현재 실행 계약" not in text:
        title_end = text.find("\n", text.find("# "))
        text = text[: title_end + 1] + "\n" + contract + text[title_end + 1 :]
    text = re.sub(
        r"## 경계\n.*?(?=\n## 우선 공격 대상)",
        "## 경계\nPart 경계는 수정 금지선이 아니라 semantic owner 지도다. "
        "다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. "
        "다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.\n",
        text,
        flags=re.S,
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------
# AGENTS / long-horizon: make lens-counting explicitly invalid.
# ---------------------------------------------------------------------------
agents_path = "AGENTS.md"
agents = read(agents_path)
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in agents:
    anchor = "- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:**"
    start = agents.find(anchor)
    if start < 0:
        raise SystemExit("AGENTS adversarial anchor missing")
    end = agents.find("\n", start)
    insert = (
        "\n- **`FULL_LOOP_IS_NOT_A_REVIEW_LENS`:** 적대적 검토의 `loop_index` 하나는 관점 하나가 아니라 "
        "현재 상태/정본/실제 구현 readback → 최소 3개 실질 대안/현 선택 재검토 → full-scope attack → critique 검증 → "
        "검증된 finding 수정 → 실행·회귀·reference 검증 → `BETTER_ALTERNATIVE_SEARCH` → `LONG_TERM_PLAN_FIT_RECHECK` → "
        "개선된 전체 상태 재공격을 모두 포함한다. `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 lens를 나눠 센 횟수는 "
        "full loop로 계수하지 않는다. 최소 5회는 이 전체 lifecycle을 5번 반복한다는 뜻이다.\n"
        "- **`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`:** Base P01~P09 최적화는 기본적으로 한 GPT coordinator 채팅에서 "
        "P01→P09 순서로 수행한다. Part ownership은 semantic responsibility이지 write barrier가 아니다. 검증된 cross-Part/CP0 finding은 "
        "`CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 "
        "`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`로 계속 보호한다.\n"
    )
    agents = agents[: end + 1] + insert + agents[end + 1 :]
write(agents_path, agents)

long_path = "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"
long_text = read(long_path)
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in long_text:
    marker = "ADVERSARIAL_REVIEW_UNTIL_CLEAN"
    pos = long_text.find(marker)
    if pos < 0:
        raise SystemExit("long-horizon adversarial anchor missing")
    line_end = long_text.find("\n", pos)
    addition = (
        "\n`FULL_LOOP_IS_NOT_A_REVIEW_LENS`: 회차 번호를 scope/UX/CI/security 같은 서로 다른 lens에 배정하지 않는다. "
        "각 counted loop가 현행/정본/실제 구현, 최소 3개 대안, 전체 attack, critique 검증, 수정, 실행·회귀·reference 검증, "
        "better-alternative search, long-term fit, 전체 결과 재공격을 모두 반복해야 한다.\n"
    )
    long_text = long_text[: line_end + 1] + addition + long_text[line_end + 1 :]
write(long_path, long_text)

# ---------------------------------------------------------------------------
# Adversarial Skill + protocol: true full loop, no lens counting.
# ---------------------------------------------------------------------------
skill_path = "skills/running-adversarial-review-and-refinement/SKILL.md"
skill = read(skill_path)
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in skill:
    anchor = "### `POST_CHANGE_MONITOR_LOOP`"
    if anchor not in skill:
        raise SystemExit("adversarial post-change anchor missing")
    section = r'''### Full loop is not a review lens

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

한 `loop_index`는 scope, UX, CI 같은 **관점 하나가 아니다**. 각 counted loop는 현재 승인 범위 전체를 아래 lifecycle로 처음부터 끝까지 다시 검토한다.

```text
CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK
→ MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK
→ FULL-SCOPE ATTACK
→ VALIDATE CRITIQUE
→ FIX / REFINE VERIFIED FINDINGS
→ EXECUTION / REGRESSION / REFERENCE VERIFICATION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK THE WHOLE RESULTING STATE
```

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`, `Loop 4=long-term`, `Loop 5=review`처럼 서로 다른 lens를 한 번씩 검사한 보고는 **full loop로 계수하지 않는다**. Scope/UX/CI/security/cost/consumer/rollback 같은 lens는 각 full loop 내부의 attack coverage다.

회차마다 대표 finding을 제목으로 강조할 수 있지만 대표 finding이 그 회차의 검토 범위를 뜻하지 않는다. 최소 5회는 위 전체 lifecycle을 최소 5번 실제 반복한다는 뜻이다. finding이 없는 회차도 전체 lifecycle evidence가 있으면 유효하지만, lens 하나만 수행한 회차는 finding 수와 무관하게 무효다.

'''
    skill = skill.replace(anchor, section + anchor, 1)

old_evidence = '''loop_index: 1..N
input_state_or_head:
evidence_delta: []
full_scope_findings: []
validated_findings: []
changes_applied: []
verification: []
better_alternative_result:
long_term_fit:
unresolved: []
output_state_or_head:
clean_exit_candidate: true | false'''
new_evidence = '''loop_index: 1..N
input_state_or_head:
full_scope_coverage:
  current_state_canon_actual_implementation_readback: true | false
  alternatives_rechecked: true | false
  full_scope_attack: true | false
  critique_validated: true | false
  verified_findings_refined: true | false
  verification_rechecked: true | false
  better_alternative_rechecked: true | false
  long_term_fit_rechecked: true | false
  whole_state_re_attacked: true | false
evidence_delta: []
full_scope_findings: []
validated_findings: []
changes_applied: []
verification: []
better_alternative_result:
long_term_fit:
unresolved: []
output_state_or_head:
clean_exit_candidate: true | false'''
if old_evidence not in skill:
    raise SystemExit("adversarial loop evidence block missing")
skill = skill.replace(old_evidence, new_evidence, 1)
write(skill_path, skill)

protocol_path = "skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md"
protocol = read(protocol_path)
if "## Full-loop evidence contract" not in protocol:
    anchor = "## 공격 렌즈"
    if anchor not in protocol:
        raise SystemExit("finding protocol attack anchor missing")
    section = r'''## Full-loop evidence contract

각 counted adversarial loop는 lens 하나가 아니라 전체 lifecycle임을 다음 evidence로 증명한다.

```yaml
loop_index:
full_scope_coverage:
  current_state_canon_actual_implementation_readback: true
  alternatives_rechecked: true
  attack_surfaces_rechecked: []
  critique_validated: true
  fixes_refined_or_no_change_justified: true
  verification_rechecked: true
  better_alternative_rechecked: true
  long_term_fit_rechecked: true
  whole_state_re_attacked: true
representative_findings: []
```

`full_scope_coverage`의 필수 항목이 false이거나 evidence가 없으면 그 회차는 `FULL_LOOP_COUNT_MINIMUM`에 넣지 않는다. `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI` 같은 관점 분할은 이 계약을 충족하지 않는다.

'''
    protocol = protocol.replace(anchor, section + anchor, 1)
protocol = protocol.replace(
    "GitHub `main`과 프로젝트 Google Sheets의 Decision·Commit·대체 관계 불일치.",
    "GitHub `main`과 적용 가능한 Project Notion human-facing state / repository authority의 Decision·Commit·대체 관계 불일치.",
)
protocol = protocol.replace(
    "프로젝트가 Google Sheets를 사용하면 해당 행을 재조회했는가?",
    "적용 가능한 Project Notion human-facing state와 repository authority를 destination readback했는가?",
)
protocol = protocol.replace(
    "필요한 정본·도구·권한·CI·런타임·Sheets 증거가 없어 판정할 수 없다.",
    "필요한 정본·도구·권한·CI·런타임·Notion/repository evidence가 없어 판정할 수 없다.",
)
protocol = protocol.replace(
    "GitHub `main`과 Google Sheets를 재조회해 일치하는가?",
    "GitHub `main`과 적용 가능한 Project Notion/repository authority를 재조회해 일치하는가?",
)
write(protocol_path, protocol)

append_once(
    "skills/running-adversarial-review-and-refinement/LEARNING_LOG.md",
    "2026-08-19 · full loop is not a review lens",
    '''## 2026-08-19 · full loop is not a review lens

- 관찰: 정본은 이미 full-scope review를 요구했지만 실제 완료보고가 `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 lens별 회차로 축약될 수 있었다.
- 교훈: 최소 5회는 서로 다른 관점 5개가 아니라 **동일한 전체 lifecycle을 개선된 상태에 대해 최소 5번 반복**한다는 뜻이어야 한다.
- 반영: `FULL_LOOP_IS_NOT_A_REVIEW_LENS`와 full-scope coverage evidence를 추가하고 lens-only 회차를 계수하지 않는다.
- reuse_scope: BASE_PROMOTION_CANDIDATE
''',
)

# ---------------------------------------------------------------------------
# Human-facing Project Home contract.
# ---------------------------------------------------------------------------
project_os_path = "skills/managing-game-project-operating-system/SKILL.md"
project_os = read(project_os_path)
if "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN" not in project_os:
    anchor = "## HiGodot provider adoption contract"
    if anchor not in project_os:
        raise SystemExit("project OS HiGodot anchor missing")
    section = r'''## Human-facing Project Home contract

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Project Notion Home은 링크 목록이 아니라 사람이 **추가 이동 없이 프로젝트의 핵심을 이해하는 첫 화면**이다. 하위 페이지는 drilldown/evidence/긴 표/asset/log를 위한 상세면이며, 아래 핵심 설명을 대체하지 않는다.

Project Home에는 최소 다음을 직접 보여준다.

1. **프로젝트 한 줄 정의** — 무엇을 만드는 프로젝트인지.
2. **핵심 플레이어/사용자 가치** — 사용자가 무엇을 느끼고 선택하며 왜 계속하는지.
3. **현재 확정 방향** — 유지해야 할 방향과 보호/금지 요소.
4. **Core Loop / 주요 Flow** — 플레이/사용 흐름과 보상·진척 연결.
5. **핵심 시스템** — 각 시스템의 목적, 작동, 서로 주고받는 입력/출력, 기대효과.
6. **UX/UI/Visual** — 화면 구조, 정보 계층, 아트 방향, 승인된 Visual과 아직 미확정인 부분.
7. **현재 구현상태** — repository/code/Scene/data 기준 구현됨·부분·미구현을 구분.
8. **검증상태** — static/runtime/device/human/accessibility/platform/store 등 evidence ceiling을 분리해 PASS/PARTIAL/NOT_RUN/BLOCKED_UNVERIFIED로 표시.
9. **현재 blocker / 다음 작업** — 바로 이어서 해야 할 일과 완료조건.
10. **최근 중요한 결정** — 무엇을 왜 선택/기각/보류했는지.
11. **주요 위험 / revisit condition** — 어떤 증거·환경·성과 변화에서 다시 결정해야 하는지.

하위 페이지 링크는 위 내용을 더 깊게 보는 `drilldown`이다. Home 본문이 "상세는 08 페이지 참조"만 남아 위 핵심을 설명하지 않는 상태는 완료가 아니다.

Repository가 `REPOSITORY_STRUCTURED_CANON`이고 Notion이 `NOTION_HUMAN_FACING_CANON`이라는 권위 분리는 그대로 유지한다. Home은 runtime truth를 새로 만들지 않고 latest merged repository facts와 사용자 확정 방향을 사람이 이해 가능한 형태로 투영한다.

'''
    project_os = project_os.replace(anchor, section + anchor, 1)
write(project_os_path, project_os)

append_once(
    "skills/managing-game-project-operating-system/LEARNING_LOG.md",
    "2026-08-19 · self-contained Project Home before drilldown",
    '''## 2026-08-19 · self-contained Project Home before drilldown

- 관찰: Project Home이 핵심 방향은 보여주지만 시스템/검증/구현 설명을 하위 페이지 링크에 의존하면 사용자가 프로젝트 전체를 읽기 위해 계속 이동해야 한다.
- 교훈: Notion human-facing canon의 첫 화면은 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`을 만족해야 하며, 하위 페이지는 상세 증거용이어야 한다.
- 기대효과: cold-start 이해도 향상, 반복 질문 감소, 잘못된 project-state 추정 감소.
- reuse_scope: BASE_PROMOTION_CANDIDATE
''',
)

auth_path = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
auth = json.loads(auth_path.read_text(encoding="utf-8"))
auth["human_home_policy"] = "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN"
auth["human_home_required_sections"] = [
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
auth["human_home_drilldown_rule"] = "CHILD_PAGES_ARE_DETAIL_EVIDENCE_NOT_REQUIRED_FOR_CORE_UNDERSTANDING"
auth_path.write_text(json.dumps(auth, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

notion_policy_path = "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
notion_policy = read(notion_policy_path)
if "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN" not in notion_policy:
    anchor = "## "
    first = notion_policy.find(anchor, notion_policy.find("\n") + 1)
    section = r'''## Project Home human-facing contract

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

각 Project Home은 프로젝트 한 줄 정의·플레이어/사용자 가치·확정 방향·Core Loop/Flow·핵심 시스템 목적/상호작용·UX/UI/Visual·현재 구현상태·검증 evidence ceiling·blocker/다음 작업·중요 결정·위험/revisit condition을 본문에서 직접 설명한다. 하위 `08 · 핵심 시스템 · 상세` 같은 페이지는 상세 evidence와 긴 표를 위한 drilldown이며 Home의 핵심 이해를 대신하지 않는다.

'''
    if first < 0:
        notion_policy = notion_policy.rstrip() + "\n\n" + section
    else:
        notion_policy = notion_policy[:first] + section + notion_policy[first:]
write(notion_policy_path, notion_policy)

# ---------------------------------------------------------------------------
# P02/P08/P07 freshness + legacy ownership fixes.
# ---------------------------------------------------------------------------
config_path = ROOT / ".github/reference-freshness.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
for rule in config.get("coupled_change_rules", []):
    name = rule.get("name")
    if name == "local-skill-contract-learning-test-sync":
        allowed = rule.setdefault("require_any_changed", [])
        for pattern in (
            "tests/test_p0[1-9]_*.py",
            "tests/test_sequential_part_coordinator_contract.py",
            "tests/test_full_adversarial_loop_semantics.py",
            "tests/test_human_home_self_contained_contract.py",
        ):
            if pattern not in allowed:
                allowed.append(pattern)
    elif name == "reference-checker-test-and-config-sync":
        required = rule.setdefault("require_all_changed", [])
        if ".github/reference-freshness.json" in required:
            required.remove(".github/reference-freshness.json")
        if "tests/test_reference_freshness.py" not in required:
            required.append("tests/test_reference_freshness.py")
        rule["semantic_note"] = "Config companion changes only when config schema/keys/semantics change; parser-only fixes require owned regression test, not a no-op config edit."
    elif name == "legacy-retention-shared-skill-sync":
        required = rule.setdefault("require_all_changed", [])
        if "skills/BASE_SHARED_SKILL_ROUTES.json" in required:
            required.remove("skills/BASE_SHARED_SKILL_ROUTES.json")
        learning = "skills/governing-legacy-retention-and-archives/LEARNING_LOG.md"
        if learning not in required:
            required.append(learning)
        rule["semantic_note"] = "Shared route companion is required only when route identity/trigger/activation semantics change, not for internal procedure/evidence edits."
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Parse all backticked aliases from the first Markdown table cell.
checker_path = "tools/check_canonical_reference_freshness.py"
checker = read(checker_path)
old = '''def parse_legacy_aliases(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    aliases: set[str] = set()
    table_row = re.compile(r"^\\|\\s*`([^`]+)`\\s*\\|")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = table_row.match(line)
        if match:
            aliases.add(match.group(1).strip())
    return aliases
'''
new = '''def parse_legacy_aliases(path: Path) -> set[str]:
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
if old not in checker:
    raise SystemExit("parse_legacy_aliases implementation anchor missing")
checker = checker.replace(old, new, 1)
write(checker_path, checker)

# Registry: only normalize the exact stale P03 active trigger/review terms identified by P01/P03.
registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry_text = registry_path.read_text(encoding="utf-8")
registry_text = registry_text.replace("google-sheets-drift", "configured-workspace-authority-drift")
registry_text = registry_text.replace(
    "GitHub·Google Sheets 불일치",
    "GitHub·configured workspace/repository authority 불일치",
)
registry_path.write_text(registry_text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Update permanent partition workflow to actually consume the new tests.
# ---------------------------------------------------------------------------
workflow_path = " .github/workflows/base-partition-contract.yml".strip()
workflow = read(workflow_path)
for test_path in (
    "tests/test_sequential_part_coordinator_contract.py",
    "tests/test_full_adversarial_loop_semantics.py",
    "tests/test_human_home_self_contained_contract.py",
):
    quoted = f"      - '{test_path}'"
    if quoted not in workflow:
        anchor = "      - 'tests/test_base_partition_contract.py'"
        workflow = workflow.replace(anchor, anchor + "\n" + quoted, 1)
compile_old = "python -m py_compile tools/check_base_partition_scope.py tools/periodic_source_scan_queue.py tests/test_base_partition_contract.py"
compile_new = (
    "python -m py_compile tools/check_base_partition_scope.py tools/periodic_source_scan_queue.py "
    "tests/test_base_partition_contract.py tests/test_sequential_part_coordinator_contract.py "
    "tests/test_full_adversarial_loop_semantics.py tests/test_human_home_self_contained_contract.py"
)
if compile_old in workflow:
    workflow = workflow.replace(compile_old, compile_new, 1)
run_old = "python -m unittest tests.test_base_partition_contract tests.test_periodic_source_scan_queue -v"
run_new = (
    "python -m unittest tests.test_base_partition_contract tests.test_sequential_part_coordinator_contract "
    "tests.test_full_adversarial_loop_semantics tests.test_human_home_self_contained_contract "
    "tests.test_periodic_source_scan_queue -v"
)
if run_old in workflow:
    workflow = workflow.replace(run_old, run_new, 1)
write(workflow_path, workflow)

# Update existing partition contract tests from hard chat barriers to semantic coordinator contract.
test_path = "tests/test_base_partition_contract.py"
test = read(test_path)
test = test.replace(
    '        self.assertEqual("INTEGRATION_ONLY", manifest["control_plane"]["write_authority"])\n        self.assertEqual(9, manifest["integration"]["total_new_gpt_chats_after_task_1"])',
    '        self.assertEqual("COORDINATOR_OR_INTEGRATION", manifest["control_plane"]["write_authority"])\n        self.assertEqual(0, manifest["integration"]["total_new_gpt_chats_after_task_1"])\n        self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", manifest["coordinator_execution"]["policy"])',
)
test = test.replace(
    '    def test_one_chat_one_part_notion_and_github_isolation(self) -> None:\n',
    '    def test_single_coordinator_preserves_unique_notion_part_pages_and_semantic_attribution(self) -> None:\n',
)
test = test.replace(
    '        self.assertEqual("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", isolation["worker_model"])',
    '        self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", isolation["worker_model"])',
)
test = test.replace(
    '        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["hub_write"])\n        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["shared_visual_write"])',
    '        self.assertEqual("COORDINATOR", isolation["notion"]["hub_write"])\n        self.assertEqual("COORDINATOR", isolation["notion"]["shared_visual_write"])',
)
test = test.replace(
    '            self.assertEqual("ONE_CHAT_END_TO_END", part["chat_ownership"])\n            self.assertEqual("OWN_PART_PAGE_ONLY", part["notion_write_authority"])',
    '            self.assertEqual("CURRENT_COORDINATOR_CHAT_SEQUENTIAL_CHECKPOINT", part["chat_ownership"])\n            self.assertEqual("COORDINATOR_CURRENT_OR_AFFECTED_PART", part["notion_write_authority"])',
)
test = test.replace(
    '        self.assertIn("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", worker)\n        self.assertIn("자기 `notion_page_url`만 직접 수정", worker)\n        self.assertIn("Base Hub", INTEGRATION_PROMPT.read_text(encoding="utf-8"))',
    '        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", worker)\n        self.assertIn("PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER", worker)\n        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", INTEGRATION_PROMPT.read_text(encoding="utf-8"))',
)
test = test.replace(
    '        self.assertIn("--integration", text)\n        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)',
    '        self.assertIn("--integration", text)\n        self.assertIn("--coordinator", text)\n        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)\n        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", text)\n        self.assertIn("SEMANTIC_OWNER:", text)',
)
test = test.replace(
    '        self.assertEqual("READ_ONLY_UNLESS_INTEGRATION_ASSIGNMENT_OR_CROSS_PART_CHANGE_REQUEST", manifest["unassigned_path_policy"])',
    '        self.assertEqual("COORDINATOR_REVIEW_WITH_SEMANTIC_OWNER_ATTRIBUTION", manifest["unassigned_path_policy"])',
)
# The prior test name/semantics remain useful for strict --part compatibility; add coordinator assertions.
needle = '        self.assertIn("OUT_OF_PARTITION_WRITE", outside.stdout)\n'
if needle in test and 'SEMANTIC_OWNER:P04' not in test:
    addition = (
        needle
        + '        coordinator = self.run_scope("--coordinator", "--files", "AGENTS.md", "skills/designing-vertical-slices/SKILL.md")\n'
        + '        self.assertEqual(0, coordinator.returncode, coordinator.stdout + coordinator.stderr)\n'
        + '        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", coordinator.stdout)\n'
        + '        self.assertIn("SEMANTIC_OWNER:P04", coordinator.stdout)\n'
    )
    test = test.replace(needle, addition, 1)
write(test_path, test)

# ---------------------------------------------------------------------------
# Reference freshness regression for multi-alias cells.
# ---------------------------------------------------------------------------
ref_test_path = "tests/test_reference_freshness.py"
ref_test = read(ref_test_path)
if "test_parse_legacy_aliases_reads_every_alias_in_first_table_cell" not in ref_test:
    marker = "\n\nif __name__ == \"__main__\":"
    if marker not in ref_test:
        raise SystemExit("reference freshness test main marker missing")
    method = r'''

    def test_parse_legacy_aliases_reads_every_alias_in_first_table_cell(self) -> None:
        from tempfile import TemporaryDirectory
        from tools.check_canonical_reference_freshness import parse_legacy_aliases

        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "aliases.md"
            path.write_text(
                "| Legacy alias | Current |\n"
                "|---|---|\n"
                "| `old-one` / `old-two` / `old-three` | current-skill |\n",
                encoding="utf-8",
            )
            self.assertEqual(
                {"old-one", "old-two", "old-three"},
                parse_legacy_aliases(path),
            )
'''
    ref_test = ref_test.replace(marker, method + marker, 1)
write(ref_test_path, ref_test)

print("SEQUENTIAL_COORDINATOR_MIGRATION_APPLIED")
