# Changelog

## v1.5.0 - shared planning knowledge library

공용 AI 협업 규칙 저장소를 기획·아트·연출·조사·인수인계 방법과 사례를 누적하는 지식 베이스로 확장했다.

변경:

- `docs/knowledge/README.md`와 methods·research·skills·cases 분류를 추가했다.
- 프로젝트 인수인계·컨텍스트 설계 방법을 추가했다.
- 아트 디렉션·제작 규격 방법과 실무 스킬 매트릭스를 추가했다.
- 애니메이션·전투 연출 방법과 실무 스킬 매트릭스를 추가했다.
- 조사 질문, 출처 우선순위, 근거·적용 결론을 다루는 공용 조사 방법을 추가했다.
- 기획 인수인계·검수 스킬 매트릭스를 추가했다.
- 프로젝트·벤치마킹 사례를 기록하는 `templates/KNOWLEDGE_CASE_STUDY.md`를 추가했다.
- OMENWARD에서 추출한 공용 병종 데이터·진영 시각 세트, 미니맵 제거, 조건부 우회로 공개, 문서 인수인계 사례를 추가했다.
- README, Documentation Map, 벤치마킹 가이드를 새 지식 구조에 맞게 갱신했다.
- 활성 프로젝트 사양은 프로젝트 저장소에 남기고 Base 사례에는 일반화된 문제·판단·검증만 기록하는 경계를 명시했다.

## v1.4.0 - content design and first-10-minute validation

기능 목록보다 의도·플레이 경험·규칙·흐름을 먼저 설계하고, 핵심 재미와 첫 10분을 최소 PoC로 검증하는 공용 콘텐츠 기획 기준을 추가했다.

변경:

- `docs/CONTENT_DESIGN_METHOD.md`를 추가했다.
- 핵심 재미, Dopamine Driven Development, 첫 10분 계약, 콘텐츠 정체성 카드, 정보 역할 분리, PoC 재조정 기준을 정리했다.
- 콘텐츠를 추가하지 않는 판단과 P0/P1/P2 우선순위 기준을 추가했다.
- Codex 전달용 사양 항목과 구현 사실·승인 설계·미확정 구분을 명시했다.
- `templates/CONTENT_DESIGN_BRIEF.md`를 추가했다.
- README와 문서 역할표에 새 공용 문서와 템플릿을 연결했다.

## v1.3.0 - resource-aware agent operation

여러 AI와 선택형 보조 도구를 함께 사용할 때 핵심 작업량을 유지하면서 로컬 자원 중복을 줄이는 공용 기준을 추가했다.

변경:

- 성능 문제는 작업량 축소 전에 메모리와 중복 프로세스를 측정하도록 했다.
- 선택형 MCP, 대시보드, 언어 서버는 필요한 작업에서만 실행하도록 했다.
- 대용량 외부 worker의 기본 동시 실행 수와 결과 회수 범위를 제한하도록 했다.
- 성공한 임시 자원만 정리하고 실패하거나 변경이 남은 작업 공간은 보존하도록 했다.
- 재시작 후 프로세스 수와 전후 자원 사용량으로 최적화 결과를 검증하도록 했다.

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
