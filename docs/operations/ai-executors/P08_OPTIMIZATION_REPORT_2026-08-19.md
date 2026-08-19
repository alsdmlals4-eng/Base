# P08 · AI Operations & External Executors — Optimization Report (2026-08-19)

## Baseline

```yaml
part_id: P08
baseline_main: df8ef644d30fc96456da23a5157e5efb61b620bb
branch: opt/base-part-P08-ai-operations-tightening
pr: 535
runtime_model: ONE_BASE
new_active_skills: 0
new_paid_dependencies: 0
```

P08은 Base의 AI 작업에서 **Instruction/Context → Model/Cost → Source Research → External AI Worktree → Optional Executor → Evidence Review** 연결을 전문적으로 유지하는 Maintenance / Specialization View다. P01의 GPT/Codex 역할 정본, P03의 Git/worktree 격리, P07의 검증 권위, CP0의 Partition/Registry/Workflow는 읽기 전용 의존성이다.

## 중요 규칙 감사

| Rule | Canonical source / owner | 보장하는 것 | Finding | Disposition |
|---|---|---|---|---|
| `GPT_FIRST_PLANNING_AND_REVIEW` | P01 `GPT_CODEX_WORKFLOW_POLICY.md` | GPT가 기본 계획·검수 책임자이며 Codex를 자동 다음 단계로 만들지 않음 | P08 external-AI Skill이 Codex 검수를 고정해 authority drift 발생 | `IMPROVE` — P08 consumer 정렬 |
| `OPTIONAL_CODEX_EXECUTOR` | P01 + P08 consumer | 실제 filesystem/runtime/build 권위가 필요할 때만 Codex 사용 | 문서/외부 AI 검수까지 Codex가 의무처럼 보임 | `IMPROVE` |
| `ZERO_INCREMENTAL_COST_REQUIRED` / `GPT_PRO` | Base invariant + P08 model-cost | 새 종량제 비용의 암묵적 활성화 방지 | 구독 포함 사용량과 credits/API의 표면 구분이 약함 | `IMPROVE` — `COST_SURFACE_GATE` |
| `DEFAULT_SUPPORTING_SKILL_BUDGET: 1` | `SKILL_ROUTING_PRECISION_GUIDE.md` | 겹치는 Skill의 과잉 fan-out 방지 | Skill에는 강하지만 Tool에는 명시적 current-stage gate가 없음 | `IMPROVE` — `TOOL_SHORTLIST_JUST_IN_TIME` |
| external AI = `REVIEW_PENDING` | `orchestrating-deepseek-worktrees` | 외부 모델 결과를 canon으로 직접 승격하지 않음 | 유지 가치 높음 | `KEEP` + rehydration 강화 |
| exact current canon before mutation | Base hierarchy + P01/P03 | stale handoff가 실제 저장소를 덮지 않음 | external executor에 명시적 실행 직전 gate 부족 | `IMPROVE` — `EXECUTOR_REHYDRATION_GATE` |

삭제한 중요 규칙은 없다.

## Skill / Mode 감사

### `orchestrating-deepseek-worktrees`

```yaml
mode: external-ai-worktree orchestration
trigger: external-ai | large-draft | isolated-worktree
responsibility: 외부 AI의 대량 초안/분류를 격리하고 REVIEW_PENDING 결과로 회수
inputs: canon allowlist, exact base, write/protected paths, output/review contract
outputs: isolated worktree result, evidence/assumptions, reviewer handoff
status: ACTIVE
disposition: IMPROVE
```

핵심 변경:

- `GPT_PRIMARY_REVIEWER`
- `OPTIONAL_CODEX_EXECUTOR`
- `EXECUTOR_REHYDRATION_GATE`
- provider 이름이 달라졌다는 이유만으로 별도 Skill을 만들지 않음
- 실제 executor가 시작 직전 `AGENTS.md`, current canon, exact branch/commit, protected paths, tests를 다시 읽음

Skill ID를 provider-neutral 이름으로 즉시 바꾸는 안은 **기각**했다. 기존 Registry/consumer/template/tool/schema migration의 blast radius가 크고, 현재 문제는 이름보다 권한·검수 semantics였다.

### `optimizing-ai-model-and-prompt-costs`

```yaml
modes:
  - route-model-and-effort
  - design-cacheable-prefix
  - estimate-cost
  - measure-actual-usage
  - recalibrate
status: ACTIVE
disposition: IMPROVE
```

기존 5개 mode는 유지한다. 새 mode/Skill 대신 mode 실행 전 `COST_SURFACE_GATE`를 추가했다.

```text
SUBSCRIPTION_INCLUDED
SEPARATELY_METERED
UNVERIFIED_COST_SURFACE
COST_GATE_BLOCKED
```

