# Completion and Destination Freshness Gate

이 문서는 Base Loop 계약의 **시작 준비(readiness)**와 **완료 증명(completion)**을 분리하고, GitHub·Notion 같은 목적지가 실제 readback 없이 `SYNCED`로 간주되는 것을 막는 좁은 공용 계약이다.

새 Skill이나 Work Mode가 아니다. 기존 `LOOP_ENGINEERING_CONTROL_PLANE`, Requirement Coverage, Evidence, post-merge readback을 연결하는 machine-checkable completion layer다.

## 1. Readiness와 Completion은 다른 질문이다

```text
readiness
= 승인된 요구가 작업·산출물·테스트·증거에 안전하게 연결되어 작업을 시작할 수 있는가?

completion
= 승인된 요구가 실제로 닫혔고, 필수 검사가 실행됐으며, 목적지 상태까지 다시 읽어 완료를 증명할 수 있는가?
```

`tools/check_loop_execution_capsule.py`의 기본 phase는 기존과 동일한 `readiness`다.

```bash
python tools/check_loop_execution_capsule.py <capsule>
python tools/check_loop_execution_capsule.py <capsule> --phase readiness
```

완료 판정은 명시적으로 실행한다.

```bash
python tools/check_loop_execution_capsule.py <capsule> --phase completion
```

## 2. Requirement closure

Readiness에서는 Requirement Coverage item이 `MAPPED` 또는 `IMPLEMENTED`일 수 있다. 이 상태를 막으면 아직 시작하지 않은 정상 작업도 실패하므로 기존 validator는 유지한다.

Completion에서는 다음만 닫힌 상태다.

```text
VERIFIED
DEFERRED_APPROVED
```

- `VERIFIED`: 요구사항이 승인된 acceptance/evidence 경로로 실제 검증됨.
- `DEFERRED_APPROVED`: 완료 범위 밖으로 미룬 것이 사용자/승인 계약에 명시되어 있음.
- `MAPPED` / `IMPLEMENTED`: 작업 진행 상태이며 완료 증거가 아니다.

Coverage ledger 전체 status도 `VERIFIED`여야 한다.

## 3. Verification Receipt

`LOOP_VERIFICATION_RECEIPT`는 완료 시점의 실행·생략·목적지 readback을 구조화한다.

빈 receipt로 완료 Gate를 우회할 수 없도록 **최소 1개의 check와 최소 1개의 destination readback**을 반드시 포함한다. 현재 작업에 적용 가능한 검증이나 목적지가 정말 없다면 completion contract 자체가 필요 없는 작업인지 먼저 재라우팅하며, `checks=[]` 또는 `destinations=[]`를 `VERIFIED`의 근거로 사용하지 않는다.

### Required check

각 check는 최소 다음을 가진다.

```yaml
check_id:
required: true | false
status: PASS | FAIL | NOT_RUN | SKIPPED
evidence_ref:
reason:
```

규칙:

- `required=true`이면 `PASS`만 completion을 허용한다.
- `FAIL`, `NOT_RUN`, `SKIPPED`는 이유를 남겨야 한다.
- required `PASS`는 `evidence_ref`가 있어야 한다.
- 필수 검사를 실행하지 못한 것은 보고서에 적었다는 이유만으로 완료로 승격하지 않는다.

## 4. Destination freshness

`SYNCED`는 입력 라벨이 아니라 **readback 비교의 결론**이다.

```text
expected_ref
→ 실제 목적지 재조회
→ observed_ref
→ expected_ref == observed_ref
→ SYNCED
```

목적지는 최소 다음을 가진다.

```yaml
destination_id:
kind: GITHUB | NOTION | OTHER
required: true | false
expected_ref:
observed_ref:
sync_state: SYNCED | STALE | UNVERIFIED | NOT_APPLICABLE
evidence_ref:
```

필수 목적지는 다음을 모두 만족해야 한다.

1. expected/observed ref가 존재한다.
2. 둘이 일치한다.
3. `sync_state == SYNCED`다.
4. readback `evidence_ref`가 존재한다.

`SYNCED`인데 ref가 다르면 completion은 실패한다.

## 5. Notion 경계

Base CI가 Notion API를 직접 호출하도록 강제하지 않는다. 이는 credentials, API availability, CI coupling을 불필요하게 늘린다.

대신 현재 승인된 executor/connector가 다음을 수행한다.

```text
fresh GitHub main readback
→ applicable Notion current-state update
→ Notion destination readback
→ expected/observed ref 기록
→ Verification Receipt
→ completion validation
```

따라서 인터페이스는 달라도 completion 기준은 같다.

## 6. Backward compatibility

`verification_receipt_path`는 Capsule schema의 optional field다.

- 기존 downstream Capsule은 계속 readiness-valid다.
- 기존 작업을 강제로 마이그레이션하지 않는다.
- completion phase를 사용하는 새/갱신 workflow만 receipt를 채택한다.
- Base template은 새 작업이 이 경로를 자연스럽게 사용하도록 receipt를 포함한다.

기존 프로젝트를 일괄 수정하지 않는다. 실제 completion workflow 또는 stale destination 문제가 있는 프로젝트만 bounded adoption 대상으로 삼는다.

## 7. Failure and rollback

Completion failure는 readiness나 이미 생성된 결과물을 자동 삭제하지 않는다.

```text
completion finding
→ 원인 분류
→ missing verification / stale destination / requirement gap 교정
→ 해당 검사/readback 재실행
→ completion 재판정
```

이 Gate 자체를 되돌릴 때는 Base PR을 revert하면 된다. 기존 `validate_bundle()` readiness contract는 별도 경로로 유지된다.
