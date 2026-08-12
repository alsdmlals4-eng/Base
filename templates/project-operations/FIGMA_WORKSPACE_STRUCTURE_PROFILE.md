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