`GPT_PRO` 포함 사용량에서 별도 billing 계산이 필요하지 않으면 Context/Skill/Tool/retry 효율만 최적화한다. credits/API/별도 SaaS·compute/storage는 사용자 승인 전 `SEPARATELY_METERED` 기본 경로가 아니다.

### `SKILL_ROUTING_PRECISION_GUIDE`

기존 sparse Skill routing은 유지한다. 새 router Skill을 만들지 않고 Tool selection에 다음 계약만 추가했다.

```text
TOOL_SHORTLIST_JUST_IN_TIME: REQUIRED
```

Skill shortlist와 Tool shortlist를 하나의 숫자 예산으로 합치지 않는다. Tool은 현재 단계의 정본/실행 기능에 필요한 목적 집합만 선택하며, 정확성을 위해 서로 다른 정본 도구가 둘 이상 필요하면 그대로 사용한다.

## Module 감사

| Module | 책임 | 입력 | 출력 | 연결 / 검증 | Disposition |
|---|---|---|---|---|---|
| AI Instruction / Context | 권위 계층, Prompt contract, context curation | user intent, canon, current decision | work package/context pack | P01 intake, P07 evidence | `KEEP` |
| Model / Cost Routing | 품질 위험·모델·비용 surface 판단 | task risk, provider facts, cost surface | model/cost checkpoint | current provider official source | `IMPROVE` |
| Source / Research Operations | source discovery를 현재 결정에 필요한 evidence로 바꿈 | source radar, current question | ADOPT/ADAPT/TEST/etc. | Learning system | `KEEP` |
| External AI Worktree Orchestration | 대량 외부 AI 결과 격리 | canon allowlist, base SHA, worktree | REVIEW_PENDING result | P03 isolation, P07 review | `IMPROVE` |
| Optional Executor Handoff | 실제 실행 권위가 필요한 단계만 executor 사용 | approved contract + current canon | diff/runtime/build evidence | P01 authority | `IMPROVE` |

모듈을 더 쪼개거나 새 orchestration runtime을 만들 필요는 발견되지 않았다.

## 실질 대안

### A. 현행 유지

장점: 변경/회귀 위험 최소.

탈락 이유: P08 consumer의 hard-coded Codex reviewer, cost surface ambiguity, external-executor stale-context 위험이 남는다.

### B. 기존 2 Skill 유지 + 의미 경계만 강화 — 선택

- Skill/Mode 수 증가 없음
- P01/P03/P07 owner를 침범하지 않음
- P08 consumer만 현재 Base authority에 정렬
- 추가비용 경로를 fail-closed
- Tool overload는 별도 시스템 대신 sparse just-in-time contract로 흡수

장기 적합성이 가장 높다.

### C. provider-neutral executor subsystem 전면 재구성

예: Skill ID/branch/template/schema/tool을 `external-ai-*`로 모두 migration.

장점: 용어 일관성.

탈락 이유: CP0/Registry, template/tool/schema/test owner, P03/P07 consumer까지 건드리는 cross-Part migration이 필요하다. 현재 확인된 사용자 가치는 이름 변경보다 실행 권한과 freshness 보장이다.

### D. 동적 Skill/Tool retriever 또는 새 orchestration service 구축

장점: 매우 큰 Skill/Tool pool에서 자동 후보 축소 가능.

탈락 이유: 현재 Base는 이미 sparse Registry와 trigger/negative-trigger/tie-break를 갖고 있다. 새 runtime은 context·maintenance·failure surface를 늘리며 실측 model-run bottleneck 증거가 없다.

## Better Alternative Search / Long-term fit

벤치마크를 다시 대입해도 B가 유지된다.

- Tool 겹침 문제는 새 Tool을 추가해서 해결하지 않는다.
- context 부족은 giant prompt가 아니라 repository canon + just-in-time hydration으로 해결한다.
- external executor diversity는 provider별 Skill proliferation보다 하나의 isolation contract가 낫다.
- 비용은 가격표 최적화보다 **포함 구독 surface와 별도 종량제를 먼저 분리**해야 현재 사용자 정책에 맞는다.

재검토 조건:

- 외부 executor가 2개 이상 정기 운영되고 DeepSeek-specific naming 때문에 실제 routing 오류가 반복됨
- Base Skill/Tool pool이 커져 sparse metadata + tie-break만으로 오선택이 model-run eval에서 증가함
- GPT/Codex product의 구독/credits 정책이 변경됨
- external worktree template/tool/schema의 owner가 CP0 Integration에서 재분류됨
- 현재 P08 계약이 runtime/build evidence를 막거나 중복 executor handoff를 유발함

## Source disposition

