# 게임 UX/UI 디자인 시스템 방법

For visual-workspace selection, pinning, and Godot comparison, follow `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`; Figma is a screen contract, not an implementation verdict.

## 1. 목적

화면을 예쁘게 만드는 작업과 플레이어가 게임을 이해하고 선택하는 구조를 분리하지 않는다. UX/UI 작업은 다음 순서로 진행한다.

```text
플레이어 가치
→ 화면별 중심 질문
→ 정보 계층
→ 상호작용과 상태
→ 접근성·폴백
→ Godot 구현 계약
→ 구현 준비도
→ UI 폴리싱
→ 실제 렌더 감사
→ 사람 이해 검증
```

## 2. 시작 입력

```yaml
project_core:
player_promise:
target_platform:
minimum_and_target_resolution:
input_devices:
session_context:
current_canonical_docs:
actual_ui_files:
protected_rules_and_assets:
known_player_risks:
validation_environment:
```

정본·실제 화면·검증 환경을 읽지 못했으면 추정으로 구현 완료를 주장하지 않는다.

## 3. 설계 순서

### 3.1 경험 계약

기능명이 아니라 플레이어가 느끼고 판단하고 행동하는 단위를 쓴다.

```text
상황
→ 플레이어가 알아차릴 변화
→ 해야 할 판단
→ 선택 가능한 행동
→ 즉시 피드백
→ 장기 의미
```

완료 기준은 “버튼이 있다”가 아니라 “플레이어가 도움 없이 올바른 다음 행동과 이유를 설명한다”처럼 관찰 가능하게 작성한다.

### 3.2 화면 중심 질문

각 화면에 다음을 하나씩 둔다.

- 플레이어는 지금 무엇을 결정하는가.
- 첫 시선은 어디로 가야 하는가.
- 가장 중요한 행동은 무엇인가.
- 이 화면을 벗어나는 정상·취소·실패 경로는 무엇인가.

중심 질문이 둘 이상이면 화면을 분리하거나 점진 공개한다.

### 3.3 정보 계층

```text
L0: 즉시 생존·진행에 필요한 상시 정보
L1: 현재 선택을 판단하는 비교 정보
L2: 결과 원인과 복기 정보
L3: 선택적 상세·용어집·과거 기록
```

모든 정보를 HUD에 상시 노출하지 않는다. 반대로 현재 행동 가능 여부와 실패 원인은 상세창 안에 숨기지 않는다.

### 3.4 삭제·축소 우선

새 요소를 추가하기 전에 다음 순서로 검토한다.

```text
REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ FEEDBACK 강화
→ ADD
```

동일 의미의 아이콘·텍스트·배지를 중복 추가하지 않는다. 다중 채널은 같은 의미를 동등하게 전달하는 용도이며 장식 중복과 다르다.

### 3.4a Design Read와 시각 의도

토큰이나 스타일 이름을 고르기 전에 화면의 `design intent`와 플레이어가 받아야 할 인상을 짧은 prose로 고정한다. `modern / clean / premium` 같은 범용 형용사만 나열하지 않고 프로젝트 맥락에 맞는 `specific reference`와 **왜 그 참조가 맞는지**를 함께 적는다. 특정 제품·브랜드·창작자의 화면 표현을 복제하지 않고 역할·제약·차별화 축만 변환한다.

```yaml
Design Read:
  design_intent:
  specific_reference:
  reference_reason:
  visual_variance: 1-10
  motion_intensity: 1-10
  information_density: 1-10
  intentional_do: []
  intentional_dont: []
```

