# Periodic External Source Watchlist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans task-by-task. This file records the implemented scope and remaining verification gate.

**Goal:** Base에 게임 제작뿐 아니라 프롬프트·Agent 작업구조·Skill 진화·소설/게임 스토리·YouTube/영상 편집 외부 Source를 주기적으로 발견·검증·흡수하는 공용 Watchlist를 추가한다.

**Architecture:** 새 ACTIVE Skill이나 scheduler를 만들지 않는다. 하나의 Base-wide Watchlist가 Source 발견을 담당하고 기존 owner가 적용을 담당한다. 초기 bootstrap 기간은 2026-02-10~2026-08-10이며, 모든 사이트의 전체 corpus를 증명할 수 없을 때는 `PARTIAL_INDEX_REVIEW`로 제한한다.

## Global constraints

- [x] 새 ACTIVE Skill `0`
- [x] 새 Work Mode `0`
- [x] `skills/SKILL_REGISTRY.json` 변경 없음
- [x] `[수정제안서]/PROPOSAL_REGISTRY.json` 변경 없음
- [x] release lock / frozen artifacts 변경 없음
- [x] GitHub Actions `contents: read` 유지
- [x] discovery/news/vendor 글을 정본으로 승격하지 않음
- [x] 원출처 역추적과 적대적 검토 유지
- [x] 새 사이트 추가는 repeat-value / owner / overlap / commercial-interest gate 통과 시 허용

## Task 1 — RED contract

**Files**
- `tests/test_periodic_external_source_watchlist.py`
- `.github/workflows/validate-evidence-knowledge.yml`

- [x] Watchlist/recent-review/one-hop consumer가 없으면 실패하는 test를 먼저 추가.
- [x] CI path/py_compile/unittest/artifact에 test 연결.
- [x] Draft PR #250에서 production docs 전 expected RED 확인.

## Task 2 — Initial source research

**Domains**

```text
GAME_DEVELOPMENT
PROMPT_AND_AGENT_WORKFLOW
SKILL_AUTHORING_AND_EVOLUTION
FICTION_AND_INTERACTIVE_NARRATIVE
YOUTUBE_AND_VIDEO_EDITING
```

- [x] Hada + game development 초기 pool 검토.
- [x] Prompt/agent/Skill 공식 Source 확장: OpenAI, Anthropic, GitHub Copilot, Google, Microsoft.
- [x] Fiction/interactive narrative Source 확장: Reedsy, inkle/ink, Yarn Spinner, IGDA Game Writing, Emily Short, GDC narrative.
- [x] YouTube/editing Source 확장: YouTube official Analytics/Help, Blackmagic DaVinci Training, Frame.io, vidIQ, game marketing cases.
- [x] 추가 Source: How To Market A Game, Deconstructor of Fun, AMD GPUOpen.
- [x] 2026-02-10~2026-08-10에 대해 `FULL_INDEX_REVIEW / PARTIAL_INDEX_REVIEW / STATIC_REFERENCE_REVIEW`를 구분.
- [x] 글 개수보다 reusable topic cluster와 Base overlap/disposition을 기록.

**Output**
- `docs/knowledge/game-development/RECENT_EXTERNAL_EVIDENCE_REVIEW_2026-08-10.md`

## Task 3 — Implement Base-wide Watchlist