| Source | Finding | Disposition |
|---|---|---|
| OpenAI — Harness engineering | giant instruction manual보다 repository knowledge/system-of-record와 검증 가능한 harness가 중요 | `ADAPT` — current canon + just-in-time context |
| OpenAI — Unrolling the Codex agent loop | instruction/tool output/task state가 같은 context를 소비 | `ADAPT` — 불필요 Tool/context 선로딩 금지 |
| OpenAI Help — Codex with ChatGPT plan / flexible credits | Pro에는 Codex 포함 사용량이 있으나 credits는 한도 이후의 pay-as-you-go add-on | `ADOPT` — `SUBSCRIPTION_INCLUDED` vs `SEPARATELY_METERED` |
| Anthropic — Writing effective tools for agents | 목적이 겹치거나 과도한 Tool은 agent 선택을 방해할 수 있음 | `ADAPT` — Tool shortlist |
| Anthropic — Effective context engineering | context는 유한 자원이며 just-in-time retrieval이 중요 | `ADAPT` |
| Git `git-worktree` official docs | 한 repository에서 linked worktree로 branch 작업을 격리 가능 | `ADOPT` — isolation mechanism only; authority는 별도 |
| ToolScope ACL 2026 | 중복/겹침 Tool filtering/merging 효과 보고 | `REFERENCE_ONLY` — Base 정확도 개선율로 직접 일반화하지 않음 |
| SkillRouter 2026 | close Skill 후보에서 full body reranking이 강한 신호 | `REFERENCE_ONLY` — 현재 tie-break 근거, Base 수치효과 `NOT_RUN` |

## Cross-Part / CP0 requests

### Request 1 — external AI contract artifact ownership

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P08
  target_owner: CP0
  target_paths:
    - templates/ai/DEEPSEEK_WORK_PACKAGE.md
    - templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md
    - tools/check_external_ai_worktree_contract.py
    - schemas/external-ai-worktree-contract-v1.schema.json
    - tests/test_external_ai_worktree_contract.py
  reason: P08 Skill의 직접 companion contract인데 현재 P08 owned_write_paths/allowed_new_paths에 없음
  evidence: orchestrating-deepseek-worktrees가 이 Template/contract/checker를 직접 소비
  required_semantic_change: P08 ownership으로 재분류하거나 명시적 read-only owner/Integration 변경 경계를 선언; reviewer 명칭은 GPT-primary/optional-Codex와 충돌하지 않게 provider-neutral화
  acceptance_criteria:
    - single canonical owner
    - no semantic path overlap
    - existing checker/test remains green
  blocking: false
```

현재 Skill에서 template의 `Codex 인계` 문구는 Codex가 실제 optional executor일 때만 literal로 해석하고, GPT 검수 시 동일 field를 responsible-reviewer handoff로 해석하는 compatibility rule을 둬 즉시 동작 충돌을 차단했다.

### Request 2 — generated Codex plugin ownership

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P08
  target_owner: CP0
  target_paths:
    - .codex-plugin/plugin.json
    - tools/build_base_v9_artifacts.py
    - tests/test_v9_registry_generation.py
  reason: Manifest는 .codex-plugin/**를 P08 write path로 두지만 plugin.json은 CP0 generator/release-lock에서 생성·검증되는 derivative
  evidence: current plugin active_skill_count=27 is released v9 lock identity while generated current skill map=30; generator test intentionally preserves this separation
  required_semantic_change: direct P08-editable source인지 CP0/generated derivative인지 owner semantics 명시
  acceptance_criteria:
    - no direct-edit ambiguity
    - released lock identity preserved
    - current registry view and released plugin snapshot remain distinguishable
  blocking: false
```

`plugin.json`은 이번 PR에서 수정하지 않았다.

