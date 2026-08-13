#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_ID = "BCP-2026-027-claim-and-intent-verification-gate"
PR_URL = "https://github.com/alsdmlals4-eng/Base/pull/319"
FIRST_GREEN_HEAD = "eef62df811ae64ff92fa6692a3e91edb8a5e343b"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def update_registry() -> None:
    path = "[수정제안서]/PROPOSAL_REGISTRY.json"
    registry = json.loads(read(path))
    matches = [item for item in registry["proposals"] if item["proposal_id"] == PROPOSAL_ID]
    if len(matches) != 1:
        raise RuntimeError(f"expected one BCP-027 entry, found {len(matches)}")
    item = matches[0]
    if item["status"] not in {"APPROVED_FOR_IMPLEMENTATION", "IMPLEMENTED"}:
        raise RuntimeError(f"unexpected BCP-027 status: {item['status']}")
    item["status"] = "IMPLEMENTED"
    item["implementation_pr"] = PR_URL
    write(path, json.dumps(registry, ensure_ascii=False, indent=2) + "\n")


def update_proposal() -> None:
    path = "[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md"
    text = read(path)
    text = text.replace(
        "- Registry 상태: `APPROVED_FOR_IMPLEMENTATION`",
        "- Registry 상태: `IMPLEMENTED`",
        1,
    )
    stale = (
        "- 상태 설명: 신규 제안은 검사 규칙에 따라 `SUBMITTED`로 시작한다. "
        "`approval_ref`는 위 명시적 사용자 승인 증거의 위치를 가리키며, 구현 완료 상태와 "
        "`implementation_pr`은 별도 구현 PR의 검증·병합 단계에서 전환한다."
    )
    current = (
        "- 상태 설명: 제안은 `SUBMITTED`에서 시작해 사용자 승인과 별도 구현 PR의 "
        "exact-head GREEN을 거쳐 `IMPLEMENTED`로 전환했다. 병합 완료는 PR merged 상태, "
        "merge SHA, 새 `main` readback과 post-merge 검사가 확인된 뒤에만 별도로 주장한다."
    )
    if stale in text:
        text = text.replace(stale, current, 1)
    elif current not in text:
        raise RuntimeError("proposal lifecycle explanation anchor not found")

    marker = "### 구현 closeout — PR #319"
    if marker not in text:
        closeout = f"""

{marker}

- 구현 owner: `reviewing-and-validating-project-changes`
- 구현 방식: 새 ACTIVE Skill이 아닌 `claim-and-intent-verification` Skill Mode·reference·기존 Registry owner 확장
- 첫 완전 GREEN exact head: `{FIRST_GREEN_HEAD}`
- Base v9 workflow: `31698327204` — success; 328 tests passed, 1 Godot exact-engine test skipped as not configured; adversarial gate success
- Game Project Operating System workflow: `31698327106` — success; proposal validation, reference-freshness, 410 tests passed with 15 environment-bound skips, publication validation and `ci-gate` success
- 관련 workflow: evidence knowledge `31698327100`, visual/sheet `31698327110`, Skill behavior evidence `31698327112`, integrated vertical slice `31698327128`, game UX/UI `31698327132` — all success
- 행동 평가: `SBE-038` 계약·라우팅 회귀 PASS; 외부 model behavior run은 실행하지 않았으므로 `NOT_RUN`
- 동시 변경 preflight: current `main@e2c1d0c4b6fd0a7ce7874d200176d267a7d614d5`, PR #312와 changed-path intersection 0, implementation branch `behind_by=0`
- 보호 결과: ACTIVE Skill 30개와 `PLAN / BUILD / REVIEW` 유지; PR #312·#316 소유 경로 비변경
- 증거 원본: `docs/evidence/2026-08-13-claim-and-intent-verification-gate.md`
- 롤백: PR #319의 단일 squash merge commit을 revert한다. Registry metadata, generated views, Skill Mode/reference, Template·운영 문서, behavior fixture, learning/evidence records와 tests를 함께 되돌린다.
- 통합 경계: 이 closeout은 구현·exact-head 검증 완료를 기록한다. 실제 병합 완료는 merge SHA와 post-merge `main` readback 없이는 주장하지 않는다.
"""
        text = text.rstrip() + closeout
    write(path, text.rstrip() + "\n")


