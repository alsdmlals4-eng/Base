# UI/UX·아트 디자인 규칙 강화 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base의 기존 `auditing-and-refining-ui-art` 책임을 유지하면서 심리학·GUI 관례·접근성·게임 UI·비주얼 디자인 원칙을 증거 강도별로 통합하고, 프로젝트별 예외와 검증을 강제한다.

**Architecture:** 신규 ACTIVE Skill을 만들지 않는다. 기존 owner가 이미 읽는 `references/ux-ui-reference-library.md`에서 `docs/knowledge/game-development/`의 공용 rulebook·완전성 매트릭스를 라우팅하고, `GAME_UX_UI_SYSTEM`이 프로젝트별 적용 강도·예외·검증을 기록하며, `GAME_UX_UI_REVIEW_CHECKLIST`와 전용 회귀 테스트가 오용을 차단한다. 규범 표준·플랫폼 권고·인지/사용성 휴리스틱·시각 스타일 기본값을 분리한다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, Base reference-freshness/UX UI validation workflow.

## Global Constraints

- 사용자 최신 지시와 프로젝트 정본이 외부 레퍼런스보다 높은 권한을 가진다.
- 신규 ACTIVE Skill, Registry identity 변경, 제품 코드·Godot Scene·Theme 변경은 하지 않는다.
- 접근성·상호작용 의미·복구 가능성은 시각 스타일 휴리스틱보다 우선한다.
- 수치는 출처·플랫폼·단위를 보존하고 서로 다른 표준을 하나의 전역 상수로 합치지 않는다.
- 심리학 법칙을 강제 조작·다크 패턴·허위 진행·의도적 지연의 근거로 사용하지 않는다.
- 실제 사용자/실기기 검증을 자동 테스트로 대체하지 않는다.

---

### Task 1: 회귀 계약을 먼저 고정

**Files:**
- Create: `tests/test_ui_ux_visual_design_rules.py`
- Modify: `.github/workflows/validate-game-ux-ui-system.yml`

**Interfaces:**
- Consumes: 기존 `auditing-and-refining-ui-art` reference root와 planning/review templates.
- Produces: rulebook 존재·분류·핵심 접근성/심리/GUI/시각 휴리스틱·다크패턴 방지·프로젝트 적용 계약을 검사하는 테스트.

- [ ] 새 테스트가 아직 존재하지 않는 rulebook을 요구하도록 작성한다.
- [ ] UX/UI workflow의 path filter와 unittest 실행 목록에 새 테스트를 연결한다.
- [ ] 구현 전 HEAD에서 새 테스트의 expected failure가 발생하는지 CI로 확인한다.

### Task 2: 통합 Rulebook 작성

**Files:**
- Create: `docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md`
- Create: `docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md`
- Modify: `skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md`

**Interfaces:**
- Consumes: W3C WCAG 2.2, Apple HIG, Android accessibility guidance, Xbox Accessibility Guidelines, Laws of UX, Anthony Hobday visual rules, Adham Dannaway UI tips, 사용자 제공 GUI 원칙 자료.
- Produces: `MUST / SHOULD / STYLE_DEFAULT / TEST_REQUIRED` 규칙 계층, 사용자 제공 Laws of UX 31개 완전성 매핑, 플랫폼별 수치·예외·검증 계약.

- [ ] 규범 표준과 휴리스틱을 분리한다.
- [ ] 버튼/링크/폼/메뉴/대화상자/알림/아이콘/선택 컨트롤/탭/검색의 의미 문법을 통합한다.
- [ ] Hick/Fitts/Jakob/cognitive load/working memory/Gestalt/flow/goal-gradient/Zeigarnik/Peak-End/Tesler/Postel/Occam/Pareto/Parkinson 등을 적용 조건·오용 방지와 함께 통합한다.
- [ ] 사용자 제공 Laws of UX 31개를 누락 없이 1:1 대조하고 중복 원칙은 명시적으로 정규화한다.
- [ ] 접근성 수치는 Web 24 CSS px, Apple 44×44 pt, Android 48×48 dp처럼 출처 단위를 보존한다.
- [ ] 게임 UI의 controller focus, remapping, subtitles/captions, TV 거리, motion/FOV/camera options를 보강한다.
- [ ] 순수 black/white 회피, 8 기반 scale, 12-column, 16px body, 70자 line length, shadow/brightness/radius 등은 스타일 기본값 또는 웹 한정 휴리스틱으로 낮춘다.
- [ ] Miller 7±2 메뉴 제한, 허위 progress, 근거 없는 deliberate delay, 색상 단독 상태, semantic/focus order를 깨는 visual-weight 정렬을 금지한다.

### Task 3: 프로젝트 적용·검토 surface 강화

**Files:**
- Modify: `templates/planning/GAME_UX_UI_SYSTEM.md`
- Modify: `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md`

**Interfaces:**
- Consumes: 통합 Rulebook의 tier와 platform profile.
- Produces: 프로젝트별 adopted/adapted/rejected/tested rule profile과 리뷰 게이트.

- [ ] `rule_id / tier / platform / project decision / exception reason / verification`을 기록하는 표를 추가한다.
- [ ] 의미 문법·인지 부하·접근성·시각 스타일·행동 심리 윤리 검토를 체크리스트에 추가한다.
- [ ] 스타일 규칙이 접근성·정보 위계·프로젝트 아트 방향을 침범하면 기각하도록 한다.

### Task 4: 적대적 검토와 회귀 확인

**Files:**
- Create: `docs/audits/2026-08-10-ui-ux-art-rules-adversarial-review.md`

**Interfaces:**
- Consumes: 변경 diff, 사용자 자료, 공식/현업 벤치마크.
- Produces: 충돌·왜곡·누락·과잉 규범화와 보정 결과 기록.

- [ ] 사용자 자료의 강점과 그대로 강제하면 위험한 항목을 분리한다.
- [ ] 표준 간 단위/플랫폼 충돌을 공격한다.
- [ ] 게임의 의도적 미스터리·긴장과 일반 앱 UX 휴리스틱의 충돌을 공격한다.
- [ ] 접근성 숫자 준수만으로 실제 사용 가능성을 과장하지 않는지 재검토한다.
- [ ] 최종 diff에서 신규 ACTIVE Skill·Registry identity·제품 코드 변경이 0인지 확인한다.
- [ ] UX/UI 전용 CI와 관련 Base 필수 검사를 exact HEAD 기준으로 확인한다.
