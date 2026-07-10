# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다.

Base 공용 규칙을 먼저 복사한 뒤, 이 프로젝트의 엔진, 폴더 구조, 금지 범위, 검증 방법을 여기에 적는다.

## Project

- Project name:
- Engine:
- Language:
- Genre:

## Base Rules

- Base repository: `alsdmlals4-eng/Base`
- Local copy version file: `docs/BASE_RULES_VERSION.md`
- Local shared rules:
  - `docs/AI_SHARED_WORK_RULES.md`
  - `docs/AI_WORKFLOW_RULES.md`
  - `docs/MVP_WORKFLOW_CHECKLIST.md`
  - `docs/BENCHMARKING_REFERENCE_GUIDE.md`
  - `docs/DOCUMENTATION_MAP.md`

작업자는 Base 링크만 믿지 말고, 현재 프로젝트 저장소에 동기화된 로컬 사본과 이 파일을 먼저 읽는다.

## Project-Specific Rules

- 이 프로젝트에서 반드시 지킬 규칙을 적는다.
- 금지할 엔진/언어/구조를 적는다.
- 기존 사용자 변경사항을 되돌리거나 덮어쓰지 않는다.
- 요청 범위 밖 리팩터링을 하지 않는다.
- 정상 작동하는 구조를 임의로 바꾸지 않는다.

## Work Preparation

1. `AGENTS.md`
2. `docs/BASE_RULES_VERSION.md`
3. `docs/DOCUMENTATION_MAP.md`
4. `docs/AI_SHARED_WORK_RULES.md`
5. `docs/AI_WORKFLOW_RULES.md`
6. `docs/MVP_WORKFLOW_CHECKLIST.md`
7. `docs/BENCHMARKING_REFERENCE_GUIDE.md`
8. 프로젝트 전용 Codex / 구현 규칙
9. `README.md`
10. `PROJECT_BRIEF.md`
11. `DESIGN_INTENT.md`
12. `MVP_ROADMAP.md`
13. `TEST_CHECKLIST.md`
14. 현재 Issue / Goal
15. 실제 수정 대상 파일

## Validation

- 실행 명령:
- 테스트 명령:
- 수동 확인 순서:

## Report Format

```md
## 변경 파일

-

## 변경 이유

-

## 구현 내용

-

## 검증 내용

-

## 확인할 항목

1.
2.
3.

## 남은 위험

-

## Base 승격 후보

- 대상:
- 현재 프로젝트에서 확인된 반복 사용 근거:
- 공용 규칙으로 일반화할 내용:
- 프로젝트 전용으로 남겨야 할 내용:
- Base 반영 필요성: 필요 / 불필요 / 추가 검증 필요
- 권장 Base 커밋명:
- Base 반영 후 프로젝트 동기화 필요 여부:
```
