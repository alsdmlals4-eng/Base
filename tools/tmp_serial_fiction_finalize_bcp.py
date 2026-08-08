from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BCP_ID = "BCP-2026-009-serial-fiction-writing-and-revision-discipline"
PR_URL = "https://github.com/alsdmlals4-eng/Base/pull/225"
PROPOSAL = ROOT / "[수정제안서]" / BCP_ID / "PROPOSAL.md"
REGISTRY = ROOT / "[수정제안서]" / "PROPOSAL_REGISTRY.json"


def main() -> None:
    text = PROPOSAL.read_text(encoding="utf-8")
    text = text.replace(
        "- 상태: `APPROVED_FOR_IMPLEMENTATION`",
        "- 상태: `IMPLEMENTED`",
        1,
    )
    text = text.replace(
        "- 구현 PR: `null` — 별도 구현 PR에서 연결한다.",
        f"- 구현 PR: {PR_URL}",
        1,
    )
    stale = (
        "구현은 이 lifecycle 변경이 병합된 뒤 최신 `main`에서 별도 PR로 시작한다. "
        "롤백은 BCP 상태와 Registry의 approval_ref를 함께 `SUBMITTED/null`로 되돌리면 된다."
    )
    current = (
        f"구현은 {PR_URL}에서 수행했다. 이 상태는 PR이 존재하고 전용 Skill·Knowledge·라우팅·behavior/evidence·계약 테스트가 구현된 것을 뜻하며, "
        "실제 독자 만족도·상업 성과까지 검증했다는 뜻은 아니다. 롤백은 구현 PR의 변경을 되돌리고 BCP 상태를 `APPROVED_FOR_IMPLEMENTATION`으로 복원한다."
    )
    if stale in text:
        text = text.replace(stale, current, 1)
    elif current not in text:
        marker = "동일 승인 범위는 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 따르되 새 범위·새 사용자 결정·P0/P1·검증 실패는 자동 승인으로 간주하지 않는다."
        if marker not in text:
            raise RuntimeError("approval section marker not found")
        text = text.replace(marker, marker + "\n\n" + current, 1)
    PROPOSAL.write_text(text, encoding="utf-8")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entry = next(item for item in registry["proposals"] if item["proposal_id"] == BCP_ID)
    entry["status"] = "IMPLEMENTED"
    entry["implementation_pr"] = PR_URL
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
