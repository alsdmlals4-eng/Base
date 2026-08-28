# Notion Retirement and Repository Migration Checklist

> Status: `PROJECT_TEMPLATE`
> Default Notion state: `LEGACY_READ_ONLY_MIGRATION_SOURCE`
> Target authority: `REPOSITORY_PRIMARY_PROJECT_CANON`
> Safety rule: existing Notion pages and databases are not deleted by default

## 0. Project and source identity

```yaml
project_id:
project_name:
repository:
repository_main_commit:
project_agents_path:
notion_source_name:
notion_source_locator:
notion_access_state: READABLE | PARTIAL | UNAVAILABLE
legacy_sheet_locators:
audit_started_at:
audit_completed_at:
auditor:
```

- [ ] 대상 Project와 repository가 정확히 일치한다.
- [ ] 다른 프로젝트의 Notion record를 섞지 않는다.
- [ ] Notion을 읽지 못한 범위는 `BLOCKED_UNVERIFIED`로 남긴다.
- [ ] 과거 대화나 기억만으로 Notion 고유 자료가 없다고 추정하지 않는다.
- [ ] audit 중 Notion에 신규 기획·승인·asset write를 추가하지 않는다.

## 1. Current repository destination inventory

| Destination ID | 책임 | canonical path | current commit | readback | 비고 |
|---|---|---|---|---|---|
| DEST-001 | AI 기획·구현 명세 | `docs/canon/AI_GAME_SPEC.md` |  |  |  |
| DEST-002 | 승인 결정 | `CURRENT_CONFIRMED_DECISIONS.md` |  |  |  |
| DEST-003 | 현재 상태 | `ACTIVE_CONTEXT.md` |  |  |  |
| DEST-004 | Codex 인계 | `docs/handoffs/CURRENT_CODEX_HANDOFF.md` |  |  |  |
| DEST-005 | Asset manifest | `assets/ASSET_MANIFEST.json` |  |  |  |
| DEST-006 | 사람용 PDF | `docs/exports/` |  |  | 파생본 |

프로젝트가 다른 구조를 사용하면 동등 owner path를 기록한다. 경로가 없으면 무조건 새 파일을 만들지 말고 프로젝트의 최신 `AGENTS.md`와 registry를 먼저 확인한다.

## 2. Legacy material inventory

각 Notion page/database/view/attachment 또는 의미 있는 record 묶음을 한 행으로 분류한다.

| Legacy ID | source locator | Project | 자료 유형 | 요약 | current consumer | repository equivalent | classification | destination | provenance | destination_readback | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LEGACY-001 |  |  |  |  |  |  | UNIQUE |  |  | NOT_RUN |  |

### classification

- `UNIQUE`: 현재 repository canon 또는 보존할 Library reference에 없는 고유 의미·asset·결정·증거.
- `DUPLICATE`: current repository owner와 의미가 같고 source identity를 확인했다.
- `OBSOLETE`: 승인된 supersession 또는 폐기 근거가 있고 active consumer가 없다.
- `BLOCKED_UNVERIFIED`: 접근, 출처, Project identity, 내용 또는 destination을 검증할 수 없다.

분류 규칙:

- [ ] 최신 수정 시각만으로 authority를 판정하지 않는다.
- [ ] 내용이 비슷하다는 이유만으로 `DUPLICATE` 처리하지 않는다.
- [ ] 오래되었다는 이유만으로 `OBSOLETE` 처리하지 않는다.
- [ ] 구현에 사용 중인 locator가 있으면 current consumer를 확인하기 전 폐기하지 않는다.
- [ ] 승인 이미지의 원본·버전·교체 관계를 확인한다.
- [ ] AI/System metadata와 사람이 읽는 설명을 의미 단위로 통합하되 증거를 잃지 않는다.

## 3. UNIQUE migration mapping

### 3.1 Planning, decisions, systems and content

