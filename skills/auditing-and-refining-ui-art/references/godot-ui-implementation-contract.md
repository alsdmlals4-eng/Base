# Godot UI 구현 계약

## 1. 원칙

Godot UI는 게임 상태를 새로 계산하는 계층이 아니라, 권위 있는 상태를 표시하고 사용자 의도를 도메인 계층에 전달하는 경계다.

```text
도메인 상태·규칙
→ 표시용 View Data
→ Control/Scene 표시
→ 사용자 입력
→ Signal 또는 명시적 Command
→ 권위 있는 도메인 처리
→ 새 상태와 결과 Event
→ UI 갱신
```

## 2. 기존 구조 우선 감사

새 UI 구조를 만들기 전에 확인한다.

- `project.godot`의 stretch·viewport·input map·autoload
- 기존 `Theme`, Theme factory, StyleBox, font, icon catalog
- 기존 UI Scene·script·layout root
- Container와 수동 좌표 사용 범위
- runtime/editor layout customization과 저장 계층
- 상태 소유자, event bus, signal, view model 또는 presenter
- 최소·목표 해상도와 플랫폼
- 기존 focus neighbor와 입력 장치 전환
- 테스트·headless·렌더 캡처 방법

기존 시스템이 있으면 확장한다. 새 Theme 기반, 범용 데이터 바인딩, 두 번째 레이아웃 저장, 범용 EditorPlugin을 기본으로 만들지 않는다.

## 3. 책임 경계

### 도메인 계층

- 피해·회복·비용·보상·확률·AI·저장·진행 판정
- 행동 가능 여부와 실패 이유
- 권위 있는 상태 변경과 결과 Event

### UI 계층

- 권위 상태를 읽을 수 있는 형태로 표시
- 선택 후보·예상 비용·위험·결과를 표현
- 포커스·입력·애니메이션·음향·텍스트 폴백
- 사용자 의도를 `Signal` 또는 명시적 Command로 반환
- 도메인 결과를 재계산하지 않고 Event와 상태를 표현

### 금지

- 버튼 callback에서 피해·보상·저장 결과 지급
- 화면마다 같은 계산을 복제
- UI animation 완료를 규칙 처리의 권위 시점으로 사용
- 표시용 정렬·필터가 도메인 데이터 순서나 저장을 몰래 변경
- UI가 게임 상태를 장기 소유

## 4. Scene 분리 기준

재사용 Scene은 다음을 모두 만족할 때만 분리한다.

1. 둘 이상의 화면 또는 반복 목록에서 같은 의미와 상태를 가진다.
2. 입력·출력 계약을 내부 구현 없이 설명할 수 있다.
3. 도메인 계산을 포함하지 않는다.
4. Theme와 데이터만 바꿔도 재사용 가능하다.
5. 독립 상태·포커스·긴 텍스트 fixture를 테스트할 가치가 있다.

한 화면에서만 쓰는 상세 패널이나 단순 wrapper는 불필요하게 범용화하지 않는다.

## 5. Control과 Container

- 화면 안정 영역은 `Control` anchor·offset과 적절한 `Container`가 소유한다.
- 반복 목록은 `VBoxContainer`, `HBoxContainer`, `GridContainer`, `FlowContainer`, `ScrollContainer` 등 의미에 맞는 Container를 사용한다.
- 수동 좌표·크기 지정은 연출, 보드 좌표, 드래그 배치처럼 의도와 검증이 있을 때만 사용한다.
- Container 자식의 좌표를 매 프레임 덮어쓰지 않는다.
- 최소 크기와 size flags가 긴 한국어·확대 글꼴·다양한 비율에서 어떻게 동작하는지 확인한다.
- 모바일은 safe area와 터치 가림, PC는 창 크기와 최소 해상도를 검증한다.

## 6. Theme와 토큰

```text
기초 토큰
→ semantic token
→ component state
→ project variant
```

예:

```text
spacing_1 / spacing_2 / spacing_3
text_primary / text_muted / text_danger
surface_default / surface_selected
focus_outline / disabled_pattern
button_primary / button_danger
```

- 숫자와 색상은 프로젝트 Theme/Resource에서 중앙 관리한다.
- 상태 의미를 색상 하나에 연결하지 않는다.
- 화면별 임의 StyleBox 복제보다 Theme type/variation을 우선한다.
- 프로젝트 아트 방향을 Material·플랫폼 기본 외형으로 덮어쓰지 않는다.
- 외부 폰트·아이콘은 라이선스와 폴백을 기록한다.

## 7. 컴포넌트 상태

필요 상태를 명시적으로 지원한다.

```text
normal
hover
focused
pressed
selected
disabled
locked
loading
warning
error
new
```

- `disabled`: 현재 실행할 수 없으며 이유와 복구가 있다.
- `locked`: 아직 해금되지 않았으며 조건이 있다.
- `loading`: 처리 중이며 중복 입력 정책이 있다.
- `error`: 실패 원인과 가능한 다음 행동이 있다.
- `selected`: 포커스와 별개의 지속 선택 상태다.

포커스·hover·선택을 같은 스타일 하나로 합치지 않는다.

## 8. Signal 계약

Signal 이름은 사용자 의도를 말한다.

```gdscript
signal selection_requested(item_id: StringName)
signal confirmation_requested(action_id: StringName)
signal cancellation_requested()
signal detail_requested(item_id: StringName)
```

