from __future__ import annotations

import json
from pathlib import Path

proposal_path = Path("[수정제안서]/BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity/PROPOSAL.md")
proposal = proposal_path.read_text(encoding="utf-8")
proposal = proposal.replace("- 상태: `APPROVED_FOR_IMPLEMENTATION`", "- 상태: `IMPLEMENTED`")
proposal = proposal.replace(
    "- 구현 PR: `없음`",
    "- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/179`, `https://github.com/alsdmlals4-eng/Base/pull/181`",
)
proposal = proposal.replace(
    "- 활성 구현: `NOT_STARTED`",
    "- 활성 구현: `IMPLEMENTED_IN_BASE_STATIC_CONTRACTS`",
)
marker = "- 권한·무결성 구현 계획: `docs/superpowers/plans/2026-08-05-game-entitlement-integrity-drm-capability-pack.md`\n"
closure_lines = [
    marker.rstrip("\n"),
    "- Cloud Run 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/179`",
    "- Cloud Run 구현 병합 커밋: `dcc1a1bfa5f97a93351e2949e5aad04f06e9003d`",
    "- 권한·무결성 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/181`",
    "- 권한·무결성 구현 병합 커밋: `6ce0e5375f9ad1a0a56a337b7e4813f0296e3e0c`",
    "- Base 정적 구현 완료 범위: Guide·Template·기존 owner route·전용 계약/반례 test·reference freshness·Learning Log·Changelog",
    "- 생명주기 판정: `IMPLEMENTED`",
]
if closure_lines[1] not in proposal:
    if marker not in proposal:
        raise RuntimeError("implementation plan marker not found")
    proposal = proposal.replace(marker, "\n".join(closure_lines) + "\n", 1)
proposal_path.write_text(proposal, encoding="utf-8")

registry_path = Path("[수정제안서]/PROPOSAL_REGISTRY.json")
registry = json.loads(registry_path.read_text(encoding="utf-8"))
for item in registry["proposals"]:
    if item["proposal_id"] == "BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity":
        item["status"] = "IMPLEMENTED"
        item["implementation_pr"] = "https://github.com/alsdmlals4-eng/Base/pull/181"
        break
else:
    raise RuntimeError("BCP-2026-007 registry item not found")
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
