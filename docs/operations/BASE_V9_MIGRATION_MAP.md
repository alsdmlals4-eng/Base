# Base v9 Migration Map

## Rule

Open pull requests are evidence and proposals, not merge instructions. Their
unique requirements are re-evaluated against the v9 Registry, contracts, tests,
and migration evidence. This work does not directly merge PR #5, #18, #28, #29,
or #30.

구형 PR은 직접 병합하지 않는다. v9 계약과 현재 소비자, 검증 증거를 기준으로
필요한 책임만 흡수·대체하고 terminal 판정을 남긴다.

## Terminal status markers

- `[구현됨]`: PR의 고유 가치가 현행 책임 원본과 검증 경로에 반영된 terminal 상태다.
- `[대체됨]`: PR의 정확한 파일 구조·강제 범위·Skill 분리는 채택하지 않았지만, 보존할 가치와 남은 과제의 현행 책임 경로가 확정된 terminal 상태다.
- 두 terminal 상태 모두 `do_not_reassess: true`를 유지하며, 새 회귀·새 충돌·대체 경로 소실 증거가 없는 한 다음 저장소 감사에서 다시 검토하지 않는다.
- 과거 문구나 파일 구조를 그대로 병합하지 않았더라도 더 넓은 현행 계약이 동일한 목적과 보호 범위를 충족하면 `IMPLEMENTED_BY_CURRENT_CONTRACT`로 기록할 수 있다.
- terminal 상태를 되돌릴 때는 `docs/operations/GITHUB_OBJECT_LEDGER.json`의 replacement·verification 경로가 실제로 깨졌다는 증거를 먼저 남긴다.

| Source | terminal marker | resolution | 현행 판정과 대체 경로 |
| --- | --- | --- | --- |
| PR #5 | `[구현됨]` | `IMPLEMENTED_BY_CURRENT_CONTRACT` | 고정 5개 본책을 그대로 복원하지 않는다. 선택형 분야 Registry, `DESIGN_DOCUMENT_REGISTRY`, `DOCUMENT_UPDATE_MATRIX`, 이미지 승인 정책으로 더 넓게 구현했다. |
| PR #18 | `[대체됨]` | `SUPERSEDED_BY_CURRENT_CONTRACT` | 11개 분야 강제 설치는 현행의 선택형 카탈로그와 충돌해 채택하지 않았다. Proposal Registry는 현행에 남고 Node 24 Action 전환은 `BCP-2026-002`가 별도 책임진다. |
| PR #28 | `[구현됨]` | `IMPLEMENTED_BY_CURRENT_CONTRACT` | 구현 인계는 `implementation-package-handoff`, 플레이어 결정 표면은 UX/UI의 `screen_question·information_layers`, 파생본 출처·최신성은 Publication Manifest와 `derivative-freshness`로 구현했다. |
| PR #29 | `[대체됨]` | `SUPERSEDED_BY_CURRENT_CONTRACT` | 제안한 4개 Skill ID 분리는 채택하지 않았다. 컨셉·SWOT/VRIO·코어 루프·Why→How→What 책임을 `analyzing-and-refining-game-concepts`와 reference에 통합 유지한다. |
| PR #30 | `[대체됨]` | `SUPERSEDED_BY_CURRENT_CONTRACT` | 모든 L1에 3단계를 기계적으로 강제하지 않는다. 현행은 위험·규모 비례 Work Mode 전환과 증거 없는 완료 주장 금지로 목적을 보존한다. |

각 PR의 replacement path, verification path, 종료일과 `do_not_reassess` 값은 `docs/operations/GITHUB_OBJECT_LEDGER.json`이 기계 원본이다.

## Legacy disposition

Integrity findings and legacy materials use one of these dispositions before any
destructive action: `KEEP`, `CONSOLIDATE`, `ARCHIVE`, `RETIRE`, or `BLOCKED`.
Each record identifies consumers, replacement path, provenance, and rollback
instruction. A missing consumer audit or rollback path leaves the item `BLOCKED`.

## ROLLBACK

For a migration change, retain the prior identifier or document as an explicit
legacy alias until all known consumers have been migrated and the new generated
artifacts verify. To roll back a terminal PR disposition, restore its nonterminal
ledger record, identify the broken replacement or verification path, and rerun
Registry, link, consumer, generator, and focused regression validation. Do not
delete historical evidence merely because an alias or PR is retired.
