# Changelog

## v1.0.0 - initial shared rules

초기 공용 규칙 저장소 구조를 추가했다.

추가 문서:

- `README.md`
- `AGENTS.md`
- `docs/AI_SHARED_WORK_RULES.md`
- `docs/AI_WORKFLOW_CHECKLIST.md`
- `templates/`

핵심 원칙:

- Base는 공용 규칙의 원본 저장소다.
- 각 프로젝트는 Base 문서를 로컬 사본으로 동기화한다.
- 각 프로젝트는 `docs/BASE_RULES_VERSION.md`에 Base 기준 커밋 SHA와 동기화 날짜를 기록한다.
- 프로젝트 전용 규칙은 프로젝트 저장소에 둔다.