**File**
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`

- [x] Source domain / role / use / limitation 정의.
- [x] 새 사이트 추가 Gate 정의.
- [x] `ORIGINAL_SOURCE_BACKTRACE` 정의.
- [x] freshness / dedupe / same-goal PR / adversarial review 정의.
- [x] market/vendor benchmark guardrail 정의.
- [x] future delta scan과 full-rescan trigger 정의.
- [x] Base가 scheduler가 아니라는 경계 명시.

## Task 4 — Integrate into existing owners

### Game evidence

- [x] `docs/knowledge/game-development/README.md` one-hop discovery.
- [x] `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`에 discovery-only 연결과 playtest evidence-type 보강.
- [x] `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`에서 fresh candidate → original-source verification 연결.

### Prompt / Agent / Skill

- [x] `docs/AI_SKILL_ADOPTION_GUIDE.md`에서 Watchlist 연결.
- [x] Prompt / Instruction / Skill / Agent / deterministic Tool 배치 Gate 추가.
- [x] reusable prompt minimum contract 추가.
- [x] monolithic prompt 분리 조건을 independent responsibility/test/routing으로 제한.
- [x] agent/Skill over-fragmentation 방지.
- [x] eval에 harness/tool/permission/budget/configuration 영향 검토 추가.
- [x] 새 Skill을 만들지 않고 `evolving-project-discipline-skills`의 consolidation-first를 유지.

### Fiction / game narrative

- [x] `NARRATIVE_AND_RELATIONSHIP_METHOD.md`에서 Watchlist 연결.
- [x] 소설과 게임 스토리의 공통 craft / medium-specific boundary 추가.
- [x] `CANON_AND_CONTINUITY → DEVELOPMENTAL_STRUCTURE → SCENE_AND_CHARACTER → DIALOGUE_AND_INFORMATION → LINE_AND_PROSE → COPY_AND_PROOF → CROSS_RANGE_RECONCILIATION` 퇴고 순서 추가.
- [x] `templates/planning/NARRATIVE_CONTENT_PLAN.md`의 존재하지 않는 `docs/planning/NARRATIVE_CONTENT_METHOD.md` 참조를 현행 owner로 수정.

### YouTube / editing

- [x] `producing-game-development-youtube-videos`에서 Watchlist 연결.
- [x] story/evidence-first rough cut → trim → dialogue/audio → graphics/captions → color/VFX → export QC 순서 추가.
- [x] versioned review record 추가.
- [x] YouTube 공식 metric 정의 우선 / vendor benchmark context-limit 추가.
- [x] retention drop/spike/rewatch를 observation으로 한정.
- [x] `EPISODE_PACKET.md`에 edit review rounds, expanded Analytics/sample context 추가.

## Task 5 — Protected-boundary adversarial review

- [x] discovery-feed authority inflation 공격.
- [x] six-month recency bias 공격.
- [x] vendor benchmark 과잉 일반화 공격.
- [x] Skill/agent 수 증가 = capability 향상 오해 공격.
- [x] 소설 선형 craft ↔ 게임 agency/state 혼동 공격.
- [x] YouTube CTR/retention → 판매/품질 인과 오해 공격.
- [x] open PR #247의 UI/UX/accessibility owner와 중복 구현 회피.
- [x] partial-file overwrite로 `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md` tail이 잘린 회귀를 diff review에서 발견하고 복구.

## Task 6 — Final validation

- [x] 전용 Evidence Knowledge CI가 game-only 구현 단계에서 GREEN인 것을 확인.
- [ ] 확장된 5-domain exact PR head에서 Evidence Knowledge CI GREEN 확인.
- [ ] Base v9 / Game Project OS / Dependency Review / 관련 workflow exact-head 상태 확인.
- [ ] 최종 diff에서 보호 Registry/Proposal Registry/release artifacts 변경 0 재확인.
- [ ] unresolved review thread / merge conflict 확인.
- [ ] PR body를 최종 범위·검증 결과로 갱신하고 Draft를 해제.
- [ ] 승인된 범위와 모든 required check가 만족되면 PR을 병합하고 main exact commit 검증.

## Task 7 — External scheduler sync

- [ ] 기존 `Base 개선 소스 스캔` Automation을 중복 생성하지 않고 갱신.
- [ ] Automation이 최신 Watchlist 5개 domain을 읽도록 설정.
- [ ] 새 Source 추가 Gate·original-source backtrace·adversarial review·low-risk-only automatic update를 유지.
- [ ] 의미 있는 근거가 없으면 `NO_CHANGE`를 정상 보고하도록 유지.