### Request 3 — P08 focused test CI discoverability

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P08
  target_owner: CP0
  target_paths:
    - .github/workflows/**
    - tests/test_p08_*.py
  reason: tests/test_p08_ai_operations_contract.py는 P08 allowed_new_path지만 최초 RED commit에서 기존 selected CI suite가 이 파일을 실행하지 않음
  evidence: PR #535 initial exact head e5da92bd4fba4ad5e4d93afb32e3b2906ef8e35a에서 general workflows가 새 test를 선택 실행하지 않음
  required_semantic_change: future Integration에서 P08 focused suite 또는 existing relevant workflow가 tests/test_p08_*.py를 실제 실행하도록 검토
  acceptance_criteria:
    - no broad full-suite cost explosion
    - changed P08 contract test is executable in CI
  blocking: false
```

P08는 `.github/**`를 직접 수정하지 않는다.

## Full adversarial improvement loops

각 loop는 P08 전체 intent, authority, rules, Skills/Modes, modules, consumer docs, cost/security, source evidence, ownership, tests, rollback, long-term fit을 다시 확인했다.

### Loop 1 — baseline full attack

Valid findings:

1. External-AI Skill이 Codex 검수를 고정 → GPT-primary authority와 충돌.
2. external executor가 handoff 이후 변경된 canon을 재수화하는 명시 gate 부족.
3. model-cost Skill이 GPT Pro 포함 사용량과 credits/API의 별도 비용 surface를 먼저 분리하지 않음.
4. sparse Skill routing은 강하지만 Tool overload에 같은 current-stage 원칙이 명시되지 않음.

Fix: 세 P08 canonical owner에 bounded semantic tightening. 새 Skill/Mode/runtime 없음.

### Loop 2 — improved state full re-attack

Finding: `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`의 Godot 구현/협업 예시가 여전히 Codex Plan→Build를 표준 직렬 단계처럼 보여 새 Skill contract와 consumer drift 발생.

Fix: Guide를 `GPT_FIRST_PLANNING_AND_REVIEW` + `OPTIONAL_CODEX_EXECUTOR`와 `COST_SURFACE_GATE`에 정렬. 기존 Eval/security/license 내용은 유지.

### Loop 3 — ownership / consumer / generated-artifact full re-attack

Findings:

- P08 external-AI Skill companion Template/checker/schema/test의 owner가 Manifest에 직접 표현되지 않음.
- `.codex-plugin/**`는 P08 write path지만 `plugin.json`은 CP0 generator/release-lock derivative라 direct-edit 의미가 모호함.
- 신규 `test_p08_*`는 allowed path이나 현재 selected CI에서 자동 실행되지 않음.

Fix: P08 범위를 넘지 않고 세 건 모두 CP0 `CROSS_PART_CHANGE_REQUEST`로 격리. 현재 실행 semantics는 compatibility rule로 fail-closed. generated plugin 직접 수정 금지.

### Loop 4 — external benchmark / security / cost full re-attack

- OpenAI current plan/credits documentation으로 included usage와 extra credits가 별도임을 재확인.
- Anthropic current tool/context guidance로 Tool shortlist와 just-in-time context의 방향을 재검증.
- Git 공식 worktree 문서로 isolation mechanism을 재확인.
- Secret/API key/auto top-up activation 없음.
- provider API/SaaS/credits 구매 또는 호출 없음.
- ToolScope/SkillRouter 연구 수치를 Base model-accuracy 숫자로 승격하지 않음: `NOT_RUN` 유지.

New MUST_FIX: 0.

### Loop 5 — full diff / scope / regression / rollback / long-term re-attack

- current main은 baseline SHA에서 변하지 않았는지 merge 직전 다시 확인하도록 gate 유지.
- 변경 경로는 P08 `owned_write_paths` 또는 `allowed_new_paths`로만 제한.
- 다른 Part branch/PR/Notion page 수정 없음.
- active Skill count/Registry/CP0/workflow/schema/runtime 변경 없음.
- 롤백은 PR #535 squash merge revert 한 단위로 가능하며 project/game data migration 없음.
- 더 나은 대안 탐색에서 C/D를 다시 비교했으나 현재 measured blocker 없이 구조를 확대하는 비용이 더 큼.

New validated MUST_FIX: 0.

```yaml
FULL_LOOP_COUNT: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: satisfied
new_valid_MUST_FIX_after_loop_5: 0
blocking_finding: 0
canonical_conflict: 0
ownership_conflict_within_P08_write_scope: 0
cross_part_nonblocking_requests: 3
acceptance_failure: 0
unsupported_PASS: 0
CLEAN_REVIEW_EXIT: CONDITIONAL_ON_FINAL_EXACT_HEAD_CI_AND_POSTMERGE_READBACK
```

## Validation / evidence ceiling

### Directly observed

- baseline/latest-main readback from GitHub
- exact PR diff/readback
- P08 Notion page read
- current official external benchmark sources read
- changed paths are all P08-owned/allowed by Manifest inspection
- new paid dependency/API call/provider call: none

### CI / focused tests

- initial `test_p08_*` RED was **not executed by selected CI**, so no RED PASS/FAIL is claimed.
- final Required workflows and exact-head state are recorded on PR #535 after the last content commit.
- `tests/test_p08_ai_operations_contract.py` remains a focused executable contract for future local/CI discovery.

### NOT_RUN

- local repository `python tools/check_base_partition_scope.py ...` command: local clone unavailable in this session because `github.com` DNS resolution failed in the container.
- local `python -m unittest discover -s tests -p 'test_*model*.py' -v`: same reason.
- external model behavior/model-selection accuracy eval.
- provider billing/cache-hit measurement.
- real DeepSeek/Codex worktree execution for this docs/policy-only change.

No NOT_RUN item is reported as PASS.

## Rollback

Revert PR #535 squash merge as one unit. No project save/data/schema migration, runtime asset mutation, paid service activation, credential change, external worktree deletion, or CP0 Registry change is part of this PR.
