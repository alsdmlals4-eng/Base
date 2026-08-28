# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다. Base 공용 원칙을 프로젝트의 엔진, 구조, 세계관, 용어, 보호 범위와 검증 방식에 맞게 분화한다.

## 1. Top-level continuity rule

새 채팅, 새 GPT, 새 Codex와 새 작업자가 과거 대화 없이 **프로젝트 저장소만으로** 방향, 현재 상태, 다음 작업, 보호 범위, 책임 원본과 검증 방법을 찾을 수 있어야 한다.

- 프로젝트 기획 정본은 핵심 경험·방향·범위·금지 방향을 책임진다.
- Roadmap은 단계·우선순위·선행 조건·종료 기준을 책임진다.
- Active Context는 현재 상태 원본이며 Handoff는 경계 시점 스냅샷이다.
- Documentation Map과 registry는 질문별 current owner를 연결한다.
- 같은 정보의 경쟁하는 활성 복제본을 만들지 않는다.
- PDF·대화·memory·Library·legacy workspace를 repository current truth로 승격하지 않는다.

## 2. Project identity

- Project name:
- Repository:
- Default branch:
- Engine:
- Language:
- Genre:
- Target platform:
- Core player promise:
- Pointed fun hypothesis:
- Current concept·PoC stage:
- Ambiguous project terms:

## 3. Base and current authority bootstrap

- Base repository: `alsdmlals4-eng/Base`
- Adopted Base version/freshness record: `docs/BASE_RULES_VERSION.md`
- Project-local Base copy: compatibility/cache가 있을 때만 사용하며 source commit과 동기화 날짜를 확인한다.

`current Base`는 과거 고정 파일 목록으로 추정하지 않는다. Base의 최신 completed `main`, `AGENTS.md`, `START_HERE.md`, current Documentation Map/Skill Registry와 현재 작업에 필요한 최소 owner를 확인한다. 프로젝트-local copy가 오래되면 최신 사용자 지시와 프로젝트 정본을 보호하며 current Base와 reconcile한다.

## 4. Repository-first project authority

```text
latest user instruction
→ this AGENTS.md + project security / engine / data rules
→ ACTIVE_CONTEXT + approved work contract + confirmed decisions
→ registered repository canon + actual code/data/assets/tests/runtime evidence
→ adopted current Base contract
→ Base remote
→ LEGACY_READ_ONLY_MIGRATION_SOURCE when unique material remains
→ external references / past conversation / memory / inference
```

### REPOSITORY_PRIMARY_PROJECT_CANON

```text
AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
→ project meaning / systems / content / UX / data / implementation contract

repository structured and runtime truth
→ Markdown / JSON / game data / code / Scene / Resource / config
→ tracked implementation asset / ASSET_MANIFEST
→ tests / build / runtime / play evidence
→ exact commit / PR / rollback history

HUMAN_GDD_PDF_DERIVED_VIEW
→ exact repository commit에서 생성한 사람용 상세 기획서 PDF

CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
```

- PDF는 독립 정본이 아니다.
- Work와 Library는 작업·참고·후보·PDF 보관 surface이며 repository version control을 대체하지 않는다.
- 신규 Notion page/database/write/upload/sync/readback은 기본 workspace, 승인 Gate, Codex 인계 또는 완료 조건이 아니다.
- 기존 Notion과 Google Sheets는 고유 미이관 자료가 있을 때만 `LEGACY_READ_ONLY_MIGRATION_SOURCE`로 읽는다.
- 과거 `DOMAIN_SPLIT_CANON`, `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`은 `LEGACY_DISCOVERY_ONLY` migration alias다.

## 5. Default reading order

작업 계약은 `github_issue` 또는 `approved_direct_request`다.

```text
this AGENTS.md
→ project START_HERE.md
→ ACTIVE_CONTEXT.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ Documentation Map / registry / current AI canon
→ CURRENT_CODEX_HANDOFF / ASSET_MANIFEST when relevant
→ same-Goal open and recent PR read-only reconciliation
→ actual code / data / Scene / Resource / assets / tests / runtime evidence
→ adopted current Base owner when required
→ legacy Notion/Sheet only when unique migration input may remain
```

`모두 확인`은 저장소 전체와 모든 과거 Base 문서를 무작정 읽는다는 뜻이 아니다. Archive·backup·deprecated·migration-only 자료는 현재 질문에 필요할 때만 progressive-load한다.

## 6. Project-specific rules

