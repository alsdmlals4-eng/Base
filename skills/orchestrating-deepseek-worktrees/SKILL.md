---
name: orchestrating-deepseek-worktrees
description: Use when a large drafting, classification, comparison, or repetitive transformation can be isolated for an external model.
---

# Orchestrating DeepSeek Worktrees

## Core principle

대용량 초안 작업은 별도 worktree와 브랜치에 격리하고, 외부 AI의 결과를 신뢰된 기준 문서가 아니라 **검수 대기 입력**으로 취급한다. GPT 또는 현재 작업의 책임 검수자가 실제 diff, 근거, 테스트를 확인한 뒤 필요한 변경만 기준 브랜치에 반영한다.

이 Skill의 이름과 기존 `ai/deepseek-*` 경로는 현재 호환성을 위한 식별자다. 다른 외부 모델을 쓰더라도 같은 격리·권한·검수 계약을 충족해야 하며, provider 이름 때문에 별도 Skill을 자동 생성하지 않는다.

## Review authority contract

```text
GPT_PRIMARY_REVIEWER
OPTIONAL_CODEX_EXECUTOR
EXTERNAL_AI_RESULT: REVIEW_PENDING
```

- 기본 계획·검수 책임자는 GPT다.
- Codex는 외부 AI 결과가 실제 코드·Scene·Resource·data 변경, 대규모 기계 변경, 로컬 runtime/build/performance 검증처럼 별도 실행 권위를 요구할 때만 `OPTIONAL_CODEX_EXECUTOR`로 사용한다.
- 문서·분류·비교 결과를 현재 GPT가 직접 검수할 수 있으면 Codex를 의무 단계로 추가하지 않는다.
- 결과 검증 의미는 `reviewing-and-validating-project-changes`의 관련 계약을 따른다. 해당 Skill/Part의 소유권을 P08이 가져오지 않는다.

## Use when

- 긴 문서의 초안·요약·분류·표 변환이 필요하다.
- 후보안, 문구, 데이터 카드처럼 반복적인 산출물이 많다.
- 같은 기준 문맥을 유지한 채 여러 하위 작업을 처리한다.
- GPT/Codex의 컨텍스트를 실제 정본 조사·검수·반영에 집중시키려 한다.

## Do not use when

- 보안·결제·저장 이관처럼 오판 비용이 큰 변경의 최종 판단.
- 실제 파일과 테스트를 읽어야만 가능한 버그 수정의 최종 구현.
- 사용자 승인 없이 제품 방향이나 기준 문서를 확정하는 작업.
- 비밀값, 비공개 자료, 권한 없는 외부 원문을 모델에 전달해야 하는 작업.
- 현재 GPT가 같은 품질로 직접 처리할 수 있는 작은 작업인데 단순히 외부 모델을 사용할 수 있다는 이유만으로 우회하는 경우.

## Required inputs

- 승인된 목표와 사용자 가치.
- 읽을 기준 문서 allowlist.
- 수정 가능 경로와 보호 경로.
- 산출물 형식과 검수 기준.
- 기준 브랜치와 시작 커밋.
- 외부 전송이 허용된 자료 범위.
- 실제 검수 책임자와 optional executor 필요 조건.

## EXECUTOR_REHYDRATION_GATE

외부 AI나 후속 executor는 handoff 요약만 믿고 시작하지 않는다. **실행 직전** 최소한 다음을 다시 읽어 현재 상태를 복원한다.

```text
latest applicable user instruction
→ project AGENTS.md / repository authority
→ current Active Context / confirmed decisions when present
→ exact branch/commit
→ current allowlist / protected paths
→ relevant canonical files and tests
→ current worktree dirty/integration state
```

- handoff의 SHA·경로·요약과 실제 GitHub/프로젝트 상태가 다르면 실제 상태를 우선하고 차이를 보고한다.
- 다른 프로젝트, 다른 worktree, 다른 branch의 상태를 편의상 재사용하지 않는다.
- 외부 AI 결과가 오래된 canon을 전제로 했다면 결과를 그대로 승격하지 않고 필요한 부분만 재검수한다.
- 실행 권위가 없는 surface에서 실행했다고 주장하지 않는다.

## Workspace contract

권장 구조:

```text
main worktree                 실제 기준선·최종 반영
.worktrees/deepseek-<topic>/  대용량 초안·후보안
branch: ai/deepseek-<topic>   외부 AI 작업 브랜치
```

- `.worktrees/`는 저장소에서 무시되는 경로인지 먼저 확인한다.
- 한 브랜치는 한 작업 목적만 가진다.
- 기존 작업 중인 브랜치를 외부 AI가 재사용하지 않는다.
- 초안은 프로젝트가 정한 `drafts/external-ai/<topic>/` 또는 명시된 대상 파일에만 작성한다.
- dirty 상태와 미통합 결과가 있으면 worktree를 자동 삭제하지 않는다.
- Git worktree가 한 저장소에서 여러 linked worktree를 지원한다는 사실은 격리 수단의 근거일 뿐, 서로 다른 작업의 권한이나 canon을 공유한다는 뜻이 아니다.

