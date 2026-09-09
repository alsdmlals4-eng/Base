# 기획 우선·Grill Me 결정 배치 정책

이 문서는 Base와 Base를 채택한 프로젝트에서 **기획 우선 원칙**, 상세 데이터·수치 결정권, Grill Me 승인 Decision의 기록·PR·검증·병합 순서를 책임지는 상세 정본이다.

`AGENTS.md`가 항상 적용되는 상위 규칙이며, 이 문서는 다음 정본을 Grill Me 승인 배치에 맞게 구체화한다.

- `docs/OPERATING_MODEL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/CONFIRMED_DECISION_SYNC_POLICY.md`
- `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`
- `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`

## 0. Workspace authority

프로젝트의 활성 계획·결정 동기화는 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`의 `REPOSITORY_PRIMARY_CANON`을 따른다. `V4_NOTION_EXCEPTION_ONLY` / `NO_NEW_NOTION_WRITE_BY_DEFAULT`이며 V3 `DOMAIN_SPLIT_CANON`은 compatibility/history source다.

```yaml
workspace_authority: FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER
human_workspace: APPROVED_HUMAN_BLUEPRINT_PDF_CANON
structured_workspace: REPOSITORY_PRIMARY_CANON
legacy_google_sheets: COMPATIBILITY_ONLY
```

- 사람용 프로젝트 계획·결정·설명은 repository source의 exact-SHA `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` 또는 repository-native view로 제공한다.
- 구조화 상태·실행 계약·runtime truth·Git 추적은 `REPOSITORY_PRIMARY_CANON`이 소유한다.
- Google Sheets는 `COMPATIBILITY_ONLY` legacy migration source다. 신규 입력·활성 동기화·완료 판정의 필수 surface로 사용하지 않는다.
- V4 exception이 실제로 승인된 경우에만 Notion destination을 owner·scope·value·exit/revisit 조건과 함께 동기화하고 **destination readback**으로 확인한다. 그 외에는 Notion 기록을 발명하지 않는다.

충돌 시 최신 사용자 지시와 프로젝트 `AGENTS.md` 다음으로 Base `AGENTS.md`와 이 정책을 적용한다. 기존 문서의 “승인 Decision 즉시 동기화”는 계속 유효하지만, Grill Me 승인에서는 **활성 배치 Branch의 repository owner에 즉시 내구 기록**하고 exact-SHA derived view를 갱신·재조회하는 것을 뜻한다. V4 exception은 실제 적용된 경우에만 추가 목적지를 갱신한다. 배치 PR이 병합되기 전에는 main 동기화 완료를 주장하지 않는다.

## 1. 기획 우선 원칙

```text
요청·현재 단계 복원
→ PLAN
→ 정본·실제 구현·대안·기획 충돌·완료 기준·검증·롤백
→ 필요한 Grill Me 사용자 승인
→ 승인된 실행 계약
→ BUILD
→ REVIEW
→ 정본·상태·발행·Handoff 동기화
```

- `L1` 이상 작업은 `PLAN`을 먼저 수행한다.
- 사용자 승인 또는 기존에 승인된 실행 계약 없이 제품·정본 변경 `BUILD`에 진입하지 않는다.
- `PLAN`은 장문의 문서 작성을 강제하는 단계가 아니다. 현재 결정과 구현 사실, 범위, 비목표, 충돌, 완료 기준, 검증, 롤백을 복원 가능한 수준으로 닫는 Gate다.
- `L0` 오탈자, 명백한 단일 파일 기계 수정, 동일 입력 검사 재실행은 기획 우선 Gate의 예외다.
- 이미 승인된 Plan을 실행하며 범위·전제·정본이 바뀌지 않았다면 인터뷰를 반복하지 않는다.

## 2. 상세 데이터·수치와 기획 충돌의 결정권

### 2.1 GPT 권장 기본값

다음 조건을 모두 만족하는 항목은 `DETAILED_NUMERIC_DEFAULT`이자 `RECOMMENDED_DEFAULT`로 처리한다.

```yaml
classification: DETAILED_NUMERIC_DEFAULT
decision_state: RECOMMENDED_DEFAULT
authority: GPT_RECOMMENDATION
requirements:
  - reversible
  - project_direction_unchanged
  - approved_design_implemented_without_reinterpretation
  - reason_recorded
  - adjustment_condition_recorded
  - validation_recorded
  - evidence_limit_recorded