- `visual variance`, `motion intensity`, `information density`는 후보를 비교하고 의도를 전달하는 설계 축이지 Base 공용 고정 수치가 아니다.
- 토큰·Schema·lint·diff는 구조와 일관성의 증거일 뿐 실제 렌더 품질, 플레이어 이해, 브랜드 적합성의 자동 PASS가 아니다.
- 최소 폭·긴 한국어·브라우저 zoom·text scaling·사용자 spacing override에서도 `essential text`는 의미를 잃게 잘리거나 가려지지 않고 reflow되어야 한다.
- badge·chip·count의 의미는 색 하나에만 의존하지 않는다. 빠른 반복 입력이나 animation cancel 뒤에도 최종 `semantic state`, focus, content가 서로 일치해야 한다.
- Do/Don't는 프로젝트 의도를 지키는 짧고 검증 가능한 제약으로 유지한다. 금지 목록이 늘어나면 vague intent를 보완하는 대신 더 구체적인 reference와 이유로 다시 정리한다.

### 3.5 패턴 선택

`game-ux-pattern-library.md`에서 문제와 플레이어 위험이 일치하는 패턴만 읽는다. 패턴은 다음 중 하나로 판정한다.

- `ADOPT`: 문제와 플랫폼이 거의 같아 구조를 채택한다.
- `ADAPT`: 핵심 원리는 채택하되 프로젝트 코어·입력·장르에 맞게 변환한다.
- `AVOID`: 플레이어 경험이나 코어를 해치므로 적용하지 않는다.
- `TEST`: 장점이 있으나 실제 플레이 증거가 필요하다.
- `IGNORE`: 현재 문제와 무관하다.

### 3.6 상태와 피드백

필요한 상태만 선언한다.

```text
normal / hover / focused / pressed / selected
available / disabled / locked
loading / success / warning / error
new / updated / resolved
```

각 상태는 다음을 답한다.

- 무엇이 달라졌는가.
- 왜 달라졌는가.
- 지금 가능한 행동은 무엇인가.
- 상태가 언제 해제되는가.
- 색·소리·모션이 없어도 의미가 남는가.

### 3.7 입력과 복구

- 입력 접수 여부를 즉시 보여 준다.
- 반복 행동과 파괴적 행동의 확인 강도를 구분한다.
- 되돌릴 수 있으면 확인창보다 실행 취소를 우선 검토한다.
- 취소·뒤로·팝업 종료 뒤 의미 있는 위치로 복귀한다.
- 입력 장치가 바뀌어도 현재 맥락과 선택이 사라지지 않게 한다.

### 3.8 접근성 게이트

정보·입력·탐색·시간·텍스트·인지·모션·음향 장벽을 각각 검토한다. 기술적으로 노출됐다는 사실과 실제 사용 가능성을 분리한다.

```yaml
barrier:
affected_player_action:
primary_path:
equivalent_path:
validation_method:
status: NOT_RUN | PARTIAL | PASSED | FAILED | BLOCKED
```

### 3.9 Godot 계약

`godot-ui-implementation-contract.md`를 사용한다. UI는 도메인 상태를 계산하지 않고 표시 데이터와 사용자 의도 사이의 경계로 유지한다.

### 3.10 폴리싱 준비도와 실행

폴리싱 전에 기능 흐름·화면 중심 질문·정보 계층·상태 소유권·주 입력 경로가 정의됐는지 확인한다. 미확정이면 장식으로 가리지 않고 해당 설계 단계로 되돌린다.

```text
P0 BLOCKER
→ P1 CLARITY
→ P2 CONSISTENCY
→ 피드백 예산
→ 모션·음향·햅틱 폴백
→ 반복 사용·중단·재진입
→ 성능·전후 증거
→ P3 DELIGHT
```

상세 계약은 `ui-polishing-method.md`를 사용한다.

### 3.11 검증

| 증거 | 증명하는 것 | 증명하지 못하는 것 |
|---|---|---|
| Markdown·Schema 검사 | 구조·필수 항목 | 화면 가독성 |
| 정적 UI 스캔 | 위험 후보 | 결함 확정 |
| Godot 파싱 | 리소스·문법 | 실제 플레이 이해 |
| 렌더 캡처 | 배치·잘림·상태 | 입력 완결성 |
| 입력 스모크 | 포커스·경로 | 장기 학습 |
| 사람 플레이 | 이해·판단·복구 | 전체 사용자 대표성 |
| 보조기기 사용자 검증 | 특정 실제 접근 경로 | 모든 접근성 준수 |

