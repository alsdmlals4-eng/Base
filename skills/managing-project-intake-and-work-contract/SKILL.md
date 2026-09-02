---
name: managing-project-intake-and-work-contract
description: Use when routing a project request, closing material ambiguity, defining a work contract, or sequencing approved dependent work.
---

# Managing Project Intake and Work Contracts

> `BASE_CURRENT_OPERATIONAL_BOOTSTRAP`: when current scope requires **Base-only maintenance** and future project sessions to fresh-read current Base without project-side preinstallation, read `docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md`. It is a nonpersistent PM/workflow overlay: target-project `AGENTS.md`, product canon, protected paths and adopted Base release retain authority. Do not copy the detailed playbook into this file. Scoped learning and regression provenance: `references/base-current-project-work-bootstrap/LEARNING_LOG.md`.


## Core principle

요청 접수는 `의도 파악 → Work Mode 자동 선택 → Skill 자동 선택 → 필요한 Skill Mode 선택 → 사실 조사 → first-prompt 방향 고정 → 실행 계약 → Grill Me 정합성 확인 → 필요 시 작업 분해·순서화 → 실행 보고`인 하나의 상태 흐름이다.

사용자는 Skill 이름이나 mode를 선언할 필요가 없다. Registry trigger와 현재 작업 단계로 필요한 최소 Skill·Skill Mode만 자동 선택하고, 실제 사용 이유와 얻은 결과를 최종 보고에 남긴다.

모든 L1 이상 지시문 작성은 이 Skill에서 좋은 프롬프트 변환을 수행한 뒤 `Grill Me alignment gate`로 의도·기획·범위가 맞는지 확인한다. 유효한 승인 없이 제품·프로젝트 작업으로 진행하지 않는다.

새 기능 또는 기능 계약·공개 경계를 의미 있게 바꾸는 요청은 작업 크기와 무관하게 이 Skill의 intake를 거친다. 작은 단일 파일·단일 단계라도 L1 intake 대상이며, 작업 분해가 필요하지 않더라도 기능 계약의 정본 owner, 공개·통합 경계, 실제 consumer·의존 방향, 검증·롤백을 기존 실행 계약과 실행계획에 연결한다.

Registry의 승인된 작은 작업 비사용 조건은 이미 승인·정의된 기능 경계를 그대로 구현하는 continuation에만 적용한다. 새 기능 또는 공개 계약·상태 소유권·consumer 연결이 생기거나 바뀌면 작은 변경으로 intake를 우회하지 않는다.

## Mandatory pre-build planning gate

`FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`

`REUSE_FIRST_PREFLIGHT_REQUIRED`

`PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT`

`USER_APPROVAL_BEFORE_BUILD`

`REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK`

`POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK`

`REUSE_LEARNING_HANDOFF_REQUIRED`

L1 이상 중요 Base/프로젝트 작업은 실행안을 먼저 정해 두고 근거를 맞추지 않는다. `FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`에서 현재 요청에 실제 영향을 주는 범위를 먼저 복원한다.

```text
latest user request
→ Base current owners / relevant Skill / current main
→ target project GitHub current main / canon / actual code·data·assets·tests
→ V4 Notion exception / legacy migration source only when its recorded scope applies
→ same-goal open/recent PR read-only reconciliation
→ confirmed decisions / current implementation / evidence
→ Project Asset/Reference/Benchmark surfaces already approved or collected
→ docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json + current adoption profile/matrix + REUSABLE_MODULE_REGISTRY
→ Base accumulated knowledge/case/reference owners relevant to the current decision
→ targeted cross-project verified implementation/pattern evidence only when the registry/profile/current bottleneck points to it
→ benchmark + professional practice + success/failure cases (all L1+ work: task-appropriate source set)
→ owner-specific reuse/adapt/reference/no-reuse disposition
→ >= 3 materially distinct alternatives
→ Implementation Reality Gate
→ provisional best long-term option
```

모든 파일을 무작정 읽는다는 뜻이 아니라 Registry·Documentation Map·프로젝트 정본으로 **이번 변경의 실제 owner와 영향 consumer를 빠짐없이 식별**한다. Base 자체 작업은 Base repository owner를, 프로젝트 작업은 exact project repository와 파생 PDF를 먼저 읽는다. `V4_NOTION_EXCEPTION_ONLY`: `NO_NEW_NOTION_WRITE_BY_DEFAULT`이며 Notion은 명시된 V4 exception 또는 UNIQUE material을 가진 legacy migration source일 때만 그 scope를 read-only로 대조하거나 승인된 예외 쓰기·destination readback을 수행한다. open/draft/ready PR은 `OPEN_PR_READ_ONLY_BY_DEFAULT`로 확인하되 명시적 권한 없이 흡수·수정하지 않는다.

`REUSE_FIRST_PREFLIGHT_REQUIRED`: 신규 또는 의미 있게 개정하는 시스템·메커닉·데이터/콘텐츠 구조·UI/UX·시각/Asset·도구/자동화·workflow·Skill/Eval·QA/Test는 신규 설계·제작 전에 위 source order를 실제로 확인한다. 현재 프로젝트에서 이미 해결된 구현·컴포넌트·Scene·Resource·자산·테스트가 있으면 그것이 첫 후보이고, 프로젝트의 승인된 Asset/Reference/Benchmark와 Base의 reuse handoff/profile/matrix/Registry 및 **Base accumulated knowledge/case/reference**를 fresh external research보다 먼저 확인한다. 다른 프로젝트는 모든 프로젝트를 전수 검색하지 않고 Registry/profile/current bottleneck이 가리키는 직접 관련 consumer만 targeted cross-project evidence로 확인한다.

적용 대상에서 preflight가 `NOT_RUN`이면 신규 제작·custom design·`BUILD_NEW` readiness는 `BLOCKED_UNVERIFIED`다. 동일 승인 범위에서 이미 수행한 preflight의 scope·consumer·freshness가 변하지 않았으면 `REUSED_EVIDENCE`로 재사용할 수 있다. 오탈자·형식 정리처럼 새 설계/제작 판단이 없는 기계적 작업은 이유가 있는 `NOT_APPLICABLE`을 허용한다. Base나 타 프로젝트 후보는 프로젝트 정본·고유 경험을 덮어쓰지 않으며, 발견만으로 project adoption·Asset 승인·runtime proof가 되지 않는다. disposition은 해당 owner가 이미 가진 `REUSE / ADAPT / REFERENCE_ONLY / NO_REUSE / BUILD_NEW` 등 기존 어휘를 사용하고 새 공용 taxonomy를 만들지 않는다.

`MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT` / `BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED`: Base·프로젝트의 모든 L1+ 작업은 변경 전에 task-appropriate benchmark를 실제로 수행한다. 먼저 exact repository revision의 같은 책임·실제 consumer·현재 설정을 비교하고, 그 뒤 current Base 사례·승인 Reference/Benchmark·직접 관련 유사 구현·필요한 공식 원출처를 검토한다. 결과는 기존 work contract 또는 start receipt에 `benchmark_preflight_state: PASS | REUSED_EVIDENCE | NOT_APPLICABLE | BLOCKED_UNVERIFIED`, `source_and_evidence`, `observed_pattern`, `project_fit_and_difference`, `ADOPT / ADAPT / REJECT | NOT_APPLICABLE`로 남긴다. 이 절차는 고정된 게임 장르·화면·메뉴 목록·그림체·구도를 주입하지 않는다. 현재 프로젝트의 세계관·플랫폼·계약·실제 소비처에 맞는 방향과 필요한 flow를 찾는 비교 단계다. L0 순수 기계 수정만 이유가 있는 `NOT_APPLICABLE`이고, 필수 원출처를 읽지 못하면 추측으로 진행하지 않는다.

`LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED`: 같은 preflight에서 이번 범위의 context·설정·entrypoint·문서·생성물을 `ACTIVE_OWNER | COMPATIBILITY | ARCHIVE | OBSOLETE_CANDIDATE | UNKNOWN_UNVERIFIED`로 구분한다. `NO_BROAD_SWEEP_WITHOUT_SCOPE`: token 절감을 이유로 저장소 전체를 무차별 재작성하지 않는다. `NO_DELETION_BY_AGE_OR_NAME`: 날짜·구형 이름·파일명만으로 삭제하지 않는다. 실제 제거는 `REFERENCES_AND_CONSUMERS_ZERO_BEFORE_REMOVAL`과 `GIT_RECOVERABLE_REMOVAL_AND_READBACK`을 충족한 뒤 연결 문서·생성물·검증 경로를 다시 읽고 수행한다. source·consumer·provenance를 읽지 못한 자료는 `UNKNOWN_UNVERIFIED`로 보존하며, archive·compatibility 자료를 current owner로 오인하지 않도록 entrypoint와 documentation map만 먼저 교정한다.

`PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT`: 위 조사가 끝난 뒤 BUILD 전에 사용자에게 최소 다음을 한 묶음으로 보고한다.

```text
현재 상태 / 발견 문제
→ 변경 전
→ 변경 후
→ 기대효과
→ 예상 위험·부작용
→ 완화책
→ 수정 대상/보호 대상
→ 롤백
→ 실제 검증 계획과 NOT_RUN ceiling
```

보고는 이미 수행한 조사·대안·적대적 검토 evidence를 요약하는 단계이며, “앞으로 조사하겠다”는 계획만으로 이 Gate를 통과하지 않는다.

`USER_APPROVAL_BEFORE_BUILD`: 새 기획 결정·구조 변경·정책 변경·중요 제품 변경은 위 설계 묶음의 사용자 승인 뒤에만 BUILD한다. 기존 승인 계약의 동일 범위 continuation은 approval reference를 재사용하며 routine 단계마다 다시 묻지 않는다.

`REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK`: 승인된 작업 중 새로 확정된 결정·Flow·Visual·핵심 데이터는 작업 종료까지 미루지 않고 올바른 repository owner에 같은 승인 단위로 반영하고 commit/readback한다. 사람이 보는 정보는 exact source SHA를 지닌 `HUMAN_GDD_PDF_DERIVED_VIEW` 또는 repository-native view로 갱신한다. `V4_NOTION_EXCEPTION_ONLY`인 경우에만 예외 contract의 owner·scope·value·exit/revisit 조건에 맞는 destination을 추가 갱신·readback하며, GitHub와 Notion의 역할을 복제하지 않는다. structured/runtime 의미가 바뀌면 repository를 먼저 동기화한다.

`POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK`: 구현·문서·파생 view·적용 가능한 V4 exception 변경 뒤에는 결과가 “작성됐다”는 사실만 보지 않는다. 실제 변경 상태 전체를 `running-adversarial-review-and-refinement`의 완전한 개선 루프로 최소 5회, 이후 clean까지 다시 검토하고, 같은 Goal의 open/recent PR·current main·repository/PDF readback·consumer/reference freshness·Implementation Reality evidence를 재확인한다. V4 exception이 실제 적용됐을 때만 해당 destination readback을 추가한다. valid finding을 수정해 candidate가 바뀌면 수정 결과를 다시 전체 범위로 검토한다.

`REUSE_LEARNING_HANDOFF_REQUIRED`: reuse-first가 적용된 작업의 종료에서는 `PROJECT_WORK_REUSE_HANDOFF.json`이 이미 정의한 `selected_modules / reuse_mode / project_paths_changed / verification_evidence / evidence_ceiling / rollback / project_only_lessons / base_promotion_candidates`를 평가한다. 실제 새 학습이 없으면 `NO_NEW_REUSE_LEARNING`으로 닫고 Registry/Notion/Base 문서 churn을 만들지 않는다. Base 승격은 기존 promotion gate와 실제 consumer/regression evidence를 통과한 경우에만 수행하며 프로젝트 전용 교훈은 프로젝트 owner에 남긴다.

