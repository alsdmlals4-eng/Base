# 정본·참조 최신성 감사

## 기준선

- Base commit:
- Head commit:
- 비교 diff:
- 활성 파일 범위:
- History·Legacy·Backup 제외 범위:

## 변경된 정본

| 정본 | 변경 유형 | 책임 | 이전 참조 | 현재 참조 |
|---|---|---|---|---|
|  | 추가/수정/이동/삭제/교체 |  |  |  |

## 영향 지도

| 정본 | 소비자·참조·파생본 | 관계 근거 | 갱신 필요 | 실제 변경 |
|---|---|---|---|---|
|  |  | Registry/Link/Import/ID/Generator | must-update/inspect/history-only/unrelated | changed/untouched |

## 오래된·고아 참조

| ID | 유형 | 파일 | 오래된 값 | 현재 값 | 근거 | 판정 |
|---|---|---|---|---|---|---|
| REF-001 | STALE_REFERENCE |  |  |  |  | BLOCKING/FIX_NOW/FOLLOW_UP/ALLOWED_LEGACY/FALSE_POSITIVE/UNVERIFIED |

## 내용 충돌·중복 정본

| ID | 책임 질문 | 정본 후보 | 충돌 내용 | 현행 판정 | 필요한 조치 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 파생본·Manifest·해시

| 원본 | 파생본·Manifest | 정책 | 입력 해시 | 출력 해시 | 렌더·실행 | 상태 |
|---|---|---|---|---|---|---|
|  |  | source_only/milestone_sync/always_sync |  |  | PASSED/FAILED/NOT_RUN | CURRENT/STALE/FAILED/UNVERIFIED |

## 변경 전파 누락

| 변경된 정본 | 변경됐어야 할 소비자 | Diff 포함 | 미변경 사유 | 판정 |
|---|---|---|---|---|
|  |  | yes/no |  |  |

## 허용된 Legacy·History

| 파일 | 이전 표현 | 유지 이유 | 실행 경로에서 제외됐는가 |
|---|---|---|---|
|  |  | Alias/Change Log/Case/Git history | yes/no |

## 자동 검사

```text
python tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base <base-sha> --head <head-sha>
```

- 결과:
- 스캔 파일 수:
- Legacy Alias 수:
- Changed file 수:
- 오탐·수동 검토:

## 실제 수정

| Finding | 수정 파일 | 수정 내용 | 검증 |
|---|---|---|---|
|  |  |  |  |

## 수정하지 않은 파일

| 파일 | 영향 후보였던 이유 | 수정하지 않은 근거 |
|---|---|---|
|  |  |  |

## 미검증·후속 작업

- 미검증:
- 별도 후속 작업:
- 사용자 결정 필요:
- 롤백:

## 최종 판정

- PASS
- PASS_WITH_FOLLOWUP
- CHANGES_REQUIRED
- BLOCKED
- UNVERIFIED
