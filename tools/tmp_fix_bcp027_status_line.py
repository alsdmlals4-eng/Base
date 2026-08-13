#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proposal_path = ROOT / "[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md"
    proposal = proposal_path.read_text(encoding="utf-8")
    old = "- 신규 제안 Registry 상태: `SUBMITTED`"
    new = "- 최종 Registry 상태: `IMPLEMENTED`"
    if old in proposal:
        if proposal.count(old) != 1:
            raise RuntimeError(f"ambiguous proposal status anchor: {proposal.count(old)}")
        proposal = proposal.replace(old, new, 1)
    elif new not in proposal:
        raise RuntimeError("proposal status anchor not found")
    proposal_path.write_text(proposal, encoding="utf-8")

    test_path = ROOT / "tests/test_base_change_proposals.py"
    test = test_path.read_text(encoding="utf-8")
    anchor = '        self.assertNotIn("구현 PR: 아직 없음", proposal)\n'
    addition = (
        anchor
        + '        self.assertNotIn("신규 제안 Registry 상태: `SUBMITTED`", proposal)\n'
        + '        self.assertIn("최종 Registry 상태: `IMPLEMENTED`", proposal)\n'
    )
    if 'self.assertNotIn("신규 제안 Registry 상태: `SUBMITTED`", proposal)' not in test:
        if test.count(anchor) != 1:
            raise RuntimeError(f"lifecycle test anchor count: {test.count(anchor)}")
        test = test.replace(anchor, addition, 1)
    test_path.write_text(test, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
