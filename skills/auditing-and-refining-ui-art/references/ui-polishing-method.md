# 게임 UI 폴리싱 방법

## 1. 목적과 비목표

UI 폴리싱은 기능을 더하는 단계가 아니라, 이미 합의된 플레이어 경험과 UI 구조를 **더 명확하고 일관되며 만족스럽고 반복 사용에 견디게 마감하는 검증 단계**다.

폴리싱은 다음을 하지 않는다.

- 미확정 게임 코어·정보 구조·도메인 규칙을 효과로 숨기지 않는다.
- 버튼·창·애니메이션·파티클을 이유 없이 추가하지 않는다.
- 다른 제품의 외형·아이콘·문구·고유 상호작용을 복제하지 않는다.
- 자동 검사만으로 실제 플레이어 이해나 접근성 완료를 주장하지 않는다.
- 프로젝트별 시간·색·크기·간격·사운드·햅틱을 Base 영구 상수로 만들지 않는다.

## 2. 진입 조건과 중단 조건

### 진입 조건

```yaml
functional_path: PASS | PARTIAL
screen_question: DEFINED
information_hierarchy: DEFINED
state_owner: IDENTIFIED
primary_input_paths: DECLARED
minimum_and_target_resolution: DECLARED
protected_core_and_assets: DECLARED
baseline_capture: AVAILABLE | PLANNED
```

`PARTIAL`로 진입할 때는 폴리싱 대상과 미완성 기능의 경계를 분리한다.

### 중단하고 설계로 되돌리는 조건

- 한 화면의 중심 질문이 둘 이상이며 우선순위를 설명할 수 없다.
- 행동 가능 여부·비활성 이유·오류 원인이 권위 상태에서 제공되지 않는다.
- UI가 피해·보상·저장·진행 결과를 재계산한다.
- 핵심 흐름이 선언한 입력 장치에서 완주되지 않는다.
- 레이아웃 잘림·포커스 갇힘·중복 결과 같은 P0 문제가 남아 있다.
- 폴리싱이 새 기능·새 규칙·새 콘텐츠 발명을 요구한다.

## 3. 우선순위

### P0 BLOCKER

입력 불가, 포커스 갇힘, 화면 잘림, 결과 중복, 진행 차단, modal 탈출 불가, 핵심 상태 누락.

### P1 CLARITY

중심 행동·현재 상태·비활성 이유·비용·위험·오류·복구·결과 인과를 오해할 가능성.

### P2 CONSISTENCY

정보 계층, 간격, 타이포그래피, 수치 단위, 컴포넌트 상태, 문구, 입력 관습, 포커스 표현의 불일치.

### P3 DELIGHT

미세 모션, 음향, 햅틱, 파티클, 빛, 보상 연출, 장식. P0~P2가 해결되거나 명시적으로 차단된 뒤에만 진행한다.

## 4. 폴리싱 패스 순서

```text
기능·구조·상태 소유권 준비도
→ REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ P0 BLOCKER
→ P1 CLARITY
→ P2 CONSISTENCY
→ FEEDBACK 강화
→ 모션·음향·햅틱 예산
→ 접근성·폴백
→ 반복 사용·중단·재진입
→ 성능·해상도·현지화
→ 전후 증거
→ P3 DELIGHT가 여전히 필요한 경우만 ADD
```

새 장식보다 삭제·축소·통합·명료화를 먼저 검토한다. 동일 의미의 테두리·아이콘·문구·점멸을 겹쳐 중요도를 왜곡하지 않는다.

## 5. 피드백 예산

| 등급 | 사용 예 | 목표 | 과잉 위험 |
|---|---|---|---|
| `routine` | hover, 탭, 반복 선택 | 입력 가능성과 선택 위치 확인 | 반복 피로, 소음 |
| `confirming` | 구매, 장착, 확정 | 입력 접수와 실제 결과 구분 | 결과 전에 성공처럼 보임 |
| `warning` | 비용 부족, 위험, 오류 | 원인·영향·복구 행동 전달 | 흔들림·점멸만 남음 |
| `reward` | 희귀 보상, 승급, 마일스톤 | 가치와 변화 위치 전달 | 반복 보상 지연, 인플레이션 |
| `critical` | 생존 위험, 영구 손실, 접근 차단 | 즉시 인지와 안전한 대응 | 지속적 경보로 중요도 붕괴 |

- 같은 화면의 모든 요소를 최고 강도로 강조하지 않는다.
- 자주 반복되는 행동일수록 지속 시간·이동 거리·음량·햅틱 강도를 줄인다.
- 입력 접수, 처리 중, 성공, 실패는 서로 다른 상태로 남긴다.
- 보상 연출은 건너뛰거나 빠르게 완료해도 획득 위치·수치·원인이 남는다.

## 6. 계층·간격·타이포그래피·수치·문구

