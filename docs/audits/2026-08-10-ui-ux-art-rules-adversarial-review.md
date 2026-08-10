# 2026-08-10 UI/UX·아트 디자인 규칙 적대적 검토

## 범위

- Base latest main 재대조: `0a7c4a4286b1107b1bfa03dc4b4e4ce88fbbd5b8`
- owner: `skills/auditing-and-refining-ui-art`
- 기존 구조: UX/UI 설계 → pattern selection → design system → accessibility → polishing → runtime audit → human evidence
- 신규 ACTIVE Skill: 금지
- 제품 코드/Godot Scene/Theme 변경: 금지

## 입력 근거

### 사용자 제공

- Laws of UX 31개 원칙 요약
- Anthony Hobday visual design safe rules 요약
- Adham Dannaway UI tips 요약
- GUI 기본 요소(버튼·폼·메뉴·링크·대화상자·알림·아이콘·선택 컨트롤·탭·검색)와 창/스크롤·포인터 지침 요약

### 외부 원문 재검증

- W3C WCAG 2.2 / Target Size Minimum
- Apple HIG Accessibility / UI Design Tips
- Android Developers Accessibility
- Xbox Accessibility Guidelines 101/102/104/107/113/114/117
- Laws of UX 원문
- Anthony Hobday `Visual design rules you can safely follow every time`
- Adham Dannaway `16 little UI design tips that make a big impact`

## 기존 Base와의 중복 판정

`auditing-and-refining-ui-art`는 이미 다음을 소유한다.

- 화면 중심 질문·첫 시선·정보 계층
- 상태와 다중 피드백 채널
- input/focus/복귀
- 접근성 gate
- Godot 상태 소유 경계
- P0 BLOCKER → P3 DELIGHT 폴리싱
- 실제 렌더/입력/사람 이해 증거

따라서 별도 `laws-of-ux`, `visual-design-rules`, `ui-best-practices` ACTIVE Skill을 추가하면 owner 중복·라우팅 분산·규칙 충돌이 생긴다. 결론은 `ABSORB`다. 기존 owner가 이미 직접 연결하는 `references/ux-ui-reference-library.md`가 공용 knowledge 문서를 라우팅하고, template/checklist/test/workflow가 실행 계약을 검증한다.

---

## 적대적 Finding

### AR-01 — Target size 숫자 충돌

**공격:** 사용자 자료의 `1×1cm`, WCAG `24×24 CSS px`, Apple `44×44 pt`, Android `48×48 dp`를 하나의 최소 버튼 크기로 합치면 플랫폼·단위·입력 차이가 사라진다.

**판정:** `MUST_FIX`

**보정:**
- Web WCAG floor는 `24×24 CSS px` 또는 성공 기준 예외를 보존.
- Apple touch는 `44×44 pt`, Android touch는 `48×48 dp`를 각각 플랫폼 권고로 보존.
- 게임은 TV 거리·controller focus·실제 기기 입력을 추가 검증.
- 전역 `min_button_px` 상수로 병합 금지.

### AR-02 — Contrast 숫자의 적용 범위 왜곡

**공격:** `UI 3:1`, `small text 4.5:1`을 모든 게임 화면에 같은 방식으로 적용하면 움직이는 배경, couch distance, HUD, subtitle 문제가 빠진다.

**판정:** `MUST_FIX`

**보정:**
- Web WCAG text/non-text 성공 기준과 Xbox 게임 contrast 지침을 분리.
- 숫자는 baseline이며 gameplay 배경에서 outline/background/high-contrast option을 실제로 확인.

### AR-03 — “순수 black/white 금지”의 접근성 역전

**공격:** near-black/near-white를 강제하면 필요한 high contrast를 오히려 낮출 수 있다.

**판정:** `MUST_FIX`

**보정:** `STYLE_DEFAULT`로만 유지하고 contrast/accessibility가 우선.

### AR-04 — 12-column·16px·70자·8배수의 전역 법칙화

**공격:** 웹 기반의 유용한 default를 HUD·TV·radial menu·mobile·split-screen·게임패드 UI에 강제하면 레이아웃과 정보 밀도가 왜곡된다.

