# Project Work Kanban Checklist Design

## Status

- Design status: `USER_APPROVED_IN_CHAT`
- Repository baseline: `32f4dd5ba6042dc34611e2c8912f300b90491e0a`
- Scope: Base 공용 프로젝트 작업 운영 계약과 템플릿
- Product runtime impact: 없음
- GitHub Projects board provisioning: 현재 연결 도구에서 직접 수행하지 않음

## 1. Problem

Base에는 이미 다음 계약이 존재한다.

- 프로젝트 시작 시 정본·현재 단계·남은 작업·우선순위를 복원하는 `WORK_PROJECT_START_CANON_CHECKLIST`
- `ready_tasks / deferred_tasks / completed_tasks`로 실행을 이어가는 continuous work queue
- Issue·Goal·PR의 생명주기와 1인 개발 WIP 제한
- 기획·구현·정적 검사·자동 테스트·런타임·Human/Player 검증을 분리하는 개발 게이트와 evidence hierarchy

그러나 이 정보는 서로 다른 owner에 분산되어 있고, 하나의 Goal 또는 Playable Slice를 수행하는 동안 다음 질문에 지속적으로 답하는 운영용 파생 뷰가 없다.

- 전체 작업 중 몇 개가 실제 증거까지 완료됐는가?
- 현재 하나의 active task는 무엇인가?
- 무엇이 검증 대기·차단·사용자 결정 대기인가?
- 다음 안전 작업은 무엇인가?
- 체크박스가 완료된 이유와 exact evidence는 무엇인가?

따라서 이미지와 같은 카드 상세 체크리스트와 칸반 흐름을 도입하되, 보드 자체가 기획·구현·승인 상태의 두 번째 정본이 되지 않도록 해야 한다.

## 2. Goals

1. 프로젝트 작업 시작·재개 시 현재 Goal 또는 Playable Slice의 전체 작업을 카드와 세부 체크리스트로 구성한다.
2. 각 항목을 단순 수동 체크가 아니라 evidence-backed 상태로 판정한다.
3. `READY → IN_PROGRESS → VERIFY_REVIEW → DONE` 흐름과 `BLOCKED_DECISION` 측면 큐를 제공한다.
4. GPT가 PM 역할로 진행률, 의존성, 차단 사유, 다음 행동과 evidence를 지속 갱신한다.
5. GitHub Issue를 지속 가능한 작업 항목으로 사용하고 GitHub Projects는 선택형 파생 칸반 뷰로 사용한다.
6. 기존 repository canon, 실제 코드·데이터·Scene·Resource·asset·test·evidence owner를 보존한다.
7. 별도 HTML 대시보드, 유료 PM 도구, 신규 독립 workflow framework를 만들지 않는다.

## 3. Non-goals

- 모든 기존 프로젝트에 빈 Issue나 보드를 일괄 생성하지 않는다.
- 체크리스트가 프로젝트 Decision, GDD, data schema, asset manifest 또는 runtime truth를 소유하지 않는다.
- 작은 체크 하나마다 Issue를 생성하지 않는다.
- GitHub Projects가 없거나 현재 도구로 설정할 수 없다는 이유로 작업 실행을 막지 않는다.
- 완료율 숫자를 생산성·품질·플레이어 가치의 단독 지표로 사용하지 않는다.
- 테스트 PASS를 runtime, UX, Human/Player 또는 release PASS로 승격하지 않는다.
- 기존 open/draft/ready PR을 인수·수정·병합하지 않는다.

## 4. Alternatives and decision

### A. Markdown checklist only

장점은 repository 추적과 단순성이다. 단점은 상태별 보기, WIP, 차단 작업, 여러 Goal 검색과 GitHub-native progress 연결이 약하다는 점이다.

**Decision: REJECT as the sole system.** 카드 내부의 bounded checklist 표현으로만 사용한다.

### B. GitHub Projects as the source of truth

장점은 board/table/roadmap, custom fields, filter, automation이다. 단점은 project field가 repository canon과 별도의 상태 authority가 되기 쉽고, 현재 연결 도구에서 보드 설정을 직접 쓰지 못한다는 점이다.

