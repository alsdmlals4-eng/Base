# 게임 UX/UI 공용 체계 적대적 검토

- 대상 PR: Base #57
- 기준 branch: `gpt/game-ux-ui-system-20260729`
- Work Mode: `REVIEW`
- 주 Skill: `running-adversarial-review-and-refinement`
- 전문 Skill: `auditing-and-refining-ui-art`
- Foundation: `evolving-project-discipline-skills`, `reviewing-and-validating-project-changes`
- 검토일: 2026-07-29

## 1. Review Scope Map

검토 대상:

- 기존 Skill ID와 A~E UI 감사 계약
- 새 UX 설계 Skill Mode
- 공식 레퍼런스 채택 정책
- 패턴 라이브러리
- Godot UI 상태 소유 계약
- 프로젝트 어댑터 계약
- 템플릿과 구조 테스트
- CI 소비자
- 기존 UI 감사 회귀

범위 밖:

- 프로젝트 제품 코드·Scene·데이터·수치
- 실제 Godot 렌더·입력
- Android/PC 실기기
- 장애 사용자·보조기기·일반 플레이어 검증

## 2. 공격과 판정

### F-01 — 새 광역 Skill ID가 기존 UI 감사와 중복될 위험

- 공격: UX/UI 설계 Skill을 새로 만들면 `auditing-and-refining-ui-art`, 프로젝트 UX Skill, 통합 검증 Skill 사이에서 주 책임이 중복된다.
- 사실 검증: 기존 Skill은 A~E 감사·승인 수정·재검수를 이미 담당하고 프로젝트들이 해당 ID를 참조한다.
- 판정: `MUST_FIX`.
- 처리: 새 ID를 만들지 않고 기존 ID와 경로를 유지했다. 설계 Mode와 감사 Mode를 분리하고 타 Skill 경계를 명시했다.
- 회귀: 기존 scanner 명령, A~E, `CANDIDATE`, 승인 전 수정 금지, 전후 렌더 계약을 구조 테스트로 고정했다.

### F-02 — 기능 목록과 컴포넌트 목록이 UX 설계를 대체할 위험

- 공격: Theme·Button·Card 목록만 늘고 플레이어가 무엇을 판단하는지 빠질 수 있다.
- 판정: `MUST_FIX`.
- 처리: `experience-contract`, 화면별 중심 질문, 첫 시선, 정보 L0~L3, 관찰 가능한 성공 기준을 필수화했다.
- 회귀: 프로젝트 템플릿의 첫 Section을 플레이어 UX 약속으로 고정했다.

### F-03 — 공식 웹/앱 지침을 게임에 그대로 복제할 위험

- 공격: WCAG·Material·Apple의 수치·컴포넌트·시각 언어를 Godot 게임에 무비판적으로 적용할 수 있다.
- 판정: `MUST_FIX`.
- 처리: 모든 레퍼런스를 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정하고 플랫폼·장르·코어 변환 축과 복제 금지를 기록했다.
- 회귀: Reference Card에 비적용 부분·편향·검증 필요 항목을 요구한다.

### F-04 — UI가 도메인 계산과 저장 상태를 소유할 위험

- 공격: 예상 결과·피드백을 구현하며 피해·보상·저장·진행을 UI callback이나 animation 완료 시점에 계산할 수 있다.
- 판정: `MUST_FIX`.
- 처리: `권위 상태 → View Data → UI → 사용자 의도 Signal → 도메인 처리 → 결과 Event` 경계를 명시했다.
- 회귀: 구조 테스트에서 도메인 규칙, 사용자 의도, Signal, 재계산 금지 문구를 검사한다.

### F-05 — 색·소리·모션을 많이 쓰면 접근성이 해결됐다고 오판할 위험

- 공격: 다중 효과가 있어도 각 효과가 같은 의미를 독립적으로 전달하지 못할 수 있다.
- 판정: `MUST_FIX`.
- 처리: 장식 중복과 동등 신호를 구분하고 각 채널을 하나씩 끈 상태의 검증을 요구했다.
- 회귀: 접근성 체크리스트에서 색·소리·모션 각각의 독립 폴백을 검사한다.

### F-06 — 자동 검사 통과를 사람 이해 증거로 대체할 위험

- 공격: Markdown·정적 UI·Godot parse가 통과하면 플레이어가 이해했다고 표시할 수 있다.
- 판정: `MUST_FIX`.
- 처리: 자동·정적·런타임·기기·사람·보조기기 증거를 분리하고 미실행 상태를 `HUMAN_NOT_RUN`으로 유지했다.
- 회귀: 새 테스트가 자동 검사와 사람 이해 분리 문구를 강제한다.

### F-07 — 새 구조 테스트가 CI에서 실행되지 않는 위험

- 공격: 테스트 파일을 추가해도 기존 workflow가 명시 목록만 실행해 누락할 수 있다.
- 실제 증거: RED PR #58의 기존 운영체계 workflow는 성공했으나 새 테스트를 실행하지 않았다.
- 판정: `MUST_FIX`.
- 처리: `.github/workflows/validate-game-ux-ui-system.yml`을 추가해 새 UX/UI 계약 테스트와 기존 UI 감사 테스트를 함께 실행한다.
- RED 증거: 구현 전 commit과 새 workflow를 결합한 run에서 `Validate Game UX UI System`이 실패했다.
- GREEN 요구: PR #57 최신 HEAD에서 같은 workflow가 성공해야 한다.

