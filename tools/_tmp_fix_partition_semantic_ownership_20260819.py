from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
model_path = ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md"
worker_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md"
integration_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md"
test_path = ROOT / "tests/test_base_partition_contract.py"

NOTION_HUB = "https://app.notion.com/p/3c11b237eb1c81748c9ce43831b4f55d?pvs=204"
NOTION_SHARED_VISUAL = "https://app.notion.com/p/3c11b237eb1c81a6b773ed6726171561?pvs=204"
NOTION_PARTS = {
    "P01": "https://app.notion.com/p/3c11b237eb1c8179a4bff44ce3cd5316?pvs=204",
    "P02": "https://app.notion.com/p/3c11b237eb1c8137888edd1e41745099?pvs=204",
    "P03": "https://app.notion.com/p/3c11b237eb1c8122acffca50aed2c68f?pvs=204",
    "P04": "https://app.notion.com/p/3c11b237eb1c81f2a6d7de82c0938277?pvs=204",
    "P05": "https://app.notion.com/p/3c11b237eb1c81498eb5da3fea812390?pvs=204",
    "P06": "https://app.notion.com/p/3c11b237eb1c817eb473ea7758a1999d?pvs=204",
    "P07": "https://app.notion.com/p/3c11b237eb1c8110b3c3f659a7fe266e?pvs=204",
    "P08": "https://app.notion.com/p/3c11b237eb1c8169b55af5b2f27d9bb7?pvs=204",
    "P09": "https://app.notion.com/p/3c11b237eb1c812f9de1f7f5e2996d81?pvs=204",
}

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["operating_mode"] = {
    "policy": "PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION",
    "daily_default": "UNIFIED_BASE",
    "partition_activation": "MATERIAL_AUDIT_SPECIALIZATION_LEARNING_OR_CONFLICT_BOUNDARY",
    "activate_only_relevant_parts": True,
    "run_all_parts_for_every_task": False,
    "integration_returns_to_one_base": True,
}
manifest["collaboration_isolation"] = {
    "worker_model": "ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END",
    "github": {
        "one_branch_per_part": True,
        "one_pr_per_part": True,
        "branch_template": "opt/base-part-{PART_ID}-{slug}",
        "other_part_branches_prs": "READ_ONLY_DO_NOT_MUTATE",
        "control_plane_write": "INTEGRATION_ONLY",
    },
    "notion": {
        "hub_url": NOTION_HUB,
        "hub_write": "INTEGRATION_ONLY",
        "shared_visual_url": NOTION_SHARED_VISUAL,
        "shared_visual_write": "INTEGRATION_ONLY",
        "part_page_write": "OWN_PART_ONLY",
        "other_part_pages": "READ_ONLY",
        "cross_part_change": "CROSS_PART_CHANGE_REQUEST",
        "image_rule": "PART_SPECIFIC_VISUALS_TO_OWN_PAGE_SHARED_VISUALS_TO_INTEGRATION_SHARED_REFERENCE",
    },
}

for part in manifest["parts"]:
    pid = part["part_id"]
    part["chat_ownership"] = "ONE_CHAT_END_TO_END"
    part["branch_template"] = f"opt/base-part-{pid}-<slug>"
    part["notion_page_url"] = NOTION_PARTS[pid]
    part["notion_write_authority"] = "OWN_PART_PAGE_ONLY"
    part["notion_read_only_pages"] = [NOTION_HUB, NOTION_SHARED_VISUAL] + [url for other, url in NOTION_PARTS.items() if other != pid]

p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
paths = p05["owned_write_paths"]
for broad in (
    "docs/knowledge/game-development/*UI*",
    "docs/knowledge/game-development/UI_*",
    "docs/knowledge/game-development/*UX*",
):
    while broad in paths:
        paths.remove(broad)
for exact in (
    "docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md",
    "docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md",
    "docs/knowledge/OPEN_SOURCE_GODOT_UI_REFERENCE_CATALOG.md",
):
    if exact not in paths:
        paths.append(exact)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

model = model_path.read_text(encoding="utf-8")
marker = "## 운영 모드 — 하나의 Base, 필요할 때만 Partition\n"
if marker not in model:
    anchor = "설계 기준 main: `f93016dbe90d3d1d906afaaaa75005b490220e90`. 실제 Part 시작 시에는 이 SHA를 그대로 재사용하지 않고 최신 `main`을 다시 읽어 exact baseline으로 pin한다.\n"
    section = """

## 운영 모드 — 하나의 Base, 필요할 때만 Partition

`PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION`

- Base의 일상 사용과 프로젝트 적용은 **하나의 통합 Base**가 기본이다.
- P01~P09는 Base를 9개 제품이나 9개 상시 runtime으로 쪼개는 구조가 아니다.
- Partition은 대규모 감사, 분야별 심층 최적화, 전문 Source 학습, 책임 추적, 충돌 격리가 실질적으로 필요할 때만 활성화한다.
- 일반 작업마다 P01~P09 전체를 강제 호출하지 않는다. 작업과 직접 관련된 Part만 선택적으로 사용할 수 있다.
- 여러 Part를 사용했으면 Integration이 cross-part finding과 CP0를 정리해 결과를 다시 **ONE BASE**로 돌려놓는다.
- 장기 성과는 Part 수 증가가 아니라 Base 전체 정확성, 사용자 이해도, 충돌 감소, 재사용성, Context 효율로 판단한다.
"""
    if anchor not in model:
        raise SystemExit("operating model insertion anchor missing")
    model = model.replace(anchor, anchor + section, 1)