## Process

1. 현재 기준 브랜치, dirty 상태, 시작 커밋을 기록한다.
2. 작업을 한 문장 목표와 독립 검수 가능한 단위로 자른다.
3. 별도 브랜치와 worktree를 만든다.
4. `templates/ai/DEEPSEEK_WORK_PACKAGE.md`로 작업 계약을 작성한다.
5. 공통 규칙과 반복 입력은 프롬프트 앞부분에 고정하고, 매 작업의 가변 요청은 뒤에 둔다.
6. 긴 저장소 전체를 전달하지 않고 Documentation Map과 allowlist로 필요한 파일만 제공한다.
7. 외부 AI 실행 직전에 `EXECUTOR_REHYDRATION_GATE`를 수행한다.
8. 결과는 고정 Markdown 또는 JSON 스키마로 회수한다.
9. 외부 AI는 근거, 가정, 미확인, 변경 후보를 분리하고 자체 완료를 주장하지 않는다.
10. GPT가 기본 책임 검수자로 결과·현재 정본·실제 diff를 비교한다. 실행 권위가 추가로 필요한 경우에만 Codex를 `OPTIONAL_CODEX_EXECUTOR`로 호출해 필요한 파일/테스트/runtime 증거를 직접 재확인한다.
11. 승인된 최소 diff만 실제 작업 브랜치에 재작성하거나 선택적으로 가져온다.
12. 기준 테스트와 문서 동기화를 확인한 뒤 worktree를 정리한다.

`templates/ai/DEEPSEEK_WORK_PACKAGE.md`의 기존 `Codex 인계` 표기는 Codex가 실제 optional executor로 선택된 경우에만 그대로 해석한다. GPT가 직접 검수하는 경우 같은 필드를 **책임 검수자 인계 정보**로 사용한다. 템플릿 자체의 provider/reviewer-neutral 명칭 변경은 P08 소유 범위 밖이면 `CROSS_PART_CHANGE_REQUEST`로 넘긴다.

## Token and context efficiency

- 공통 규칙·문서·출력 스키마를 안정적인 접두부로 유지한다.
- 원문 전체 반복 대신 현재 결정에 필요한 정본과 정확한 파일 경로를 전달한다.
- 파일별 요약이 아니라 결정에 필요한 차이와 근거를 회수한다.
- 서로 독립적인 대량 작업만 병렬화한다.
- 같은 파일을 여러 모델이 동시에 수정하지 않는다.
- API 사용이 사용자 승인된 별도 비용 경로일 때만 cache hit·miss 사용량을 비용 검토에 활용한다.
- 구조화된 후속 처리가 필요하면 JSON 스키마와 예시를 함께 제공한다.
- 컨텍스트가 커졌다는 이유만으로 관련 없는 Skill/Tool을 미리 로드하지 않는다.

## Output contract

- 작업 패키지.
- worktree 경로, 브랜치, 시작 커밋.
- 실행 직전 rehydration에서 확인한 exact branch/commit과 canon.
- 생성·수정 후보 파일 목록.
- 초안 산출물.
- 근거·가정·미확인 목록.
- 책임 검수자 검수 포인트와 optional executor 필요 여부.
- 정리 또는 보존해야 할 worktree 상태.

## Failure conditions

- 외부 AI가 main 또는 사용자의 활성 worktree를 직접 수정한다.
- 저장소 전체를 무조건 전달한다.
- 초안과 승인된 기준 문서를 같은 경로에서 혼합한다.
- 모델 보고만 믿고 실제 diff·참조·테스트를 확인하지 않는다.
- handoff 요약을 최신 canon으로 간주하고 `EXECUTOR_REHYDRATION_GATE`를 생략한다.
- GPT가 검수 가능한 작업에도 Codex를 의무 단계로 호출한다.
- 충돌을 자동 해결하거나 미검증 변경을 자동 push한다.
- 토큰 절약을 이유로 보안·저장·호환성 검증을 생략한다.

## Validation scenarios

1. 긴 기획서 통합은 외부 AI가 중복 후보와 통합안을 만들고, GPT가 현행 책임 원본과 참조를 확인한다. 실제 저장소 변경 권위가 필요할 때만 Codex를 추가한다.
2. 데이터 카드 100개 생성은 고정 스키마로 분할하고, 책임 검수자가 표본·예외·스키마 검사를 수행한다. 실행 가능한 자동검사가 필요하면 optional executor를 사용한다.
3. 실제 코드 수정이 필요한 버그는 외부 AI에 최종 수정을 맡기지 않고 조사 메모만 입력으로 사용하며, 구현 executor는 실제 저장소와 테스트를 다시 읽는다.
4. handoff 후 main 또는 프로젝트 정본이 바뀐 경우 외부 AI 결과를 그대로 적용하지 않고 exact branch/commit과 현재 canon을 재수화한 뒤 차이를 먼저 검토한다.

Templates:

- `templates/ai/DEEPSEEK_WORK_PACKAGE.md`
- `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
