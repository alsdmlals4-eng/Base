# CURRENT_CONFIRMED_DECISIONS

> 이 문서는 **현재 승인된 결정만 빠르게 복원**하기 위한 프로젝트 운영 템플릿이다. 현재 승인 결정·설명·Flow/Wireframe·구조화 상태·Commit·실행 진실은 V4 `REPOSITORY_PRIMARY_CANON`을 따른다. 사람용 PDF는 exact-SHA `HUMAN_GDD_PDF_DERIVED_VIEW`이며, Notion과 Google Sheets는 legacy migration 또는 명시된 V4 exception에서만 사용하고 신규 입력이나 active sync 정본이 아니다.

```yaml
project:
repository:
notion_project:
notion_project_key:
workspace_authority: DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
repository_primary_canon: REPOSITORY_PRIMARY_CANON
human_gdd_pdf_derived_view:
notion_exception_or_legacy_source:
google_sheet_compatibility_source:
legacy_sheet_role: COMPATIBILITY_ONLY
status: ACTIVE
last_verified_main_sha:
last_notion_readback_at:
```

## 1. 현재 승인 Decision

| Decision ID | 상태 | 결정 | 대체/선행 | 반영 Commit | Notion 기록 | GitHub 추적 |
|---|---|---|---|---|---|---|
| DEC-YYYY-NNN | APPROVED_PENDING_MERGE / SYNCED_TO_MAIN / SUPERSEDED |  |  |  |  |  |

Decision 상세 기록은 다음 필드를 사용한다.

```yaml
decision_id:
status:
summary:
user_approval_ref:
branch_commit:
merge_commit:
notion_record_url:
notion_project_relation:
notion_readback: PASS | NOT_APPLICABLE | BLOCKED_UNVERIFIED
google_sheet_compatibility_source:
legacy_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | ARCHIVED_APPROVED
supersedes: []
revisit_condition:
```

## 2. Repository·derived human view 동기화 상태

```yaml
repository_primary_canon: REPOSITORY_PRIMARY_CANON
human_gdd_pdf_derived_view:
last_branch_commit:
last_merge_commit:
last_main_readback:
notion_project:
last_notion_readback_at:
notion_readback_status: PASS | NOT_APPLICABLE | BLOCKED_UNVERIFIED
legacy_google_sheet_role: COMPATIBILITY_ONLY
```

- Base 자체 작업처럼 프로젝트 Notion 목적지가 적용되지 않으면 `NOT_APPLICABLE`을 기록하고 목적지를 발명하지 않는다.
- 프로젝트 결정·Flow/Wireframe·구조화 상태·Commit·실제 구현은 Repository가 소유한다.
- V4 exception/migration scope에서 실제 Notion write가 있었다면 정확한 Project relation의 record를 갱신하고 **destination readback**한다. 그런 scope가 없으면 `NOT_APPLICABLE`로 기록한다.
- legacy Sheet는 아직 이관되지 않은 **UNIQUE** material이 있을 때만 `google_sheet_compatibility_source`로 읽는다. Sheet 행 갱신은 active Decision sync 완료 조건이 아니다.

## 3. 미이관 legacy 자료

| Source | 판정 | 현행 owner | 이관 증거 | consumer/reference 상태 | 처리 |
|---|---|---|---|---|---|
|  | UNIQUE / DUPLICATE / OBSOLETE |  |  |  | MIGRATE / KEEP_COMPATIBILITY / ARCHIVE_APPROVED |

`UNIQUE`는 올바른 Notion/Repository owner로 이관 → destination readback/Test → consumer/reference 확인 뒤에만 원본 수명주기를 판정한다. `DUPLICATE`와 `OBSOLETE`도 active reference 0과 복구 경로를 확인하기 전에는 파괴적으로 삭제하지 않는다.

## 4. 중복 질문 방지

새 질문을 만들기 전에 다음 순서로 확인한다.

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`·`START_HERE`·Active Context
3. 이 문서의 승인 Decision
4. 동일 Goal의 최근 병합 PR과 read-only open PR
5. 관련 분야 정본·실제 코드/데이터/씬/자산/Test
6. 적용 가능한 V4 exception/migration Notion 기록
7. `UNMIGRATED_UNIQUE_MATERIAL`이 있는 경우에만 legacy Sheet compatibility source

이미 답이 있으면 다시 묻지 않는다. 충돌이 있을 때만 사용자 결정으로 승격한다.

## 5. 승인 직후 기록

```text
사용자 승인
→ Decision ID 생성/재사용
→ GitHub 추적 surface
→ 활성 Branch의 CURRENT_CONFIRMED_DECISIONS + 분야 정본
→ 필요하면 V4 exception/migration destination write와 readback
→ 논리 Commit
→ APPROVED_PENDING_MERGE
```

PR 병합 전에는 `SYNCED_TO_MAIN`을 사용하지 않는다.

## 6. 병합 후 readback

```text
merge
→ exact merge SHA
→ main의 Decision/분야 정본 재조회
→ 실제 구현·consumer 영향 재확인
→ 필요하면 V4 exception/migration destination 재조회
→ repository 정본과 파생 PDF/예외 record 의미 일치 확인
→ SYNCED_TO_MAIN
```

불일치가 있으면 `BLOCKED_UNVERIFIED`로 두고 완료를 주장하지 않는다.

## 7. Post-change 검토

| 항목 | 상태 | 증거/조치 |
|---|---|---|
| exact-head required checks | PASS / FAIL / NOT_RUN |  |
| main readback | PASS / FAIL |  |
| V4 exception/migration destination readback | PASS / NOT_APPLICABLE / FAIL |  |
| Decision ID/내용/Commit 일치 | PASS / FAIL |  |
| legacy Sheet 재승격 없음 | PASS / FAIL |  |
| stale consumer/reference | 0 / N |  |
| unresolved thread | 0 / N |  |

## 8. 종료 조건

- 현재 승인 Decision을 과거 대화 없이 복원할 수 있다.
- `REPOSITORY_PRIMARY_CANON`과 파생 PDF/legacy source의 역할이 섞이지 않는다.
- 적용 가능한 사람용 변경은 repository owner와 exact-SHA derived view readback을 가지며, 실제 exception/migration write만 destination readback을 가진다.
- `COMPATIBILITY_ONLY` Sheet는 active workspace로 재승격되지 않는다.
- 병합 전/후 상태와 Commit이 구분된다.
- 실행하지 않은 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