이 Gate는 `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, `docs/CONFIRMED_DECISION_SYNC_POLICY.md`와 reuse owner의 기존 계약을 재서술하는 새 정본이 아니라 intake에서 **그 owner들을 건너뛰지 못하게 만드는 실행 진입 계약**이다.

`CONTINUATION_INTENT_ALIASES`는 `[연속작업] 진행해`뿐 아니라 이미 승인된 동일 계약에 대한 `진행해`, `계속해`, `남은 작업 진행` 같은 명확한 계속 실행 의도를 인식한다. 유효한 approval reference가 있을 때만 `APPROVED_CONTRACT_CONTINUATION`으로 `references/continuous-work-execution.md`를 적용해 남은 범위에 `CONTINUOUS_WORK_ACTIVE`를 결합한다. 이는 `PLAN / BUILD / REVIEW`를 대체하거나 새 범위를 승인하지 않으며, 사용자 전용 결정·미검증 차단·고위험 외부 행위의 확인 Gate를 제거하지 않는다. blocker가 생기면 즉시 전역 종료하지 않고 `recover → local defer → independent ready work → global stop last` 순서로 처리한다.

명시적인 user-directed 계속 작업에서 `same-goal`의 `in-progress PR`이 이미 있으면 `USER_DIRECTED_PARALLEL_PR`로 라우팅한다. 기존 PR은 read-only overlap evidence로만 확인하고 **do not modify/rebase/update** 하며, **current completed main**에서 **separate branch/PR**을 만든다. ordinary same-workstream coordination에서 허용된 경우 `synchronizing-local-and-github-state`의 concurrent preflight와 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 사용할 수 있다.

그러나 `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 항상 먼저 적용된다. 현재 작업의 더 구체적인 승인 계약이 다른 open/draft/ready PR 또는 다른 workstream을 `read-only / no absorption`으로 지정하면 standing copy-integration보다 우선한다. 그 PR의 material delta를 own 작업으로 가져오려면 **explicit absorption authorization**이 별도로 있어야 하며, 다른 workstream에는 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`을 충족해야 한다. 없으면 overlap 탐지·경로 회피·main의 이미 병합된 결과 재평가만 수행하고 selective copy·재구현·흡수·close·supersede 처리를 하지 않는다.

흡수가 명시적으로 허용된 ordinary coordination에서만 `PROVISIONAL_INTEGRATION`을 사용한다. owner PR branches는 read-only로 보존하고 필요한 material delta만 selective copy·재구현한 뒤 semantic reconciliation과 exact-head 검증을 수행한다. `absorbed_owner_deltas`와 `residual_owner_deltas`로 coverage를 증명한다. `scheduled/periodic` repository-writing automation도 unrelated open PR 존재 자체를 전역 blocker로 사용하지 않고 실제 path/semantic overlap만 국소 조정한다. 상세 경계는 `references/continuous-work-execution.md`와 `synchronizing-local-and-github-state`를 따른다.

`PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER` / `VIDEO_LINK_IS_NOT_UNREADABLE_UNTIL_DECLARED_READER_LADDER_EXHAUSTED`: 사용자가 YouTube 같은 공개 영상의 내용 확인·요약·역공학·흡수를 요청하면 일반 웹 페이지 렌더 실패만으로 링크를 읽을 수 없다고 판정하지 않는다. 먼저 `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`의 현행 `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`와 `tools/public_video_research_ingest.py`를 읽고, 해당 owner가 선언한 `source_ladder`와 evidence ceiling을 실제로 실행한다.

```text
exact video/source identity readback
→ current owner-declared source_ladder
→ normalize any already-available local transcript through the existing adapter
→ preserve ASR_FALLBACK_REQUIRED and source-binding ceiling
→ only after the declared reader ladder is exhausted: BLOCKED_UNVERIFIED
```

- 이 route는 root `AGENTS.md`의 unreadable external-link blocker를 약화하거나 별도 자막 정본을 만들지 않는다. 전용 owner가 이미 선언한 reader와 허용 fallback을 소진하기 전에는 “현재 도구로 읽지 못함”이 확정되지 않았다는 source-specific dispatch다.
- 영상·오디오 자체를 자동 다운로드하거나 `yt-dlp`·ASR·새 패키지를 자동 설치하지 않는다. hosted transcript SaaS·paid proxy·별도 유료 API/계정/credit를 기본 fallback으로 추가하지 않는다.
- 자막 전문은 local research evidence로만 다루고 repository에는 결정에 필요한 파생 요약·짧은 인용·timestamp·source identity만 남긴다.
- local transcript는 원 영상 binding과 생성 출처가 별도 검증되기 전 `UNVERIFIED`다. `TRANSCRIPT_READY_IS_NOT_FACT_OR_PROJECT_FIT_PASS`: caption ingest 성공도 발언의 사실성·프로젝트 적합성·Base 흡수 승인이 아니다.
- 내용 증거를 확보한 뒤 `PROJECT_REUSE_OPPORTUNITY_SCAN`과 현재 owner 비교로 `ADOPT / ADAPT / REJECT`를 판정한다. 제목·검색 스니펫·주변 자료를 본문 대신 사용하지 않는다.

`AI_SOLUTION_LAYER_SELECTION_BEFORE_BUILD`: 새 LLM·multimodal·RLHF/fine-tuning·prompt/context·knowledge base/RAG·API/MCP·agent/workflow/harness·AGI/ASI 관련 기능·도구·구조 요청은 `docs/CAPABILITY_COMPOSITION_MAP.md`의 `AI_SOLUTION_LAYER_SELECTION`으로 먼저 라우팅한다. 용어 목록을 feature backlog로 바꾸지 않고 `measured bottleneck → smallest sufficient layer → existing owner/actual consumer → eval/evidence` 순서로 판정한다.

- `NO_AUTO_FEATURE_FROM_VOCABULARY`: 영상·기사에서 유용한 용어를 발견했다는 사실만으로 runtime, dependency, paid service, provider, framework, fine-tuning, vector database 또는 MCP server를 추가하지 않는다. 실제 consumer와 Existing Solution First 비교를 거친 최소 `BUILD_NEW`만 별도 승인·검증한다.

새 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층 요청은 일반 설계보다 먼저 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`와 `evaluating-godot-assets-and-plugins-before-creation: inventory-current-environment / disposition`으로 라우팅한다. `existing_solution_disposition`과 비교 증거·사용자 승인 상태 없이 `BUILD_NEW` 계약을 만들지 않는다.

## Terminology

- `Work Mode`: AI의 현재 작업 자세·권한·증거 기준. `PLAN / BUILD / REVIEW` 중 한 시점에 하나를 주로 사용한다.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 전문 작업 계약.
- `Skill Mode`: 한 Skill 안에서 선택하는 세부 절차. 이 문서의 `route`, `first-prompt`, `clarify` 등이 해당한다.
- `Prompt`: 사용자의 현재 목표·제약·산출물. Skill 선언문이 아니다.
- `Direction anchor`: 지시문 가장 앞에서 핵심 행동·결과·지배 기준을 고정하는 1~2문장. 배치 순서는 권한을 만들지 않는다.
- `Continuous Work`: 유효한 승인 계약과 `CONTINUATION_INTENT_ALIASES`가 함께 있을 때 `APPROVED_CONTRACT_CONTINUATION`으로 활성화되는 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 상태. Work Mode가 아니라 승인된 계약 안에서 다음 미완료 작업으로 계속 이동하는 orchestration flag다.

상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

승인 결정 복원·중복 질문 방지·Repository/Notion 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

프로젝트 workspace 권위: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` (`DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`, `REPOSITORY_PRIMARY_CANON`, `HUMAN_GDD_PDF_DERIVED_VIEW`, legacy Notion/Google Sheets migration boundary). V3 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`은 `V3_COMPATIBILITY_AND_HISTORY_ONLY`이며 신규 project work route가 아니다.

legacy Google Sheets 해석·이관이 필요한 경우에만 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 compatibility 계약을 참고한다. 이는 신규 입력이나 active workspace 권위를 만들지 않는다. 기존 consumer가 사용하는 legacy literal `project_google_sheet`는 `google_sheet_compatibility_source`의 호환 alias일 뿐이며 신규 Sheet·active sync·정본 권위를 뜻하지 않는다.

연속작업 활성화·자동 승인·blocker recovery·종료 경계: `references/continuous-work-execution.md`

예기치 않은 실행 중단의 Retry/Resume·Watchdog 신호·중복 실행 방지: `references/task-recovery-protocol.md`

## Skill Modes

