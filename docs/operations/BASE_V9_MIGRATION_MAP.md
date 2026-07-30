# Base v9 Migration Map

## Rule

Open pull requests are evidence and proposals, not merge instructions. Their
unique requirements are re-evaluated against the v9 Registry, contracts, tests,
and migration evidence. This work does not directly merge PR #5, #18, #28, #29,
or #30.

열린 PR은 직접 병합하지 않는다. v9 계약과 현재 소비자, 검증 증거를 기준으로
필요한 책임만 흡수하거나 보류한다.

## Terminal status markers

- `[구현됨]`: PR의 고유 가치가 현행 책임 원본과 검증 경로에 반영된 terminal 상태다.
- `[구현됨]` 항목은 `do_not_reassess: true`를 유지하며, 새 회귀·새 충돌·대체 경로 소실 증거가 없는 한 다음 저장소 감사에서 다시 검토하지 않는다.
- 정확한 과거 문구나 파일 구조를 그대로 병합하지 않았더라도, 더 넓은 현행 계약이 동일한 목적과 보호 범위를 충족하면 `IMPLEMENTED_BY_CURRENT_CONTRACT`로 기록할 수 있다.
- 미채택·대체·보류 항목은 `[구현됨]`으로 표시하지 않는다. terminal 여부와 재검토 조건을 별도로 기록한다.

| Source | terminal marker | v9 disposition | Preserved value | Compatibility and migration requirement |
| --- | --- | --- | --- | --- |
| PR #5 | `[구현됨]` | `IMPLEMENTED_BY_CURRENT_CONTRACT` | 분야별 책임 원본, 변경 영향 라우팅, 최신 승인 이미지 관리 | 고정 5개 본책을 그대로 복원하지 않는다. 선택형 분야 Registry·`DOCUMENT_UPDATE_MATRIX`·이미지 승인 정책으로 더 넓게 구현됐으며 `do_not_reassess: true`를 적용한다. |
| PR #18 | — | `CONSOLIDATE_REVIEW` | Earlier Skill consolidation rationale, 11분야 카탈로그, 제안서·Workflow 유지보수 근거 | 현행은 11개 분야 강제 설치를 금지하고 선택형 카탈로그를 사용한다. Node 24 Action major 전환도 별도 제안 상태이므로 아직 `[구현됨]`이 아니다. |
| PR #28 | — | `ADOPT_AS_CONTRACT` | Handoff, provenance, and decision-surface requirements | Express as current contract fields and generated provenance rather than a blind file-level merge |
| PR #29 | — | `REASSESS_BOUNDARY` | Game-design specialization proposal | Add, split, absorb, or reject only after responsibility-overlap and lifecycle checks; record the final Registry decision |
| PR #30 | — | `ADOPT_AS_GATE` | PLAN→BUILD→REVIEW gate expectation | 현행은 단계 전환과 REVIEW 완료 증거를 보존하지만 모든 L1 작업에 3단계를 의무화하지 않는다. 정확한 요구의 채택 여부를 확정하기 전에는 `[구현됨]`으로 표시하지 않는다. |

PR #5의 기계 원장은 `docs/operations/GITHUB_OBJECT_LEDGER.json`이다. 현행 대체 경로와 회귀 검증이 사라지면 terminal 상태를 자동 유지하지 않고 새 finding으로 재개한다.

## Legacy disposition

Integrity findings and legacy materials use one of these dispositions before any
destructive action: `KEEP`, `CONSOLIDATE`, `ARCHIVE`, `RETIRE`, or `BLOCKED`.
Each record identifies consumers, replacement path, provenance, and rollback
instruction. A missing consumer audit or rollback path leaves the item `BLOCKED`.

## ROLLBACK

For a migration change, retain the prior identifier or document as an explicit
legacy alias until all known consumers have been migrated and the new generated
artifacts verify. To roll back, restore the prior mapping, regenerate outputs,
and rerun Registry, link, and consumer validation. Do not delete historical
evidence merely because an alias is retired.
