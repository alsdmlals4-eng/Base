# <프로젝트명> UX/UI 시스템

> 책임: 플레이어 경험·화면 흐름·정보 구조·상호작용·상태·접근성·Godot UI 계약
> 공용 기준: Base `auditing-and-refining-ui-art`
> 시각 요소 선정 기준: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`
> 상태: `DRAFT | APPROVED | IMPLEMENTED | VALIDATED | SUPERSEDED`

## 1. 프로젝트 UX 약속

## 시각 협업 Artifact

- usage_context: `NOTION_PROJECT / REPOSITORY_HANDOFF / BOTH`
- project_workspace: `NOTION_DEFAULT_PROJECT_WORKSPACE`
- Notion Project·Screen·Asset 관계:
- Decision ID·repository 책임 원본:
- 승인 Preview·Source Commit·구현 제외 범위:

시각 Artifact는 현재 Project 관계와 책임 원본을 찾기 위한 사람용 보조 표현이다. 외부 보드나 과거 링크가 남아 있어도 활성 정본으로 복구하지 않으며, 현재 의미·승인 상태·구현 사실은 Notion 관계와 repository owner에서 확인한다.

```text
<플레이어가 무엇을 보고>
→ <어떤 판단을 하고>
→ <어떤 행동을 선택하고>
→ <어떤 즉시 피드백과 장기 의미를 얻는가>
```

### 관찰 가능한 성공 기준

- <도움 없이 설명할 수 있는 것>
- <완주할 수 있는 입력 흐름>
- <오류나 실수에서 복구할 수 있는 것>

## 2. 범위

### 포함

- <화면·흐름·컴포넌트>

### 제외

- <도메인 규칙·제품 범위·후행 플랫폼>

### 보호 대상

- 프로젝트 코어:
- 상태 소유자:
- 승인 자산:
- 제품 경로:

## 3. 플랫폼·해상도·입력

| 항목 | 계약 | 검증 상태 |
|---|---|---|
| 목표 플랫폼 | | |
| 최소 해상도 | | |
| 목표 해상도 | | |
| 포인터 | | |
| 키보드 | | |
| 게임패드 | | |
| 터치 | | |
| 안전 영역 | | |
| 긴 한국어 | | |

## 3A. UI/UX·비주얼 규칙 프로필

> Base `ui-ux-visual-design-rulebook.md`의 규칙을 프로젝트에 그대로 복제하지 않는다. 규범 표준·플랫폼 권고·인지/사용성 휴리스틱·시각 스타일 휴리스틱을 구분하고, 실제 플랫폼·거리·입력·장르·아트 방향에 맞춰 판정한다.

| rule_id | source_type | tier | platform | 프로젝트 판정 | 적용/예외 사유 | 동등 경로 | 검증 증거 | 상태 |
|---|---|---|---|---|---|---|---|---|
| | normative/platform/usability_heuristic/visual_heuristic | MUST/SHOULD/STYLE_DEFAULT/TEST_REQUIRED | | ADOPT/ADAPT/AVOID/TEST/IGNORE | | | | NOT_RUN/PARTIAL/PASSED/FAILED/BLOCKED |

규칙 적용 순서:

```text
사용자 최신 지시·프로젝트 코어·보호 아트 방향
→ 의미/상태/복구/안전
→ 접근성·입력 완결성
→ 화면 중심 질문·정보 위계
→ 플랫폼 관례
→ 인지·사용성 휴리스틱
→ 시각 STYLE_DEFAULT
→ 장식
```

- `MUST` 예외는 **예외 사유**, 동등한 접근/복구 경로, 검증 증거를 남긴다.
- `SHOULD`는 장르·프로젝트 코어와 충돌하면 `ADAPT` 또는 `TEST`로 내린다.
- `STYLE_DEFAULT`는 접근성·semantic/focus/read order나 승인 아트 방향보다 높은 권한을 갖지 않는다.
- `TEST_REQUIRED`는 실제 렌더·입력·플레이 증거가 없으면 `PASSED`로 올리지 않는다.
- Web 24×24 CSS px, Apple 44×44 pt, Android 48×48 dp처럼 단위와 적용 범위를 보존한다.

## 4. 사용자 여정과 화면 중심 질문

| 단계/화면 | 진입 조건 | 중심 질문 | 첫 시선 | 핵심 행동 | 취소·복귀 | 결과·다음 행동 |
|---|---|---|---|---|---|---|
| | | | | | | |

## 5. 정보 계층

### L0 상시 필수

-

### L1 현재 선택 판단

-

### L2 결과·인과·복기

-

### L3 선택적 상세·재열람

-

## 6. 점진적 공개와 학습

```text
<상황>
→ <최소 안내>
→ <즉시 행동>
→ <피드백>
→ <다음 층 공개>
→ <재열람 위치>
```

복귀 플레이어·기존 저장 보호:

-

## 7. 공용 패턴 프로필

| Pattern ID | 판정 | 프로젝트 적용 | 적용하지 않는 조건 | 검증 |
|---|---|---|---|---|
| UXP-STATUS-VISIBILITY | | | | |
| UXP-ACTION-FEEDBACK | | | | |
| UXP-PREDICT-BEFORE-COMMIT | | | | |
| UXP-PROGRESSIVE-DISCLOSURE | | | | |
| UXP-COMPARABLE-CHOICES | | | | |
| UXP-SAFE-REVERSAL | | | | |
| UXP-ERROR-RECOVERY | | | | |
| UXP-FOCUS-NAVIGATION | | | | |
| UXP-MULTI-CHANNEL-CUES | | | | |
| UXP-RETURNING-PLAYER-MEMORY | | | | |
| UXP-CAUSAL-RECAP | | | | |
| UXP-EMPTY-LOCKED-FALLBACK | | | | |

## 8. 프로젝트 고유 패턴

```yaml
pattern_id:
problem:
player_risk:
core_flow:
states:
feedback_channels:
fallbacks:
failure_modes:
validation:
```

## 9. 컴포넌트와 상태

### Visual Requirement Gate

새 컴포넌트·아이콘·장식·이미지 슬롯을 추가하기 전에 Art Guide의 `Visual Requirement Gate`를 통과한다. UI 문서는 전역 자산 필요성 규칙을 복제하지 않고, 화면에서 실제로 소비하는 requirement의 상태·입력·정보 책임만 상세화한다.

| requirement_id | 컴포넌트/시각요소 | why_needed | delete_test | reuse_candidate | priority | disposition | 소비 화면·행동 | 검증 |
|---|---|---|---|---|---|---|---|---|
| | | | | | P0/P1/P2/P3 | REUSE/ADAPT/SOURCE/GENERATE/CREATE/DEFER/CUT | | |

- `delete_test`가 핵심 흐름·판단·접근성 손실을 설명하지 못하면 신규 UI 추가보다 `DEFER/CUT`을 우선 검토한다.
- `reuse_candidate`는 현재 Theme·Control·Container·재사용 Scene·프로젝트 컴포넌트를 먼저 확인한다.
- `priority`는 기존 `P0 BLOCKER / P1 CLARITY / P2 CONSISTENCY / P3 DELIGHT`와 동일한 언어를 사용한다.
- `disposition`이 `SOURCE_EXISTING`이면 기존 자산/플러그인 평가 경로, 이미지 `GENERATE_EXPLORATION`이면 아트 생성 경로로 넘긴다.

### 컴포넌트 계약

| 컴포넌트 | 데이터 입력 | 사용자 의도 출력 | 상태 | Theme variation | 포커스/입력 | 폴백 |
|---|---|---|---|---|---|---|
| | | | | | | |

상태 최소 검토:

```text
normal / hover / focused / pressed / selected
disabled / locked / loading / warning / error / new
```

## 10. 피드백·문구·오류 복구

| 행동/상태 | 즉시 접수 | 처리 중 | 성공 | 실패 원인 | 복구 행동 | 색·소리·모션 폴백 |
|---|---|---|---|---|---|---|
| | | | | | | |

## 11. UI 폴리싱 계약

### 폴리싱 준비도

| 항목 | 상태 | 차단 사유·다음 행동 |
|---|---|---|
| 기능 흐름 | PASS/PARTIAL/FAIL/NOT_RUN | |
| 화면 중심 질문·정보 계층 | PASS/PARTIAL/FAIL/NOT_RUN | |
| 상태 소유권 | PASS/PARTIAL/FAIL/NOT_RUN | |
| 입력·해상도 baseline | PASS/PARTIAL/FAIL/NOT_RUN | |

### P0~P3 우선순위

| 우선순위 | Finding | 영향 | 변경 | 검증 | 상태 |
|---|---|---|---|---|---|
| P0 BLOCKER | | | | | |
| P1 CLARITY | | | | | |
| P2 CONSISTENCY | | | | | |
| P3 DELIGHT | | | | | |

### 피드백 예산

| 등급 | 행동·상태 | 시각 | 음향 | 햅틱 | 반복 빈도 | 폴백 |
|---|---|---|---|---|---|---|
| routine | | | | | | |
| confirming | | | | | | |
| warning | | | | | | |
| reward | | | | | | |
| critical | | | | | | |

### 반복 사용·중단·재진입

| Fixture | 예상 결과 | 실행 결과 | 상태 | Artifact |
|---|---|---|---|---|
| 빠른 반복 입력·중복 입력 | | | NOT_RUN | |
| 애니메이션 중단·즉시 완료 | | | NOT_RUN | |
| modal 종료·재진입·포커스 복귀 | | | NOT_RUN | |
| reduced motion·mute·haptic off | | | NOT_RUN | |
| 반복 사용 피로·UI 성능 | | | NOT_RUN | |

### 전후 Artifact

| 조건 | Before | After | 관찰 변화 | 회귀 |
|---|---|---|---|---|
| 같은 build/state/resolution/input/locale | | | | |

## 12. 접근성 장벽

| 장벽 | 영향 행동 | 기본 경로 | 동등 경로 | 검증 | 상태 |
|---|---|---|---|---|---|
| 정보 | | | | | NOT_RUN |
| 입력 | | | | | NOT_RUN |
| 포커스·탐색 | | | | | NOT_RUN |
| 텍스트·인지 | | | | | NOT_RUN |
| 시간 | | | | | NOT_RUN |
| 모션 | | | | | NOT_RUN |
| 음향 | | | | | NOT_RUN |

## 13. Godot 구현 계약

### 기존 구조

- Theme/Factory:
- Layout/Container:
- UI Scene:
- 상태 소유자:
- 이벤트/Signal:
- 런타임 편집/저장:

### 경계

```text
권위 상태
→ View Data
→ UI 표시
→ 사용자 의도 Signal
→ 도메인 처리
→ 결과 상태/Event
→ UI 갱신
```

### 금지

- UI에서 피해·보상·저장·진행 재계산
- UI animation 완료를 규칙 처리 시점으로 사용
- 기존 시스템 조사 없이 새 UI 프레임워크 추가

## 14. 레퍼런스 판정

| 출처 | 확인일 | 문제 | 적용 원리 | 판정 | 변환 축 | 복제 금지 |
|---|---|---|---|---|---|---|
| | | | | ADOPT/ADAPT/AVOID/TEST/IGNORE | | |

## 15. 검증 매트릭스

| 증거 | 대상 | 방법 | 통과 기준 | 상태 | Artifact |
|---|---|---|---|---|---|
| 문서·Schema | | | | NOT_RUN | |
| 정적 UI | | | | NOT_RUN | |
| Godot parse | | | | NOT_RUN | |
| 렌더 | | | | NOT_RUN | |
| 입력·포커스 | | | | NOT_RUN | |
| 기기 | | | | NOT_RUN | |
| 사람 이해 | | | | HUMAN_NOT_RUN | |
| 보조기기 사용자 | | | | HUMAN_NOT_RUN |

## 16. Base 승격과 프로젝트 전용 유지

### Base 승격 후보

-

### 프로젝트 전용

-

## 17. 완료·미검증·다음 게이트

- 완료:
- 미검증:
- 남은 위험:
- 다음 게이트:
- 롤백:


## 선택형 프로젝트 DESIGN.md 연결

> `DESIGN.md`는 시각 토큰 정본이며 이 문서의 플레이어 경험·화면 흐름·상태·접근성·Godot 소유권을 대체하지 않는다.

| 항목 | 값 |
|---|---|
| 사용 여부 | NOT_USED / DRAFT / ACTIVE / SUPERSEDED |
| 경로 | `DESIGN.md` 또는 프로젝트가 등록한 경로 |
| 형식·버전 | `google-design-md / alpha` 또는 승인된 프로젝트 형식 |
| source commit/release | |
| 시각 토큰 범위 | 색·타이포그래피·간격·형태·깊이·컴포넌트 표현 |
| Godot Theme mapping | |
| Web token mapping | |
| 검증 상태 | NOT_RUN / PARTIAL / PASSED / FAILED / BLOCKED |

게임 규칙, 도메인 상태, 입력 결과, 보상·저장·진행은 `DESIGN.md`가 소유하지 않는다. 외부 브랜드·getdesign 계열 자료는 `reference_provenance`와 변환 축을 기록하고 고유 자산·상표 표현을 복제하지 않는다.

## UI 모션·상호작용 계약

```yaml
모션 목적:
상태 변화:
staging과 첫 시선:
입력 접수:
처리 중:
결과 위치:
중단:
즉시 완료:
빠른 반복·재진입:
Reduced Motion:
mute:
haptic-off:
도메인 상태 권위:
성능·전후 증거:
```

프로젝트별 timing·easing 값은 실제 반복 빈도와 목표 플랫폼에서 검증한다.

## 생성형 Visual 범위·독립 산출물 계약

### `VISUAL_TASK_SCOPE_FIDELITY`

bounded visual 작업은 생성 전에 아래 범위를 고정한다.

```yaml
visual_question:
target_screen:
target_state:
excluded_scope:
```

결과가 broad dashboard, unrelated screen, undeclared state 또는 새 규칙·UI로 확대되면 같은 deliverable의 완료로 세지 않는다.

### `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N개 visual 결과를 요청하면 기본값은 N개의 **independent deliverable**이다. 각 결과는 독립 검토·교체·배치 가능해야 한다. collage는 요청되거나 명시적으로 승인된 경우에만 N개와 동등하다.

### `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

판단에 중요한 경로·선택·잠금·상태가 art/background와 경쟁하면 style 전체 교체, color/intensity만 강화, 기존 identity를 유지한 독립 semantic cue 중 최소 세 방향을 비교한다. cue는 프로젝트 상황에 맞춰 color, direction, shape, text/icon, brightness/thickness, motion 등에서 고르며 특정 값은 Base 상수로 만들지 않는다.

- scope_contract: NOT_RUN | PASS | FAIL | BLOCKED
- deliverable_count_contract: NOT_RUN | PASS | FAIL | BLOCKED
- semantic_redundancy_review: NOT_RUN | PASS | FAIL | BLOCKED
- human_comprehension: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
- runtime_device_validation: NOT_RUN | PARTIAL | PASSED | FAILED | BLOCKED

문서·mock·repository test만으로 마지막 두 상태를 PASS 처리하지 않는다.
