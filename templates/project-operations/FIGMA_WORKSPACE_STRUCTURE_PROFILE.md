# Figma Workspace Structure Profile

이 문서는 Base의 `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`와 `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`를 보완하는 **요금제·좌석 제약 인지형 Figma 구조 운영 규칙**이다.

Figma는 GitHub/GDD/Decision 또는 실제 Godot 구현의 정본을 대체하지 않는다. 이 문서가 정하는 것은 Figma 안의 **팀/프로젝트/파일/페이지 조직 방법**과 Starter → Professional 마이그레이션 규칙이다.

---

## 1. 기본 조직 원칙

1인 개발자가 여러 게임 프로젝트를 운영하는 기본 구조는 다음을 권장한다.

```text
Figma Team (1개)
├─ 00_BASE
├─ 10_<PROJECT_A>
├─ 20_<PROJECT_B>
└─ ...
```

- **Figma Team은 기본 1개**로 유지한다.
- **GitHub 저장소/게임 프로젝트 1개 ≒ Figma Project 1개**로 대응한다.
- 게임마다 별도 Team을 만들지 않는다.
- Base Figma는 공용 작업 규칙·메타 컴포넌트만 담고, 프로젝트 고유 아트/UI는 프로젝트 Figma에 둔다.
- Organization/Enterprise 전용 다중 Team 관리 기능이 실제로 필요해질 때만 상위 구조를 검토한다.

---

## 2. 프로젝트 기본 파일 구조

Professional 이상에서 권장하는 프로젝트 파일 구조는 최소 3파일이다.

```text
<PROJECT>
├─ 00_<PROJECT>_HUB
├─ 10_<PROJECT>_ART
└─ 20_<PROJECT>_UI_UX
```

필요할 때만 추가한다.

```text
90_<PROJECT>_ARCHIVE
```

### 00_<PROJECT>_HUB

프로젝트 Figma의 입구. 다음 내용을 둔다.

```text
00_START_HERE
10_CURRENT_STATE
20_SSOT_MAP
30_ART_DIRECTION
40_UX_PRINCIPLES
50_DECISION_MIRROR
60_IMPLEMENTATION_MAP
70_GPT_CONTEXT
90_CHANGELOG
```

`DECISION_MIRROR`는 GitHub Decision의 두 번째 정본이 아니라 링크·요약 인덱스다.

### 10_<PROJECT>_ART

```text
00_GUIDE
10_ART_DIRECTION
20_SOURCE_IMAGES
30_AI_WORKBENCH
40_CHARACTERS
50_ENVIRONMENTS
60_BUILDINGS
70_EFFECTS_ICONS
80_SPRITES
85_EXPORT_READY
90_REVIEW
95_APPROVED
99_ARCHIVE
```

- `SOURCE_IMAGES`: 사용자 제공/외부/생성 원본 보존. AI가 직접 덮어쓰지 않는다.
- `AI_WORKBENCH`: GPT/Codex가 자유롭게 복제·생성·수정하는 영역.
- `REVIEW`: 승인 후보.
- `APPROVED`: 사용자 승인 시각 기준. 기본 읽기 전용 취급.
- `ARCHIVE`: superseded 승인본과 과거 버전 보존.

### 20_<PROJECT>_UI_UX

```text
00_GUIDE
10_FOUNDATIONS
20_COMPONENTS
30_SCREENS
40_SCREEN_STATES
50_USER_FLOWS
60_GAMEPLAY_FLOWS
70_PROTOTYPES
80_AI_WORKBENCH
85_REVIEW
90_DEV_HANDOFF
95_APPROVED
99_ARCHIVE
```

Screen과 Flow는 분리한다.

- `SCREENS`: 화면 자체.
- `USER_FLOWS`: 플레이어의 화면 이동·취소·복귀 경로.
- `GAMEPLAY_FLOWS`: 게임 규칙·선택·성공/실패 흐름의 시각 표현.
- `DEV_HANDOFF`: Figma frame/node ↔ GitHub spec ↔ Godot scene/script 연결.

---

## 3. Professional 권장 5페이지 Visual Bible

Base의 기존 Visual Bible lifecycle을 유지한다.

```text
00_DIRECTION
01_APPROVED_REFERENCE
02_WIP
03_REJECTED
04_FINAL
```

의미는 `FIGMA_VISUAL_BIBLE_PROFILE.md`를 따른다.

이 5페이지 구조는 Artifact lifecycle을 새로 만들지 않는다.

---

## 4. Starter 3페이지 fallback

Figma Starter의 페이지 수 또는 좌석/도구 호출 제약으로 5페이지 구조를 만들 수 없는 경우 **기능을 버리지 말고 3페이지 압축형**을 사용한다.

```text
00_DIRECTION
01_APPROVED_REFERENCE
02_WORKSPACE
```