isolation_marker = "## 채팅·GitHub·Notion 충돌 격리\n"
if isolation_marker not in model:
    anchor = "## CP0 · Base Control Plane\n"
    section = f"""## 채팅·GitHub·Notion 충돌 격리

`ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END`

- P01~P09는 각각 **새 GPT 채팅 하나가 처음부터 완료까지** 책임진다.
- 각 채팅은 자기 `opt/base-part-Pxx-<slug>` branch와 자기 PR 하나만 수정한다.
- 다른 Part branch/worktree/PR은 읽을 수 있지만 수정·rebase·merge·close·흡수하지 않는다.
- GitHub CP0와 `.github`, Registry, generated output은 Integration만 쓴다.
- Notion Base Hub와 `00 · Base 공용 Visual Reference`는 Integration 전용 쓰기 영역이다.
- 각 Part 채팅은 Manifest의 `notion_page_url` 하나만 직접 갱신한다. 다른 Part 페이지는 read-only다.
- Part 전용 이미지·다이어그램은 자기 Notion 페이지에 둔다. 여러 Part가 공유하는 시각 자료는 직접 공용 페이지에 쓰지 않고 `CROSS_PART_CHANGE_REQUEST`로 Integration에 전달한다.
- 동일 의미를 GitHub/Notion 양쪽에 독립 정본으로 만들지 않는다. GitHub가 구조화 규칙/Skill/Test 정본이고 Notion은 사람이 보는 설명·시각화·학습면이다.

{anchor}"""
    if anchor not in model:
        raise SystemExit("isolation insertion anchor missing")
    model = model.replace(anchor, section, 1)
model_path.write_text(model, encoding="utf-8", newline="\n")

worker = worker_prompt_path.read_text(encoding="utf-8")
worker_marker = "## Partition의 의미\n"
if worker_marker not in worker:
    anchor = "당신은 Base 전체가 아니라 제공된 **하나의 Partition**만 책임진다.\n"
    section = """

## Partition의 의미

`PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION`

이 지시문은 Base의 일상 실행을 9개로 분해하라는 뜻이 아니다. Base는 하나의 통합 시스템이며, 이 채팅은 대규모 감사·전문화·학습을 위해 선택적으로 활성화된 하나의 Maintenance View다. 다른 Part를 직접 수정하지 않되 cross-part 문제를 무시하지 말고 `CROSS_PART_CHANGE_REQUEST`로 남긴다.
"""
    if anchor not in worker:
        raise SystemExit("worker prompt insertion anchor missing")
    worker = worker.replace(anchor, anchor + section, 1)

worker_isolation_marker = "## 0A. 이 채팅의 단독 소유권\n"
if worker_isolation_marker not in worker:
    anchor = "## 1. 실행 주체\n"
    section = """## 0A. 이 채팅의 단독 소유권

`ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END`

- 이 채팅은 할당된 Part 하나를 처음부터 완료/PR까지 책임진다.
- 시작 시 Manifest에서 자기 `notion_page_url`과 `branch_template`을 읽는다.
- GitHub에서는 자기 Part branch/PR만 수정한다. 다른 Part branch/PR은 read-only다.
- Notion에서는 자기 `notion_page_url`만 직접 수정한다. Base Hub, 공용 Visual Reference, 다른 Part 페이지는 read-only다.
- 공용 시각 자료나 다른 Part/CP0 변경이 필요하면 직접 쓰지 말고 `CROSS_PART_CHANGE_REQUEST`를 남긴다.
- 이미지·다이어그램은 Part 전용이면 자기 Notion 페이지에, 프로젝트 고유이면 정확한 Project Notion에 배치한다. 공용 자료의 중복 복사는 금지한다.

""" + anchor
    if anchor not in worker:
        raise SystemExit("worker isolation insertion anchor missing")
    worker = worker.replace(anchor, section, 1)
worker_prompt_path.write_text(worker, encoding="utf-8", newline="\n")

integration = integration_prompt_path.read_text(encoding="utf-8")
integration_marker = "## 0. Integration의 의미\n"
if integration_marker not in integration:
    anchor = "P01..P09의 독립 최적화 결과를 최신 Base `main`에 안전하게 통합한다. 개별 Part 작업을 대신하지 않고 **CP0·cross-part 정합성·전체 회귀·최종 merge**만 책임진다.\n"
    section = """

## 0. Integration의 의미

Partition의 최종 산출물은 9개의 독립 Base가 아니라 **하나의 통합 Base**다. 필요한 Part만 활성화할 수 있으며, Integration은 실제로 수행된 Part의 결과만 모아 CP0·정본·Skill/Module 관계를 정리한다. 모든 일반 작업에 9개 Part 실행을 강제하지 않는다.
"""
    if anchor not in integration:
        raise SystemExit("integration prompt insertion anchor missing")
    integration = integration.replace(anchor, anchor + section, 1)

