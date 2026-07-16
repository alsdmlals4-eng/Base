---
name: orchestrating-deepseek-worktrees
description: Use when a large drafting, classification, comparison, or repetitive transformation task can be delegated to DeepSeek or another external model while Codex retains review and repository integration responsibility.
---

# Orchestrating DeepSeek Worktrees

## Core principle

대용량 초안 작업은 별도 worktree와 브랜치에 격리하고, 외부 AI의 결과를 신뢰된 기준 문서가 아니라 **검수 대기 입력**으로 취급한다. Codex 또는 저장소 책임자가 실제 diff, 근거, 테스트를 확인한 뒤 필요한 변경만 기준 브랜치에 반영한다.

## Use when

- 긴 문서의 초안·요약·분류·표 변환이 필요하다.
- 후보안, 문구, 데이터 카드처럼 반복적인 산출물이 많다.
- 같은 기준 문맥을 유지한 채 여러 하위 작업을 처리한다.
- Codex의 컨텍스트와 토큰을 실제 파일 조사·검수·반영에 집중시키려 한다.

## Do not use when

- 보안·결제·저장 이관처럼 오판 비용이 큰 변경의 최종 판단.
- 실제 파일과 테스트를 읽어야만 가능한 버그 수정.
- 사용자 승인 없이 제품 방향이나 기준 문서를 확정하는 작업.
- 비밀값, 비공개 자료, 권한 없는 외부 원문을 모델에 전달해야 하는 작업.

## Required inputs

- 승인된 목표와 사용자 가치.
- 읽을 기준 문서 allowlist.
- 수정 가능 경로와 보호 경로.
- 산출물 형식과 검수 기준.
- 기준 브랜치와 시작 커밋.
- 외부 전송이 허용된 자료 범위.

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

## Process

1. 현재 기준 브랜치, dirty 상태, 시작 커밋을 기록한다.
2. 작업을 한 문장 목표와 독립 검수 가능한 단위로 자른다.
3. 별도 브랜치와 worktree를 만든다.
4. `templates/ai/DEEPSEEK_WORK_PACKAGE.md`로 작업 계약을 작성한다.
5. 공통 규칙과 반복 입력은 프롬프트 앞부분에 고정하고, 매 작업의 가변 요청은 뒤에 둔다.
6. 긴 저장소 전체를 전달하지 않고 Documentation Map과 allowlist로 필요한 파일만 제공한다.
7. 결과는 고정 Markdown 또는 JSON 스키마로 회수한다.
8. 외부 AI는 근거, 가정, 미확인, 변경 후보를 분리하고 자체 완료를 주장하지 않는다.
9. Codex가 `skills/reviewing-external-ai-drafts/SKILL.md`로 결과를 검수한다.
10. 승인된 최소 diff만 실제 작업 브랜치에 재작성하거나 선택적으로 가져온다.
11. 기준 테스트와 문서 동기화를 확인한 뒤 worktree를 정리한다.

## Token and context efficiency

- 공통 규칙·문서·출력 스키마를 안정적인 접두부로 유지한다.
- 원문 전체 반복 대신 Active Context와 정확한 파일 경로를 전달한다.
- 파일별 요약이 아니라 결정에 필요한 차이와 근거를 회수한다.
- 서로 독립적인 대량 작업만 병렬화한다.
- 같은 파일을 여러 모델이 동시에 수정하지 않는다.
- API 사용 시 cache hit·miss 사용량을 기록할 수 있으면 비용 검토에 활용한다.
- 구조화된 후속 처리가 필요하면 JSON 스키마와 예시를 함께 제공한다.

## Output contract

- 작업 패키지.
- worktree 경로, 브랜치, 시작 커밋.
- 생성·수정 후보 파일 목록.
- 초안 산출물.
- 근거·가정·미확인 목록.
- Codex 검수에 필요한 변경 요약.
- 정리 또는 보존해야 할 worktree 상태.

## Failure conditions

- 외부 AI가 main 또는 사용자의 활성 worktree를 직접 수정한다.
- 저장소 전체를 무조건 전달한다.
- 초안과 승인된 기준 문서를 같은 경로에서 혼합한다.
- 모델 보고만 믿고 실제 diff·참조·테스트를 확인하지 않는다.
- 충돌을 자동 해결하거나 미검증 변경을 자동 push한다.
- 토큰 절약을 이유로 보안·저장·호환성 검증을 생략한다.

## Validation scenarios

1. 긴 기획서 통합은 DeepSeek가 중복 후보와 통합안을 만들고, Codex가 현행 책임 원본과 참조를 확인해 반영한다.
2. 데이터 카드 100개 생성은 고정 스키마로 분할하고, Codex가 표본·예외·스키마 검사를 수행한다.
3. 실제 코드 수정이 필요한 버그는 DeepSeek에 최종 수정을 맡기지 않고, 조사 메모만 입력으로 사용한다.

Templates:

- `templates/ai/DEEPSEEK_WORK_PACKAGE.md`
- `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
