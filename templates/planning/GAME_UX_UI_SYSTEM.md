# <프로젝트명> UX/UI 시스템

> 책임: 플레이어 경험·화면 흐름·정보 구조·상호작용·상태·접근성·Godot UI 계약
> 공용 기준: Base `auditing-and-refining-ui-art`
> 상태: `DRAFT | APPROVED | IMPLEMENTED | VALIDATED | SUPERSEDED`

## 1. 프로젝트 UX 약속

## 시각 협업 Artifact

- usage_context: GDD / EXTERNAL_COLLABORATION / BOTH
- Figma Frame·Whimsical Board:
- Decision ID·GitHub 책임 원본:
- Snapshot·Source Commit·구현 제외 범위:

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
| 보조기기 사용자 | | | | HUMAN_NOT_RUN | |

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
