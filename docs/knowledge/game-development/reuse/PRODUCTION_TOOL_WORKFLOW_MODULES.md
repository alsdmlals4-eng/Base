# Production Tool & Workflow Reusable Modules

이 문서는 프로젝트에서 반복되는 **도구·자동화·검증·작업구조**의 공용 계약을 관리한다.

현재 원칙:

```text
EXISTING_OWNER_REUSE
REPOSITORY_NATIVE_EVIDENCE_FIRST
NO_TOOL_HUB_OR_NEW_BROAD_GUI_DEFAULT
NO_QA_CAPTURE_APP_DEFAULT
NO_EXTERNAL_HTML_WORKSPACE_DEFAULT
NO_NEW_PAID_SERVICE_DEFAULT
```

새 Tool Hub·QA capture app·외부 HTML dashboard·광역 Skill을 만들기 위한 목록이 아니다. 기존 Base owner, repository/runtime evidence, project-owned simulator/adapter로 해결할 수 있으면 그것이 기본이다.

---

## RM-TOOL-001 · DATA_SCHEMA_CROSSREF_VALIDATOR

**상태:** `REFERENCE_IMPLEMENTATION_EXISTS`.

구현: `tools/reuse_modules/data_schema_crossref_validator.py`.

문제: JSON/Resource/Markdown 콘텐츠가 늘수록 ID 오타, dangling reference, enum 오류, duplicate key, 상태 전이 누락이 반복된다.

```yaml
module: DATA_SCHEMA_CROSSREF_VALIDATOR
inputs:
  roots: []
  schema_rules: []
  id_namespaces: []
checks:
  - parseability
  - schema/type
  - unique IDs
  - reference existence
  - enum/domain constraints
  - forbidden cycles where configured
  - unreachable/orphan records where configured
outputs:
  - deterministic finding list
  - file/path/record locator
  - severity
  - remediation hint
```

원칙:

- validator는 데이터를 수정하지 않는다.
- 프로젝트별 schema는 adapter/config가 소유한다.
- project runtime parser가 있으면 우선 재사용한다.

---

## RM-TOOL-002 · DETERMINISTIC_SEED_REPLAY_CAPTURE

**상태:** `MODULE_CONTRACT_DEFINED`.

RNG·동시해결·stage progression이 있는 게임에서 결과 재현성과 preview/runtime 인과 경계를 명시한다.

```yaml
run_identity:
  build_or_commit:
  scenario_id:
  seed:
initial_state_hash:
input_events: []
causal_boundary:
  preview_reads_state: true
  preview_mutates_runtime_state: false
  preview_consumes_runtime_rng: false
  runtime_rng_consumption_points: []
resolution_windows: []
state_checkpoints: []
result_hash:
replay_format_version:
```

필수 invariant:

```text
PREVIEW_DOES_NOT_MUTATE_CAUSAL_STATE
PREVIEW_DOES_NOT_CONSUME_RUNTIME_RNG
RNG_CONSUMPTION_HAS_EXPLICIT_CAUSAL_BOUNDARY
```

presentation-only jitter는 deterministic state hash에서 제외할 수 있다. Replay가 private/hidden information을 노출하지 않는지도 확인한다.

---

## RM-TOOL-003 · BALANCE_SCENARIO_BATCH_SIMULATOR

**상태:** `REFERENCE_IMPLEMENTATION_EXISTS · MULTI_PROJECT_READ_ONLY_CONTRACT_EVIDENCE`.

구현: `tools/reuse_modules/balance_scenario_batch_simulator.py`.
상세 evidence: `RM_TOOL_003_IMPLEMENTATION_PILOT.md`.

공용 가치는 **게임 규칙 simulator를 Base가 소유하는 것**이 아니라, project-owned deterministic runner가 만든 run record를 같은 분석 계약으로 읽는 데 있다.

```text
project-authoritative rules/data
→ project-owned simulator or deterministic adapter
→ run records
→ Base analyzer
→ distribution / tails / failure / dominant choice / paired_seed_delta / goal_seek
→ GPT/human review
→ project decision owner
```

```yaml
snapshot_input:
scenario_set:
seed_policy:
runs_per_scenario:
metrics:
  distributions: [mean, median, percentile_05, percentile_25, percentile_75, percentile_95]
  tails: []
  dominant_choices: []
  failure_rates: []
  paired_seed_delta: []
comparison:
  baseline:
  candidates: []
  pair_by_seed: true
explainability:
  reason_trace: []
  trigger_counts: []
  outlier_runs: []
goal_seek:
  targets: []
  adjustable_parameters: []
  locked_parameters: []
  constraints: []
  output_candidates_only: true
```

### 분석 원칙

- 평균 하나가 아니라 분포·꼬리·실패율·지배 선택지를 함께 본다.
- baseline/candidate는 가능한 경우 same-seed pairing으로 비교한다.
- outlier는 제거 전에 원인을 trace한다.
- `goal_seek`는 후보 범위를 제안할 수 있지만 project canon을 자동 수정하지 않는다.
- project data와 final balance authority는 프로젝트가 소유한다.

### Human-consumption boundary

```text
NO_TOOL_HUB_OR_BALANCE_GUI_ACTIVE_ROUTE
CLI + machine-readable JSON
→ GPT/human analysis
→ 필요 시 exact Project Notion human summary
```

Tool Hub, 별도 Electron Balance 앱, 외부 HTML dashboard, 프로젝트 local GUI는 현재 active/default/revisit 경로가 아니다. CLI/JSON이 현재 evidence 목적을 충족한다.

향후 사용자가 현재 `Tool Hub 미사용` 결정을 명시적으로 변경하고, 반복된 실제 병목이 증명되며, Existing Solution First + 최소 3개 실질 대안 + 장기 적합성 검토를 다시 통과한 경우에만 별도 surface를 새 기획으로 검토한다.

Evidence ceiling:

```text
SIMULATION_PASS
!= PRODUCT_BALANCE_PASS
!= PLAYER_FUN_PASS
```

---

## Cross-cutting contract · ATOMIC_RESOLUTION_BOUNDARY

이 항목은 새 RM ID를 추가하지 않는다. `RM-SYS-002 PHASED_SESSION_STATE_MACHINE`, `RM-SYS-004 EXPLAINABLE_RESULT_PACKET`, `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`가 공유하는 경계다.

```yaml
resolution_window:
  window_id:
  opens_on:
  allowed_mutations: []
  deferred_authoritative_checks: []
  priority_rules: []
  closes_when:
  publish_after_close:
  replay_checkpoint:
preview_policy:
  reads_authoritative_state: true
  mutates_authoritative_state: false
  consumes_runtime_rng: false
```

연쇄 중간 상태가 final result처럼 publish되지 않게 하고, 프로젝트별 effect ordering 자체는 통일하지 않는다.

---

## RM-TOOL-004 · REPOSITORY_NATIVE_EVIDENCE_CAPTURE

**상태:** `EXISTING_OWNER_REUSE · NO_DEDICATED_CAPTURE_APP`.

별도 QA 관리 앱 없이 repository/runtime/test/CI 증거를 exact project/build identity에 묶는다.

```yaml
project_identity:
build_identity:
validation_contract:
  resolution_or_viewport:
  input_path:
  accessibility_checks:
  expected_state_or_screen:
capture_sources:
  screenshots: []
  video: []
  logs: []
  test_results: []
  machine_state: []
storage:
  repository_or_ci_artifact:
  notion_human_link_when_useful:
verdict:
  human_or_rule_owner:
  evidence_ceiling:
```

- GUT/Godot/Hera/CLI/CI처럼 프로젝트가 이미 채택한 evidence source를 우선한다.
- screenshot/video가 필요하면 build/commit/viewport/input context를 함께 기록한다.
- Notion은 human link/preview가 될 수 있지만 runtime truth를 대체하지 않는다.
- 사람을 관찰하지 않았으면 usability/fun evidence는 `NOT_RUN`이다.
- `REPOSITORY_NATIVE_EVIDENCE_CAPTURE != AI_AUTO_PASS`.

---

## RM-TOOL-005 · PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER

**상태:** `MODULE_CONTRACT_DEFINED · REFERENCE_IMPLEMENTATION_EXISTS · PROJECT_ADOPTION_NOT_RUN`.

구현: `tools/public_video_research_ingest.py`.

공개 영상이 연구 근거일 때 검색 스니펫/기억으로 본문을 대체하지 않고 caption/transcript provenance와 timestamp evidence를 구조화한다.

```yaml
module: PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER
inputs:
  source_url:
  preferred_languages: [ko, en, en-US]
  yt_dlp_executable: yt-dlp
  local_transcript_file: optional [.vtt, .srt, .txt]
source_ladder:
  - accessible_manual_caption
  - accessible_auto_caption
  - caller_supplied_local_transcript
  - optional_existing_local_asr_adapter
  - BLOCKED_UNVERIFIED
outputs:
  retrieval_tool_and_version:
  transcript_source_kind:
  transcript_language:
  timestamped_segments: []
  video_binding: UNVERIFIED
  creation_source: UNKNOWN
storage_policy:
  full_transcript: LOCAL_RESEARCH_ONLY
  repository_evidence: DERIVED_NOTES_AND_TIMESTAMPS_ONLY
```

### 구현·비용 경계

- metadata/caption track만 조사하고 영상·오디오 자체를 Base에 보관하지 않는다.
- manual caption을 auto caption보다 우선하고 provenance를 분리한다.
- caption이 없으면 `ASR_FALLBACK_REQUIRED`로 분류한다.
- `caller_supplied_local_transcript`는 `.vtt/.srt/.txt`를 받을 수 있지만 `video_binding: UNVERIFIED`, `creation_source: UNKNOWN`을 유지한다.
- `.vtt/.srt`의 timestamp가 있다는 사실만으로 원 영상과 일치한다고 주장하지 않는다.
- hosted paid transcript API/SaaS를 자동 fallback으로 쓰지 않는다.

증거 ceiling:

```text
CAPTION_INGEST_PASS != SPEAKER_CLAIM_FACT_PASS
LOCAL_TRANSCRIPT_READY != VERIFIED_VIDEO_BINDING
TIMESTAMPS_PRESENT != TIMESTAMPS_MATCH_SOURCE_VIDEO
LOCAL_TRANSCRIPT_TIMESTAMPS_ONLY_VIDEO_BINDING_UNVERIFIED_NOT_FACT_VERIFICATION
LOCAL_TRANSCRIPT_TEXT_ONLY_VIDEO_BINDING_UNVERIFIED_NOT_FACT_VERIFICATION
```

---

## RM-WORK-001 · PROJECT_REUSE_OPPORTUNITY_SCAN

**상태:** `BASE_ACTIVE_METHOD`.

```text
PROJECT_CANON_FIRST
→ repeated cost / bottleneck map
→ candidate search
→ multi-source reverse engineering
→ reusable contract
→ Existing Solution First
→ fit / cost / risk
→ NOVELTY_DELTA
→ project pilot
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

새 `reuse-discovery` 광역 Skill을 만들지 않는다.

---

## RM-WORK-002 · SKILL_WORKFLOW_PATTERN_EVAL

**상태:** `BASE_ACTIVE_METHOD`.

Owner: `docs/AI_SKILL_ADOPTION_GUIDE.md`.

```yaml
candidate:
trigger:
inputs:
source_of_truth:
steps:
output:
failure_recovery:
placement_options:
  - existing instruction
  - template/reference
  - existing Skill mode
  - deterministic tool
  - EXTERNAL_PROCESS_OVERLAY
  - new Skill/Agent last
baseline_eval:
candidate_eval:
negative_route_eval:
maintenance_cost:
HUMAN_EDIT_DELTA:
  baseline_total_minutes:
  candidate_generation_or_creation_minutes:
  attempt_count:
  human_edit_minutes:
  integration_minutes:
  qa_minutes:
  candidate_total_minutes:
  net_minutes_saved:
  quality_delta:
  consistency_delta:
  repeatability:
```

`HUMAN_EDIT_DELTA`는 생성시간만이 아니라 사람 수정·재시도·통합·QA까지 포함한 total effort를 비교한다.

### PROJECT_SUBSYSTEM_CHANGE_MAP

Skill 개수보다 실제 subsystem owner/consumer/test 연결을 추적한다.

```yaml
project_subsystem_change_map:
  subsystem:
  canonical_owner:
  authored_data_owner:
  mutable_runtime_owner:
  resolver_or_service_owner:
  presenter_or_ui_owner:
  touch_points: []
  cross_domain_dependencies: []
  invariants: []
  required_tests: []
  forbidden_shortcuts: []
  rollback:
```

presenter/UI는 gameplay state의 우회 owner가 되지 않는다. 반복 빈도와 routing/eval 개선이 실제로 확인될 때만 dedicated Skill로 승격한다.

---

# 1차 공용 조합

## 데이터 중심

```text
PROJECT_REUSE_OPPORTUNITY_SCAN
→ DATA_SCHEMA_CROSSREF_VALIDATOR
→ project-specific tests
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE when needed
```

## RNG / 결과 해결 중심

```text
DETERMINISTIC_SEED_REPLAY_CAPTURE
→ ATOMIC_RESOLUTION_BOUNDARY
→ BALANCE_SCENARIO_BATCH_SIMULATOR when justified
→ EXPLAINABLE_RESULT_PACKET
→ repository-native runtime evidence
→ human/player validation when required
```

## 공개 영상 연구

```text
PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER
→ transcript provenance + timestamp evidence
→ PROJECT_REUSE_OPPORTUNITY_SCAN
→ multi-source / existing-solution comparison
→ derived notes only
```

---

# Godot 재사용 구현 원칙

공용 Pilot은 다음을 우선 비교한다.

```text
Resource data contract
+ small rule service/script
+ project adapter
+ project-owned scene/presenter
```

adapter가 공용 코드보다 커지거나 프로젝트마다 상태/시간/rollback 의미가 크게 다르면 project-local 구현을 유지한다.

---

# 완료·재검토 규칙

- `RM-TOOL-001`과 `RM-TOOL-003`은 실제 Base reference implementation이 존재한다.
- `RM-TOOL-002`는 contract이며 executable 완료를 주장하지 않는다.
- `RM-TOOL-004`는 별도 앱이 아니라 현재 repository/runtime evidence를 조합하는 활성 방법이다.
- `RM-TOOL-005`는 bounded reference implementation이 있으나 live site compatibility/project adoption은 별도 검증한다.
- `ATOMIC_RESOLUTION_BOUNDARY`와 `PROJECT_SUBSYSTEM_CHANGE_MAP`은 기존 owner를 보강하는 계약이다.
- Tool Hub·QA Studio·외부 HTML·새 local management GUI는 이 문서의 자동 재검토 후보가 아니다.
- 새 tool/surface가 필요하다는 반복 실제 증거가 생기면 Existing Solution First, 최소 3개 실질 대안, 비용/보안/권위/rollback, 사용자 명시 승인을 다시 거친다.