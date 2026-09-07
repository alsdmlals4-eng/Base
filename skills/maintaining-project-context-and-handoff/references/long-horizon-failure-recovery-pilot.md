# Long-Horizon Failure/Recovery Pilot

## Purpose and owner

기존 [fresh-read-project-bootstrap.md](fresh-read-project-bootstrap.md)의 복원 품질을 시험하는 작은 평가 묶음이다. 새 Skill, agent executor, memory store, 전역 필수 Gate 또는 두 번째 프로젝트 정본을 만들지 않는다. 시험 정의의 단일 원본은 [long-horizon-failure-recovery-pilot.json](long-horizon-failure-recovery-pilot.json)이며, 이 문서는 실행 방법과 증거 경계만 책임진다.

`MODEL_RUN_STATUS: NOT_RUN` / `TRANSFER_ACCEPTED_NOT_CLAIMED`

JSON의 `live_status: NOT_RUN`과 빈 `observed_evidence`는 명세가 실행 결과로 오인되는 것을 막는다. 실제 실행 결과는 기존 작업의 PR/evidence owner에 별도로 기록하고, 명세 파일을 결과 장부로 바꾸지 않는다. 이 묶음을 프로젝트에 자동 설치하거나 새 비용·권한을 활성화하지 않는다.

## Reuse and alternatives

| 선택지 | 판정 | 이유 |
|---|---|---|
| 새 범용 하네스·기억 DB·scheduler | REJECT | 현재 문제에 비해 책임 중복과 운영 비용이 크다. |
| 기존 문서의 토큰 존재 검사만 추가 | REJECT | 실제 오류 뒤 후속 명령이 중단되는지는 증명하지 못한다. |
| 기존 검사기의 로컬 연결 시험 + 별도 live pilot | ADAPT | 실제 consumer를 재사용하고, 아직 증명하지 못하는 행동을 명시한다. |

기존 `tools/check_skill_behavior_evals.py::validate_result_identity`와 `tools/run_local_validation.py::run_validation`을 수정 없이 시험에서 연결한다. 기존 개별 검사와 겹치는 일반 규칙은 재작성하지 않는다. `tests/test_long_horizon_failure_recovery.py`는 실제 임시 Git 저장소·원본 해시·자식 프로세스로 **검사 실패가 후속 임시 쓰기를 차단하는지** 확인한다. 생산 코드의 새 승인 Gate가 아니다: `NO_PRODUCTION_AUTHORIZATION_GATE`.

## Local execution and evidence boundary

저장소 root에서 실행한다. `git`, Python과 Base의 기존 `jsonschema` 의존성이 필요하다.

```sh
python -m unittest discover -s tests -p test_long_horizon_failure_recovery.py -v
```

이 테스트는 기존 전체 `unittest discover` 경로에도 포함된다. 별도 CI workflow나 유료 API 호출은 추가하지 않는다. 기존 전체 검증은 `AGENTS.md`의 `tools/run_local_validation.py --trusted-history-commit <fresh-main-sha>`를 따른다.

| 결과 | 증명하는 것 | 증명하지 못하는 것 |
|---|---|---|
| 명세 검사 PASS | 6개 시험, negative control, 원본 연결, NOT_RUN 경계가 보존됨 | 실제 agent가 요약 누락을 복구함 |
| `UNIT_GUARD_ONLY` | 변경된 HEAD/원본/평가 파일 집합, NOT_RUN, 비독립 문맥, 누락 schema/도구, 비정상 종료가 후속 임시 쓰기를 차단함 | 원격 side effect 멱등성, task_id/call_id routing, 동시 쓰기 격리, 지시 취소·승인 강제 |
| 독립 live pilot 결과 | 기록한 provider·버전·설정·revision·작업에서 관측한 행동 | 모든 프로젝트·모델·향후 버전의 일반 신뢰성 |

테스트의 `COMPLETED`, model/review 필드는 schema를 통과시키기 위한 **synthetic fixture**다. 모델 실행·독립 검토·routing 점수 결과로 내보내지 않는다. identity 검사 성공은 실제 검증 내용의 정당성이나 쓰기 권한을 승인하지 않는다. 같은 유효 입력을 다시 실행하면 효과가 반복될 수 있으며, 검사 뒤 쓰기 전의 경쟁 조건도 이 시험이 해결하지 않는다.

## Live pilot protocol