- `route`: 요청 의도·현재 단계·위험을 파악하고 Work Mode, 작업 수준, 변경 유형, 주 책임 분야와 최소 Skill 집합을 자동 판정한다. `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 계속 실행 의도와 기존 approval reference를 함께 감지한다.
- `first-prompt`: 핵심 방향 문장을 지시문 가장 앞에 배치하고 Task·Context·Source·Constraints·Output·Validation을 순서화한 뒤 전체 계약과 충돌하지 않는지 검사한다. 상세 절차는 `references/first-prompt-direction-anchoring.md`를 사용한다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환하고, opt-in이 있으면 현재 승인 범위에 `continuous_work_state`를 결합한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다. 모든 L1 이상 지시문은 실행 전 `Grill Me alignment gate`를 거치며, 프로젝트 방향을 바꾸는 핵심 결정은 `references/grill-me-protocol.md`를 사용한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.
- `execution-report`: 실제 실행한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다.

하나의 호출에서 필요한 Skill Mode만 순서대로 실행한다. L1 이상 지시문 작성의 기본 순서는 `route → first-prompt → contract → clarify`다. 이미 exact contract already approved 상태이고 유효한 approval reference가 있으면 `clarify`는 승인 재사용을 기록하고 중복 질문하지 않는다. `CONTINUATION_INTENT_ALIASES`는 미승인 계약을 임의 승인하지 않으며, `CONFIRMED` 또는 `REUSED_APPROVAL` 이후 현재 승인 범위에 연속 실행 상태를 적용한다. `decompose-and-sequence`는 `CONFIRMED` 이후에만 실행한다. L1 이상 작업 종료 시 `execution-report`를 실행하되 짧은 작업에서는 최종 답변의 한 섹션으로 압축할 수 있다.

## Work Mode selection

### `PLAN`

- 요구·근거·설계·정본·작업 순서를 확정한다.
- 읽기·조사·제안이 기본이며 승인 전 제품 동작·구조를 변경하지 않는다.

### `BUILD`

- 승인된 계약 범위의 코드·데이터·문서·자산을 구현한다.
- 단계별 검증·롤백을 유지한다.

### `REVIEW`

- 결과를 적대적으로 검토하고 반례·회귀·증거를 찾는다.
- 기본 읽기 전용이다. 수정까지 요청되거나 승인된 finding이 있으면 `BUILD`로 전환해 최소 수정하고 다시 `REVIEW`로 검증한다.

복합 작업은 `PLAN → BUILD → REVIEW`로 전환할 수 있지만 한 시점의 주 Work Mode는 하나다. `CONTINUOUS_WORK_ACTIVE`에서도 이 규칙은 동일하다.

## Automatic selection policy

- 사용자가 Skill·Skill Mode를 언급하지 않아도 현재 요청과 Registry trigger를 비교한다.
- `load_by_default=false`는 자동 선택 금지가 아니라 trigger 불일치 시 읽지 않는다는 뜻이다.
- trigger가 일치하고 `do_not_use_when`에 걸리지 않는 최소 집합만 사용한다.
- 새 기능 또는 기능 계약·공개 경계의 의미 변경은 trigger가 일치한 것으로 보고, 작업 크기·단계 수와 무관하게 intake와 기능 계약 reference를 사용한다.
- 주 책임 분야 Skill은 최대 하나다. Foundation·검증·발행·Handoff는 현재 단계에 필요한 것만 추가한다.
- 사용자에게 “어떤 Skill을 쓸까요?”라고 선택을 전가하지 않는다.
- 사용자가 Skill을 지정해도 trigger·권한·비사용 조건과 충돌하면 그대로 실행하지 않고 이유를 설명한다.
- 새 범위·실패·정본 변경이 생기면 Work Mode와 Skill 라우팅을 다시 계산한다.
- Skill 파일을 읽은 것과 Skill 절차를 실제 실행한 것을 구분한다.
- L1 이상 작업을 다른 에이전트·Codex·외부 AI에 넘기는 지시문도 먼저 이 Skill의 `first-prompt → contract → clarify`를 거친다.
- 신규 실행 기술 제작 압력이 감지되면 설계 Skill보다 기존 대안 평가 Skill을 먼저 호출하고 `existing_solution_disposition`을 계약 입력으로 요구한다.
- 유효한 approval reference 또는 명확한 계속 실행 의도 중 하나라도 없으면 `CONTINUOUS_WORK_INACTIVE`로 유지하고 기존 승인·Grill Me 흐름을 바꾸지 않는다.

## Use when

- 새 L1 이상 요청 또는 여러 분야에 걸친 요청을 접수한다.
- 기능·게임 경험·아트 방향·아키텍처·워크플로·Base 변경을 결정한다.
- 새 기능 또는 기능 계약·공개 경계·상태 소유권·consumer 연결을 만들거나 의미 있게 바꾼다. 단일 파일·단일 단계의 작은 기능도 포함한다.
- 요청이 짧거나 모호하거나 여러 파일·산출물에 영향을 준다.
- 승인된 요구를 Issue·Goal·Plan 또는 실행 프롬프트로 넘긴다.
- GPT·Codex·외부 AI용 작업 지시문을 작성하거나 개선한다.
- 큰 작업을 단계·의존성·병렬 묶음·게이트로 분해한다.
- 범위가 바뀌어 분야·Skill·검증·실행 순서를 다시 계산한다.
- 새 MCP·addon·CLI·framework·Skill·Mode 또는 기존 실행 권위와 겹칠 수 있는 도구를 제안한다.
- 사용자가 `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 등으로 현재 승인된 동일 계약의 연속 실행을 명시적으로 요청한다.

## Do not use when

- 새 기능·기능 계약·공개 경계 변경이 없는 오탈자나 명확한 단일 파일 기계 수정인 L0 작업이다.
- 입력과 판정 기준이 동일한 검사를 재실행한다.
- 승인된 Plan에 분야·범위·완료·검증·실행 순서가 이미 확정됐고 기능 계약·공개 경계·상태 소유권·consumer가 변하지 않았다. 이때 기존 approval reference를 재사용한다.
- 저장소 변경·결정·검증이 없는 단순 설명이다.
- 요구가 확정되지 않았는데 구현 세부 순서부터 고정하려 한다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
current_confirmed_decisions:
  project_notion_exception_or_legacy_source:
project_asset_reference_benchmark_surfaces:
google_sheet_compatibility_source:
related_open_and_recent_prs:
documentation_map:
design_document_registry:
skill_registry:
current_stage_and_gate:
current_issue_or_approved_request:
actual_code_data_assets_tests:
delivery_constraints:
known_dependencies_and_blockers:
available_people_tools_permissions:
external_deliveries:
milestone_or_deadline:
validation_environment:
rollback_constraints:
approval_reference:
continuous_work_trigger:
continuation_intent:
continuous_work_state: CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE
copy_integration_standing_authorization: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
reuse_handoff:
reuse_preflight_state: NOT_RUN | COMPLETE | REUSED_EVIDENCE | NOT_APPLICABLE
reuse_preflight_evidence: []
reuse_disposition:
reuse_learning_handoff:
existing_solution_inventory:
  existing_solution_disposition:
  existing_solution_evidence:
    existing_solution_user_approval:
benchmark_preflight_receipt:
context_configuration_hygiene:
project_work_kanban:
```

`PROJECT_WORK_KANBAN_CHECKLIST`: `benchmark_preflight_receipt`, `context_configuration_hygiene`, `project_work_kanban`은 위 `request` metadata나 `existing_solution_evidence`의 하위 필드가 아니다. L1+ 작업에서 project/Base repository가 소유하는 **같은 root receipt JSON의 형제 필드**다. 별도 빈 PM 보드나 두 번째 상태 정본을 만들지 않는다. 아래 예시는 `validate_work_contract_receipt.py`의 실제 start 실행 Gate에 전달할 수 있는 최소 구조이며, 실제 작업에서는 예시 값을 fresh-read evidence, 현재 승인 Goal과 그 Goal의 모든 필수 작업으로 바꾼다.

WORK_CONTRACT_RECEIPT_ROOT_JSON_EXAMPLE

```json
{
  "work_level": "L1",
  "benchmark_preflight_receipt": {
    "state": "PASS",
    "entries": [
      {
        "source_and_evidence": "exact repository SHA and directly relevant approved benchmark",
        "observed_pattern": "observed owner-to-consumer boundary",
        "project_fit_and_difference": "reuse the boundary without copying project-specific values or presentation",
        "disposition": "ADAPT"
      }
    ]
  },
  "context_configuration_hygiene": {
    "scope": "only current task paths and their direct consumers",
    "inventory": [
      {
        "path": "repository-relative current owner path",
        "classification": "ACTIVE_OWNER",
        "owner_or_provenance": "verified current repository owner",
        "references_and_consumers": "direct consumer/readback checked",
        "removal_proposed": false
      }
    ]
  },
  "project_work_kanban": {
    "goal_or_slice_issue_ref": "existing approved Goal locator",
    "source_main_sha": "0123456789abcdef0123456789abcdef01234567",
    "work_item_refs": ["TASK-01"],
    "active_work_item_ref": "TASK-01",
    "next_action": "perform the next approved task",
    "work_items": [
      {
        "work_item_id": "TASK-01",
        "title": "observable approved outcome",
        "status": "IN_PROGRESS",
        "canon_owner": "repository-relative canonical owner",
        "actual_consumers": ["actual project consumer"],
        "depends_on": [],
        "acceptance_criteria": ["AC-01"],
        "required_evidence": ["E2_TEST"],
        "checklist": [
          {
            "id": "AC-01",
            "text": "condition, action, and expected result",
            "status": "NOT_RUN"
          }
        ],
        "verification": [
          {
            "level": "E2_TEST",
            "status": "NOT_RUN",
            "evidence": []
          }
        ],
        "next_action": "run the first approved implementation or verification step"
      }
    ]
  }
}
```

실행 경로는 `python <resolved-Base-root-at-current-Base-or-project-adapter-pin>/tools/validate_work_contract_receipt.py --receipt <repository-owned-json-receipt> --phase start --expected-source-sha <fresh-read-project-source-sha> --render-markdown`이다. Base root·adapter pin·receipt를 해석하지 못하거나 nonzero이면 `BLOCKED_UNVERIFIED`이며 새 설계·제작·구현을 시작하지 않는다. 작업 전환은 다음 승인 작업을 먼저 active로 기록한 뒤 같은 trusted source와 `--phase resume`으로 검사한다. 마감은 모든 필수 작업을 같은 최종 HEAD에서 다시 검증하고 `--phase closeout --expected-source-sha <fresh-read-project-source-sha> --expected-head-sha <fresh-read-final-head-sha> --render-markdown`을 실행한다. `TRUSTED_VERIFICATION_TARGET_HEAD`: receipt의 `verified_head_sha`를 기대값으로 복사하지 않고 신뢰한 caller가 final HEAD를 별도로 읽는다.

## Read first

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, repository-owned Asset/Reference/Benchmark와 exact-SHA derived PDF; V4 exception/legacy source는 적용 조건이 기록됐을 때만
4. `docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json`, current adoption profile/matrix, `REUSABLE_MODULE_REGISTRY.md`
5. 현재 결정과 관련된 기존 Base knowledge/case/reference owner
6. Registry/profile/current bottleneck이 가리키는 경우에만 직접 관련 다른 프로젝트의 검증된 implementation/pattern evidence
7. legacy Sheet에 UNIQUE 미이관 material이 실제 있을 때만 `google_sheet_compatibility_source`
8. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
9. 현재 Issue·Plan·책임 원본과 실제 파일
10. `SKILL_REGISTRY.json`
11. 신규 MCP·addon·CLI·framework·Skill·Mode이면 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`와 Godot 평가 Skill
12. L1 이상 지시문 작성 시 `references/first-prompt-direction-anchoring.md`
13. 필요한 경우 `references/question-and-source-model.md`
14. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`
15. Grill Me 정합성 확인과 핵심 결정 인터뷰가 필요한 경우 `references/grill-me-protocol.md`
16. `CONTINUATION_INTENT_ALIASES`와 유효한 승인 계약이 함께 있으면 `references/continuous-work-execution.md`
17. 새 기능 또는 기능 계약·공개 경계를 만들거나 의미 있게 바꾸는 경우에는 작업 분해가 필요하지 않은 작은 기능을 포함해 `references/work-decomposition-and-sequencing.md`; 그 밖에는 작업 분해·순서화가 필요할 때만 읽는다.

## Workflow

### 1. Route automatically once

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

새 기능 또는 기능 계약·공개 경계의 의미 변경은 크기가 작아도 `L1` 이상으로 분류한다. 이미 승인된 기능 경계를 그대로 구현하는 작은 continuation만 기존 approval reference로 intake 재작성을 생략할 수 있다.

최종 결정을 소유하는 `primary_discipline`은 하나만 지정한다. 실제 입력·산출물·검증이 바뀌는 분야만 `affected_disciplines`에 추가한다.

```text
요청 의도·현재 단계·위험
→ PLAN / BUILD / REVIEW
→ Registry trigger·do_not_use_when
→ 최소 Skill 집합
→ 각 Skill의 필요한 Skill Mode
→ CONTINUATION_INTENT_ALIASES와 approval reference 존재 여부
→ CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE 후보
```

발행·검증·Handoff Skill은 해당 단계에 도달할 때까지 `deferred_skills`에 둔다. 연속작업 후보는 승인 상태가 확인되기 전 실행 권한이 아니다.

### 1.5 Existing Solution First Gate

신규 MCP·addon·CLI·framework·Skill·Mode·execution layer 요청이면 다음을 `PLAN`의 첫 blocker로 둔다.

```text
current environment inventory
→ connected MCP·enabled addon·dependency·existing implementation
→ open/recent PR
→ maintained external solution
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
→ adversarial review
→ user-visible approval state
```

`existing_solution_disposition`이 없으면 `AWAITING_EXISTING_SOLUTION_REVIEW`다. `BUILD_NEW`는 대안으로 해결할 수 없는 차단 결함과 사용자 승인이 모두 있어야 하며, 없으면 custom design·code·PR을 만들지 않는다.

### 1.6 Reuse-First Project Preflight

새로 만들거나 의미 있게 바꾸는 시스템·메커닉·데이터/콘텐츠 구조·UI/UX·시각/Asset·도구/자동화·workflow·Skill/Eval·QA/Test는 tool-only Existing Solution First보다 넓은 `REUSE_FIRST_PREFLIGHT_REQUIRED`를 적용한다.

```text
current project authority + actual implementation/assets/tests
→ Project Asset/Reference/Benchmark already approved or collected
→ PROJECT_WORK_REUSE_HANDOFF + adoption profile/matrix + REUSABLE_MODULE_REGISTRY
→ Base accumulated knowledge/case/reference relevant to this decision
→ targeted cross-project verified evidence only when directly pointed to
→ decision-relevant external benchmark/professional practice/success-failure cases
→ owner-specific reuse/adapt/reference/no-reuse disposition
→ new creation only for the unresolved gap
```

`NOT_RUN`은 신규 제작·`BUILD_NEW`를 차단한다. `REUSED_EVIDENCE`는 동일 승인 범위·같은 consumer·freshness 확인을 만족할 때만 쓴다. `NOT_APPLICABLE`은 새 설계 판단이 없는 기계적 변경에만 이유와 함께 사용한다. 재사용 때문에 프로젝트 고유 규칙·표현·플레이어 경험을 평준화하지 않는다.

### 2. Inspect repository facts

최신 `main`, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 실제 파일과 정확한 Project Notion workspace에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. legacy Sheet는 `google_sheet_compatibility_source`에 UNIQUE 미이관 material이 있을 때만 migration evidence로 읽는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

### 3. Build one requirement model

```text
원 요청
→ 문제·목적
→ 사용자·플레이어 경험
→ 범위·비목표
→ 제약·보호 대상
→ 산출물
→ 완료 기준
→ 검증
→ 미검증·보류
```

### 3.1 Build the first prompt

모든 L1 이상 지시문 작성은 `references/first-prompt-direction-anchoring.md`를 사용한다.

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
→ conflict scan
```