**Decision: REJECT as canon; ADOPT as optional derived view.**

### C. Repository canon + GitHub Issues + optional Projects derived view

Issue는 Goal/Slice와 독립 작업의 지속 가능한 논의·상태·evidence surface다. 프로젝트 사실과 구현 상태는 기존 repository owner에 남기고, Projects는 Issue/PR을 시각화하는 파생 운영면으로 사용한다.

**Decision: ADOPT.** 현재 Base의 repository-first, GitHub work-item lifecycle, continuous work queue와 가장 잘 결합된다.

## 5. Authority model

```text
Project repository owners
  = 기획·결정·데이터·승인 asset·code·Scene·Resource·test·runtime evidence의 정본

GitHub Goal/Slice issue
  = 승인된 목표·범위·완료 기준·하위 작업 관계의 지속 가능한 work-item owner

GitHub task issue
  = 독립 실행·검증·차단·재개가 필요한 작업 단위

Card checklist
  = 해당 work item 안의 bounded execution/verification receipt

GitHub Projects
  = Issue/PR과 field를 보여 주는 optional derived kanban/table/roadmap view
```

보드 field와 체크리스트는 owner의 현재 사실을 요약한다. 충돌 시 repository owner, exact implementation/evidence, Goal/Issue 순으로 다시 읽고 파생 뷰를 교정한다.

## 6. Work hierarchy

```text
Project
└─ Goal or Playable Slice parent issue
   ├─ Independent task issue
   │  ├─ Bounded checklist item
   │  ├─ Bounded checklist item
   │  └─ Verification item
   ├─ Independent task issue
   └─ User-decision issue when materially independent
```

### 6.1 Parent Goal/Slice issue

다음 중 하나를 책임진다.

- 플레이어가 완주할 수 있는 current Playable Slice
- 사용자 검토를 받은 기능 패키지
- 독립 승인·검증·롤백이 가능한 기획/운영 Goal

부모 issue에는 player/user value, approved scope, non-scope, protected scope, acceptance, repository owner locators, exact baseline, 하위 작업과 aggregate progress를 둔다.

### 6.2 Independent task issue

다음 중 하나라도 해당하면 별도 task issue를 허용한다.

- 별도 owner 또는 PR을 가진다.
- 독립적으로 blocked/deferred/resumed 될 수 있다.
- 별도 acceptance 또는 verification이 있다.
- 다른 작업이 의존한다.
- reviewer가 이 작업만 승인 또는 거절할 수 있다.

그렇지 않은 2~5분 단위 절차는 card checklist에 둔다.

### 6.3 No issue explosion

작은 체크, 동일 파일의 단순 순차 수정, 하나의 테스트 사이클 안에서 분리 가치가 없는 단계는 별도 Issue로 만들지 않는다. 한 Goal에 무수한 카드가 생겨 PM 비용이 개발 비용보다 커지는 구조를 금지한다.

## 7. Status model

### 7.1 Board columns

```text
BACKLOG
READY
IN_PROGRESS
VERIFY_REVIEW
DONE

BLOCKED_DECISION
```

`BLOCKED_DECISION`은 정상 흐름의 완료 단계가 아니라 측면 큐다. blocker가 해결되면 원래 흐름의 적절한 상태로 복귀한다.

### 7.2 Work item states

| State | Meaning | Counts complete |
|---|---|---:|
| `BACKLOG` | 승인 범위 후보지만 아직 실행 순서에 들지 않음 | No |
| `READY` | owner·dependency·acceptance·verification이 준비됨 | No |
| `IN_PROGRESS` | 현재 수행 중인 active task | No |
| `VERIFY_REVIEW` | 구현/준비는 끝났고 evidence와 검토가 남음 | No |
| `BLOCKED_UNVERIFIED` | 필수 source, executor 또는 evidence가 없어 판정 불가 | No |
| `USER_DECISION_REQUIRED` | 제품 의미·범위·비용·권한 등 사용자 결정 필요 | No |
| `DEFERRED` | 현재 Goal에서 재개 조건과 함께 뒤로 이동 | No |
| `DONE` | acceptance와 요구 evidence가 충족됨 | Yes |
| `NOT_APPLICABLE` | 해당 항목에 적용되지 않으며 이유가 기록됨 | Excluded |