```

예: 플레이테스트 전 초기 밸런스 시험값, 입력 버퍼·전환 시간·쿨다운의 첫 구현값, 로그·오류 처리·내부 데이터 구조·테스트 세부, 승인된 기획을 구현하기 위한 가역적 기술 수치.

GPT 권장안대로 진행하더라도 실제 테스트 전에는 확정 밸런스, 사람 검증, 제품 성숙도 상승으로 보고하지 않는다.

### 2.2 반드시 Grill Me가 필요한 기획 충돌

다음 중 하나라도 성립하면 `PLANNING_CONFLICT`, `USER_DECISION_REQUIRED`, `GRILL_ME_REQUIRED`로 승격한다.

- 난이도 곡선이 달라진다.
- 경제·가격·비용·보상 구조가 달라진다.
- 성장 속도·세션 길이·메타 진행이 달라진다.
- 특정 빌드·전략의 우열 또는 선택 의미가 달라진다.
- 보상 의미·핵심 플레이 경험·주요 UX가 달라진다.
- 프로젝트 코어·범위·콘텐츠 의미·제작 비용 우선순위가 달라진다.
- 기존 승인 Decision을 폐기·대체한다.
- 분야 책임 원본끼리 충돌한다.

```yaml
classification: PLANNING_CONFLICT
decision_state: USER_DECISION_REQUIRED
decision_protocol: GRILL_ME_REQUIRED
```

Grill Me는 저장소와 도구로 해결할 수 없는 사용자 결정만 한 번에 하나씩 묻는다. 각 질문에는 충돌, 선택지, 장단점, GPT 권장안, 선택 시 확정되는 영향을 포함한다.

## 3. 승인 Decision의 즉시 기록

사용자 승인 답변을 다음 체크포인트까지 대화 메모리나 임시 메모에만 누적하지 않는다.

```text
사용자 답변 원문
→ 동일 Decision ID 생성 또는 재사용
→ GitHub 추적 surface 기록
→ 활성 배치 Branch의 CURRENT_CONFIRMED_DECISIONS·분야 책임 원본 갱신
→ 적용 가능한 Project relation의 Notion 사람용 기록 갱신
→ destination readback
→ Decision별 논리 Commit
→ 배치 승인 수·체크포인트 사유 재계산
```

- Branch 정본은 복원 가능한 승인 작업면이지만 main 통합 완료가 아니다.
- `APPROVED_PENDING_MERGE`는 사용자 승인과 Branch Commit, 적용 가능한 사람용 목적지 readback을 보존한다는 뜻이다.
- 배치 PR 병합 전에는 `MAIN_UPDATED`, `SYNCED`, `SYNCED_TO_MAIN`을 주장하지 않는다.
- Notion 목적지가 구성되지 않았거나 적용되지 않는 작업은 내용을 추정하지 않고 `NOT_APPLICABLE` 또는 `BLOCKED_UNVERIFIED`를 사실대로 기록한다.
- legacy `google_sheet_compatibility_source`에 아직 이관되지 않은 **UNIQUE** material이 있을 때만 migration input으로 읽는다. Sheet 행 갱신은 활성 Decision sync 요구사항이 아니다.

## 4. 최대 10건 Grill Me 결정 배치

```yaml
grill_me_batch_id: GM-BATCH-YYYY-MM-DD-NN
MAX_APPROVED_DECISIONS_PER_BATCH: 10
approved_decision_count: 0
checkpoint_reason: TEN_APPROVALS | HIGH_IMPACT | CANON_CONFLICT | IMPLEMENTATION_BLOCKED | SESSION_END | USER_REQUEST | DIFF_SIZE
status: COLLECTING | CHECKPOINT_REQUIRED | BATCH_PR_OPEN | CHECKS_RUNNING | REVIEW_REQUIRED | MERGED | SYNCED_TO_MAIN | BLOCKED
```

`10`은 정확히 채워야 하는 최소량이 아니라 한 PR의 **최대 승인 Decision 수**다. 작은 자기완결 변경이 검토 정확도·롤백·병합에 유리하므로 다음 경우에는 **조기 체크포인트**를 연다.

- `HIGH_IMPACT`: 프로젝트 코어·주요 UX·경제·세션 구조 등 광범위하거나 되돌리기 어려운 결정
- `CANON_CONFLICT`: 기존 Decision 대체 또는 분야 정본 충돌
- `IMPLEMENTATION_BLOCKED`: 다음 구현 패키지가 현재 결정을 즉시 필요로 함
- `SESSION_END`: 인터뷰 또는 작업 세션 종료
- `USER_REQUEST`: 사용자가 지금 PR 검토·병합을 요청함
- `DIFF_SIZE`: 변경이 자기완결 검토 단위를 넘기기 전 분리 필요

규칙:

- 같은 Goal에는 하나의 활성 Grill Me 배치 PR만 둔다.
- 10번째 승인 뒤에는 **병합·재동기화 전 11번째 질문**을 금지한다.
- 인터뷰가 10건 미만에서 끝나도 잔여 승인 건을 같은 Gate로 닫는다.
- 배치가 `BLOCKED`면 새 질문보다 기존 배치 복구를 우선한다.
- 고위험 Decision은 10건을 기다리지 않고 조기 체크포인트로 분리한다.

## 5. 배치 PR 검증·적대적 검토·병합

```text
BATCH_PR_OPEN
→ latest exact-head required checks
→ 변경 Decision·정본·실제 구현·untouched 소비자 영향 지도
→ attack → validate-critique → regression-recheck → decision-report
→ unresolved thread 0
→ P0/P1 0
→ 사용자 결정 미해결 0
→ 저장소가 허용한 정상 merge
→ merged main SHA 재조회
→ GitHub 정본·분야 원본 재조회
→ 적용 가능한 Notion 사람용 destination 재조회
→ SYNCED_TO_MAIN
```

병합 금지 조건:

- latest exact-head required check 실패·미실행
- unresolved thread가 1개 이상
- P0/P1 finding이 1개 이상
- `PLANNING_CONFLICT` 또는 `USER_DECISION_REQUIRED` 미해결
- `BLOCKED_UNVERIFIED`
- Decision ID·Branch Commit·구조화 정본·적용 가능한 Notion 사람용 기록 사이의 의미 불일치
- destination readback 실패
- 범위 밖 제품 코드·자산·정본 변경

병합 후 `REPOSITORY_PRIMARY_CANON`과 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`의 Decision ID·결정·대체 관계·merge Commit이 일치하고 source/readback이 끝났을 때만 `SYNCED_TO_MAIN`을 사용한다. V4 exception destination은 실제 적용됐을 때만 별도 readback한다. `COMPATIBILITY_ONLY` Sheet의 migration state는 별도 상태이며 active sync 완료를 좌우하지 않는다.