notion_marker = "## 1A. Notion/GitHub 충돌 통합\n"
if notion_marker not in integration:
    anchor = "## 2. Scope 감사\n"
    section = f"""## 1A. Notion/GitHub 충돌 통합

- 각 Part는 자기 branch/PR 및 자기 Notion 페이지 하나만 썼는지 확인한다.
- Base Hub `{NOTION_HUB}`와 공용 Visual `{NOTION_SHARED_VISUAL}`은 Integration만 갱신한다.
- 다른 Part 페이지를 직접 수정한 흔적은 scope 위반으로 취급한다.
- 공용 Visual 후보는 중복 제거·정본 확인 후 한 번만 공용 페이지에 승격한다.
- GitHub structured canon과 Notion human-facing summary가 같은 의미를 서로 다른 정본처럼 소유하지 않도록 readback한다.

""" + anchor
    if anchor not in integration:
        raise SystemExit("integration notion insertion anchor missing")
    integration = integration.replace(anchor, section, 1)
integration_prompt_path.write_text(integration, encoding="utf-8", newline="\n")

tests = test_path.read_text(encoding="utf-8")
needle = "    def test_each_part_has_a_context_pack_and_operational_contract(self) -> None:\n"
insert = '''    def test_hybrid_partition_mode_keeps_one_unified_base(self) -> None:\n        manifest = self.load_manifest()\n        mode = manifest["operating_mode"]\n        self.assertEqual("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", mode["policy"])\n        self.assertEqual("UNIFIED_BASE", mode["daily_default"])\n        self.assertTrue(mode["activate_only_relevant_parts"])\n        self.assertFalse(mode["run_all_parts_for_every_task"])\n        self.assertTrue(mode["integration_returns_to_one_base"])\n        for path in (OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT):\n            text = path.read_text(encoding="utf-8")\n            self.assertIn("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", text)\n\n    def test_one_chat_one_part_notion_and_github_isolation(self) -> None:\n        manifest = self.load_manifest()\n        isolation = manifest["collaboration_isolation"]\n        self.assertEqual("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", isolation["worker_model"])\n        self.assertTrue(isolation["github"]["one_branch_per_part"])\n        self.assertTrue(isolation["github"]["one_pr_per_part"])\n        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["hub_write"])\n        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["shared_visual_write"])\n        urls = []\n        branches = []\n        for part in manifest["parts"]:\n            self.assertEqual("ONE_CHAT_END_TO_END", part["chat_ownership"])\n            self.assertEqual("OWN_PART_PAGE_ONLY", part["notion_write_authority"])\n            urls.append(part["notion_page_url"])\n            branches.append(part["branch_template"])\n        self.assertEqual(9, len(set(urls)))\n        self.assertEqual(9, len(set(branches)))\n        worker = WORKER_PROMPT.read_text(encoding="utf-8")\n        self.assertIn("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", worker)\n        self.assertIn("자기 `notion_page_url`만 직접 수정", worker)\n        self.assertIn("Base Hub", INTEGRATION_PROMPT.read_text(encoding="utf-8"))\n\n    def test_p05_visual_scope_avoids_broad_ui_ux_globs(self) -> None:\n        manifest = self.load_manifest()\n        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")\n        for broad in ("docs/knowledge/game-development/*UI*", "docs/knowledge/game-development/UI_*", "docs/knowledge/game-development/*UX*"):\n            self.assertNotIn(broad, p05["owned_write_paths"])\n        self.assertIn("docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md", p05["owned_write_paths"])\n        self.assertIn("docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md", p05["owned_write_paths"])\n\n'''
if "def test_hybrid_partition_mode_keeps_one_unified_base" not in tests:
    if needle not in tests:
        raise SystemExit("test insertion anchor missing")
    tests = tests.replace(needle, insert + needle, 1)
elif "def test_one_chat_one_part_notion_and_github_isolation" not in tests:
    anchor = "    def test_p05_visual_scope_avoids_broad_ui_ux_globs(self) -> None:\n"
    if anchor not in tests:
        raise SystemExit("secondary test insertion anchor missing")
    one_chat_test = insert.split("    def test_p05_visual_scope_avoids_broad_ui_ux_globs", 1)[0].split("    def test_one_chat_one_part_notion_and_github_isolation", 1)[1]
    one_chat_test = "    def test_one_chat_one_part_notion_and_github_isolation" + one_chat_test
    tests = tests.replace(anchor, one_chat_test + anchor, 1)
test_path.write_text(tests, encoding="utf-8", newline="\n")

print("PARTITION_HYBRID_NOTION_GITHUB_ISOLATION_HARDENED")
