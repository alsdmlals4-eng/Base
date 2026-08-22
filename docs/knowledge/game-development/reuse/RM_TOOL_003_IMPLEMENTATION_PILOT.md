# RM-TOOL-003 · Balance Scenario Batch Simulator Implementation Pilot

- 상태: `BASE_REFERENCE_IMPLEMENTED · MULTI_PROJECT_PILOTS_MERGED_MAIN_READBACK`
- 기준일: 2026-08-22 KST
- 계약 owner: `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- 구현: `tools/reuse_modules/balance_scenario_batch_simulator.py`
- 입력 예시: `templates/reuse-modules/BALANCE_SCENARIO_BATCH_MANIFEST.json`
- 회귀: `tests/test_balance_scenario_batch_simulator.py`, `tests/test_balance_scenario_batch_schema.py`, `tests/test_balance_scenario_batch_read_only.py`
- Base reference merge: PR #580 → `8c9a32379244e9de67c72ae949653cd3a16b5746`
- Registry freshness: PR #591 → `e37c4e72344662b344f62a442dd2f7f39dbad34e`

## 1. 구현 판정

`RM-TOOL-003`은 거대 Balance GUI나 게임별 simulator를 Base에 합치는 방식이 아니라 **project-supplied deterministic run record를 읽기 전용으로 분석하는 작은 공용 kernel**로 구현한다.

```text
project-authoritative rules/data
→ project-owned simulator or deterministic adapter
→ run records
→ Base RM-TOOL-003 analyzer
→ distribution / tail / failure / choice / paired-seed / goal-seek report
→ human/GPT review
→ project decision owner
```

Base는 다음을 소유하지 않는다.

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

분석 결과가 잘못된 입력을 조용히 흡수하지 않도록 다음을 거부한다.

- bool/float/string seed의 integer 암묵 변환
- empty/non-string variant
- non-object metrics
- non-list choices/failures/goal_seek
- duplicate `(variant, seed)` pair
- nonnumeric metric
- NaN/Infinity metric 또는 goal target
- 없는 variant를 참조하는 goal-seek
- 잘못된 snapshot/evidence container

반환 report의 `snapshot`과 `evidence_ceiling`도 deep-copy해 결과 후처리가 입력 manifest를 alias로 변경하지 못하게 한다.

## 4. 5회 적대적 개선 루프

1. **수치 유효성 공격** — `NaN/Infinity`가 통계를 오염할 수 있어 finite-only 입력으로 교정.
2. **비율 의미 공격** — 동일 failure tag가 한 run에 중복되면 failure rate가 100%를 넘을 수 있어 run별 dedupe와 denominator를 명시.
3. **Goal-seek 공격** — 중앙값만 목표 안에 들면 volatile 후보가 stable 후보와 동률이 되는 문제를 발견해 실제 inside-target share를 추가하고 tie-break에 반영.
4. **재현 identity 공격** — `int(1.9)`, `int("1")` 같은 암묵 변환이 seed identity를 붕괴시킬 수 있어 strict JSON integer와 container schema로 교정.
5. **Read-only 공격** — 반환 metadata가 입력 객체를 alias하면 report mutation이 input을 변경할 수 있어 deep-copy로 격리.

```yaml
FULL_LOOP_COUNT: 5
BASE_KERNEL_VALID_MUST_FIX_REMAINING: 0
HUMAN_PLAYER_EVIDENCE: NOT_RUN
PRODUCT_BALANCE_PASS: NOT_CLAIMED
```

## 5. 프로젝트 소비자 검증

### OMENWARD · PR #202

- source: `docs/analysis/balance/current_normalized_balance_budget.v1.json`
- mode: `READ_ONLY_PLANNING_ENVELOPE_PILOT`
- 10,000 deterministic seeds로 raw wave search envelope를 추출 후 현재 계약대로 합계 1 정규화.
- 정규화 결과가 raw search envelope 밖으로 나가는 비율을 발견: W1 `1.24%`, W2 `1.93%`, Final `3.44%`.
- 이 결과는 오류 판정이 아니라 **final numerics 전에 pre/post-normalization semantics를 명확히 해야 한다는 planning finding**이다.
- product/runtime/canon mutation 없음.
- 최초 #202 CI의 Project Core/GDD 실패는 sidecar가 아니라 당시 current-main canon/legacy-validator drift였고, 선행 #201에서 해소됐다.
- #201 exact head `17f8b0a7a5753fe16ff54806ecaa31dcea3ef609`의 15개 PR workflow가 모두 `SUCCESS`; squash merge `4876748eb4683b4f7f711f30e0029ffad4f707b2`.
- #201 병합 후 #202는 새 main에서 다시 `mergeable=true`로 확인했고 squash merge `b46374e511447cb531709a5d56f3ba9a6e4dcc8d`.
- Omenward final `main`과 두 sidecar 파일을 직접 readback했다.

Evidence ceiling: `PLANNING_ENVELOPE_ONLY · CURRENT_V4_7_PLAYER_EVIDENCE_NOT_RUN · HUMAN_VALIDATION_NOT_RUN · FINAL_PRODUCT_NUMERICS_NOT_APPROVED`.

### BLACKSMITH · PR #181

- 프로젝트에 `tools/simulate_enhancement_balance.py`라는 project-owned deterministic simulator가 이미 존재한다.
- Existing Solution First 결과, Base가 enhancement rules를 다시 구현하는 것은 duplicate authority라 `REJECT`.
- project simulator가 rule/run-generation owner를 유지하고, 필요 시 개별 trial record를 Base kernel에 전달하는 구조를 `ADOPT`.
- 이번 Pilot은 interoperability/field ownership만 검증하고 새 trial export나 runtime 연결은 만들지 않는다.
- exact head `cb5dc9509769f3ae4ea8436718bfe0b2c917b115`의 5개 관련 workflow가 모두 `SUCCESS`.
- squash merge `307126031956bf5345da20a7b0c4466aa26c9b94`; Blacksmith `main`과 Notion Handoff를 readback했다.

Evidence ceiling: `PROJECT_SIMULATOR_EXISTS · INTEROP_CONTRACT_REVIEWED · NEW_TRIAL_EXPORT_NOT_IMPLEMENTED · FINAL_PRODUCT_BALANCE_NOT_APPROVED`.

### NINJA_SURVIVAL · PR #24

- 현재 legacy `WaveSpawner`의 deterministic cap actuator만 exhaustive initial state `0..8`로 검증.
- default `batch_size=2`, `max_active_enemies=8`; enabled variant는 모든 case에서 cap violation 0, disabled variant는 spawn 0.
- `data/stages/`는 `.gitkeep`만 존재하므로 DEC-026 새 stage/encounter balance를 임의 생성하지 않는다.
- 이 Pilot은 shared run-record 인터페이스가 deterministic actuator에도 적용됨만 증명한다.
- exact head `6b4cb0bfc48d9029f209ea9e9d4f0d0692220722`의 GUT run `32539901612`: `SUCCESS`.
- squash merge `46c5e151808f2481cc20be0003dd03866133ae49`; Ninja Survival `main`과 Notion Handoff를 readback했다.

Evidence ceiling: `LEGACY_MVP3_ACTUATOR_CONTRACT_ONLY · DEC014_026_RUNTIME_NOT_STARTED · PRODUCT_BALANCE_NOT_EVALUATED`.

## 6. 공용성 판정

세 프로젝트는 서로 다른 형태의 소비자를 제공한다.

| 소비 형태 | 프로젝트 | 결과 |
|---|---|---|
| planning envelope 자체를 read-only로 분석 | OMENWARD | 공용 분포/경계 분석 가치 확인 |
| 이미 project simulator가 존재 | BLACKSMITH | Base는 post-processor여야 함 확인 |
| deterministic runtime actuator, 신규 balance data 미존재 | NINJA_SURVIVAL | run-record 계약은 적용 가능하되 새 수치 발명 금지 확인 |

따라서 **공용 kernel은 유지 가치가 있고, game-rule simulator는 project-owned가 맞다.**

## 7. Tool Hub / GUI 판정

현재는 `DEFER`한다.

이유:

1. 세 소비자가 모두 같은 GUI를 필요로 한다는 증거가 없다.
2. Blacksmith는 이미 project-local simulator가 있다.
3. Omenward는 현재 implementation gate가 닫혀 있다.
4. Ninja는 신규 stage balance data가 아직 없다.
5. CLI + machine-readable JSON으로 현재 검증 목적을 충족한다.

다음 조건 중 둘 이상이 실제로 반복될 때 기존 Tool Hub의 thin surface를 재검토한다.

- 2개 이상 프로젝트에서 사용자가 같은 launch/manifest/report 작업을 반복 수행한다.
- CLI report 비교가 human workflow의 반복 병목으로 관찰된다.
- project identity/security boundary를 기존 Tool Hub adapter로 안정적으로 고정할 수 있다.
- UI가 새로운 authority를 만들지 않고 기존 kernel을 호출만 한다.

**새 독립 Electron/HTML Balance 앱, 두 번째 Hub, 자동 수치 패치는 계속 `REJECT/DEFER`.**

## 8. 다음 프로젝트 적용 규칙

새 프로젝트에 적용할 때는 순서가 고정된다.

```text
project canon/runtime owner 확인
→ existing project simulator/runner 우선
→ deterministic run-record adapter가 필요한지 판단
→ Base analyzer 실행
→ report evidence ceiling 확인
→ 사람/GPT가 해석
→ 프로젝트 정본 변경은 별도 승인/검증
```

`RM-TOOL-003` 존재 자체는 project balance PASS, 재미 PASS, 자동 패치 권한을 주지 않는다.

## 9. Post-change closeout

```yaml
BASE_REFERENCE_PR_580: MERGED_8c9a32379244e9de67c72ae949653cd3a16b5746
REGISTRY_PR_591: MERGED_e37c4e72344662b344f62a442dd2f7f39dbad34e
OMENWARD_PR_201: MERGED_4876748eb4683b4f7f711f30e0029ffad4f707b2
OMENWARD_PR_202: MERGED_b46374e511447cb531709a5d56f3ba9a6e4dcc8d
BLACKSMITH_PR_181: MERGED_307126031956bf5345da20a7b0c4466aa26c9b94
NINJA_SURVIVAL_PR_24: MERGED_46c5e151808f2481cc20be0003dd03866133ae49
PROJECT_MAIN_READBACK: PASS
PROJECT_NOTION_HANDOFF_READBACK: PASS
REGISTRY_REFERENCE_IMPLEMENTATION_FRESHNESS: PASS
RM_TOOL_003_MUST_FIX_REMAINING: 0
HUMAN_PLAYER_EVIDENCE: NOT_RUN
FINAL_PRODUCT_BALANCE: NOT_APPROVED
```

완료 판정은 **공용 analyzer 구현 + 세 프로젝트의 서로 다른 소비 형태 검증 + 실제 PR 병합/main readback + Notion Handoff 동기화 + Registry freshness**까지다. 이것은 각 게임의 재미·난이도·final numerics가 승인됐다는 뜻이 아니다.

## 10. Rollback

- Base reference: #580 merge `8c9a32379244e9de67c72ae949653cd3a16b5746`을 revert하고, Registry에서 #591이 추가한 `RM-TOOL-003 REFERENCE_IMPLEMENTATION_EXISTS` freshness claim만 별도 정합화한다. #591 전체를 revert해 다른 context-synthesis 변경을 제거하지 않는다.
- Omenward Pilot: #202 merge `b46374e511447cb531709a5d56f3ba9a6e4dcc8d`를 revert하면 두 docs-only sidecar가 제거된다. #201 canon reconciliation은 독립 owner이므로 RM-TOOL-003 rollback 대상으로 묶지 않는다.
- Blacksmith Pilot: #181 merge `307126031956bf5345da20a7b0c4466aa26c9b94`를 revert하면 docs/evidence sidecar만 제거된다.
- Ninja Survival Pilot: #24 merge `46c5e151808f2481cc20be0003dd03866133ae49`를 revert하면 legacy actuator docs/evidence sidecar만 제거된다.
- project-owned simulator와 기존 balance canon은 이 Base reference의 rollback과 독립적이다.