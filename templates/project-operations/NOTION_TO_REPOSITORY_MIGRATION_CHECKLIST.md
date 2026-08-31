# Notion → Repository 안전 이관·퇴역 체크리스트

> 목적: 기존 프로젝트의 Notion-only 자료를 손실 없이 repository 중심 구조로 옮기고 Notion을 active workflow에서 퇴역시킨다.
>
> 이 체크리스트는 신규 Notion 구조를 만드는 템플릿이 아니다. 기본 상태는 `NO_NEW_NOTION_WRITE_BY_DEFAULT`다.

## 0. 작업 식별

```yaml
project:
repository:
base_branch:
source_sha_before_migration:
project_agents_path:
active_context_path:
notion_workspace_or_home:
migration_started_at:
migration_owner:
status: INVENTORY | MIGRATING | VERIFYING | LEGACY_READ_ONLY | RETIRED
```

## 1. 안전 경계

- [ ] 대상 프로젝트의 최신 `AGENTS.md`, Active Context, 승인 Decision, 실제 repository 구현을 먼저 읽었다.
- [ ] 같은 Goal의 open/draft PR과 수정 경로를 확인하고 read-only 경계를 기록했다.
- [ ] 신규 Notion write를 중단했다: `NO_NEW_NOTION_WRITE_BY_DEFAULT`.
- [ ] 기존 Notion은 이관 종료 전 `LEGACY_READ_ONLY`로 취급한다.
- [ ] 삭제·대량 이동·DB 구조 변경 없이 read/inventory부터 수행한다.
- [ ] 오래된 Notion 값은 current Decision으로 자동 승격하지 않는다.
- [ ] 프로젝트별 고유 용어·수치·승인 에셋을 임의 교정하지 않는다.

## 2. Notion 자료 전수 inventory

각 페이지·DB·record·attachment를 다음 중 하나로 분류한다.

| ID | 위치 | 종류 | current 여부 | 고유성 | 대상 owner | 처리 | 증거 |
|---|---|---|---|---|---|---|---|
| | | Page / DB / Table / Flow / Image / File / Decision / Evidence | Current / Candidate / Legacy / Unknown | Unique / Duplicate / Superseded / Empty | | MIGRATE / LINK / ARCHIVE / REJECT / BLOCKED | |

- [ ] Project Home과 직접 연결된 child page를 확인했다.
- [ ] AI/System 영역의 Work·Asset·Screen·Reference·Benchmark·System record를 확인했다.
- [ ] database view만 보지 않고 source record와 attachment를 확인했다.
- [ ] collapsed toggle·subpage·linked DB·relation·rollup의 숨은 의미를 확인했다.
- [ ] 이미지·파일·PDF·ZIP·audio attachment 존재 여부를 확인했다.
- [ ] URL만 남은 외부 자료는 접근 가능성과 provenance를 확인했다.
- [ ] 중복·후보·폐기 자료를 current canon과 분리했다.

## 3. 정본 대상 매핑

| 기존 Notion 역할 | 기본 이관 대상 | 확인 항목 |
|---|---|---|
| 프로젝트 개요·핵심 약속 | `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` | 플레이어 경험·차별점·범위 |
| 확정 Decision | `docs/canon/CURRENT_CONFIRMED_DECISIONS.md` 또는 decision log | ID·날짜·승인·supersession |
| 핵심 시스템·콘텐츠 | AI production spec 또는 domain canon | 규칙·상태·데이터·Acceptance |
| 표·밸런스·콘텐츠 DB | JSON/CSV/Markdown + schema | 열 의미·단위·ID·relation |
| Flow·상태도 | Mermaid/SVG/Markdown source | node·edge·조건·예외 |
| Visual Direction | design canon + PDF 장 | 스타일 의미·금지·consumer |
| 승인 runtime image | repository binary + `ASSET_MANIFEST.json` | path·SHA-256·consumer·상태 |
| 제작 원본·대용량 reference | project-local source 또는 Library non-canon | locator·hash·provenance |
| 작업 상태·다음 단계 | `docs/ACTIVE_CONTEXT.md` | current Goal·blocker·next |
| Codex 인계 | `docs/handoffs/CURRENT_CODEX_HANDOFF.md` | exact SHA·scope·acceptance |
| 구현·검수 증거 | `evidence/` 또는 project evidence owner | 환경·명령·결과·ceiling |
| 사람용 Home 요약 | 사용자용 상세 GDD PDF | source SHA·생성일·scope |