## 6. 적대적 검토 체크리스트

배치마다 다음 실패 가정을 공격한다.

- 기획 우선이 불필요한 폭포수 문서 작업으로 변했다.
- GPT 권장 수치가 실제로는 플레이 경험과 프로젝트 방향을 바꿨다.
- 사용자에게 물어야 할 기획 충돌을 기술 기본값으로 숨겼다.
- 저장소에서 확인 가능한 사실을 Grill Me 질문으로 전가했다.
- 10건 배치가 너무 커져 하나의 자기완결 변경이 아니게 됐다.
- 중요한 Decision이 11번째 질문까지 지연됐다.
- 승인 내용이 Branch·정본·적용 가능한 Notion 목적지에 즉시 기록되지 않았다.
- 병합 전 main 동기화를 주장했다.
- legacy Sheet가 다시 활성 사람용 정본처럼 취급됐다.
- 같은 Goal에 여러 활성 결정 PR이 생겼다.
- 적대적 검토가 반대를 위한 반대로 변했다.
- exact-head가 아닌 이전 Commit의 성공 검사를 사용했다.

판정은 `MUST_FIX / SHOULD_FIX / OPTIONAL / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`로 구분한다.

## 7. 벤치마킹 근거와 적용 한계

공식 코드 리뷰 실무는 작은 자기완결 변경이 더 빠르고 정확하게 검토되고, 롤백·병합도 쉽다고 권장한다. 따라서 “정확히 10건을 채운 뒤 한 번에 검토”하는 고정 최소 배치는 채택하지 않고 최대 10건 상한과 조기 체크포인트를 사용한다.

- Google Engineering Practices — Small CLs: `https://google.github.io/eng-practices/review/developer/small-cls.html`
- Google Engineering Practices — Standard of Code Review: `https://google.github.io/eng-practices/review/reviewer/standard.html`
- GitHub Docs — Required status checks: `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`

외부 벤치마크는 요구사항 정본이 아니다. 이 정책은 사용자의 10회 체크포인트 의도와 Base의 복원성·검토 가능성·증거 우선 원칙을 함께 만족시키기 위한 적용안이다.

## 8. 완료 조건

- L1 이상 작업이 승인 없는 BUILD로 진입하지 않는다.
- 상세 수치 기본값과 기획 충돌이 명시적으로 분류된다.
- 기획 충돌은 Grill Me 사용자 승인 전 확정되지 않는다.
- 승인 Decision이 대화 메모리에만 남지 않고 Branch·GitHub·적용 가능한 Notion 목적지에 기록되고 destination readback이 끝난다.
- Google Sheets는 `COMPATIBILITY_ONLY`이며 신규 입력·active sync 필수 surface가 아니다.
- 한 배치가 10건을 초과하지 않는다.
- 고위험·충돌·세션 종료 시 조기 체크포인트가 열린다.
- 10번째 승인 뒤 11번째 질문이 차단된다.
- latest exact-head 검사와 적대적 검토가 모두 통과한다.
- unresolved thread 0, P0/P1 0이다.
- 병합 뒤 main과 적용 가능한 Notion destination을 재조회하고 `SYNCED_TO_MAIN`을 확인한다.

## 9. 증거 한계

정책·Template·정적 회귀 통과는 실제 프로젝트 운영 성공을 의미하지 않는다. 첫 프로젝트 Pilot 전까지 다음은 `NOT_RUN`이다.

- 실제 10건 또는 조기 체크포인트 Grill Me 배치 운영
- 사용자 질문 피로와 결정 품질 평가
- 배치 PR 크기·리뷰 시간·재작업률 측정
- 실제 프로젝트 Notion relation에 대한 end-to-end 쓰기·readback pilot
- 사람·기기·접근성 검증

> V4 정본 경로: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON`은 편집 가능한 구조화·실행·runtime·작업상태·evidence 정본이다. `USER_APPROVED_AND_MANIFEST_REGISTERED`를 충족한 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`만 불변 사람용 시각·검수 정본이다. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON`과 PDF 주석은 repository-owned fact를 직접 바꾸지 않는다. 상세 owner는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`과 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`다.