- Project terminology:
- Engine and language rules:
- Scene/Node/Resource responsibility:
- Data and save compatibility contract:
- UI/UX and input rules:
- Art/visual/audio rules:
- Protected approved assets:
- Story/canon protection:
- Security/privacy rules:
- Protected paths:
- Forbidden structures:
- Out-of-scope refactoring:
- Preserve current user changes:

## 7. Request-to-work rule

기능·게임 경험·아트 방향·구조·workflow 변경은 current Base의 intake owner인 `managing-project-intake-and-work-contract`를 사용한다. Registry가 successor/alias를 선언하면 current route를 따른다.

```text
route
→ current repository facts and actual implementation
→ reuse-first preflight
→ current project identity and protected scope
→ meaningful alternatives when required
→ implementation reality gate
→ bounded work contract
→ user approval for material new decisions
→ execution and evidence
```

오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행은 불필요하게 확대하지 않는다. 저장소에서 확인할 수 있는 사실은 사용자에게 다시 묻지 않는다.

- Work contract type: `github_issue` / `approved_direct_request`
- Current intake Skill/mode:
- Approval reference:
- Current executable contract:
- Protected scope:
- Explicit non-scope:
- Rollback:

Skill의 legacy Notion-first clause가 current repository-first workspace owner와 충돌하면 current owner가 우선한다.

## 8. Existing Solution First

신규 또는 의미 있게 개정하는 시스템·데이터/콘텐츠 구조·UI/UX·시각/asset·도구·workflow·Skill·QA/Test는 다음 순서로 확인한다.

```text
current project implementation / assets / tests
→ approved Project Asset / Reference / Benchmark
→ adopted Base reuse / knowledge / cases
→ directly related verified cross-project evidence
→ decision-relevant external benchmark
→ REUSE / ADAPT / REFERENCE_ONLY / NO_REUSE / BUILD_NEW
```

모든 프로젝트를 전수 검색하지 않는다. 프로젝트 정체성과 current canon이 Base reference보다 우선한다.

## 9. Core concept and PoC

핵심 컨셉·제약·뾰족한 재미·SWOT·MDA/DDE·PoC·기획 재조정은 current router가 지정한 game-concept Skill을 사용한다.

```text
frame
→ constrain
→ sharpen
→ structure
→ analyze
→ poc-contract
→ recalibrate
→ production-gate
```

- 기능 목록을 핵심 컨셉으로 대체하지 않는다.
- PoC는 가장 위험한 가설의 최소 검증이며 전체 게임이나 Vertical Slice로 팽창시키지 않는다.
- PoC 결과는 유지·증폭·변경·삭제·보류·재검증 결정에 반영한다.

## 10. Desktop GPT two-artifact master GDD