다음처럼 결과나 구현 세부를 UI가 소유하는 이름은 피한다.

```gdscript
signal damage_applied(amount)
signal gold_saved()
signal database_updated()
```

도메인 처리 결과는 권위 계층이 상태 또는 event로 돌려준다.

## 9. 포커스·입력

- 화면 진입 시 첫 의미 포커스를 지정한다.
- 시각 순서와 `focus_neighbor_*`, `focus_next`, `focus_previous`가 일치한다.
- 동적 항목 추가·삭제 뒤 포커스를 유효한 이웃으로 복구한다.
- modal을 닫으면 modal을 연 요소 또는 가장 가까운 의미 위치로 돌아간다.
- 비활성·숨김 항목에 포커스가 갇히지 않는다.
- 포인터·키보드·게임패드·터치 중 프로젝트가 선언한 경로를 각각 완주한다.
- 입력 아이콘은 현재 장치에 맞게 바뀌되 문맥과 선택은 유지한다.
- 취소/뒤로 입력은 화면마다 같은 의미를 유지한다.

## 10. 텍스트·현지화

- 한국어의 긴 조사·서술·숫자 단위를 fixture로 검증한다.
- 스마트 줄바꿈, 최소 너비, tooltip 또는 상세 패널을 사용한다.
- 중요 정보는 잘린 텍스트나 hover에만 두지 않는다.
- 버튼 문구는 결과 행동을 말한다: `확인`보다 `장비 분해`, `재도전 비용 2 지불`.
- 오류는 원인·영향·복구를 포함한다.
- 내부 enum·ID·영문 오류 코드를 플레이어 문구로 직접 노출하지 않는다.

## 11. 애니메이션·음향·폴백

- 애니메이션은 상태 변경을 설명하며 규칙 처리의 권위가 아니다.
- 모션 감소·즉시 완료·빠른 재생에서 결과와 입력 가능 시점이 일치한다.
- 음향을 끄면 자막·아이콘·로그 또는 시각 상태가 의미를 보존한다.
- 자산 누락 시 기본 텍스트·도형·아이콘으로 핵심 기능이 유지된다.
- 경고 플래시·흔들림·카메라 이동은 강도·반복·중단 가능성을 검증한다.

## 12. UI 폴리싱 구현 계약

### semantic feedback token

```text
feedback_routine
feedback_confirming
feedback_warning
feedback_reward
feedback_critical
motion_reduced
sound_muted
haptic_disabled
```

- token은 절대 시간·음량·색을 공용 상수로 강제하지 않고 프로젝트 Theme·Resource의 의미 계층을 제공한다.
- 같은 의미는 화면마다 같은 feedback tier를 사용하며, 자주 반복되는 행동은 낮은 강도를 사용한다.

### Tween·AnimationPlayer 중단과 재진입

- 새 전환 시작 전에 기존 Tween의 종료·대체·병합 정책을 선언한다.
- scale·alpha·position을 상대 누적해 재진입 drift를 만들지 않는다.
- 즉시 완료와 `reduced motion` 경로에서도 최종 상태와 입력 가능 시점이 같다.
- 애니메이션 완료 callback은 피해·보상·저장·진행 지급의 권위가 아니다.

### 중복 입력

- 도메인 계층이 중복 실행 방지와 idempotency를 책임한다.
- UI는 pending 상태와 입력 접수 피드백을 제공하되 성공 결과를 선지급하지 않는다.
- 빠른 연타, 게임패드 버튼 유지, 터치 double tap을 fixture로 검증한다.

### 동등한 피드백 경로

- `reduced motion`: 정적 상태·페이드·즉시 완료.
- mute: 텍스트·아이콘·상태·로그.
- haptic off: 시각·음향 또는 텍스트 상태.
- 누락 자산: 기본 텍스트·도형·아이콘.

### 반복 사용과 성능

- 반복 화면 전환과 목록 갱신에서 Tween·Signal·Timer·AudioStreamPlayer가 누적되지 않는다.
- UI 전환 frame time, allocation, draw call, memory spike 후보를 목표 플랫폼에서 기록한다.
- 성능 측정을 실행하지 않았으면 `NOT_RUN` 또는 `UNVERIFIED`로 유지한다.

## 13. 검증 매트릭스

### 정적

- scene/script/resource parse
- Theme type/variation 참조
- Signal 연결과 상태 소유 경계
- 금지된 UI 도메인 계산 후보
- focus 설정·접근성 메타데이터 후보

### 런타임

- 최소·목표 해상도와 창 비율
- 긴 한국어·최대 수치·빈 목록
- 정상·disabled·locked·loading·error
- 포인터·키보드·게임패드·터치
- modal 진입·취소·복귀
- 모션 감소·음향 끄기·자산 누락

### 인간

- 중심 질문과 다음 행동 설명
- 비용·위험·결과 예측
- 오류·실수 복구
- 결과 인과 설명

자동 테스트가 통과해도 인간 항목은 `HUMAN_NOT_RUN`일 수 있다.

## 14. 완료 출력

```yaml
existing_ui_system:
state_owner:
view_data_source:
component_scenes:
theme_variations:
signal_contracts:
focus_contract:
input_paths:
resolution_fixtures:
text_fixtures:
fallbacks:
feedback_tiers:
reduced_motion:
duplicate_input_policy:
interruption_and_reentry:
repetition_and_performance:
static_validation:
runtime_validation:
human_validation:
remaining_risks:
```
