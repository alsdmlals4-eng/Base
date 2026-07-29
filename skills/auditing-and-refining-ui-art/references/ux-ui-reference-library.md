# UX/UI 공식 레퍼런스 라이브러리

> 최종 확인: 2026-07-29

외부 자료는 프로젝트 요구사항이나 구현 사실의 정본이 아니다. 문제·플랫폼·플레이어 위험이 일치하는 원리만 채택하고 브랜드 외형·자산·문구를 복제하지 않는다.

## 채택 판정

| 판정 | 의미 |
|---|---|
| `ADOPT` | 구조와 원칙을 공용 기본값으로 채택 |
| `ADAPT` | 원리는 채택하되 게임·Godot·플랫폼에 맞게 변환 |
| `AVOID` | 프로젝트 코어·가독성·접근성을 해치므로 사용하지 않음 |
| `TEST` | 실제 플레이·기기·사용자 검증 전에는 확정하지 않음 |
| `IGNORE` | 현재 문제와 무관해 읽기·적용 대상에서 제외 |

## 1. Xbox Accessibility Guidelines

- 허브: https://learn.microsoft.com/en-us/xbox/accessibility/guidelines
- 입력: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107
- 목표 명료성: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/109
- UI 포커스: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/113
- UI 맥락: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/114
- 대비: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102
- 다중 채널: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103
- 자막: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104
- 모션: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117

### Base 판정

- `ADOPT`: 중요한 정보를 여러 채널로 제공, 포커스와 맥락 보존, 목표와 다음 행동 명료화, 입력 대안, 취소·되돌리기 검토.
- `ADAPT`: Xbox 전용 입력·플랫폼 항목을 프로젝트가 실제 지원하는 PC·Android·게임패드 범위로 변환.
- `TEST`: 시간 제한, 입력 반복, 모션 강도와 텍스트 크기는 실제 장르·기기·사용자 증거로 조정.
- `AVOID`: 체크리스트 존재만으로 접근성 완료를 주장하는 것.

## 2. W3C WCAG 2.2

- 원문: https://www.w3.org/TR/WCAG22/

### Base 판정

- `ADAPT`: 인지 가능, 운용 가능, 이해 가능, 견고성 원칙을 게임 UI의 텍스트·대비·포커스·입력·오류·목표 크기·도움말에 변환.
- `TEST`: 웹 기준 수치와 성공 기준을 게임 화면·TV 거리·모바일 손가락·게임패드 탐색에 그대로 고정하지 않고 목표 플랫폼에서 검증.
- `IGNORE`: 프로젝트에 없는 브라우저 문서 구조나 웹 전용 기술 요구.
- `AVOID`: WCAG 자동 스캔 통과를 게임 접근성 전체 통과로 표시하는 것.

## 3. Godot 공식 UI 문서

- UI 개요: https://docs.godotengine.org/en/stable/tutorials/ui/index.html
- 키보드·컨트롤러 GUI navigation: https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html
- Theme: https://docs.godotengine.org/en/stable/classes/class_theme.html
- Theme editor: https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_theme_editor.html
- Control: https://docs.godotengine.org/en/stable/classes/class_control.html
- Container: https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html

### Base 판정

- `ADOPT`: `Control`·`Container`·`Theme`·명시적 포커스와 입력 액션을 네이티브 구현 기반으로 사용.
- `ADAPT`: 기존 프로젝트 Theme·Scene·레이아웃·편집 시스템을 먼저 조사하고 필요한 최소 단위만 재사용.
- `AVOID`: 프로젝트를 조사하지 않고 범용 UI 프레임워크, 두 번째 상태 저장 계층, 화면별 중복 Theme를 추가.
- `TEST`: focus neighbor 자동 추론과 복합 동적 목록은 실제 탐색 순서로 검증.

## 4. Apple Human Interface Guidelines

- 접근성: https://developer.apple.com/design/human-interface-guidelines/accessibility/
- 게임 설계: https://developer.apple.com/design/human-interface-guidelines/designing-for-games/
- 게임 컨트롤: https://developer.apple.com/design/human-interface-guidelines/game-controls

### Base 판정

- `ADAPT`: 명료한 상태·입력 피드백·플랫폼 관습·대체 입력·가독성 원리를 해당 프로젝트의 Android/PC/Godot 입력으로 변환.
- `TEST`: 터치 영역·제스처·게임 컨트롤 배치는 실제 기기와 손 크기·잡는 방식으로 검증.
- `IGNORE`: Apple 플랫폼 전용 API와 프로젝트가 지원하지 않는 장치.
- `AVOID`: Apple 시각 언어를 다른 프로젝트의 고유 아트 방향보다 우선.

## 5. Material Design 3

- 시스템 허브: https://m3.material.io/
- 상호작용 상태: https://m3.material.io/foundations/interaction/states/overview

