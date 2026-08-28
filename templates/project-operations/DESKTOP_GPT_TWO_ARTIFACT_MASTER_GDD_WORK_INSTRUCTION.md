# Desktop GPT — Repository-First 2파일 통합 제작 기획서 작업지시문

> Template ID: `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`
> Default authority: `REPOSITORY_PRIMARY_PROJECT_CANON`
> Output count: `EXACTLY_TWO_DELIVERABLES`
> User download: `PDF_ONLY_USER_DOWNLOAD`
> Notion: `NOTION_INPUT_ONLY_NO_OUTPUT`
> Image generation: `NO_AUTOMATIC_IMAGE_GENERATION`

아래 블록을 대상 프로젝트의 새 Desktop GPT Work 채팅에 붙여 넣고 프로젝트명·저장소·현재 목표만 바꿔 사용한다.

---

## 실행 지시문

```text
@GitHub 필요 시 연결된 파일·프로젝트 도구를 사용해 <PROJECT_NAME>의 통합 제작 기획서를 repository-first 방식으로 완성해.

최상위 목표
- 사람용 상세 제작 기획서 PDF와 repository에 저장할 AI용 상세 기획·구현 명세 Markdown, 정확히 2개의 기본 산출물만 유지한다.
- 사람용 PDF만 사용자에게 다운로드 링크로 제공한다.
- AI Markdown은 다운로드 파일로 별도 제공하지 말고 repository path, branch, exact commit SHA, PR, validation result만 보고한다.
- 기존 Notion은 고유 미이관 자료가 있을 때 입력으로만 fresh-read한다. 신규 Notion page/database 작성, upload, sync, readback을 완료 조건으로 만들지 않는다.

정본과 fresh-read
1. Base 최신 completed main의 START_HERE.md, AGENTS.md, repository-first workspace contract/policy, GPT–Codex handoff policy를 읽는다.
2. 대상 프로젝트 최신 completed main, 모든 open/draft PR read-only 상태, project AGENTS.md, START_HERE, ACTIVE_CONTEXT, CURRENT_CONFIRMED_DECISIONS, design/document registry, 현재 AI spec·handoff·asset manifest, 실제 code/data/Scene/Resource/test/evidence를 읽는다.
3. 과거 채팅·memory·PDF·Library·Notion은 discovery 또는 migration input일 뿐 current repository canon을 덮지 않는다.
4. latest user decision과 repository truth가 충돌하면 충돌을 기록하고 latest authority를 따른다.
5. main이나 open PR이 작업 중 변경되면 stale 가정을 버리고 latest-main reconciliation을 수행한다.

기본 산출물
A. HUMAN_MASTER_GDD_PDF
- 시각자료가 포함된 사용자용 상세 제작 기획서다.
- 단순 소개·요약본이 아니라 핵심 시스템·콘텐츠와 실제 구현 원리를 사람이 이해할 수 있어야 한다.
- exact source branch/SHA, canon version, 포함 범위, 작성일, 승인 상태, 구현 상태, evidence ceiling, 미해결 결정과 blocker를 표지 또는 첫 페이지에 표시한다.
- PDF는 정본이 아니라 exact repository commit의 HUMAN_GDD_PDF_DERIVED_VIEW다.

B. AI_PRODUCTION_SPEC_MARKDOWN
- repository의 AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN owner에 저장한다.
- 권장 경로는 project AGENTS/registry가 정한 경로이며, 경로가 없을 때만 docs/canon/AI_GAME_SPEC.md 또는 docs/design/PROJECT_AI_PRODUCTION_SPEC.md를 제안한다.
- current project meaning, Codex implementation contract, data/state/asset/test/evidence를 구조화한다.

CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED
두 산출물에 다음을 실제 프로젝트 사실에 맞게 포함한다.
- 프로젝트 비전, 플레이어 약속, 핵심 감정, 첫인상, 의미 있는 선택과 trade-off, 차별점과 판매 포인트
- Core / Session / Meta Loop, 전체 game flow, 화면·씬·상태 전환
- 핵심·서브 시스템별 목적, trigger, input, state, rule, output, feedback, 예외, 의존성, 실패·복구
- 핵심 콘텐츠별 역할, 등장·획득 조건, 변주, 보상, 소비 시스템, 필요한 이미지·사운드·VFX
- 진행·경제·성장 구조와 data source/sink, softlock·snowball·save compatibility 위험
- UX/UI 화면 목적, 정보 우선순위, 조작, 상태, 접근성, 입력 장치와 해상도 제약
- Godot Scene/Node/Resource/Script 책임, data owner, signal/event payload, 상태 전이, save/load, asset integration, 구현 순서
- automated test, integration, Godot runtime, visual/audio consumption, play/UX, release evidence를 분리한 Acceptance Criteria
- 명시적 제외 범위, 보호 규칙, blocker, 위험, rollback, 다음 단일 milestone

SHARED_ID_AND_SOURCE_SHA_REQUIRED
- 두 산출물은 동일한 SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC ID registry를 사용한다.
- 같은 기준 branch와 exact source SHA를 기록한다.
- DOCUMENTED / CONFIRMED / IMPLEMENTED / AUTOMATED_TEST_PASS / RUNTIME_VERIFIED / UX_VERIFIED / RELEASE_READY를 분리한다.
- PDF 생성 전 AI spec과 actual repository 상태의 ID, 규칙, asset 상태, 구현 상태, evidence ceiling drift를 검사한다.

이미지·에셋 규칙
- 실제 game consumer, screen/scene/object/action/state에서 필요한 asset family를 역산한다.
- 승인된 기존 이미지와 실제 build capture를 우선 사용한다.
- 사용자가 이번 작업에서 이미지 생성·편집을 명시적으로 요청하지 않았다면 새 이미지를 만들지 않는다.
- candidate/reference/rejected와 approved runtime asset을 구분한다.
- 구현 asset은 repository_path, actual_consumer, approval_status, version, sha256, provenance, rights/license, implementation_status를 asset manifest에 기록하고 readback한다.
- Notion attachment가 없어도 repository path + manifest + SHA-256이 있으면 구현 입력이 될 수 있다. 반대로 Notion preview만 있고 repository input이 없으면 implementation-ready가 아니다.

산출물 제한
- NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX
- NO_SEPARATE_IMAGE_BUNDLE
- NO_NOTION_OUTPUT
- NO_AUTOMATIC_IMAGE_GENERATION
- 필요한 appendix, benchmark, traceability, asset matrix는 PDF와 AI Markdown 내부에 통합한다.

Notion·legacy migration
- 기존 Notion/Sheet에 고유 자료가 있으면 UNIQUE / DUPLICATE / OBSOLETE / BLOCKED_UNVERIFIED로 분류한다.
- UNIQUE는 repository canon, tracked runtime asset 또는 비정본 Library reference로 이동하고 provenance와 destination readback을 남긴다.
- 읽지 못한 범위는 BLOCKED_UNVERIFIED이며 duplicate/obsolete로 추정하지 않는다.
- 기존 Notion page/database는 삭제하지 않고 LEGACY_READ_ONLY로 둔다.
- 프로젝트 퇴역 완료 조건은 NOTION_UNIQUE_CANON_COUNT = 0, CODEX_NOTION_DEPENDENCY_COUNT = 0, ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0이다.

작업 방법
1. 현재 프로젝트 상태와 정본을 재구성한다.
2. 기존 reusable system, asset, reference, benchmark를 먼저 확인한다.
3. 최소 3개 실질 대안과 ADOPT / ADAPT / REJECT를 비교해야 하는 중요한 결정만 비교한다.
4. 의미 충돌·누락을 적대적으로 검토하고, 승인 범위의 안전한 교정은 계속 수행한다.
5. AI spec을 먼저 current repository canon으로 갱신하고 readback한다.
6. Codex 구현이 필요한 범위는 exact planning commit 기반 CURRENT_CODEX_HANDOFF를 만든다. 직접 Codex를 호출하거나 이미지를 생성하지 않는다.
7. 실제 implementation/test/runtime evidence가 있으면 반영하되, 실행하지 않은 검증을 PASS로 쓰지 않는다.
8. 의미 있는 review gate에서 PDF를 생성하고 모든 페이지를 render/readback해 글자 깨짐, 잘림, 표·이미지·목차 오류를 확인한다.
9. PDF 검토 수정은 repository canon으로 되돌린 뒤 필요한 경우 재생성한다.
10. exact-head test/CI, unresolved thread, current main freshness를 확인하고 허용 범위에서 PR·안전한 squash merge·postmerge readback까지 수행한다.

최종 사용자 보고
- 사용자 다운로드: 사람용 PDF 링크 1개만 제공
- AI spec: repository path / branch / exact commit SHA / PR / validation result 보고
- 작업 전 → 개선된 기능 → 실제 사용 예 → 기대효과 → trade-off → 미개선·미검증 범위 순으로 설명
- 사용한 Work Mode·Skill·검증 증거를 명시
- Base 정책 PASS와 개별 프로젝트 migration/runtime/UX PASS를 혼동하지 않음
- REQUIRED_WORK_REMAINING, blockers, rollback, 다음 단일 milestone을 보고
```

---

## Template 적용 확인

```yaml
project_name:
repository:
source_main_sha:
project_ai_spec_path:
human_pdf_output_path:
work_scope:
legacy_notion_locator:
image_generation_explicitly_requested: false
```

- [ ] 정확히 두 기본 산출물이다.
- [ ] 사용자 다운로드 링크는 PDF 하나다.
- [ ] AI Markdown은 repository identity로만 보고한다.
- [ ] Notion 신규 write/output을 만들지 않는다.
- [ ] 동일 ID와 exact source SHA를 사용한다.
- [ ] 핵심 시스템·콘텐츠와 Godot 구현 원리가 상세하다.
- [ ] 이미지 생성은 명시적 사용자 요청이 있을 때만 한다.
- [ ] 실행하지 않은 test/runtime/UX를 PASS로 표시하지 않는다.
- [ ] PDF render/readback과 repository readback을 각각 수행한다.
