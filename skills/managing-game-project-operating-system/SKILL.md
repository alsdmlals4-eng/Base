---
name: managing-game-project-operating-system
description: Use when installing, auditing, reconciling, migrating, or verifying a project repository operating system and its cold-start paths.
---

# Managing the Game Project Operating System

Base v9.1 projects use the focused [project adapter and routing contract](references/project-adapter-and-routing-contract.md). Validate the canonical adapter and generated snapshot before shared-route execution; copied shared bodies or failed pins are blocking integrity failures.

## Core principle

신규 설치, 기존 구조 감사, 구형 파일 정리, 승인된 마이그레이션과 운영체계 검수는 같은 책임 원본·참조·복구 계약을 공유한다. `Work Mode`와 `Skill Mode`를 구분하며, 읽기 전용 조사와 승인된 쓰기 작업을 혼동하지 않는다. 프로젝트 workspace는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`의 `DOMAIN_SPLIT_CANON`을 따른다. 기본 사람용 workspace는 `NOTION_DEFAULT_PROJECT_WORKSPACE` / `NOTION_HUMAN_FACING_CANON`, 구조화·runtime truth는 `REPOSITORY_STRUCTURED_CANON`, Google Sheets는 `COMPATIBILITY_ONLY` legacy migration input이다.

Google Sheets legacy migration의 공용 의미·폐기 경계는 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 따른다. 이 참조는 Sheet를 신규 입력면이나 active project workspace로 재승격하지 않는다. 기존 consumer가 사용하는 legacy literal `project_google_sheet`는 `google_sheet_compatibility_source`의 호환 alias일 뿐이며 신규 install·active sync·정본 권위를 뜻하지 않는다.

Godot MCP/addon/CLI 공급자 도입·업데이트는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다. HiGodot (`hi-godot/godot-ai`)만 persistent Godot authoring 실행 권위이며 프로젝트는 `HIGODOT_ADOPTION_RECORD.json`에 exact pin, Godot 버전, host client, canary, regression, rollback과 미검증을 기록한다. GUT과 Hera Agent Godot은 프로젝트가 실제 필요에 따라 채택하는 별도 **third-party 검증 도구**이며, GUT은 deterministic GDScript tests, Hera는 `LIVE_QA_AND_OBSERVABILITY_ONLY`로만 공존한다.

- `Work Mode`: `PLAN / BUILD / REVIEW`
- 이 문서의 `mode`: 운영체계 Skill 내부의 **Skill Mode**

## Skill Modes

- `install`: 신규 또는 내용이 거의 없는 프로젝트에 운영체계와 승인된 third-party provider record를 설치한다.
- `audit`: 기존 프로젝트를 변경 없이 조사하고 현재 구조·위험·보존표·addon/MCP/CLI provider inventory를 만든다.
- `reconcile-legacy`: 구형·중복·버전명 파일과 파생본을 현행 정본에 맞춰 갱신·통합·호환 보존·아카이브·승인 삭제한다.
- `migrate`: 사용자가 승인한 처리표 범위만 새 책임 구조로 재배치한다.
- `verify`: 설치·정리·마이그레이션·provider upgrade·대규모 변경 뒤 전체 연결을 증거로 검수한다.

```text
신규·내용 거의 없음 → install
기존 운영 프로젝트 → audit
v2·final·latest·복제본·구형 파생본 존재 → audit → reconcile-legacy
승인된 구조 이동표 있음 → migrate
설치·정리·마이그레이션·주요 게이트·HiGodot/GUT/Hera upgrade 후 → verify
```

`reconcile-legacy`는 별도 신규 Skill이 아니다. 기존 프로젝트의 책임 원본·참조·보존·삭제 권한을 다루는 같은 생명주기이므로 이 Skill의 전문 Skill Mode로 유지한다.

## Required inputs

```yaml
target_repository:
work_mode: PLAN/BUILD/REVIEW
project_mode: new/existing/installed
requested_skill_mode: install/audit/reconcile-legacy/migrate/verify
base_version:
project_agents:
project_start_here:
documentation_map:
active_context:
current_confirmed_decisions:
project_notion_workspace:
google_sheet_compatibility_source:
related_open_and_recent_prs:
development_gates:
design_document_registry:
skill_registry:
publications_and_manifests:
visual_and_asset_manifests:
roadmap_issues_plans_prs:
actual_code_data_assets_tests:
protected_paths_decisions_assets:
approved_migration_table:
approved_legacy_reconciliation_table:
known_versioned_duplicates_and_aliases:
governance_and_workflow_state:
rollback_ref:
third_party_provider_inventory:
higodot_adoption_record:
higodot_exact_pin:
higodot_previous_rollback_pin:
higodot_canary_evidence:
higodot_project_regression_evidence:
godot_test_framework:
gut_exact_version:
gut_test_consumption_path:
hera_cli_addon_pair:
hera_live_qa_consumption_path:
hera_source_delta_guard:
```

## Shared read order

```text
최신 사용자 지시
→ AGENTS·README·START_HERE
→ Work Mode·Skill 라우팅 계약
→ Active Context·Documentation Map·Roadmap·Development Gates
→ CURRENT_CONFIRMED_DECISIONS.md·동일 Goal의 열린·최근 병합 PR·정확한 Project Notion workspace
→ Google Sheets legacy source는 UNIQUE 미이관 material 확인이 필요할 때만
→ Design Document Registry·Skill Registry
→ 관련 책임 원본·Skill·Learning Log
→ third-party provider inventory·HIGODOT_ADOPTION_RECORD.json·GUT/Hera adoption state
→ DOCX/PDF·다이어그램·승인 이미지·Manifest
→ 실제 코드·데이터·자산·테스트
→ Issue·Plan·PR·Workflow·최근 변경
```

전체 skills 폴더를 기본 로드하지 않는다. 백업·보류·제거 후보는 감사·정리 대상일 때만 읽는다.

## Shared operating contract

- 한 질문에는 등록된 현행 Markdown 또는 JSON 책임 원본 하나만 둔다.
- PDF·DOCX·다이어그램은 Registry 발행 정책과 Manifest를 따른다.
- trigger가 일치하는 최소 Skill·Skill Mode를 자동 선택한다.
- 승인·구현·검증·발행 최신성·사람 검수 상태를 분리한다.
- 기존 승인 결정·수치·자산·실패·보류·참조는 조사와 승인 없이 제거하지 않는다.
- 파일 존재와 실제 실행·강제를 구분한다.
- 새 AI가 과거 대화 없이 `CURRENT_CONFIRMED_DECISIONS.md`에서 현재 승인 상태와 다음 작업을 찾을 수 있어야 한다.
- 질문 전에 최신 `main`, 기존 Decision, 분야 정본, 동일 Goal의 PR과 정확한 Project Notion workspace를 비교하고 이미 답한 질문은 반복하지 않는다. legacy Sheet는 `google_sheet_compatibility_source`에 UNIQUE 미이관 정보가 있을 때만 대조한다.
- 승인된 Decision은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`와 workspace authority contract에 따라 Repository 정본과 적용 가능한 `NOTION_HUMAN_FACING_CANON`에 기록하고 **destination readback**한다. Google Sheets 쓰기는 active Decision sync 요구사항이 아니다.
- `BEST_LONG_TERM_EFFICIENT_METHOD`를 운영체계의 작업목표로 사용한다. 응답 속도·최소 토큰보다 정확성, 출시 품질, 유지보수성, 재사용성, 되돌리기 가능성, 수명주기 총비용을 우선하고, 공식/1차 자료·벤치마크·현업 운영·실무 성공/실패 사례를 최소 3개 실질 대안과 비교한다.
- `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`: GitHub 병합 뒤 exact new main을 재조회하고 전체 승인 범위를 적대적으로 검토한다. 유효 finding은 `POSTMERGE_CORRECTION_REQUIRED`로 latest main의 새 Branch/PR에서 교정·회귀 검증한다. 적용 가능한 Notion current-state는 GitHub 증거 뒤에만 갱신하고, GitHub/Notion 양쪽 destination을 다시 읽어 `PROGRESS_READBACK_REQUIRED`와 남은 작업 계산을 닫는다.
- `REMAINING_WORK_COMPLETION_GATE`: Base 공용 완료 규칙을 모든 프로젝트 작업에도 적용한다. 계획된 작업을 끝낸 뒤 `REMAINING_WORK_RECALCULATION_REQUIRED`와 `IMPLEMENTATION_CORRECTION_RESCAN`을 수행하고, 새 유효 finding이 있으면 `NEW_FINDING_REOPENS_REMAINING_WORK`로 BUILD/verify를 재개한다. 최종 후보의 기존 `POST_CHANGE_MONITOR_LOOP`가 곧 `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`이며 별도 두 번째 검토 루프를 만들지 않는다.