## 4. 산출물 최소 단위

작은 작업은 새 문서를 만들지 않고 현행 UX/UI 책임 원본의 한 Section으로 갱신한다. 큰 시스템은 `templates/planning/GAME_UX_UI_SYSTEM.md`를 프로젝트 구조에 맞게 적용한다.

필수 산출물:

1. 플레이어 경험과 중심 질문
2. 사용자 여정·화면 흐름
3. 정보 계층
4. 적용 패턴과 기각 패턴
5. 상태·피드백·입력 계약
6. 접근성 장벽·폴백
7. Godot 소유권 계약
8. 폴리싱 준비도·우선순위·피드백 예산·전후 증거
9. 검증 매트릭스와 미검증

## 5. 실패 조건

- 기능 목록을 UX 설계로 대체한다.
- 외부 레퍼런스 화면을 프로젝트에 복제한다.
- UI가 규칙·저장·보상을 재계산한다.
- 색·소리·모션 하나만으로 중요한 상태를 전달한다.
- 비활성 이유와 복구 경로가 없다.
- 화면마다 다른 확인·취소 의미를 사용한다.
- 자동 테스트만으로 사람 이해를 통과 처리한다.
- 최소 해상도·긴 한국어·입력 장치를 선언하지 않는다.
- 기존 프로젝트 Theme·레이아웃·편집 시스템을 조사하지 않고 새 프레임워크를 추가한다.

## 3.12 UI 모션·상호작용

모션이 상태 변화·입력 접수·공간 관계·결과 위치를 설명해야 하는 경우 `ui-motion-and-interaction-principles.md`를 사용한다. 모션 목적, 중단, 즉시 완료, 빠른 반복, 재진입, Reduced Motion, mute, haptic-off, 성능과 도메인 상태 권위를 검증한다. 프로젝트별 timing·easing 값은 실제 입력 빈도와 목표 플랫폼 증거로 정하며 Base 상수로 고정하지 않는다.

## 6. BCP-008 시각 토큰·외부 조달 확장

프로젝트 시각 토큰을 별도 파일로 기계 판독해야 할 때만 아래 `6.1` 계약과 `templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md`를 사용한다. 외부 Web UI 코드·Registry·MCP를 검토할 때는 아래 `6.2` 계약을 사용한다.

두 확장은 선택 사항이며 기존 `GAME_UX_UI_SYSTEM`의 경험·행동·상태·접근성 권위를 대체하지 않는다. 소스 조회, 코드 채택, 설치, 실제 렌더 품질은 각각 독립 Gate로 판정한다.

### 6.1 Project DESIGN.md Adapter

## 목적

프로젝트의 색·타이포그래피·간격·형태·깊이·컴포넌트 표현을 AI와 도구가 읽을 수 있는 시각 토큰 정본으로 관리한다. `GAME_UX_UI_SYSTEM`은 플레이어 경험·화면 흐름·정보 계층·상태·입력·접근성·Godot 소유권의 상위 행동 정본으로 유지한다.

YAML token은 반복 가능한 값을 고정하지만 시각 언어의 목적과 적용 이유를 대신하지 않는다. `DESIGN.md`의 Markdown prose에는 위 `Design Read`의 의도·구체 참조 이유·의도적 예외를 남기고, token 값만으로 실제 디자인 품질을 판정하지 않는다.

## 적용 조건

- 여러 화면·구현자·도구에서 반복되는 시각 토큰이 있다.
- Godot Theme 또는 Web CSS/token으로 변환할 명시적 값이 필요하다.
- 외부 브랜드·getdesign 계열 참고를 프로젝트 고유 원칙으로 변환해 출처와 차이를 기록해야 한다.

작은 단일 화면이나 시각 방향이 아직 미확정이면 새 `DESIGN.md`를 만들지 않는다.

## 권한 경계