- 핵심 행동·의도한 결과·지배 기준을 1~2문장으로 압축해 지시문 가장 앞에 둔다.
- Task, Context, Source, Constraints, Output, Validation을 명확히 분리한다.
- 정석안·파격안·통합안은 설계·결정 탐색에 실제 가치가 있을 때만 같은 기준으로 비교한다.
- 앞 문장이 전체 계약을 좁히거나 과장하거나 뒤의 `HARD_CONSTRAINT`와 충돌하면 전체 지시문을 다시 작성한다.
- first-prompt는 초안이며 아직 실행 권한이 없다.

### 3.5 Apply the neutral-recommendation-gate

권장안·판정·설계 선택이 있으면 사용자안과 AI 최초안을 같은 기준으로 비교한다.

```yaml
evaluation_criteria: []
alternatives: []
counterevidence: []
benefits_costs_and_risks: []
reversibility:
unknowns_and_evidence_limits: []
recommended_conclusion:
agreement_or_disagreement_reason:
```

- 사용자안이 검토를 통과하면 근거와 함께 동의한다.
- 다른 안이 더 강하면 차이를 만드는 증거와 함께 권장한다.
- 반대를 위한 반대를 만들지 않는다.
- 증거 부족은 `BLOCKED_UNVERIFIED`로 남긴다.
- L1 이상 기능·설계·아키텍처·정책·방향 결정은 `running-adversarial-review-and-refinement`의 `attack → validate-critique → decision-report`를 PLAN 사전판정 지원 Skill로 실행한다.
- 이 판정의 승인 finding은 `refine-approved-findings`에서 주 책임 분야 Skill BUILD로 한 번만 구현·수정하고, `regression-recheck → decision-report`로 복귀한다.

### 4. Run the Grill Me alignment gate

좋은 프롬프트 변환과 실행 계약 작성 뒤, 실행 전 `Grill Me alignment gate`로 의도·기획 정합성을 확인한다.

- 결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다.
- 기존 Decision이 유효하면 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부·초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.
- 상세 요청은 처음부터 다시 인터뷰하지 않고 direction anchor와 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.
- 계약이 완전하지만 승인되지 않았다면 direction anchor·범위·보호 대상·산출물·검증을 한 번 보여 주고 명시적 승인을 받는다.
- exact contract already approved 상태이면 approval reference를 기록하고 중복 질문 없이 `REUSED_APPROVAL`로 통과한다.
- 중대한 승인 또는 확인이 없으면 `AWAITING_USER_CONFIRMATION`을 유지하고 BUILD·위임·실행으로 이동하지 않는다.

### 5. Closure and confirmation

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

확인 결과는 `CONFIRMED` 또는 `REUSED_APPROVAL`과 approval reference로 기록한다.

### 5.5 Activate bounded continuous work for an approved contract

`[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 `CONTINUATION_INTENT_ALIASES`가 있고 현재 계약이 `CONFIRMED` 또는 `REUSED_APPROVAL`이면 `APPROVED_CONTRACT_CONTINUATION`으로 `references/continuous-work-execution.md`를 적용해 `CONTINUOUS_WORK_ACTIVE`로 전환한다.

```text
현재 승인된 작업 계약
→ ready task 선택
→ BUILD
→ REVIEW attack → validate-critique
→ 범위 안의 기술적 단일 최소 안전 권장안이면 자동 승인 간주
→ BUILD 최소 반영
→ REVIEW regression-recheck
→ blocker가 있으면 recovery ladder
→ 당장 해결 불가한 국소 task는 defer
→ 독립 ready task 계속
→ 상태 변화 뒤 deferred task 재평가
→ 완료 또는 GLOBAL_TERMINAL_BLOCKER까지 반복
```

`USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위는 자동 승인하지 않는다. 그러나 그 상태가 국소적이거나 복구 가능하면 전체 루프를 즉시 종료하지 않는다. `RECOVERABLE_VERIFICATION_BLOCKER`와 `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`는 재조회·대체 증거·authorized alternate executor를 먼저 시도하고, 당장 풀리지 않으면 해당 task만 defer한다. `GLOBAL_TERMINAL_BLOCKER`는 recovery path를 소진하고 실행 가능한 독립 task가 없을 때만 사용한다. 유효한 계약이나 계속 실행 의도가 없는 요청은 `CONTINUOUS_WORK_INACTIVE`다.

### 6. Produce the executable contract

```md
# 작업 제목
## Direction Anchor
## 목적
## Work Mode
## Continuous Work State
## 맥락·정본·실제 근거
## 목표 사용자·플레이어 경험
## Reuse-First Preflight and Disposition
## Existing Solution Inventory and Disposition
## 작업 범위
## 제약·제외·보호 범위
## 자동 선택 Skill·Skill Mode
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성·롤백
## Grill Me 정합성·승인 근거
## 작업 후 Skill 실행 보고
```

### 7. Decompose and sequence

승인 계약을 활동 목록이 아니라 검증 가능한 결과 단위로 나눈다.

```yaml
step_id:
outcome:
why_now:
work_mode:
inputs:
files_or_systems:
owner_or_skill:
skill_mode:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

의존성은 `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES / OPTIONAL_FOLLOWUP`으로 구분한다.

```text
환경·권한·입력 선행 조건
→ 정본·인터페이스·Schema 계약
→ 가장 위험한 가설·기술 불확실성
→ 핵심 사용자·플레이어 경로
→ 데이터·자산·인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 사용자 체감 검수·통합·인수인계
```

순서는 의존성 해소, 위험 감소, 사용자 가치, 피드백 속도, 되돌리기 난이도, 자원 충돌로 결정한다. 일정 숫자를 근거 없이 발명하지 않는다. 병렬화는 입력·출력 경계가 고정되고 같은 파일·Schema·자산을 경쟁적으로 수정하지 않으며 독립 검증이 가능할 때만 허용한다. `CONTINUOUS_WORK_ACTIVE`에서는 이 순서에서 다음 미완료 결과를 자동 선택하되 승인 범위를 넘어 새 결과를 추가하지 않는다.

### 8. Report execution

실제로 실행한 항목마다 다음을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
trigger_and_reason:
work_performed:
result:
evidence:
status: PASS/PARTIAL/FAIL/UNVERIFIED
```

최종 사용자 보고에는 최소한 다음이 있어야 한다.

```text
사용한 Work Mode·Skill·Skill Mode
→ 사용한 이유
→ 얻은 결과·증거
```

`CONTINUOUS_WORK_ACTIVE`였다면 완료한 작업, deferred 작업, blocker recovery, 적대 검토 finding, 자동 승인해 반영한 기술 권장안, 검증 증거, 종료 상태를 최종 보고에 함께 남긴다.

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음` 중 하나로 이유를 기록한다. 모든 Registry 항목을 나열하지 않는다.

템플릿: `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## Project workspace handling

```yaml
workspace_authority: DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
project_canon: REPOSITORY_PRIMARY_CANON
human_facing_view: HUMAN_GDD_PDF_DERIVED_VIEW
notion: LEGACY_OPTIONAL_READ_ONLY_MIGRATION_SOURCE
google_sheets: MIGRATION_COMPATIBILITY_ONLY
google_sheet_compatibility_source: OPTIONAL_LEGACY_MIGRATION_INPUT
```

