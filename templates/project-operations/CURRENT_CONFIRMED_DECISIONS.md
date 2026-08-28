# CURRENT_CONFIRMED_DECISIONS

> 이 문서는 **현재 승인된 결정만 빠르게 복원**하기 위한 프로젝트 repository 정본 템플릿이다. 승인 Decision의 현재 의미·상태·Commit·consumer 반영은 `REPOSITORY_PRIMARY_PROJECT_CANON`이 소유한다. 사람용 상세 기획서 PDF는 exact repository commit의 `HUMAN_GDD_PDF_DERIVED_VIEW`이며 독립 정본이 아니다. 기존 Notion과 Google Sheets는 고유 미이관 자료가 있을 때만 읽는 `LEGACY_READ_ONLY_MIGRATION_SOURCE` / `COMPATIBILITY_ONLY` 자료다.

```yaml
project:
repository:
workspace_authority: REPOSITORY_PRIMARY_PROJECT_CANON
confirmed_decision_owner: CURRENT_CONFIRMED_DECISIONS.md
ai_canon_owner:
human_view: HUMAN_GDD_PDF_DERIVED_VIEW
asset_manifest_owner:
current_handoff_owner:
legacy_notion_project:
legacy_notion_project_key:
legacy_notion_role: LEGACY_READ_ONLY_MIGRATION_SOURCE
legacy_google_sheet_role: COMPATIBILITY_ONLY
status: ACTIVE
last_verified_main_sha:
last_repository_readback_at:
last_human_pdf_source_sha:
```

## 1. 현재 승인 Decision

| Decision ID | 상태 | 결정 | 대체/선행 | 영향 owner·consumer | Branch Commit | Merge Commit | 검증 상태 |
|---|---|---|---|---|---|---|---|
| DEC-YYYY-NNN | APPROVED_PENDING_MERGE / SYNCED_TO_MAIN / SUPERSEDED |  |  |  |  |  |  |

Decision 상세 기록:

```yaml
decision_id:
status:
summary:
user_approval_ref:
protected_meaning:
changeable_scope:
repository_paths_changed: []
consumers_affected: []
branch_commit:
merge_commit:
repository_readback: PASS | FAIL | BLOCKED_UNVERIFIED | NOT_RUN
implementation_status: DOCUMENTED | CONFIRMED | IMPLEMENTED | AUTOMATED_TEST_PASS | RUNTIME_VERIFIED | UX_VERIFIED | RELEASE_READY
human_pdf_source_sha:
human_pdf_sync: CURRENT | STALE_DERIVED_VIEW | NOT_APPLICABLE
legacy_notion_record_url:
legacy_notion_project_relation:
legacy_notion_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | BLOCKED_UNVERIFIED
legacy_google_sheet_compatibility_source:
legacy_sheet_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | ARCHIVED_APPROVED
supersedes: []
revisit_condition:
rollback:
```

## 2. Repository Decision sync 상태

```yaml
repository_primary_canon: REPOSITORY_PRIMARY_PROJECT_CANON
ai_canon_owner:
confirmed_decision_owner: CURRENT_CONFIRMED_DECISIONS.md
last_branch_commit:
last_merge_commit:
last_main_readback:
consumer_readback: PASS | FAIL | BLOCKED_UNVERIFIED | NOT_RUN
asset_manifest_readback: PASS | FAIL | NOT_APPLICABLE | BLOCKED_UNVERIFIED | NOT_RUN
human_pdf_view: HUMAN_GDD_PDF_DERIVED_VIEW
human_pdf_source_sha:
human_pdf_state: CURRENT | STALE_DERIVED_VIEW | NOT_APPLICABLE
legacy_notion_role: LEGACY_READ_ONLY_MIGRATION_SOURCE
legacy_sheet_role: COMPATIBILITY_ONLY
```

- 승인 Decision은 먼저 활성 Branch의 이 문서, AI canon, 분야 owner와 실제 consumer에 반영한다.
- repository write 성공만으로 끝내지 않고 exact path·내용·Commit·consumer를 다시 읽는다.
- 사람용 PDF가 필요한 Gate이면 동일 Decision ID와 exact source SHA로 새 PDF를 생성한다. PDF 생성은 Decision sync의 필수 단계가 아니라 파생 review 단계다.
- 신규 Notion page/database/write/upload/sync/readback은 승인 Decision 완료 조건이 아니다.
- Base 자체나 신규 프로젝트에서 legacy destination을 발명하지 않는다.

## 3. 미이관 legacy 자료

| Source ID | Source | 판정 | 현재 의미 | destination | provenance | destination readback | 처리 |
|---|---|---|---|---|---|---|---|
| LEGACY-001 |  | UNIQUE / DUPLICATE / OBSOLETE / BLOCKED_UNVERIFIED |  |  |  |  | MIGRATE / KEEP_READ_ONLY / ARCHIVE_APPROVED |

```text
UNIQUE
→ repository Decision/AI canon/actual asset owner 또는 비정본 Library reference로 이관
→ provenance
→ destination readback
→ consumer 확인
→ legacy read-only
```

- 읽지 못한 자료는 `BLOCKED_UNVERIFIED`이며 `DUPLICATE`나 `OBSOLETE`로 추정하지 않는다.
- `DUPLICATE`와 `OBSOLETE`도 active reference 0과 rollback을 확인하기 전 파괴적으로 삭제하지 않는다.
- legacy Sheet는 `COMPATIBILITY_ONLY`를 넘어 active Decision workspace로 재승격하지 않는다.

## 4. 중복 질문 방지

새 질문 전 확인 순서:

1. 최신 사용자 지시.
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context.
3. 이 문서의 승인 Decision.
4. 관련 AI canon·분야 owner·actual code/data/Scene/Resource/asset/test.
5. 같은 Goal의 최근 병합 PR과 read-only open PR.
6. 필요한 경우 exact source commit의 사람용 PDF.
7. 승인 근거가 legacy 자료에만 있을 가능성이 있을 때만 Notion/Sheet migration source.

이미 답이 있고 current repository와 일치하면 다시 묻지 않는다. 유효한 의미 충돌만 사용자 결정으로 승격한다.

## 5. 승인 직후 기록

```text
사용자 승인
→ Decision ID 생성 또는 재사용
→ 활성 Branch의 CURRENT_CONFIRMED_DECISIONS 갱신
→ AI canon·data/asset/UX owner·actual consumer 영향 반영
→ repository destination readback
→ logical commit
→ APPROVED_PENDING_MERGE
```

- PR 병합 전 `SYNCED_TO_MAIN`을 사용하지 않는다.
- 구현이 필요한 Decision은 `CONFIRMED`와 `IMPLEMENTED`를 분리한다.
- legacy 자료에 고유 승인 근거가 있으면 별도 migration evidence를 남긴다. 이것이 모든 Decision에 Notion write를 요구하는 것은 아니다.

## 6. 병합 후 readback

```text
squash merge
→ exact merge SHA
→ main의 Decision·AI canon·분야 owner 재조회
→ actual consumer와 구현·test/runtime evidence 확인
→ human PDF가 있는 경우 source SHA와 Decision ID drift 확인
→ legacy dependency counts 재계산 when applicable
→ SYNCED_TO_MAIN
```

불일치가 있으면 `BLOCKED_UNVERIFIED` 또는 `STALE_DERIVED_VIEW`로 두고 완료를 주장하지 않는다.

## 7. Post-change 검토

| 항목 | 상태 | 증거·조치 |
|---|---|---|
| exact-head required checks | PASS / FAIL / NOT_RUN |  |
| main readback | PASS / FAIL / BLOCKED_UNVERIFIED |  |
| Decision ID·내용·Commit 일치 | PASS / FAIL |  |
| owner·consumer readback | PASS / FAIL / NOT_RUN |  |
| human PDF source SHA | CURRENT / STALE_DERIVED_VIEW / NOT_APPLICABLE |  |
| asset manifest readback | PASS / FAIL / NOT_APPLICABLE |  |
| legacy Notion migration | PASS / BLOCKED_UNVERIFIED / NOT_APPLICABLE |  |
| legacy Sheet 재승격 없음 | PASS / FAIL |  |
| stale consumer/reference | 0 / N |  |
| unresolved thread | 0 / N |  |

## 8. Legacy compatibility aliases

다음 과거 token은 오래된 handoff·test·migration source를 찾기 위한 `LEGACY_DISCOVERY_ONLY` 별칭이다.

```text
NOTION_HUMAN_FACING_CANON
REPOSITORY_STRUCTURED_CANON
DOMAIN_SPLIT_CANON
```

이 token의 존재는 Notion을 현재 Decision write destination이나 완료 조건으로 복원하지 않는다.

## 9. 종료 조건

- 현재 승인 Decision을 과거 대화 없이 repository에서 복원할 수 있다.
- 승인 의미, Branch/Merge Commit, owner·consumer 영향과 evidence ceiling이 연결된다.
- `DOCUMENTED`, `CONFIRMED`, `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, `RELEASE_READY`가 구분된다.
- PDF가 있으면 같은 Decision ID와 exact source SHA를 사용하며 독립 정본이 아니다.
- legacy Notion/Sheet write 권한이나 존재에 active Decision sync가 의존하지 않는다.
- 실행하지 않은 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
