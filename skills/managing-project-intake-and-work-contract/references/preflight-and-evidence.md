# Preflight and Evidence Gates

신규 L1+ 설계·제작 판단의 preflight 또는 해당 Gate 감사를 수행할 때 읽는다. 동일 승인·consumer·freshness가 유지된 continuation은 기존 증거를 재사용한다. 이 module은 intake의 일부이며 별도 승인 owner가 아니다.

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

`POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK`: 구현·문서·파생 view·적용 가능한 V4 exception 변경 뒤에는 결과가 “작성됐다”는 사실만 보지 않는다. 실제 변경 상태 전체를 `running-adversarial-review-and-refinement`의 전체 적대적 검토로 정확히 2회 확인하고, 같은 Goal의 open/recent PR·current main·repository/PDF readback·consumer/reference freshness·Implementation Reality evidence를 재확인한다. V4 exception이 실제 적용됐을 때만 해당 destination readback을 추가한다. valid finding으로 candidate가 바뀌면 남은 회차에서 전체 결과를 확인하고, 2회 뒤에는 영향 범위 수정·검증만 수행한다. 전체 검토를 추가하지 않는 회차 경계는 `docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md`를 따른다.

`REUSE_LEARNING_HANDOFF_REQUIRED`: reuse-first가 적용된 작업의 종료에서는 `PROJECT_WORK_REUSE_HANDOFF.json`이 이미 정의한 `selected_modules / reuse_mode / project_paths_changed / verification_evidence / evidence_ceiling / rollback / project_only_lessons / base_promotion_candidates`를 평가한다. 실제 새 학습이 없으면 `NO_NEW_REUSE_LEARNING`으로 닫고 Registry/Notion/Base 문서 churn을 만들지 않는다. Base 승격은 기존 promotion gate와 실제 consumer/regression evidence를 통과한 경우에만 수행하며 프로젝트 전용 교훈은 프로젝트 owner에 남긴다.

이 Gate는 `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, `docs/CONFIRMED_DECISION_SYNC_POLICY.md`와 reuse owner의 기존 계약을 재서술하는 새 정본이 아니라 intake에서 **그 owner들을 건너뛰지 못하게 만드는 실행 진입 계약**이다.