- 첫 시선, 중심 행동, 비용·조건, 부가 정보 순서가 크기·대비·간격으로 드러난다.
- 모든 요소를 강조하지 않고 한 화면의 주 강조와 보조 강조를 제한한다.
- 긴 한국어, 최대 수치, 음수·소수·단위, 현지화 확장 fixture를 사용한다.
- 중요한 정보는 hover·잘린 텍스트·이미지 안 글자에만 두지 않는다.
- 수치 증감은 색 외에 부호·화살표·문구·전후 값을 사용한다.
- 버튼 문구는 `확인`보다 실제 결과 행동을 말한다.

## 7. 상태·어포던스·포커스·오류 복구

- `normal / hover / focused / pressed / selected`를 같은 스타일로 합치지 않는다.
- `disabled / locked / loading / warning / error / new`는 이유·해제 조건·다음 행동을 제공한다.
- 포커스 순서는 시각 순서와 일치하며 modal 종료 뒤 이전 의미 위치로 복귀한다.
- 클릭 가능한 요소의 형태와 클릭 불가능한 장식의 형태를 구분한다.
- 입력이 거부될 때 단순 흔들림보다 원인·영향·복구를 우선 표시한다.

## 8. 모션·음향·햅틱과 동등 경로

### 모션

- 모션은 상태 변화의 원인과 방향을 설명한다.
- 장식 모션은 핵심 정보보다 먼저 시선을 빼앗지 않는다.
- `reduced motion`에서는 페이드·정적 상태·즉시 완료 등 동등 경로를 제공한다.
- AnimationPlayer·Tween 완료가 도메인 규칙 처리의 권위 시점이 아니다.

### 음향

- 입력 접수, 확인, 오류, 보상은 의미 그룹으로 재사용한다.
- 음향을 꺼도 텍스트·아이콘·상태·로그로 의미가 남는다.
- 동일 행동에 화면마다 다른 의미의 소리를 사용하지 않는다.

### 햅틱

- 시각·음향과 같은 원인·결과에 맞춰 사용한다.
- 햅틱을 유일한 정보 채널로 사용하지 않는다.
- 반복 UI 행동에 과도하게 사용하지 않고 끄기 경로를 제공한다.

## 9. 반복 사용·중단·재진입

필수 fixture:

```yaml
rapid_repeat:
duplicate_input:
animation_interruption:
instant_complete:
modal_reentry:
input_device_switch:
long_session_repetition:
```

검증한다.

- 빠른 연타가 구매·보상·저장·전환 결과를 중복 생성하지 않는다.
- 진행 중 애니메이션을 다시 실행할 때 누적 scale·alpha·position drift가 없다.
- 화면을 닫고 다시 열면 선택·포커스·상태가 유효한 위치에서 복구된다.
- 모션 즉시 완료에서도 입력 가능 시점과 결과 표시가 일치한다.
- 프로젝트가 정한 짧은 회귀 fixture와 실제 세션 반복 빈도에서 효과가 조작 지연이나 피로를 만들지 않는지 확인한다.

반복 횟수는 공용 통과값으로 고정하지 않는다. 화면의 실제 사용 빈도·세션 길이·플랫폼 입력 방식에 따라 프로젝트 플레이 증거로 정한다.

## 10. 해상도·현지화·폴백·성능

- 최소·목표 해상도, 선언된 화면 비율, safe area를 같은 상태 fixture로 비교한다.
- 이미지·폰트·아이콘·사운드 누락 시 텍스트·도형·기본 아이콘으로 핵심 기능을 유지한다.
- 파티클·blur·shader·동적 그림자·대형 Texture·빈번한 Theme override의 비용을 목표 플랫폼에서 측정한다.
- 평균 FPS만 보지 않고 UI 전환 frame time, allocation, draw call, memory spike 후보를 기록한다.
- 성능 환경이 없으면 `NOT_RUN` 또는 `UNVERIFIED`로 둔다.

## 11. 전후 증거

전후 비교는 같은 조건을 사용한다.

```yaml
build_or_commit:
screen_and_state:
resolution:
input_device:
locale_and_text_fixture:
accessibility_settings:
before_artifact:
after_artifact:
observed_change:
regression_check:
human_evidence: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
```

이미지 한 장만으로 입력 완결성·피로·성능·사람 이해를 통과 처리하지 않는다.

## 12. 실패 조건과 완료 판정

### 실패 조건

- P0~P2보다 P3 장식을 먼저 적용한다.
- 모든 요소에 확대·흔들림·점멸·사운드·햅틱을 추가한다.
- 효과가 결과보다 오래 입력을 막는다.
- 색·소리·모션·햅틱 하나가 유일한 정보 채널이다.
- 애니메이션 중단·빠른 반복 입력에서 도메인 결과가 중복된다.
- 전후 조건이 달라 개선을 비교할 수 없다.
- 자동 테스트를 사람 검증으로 보고한다.

### 완료 출력

```yaml
polish_scope:
readiness:
priority_findings:
  p0_blocker:
  p1_clarity:
  p2_consistency:
  p3_delight:
feedback_mapping:
motion_and_audio:
  reduced_motion:
  mute_fallback:
  haptic_off_fallback:
repetition_and_interruption:
performance_risk:
before_after_artifacts:
human_evidence: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
result: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED
remaining_risks:
```
