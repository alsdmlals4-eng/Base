#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_RED_HEAD = "bf0890439cbef96777171cc00a0229c65e852af8"
CANONICAL_RED_RUN = "31657742630"
STALE_RED_MARKERS = (
    "9a4a6e688e993114466e3f25831555b23fcf5912",
    "8a161eca8d129584aecb3898e8d5622dcfc89efb",
    "31656590653",
    "94312314139",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"missing {label} anchor")
    if text.count(old) != 1:
        raise RuntimeError(f"ambiguous {label} anchor: {text.count(old)}")
    return text.replace(old, new, 1)


def update_proposal() -> None:
    path = "[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md"
    text = read(path)
    text = replace_once(
        text,
        "- 구현 PR: 아직 없음",
        "- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/319`",
        "proposal implementation PR",
    )
    write(path, text)


def update_plan() -> None:
    path = "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md"
    text = read(path)
    old = """**Recorded RED**

- initial test commit: `9a4a6e688e993114466e3f25831555b23fcf5912`
- canonical aggregation commit: `8a161eca8d129584aecb3898e8d5622dcfc89efb`
- Game Project OS run: `31656590653`
- docs-validation job: `94312314139`
- result: 113 tests, exactly 6 new-contract failures; existing listed contracts passed before those failures
"""
    new = f"""**Recorded RED — canonical PR #319**

- exact RED head: `{CANONICAL_RED_HEAD}`
- Game Project Operating System run: `{CANONICAL_RED_RUN}`
- result: existing contracts reached the dedicated suite and exactly 6 new Claim/Intent assertions failed because the production Mode, reference, Registry routing, Template/workflow integration, `SBE-038`, and central learning record were absent
- additional finding: 3 trailing-whitespace defects in this plan were detected and removed before GREEN
- superseded evidence: PR #317 was closed unmerged and its earlier RED identifiers are not implementation authority for PR #319
"""
    text = replace_once(text, old, new, "plan RED evidence")
    write(path, text)


def update_design() -> None:
    path = "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md"
    text = read(path)
    old = """`tests/test_claim_and_intent_verification_contract.py`를 먼저 추가하고, 기존 CI가 새 파일을 실행하지 않는 문제를 발견했다. 이미 docs·contract suite에서 실행되는 `tests/test_repository_governance_baseline.py`에 전용 test case를 import해 canonical suites에 연결했다.

Exact RED head `8a161eca8d129584aecb3898e8d5622dcfc89efb`의 docs-validation은 기존 계약을 통과한 뒤 새 Gate 계약 6개만 실패했다.
"""
    new = f"""`tests/test_claim_and_intent_verification_contract.py`를 production 변경보다 먼저 배치하고, 기존 always-run governance suite가 전용 test case를 실행하도록 연결했다. 폐기된 PR #317의 초기 test-discovery 실험은 구현 권한으로 재사용하지 않았다.

Canonical PR #319의 exact RED head `{CANONICAL_RED_HEAD}`와 Game Project Operating System run `{CANONICAL_RED_RUN}`은 기존 계약을 거쳐 전용 suite에 도달한 뒤, production Mode·reference·Registry routing·Template/workflow integration·`SBE-038`·중앙 Learning Log가 없다는 6개 계약만 의도대로 실패했다. 같은 run에서 plan의 trailing whitespace 3건도 별도 형식 결함으로 검출했다.
"""
    text = replace_once(text, old, new, "design RED evidence")
    write(path, text)


def update_regression() -> None:
    path = "tests/test_base_change_proposals.py"
    text = read(path)
    anchor = '''        evidence = (ROOT / "docs/evidence/2026-08-13-claim-and-intent-verification-gate.md").read_text(encoding="utf-8")
        for token in (
'''
    replacement = f'''        evidence = (ROOT / "docs/evidence/2026-08-13-claim-and-intent-verification-gate.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md").read_text(encoding="utf-8")
        design = (ROOT / "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md").read_text(encoding="utf-8")
        self.assertNotIn("구현 PR: 아직 없음", proposal)
        self.assertIn("{CANONICAL_RED_HEAD}", plan + "\\n" + design)
        for stale in {STALE_RED_MARKERS!r}:
            self.assertNotIn(stale, plan + "\\n" + design)
        for token in (
'''
    text = replace_once(text, anchor, replacement, "lifecycle regression")
    write(path, text)


def verify_targets() -> None:
    proposal = read("[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md")
    plan = read("docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md")
    design = read("docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md")
    if "구현 PR: 아직 없음" in proposal:
        raise RuntimeError("stale proposal implementation state remains")
    if CANONICAL_RED_HEAD not in plan or CANONICAL_RED_HEAD not in design:
        raise RuntimeError("canonical PR #319 RED evidence is missing")
    for marker in STALE_RED_MARKERS:
        if marker in plan or marker in design:
            raise RuntimeError(f"stale PR #317 RED marker remains: {marker}")


def main() -> int:
    update_proposal()
    update_plan()
    update_design()
    update_regression()
    verify_targets()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