### Base 판정

- `ADAPT`: 토큰→컴포넌트→상태→패턴 계층, 일관된 상태 표현, 디자인 값의 중앙 관리 원리를 Godot Theme와 Resource에 변환.
- `TEST`: 상태 투명도·크기·간격·모션 숫자는 초기값일 뿐 프로젝트 화면과 기기로 검증.
- `AVOID`: Material 컴포넌트 외형과 모바일 앱 내비게이션을 게임에 그대로 복제.
- `IGNORE`: 프로젝트에 없는 웹/앱 제품 표면.

## 6. Nielsen Norman Group

- 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- Design Systems 101: https://www.nngroup.com/articles/design-systems-101/
- Design Pattern Guidelines: https://www.nngroup.com/articles/design-pattern-guidelines/
- Content Design Systems: https://www.nngroup.com/articles/content-design-systems/

### Base 판정

- `ADAPT`: 시스템 상태, 현실과의 일치, 사용자 통제, 일관성, 오류 예방, 회상보다 인식, 유연성, 최소주의, 오류 복구, 도움말을 게임의 HUD·행동·로그·튜토리얼·복귀 흐름에 적용.
- `TEST`: 업무용 제품의 효율성 휴리스틱이 의도적 긴장·미스터리·발견을 제거하지 않는지 검증.
- `AVOID`: 장르적 불확실성과 조작 불명료를 같은 것으로 취급.

## 7. UI 폴리싱 근거 보강

### W3C 세부 성공 기준

- 포커스 외형: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- 목표 크기 최소: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- 상호작용 애니메이션: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html

Base 판정:

- `ADOPT`: 키보드 포커스는 인접 상태와 구분되고, 상호작용 모션은 필수 정보가 아니면 줄이거나 끌 수 있다.
- `ADAPT`: 웹 CSS 수치를 게임 화면 거리·해상도·터치·게임패드에 그대로 고정하지 않고 목표 기기에서 검증한다.
- `AVOID`: 체크리스트 수치만 충족하고 실제 포커스 탐색·읽기·입력 성공을 검증하지 않는 것.

### Xbox 폴리싱 관련 지침

- 오류·파괴적 행동: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/115
- 햅틱 피드백: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/110

Base 판정:

- `ADOPT`: 영구 결과 전에 검토·수정하거나 가능한 경우 되돌리기, 햅틱 끄기와 동등한 시각·음향 경로.
- `TEST`: 경고 지속 시간·진동 강도·반복 빈도는 실제 장르와 기기에서 검증한다.

### Apple 피드백·모션·햅틱·게임 컨트롤

- 피드백: https://developer.apple.com/design/human-interface-guidelines/feedback
- 모션: https://developer.apple.com/design/human-interface-guidelines/motion
- 햅틱: https://developer.apple.com/design/human-interface-guidelines/playing-haptics
- 게임 컨트롤: https://developer.apple.com/design/human-interface-guidelines/game-controls

Base 판정:

- `ADAPT`: 행동 중요도에 비례한 피드백, 같은 원인에 정렬된 시각·음향·햅틱, 목적 있는 모션, 눌림 상태 가시성을 Godot 프로젝트에 변환한다.
- `AVOID`: 모든 반복 행동에 햅틱·사운드·튕김을 중첩하거나 플랫폼 고유 외형을 게임 아트보다 우선하는 것.
- `TEST`: 모션 거리·시간·음량·햅틱 강도와 반복 피로는 실제 기기에서 검증한다.

### Godot 폴리싱 구현 원리

- `Theme` preview와 variation으로 상태를 중앙 관리하고, `Container`와 focus neighbor를 실제 해상도·입력 순서로 검증한다.
- Tween·AnimationPlayer는 표시를 책임하며 도메인 결과를 소유하지 않는다.
- 중단·즉시 완료·재진입·입력 장치 전환에서도 선택과 포커스가 보존되는지 테스트한다.

## 8. 레퍼런스 사용 절차

```text
현재 플레이어 문제와 증거
→ 관련 공식 원문 최소 범위
→ 적용 가능한 원리
→ 프로젝트 코어와 충돌
→ ADOPT / ADAPT / AVOID / TEST / IGNORE
→ 구현 계약
→ 자동·런타임·사람 검증
```

각 참고는 `templates/research/UX_UI_REFERENCE_CARD.md`로 기록한다.

## 9. 금지

- 출처 제목만 보고 원문을 읽지 않은 채 규칙 생성.
- 최신 확인일·플랫폼·버전 없이 영구 표준으로 고정.
- 다른 제품의 화면, 아이콘, 문구, 고유 상호작용을 복제.
- 공식 지침을 사용자의 최신 결정이나 프로젝트 정본보다 높은 권한으로 사용.
- 자동 검사·전문가 검토·실제 사용자 검증을 같은 증거로 합침.
