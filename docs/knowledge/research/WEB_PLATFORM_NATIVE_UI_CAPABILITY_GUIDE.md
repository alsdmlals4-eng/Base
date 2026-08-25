# Web Platform Native UI Capability Guide

> 상태: 공용 비실행 knowledge guide
> 적용 대상: 이미 승인된 웹 기반 thin GUI, 내부 웹 UI, 정적/동적 브라우저 surface의 구현 선택
> 비적용 대상: Godot 런타임 UI 등 Web Platform이 실행 환경이 아닌 surface
> 기준 원칙: Existing Solution First를 Web Platform 구현 선택에 구체화하되, surface authority 자체는 변경하지 않는다.

이 Guide의 목적은 기능 목록을 암기하거나 특정 framework를 금지하는 것이 아니다. 브라우저가 이미 제공하는 기능을 먼저 검토하고, 실제 지원 범위·접근성·입력 방식·사용성·실행 증거를 확인한 뒤 dependency 또는 custom implementation이 필요한지 판단하는 데 사용한다.

## 1. 구현 선택 순서

웹 UI 요구가 생기면 다음 순서로 가장 작은 충분 해법을 평가한다.

1. **Semantic HTML** — 의미 구조와 기본 상호작용으로 요구를 충족할 수 있는지 확인한다.
2. **Native CSS** — 레이아웃·상태·반응형·시각 처리를 브라우저 CSS 기능으로 해결할 수 있는지 확인한다.
3. **Browser API** — top layer, formatting, highlighting, transition 등 플랫폼 API가 이미 책임질 수 있는지 확인한다.
4. **기존 Base/프로젝트 구현** — 검증된 내부 구현을 재사용할 수 있는지 확인한다.
5. **검증된 경량 dependency** — native/기존 구현이 목표 브라우저, 접근성, 유지보수 요구를 충족하지 못할 때 최소 범위로 평가한다.
6. **Minimal Custom Implementation** — 위 선택지가 충분하지 않을 때만 직접 구현한다.

이 순서는 비용·코드량을 줄이기 위한 기본 탐색 순서이지 절대 우선권이 아니다. native 기능이 실제 요구를 충족하지 못하면 검증된 dependency나 custom implementation을 선택할 수 있다.

## 2. 공용 계약

### `PLATFORM_NATIVE_FIRST`

웹 UI에서는 Web Platform 자체를 Existing Solution의 첫 후보로 평가한다.

- 새 modal/menu/layout/state helper를 직접 만들기 전에 해당 책임을 이미 가진 플랫폼 기능이 있는지 확인한다.
- native 선택이 목표 브라우저·접근성·보안·성능·유지보수 요구를 충족하지 못하면 다음 선택지로 이동한다.
- React, Vue, Svelte 등 특정 framework를 전역적으로 금지하거나 강제하는 규칙이 아니다.

### `CAPABILITY_NOT_DEVICE_LABEL`

상호작용 설계는 `mobile/desktop` 같은 기기 라벨이나 User-Agent 추측보다 실제 capability를 우선한다.

- pointer 정밀도와 존재 여부를 볼 때 `pointer`와 `any-pointer`를 구분한다.
- hover 가능 여부는 `hover`와 `any-hover`를 필요에 맞게 확인한다.
- touch 장치가 있다고 해서 keyboard, mouse, trackpad가 없다고 가정하지 않는다.
- 하나의 장치에 fine/coarse pointer나 여러 입력 capability가 동시에 존재할 수 있음을 전제로 한다.
- 핵심 작업 경로는 실제 지원 대상인 touch, pointer, keyboard 흐름을 기준으로 검증한다.

### `PROGRESSIVE_ENHANCEMENT_REQUIRED_FOR_NEWLY_AVAILABLE`

지원 범위가 새롭거나 일부 환경에서 차이가 있는 기능은 핵심 작업을 깨뜨리지 않는 점진적 향상으로 다룬다.

- 핵심 정보·작업은 지원하지 않는 환경에서도 사용할 수 있어야 한다.
- CSS 기능은 필요할 때 `@supports`, JavaScript 기능은 적절한 feature detection을 사용한다.
- 지원되지 않을 때의 `fallback` 또는 graceful degradation을 명시한다.
- 프로젝트가 관리하는 target-browser matrix가 해당 기능을 명시적으로 보장하고 실제 검증했다면 기본 경로 승격을 허용할 수 있다.

