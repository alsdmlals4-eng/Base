# Base 작업 구조·Skill 동시작업 안전성 적대적 감사

## 0. 판정 요약

- 감사일: 2026-08-13
- 고정 기준: `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- Work Mode: `PLAN → BUILD → REVIEW`
- Existing Solution First: `ABSORB`
- 적용 책임: intake/work-contract, Git sync, adversarial review, change validation
- 적용 Superpowers: brainstorming, writing-plans, isolated-branch substitute, TDD, executing-plans, systematic-debugging, verification-before-completion, review/integration gate
- 결론: 새 Skill·Work Mode·lock service를 만들지 않고 기존 `synchronizing-local-and-github-state`에 identity-bound·phase-bound `CONCURRENT_CHANGE_PREFLIGHT`를 흡수한다.
- 동시작업 보호: PR #312가 소유한 파일은 수정하지 않았다. README의 stale ACTIVE Skill 표기는 #312 comment로 전달했다.
- 증거 한계: connector 기반 GitHub 정본·PR·Actions를 사용했다. 로컬 checkout, 전체 tracked byte inventory, `git fsck`, 로컬 full validation, Godot runtime/render는 `BLOCKED_UNVERIFIED`다.
- 최종 판정 방식: PR #313 exact reviewed HEAD의 모든 적용 workflow와 post-merge main readback에 결합한다. 이 문서가 자기 자신의 최종 commit SHA를 고정값으로 주장하지 않는다.

## 1. 현행 Base 구조

### 1.1 권한과 정본

```text
최신 사용자 요청
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ Active Context·확정 결정·승인 계약
→ 분야 정본·코드·데이터·Scene·자산·Test
→ 프로젝트가 채택한 Base 사본
→ Base 원격 정본
→ 외부 공식 근거·사례
→ 과거 대화·추정
```

| 책임 | Base 정본 |
| --- | --- |
| 항상 적용 규칙 | `AGENTS.md` |
| 작업 생명주기·상태·증거 | `docs/OPERATING_MODEL.md` |
| PLAN/BUILD/REVIEW·Skill 라우팅 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` |
| 문서 역할·소비자 지도 | `docs/DOCUMENTATION_MAP.md` |
| ACTIVE Skill 기계 권한 | `skills/SKILL_REGISTRY.json` |
| 사람용 파생 Skill Map | `docs/generated/BASE_ACTIVE_SKILLS.md` |
| 변경 검증 | `reviewing-and-validating-project-changes` + Tests/Actions |
| 적대 검토·사후 감시 | `running-adversarial-review-and-refinement` |
| Git 상태·전달 | `synchronizing-local-and-github-state` |

### 1.2 Work Mode와 Skill

현행 Work Mode는 세 개다.

```text
PLAN   → 의도·근거·범위·승인 고정
BUILD  → 승인 범위 최소 구현·단계 검증
REVIEW → 독립 공격·비판 검증·회귀·판정
```

Registry-derived ACTIVE Skill 관찰값은 `30`개다. 수는 설계 목표나 상한이 아니며 trigger가 맞는 최소 Skill만 지연 로딩한다. 이번 변경은 네 번째 Work Mode나 31번째 ACTIVE Skill을 만들지 않는다.

### 1.3 구조 강점

- Registry 기반 최소 Skill 선택
- Skill body와 reference의 점진적 공개
- exact-SHA 검증과 Required Checks
- Loop Engineering의 `TASK_LEASE`, path/semantic resource 개념
- post-change monitor와 post-merge main readback
- Skill body 변경에 Learning Log와 established consumer test를 요구하는 canonical-reference freshness

## 2. 외부 현업·시장 비교

조사일은 2026-08-13이다. 시장 점유율을 추정하지 않고 공식·1차 문서에서 검증 가능한 운영 패턴을 비교했다.