### `REMAINING_WORK_COMPLETION_GATE`

프로젝트에서 계획된 남은 작업이 0으로 보이는 순간은 완료가 아니라 `COMPLETION_CANDIDATE`다. 실제 Repository·적용 가능한 Notion·Decision·PR·구현·Test·consumer·evidence 상태를 다시 읽어 `REMAINING_WORK_RECALCULATION_REQUIRED`를 수행한다.

```text
planned project work exhausted
→ REMAINING_WORK_RECALCULATION_REQUIRED
   ├─ remaining > 0 → BUILD / verify 계속
   └─ remaining = 0 → COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   implementation / canon / Notion / tests / consumers / PRs / runtime/readback evidence
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK
   │  → existing owner 최소 교정
   │  → regression + destination readback
   │  → remaining-work recalculation again
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ same final `POST_CHANGE_MONITOR_LOOP`
→ `running-adversarial-review-and-refinement` minimum-five full loops
→ CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ completion report
```

`IMPLEMENTATION_CORRECTION_RESCAN`은 `running-adversarial-review-and-refinement`가 소유하며 새 Skill이 아니다. 프로젝트 core/승인 intent와 실제 구현의 불일치, 정본·Notion/Repository drift, untouched Test·Template·consumer·reference, 동일 Goal PR, rollback/복구, runtime/readback evidence를 다시 공격한다. 검증된 finding은 현재 승인 범위의 남은 작업으로 편입한다. `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED` 역시 새 cycle이 아니라 최종 completion candidate를 입력으로 한 동일 `POST_CHANGE_MONITOR_LOOP`를 뜻한다.

