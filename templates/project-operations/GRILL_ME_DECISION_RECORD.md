# GRILL_ME_DECISION_RECORD

> Grill Me 질문 하나의 근거·선택지·사용자 답변·승인 Decision·repository 반영 상태를 보존한다. 현재 Decision 권위는 `REPOSITORY_PRIMARY_PROJECT_CANON`, 사람용 상세 검토본은 exact commit의 `HUMAN_GDD_PDF_DERIVED_VIEW`다. 기존 Notion과 Google Sheets는 고유 미이관 자료가 있을 때만 읽는 `LEGACY_READ_ONLY_MIGRATION_SOURCE` / `COMPATIBILITY_ONLY`다.

```yaml
question_id: GRILL-ME-YYYY-NNN
decision_id: DEC-YYYY-NNN
status: DRAFT | USER_DECISION_REQUIRED | APPROVED_PENDING_MERGE | SYNCED_TO_MAIN | SUPERSEDED
project:
repository:
source_branch:
source_commit:
repository_decision_owner: CURRENT_CONFIRMED_DECISIONS.md
ai_canon_owner:
human_pdf_view: HUMAN_GDD_PDF_DERIVED_VIEW
legacy_notion_record:
legacy_google_sheet_compatibility_source:
legacy_sheet_role: COMPATIBILITY_ONLY
```

## 1. 질문을 만든 이유

- 해결하려는 충돌·모호성:
- 플레이어·사용자 결과에 미치는 영향:
- repository owner와 실제 구현에서 이미 확인한 사실:
- 같은 Goal의 최근 병합 PR:
- read-only open/draft/ready PR과 overlap:
- 재사용 가능한 기존 결정·시스템·asset·evidence:
- legacy Notion/Sheet read가 실제 필요한가: YES / NO
- 기술 기본값이나 기존 승인으로 해결할 수 없는 이유:
- 사용자가 아니면 결정할 수 없는 이유:

질문 전에는 current repository에서 답을 찾는다. Notion을 기본 질문 근거로 요구하지 않는다.

## 2. 질문

**Question ID:**

질문:

- 이번 결정으로 바뀌는 것:
- 바뀌지 않는 보호 범위:
- 명시적 제외 범위:

## 3. 선택지 비교

| 선택지 | 플레이어·사용자 가치 | 구현·운영 비용 | 위험 | 되돌리기 | 장기 적합성 |
|---|---|---|---|---|---|
| A |  |  |  |  |  |
| B |  |  |  |  |  |
| C |  |  |  |  |  |

### GPT 권장안

- 권장:
- 이유:
- 반대 근거:
- ADOPT / ADAPT / REJECT:
- 더 나은 대안 재탐색 결과:
- evidence ceiling:
- 재검토 조건:

허수 대안으로 세 개를 채우지 않는다. 실질 대안이 둘뿐이면 그 이유를 남긴다.

## 4. 사용자 답변

- 사용자 답변 원문:
- 승인 시각·참조:
- 승인 범위:
- 승인하지 않은 범위:

## 5. 최종 결정

```yaml
decision_id:
summary:
player_or_user_outcome:
protected_meaning:
changeable_scope:
removed_or_deferred_scope:
supersedes: []
revisit_condition:
rollback:
```

## 6. Repository 반영 위치

```yaml
repository_primary_canon: REPOSITORY_PRIMARY_PROJECT_CANON
confirmed_decision_path: CURRENT_CONFIRMED_DECISIONS.md
ai_canon_path:
domain_owner_paths: []
consumer_paths: []
asset_manifest_entries: []
branch:
branch_commit:
merge_commit:
repository_readback: PASS | FAIL | BLOCKED_UNVERIFIED | NOT_RUN
consumer_readback: PASS | FAIL | BLOCKED_UNVERIFIED | NOT_RUN
human_pdf_source_sha:
human_pdf_sync: CURRENT | STALE_DERIVED_VIEW | NOT_APPLICABLE
legacy_notion_record_url:
legacy_notion_project_relation:
legacy_notion_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | BLOCKED_UNVERIFIED
legacy_google_sheet_compatibility_source:
legacy_sheet_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | ARCHIVED_APPROVED
```

