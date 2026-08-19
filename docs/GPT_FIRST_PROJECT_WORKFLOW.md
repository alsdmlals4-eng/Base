# GPT-first 프로젝트 기획·검수·구현 생명주기

이 문서는 Base와 Base를 채택한 프로젝트에서 **GPT가 기획과 검수의 주 책임자**이고, Codex는 실제 저장소·엔진 실행이 필요할 때만 선택적으로 호출되는 보조 executor라는 기본 운영 계약을 정의한다.

기존 `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 on-demand handoff 세부 실행 규칙을 대체하지 않고, 그보다 앞선 프로젝트 작업 순서와 사용자 경험을 고정한다.

## 1. Machine contract

```text
GPT_PRIMARY_PLANNING_REVIEW
GPT_FINAL_REVIEW_AUTHORITY
CODEX_OPTIONAL_SUB_EXECUTOR
ONE_SHOT_CODEX_HANDOFF_WHEN_NEEDED
GITHUB_NOTION_PREFLIGHT_REQUIRED
NOTION_VISUAL_CHECKPOINT_BEFORE_POC
UX_UI_REPRESENTATIVE_STATE_REQUIRED
APPROVED_VISUALS_FEED_POC
APPROVAL_TO_ADVERSARIAL_REVIEW_SYNC_PR_READBACK
USER_LEARNING_COMPLETION_REPORT
```

## 2. 역할 분리

### GPT — 기본 주 책임

GPT는 프로젝트 작업의 기본 진입점이며 다음을 끝까지 책임진다.

- 최신 사용자 의도·프로젝트 방향 복원
- GitHub `main`, 프로젝트 정본, 실제 코드·데이터·Scene·Resource·Test 조사
- Project Notion Home, Visual/Story Bible, Flow/Storyboard, Asset/Reference/Benchmark, 핵심 시스템 표 조사
- 누락·충돌·구형 결정·중복 작업·진행 중 다른 workstream 식별
- 현행 조사, 최소 3개 실질 대안, 벤치마킹, trade study, 더 나은 대안 재탐색
- 프로젝트 코어·플레이어 경험·세계관·시스템·데이터·UI/UX·아트 방향 기획
- 이미지가 판단에 중요한 작업의 시각 후보 생성·검수·Notion 배치·readback
- 사용자 승인 전 적대적 검토와 장기계획 적합성 검토
- 승인된 결과의 repository/Notion 동기화 범위 결정
- 구현 결과의 diff·runtime evidence·UX/UI·기획 일치 최종 검수
- 사용자 학습형 완료보고

GPT가 실제 runtime/engine mutation 권한을 현재 세션에서 갖지 않으면 구현 완료를 주장하지 않는다.

### Codex — 필요 시 보조 executor

`CODEX_OPTIONAL_SUB_EXECUTOR`는 Codex를 모든 작업의 의무 단계로 만들지 않는다.

Codex는 다음과 같은 경우에만 사용한다.

- 실제 저장소 파일의 다수 수정·리팩터링·테스트가 필요한 경우
- Godot Scene/Resource/GDScript 구현과 runtime 검증이 필요한 경우
- 로컬 실행환경에서 재현해야 하는 버그·빌드·성능 검사가 필요한 경우
- GPT가 승인된 구현 계약은 확정했지만 현재 세션에 필요한 실행 권위가 없는 경우
- 사용자가 명시적으로 Codex 검토/구현을 요청한 경우

작은 문서 수정, Notion 기획 정리, 조사·비교·기획 검수만으로 닫히는 작업에 Codex를 억지로 호출하지 않는다.

Codex가 호출되어도 프로젝트 방향, 플레이어 경험, 핵심 규칙의 최종 판정 권한은 GPT 검수 단계로 돌아온다.

## 3. 작업 시작 preflight

L1 이상 프로젝트 작업은 가능하면 다음 순서로 읽는다.

```text
latest user request
→ Base AGENTS / START_HERE / relevant policy
→ project GitHub latest main HEAD
→ same-goal open/recent PRs read-only classification
→ project AGENTS / START_HERE / ACTIVE_CONTEXT / confirmed decisions
→ actual code / data / scenes / resources / tests
→ exact Project Notion Home and relevant project-filtered surfaces
→ conflicts / missing sync / stale data classification
→ planning
```

GitHub와 Notion 중 하나만 보고 프로젝트 상태를 추정하지 않는다. Notion은 사람용 기획·시각 정본, repository는 structured/runtime truth라는 `DOMAIN_SPLIT_CANON`을 유지한다.

다른 채팅의 branch/worktree/path/PR은 기본적으로 수정하지 않는다.

## 4. 기획·검수 단계와 시각 checkpoint

### `NOTION_VISUAL_CHECKPOINT_BEFORE_POC`

이미지·UI·UX·화면 정보 구조가 플레이 경험 판단에 materially relevant하면, 회색 박스만으로 PoC를 먼저 만든 뒤 뒤늦게 시각 요소를 붙이는 것을 기본 경로로 삼지 않는다.

```text
concept / system / player experience
→ UX flow and representative UI states
→ image / visual candidate planning
→ candidate generation or approved reference composition
→ GPT visual + UX review
→ attach to exact Project in Notion
→ Notion destination readback
→ user approval
→ APPROVED_VISUALS_FEED_POC
→ PoC / demo implementation
→ runtime demo test
```

### `UX_UI_REPRESENTATIVE_STATE_REQUIRED`

PoC 전에 모든 화면을 완성할 필요는 없다. 그러나 시각과 UX가 테스트 결과를 바꿀 수 있다면 최소한 다음 대표 상태를 기획·검수한다.

- core loop 진입 화면 또는 첫 인상
- 주 플레이 상태
- 핵심 선택/결정 상태
- 성공·실패·보상 또는 주요 feedback 상태
- 시스템 이해에 중요한 popup / HUD / navigation 상태

기술-only spike처럼 시각이 결과에 영향을 주지 않는 PoC는 이 Gate를 생략할 수 있으나, 생략 이유를 기록한다.

### `APPROVED_VISUALS_FEED_POC`

사용자가 승인한 시각 후보가 PoC의 판단 근거라면 PoC는 가능한 한 그 승인 이미지를 직접 사용하거나, 동일 provenance를 가진 구현용 파생 자산을 사용한다. 임의의 다른 이미지·스타일로 대체하지 않는다.

Notion preview가 runtime 적용 증거는 아니다. 구현 후 실제 scene/resource/build가 해당 자산을 소비했는지 별도 검증한다.

## 5. 사용자 승인 단위의 닫힘

### `APPROVAL_TO_ADVERSARIAL_REVIEW_SYNC_PR_READBACK`

사용자가 L1 이상 material change/deliverable을 승인하면 그 승인 단위는 다음 상태까지 닫는다.

```text
USER APPROVAL
→ adversarial review of the approved scope
→ verified findings refined
→ repository structured changes prepared
→ Notion human-facing changes prepared
→ image/asset provenance + implementation path checked when relevant
→ branch/commit/PR
→ EXACT-HEAD PR GATE
→ required checks + unresolved thread 0 + P0/P1 0
→ merge when policy permits
→ POSTMERGE READBACK from GitHub main
→ Notion destination/status readback
→ cross-domain sync verdict
→ learning-oriented user report
```

사소한 문구·오탈자처럼 L0인 변경을 억지로 대형 PR로 만들지는 않는다. 그러나 사용자가 승인한 하나의 material 작업 단위는 승인만 받고 미동기화 상태로 장기간 방치하지 않는다.

이미지 파일도 구현/PoC 입력으로 승인되면 동일하게 provenance, Notion readback, repository asset path, PR/merge, runtime consumption evidence를 분리한다.

## 6. Codex handoff

Codex가 필요한 경우 GPT는 사용자가 새 PowerShell에서 **한 번에 붙여넣을 수 있는 하나의 실행 블록**을 우선 제공한다.

```text
fresh PowerShell
→ exact project/repository/worktree resolve
→ latest main / branch identity check
→ required local capability check
→ launch or attach Codex in exact target
→ pass one complete implementation contract
```

Codex prompt에는 최소한 다음을 포함한다.

```yaml
project_identity:
github_repository:
notion_project_home:
base_main_sha:
project_main_sha:
approved_goal:
player_or_user_experience:
important_rules: []
important_skills: []
module_map: []
approved_visual_inputs: []
notion_records_to_read: []
repository_paths_to_read: []
protected_paths_and_behavior: []
implementation_scope: []
acceptance_criteria: []
required_tests: []
runtime_checks: []
forbidden_changes: []
rollback: []
completion_report_required: true
```

Codex는 붙여넣은 명세만 믿지 않고 GitHub와 현재 프로젝트 파일을 다시 읽는다. Notion 내용이 구현 방향에 materially relevant하고 연결 접근이 가능한 환경이면 해당 Project 범위의 Notion도 확인한다. 접근할 수 없는 Notion 사실을 추정하지 않는다.

Codex가 구현을 마치면 GPT 검수로 돌아와 diff, test, runtime evidence, approved visuals, Notion 상태와 기획 방향을 다시 비교한다.

## 7. `USER_LEARNING_COMPLETION_REPORT`

Base와 프로젝트의 L1 이상 완료 보고는 단순히 `완료 / 테스트 통과`로 끝내지 않는다.

사용자가 시스템을 학습할 수 있도록 최소한 다음을 설명한다.

### 이 작업/파트는 무엇인가

Base 또는 프로젝트 전체에서 해당 범위가 맡는 역할을 쉬운 말로 설명한다.

### 핵심 규칙

중요도 순으로 핵심 규칙을 설명한다.

- 무엇을 보장/차단하는가
- 왜 필요한가
- 실제로 언제 작동하는가
- canonical owner는 어디인가

### 핵심 Skill

실제로 사용한 주요 Skill/Mode를 설명한다.

- 호출 조건
- 책임
- 다른 Skill과의 경계
- 유지/개선/흡수/제거 판정

### 핵심 모듈

| Module | 역할 | 입력 | 출력 | 연결 대상 |
|---|---|---|---|---|

모듈화하지 않은 부분도 이유를 설명한다. 모듈 수를 늘리는 것 자체를 개선으로 간주하지 않는다.

### 변경 전 / 변경 후

- 변경 전 구조와 문제
- 변경 후 구조
- 제거·흡수·유지한 것
- 추가하지 않은 것과 이유
- 사용자/플레이어 체감 변화
- 장기 효과
- trade-off
- 재검토 조건

### 검증 증거

- 실제 실행한 테스트/빌드/런타임/Notion readback
- 통과/실패/미실행
- PR/merge/main SHA
- 남은 위험과 external blocker

## 8. 비용

현재 기본 유료 플랜은 `GPT_PRO` 하나다.

`NOTION_PAID_ON_REQUEST_ONLY`:

- Notion은 기본적으로 현재 무료 범위에서 운영한다.
- 유료 Notion 기능이 없어도 가능한 안전한 fallback을 먼저 사용한다.
- 반복 수작업, 데이터 규모, 동시성, 권한/자동화 한계 때문에 실제 비용 대비 이익이 명확할 때만 `COST_BENEFIT_EVIDENCE_BEFORE_NOTION_UPGRADE`를 작성한다.
- 그 뒤 사용자에게 비용·얻는 기능·무료 대안·미결 위험을 설명하고 명시적 결제 승인을 요청한다.
- 승인 전에는 paid Notion AI, Business/Enterprise-only 기능, 별도 metered automation을 실행 경로로 가정하지 않는다.

## 9. 재검토 조건

다음 중 하나가 발생하면 이 역할 분리를 다시 검토한다.

- GPT가 프로젝트 파일/엔진을 안정적으로 직접 수정·검증할 수 있는 공식 실행면이 기본 제공됨
- Codex 호출 비용/제약이 크게 변함
- Notion 무료 범위가 핵심 작업을 반복적으로 차단함
- 프로젝트 규모가 커져 한 번의 GPT 검수로 구조를 안전하게 유지하기 어려움
- 외부 팀원이 추가되어 별도 review/ownership 구조가 필요해짐

재검토 전까지 기본은 **GPT 기획·검수 우선, Codex 필요 시 보조**다.
