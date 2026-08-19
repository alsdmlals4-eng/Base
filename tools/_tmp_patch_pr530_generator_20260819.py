from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1. Keep the generated Sheet contract migration-only.
generator_path = ROOT / "tools" / "build_base_v9_artifacts.py"
generator = generator_path.read_text(encoding="utf-8")
old = '''        "project_sheet_role": "USER_FACING_GDD_WORKSPACE",
        "sheet_only_change_status": "PROPOSED_SHEET_CHANGE",
'''
new = '''        "project_sheet_role": "MIGRATION_ONLY_LEGACY_SOURCE",
        "sheet_only_change_status": "MIGRATION_PROPOSAL_ONLY",
'''
if old not in generator:
    raise SystemExit("sheet generator anchor missing")
generator_path.write_text(generator.replace(old, new, 1), encoding="utf-8", newline="\n")

# 2. The existing visual-dashboard Skill remains useful as the Notion Home / Visual Map
#    human-facing projection owner. Only its retired standalone HTML behavior disappears.
registry_path = ROOT / "skills" / "SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
row = next(item for item in registry["skills"] if item["skill_id"] == "building-project-visual-dashboards")
row["status"] = "ACTIVE"
row["trigger_tags"] = [
    tag for tag in row.get("trigger_tags", [])
    if tag not in {"html-dashboard", "standalone-dashboard", "external-html-workspace"}
]
for tag in (
    "notion-project-home",
    "notion-visual-map",
    "human-facing-project-view",
    "self-contained-home",
):
    if tag not in row["trigger_tags"]:
        row["trigger_tags"].append(tag)
row["use_when"] = [
    "프로젝트 개요·Core Loop·핵심 시스템·UX/UI/Visual·구현/검증 상태·위험·다음 작업을 사람이 한 화면에서 이해해야 할 때 Notion Project Home과 Visual Map을 구성·갱신한다. Repository structured/runtime truth를 복제 정본으로 만들지 않는다."
]
row["do_not_use_when"] = [
    "standalone HTML/CSS/JavaScript 프로젝트 dashboard 또는 별도 local visual workspace를 만들려는 작업, 단순 repository 상태 조회, 실제 runtime evidence 생성 자체가 목적일 때는 사용하지 않는다."
]
row["review_triggers"] = [
    "Home 핵심 설명을 하위 링크로만 밀어냄",
    "Notion과 repository를 독립 정본으로 복제함",
    "standalone HTML project dashboard 재도입",
    "실행하지 않은 runtime/UX 검증을 Home에서 PASS로 표시",
    "프로젝트 relation/identity 혼입",
]
row["last_reviewed_at"] = "2026-08-19"
row["last_reviewed_commit"] = "PENDING_PR530_SELECTIVE_INTEGRATION"
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