**판정:** `MUST_FIX`

**보정:** 모두 `STYLE_DEFAULT` 또는 context-bound heuristic으로 내림. 단위·거리·locale·장르별 검증 요구.

### AR-05 — Shadow/brightness/radius 경험칙의 가짜 과학화

**공격:** `blur=distance×2`, dark/light container brightness 12%/7%, nested radius subtraction을 물리 법칙처럼 자동 적용하면 실제 elevation·contrast·아트 방향과 충돌한다.

**판정:** `MUST_FIX`

**보정:** 시각 starting point로만 허용하고 실제 렌더와 아트 direction으로 판단.

### AR-06 — visual weight ordering vs semantic/focus order

**공격:** “가장 무거운 요소를 바깥쪽/먼저” 규칙이 reading order나 keyboard/controller focus order를 바꾸면 접근성이 깨진다.

**판정:** `MUST_FIX`

**보정:** semantic reading/action sequence와 focus order가 시각 composition보다 우선.

### AR-07 — Miller 7±2 오용

**공격:** 작업 기억 연구를 메뉴 항목 수 5~9개 제한으로 변환하면 명확한 메뉴가 불필요하게 중첩되고 숨겨질 수 있다.

**판정:** `MUST_FIX`

**보정:** 7±2를 하드 캡으로 금지. recognition over recall, grouping, clear labels, search/filter를 우선.

### AR-08 — Goal-Gradient/Zeigarnik의 retention dark pattern화

**공격:** 미완료 효과와 목표 접근 동기를 badge pressure, streak anxiety, false progress에 사용하면 UX 원칙이 조작 기술로 변한다.

**판정:** `MUST_FIX`

**보정:** 실제 progress와 재개 위치의 명료성만 지원. 허위 진행·강박적 pressure 금지.

### AR-09 — Peak-End로 지속 불편을 덮는 문제

**공격:** 강한 보상 연출과 좋은 ending이 중간의 반복 마찰·읽기 어려움·입력 지연을 정당화할 수 있다.

**판정:** `MUST_FIX`

**보정:** peak/end는 P3 delight이며 P0~P2 usability/accessibility debt를 가릴 수 없다.

### AR-10 — “의도적 지연이 신뢰를 높인다”의 일반화

**공격:** 실제로 빠른 처리를 일부러 늦추면 사용자의 시간을 소비하고 시스템 상태를 기만할 수 있다.

**판정:** `MUST_FIX`

**보정:** 근거 없는 deliberate delay 금지. safety/comprehension/network stability/pacing 같은 명시 목적과 테스트가 있을 때만 허용.

### AR-11 — Postel 원칙의 보안/도메인 침범

**공격:** 모든 사용자 입력을 관대하게 받는다는 원칙이 schema, 결제, 저장 포맷, 보안 경계를 약화시킬 수 있다.

**판정:** `MUST_FIX`

**보정:** 표현 형식·공백·하이픈·동의어 등 사용자 친화 변형만 유연하게 처리하고 authoritative validation은 유지.

### AR-12 — 일반 앱 UX가 게임의 의도적 불확실성을 제거

**공격:** Hick/Occam/Tesler/최소주의를 과잉 적용하면 미스터리·탐색·전략적 선택이라는 게임 코어를 삭제할 수 있다.

**판정:** `MUST_FIX`

**보정:** 장르 complexity는 보호하고 extraneous cognitive load만 줄인다. 조작 가능성·포커스·취소·필수 feedback은 명확하게 유지.

### AR-13 — Aesthetic-Usability 효과의 역설

**공격:** polish가 좋아질수록 실제 usability 문제가 사용자 테스트에서 덜 드러날 수 있다.

**판정:** `SHOULD_FIX`

**보정:** perceived quality와 task success/error/recovery evidence를 분리한다.

### AR-14 — 가독성 규칙의 라틴 문자 편향

**공격:** left-align, x-height, uppercase, 70-char line length를 언어 일반 규칙으로 쓰면 한글·CJK·RTL locale에 맞지 않는다.

**판정:** `MUST_FIX`

**보정:** reading edge, script/font metrics, 긴 한국어, locale별 실제 렌더를 기준으로 변환.