승인 범위 안에 완료 조건을 막는 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, 미해결 `DEFER`가 남으면 `전체 완료`라고 보고하지 않는다. 해당 상태와 재개 조건을 그대로 노출한다. 범위 밖 future improvement는 별도 후보로 `DEFER`할 수 있으나 현재 범위의 미완료를 숨기는 용도로 사용하지 않는다.

## Project workspace authority contract

```yaml
workspace_authority: DOMAIN_SPLIT_CANON
default_project_workspace: NOTION_DEFAULT_PROJECT_WORKSPACE
human_facing_canon: NOTION_HUMAN_FACING_CANON
structured_runtime_canon: REPOSITORY_STRUCTURED_CANON
google_sheets: COMPATIBILITY_ONLY
google_sheet_compatibility_source: OPTIONAL_LEGACY_MIGRATION_INPUT
```

- 사람용 프로젝트 계획·결정·설명·시각 자료는 정확한 Project relation의 Notion workspace에 둔다.
- 구조화 상태·Commit·runtime truth·실제 코드/데이터/씬/자산/Test는 Repository가 소유한다.
- 기존 Google Sheet의 값·수식·이미지·사용자 편집은 삭제 전에 `UNIQUE / DUPLICATE / OBSOLETE`로 감사한다.
- Sheet-only 고유 정보는 현행 owner로 이관 → readback/Test → consumer/reference 확인 후에만 원본 수명주기를 판정한다.
- 신규 install은 Google Sheet URL이나 tab을 요구하거나 생성하지 않는다.