`DESIGN.md`가 소유:
- 색, typography, spacing, radius, border, elevation
- 컴포넌트의 시각적 variant와 Do/Don't
- Godot `Theme`·`StyleBox`·Font·Color·Constant mapping
- Web CSS variable·DTCG·Tailwind mapping

`GAME_UX_UI_SYSTEM`이 소유:
- 플레이어 경험, 화면 질문, journey, information hierarchy
- 상태 의미·도메인 소유권·입력 결과
- 접근성 행동·복구·오류·피드백 계약

게임 규칙·보상·저장·진행은 어느 시각 토큰 파일도 소유하지 않는다.

## 형식·버전 고정

```yaml
format: google-design-md | project-design-md
format_version: alpha | <approved-version>
source_commit_or_release:
last_verified_at:
canonical_scope: visual-language-only
```

외부 형식이 alpha이면 자동 갱신하지 않고 exact source identity를 고정한다. 형식 변경은 diff·migration·rollback을 거친다.

## 플랫폼 mapping

### Godot
- token을 `Theme`, `StyleBox`, Font, Color, Constant와 재사용 Scene에 매핑한다.
- CSS·React 컴포넌트를 Godot 구현으로 간주하지 않는다.
- Theme 적용 뒤 실제 최소/목표 해상도와 입력 장치에서 렌더한다.

### Web
- token을 CSS custom property·DTCG·Tailwind config 중 승인된 형식에 매핑한다.
- 외부 UI 코드는 아래 `6.2 External UI Procurement and Anti-Generic Quality Gate`를 별도로 통과한다.

## 검증

- 토큰 ID 중복·순환 참조·누락 mapping
- 긴 한국어·최소 해상도·색 대비·포커스·Reduced Motion
- 같은 상태가 Godot Theme와 Web CSS에서 다른 의미가 되지 않는지
- 실제 렌더 전후와 프로젝트 고유 방향

자동 lint는 사람 이해·브랜드 적합성·접근성 준수를 자동 증명하지 않는다.

### 6.2 External UI Procurement and Anti-Generic Quality Gate

## 목적

shadcn/ui Registry·MCP 등 외부 UI 코드와 디자인 참고 자료를 프로젝트에 넣기 전에 출처·공급망·플랫폼 적합성·실제 품질을 분리해 판정한다.

## Gate 분리

```text
1. Source acquisition
2. Code admission
3. Installation approval
4. Runtime·accessibility validation
5. Actual render anti-generic review
```

`MCP 연결 성공`은 검색 통로가 열렸다는 뜻일 뿐 `설치 승인`, 코드 안전, 접근성, 실제 렌더 품질 통과가 아니다.

## Procurement receipt

```yaml
registry_source:
exact_version_or_commit:
registry_item:
source_paths: []
content_hash:
license:
dependencies: []
registry_dependencies: []
scripts: []
secrets: []
files_added_or_replaced: []
existing_system_overlap: []
security_review:
accessibility_review:
runtime_review:
actual_render:
rollback:
decision: ADOPT | ADAPT | REJECT | BLOCKED_UNVERIFIED
reason_codes: []
```

다음 중 하나라도 확인되지 않으면 fail closed한다.

- exact source identity와 content hash
- license와 프로젝트 배포 조건
- declared dependency와 실제 import·생성 결과
- install script·postinstall·network·secret 요구
- 기존 파일 덮어쓰기·상태 소유권·rollback

문서·Registry·source 간 의존성 선언이 다르면 즉시 결함으로 단정하지 않고 CLI 변환·생성 결과를 확인할 때까지 `BLOCKED_UNVERIFIED`로 둔다.

## 플랫폼 판정

### Web

프로젝트가 React·Web 표면이고 기존 디자인 시스템과 충돌하지 않으면 `ADOPT` 또는 `ADAPT` 후보가 될 수 있다. 소스 소유형 배포라도 upstream provenance와 update 책임은 남는다.

### Godot