### `NATIVE_IS_NOT_AUTOMATIC_UX_PASS`

브라우저 native 기능이라는 사실은 UX·접근성·affordance 검증을 면제하지 않는다.

- 일반 콘텐츠 영역에서 scrollbar를 숨기는 것은 스크롤 가능성의 시각적 단서를 제거하므로 기본 선택으로 사용하지 않는다.
- 핵심 기능을 `hover-only` 상호작용에만 두지 않는다.
- motion은 `prefers-reduced-motion`과 제품의 접근성 요구를 존중한다.
- focus 이동, 키보드 탈출, touch target, 읽기 순서, semantic structure를 실제 상호작용 기준으로 검증한다.
- “코드가 짧다”는 이유만으로 사용자 경험이 더 좋다고 판정하지 않는다.

### `SUPPORT_STATUS_IS_DATED_EVIDENCE`

브라우저 지원 상태는 영구 Base 불변식이 아니라 날짜가 붙은 기술 증거다.

기능 채택 기록에는 가능한 범위에서 다음을 남긴다.

```yaml
feature: <feature-or-api>
official_source: <official-compatibility-source>
verified_at: YYYY-MM-DD
support_state: WIDELY_AVAILABLE | NEWLY_AVAILABLE | LIMITED_OR_EXPERIMENTAL
target_browser_evidence: <tested-targets-or-NOT_RUN>
fallback: <fallback-or-not-required-reason>
```

판정 의미:

- `WIDELY_AVAILABLE`: 기본 후보가 될 수 있지만 프로젝트의 실제 target-browser 흐름 검증을 생략하지 않는다.
- `NEWLY_AVAILABLE`: 기본적으로 progressive enhancement로 사용하고, 목표 환경 검증 후 핵심 경로 승격 여부를 결정한다.
- `LIMITED_OR_EXPERIMENTAL`: 기본 production dependency로 두지 않고 PoC/HOLD를 우선한다. 꼭 필요하면 명시적 target과 검증된 fallback을 함께 둔다.

### `ACCESSIBILITY_INPUT_FALLBACK_REQUIRED`

상호작용은 입력 수단 하나에 종속되지 않아야 한다.

- hover에 정보가 있다면 keyboard focus와 touch에서도 같은 핵심 정보에 도달할 수 있어야 한다.
- pointer가 없는 keyboard-only 흐름도 필요한 제품에서는 실제로 이동·선택·닫기가 가능해야 한다.
- modal/top-layer UI를 직접 재구현할 경우 focus management와 escape/close behavior까지 제품 책임이 된다는 점을 비용에 포함한다.
- reduced motion, contrast, semantic element, focus visibility를 구현 후 실제 화면에서 확인한다.

### `LIVE_BEHAVIOR_EVIDENCE_OVER_CODE_SNIPPET`

코드 조각이 존재하거나 문법적으로 유효하다는 것만으로 production PASS를 선언하지 않는다.

권장 증거 단계:

```text
CODE_SNIPPET_ONLY
→ STATIC_RENDER_VERIFIED
→ INTERACTION_PATH_VERIFIED
→ TARGET_BROWSER_SET_VERIFIED
→ ACCESSIBILITY_INPUT_VERIFIED
```

요구 기능의 위험도와 범위에 맞춰 필요한 증거 단계를 정한다. 최소한 사용자가 실제로 거치는 핵심 상호작용은 render/interaction evidence로 확인한다.

### `RETIRED_SURFACE_IS_NOT_REACTIVATED`

이 Guide는 이미 승인된 웹 surface의 **구현 방법**만 선택한다. surface authority나 프로젝트 작업공간을 새로 만들 권한은 없다.

- `Tool Hub`를 active/default project route로 되살리지 않는다.
- `QA Evidence Studio`를 active/default project route로 되살리지 않는다.
- `external HTML workspace`를 기획·프로젝트 관리의 canonical authority로 되살리지 않는다.
- 새 surface가 필요하면 해당 Base authority와 변경 생명주기에서 별도로 승인한다.

## 3. 기능별 적용은 allow-list가 아니라 조사 후보로 관리한다

다음은 “있으면 먼저 조사할 native 후보”의 예시다. 특정 프로젝트에서 영구 채택을 강제하는 목록이 아니다.