## HiGodot provider adoption contract

```yaml
provider: hi-godot/godot-ai
authority: SOLE_GODOT_EXECUTION_AUTHORITY
persistent_authoring_authority: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
exact pin: required
floating_latest: forbidden
automatic_unreviewed_update: forbidden
network_mode: LOOPBACK_ONLY
deepseek: FORBIDDEN
rollback: required
```

### Install

1. `evaluating-godot-assets-and-plugins-before-creation`의 disposition이 `REUSE` 또는 승인된 `REFACTOR`인지 확인한다.
2. exact release 또는 exact commit, package/source origin, license, Godot 버전과 host client를 기록한다.
3. 개인 Codex·GPT profile에만 MCP를 등록하고 DeepSeek Analysis에는 등록·credential을 두지 않는다.
4. 프로젝트에 활성 `.vscode/mcp.json`이나 `.codex/config.toml`을 공용 commit하지 않는다.
5. `templates/project-operations/HIGODOT_ADOPTION_RECORD.json`을 프로젝트 record로 설치하고 실제 값을 채운다.
6. connection, runtime, regression, production readiness를 독립 상태로 유지한다.

### Upgrade

```text
new release identified
→ release note·dependency·tool schema·transport·security diff
→ compatibility and adversarial review
→ isolated fixture
→ Godot import and plugin startup
→ read canary
→ destructive canary and exact restore
→ representative project canary
→ full affected project regression
→ staged adoption
→ previous exact pin and rollback package retained
```

`destructive canary`는 최소한 Node 삭제/복원, file write·move·delete/복원, project settings 또는 autoload 변경/복원을 실제로 검증하되 source fixture를 최종적으로 exact restore한다. 실행하지 못한 OS·device·Editor UI·human flow는 `NOT_RUN`이다.

### Verify

- 실제 installed version이 adoption record의 exact pin과 일치하는가
- HiGodot 외 두 번째 Godot **persistent mutation authority**가 활성화되지 않았는가
- network가 loopback only이고 LAN/public URL/forwarding/tunnel이 없는가
- Codex·GPT profile과 DeepSeek 금지 경계가 유지되는가
- enabled domain의 read·L1·L2 canary와 project regression evidence가 있는가
- rollback pin·package·절차가 실제로 존재하는가
- 단순 connection 또는 tools/list를 production readiness로 승격하지 않았는가

## Godot deterministic-test and live-QA adoption contract

GUT과 Hera는 HiGodot `HIGODOT_ADOPTION_RECORD.json`에 억지로 합치지 않는다. 프로젝트의 기존 `third-party` provider/addon inventory에 exact version, source, license, Godot compatibility, adoption state, consumption path, owner boundary, validation, rollback/removal을 기록한다.

### GUT

```yaml
role: DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED
gut_exact_version: required
godot_compatibility_match: required
gut_test_consumption_path: required_when_adopted
floating_latest: forbidden
```

- 테스트 가능한 GDScript 제품 코드와 반복 가능한 상태 규칙이 있을 때만 채택한다.
- Godot 버전별 공식 compatibility matrix를 확인하고 exact version을 고정한다.
- GUT 채택 이후 같은 GDScript test case를 HiGodot `McpTestSuite`와 두 canonical suite로 유지하지 않는다. 기존 `McpTestSuite` case는 migration input으로 보존한다.
- C#/.NET·native SDK·platform sandbox·build/package test authority를 강제 대체하지 않는다.
- 설치돼 있지만 실제 test/CI 소비가 없으면 `INSTALLED_UNUSED`; 필요가 아직 없으면 `DEFERRED`다.

### Hera Agent Godot

```yaml
role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
hera_cli_addon_pair: exact_match_required
hera_live_qa_consumption_path: required_when_adopted
hera_source_delta_guard: required_for_acceptance
persistent mutation authority: forbidden
floating_latest: forbidden
```