React·CSS·Tailwind 컴포넌트는 Godot `Control`·`Theme`·Scene 구현이 아니다. Web 관리 도구가 별도 범위로 승인되지 않은 한 Godot 프로젝트에 기본 설치하지 않고 `REJECT` 또는 `BLOCKED_UNVERIFIED`로 판정한다.

## Anti-generic quality

설치 뒤 다음을 실제 렌더에서 검토한다.

```yaml
Design Read:
page_or_screen_kind:
audience:
project_vibe:
visual_variance:
motion_intensity:
information_density:
repeated_default_patterns: []
intentional_exceptions: []
actual_render:
before_after:
```

- 흔한 AI 기본값을 후보로 찾되 gradient, card, glass, serif 등 표현을 무조건 금지하지 않는다.
- 계층·가독성·상태·입력·복구·접근성을 장식보다 먼저 해결한다.
- 프로젝트의 DESIGN.md·GAME_UX_UI_SYSTEM·실제 목적에 맞는 의도적 표현은 보존한다.
- 실제 렌더 없이 “AI 티가 제거됐다”고 주장하지 않는다.

## 판정

- `ADOPT`: source·license·dependency·overwrite·runtime·accessibility·render가 검증됐고 최소 수정으로 적합하다.
- `ADAPT`: 원리는 적합하지만 프로젝트 token·상태·입력·플랫폼에 맞는 변환이 필요하다.
- `REJECT`: 플랫폼·코어·보안·라이선스·상태 소유권과 충돌한다.
- `BLOCKED_UNVERIFIED`: 필요한 source·CLI 변환·build·runtime·접근성·렌더 증거가 없다.

## 적대적 검토

- “공식 Registry”라는 이유로 코드를 무검토 설치했는가.
- source 조회 성공을 설치·빌드·품질 성공으로 승격했는가.
- dependency 선언과 실제 import·lockfile이 일치하는가.
- MCP 또는 설치 도구가 secret·network·shell·overwrite 범위를 넓혔는가.
- 외부 컴포넌트가 도메인 상태를 소유하거나 기존 시스템을 이중화하는가.
- default styling을 그대로 배치해 프로젝트 고유 방향과 접근성을 잃었는가.
- rollback이 source receipt와 실제 변경 파일을 복원할 수 있는가.

## 7. BCP-2026-035 · bounded generated-visual integrity

### `VISUAL_TASK_SCOPE_FIDELITY`

single-screen mock, state sheet, before/after, visual QA reference처럼 범위가 고정된 visual 작업은 생성 전 `visual_question / target_screen / target_state / excluded_scope`를 기록한다. 결과가 broad dashboard, unrelated screen, undeclared state 또는 새 게임 규칙·UI로 확대되면 같은 deliverable의 PASS가 아니다. 탐색 가치가 있으면 별도 candidate로 보존할 수 있지만 원래 visual question을 대신하지 않는다.

### `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N개의 결과를 요청하면 기본 계약은 N개의 independent deliverable이다. 각 결과는 독립 검토·교체·배치할 수 있어야 한다. N-panel collage는 collage가 요청되거나 명시적으로 승인된 경우에만 동등하다. 의미 손실 없이 분리 가능하면 분리하고, panel 문맥에 종속돼 crop 시 의미가 깨지면 bounded brief로 재생성한다.

### `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

경로·선택·잠금·상태 같은 판단 정보가 art/background와 경쟁하면 `whole-style replacement / color-intensity-only / identity-preserving independent semantic cues`를 비교한다. 기존 제품 정체성을 보존할 가치가 있으면 세 번째 방향을 먼저 검토한다. cue는 color, direction, shape, text/icon, brightness/thickness, motion 중 프로젝트에 맞는 서로 독립적인 신호를 조합하며 Base는 특정 값이나 표현을 상수화하지 않는다.

이 계약은 생성 작업의 process integrity를 다룬다. repository contract, mock, screenshot 또는 Notion readback만으로 `human comprehension`, 접근성, runtime/device correctness를 PASS 처리하지 않는다.
