# Work 프로젝트 실행 Current Router

```text
WORK_PROJECT_EXECUTION_CURRENT_ROUTER
THIN_ROUTER_NOT_SECOND_CANON
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_BASE_OWNER_WINS_ON_DRIFT
```

> 이 파일은 프로젝트 사실이나 세부 실행 절차를 복제하지 않는다. 새 Work가 현재 Project GitHub·Notion·실제 구현과 Base latest completed main에서 필요한 owner를 빠르게 찾도록 연결하는 얇은 진입점이다.

## 1. 권위 순서

```text
사용자의 최신 명시 지시
→ Project AGENTS / Active Context / 승인 Decision
→ Project 분야별 GitHub·Notion current canon
→ 실제 code/data/Scene/Resource/asset/test/runtime evidence
→ Project가 채택한 current Base owner
→ Base latest completed main
→ 과거 채팅·Memory·handoff
```

과거 대화와 Memory는 discovery 후보일 뿐 current truth가 아니다. 충돌하면 Project canon과 실제 구현을 fresh-read하고 `CONTEXT_DRIFT_RECHECK_REQUIRED`로 되돌린다.

## 2. 기본 로드 순서

현재 프로젝트 작업을 시작하거나 재개할 때 다음을 순서대로 적용한다.

```text
1. exact Project identity / repository / Notion Home / actual implementation
2. Base latest completed main / root AGENTS / current Skill Registry inventory
3. templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md
4. templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md
5. templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
6. templates/project-operations/WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
7. 현재 Goal에 trigger되는 Base·Project 전문 owner
8. Work preparation → Codex implementation → Work final review → user validation
```

```text
WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md
WORK_PROJECT_START_CANON_CHECKLIST.md
WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
```

## 3. 시작 전 정본 교정 Gate

새 기획·이미지·사운드·Codex mutation 전에 `WORK_PROJECT_START_CANON_CHECKLIST.md`로 다음을 확인한다.

```text
핵심 재미와 player promise
핵심 시스템과 실제 consumer
evidence-based SWOT
current stage / active Slice / accepted frontier
실제 구현·test·Visual·Audio 상태
남은 required work
의존성·player value·risk 기반 작업순서
stale / duplicate / conflict / missing canon
GitHub structured canon·Notion human canon readback
```

승인 범위의 작은 정본 결함은 먼저 교정한다. 프로젝트 Core·주요 UX·경제·서사·Art Direction처럼 제품 의미가 바뀌는 결정만 보류한다.

## 4. Work↔Codex 최소 전환

`WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`를 따라 다음 구조를 유지한다.

```text
Work
→ 기획·검수·UI/UX·Data·Visual·Audio·VFX·권리·Acceptance·QA 입력 완료
→ WORK_PRODUCTION_INPUT_PACKET readback
→ Codex single implementation window
→ actual code/Scene/Resource/runtime/test/build
→ CONSOLIDATED_RETURN_PACKET
→ Work final evidence review·교정·canon sync·merge/readback
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

작은 누락마다 Work↔Codex를 왕복하지 않는다. 실제 제품 구현이 필요하면 current Codex handoff owner로 전환하고, Work가 구현됐다고 추측하지 않는다.

## 5. Project-local Visual opt-in

사용자가 이미지 binary를 Notion에 중복 업로드하지 않고 각 프로젝트 로컬·repository 자산으로 관리하라고 명시한 경우 다음 owner를 함께 적용한다.

```text
WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md
PROJECT_LOCAL_VISUAL_BINARY_FIRST
NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY
NO_NOTION_BINARY_UPLOAD_REQUIRED
```

경로:

```text
Notion Visual 구조·Art Direction fresh-read
→ exact project-local candidate
→ format/dimensions/SHA-256/provenance/rights readback
→ PROJECT_ASSET_APPROVED
→ tracked project asset + ASSET_MANIFEST
→ feature-branch commit/push/remote readback
→ Codex project-relative locator
→ Godot import/runtime consumer evidence
```

Notion human-facing text·상태를 실제로 수정했다면 해당 destination readback은 유지한다. binary를 올리지 않았으면 업로드했다고 주장하지 않는다. Project가 별도 binary owner를 갖고 있으면 Project 결정이 우선한다.

## 6. 증거 Identity

`WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`로 다음을 분리한다.

```text
제품 구현 기준 SHA
!= 문서·router 동기화 SHA
!= current validation HEAD
!= build/runtime candidate HEAD

TEST_LOGIC_PASS
!= CI_GATE_PASS

Godot import cache
!= product source

LOCAL_VISUAL_CANDIDATE
!= PROJECT_ASSET_APPROVED
!= RUNTIME_PROMOTED

local commit
!= remote synchronized

machine QA
!= Human usability
!= Player Experience
```

player-facing bytes 또는 package 설정이 바뀌면 영향 후보를 supersede하고 필요한 runtime/build/screenshot Gate를 다시 수행한다.

## 7. Git·Godot·컴퓨터 조작

실제 callable tool이 있을 때 current Project 범위에서만 다음을 자동 실행한다.

```text
remote/upstream/default branch 탐색
→ fetch
→ clean·tracking·non-diverged일 때만 pull --ff-only
→ current-task feature branch commit/push
→ remote HEAD readback
→ PR / exact-head required checks / safe squash merge
→ post-merge main readback

exact project/worktree 확인
→ exact Godot binary/project/session 확인
→ Editor/game/GUT/Hera 또는 adopted equivalent 실행
→ runtime/screen/build evidence
```

금지:

```text
direct main push
force push
blind stash/reset/clean/rebase
다른 open PR takeover
무관한 앱·파일·credential 조작
OS 보안·계정 권한 변경
새 유료 비용
공개 Release·스토어 게시
```

## 8. 계속 실행과 완료

```text
bounded retry
→ evidence-equivalent fallback
→ 막힌 task만 defer
→ 독립 ready work 계속
→ current Slice machine-executable required work = 0
→ actual-state completion rescan
→ 최소 5회 full-scope adversarial review
→ blocking finding 0
```

Human QA는 사용자의 실제 플레이 전까지 다음으로 유지한다.

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

자동화 완료 뒤 다운로드 가능한 internal build와 사용자 검증 패킷을 제공한다. 사용자가 실제 버티컬 슬라이스를 검증하기 전에는 다음 Slice로 자동 진입하지 않는다.

## 9. Project-specific leakage 방지

다음은 이 router에 고정하지 않는다.

- 프로젝트명·캐릭터·세계관·기능명
- 특정 PR/Issue/Task/Decision 번호
- 특정 SHA·branch·worktree·절대 경로
- 특정 해상도·HUD·palette·Art Style
- 특정 완료 목록·다음 우선순위
- 특정 플랫폼 전용 Human gate

이 값들은 exact Project canon과 실제 구현에서 fresh-read한다.

## 10. 최종 원칙

```text
fresh-read before assumption
canon correction before new production
Work inputs complete before Codex
one Codex implementation window when possible
machine evidence without Human/Player overclaim
project-local durable Visual bytes under explicit opt-in
safe Git/Godot automation when callable
remaining required work zero is completion candidate
user validation before next Slice
```
