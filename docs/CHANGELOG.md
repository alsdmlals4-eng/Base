# Changelog

## v1.0.1 - workflow cleanup

공용 규칙 문서 구조를 정리했다.

변경:

- `docs/MVP_WORKFLOW_CHECKLIST.md`에 상세 작업 순서와 체크리스트를 통합했다.
- `docs/BENCHMARKING_REFERENCE_GUIDE.md`의 기본 표를 `게임/사례`, `관찰포인트`, `반응`, `프로젝트 적용(+사유)` 형식으로 통일했다.
- `docs/AI_SHARED_WORK_RULES.md`에 Base 승격 운영 방식과 `Base 승격 후보` 보고 형식을 추가했다.
- `docs/DOCUMENTATION_MAP.md`를 최종 Base 문서 구조에 맞게 정리했다.
- `templates/AGENTS.project.md`의 읽기 순서와 보고 형식을 최신화했다.
- 중복 체크리스트 문서인 `docs/AI_WORKFLOW_CHECKLIST.md`를 제거했다.

## v1.0.0 - initial shared rules

초기 공용 규칙 저장소 구조를 추가했다.

추가 문서:

- `README.md`
- `AGENTS.md`
- `docs/AI_SHARED_WORK_RULES.md`
- `docs/AI_WORKFLOW_RULES.md`
- `docs/MVP_WORKFLOW_CHECKLIST.md`
- `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- `docs/DOCUMENTATION_MAP.md`
- `templates/`

핵심 원칙:

- Base는 공용 규칙의 원본 저장소다.
- 각 프로젝트는 Base 문서를 로컬 사본으로 동기화한다.
- 각 프로젝트는 `docs/BASE_RULES_VERSION.md`에 Base 기준 커밋 SHA와 동기화 날짜를 기록한다.
- 프로젝트 전용 규칙은 프로젝트 저장소에 둔다.
