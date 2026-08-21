# Production Tool & Workflow Reusable Modules

이 문서는 프로젝트 10개의 반복 제작비를 기준으로 **도구·자동화·검증·작업구조** 재사용 후보를 정리한다.

새 Tool Hub·QA capture app·광역 Skill을 만들기 위한 목록이 아니다. 같은 책임의 기존 Base owner와 repository/runtime evidence가 있으면 `EXISTING_OWNER_REUSE`가 기본이다.

---

## RM-TOOL-001 · DATA_SCHEMA_CROSSREF_VALIDATOR

**문제:** JSON/Resource/Markdown 기반 콘텐츠가 늘수록 ID 오타, dangling reference, 잘못된 enum, 중복 key, 상태 전이 누락이 반복된다.

적용 후보:
- URBAN_LEGEND: 사건·동료·장비·연구·활동.
- NINJA_SURVIVAL: 아이템·조합·보상·적/스테이지.
- OMENWARD: TokenSource·roulette·unit·stage.
- GRIMOIRE: 글자·회로·주문·effect.
- TETRIS: Skill·Energy/Tier bridge.
- SWITCHY: semantic asset/data manifests.
- BLACKSMITH: item/order/history definitions.

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
exit_contract:
  invalid_contract: nonzero
  warnings_only: configurable
```

### 구현 원칙

- validator는 데이터를 수정하지 않는다.
- 프로젝트별 schema는 adapter/config로 둔다.
- 문자열 전체를 하드코딩한 하나의 Base 검사기로 만들지 않는다.
- project runtime owner가 존재하면 그 serialization/parser를 가능하면 재사용한다.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT`.

---

## RM-TOOL-002 · DETERMINISTIC_SEED_REPLAY_CAPTURE

**문제:** RNG·동시해결·stage progression이 있는 게임은 “왜 이 결과가 나왔나”를 재현하기 어렵다.

적용:
- TEN_PACES: 계획 resolution replay.
- OMENWARD: roulette + battle result.
- BLACKSMITH: 강화 outcome/lifecycle scenario.
- NINJA_SURVIVAL: reward/build/encounter sequence.
- TETRIS: piece/chain sequence test.
- SWITCHY: sealed layout retry.

```yaml
run_identity:
  build_or_commit:
  scenario_id:
  seed:
initial_state_hash:
input_events: []
state_checkpoints: []
result_hash:
replay_format_version:
```

검증:
1. 같은 build + scenario + seed + input → 같은 deterministic state hash가 필요한 범위를 선언.
2. presentation timestamp·animation jitter처럼 비결정적이어도 되는 값은 hash에서 제외.
3. replay가 private/hidden information을 부적절하게 노출하지 않는지 확인.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT`.

---

## RM-TOOL-003 · BALANCE_SCENARIO_BATCH_SIMULATOR

**판정:** `MODULE_CONTRACT_DEFINED`.

Balance/scenario simulation은 공통 가치가 있지만 현재 공용 executable이 존재한다고 가정하지 않는다. 별도 대형 Tool을 만들기 전에 프로젝트별 snapshot + deterministic runner + repository-native report 조합을 우선 비교한다.

```yaml
snapshot_input:
scenario_set:
seed_policy:
runs_per_scenario:
metrics:
  distributions: []
  tails: []
  dominant_choices: []
  failure_rates: []
comparison:
  baseline:
  candidate:
output:
  report:
  machine_readable_summary:
  patch_suggestions_non_authoritative:
```

1차 project scenarios:
- OMENWARD: roulette 확률·wave·unit 결과 분포.
- NINJA_SURVIVAL: 보상/백팩 조합/encounter build 성능.
- BLACKSMITH: 강화·경제·의뢰 결과 분포.
- TETRIS: Line/Chain reward bridge와 skill 선택 분포.

증거 ceiling:
- simulation은 플레이어 재미를 증명하지 않는다.
- patch suggestion은 프로젝트 수치 정본을 자동 수정하지 않는다.
- 실제 executable 구현은 별도 evidence/approval 없이 완료로 주장하지 않는다.

---

## RM-TOOL-004 · REPOSITORY_NATIVE_EVIDENCE_CAPTURE

**판정:** `EXISTING_OWNER_REUSE · NO_DEDICATED_CAPTURE_APP`.

프로젝트 검증 증거는 별도 QA 관리 앱을 기본 경로로 두지 않고 **이미 존재하는 repository/runtime/test/CI 증거**를 exact project/build identity에 묶는다.

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

원칙:

1. GUT/Godot/Hera/CLI/CI처럼 현재 프로젝트가 이미 채택한 evidence source를 우선한다.
2. screenshot/video가 필요한 경우 현재 실행환경에서 직접 캡처하고 commit/build/viewport/input context를 함께 기록한다.
3. Notion은 사람이 보는 링크·preview·설명면이 될 수 있지만 repository/runtime truth를 대체하지 않는다.
4. 사람이 실제로 관찰하지 않은 usability/fun evidence는 `NOT_RUN`이다.
5. capture app·project adapter·별도 local management UI를 신규 기본 의존성으로 만들지 않는다.

`REPOSITORY_NATIVE_EVIDENCE_CAPTURE != AI_AUTO_PASS`.

---

## RM-TOOL-005 · PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER

**문제:** GDC 발표·개발자 인터뷰·튜토리얼·제작 회고처럼 공개 영상이 조사 근거일 때 웹 검색 스니펫이나 기억만으로 내용을 대체하면 실제 발언·맥락·timestamp를 잃고 `BLOCKED_UNVERIFIED`가 반복된다.

**판정:** `PATTERN_EXTRACT + BASE_REFERENCE_IMPLEMENTATION`.

Reference implementation: `tools/public_video_research_ingest.py`.

```yaml
module: PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER
inputs:
  source_url:
  preferred_languages: [ko, en, en-US]
  yt_dlp_executable: yt-dlp
