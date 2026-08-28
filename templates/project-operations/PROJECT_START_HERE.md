# [프로젝트명] 시작 지점

> 사용자, 새 GPT, 새 Codex와 새 작업자가 프로젝트 전체 상태를 가장 먼저 확인하는 repository-first 대시보드다. 기획·결정·데이터 의미는 등록된 repository owner를, 구현 상태는 실제 파일·asset·test·runtime evidence를 따른다.

- 공식 위치: 프로젝트 `AGENTS.md` 또는 Documentation Map이 선언한 `START_HERE.md`
- 현재 repository: 
- 기준 branch: 
- 기준 commit: 
- AI 기획 정본: 
- Active Context: `ACTIVE_CONTEXT.md`
- 확정 결정: `CURRENT_CONFIRMED_DECISIONS.md`
- current Codex handoff: 
- Asset Manifest: 
- 기획서 Registry: `DESIGN_DOCUMENT_REGISTRY.json`
- Skill Registry: `SKILL_REGISTRY.json`
- 사람용 상세 기획서 PDF: exact source commit의 `HUMAN_GDD_PDF_DERIVED_VIEW`

## 1. Authority

```text
latest user instruction
→ project AGENTS.md + security / engine / data rules
→ ACTIVE_CONTEXT + approved work contract + confirmed decisions
→ repository canonical Markdown / JSON / game data / tracked assets
→ actual code / Scene / Resource / tests / build / runtime evidence
→ adopted current Base contract
→ LEGACY_READ_ONLY_MIGRATION_SOURCE when unique material remains
→ external references / memory / past conversation / inference
```

### Current workspace contract

```text
REPOSITORY_PRIMARY_PROJECT_CANON
AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
HUMAN_GDD_PDF_DERIVED_VIEW
CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
```

- PDF는 독립 정본이 아니다.
- ChatGPT Work와 Library는 작업·참고·후보·PDF 보관 surface이며 repository version control을 대체하지 않는다.
- 신규 Notion page/database/write/upload/sync/readback은 기본 작업 또는 완료 조건이 아니다.
- 기존 Notion/Sheet는 고유 미이관 자료가 있을 때만 `LEGACY_READ_ONLY_MIGRATION_SOURCE`로 읽는다.
- 과거 `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`, `DOMAIN_SPLIT_CANON`은 `LEGACY_DISCOVERY_ONLY` alias다.

## 2. 공용 작업목표와 병합 후 종료 조건

- `BEST_LONG_TERM_EFFICIENT_METHOD`: 사용자·플레이어 가치, 정확성, 출시 품질, 유지보수성, 재사용성, 되돌리기 가능성과 수명주기 총비용을 함께 비교한다.
- `QUALITY_OVER_RESPONSE_SPEED`: 중요한 작업은 필요한 조사·추론·도구 실행·검증을 실제로 수행한다.
- `BENCHMARK_PRACTICE_COMPARISON`: 중요한 결정은 현행 상태와 최소 3개 실질 대안을 공식/1차 자료, 현업 성공·실패 사례와 비교한다.
- `POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP`: 병합 뒤 exact new main에서 repository owner, 실제 구현·asset manifest·test/evidence와 해당 Gate의 PDF identity를 다시 읽는다. 유효 finding은 latest main의 새 Branch/PR에서 교정하고 남은 작업을 재계산한다.
- `ISSUE_SUCCESSOR_FRESHNESS_REQUIRED`: Issue를 사용하는 프로젝트는 exact main·current canon·실제 구현·evidence와 open/closed Issue를 다시 대조한다. Issue 상태만으로 현재 권한이나 완료를 만들지 않는다.
- `FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK`: 계획된 작업이 끝난 뒤 remaining-work recalculation, implementation correction rescan, adversarial clean exit를 수행한다.

## 3. 한눈에 보기

| 항목 | 현재 기준 |
|---|---|
| 한 줄 약속 |  |
| 대상 플레이어 |  |
| 핵심 행동·선택 |  |
| 뾰족한 재미 가설 |  |
| 첫인상·핵심 감정 |  |
| 차별점·판매 포인트 |  |
| 장르·플랫폼 |  |
| 엔진·핵심 기술 |  |
| 현재 제품 단계 |  |
| 현재 작업 Gate |  |
| 다음 Greenlight |  |
| 최우선 작업 |  |
| 가장 큰 위험 |  |
| 기준 Git commit |  |
| Base 기준 commit |  |
| 최근 운영체계 Health Review |  |
| 최근 postmerge repository readback |  |
| 현재 사람용 PDF source SHA |  |

## 4. 현재 상태

| 구분 | 요약 | 책임 원본·실제 증거 |
|---|---|---|
| 확정 |  |  |
| 구현 |  |  |
| 자동 테스트 |  |  |
| runtime 검증 |  |  |
| UX/플레이 검증 |  |  |
| 진행 중 |  |  |
| 미확정·확인 필요 |  |  |
| 보류 |  |  |
| 불일치 |  |  |

