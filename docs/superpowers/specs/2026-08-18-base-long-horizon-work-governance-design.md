# Base Long-Horizon Work Governance Refresh Design

## Goal

Base의 기존 Work Contract·Grill Me·연속작업·적대적 검토·Tool Hub·Loop Engineering을 새로 복제하지 않고, 장기 작업에서 누락·충돌·구형 참조가 생기지 않도록 하나의 공용 장기 작업 계약으로 연결한다.

## Why now

2026-08-18 `main` 감사에서 다음을 확인했다.

- `AGENTS.md`는 기획 우선, 무추가비용, Existing Solution First, 연속작업, PR 흡수 계약을 이미 갖고 있다.
- 열린 PR #399의 sparse Skill routing은 현재 main에 아직 없는 유효 delta다.
- PR #460은 #468, #450은 #452, #445는 #446으로 이미 material delta가 흡수된 상태다.
- `docs/LOOP_ENGINEERING_A2_RUNTIME.md`는 2026-08-14의 foundation snapshot을 현재 상태처럼 기술하지만 `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`은 project test executor, PR handoff/postmerge closure, durable resume, REAL subscription Codex transport와 3회 REAL burn-in 완료를 기록한다. 현재 상태 권위가 분리되어 drift가 발생했다.
- Google Sheets는 기존 프로젝트 호환성과 proposal 보존 계약이 광범위하게 연결되어 있으므로 즉시 삭제하면 안전하지 않다. 새 작업은 Figma + repo-native structured data를 기본으로 하고 기존 Sheet는 migration source로 단계적으로 축소해야 한다.

## External evidence applied

- Google Engineering Practices: 작은 self-contained change는 더 철저한 검토, 낮은 bug 위험, 쉬운 merge/rollback을 돕는다.
- DORA: small batch는 software delivery 성과와 연결되고 AI-assisted development의 불안정성을 완화하는 countermeasure다.
- ToolScope (ACL 2026): redundant/overlapping tools는 selection ambiguity를 만들 수 있고 merge/filtering이 실험에서 tool-selection accuracy를 개선했다.
- MetaTool (ICLR 2024): similar-choice·multi-tool selection은 별도 실패 영역이다.
- Godot official docs: Resource는 재사용 가능한 data container이므로 밸런스/설정값을 UI 문서보다 repo-native data로 유지하는 근거가 된다.

외부 근거는 Base 정본이 아니며 Base에서 동일 효과 크기를 주장하지 않는다.

## Architecture

### 1. No new Skill by default

새 Skill 대신 다음 기존 owner를 유지한다.

- intake/approval/continuous work: `managing-project-intake-and-work-contract`
- game OS: `managing-game-project-operating-system`
- adversarial review: `running-adversarial-review-and-refinement`
- Git/PR coordination: `synchronizing-local-and-github-state`
- canonical freshness: `auditing-canonical-reference-freshness`
- archive/supersession: `governing-legacy-retention-and-archives`

새 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`는 이 owner들을 잇는 공용 lifecycle policy이며 독립 Skill이 아니다.

### 2. Long-horizon lifecycle

```text
RESEARCH
→ CURRENT-STATE / OPEN-PR RECONCILIATION
→ DIRECTION / INTENT
→ BENCHMARK SYNTHESIS
→ EXPECTED EFFECTS / RISKS / MITIGATIONS
→ ONE USER APPROVAL
→ SMALL TDD SLICES
→ TOOL HUB / LOOP ENGINEERING WHEN RELEVANT
→ BUILD / RUNTIME TEST
→ FIVE DISTINCT ADVERSARIAL ROUNDS
→ EXACT-HEAD PR GATE
→ MERGE
→ POSTMERGE READBACK
→ LESSON PROMOTION / SUPERSESSION
→ REQUIRED WORK REMAINING = 0
```

`required work remaining = 0`은 승인된 contract acceptance criteria 안에서만 계산한다. external blocker와 optional backlog는 별도 축이다.

### 3. Five distinct adversarial rounds

반복 의식이 아니라 공격면을 분리한다.

1. intent / assumptions / scope distortion
2. canonical ownership / structure / dependency / duplicate authority
3. failure / security / concurrency / recovery
4. player value / industry benchmark / cost / maintainability
5. regression / evidence / completion / postmerge freshness

각 round는 findings, severity, disposition, recheck, unresolved를 기록한다. merge gate는 P0/P1=0을 유지한다.

### 4. Game-work contract

큰 방향을 먼저 사용자와 잡고, 세부 데이터는 GPT 권장 기본값으로 진행하되 값은 parameter/budget으로 외부화한다.

```text
player promise
→ core loop
→ core systems
→ world/storyline fit
→ reusable modules
→ dummy balance budget
→ playable build
→ deterministic/runtime tests
→ tune from evidence
```

벤치마킹은 한 게임을 복제하지 않고 여러 게임·도구·실무사례에서 원리를 분리해 `ADOPT / ADAPT / REJECT` 후 프로젝트 세계관·핵심 경험에 맞게 재해석한다.

### 5. Figma and structured data

New work default:

- visual direction, approved visual references, screen/component/state/prototype collaboration → Figma
- durable rules/decisions → GitHub canon
- balance/economy/schema/runtime configuration → project repo-native JSON/CSV/Godot Resource 등
- Google Sheets → legacy migration/proposal source only until project migration is proven

Sheet를 destructive delete하지 않는다. migration readback, replacement pointers, proposal reconciliation이 끝난 뒤 active workflow에서 제거하고 `[대체됨]`/SUPERSEDED 표시한다.

### 6. Tool surfaces

- Tool Hub는 현재 등록된 로컬 tool의 runtime/health/project binding owner다.
- 외부 HTML tool catalog는 `DERIVED_DISCOVERY_SURFACE`; executable authority나 canon이 아니다.
- Figma는 visual workspace이지 runtime evidence가 아니다.
- Tool/visual state는 `PASS`, `NOT_RUN`, `BLOCKED_*`를 혼동하지 않는다.

### 7. Loop freshness

`docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`을 current operational checkpoint로 사용하고 `docs/LOOP_ENGINEERING_A2_RUNTIME.md`는 foundation/history 문서임을 명시한다. 상태를 두 군데 수동 복제하지 않는다.

## Open PR absorption

- #399: material delta를 latest-main integration branch로 selective copy한다. old head의 failed broad checks를 그대로 성공으로 간주하지 않고 latest-head CI로 재검증한다.
- #460/#450/#445: successor merge로 material delta가 사라진 경우 superseded 처리한다.
- #369/#384: current main implementation과 비교해 unique material delta가 남는 경우만 보존한다.
- #496: unrelated dependency update는 이 contract에 흡수하지 않는다.

## Safety / cost

`ZERO_INCREMENTAL_COST_REQUIRED` 유지. GPT Pro와 Figma Pro 구독 범위 외 pay-as-you-go API, 추가 SaaS, 신규 유료 runner/credit을 도입하지 않는다.

## Success criteria

- 항상 읽히는 Base entry rule에서 long-horizon policy를 찾을 수 있다.
- sparse Skill routing guide와 regression이 latest main 기준으로 green이다.
- 5 distinct review rounds가 machine-checkable contract로 존재한다.
- core-loop/budget/story/reuse/build-test 계약이 존재한다.
- Figma default + repo-native structured data + Sheet migration boundary가 명시된다.
- stale Loop status doc가 current operational checkpoint를 잘못 덮어쓰지 않는다.
- exact-head required checks가 pass하고 postmerge main readback을 수행한다.
- 승인 범위의 required work remaining이 0이고 blocker/optional backlog는 별도 보고된다.