- 최신 repository 정본·실제 파일을 현재 계획·결정·구조화·runtime truth로 읽고, 사람용 PDF에는 exact source SHA와 evidence ceiling을 기록한다.
- Base 자체 작업처럼 project-scoped migration surface가 적용되지 않으면 목적지를 발명하지 않는다.
- 기존 Notion 또는 Google Sheet가 실제 존재하면 고유 사용자 자료를 `UNIQUE / DUPLICATE / OBSOLETE`로 판정한다. `UNIQUE`만 repository 또는 명시적 non-canon 보관소로 이관 → readback/Test → consumer/reference 확인한다.
- Notion과 Sheet는 신규 입력·active Decision sync·완료 판정에 필요하지 않으며 신규 프로젝트에 생성하지 않는다. V4 예외는 explicit user approval, owner, scope, measurable value, revisit/exit 조건이 있을 때만 적용한다.

## State model

```text
RECEIVED
→ ROUTED
→ AWAITING_REUSE_PREFLIGHT | AWAITING_EXISTING_SOLUTION_REVIEW | PROMPT_DRAFTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED | REUSED_APPROVAL
→ CONTRACT_READY
→ EXECUTION_PLAN_READY
→ EXECUTED
→ REPORTED
→ SUPERSEDED | ABANDONED
```

연속작업은 위 상태 머신을 대체하지 않는 직교 실행 flag다.

```text
CONTINUOUS_WORK_INACTIVE
→ (CONTINUATION_INTENT_ALIASES + CONFIRMED/REUSED_APPROVAL)
→ CONTINUOUS_WORK_ACTIVE
→ COMPLETE | STOPPED_USER_DECISION | GLOBAL_TERMINAL_BLOCKER | STOPPED_BY_USER
```

`BLOCKED_UNVERIFIED`, `EVIDENCE_TRANSPORT_INCOMPLETE`, `DEFERRED_EXTERNAL_EXECUTOR`는 개별 task/evidence 상태가 될 수 있으며 자동으로 전역 종료 상태가 되지 않는다.

## Output contract

```yaml
work_mode:
work_level:
change_types: []
primary_discipline:
affected_disciplines: []
foundation_skills: []
discipline_skills: []
deferred_skills: []
read_first: []
actual_paths: []
reuse_preflight_state: NOT_RUN | COMPLETE | REUSED_EVIDENCE | NOT_APPLICABLE
reuse_preflight_evidence: []
reuse_candidates: []
reuse_disposition:
reuse_learning_handoff:
existing_solution_inventory: []
existing_solution_disposition:
existing_solution_evidence: []
existing_solution_user_approval:
direction_anchor:
prompt_contract:
prompt_conflict_scan:
requirement_status:
approval_state:
approval_reference:
user_confirmation_ref:
continuous_work_trigger:
continuous_work_state: CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE
work_contract_path:
execution_sequence_path:
steps: []
dependencies: []
parallel_batches: []
gates: []
validation: []
skill_execution_report: []
remaining_unknowns: []
```

## Definition of Done

