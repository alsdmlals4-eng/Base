# 주기적 전문 Source Radar 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `docs/superpowers/specs/2026-08-13-prompt-planning-writing-source-pack-design.md`

**Goal:** 기존 외부 Source 정책 아래에 프롬프트·기획·글쓰기 작법·작업구조·실행 Source·Godot 자산 전문 Radar를 추가하고, 기존 owner·Evidence ceiling·validation·rollback을 명시한다.

**Architecture:** `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`와 Evidence Method가 계속 권위 owner다. `PERIODIC_SPECIALTY_SOURCE_RADAR.md`는 비실행 discovery extension이며 Hub에서 한 번에 연결한다. 새 ACTIVE Skill, Work Mode, scheduler, Ledger, installer를 만들지 않는다.

**Baseline:** `f08a78b33aa1d458376da8f783553fe9ce7aa9cd`

## Global Constraints

- Existing Solution First와 consolidation-first.
- 프로젝트 정본·실제 코드·데이터·씬·원고·실행 증거가 Base와 외부 자료보다 우선한다.
- Source popularity, framework 이름, vendor score, tool PASS는 authority가 아니다.
- 실행 후보는 source review·sandbox·pin·rollback 전 `QUARANTINED`다.
- 특정 모델·조직·장르·창작자의 조언을 공용 Hard Rule이나 식별 가능한 모사로 승격하지 않는다.
- 열린 PR의 동일 path·owner를 중복 수정하지 않는다.
- 실행하지 않은 검사는 `NOT_RUN`으로 보고한다.

---

### Task 1: 계약을 RED로 고정

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

- [x] **Step 1: 전문 Source artifact와 authority/routing 계약 추가**

요구 사항:

- Watchlist·Evidence Method owner 경계.
- 프롬프트·기획·작법·작업구조·실행 Source·Godot 자산 분야.
- representative eval, player evidence, 단계형 퇴고, 매체 경계.
- `executable_surface`, `trust_state`, upstream·pin·permission·sandbox·rollback.
- 새 ACTIVE Skill·scheduler·Ledger 금지.

- [x] **Step 2: RED 확인**

Evidence Knowledge run `31700962635`에서 기존 79개 계약은 통과하고 전문 Source artifact 부재 계약만 실패했다. 구조 재검토 후 직접-흡수 계약 run `31701862765`에서도 기존 계약은 유지되고 새 두 계약만 실패했다.

### Task 2: 전문 Radar 최소 구현

**Files:**
- Create: `docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md`

- [x] **Step 1: Prompt/Agent Source와 eval·security Gate 작성**
- [x] **Step 2: 게임 기획·플레이어 경험·작업구조 Source 작성**
- [x] **Step 3: 한국어 규범·글쓰기·연재·interactive narrative Source 작성**
- [x] **Step 4: 외부 Skill·addon·script·MCP·binary 실행 위험 축 작성**
- [x] **Step 5: Godot Asset Store·legacy Library·curated list·asset Source 작성**
- [x] **Step 6: cadence·승격·완료 상태·적대적 질문 작성**

### Task 3: Hub one-hop routing

**File:**
- Modify: `docs/knowledge/game-development/README.md`

- [x] 문서 지도에 Radar를 추가한다.
- [x] Radar가 두 번째 Watchlist·Skill·scheduler·Ledger가 아님을 명시한다.
- [x] prompt·game design·fiction·Skill evolution·asset evaluation·validation 기존 Skill 조합으로 라우팅한다.
- [x] Evidence Knowledge 완료 판정에 두 계약 테스트를 연결한다.

### Task 4: GREEN과 회귀 검증

- [x] 로컬 focused contract compile·2-test GREEN.
- [ ] PR exact-head의 `tests/test_periodic_external_source_watchlist.py` 전체 GREEN.
- [ ] PR exact-head의 `tests/test_periodic_external_source_discovery_seeds.py` 전체 GREEN.
- [ ] Evidence Knowledge workflow 전체 GREEN.
- [ ] 실제 실행된 repository checks의 final head conclusion 확인.
- [ ] ACTIVE Skill·Work Mode·Registry 권위 불변 확인.

### Task 5: 적대적 검토와 최소 수정

- [ ] 두 번째 Watchlist·Source canon·Skill 생성 여부.
- [ ] decision relevance 없는 링크 dump·중복 Source·문서 비대화.
- [ ] vendor/model prompt tip·framework·simulation·benchmark 과장.
- [ ] 언어 authority와 창작 품질 혼동, creator style 모사 위험.
- [ ] listing·marketplace·Scorecard·scanner를 vetting/security PASS로 과장.
- [ ] executable candidate quarantine·pin·rollback 우회.
- [ ] project canon·dependency 상태의 Base 승격.
- [ ] 열린 PR path/owner 충돌.

실제 affected consumer·failure mode가 있는 finding만 유지한다. 취향·중복 지적은 기각 사유를 기록한다.

### Task 6: PR·exact-head·병합 Gate

- [ ] current `main`, branch behind/ahead, 열린 PR changed paths를 재확인한다.
- [ ] 최종 head의 모든 적용 workflow conclusion과 unresolved review thread를 확인한다.
- [ ] main 이동 시 동기화 후 exact-head 검증을 다시 실행한다.
- [ ] repository 정책이 허용하면 squash merge한다.
- [ ] merge SHA와 새 `main`에서 Radar·Hub·tests를 readback한다.

## Expected Files

```text
docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md
docs/knowledge/game-development/README.md
docs/superpowers/specs/2026-08-13-prompt-planning-writing-source-pack-design.md
docs/superpowers/plans/2026-08-13-prompt-planning-writing-source-pack.md
tests/test_periodic_external_source_watchlist.py
tests/test_periodic_external_source_discovery_seeds.py
```

## Rollback

이 PR의 squash merge commit을 revert한다. Radar, Hub route, tests, spec, plan이 함께 되돌아가며 runtime·save/data Schema·Skill Registry·project canon migration은 없다.