### F-08 — Registry 설명이 기존 감사 중심이라 설계 요청 발견성이 부족할 위험

- 공격: 공용 Registry의 trigger는 `ui-art-audit`, `godot-ui`, `web-ui`, `visual-refinement`, `render-review`이며 use_when은 감사 중심이다.
- 사실 검증: 기존 `godot-ui` trigger와 실제 Skill frontmatter는 새 설계 요청을 라우팅할 최소 호환성을 가진다. 프로젝트들은 별도 adapter와 프로젝트 UX Skill에서 명시적으로 Base mode를 연결한다.
- 판정: `SHOULD_FIX`.
- 처리: `skills/README.md`와 agent interface를 UX 설계·감사 역할로 갱신한다. Registry 전체 one-line 구조 변경은 이번 PR에서 불필요한 광역 충돌을 피하기 위해 보류한다.
- 후속 조건: 실제 자동 라우팅에서 `UX design system`, `information architecture`, `interaction pattern`, `accessibility`, `Godot UI contract` 요청이 누락되면 Registry trigger 확장을 별도 작은 PR로 진행한다.

### F-09 — 패턴 라이브러리가 체크리스트 과잉과 화면 획일화를 만들 위험

- 공격: 모든 화면에 12개 패턴을 강제하면 과설계·정보 과밀·장르 훼손이 발생한다.
- 판정: `MUST_FIX`.
- 처리: 문제와 플레이어 위험이 일치하는 패턴만 선택하고 `IGNORE / AVOID`를 허용한다. 새 요소는 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK 강화 → ADD` 순으로 검토한다.

### F-10 — 기존 프로젝트 문서와 공용 템플릿이 중복 정본을 만들 위험

- 공격: 프로젝트마다 새 `UX_UI_SYSTEM.md`를 무조건 만들면 기존 UI 명세·전문 Skill과 권한이 충돌한다.
- 판정: `MUST_FIX`.
- 처리: adapter 계약을 A/B/C 유형으로 나눴다. 기존 Skill이나 책임 원본이 있으면 갱신하고, 둘 다 없을 때만 템플릿을 설치한다.

### F-11 — HTML 기획 대시보드로 다시 확장될 위험

- 공격: Base에 기존 dashboard Skill이 있어 UX 흐름을 HTML 도구로 자동 전환할 수 있다.
- 판정: `MUST_FIX`.
- 처리: 설계·계획의 제외 범위에 HTML 기획 대시보드를 명시했다. 이번 결과는 Markdown·Skill·reference·template·test로 제한한다.

### F-12 — 기존 UI 감사의 시각 품질 책임이 약해질 위험

- 공격: UX 설계 내용이 늘어 A~E 감사·실제 렌더·승인 수정 게이트가 묻힐 수 있다.
- 판정: `MUST_FIX`.
- 처리: Skill을 설계와 구현 결과 감사 Section으로 분리하고 기존 명령·상태·승인·재감사를 그대로 보존했다.
- 회귀: 새 workflow가 `tests/test_ui_art_audit.py`도 함께 실행한다.

## 3. Rejected Critiques

### R-01 — UX 설계와 UI 감사를 반드시 별도 Skill로 분리해야 한다

- 기각 이유: 프로젝트들의 기존 Skill 참조와 Base Registry 호환성을 깨고, 실제 작업에서는 설계→구현→감사가 같은 UI 책임 경계와 reference를 공유한다. 명시적 Mode 분리로 충분하다.

### R-02 — 모든 프로젝트에 동일한 파일명과 폴더 구조를 설치해야 한다

- 기각 이유: 프로젝트별 운영체계와 현행 정본 경로가 다르며 강제 표준화는 stale 참조와 중복 정본을 만든다.

### R-03 — 접근성 수치를 공용 고정값으로 제공해야 한다

- 기각 이유: 플랫폼·거리·입력·장르에 따라 달라진다. 공식 기준은 참고하되 실제 목표 환경 검증 전에는 `TEST`다.

## 4. Regression Recheck

| 항목 | 상태 | 증거 |
|---|---|---|
| 기존 Skill ID·경로 | PASS | 동일 ID/경로 유지 |
| 기존 A~E 감사·scanner | PENDING_CI | `tests/test_ui_art_audit.py` |
| 새 UX/UI 구조 계약 | PENDING_CI | `tests/test_game_ux_ui_system.py` |
| RED 실패 | PASS | PR #58 전용 workflow failure |
| GREEN 성공 | PENDING_CI | PR #57 최신 HEAD |
| 공식 레퍼런스 분류 | PASS_STATIC | reference library와 test |
| 프로젝트 어댑터 경계 | PASS_STATIC | project adapter contract |
| 제품 코드·Scene·데이터 | PASS_DIFF | Base 공용 문서·Skill·test·workflow만 변경 |
| Godot runtime | NOT_RUN | Base는 프로젝트 runtime이 없음 |
| 사람 플레이 | HUMAN_NOT_RUN | 프로젝트 적용 후 별도 |
| 보조기기 사용자 | HUMAN_NOT_RUN | 별도 사용자 검증 필요 |

## 5. Decision

현재 남은 병합 게이트:

1. PR #57의 `Validate Game UX UI System` 성공.
2. 운영체계 CI required gate 성공.
3. changed files가 공용 문서·Skill·Template·Test·Workflow 범위인지 재확인.
4. Base 병합 후 main HEAD에서 post-merge 재검토.
5. 병합된 Base commit을 기준으로 다섯 프로젝트 어댑터 적용.
