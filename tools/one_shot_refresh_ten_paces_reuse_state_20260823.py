from __future__ import annotations

from pathlib import Path


MATRIX = Path("docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json")
HANDOFF = Path("docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    matrix = MATRIX.read_text(encoding="utf-8")
    matrix = replace_once(
        matrix,
        '"state": "DEFERRED_CONCURRENT_MAIN_CHURN",',
        '"state": "DEFERRED_PROJECT_WORK_GATE",',
        "Ten Paces manifest state",
    )
    matrix = replace_once(
        matrix,
        '"attempted_prs": [167, 169],',
        '"historical_attempted_prs": [167, 169],',
        "Ten Paces historical attempted PRs",
    )
    matrix = replace_once(
        matrix,
        '"observed_main_commits": [',
        '"historical_observed_main_commits": [',
        "Ten Paces historical observed main commits",
    )
    matrix = replace_once(
        matrix,
        '      "blocker": "manifest-only rollout deferred because concurrent planning main advanced twice while two TDD attempts were open; protected runtime paths still require an approved BUILD package",\n      "revisit": "after the concurrent planning wave stabilizes, re-read current main and install the manifest; runtime modules remain gated by an approved BUILD package"',
        '      "evidence": "historical manifest-only attempts #167/#169 were deferred during concurrent planning churn; current Ten Paces later stabilized and the first-five-duel Phase I–VI implementation was authorized and merged, so that churn is historical evidence rather than the current blocker",\n      "blocker": "Base reuse preinstallation remains intentionally unrun; adoption now requires a current approved project task, fresh main + exact Notion + open-PR overlap checks, and an actually consumed module",\n      "revisit": "during the next approved Ten Paces project task, re-read current main, exact Notion state and open PRs, then install or adapt only modules actually consumed by that task while preserving hidden-information and Human/device evidence boundaries"',
        "Ten Paces current blocker and revisit",
    )
    MATRIX.write_text(matrix, encoding="utf-8")

    handoff = HANDOFF.read_text(encoding="utf-8")
    handoff = replace_once(
        handoff,
        '"next_project_work_action": "After planning main stabilizes and an approved BUILD package exists, reuse hidden-plan, explainability, deterministic replay, UI, symbol, and telegraph contracts without exposing protected hidden information."',
        '"next_project_work_action": "Read current main + exact Notion state + open PRs first; the first-five-duel Phase I–VI is already implemented, so reuse hidden-plan, explainability, deterministic replay, UI, symbol, and telegraph contracts only when a current approved project task actually consumes them, without exposing protected hidden information or promoting Human/device evidence."',
        "Ten Paces current project-work handoff",
    )
    HANDOFF.write_text(handoff, encoding="utf-8")


if __name__ == "__main__":
    main()
