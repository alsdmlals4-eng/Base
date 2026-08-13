# 프롬프트·기획·글쓰기 작법 Source Pack 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `docs/superpowers/specs/2026-08-13-prompt-planning-writing-source-pack-design.md`

**Goal:** 기존 외부 Source Watchlist 아래에 프롬프트·기획·글쓰기 작법의 조사 대상, 권위 한계, 기존 owner 라우팅과 검증 Gate를 제공한다.

**Architecture:** 새 ACTIVE Skill이나 두 번째 Watchlist를 만들지 않는다. `PROMPT_PLANNING_WRITING_SOURCE_PACK.md`는 기존 Watchlist와 Evidence Method에 종속된 Reference이며, Hub에서 한 번에 발견하고 기존 prompt·game-design·fiction owner로 결과를 전달한다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions.

## Global Constraints

- 기준 `main`: `f08a78b33aa1d458376da8f783553fe9ce7aa9cd`.
- 기존 Source role, `ORIGINAL_SOURCE_BACKTRACE`, Existing Solution First와 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY` 판정을 재사용한다.
- 새 ACTIVE Skill, Work Mode, scheduler, 독립 ledger, 자동 설치기를 만들지 않는다.
- 외부 Source는 정본·실제 프로젝트 파일·실행 증거를 대체하지 않는다.
- 특정 모델·조직·장르·작가의 방법을 공용 Hard Rule이나 식별 가능한 모사로 승격하지 않는다.
- PR #322와 #312의 소유 경로를 수정하지 않는다.
- 실행하지 않은 검사는 `NOT_RUN`으로 보고한다.

---

### Task 1: Source Pack 계약을 RED로 고정

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`

**Interfaces:**
- Consumes: 기존 Watchlist·Hub·Evidence Knowledge workflow.
- Produces: Source Pack 존재, owner 경계, 세 domain·consumer·Guardrail을 검증하는 계약.

- [ ] **Step 1: 실패 계약을 추가한다**

`SOURCE_PACK` 경로와 다음 검사를 추가한다.

- Pack과 Hub one-hop route 존재.
- `owner_policy`, `evidence_owner`, `scheduler_authority: EXTERNAL_TO_BASE`.
- `PROMPT_AND_AGENT_WORKFLOW`, `PLANNING_AND_DESIGN_METHODS`, `WRITING_AND_REVISION_CRAFT`.
- 프롬프트의 exact product/model/surface, placement, Golden Set, actual harness eval, 외부 실행 후보 격리.
- 기획의 player/user problem, decision delta, consumer, validation artifact, rollback.
- 글쓰기의 단계형 퇴고, 한국어 규범 권위 한계, 선형/인터랙티브 경계, style imitation 금지.
- 새 ACTIVE Skill·독립 scheduler·독립 ledger 금지.

- [ ] **Step 2: RED를 관찰한다**

Run: `python -m unittest tests/test_periodic_external_source_watchlist.py -v`

Expected: 새 Source Pack 파일과 Hub route가 없어서 새 계약만 FAIL한다. 기존 계약 실패는 blocker로 분리한다.

### Task 2: 최소 Source Pack과 Hub route 구현

**Files:**
- Create: `docs/knowledge/game-development/PROMPT_PLANNING_WRITING_SOURCE_PACK.md`
- Modify: `docs/knowledge/game-development/README.md`

**Interfaces:**
- Consumes: Watchlist 정책, Evidence Method, 기존 prompt·game-design·fiction owner.
- Produces: 세 분야 Source pool, 적용 Gate, candidate packet, cadence, 기존 owner 라우팅.

- [ ] **Step 1: Pack을 생성한다**

세 분야에 대해 Source 역할, scan surface, 사용 목적, 적용 한계와 기존 consumer를 기록한다. 외부 Skill·script·hook·MCP·binary 후보에는 upstream, pin, license, external access, permission, sandbox, rollback 필드를 요구한다.

- [ ] **Step 2: Hub one-hop route를 추가한다**

문서 지도에 Pack을 추가하고 프롬프트·기획·글쓰기 작법 결과가 각각 기존 owner로 가도록 라우팅한다. Pack이 실행 Skill·Evidence owner·scheduler가 아님을 명시한다.

- [ ] **Step 3: GREEN을 확인한다**

Run: `python -m unittest tests/test_periodic_external_source_watchlist.py -v`

Expected: PASS.

### Task 3: 회귀·구조 검증

**Files:**
- Verify: `tests/test_periodic_external_source_watchlist.py`
- Verify: `.github/workflows/validate-evidence-knowledge.yml`

- [ ] **Step 1: 정적 검사를 실행한다**

Run: `python -m py_compile tests/test_periodic_external_source_watchlist.py`

Expected: exit 0.

- [ ] **Step 2: Evidence Knowledge 계약을 실행한다**

Run: `.github/workflows/validate-evidence-knowledge.yml`의 현행 compile·unittest 명령.

Expected: 관련 계약 전체 PASS. 환경 의존 skip은 실행 로그와 함께 분리한다.

- [ ] **Step 3: diff·경로·권위 회귀를 확인한다**

- Watchlist·Evidence Method가 owner인지 확인.
- ACTIVE Skill·Registry·Work Mode가 변하지 않았는지 확인.
- 열린 PR #322·#312와 exact changed-path 교집합을 확인.
- Source Pack이 두 번째 Watchlist·독립 일정 owner가 아닌지 확인.

### Task 4: 적대적 검토·병합 Gate

- [ ] **Step 1: 전체 PR diff를 공격한다**

검토 대상: 기존 owner 중복, 모델·조직·장르 과잉 일반화, 문법 권위와 창작 품질 혼동, 선형/연재/인터랙티브 경계 손실, 특정 창작자 모사, 인기·판매량의 권위 세탁, consumer·검증·rollback 없는 Source, 문서 수 증가 자체를 개선으로 보는 오류.

- [ ] **Step 2: 비판을 검증하고 최소 수정한다**

실제 affected consumer·test·권위 충돌이 있는 finding만 유지한다. 취향·중복 지적은 기각 사유를 기록한다.

- [ ] **Step 3: exact-head 검증과 리뷰 상태를 확인한다**

- 최종 head SHA의 적용 workflow conclusion.
- unresolved review thread 0.
- current `main`과 strict up-to-date·path overlap 재검사.
- 새 commit이 생기면 검증을 다시 실행.

- [ ] **Step 4: 병합 후 readback한다**

승인된 squash 경로로 merge하고 merge SHA를 기록한다. 새 `main`에서 Pack, Hub route, test를 exact-ref로 재조회하며 push workflow가 실제 실행된 경우 conclusion을 확인한다.

## Rollback

이 PR의 squash merge commit 하나를 revert한다. Pack, Hub route, test, spec, plan이 함께 되돌아가며 데이터·Schema·runtime migration은 없다.