프로젝트 정본을 통합 상세 기획서로 정리할 때는 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 사용한다.

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN
```

- 사용자 기본 다운로드: `PDF_ONLY_USER_DOWNLOAD`.
- AI Markdown은 repository path·branch·exact commit SHA·PR·validation result로 보고한다.
- PDF와 AI Markdown은 같은 `SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC` ID와 source SHA를 사용한다.
- 두 산출물에 플레이어 가치, Core/Session/Meta Loop, 핵심·서브 시스템, 콘텐츠, UX/UI, 데이터·상태, 실제 asset/audio/VFX consumer, Godot Scene/Node/Script/Resource 구현 원리, Acceptance와 evidence ceiling을 포함한다.
- PDF review에서 승인된 변경은 repository canon에 먼저 반영한다.
- 별도 DOCX·ZIP·appendix·image bundle·Notion output을 기본 생성하지 않는다.
- 이미지 생성·편집은 사용자가 명시적으로 요청했을 때만 진행한다.

## 11. Asset and visual contract

이미지·사운드·VFX 요구는 실제 game consumer, screen/scene/object/action/state에서 역산한다.

`REPOSITORY_PATH_MANIFEST_SHA256_READBACK` 최소 필드:

```text
asset_id
repository_path
actual_consumer
approval_status
version
sha256
source_or_provenance
rights_or_license_state
implementation_status
supersedes_or_replaced_by
```

- candidate/reference/rejected와 current-use approved runtime asset을 구분한다.
- Notion preview나 attachment만으로 implementation-ready가 아니다.
- repository asset과 manifest가 없으면 `GPT_VISUAL_REQUEST` 또는 명시적 blocker다.
- 사용자가 명시하지 않은 새 이미지 생성·교체를 자동 승인으로 해석하지 않는다.

## 12. GPT–Codex role boundary

GPT는 기획·조사·검수·명시적으로 승인된 이미지 작업·repository AI canon·Codex handoff·최종 검수를 담당한다.

Codex는 actual Godot product implementation이 필요한 `PLAY_MEANINGFUL_WORK_SLICE`에서만 진입한다.

```text
repository AI canon and current handoff
→ EXACT_REPOSITORY_COMMIT
→ actual code/data/Scene/Resource/asset/test fresh-read
→ bounded Godot implementation
→ automated/runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ CANON_SYNC_AFTER_VALIDATION
```

Notion 부재만으로 Codex를 막지 않는다. 코어·경제·주요 UX·서사·Art Direction·승인 asset 의미·플랫폼/비용/보안 경계 변경이 필요하면 `CHANGE_PROPOSAL`로 반환한다.

## 13. Legacy migration gate

기존 Notion/Sheet의 고유 자료를 이관할 때만 `NOTION_OPERATION_GATE.md`와 migration checklist를 적용한다.

```text
exact project and source identity
→ current source read
→ UNIQUE / DUPLICATE / OBSOLETE / BLOCKED_UNVERIFIED
→ smallest bounded migration
→ repository canon / tracked asset / non-canon Library reference
→ provenance
→ destination readback
→ consumer check
→ legacy read-only
```

- 읽지 못한 자료를 duplicate/obsolete로 추정하지 않는다.
- 전체 page replacement보다 targeted read/write를 우선한다.
- 사용자 승인 없이 page/database/attachment를 삭제하지 않는다.
- project retirement claim:

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

이 count의 0은 runtime·UX·release PASS가 아니다.

## 14. GitHub and concurrency

- current open PR 번호를 template에 고정하지 않는다.
- 작업 시작 시 실제 GitHub 상태를 확인한다.
- 다른 workstream open/draft/ready PR은 read-only다.
- 명시적 권한 없이 수정·흡수·close·rebase·merge하지 않는다.
- current task PR도 exact head, required checks, review, unresolved thread, ruleset과 current main freshness를 확인한다.
- force push, direct main, destructive reset/clean, admin/ruleset bypass를 사용하지 않는다.
- repository가 squash-only면 squash merge만 사용한다.

## 15. Required environment and cost

- Required tools and files:
- Required accounts and repository permissions:
- Installation/readback commands:
- Current paid plan:
- Separately metered dependency:

기본 경로는 추가 금전 지출 0이다. 승인 없이 신규 유료 SaaS·API·credit·runner·storage를 필수화하지 않는다. 필요한 도구·권한이 없으면 이유, 최소 설치·적용 방법과 확인 명령을 제시한다.

## 16. Validation

- Contract and diff check:
- Format/lint:
- Automated tests:
- Godot run path:
- Save/load:
- Asset manifest readback:
- Edge/failure/counterexample:
- Adjacent regression:
- Manual review:
- Cold-start review:
- PDF render/readback when generated:
- Evidence report:
- Destination readback:
- Rollback:

`DOCUMENTED`, `CONFIRMED`, `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, `RELEASE_READY`를 분리한다. 실행하지 않은 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`와 사유를 기록한다.

## 17. Completion and correction gate

계획된 task가 소진되거나 `required_work_remaining: 0`이어도 즉시 완료하지 않는다.

```text
REMAINING_WORK_RECALCULATION_REQUIRED
→ remaining == 0이면 COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ final POST_CHANGE_MONITOR_LOOP
→ minimum required full-scope loops, then until CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ completion report
```

병합 뒤에는 `POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP`로 exact main의 repository owner, actual implementation, asset manifest, evidence, PDF source identity와 legacy migration 잔여를 다시 확인한다.

## 18. End-of-work and learning

1. 프로젝트 고유 결정·수치·구현 상태를 올바른 repository owner와 tests/Roadmap에 반영한다.
2. Active Context를 최신화하고 필요 시 Handoff snapshot을 만든다.
3. Skill·Documentation Map·Issue·Plan 연결을 확인한다.
4. 실패·중요 결정·재사용 교훈·검증 결과를 Learning Log에 기록한다.
5. 공용화 가치가 있으면 current Base proposal lifecycle로 제안한다.
6. 새 작업자가 cold-start 질문에 답할 수 있는지 확인한다.
7. remaining-work recalculation·correction rescan·adversarial clean exit evidence를 남긴다.

## 19. Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작·결정·자산
## 플레이어 경험·핵심 시스템·콘텐츠 변화
## 구현·문서·asset 변경
## 검증 판정과 evidence ceiling
## 작업 전 → 개선 기능 → 실제 사용 예 → 기대효과 → trade-off
## legacy migration status
## 미검증·남은 위험·rollback
## next single milestone
```
