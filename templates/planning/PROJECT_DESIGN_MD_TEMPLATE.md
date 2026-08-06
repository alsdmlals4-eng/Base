---
format: project-design-md
format_version: alpha
source_commit_or_release: ""
last_verified_at: ""
canonical_scope: visual-language-only
colors:
  background:
    value: ""
    role: ""
  foreground:
    value: ""
    role: ""
  accent:
    value: ""
    role: ""
typography:
  body:
    family: ""
    size: ""
    line_height: ""
  heading:
    family: ""
    scale: []
spacing:
  base_unit: ""
  scale: []
shapes:
  radius: []
  border: []
  elevation: []
components:
  button:
    tokens: []
    states: []
godot_theme_mapping:
  theme_path: ""
  token_map: {}
web_token_mapping:
  css_or_dtcg_path: ""
  token_map: {}
accessibility_constraints:
  contrast: "NOT_RUN"
  focus_visibility: "NOT_RUN"
  reduced_motion: "NOT_RUN"
reference_provenance: []
validation_status: NOT_RUN
---

# <프로젝트명> DESIGN.md

## 시각 언어

<이 프로젝트가 어떤 감정과 위계를 시각적으로 전달하는지 설명한다.>

## 토큰 사용 원칙

- 색·글꼴·간격·형태 값은 front matter의 token ID를 참조한다.
- 상태 의미와 행동은 `GAME_UX_UI_SYSTEM`을 따른다.
- 이 파일은 게임 규칙·보상·저장·진행·도메인 상태를 소유하지 않는다.

## 컴포넌트 시각 규칙

### Do

-

### Don't

-

## Godot Theme 적용

- `Theme`·`StyleBox`·Font·Color·Constant mapping:
- 실제 렌더 조건:

## Web token 적용

- CSS variable·DTCG·Tailwind mapping:
- 외부 UI 코드 조달 Gate:

## 접근성 제약

- 대비:
- 포커스:
- 긴 한국어:
- 최소 해상도:
- Reduced Motion:

## 외부 레퍼런스와 변환

| source | exact version/date | official 여부 | 채택 원리 | 변환 축 | 복제 금지 |
|---|---|---|---|---|---|
| | | | | | |

## 검증·미검증·롤백

- validation_status:
- actual render:
- human review: HUMAN_NOT_RUN
- unresolved risks:
- rollback:
