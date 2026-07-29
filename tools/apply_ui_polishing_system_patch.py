from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one replacement marker, found {count}: {old!r}")
    write(path, text.replace(old, new, 1))


def replace_all(path: str, old: str, new: str, expected: int) -> None:
    text = read(path)
    if new in text and old not in text:
        return
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} markers, found {count}: {old!r}")
    write(path, text.replace(old, new))


def create_polishing_reference() -> None:
    path = "skills/auditing-and-refining-ui-art/references/ui-polishing-method.md"
    content = """# 게임 UI 폴리싱 방법

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
- 10회 이상의 반복 사용에서 효과가 조작 지연이나 피로를 만들지 않는지 확인한다.

반복 횟수는 공용 통과값이 아니라 짧은 회귀 fixture의 시작값이다. 실제 세션 빈도는 프로젝트 플레이 증거로 조정한다.

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
"""
    write(path, content)


def patch_skill() -> None:
    path = "skills/auditing-and-refining-ui-art/SKILL.md"
    replace_once(
        path,
        "description: Use when planning or reviewing game UX, UI information architecture, interaction patterns, input, accessibility, Godot UI contracts, rendered interface quality, or approved UI refinements without moving domain rules into presentation code.",
        "description: Use when planning, polishing, or reviewing game UX, UI information architecture, interaction patterns, input, accessibility, Godot UI contracts, rendered interface quality, or approved UI refinements without moving domain rules into presentation code.",
    )
    replace_once(path, "# 게임 UX/UI 설계·감사", "# 게임 UX/UI 설계·폴리싱·감사")
    replace_once(
        path,
        "플레이어 경험을 화면·정보·입력·상태·피드백·접근성·Godot 구현 계약으로 변환하고, 구현된 Godot 또는 Web UI를 실제 렌더와 증거로 감사한다.",
        "플레이어 경험을 화면·정보·입력·상태·피드백·접근성·Godot 구현 계약으로 변환하고, 준비된 UI를 증거 기반으로 폴리싱하며, 구현된 Godot 또는 Web UI를 실제 렌더와 증거로 감사한다.",
    )
    replace_once(
        path,
        "- `playtest-contract`: build·commit·해상도·입력·참가자·과제·가설·행동/설명 증거·중단/통과 기준을 고정한다.\n\n### 구현 결과 감사",
        "- `playtest-contract`: build·commit·해상도·입력·참가자·과제·가설·행동/설명 증거·중단/통과 기준을 고정한다.\n\n### 폴리싱\n\n- `polishing-pass`: 기능·정보 구조·상태 소유권이 충분히 안정된 화면에서 `P0 BLOCKER → P1 CLARITY → P2 CONSISTENCY → P3 DELIGHT` 순서로 계층·가독성·상태·피드백·모션·음향·햅틱·반복 사용·중단·재진입·성능을 마감하고 전후 증거를 만든다.\n\n### 구현 결과 감사",
    )
    replace_once(
        path,
        "- 실제 사용자 이해 가설과 플레이테스트 계약을 정의한다.",
        "- 실제 사용자 이해 가설과 플레이테스트 계약을 정의한다.\n- 기능과 정보 구조가 준비된 화면의 UI 폴리싱 우선순위·피드백 예산·반복 피로·중단·재진입·전후 증거를 정의한다.",
    )
    replace_once(
        path,
        "→ playtest-contract\n→ 필요 시 runtime-ui-audit",
        "→ playtest-contract\n→ 구현 준비도가 충족되면 polishing-pass\n→ runtime-ui-audit",
    )
    replace_once(
        path,
        "9. 자동 검사와 사람 이해 증거를 분리하고 실행하지 않은 항목은 `NOT_RUN` 또는 `UNVERIFIED`로 둔다.",
        "9. 폴리싱은 `P0 BLOCKER → P1 CLARITY → P2 CONSISTENCY → P3 DELIGHT` 순서로 진행하고, P0~P2가 남아 있으면 장식 효과를 보류한다.\n10. 자주 반복되는 행동은 낮은 피드백 강도를 사용하고 모션·음향·햅틱을 끈 동등 경로를 둔다.\n11. 빠른 반복 입력, 중복 입력, 애니메이션 중단·재진입, modal 재진입에서 결과 중복과 시각 drift를 검사한다.\n12. 자동 검사와 사람 이해 증거를 분리하고 실행하지 않은 항목은 `NOT_RUN` 또는 `UNVERIFIED`로 둔다.",
    )
    replace_once(
        path,
        "- [project-adapter-contract.md](references/project-adapter-contract.md)",
        "- [project-adapter-contract.md](references/project-adapter-contract.md)\n- [ui-polishing-method.md](references/ui-polishing-method.md)",
    )
    replace_once(
        path,
        "feedback_channels:\ninput_and_focus:",
        "feedback_channels:\npolish_readiness:\npolish_priority:\nfeedback_budget:\nrepetition_and_interruption:\nbefore_after_artifacts:\ninput_and_focus:",
    )
    replace_once(
        path,
        "- 비활성·잠금·오류 상태는 원인과 가능한 다음 행동을 제공한다.",
        "- 비활성·잠금·오류 상태는 원인과 가능한 다음 행동을 제공한다.\n- UI 폴리싱은 구조·가독성·상태·피드백을 먼저 해결하고 장식은 마지막에 적용한다.\n- 반복 사용·빠른 입력·애니메이션 중단·재진입에서 결과 중복, 누적 transform, 입력 지연과 피로를 검증한다.",
    )


def patch_design_method() -> None:
    path = "skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md"
    replace_once(
        path,
        "→ 실제 렌더\n→ 사람 이해 검증",
        "→ 구현 준비도\n→ UI 폴리싱\n→ 실제 렌더 감사\n→ 사람 이해 검증",
    )
    replace_once(
        path,
        "### 3.10 검증",
        "### 3.10 폴리싱 준비도와 실행\n\n폴리싱 전에 기능 흐름·화면 중심 질문·정보 계층·상태 소유권·주 입력 경로가 정의됐는지 확인한다. 미확정이면 장식으로 가리지 않고 해당 설계 단계로 되돌린다.\n\n```text\nP0 BLOCKER\n→ P1 CLARITY\n→ P2 CONSISTENCY\n→ 피드백 예산\n→ 모션·음향·햅틱 폴백\n→ 반복 사용·중단·재진입\n→ 성능·전후 증거\n→ P3 DELIGHT\n```\n\n상세 계약은 `ui-polishing-method.md`를 사용한다.\n\n### 3.11 검증",
    )
    replace_once(
        path,
        "7. Godot 소유권 계약\n8. 검증 매트릭스와 미검증",
        "7. Godot 소유권 계약\n8. 폴리싱 준비도·우선순위·피드백 예산·전후 증거\n9. 검증 매트릭스와 미검증",
    )


def patch_reference_library() -> None:
    path = "skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md"
    addition = """## 7. UI 폴리싱 근거 보강

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

"""
    replace_once(path, "## 7. 레퍼런스 사용 절차", addition + "## 8. 레퍼런스 사용 절차")
    replace_once(path, "## 8. 금지", "## 9. 금지")


def patch_godot_contract() -> None:
    path = "skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md"
    addition = """## 12. UI 폴리싱 구현 계약

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

"""
    replace_once(path, "## 12. 검증 매트릭스", addition + "## 13. 검증 매트릭스")
    replace_once(path, "## 13. 완료 출력", "## 14. 완료 출력")
    replace_once(
        path,
        "fallbacks:\nstatic_validation:",
        "fallbacks:\nfeedback_tiers:\nreduced_motion:\nduplicate_input_policy:\ninterruption_and_reentry:\nrepetition_and_performance:\nstatic_validation:",
    )


def patch_agent() -> None:
    path = "skills/auditing-and-refining-ui-art/agents/openai.yaml"
    write(
        path,
        """interface:\n  display_name: \"게임 UX/UI 설계·폴리싱·감사\"\n  short_description: \"게임 경험·정보 구조·접근성·Godot UI 계약을 설계하고 준비된 화면을 증거 기반으로 폴리싱한 뒤 실제 결과를 감사합니다.\"\n  default_prompt: \"Use $auditing-and-refining-ui-art to define the player experience, information flow, interaction patterns, component states, accessibility fallbacks, and Godot UI ownership contract; run the polishing-pass only after functional and information-architecture readiness; then audit rendered results. Prioritize P0 blockers, P1 clarity, and P2 consistency before P3 delight, preserve domain rules, require approval before edits, test repeated use and interruption, and separate automated checks from human evidence.\"\n""",
    )


def patch_template() -> None:
    path = "templates/planning/GAME_UX_UI_SYSTEM.md"
    for old, new in (
        ("## 16. 완료·미검증·다음 게이트", "## 17. 완료·미검증·다음 게이트"),
        ("## 15. Base 승격과 프로젝트 전용 유지", "## 16. Base 승격과 프로젝트 전용 유지"),
        ("## 14. 검증 매트릭스", "## 15. 검증 매트릭스"),
        ("## 13. 레퍼런스 판정", "## 14. 레퍼런스 판정"),
        ("## 12. Godot 구현 계약", "## 13. Godot 구현 계약"),
        ("## 11. 접근성 장벽", "## 12. 접근성 장벽"),
    ):
        replace_once(path, old, new)
    section = """## 11. UI 폴리싱 계약

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

"""
    replace_once(path, "## 12. 접근성 장벽", section + "## 12. 접근성 장벽")


def patch_checklist() -> None:
    path = "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md"
    for old, new in (
        ("## 10. 최종 판정", "## 11. 최종 판정"),
        ("## 9. 적대적 검토", "## 10. 적대적 검토"),
        ("## 8. 사람 이해 증거", "## 9. 사람 이해 증거"),
        ("## 7. 런타임 증거", "## 8. 런타임 증거"),
        ("## 6. 자동·정적 증거", "## 7. 자동·정적 증거"),
        ("## 5. Godot 구현 경계", "## 6. Godot 구현 경계"),
        ("## 4. 접근성", "## 5. 접근성"),
    ):
        replace_once(path, old, new)
    section = """## 4. UI 폴리싱 게이트

- [ ] 폴리싱 준비도에서 기능 흐름·정보 구조·상태 소유권·입력 baseline이 확인됐다.
- [ ] `P0 BLOCKER`와 `P1 CLARITY`, `P2 CONSISTENCY`가 해결되거나 명시적으로 차단되기 전 `P3 DELIGHT` 장식을 우선하지 않았다.
- [ ] 새 요소 추가 전에 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK → ADD`를 검토했다.
- [ ] routine·confirming·warning·reward·critical의 피드백 예산이 행동 중요도와 반복 빈도에 맞는다.
- [ ] 자주 반복되는 행동이 희귀 보상·위험 경고보다 강한 모션·음향·햅틱을 사용하지 않는다.
- [ ] 시각·음향·햅틱이 같은 원인과 결과를 전달하며 하나의 채널에만 의미를 의존하지 않는다.
- [ ] `reduced motion`, mute, haptic off에서도 같은 상태·결과·다음 행동이 남는다.
- [ ] 빠른 반복 입력·중복 입력에서 구매·보상·저장·전환 결과가 중복되지 않는다.
- [ ] 애니메이션 중단·즉시 완료·재진입에서 누적 transform, 포커스 손실, 입력 지연이 없다.
- [ ] modal 종료·화면 재진입 뒤 이전 의미 있는 선택과 포커스가 복구된다.
- [ ] 반복 사용에서 효과 피로·조작 지연·Signal/Tween/Timer 누적 위험을 검토했다.
- [ ] 전후 Artifact가 같은 build·상태·해상도·입력·locale·접근성 설정을 사용한다.
- [ ] 폴리싱이 미확정 코어·정보 구조·도메인 규칙 문제를 가리지 않는다.

"""
    replace_once(path, "## 5. 접근성", section + "## 5. 접근성")


def patch_registry(reviewed_commit: str) -> None:
    path = ROOT / "skills/SKILL_REGISTRY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    skill = next(
        item for item in data["skills"] if item["skill_id"] == "auditing-and-refining-ui-art"
    )
    skill["trigger_tags"] = [
        "game-ux",
        "ui-design",
        "ui-information-architecture",
        "interaction-pattern",
        "ui-polishing",
        "interaction-feedback",
        "microinteraction",
        "motion-feedback",
        "audio-haptic-feedback",
        "godot-ui",
        "web-ui",
        "runtime-ui-audit",
        "visual-refinement",
        "render-review",
    ]
    skill["use_when"] = [
        "게임 UX/UI 경험·흐름·정보 구조·패턴·상태·접근성·Godot 계약을 설계하거나, 준비된 UI를 명확성·일관성·피드백·모션·음향·햅틱·반복 사용·성능 기준으로 폴리싱하거나, 구현된 Godot·Web UI를 실제 렌더·입력·폴백 증거로 감사·재검수한다."
    ]
    skill["do_not_use_when"] = [
        "UI와 무관한 도메인 로직만 변경하거나, 실제 화면·UX 계약 없이 미감 취향만 평가하거나, 새 이미지 프롬프트·아트 자산 제작만 수행한다."
    ]
    skill["review_triggers"] = [
        "목적 있는 디자인 오탐",
        "승인 전 자동 수정",
        "전후 렌더 누락",
        "플랫폼 어댑터 누락",
        "폴리싱으로 구조 결함 은폐",
        "효과 과잉",
        "반복 피로 미검증",
        "중단·재진입 중복 결과",
        "Registry drift",
    ]
    skill["last_reviewed_at"] = "2026-07-29"
    skill["last_reviewed_commit"] = reviewed_commit
    skill["knowledge_state"] = "PATTERN"
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def patch_learning_log() -> None:
    path = "skills/SKILL_LEARNING_LOG.md"
    text = read(path)
    heading = "## 2026-07-29 — UX/UI 폴리싱 패스와 Registry 전파 교훈"
    if heading in text:
        return
    entry = f"""{heading}

- **Trigger:** UI 폴리싱 실무 방법을 외부 공식 근거와 함께 조사해 Base Skill·작업 구조에 반영하라는 요청.
- **Finding:** 2026-07-29 PR #57에서 `auditing-and-refining-ui-art`가 UX/UI 설계까지 확장됐지만 기계 권한인 `skills/SKILL_REGISTRY.json`은 구현 후 감사 중심의 이전 trigger와 설명을 유지했다. UX/UI 전용 coupled-change rule도 Registry·Learning Log 동기화를 요구하지 않아 consumer drift를 차단하지 못했다.
- **Decision:** **새 Skill을 추가하지 않음**. 기존 Skill에 `polishing-pass`를 추가하고 `ui-polishing-method.md`, 프로젝트 Template, Review Checklist, Godot 중단·재진입·반복 사용 계약을 연결한다. Skill 변경 시 Registry·Learning Log·전용 Test·CI·상위 라우터를 함께 갱신하도록 coupled-change를 강화한다.
- **Evidence:** TDD RED에서 새 Reference·Mode·Template·Registry·라우터 누락이 실제 실패했고 기존 A~E 감사 회귀는 통과했다. W3C·Xbox·Apple·Godot·Material·Nielsen 원칙은 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 사용하며 프로젝트 정본을 대체하지 않는다.
- **Boundary:** 실제 모션 시간·색·간격·폰트·사운드·햅틱, Scene·script·asset 경로, 렌더·기기·플레이어 결과는 프로젝트에 유지한다. Base 문서 반영은 런타임·사람 검증 완료가 아니다.
- **Learning state:** 공용 구조와 drift 방지 계약은 `PATTERN` 후보이며, 여러 프로젝트에서 이해 시간·오입력·반복 피로·재작업 감소를 확인하기 전 실제 효과는 `OBSERVATION`이다.
- **Next trigger:** 서로 다른 두 프로젝트 이상에서 `polishing-pass`와 전후 Artifact를 사용하고 P0~P3 finding·입력 오류·피로·성능·사람 이해 결과를 비교할 때 재검토한다.

"""
    marker = "# Base Skill Learning Log\n\n"
    if not text.startswith(marker):
        raise RuntimeError(f"{path}: unexpected header")
    write(path, marker + entry + text[len(marker) :])


def patch_reference_freshness() -> None:
    path = ROOT / ".github/reference-freshness.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rule = next(
        item
        for item in data["coupled_change_rules"]
        if item["name"] == "game-ux-ui-skill-sync"
    )
    rule["require_all_changed"] = [
        "skills/SKILL_REGISTRY.json",
        "skills/SKILL_LEARNING_LOG.md",
        "skills/README.md",
        "tests/test_game_ux_ui_system.py",
        ".github/workflows/validate-game-ux-ui-system.yml",
    ]
    rule["require_any_changed"] = [
        "skills/auditing-and-refining-ui-art/agents/openai.yaml",
        "skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md",
        "skills/auditing-and-refining-ui-art/references/game-ux-pattern-library.md",
        "skills/auditing-and-refining-ui-art/references/ui-polishing-method.md",
    ]
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def patch_workflow() -> None:
    path = " .github/workflows/validate-game-ux-ui-system.yml".strip()
    marker = '      - "skills/README.md"\n'
    addition = (
        marker
        + '      - "skills/SKILL_REGISTRY.json"\n'
        + '      - "skills/SKILL_LEARNING_LOG.md"\n'
        + '      - "AGENTS.md"\n'
        + '      - "START_HERE.md"\n'
        + '      - "docs/OPERATING_MODEL.md"\n'
        + '      - "docs/DOCUMENTATION_MAP.md"\n'
    )
    replace_all(path, marker, addition, expected=2)


def patch_routers() -> None:
    replace_once(
        "skills/README.md",
        "| `auditing-and-refining-ui-art` | 게임 UX 경험·흐름·패턴·상태·접근성·Godot UI 계약을 설계하고 구현된 Godot·Web UI를 A~E 영역으로 감사해 승인 범위만 개선·재검수함 |",
        "| `auditing-and-refining-ui-art` | 게임 UX 경험·흐름·정보 구조·패턴·상태·접근성·Godot UI 계약을 설계하고, 준비된 UI를 증거 기반으로 폴리싱하며, 구현된 Godot·Web UI를 A~E 영역으로 감사해 승인 범위만 개선·재검수함 |",
    )
    replace_once(
        "AGENTS.md",
        "| 구현된 Godot·Web UI 감사 | `auditing-and-refining-ui-art` |",
        "| 게임 UX/UI 설계·폴리싱·구현된 Godot·Web UI 감사 | `auditing-and-refining-ui-art` |",
    )
    replace_once(
        "START_HERE.md",
        "- 구현된 Godot·Web UI 결과 감사: `skills/auditing-and-refining-ui-art/SKILL.md`",
        "- 게임 UX/UI 설계·폴리싱·구현 결과 감사: `skills/auditing-and-refining-ui-art/SKILL.md`",
    )
    replace_once(
        "START_HERE.md",
        "생성 전 설계, 구현 후 시각 감사, 접근성 장벽 검수는 입력·도구·판정이 다르므로 구분한다. UI 감사는 사용자 승인 전 대상 파일을 수정하지 않으며 전후 실제 렌더로 재검수한다.",
        "생성 전 설계, 준비된 화면의 UI 폴리싱, 구현 후 시각 감사, 접근성 장벽 검수는 입력·도구·판정이 다르므로 구분한다. 폴리싱·UI 감사는 사용자 승인 전 대상 파일을 수정하지 않으며 전후 실제 렌더로 재검수한다.",
    )
    replace_once(
        "docs/OPERATING_MODEL.md",
        "| 구현된 Godot·Web UI 감사·개선 | `auditing-and-refining-ui-art` |",
        "| 게임 UX/UI 설계·폴리싱·구현된 Godot·Web UI 감사·개선 | `auditing-and-refining-ui-art` |",
    )
    replace_once(
        "docs/DOCUMENTATION_MAP.md",
        "| Godot·Web UI 아트 감사 | `auditing-and-refining-ui-art` | 실행 결과 A~E 감사·승인된 개선·전후 렌더 재검수 |",
        "| 게임 UX/UI 설계·폴리싱·Godot·Web UI 감사 | `auditing-and-refining-ui-art` | 경험·정보 구조·상태·접근성·Godot 계약 설계 / `polishing-pass` / 실행 결과 A~E 감사·승인된 개선·전후 렌더 재검수 |",
    )
    replace_once(
        "docs/DOCUMENTATION_MAP.md",
        "| 접근성·성능을 어떤 증거로 검증하는가? | `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md` | `templates/quality/PROJECT_CHANGE_VALIDATION.md` |",
        "| UI 폴리싱을 어떤 순서와 증거로 진행하는가? | `skills/auditing-and-refining-ui-art/references/ui-polishing-method.md` | `templates/planning/GAME_UX_UI_SYSTEM.md`, `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md` |\n| 접근성·성능을 어떤 증거로 검증하는가? | `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md` | `templates/quality/PROJECT_CHANGE_VALIDATION.md` |",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewed-commit", required=True)
    args = parser.parse_args()

    create_polishing_reference()
    patch_skill()
    patch_design_method()
    patch_reference_library()
    patch_godot_contract()
    patch_agent()
    patch_template()
    patch_checklist()
    patch_registry(args.reviewed_commit)
    patch_learning_log()
    patch_reference_freshness()
    patch_workflow()
    patch_routers()


if __name__ == "__main__":
    main()
