# 주기적 Source Radar — 프롬프트·기획·작법 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `docs/superpowers/specs/2026-08-13-prompt-planning-writing-source-pack-design.md`

**Goal:** 기존 주기적 외부 Source 시스템에 프롬프트·게임 기획·글쓰기 작법·작업구조·실행 Source·Godot 자산 조사 경로를 추가하고, 권위·실행 위험·기존 owner·검증·rollback을 명시한다.

**Architecture:** Watchlist가 Source·Evidence·scan 정책 owner를 유지한다. Discovery Seeds에 상세 후보군을 추가하고 Watchlist에 실행 위험 필드를 흡수한다. 새 Skill, Registry entry, Work Mode, scheduler, ledger row 또는 별도 Source canon은 만들지 않는다.

**Baseline:** `f08a78b33aa1d458376da8f783553fe9ce7aa9cd`

## Global Constraints

- Existing Solution First와 consolidation-first.
- 프로젝트 canon·실제 구현·실행 증거가 Base와 외부 자료보다 우선한다.
- Source popularity, framework 이름, vendor score와 tool PASS는 authority가 아니다.
- 실행 후보는 source review·sandbox·pin·rollback 전 `QUARANTINED`다.
- 새 commit은 이전 exact-head 검증을 무효화한다.
- 열린 PR #322·#312 소유 경로를 수정하지 않는다.
- 실행하지 않은 검사는 `NOT_RUN`으로 보고한다.

---

### Task 1: 직접 흡수 계약을 RED로 고정

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

- [ ] **Step 1: Watchlist 계약 추가**

프롬프트 평가·게임 기획·작법 lens, Godot Asset Store·legacy Library, 공급망 Source, `executable_surface`, `trust_state`, source/pin/permission/sandbox/rollback 필드를 요구한다.

- [ ] **Step 2: Discovery Seed 계약 추가**

다음 six group과 기존 consumer 라우팅을 요구한다.

```text
Prompt engineering / evaluation / security
Game design / planning research and system modeling
Writing craft / Korean prose / story industry
Work structure / documentation / decision methods
Skill / addon / executable source discovery and quarantine
Godot Asset Store / reusable production assets
```

- [ ] **Step 3: RED 확인**

```bash
python -m unittest \
  tests.test_periodic_external_source_watchlist.PeriodicExternalSourceWatchlistTests.test_prompt_planning_writing_and_executable_source_lenses_preserve_evidence_boundaries \
  tests.test_periodic_external_source_discovery_seeds.PeriodicExternalSourceDiscoverySeedTests.test_prompt_planning_writing_work_structure_executable_and_asset_sources_route_to_existing_owners \
  -v
```

Expected: baseline에 새 fields·headings·Source route가 없어 두 계약이 FAIL한다. 기존 test failure는 별도 blocker로 분리한다.

### Task 2: Watchlist 정책 최소 보강

**File:** `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`

- [ ] 게임 기획·프롬프트 평가·글쓰기 작법의 우선 질문과 claim ceiling을 기존 domain 안에 흡수한다.
- [ ] Godot Asset Store를 현재 discovery surface로, Asset Library를 legacy discovery로 구분한다.
- [ ] OpenSSF Scorecard, OSV/OSV-Scanner, deps.dev, SLSA의 제한된 역할을 기록한다.
- [ ] Candidate capture와 `SOURCE_CONTEXT_PACKET`에 execution-risk fields를 추가한다.
- [ ] unknown 실행 행동은 quarantine, listing·score·scan PASS는 vetting/security PASS가 아니라는 Gate를 추가한다.

### Task 3: Discovery Seed group 추가

**File:** `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

- [ ] Prompt: 공식 vendor guidance 재사용 + DSPy, promptfoo, OWASP GenAI, DAIR.AI.
- [ ] Game planning: DiGRA, Game Studies, MDA, Game Design Patterns, Game Design Workshop, Machinations.
- [ ] Writing: 국립국어원, KOCCA/Storyum, Writing Excuses, Brandon Sanderson BYU, Jane Friedman, Writer's Digest, Writer Beware.
- [ ] Work structure: Diátaxis, ADR, C4, DORA.
- [ ] Executable Source: Agent Skills specification, `anthropics/skills`, `obra/superpowers`, skills.sh, OpenSSF, OSV, deps.dev, SLSA.
- [ ] Godot assets: Asset Store, legacy Library, awesome-godot, GDQuest, Kenney, Poly Haven, Freesound, OpenGameArt, Godot Shaders.
- [ ] 각 group에 existing consumer, scan route, claim ceiling, project-only destination을 기록한다.
- [ ] 신규 Source는 `ACTIVE_DISCOVERY_SEED`로 두고 Ledger history/counter를 만들지 않는다.

### Task 4: GREEN과 회귀 검증

- [ ] Focused compile과 two-test GREEN.
- [ ] `tests/test_periodic_external_source_watchlist.py` 전체.
- [ ] `tests/test_periodic_external_source_discovery_seeds.py` 전체.
- [ ] Evidence Knowledge workflow의 현행 compile·unittest 전체.
- [ ] Base v9와 Game Project Operating System workflow 중 실제 실행된 check를 exact head에서 확인한다.
- [ ] ACTIVE Skill 30개와 `PLAN / BUILD / REVIEW`가 유지되는지 확인한다.

### Task 5: 적대적 검토와 최소 수정

전체 diff에서 다음을 공격한다.

- 새 Skill·owner·Source canon 중복.
- decision relevance 없는 link dump와 문서 비대화.
- vendor/model prompt tip의 전역 규칙화.
- framework·simulation의 player evidence 위장.
- 작가 popularity·예시를 voice/style 복제 근거로 사용.
- listing·marketplace를 vetted dependency로 사용.
- Scorecard·vulnerability scan을 complete security PASS로 과장.
- executable candidate의 quarantine 우회.
- Godot Asset Store beta/successor·license·compatibility의 stale claim.
- Ledger history·contribution의 추정 작성.
- PR #322·#312와 path/owner overlap.

실제 affected consumer·failure mode가 있는 지적만 유지한다. 취향·중복 지적은 기각 사유를 기록하고 변경하지 않는다.

### Task 6: PR·exact-head·병합 Gate

- [ ] current `main`, PR #322·#312 changed paths, branch behind/ahead를 재확인한다.
- [ ] 최종 head의 모든 적용 workflow conclusion을 확인한다.
- [ ] unresolved review thread 0과 독립 review를 확인한다.
- [ ] main 이동 시 동기화 후 exact-head 검증을 다시 실행한다.
- [ ] repository 정책이 허용하면 squash merge한다.
- [ ] merge SHA와 새 `main`에서 Watchlist·Seeds·tests를 readback한다.

## Expected Files

```text
docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md
docs/superpowers/specs/2026-08-13-prompt-planning-writing-source-pack-design.md
docs/superpowers/plans/2026-08-13-prompt-planning-writing-source-pack.md
tests/test_periodic_external_source_watchlist.py
tests/test_periodic_external_source_discovery_seeds.py
```

## Rollback

이 PR의 squash merge commit을 revert한다. Watchlist fields, Discovery Seed groups, tests, spec, plan이 함께 되돌아가며 runtime·data Schema·Skill Registry·project canon migration은 없다.