`DOCUMENTED`, `CONFIRMED`, `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, `RELEASE_READY`를 서로 다른 상태로 유지한다.

## 5. 핵심 플레이어 경험

- 한 문장 핵심 컨셉:
- 플레이어가 반복해서 보는 것:
- 반복해서 판단하는 것:
- 반복해서 행동하는 것:
- 행동 직후 받아야 하는 피드백:
- 다음 플레이를 부르는 동기:
- 지켜야 할 감정·약속:
- 의미 있는 선택과 포기:
- 금지 방향:
- 현재 PoC 가설·결과:

프로젝트 전체의 상세 방향은 `DESIGN_DOCUMENT_REGISTRY.json` 또는 프로젝트가 선언한 AI canon owner에서 찾는다. 핵심 컨셉·뾰족한 재미·PoC가 미확정이면 `analyzing-and-refining-game-concepts`를 사용한다.

## 6. 현재 개발 단계와 Gate

| 구분 | 현재 상태 | 진입 조건 | 종료 기준 | evidence | 책임 원본 |
|---|---|---|---|---|---|
| 기획 방향·PoC |  |  |  |  | AI canon |
| 작업 실행 Gate |  |  |  |  | `DEVELOPMENT_GATES.md` |
| 제품 milestone |  |  |  |  | Roadmap·actual project |
| 사람용 PDF review |  |  |  |  | PDF export checklist |

```text
기획: 핵심 컨셉 → 제약 → 뾰족한 재미 → 기획 요소 정렬 → PoC → 재조정 → Production 판정
작업: Intake·Context → Ready → Approval → Implementation → Verification → Canon Sync → Completion
제품: Concept → Prototype → Graybox → First Playable → Vertical Slice → Production → Alpha → Beta → Release Candidate
```

## 7. 활성 책임 원본

| 분야·책임 범위 | repository owner | runtime consumer | 상태 | source commit | evidence / next work |
|---|---|---|---|---|---|
| 프로젝트 전체 AI spec |  |  |  |  |  |
| confirmed decisions |  |  |  |  |  |
| current context |  |  |  |  |  |
| current handoff |  |  |  |  |  |
| 시스템 |  |  |  |  |  |
| 콘텐츠 |  |  |  |  |  |
| UX/UI |  |  |  |  |  |
| 데이터·밸런스 |  |  |  |  |  |
| asset/audio/VFX |  |  |  |  |  |
| tests/runtime evidence |  |  |  |  |  |

작은 프로젝트에서 여러 책임을 한 owner에 통합하면 `responsibility_coverage`에 범위를 기록한다. 프로젝트가 사용하지 않는 분야를 강제로 만들지 않는다.

## 8. Desktop GPT 2파일 통합 기획서

프로젝트 정본을 상세 기획서로 정리하는 작업에서는 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 적용한다.

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN
```

- 사용자 다운로드: `PDF_ONLY_USER_DOWNLOAD`.
- AI Markdown은 repository path·branch·exact commit SHA·PR·validation result로 보고한다.
- 두 산출물은 같은 `SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC` ID와 exact source SHA를 사용한다.
- PDF는 핵심 시스템·콘텐츠·UX/UI·데이터·실제 asset consumer와 Godot 구현 원리를 사람이 이해할 수 있는 상세도로 포함한다.
- PDF 검토 수정은 repository canon으로 되돌린다.
- 별도 DOCX·ZIP·appendix·image bundle·Notion output을 기본 생성하지 않는다.
- 이미지 생성·편집은 사용자가 명시적으로 요청했을 때만 진행한다.

관련 Template:

- `AI_PROJECT_CANON_SPEC.md`
- `HUMAN_GDD_PDF_EXPORT_CHECKLIST.md`
- `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md`

## 9. 최신 시각·사운드 자료

| ID | 항목 | actual consumer | approval/version | repository path | SHA-256 | 구현·runtime 상태 | 차이·다음 작업 |
|---|---|---|---|---|---|---|---|
| AST-001 |  |  |  |  |  |  |  |
| AUD-001 |  |  |  |  |  |  |  |

콘셉트 이미지, candidate/reference, 승인된 runtime asset과 실제 build capture를 같은 상태로 취급하지 않는다.

`REPOSITORY_PATH_MANIFEST_SHA256_READBACK`이 없는 구현 입력은 implementation-ready가 아니다. Notion attachment 부재만으로 구현을 막지 않는다.

## 10. 프로젝트 Skill 시작 경로