- Hera restricted live QA는 HiGodot과 공존할 수 있다. **persistent mutation authority** 또는 unrestricted editor writer로 활성화되면 blocking duplicate authority다.
- Base 채택은 localhost + shared token을 사용하고 token 원문을 저장소·prompt·log·evidence에 기록하지 않는다.
- acceptance QA 전후 tracked source를 비교해 Hera-phase delta `NONE`을 요구한다.
- `game set` 또는 state-changing runtime `call`은 `DIAGNOSTIC_ONLY`이며 acceptance evidence가 아니다. restore 또는 restart 후 정상 경로를 다시 검증한다.
- 설치돼 있지만 live-QA consumption이 없으면 `INSTALLED_UNUSED`; 실행 가능한 game/live-QA 요구가 없으면 `DEFERRED`다.

## Skill Mode: install

1. 신규·빈 프로젝트인지 확인한다. 고유 문서·자산·이력이 있으면 `audit`로 전환한다.
2. 루트 `[기획서]/00_프로젝트_허브/`와 시작 문서·`CURRENT_CONFIRMED_DECISIONS.md`·Registry·게이트를 설치한다.
3. 정확한 Project Notion workspace와 Project relation을 확인·연결한다. 적용되지 않으면 `NOT_APPLICABLE`로 두며 새 Google Sheet를 만들거나 요구하지 않는다. 기존 legacy Sheet가 실제 존재하면 `google_sheet_compatibility_source`로만 기록한다.
4. 프로젝트가 실제 선택한 책임 분야만 등록한다.
5. 서술은 Markdown, 구조·상태·게임 데이터는 JSON을 선택한다.
6. 발행 생성기·Manifest·선택 파생본 정책을 설치한다.
7. Foundation·분야 Skill Registry와 Learning Log를 설치한다.
8. Visual Source·Asset Manifest와 승인 상태를 연결한다.
9. Governance 검사·Actions·Required Check 준비 상태를 구분한다.
10. 승인된 HiGodot 사용 프로젝트이면 provider adoption contract와 exact pin record를 설치한다.
11. GUT 또는 Hera가 현재 프로젝트에서 실제 필요하고 평가 결과가 `REUSE` 또는 승인된 `REFACTOR`일 때만 기존 third-party inventory에 project-specific adoption을 기록한다. 모든 프로젝트에 일괄 설치하지 않는다.
12. `verify`로 콜드 스타트와 결정 복원·동기화·provider 경계를 확인한다.

## Skill Mode: audit

첫 단계는 `PLAN` 또는 `REVIEW` Work Mode이며 대량 삭제·이동·통합을 수행하지 않는다.

| 현재 경로 | 역할 | 추정 버전 | 참조 | 고유 정보 | 중복·충돌 | 상태 | 제안 | 위험 | 검증 |
|---|---|---|---|---|---|---|---|---|---|

산출물:

- 현재 책임 문서·Skill·자산·파생본 지도
- enabled addon·connected MCP·CLI·provider pin·host profile inventory
- GUT/Hera exact pin·consumption·owner boundary·source-delta guard 상태
- `CURRENT_CONFIRMED_DECISIONS.md`·분야 정본·GitHub `main`·정확한 Project Notion record의 Decision·Commit·대체 관계 대조
- 실제 legacy Sheet가 있으면 `COMPATIBILITY_ONLY` 범위의 UNIQUE/DUPLICATE/OBSOLETE migration inventory
- 중복·충돌·누락·구형 참조 목록
- 목표 Registry와 책임 원본 구조
- 갱신·통합·호환 보존·아카이브·삭제 후보
- 변경 전후 예상 구조
- 보존·참조·롤백 검증 계획
- 사용자가 승인해야 할 처리표

## Skill Mode: reconcile-legacy

다음 신호가 있으면 자동 선택한다.