source_ladder:
  - accessible_manual_caption
  - accessible_auto_caption
  - optional_existing_local_asr_adapter
  - BLOCKED_UNVERIFIED
outputs:
  source_identity:
  retrieval_tool_and_version:
  transcript_status:
  transcript_source_kind:
  transcript_language:
  timestamped_segments: []
storage_policy:
  full_transcript: LOCAL_RESEARCH_ONLY
  default_output_root: .tmp/public-video-research
  repository_evidence: DERIVED_NOTES_AND_TIMESTAMPS_ONLY
```

### 구현·비용 경계

1. Base reference implementation은 `yt-dlp --skip-download --dump-single-json`으로 metadata/caption track만 찾고 선택한 WebVTT만 읽는다. 영상·오디오를 다운로드하지 않는다.
2. manual caption을 auto caption보다 우선하며 둘의 provenance를 분리한다.
3. caption이 없으면 `ASR_FALLBACK_REQUIRED`를 반환한다. local ASR이 이미 준비된 환경에서 별도 bounded adapter로 처리할 수 있지만 Base가 모델·GPU runtime·ffmpeg를 자동 설치하지 않는다.
4. hosted transcript SaaS, paid proxy, separately metered API/credit를 자동 fallback으로 사용하지 않는다.
5. full transcript는 기본적으로 Git ignore 대상인 `.tmp/` local research packet으로만 저장한다. GitHub/Notion에는 현재 결정에 필요한 derived note·짧은 인용·timestamp·source URL을 남긴다.
6. caption URL은 HTTPS YouTube/GoogleVideo host로 제한하고 untrusted metadata가 임의 host fetch로 이어지지 않게 한다.

### 증거 ceiling

```text
CAPTION_INGEST_PASS
!= SPEAKER_CLAIM_FACT_PASS
!= COPYRIGHT_CLEARANCE
!= PROJECT_FIT_PASS
!= ASR_OR_CAPTION_PERFECT_ACCURACY
```

실제 live YouTube retrieval은 `yt-dlp`가 준비된 실행환경에서 대표 영상으로 별도 검증한다. unit test만으로 site compatibility를 PASS 처리하지 않는다.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_ADDED · PROJECT_ADOPTION_NOT_RUN`.

---

## RM-WORK-001 · PROJECT_REUSE_OPPORTUNITY_SCAN

**상태:** `BASE_ACTIVE_METHOD`.

현재 Base의 merged reverse-engineering pipeline과 `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`가 owner다.

