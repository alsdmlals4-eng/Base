# Planning-First Grill Me Batch Governance Design

## Goal

Base 작업 순서에 다음 세 계약을 하나의 상태 흐름으로 통합한다.

1. 기획 우선: `L1` 이상 작업은 `PLAN`과 승인된 실행 계약 없이 `BUILD`로 진입하지 않는다.
2. 상세 데이터·초기 수치는 GPT `RECOMMENDED_DEFAULT`로 진행하되, 프로젝트 방향을 바꾸는 기획 충돌은 Grill Me로 사용자 승인 후 확정한다.
3. Grill Me 승인 Decision은 최대 10건 단위로 하나의 배치 PR에서 exact-head 검사와 적대적 검토를 통과한 뒤 병합한다.

## Existing conflict

현행 정책은 승인 Decision 한 건마다 정본과 `main`에 즉시 반영할 수 있다. 새 요구는 10건 단위 PR 검증·병합을 요구한다. 승인 기록을 10건 동안 메모리에만 누적하면 중단 복원과 즉시 동기화 계약을 깨고, 반대로 매 건 `main`에 직접 반영하면 배치 PR 검증을 우회한다.

## Authority design

상세 문구를 여러 장문 문서에 복제하지 않는다.

- `AGENTS.md`: 항상 적용되는 기획 우선·결정권·10건 상한의 불변 규칙과 상세 정책 경로
- `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`: 상태 전이, 분류, 조기 체크포인트, PR·적대적 검토·Sheet 계약의 단일 상세 원본
- `templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md`: 프로젝트 실행 기록 Template
- `tests/test_deep_interview_contract.py`: 기존 Required CI가 실제 실행하는 단일 회귀

별도 standalone 테스트를 두지 않는다. 저장소에 존재하지만 Required CI가 실행하지 않는 검증 파일이 생기는 것을 피하고, Deep Interview 계약이 정책·Template 발견성과 핵심 상태를 함께 소유한다.

이 정책은 기존 즉시 동기화를 폐기하지 않는다. Grill Me 승인에서 “즉시”는 활성 배치 Branch와 GitHub 추적 surface에 내구 기록한다는 의미이며, main 통합 완료는 배치 PR 병합 뒤에만 확정한다.

## Chosen model

```text
사용자 승인
→ 동일 Decision ID로 GitHub 추적 surface 기록
→ 활성 Grill Me 배치 Branch의 권위 문서에 즉시 반영
→ Decision별 논리 Commit
→ Sheet에는 APPROVED_PENDING_MERGE로 기록
→ 승인 10건 또는 조기 체크포인트
→ 하나의 배치 PR 갱신
→ latest exact-head required checks
→ attack → validate-critique → regression-recheck → decision-report
→ P0/P1·미해결 thread·기획 충돌 0이면 squash merge
→ merged main SHA 재조회
→ Sheet 행을 SYNCED_TO_MAIN으로 승격하고 재조회
→ 다음 Grill Me 질문
```

`10`은 최소 대기량이 아니라 한 배치의 최대 승인 Decision 수다. 다음 경우에는 10건 전에도 조기 체크포인트를 연다.

- 프로젝트 코어·주요 UX·경제·세션 구조처럼 광범위하거나 되돌리기 어려운 결정
- 정본 충돌 또는 기존 Decision 대체
- 다음 구현 패키지가 해당 Decision을 즉시 필요로 함
- 세션·인터뷰 종료, 사용자 명시 요청, 변경 diff 과대화
- 검증·Sheet·권한 실패로 다음 질문의 전제가 불안정함

10번째 승인 후에는 배치가 병합·재동기화되기 전 11번째 질문을 금지한다. 인터뷰가 10건 미만에서 끝나도 잔여 승인 건을 같은 게이트로 닫는다.

## Decision classification

### GPT recommended detailed defaults

다음은 `DETAILED_NUMERIC_DEFAULT` / `RECOMMENDED_DEFAULT`로 진행할 수 있다.

- 플레이테스트 전 밸런스 초깃값
- 쿨다운·입력 버퍼·전환 시간의 초기 시험값
- 내부 데이터 구조·로그·오류 처리·테스트 세부
- 기존 승인 기획을 구현하기 위한 가역적 기술값

각 값은 근거, 조정 조건, 검증, 정본 영향을 기록한다. 실제 테스트 결과가 없으면 확정 밸런스나 제품 검증으로 보고하지 않는다.

### Grill Me required conflicts

수치라도 난이도 곡선, 경제, 성장 속도, 세션 길이, 빌드 우열, 보상 의미, 핵심 플레이 경험을 실질적으로 바꾸면 `PLANNING_CONFLICT` / `USER_DECISION_REQUIRED` / `GRILL_ME_REQUIRED`다. 분야 정본 간 충돌, 기존 승인 Decision의 폐기·대체, 주요 UX·범위·비용 충돌도 Grill Me에서 한 번에 하나씩 승인받는다.

## Authority and state

- 승인 직후 Branch 정본은 복원 가능한 작업 권위 surface지만 `main` 통합 상태가 아니다.
- Sheet의 `APPROVED_PENDING_MERGE`는 승인 사실을 보존하지만 GitHub main 동기화 완료를 주장하지 않는다.
- `SYNCED_TO_MAIN`은 배치 PR 병합 SHA와 Sheet 재조회가 일치할 때만 사용한다.
- 동일 Goal에는 하나의 활성 Grill Me 배치 PR만 둔다.

## Verification

- `AGENTS.md`가 단일 상세 정책과 Template을 발견 가능하게 연결한다.
- 기존 CI가 실행하는 Deep Interview 회귀가 기획 우선, 분류, 10건 상한, 조기 체크포인트, exact-head, 적대적 검토, merged-main Sheet 승격을 확인한다.
- Base v9 운영 계약과 adversarial gate가 Registry·release-lock 무결성을 계속 검증한다.
- Registry와 v9.4.1 release lock bytes는 변경하지 않는다.

## Benchmark interpretation

- 작은 자기완결 변경은 검토·롤백·병합에 유리하므로 10건 고정 최소 배치는 거부한다.
- required checks는 최신 PR HEAD에서 실행된 결과만 사용한다.
- 작성과 검토 책임은 분리하고, 적대적 검토는 반대를 위한 반대가 아니라 설계·기능·복잡도·테스트·문서 영향을 확인한다.

## Non-goals

- 새 광역 Skill 추가
- Registry 또는 v9.4.1 release lock 변경
- 모든 수치를 사용자에게 질문
- 승인 Decision을 10건 동안 메모리에만 보류
- 기존 장문 운영 문서에 같은 상세 절차 복제
- Required CI가 실행하지 않는 중복 테스트 파일 추가
- 실제 외부 모델·사람·기기 검증을 자동 완료로 승격