| 비교 대상 | 관찰 패턴 | Base 판단 |
| --- | --- | --- |
| OpenAI Codex | 저장소 지시를 경로에 맞춰 계층적으로 적용하고 실제 tool 결과를 Agent loop 증거로 사용 | 현행 `AGENTS.md` 권한·증거 우선 유지 |
| GitHub Copilot Agent Skills | 관련 Skill을 선택한 뒤 body를 필요할 때 context에 로드 | 새 broad Skill 대신 기존 sync owner에 흡수 |
| Claude Code | Skill on-demand loading, 병렬 세션은 worktree로 파일 편집 격리 | remote branch 격리와 PR/path/semantic preflight 결합 |
| GitHub strict checks / merge queue | 최신 base와 결합된 상태에서 required checks를 검증 | merge 직전 current main + exact reviewed HEAD 재검사 |
| Google Cloud DORA | 작고 독립적이며 testable한 batch와 짧은 Branch가 피드백·복구를 지원 | PR #312와 비중첩인 최소 책임 변경 유지 |

Primary references:

- OpenAI, *Unrolling the Codex agent loop* (2026-01-23): https://openai.com/index/unrolling-the-codex-agent-loop/
- GitHub Docs, *Adding agent skills for GitHub Copilot*: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- GitHub Docs, *Available rules for rulesets*: https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Docs, *Managing a merge queue*: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- Anthropic, *How Claude Code works*: https://code.claude.com/docs/en/how-claude-code-works
- Anthropic, *Run parallel sessions with worktrees*: https://code.claude.com/docs/en/worktrees
- Google Cloud DORA, *Working in small batches*: https://dora.dev/capabilities/working-in-small-batches/
- Google Cloud DORA, *Continuous integration*: https://dora.dev/capabilities/continuous-integration/

## 3. 적대적 finding

### F-01 — README ACTIVE Skill drift

- 분류: `CONFLICTING_SOURCE / STALE_CONSUMER`
- 증거: generated Registry view는 ACTIVE Skill `30`, README는 `27`과 수동 목록을 유지한다.
- 위험: cold start와 감사에서 오래된 목록이 정본처럼 보인다.
- 충돌 검토: README는 열린 PR #312의 변경 경로다. 이 PR에서 바로 고치면 병렬 writer가 된다.
- 조치: #312에 생성 Map 연결 또는 정합성 갱신을 요청했다.
- 상태: `WAITING_RESOURCE`; PR #313은 README를 수정하지 않는다.

### F-02 — 일반 Git sync가 Loop resource 정보를 소비하지 않음

- 분류: `MISSING_CONSUMER / CONTRACT_GAP`
- 변경 전: DIRTY, ahead/behind, DIVERGED 판정 중심.
- 누락:
  1. open/recent same-goal PR
  2. PR별 changed paths
  3. semantic resource overlap
  4. source main과 current main 이동
  5. 증거를 읽지 못했을 때 fail-closed 판정
- 조치: 기존 Skill의 `inspect`에 `CONCURRENT_CHANGE_PREFLIGHT`를 흡수하고 safe-sync protocol에 write/PR/merge/post-merge 재검사를 추가했다.

### F-03 — 새 broad Skill 또는 중앙 lock service

- 분류: `REJECTED_CRITIQUE / DUPLICATE_RESPONSIBILITY`
- 공격안: 동시작업 전용 ACTIVE Skill, scheduler, 강제 lock server 신설.
- 기각 근거:
  - 기존 sync owner와 Loop Control Plane이 이미 있다.
  - 새 Skill은 Registry·routing·문서·test 소비자를 중복한다.
  - lock service는 인증·가용성·stale lease·복구 운영비를 만든다.
- 결론: 현재 증거로는 과잉 설계다. 실제 충돌 사례가 누적될 때 별도 제안으로 재평가한다.

### F-04 — 현재 PR self-conflict

- 분류: `AMBIGUOUS_IDENTITY`
- 공격: same-goal/open PR 비교가 현재 PR 자체를 포함하면 자신을 `DUPLICATE_WORK`로 판정한다.
- 조치: `current_task_or_pr_identity`를 필수화하고 비교에서 현재 Task/PR을 제외한다. identity가 불명확하면 `BLOCKED_UNVERIFIED`다.

### F-05 — 첫 write parent와 최종 reviewed HEAD의 의미 충돌