- 요청 접수·작업 계약: `managing-project-intake-and-work-contract`
- 운영체계 설치·감사·legacy 이관: `managing-game-project-operating-system`
- 기획 책임 원본·발행: `managing-design-documents`
- 프로젝트 Skill 통합·학습: `evolving-project-discipline-skills`
- Active Context·Handoff: `maintaining-project-context-and-handoff`
- 핵심 컨셉·SWOT·MDA/DDE·PoC·재조정: `analyzing-and-refining-game-concepts`
- 변경·외부 AI 결과 검증: `reviewing-and-validating-project-changes`
- 적대적 검토: `running-adversarial-review-and-refinement`
- Base 제안: `managing-base-change-proposals`
- current interview: `INTERVIEW_REGISTRY.json`의 활성 항목 또는 없음
- 확정 실행 계약: 승인된 contract 경로 또는 없음
- 현재 작업의 주 책임 Skill:
- 필요한 Foundation Skill:
- 후속 단계에서만 실행할 mode·Skill:
- Learning Log:

전체 skills 폴더를 읽지 않고 현재 작업에 필요한 최소 Skill만 선택한다. Skill의 legacy Notion token은 current repository-first workspace policy보다 높은 권한을 갖지 않는다.

## 11. 새 작업자의 읽기 순서

```text
project AGENTS.md
→ this START_HERE.md
→ ACTIVE_CONTEXT.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ Documentation Map·Development Gates
→ AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN owner
→ CURRENT_CODEX_HANDOFF·ASSET_MANIFEST
→ Design Document Registry·현재 분야 owner
→ Skill Registry·필요한 Skill과 mode
→ Roadmap·Issue·Goal·Plan
→ actual code·data·Scene·Resource·assets·tests·evidence
→ exact source commit의 human PDF when review requires it
→ legacy Notion/Sheet only when unique migration input may remain
```

별도 `HANDOFF.md`는 경계 시점의 스냅샷이며 두 번째 활성 현재 상태 원본으로 사용하지 않는다.

## 12. Legacy migration state

| Legacy ID | source | classification | destination | destination readback | active consumer | 상태 |
|---|---|---|---|---|---|---|
| LEGACY-001 |  | UNIQUE / DUPLICATE / OBSOLETE / BLOCKED_UNVERIFIED |  |  |  |  |

```text
NOTION_UNIQUE_CANON_COUNT =
CODEX_NOTION_DEPENDENCY_COUNT =
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT =
```

세 값이 모두 0이고 모든 UNIQUE destination readback이 PASS일 때만 해당 프로젝트의 Notion dependency 제거를 주장한다. 기존 page/database는 사용자 삭제 지시 없이 제거하지 않는다.

## 13. 지금 하지 말아야 할 것

- 보류 영역을 재개 승인 없이 구현하지 않는다.
- 기존 승인 이미지가 있는 항목의 새 시안을 별도 지시 없이 만들지 않는다.
- JSON·PDF·asset manifest 존재를 구현·검증 완료로 표시하지 않는다.
- PDF를 독립 정본으로 수동 유지하지 않는다.
- 기획 owner를 Registry 밖에 중복 생성하지 않는다.
- 기능 목록을 핵심 컨셉이나 PoC evidence로 대체하지 않는다.
- 정의되지 않은 약어를 임의 해석하지 않는다.
- 범위 밖 리팩터링과 기능 확장을 현재 작업에 섞지 않는다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 백업·보류·제거 후보를 기본 context에 포함하지 않는다.
- 전체 skills 폴더를 기본 로드하지 않는다.
- 사용자 승인 전 기존 프로젝트 파일이나 legacy workspace를 대량 삭제·이동·통합하지 않는다.
- 신규 Notion workspace나 GitHub+Notion 이중 sync를 기본 완료 조건으로 만들지 않는다.
- Issue가 open/closed라는 이유만으로 구현 권한이나 완료를 단정하지 않는다.

## 14. 다음 작업

| 우선순위 | 작업 | 주 책임 | 영향 분야 | 선행 조건·Ready | 완료 기준 | 검증 | owner·Skill |
|---:|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |

## 15. 최근 결정과 변경

- 최근 결정: `CURRENT_CONFIRMED_DECISIONS.md` / `DECISION_LOG.md`
- 최근 변경: `CHANGELOG.md`
- 현재 단계·Gate: `DEVELOPMENT_GATES.md`
- AI canon: 
- current handoff: 
- Asset Manifest: 
- Skill Registry: `SKILL_REGISTRY.json`
- 최근 운영체계 Health Review:
- 최근 변경 검증:
- 최근 issue successor freshness:
- 최근 human PDF review source SHA:

## 16. 콜드 스타트 확인

새 작업자는 다음을 답할 수 있어야 한다.

- 게임의 핵심 약속과 뾰족한 재미는 무엇인가?
- 현재 PoC·구현·검증 상태와 다음 Gate는 무엇인가?
- 무엇을 변경하면 안 되는가?
- repository의 현재 AI canon, decisions, handoff, asset manifest와 runtime evidence는 어디인가?
- 현재 작업에 필요한 Skill과 mode는 무엇인가?
- 사람용 PDF의 source commit과 evidence ceiling은 무엇인가?
- legacy Notion/Sheet에 남은 고유 자료와 dependency count는 무엇인가?
- 다음 단일 milestone과 rollback은 무엇인가?
