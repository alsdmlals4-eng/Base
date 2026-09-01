# 실행 순서·의존성 계획

## 목표와 완료

- 작업 계약:
- 사용자·플레이어 가치:
- 최종 완료 기준:
- 제외·보호 범위:
- 현재 게이트:

## 기능별 코드·계약 경계

새 기능 또는 기능 계약·공개 경계를 의미 있게 바꾸는 경우 아래 표를 기존 owner·경로와 연결해 작성한다. 별도 Registry·중복 정본은 만들지 않는다. 단일 단계·단일 파일의 작은 기능도 새 경계를 만들거나 바꾸면 한 행을 작성한다. 이미 승인된 기능 경계를 그대로 구현해 변경 사항이 없으면 `N/A`와 기존 계약 경로·사유를 기록한다.

| 기능·모듈 ID | 사용자 가치·책임·비목표 | 계약 정본 owner | 구현·데이터·테스트 위치 | 변동 값 owner·고정 경계 | 공개 출력·통합 경계 | 실제 consumer·의존 방향 | 검증·롤백 |
|---|---|---|---|---|---|---|---|
| F-01 |  |  |  |  |  |  |  |

## 작업 시작 고정 preflight

| 항목 | 현재 source·exact SHA | 관찰 사실·현재 consumer | 비교/역공학 결론 | 상태 |
|---|---|---|---|---|
| Benchmark / reverse engineering |  |  | `ADOPT / ADAPT / REJECT / NOT_APPLICABLE` | `PASS / REUSED_EVIDENCE / NOT_APPLICABLE / BLOCKED_UNVERIFIED` |
| Legacy context / configuration hygiene |  | `ACTIVE_OWNER / COMPATIBILITY / ARCHIVE / OBSOLETE_CANDIDATE / UNKNOWN_UNVERIFIED` | entrypoint 교정 또는 안전한 정리 계획 | `NO_CHANGE / CORRECTED / REMOVAL_VERIFIED / DEFERRED_UNKNOWN_UNVERIFIED` |

`BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED`: L1+ 작업은 이 표를 완료한 뒤에만 새 설계·제작·구현으로 진행한다. benchmark는 프로젝트에 맞는 flow·wireframe·기능·시각 방향을 찾는 비교이며, 고정된 메뉴·버튼·장르·구도를 주입하지 않는다. `NO_DELETION_BY_AGE_OR_NAME`: hygiene의 실제 제거는 references·consumer 0, Git recoverability, destination readback와 재검증을 확보한 경우에만 허용한다.

### 기계 검증 work-contract receipt (L1+ 필수)

`PROJECT_WORK_KANBAN_CHECKLIST`: 아래 repository-owned JSON receipt를 실제 값으로 작성하고, 새 설계·제작·구현 전에 `python <resolved-Base-root-at-current-Base-or-project-adapter-pin>/tools/validate_work_contract_receipt.py --receipt <receipt.json> --phase start --expected-source-sha <fresh-read-project-source-sha> --render-markdown`을 실행한다. `PASS`/`REUSED_EVIDENCE`는 비어 있는 표나 추측으로 통과할 수 없고, `NOT_APPLICABLE`은 L0의 순수 기계 수정만 허용한다. project receipt는 project repository에 두고, Base pin이나 tool root를 확인할 수 없으면 `BLOCKED_UNVERIFIED`로 둔다.

```json
{
  "work_level": "L1",
  "benchmark_preflight_receipt": {
    "state": "PASS",
    "entries": [
      {
        "source_and_evidence": "exact repository SHA, official source, or approved benchmark path",
        "observed_pattern": "directly observed reusable pattern",
        "project_fit_and_difference": "why the pattern fits here and what must not be copied",
        "disposition": "ADAPT"
      }
    ]
  },
  "context_configuration_hygiene": {
    "scope": "only files and consumers in this task",
    "inventory": [
      {
        "path": "repository-relative path",
        "classification": "ACTIVE_OWNER",
        "owner_or_provenance": "current owner or verified source",
        "references_and_consumers": "actual readback result",
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

작업 전환은 다음 승인 작업을 먼저 `IN_PROGRESS`와 `active_work_item_ref`로 기록한 뒤 `--phase resume --expected-source-sha <fresh-read-project-source-sha> --render-markdown`으로 다시 검사한다. 최종 마감은 모든 필수 작업의 evidence를 같은 최종 HEAD에서 재검증하고 `--phase closeout --expected-source-sha <fresh-read-project-source-sha> --expected-head-sha <fresh-read-final-head-sha> --render-markdown`을 사용한다. `TRUSTED_VERIFICATION_TARGET_HEAD`: receipt의 `verified_head_sha`를 기대값으로 다시 복사하지 않고 신뢰한 caller가 현재 최종 HEAD를 별도로 읽어 전달한다.

## 선행 조건

| ID | 환경·권한·결정·입력 | 상태 | 해결 방법 | 차단 작업 |
|---|---|---|---|---|
| PRE-01 |  | READY/BLOCKED/UNVERIFIED |  |  |

## 단계 목록

| Step | 결과 | 입력 | 대상 파일·시스템 | 선행 | 병렬 | 완료 기준 | 검증 | 롤백 |
|---|---|---|---|---|---|---|---|---|
| S1 |  |  |  |  |  |  |  |  |

## 의존성 지도

```text
S1 --BLOCKS--> S2
S1 --INFORMS--> S3
S2 --USES_OUTPUT--> S4
S3 --PARALLEL_WITH--> S4
S4 --VALIDATES--> S5
```

## 실행 묶음

### 묶음 A — 선행·불확실성 해소

- 단계:
- 진입 조건:
- 종료 증거:
- 실패 시 재계획:

### 묶음 B — 핵심 경로 구현

- 단계:
- 진입 조건:
- 종료 증거:
- 실패 시 재계획:

### 묶음 C — 통합·회귀·발행

- 단계:
- 진입 조건:
- 종료 증거:
- 실패 시 재계획:

## 우선순위 근거

| Step | 의존성 해소 | 위험 감소 | 사용자 가치 | 피드백 속도 | 되돌리기 난이도 | 순서 이유 |
|---|---|---|---|---|---|---|
|  | HIGH/MEDIUM/LOW |  |  |  |  |  |

## 병렬화 계약

| 병렬 묶음 | 출력 경계 | 공유 자원 | 충돌 방지 | 통합 지점 |
|---|---|---|---|---|
|  |  |  |  |  |

## 게이트

| Gate | 진입 조건 | 통과 증거 | 실패 시 | 미검증 시 |
|---|---|---|---|---|
| G1 |  |  |  |  |

## 위험·재계획

- 가장 위험한 가설:
- 외부 의존성:
- 같은 파일·Schema 충돌:
- 사용자 확인 재요청 조건:
- 범위 변경 시 폐기되는 단계:
- 안전한 중단점:

## GitHub 매핑

- Parent Issue:
- Sub-issues:
- Blocking dependencies:
- Milestone:
- PR 분리 기준:
