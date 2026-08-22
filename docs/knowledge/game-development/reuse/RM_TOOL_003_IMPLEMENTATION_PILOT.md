# RM-TOOL-003 · Balance Scenario Batch Simulator Implementation Pilot

- 상태: `BASE_REFERENCE_IMPLEMENTED · MULTI_PROJECT_PILOTS_MERGED_MAIN_READBACK`
- 기준일: 2026-08-22 KST
- 계약 owner: `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- 구현: `tools/reuse_modules/balance_scenario_batch_simulator.py`
- 입력 예시: `templates/reuse-modules/BALANCE_SCENARIO_BATCH_MANIFEST.json`
- 회귀: `tests/test_balance_scenario_batch_simulator.py`, `tests/test_balance_scenario_batch_schema.py`, `tests/test_balance_scenario_batch_read_only.py`
- Base reference merge: PR #580 → `8c9a32379244e9de67c72ae949653cd3a16b5746`
- Registry freshness: PR #591 → `e37c4e72344662b344f62a442dd2f7f39dbad34e`

## 1. 현재 구현 판정

`RM-TOOL-003`은 거대 Balance GUI나 게임별 simulator를 Base가 소유하는 구조가 아니다. **project-supplied deterministic run record를 읽기 전용으로 분석하는 작은 공용 kernel**이다.

```text
project-authoritative rules/data
→ project-owned simulator or deterministic adapter
→ run records
→ Base RM-TOOL-003 analyzer
→ distribution / tail / failure / choice / paired-seed / goal-seek report
→ GPT/human review
→ project decision owner
```

Base가 소유하지 않는 것:

- 프로젝트 전투/강화/스폰/경제 규칙
- 프로젝트 runtime state
- 프로젝트 final balance decision
- project data 자동 수정
- 재미/난이도 human PASS

## 2. 공용 kernel 기능

현재 reference implementation은 Python stdlib-only이며 다음을 수행한다.

- per-variant run count
- numeric metric mean / median / min / max / P05 / P25 / P75 / P95
- tail run locator
- run-level failure-tag rate
- choice-event frequency와 dominant choice
- baseline ↔ candidate same-seed paired delta
- bounded non-authoritative goal-seek ranking
- target range 안에 들어온 실제 run 비율
- snapshot/evidence-ceiling provenance 전달
- JSON CLI report

명시적 경계:

```text
mutates_project_data = false
failure_rate_denominator = RUNS_CONTAINING_TAG
choice_share_denominator = TOTAL_CHOICE_EVENTS
percentile_method = LINEAR_INDEX_Q_TIMES_N_MINUS_1
```

## 3. Fail-closed 입력 계약

다음을 거부한다.

- bool/float/string seed의 integer 암묵 변환
- empty/non-string variant
- non-object metrics
- non-list choices/failures/goal_seek
- duplicate `(variant, seed)` pair
- nonnumeric metric
- NaN/Infinity metric 또는 goal target
- 없는 variant를 참조하는 goal-seek
- 잘못된 snapshot/evidence container

반환 report의 `snapshot`과 `evidence_ceiling`은 deep-copy한다.

## 4. 프로젝트 소비자 검증

### OMENWARD · PR #202

- read-only planning envelope Pilot.
- 10,000 deterministic seed 분석에서 normalization 이후 raw envelope 밖 표본을 W1 `1.24%`, W2 `1.93%`, Final `3.44%` 관찰.
- 이는 final balance PASS가 아니라 pre/post-normalization semantics를 명확히 해야 한다는 planning finding이다.
- squash merge `b46374e511447cb531709a5d56f3ba9a6e4dcc8d` 후 main readback.

Evidence ceiling: `PLANNING_ENVELOPE_ONLY · HUMAN_VALIDATION_NOT_RUN · FINAL_PRODUCT_NUMERICS_NOT_APPROVED`.

### BLACKSMITH · PR #181

- project-owned `tools/simulate_enhancement_balance.py`가 rule/run-generation owner다.
- Base는 enhancement rules를 중복 구현하지 않고 post-processor 경계만 제공한다.
- exact head required workflows PASS 후 squash merge `307126031956bf5345da20a7b0c4466aa26c9b94`.

Evidence ceiling: `PROJECT_SIMULATOR_EXISTS · INTEROP_CONTRACT_REVIEWED · FINAL_PRODUCT_BALANCE_NOT_APPROVED`.

### NINJA_SURVIVAL · PR #24

- legacy `WaveSpawner` cap actuator를 initial state `0..8`로 deterministic 검증.
- enabled variant cap violation 0, disabled spawn 0.
- 신규 stage balance data를 발명하지 않았다.
- GUT run `32539901612`: `SUCCESS`; squash merge `46c5e151808f2481cc20be0003dd03866133ae49`.

Evidence ceiling: `LEGACY_MVP3_ACTUATOR_CONTRACT_ONLY · PRODUCT_BALANCE_NOT_EVALUATED`.

## 5. 공용성 판정

| 소비 형태 | 프로젝트 | 결론 |
|---|---|---|
| planning envelope read-only 분석 | OMENWARD | 공용 분포/경계 분석 가치 확인 |
| 기존 project simulator | BLACKSMITH | Base는 post-processor여야 함 |
| deterministic actuator | NINJA_SURVIVAL | run-record 계약은 재사용 가능, 새 수치 발명 금지 |

공용 kernel은 유지 가치가 있고 game-rule simulator는 project-owned가 맞다.

## 6. UI / human-consumption boundary

`NO_TOOL_HUB_OR_BALANCE_GUI_ACTIVE_ROUTE`

현재 승인 경로:

```text
CLI + machine-readable JSON
→ GPT/human analysis
→ 필요할 때 exact Project Notion human summary
```

다음은 현재 active/default/revisit 경로가 아니다.

```text
Tool Hub
새 Electron Balance 앱
외부 HTML dashboard
프로젝트용 별도 local GUI
자동 수치 패치 UI
```

CLI/JSON으로 현재 검증 목적이 충족되며, 별도 UI는 새로운 authority·설치·routing·maintenance cost만 추가한다. **기존 Tool Hub의 thin surface를 재검토하지 않는다.**

향후 사용자가 `Tool Hub 미사용` 결정을 명시적으로 뒤집고, 반복된 실제 프로젝트 병목이 증명되며, Existing Solution First + 최소 3개 실질 대안 + 장기 적합성 검토를 다시 통과한 경우에만 새 human-consumption surface를 별도 기획한다.

## 7. 다음 프로젝트 적용 규칙

```text
project canon/runtime owner 확인
→ existing project simulator/runner 우선
→ deterministic run-record adapter 필요성 판단
→ Base analyzer 실행
→ report evidence ceiling 확인
→ GPT/human 해석
→ 필요한 human summary는 Notion
→ project canon 변경은 별도 승인/검증
```

`RM-TOOL-003` 존재 자체는 project balance PASS, 재미 PASS, 자동 패치 권한을 주지 않는다.

## 8. 검증·완료 상태

기존 구현 과정의 5회 전체 적대적 개선에서 finite-only metric, failure denominator, target-share, strict seed/schema, deep-copy read-only 경계를 확정했다.

```yaml
FULL_LOOP_COUNT: 5
BASE_KERNEL_VALID_MUST_FIX_REMAINING: 0
RM_TOOL_003_BASE_KERNEL: BASE_REFERENCE_IMPLEMENTED_MERGED
OMENWARD_PR_202: MERGED_b46374e511447cb531709a5d56f3ba9a6e4dcc8d
BLACKSMITH_PR_181: MERGED_307126031956bf5345da20a7b0c4466aa26c9b94
NINJA_SURVIVAL_PR_24: MERGED_46c5e151808f2481cc20be0003dd03866133ae49
PROJECT_MAIN_READBACK: PASS
PROJECT_NOTION_HANDOFF_READBACK: PASS
RM_TOOL_003_TOOL_HUB_GUI: RETIRED_NOT_ACTIVE_ROUTE
HUMAN_PLAYER_EVIDENCE: NOT_RUN
PRODUCT_BALANCE_PASS: NOT_CLAIMED
```

## 9. Rollback

- Base reference는 #580 merge `8c9a32379244e9de67c72ae949653cd3a16b5746`과 #591의 RM-TOOL-003 freshness claim을 함께 정합화한다.
- Omenward/Blacksmith/Ninja Pilot은 각 docs/evidence sidecar merge를 독립 revert할 수 있다.
- project-owned simulator와 기존 balance canon은 Base analyzer rollback과 독립적이다.
- 폐기된 Tool Hub/GUI 경로는 Git history가 audit/rollback 근거이며 active owner로 복원하지 않는다.