```text
PROJECT_CANON_FIRST
→ REPEATED_COST_AND_BOTTLENECK_MAP
→ candidate search
→ multi-source reverse engineering
→ reusable contract
→ Existing Solution First
→ fit / cost / risk
→ NOVELTY_DELTA
→ project pilot
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

새 `reuse-discovery` 광역 Skill을 만들지 않는다. 프로젝트 기획/벤치마킹 작업의 조건부 절차로 사용한다.

---

## RM-WORK-002 · SKILL_WORKFLOW_PATTERN_EVAL

**상태:** `BASE_ACTIVE_METHOD`.

Owner: `docs/AI_SKILL_ADOPTION_GUIDE.md`의 `REVERSE_ENGINEERED_SKILL_WORKFLOW_CANDIDATE`, `PATTERN_NOT_PACKAGE_COPY`, `EVAL_BEFORE_PROMOTION`.

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

`HUMAN_EDIT_DELTA`는 “AI가 몇 초 만에 만들었다” 같은 생성 시간만으로 생산성을 과장하지 않기 위한 공통 측정 계약이다. 외부 Tool/Workflow/Visual provider 후보는 재시도·사람 수정·통합·QA까지 포함한 total effort와 품질·일관성을 기존 baseline과 비교한다.

### 승격 금지 조건

- 유명 팀이 쓴다는 이유만 있음.
- 이름만 다르고 기존 Skill과 책임이 같음.
- trigger가 너무 넓어 unrelated 작업까지 라우팅함.
- 실제 전후 Eval이 없음.
- Tool/권한/정본 경계가 명확하지 않음.
- 생성 속도만 빠르고 사람 수정·통합·QA를 포함한 총비용이 개선되지 않음.

---

# 1차 공용 Tool/Workflow 조합

## A. 데이터 중심 프로젝트

```text
PROJECT_REUSE_OPPORTUNITY_SCAN
→ DATA_SCHEMA_CROSSREF_VALIDATOR
→ project-specific unit tests
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE when runtime/UI evidence is needed
```

추천 대상: URBAN_LEGEND, NINJA_SURVIVAL, OMENWARD, GRIMOIRE, BLACKSMITH.

## B. RNG/해결 결과가 중요한 프로젝트

```text
DETERMINISTIC_SEED_REPLAY_CAPTURE
→ BALANCE_SCENARIO_BATCH_SIMULATOR when justified
→ EXPLAINABLE_RESULT_PACKET
→ repository-native runtime evidence
→ human/player validation when the claim requires it
```

추천 대상: OMENWARD, NINJA_SURVIVAL, BLACKSMITH, TETRIS, TEN_PACES.

## C. 콘텐츠/서사 프로젝트

```text
CANON_SOURCE_PROVENANCE_REGISTRY
→ DATA_SCHEMA_CROSSREF_VALIDATOR
→ CONTINUITY_REVISION_REGRESSION
→ EXTERNAL_ARTIFACT_RECONCILIATION_WORKFLOW
```

추천 대상: COC_FICTION, URBAN_LEGEND, GRIMOIRE.

## D. 공개 영상 기반 벤치마킹·제작 사례 조사

```text
PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER when direct video evidence is required
→ timestamped local evidence packet
→ PROJECT_REUSE_OPPORTUNITY_SCAN
→ multi-source / rights / fit review
→ derived decision evidence only
```

`PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`는 모든 YouTube URL을 자동 전사하는 상시 crawler가 아니다. 현재 의사결정에 영상 본문 evidence가 실제로 필요한 경우에만 조건부로 사용한다.

---

# Godot 재사용 구현 원칙

Godot 프로젝트의 공용 Pilot이 필요할 때 다음을 우선 비교한다.

```text
Resource data contract
+ small rule service/script
+ project adapter
+ project-owned scene/presenter
```

하지만 다음 경우 project-local 구현을 유지한다.

- adapter가 공용 코드보다 커짐.
- 프로젝트마다 상태/시간/rollback 의미가 다름.
- shared dependency가 upgrade/CI 위험을 키움.
- 공용화로 코드량은 줄어도 이해/디버그 시간이 늘어남.

---

# Benchmark / Existing Solution notes

## Godot

- Scenes/Resources의 재사용·인스턴스화를 `ADOPT` 후보로 검토한다.
- 하나의 거대 autoload/global manager는 이 조사에서 도출된 결론이 아니다.

## GitHub reusable workflow pattern

반복 CI 절차를 복사하지 않고 중앙 호출 계약으로 재사용하는 원리를 workflow module 설계에 `ADAPT`한다. Base 자체 Required Check 구조는 별도 CI owner가 소유한다.

## External addons/tools

Godot addon, GitHub repo, marketplace tool은 발견 즉시 설치하지 않는다.

```text
Existing Solution First
→ license
→ version/Godot compatibility
→ security/supply chain
→ maintenance
→ exact project consumer
→ bounded pilot
→ rollback
```

공개 영상 ingest도 같은 원칙을 적용한다. `ytscribe` 같은 직접 재사용 후보, `youtube-transcript-api` 같은 API wrapper, `yt-dlp` thin adapter, hosted service를 비용·유지보수·권한·복구 기준으로 비교한 뒤 현재 Base에는 좁은 `yt-dlp` adapter만 둔다.

---

# 구현 우선순위

| Priority | Module | 이유 |
|---|---|---|
| P0 | `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR` | 여러 프로젝트의 반복 오류를 낮은 UI/runtime 위험으로 줄일 수 있음 |
| P0 | `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE` | simulation/replay/debug 기반을 공유할 수 있음 |
| P1 | `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR` | 가치가 크지만 project snapshot/runner evidence가 먼저 필요 |
| P1 PILOT | `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER` | 반복적인 공개 영상 조사에서 provenance 누락을 줄이되 live site compatibility 검증이 필요 |
| ACTIVE | `RM-TOOL-004 REPOSITORY_NATIVE_EVIDENCE_CAPTURE` | 별도 앱 없이 기존 test/runtime/CI 증거를 재사용 |
| ACTIVE | `RM-WORK-001/002` | 이미 Base 방법으로 존재 |

# 완료 상태

이 문서의 신규 tool contract는 실제 executable 구현과 분리한다. `RM-TOOL-004`는 별도 프로그램이 아니라 현재 repository/runtime evidence를 조합하는 **활성 방법 계약**이다. `RM-TOOL-001/002/003`은 실제 공용 executable 증거가 생기기 전까지 `IMPLEMENTATION_NOT_BUILT` 또는 project-local pilot 상태를 유지한다.

`RM-TOOL-005`는 Base reference implementation과 network-free unit test를 갖지만 **실제 공개 영상 live retrieval과 프로젝트 adoption은 아직 별도 증거가 필요**하다. 따라서 현재 상태를 project/runtime PASS로 과장하지 않는다.