- 분류: `PHASE_CONFLATION`
- 공격: 첫 write 전에는 final changed HEAD가 존재하지 않는다. 한 필드로 parent와 reviewed head를 표현하면 stale Branch overwrite가 가능하다.
- 조치:
  - 첫 write 전: `write_parent_sha` + `expected_head_sha: PENDING_FIRST_WRITE`
  - write 성공 뒤: 반환 commit을 exact `expected_head_sha`로 기록
  - 후속 write 전: Branch reread 뒤 이전 head를 새 `write_parent_sha`로 승격
  - PR/CI/merge: exact reviewed `expected_head_sha`에 결합

### F-06 — standalone test만 추가하고 기존 consumer·Learning Log를 누락

- 분류: `MISSING_CONSUMER / LEARNING_GAP`
- 발견 경로: 첫 통합 후보에서 Base v9 focused suite는 통과했지만 Game Project Operating System workflow의 canonical-reference freshness가 실패했다.
- 의미: 새 전용 테스트가 있어도 기존 통합 suite와 학습 기록을 갱신하지 않으면 운영체계 전체가 변경을 인식하지 못한다.
- 부적절한 우회:
  - `.github/reference-freshness.json`을 약화
  - 허용 목록의 관련 없는 테스트를 형식적으로 수정
  - Learning Log 없이 검사만 재실행
- 조치:
  - `skills/synchronizing-local-and-github-state/LEARNING_LOG.md` 추가
  - GPT/Codex handoff·Git authority·exact-head·merge를 이미 소유하는 `tests/test_gpt_codex_workflow_contract.py`에 통합 회귀 추가

### F-07 — 감사 범위 한계

- 분류: `BLOCKED_UNVERIFIED`
- 확인됨: 권한 지도, Registry-derived Skill Map, 관련 Skill/reference/tests, PR/open-path inventory, exact-head Actions.
- 미확인: 로컬 전체 tracked byte inventory, `git fsck`, local full validation, Godot runtime/render, repository settings UI.
- 방어: “Base 전체 파일을 byte 단위로 읽었다”고 주장하지 않는다. 정본·참조·영향 지도와 Actions/post-merge readback으로 범위를 명시적으로 보완한다.

## 4. 변경 전후

| 항목 | 변경 전 | 변경 후 |
| --- | --- | --- |
| 현재 작업 식별 | 없음 | `current_task_or_pr_identity`, self 제외 |
| 기준 SHA | local/remote HEAD·ahead/behind | source main, current main, write parent, reviewed head 분리 |
| 첫 write | final HEAD 의미 불명확 | `write_parent_sha` + `PENDING_FIRST_WRITE` |
| 후속 write | Branch 이동 재검사 불명확 | 반환 commit 고정 → reread → 다음 parent |
| 열린 PR | 일반 sync 계약에 없음 | same-goal open/recent PR + changed paths 필수 |
| 충돌 단위 | path/history 중심 | `PATH_OVERLAP`와 `SEMANTIC_OVERLAP` 분리 |
| 중복 구현 | 명시 상태 없음 | `SAME_GOAL → DUPLICATE_WORK` |
| main 이동 | merge 전 contract 불명확 | `STALE_BASE_SHA`, reconcile 뒤 재검사 |
| 증거 부재 | 동시작업 ceiling 불명확 | `UNKNOWN + BLOCKED_UNVERIFIED` |
| 조정 | 충돌 뒤 merge/rebase | write 전 비중첩 축소·owner PR coordination·handoff/release |
| 병합 증거 | Required Checks 중심 | exact reviewed HEAD + current main + PR/resource 재검사 |
| 병합 후 | HEAD 대조 | main readback + same-goal/canon/consumer 감사 |
| 학습·통합 소비자 | 새 test만으로 누락 가능 | dedicated test + established workflow test + Skill Learning Log |
| 구조 복잡도 | 3 Work Modes, 30 ACTIVE Skills | 그대로 유지 |

## 5. TDD·디버깅 증거

### RED 1 — 생산 계약 누락

```text
head: acb59559701f90ceb835a8a271c630058b863696
workflow run: 31653620789
job: 94303084090
focused tests: 327
failures: 2
skipped: 1
```

실패는 preflight와 first-write recheck 누락 두 건에 한정됐다.

