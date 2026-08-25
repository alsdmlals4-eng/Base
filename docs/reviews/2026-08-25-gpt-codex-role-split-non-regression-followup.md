# GPT–Codex 역할 분리 · Non-Regression Follow-up — 2026-08-25

이 문서는 `docs/reviews/2026-08-25-gpt-codex-role-split-adversarial-review.md`의 후속 전체 재공격 기록이다. 작업지시문 revision은 현재 범위가 아니다.

## 왜 후속 검토가 필요했나

첫 역할 분리 교정은 방향 자체는 맞았지만, `docs/GPT_CODEX_WORKFLOW_POLICY.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`, Handoff Skill/Reference를 원본 대비 diff로 재공격하자 **역할과 무관하게 보존해야 할 실행·복구·handoff safety가 과도하게 축약된 실제 finding**이 발견됐다.

이 finding은 구형 test가 낡았다는 이유만으로 무시할 수 없다.

## Loop 6 — Canonical policy non-regression

### 발견

첫 rewrite에서 다음 capability가 약화됐다.

- `CONTINUOUS_WORK_EXECUTOR_HANDOFF`와 executor unavailable 시 국소 `DEFERRED_EXTERNAL_EXECUTOR`
- HiGodot 등 project persistent authoring authority 보존
- stale PID/session·wrong target·dirty/diverged·destructive Git 방지
- Codex Plan의 명시적 write 금지 범위
- L2+ 마스터 구현계획·package dependency·rollback
- Push 전후 actual change inventory / remote HEAD
- 동일 승인 범위의 무재승인 병합 wording

### 교정

`docs/GPT_CODEX_WORKFLOW_POLICY.md`에서 이 capability를 삭제하지 않고 **실행 owner를 Codex로 이동**했다.

```text
OLD
GPT / user local launcher owns shell/Codex bootstrap safety

NEW
Codex execution environment owns freshness / wrong-target / authoring authority / VCS safety
```

과거 literal `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`, `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`, `ASSUME_PREVIOUS_POWERSHELL_CLOSED`는 safety lineage의 historical/compatibility 이름으로 남기되 GPT local-Codex orchestration을 current default로 복원하지 않는다.

## Loop 7 — Routing lifecycle non-regression

### 발견

첫 routing rewrite에서 역할 분리를 단순화하는 과정에 다음이 줄었다.

- Grill Me 상세 원칙
- REVIEW impact map → finding 분류 → owner route
- Global Progress Queue recovery/defer/continue
- `EVIDENCE_TRANSPORT_INCOMPLETE`
- `CONTINUOUS_WORK_EXECUTOR_HANDOFF` 무재승인 경계
- `GLOBAL_TERMINAL_BLOCKER`의 엄격한 종료 조건
- 병합 exact-head/thread/ruleset 조건
- 실행 보고의 deferred/recovery 상태

### 교정

`docs/WORK_MODE_AND_SKILL_ROUTING.md`를 재작성해 다음을 모두 보존했다.

```text
PLAN = GPT
BUILD = Codex
REVIEW = GPT
```

finding은 responsibility 기준으로 나눈다.

```text
DOC_OR_CANON_CORRECTION → GPT bounded correction
IMPLEMENTATION_CORRECTION → CODEX_IMPLEMENTATION_HANDOFF
USER_DECISION_REQUIRED → user
BLOCKED_UNVERIFIED → recovery/defer
```

`ON_DEMAND_CODEX_HANDOFF` / `USER_REQUESTED_CODEX_HANDOFF` / `기획·구현·POC 누적`은 migration/compatibility 의미를 명시하고 과거 GPT implementation flow를 재활성화하지 않는다.

## Loop 8 — Handoff continuity / post-merge non-regression

### 발견

첫 Handoff Skill rewrite에서 다음 historical/live 상태 분리와 resume safety가 축약됐다.

- `LIVE_CONTINUATION_STATE`
- `PRE_MERGE_SNAPSHOT`
- `OBSERVE_POST_MERGE_TRUTH`
- stale PID/session은 historical evidence일 뿐 current authority가 아니라는 규칙
- `current process, transport ownership, server registration, exact target session` fresh-read
- transport recovery owner 중복 금지
- Cold-start questions / Definition of Ready / Definition of Done / Failure conditions

### 교정

`skills/maintaining-project-context-and-handoff/SKILL.md`에 전부 복원했다.

중요 변경은 역할만 바뀐 것이다.

```text
GPT Handoff planning / final review
→ Codex GitHub + Notion rehydration / implementation
→ GPT final review
```

post-merge historical snapshot, live router, actual remote truth 경계는 유지한다.