- [ ] 각 고유 항목에 repository owner 또는 명시적 non-canon 보관 위치가 있다.
- [ ] 하나의 의미를 두 active canon에 복제하지 않았다.
- [ ] repository 경로가 기존 프로젝트 구조와 맞고 빈 형식 파일을 만들지 않았다.

## 4. 텍스트·표·관계 데이터 이관

- [ ] 페이지 본문을 제목만이 아니라 의미 단위로 이관했다.
- [ ] 표의 열 이름·자료형·단위·기본값·허용값을 보존했다.
- [ ] relation/rollup/formula를 단순 텍스트로 잃지 않고 계산 또는 참조 의미를 기록했다.
- [ ] Project relation은 기존 record provenance를 보존했다: `PROJECT_RELATION_REQUIRED`.
- [ ] record ID·Decision ID·Asset ID·System ID를 가능한 한 유지했다.
- [ ] current/candidate/legacy/superseded 상태를 명시했다.
- [ ] 충돌한 값은 추측 병합하지 않고 source·date·authority를 기록했다.
- [ ] JSON/CSV가 runtime과 연결된다면 schema validation 또는 loader test를 실행했다.

## 5. 이미지·파일·binary 이관

미리보기·스크린샷·페이지에 보이는 thumbnail은 원본 이관 증거가 아니다.

- [ ] 각 attachment의 **원본 binary**를 확보했다.
- [ ] 파일명·MIME·가로세로·색공간·투명도 등 필요한 기술 속성을 확인했다.
- [ ] 원본 binary의 `SHA-256`을 계산했다.
- [ ] 실제 게임 소비 asset은 프로젝트가 통제하는 repository 경로에 저장했다.
- [ ] 대형 제작 원본은 project-local source 또는 Library non-canon 위치와 locator를 기록했다.
- [ ] 각 승인 asset에 actual consumer를 기록했다.
- [ ] `approval_status`와 `implementation_status`를 분리했다.
- [ ] provenance와 라이선스·상업 사용 경계를 기록했다.
- [ ] `assets/ASSET_MANIFEST.json` 또는 프로젝트 owner에서 binary/hash/path를 readback했다.
- [ ] repository에 나타났다는 사실만으로 Godot import·runtime 연결 완료를 주장하지 않았다.

권장 asset receipt:

```json
{
  "asset_id": "",
  "consumer": "",
  "repository_path": "",
  "sha256": "",
  "approval_status": "CANDIDATE | APPROVED",
  "implementation_status": "PENDING | READY | INTEGRATED | VERIFIED",
  "provenance": "",
  "source_locator": "",
  "readback": ""
}
```

## 6. Flow·Storyboard·시각 설명자료 이관

- [ ] Flow의 node·edge·condition·failure/recovery 의미가 보존됐다.
- [ ] Mermaid/SVG/Markdown source와 사람이 보는 렌더 결과를 모두 확인했다.
- [ ] Storyboard의 화면 순서·입력·상태·feedback·transition을 보존했다.
- [ ] 설명용 시각자료와 runtime asset을 구분했다.
- [ ] 사람용 PDF에 필요한 시각자료를 해당 시스템·화면 설명 근처에 배치했다.
- [ ] PDF 생성 성공과 실제 runtime 화면 검증을 구분했다.

## 7. AI·Codex 재수화 경로 교정

- [ ] `AGENTS.md`가 repository-first active owner를 가리킨다.
- [ ] `START_HERE`가 current canon과 구현 진입점을 연결한다.
- [ ] Active Context가 현재 Goal·blocker·next work를 반영한다.
- [ ] AI production spec에 승인 기획 의미와 acceptance가 있다.
- [ ] Codex handoff가 `exact_source_sha`를 포함한다.
- [ ] Codex handoff가 Notion page/database/attachment 조회를 필수로 요구하지 않는다.
- [ ] 승인 asset은 repository path + SHA-256 + manifest로 회수 가능하다.
- [ ] 새 채팅에서 GitHub만 fresh-read해 현재 작업을 재구성할 수 있다.

## 8. 사람용 PDF 점검

