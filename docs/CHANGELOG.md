# Changelog

## v1.2.0 - diegetic tutorial guide principles

서사형 안내 캐릭터가 시스템 정보와 튜토리얼을 안전하고 반복 피로 없이 전달하는 공용 기준을 추가했다.

변경:

- 안내자의 세계관 내 역할을 담당 시스템과 일치시키도록 했다.
- 최초 상세 안내와 재방문용 짧은 안내를 분리하고 확인 상태를 저장하도록 했다.
- 음향 신호에 동등한 시각 또는 문구 신호를 함께 제공하도록 했다.
- 미획득 단서·정답·숨은 수치를 안내자가 누설하지 않도록 했다.

## v1.1.0 - skill adoption and context compaction

외부 AI 스킬을 공용 규칙에 안전하게 채택하고 긴 작업 context를 줄이는 기준을 추가했다.

변경:

- `docs/AI_SKILL_ADOPTION_GUIDE.md`를 추가했다.
- 7개 공개 스킬 저장소에서 최소 구현, 간결한 보고, UI brief, feedback loop, 보안 preflight, 최신성 조사, verification 원칙을 추출했다.
- 외부 스킬은 프로젝트 규칙보다 낮은 선택형 보조 수단으로 정의했다.
- 플러그인 설치 전 스크립트·hook·MCP·외부 API·쿠키·비밀값·쓰기 권한을 확인하도록 했다.
- active context capsule과 phase-boundary compact 기준을 추가했다.
- README, 공용 문서 목록, workflow 문서를 새 가이드에 연결했다.

## v1.0.2 - custom instructions and file lifecycle notes

맞춤형 지침과 파일 변경 의도 기록 규칙을 추가했다.

변경:

- `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`를 추가했다.
- `templates/custom-instructions.gpt.md`를 추가했다.
- `templates/custom-instructions.codex.md`를 추가했다.
- `README.md`와 `docs/DOCUMENTATION_MAP.md`에 맞춤형 지침 문서를 추가했다.
- `docs/AI_SHARED_WORK_RULES.md`에 파일 생성/수정/삭제/이동/이름 변경 시 의도와 영향 기록 규칙을 추가했다.
- `docs/MVP_WORKFLOW_CHECKLIST.md`에 파일 변경 의도 체크리스트를 추가했다.

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