| 요구 | 먼저 조사할 후보 | 추가 확인 |
| --- | --- | --- |
| modal | `<dialog>` | focus, close path, target-browser behavior |
| non-modal top-layer panel/menu | Popover | dismissal, anchor/positioning need, compatibility |
| 일시적 비활성 subtree | `inert` | focus/assistive-tech behavior |
| 컴포넌트 자체 공간 기준 반응형 | Container Query | target-browser support |
| 하위 상태에 따른 부모 스타일 | `:has()` | selector cost와 support |
| 입력 capability | `any-pointer`, `any-hover` | 복수 입력장치 공존 |
| locale 기반 숫자/통화 | `Intl.NumberFormat` | locale/currency requirements |
| boolean 상태와 class 동기화 | `classList.toggle(name, boolean)` | state owner 명확성 |
| motion 감소 | `prefers-reduced-motion` | 대체 transition/정적 상태 |
| 검색·주석 text range 강조 | CSS Custom Highlight API | support와 semantic fallback |
| DOM 상태 전환 | View Transitions API | enhancement-only fallback |

기능의 “신기함”이나 코드 길이보다 사용자 작업 경로, 접근성, 지원 환경, 유지보수 비용을 우선한다.

## 4. 2026-08-25 지원 상태 참고 스냅샷

> `REFERENCE_SNAPSHOT_NOT_CANON`
>
> 아래 값은 `verified_at: 2026-08-25` 기준 조사 보조 자료다. 실제 구현 시 공식 문서에서 현재 상태를 다시 확인한다.

| 기능 | 당시 참고 상태 | 공식 확인 출처 |
| --- | --- | --- |
| `any-pointer`, `any-hover` | widely available 계열 | MDN media feature reference |
| `<dialog>` | widely available 계열 | MDN `<dialog>` reference |
| `inert` | widely available 계열 | MDN `inert` global attribute |
| Popover | 구성 요소별 Baseline 2024/2025 차이 존재 | MDN Popover API / `popover` attribute |
| CSS Custom Highlight API | Baseline 2025 | MDN CSS Custom Highlight API |
| `@scope` | Baseline 2025 | MDN `@scope` reference |

공식 재검증 링크:

- <https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-pointer>
- <https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-hover>
- <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog>
- <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert>
- <https://developer.mozilla.org/en-US/docs/Web/API/Popover_API>
- <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover>
- <https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API>
- <https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40scope>

지원 표를 Base에 영구 고정하지 않는다. 새 구현 또는 중요한 변경 시 `verified_at`을 갱신하고 실제 target-browser evidence를 다시 수집한다.

## 5. Implementation Reality Gate 연결

웹 native 기능을 채택할 때 최소 확인 순서는 다음과 같다.

1. 이 웹 surface 자체가 현재 Base/프로젝트 authority에서 허용된 surface인지 확인한다.
2. 플랫폼 native 후보와 기존 구현을 비교했는지 확인한다.
3. 공식 지원 근거와 `verified_at`을 기록한다.
4. unsupported 환경에서 필요한 `fallback`을 정의한다.
5. keyboard/touch/pointer/focus/motion 등 관련 입력·접근성 경로를 확인한다.
6. 코드 snippet이 아니라 실제 render/interaction evidence를 남긴다.
7. dependency/custom implementation을 선택했다면 native보다 적합한 이유를 기록한다.
8. 이 Guide를 근거로 퇴역 surface나 별도 HTML workspace를 재도입하지 않았는지 확인한다.

## 6. 빠른 판정 예

- 브라우저 native 기능이 요구를 충분히 만족하고 target-browser·접근성 검증까지 통과함 → **ADOPT**
- 핵심 경로는 기존 구현을 유지하고 native 기능을 지원 환경에서만 향상으로 사용함 → **ADAPT**
- 기능은 유망하지만 `NEWLY_AVAILABLE` 또는 목표 환경 증거가 부족함 → **HOLD / progressive enhancement**
- `LIMITED_OR_EXPERIMENTAL`이고 핵심 기능을 깨뜨릴 fallback도 없음 → **REJECT_DEFAULT**
- native가 있지만 UX affordance를 악화함(예: 일반 콘텐츠 scrollbar 은닉) → **REJECT_DEFAULT**

이 Guide의 목표는 native 기능 사용률을 높이는 것이 아니라 **불필요한 재구현을 줄이면서도 실제 사용자 경험과 검증 수준을 낮추지 않는 것**이다.