## Loop 9 — Package / VCS reference non-regression

`skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`를 다시 검수해 다음을 복원/강화했다.

- 최신 `main`
- read-only Codex Plan
- Plan `file_write: FORBIDDEN`, `commit_push_pr_issue: FORBIDDEN`
- master implementation plan owner = GPT
- package boundary / `SEQUENTIAL`
- Push 전 actual status, overlap, user-change protection
- Push 후 Commit SHA + **원격 HEAD**
- current required checks/ruleset/merge method discovery
- `AUTO_MERGE_AFTER_REQUIRED_CHECKS`
- `AUTO_MERGE_ELIGIBLE`
- `WAITING_GPT_VISUAL`
- GitHub + Notion rehydration
- Codex image-generation prohibition

과거 `godot_runtime_files_only` 같은 지나치게 좁은 공용 Build 제한은 유지하지 않고 `APPROVED_PACKAGE_ONLY`로 일반화했다.

## Loop 10 — Current evidence / stale test distinction

### 현재 판단 기준

실패를 두 종류로 분리한다.

1. **REAL_NON_REGRESSION_FINDING**
   - 역할 변경과 무관한 안전/복구/증거 capability가 실제 사라짐.
   - GPT가 문서 owner 범위에서 즉시 복원.

2. **STALE_CONTRACT_TO_MIGRATE**
   - `GPT_GODOT_PREPRODUCTION_ALLOWED`, `OPTIONAL_CODEX_EXECUTOR`, GPT one-copy/paste local launcher 등 사용자가 명시적으로 폐기한 old behavior를 test가 active requirement로 요구.
   - test를 삭제하지 않고 새 semantic owner/regression으로 Codex가 migration.

### exact-head 상태

이 follow-up 작성 직전 latest document head lineage에서:

- `Validate One-Shot Local Executor Bootstrap`은 여전히 old local-bootstrap contract 때문에 FAIL.
- Base Partition / Skill Routing / Base v9 / Game Project OS는 새 commits에 대해 재실행 중이거나 후속 결과가 필요한 상태.

따라서 `CLEAN_REVIEW_EXIT = false`다.

## 유지 / 강화 / 이동 / 폐기 판정

| Capability | 판정 | 현재 의미 |
|---|---|---|
| 기획·벤치마킹·최소 3안 | KEEP | GPT |
| 적대적 review lifecycle | KEEP | GPT review → owner별 correction route |
| IRG / evidence ceiling | KEEP | 계획·구현·검증 층 분리 |
| Notion human canon | KEEP | GPT/사용자 planning surface |
| GitHub structured/runtime truth | KEEP | Codex implementation + actual evidence |
| Continuous Work recovery | KEEP | BUILD만 Codex executor로 route |
| post-merge snapshot/live-state | KEEP | history overwrite 금지 |
| authoring authority | KEEP | Codex도 project authority 준수 |
| local freshness / wrong-target | MOVE | GPT launcher → Codex execution environment |
| GPT 제품 code/POC implementation | RETIRE | GPT는 planning/review owner |
| user-request-only Codex Build | RETIRE | IMPLEMENTATION_READY가 정상 handoff trigger |
| Codex Plan | KEEP | optional read-only technical preflight |
| Codex Build | STRENGTHEN | implementation/coding owner |
| Codex GitHub-only rehydration | STRENGTHEN | GitHub + Notion 둘 다 필수 |
| Codex image creation/editing | FORBID | GPT visual pipeline only |
| missing visual route | ADD | GPT_VISUAL_REQUEST |
| approved Visual delivery/readback | STRENGTHEN | Notion current-use approval required |
| open independent PR protection | KEEP | read-only |
| exact-head/required-check/thread/merge Gate | KEEP | current repository discovery |

## 현재 상태

```yaml
role_design: APPROVED_BY_USER
canonical_policy_non_regression: IMPROVED_AFTER_FINDING
routing_non_regression: IMPROVED_AFTER_FINDING
handoff_continuity_non_regression: IMPROVED_AFTER_FINDING
package_vcs_non_regression: IMPROVED_AFTER_FINDING
notion_role_alignment: READBACK_CONFIRMED
stale_test_consumer_migration: PENDING_CODEX
work_instruction_revision: DEFERRED_NOT_CANON
clean_review_exit: false
merge_ready: false
```

다음 구현 단계는 Codex가 `docs/handoffs/2026-08-25-gpt-codex-role-split-codex-handoff.md`를 읽고 stale test/registry/generated/secondary active consumers를 새 semantic contract로 migration하는 것이다.