- 사용자가 Skill을 선언하지 않아도 trigger 기반으로 Work Mode·최소 Skill·Skill Mode를 자동 선택했다.
- 같은 요청의 수준·분야·범위를 여러 Skill에서 다시 판정하지 않았다.
- 저장소 사실과 사용자 판단이 구분됐다.
- 적용 대상이면 `REUSE_FIRST_PREFLIGHT_REQUIRED`로 현재 프로젝트 → Project Asset/Reference/Benchmark → Base reuse + accumulated knowledge/case/reference → targeted cross-project → decision-relevant external benchmark 순서를 확인하고 disposition을 남겼다.
- 적용 대상의 `reuse_preflight_state`가 `NOT_RUN`인 채 신규 제작·`BUILD_NEW`로 이동하지 않았다. `REUSED_EVIDENCE`와 `NOT_APPLICABLE`은 각각 동일 범위 freshness와 기계적 변경 근거를 남겼다.
- 신규 실행 기술이면 current environment와 external alternative를 조사하고 `existing_solution_disposition`을 기록했다.
- `BUILD_NEW`이면 대안으로 해결 불가능한 결함과 사용자 승인이 있다.
- 모든 L1 이상 지시문 작성에서 `first-prompt → contract → clarify`가 실행됐다.
- direction anchor가 지시문 가장 앞에 있고 전체 범위·제약·산출물과 일치한다.
- Task·Context·Source·Constraints·Output·Validation이 추적된다.
- 범위·제외·보호·완료·검증이 추적된다.
- `FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`으로 Base/Project repository·exact-SHA derived view·Skill/open-recent PR/실제 구현 상태가 현재 작업 범위에서 감사됐고, V4 exception/legacy source는 적용될 때만 대조됐다.
- `PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT`의 변경 전·변경 후·기대효과·위험·롤백·검증 계획이 BUILD 전에 보고됐다.
- 필요한 사용자 확인 전에는 구현 계약이나 실행 순서를 확정하지 않았다.
- `USER_APPROVAL_BEFORE_BUILD` 또는 유효한 기존 approval reference가 확인됐다.
- 승인된 사람이 봐야 할 결정은 `REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK`로 repository와 exact-SHA derived view에 필요한 시점에 반영·readback됐고, V4 exception은 실제 적용됐을 때만 별도 destination readback됐다.
- BUILD 뒤 `POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK`로 전체 결과·PR·main·repository/PDF·consumer를 다시 검토했고, V4 exception은 적용됐을 때만 재확인했다.
- reuse-first가 적용된 작업 종료에서 `REUSE_LEARNING_HANDOFF_REQUIRED`를 평가했고, 새 학습이 없으면 `NO_NEW_REUSE_LEARNING`으로 종료해 억지 Base churn을 만들지 않았다.
- 권장안이 있으면 사용자안과 AI 최초안에 동일한 평가 기준·대안·반증·위험·되돌리기 난이도를 적용했다.
- Grill Me alignment gate 또는 유효한 approval reference가 실행 전에 확인됐다.
- 기존 승인 계약에는 중복 질문하지 않았다.
- `CONTINUATION_INTENT_ALIASES`와 유효한 승인 계약이 함께 있을 때만 `CONTINUOUS_WORK_ACTIVE`를 사용했고, 승인된 계약 밖으로 범위를 넓히지 않았다.
- 연속작업 중 사용자 결정·고위험 행위는 자동 승인하지 않았고, recoverable/local blocker는 recovery ladder와 independent-ready-task scan 없이 전역 종료하지 않았다.
- 승인된 동일 범위의 구현·검증 방법과 병합에는 기존 approval reference와 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 재사용했다.
- `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 적용되는 다른 workstream PR은 `explicit absorption authorization` 없이 흡수하지 않았다.
- `REPOSITORY_PRIMARY_CANON`과 `HUMAN_GDD_PDF_DERIVED_VIEW`의 역할이 분리됐고 Notion/Google Sheets는 V4 exception 또는 migration source로만 남는다.
- 새 기능 또는 의미 있는 기능 계약 변경은 크기와 무관하게 정본 owner·공개/통합 경계·실제 consumer/의존 방향·검증·롤백이 `execution_sequence_path`의 기능별 코드·계약 경계에 연결됐다.
- 큰 작업은 독립 검증 가능한 결과·의존성·병렬 묶음·게이트로 분해됐다.
- 실제 사용한 Work Mode·Skill·Skill Mode의 이유와 결과·증거를 보고했다.
- 새 작업자가 같은 입력에서 동등한 계약·라우팅·실행 보고를 복원할 수 있다.

## Failure conditions

- 사용자에게 Skill 이름이나 Skill Mode 선언을 요구함
- Work Mode와 Skill Mode를 같은 개념으로 혼용함
- 전체 skills 폴더를 기본 로드함
- trigger 없이 임의로 Skill을 호출함
- 작은 단일 파일·단일 단계라는 이유로 새 기능 또는 기능 계약·공개 경계 변경을 intake와 기능 계약 reference 없이 실행함
- 실행계획에서 기능 계약 정본 owner·공개/통합 경계·실제 consumer/의존 방향을 누락함
- 적용 대상 신규 설계·제작에서 `REUSE_FIRST_PREFLIGHT_REQUIRED`를 생략하거나 `NOT_RUN`인데 신규 제작·`BUILD_NEW`로 이동함
- Base Registry/profile가 좁은 consumer를 가리키는데도 모든 프로젝트를 전수 검색해 비용·context를 불필요하게 늘림
- Project Asset/Reference/Benchmark 또는 Base accumulated knowledge/case/reference를 확인하지 않고 같은 내용을 외부에서 처음부터 재조사함
- stale/다른 범위 evidence를 `REUSED_EVIDENCE`로 재사용하거나 설계 판단이 있는데 `NOT_APPLICABLE`로 우회함
- 후보 발견을 project adoption·Asset 승인·runtime proof로 승격함
- reuse-first 적용 작업 종료에서 `REUSE_LEARNING_HANDOFF_REQUIRED`를 생략하거나 새 학습이 없는데 Registry churn을 만듦
- 현재 사용 도구·connected MCP·addon·관련 PR 조사 없이 custom MCP/addon/Skill/framework 설계 시작
- `existing_solution_disposition` 또는 사용자 승인 없이 `BUILD_NEW`
- L1 이상 지시문을 intake·좋은 프롬프트 변환 없이 바로 작성하거나 실행함
- 핵심 방향 문장을 뒤쪽에 숨기거나 전체 계약과 다르게 작성함
- 앞 문장의 순서를 근거로 `HARD_CONSTRAINT`·정본·상위 지시를 덮어씀
- Task·Context·Source·Constraints·Output·Validation 중 필요한 항목을 누락함
- `FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`의 실제 조사 없이 바로 계획·결론을 제시함
- 계획만 말하고 `PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT`를 완료 증거처럼 취급함
- `USER_APPROVAL_BEFORE_BUILD` 없이 중요 구조·기획·정책을 구현함
- 승인된 human-facing 변경을 repository 및 exact-SHA derived view에 반영하지 않거나, V4 exception을 일반 기본 Notion write로 바꾼 채 `SYNCED`로 주장함
- BUILD 뒤 전체 적대적 검토와 PR/main/repository-derived-view 재확인을 생략함
- 기계적 작업에도 정석안·파격안·통합안을 강제함
- 저장소에서 확인할 사실을 사용자에게 질문함
- 주 책임 분야를 여러 개 지정함
- 상세 요청을 무시하고 포괄 질문을 반복함
- exact contract already approved인데 approval reference를 무시하고 중복 질문함
- Grill Me alignment gate 또는 유효 승인 없이 실행 계약·BUILD·위임으로 이동함
- 유효한 승인 계약이나 명확한 계속 실행 의도 없이 일반 요청을 연속작업 자동 승인으로 처리함
- 연속작업을 이유로 진짜 `USER_DECISION_REQUIRED`, 범위 확대 또는 고위험 외부 행위를 자동 승인함
- recoverable verification·현재 세션 tool 부재·국소 blocker를 recovery/defer/independent-task scan 없이 전역 종료함
- 연속작업을 scheduler·webhook·백그라운드 실행이나 다른 채팅 자동 메시지 전달로 오해함
- 실제로 호출할 수 없는 Codex/agent/executor를 실행했다고 주장함
- standing copy-integration을 더 구체적인 `read-only / no absorption` 작업 계약보다 우선함
- 다른 workstream PR을 **explicit absorption authorization** 없이 selective copy·재구현·흡수·close·supersede 처리함
- Google Sheets를 신규 입력·active 사람용 workspace·Decision sync 필수 surface로 사용함
- legacy Sheet UNIQUE material을 현행 owner readback/Test·consumer 확인 없이 삭제함
- 원 요청의 산출물을 문서로 임의 축소함
- 제외·보호·보류·미검증을 손실함
- 측정 불가능한 완료 기준만 작성함
- 활동 이름만 있는 체크리스트를 만듦
- 의존성·같은 파일 충돌·검증·롤백 없이 모든 작업을 병렬화함
- 실제로 사용하지 않은 Skill을 사용했다고 보고함
- 사용 이유·결과·증거 없이 Skill ID만 나열함
- 사용자의 선호나 AI 최초안에 근거 없이 동의함
- 적대적 검토를 반대를 위한 반대로 오용함

## Legacy aliases

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `grill-me`, `grillme`, `Grill Me` → `clarify` + `references/grill-me-protocol.md`
- `transforming-requests-into-prompts` → `first-prompt` + `contract` + `clarify`
- `[좋은 프롬프트]`, `좋은 프롬프트`, `퍼스트 프롬프트`, `first prompt` → `first-prompt` + `contract` + `clarify`
- `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` → 유효한 현재 승인 계약 + `references/continuous-work-execution.md`

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## Base v9.4 지시 권위·Context 큐레이션

L1 이상 Prompt 계약에서 강한 지시를 추가하기 전에 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 권위를 분류한다. 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 완화하지 않는다.

입력·출력·불변조건·실패조건·검증을 예시보다 먼저 정의하는 Interface-first 계약을 사용한다. 예시는 정상·실패·경계·회귀 Fixture 또는 Golden Set으로 보존한다.

Direction anchor와 first-prompt 순서화는 `references/first-prompt-direction-anchoring.md`를 따른다. Context 큐레이션은 현재 `decision_question`을 고정한 뒤 권위·freshness·representation·deduplication·known conflicts·반대 근거·`progressive_load_trigger`·`refresh_trigger`를 기록한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.

## BCP-008 L2+ 명세 추적성

`L2 이상` 작업에서 승인된 요구가 여러 Task·파일·검증으로 분산되면 `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`를 사용한다. 이 Packet은 **별도 책임 원본이 아니다**. intake는 Decision·Requirement·Acceptance ID와 범위를 연결하고, 분야 정본·실제 구현·검증의 내용을 복제하지 않는다.

```text
Decision
→ Requirement
→ Acceptance Criteria
→ Task
→ Implementation Path
→ Verification Evidence
```

- `L0·L1`에는 기본 적용하지 않는다. 다만 실제 영향이 여러 시스템·파일로 확장되면 작업 수준을 다시 판정한다.
- Packet 생성 자체를 완료로 보지 않고 `coverage_status`, `unmapped_items`, `BLOCKED_UNVERIFIED`를 기록한다.
- 문서 정본 연결은 `managing-design-documents`, 실제 diff·테스트 증거 대조는 `reviewing-and-validating-project-changes`가 소유한다.
- 같은 ID를 새 문서마다 재정의하거나 별도 Spec 정본을 만들지 않는다.
