from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "governing-legacy-retention-and-archives"
SKILL_COMMIT = "d77888a23a37efe8a067b1574d0399ade798af1f"


def write_json_preserving_layout(path: Path, data: object) -> None:
    original = path.read_text(encoding="utf-8")
    compact = "\n" not in original.strip()
    if compact:
        rendered = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(rendered, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"expected text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def update_registry() -> None:
    path = ROOT / "skills/SKILL_REGISTRY.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    if not any(item["skill_id"] == SKILL_ID for item in registry["skills"]):
        registry["skills"].append(
            {
                "skill_id": SKILL_ID,
                "layer": "foundation",
                "discipline": "project-operations-knowledge-governance",
                "path": "skills/governing-legacy-retention-and-archives/SKILL.md",
                "status": "ACTIVE",
                "load_by_default": False,
                "trigger_tags": [
                    "legacy-retention",
                    "archive-policy",
                    "superseded-document",
                    "obsolete-plan",
                    "inactive-skill",
                    "backup-folder",
                    "blank-placeholder",
                    "branch-retention",
                    "archive-manifest",
                    "historical-evidence",
                ],
                "use_when": [
                    "구형 문서·Skill·증거·생성물·병합 브랜치를 원문과 복구 근거를 보존한 채 현재 정본·구현 권한·기본 라우팅에서 격리한다."
                ],
                "do_not_use_when": [
                    "현재 정본의 일반 편집, 단순 stale-reference 확인, 임시 빌드 산출물 청소 또는 비밀정보 보존 요청이다."
                ],
                "learning_log": "skills/SKILL_LEARNING_LOG.md",
                "review_triggers": [
                    "빈 파일 퇴역",
                    "metadata 없는 backup 이동",
                    "archive의 현재 정본 오염",
                    "inactive Skill 직접 라우팅",
                    "rollback ref 누락",
                    "비밀정보 archive",
                    "unique commit 감사 없는 branch 삭제",
                ],
                "last_reviewed_at": "2026-07-25",
                "last_reviewed_commit": SKILL_COMMIT,
                "knowledge_state": "PATTERN",
            }
        )
        write_json_preserving_layout(path, registry)


def update_coverage() -> None:
    path = ROOT / "skills/SKILL_COVERAGE.json"
    coverage = json.loads(path.read_text(encoding="utf-8"))
    if not any(
        item["id"] == "legacy-retention-and-archive-governance"
        for item in coverage["responsibilities"]
    ):
        coverage["responsibilities"].append(
            {
                "id": "legacy-retention-and-archive-governance",
                "skills": [SKILL_ID],
                "status": "COVERED",
            }
        )
        write_json_preserving_layout(path, coverage)


def update_structure_tests() -> None:
    path = ROOT / "tests/test_game_project_operating_system_structure.py"
    replace_once(
        path,
        '            "skills/pruning-stale-and-nonfunctional-material/SKILL.md",\n',
        '            "skills/pruning-stale-and-nonfunctional-material/SKILL.md",\n'
        '            "skills/governing-legacy-retention-and-archives/SKILL.md",\n'
        '            "skills/governing-legacy-retention-and-archives/references/archive-contract.md",\n'
        '            "skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md",\n',
    )
    replace_once(
        path,
        '            "schemas/skill-registry-v3.schema.json",\n',
        '            "schemas/skill-registry-v3.schema.json",\n'
        '            "schemas/archive-retention-adapter-v1.schema.json",\n'
        '            "schemas/archive-manifest-v1.schema.json",\n',
    )
    replace_once(
        path,
        '            "templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md",\n',
        '            "templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md",\n'
        '            "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",\n'
        '            "templates/project-operations/ARCHIVE_MANIFEST.json",\n'
        '            "templates/project-operations/ARCHIVE_README.md",\n'
        '            "templates/project-operations/github/check_archive_governance.py",\n',
    )
    replace_once(
        path,
        '            "tests/test_skill_system_coverage.py",\n',
        '            "tests/test_skill_system_coverage.py",\n'
        '            "tests/test_legacy_retention_archive_governance.py",\n',
    )
    replace_once(
        path,
        '        self.assertEqual(len(registry["skills"]), 25)\n',
        '        self.assertEqual(len(registry["skills"]), 26)\n',
    )
    replace_once(
        path,
        '            "managing-base-change-proposals",\n        }.issubset(seen))\n',
        '            "managing-base-change-proposals",\n'
        '            "governing-legacy-retention-and-archives",\n'
        '        }.issubset(seen))\n',
    )


def update_workflow() -> None:
    path = ROOT / ".github/workflows/validate-game-project-operating-system.yml"
    replace_once(
        path,
        '      - "tests/test_skill_system_coverage.py"\n',
        '      - "tests/test_skill_system_coverage.py"\n'
        '      - "tests/test_legacy_retention_archive_governance.py"\n',
    )
    replace_once(
        path,
        '            templates/project-operations/github/check_design_document_publications.py \\\n',
        '            templates/project-operations/github/check_design_document_publications.py \\\n'
        '            templates/project-operations/github/check_archive_governance.py \\\n',
    )
    replace_once(
        path,
        '            tests/test_skill_system_coverage.py \\\n',
        '            tests/test_skill_system_coverage.py \\\n'
        '            tests/test_legacy_retention_archive_governance.py \\\n',
    )
    replace_once(
        path,
        '            tests/test_skill_system_coverage.py \\\n            tests/test_game_project_operating_system_structure.py \\\n',
        '            tests/test_skill_system_coverage.py \\\n'
        '            tests/test_legacy_retention_archive_governance.py \\\n'
        '            tests/test_game_project_operating_system_structure.py \\\n',
    )


def update_skill_boundaries() -> None:
    append_once(
        ROOT / "skills/managing-game-project-operating-system/SKILL.md",
        "## Legacy retention boundary",
        """
## Legacy retention boundary

보존 위치, archive metadata, inactive Skill 호환, branch/tag retention 또는 원문 비우기 금지를 결정할 때는 **REQUIRED SUB-SKILL:** `governing-legacy-retention-and-archives`를 사용한다. 이 Skill은 inventory·migration 범위를 소유하지만 archive의 비권한 증명 계약을 장문 복제하지 않는다.
""",
    )
    append_once(
        ROOT / "skills/pruning-stale-and-nonfunctional-material/SKILL.md",
        "## Archive handoff",
        """
## Archive handoff

후보를 `ARCHIVE`로 판정한 뒤 보존 분류, 원문·metadata·Manifest, active authority 제거, secret·branch 경계는 **REQUIRED SUB-SKILL:** `governing-legacy-retention-and-archives`에 전달한다.
""",
    )
    append_once(
        ROOT / "skills/SKILL_LEARNING_LOG.md",
        "legacy-retention-archive-governance-2026-07-25",
        """
## legacy-retention-archive-governance-2026-07-25

- 날짜: 2026-07-25
- Skill: `governing-legacy-retention-and-archives`
- 근거: 구형 자료를 삭제하거나 비우지 않고 현재 권한에서 격리하는 공용 판단 계약이 여러 프로젝트에서 반복 필요했다.
- RED: coverage checker가 미등록 compact target을 거부한 Actions run `30160236473`의 `ubuntu-contract` 실패를 관찰했다.
- 수동 fresh-context pressure scenarios: `NOT_RUN` — 현재 대화 환경에 독립 실행 agent가 없음.
- 변경: 분류 8종, 원문 보존, Manifest·adapter, inactive Skill, 생성물, secret와 branch 경계를 공용 Foundation Skill로 분리했다.
- 지식 상태: `PATTERN`
""",
    )


def main() -> None:
    update_registry()
    update_coverage()
    update_structure_tests()
    update_workflow()
    update_skill_boundaries()


if __name__ == "__main__":
    main()