### 7.3 Checklist item states

Markdown task list의 `[x]`는 오직 `PASS`일 때만 사용한다. 다른 상태는 체크하지 않은 항목과 명시적 prefix를 사용한다.

```text
- [x] PASS — ... evidence: ...
- [ ] IN_PROGRESS — ...
- [ ] READY — ...
- [ ] BLOCKED_UNVERIFIED — ... blocker: ...
- [ ] USER_DECISION_REQUIRED — ...
- [ ] DEFERRED — ... resume_when: ...
- [ ] FAIL — ... evidence: ...
- [ ] NOT_APPLICABLE — ... reason: ...
```

`NOT_APPLICABLE`은 진행률 분모에서 제외한다. `BLOCKED`, `DEFERRED`, `USER_DECISION_REQUIRED`, `FAIL`, 문서만 작성된 구현 항목은 완료로 계산하지 않는다.

## 8. Progress calculation

```text
applicable_items = all checklist items - NOT_APPLICABLE items
completed_items = PASS items only
progress = completed_items / applicable_items
```

규칙:

- 카드 진행률은 card checklist 기준이다.
- 부모 Goal/Slice 진행률은 필수 child task의 `DONE` 수를 기본값으로 사용한다.
- 선택적 polish나 명시적으로 future scope인 항목은 현재 Goal 분모에 넣지 않는다.
- `0/0`은 100%가 아니라 `NO_APPLICABLE_CHECKLIST`로 표시한다.
- 진행률은 상태 요약일 뿐 acceptance와 evidence를 대체하지 않는다.

## 9. Evidence model

기존 Base evidence hierarchy를 재사용한다.

```text
E0_CONTRACT
E1_STATIC
E2_TEST
E3_RUNTIME
E4_VISUAL
E5_PLAY
E6_HUMAN_PLAYTEST
```

각 work item은 요구되는 evidence level만 명시한다. 카드 전체 `DONE`은 다음을 모두 만족해야 한다.

