from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md"


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    replace_once(
        "START_HERE.md",
        "`전부 살펴본다`는 모든 파일을 무작정 읽는 뜻이 아니다. 현재 작업에 필요한 책임 원본과 최소 스킬 집합을 Registry와 Documentation Map에서 선별한다.\n",
        "`전부 살펴본다`는 모든 파일을 무작정 읽는 뜻이 아니다. 현재 작업에 필요한 책임 원본과 최소 스킬 집합을 Registry와 Documentation Map에서 선별한다.\n\n"
        "상세 기획·Demo-First Vertical Slice·GPT→Codex·전체 검수 지시를 파일 하나로 첨부해야 할 때는 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`를 사용한다. 이 Prompt가 작업 시작 인터뷰를 수행하지만 최신 Base·프로젝트 정본보다 높은 권한을 갖지 않는다.\n",
    )
    replace_once(
        "START_HERE.md",
        "대표 플레이 구간으로 핵심 경험·목표 품질·접근성·성능·시스템 연결·실제 플레이 증거·제작 파이프라인을 함께 검증한다. 핵심 컨셉이나 뾰족한 재미가 미확정이면 먼저 `analyzing-and-refining-game-concepts`를 사용한다.\n",
        "대표 플레이 구간으로 핵심 경험·목표 품질·접근성·성능·시스템 연결·실제 플레이 증거·제작 파이프라인을 함께 검증한다. 핵심 컨셉이나 뾰족한 재미가 미확정이면 먼저 `analyzing-and-refining-game-concepts`를 사용한다. 상세 정본과 인터뷰·실행 계약을 한 파일로 첨부할 때는 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`를 사용한다.\n",
    )
    replace_once(
        "START_HERE.md",
        "코드·데이터·문서·자산 변경은 먼저 전체 영향 범위에서 수정·개선 후보를 적대적으로 찾고, 기술적으로 판단 가능한 사항은 근거·우선순위·영향 파일·수정 방향·검증 방법을 검수안으로 정리한다.",
        "저장소 전체의 누락·구형 파일·중복 정본·untouched 소비자·Prompt drift를 감사할 때는 `running-adversarial-review-and-refinement`의 `repository-wide-audit` mode를 사용한다. 검색 결과만으로 전수 검수를 주장하지 않고 tracked inventory 또는 미검증 범위를 기록한다.\n\n코드·데이터·문서·자산 변경은 먼저 전체 영향 범위에서 수정·개선 후보를 적대적으로 찾고, 기술적으로 판단 가능한 사항은 근거·우선순위·영향 파일·수정 방향·검증 방법을 검수안으로 정리한다.",
    )

    replace_once(
        "docs/DOCUMENTATION_MAP.md",
        "| 기획 작업순서·근거·데모 우선 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | 누락·충돌 선감사, 3층 근거 묶음, 분야별 Approval Bundle, 소비처 전파, 개별 프로젝트 Sheet tab, Demo-First Vertical Slice |\n",
        "| 기획 작업순서·근거·데모 우선 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | 누락·충돌 선감사, 3층 근거 묶음, 분야별 Approval Bundle, 소비처 전파, 개별 프로젝트 Sheet tab, Demo-First Vertical Slice |\n"
        "| Vertical Slice 통합 첨부 실행문 | `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | 상세 정본·저장소 우선 인터뷰·기획·Demo-First Slice·GPT→Codex·전체 감사·검증을 파일 하나로 첨부; 최신 Base·프로젝트 정본이 우선 |\n",
    )
    replace_once(
        "docs/DOCUMENTATION_MAP.md",
        "| 적대적 검토·비판 검증·개선·회귀 | `running-adversarial-review-and-refinement` | `attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report`; 병합 후 새 main·Decision·정본·Sheets 재검사 |",
        "| 적대적 검토·비판 검증·개선·회귀 | `running-adversarial-review-and-refinement` | `attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report`; 전체 파일·구형 계약·untouched 소비자는 `repository-wide-audit`; 병합 후 새 main·Decision·정본·Sheets 재검사 |",
    )

    replace_once(
        "templates/project-operations/README.md",
        "프로젝트 작업 중 원격 Base의 최신 상태를 암묵적으로 적용하지 않는다.\n",
        "프로젝트 작업 중 원격 Base의 최신 상태를 암묵적으로 적용하지 않는다.\n\n"
        "## 단일 첨부용 통합 실행문\n\n"
        "상세 기획 정본과 작업 인터뷰·Demo-First Vertical Slice·GPT→Codex·적대적 검토·완전성 감사를 파일 하나로 전달할 때는 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`를 첨부한다. 별도 축약 실행문은 필요하지 않다. Prompt는 프로젝트에 동기화된 Base 기준과 프로젝트 정본보다 높은 권한이 아니며 drift는 `STALE_PROMPT_CONTRACT`로 보고한다.\n",
    )

    replace_once(
        "skills/SKILL_LEARNING_LOG.md",
        "# Base Skill Learning Log\n",
        "# Base Skill Learning Log\n\n"
        "## 2026-07-28 — 통합 실행문과 저장소 전체 감사\n\n"
        "- **Trigger:** v6 상세 참고 계약과 축약 실행문을 한 파일로 통합하고, 전체 파일에서 누락·구형 계약·untouched 소비자를 검수해야 했다.\n"
        "- **Finding:** 새 광역 Skill을 추가하면 기존 적대적 검토·reference freshness·legacy governance와 책임이 중복된다. 또한 활성 Vertical Slice 오케스트레이션에는 별도 `CORE_POC` 흐름이 남았고 관련 계약 테스트는 CI에서 직접 소비되지 않았다.\n"
        "- **Decision:** `running-adversarial-review-and-refinement`에 `repository-wide-audit` mode와 전문 Reference를 추가하고, 상세 정본과 인터뷰를 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` 한 파일로 통합했다.\n"
        "- **Evidence:** Registry trigger, Migration Traceability, entrypoint, reference-freshness coupled rule, Demo-First·v6·v7 contract tests로 전파를 검증한다.\n"
        "- **Next trigger:** Prompt·Gate·Skill·Template 변경 뒤 활성 구형 용어 또는 untouched 소비자가 발견될 때 재감사한다.\n",
    )

    replace_once(
        "docs/CHANGELOG.md",
        "## Unreleased - Base audit and operating-contract consistency\n",
        "## Unreleased - Base audit and operating-contract consistency\n\n"
        "- v6 상세 참고 계약과 축약 실행문을 상세 정본 포함 단일 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`로 통합하고, 저장소 우선 인터뷰·Demo-First Slice·3층 Evidence Pack·Approval Bundle·GPT→Codex·완전성 감사를 연결했다. 적대적 검토에는 중복 Skill 없이 `repository-wide-audit` mode를 추가하고 활성 구형 계약·untouched 소비자·Prompt drift·파생본 최신성을 검수하도록 확장했다.\n",
    )


if __name__ == "__main__":
    main()
