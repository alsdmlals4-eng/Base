# Intake Completion and Failure Checks

intake 변경의 검토·회귀·마감 시 읽는다. 새로운 작업의 기본 접수에서 모든 과거 실패 목록을 선행 로드하지 않는다. 동일 승인 계약의 전체 검토 예산은 정확히 2회이며 단계마다 재시작하지 않는다.

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
