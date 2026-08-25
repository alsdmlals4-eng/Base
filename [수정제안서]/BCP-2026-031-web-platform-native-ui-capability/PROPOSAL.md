# BCP-2026-031 — Web Platform Native UI Capability Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base` + 사용자 제공 GeekNews/HTMLcat 요약
- 기준 Base 커밋: `3c3376845b9a1b7921a4260aa6259cd61533ffc4`
- 외부 자료 재확인일: `2026-08-25`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- 지식 상태: `사용자 제공 관찰 + 공식 MDN 현재 지원 상태 교차검증`

## 관찰과 증거

사용자가 제공한 HTMLcat/GeekNews 자료는 HTML/CSS/JS 자체가 제공하는 최근 기능을 이용해 라이브러리·직접 구현을 줄이는 여러 사례를 묶고 있다. 반복되는 공통 원리는 개별 기능 42개의 암기가 아니라 다음 네 가지다.

1. 웹 UI 요구가 생기면 별도 라이브러리나 직접 JavaScript 구현 전에 Semantic HTML → Native CSS → Browser API 순으로 플랫폼 기능을 먼저 확인한다.
2. `mobile/desktop` 같은 기기 라벨보다 `any-pointer`, `any-hover` 등 실제 입력 capability를 기준으로 상호작용을 결정한다.
3. 새 기능은 브라우저 지원 상태를 확인하고 Progressive Enhancement와 fallback을 유지한다.
4. 기술적으로 가능한 native 기능도 접근성·affordance·입력 방식·실제 사용자 흐름을 해치면 채택하지 않는다. 대표 반례는 일반 콘텐츠 영역의 scrollbar 은닉이다.

2026-08-25 공식 MDN 교차검증에서 확인한 현재 예시는 다음과 같다.

- Popover HTML/API는 최신 브라우저에서 넓게 사용할 수 있으나 API 세부 범위별 지원 차이가 있어 현재 support 상태를 함께 확인해야 한다.
- CSS `@scope`는 MDN Baseline 2025로 표시된다.
- CSS Custom Highlight API는 MDN Baseline 2025로 표시된다.
- 위 상태는 영구 정본값이 아니라 `verified_at`이 붙은 기술 스냅샷으로 취급해야 한다.

검증 원출처:

- `https://developer.mozilla.org/en-US/docs/Web/API/Popover_API`
- `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover`
- `https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40scope`
- `https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API`

Base에는 이미 `Existing Solution First Gate`와 `TOOL_INTERFACE_SURFACE_SELECTION`이 존재한다. 후자는 core/CLI/programmatic contract와 선택적 thin GUI를 분리하고, Tool Hub·QA Evidence Studio·external HTML workspace 같은 퇴역 작업면을 되살리지 말라고 명시한다. 그러나 **웹 기반 thin GUI/내부 도구를 실제로 구현할 때 Web Platform 자체를 기존 해법으로 먼저 평가하는 전용 판단·검증 계약**은 현재 명시적으로 라우팅되어 있지 않다.

## 일반화 후보

새 Skill이나 새 웹 도구를 만들지 않고 기존 Base 지식 계층에 비실행 Guide를 추가한다.

```text
웹 UI 요구
→ semantic HTML로 해결 가능한가?
→ native CSS로 해결 가능한가?
→ browser API로 해결 가능한가?
→ 기존 Base/프로젝트 구현이 있는가?
→ 검증된 경량 dependency가 필요한가?
→ 마지막에만 minimal custom implementation
```

핵심 계약 후보:

- `PLATFORM_NATIVE_FIRST`: 웹 UI에서는 Web Platform 자체를 Existing Solution의 첫 후보로 평가한다.
- `CAPABILITY_NOT_DEVICE_LABEL`: device type 추측 대신 실제 pointer/hover/touch/keyboard capability와 목표 입력 흐름을 본다.
- `PROGRESSIVE_ENHANCEMENT_REQUIRED_FOR_NEWLY_AVAILABLE`: 새 기능은 unsupported 환경에서도 핵심 작업이 유지되도록 fallback 또는 graceful degradation을 둔다.
- `NATIVE_IS_NOT_AUTOMATIC_UX_PASS`: native라는 이유만으로 UX·접근성 검증을 면제하지 않는다.
- `SUPPORT_STATUS_IS_DATED_EVIDENCE`: Baseline/Widely available/Limited/Experimental 판정에는 확인 출처와 날짜를 붙이고 영구 규칙처럼 고정하지 않는다.
- `ACCESSIBILITY_INPUT_FALLBACK_REQUIRED`: hover-only, pointer-only, motion-only 기능을 기본 작업 경로로 만들지 않는다.
- `LIVE_BEHAVIOR_EVIDENCE_OVER_CODE_SNIPPET`: 기능 채택 근거는 코드 조각만이 아니라 실제 렌더/상호작용 또는 대상 브라우저 실행 증거를 요구한다.

기능별 예시는 `ADOPT / ADAPT / HOLD / REJECT_DEFAULT`로만 관리하고, 특정 API 지원 상태를 영구 Base 불변식으로 승격하지 않는다.

## 프로젝트 전용으로 남길 내용

- 특정 프로젝트의 UI 컴포넌트·디자인·색상·DOM 구조.
- 특정 브라우저 버전의 현재 지원표를 영구 프로젝트 정본으로 고정하는 행위.
- HTMLcat의 42개 항목 전체 복제.
- Tool Hub·QA Evidence Studio·external HTML workspace 등 현재 퇴역한 작업면의 재도입.
- React/Vue/Svelte 등 특정 framework를 전역적으로 금지하거나 강제하는 규칙.

## 적용 조건과 비사용 조건

적용 조건:

- Base 또는 프로젝트에서 웹 기반 thin GUI, 로컬 내부 도구, 정적/동적 웹 UI를 새로 만들거나 수정할 때.
- UI 기능을 직접 구현할지, Web Platform API를 쓸지, dependency를 추가할지 비교할 때.
- 반응형·입력 capability·modal/popover·검색 강조·transition 등 브라우저가 이미 제공할 수 있는 영역을 설계할 때.

비사용 조건:

- Godot 런타임 UI처럼 Web Platform이 실행 환경이 아닌 경우에는 강제하지 않는다.
- native 기능이 프로젝트 지원 브라우저·접근성 요구·보안 요구를 충족하지 못하면 dependency/custom implementation을 막지 않는다.
- 퇴역한 HTML workspace/Tool Hub를 이 Guide를 근거로 다시 active route로 올리지 않는다.
- 시각적 장식이나 기술 과시를 위해 Experimental 기능을 production 기본값으로 쓰지 않는다.

## 반례와 위험

### 최소 3안 비교

| 안 | 장점 | 위험·비용 | 판정 |
| --- | --- | --- | --- |
| A. HTMLcat 기능 42개를 AGENTS/체크리스트에 직접 복사 | 즉시 눈에 띄고 항목별 검색이 쉬움 | root 규칙 비대화, 지원 상태 노후화, 외부 목록 중복, 기능 나열이 판단 원칙을 가림 | `REJECT` |
| B. `web-native-ui` 신규 Skill 생성 | 자동 라우팅과 실행 절차를 강제하기 쉬움 | 독립 실행 경계가 약하고 기존 UI/검증/Existing Solution 책임과 중복, Skill 증가 | `REJECT` |
| C. 기존 knowledge/research + capability routing에 얇은 Guide 추가 | Web Platform 선택 원칙만 공용화하고 현재 surface retirement·Skill 구조를 보존, 지원 상태를 dated evidence로 관리 가능 | routing 누락을 막는 focused regression test 필요 | `ADOPT` |

주요 위험과 대응:

1. **Native fetishism** — 플랫폼 기능이 있다는 이유만으로 무조건 채택하지 않는다. 접근성·사용성·지원 범위·유지보수 비용을 같은 기준으로 비교한다.
2. **지원 상태 노후화** — API 이름별 영구 허용/금지표 대신 `verified_at`, 공식 source, 현재 Baseline/compatibility를 구현 시 재확인한다.
3. **Progressive enhancement를 핑계로 깨진 fallback 허용** — 핵심 작업 경로가 unsupported 환경에서 실제 작동하는지 검증한다.
4. **device detection 오용** — user-agent/device label을 capability proxy로 사용하지 않는다.
5. **접근성 회귀** — hover-only, scrollbar 제거, motion 강제, focus trapping 재구현 같은 패턴을 별도 경고한다.
6. **퇴역 surface 부활** — 이 제안은 HTML 기반 UI 구현 방법만 다루며 Tool Hub/QA Studio/project-management HTML workspace의 authority를 변경하지 않는다.
7. **라이브 데모 없는 코드 카탈로그화** — 실제 채택 기능은 코드 snippet 존재가 아니라 실제 렌더/interaction evidence로 검증한다.

## 영향 범위와 검증

승인 시 최소 구현 범위:

- `docs/knowledge/research/WEB_PLATFORM_NATIVE_UI_CAPABILITY_GUIDE.md` 신규.
- `docs/knowledge/README.md`에 필요한 최소 라우팅 추가.
- `docs/DOCUMENTATION_MAP.md`에 책임 원본 라우팅 추가.
- `tests/test_web_platform_native_ui_capability.py`에 focused regression 추가.

검증 조건:

- Guide가 `PLATFORM_NATIVE_FIRST`, `CAPABILITY_NOT_DEVICE_LABEL`, `PROGRESSIVE_ENHANCEMENT_REQUIRED_FOR_NEWLY_AVAILABLE`, `NATIVE_IS_NOT_AUTOMATIC_UX_PASS`, `SUPPORT_STATUS_IS_DATED_EVIDENCE`, `LIVE_BEHAVIOR_EVIDENCE_OVER_CODE_SNIPPET`을 명시한다.
- Guide가 Web Platform → existing implementation → dependency → custom 구현의 순서를 설명하되 framework 금지 규칙으로 오해되지 않는다.
- `Tool Hub`, `QA Evidence Studio`, `external HTML workspace`를 active/default route로 복원하지 않는다.
- docs routing에서 Guide를 발견할 수 있다.
- focused test와 기존 관련 회귀 테스트가 통과한다.

## 필요한 도구·파일·권한

- 필요 항목: GitHub connector, 공식 Web/MDN 조사.
- 필요한 이유: latest main 확인, proposal/implementation PR 분리, current browser support evidence 확인.
- 설치·적용 방법: 신규 설치 없음.
- 설치 후 확인 명령: 해당 없음.
- 최소 권한: Base current-task branch/PR 정상 권한. force push/admin bypass 불필요.
- 추가 금전 비용: `0`.

## 승인과 구현

- 사용자 승인 근거: 2026-08-25 현재 작업 대화에서 본 제안의 핵심 방향(`Browser/Platform Native First + Capability Detection + Progressive Enhancement + Live Evidence Gate`, 기능 목록 복제 금지)을 설명한 뒤 사용자가 `좋아 진행해`라고 명시했다.
- 현재 단계: 사용자 의도는 승인되었지만 BCP lifecycle상 먼저 proposal-only PR을 병합하고, 그 후 동일 승인 범위만 `APPROVED_FOR_IMPLEMENTATION`으로 기록한다.
- 승인 범위: 위 `승인 시 최소 구현 범위`만 반영한다.
- 승인 제외: 신규 Skill/Tool/dependency, 퇴역 surface 부활, AGENTS root 비대화, 특정 framework 전역 금지, Experimental 기능 production 강제.
- 구현 PR: `없음`
- 롤백: 구현 Guide/routing/test만 제거하면 기존 Base 동작과 authority 구조로 완전히 복귀한다.
