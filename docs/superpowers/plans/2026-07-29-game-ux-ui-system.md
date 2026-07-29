# 게임 UX/UI 공용 체계 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 UI 아트 감사 스킬을 호환성 있게 확장하여 UX 설계·패턴·접근성·Godot 구현 계약·플레이테스트·런타임 감사를 연결하고, 다섯 게임 프로젝트가 공용 체계를 프로젝트 전용으로 적용하게 한다.

**Architecture:** Base는 공용 Skill·reference·template·test의 단일 원본을 유지한다. 프로젝트는 공용 Skill 본문을 복제하지 않고 기존 UX 전문 Skill 또는 책임 원본에서 Base Skill ID와 프로젝트 고유 패턴·검증만 어댑트한다. 제품 코드·Scene·데이터는 이번 작업에서 변경하지 않는다.

**Tech Stack:** Markdown, YAML, JSON, Python unittest, GitHub branches/PRs/Actions, Godot 4 UI 계약 문서.

## Global Constraints

- 대상: Base, Blacksmith, GRIMOIRE-, omenward, Ten-Paces-Hidden-Moves, urban-legend.
- 제외: MylittleBoat, ninja-survival-godot, Coc-Fiction, Unity archive.
- HTML 기획 대시보드는 생성·복구·기본 적용하지 않는다.
- 기존 Skill ID `auditing-and-refining-ui-art`를 유지한다.
- 기존 A~E UI 아트 감사와 스캐너 동작을 보존한다.
- 프로젝트 코어·수치·코드·Scene·게임 데이터는 변경하지 않는다.
- 외부 레퍼런스는 요구사항이나 구현 사실의 정본이 아니다.
- 실행하지 않은 런타임·실기기·보조기기·사람 플레이 검증은 `NOT_RUN` 또는 `UNVERIFIED`다.
- 각 저장소는 branch → PR → 검증 → main 병합 → post-merge 재검토 순서로 처리한다.

---

## File Structure

### Base

- Modify: `skills/auditing-and-refining-ui-art/SKILL.md` — UX 설계와 UI 감사를 분리한 통합 Skill Mode.
- Modify: `skills/auditing-and-refining-ui-art/agents/openai.yaml` — 새 역할과 기본 프롬프트.
- Create: `skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md` — 설계 순서·산출물·게이트.
- Create: `skills/auditing-and-refining-ui-art/references/game-ux-pattern-library.md` — 반복 패턴 카드.
- Create: `skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md` — 공식 출처와 채택 판정.
- Create: `skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md` — Godot 상태·Theme·Control·Container·Signal 계약.
- Create: `skills/auditing-and-refining-ui-art/references/project-adapter-contract.md` — 프로젝트별 최소 적용 방식.
- Create: `templates/planning/GAME_UX_UI_SYSTEM.md` — 프로젝트 책임 원본 템플릿.
- Create: `templates/research/UX_UI_REFERENCE_CARD.md` — 레퍼런스 평가 카드.
- Create: `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md` — 설계·접근성·런타임·사람 검증 체크.
- Create: `tests/test_game_ux_ui_system.py` — 파일·모드·경계·참조·기존 감사 보존 계약.
- Create: `docs/audits/2026-07-29-game-ux-ui-system-adversarial-review.md` — 공격·비판 검증·수정·회귀 결과.

### Projects

- Blacksmith: 프로젝트 UX/UI 책임 원본과 Base adapter 갱신.
- GRIMOIRE-: 마법 작성 UX/UI 책임 원본과 Base adapter 갱신.
- omenward: 기존 `03-ux-ui-accessibility` Skill을 공용 체계의 프로젝트 어댑터로 확장.
- Ten-Paces-Hidden-Moves: 기존 전투 UX Skill과 UI 명세를 공용 패턴에 연결.
- urban-legend: 기존 프로젝트 UX Skill과 Godot UI 구조 문서를 공용 패턴에 연결.

---

### Task 1: RED 계약 테스트

**Files:**
- Create: `tests/test_game_ux_ui_system.py`

**Interfaces:**
- Consumes: 설계 문서의 파일 목록·Skill Mode·경계.
- Produces: 공용 UX/UI 체계가 없거나 불완전할 때 실패하는 구조 계약.

- [ ] **Step 1: 공용 파일과 Skill Mode를 요구하는 테스트 작성**
- [ ] **Step 2: 현재 branch에서 테스트 실행 또는 PR CI 실행**
- [ ] **Step 3: 새 파일이 없어 실패하는지 확인**
- [ ] **Step 4: 실패가 import나 문법 오류가 아니라 누락 계약 때문인지 확인**
- [ ] **Step 5: 테스트 전용 커밋 기록**

