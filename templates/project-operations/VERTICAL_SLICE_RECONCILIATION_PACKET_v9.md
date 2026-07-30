# Vertical Slice v9 복원·감사 패킷

이 템플릿은 `RECONCILIATION_PLANNING_PROFILE`용이다. 사실·가정·미결정을 섞지 않고, 제품 파일과 Sheet 값을 변경하지 않는다.

## A. Baseline Recovery Record

| 항목 | 사실 | 증거 |
| --- | --- | --- |
| main 기준선 | `[SHA]` | `[remote/main]` |
| 현재 Gate | `[상태]` | `[정본]` |
| 구현/검증 | `[상태]` | `[테스트/파일]` |
| 보호 범위 | `[경로]` | `[adapter]` |
| Sheet | `[SYNCED/PROPOSED/NOT_CONFIGURED]` | `[ID/SHA]` |

## B. Legacy Requirement Traceability

| Legacy ID/문장 | 현재 책임 원본 | 판정 | 근거 | 후속 |
| --- | --- | --- | --- | --- |
| `[v6~v8 item]` | `[path/Decision]` | `CURRENT / LEGACY_REFERENCE_ALLOWED / CANON_CONFLICT / STALE_REFERENCE` | `[evidence]` | `[none/plan]` |

## C. Source / Consumer / Propagation Map

| 책임 원본 | 소비자 | 전파 대상 | 보호 여부 | 재조회 |
| --- | --- | --- | --- | --- |
| `[path]` | `[doc/skill/implementation]` | `[Sheet/Figma/Issue/test]` | `[yes/no]` | `[command or review]` |

## D. Finding Ledger

| ID | 종류 | 심각도 | 증거 | 상태 | 소유자 | 다음 Gate |
| --- | --- | --- | --- | --- | --- |
| `FND-001` | `DUPLICATE / OMISSION / CONFLICT / STALE` | `P0..P3` | `[link]` | `[open]` | `[role]` | `[gate]` |

## E. Readiness / Critical Gate

| 항목 | 상태 | 증거 | 차단 여부 |
| --- | --- | --- | --- |
| 핵심 플레이어 경험 | `[state]` | `[source]` | `[yes/no]` |
| 대표 화면·선택·피드백 | `[state]` | `[source]` | `[yes/no]` |
| 자동 검증 | `[PASS/NOT_RUN]` | `[test]` | `[yes/no]` |
| 런타임·사람·실기기 | `[NOT_RUN]` | `[reason]` | `[yes/no]` |

## F. Intermediate Visual Checkpoint + Screen Interpretation Review

```text
Screen purpose:
First glance:
Primary action:
Platform / resolution / aspect / input:
State · risk · cost · reward · success/failure/recovery:
Information hierarchy · Korean · accessibility:
Decision IDs / canonical sources:
Confirmed facts:
MISSING_CANON:
Art direction / alternatives (max 3):
Output: DRAFT_VISUAL | TEXT_WIREFRAME | MERMAID | FIGMA_FALLBACK
```

| Review class | 내용 | 다음 처리 |
| --- | --- | --- |
| Confirmed | `[정본과 일치]` | `[keep]` |
| `MISSING_CANON` | `[AI 가정/미결정]` | `[Decision]` |
| `VISUAL_CANONICAL_CONFLICT` | `[충돌 표현]` | `[reject/escalate]` |
| `TECHNICAL_REVIEW_PROPOSAL` | `[채택 후보 UX]` | `[feasibility]` |
| Rejected | `[버릴 표현과 이유]` | `[none]` |

## G. Approval Bundle / Change Plan

| 제안 | 이유 | 변경 대상 | 제외 범위 | 소비자 | 수용 기준 |
| --- | --- | --- | --- | --- | --- |
| `[proposal]` | `[finding]` | `[canon/implementation]` | `[protected paths]` | `[map]` | `[test + manual]` |
