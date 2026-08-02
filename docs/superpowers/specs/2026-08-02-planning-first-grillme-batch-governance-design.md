# Planning-First Grill Me Batch Governance Design

## Goal

Base 작업 순서에 다음 세 계약을 하나의 상태 흐름으로 통합한다.

1. 기획 우선: L1 이상 작업은 PLAN과 승인된 실행 계약 없이 BUILD로 진입하지 않는다.
2. 상세 데이터·초기 수치는 GPT `RECOMMENDED_DEFAULT`로 진행하되, 프로젝트 방향을 바꾸는 기획 충돌은 Grill Me로 사용자 승인 후 확정한다.
3. Grill Me 승인 Decision은 최대 10건 단위로 하나의 배치 PR에서 exact-head 검사와 적대적 검토를 통과한 뒤 병합한다.

## Existing conflict

현행 정책은 승인 Decision 한 건마다 정본과 `main`에 즉시 반영할 수 있다. 새 요구는 10건 단위 PR 검증·병합을 요구한다. 승인 기록을 10건 동안 메모리에만 누적하면 중단 복원과 즉시 동기화 계약을 깨고, 반대로 매 건 `main`에 직접 반영하면 배치 PR 검증을 우회한다.

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

다음은 `RECOMMENDED_DEFAULT`로 진행할 수 있다.

- 플레이테스트 전 밸런스 초깃값
- 쿨다운·입력 버퍼·전환 시간의 초기 시험값
- 내부 데이터 구조·로그·오류 처리·테스트 세부
- 기존 승인 기획을 구현하기 위한 가역적 기술값

각 값은 근거, 조정 조건, 검증, 정본 영향을 기록한다. 실제 테스트 결과가 없으면 확정 밸런스나 제품 검증으로 보고하지 않는다.

### Grill Me required conflicts

수치라도 난이도 곡선, 경제, 성장 속도, 세션 길이, 빌드 우열, 보상 의미, 핵심 플레이 경험을 실질적으로 바꾸면 `USER_DECISION_REQUIRED`다. 분야 정본 간 충돌, 기존 승인 Decision의 폐기·대체, 주요 UX·범위·비용 충돌도 Grill Me에서 한 번에 하나씩 승인받는다.

## Authority and state

- 승인 직후 Branch 정본은 복원 가능한 작업 권위 surface지만 `main` 통합 상태가 아니다.
- Sheet의 `APPROVED_PENDING_MERGE`는 승인 사실을 보존하지만 GitHub main 동기화 완료를 주장하지 않는다.
- `SYNCED_TO_MAIN`은 배치 PR 병합 SHA와 Sheet 재조회가 일치할 때만 사용한다.
- 동일 Goal에는 하나의 활성 Grill Me 배치 PR만 둔다.

## Verification

- 문서·Skill·Template가 동일 용어와 상태를 사용한다.
- focused contract test가 기획 우선, 분류, 10건 상한, 조기 체크포인트, exact-head, 적대적 검토, merged-main Sheet 승격을 검사한다.
- 기존 중립적 적대 검토와 deep-interview 회귀를 함께 실행한다.
- Skill 본문 변경은 Learning Log와 reference-freshness 결합 규칙을 충족한다.

## Benchmark interpretation

- 작은 자기완결 변경은 검토·롤백·병합에 유리하므로 10건 고정 최소 배치는 거부한다.
- required checks는 최신 PR HEAD에서 실행된 결과만 사용한다.
- 작성과 검토 책임은 분리하고, 적대적 검토는 반대를 위한 반대가 아니라 설계·기능·복잡도·테스트·문서 영향을 확인한다.

## Non-goals

- 새 광역 Skill 추가
- Registry 또는 v9.4.1 release lock 변경
- 모든 수치를 사용자에게 질문
- 승인 Decision을 10건 동안 메모리에만 보류
- 실제 외부 모델·사람·기기 검증을 자동 완료로 승격