- `v2`, `v3`, `final`, `final2`, `latest`, 날짜 접미사 등 활성 복제본
- 같은 책임을 가진 Markdown·JSON·PDF·DOCX 다중 현행본
- 새 경로로 대체됐지만 활성 파일이 계속 참조하는 구형 경로·ID·Schema
- 원본보다 오래된 생성물·Manifest·해시
- 삭제된 Skill·명령·파일을 실행 경로가 참조함
- Google Sheets·Figma·외부 HTML workspace·폐기된 custom local Tool/Hub가 active authority처럼 남아 있음
- HiGodot과 겹치는 과거 Base MCP·Bridge, unrestricted Hera writer 또는 다른 persistent mutation addon이 활성 경로에 남음

Hera가 존재한다는 사실만으로 legacy conflict로 판정하지 않는다. `LIVE_QA_AND_OBSERVABILITY_ONLY`로 제한되고 exact pair·consumption·source-delta guard가 검증된 Hera는 허용된 검증 도구다.

파일별로 하나를 판정한다.

```text
CURRENT
UPDATE_IN_PLACE
MERGE_TO_CANONICAL
COMPATIBILITY_STUB
ARCHIVE_HISTORY
DELETE_APPROVED
KEEP_UNRESOLVED
```

처리 순서:

```text
인벤토리·해시·참조 수집
→ 현행 정본 판정
→ 고유 결정·예외·이미지·보류 승계
→ 충돌·미확정 분리
→ 처리표 승인 확인
→ BUILD Work Mode로 UPDATE·MERGE·STUB·ARCHIVE·DELETE 실행
→ Registry·참조·생성기·테스트·파생본 갱신
→ REVIEW Work Mode로 reference-freshness·회귀·복구 검증
```

승인표가 없으면 `PLAN/REVIEW`에서 판정과 제안까지만 수행한다. 삭제는 다음을 모두 만족해야 한다.

- 모든 고유 정보·이미지·예외·보류가 현행 정본에 승계됨
- 활성·보조·외부 참조가 새 경로로 갱신되거나 호환 stub이 있음
- PDF·DOCX·Manifest·해시·생성기가 검증됨
- Git 이력·태그·백업 등 복구 경로가 있음
- 사용자 지시 또는 승인된 작업 계약의 삭제 근거가 있음
- `auditing-canonical-reference-freshness`에 차단 finding이 없음

템플릿: `templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md`

## Skill Mode: migrate

`approved_migration_table` 항목만 `BUILD` Work Mode에서 수행한다.

```text
고유 문장·표·결정·예외·이미지·보류 추출
→ 충돌 표시
→ 최신 사용자 결정과 실제 구현으로 현행 판정
→ 불확실성은 [확인 필요]
→ 새 책임 원본과 Registry에 승계
→ 승인 이미지·발행 경로 연결
→ 참조 갱신
→ destination readback/Test
→ consumer/reference 확인
→ 변경 전후 보존 대조
→ 기존 원본 수명주기 판정
→ verify
```

## Skill Mode: verify

각 영역을 `PASS / PARTIAL / FAIL / NOT_RUN`과 증거 경로로 기록한다.