1. 모든 필수 acceptance가 PASS 또는 근거 있는 NOT_APPLICABLE이다.
2. 요구 evidence가 PASS다.
3. `MUST_FIX`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`가 남지 않는다.
4. repository owner와 handoff/readback이 최신이다.
5. 실제 변경이 있으면 diff·exact HEAD·관련 test와 rollback이 연결된다.

예:

```text
Contract: PASS
Static: PASS
Automated test: PASS
Runtime: NOT_RUN
Visual/UX: NOT_RUN
Human/Player: PENDING
Overall work item: VERIFY_REVIEW
```

## 10. WIP and PM behavior

1인 개발 기본 WIP:

- `IN_PROGRESS`: 최대 1
- `VERIFY_REVIEW`: 최대 1
- `BLOCKED_DECISION`: 최대 1 권장

GPT PM의 책임:

1. 시작 receipt에서 current Goal/Slice와 remaining work를 복원한다.
2. dependency와 player/user value 기준으로 READY 순서를 정한다.
3. active task를 하나만 선택한다.
4. 작업·검증 후 checklist, progress, blocker, next action을 갱신한다.
5. blocker 하나 때문에 독립 READY 작업 전체를 멈추지 않는다.
6. 완료 후보에서 remaining-work recalculation과 adversarial review를 수행한다.
7. 사용자에게는 핵심 결정과 최종 Human/Player 판단만 올린다.

## 11. Card contract

공용 Markdown template은 다음 정보를 가진다.

```yaml
work_item_id:
project:
goal_or_slice:
title:
category:
status:
priority:
player_or_user_value:
why_now:
depends_on: []
blocked_by: []
scope: []
out_of_scope: []
protected_scope: []
canon_owner:
actual_consumers: []
source_main_sha:
task_branch_or_pr:
acceptance_criteria: []
required_evidence: []
progress:
blocker:
next_action:
last_updated:
```

본문에는 다음 섹션을 둔다.

- Context and authority
- Scope and protected behavior
- Dependencies and blocker
- Acceptance criteria
- Evidence-backed checklist
- Verification matrix
- Repository readback
- Next action and resume condition

## 12. GitHub issue forms

Base에 두 개의 Issue Form을 제공한다.

1. `Goal / Playable Slice`
2. `Independent Work Item`

Issue Form은 사용자 입력을 구조화하지만, 완전한 machine schema나 새로운 project database를 의미하지 않는다. Required field는 목적·가치·범위·acceptance·owner locator처럼 빈 Issue 생성을 방지하는 최소 항목으로 제한한다.

Base repository 자체의 Issue Form이 프로젝트 저장소에 자동 전파되지는 않는다. 프로젝트가 현재 Base 계약을 채택할 때 template copy/adaptation 대상으로 제공하며, 실제 프로젝트 `AGENTS.md`와 기존 Issue workflow가 우선한다.

## 13. Optional GitHub Projects profile

현재 tool capability가 Projects board provisioning을 지원하지 않으므로 implementation은 다음을 제공한다.

- 권장 field 이름과 값
- 권장 board/table view
- WIP limits
- issue 상태 ↔ board status mapping
- 수동 또는 향후 connector 설정 절차

권장 fields:

| Field | Type | Values / use |
|---|---|---|
| Status | single select | Backlog, Ready, In Progress, Verify/Review, Blocked/Decision, Done |
| Project | text or repository grouping | 프로젝트 식별 |
| Goal/Slice | text or parent issue | 부모 Goal |
| Priority | single select | P0, P1, P2, P3 |
| Category | single select | Planning, System/Data, Code, UI/UX, Visual, Audio/VFX, Bug, QA, Canon/Docs, Release |
| Evidence | single select | Not Run, Partial, Pass, Fail, Blocked |
| Next action | text | 다음 안전 작업 |

동일 의미를 issue field와 project field 양쪽에 중복 소유하지 않는다. 조직 issue field를 실제로 채택한 프로젝트에서는 그 값을 우선하고 동일 project field를 만들지 않는다.

## 14. Integration with existing Base owners

### `WORK_PROJECT_START_CANON_CHECKLIST`

`remaining_and_order` 결과를 다음으로 materialize하는 연결 규칙을 추가한다.

```text
active or next Goal/Slice
→ independent work item classification
→ issue/card creation or existing-item reuse
→ READY/BLOCKED/DECISION queue
→ user-visible progress summary
```

시작 checklist 자체는 second canon이 아니며, 카드 역시 같은 제한을 유지한다.

### `GITHUB_WORK_ITEM_LIFECYCLE_POLICY`

Goal/Slice parent issue, independent task issue, card checklist, optional Projects view의 책임과 WIP를 추가한다. 기존 one-goal-one-active-PR 원칙은 그대로 유지한다.

### `DEVELOPMENT_GATES`

Verification matrix와 evidence ceiling을 카드 template에서 링크해 재사용한다. gate 전체를 카드 본문에 복제하지 않는다.

### Continuous work queue

기존 `ready_tasks / deferred_tasks / completed_tasks`는 runtime execution model로 유지한다. 카드 상태를 queue와 다음처럼 매핑한다.

```text
READY              ↔ ready_tasks
IN_PROGRESS        ↔ ready_tasks + active lease/owner
BLOCKED/DEFERRED   ↔ deferred_tasks
DONE               ↔ completed_tasks
```

새 queue schema를 만들지 않는다.

## 15. File plan

Implementation phase의 예상 변경은 다음과 같다.

- Modify: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`
  - Goal/Slice issue, task issue, checklist, progress, Projects derived-view 규칙
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
  - remaining work → work item materialization and PM update contract
- Create: `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`
  - evidence-backed card template
- Create: `.github/ISSUE_TEMPLATE/01-goal-playable-slice.yml`
  - Base 자체 및 프로젝트 adapter용 Goal/Slice form
- Create: `.github/ISSUE_TEMPLATE/02-independent-work-item.yml`
  - 독립 작업 form
