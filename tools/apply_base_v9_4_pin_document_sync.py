#!/usr/bin/env python3
"""Synchronize Base v9.4 proposal and changelog text after pin finalization."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = "a728712cb776ec98f4875914a580fcf7d0156593"
EVIDENCE = "ef1fba11167e4da0b298123b0c85ebd268191a42"
REGISTRY = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_all(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)
    marker = "## Base v9.4 릴리스 완료"
    if marker not in text:
        text += f"""

{marker}

- 상태: `IMPLEMENTED`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/118`
- payload commit: `{PAYLOAD}`
- trusted evidence PR: `https://github.com/alsdmlals4-eng/Base/pull/120`
- trusted evidence commit: `{EVIDENCE}`
- Registry SHA-256: `{REGISTRY}`
- pin-finalization: `base-v9.4.lock.json`의 `BASE_RELEASED` 상태
- 프로젝트 적용: Base 릴리스와 분리된 프로젝트별 Issue·Branch·PR에서 수행
- 증거 상한: provider billing·cache hit·실제 절감, Godot runtime 모션·성능, 사람 UI 이해·피로는 각 적용 환경에서 별도 검증
"""
    write(path, text)


def main() -> int:
    proposals = [
        ROOT / "[수정제안서]/BCP-2026-003-ai-model-prompt-cost-optimization/PROPOSAL.md",
        ROOT / "[수정제안서]/BCP-2026-004-ai-instruction-context-ui-motion/PROPOSAL.md",
    ]
    replacements = [
        ("- 상태: `APPROVED_FOR_IMPLEMENTATION`", "- 상태: `IMPLEMENTED`"),
        ("- 제안 상태: `SUBMITTED` — 신규 제안은 제안 PR에서 이 상태로 시작한다.", "- 최종 상태: `IMPLEMENTED`"),
        ("- 사용자 승인 근거는 존재하지만 기계 상태 전환은 별도 구현 PR에서 수행한다.", "- 승인·구현·trusted evidence·pin-finalization은 분리된 PR로 완료됐다."),
        ("- 구현 상태 전환: 제안 PR 병합 후 별도 v9.4 구현 PR에서 `APPROVED_FOR_IMPLEMENTATION`과 `approval_ref`를 기록한다.", "- 구현 상태: PR #118에서 구현되고 trusted evidence PR #120 뒤 pin-finalization됐다."),
        ("- 구현 PR: `없음 — 제안 PR과 분리 예정`", "- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/118`"),
    ]
    for path in proposals:
        replace_all(path, replacements)

    changelog = ROOT / "docs/CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    marker = "### Base v9.4 released pins"
    if marker not in text:
        text += f"""

{marker}

- Finalized Base v9.4 as `BASE_RELEASED`.
- Payload: `{PAYLOAD}`.
- Trusted evidence: `{EVIDENCE}`.
- Registry SHA-256: `{REGISTRY}`.
- BCP-2026-003 and BCP-2026-004 transitioned to `IMPLEMENTED`.
- Project adoption remains a separate post-release wave.
"""
    write(changelog, text)
    print("Base v9.4 pin documents synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
