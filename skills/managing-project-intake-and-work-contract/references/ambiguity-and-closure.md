# 모호성 장부와 종료 판정

## 장부 필드

각 항목은 `ledger_id`, `area`, `statement`, `source_type`, `status`, `evidence`, `decision_owner`, `resolution_or_next_question`을 가진다.

상태:

- `CONFIRMED`: 사용자가 원하는 미래로 확인함
- `OBSERVED`: 저장소의 현재 사실을 증거로 확인함
- `NEEDS_CONFIRMATION`: 참고·추론 후보라 사용자 판단이 필요함
- `UNVERIFIED`: 증거가 없거나 접근할 수 없음
- `DEFERRED`: 선행 조건과 재개 시점을 기록함
- `REJECTED`: 요구에서 명시적으로 제외함

## 종료 점검

다음 질문에 모두 답할 수 있어야 한다.

1. 왜 이 작업을 하며 누구의 어떤 경험을 바꾸는가?
2. 무엇을 만들고 무엇을 만들지 않는가?
3. 어떤 결정·파일·데이터·자산을 보호하는가?
4. 산출물은 정확히 어떤 종류인가?
5. 성공·실패를 어떤 증거로 판정하는가?
6. 남은 미검증·보류가 실행을 막는가?

중대한 `NEEDS_CONFIRMATION`이 남으면 `AWAITING_USER_CONFIRMATION`을 유지한다. `UNVERIFIED`가 남더라도 실패 시 안전하게 멈출 수 있고 완료 판정에서 제외되지 않는 경우에만 명시적으로 진행할 수 있다.

## 상세 요청의 역인터뷰

1. 명시 요구를 구조화한다.
2. 저장소 사실과 충돌 여부를 조사한다.
3. 누락이 결과를 바꾸는 항목만 목록화한다.
4. 현재 이해를 짧게 재진술하고 틀리거나 빠진 부분을 묻는다.
5. 마지막 한 문장 확인을 받는다.

## Grill Me 의사결정 인터뷰

프로젝트 코어, 플레이어 경험, MVP, PoC, Vertical Slice, 역할·승인 경계처럼 사용자가 결정해야 하는 중요한 분기가 남으면 `clarify` Skill Mode에서 `grill-me-protocol.md`를 사용한다.

```text
저장소·대화에서 답 확인
→ 이미 답한 질문 제거
→ 결과를 바꾸는 결정 하나 선택
→ 선택지·장단점·GPT 권장안 제시
→ 사용자 답변
→ 결정 원장·책임 원본 즉시 반영
→ 다음 차단 질문 재평가
```

사용자가 `모두 권장안대로`라고 승인하면 남은 동등 유형 결정을 권장안으로 확정하고 불필요한 질문을 계속하지 않는다.

Reference: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
Template: `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
