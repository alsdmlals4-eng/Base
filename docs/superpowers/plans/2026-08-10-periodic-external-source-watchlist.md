# Periodic External Source Watchlist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base에 게임 제작 외부 정보원 주기 수집·원출처 역추적·6개월 bootstrap 검토·적대적 선별 계약을 기존 Evidence Knowledge 구조 안에 추가한다.

**Architecture:** 새 ACTIVE Skill이나 scheduler 구현을 만들지 않는다. `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`를 수집 계약의 단일 Reference로 추가하고, `REFERENCE_SOURCE_CATALOG.md`, Evidence Method, Knowledge Hub, Planning Evidence Policy가 이를 한 단계로 발견하도록 연결한다. 2026-02-10~2026-08-10 자료 조사는 별도 evidence review에 기록하고, 반복 검증된 공용 원칙만 기존 owner 문서에 최소 보강한다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, existing Base Evidence Knowledge governance.

## Global Constraints

- 새 ACTIVE Skill: `0`
- 새 Work Mode: `0`
- `[수정제안서]/PROPOSAL_REGISTRY.json`: 변경 금지
- `skills/SKILL_REGISTRY.json`: 변경 금지
- release lock / frozen snapshot: 변경 금지
- GitHub Actions permission: `contents: read` 유지
- 외부 발견 글은 정본이 아니며 가능한 경우 원출처로 역추적한다.
- 2026-02-10~2026-08-10 기간 전체가 실제로 노출되지 않는 출처는 `PARTIAL_INDEX_REVIEW`로 표시한다.
- 조사 중 반복 가치가 확인된 새 사이트는 source role·evidence tier·이해관계·중복 여부를 판정한 뒤 추가할 수 있다.
- 외부 원문 전체를 저장소에 복제하지 않는다.
- 정책 의미·Skill owner·보안·권한·라이선스·대규모 구조 변경은 자동 확정하지 않는다.

---

### Task 1: Define RED repository contract

**Files:**
- Create: `tests/test_periodic_external_source_watchlist.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

**Interfaces:**
- Consumes: existing Evidence Knowledge hub and workflow.
- Produces: executable contract requiring the new watchlist, six-month review, hub/method linkage, source roles, original-source backtrace, disposition and no-new-Skill boundary.

- [ ] **Step 1: Write the failing test**

Create a `unittest` that asserts:
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` exists.
- `docs/knowledge/game-development/RECENT_EXTERNAL_EVIDENCE_REVIEW_2026-08-10.md` exists.
- watchlist includes `Hada GeekNews`, `Godot`, `Steamworks`, `GDC Vault`, `Games User Research`, `GameDiscoverCo`, `SteamDB`, `ORIGINAL_SOURCE_BACKTRACE`, `ADOPT`, `ADAPT`, `TEST`, `AVOID`, `IGNORE`, `REFERENCE_ONLY`, `2026-02-10`, `2026-08-10`, `FULL_INDEX_REVIEW`, `PARTIAL_INDEX_REVIEW`, `AUTHORITY_TARGET`, `PROFESSIONAL_PRACTICE`, `DISCOVERY_FEED`, `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE`.
- hub, Evidence Method and Planning Evidence Policy reference the watchlist.
- recent review includes explicit review coverage and improvement dispositions.
- workflow executes this test.
- `skills/SKILL_REGISTRY.json` is not required to change.

- [ ] **Step 2: Wire the new test into CI before production docs exist**

Add `tests/test_periodic_external_source_watchlist.py` to path triggers, `py_compile`, `unittest`, and uploaded evidence in `validate-evidence-knowledge.yml` while preserving `contents: read`.

- [ ] **Step 3: Open Draft PR and verify RED**

Expected failure: missing watchlist/recent-review production documents or missing hub/method linkage. Existing unrelated contract tests should remain green.

### Task 2: Research and classify the source pool

**Files:**
- Create: `docs/knowledge/game-development/RECENT_EXTERNAL_EVIDENCE_REVIEW_2026-08-10.md`

**Interfaces:**
- Consumes: web-accessible archives/blogs/changelogs from 2026-02-10 through 2026-08-10 and current Base contracts.
- Produces: compact evidence inventory, source coverage status, topic clusters, original-source backtrace, Base overlap and disposition.

- [ ] **Step 1: Scan the initial source pool**