```text
Notion unique planning meaning
→ project AI canon or confirmed decision owner
→ source provenance and supersession
→ exact repository commit
→ destination_readback
```

- [ ] 프로젝트 정의·코어·시스템·콘텐츠·Flow 의미를 올바른 owner에 반영했다.
- [ ] 승인된 결정과 candidate/proposal을 구분했다.
- [ ] 수치·경제·데이터의 source와 적용 상태를 보존했다.
- [ ] Notion page structure를 그대로 복제하지 않고 의미 owner에 통합했다.
- [ ] repository diff에서 변경 내용을 검토했다.

### 3.2 Visuals and runtime assets

```text
Notion attachment or visual record
→ original binary/source availability check
→ actual consumer and approval state
→ repository runtime asset or non-canon Library reference
→ ASSET_MANIFEST path/version/sha256/provenance
→ destination_readback
```

- [ ] Preview만 있고 원본 binary가 없는 경우 `BLOCKED_UNVERIFIED`로 표시했다.
- [ ] 실제 game consumer가 있는 승인 asset은 repository path에 저장했다.
- [ ] candidate/reference/rejected asset은 runtime asset과 분리했다.
- [ ] `asset_id`, `repository_path`, `actual_consumer`, `approval_status`, `version`, `sha256`, `source_or_provenance`, `rights_or_license_state`, `implementation_status`를 기록했다.
- [ ] 대형 editable master는 필요 시 Library/local source에 두고 runtime input과 구분했다.
- [ ] Codex가 Notion 없이 exact commit에서 구현 입력을 회수할 수 있다.

### 3.3 Tables, Flow and storyboard

- [ ] 사람이 수정해야 하는 의미 표는 Markdown/JSON/프로젝트 데이터 owner로 옮겼다.
- [ ] Flow/Storyboard는 의미 source와 이미지 파생물을 구분했다.
- [ ] PDF에만 존재하는 현재 결정이 없도록 했다.
- [ ] 설명용 시각자료는 runtime evidence로 승격하지 않았다.

### 3.4 Evidence and history

- [ ] 구현·test·runtime evidence는 repository evidence path와 exact commit에 연결했다.
- [ ] 단순 Notion screenshot을 runtime PASS로 취급하지 않았다.
- [ ] 법적·권리·개인정보 원본은 공개 저장소에 넣지 않고 안전한 locator와 최소 metadata만 남겼다.
- [ ] rollback에 필요한 provenance를 보존했다.

## 4. destination_readback

각 `UNIQUE` 항목은 이동했다고 기록하는 것만으로 완료하지 않는다.

```yaml
legacy_id:
destination_type: REPOSITORY_CANON | REPOSITORY_TRACKED_RUNTIME_ASSET | CHATGPT_LIBRARY_NON_CANON_REFERENCE
destination_path_or_locator:
source_commit:
content_or_binary_readback: PASS | FAIL | BLOCKED | NOT_RUN
sha256_readback: PASS | FAIL | NOT_APPLICABLE | NOT_RUN
consumer_readback: PASS | FAIL | BLOCKED | NOT_RUN
supersession_readback: PASS | FAIL | NOT_APPLICABLE | NOT_RUN
known_limits:
```

- [ ] destination 파일·record를 실제로 다시 읽었다.
- [ ] binary는 SHA-256을 다시 계산하거나 저장소 manifest와 비교했다.
- [ ] current consumer가 새 path를 참조하는지 확인했다.
- [ ] 기존 Notion locator를 제거하기 전에 새 locator가 새 세션에서도 동작하는지 확인했다.
- [ ] readback 실패 항목을 완료로 세지 않았다.

## 5. Codex dependency audit

| Dependency ID | current handoff or code reference | Notion dependency | repository replacement | exact commit | 검증 | 상태 |
|---|---|---|---|---|---|---|
| DEP-001 |  |  |  |  |  |  |