### Task 2: Base Skill 확장

**Files:**
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Modify: `skills/auditing-and-refining-ui-art/agents/openai.yaml`

**Interfaces:**
- Consumes: 기존 A~E 감사 계약과 스캐너.
- Produces: `experience-contract`, `flow-and-information-architecture`, `pattern-selection`, `design-system-contract`, `godot-ui-contract`, `accessibility-gate`, `playtest-contract`, `runtime-ui-audit`, `refine-approved-findings`, `reaudit`.

- [ ] **Step 1: 기존 감사 책임·명령·Findings schema를 보존**
- [ ] **Step 2: UX 설계 모드와 감사 모드의 입력·출력·사용/비사용 조건 작성**
- [ ] **Step 3: 도메인 계산·최종 아트·사람 검증과의 경계 작성**
- [ ] **Step 4: 에이전트 표시명과 기본 프롬프트 갱신**
- [ ] **Step 5: 기존 scanner 테스트와 새 구조 테스트 실행**

### Task 3: Reference와 Template

**Files:**
- Create: `skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md`
- Create: `skills/auditing-and-refining-ui-art/references/game-ux-pattern-library.md`
- Create: `skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md`
- Create: `skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md`
- Create: `skills/auditing-and-refining-ui-art/references/project-adapter-contract.md`
- Create: `templates/planning/GAME_UX_UI_SYSTEM.md`
- Create: `templates/research/UX_UI_REFERENCE_CARD.md`
- Create: `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md`

**Interfaces:**
- Consumes: 공용 Skill Mode.
- Produces: 프로젝트가 선택적으로 읽고 적용할 방법·패턴·공식 참고·템플릿.

- [ ] **Step 1: UX 설계 순서와 삭제·축소 우선 원칙 작성**
- [ ] **Step 2: 최소 12개 패턴을 문제·상태·폴백·실패·검증 단위로 작성**
- [ ] **Step 3: 공식 출처·확인일·채택 판정·복제 금지 작성**
- [ ] **Step 4: Godot Theme·Control·Container·Signal·focus 계약 작성**
- [ ] **Step 5: 프로젝트 어댑터와 책임 원본·연구·검토 템플릿 작성**
- [ ] **Step 6: 새 테스트가 통과하는지 확인**

### Task 4: Base 적대적 검토와 병합

**Files:**
- Create: `docs/audits/2026-07-29-game-ux-ui-system-adversarial-review.md`

**Interfaces:**
- Consumes: Base PR 실제 diff·테스트·기존 소비자.
- Produces: `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED` 판정과 회귀 결과.

- [ ] **Step 1: skill 중복·라우팅 과대·기존 감사 회귀를 공격**
- [ ] **Step 2: 공식 레퍼런스의 웹/모바일 편향과 수치 오용을 공격**
- [ ] **Step 3: 프로젝트 어댑터가 공용 본문을 복제하도록 유도하는지 공격**
- [ ] **Step 4: 비판의 사실성·영향·범위·수정 비용 재검증**
- [ ] **Step 5: 검증된 MUST_FIX와 범위 내 SHOULD_FIX만 수정**
- [ ] **Step 6: 새 PR HEAD에서 테스트·diff·참조 회귀 확인**
- [ ] **Step 7: Base PR을 main에 병합하고 새 main HEAD 재조회**

### Task 5: Blacksmith 적용

**Files:**
- Create: `[기획서]/04_시스템/BLACKSMITH_UX_UI_SYSTEM.md`
- Modify: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: 병합된 Base UX/UI Skill과 프로젝트 AGENTS.
- Produces: 세로형 Android·터치·안전 영역·강화 위험/보상 비교의 프로젝트 UX 계약.

- [ ] **Step 1: 기존 UI·접근성·강화 문서와 중복 여부 확인**
- [ ] **Step 2: 모바일 핵심 패턴과 Godot 구현 경계 작성**
- [ ] **Step 3: Base adapter commit·override 갱신**
- [ ] **Step 4: Documentation Map에 책임 원본 연결**
- [ ] **Step 5: JSON·문서·보호 경로 diff 검증**
- [ ] **Step 6: PR 검토·병합·post-merge 재검토**

### Task 6: GRIMOIRE- 적용

**Files:**
- Create: `docs/planning/GAME_UX_UI_SYSTEM.md`
- Modify: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Modify: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: 병합된 Base UX/UI Skill과 확정된 마법 작성·시각 표현·점진 공개 문서.
- Produces: 직접 작성·인식·주문 설계 실패 분리, 모바일 입력, 학습 단계의 프로젝트 UX 계약.