- 승인 Decision은 같은 ID로 current Branch의 confirmed-decision owner, AI canon, 분야 owner와 실제 consumer에 반영한다.
- 신규 Notion record 작성·갱신·readback은 기본 Decision sync 단계가 아니다.
- 승인 근거가 legacy source에만 있거나 unique migration material이 있을 때만 migration checklist를 적용한다.
- 사람용 PDF가 필요한 Gate이면 같은 Decision ID와 exact source SHA를 사용한다.

## 7. 상태 전이

```text
DRAFT
→ USER_DECISION_REQUIRED
→ 사용자 승인
→ repository Decision ID와 current owners 반영
→ repository destination and consumer readback
→ logical commit
→ APPROVED_PENDING_MERGE
→ exact-head checks / review / unresolved thread 0 / safe squash merge
→ exact main Decision and consumer readback
→ optional human PDF source-SHA drift check
→ SYNCED_TO_MAIN
```

- `CONFIRMED`는 `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, `RELEASE_READY`를 자동 의미하지 않는다.
- legacy Google Sheets는 `COMPATIBILITY_ONLY`다. 고유 미이관 정보가 있을 때만 migration input으로 읽는다.

## 8. 비판 검증

- 이 질문은 repository에서 이미 답을 찾을 수 있었는가:
- 기술 기본값 또는 승인 범위로 처리할 수 있었는가:
- 프로젝트 방향·플레이어 결과를 실제로 바꾸는가:
- 사용자 답을 특정 선택지로 유도했는가:
- 선택지별 실제 trade-off를 같은 기준으로 비교했는가:
- 승인 후 누락된 owner·consumer·asset·test가 있는가:
- PDF나 대화에만 Decision이 남았는가:
- legacy Notion/Sheet를 active canon처럼 재승격했는가:
- 실행하지 않은 구현·test·runtime·UX를 완료로 표시했는가:

## 9. 승인 후 체크

- [ ] 동일 Decision ID를 Branch의 confirmed-decision owner에 기록했다.
- [ ] 관련 AI canon·data/UX/asset owner를 갱신했다.
- [ ] actual consumer 영향을 확인했다.
- [ ] Branch Commit을 기록했다.
- [ ] repository destination readback을 완료했다.
- [ ] PR exact-head required checks를 확인했다.
- [ ] unresolved thread 0을 확인했다.
- [ ] 병합 후 exact merge SHA와 main을 재조회했다.
- [ ] 필요한 사람용 PDF가 있으면 동일 Decision ID·source SHA를 확인했다.
- [ ] legacy Notion/Sheet를 새 active workspace로 만들지 않았다.
- [ ] 실행하지 않은 검증을 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남겼다.

## 10. Legacy compatibility aliases

다음 token은 오래된 record·test·migration source를 찾기 위한 `LEGACY_DISCOVERY_ONLY` 별칭이다.

```text
NOTION_HUMAN_FACING_CANON
REPOSITORY_STRUCTURED_CANON
DOMAIN_SPLIT_CANON
```

이 token은 current Decision write destination이나 완료 Gate가 아니다.

## 11. 완료 조건

- Question ID, Decision ID, GPT 권장안, 사용자 답변, 최종 결정과 repository Commit을 복원할 수 있다.
- 비타협 조건·변경 가능한 요소·제거·보류 요소가 분리된다.
- 승인 Decision이 대화 memory, PDF 또는 legacy workspace에만 남지 않는다.
- repository owner·consumer·evidence ceiling과 병합 전후 상태가 연결된다.
- active Decision sync는 Notion/Sheet 존재나 쓰기 권한에 의존하지 않는다.