def update_evidence() -> None:
    path = "docs/evidence/2026-08-13-claim-and-intent-verification-gate.md"
    text = read(path)
    old = """## Final GREEN

- Exact head: `PENDING`
- Required workflow runs: `PENDING`
- Dedicated contract execution: `PENDING`
- Active Skill count and generated map: `PENDING`
- Independent adversarial review: `PENDING`
"""
    new = f"""## First complete exact-head GREEN

- Exact head: `{FIRST_GREEN_HEAD}`
- Required workflows: all success
  - Evidence-Based Game Development Knowledge: `31698327100`
  - BCA Visual and Sheet Workflow: `31698327110`
  - Skill Behavior Evidence: `31698327112`
  - Integrated Vertical Slice Prompt: `31698327128`
  - Game UX UI System: `31698327132`
  - Base v9 Operating Contracts: `31698327204`
  - Game Project Operating System: `31698327106`
- Base v9 contract evidence: generated artifacts current; integrity and v9.4.1/.2/.3 checks passed; 328 tests passed; 1 Godot exact-engine test skipped because the executable was not configured; adversarial gate passed.
- Game Project OS evidence: proposal validation passed for 27 proposals; reference-freshness passed across 749 scanned files and 23 changed files; 410 tests passed with 15 environment-bound skips; publication validation and `ci-gate` passed.
- Dedicated Claim/Intent contract: `6/6 PASS`.
- Registered consumer regressions and Skill behavior-evidence workflow: PASS.
- Active Skill count: 30; Work Modes: `PLAN / BUILD / REVIEW`; generated active map current.
- External model behavior run: `NOT_RUN`; no model-run success is claimed.
- Independent adversarial review: must be recorded as a PR review on the final exact head after this closeout commit.
"""
    if old in text:
        text = text.replace(old, new, 1)
    elif "## First complete exact-head GREEN" not in text:
        raise RuntimeError("final GREEN evidence anchor not found")

    closeout_marker = "## BCP lifecycle closeout"
    if closeout_marker not in text:
        text = text.rstrip() + f"""

{closeout_marker}

- Registry transition: `APPROVED_FOR_IMPLEMENTATION → IMPLEMENTED`
- Implementation PR: `{PR_URL}`
- Closeout production commit: `PENDING_USER_TRIGGER`
- Final exact-head workflows after closeout: `PENDING`
- Rollback: revert the eventual PR #319 squash merge commit; no product code/data or PR #312/#316 path is affected.
"""
    write(path, text.rstrip() + "\n")


def update_lifecycle_test() -> None:
    path = "tests/test_base_change_proposals.py"
    text = read(path)
    marker = "class ClaimIntentProposalLifecycleTests"
    if marker in text:
        return
    block = f'''

class ClaimIntentProposalLifecycleTests(unittest.TestCase):
    def test_bcp_027_closeout_binds_green_evidence_and_implementation_pr(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entry = next(
            item
            for item in registry["proposals"]
            if item["proposal_id"] == "{PROPOSAL_ID}"
        )
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertEqual("{PR_URL}", entry["implementation_pr"])
        proposal = (ROOT / entry["path"]).read_text(encoding="utf-8")
        evidence = (ROOT / "docs/evidence/2026-08-13-claim-and-intent-verification-gate.md").read_text(encoding="utf-8")
        for token in (
            "### 구현 closeout — PR #319",
            "{FIRST_GREEN_HEAD}",
            "External model behavior run: `NOT_RUN`",
            "post-merge `main` readback",
        ):
            self.assertIn(token, proposal + "\\n" + evidence)
'''
    anchor = '\n\nif __name__ == "__main__":'
    if anchor in text:
        text = text.replace(anchor, block + anchor, 1)
    else:
        text = text.rstrip() + block + "\n"
    write(path, text)


def main() -> int:
    update_registry()
    update_proposal()
    update_evidence()
    update_lifecycle_test()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
