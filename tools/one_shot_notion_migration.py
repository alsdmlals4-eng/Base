from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-19"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 match, got {count}")
    return text.replace(old, new, 1)


def regex_replace_once(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 regex match, got {count}")
    return updated


def run_test(args: list[str], expect_success: bool) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    print(f"$ {' '.join(args)}")
    print(result.stdout)
    print(result.stderr)
    if expect_success and result.returncode != 0:
        raise RuntimeError(f"expected test success, exit={result.returncode}")
    if not expect_success and result.returncode == 0:
        raise RuntimeError("RED gate failed: new regression test unexpectedly passed before production edits")
    return result


def update_test_first() -> None:
    rel = "tests/test_uiux_external_reference_absorption.py"
    text = read(rel)
    text = replace_once(
        text,
        'WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"\nLEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"\n',
        'WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"\nSEEDS = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"\nLEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"\nAGENTS = ROOT / "AGENTS.md"\n',
        "test constants",
    )
    new_test = '''    def test_notion_official_replaces_figma_sources_in_periodic_loop(self) -> None:\n        watchlist = WATCHLIST.read_text(encoding="utf-8")\n        seeds = SEEDS.read_text(encoding="utf-8")\n        agents = AGENTS.read_text(encoding="utf-8")\n\n        for retired in (\n            "Huddling Figmapedia",\n            "https://huddling.ai/figma-info",\n        ):\n            self.assertNotIn(retired, watchlist)\n        self.assertNotIn("figma-practical-design-workflow", seeds)\n        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", agents)\n\n        for required in (\n            "Notion official Help / Releases / Developers",\n            "AUTHORITY_TARGET",\n            "Skills for Notion Agent",\n            "Custom Agents",\n            "Notion MCP",\n        ):\n            self.assertIn(required, watchlist)\n        self.assertIn("notion-skills-work-structure", seeds)\n\n        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))\n        self.assertFalse(any(row["source_id"] == "huddling-figmapedia" for row in ledger["sources"]))\n        matches = [row for row in ledger["sources"] if row["source_id"] == "notion-official"]\n        self.assertEqual(1, len(matches))\n        source = matches[0]\n        self.assertEqual(["AUTHORITY_TARGET"], source["roles"])\n        self.assertEqual("weekly", source["recommended_cadence"])\n        self.assertEqual("ACTIVE", source["status"])\n        self.assertIn("Skills for Notion Agent", source["scan_surfaces"])\n\n'''
    text = regex_replace_once(
        text,
        r"    def test_huddling_figmapedia_is_a_weekly_discovery_source\(self\) -> None:\n.*?(?=    def test_existing_ui_owner_absorbs_design_read_and_resilience_principles)",
        new_test,
        "replace huddling regression test",
        flags=re.S,
    )
    text = replace_once(
        text,
        '            "https://huddling.ai/figma-info",\n',
        "",
        "remove huddling learning input assertion",
    )
    write(rel, text)


def update_watchlist() -> None:
    rel = "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
    text = read(rel)
    text = regex_replace_once(
        text,
        r"^\| \*\*Huddling Figmapedia\*\*.*\n",
        "",
        "remove Huddling watchlist row",
        flags=re.M,
    )
    text = text.replace("Huddling Figmapedia (`figma-info`), ", "")
    text = regex_replace_once(
        text,
        r"^- Huddling/Figmapedia의 설명을 Figma 공식 제품 사실이나 정책 권위로 승격했는가\?\n",
        "",
        "remove Figma/Huddling adversarial check",
        flags=re.M,
    )

    notion_row = "| **Notion official Help / Releases / Developers** | `AUTHORITY_TARGET` | Notion의 Skills for Notion Agent, Instructions와 Skills의 역할 차이, Custom Agents, database 기반 projects/tasks/views/relations/rollups/templates, automations/buttons/webhooks, Notion MCP·API와 권한·availability 변화를 조사한다. | Notion 제품 동작에만 T1 후보. Base의 정본·Skill 구조를 그대로 Notion에 종속시키지 않고, 요금제·권한·beta/availability는 적용 직전 현재 공식 문서로 재확인 |\n"
    anchor = "| **Hada GeekNews** | `DISCOVERY_FEED` | prompt engineering, agent harness, coding workflow, eval, security 원문 발견 | 반드시 원글/공식 문서로 역추적 |\n"
    if notion_row not in text:
        text = replace_once(text, anchor, anchor + notion_row, "insert Notion workflow source")

    skill_anchor = "| **Google Developers Blog — ADK Agent Skills** | `AUTHORITY_TARGET` | on-demand loading, progressive disclosure, inline/file-based/generated skill pattern |"
    if "**Notion official — Skills / Custom Agents**" not in text:
        idx = text.find(skill_anchor)
        if idx < 0:
            raise RuntimeError("Notion skill source anchor not found")
        line_end = text.find("\n", idx)
        notion_skill_row = "\n| **Notion official — Skills / Custom Agents** | `AUTHORITY_TARGET` | 반복 업무를 on-demand Skill로 캡슐화하는 법, persistent Instructions와의 경계, Custom Agents에서 Skill을 재사용하는 구조, workspace/database 기반 자동화 패턴 | Notion 제품 구현을 Base Skill 포맷으로 복제하지 않는다. reusable principle만 Existing Solution First + 적대적 검토 후 `ADAPT` |"
        text = text[:line_end] + notion_skill_row + text[line_end:]

    weekly_pattern = r"^- `weekly`: (.*)$"
    match = re.search(weekly_pattern, text, flags=re.M)
    if not match:
        raise RuntimeError("weekly cadence line not found")
    weekly = match.group(1)
    if "Notion official Help / Releases / Developers" not in weekly:
        weekly = "Notion official Help / Releases / Developers, " + weekly
        text = text[: match.start(1)] + weekly + text[match.end(1) :]

    write(rel, text)


def update_discovery_seeds() -> None:
    rel = "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
    text = read(rel)
    replacement = '''## 12. Notion skills, work structure, and utilization workflow\n\nNotion은 Base의 정본이나 필수 workspace로 승격하지 않는다. 이 seed는 **Notion 자체 기능의 현재 동작과 반복 가능한 지식·작업 구조를 조사하는 공식 source**이며, 발견한 원리는 Existing Solution First와 적대적 검토를 통과한 뒤 기존 Base owner에 최소 흡수한다.\n\n```yaml\nseed_group: notion-skills-work-structure\nstatus: ACTIVE_DISCOVERY_SEED\ndomains:\n  - PROMPT_AND_AGENT_WORKFLOW\n  - SKILL_AUTHORING_AND_EVOLUTION\nsource_role: AUTHORITY_TARGET_FOR_NOTION_BEHAVIOR\nrecommended_cadence: weekly\nurls:\n  skills: https://www.notion.com/help/skills-for-notion-agent\n  custom_agents: https://www.notion.com/help/custom-agents\n  notion_mcp: https://www.notion.com/help/notion-mcp\n  databases: https://www.notion.com/help/category/databases\n  database_automations: https://www.notion.com/help/database-automations\n  releases: https://www.notion.com/releases\n  developers: https://developers.notion.com/\nscan_surfaces:\n  - Skills for Notion Agent and reusable task instructions\n  - persistent Instructions vs on-demand Skills vs autonomous Custom Agents\n  - databases, projects/tasks, views, relations, rollups, formulas and templates\n  - database automations, buttons, triggers, webhooks and failure boundaries\n  - Notion MCP, API, permissions and connected-app boundaries\n  - release notes, beta/general availability and plan/seat changes when adoption depends on them\n```\n\n### 12.1 흡수 질문\n\n```text\n반복 작업을 매번 긴 prompt로 다시 쓰고 있는가?\n→ persistent preference는 instruction, 필요할 때만 부르는 절차는 skill, 시간/이벤트 기반 자율 실행은 agent/automation으로 책임을 분리할 수 있는가?\n→ database property·view·relation이 실제 의사결정과 handoff를 줄이는가, 아니면 관리 오버헤드만 늘리는가?\n→ template/button/automation이 반복 수작업을 줄이되 숨은 side effect와 권한 확대를 만들지 않는가?\n→ Notion MCP/API가 기존 GitHub·Google Sheets·repo-native owner를 대체하려는가, 아니면 명확한 보조 read/write 경계가 있는가?\n→ 공개 공식 자료에서 확인한 원리가 Base의 기존 Skill/Mode/Template에 이미 있는가?\n→ 기능 availability·plan·permission이 바뀌어도 Base 정본과 프로젝트 실행이 깨지지 않는가?\n```\n\n### 12.2 승격 경계\n\n- Notion 기능명이 생겼다는 이유로 새 `notion-*` Skill을 만들지 않는다.\n- 반복 가치가 검증된 원리만 기존 owner에 `ADAPT`; 이미 있는 계약은 `ALREADY_COVERED`로 닫는다.\n- Notion 페이지·database를 Base/GitHub 정본보다 높은 권한으로 만들지 않는다.\n- 별도 유료 플랜·AI credit·API 비용·automation quota가 필요한 경로는 `ZERO_INCREMENTAL_COST_REQUIRED`와 새 사용자 승인을 통과하기 전 활성화하지 않는다.\n- 실제 연결 workspace를 읽거나 쓰지 않은 조사에서는 Notion 사용 완료·자동화 동작을 주장하지 않는다.\n- 실질 개선이 없으면 `NO_CHANGE`로 닫고 source scan 기록만 갱신한다.\n'''
    text = regex_replace_once(
        text,
        r"^## 12\. Figma practical design workflow\n.*?(?=^## 13\. |\Z)",
        replacement,
        "replace Figma discovery seed with Notion",
        flags=re.S | re.M,
    )
    write(rel, text)


def update_ledger() -> None:
    rel = "docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
    data = json.loads(read(rel))
    sources = data["sources"]
    before = len(sources)
    sources = [row for row in sources if row.get("source_id") != "huddling-figmapedia"]
    if len(sources) != before - 1:
        raise RuntimeError("expected exactly one huddling-figmapedia ledger row")
    if any(row.get("source_id") == "notion-official" for row in sources):
        raise RuntimeError("notion-official ledger row already exists unexpectedly")
    sources.append(
        {
            "source_id": "notion-official",
            "name": "Notion official Help / Releases / Developers",
            "domains": ["PROMPT_AND_AGENT_WORKFLOW", "SKILL_AUTHORING_AND_EVOLUTION"],
            "roles": ["AUTHORITY_TARGET"],
            "recommended_cadence": "weekly",
            "scan_surfaces": [
                "Skills for Notion Agent",
                "Instructions vs Skills vs Custom Agents",
                "databases/projects/tasks/views/relations/rollups/templates",
                "database automations/buttons/webhooks",
                "Notion MCP",
                "developer docs/API/permissions",
                "release notes and availability",
            ],
            "last_successful_scan_at": DATE,
            "last_material_candidate_at": DATE,
            "last_base_contribution_at": None,
            "last_base_contribution_ref": None,
            "material_candidate_count_since_tracking_start": 1,
            "base_contribution_count_since_tracking_start": 0,
            "status": "ACTIVE",
        }
    )
    data["sources"] = sources
    write(rel, json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")


def update_learning_log() -> None:
    rel = "skills/auditing-and-refining-ui-art/LEARNING_LOG.md"
    text = read(rel)
    text = replace_once(
        text,
        "## 2026-08-19 — UI/UX 외부 Source 선택 흡수와 Figma discovery watch",
        "## 2026-08-19 — UI/UX 외부 Source 선택 흡수",
        "learning log title",
    )
    text = replace_once(
        text,
        ", `https://huddling.ai/figma-info`.",
        ".",
        "remove Figma source URL from learning log",
    )
    text = regex_replace_once(
        text,
        r"^- \*\*Decision:\*\* Huddling Figmapedia.*\n",
        "",
        "remove Huddling learning decision",
        flags=re.M,
    )
    text = replace_once(
        text,
        "- **Next trigger:** 세 upstream source의 material update, Huddling 후보가 반복적으로 Figma 공식 원문과 불일치, 또는 서로 다른 두 프로젝트에서 이 Design Read/복원력 계약의 실제 효과가 관찰될 때 재검토한다.",
        "- **Next trigger:** 유지 중인 두 upstream source의 material update 또는 서로 다른 두 프로젝트에서 이 Design Read/복원력 계약의 실제 효과가 관찰될 때 재검토한다.",
        "learning next trigger",
    )
    write(rel, text)


def update_active_figma_policy() -> None:
    rel = "AGENTS.md"
    text = read(rel)
    anchor = "- **현재 유료 플랜 고정:** `CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO`, `PAID_PLAN_COUNT: 2`. 현재 사용 가능한 유료 플랜은 **GPT Pro와 Figma Pro 두 개뿐**이다. 두 플랜 안의 기능도 별도 metered billing으로 전환되는 경로는 허용 범위가 아니다. 다른 유료 AI/API/SaaS/상위 플랜/marketplace/runner/compute/storage를 사용하거나 결제하려면 **새 사용자 승인**이 필요하다.\n"
    override = anchor + "- **Figma 사용 중단 오버라이드:** `FIGMA_USAGE: DISABLED_BY_USER`. 유료 플랜의 보유·구독 상태와 무관하게 사용자가 다시 명시적으로 승인하기 전에는 Figma 기능·connector·MCP·workspace·Visual Bible을 Base/프로젝트의 기본·보조·대안 경로로 선택하지 않고, 주기 참고 Source에서도 조사하지 않는다. 과거 Figma 문서·코드·Template·evidence는 역사·호환성 자료로만 보존하며 현재 작업 권위를 갖지 않는다. Notion은 공식 공개 자료를 학습 Source로 조사할 수 있지만, 실제 workspace 채택·유료 기능 사용은 별도 현재 결정과 비용 Gate를 따른다.\n"
    if "FIGMA_USAGE: DISABLED_BY_USER" not in text:
        text = replace_once(text, anchor, override, "AGENTS Figma disable override")
    write(rel, text)

    rel = "docs/VISUAL_COLLABORATION_TOOL_POLICY.md"
    text = read(rel)
    heading = "# Visual Collaboration Tool Policy\n"
    active = '''# Visual Collaboration Tool Policy\n\n## Active status — 2026-08-19\n\n`FIGMA_USAGE: DISABLED_BY_USER`가 현재 사용자 결정이다. 새 기획·UI/UX·시각 작업은 Figma를 기본·보조·fallback workspace로 선택하거나 자동 read/write하지 않는다. 이 문서 아래의 Figma Visual Bible·delivery·component·prototype 설명은 기존 구현과 과거 Decision을 해석하기 위한 `LEGACY_FIGMA_REFERENCE`이며 새 작업의 활성 지시가 아니다. 사용자가 Figma 재도입을 명시적으로 승인하기 전에는 GitHub 정본, repo-native 구조화 데이터, 승인된 로컬/프로젝트 자산과 실제 Godot/runtime evidence를 사용하고, 다이어그램 도구는 현재 요청에 필요한 경우에만 별도 선택한다.\n'''
    if "## Active status — 2026-08-19" not in text:
        text = replace_once(text, heading, active, "visual policy active override")
    write(rel, text)


def main() -> None:
    update_test_first()
    red = run_test(
        ["python", "-m", "unittest", "tests.test_uiux_external_reference_absorption"],
        expect_success=False,
    )
    if "FAILED" not in (red.stdout + red.stderr):
        raise RuntimeError("RED gate did not fail as a unittest assertion failure")

    update_watchlist()
    update_discovery_seeds()
    update_ledger()
    update_learning_log()
    update_active_figma_policy()

    run_test(
        ["python", "-m", "unittest", "tests.test_uiux_external_reference_absorption"],
        expect_success=True,
    )
    run_test(
        ["python", "-m", "unittest", "tests.test_base_long_horizon_work_contract"],
        expect_success=True,
    )

    watchlist = read("docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md")
    seeds = read("docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md")
    ledger = json.loads(read("docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json"))
    if "https://huddling.ai/figma-info" in watchlist or "Huddling Figmapedia" in watchlist:
        raise RuntimeError("retired Figma discovery source remains in watchlist")
    if "figma-practical-design-workflow" in seeds:
        raise RuntimeError("retired Figma discovery seed remains active")
    if any(row.get("source_id") == "huddling-figmapedia" for row in ledger["sources"]):
        raise RuntimeError("retired Figma source remains in ledger")


if __name__ == "__main__":
    main()
