from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "developing-and-revising-serial-fiction"
REVIEWED_HEAD = "200c1d4d6560c9c75c3b7b1aa00d59c8875284bf"


def replace_once(path: str, old: str, new: str) -> None:
    file_path = ROOT / path
    text = file_path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"expected text not found in {path}: {old!r}")
    file_path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    replace_once(
        "docs/OPERATING_MODEL.md",
        "Base는 게임 프로젝트가 다음을 저장소만으로 지속하도록 돕는다.",
        "Base는 게임·연재소설 등 등록된 창작·개발 프로젝트가 공용 작업 구조를 지속해서 재사용하도록 돕는다.",
    )
    replace_once(
        "docs/OPERATING_MODEL.md",
        "Base에는 여러 프로젝트에서 재사용 가능한 판단·절차·검증만 둔다. 프로젝트 고유 세계관·수치·경로·자산·구현 상태는 대상 프로젝트가 책임진다. 구성된 프로젝트 Google Sheets는 `USER_FACING_GDD_WORKSPACE`로 사용하며 상세 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다.",
        "Base에는 여러 프로젝트에서 재사용 가능한 판단·절차·검증만 둔다. 프로젝트 고유 세계관·원고·수치·경로·자산·구현 상태는 대상 프로젝트가 책임진다. 게임 프로젝트에 구성된 GDD Google Sheets는 `USER_FACING_GDD_WORKSPACE`로 사용하며 상세 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다. 연재소설 등 다른 분야의 프로젝트 문서·Sheet는 해당 프로젝트가 선언한 정본·문서 계약을 따른다.",
    )
    replace_once(
        "docs/DOCUMENTATION_MAP.md",
        "Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관·실제 수치·구현 상태·파일 경로·승인 자산·테스트 결과는 각 프로젝트 저장소가 책임진다.",
        "Base는 게임·연재소설 등 등록된 창작·개발 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관·원고·실제 수치·구현 상태·파일 경로·승인 자산·테스트 결과는 각 프로젝트가 선언한 책임 원본이 소유한다.",
    )

    test_path = ROOT / "tests/test_serial_fiction_discipline.py"
    test = test_path.read_text(encoding="utf-8")
    marker = '        for text in (start, docs, operating):\n            self.assertIn(SKILL_ID, text)\n'
    addition = (
        marker
        + '        self.assertIn("연재소설", operating)\n'
        + '        self.assertIn("연재소설", docs)\n'
        + '        self.assertNotIn("Base는 게임 프로젝트가", operating)\n'
        + '        self.assertNotIn("Base는 여러 게임 프로젝트가", docs)\n'
    )
    if 'self.assertNotIn("Base는 게임 프로젝트가", operating)' not in test:
        if marker not in test:
            raise RuntimeError("serial fiction cold-start test marker not found")
        test = test.replace(marker, addition, 1)
        test_path.write_text(test, encoding="utf-8")

    registry_path = ROOT / "skills/SKILL_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next(item for item in registry["skills"] if item["skill_id"] == SKILL_ID)
    entry["last_reviewed_at"] = "2026-08-08"
    entry["last_reviewed_commit"] = REVIEWED_HEAD
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    spec = importlib.util.spec_from_file_location(
        "base_builder", ROOT / "tools/build_base_v9_artifacts.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    _, skills = module.load_active_skills()
    registry_hash = module.sha256_normalized_text_file(registry_path)
    (ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md").write_text(
        module.generated_summary(skills, registry_hash), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
