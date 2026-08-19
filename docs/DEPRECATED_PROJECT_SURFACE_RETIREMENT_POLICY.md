# 폐기 프로젝트 작업면 흡수·삭제 정책

이 문서는 더 이상 기본 작업면으로 사용하지 않는 **사용자-facing 로컬 도구, HTML 프로젝트 작업면, Google Sheets**를 어떻게 마지막으로 감사하고 필요한 정보만 흡수한 뒤 제거할지 정의한다.

목표는 과거 실험·도구·중복 정본이 새 작업의 탐색 후보로 반복 노출되어 컨텍스트 비용과 충돌 위험을 만드는 것을 막는 것이다.

## 1. Machine contract

```text
DEPRECATED_SURFACE_ABSORB_THEN_DELETE
USER_FACING_LOCAL_TOOL_DEFAULT: RETIRED
HTML_PROJECT_SURFACE: RETIRED
GOOGLE_SHEETS_MIGRATE_THEN_REMOVE
REPOSITORY_NATIVE_QA_EVIDENCE
GIT_HISTORY_IS_ROLLBACK_NOT_ACTIVE_CANON
NO_DEFAULT_READ_OF_RETIRED_SURFACE
```

## 2. 적용 대상

### `USER_FACING_LOCAL_TOOL_DEFAULT: RETIRED`

프로젝트 기획·자산·UX·검수의 기본 사용자 작업면으로 별도 localhost/browser/desktop 앱을 만들거나 유지하지 않는다.

현재 프로젝트 운영은 다음 기본 surface로 충분해야 한다.

```text
GPT
→ planning / research / review

Notion
→ human-facing planning / visual / asset / flow / confirmed tables

GitHub repository
→ structured data / code / scene / resource / tracked assets / tests / runtime evidence

PowerShell + Codex
→ optional implementation executor when actually needed
```

이 규칙은 repository 내부의 CI 스크립트, 빌드 스크립트, migration script, 검증 script까지 무차별 삭제하라는 뜻이 아니다. 실제 소비자가 있는 non-interactive repository automation은 그 책임과 테스트가 남아 있는 동안 유지할 수 있다.

### `HTML_PROJECT_SURFACE: RETIRED`

독립 HTML dashboard/catalog/기획 UI를 프로젝트 정본·기본 discovery surface로 유지하지 않는다.

HTML이 다음 중 하나라면 별도 판단한다.

- 게임/runtime에서 실제 소비되는 웹 asset
- 문서 빌드 결과의 derived artifact
- 테스트 fixture
- 외부 배포 산출물

위 소비 경로가 없는 프로젝트 관리용 HTML surface는 흡수 후 제거한다.

### `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`

Google Sheets는 새 기획이나 정본의 기본 작업면으로 사용하지 않는다.

기존 Sheet가 남아 있으면 **한 번의 migration source**로만 읽는다.

```text
legacy Sheet
→ unique / duplicate / obsolete 분류
→ unique meaning만 추출
→ Project identity 확정
→ human-facing planning/table/visual → Notion
→ machine/runtime structured meaning → repository-native owner
→ provenance / Decision ID / source locator 보존
→ destination readback
→ conflict check
→ migration complete
→ old Sheet active reference 제거
→ 삭제 또는 사용자가 접근 가능한 archive/trash 처리
```

migration 완료 전에는 원본을 먼저 삭제하지 않는다. 접근 권한이 없어 고유 정보 여부를 확인할 수 없으면 `BLOCKED_UNVERIFIED`로 남긴다.

## 3. 흡수 기준

폐기 surface에서 다음을 발견하면 새 권위로 흡수할 수 있다.

- 현재 승인 결정과 충돌하지 않는 고유 기획 의미
- 아직 다른 곳에 없는 provenance
- 재사용 가능한 workflow 원리
- 검증 상태 vocabulary와 fail-closed 규칙
- 실제 소비 중인 schema/contract/test 원리
- 사용자 학습에 필요한 핵심 구조

다음은 흡수하지 않는다.

- 이미 Notion/repository에 있는 중복 표현
- superseded/rejected 결정
- tool-specific UI layout
- 특정 폐기 프로그램에만 필요한 localhost/port/session 계약
- 더 이상 소비되지 않는 helper metadata
- 과거 실험의 임시 snapshot