- [ ] PDF는 repository current canon에서 생성했다.
- [ ] `source_commit`이 exact 40자 SHA다.
- [ ] `canon_version`, `generated_at`, `included_scope`, `implementation_evidence_ceiling`이 있다.
- [ ] 핵심 시스템·콘텐츠·Flow·구현 원리를 사람이 이해할 수 있다.
- [ ] 승인 이미지·화면·도표가 적절한 문맥에 배치됐다.
- [ ] 오래된 Candidate·Legacy 자료가 current처럼 표시되지 않는다.
- [ ] PDF 검토 finding을 repository owner에 반영하고 필요 시 재생성했다.
- [ ] PDF 자체를 수정하고 repository 정본 반영을 생략하지 않았다.

## 9. Exact readback·검증

- [ ] 변경 파일 목록과 diff를 확인했다.
- [ ] Markdown 링크·경로·ID·schema reference를 확인했다.
- [ ] JSON/CSV/SVG 등 구조화 파일을 parse/validate했다.
- [ ] 각 binary의 repository blob과 SHA-256을 다시 확인했다.
- [ ] 필요한 test/build/import/runtime 검증을 실제 실행했다.
- [ ] test PASS ≠ runtime PASS ≠ UX PASS ≠ player PASS를 유지했다.
- [ ] 현재 검증하지 않은 환경·플랫폼·화면 상태를 명시했다.
- [ ] postmerge exact main readback을 수행했다.

## 10. 이관 잔여 카운터

아래 값을 실제 inventory에서 계산한다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

### 카운터 설명

- `NOTION_UNIQUE_CANON_COUNT`: repository·명시적 보관소에 원문 의미와 provenance가 없는 Notion 고유 항목
- `CODEX_NOTION_DEPENDENCY_COUNT`: 구현 재개·asset 회수·Acceptance 확인에 Notion 조회가 필수인 경로
- `ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT`: 활성 완료 계약이 Notion write/readback을 요구하는 수

판정:

```text
하나라도 1 이상
→ LEGACY_READ_ONLY
→ active workflow에서는 신규 쓰기 금지
→ 고유 항목 이관을 계속 추적

모두 0
→ NOTION_RETIRED_FROM_ACTIVE_FLOW
→ NO_DELETE_REQUIRED_FOR_RETIREMENT
```

`NO_DELETE_REQUIRED_FOR_RETIREMENT`: 퇴역 완료를 위해 Notion workspace를 삭제할 필요는 없다. 삭제는 별도 사용자 승인, backup, exact readback, rollback 불필요성 확인 뒤에만 수행한다.

## 11. 적대적 검토 5회

### Loop 1 — 정본 충돌

- [ ] 같은 Decision·수치·asset이 repository와 Notion에서 다를 때 current authority가 명확한가.
- [ ] 오래된 Notion 값을 조용히 덮어쓰거나 승격하지 않았는가.

### Loop 2 — 자료 손실

- [ ] 숨은 page·relation·attachment·원본 binary가 누락되지 않았는가.
- [ ] 미리보기나 요약으로 원문 의미를 잃지 않았는가.

### Loop 3 — 구현 인계

- [ ] 새 채팅/Codex가 exact repository SHA만으로 재수화 가능한가.
- [ ] runtime asset의 path/hash/consumer가 실제로 회수되는가.

### Loop 4 — 사람용 이해

- [ ] PDF가 핵심 시스템·콘텐츠·구현 원리를 충분히 설명하는가.
- [ ] PDF snapshot과 current repository의 시점 차이를 알 수 있는가.

### Loop 5 — 완료 과장·rollback

- [ ] 문서·test PASS를 runtime/player PASS로 확대하지 않았는가.
- [ ] 기존 Notion을 삭제하지 않고도 안전하게 rollback·재감사 가능한가.

새 blocking finding이 있으면 수정 후 전체 다섯 관점을 다시 확인한다.

## 12. 완료 receipt

```yaml
project:
repository:
merged_sha:
repository_primary_canon: CONFIRMED | BLOCKED
human_pdf:
  path:
  source_commit:
  review_status:
ai_production_spec:
  path:
  readback_status:
asset_manifest:
  path:
  verified_asset_count:
notion_state: LEGACY_READ_ONLY | NOTION_RETIRED_FROM_ACTIVE_FLOW
counters:
  NOTION_UNIQUE_CANON_COUNT:
  CODEX_NOTION_DEPENDENCY_COUNT:
  ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT:
validation:
  structural:
  test:
  runtime:
  ux:
remaining_risks:
rollback:
clean_review_exit: true | false
```