- [ ] **Step 1: 승인된 마법 작성·Gate 문서와 충돌 여부 확인**
- [ ] **Step 2: 프로젝트 UX 책임 원본 작성**
- [ ] **Step 3: Base adapter·공용 route·Documentation Map 갱신**
- [ ] **Step 4: 제품 구현 금지·사람 검증 NOT_RUN 보존**
- [ ] **Step 5: PR 검토·병합·post-merge 재검토**

### Task 7: omenward 적용

**Files:**
- Modify: `skills/disciplines/03-ux-ui-accessibility/SKILL.md`
- Create: `docs/design/APPROVED_UX_UI_SYSTEM.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Base 공용 방법, 기존 core UX playtest Skill과 실제 HUD 계약.
- Produces: 위협→릴→배치→전투→다음 설계 인과를 설명하는 프로젝트 UX 계약.

- [ ] **Step 1: 기존 UX Skill과 플레이테스트 Skill의 중복 경계 분리**
- [ ] **Step 2: 설계 Skill을 Base 어댑터로 확장**
- [ ] **Step 3: 프로젝트 UX 책임 원본과 문서 맵 연결**
- [ ] **Step 4: 도메인 계산과 기존 V2 코어 불변 보존 확인**
- [ ] **Step 5: PR 검토·병합·post-merge 재검토**

### Task 8: Ten-Paces-Hidden-Moves 적용

**Files:**
- Modify: `skills/ux-ui-accessibility/combat-ux-and-accessibility/SKILL.md`
- Modify: `docs/07_COMBAT_UI_SPEC.md`

**Interfaces:**
- Consumes: Base 공용 방법과 전투 UI 책임 원본.
- Produces: 적 의도 단서·3/3/4 계획·거리·합·중단·복기의 프로젝트 패턴 프로필.

- [ ] **Step 1: 기존 강한 전투 UX 계약을 보존**
- [ ] **Step 2: Base 패턴 ID·레퍼런스 판정·검증 매트릭스 연결**
- [ ] **Step 3: 제품 경로 무변경 확인**
- [ ] **Step 4: PR 검토·병합·post-merge 재검토**

### Task 9: urban-legend 적용

**Files:**
- Modify: `skills/disciplines/urban-legend-ux-ui-accessibility/SKILL.md`
- Modify: `docs/GODOT_NATIVE_UI_ARCHITECTURE.md`
- Create: `docs/planning/UX_UI_SYSTEM.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Base 공용 방법, 조사·가설·회수 UI 원본과 기존 Godot UI 구조.
- Produces: 정보 신뢰도·가설·규칙 검증·회수·장기 기억 보조의 프로젝트 UX 계약.

- [ ] **Step 1: 기존 UI 구조와 프로젝트 Skill을 공용 방법에 연결**
- [ ] **Step 2: 조사형 UX 패턴 프로필과 상태 소유 경계 작성**
- [ ] **Step 3: Base 승격 후보를 완료된 공용 원칙으로 갱신**
- [ ] **Step 4: 문서 맵·skill route·보호 경로 검증**
- [ ] **Step 5: PR 검토·병합·post-merge 재검토**

### Task 10: 전체 회귀·실행 보고

**Files:**
- No new product files.

**Interfaces:**
- Consumes: 여섯 저장소의 merged main HEAD.
- Produces: Base 공용 승격과 프로젝트 전용 유지 항목, 검증·미검증, PR·commit·잔여 위험 보고.

- [ ] **Step 1: 각 main에서 Base commit·Skill ID·책임 원본 링크 재조회**
- [ ] **Step 2: 제외 저장소가 변경되지 않았는지 확인**
- [ ] **Step 3: 제품 코드·Scene·데이터 변경 0건 확인**
- [ ] **Step 4: 자동·정적·CI와 런타임·사람 검증을 분리해 보고**
- [ ] **Step 5: 실제 사용한 Work Mode·Skill·Mode·이유·결과·미검증 기록**

## Plan Self-Review

- 설계 문서의 모든 포함 범위는 Task 1~4에 구현·검증 단계가 있다.
- 다섯 대상 프로젝트는 Task 5~9에서 각각 독립적으로 반영·검증·병합한다.
- 제외 저장소와 제품 경로 보호가 Global Constraints와 Task 10에 명시돼 있다.
- 새 광역 Skill ID를 만들지 않아 기존 Registry의 한 줄 JSON을 불필요하게 변경하지 않는다.
- 런타임·실기기·사람 검증을 문서 정합성으로 대체하지 않는다.
- `TBD`, `TODO`, 구현 범위를 알 수 없는 placeholder는 없다.