`02_WORKSPACE` 내부 Section 권장 구조:

```text
02.1_WIP
02.2_FLOW_PROTOTYPE
02.3_GPT_INTERPRETATION
02.4_REVIEW
02.5_REJECTED
02.6_FINAL
02.7_IMPLEMENTATION_COMPARE
02.8_ARCHIVE
```

상태 의미는 Professional 5페이지 구조와 동일하다.

- `02.1_WIP` = `02_WIP`
- `02.5_REJECTED` = `03_REJECTED`
- `02.6_FINAL` = `04_FINAL`

**Starter 압축형은 임시 운영 구조이지 별도 lifecycle이 아니다.**

---

## 5. Starter → Professional 마이그레이션

Professional Full/Dev 등 충분한 편집·MCP 권한이 확보되면 다음 순서로 펼친다.

```text
00_DIRECTION                → 유지
01_APPROVED_REFERENCE       → 유지
02_WORKSPACE/02.1_WIP       → 02_WIP
02_WORKSPACE/02.2_FLOW_*    → 02_WIP 내 Flow section 또는 전용 UI/UX file
02_WORKSPACE/02.3_GPT_*     → 02_WIP 내 GPT interpretation section
02_WORKSPACE/02.4_REVIEW    → 02_WIP pending review 또는 REVIEW section
02_WORKSPACE/02.5_REJECTED  → 03_REJECTED
02_WORKSPACE/02.6_FINAL     → 04_FINAL
02_WORKSPACE/02.7_COMPARE   → 04_FINAL implementation compare
02_WORKSPACE/02.8_ARCHIVE   → 05_DEPRECATED/07_ARCHIVE 또는 프로젝트 Archive file
```

마이그레이션 시 Stable Artifact ID, `screen_id`, `flow_id`, `related_decision_ids`, `source_commit`, Visual Artifact Registry 연결을 유지한다.

기존 Section을 삭제하지 말고 이동 후 링크·Registry를 갱신한다.

---

## 6. AI 수정 권한 경계

| 영역 | GPT/Codex 기본 권한 |
| --- | --- |
| SOURCE_IMAGES | 읽기만 |
| APPROVED / APPROVED_REFERENCE | 읽기만 |
| AI_WORKBENCH / WIP | 생성·수정 가능 |
| REVIEW | 승인 후보 작성 가능 |
| COMPONENTS | 승인된 작업 범위에서만 수정 |
| REJECTED | 읽기만; 재도입은 새 검토 필요 |
| ARCHIVE | 읽기만 |
| DEV_HANDOFF | 구현 상태·경로 연결 갱신 가능 |
| FINAL | 사용자 승인 없는 직접 승격/수정 금지 |

AI가 승인 시각 정본을 직접 덮어쓰지 않는다.

변경이 필요하면:

```text
APPROVED vN
→ duplicate
→ AI_WORKBENCH/WIP vN+1
→ REVIEW
→ user approval
→ APPROVED vN+1
→ previous version ARCHIVE/SUPERSEDED
```

---

## 7. Frame naming

UI frame 권장 형식:

```text
[STATUS] SYSTEM / SCREEN / STATE / PLATFORM / VERSION
```

예:

```text
[APPROVED] Battle / HUD / Default / PC / v03
[WORKING] Battle / HUD / BossFight / PC / v04
[REVIEW] Settings / Audio / Default / PC / v01
```

Art asset 권장 형식:

```text
TYPE_SUBJECT_STATE_VIEW_VERSION
```

예:

```text
CHAR_Player_Idle_Front_v03
ENV_Forest_Night_v04
BLDG_Tower_Level01_v03
ICON_Skill_Fireball_v02
```

기존 `FIGMA_VISUAL_BIBLE_PROFILE.md`의 Stable Artifact ID 규칙과 충돌할 경우 Stable Artifact ID를 우선한다.

---

## 8. DEV_HANDOFF 최소 계약

```yaml
visual_artifact_id:
figma_file:
figma_page:
figma_frame_node:
responsible_spec:
related_decision_ids: []
godot_scene:
godot_script:
asset_paths: []
source_commit:
target_platform:
target_resolution:
input_method:
implementation_status: NOT_STARTED | IN_PROGRESS | IMPLEMENTED | VERIFIED
last_verified_at:
```

`IMPLEMENTED`는 코드 존재를 뜻할 수 있으나 `VERIFIED`는 실제 runtime capture/test 등 검증 증거가 있어야 한다.

---

## 9. 요금제·접근 상태 처리

Figma 상태는 다음과 같이 구분한다.

```text
CONFIGURED
READ_ONLY
AUTH_REQUIRED
ACCESS_DENIED
LINK_UNVERIFIED
RATE_LIMITED
PLAN_LIMITED
SYNC_PENDING
```

