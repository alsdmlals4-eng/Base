# UI 폴리싱 시스템 설계

## 1. 목표

기존 `auditing-and-refining-ui-art`를 새 Skill로 분리하지 않고 확장하여, 기능과 UX 구조가 안정된 UI를 **명확성·조작감·일관성·접근성·반복 사용 내구성·성능을 보존한 채 마감하는 공용 폴리싱 계약**을 추가한다.

폴리싱 완료는 “더 예뻐졌다”가 아니라 다음 증거로 판정한다.

- 플레이어가 중심 행동·상태·결과·복구 경로를 더 빠르고 정확하게 이해한다.
- 포인터·키보드·게임패드·터치 중 프로젝트가 선언한 입력 경로가 유지된다.
- 모션·음향·햅틱을 끄거나 줄여도 같은 의미와 게임 결과가 보존된다.
- 반복 사용에서 지연·피로·중복 입력·효과 과잉이 증가하지 않는다.
- 최소·목표 해상도와 긴 한국어·최대 수치·비정상 fixture에서 회귀가 없다.
- 전후 렌더·입력·성능·사람 이해 증거와 미검증 범위가 분리된다.

## 2. 현행 구조 분석

### 2.1 보존할 현행 책임

- `skills/auditing-and-refining-ui-art/SKILL.md`는 UX/UI 설계와 구현 결과 감사를 함께 책임한다.
- 공용 방법은 `references/`, 프로젝트 적용 형식은 `templates/`, 계약 회귀는 `tests/test_game_ux_ui_system.py`, 전용 실행은 `validate-game-ux-ui-system.yml`이 책임진다.
- 프로젝트는 Base Skill 본문을 복제하지 않고 `project-adapter-contract.md`로 공용 원리와 프로젝트 고유 값·경로·자산·실제 결과를 분리한다.
- UI는 도메인 상태·피해·보상·저장·진행을 재계산하지 않고 View Data와 사용자 의도 사이의 경계로 유지한다.

### 2.2 확인된 공백

1. 기존 설계 모드와 런타임 감사 모드 사이에 폴리싱 전용 실행 단계가 없다.
2. 상태·피드백 항목은 있으나 효과 우선순위, 모션·음향·햅틱 강도, 반복 피로, 중단·재진입, 성능 예산을 한 번에 다루는 마감 절차가 없다.
3. 프로젝트 UX/UI Template·Reference Card·Review Checklist에 폴리싱 준비도·전후 증거·반복 사용 검증 필드가 없다.
4. `skills/SKILL_REGISTRY.json`의 `auditing-and-refining-ui-art` 항목이 2026-07-29 병합된 설계 기능을 반영하지 못해 자동 라우팅이 구현 후 UI 감사에만 치우쳐 있다.
5. `.github/reference-freshness.json`의 UX/UI 전용 coupled change rule이 Skill Registry와 Learning Log 동기화를 요구하지 않아 위 drift를 차단하지 못한다.
6. 상위 라우터 일부가 여전히 이 Skill을 “구현된 UI 감사”로만 설명한다.

## 3. 외부 근거의 채택 원칙

외부 지침은 요구사항이나 구현 사실의 정본으로 사용하지 않는다. 현재 플레이어 문제와 플랫폼이 일치하는 원리만 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정한다.

### ADOPT

- 중요한 상태와 입력 접수는 즉시 보이고, 성공·실패·복구 행동을 구분한다.
- 포커스는 명확하고 예측 가능하며 modal 종료 뒤 의미 있는 위치로 복귀한다.
- 중요한 의미는 색·소리·모션·햅틱 하나에만 의존하지 않는다.
- 모션·햅틱은 선택적으로 줄이거나 끌 수 있고 게임 결과를 소유하지 않는다.
- 파괴적 행동은 실행 전 결과를 검토하거나 실행 후 되돌릴 수 있다.
- Theme·Control·Container·명시적 focus를 기존 Godot 구조 안에서 사용한다.

### ADAPT

- WCAG·Xbox·Apple·Material의 수치와 플랫폼 관습은 PC·Android·게임패드·Godot 화면 거리와 입력 방식에 맞게 검증한다.
- 업무용 제품의 효율성 원리는 장르적 긴장·미스터리·발견을 제거하지 않는 범위에서 사용한다.
- 모션 시간·크기·간격·대비 수치는 공용 영구값이 아니라 프로젝트 시작값 또는 검증 기준으로 둔다.

### AVOID

- 다른 제품의 시각 언어·아이콘·고유 상호작용을 복제한다.
- 효과를 추가해 정보 구조·비활성 원인·오류 복구 문제를 가린다.
- 자동 검사나 전문가 리뷰만으로 사람 이해·실기기·장애 사용자 검증 완료를 주장한다.

### 주요 공식 원문

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Xbox Accessibility Guidelines: https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
- Apple Human Interface Guidelines Feedback: https://developer.apple.com/design/human-interface-guidelines/feedback
- Apple Human Interface Guidelines Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- Apple Human Interface Guidelines Playing Haptics: https://developer.apple.com/design/human-interface-guidelines/playing-haptics
- Godot UI: https://docs.godotengine.org/en/stable/tutorials/ui/index.html
- Godot GUI Navigation: https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html
- Material Interaction States: https://m3.material.io/foundations/interaction/states/overview
- Nielsen Norman Group Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/

## 4. 선택한 구조

### 4.1 새 Skill을 만들지 않는다

폴리싱은 UX/UI의 별도 책임 영역이 아니라 설계 계약을 실제 화면에서 마감하는 단계다. 새 Skill ID는 자동 라우팅과 프로젝트 어댑터를 중복시키므로 기존 Skill에 `polishing-pass` Mode를 추가한다.

### 4.2 새 공용 Reference

`skills/auditing-and-refining-ui-art/references/ui-polishing-method.md`를 추가한다. 이 문서는 다음만 책임진다.

- 폴리싱 진입 조건과 중단 조건
- 문제 우선순위와 효과 예산
- 마감 패스 순서
- 모션·음향·햅틱·텍스트·숫자·상태·포커스의 동기화
- 반복 사용·중단·재진입·입력 연타·성능 검증
- 전후 증거와 사람 이해 상태

일반 UX 설계, 공용 패턴 정의, Godot 상태 소유권, 프로젝트별 값은 기존 문서가 계속 책임진다.

### 4.3 폴리싱 실행 순서

```text
기능·구조·상태 소유권 준비도 확인
→ P0 조작 차단 제거
→ P1 중심 행동·상태·오류·복구 명료화
→ P2 계층·간격·타이포그래피·수치·일관성 정리
→ 입력 접수·처리·성공·실패 피드백 정렬
→ 모션·음향·햅틱을 의미와 중요도에 맞게 예산화
→ reduced motion·mute·haptic off·자산 누락 폴백 확인
→ 반복 사용·빠른 입력·중단·재진입·성능 검사
→ 최소·목표 해상도 전후 렌더 비교
→ 사람 이해 또는 HUMAN_NOT_RUN 판정
→ 장식 효과는 남은 의미가 있을 때만 추가
```

### 4.4 우선순위

- `P0 BLOCKER`: 입력 불가, 포커스 갇힘, 정보 잘림, 결과 중복, 진행 차단.
- `P1 CLARITY`: 중심 행동·상태·비활성 이유·오류·복구·결과 인과 오해.
- `P2 CONSISTENCY`: 계층·간격·타이포그래피·컴포넌트 상태·문구·입력 관습 불일치.
- `P3 DELIGHT`: 미세 모션·음향·햅틱·파티클·빛·장식. P0~P2 미해결 상태에서는 보류한다.

### 4.5 피드백 예산

각 행동은 하나의 의미 등급을 가진다.

- `routine`: hover·탭 전환·반복 선택. 짧고 방해하지 않는 피드백.
- `confirming`: 구매·장착·결정 확정. 입력 접수와 결과를 구분하는 피드백.
- `warning`: 비용 부족·위험·오류. 원인과 복구 행동을 우선한다.
- `reward`: 희귀 보상·승급·마일스톤. 반복 빈도와 건너뛰기 가능성을 검증한다.
- `critical`: 생존·영구 손실·접근 차단. 다중 채널과 충분한 지속 시간을 사용한다.

같은 화면에서 모든 요소를 최고 강도로 강조하지 않는다. 자주 반복되는 행동일수록 효과 강도와 지속 시간을 줄인다.

## 5. 파일별 책임

### 생성

- `references/ui-polishing-method.md`: 폴리싱 방법의 단일 상세 원본.
- `docs/superpowers/specs/2026-07-29-ui-polishing-system-design.md`: 설계 결정과 범위.
- `docs/superpowers/plans/2026-07-29-ui-polishing-system.md`: 구현·검증 순서.

### 수정

- `SKILL.md`: `polishing-pass` Mode, 실행 순서, 출력 계약, 품질 Gate 연결.
- `ux-ui-design-system-method.md`: 설계→폴리싱→감사 흐름과 진입 조건 연결.
- `ux-ui-reference-library.md`: 공식 피드백·모션·햅틱·오류·포커스 근거와 채택 판정 보강.
- `godot-ui-implementation-contract.md`: semantic polish token, Tween 중단·재진입, reduced motion, 반복 성능 계약.
- `agents/openai.yaml`: 설계·폴리싱·감사의 전체 역할 반영.
- `GAME_UX_UI_SYSTEM.md`: 폴리싱 준비도·예산·전후 Artifact·반복 검증 Section 추가.
- `UX_UI_REFERENCE_CARD.md`: 외부 근거별 P0~P3·피드백 등급·반복 빈도·동등 경로·전후 검증 필드 추가.
- `GAME_UX_UI_REVIEW_CHECKLIST.md`: P0~P3·효과 강도·반복 피로·중단·재진입·폴백·전후 증거 검사 추가.
- `SKILL_REGISTRY.json`: 설계·폴리싱 trigger와 실제 use_when·review trigger 갱신.
- `SKILL_LEARNING_LOG.md`: 중복 Skill을 만들지 않은 이유와 Registry coupled-rule 누락 교훈 기록.
- `.github/reference-freshness.json`: 기존 기획 Template·Reference Card·Review Checklist 소비자를 보존하면서 Registry·Learning Log·README·Test·CI 동기화를 추가로 강제.
- `.github/workflows/validate-game-ux-ui-system.yml`: Registry·Learning Log·상위 라우터 변경도 전용 검증을 실행하도록 paths 확장.
- `tests/test_game_ux_ui_system.py`: 폴리싱 계약과 전체 소비처 동기화 회귀 테스트.
- `skills/README.md`, `AGENTS.md`, `START_HERE.md`, `docs/OPERATING_MODEL.md`, `docs/DOCUMENTATION_MAP.md`: 설계·폴리싱·감사 전체 역할을 한 줄 라우터에 반영.

## 6. 출력 계약

```yaml
polish_scope:
readiness:
  functional: PASS | PARTIAL | FAIL | NOT_RUN
  information_architecture: PASS | PARTIAL | FAIL | NOT_RUN
  state_ownership: PASS | PARTIAL | FAIL | NOT_RUN
priority_findings:
  p0_blocker:
  p1_clarity:
  p2_consistency:
  p3_delight:
feedback_mapping:
  routine:
  confirming:
  warning:
  reward:
  critical:
motion_and_audio:
  reduced_motion:
  mute_fallback:
  haptic_off_fallback:
repetition_and_interruption:
  rapid_repeat:
  duplicate_input:
  animation_interruption:
  modal_reentry:
performance_risk:
before_after_artifacts:
human_evidence: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
result: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED
remaining_risks:
```

## 7. 검증 전략

### 자동·정적

- 새 Reference와 Mode, Planning Template, Reference Card, Review Checklist, Registry trigger가 존재한다.
- UX/UI Skill 변경 시 기존 Template·Reference Card·Checklist와 Registry·Learning Log·README·전용 테스트·CI가 coupled change로 요구된다.
- 상위 라우터가 Skill을 구현 후 감사로만 축소 설명하지 않는다.
- 기존 12개 UX 패턴, A~E UI 감사, 사용자 승인 전 수정 금지, 도메인 상태 경계가 보존된다.

### 런타임·사람

Base 자체는 프로젝트 UI를 실행하지 않으므로 공용 계약 반영만 검증한다. 실제 프로젝트에서 다음을 검증하기 전 결과는 `NOT_RUN` 또는 `HUMAN_NOT_RUN`이다.

- 최소·목표 해상도와 입력 장치
- 정상·비활성·잠금·로딩·오류·누락 자산 fixture
- reduced motion·mute·haptic off
- 빠른 반복 입력과 애니메이션 중단·재진입
- 전후 렌더와 프레임·메모리 위험
- 플레이어의 중심 행동·상태·실패 원인·결과 인과 설명

## 8. 공용 승격과 프로젝트 전용 경계

### Base에 유지

- 폴리싱 진입·중단 기준
- P0~P3 우선순위
- 피드백 의미 등급과 다중 채널·폴백 원칙
- 반복 사용·중단·재진입·성능·전후 증거 검증 방법
- Godot UI의 공용 상태 소유·Theme·Signal·focus 경계

### 프로젝트에 유지

- 실제 애니메이션 시간·스케일·색·간격·폰트·사운드·햅틱 값
- 캐릭터·세계관·자원·버튼 문구·화면 이름
- 실제 Scene·script·data·asset 경로
- 승인 캡처·기기·빌드·플레이어 결과
- 프로젝트 고유 화면 효과와 브랜드 표현

## 9. 비목표

- 새 공용 Skill ID 추가
- HTML 기획 대시보드 복원
- 게임 코드·Scene·데이터·자산 수정
- 모든 프로젝트에 동일한 시간·크기·대비·반복 횟수 강제
- 폴리싱으로 미확정 코어·정보 구조·도메인 규칙 문제를 은폐
- Base 문서 변경을 프로젝트 구현 또는 사람 검증 완료로 표시
