# 폐기 프로젝트 작업면 흡수·제거 정책

이 문서는 더 이상 기본 프로젝트 작업면으로 사용하지 않는 **프로젝트 관리용 user-facing local/HTML/visual surface, Figma, Google Sheets, project-management Tool Hub, QA Evidence Studio**를 마지막으로 감사하고 고유 정보만 현행 owner로 옮긴 뒤 active routing에서 제거하는 방법을 정의한다.

## Machine contract

```text
DEPRECATED_PROJECT_SURFACE_ABSORB_THEN_REMOVE
PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED
EXTERNAL_HTML_WORKSPACE_RETIRED
GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL
FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY
TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW
QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW
REPOSITORY_NATIVE_EVIDENCE_CAPTURE
GIT_HISTORY_IS_ROLLBACK_NOT_ACTIVE_CANON
NO_DEFAULT_READ_OF_RETIRED_SURFACE
```

## 1. 기본 작업면

```text
GPT Pro
→ planning / research / benchmark / review

Notion
→ human-facing Project Home / visual / asset / flow / confirmed human tables

GitHub repository
→ structured data / code / scene / resource / tracked assets / tests / CI/runtime evidence

PowerShell + Codex
→ actual repository/runtime executor when implementation needs it

Godot + project-adopted HiGodot / GUT / Hera
→ authoring / deterministic tests / live QA under each project's current authority contract

Loop Engineering
→ bounded execution/control plane only when current project/package/evidence says it is relevant
```

프로젝트 기획·자산·UX·정본을 관리하기 위해 새 localhost/browser/desktop app 또는 standalone HTML dashboard를 기본 작업면으로 만들지 않는다. Tool Hub나 QA Evidence Studio를 프로젝트 기본 실행면으로 복원하지 않는다.

## 2. 폐기 대상

### `PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED`

과거의 Expression/Sprite 계열 프로젝트 관리·시각 작업면처럼 Notion/Repository로 대체된 user-facing local management surface는 신규 기본 경로가 아니다. 고유 capability가 남아 있는지 한 번 감사하고 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다.

### `TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW`

Tool Hub는 신규 프로젝트의 discovery, launcher, asset/visual management, PowerShell 대체면 또는 기본 coordinator가 아니다.

- 과거 Hub 구현·Plan·PR·테스트·runtime evidence는 역사/rollback 증거로 남을 수 있다.
- Hub에만 있던 UNIQUE workflow 원리, project identity, fail-closed rule이 있으면 현재 Notion/repository/PowerShell/Loop owner로 흡수한다.
- Tool Hub code가 repository에 남아 있다는 사실은 active adoption을 뜻하지 않는다.
- `START_HERE`, 일반 project handoff, 기본 PowerShell 계약은 Tool Hub를 우선 경로로 라우팅하지 않는다.
- 재도입하려면 최신 사용자 승인, Existing Solution First, 총수명주기 비용 비교와 실제 consumer evidence가 새로 필요하다.

### `QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW`

QA Evidence Studio는 더 이상 신규 project validation의 active/default utility가 아니다.

재사용할 것은 **도구 자체가 아니라 증거 계약**이다.

```text
project/build identity
→ expected validation contract
→ existing test/runtime/log/screenshot evidence
→ repository or CI artifact
→ exact commit/PR identity
→ human-facing Notion link when useful
→ PASS | FAIL | BLOCKED | NOT_RUN with evidence ceiling
```

이 계약은 `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`가 소유한다. 별도 capture app을 새로 만들거나 QA Studio adapter를 프로젝트마다 추가하지 않는다. 과거 Studio code·tests·review docs는 물리 삭제 전까지 archive/history가 될 수 있지만 신규 작업의 자동 라우팅·필수 preflight·완료 조건에 넣지 않는다.

### `EXTERNAL_HTML_WORKSPACE_RETIRED`

독립 HTML dashboard/catalog/기획 UI를 프로젝트 정본·기본 discovery surface로 유지하지 않는다. 단, 실제 game/runtime web asset, 문서 빌드 derived artifact, test fixture, 배포 산출물은 consumer가 다르므로 자동 삭제 대상이 아니다.

### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`

Google Sheets는 신규 기획·승인·상태관리의 입력면이 아니다.

```text
legacy Sheet
→ UNIQUE / DUPLICATE / OBSOLETE
→ UNIQUE human-facing meaning → repository human PDF/Markdown projection owner; explicitly scoped V4 Notion exception only when applicable
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

Figma는 신규 active visual workspace가 아니다. 과거 링크/asset에 UNIQUE provenance가 있으면 현재 repository owner와 exact-SHA human projection으로 이관·readback한 뒤 active reference를 제거한다. 명시된 V4 Notion exception만 추가 destination으로 사용한다.

## 3. `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`

전문 validation utility를 새로 만들지 않아도 다음 기존 증거를 조합해 project validation을 닫을 수 있다.

```yaml
repository_native_evidence:
  project_identity:
  commit_or_pr:
  build_identity:
  acceptance_criteria: []
  test_results: []
  runtime_logs: []
  screenshots_or_video: []
  deterministic_state_or_hash:
  platform_or_input_context:
  human_observation:
  storage:
    repository_path:
    ci_artifact:
    notion_human_link:
  verdict: PASS | FAIL | BLOCKED | NOT_RUN
  evidence_ceiling:
```

원칙:

- 기존 Godot/GUT/Hera/CLI/test/CI 출력과 직접 캡처를 우선한다.
- capture 도구가 없다는 이유로 검증을 PASS 처리하지 않는다.
- Notion preview나 screenshot은 runtime truth를 대체하지 않는다.
- 사람이 재미·이해·조작감을 관찰하지 않았으면 human/player evidence는 `NOT_RUN`이다.
- evidence 수집을 위해 새 GUI app을 만드는 것은 기본값이 아니다.

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

이 정책 변경만으로 과거 Tool Hub/QA Studio source tree를 즉시 삭제하지 않는다. 물리 삭제는 consumer 0, UNIQUE material 이관, rollback 필요성, package/test 영향과 현재 사용자 승인을 확인한 별도 bounded retirement task로 수행한다.

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
  retained_historical_code_or_evidence: []
  replacement_owner:
  rollback: Git history
  result: REMOVED | BLOCKED_UNVERIFIED | PARTIAL_RETIREMENT | RETIRED_FROM_ACTIVE_FLOW
```

`PARTIAL_RETIREMENT`에서 완료를 주장하지 않는다.