1. 루트와 시작 문서
2. Work Mode·Skill 자동 라우팅과 실행 보고
3. `CURRENT_CONFIRMED_DECISIONS.md`·분야 정본·GitHub `main`·적용 가능한 Project Notion 동기화와 destination readback
4. legacy Google Sheets가 있으면 `COMPATIBILITY_ONLY` migration 상태와 active authority 미승격
5. Design Document Registry와 단일 책임 원본
6. 구형본 처리표·Legacy Alias·활성 stale reference 부재
7. PDF·선택 DOCX·다이어그램·승인 이미지·Manifest
8. Skill Registry·최소 라우팅·Learning Log
9. Development Gates·Roadmap·결정 추적성
10. Visual Source·Asset Manifest
11. HiGodot exact pin·단일 persistent authoring 권위·host isolation·canary·regression·rollback
12. adopted GUT exact compatible pin·GDScript test consumption·duplicate canonical case 부재
13. adopted Hera exact CLI/addon pair·`LIVE_QA_AND_OBSERVABILITY_ONLY`·localhost/shared-token·live-QA consumption·source-delta `NONE`
14. Governance checker·회귀 테스트·GitHub Actions·브랜치 보호
15. 과거 대화 없이 현재 Decision을 복원하는 콜드 스타트
16. GitHub 병합 뒤 exact main·전체 적대 검토·필수 교정·적용 가능한 Notion 갱신·양쪽 readback·진행도 재계산
17. `REMAINING_WORK_RECALCULATION_REQUIRED` 뒤 `IMPLEMENTATION_CORRECTION_RESCAN`을 수행하고, 새 finding이면 `NEW_FINDING_REOPENS_REMAINING_WORK`, clean이면 최종 후보의 동일 `POST_CHANGE_MONITOR_LOOP`로 `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`와 `CLEAN_REVIEW_EXIT`를 확인

```text
결정
→ Markdown/JSON 책임 원본
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ Active Context
→ 사람용 발행본
```

## Output contract

```md
# 게임 프로젝트 운영체계 결과
## Work Mode와 Skill Mode
## 자동 선택 이유
## 현재 구조·증거
## Project Notion·Repository workspace authority
## Legacy Google Sheets compatibility/migration 상태
## Third-party provider와 HiGodot exact pin
## GUT/Hera adoption·consumption·owner boundary
## Canary·project regression·rollback
## 구형 파일·파생본 처리표
## 실제 갱신·통합·아카이브·삭제
## 제안만 한 변경
## 보존·참조·롤백 대조
## CURRENT_CONFIRMED_DECISIONS·Repository·Notion 동기화
## Registry·책임 원본·발행본
## Skill·Learning·Routing
## 자동화·GitHub 강제
## 병합 후 GitHub·Notion 적대 검토·교정·진행도 readback
## REMAINING_WORK_COMPLETION_GATE·IMPLEMENTATION_CORRECTION_RESCAN·CLEAN_REVIEW_EXIT
## 콜드 스타트
## PASS·PARTIAL·FAIL·NOT_RUN
## 얻은 결과·미검증·위험
## 다음 단계와 승인 조건
```

## Definition of Done

- Work Mode와 Skill Mode·쓰기 권한이 명확하다.
- 사용자가 Skill을 선언하지 않아도 trigger로 필요한 Skill Mode를 자동 선택했다.
- `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`, `REPOSITORY_STRUCTURED_CANON`, `COMPATIBILITY_ONLY`의 역할이 구분됐다.
- 기존 프로젝트는 `audit`와 승인 없이 대규모 변경하지 않았다.
- 구형 파일은 고유 정보·참조·파생본·복구·승인에 따라 판정됐다.
- legacy Sheet는 active workspace로 재승격되지 않았고 UNIQUE material은 현행 owner 이관·readback/Test·consumer 확인을 거쳤다.
- 삭제·통합 뒤 활성 stale reference와 untouched 소비자가 없다.
- HiGodot project이면 exact pin, DeepSeek 금지, loopback, canary, regression, rollback 상태가 기록됐다.
- GUT/Hera adopted project이면 exact pin/pair, 실제 consumption, owner boundary, rollback/removal과 Hera source-delta guard가 기록됐다.
- 신규·정리·마이그레이션·provider update 결과는 `verify` 증거를 가진다.
- 병합 뒤 `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`, `POSTMERGE_CORRECTION_REQUIRED`, `PROGRESS_READBACK_REQUIRED`가 적용 범위에서 닫혔다.
- `FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK`: 승인 범위의 actionable remaining work가 0이고 `IMPLEMENTATION_CORRECTION_RESCAN` 결과 필수 구현/교정 finding이 없으며 최종 후보의 동일 `POST_CHANGE_MONITOR_LOOP`가 `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`와 `CLEAN_REVIEW_EXIT`를 닫았다.
- 승인 범위 안에 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, 미해결 `DEFER`가 남은 상태를 `전체 완료`로 숨기지 않았다.
- 실행하지 않은 검사와 권한은 `NOT_RUN` 또는 `[미검증]`이다.
- 사용한 Skill Mode의 이유와 얻은 결과를 보고했다.