- [ ] Codex 작업지시문이 Notion fresh-read를 필수로 요구하지 않는다.
- [ ] Codex가 필요한 기획·결정·asset을 repository에서 찾을 수 있다.
- [ ] Notion-only attachment URL이 구현 입력으로 남지 않았다.
- [ ] `GPT_VISUAL_REQUEST` 반환 경로가 repository delivery로 연결된다.
- [ ] 오래된 handoff의 Notion 링크는 필요 시 `LEGACY_DISCOVERY_ONLY`로 표시했다.

## 6. Active write-route audit

| Route ID | 문서·템플릿·자동화 | 현재 Notion write 요구 | 교정 결과 | readback | 상태 |
|---|---|---|---|---|---|
| ROUTE-001 |  |  |  |  |  |

- [ ] 신규 기획 단계에 Notion page/database 생성을 요구하는 active instruction이 없다.
- [ ] 이미지 승인 완료에 Notion attachment/readback을 요구하는 active instruction이 없다.
- [ ] 작업 완료 보고에 GitHub+Notion 이중 동기화를 요구하는 active instruction이 없다.
- [ ] 사람용 검토는 milestone PDF로 라우팅된다.
- [ ] project-specific 최신 사용자 결정이 Notion 유지를 명시한 경우 예외를 기록했다.

## 7. Retirement counts

아래 값은 항목 inventory와 readback 증거로 계산한다.

```text
NOTION_UNIQUE_CANON_COUNT = <number>
CODEX_NOTION_DEPENDENCY_COUNT = <number>
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = <number>
```

### Exit Gate

- [ ] `NOTION_UNIQUE_CANON_COUNT = 0`
- [ ] `CODEX_NOTION_DEPENDENCY_COUNT = 0`
- [ ] `ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0`
- [ ] 모든 `UNIQUE` 항목의 `destination_readback`이 PASS다.
- [ ] `BLOCKED_UNVERIFIED`가 퇴역 claim에 영향을 주는지 명시했다.
- [ ] 기존 Notion page/database를 `LEGACY_READ_ONLY`로 유지했다.
- [ ] 사용자가 삭제를 별도로 요청하지 않았다면 삭제하지 않았다.

세 count가 모두 0이어도 실제 runtime·UX·출시 검증을 증명하지 않는다. 이는 Notion 중간 작업 dependency가 제거되었음을 뜻한다.

## 8. Human PDF transition

- [ ] 현재 AI canon에서 `HUMAN_GDD_PDF_DERIVED_VIEW`를 생성할 Gate를 정했다.
- [ ] PDF의 `source_commit`, `canon_version`, `included_scope`, `evidence_ceiling`을 기록했다.
- [ ] 핵심 시스템·콘텐츠·구현 원리·시각자료·남은 작업을 사람이 검토할 수 있다.
- [ ] PDF render/readback을 완료했다.
- [ ] PDF 피드백을 repository canon으로 되돌리는 경로가 있다.

## 9. Final migration record

```yaml
project_id:
repository_commit:
notion_state: LEGACY_READ_ONLY | PARTIAL_MIGRATION | BLOCKED_UNVERIFIED
legacy_items_total:
unique_migrated:
duplicate_verified:
obsolete_verified:
blocked_unverified:
NOTION_UNIQUE_CANON_COUNT:
CODEX_NOTION_DEPENDENCY_COUNT:
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT:
repository_readback:
asset_manifest_readback:
codex_handoff_readback:
human_pdf_status:
deleted_legacy_content: false
remaining_required_work:
rollback:
```

## 10. Completion language

허용:

- `Base default workflow is repository-first.`
- `This project has migrated all verified unique Notion material.`
- `Notion remains legacy read-only.`
- `Notion retirement is blocked by the listed unverified items.`

금지:

- 읽지 못한 자료를 포함해 `모든 자료 이관 완료`라고 주장.
- Notion dependency 0을 runtime/UX/release PASS로 표현.
- destination readback 없이 migration 완료 주장.
- 사용자 승인 없이 Notion page/database 또는 승인 asset 삭제.