Review the recent index/archive/search surfaces for Hada GeekNews, Godot, Steamworks, Android Developers Games, Google Play developer policy/quality, Xbox Accessibility Guidelines, GDC Vault, Game Developer, Games User Research, GameDiscoverCo, GameAnalytics, The Level Design Book, Game Accessibility Guidelines, 80 Level and SteamDB.

- [ ] **Step 2: Discover additional high-value sources**

Search for sources that materially add coverage in indie production/postmortem, game UX/research, technical art, performance, storefront/market, accessibility or AI-assisted game development. Add only if they satisfy the design's repeat-value and non-duplication gate.

- [ ] **Step 3: Cluster recent findings**

Group findings by reusable topic rather than article count, for example:
- engine/version migration and compatibility
- performance budgets and measurement
- store/demo/discovery validation
- playtesting and observation validity
- accessibility from design through testing
- production documentation and iteration
- art/technical-art pipeline
- telemetry/retention interpretation
- AI-assisted development/evals/security

- [ ] **Step 4: Compare every candidate with Base**

Classify each material cluster as `NO_CHANGE`, `EVIDENCE_ONLY_UPDATE`, `LOW_RISK_BOUNDED_UPDATE`, `BCP_OR_USER_DECISION`, or `REJECTED_OVERGENERALIZATION`.

### Task 3: Implement the watchlist reference

**Files:**
- Create: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`

**Interfaces:**
- Consumes: source classifications from Task 2.
- Produces: durable source pool and scan pipeline.

- [ ] **Step 1: Add source-role table**

For each source record: name, role, likely evidence tier, topics, scan surface, use_for, limitations, reverify condition.

- [ ] **Step 2: Add periodic scan contract**

Define candidate capture, original-source backtrace, freshness, dedupe, Base-overlap, adversarial review, disposition and change-authority boundaries.

- [ ] **Step 3: Add six-month bootstrap and future delta rules**

Record the initial 2026-02-10~2026-08-10 window and future scans as delta-from-last-successful-scan with full-rescan triggers for major source policy/version changes.

### Task 4: Integrate without duplicating authority

**Files:**
- Modify: `docs/knowledge/game-development/README.md`
- Modify: `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
- Modify: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: watchlist and recent-review outputs.
- Produces: one-hop discovery and reusable learnings without a second canon.

- [ ] **Step 1: Link the watchlist from the Knowledge Hub**

Add one document-map question for periodic external source scanning and state that the watchlist does not create an execution Skill.

- [ ] **Step 2: Extend Evidence Method**

Add a short `periodic source discovery` subsection that delegates source-pool details to the watchlist and preserves Evidence tier/disposition authority.

- [ ] **Step 3: Extend Reference Catalog**

Add/refresh only source records whose actual Evidence use is supported by the recent review; keep discovery-only feeds outside T1/T2 authority and link to the watchlist for scan role.

- [ ] **Step 4: Extend Planning Evidence Policy**

State that material L1+ research may consult the periodic watchlist for fresh candidates but still requires original-source verification and current-decision relevance.

- [ ] **Step 5: Record change and learning**

Changelog/Learning Log should record the durable principle: recurring source discovery is a feed into existing Evidence governance, not a new authority or automatic trend adoption.

### Task 5: GREEN validation and adversarial review

**Files:**
- Modify only files required by validated findings from review.

**Interfaces:**
- Consumes: exact PR head and CI evidence.
- Produces: verified implementation or explicit blocked state.

- [ ] **Step 1: Run exact-head Evidence Knowledge CI**

Expected: new watchlist test and all existing triggered Evidence Knowledge tests pass.

- [ ] **Step 2: Run broader Base CI triggered by changed governance documents**

Check all Actions associated with exact PR head; do not treat queued/skipped unrelated platform jobs as passes.

- [ ] **Step 3: Adversarial attack**

Attack for discovery-feed authority inflation, article-count theater, six-month recency bias, vendor benchmark overgeneralization, duplicated Reference Catalog authority, hidden new Skill, scheduler overclaim, and unverified "all articles read" wording.

- [ ] **Step 4: Validate critiques and minimally refine**

Fix only verified `MUST_FIX`/scope-safe `SHOULD_FIX` findings, then rerun exact-head CI.

- [ ] **Step 5: Final exact-head comparison**

Confirm `skills/SKILL_REGISTRY.json`, Proposal Registry, release locks/frozen artifacts are unchanged; unresolved review threads are zero; diff contains only approved source-watchlist/evidence-governance scope.