- 페이지 생성이 요금제 때문에 거부되면 `PLAN_LIMITED`.
- MCP 호출 한도에 도달하면 `RATE_LIMITED`.
- 실패한 write가 원자적 실패라고 확인된 경우 실제 변경으로 보고하지 않는다.
- 권한이나 요금제 제약으로 Figma 반영이 실패해도 GitHub 정본·생성물·WIP를 잃지 않는다.
- Figma 업그레이드는 기능 필요와 비용을 기준으로 사용자가 결정하며 Base가 자동 결제를 전제하지 않는다.

---

## 10. 적대적 검토 체크

다음 중 하나라도 발생하면 구조 변경을 거부하거나 보완한다.

- Figma가 GitHub/GDD/Decision의 두 번째 규칙 정본이 됨.
- 프로젝트별 Team 난립으로 권한·Library·비용 관리가 복잡해짐.
- Starter/Professional 구조가 서로 다른 Artifact lifecycle을 만듦.
- AI가 APPROVED/FINAL을 사용자 승인 없이 수정함.
- SOURCE 원본이 WIP 수정으로 덮어써짐.
- UI Screen과 Flow가 한 캔버스에 무분별하게 섞여 탐색성이 무너짐.
- `FINAL`을 Godot 구현 완료 또는 제품 asset 승인으로 오해함.
- Prototype을 runtime 검증으로 오해함.
- Figma 쓰기 실패를 성공으로 보고함.
- project-specific URL, 토큰, 비밀값을 Base 공용 템플릿에 저장함.

---

## 11. 적용 우선순위

1. Team 1개 + 프로젝트별 Figma Project 구조.
2. 프로젝트별 HUB / ART / UI_UX 3파일.
3. SOURCE → WIP/AI_WORKBENCH → REVIEW → APPROVED → ARCHIVE 보호 흐름.
4. Figma 승인 frame ↔ GitHub spec/Decision ↔ Godot 구현 연결.
5. 실제 여러 프로젝트에서 반복된 규칙만 Base 공용 규칙으로 승격.

프로젝트 고유 파일 URL·아트 방향·컴포넌트·화면 규칙은 각 프로젝트 로컬 Profile/Registry에 기록한다.

---

## 12. 실전 사용법·팁·노하우

이 절은 Figma 기능을 많이 쓰는 것이 목적이 아니라 **반복 수정 비용을 줄이고, 화면 의도를 구현자에게 안정적으로 넘기며, 승인본과 실제 런타임의 차이를 빠르게 찾는 것**을 목표로 한다. Figma 기능이 존재한다는 이유만으로 모든 프로젝트에 아래 단계를 강제하지 않는다.

### 12.1 기본 작업 순서

```text
화면 질문 / player question / screen purpose
→ 구조가 아직 불명확할 때만 FigJam 또는 low-fi frame
→ Frame + Auto Layout
→ 실제로 반복되는 UI → Component
→ 예측 가능한 state / size / type → Variants 또는 component properties
→ 여러 화면·상태에서 반복되는 design value → Variables when reuse justifies it
→ prototype으로 flow / interaction 가설 확인
→ APPROVED_REFERENCE와 비교
→ Ready for dev / annotation / Dev Mode handoff
→ Godot/Web 실제 구현
→ RUNTIME_CAPTURE
→ COMPARE_BOARD / drift classification
```

Prototype은 흐름·전환·피드백 가설을 검토하는 작업면이다. **prototype is not runtime proof**이며 Godot의 입력·성능·저장·접근성·플랫폼 동작을 증명하지 않는다.

### 12.2 Auto Layout — 반복 UI는 좌표보다 관계를 먼저 설계

- 반복되거나 반응형이어야 하는 UI는 수동 pixel pushing보다 **Auto Layout**을 우선 검토한다.
- 선택한 layer/frame에 `Shift+A`로 Auto Layout을 적용할 수 있다.
- `Hug contents`, `Fill container`, fixed size를 습관적으로 섞지 말고 각 요소가 **콘텐츠를 따라갈지, 부모 공간을 채울지, 고정될지** 의도적으로 정한다.
- padding, gap, alignment, wrapping을 먼저 조정하고 마지막에 시각 미세조정을 한다.
- 한 번만 쓰는 고정 일러스트·특수 장식처럼 관계형 layout 이점이 없는 영역에는 Auto Layout을 억지로 적용하지 않는다.
- Figma layout 기능·속성은 바뀔 수 있으므로 오래된 튜토리얼보다 현재 Figma Help를 우선하고, 기존 대형 화면을 일괄 변환하기 전에는 시각 비교와 prototype 회귀를 수행한다.

### 12.3 Components / Variants — 반복 규칙만 승격

Component는 **실제로 재사용되거나 여러 화면에서 동기화되어야 하는 것**을 승격한다.

권장 후보:

```text
Button / Primary
Button / Secondary
HUD / ResourceChip
HUD / StatusIcon
Dialog / ChoiceRow
Inventory / Slot
Tabs / Item
Input / Field
```

- `state`, `size`, `type`처럼 예측 가능한 축은 **Variants** 또는 component properties로 표현한다.
- Hover/Pressed/Disabled/Selected처럼 상태가 반복되면 **interactive components**로 prototype 연결 수를 줄일 수 있다.
- 서로 책임이 다른 UI를 한 giant component에 억지로 모으지 않는다.
- `state × size × platform × rarity × theme × ...`처럼 조합 폭발이 생기면 variant를 더 만드는 대신 component 경계를 다시 나눈다.
- **componentizing one-off decoration**은 기본적으로 피한다. 한 번만 쓰는 장식을 Component로 만드는 것은 재사용 체계가 아니라 탐색 비용일 수 있다.

### 12.4 Variables — 모든 숫자가 아니라 반복되는 의미를 토큰화

Variables는 값 자체보다 **반복되는 의미·상태·mode**가 있을 때 사용한다.

게임 UI의 작은 시작 예:

```text
Color / Semantic
  bg/default
  text/primary
  text/muted
  state/danger
  state/success

Spacing
  xs / sm / md / lg

Typography / Role
  body / label / heading

Platform or density mode
  pc / mobile    # 실제 차이가 있을 때만
```

- raw number 하나가 있다는 이유로 모두 Variable로 만들지 않는다.
- 프로젝트 초기에 거대한 design-token system부터 만들지 않는다.
- 실제 재사용이 반복되고 수정 동기화 이점이 확인될 때 확장한다.
- Variables를 prototype state에 사용할 수 있지만, prototype state도 실제 게임 state canon을 대체하지 않는다.

### 12.5 Sections / FigJam — 보드가 커질수록 탐색 단위를 명시

- **Sections**는 review 범위, flow, handoff 단위, milestone을 묶는 탐색 경계로 사용한다.
- `Ready for dev` 또는 구현 비교가 필요한 구역은 화면들이 어디까지 같은 검토 단위인지 명확히 한다.
- **FigJam**은 market map, competitor clustering, affinity grouping, journey/system diagram, critique, brainstorming과 research 정리에 사용할 수 있다.
- FigJam 카드에는 가능하면 `source / checked_at / platform / evidence label`을 같이 적는다.
- FigJam 메모·투표·스티커는 아이디어와 관찰 기록이지 GitHub/GDD의 확정 Decision이 아니다.

### 12.6 Dev Mode — 구현 handoff에서 쓰되 코드 정답으로 취급하지 않는다

`IMPLEMENTATION_PINNED` 단계 이후에는 **Dev Mode**를 다음 용도로 사용할 수 있다.

- spacing, size, applied styles/Variables 확인
- component / Variants 상태 확인
- asset export surface 확인
- annotation과 Ready for dev 상태 확인
- 변경 전후 frame/version 비교
- 디자인과 ticket/document/code-component 연결

Dev Mode code snippet이나 자동 codegen은 **translation aid**다. Godot scene hierarchy, theme, input/focus, save/data contract, runtime behavior의 생산 코드 정답이나 검증 증거가 아니다. 실제 구현은 프로젝트 code owner와 runtime/test evidence가 책임진다.

### 12.7 이름과 비교 보드 노하우

- `BlueRect`, `Frame 247`보다 `Button/Primary`, `HUD/ResourceChip`, `UI/Inventory/Empty`처럼 의미 중심으로 이름을 붙인다.
- 승인 frame을 직접 파괴적으로 수정하지 말고 WIP 복제본에서 변경한 뒤 `REVIEW → approval`을 거친다.
- 경쟁작 screenshot/reference는 비교표 가까이에 둘 수 있지만 원 출처·날짜·플랫폼을 편집 가능한 텍스트로 보존한다.
- 경쟁작의 시각 구조를 관찰해도 식별 가능한 UI 배치·아트·icon·signature style을 그대로 복제하지 않는다.

### 12.8 실전 anti-patterns

다음은 효율화처럼 보여도 기본적으로 거부하거나 축소한다.

```text
repeated responsive UI를 Auto Layout 없이 좌표로만 수동 유지
componentizing one-off decoration
책임이 다른 UI를 하나의 giant Variants matrix에 결합
실제 재사용 없는 Variables / token proliferation
prototype == runtime proof
Dev Mode snippet == production correctness
FigJam research board == game-rule canon
competitor UI / art layout == best-practice template
APPROVED frame을 WIP 실험으로 직접 덮어쓰기
```

Figma의 목적은 design-system 규모를 키우는 것이 아니라 **작은 팀이 같은 화면을 더 적게 다시 만들고, 비교·승인·구현 차이를 더 빨리 찾게 하는 것**이다.