## 4. QA Evidence Studio에서 흡수하는 원리

별도 QA Evidence Studio 앱을 기본 경로로 유지할 필요는 없지만 다음 원리는 유효하다.

### `REPOSITORY_NATIVE_QA_EVIDENCE`

- 검증 증거는 가능한 한 exact Git commit/PR head에 묶는다.
- 판정은 `PASS / FAIL / BLOCKED / NOT_RUN`을 구분한다.
- 실행하지 않은 검사를 PASS로 승격하지 않는다.
- 화면/UX 검증이 필요한 경우 screenshot/video/log 같은 증거를 repository artifact 또는 PR evidence로 연결한다.
- 하나의 critical FAIL이 있으면 전체 결과를 성공으로 포장하지 않는다.
- Android가 아직 연결되지 않았다면 `DEFERRED_NOT_CONNECTED`처럼 PC 결과와 분리한다.
- 완료 후 증거를 바꾸어 과거 결과를 소급 수정하지 않는다. 새 run/evidence로 갱신한다.

위 원리는 repository-native test, GitHub Actions artifact, engine screenshot/video/log, PR comment/evidence packet으로 구현할 수 있다. 별도 localhost browser application은 필요하지 않다.

## 5. 삭제 Gate

`DEPRECATED_SURFACE_ABSORB_THEN_DELETE`:

```text
inventory exact surface
→ identify canonical consumers
→ classify KEEP PRINCIPLE / MIGRATE DATA / DROP DUPLICATE / BLOCKED
→ migrate unique material
→ destination readback
→ update active references and tests
→ adversarial review
→ remove active files/surface
→ regression
→ exact-head PR gate
→ merge
→ postmerge search confirms no active consumer
```

삭제 전에 다음을 확인한다.

- active canonical owner가 따로 있음
- 고유 정보가 새 owner로 이동함
- destination readback 성공
- active consumer reference가 교체됨
- 테스트가 새 owner를 검증함
- rollback은 Git history로 가능함

## 6. Git history와 Archive

`Git history`는 rollback과 감사 이력이며 active canon이 아니다.

삭제된 파일을 매번 Git history에서 다시 찾아 현재 작업 후보로 올리지 않는다. 특별히 과거 회귀 원인·migration 증거·사용자 요청으로 historical inspection이 필요한 경우만 본다.

새로운 `docs/archive` 복사본을 자동으로 만들지 않는다. Git history로 충분한 경우 이중 archive를 만들지 않아 컨텍스트 중복을 막는다.

## 7. active reference 정리

폐기 surface 삭제는 파일만 지우고 끝내지 않는다.

다음을 함께 감사한다.

- `START_HERE.md`
- `README.md`
- `docs/DOCUMENTATION_MAP.md`
- `AGENTS.md`
- Work Mode / Skill routing
- Skill Registry trigger/use_when/review trigger
- templates
- schemas
- workflows
- tests
- current Notion guidance

활성 문서가 폐기 도구를 기본 경로처럼 소개하면 삭제 완료가 아니다.

## 8. Notion 유료 기능

현재 유료 플랜은 `GPT_PRO`만 기본값이다.

Notion은 무료 범위에서 우선 운영한다. 유료 Notion 기능이 실제 병목을 반복적으로 해결하고 무료 fallback보다 총비용이 낮다는 근거가 있을 때만 별도 제안한다. 사용자가 명시적으로 요청·승인하기 전에는 paid Notion 기능을 전제로 migration이나 운영 구조를 설계하지 않는다.

## 9. 완료 판정

```yaml
retired_surface:
unique_material_absorbed: true | false
notion_readback: PASS | BLOCKED | NOT_APPLICABLE
repository_readback: PASS | BLOCKED | NOT_APPLICABLE
active_references_remaining: []
files_removed: []
repository_automation_preserved: []
rollback: Git history
result: REMOVED | BLOCKED_UNVERIFIED | PARTIAL_RETIREMENT
```

`PARTIAL_RETIREMENT` 상태에서 삭제 완료를 주장하지 않는다.