### AR-15 — 접근성 체크리스트 통과 = 접근 가능 오판

**공격:** contrast 수치, target size, focus indicator가 모두 있어도 실제 controller navigation·TV 거리·assistive technology에서 막힐 수 있다.

**판정:** `MUST_FIX`

**보정:** 기존 Base의 `HUMAN_NOT_RUN`, runtime evidence, accessibility user validation 분리를 유지한다.

### AR-16 — 새 reference를 Skill package 내부에 고아로 추가

**공격:** 최초 구현에서 새 Rulebook·완전성 매트릭스를 `skills/auditing-and-refining-ui-art/references/`에 추가하고 `ux-ui-reference-library.md`에서만 연결했다. Base package integrity 계약은 `references/`의 모든 packaged source를 owner `SKILL.md`에서 직접 발견 가능하게 요구하므로 광역 governance CI가 실패했다.

**판정:** `MUST_FIX`

**보정:**
- 신규 ACTIVE Skill을 만들지 않는다.
- `SKILL.md`를 변경해 특수 `game-ux-ui-skill-sync`의 Registry/README/learning-log 등 대규모 coupling을 불필요하게 유발하지 않는다.
- 새 규칙 문서는 공용 knowledge인 `docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md`와 `UX_LAWS_COMPLETENESS_MATRIX.md`로 이동한다.
- owner가 이미 직접 연결하는 `references/ux-ui-reference-library.md`에서 두 공용 knowledge 문서를 라우팅한다.
- 전용 테스트와 workflow path filter도 새 canonical path로 이동한다.

이 보정은 CI를 피하기 위한 우회가 아니라 Base의 패키지 무결성 경계와 progressive-disclosure 구조를 유지하면서 공용 지식과 Skill package artifact를 분리하는 구조 수정이다.

---

## 반영 결과

1. `docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md`
   - `MUST / SHOULD / STYLE_DEFAULT / TEST_REQUIRED`
   - 규범 표준 / 플랫폼 권고 / 인지·사용성 휴리스틱 / 시각 스타일 휴리스틱 분리
   - GUI 의미 문법 + Laws of UX + visual rules + 게임 접근성 통합
   - dark pattern/false progress/deliberate delay/7±2 오용 방지
2. `docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md`
   - 사용자 제공 31개 원칙 `31/31 MAPPED`
   - #26 Primacy-Recency를 #16 Serial Position Effect와 중복 정규화
   - Cognitive Bias, Paradox of the Active User를 명시적으로 포함
3. `skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md`
   - 두 공용 knowledge 문서를 기존 owner의 reference route로 흡수
4. `templates/planning/GAME_UX_UI_SYSTEM.md`
   - 프로젝트별 rule profile, tier, platform, 예외 사유, 동등 경로, 검증 증거 기록
5. `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md`
   - GUI semantics, 플랫폼 수치, 심리 윤리, STYLE_DEFAULT gate 추가
6. `tests/test_ui_ux_visual_design_rules.py`, `tests/test_ux_laws_completeness_matrix.py`
   - 핵심 계약 및 31개 완전성 회귀 테스트
7. `.github/workflows/validate-game-ux-ui-system.yml`
   - 두 공용 knowledge path와 새 테스트를 UX/UI 필수 workflow에 연결

## 보호 범위 재검토

- 신규 ACTIVE Skill: `0`
- `skills/SKILL_REGISTRY.json`: 변경 `0`
- `skills/auditing-and-refining-ui-art/SKILL.md`: 변경 `0`
- 제품 코드/Godot Scene/Theme/data: 변경 `0`
- 외부 package/dependency: 추가 `0`
- 사용자 제공 규칙의 raw copy를 별도 authoritative source로 승격: `0`

## 남은 증거 상한

- 문서 contract와 CI는 Base 구조 회귀를 검증한다.
- 실제 게임 프로젝트 화면의 가독성·입력 성공·플레이어 이해 향상은 이 PR만으로 증명하지 않는다.
- 프로젝트별 adoption은 `GAME_UX_UI_SYSTEM`에서 `ADOPT/ADAPT/AVOID/TEST/IGNORE`로 다시 판정한다.
