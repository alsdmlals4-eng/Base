# Project Google Sheet Workbook Contract — Legacy Migration Compatibility

> 이 파일은 **기존 프로젝트에 남아 있는 Google Sheets 고유 정보를 안전하게 이관하기 위한 호환 계약**이다. 새 프로젝트에 Sheet workbook을 만들거나 Google Sheets를 active project workspace로 운영하기 위한 계약이 아니다.

```yaml
workspace_status: MIGRATION_COMPATIBILITY_SURFACE
legacy_surface: GOOGLE_SHEETS
legacy_role: COMPATIBILITY_ONLY
canonical_authority:
  human: NOTION_HUMAN_FACING_CANON
  structured: REPOSITORY_STRUCTURED_CANON
new_sheet_creation: FORBIDDEN_BY_DEFAULT
active_dual_sync_required: false
```

## 1. 사용 조건

이 계약은 다음을 모두 만족할 때만 사용한다.

1. 실제 프로젝트에 기존 Google Sheet가 존재한다.
2. 아직 현행 Notion/Repository owner로 이관되지 않은 정보가 있을 가능성이 있다.
3. 해당 Sheet를 읽어 `UNIQUE / DUPLICATE / OBSOLETE` 판정하는 것이 현재 작업에 필요하다.

새 프로젝트 초기화, 새 기획 입력, 새 UI/Visual workspace, 새 Decision 기록을 위해 이 파일을 호출하지 않는다.

## 2. 판정

| 분류 | 의미 | 처리 |
|---|---|---|
| `UNIQUE` | 현행 owner에 없는 고유 정보 | 올바른 Notion/Repository owner로 이관 → readback/Test → consumer/reference 확인 |
| `DUPLICATE` | 현행 정본과 의미상 중복 | 현행 정본 확인 → active reference 0 확인 → Archive/제거 후보 |
| `OBSOLETE` | 더 이상 소비되지 않는 폐기 정보 | consumer 0 확인 → Archive/제거 후보 |

고유 여부를 확인하지 않은 파괴적 삭제는 금지한다.

## 3. 이관 목적지

```text
사람이 읽고 판단하는 계획·설명·결정·시각 자료
→ NOTION_HUMAN_FACING_CANON
→ 정확한 Project relation
→ destination readback

구조화 상태·Commit·runtime truth·실제 코드/데이터/씬/자산·검증
→ REPOSITORY_STRUCTURED_CANON
→ 관련 canonical owner / actual files
→ Test / readback
```

Figma, 외부 HTML workspace, 폐기된 custom local Tool/Hub를 이관 목적지로 사용하지 않는다.

## 4. Sheet 해석 원칙

- Sheet의 tab/row 구조는 **legacy representation**일 뿐 현재 시스템의 모듈 경계를 정의하지 않는다.
- 예전 `PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS` 같은 문서는 legacy 의미 해석에만 참고할 수 있으며 새 프로젝트 표준을 정의하지 않는다.
- Sheet에만 있는 사용자 수정은 즉시 폐기하지 않고 `UNIQUE` 후보로 보존해 현행 owner와 대조한다.
- Formula, named range, chart, hidden sheet처럼 표현 방식 자체에 의미가 있을 수 있으므로 값만 복사한 뒤 원본을 지우지 않는다.
- 충돌 시 최신 사용자 지시 → 프로젝트 정본/실제 파일 → 현재 Notion Project record → legacy Sheet 순으로 권위를 적용한다.

## 5. Migration flow

```text
legacy Sheet 식별
→ read-only inventory
→ tab/row/formula/chart 의미 분류
→ UNIQUE / DUPLICATE / OBSOLETE
→ UNIQUE만 정확한 현행 owner로 이관
→ destination readback
→ 관련 Test / consumer/reference 확인
→ migration receipt 기록
→ 원본 보존 필요성 재판정
→ 명시적으로 승인된 경우에만 Archive/제거
```

이관이 끝난 뒤에는 ongoing dual sync를 요구하지 않는다. 현행 Notion/Repository owner가 성공적으로 readback되고 consumer가 그 owner를 사용하면 legacy Sheet는 active authority가 아니다.

## 6. Migration receipt

```yaml
source_sheet:
source_scope:
classification: UNIQUE | DUPLICATE | OBSOLETE
material_summary:
target_owner:
target_record_or_path:
destination_readback: PASS | FAIL | NOT_RUN
related_tests: []
consumer_reference_check: PASS | FAIL | NOT_RUN
migration_status: NOT_STARTED | MIGRATED_READBACK_VERIFIED | BLOCKED_UNVERIFIED
archive_or_delete_authorized: false
rollback_source:
```

`MIGRATED_READBACK_VERIFIED`는 실제 목적지를 다시 읽고 필요한 Test/consumer 확인을 끝냈을 때만 사용한다.

## 7. 금지

- Google Sheets를 `USER_FACING_GDD_WORKSPACE`나 신규 기본 workspace로 재승격
- 신규 프로젝트에 Sheet tab 구조를 강제
- GitHub/Notion과 Sheet의 영구 양방향 sync를 완료 조건으로 강제
- Sheet를 신규 사용자 입력면으로 사용
- Sheet 데이터를 Figma/HTML/custom Tool Hub로 재이관
- `UNIQUE` 여부·consumer·rollback 확인 없이 원본 삭제
- 실제 readback/Test 없이 `SYNCED`, `MIGRATED`, `COMPLETE` 주장

## 8. 완료 조건

legacy Sheet를 다룬 작업은 다음을 만족해야 한다.

- source와 범위를 식별했다.
- `UNIQUE / DUPLICATE / OBSOLETE` 판정을 근거와 함께 남겼다.
- `UNIQUE`는 `NOTION_HUMAN_FACING_CANON` 또는 `REPOSITORY_STRUCTURED_CANON`의 정확한 owner로 이관했다.
- destination readback과 필요한 Test/consumer/reference 확인을 수행했다.
- 원본 Archive/제거는 별도 권한과 rollback을 가진다.
- Sheet를 active project workspace로 부활시키지 않았다.
