from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
model_path = ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md"
worker_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md"
integration_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md"
test_path = ROOT / "tests/test_base_partition_contract.py"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["operating_mode"] = {
    "policy": "PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION",
    "daily_default": "UNIFIED_BASE",
    "partition_activation": "MATERIAL_AUDIT_SPECIALIZATION_LEARNING_OR_CONFLICT_BOUNDARY",
    "activate_only_relevant_parts": True,
    "run_all_parts_for_every_task": False,
    "integration_returns_to_one_base": True,
}

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
integration_prompt_path.write_text(integration, encoding="utf-8", newline="\n")

tests = test_path.read_text(encoding="utf-8")
needle = "    def test_each_part_has_a_context_pack_and_operational_contract(self) -> None:\n"
insert = '''    def test_hybrid_partition_mode_keeps_one_unified_base(self) -> None:\n        manifest = self.load_manifest()\n        mode = manifest["operating_mode"]\n        self.assertEqual("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", mode["policy"])\n        self.assertEqual("UNIFIED_BASE", mode["daily_default"])\n        self.assertTrue(mode["activate_only_relevant_parts"])\n        self.assertFalse(mode["run_all_parts_for_every_task"])\n        self.assertTrue(mode["integration_returns_to_one_base"])\n        for path in (OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT):\n            text = path.read_text(encoding="utf-8")\n            self.assertIn("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", text)\n\n    def test_p05_visual_scope_avoids_broad_ui_ux_globs(self) -> None:\n        manifest = self.load_manifest()\n        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")\n        for broad in ("docs/knowledge/game-development/*UI*", "docs/knowledge/game-development/UI_*", "docs/knowledge/game-development/*UX*"):\n            self.assertNotIn(broad, p05["owned_write_paths"])\n        self.assertIn("docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md", p05["owned_write_paths"])\n        self.assertIn("docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md", p05["owned_write_paths"])\n\n'''
if "def test_hybrid_partition_mode_keeps_one_unified_base" not in tests:
    if needle not in tests:
        raise SystemExit("test insertion anchor missing")
    tests = tests.replace(needle, insert + needle, 1)
test_path.write_text(tests, encoding="utf-8", newline="\n")

print("PARTITION_HYBRID_BOUNDARY_HARDENED")