## Failure conditions

- 기존 프로젝트에 신규 설치 구조를 강제함
- Google Sheets를 신규 입력·기본 사람용 workspace·active Decision sync surface로 요구함
- legacy Sheet UNIQUE material을 현행 owner readback/Test 없이 삭제함
- 사용자 승인 전 삭제·이동·통합함
- 파일명에 `old`·`v2`가 있다는 이유만으로 삭제함
- 파일 수 감소를 성공으로 판단함
- 고유 정보·승인 자산·보류·실패 기록을 축약함
- Git 이력만 있다는 이유로 활성 참조·복구 검증 없이 삭제함
- 호환성이 필요한 외부 경로를 stub 없이 제거함
- PDF·DOCX를 독립 책임 원본으로 수정함
- HiGodot/GUT/Hera floating latest 또는 automatic unreviewed update 사용
- DeepSeek profile에 HiGodot 등록
- 두 번째 Godot persistent mutation authority 활성화
- Hera restricted live-QA 도입을 mere presence만으로 legacy conflict 처리
- Hera persistent writer·source-delta failure·diagnostic mutation을 acceptance evidence로 허용
- GUT이 C#/.NET·native·platform test authority를 강제 대체
- consumption이 없는 addon/CLI를 `ADOPTED_ACTIVE` 완료로 보고
- canary·project regression·rollback 없이 provider update 완료 보고
- connection 성공을 production readiness로 보고
- 설치·정리·마이그레이션 뒤 `verify`를 생략함
- `REMAINING_WORK_COMPLETION_GATE`를 건너뛰고 계획 목록 소진만으로 전체 완료를 주장함
- 사용한 이유와 결과 없이 Skill 실행만 주장함

## 플랫폼 심사·자산 권리 설치와 감사

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다. 새 Skill Mode를 추가하지 않고 기존 `install / audit / migrate / verify`에 통합한다.

- `install`: 프로젝트가 채택한 등가 정본 또는 `ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`, `GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md` 인스턴스를 등록한다.
- `audit`: 음악·효과음, 폰트, 캐릭터·일러스트, 3D·애니메이션, 플러그인·에셋, 오픈소스, AI, 외주, 성우·작곡·번역 계약 Coverage를 확인한다.
- `migrate`: 기존 Asset Ledger와 계약 기록을 덮어쓰지 않고 새 필드와 연결하며 미확인은 보존한다.
- `verify`: `content_rating_target`과 `target_audience`, Steam·STOVE·Google Play 설문, build·store·trailer 일치, 자산별 권리와 secure evidence를 분리 검증한다.

필수 권리·등급·출처·계약·참조 유사성 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다. Template 존재는 실제 권리나 플랫폼 승인 증거가 아니다.

## Legacy aliases

- `installing-game-project-operating-system` → `install`
- `migrating-existing-game-project-structure` → `audit`, `reconcile-legacy` 또는 `migrate`
- `verifying-game-project-operating-system` → `verify`

Related:

- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`
- `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`
- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

## Cloud Run backend capability handoff

`docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`가 선택된 프로젝트는 `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`를 프로젝트 책임 원본으로 설치한다. 상태는 `PROJECT_OWNED_SERVICE_CONTRACT`이며 실제 identity provider, datastore, region, traffic, budget, platform IDs와 runtime evidence는 프로젝트가 소유한다.

## Entitlement and integrity capability handoff

`docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`가 선택된 프로젝트는 `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`를 `PROJECT_OWNED_ENTITLEMENT_INTEGRITY_RECORD`로 설치한다. 실제 platform account, product/package ID, SDK, signing, backend, privacy, recovery와 sandbox evidence는 프로젝트가 소유한다.