# 3. Restore P05 semantic ownership because the Skill remains active.
manifest_path = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
if "building-project-visual-dashboards" not in p05["owned_skill_ids"]:
    p05["owned_skill_ids"].append("building-project-visual-dashboards")
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 4. Reclassify the Skill body to the Notion human-facing owner.
skill_path = ROOT / "skills" / "building-project-visual-dashboards" / "SKILL.md"
skill_path.write_text('''---
name: building-project-visual-dashboards
description: Use when a project needs a self-contained Notion Project Home or Visual Map that explains concepts, loops, systems, UX/visual state, evidence, risks, and next work without replacing repository truth.
---

# Building Project Visual Dashboards — Notion Project Home & Visual Map

`NOTION_PROJECT_HOME_AND_VISUAL_MAP`

## 목적

이 Skill은 사람이 프로젝트를 **추가 페이지 이동 없이 메인 Home 한 화면에서 이해**할 수 있도록 Notion의 human-facing Project Home과 Visual Map을 구성·갱신한다.

Repository Markdown/JSON/code/scene/resource/test/runtime evidence를 복제 정본으로 만들지 않는다. Notion은 사람이 이해·비교·학습하는 projection이고, structured/runtime truth는 Repository가 계속 소유한다.

## 핵심 계약

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Project Home에는 최소 다음을 직접 설명한다.

- 프로젝트 한 줄 정의와 핵심 사용자/플레이어 가치
- 현재 확정 방향과 보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동 방식·상호작용·기대효과
- UX/UI/Visual 방향과 승인 상태
- 현재 구현상태와 repository/runtime truth 연결
- 검증상태와 evidence ceiling
- blocker / 다음 작업
- 최근 중요한 결정과 선택 이유
- 주요 위험과 revisit condition

하위 페이지는 긴 표, 전체 asset 목록, 상세 evidence, history, Source를 위한 drilldown이다. Home 핵심 이해를 “링크 참조”로 대체하지 않는다.

## 진행 흐름

```text
Project identity / latest user decisions
→ latest GitHub main + Project Notion readback
→ core direction / loop / systems / UX / visual / implementation / evidence 복원
→ 사람이 알아야 할 정보 계층 설계
→ Home 본문에 자체 완결 설명 작성
→ 필요 시 Visual Map / image / diagram 배치
→ structured/runtime locator 연결
→ destination readback
→ stale/duplicate/overclaim 검토
```

## 입력

- exact Project identity
- latest confirmed decisions
- Project GitHub main / canonical owners
- actual implementation/runtime evidence
- Project Notion existing Home/detail pages
- approved visual/reference inputs
- current blockers / next work / revisit conditions

## 출력

- self-contained Notion Project Home
- 필요한 Visual Map/diagram
- 상세 하위 페이지로 가는 drilldown link
- repository/runtime evidence locator
- `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 구분한 검증 상태

## 기대효과

- 사용자가 프로젝트를 다시 읽을 때 여러 하위 페이지를 찾아다니는 비용 감소
- Skill/Module/시스템의 목적과 연결관계를 빠르게 학습
- AI가 프로젝트를 재개할 때 human-facing 방향과 repository truth를 함께 복원하기 쉬움
- 링크 허브만 남아 핵심 방향이 숨는 문제 감소

## standalone HTML / local dashboard 금지

다음은 현행 기본 경로가 아니다.

- standalone HTML/CSS/JavaScript project dashboard 생성
- 별도 localhost project-management UI 생성
- HTML dashboard 상태를 current implementation truth로 사용
- Notion/Repository 정보를 HTML에 다시 복사해 제3의 정본 생성

과거 HTML dashboard의 UNIQUE 자료가 있으면 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`에 따라 현행 Notion/Repository owner로 흡수한다.

## 검증

- Home만 읽어도 핵심 방향·흐름·시스템·Visual·상태·다음 작업을 설명할 수 있는가
- Notion 주장과 repository/runtime evidence가 충돌하지 않는가
- 실제 미실행 검증이 PASS로 표시되지 않았는가
- 다른 프로젝트 정보가 섞이지 않았는가
- 핵심 정보를 하위 링크로만 밀어내지 않았는가
- write 뒤 exact Project destination을 readback했는가

Learning Log: `skills/building-project-visual-dashboards/LEARNING_LOG.md`
''', encoding="utf-8", newline="\n")

learning_path = ROOT / "skills" / "building-project-visual-dashboards" / "LEARNING_LOG.md"
learning_path.write_text('''# Learning Log

## 2026-08-19 · HTML builder에서 Notion human-facing projection owner로 재분류

- standalone HTML dashboard는 사용자 기본 작업면에서 제거한다.
- 그러나 “복잡한 프로젝트를 사람이 한 화면에서 이해하도록 구조화한다”는 책임 자체는 여전히 필요하다.
- 별도 Skill을 새로 만들기보다 기존 `building-project-visual-dashboards`의 목적을 Notion Project Home / Visual Map으로 재분류하는 편이 routing/consumer 안정성과 context 비용에서 더 강하다.
- QA Evidence Studio는 project-management dashboard가 아니라 specialist validation utility이므로 별도 유지한다.
- disposition: `RECLASSIFY + IMPROVE`.
- reuse_scope: `BASE_PROMOTION_CANDIDATE`.
''', encoding="utf-8", newline="\n")

print("PR530_GENERATOR_AND_NOTION_DASHBOARD_PATCH_APPLIED")
