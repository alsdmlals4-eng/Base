# 폐기 프로젝트 작업면 흡수·제거 정책

이 문서는 더 이상 기본 프로젝트 작업면으로 사용하지 않는 **프로젝트 관리용 user-facing local/HTML/visual surface, Figma, Google Sheets**를 마지막으로 감사하고 고유 정보만 현행 owner로 옮긴 뒤 active routing에서 제거하는 방법을 정의한다.

## Machine contract

```text
DEPRECATED_PROJECT_SURFACE_ABSORB_THEN_REMOVE
PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED
EXTERNAL_HTML_WORKSPACE_RETIRED
GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL
FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY
QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED
GIT_HISTORY_IS_ROLLBACK_NOT_ACTIVE_CANON
NO_DEFAULT_READ_OF_RETIRED_SURFACE
```

## 1. 기본 작업면

```text
GPT
→ planning / research / review

Notion
→ human-facing Project Home / visual / asset / flow / confirmed human tables

GitHub repository
→ structured data / code / scene / resource / tracked assets / tests / runtime evidence

Codex
→ optional implementation/runtime executor when actually useful
```

프로젝트 기획·자산·UX·정본을 관리하기 위해 새 localhost/browser/desktop app 또는 standalone HTML dashboard를 기본 작업면으로 만들지 않는다.

## 2. 폐기 대상

### `PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED`

과거의 Tool Hub, Expression/Sprite 계열 프로젝트 관리·시각 작업면처럼 Notion/Repository로 대체된 user-facing local management surface는 신규 기본 경로가 아니다. 고유 capability가 남아 있는지 한 번 감사하고 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다.

### `EXTERNAL_HTML_WORKSPACE_RETIRED`

독립 HTML dashboard/catalog/기획 UI를 프로젝트 정본·기본 discovery surface로 유지하지 않는다. 단, 실제 game/runtime web asset, 문서 빌드 derived artifact, test fixture, 배포 산출물은 consumer가 다르므로 자동 삭제 대상이 아니다.

### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`

Google Sheets는 신규 기획·승인·상태관리의 입력면이 아니다.

```text
legacy Sheet
→ UNIQUE / DUPLICATE / OBSOLETE
→ UNIQUE human-facing meaning → exact Project Notion owner
→ UNIQUE structured/runtime meaning → repository owner
→ provenance / source locator 보존
→ destination readback
→ active consumer/reference count 확인
→ migrated unique material = 0
→ active Sheet routing/template/reference 제거
→ archive/trash/delete decision
```

고유 정보 여부를 확인하지 못하면 `BLOCKED_UNVERIFIED`이고 먼저 삭제하지 않는다.

### `FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY`

Figma는 신규 active visual workspace가 아니다. 과거 링크/asset에 UNIQUE provenance가 있으면 현재 Project Notion/Repository owner로 이관·readback한 뒤 active reference를 제거한다.

## 3. QA Evidence Studio는 폐기 프로젝트 작업면과 다르다

`QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED`

QA Evidence Studio는 프로젝트 기획·정본·Visual workspace가 아니라 **실제 PC 빌드의 체크리스트·화면 증거·PASS/FAIL/BLOCKED/NOT_RUN 판정을 exact Git commit에 묶는 specialist validation utility**다.

따라서 다음 조건을 유지하는 동안 retirement 대상에 포함하지 않는다.

- repository 안에 실제 implementation과 automated contract tests가 존재
- 프로젝트 정본/asset/runtime를 자동 수정하지 않음
- evidence ceiling을 넘는 PASS를 만들지 않음
- 외부 AI/API나 별도 유료 서비스가 필요 없음
- 실제 validation consumer가 존재

향후 이 조건이 사라지거나 repository-native/GitHub artifact만으로 동일 기능을 더 단순하게 완전히 대체할 수 있다는 검증된 증거가 생기면 그때 별도 retirement review를 수행한다.

## 4. 흡수 기준

흡수 가능:
- 현재 승인 결정과 충돌하지 않는 UNIQUE 기획 의미
- 다른 곳에 없는 provenance
- 재사용 가능한 workflow 원리
- evidence vocabulary / fail-closed rule
- 실제 소비 중인 schema/contract/test 원리

흡수 금지:
- 이미 Notion/repository에 있는 중복 표현
- superseded/rejected 결정
- tool-specific layout/port/session metadata
- 폐기 프로그램에만 필요한 helper state
- 과거 임시 snapshot

## 5. 삭제 Gate

```text
inventory exact surface
→ identify consumers
→ UNIQUE / DUPLICATE / OBSOLETE
→ migrate UNIQUE
→ destination readback
→ replace active references/tests
→ adversarial review
→ remove active surface
→ regression
→ exact-head PR gate
→ merge
→ postmerge search confirms active consumer/reference = 0
```

Git history는 rollback/audit history이지 active canon이 아니다. 역사 조사 필요성이 없는 한 삭제된 surface를 매 작업마다 다시 후보로 올리지 않는다.

## 6. 비용

현재 기본 유료 플랜은 `GPT_PRO` 하나다. Notion은 Free 범위를 먼저 사용한다. 추가 유료 기능은 실제 blocker·무료 대안·비용·장기 효과를 비교한 뒤 사용자 명시 승인이 있어야 한다.

## 7. 완료 판정

```yaml
retired_surface:
  unique_material_absorbed: true | false
  notion_readback: PASS | BLOCKED | NOT_APPLICABLE
  repository_readback: PASS | BLOCKED | NOT_APPLICABLE
  active_references_remaining: []
  files_removed: []
  retained_specialist_utilities: []
  rollback: Git history
  result: REMOVED | BLOCKED_UNVERIFIED | PARTIAL_RETIREMENT
```

`PARTIAL_RETIREMENT`에서 완료를 주장하지 않는다.