1. 대상 프로젝트의 최신 AGENTS, 채택한 Base, owner, 코드·테스트와 보호 범위를 읽는다. 승인된 작업의 격리 복사본만 사용하고 실제 main/PR merge/upload/계정/자산 승인 상태를 변경하지 않는다. negative control도 임시 목적지에서만 실행한다.
2. 시험 시작 전에 project/task/case ID, exact source SHA, 관찰할 원본 파일 SHA-256, model/provider/version, 실제 tool·client 버전, 설정, 승인 범위, 동일 작업의 수용 기준과 허용 자원을 기존 evidence owner에 기록한다. 지원이 확인되지 않은 기능은 `NOT_RUN`으로 남기고 이유를 기록한다.
3. 동일 revision·작업·모델·수용 기준·안전 경계를 고정한다. 먼저 현행 A를 측정하고, 지원되는 기능 하나만 바꾼 B를 새 격리 복사본에서 측정한다. 메모리·로그·결과를 다음 arm으로 흘리지 않는다. 둘 다 동일한 실패 주입을 사용하며 negative control은 결과를 판별할 수 있는지 확인하는 별도 시험이지 안전장치 해제용 비교 arm이 아니다.
4. JSON의 setup → injection → pass_observation을 실행하고 negative_control과 대조한다. 요약을 숨긴 새 세션은 `COLD_START_SIMULATION`이다. 실제 provider compaction 이벤트 증거 없이 native compaction 시험으로 부르지 않는다. steering의 접수, 실제 반영, 진행 중 도구 종료는 각각 다른 사건이다.
5. 이벤트에는 task_id/call_id/revision, 요청·접수·실행·완료·readback 순서와 확인 가능한 시간을 연결한다. 필요 원본 locator와 결과 해시를 남기되 비밀·자격증명·전체 raw transcript를 기본 산출물로 복제하지 않는다. 독립 검수자가 같은 증거에서 효과 횟수·누락·위반·복구를 판정한다.
6. 아래 지표와 실패 원인·교정·재검증을 기존 PR/evidence에 기록한다. 미실행/미지원/blocked 사례를 성공률 분모에서 조용히 빼지 말고 전체 예정 수, 실행 수, blocked 수를 따로 표시한다. 6개는 진단용 파일럿이지 통계적 우위나 생산성 상승의 증명이 아니다. 개선이 필요할 때만 실제 업무 사례를 확대한다.

| 지표 | 기록 기준 |
|---|---|
| 결과 품질 | 사전에 고정한 수용 기준 충족 여부와 누락·퇴행 |
| 복구 | 실패 주입을 식별했는지, 안전한 완료 또는 정당한 차단인지 |
| 중복·권한 위반 | 실제 목적지 readback에서 확인한 효과 횟수와 최신 승인 범위 |
| 사용자 개입 | 명세된 시험용 지시 변경과 추가 구조 요청을 구분한 횟수 |
| 시간·사용량·비용 | 확인 가능한 계측값만 기록; 알 수 없으면 null/UNKNOWN, 0이나 절감률로 대체하지 않음 |

## Research and compatibility

2026-09-07 공식 자료에서 일반화 가능한 경계만 ADAPT했다. 특정 모델 점수나 미래 기능 활성화를 전제로 삼지 않는다.

- OpenAI Compaction: https://developers.openai.com/api/docs/guides/compaction — 불투명한 상태 전달과 사람이 만든 요약을 구분한다.
- OpenAI Mid-turn steering: https://developers.openai.com/api/docs/guides/steering — 접수는 적용 완료가 아니며 이미 시작한 도구나 완료 효과를 되돌리지 않는다.
- OpenAI Async tool calling: https://developers.openai.com/api/docs/guides/async-tool-calling — 실제 실행과 호출 결과 연결은 실행 환경이 책임진다.

구형 `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`의 무조건적인 GitHub+Notion 절차를 이 시험으로 부활시키지 않는다. 현재 bootstrap과 프로젝트 AGENTS가 우선하며 Notion은 명시된 예외 또는 실제 legacy migration 필요가 있을 때만 읽는다. 관련 미병합 PR은 current canon도 이번 작업의 승인 범위도 아니다.

## Reusable lesson and rollback

기억 문서의 존재, guard 함수의 존재, guard가 다음 실행을 막는 것, 실제 agent가 재개한 것을 별도 층으로 검증한다. 실패를 재현하는 가장 낮은 층부터 검사하고, 높은 층의 성공을 낮은 층의 PASS로 추정하지 않는다.

Rollback은 이 pilot 명세·설명·테스트와 bootstrap의 추가 링크만 함께 되돌린다. 기존 checker, runner, 스키마, Registry, 기존 프로젝트 결정과 다른 작업의 PR은 그대로 둔다.