- Create: `tests/test_project_work_kanban_checklist_contract.py`
  - owner 연결, 상태·진행률·evidence·non-goal 회귀 검사
- Create or modify only when required by existing registry/reference rules:
  - documentation map/reference freshness entries

Implementation 전 exact current owners와 generated/registry 영향 여부를 다시 확인한다. 불필요한 registry, new Skill, JSON schema, workflow 또는 dashboard는 만들지 않는다.

## 16. Acceptance criteria

1. 공용 card template이 authority, scope, dependency, acceptance, checklist, evidence, readback, next action을 제공한다.
2. `[x]`는 PASS에만 사용하고 다른 상태는 완료로 계산하지 않는 규칙이 명시된다.
3. `NOT_APPLICABLE`은 이유와 함께 분모에서 제외되며 `0/0`은 완료가 아니다.
4. Goal/Slice와 independent task의 분리 기준이 명시되어 Issue explosion을 방지한다.
5. existing start checklist가 remaining work를 card/issue queue로 연결한다.
6. existing GitHub lifecycle owner가 Issue/PR/Projects 역할과 WIP를 구분한다.
7. Projects는 optional derived view이고 repository/Issue owner를 대체하지 않는다.
8. evidence level과 overall status가 분리되어 test-only overclaim을 방지한다.
9. no HTML dashboard, no paid provider, no new Skill/schema/workflow가 기본 구현에 추가된다.
10. automated contract test가 owner links, required states, progress rules, WIP, non-goals와 issue forms를 검사한다.

## 17. Validation plan

- TDD: 새 contract test를 baseline에 적용해 RED를 확인한다.
- Markdown/YAML syntax and structural assertions.
- Base relevant focused tests.
- Full local Base validation when environment permits.
- Exact branch HEAD remote CI.
- Independent review and five full-scope adversarial rechecks.
- Current main reconciliation before merge.
- Postmerge readback of all changed owners and templates.

Evidence ceiling:

- 문서·template·contract tests PASS는 작업 운영 계약이 존재함을 증명한다.
- 실제 개별 프로젝트의 카드 생성·Projects board 구성·PM 효율·runtime/UX/Player Experience 개선은 프로젝트 적용 및 사용 evidence 전에는 `NOT_RUN`이다.

## 18. Rollback

이 변경은 공용 운영 계약과 template만 추가한다. rollback은 해당 변경 묶음을 revert하고 기존 start checklist, continuous queue, GitHub lifecycle policy를 유지하는 방식이다. 프로젝트별 Issue나 board를 자동 삭제하지 않는다.

## 19. Risks and mitigations

| Risk | Mitigation |
|---|---|
| 체크리스트가 두 번째 정본이 됨 | owner locator와 readback 필수, 충돌 시 repository truth 우선 |
| 카드 과분할 | independent task criteria와 no-issue-explosion rule |
| 체크만 하고 검증 누락 | PASS-only checkbox와 evidence matrix |
| 보드 설정이 없는 저장소에서 block | Issue/card core, Projects optional |
| field 중복 | issue field/project field duplicate prohibition |
| WIP 관리 비용 증가 | active 1, verify 1, bounded required fields |
| 완료율 게임화 | progress는 summary only, acceptance/evidence gate 유지 |
| 기존 프로젝트 일괄 churn | new/resumed material work부터 적용, no fleet-wide empty artifacts |

## 20. Long-term fit

이 설계는 새 PM 플랫폼을 만들지 않고 현재 Base의 repository-first canon, GitHub work-item lifecycle, continuous queue, development gate를 한 화면에서 소비할 수 있게 연결한다. 운영 surface는 추가되지만 새로운 사실 owner나 runtime schema는 추가하지 않는다. 실제 사용 후 다음 조건에서만 확장을 재검토한다.

- 세 프로젝트 이상에서 동일한 수동 갱신 오류가 반복됨
- Projects API/connector가 안정적으로 쓰기 가능하고 account permission이 확인됨
- card progress 계산을 자동화할 충분한 실제 issue corpus가 생김
- 자동화가 수동 template보다 명확히 낮은 유지비와 더 강한 evidence를 제공함
