# GRILL_ME_DECISION_RECORD

> Grill Me 질문 하나의 근거·사용자 답변·승인 결정·반영 상태를 보존한다. 결정 기록·Flow/Wireframe·구조화 추적과 Commit은 V4 `REPOSITORY_PRIMARY_CANON`을 따른다. 사람용 PDF는 exact-SHA 파생본이고, Notion·Google Sheets는 `COMPATIBILITY_ONLY` legacy migration 또는 명시된 V4 exception에서만 사용한다.

```yaml
질문 ID: GRILL-ME-YYYY-NNN
Decision ID: DEC-YYYY-NNN
상태: DRAFT | USER_DECISION_REQUIRED | APPROVED_PENDING_MERGE | SYNCED_TO_MAIN | SUPERSEDED
Project:
Project relation:
Notion record:
Google Sheet compatibility source:
legacy_sheet_role: COMPATIBILITY_ONLY
```

## 1. 질문을 만든 이유

- 해결하려는 충돌/모호성:
- 저장소·책임 원본·현재 대화에서 이미 확인한 사실:
- 동일 Goal의 최근 병합 PR:
- read-only open/draft/ready PR과 overlap:
- 관련 Project Notion readback:
- legacy migration source가 실제 필요한가: YES / NO
- 사용자가 아니면 결정할 수 없는 이유:

## 2. 질문

**질문 ID:**

질문:

## 3. 선택지 비교

| 선택지 | 장점 | 비용/위험 | 되돌리기 | 장기 적합성 |
|---|---|---|---|---|
| A |  |  |  |  |
| B |  |  |  |  |
| C |  |  |  |  |

### GPT 권장안

- 권장:
- 이유:
- 반대 근거:
- 더 나은 대안 재탐색 결과:
- 재검토 조건:

## 4. 사용자 답변

- 사용자 답변 원문:
- 승인 시각/참조:

## 5. 최종 결정

- 최종 결정:
- 비타협 조건:
- 변경 가능한 요소:
- 제거·보류 요소:
- supersedes:
- revisit condition:

## 6. 반영 위치

```yaml
repository_primary_canon: REPOSITORY_PRIMARY_CANON
branch:
반영 Commit:
merge_commit:
human_gdd_pdf_derived_view:
notion_exception_or_legacy_source:
notion_record_url:
notion_project_relation:
notion_readback: PASS | NOT_APPLICABLE | BLOCKED_UNVERIFIED
google_sheet_compatibility_source:
legacy_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | ARCHIVED_APPROVED
```

V4 exception/migration scope에 실제 Notion 목적지가 있으면 정확한 `Project relation` record를 갱신한 뒤 **destination readback**한다. 그런 scope가 없으면 `NOT_APPLICABLE`로 기록하고 목적지를 만들지 않는다.

## 7. 상태 전이

```text
DRAFT
→ USER_DECISION_REQUIRED
→ 사용자 승인
→ GitHub 추적 + Branch 정본 반영
→ 필요하면 V4 exception/migration record 반영 및 destination readback
→ APPROVED_PENDING_MERGE
→ exact-head 검증·리뷰·merge
→ main readback + 필요했던 V4 exception/migration readback
→ SYNCED_TO_MAIN
```

legacy Google Sheets는 `COMPATIBILITY_ONLY`다. 아직 이관되지 않은 **UNIQUE** 정보가 있는 경우에만 migration input으로 읽고, 현행 Notion/Repository owner로 이관 → readback/Test → consumer/reference 확인 뒤 원본 수명주기를 판정한다. 신규 입력·활성 동기화 때문에 Sheet를 만들거나 갱신하지 않는다.

## 8. 비판 검증

- 이 질문은 저장소에서 이미 답을 찾을 수 있었는가:
- 기술 기본값으로 처리할 수 있었는가:
- 프로젝트 방향을 실제로 바꾸는가:
- 사용자 답을 특정 선택지로 유도했는가:
- 승인 후 다른 consumer가 빠졌는가:
- repository 정본과 파생 PDF 또는 실제 exception record가 의미상 충돌하는가:
- legacy Sheet를 active canon처럼 다시 취급했는가:

## 9. 승인 후 체크

- [ ] 동일 Decision ID를 Branch 정본에 기록했다.
- [ ] 반영 Commit을 기록했다.
- [ ] 실제 필요했던 V4 exception/migration record만 갱신했다.
- [ ] 필요한 destination readback을 완료했거나 `NOT_APPLICABLE` 근거를 남겼다.
- [ ] PR exact-head required checks를 확인했다.
- [ ] unresolved thread 0을 확인했다.
- [ ] 병합 후 exact merge SHA와 main을 재조회했다.
- [ ] 필요한 V4 exception/migration destination만 다시 재조회했다.
- [ ] Google Sheets가 `COMPATIBILITY_ONLY`를 넘어 active workspace로 승격되지 않았음을 확인했다.

## 10. 완료 조건

- 질문 ID, GPT 권장안, 사용자 답변, 최종 결정, 반영 Commit을 복원할 수 있다.
- 비타협 조건·변경 가능한 요소·제거·보류 요소가 분리된다.
- 승인 Decision이 대화 메모리에만 남지 않는다.
- V4 `REPOSITORY_PRIMARY_CANON`을 Notion/정적 파생본과 같은 권위로 오해하지 않는다.
- active Decision sync는 legacy Sheet의 존재나 쓰기 권한에 의존하지 않는다.