### RED 2 — 적대 검토로 identity/SHA phase 누락 재현

```text
head: dc120e173922d97b610c115f82ba683d9c32157d
workflow run: 31654086012
job: 94304547739
focused tests: 327
failures: 2
skipped: 1
```

실패는 current identity와 write-phase 계약 두 건에 한정됐다.

### RED 3 — canonical-reference freshness consumer 누락

```text
head: 617778650deb644e0b549fc675ed942c786a6389
Validate Base v9 Operating Contracts: PASS
focused tests: 327 PASS, 1 configured Godot skip
Validate Game Project Operating System: FAIL
run: 31654405601
job: 94305570328
failing step: Check canonical reference freshness
```

실패 원인은 established test companion과 Learning Log 누락이었다. 구현 의미를 약화하지 않고 두 소비자를 추가했다.

### 최종 GREEN Gate

- PR #313 final exact head의 모든 적용 workflow 성공
- Base v9 focused suite와 generated/integrity gate 성공
- Game Project Operating System의 canonical-reference freshness 포함 전체 gate 성공
- PR #312와 changed-path 교집합 0
- unresolved review thread 0
- current main freshness와 mergeability 재확인
- squash merge 뒤 new-main readback 및 post-merge Actions 확인

## 6. 변경·보호 범위

### 변경 경로 9개

```text
docs/audits/2026-08-13-base-work-structure-adversarial-audit.md
docs/superpowers/plans/2026-08-13-concurrent-sync-preflight.md
docs/superpowers/specs/2026-08-13-concurrent-sync-preflight-design.md
skills/synchronizing-local-and-github-state/LEARNING_LOG.md
skills/synchronizing-local-and-github-state/SKILL.md
skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md
tests/test_concurrent_git_sync_preflight_contract.py
tests/test_gpt_codex_workflow_contract.py
tests/test_v9_machine_contracts.py
```

### 보호 경로

```text
README.md
START_HERE.md
docs/DOCUMENTATION_MAP.md
AGENTS.md
docs/OPERATING_MODEL.md
skills/SKILL_REGISTRY.json
docs/generated/**
.github/workflows/**
schemas/**
base*.lock.json
PR #312의 visual/Figma/shared-tool 경로
```

## 7. 기대 효과·비용·남은 위험

### 기대 효과

- 다른 채팅·Agent의 active writer를 첫 write 전에 발견한다.
- 파일이 달라도 같은 Canon·Schema·generated derivative·Scene·asset family 충돌을 판정한다.
- 현재 PR self-conflict 없이 실제 same-goal 경쟁 PR을 차단한다.
- stale work Branch, stale main, 이전 HEAD의 CI 재사용을 차단한다.
- 증거를 읽지 못한 상태를 안전한 상태로 포장하지 않는다.
- 전용 회귀, 기존 통합 회귀, Learning Log가 같은 계약을 소비한다.
- 기존 3 Work Modes·30 ACTIVE Skills·Registry routing을 유지한다.

### 비용과 위험

- write/PR/merge 전 GitHub 조회와 coordination 단계가 늘어난다.
- cooperative 계약이므로 이를 무시하는 외부 도구를 강제로 막지는 못한다.
- semantic resource 선언 품질이 낮으면 false positive/negative가 생길 수 있다.
- README drift 해결은 PR #312의 반영·병합에 의존한다.
- repository ruleset/merge queue 설정 강제화는 이번 범위가 아니다.

## 8. Rollback

PR #313의 squash merge commit 하나를 revert한다.

- 데이터·Schema migration 없음
- Registry·generated artifact 변경 없음
- dependency·workflow·repository setting 변경 없음
- project-specific 동기화 없음

## 9. Base 승격 판정

- 공용 교훈: `동시 AI 작업은 current work identity + exact write parent + Git topology + open PR paths + semantic resources + same Goal + current main freshness를 persistent write 전에 함께 판정한다.`
- 프로젝트 고유 내용: 없음
- 후속 후보: 실제 충돌/false-positive 기록이 누적될 때 semantic resource naming fixture 또는 machine-enforced lease를 별도 BCP로 검토한다.
