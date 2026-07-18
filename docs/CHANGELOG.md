# Changelog

## v2.1.0 - selective skill routing, continuous learning and root planning governance

게임 프로젝트의 Foundation·분야별 스킬이 모든 의미 있는 실행에서 학습 기록을 남기고, 실제 근거가 있을 때만 스킬 계약을 갱신하도록 운영체계를 보강했다. 새 AI는 전체 스킬을 읽지 않고 Registry에서 현재 요청에 필요한 최소 스킬만 선택하며, 활성 `[기획서]`는 저장소 루트에서 즉시 찾을 수 있도록 했다.

변경:

- Base 공용 스킬의 기계 판독 라우터 `skills/SKILL_REGISTRY.json`과 공용 학습 기록 `skills/SKILL_LEARNING_LOG.md`를 추가했다.
- `routing-project-work-by-discipline` 스킬을 추가해 주 책임 분야 하나, 영향 분야, 변경 유형, 최소 Foundation·분야 스킬과 후속 스킬을 판정하도록 했다.
- `maintaining-project-context-and-handoff` 스킬을 추가해 Active Context·Handoff를 책임 원본의 복제본이 아닌 현재 상태·다음 작업·위험 라우터로 유지하도록 했다.
- `verifying-game-project-operating-system` 스킬과 Health Review 템플릿을 추가해 루트 기획서, 책임 원본, Registry, Learning Log, 개발 게이트, 이미지·PDF, 자동화와 콜드 스타트를 증거 기반으로 검수하도록 했다.
- 분야 스킬 Method·실행 스킬·템플릿에 `trigger_tags`, `load_by_default=false`, 사용·비사용 조건, Learning Log, review trigger와 지식 상태를 추가했다.
- 모든 의미 있는 스킬 호출은 결과·실패·예외·사용자 피드백·과다 호출·누락 검증과 스킬 변경 필요성을 기록하되, 근거가 없으면 스킬 본문을 무조건 수정하지 않고 `변경 없음`과 이유를 남기도록 했다.
- 신규·승인된 프로젝트 구조에서 활성 `[기획서]`를 저장소 루트 바로 아래에 두고 중첩 현행 복제본을 금지하도록 시작 문서·Method·Installer·Documentation Map·계획 템플릿을 정렬했다.
- 프로젝트용 `SKILL_REGISTRY.json`, 사람용 `PROJECT_SKILL_MAP.md`, Foundation·분야 Skill 계약과 Learning Log 템플릿을 연결했다.
- Skill Routing Governance Checker를 추가해 루트 `[기획서]`, Registry 정책, 중복 ID, 활성 경로, trigger, Learning Log, 11개 분야 진입 스킬과 스킬 변경 동기화를 검사하도록 했다.
- Issue·PR·CODEOWNERS·GitHub Actions·공용 체크리스트를 Registry·Learning Log·Health Review와 연결했다.
- 정상 Registry, 중첩 기획서, 전체 스킬 자동 로드, 분야 진입 스킬 누락, Learning Log 누락과 스킬 변경 동기화 실패 회귀 테스트를 추가했다.

## v2.0.0 - game project repository operating system

새 채팅, 새 GPT와 새 Codex가 Base URL 하나에서 동일한 시작 규칙을 찾고, 대상 게임 프로젝트에 분야별 본책·이미지 책임 원본·GitHub 검사를 분화해 설치할 수 있는 공용 저장소 운영체계를 추가했다.

변경:

- 루트 `START_HERE.md`를 추가해 Base URL 호출 계약과 요청별 method·skill 라우팅을 고정했다.
- `AGENTS.md`에 Base 호출, 운영체계 설치, 분야·영향도 선언, Markdown 책임 원본과 이미지 캐노니컬 경로 규칙을 추가했다.
- `GAME_PROJECT_OPERATING_SYSTEM_METHOD.md`를 추가해 프로젝트 허브, 11개 제작·지원 분야, 분야별 본책, 상태 언어, 사용자 가독성, Visual Source, 개발 게이트와 자동화 경계를 정리했다.
- `installing-game-project-operating-system` 스킬을 추가해 감사→인벤토리→책임 구조 설계→설치 계획→문서·이미지·GitHub Workflow 설치→이관→콜드 스타트 검수 절차를 실행 가능하게 만들었다.
- `templates/project-operations/`에 설치 Work Order, 사용자용 시작 대시보드, 분야별 본책, 갱신 매트릭스, GPT·Codex·GitHub Workflow, Visual Source와 Asset Manifest를 추가했다.
- GitHub Issue·PR 템플릿, 경로·변경 규칙 설정, 표준 라이브러리 기반 governance 검사기와 GitHub Actions 예시를 추가했다.
- 검사기는 필수 시작 문서, 깨진 로컬 Markdown 링크, 금지된 활성 버전 파일명, Asset ID·캐노니컬 경로 중복과 변경 유형별 관련 본책 갱신 누락을 확인하도록 설계했다.
- README와 Documentation Map을 `START_HERE → 운영체계 설치 스킬 → 프로젝트 전용 템플릿` 경로로 갱신했다.
- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않고, 콘셉트·방향 승인·제작 준비·구현·시각 검증과 `MIGRATION_PENDING`을 구분하도록 했다.
- GitHub Actions 파일 존재, 실제 실행 확인, 브랜치 보호의 Required Status Check 강제를 서로 다른 설치 상태로 구분했다.
- 특정 프로젝트의 세계관·수치·실제 경로는 Base에 승격하지 않고 대상 프로젝트 본책과 Manifest에서 관리하도록 경계를 유지했다.

## v1.9.3 - applied planning, dialogue and vertical-slice cases

십보강호의 활성·백업·보류 문서 전체를 감사해 문서 작성 과정에서 확인한 재사용 가능한 노하우를 기존 Base 기획 method, 서사 method와 실행 skill에 적용 사례로 반영했다. 프로젝트 고유 수치와 무협 콘텐츠는 승격하지 않았으며, 실제 구현·플레이테스트 전인 항목은 사례 상태를 유지했다.

변경:

- `TEN_PACES_RULE_PRESENTATION_TRACEABILITY_CASE.md`를 추가해 규칙→구조화 결과→UI·연출→사용자 설명 가능성 QA의 추적 구조를 사례화했다.
- `TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`를 추가해 대표 상위 하이라이트의 보유·미보유 경로를 모두 완주 가능하게 검증하는 방법을 정리했다.
- `DIEGETIC_OPPONENT_INFORMATION_CASE.md`에 최초·반복·상세·결과 확인 문구 역할과 현지화·매핑 검수를 보강했다.
- `CONTENT_DESIGN_METHOD.md`, `PLANNING_SYSTEM_METHOD.md`, `NARRATIVE_AND_RELATIONSHIP_METHOD.md`에 프로젝트 유래 적용 사례를 추가했다.
- `writing-game-design-documents`와 `designing-vertical-slices` 스킬에 책임 원본 분리와 선택적 하이라이트 사례를 추가했다.
- README와 사례 인덱스에 신규 사례를 연결했다.
- 이전 6슬롯·9전·1~5성 문서는 백업 반례로, 문파별 성과 평가는 보류 반례로만 사용했다.
- 실제 런타임, 플레이어 문구 학습, 보유·미보유 완주율은 아직 검증되지 않았으므로 공용 검증 스킬로 승격하지 않았다.

## v1.9.2 - bidirectional learning and diegetic information cases

십보강호의 기획·연출·인수인계 최적화에서 얻은 공용 교훈을 프로젝트 고유 수치와 분리해 Base 사례로 추가했다. 공용 Base를 프로젝트에 적용하는 과정과 프로젝트 결과를 다시 Base 학습 데이터로 환류하는 과정을 사례화했으며, 내부 난도·성장 데이터를 일관된 세계관 표현으로 암시하는 정보 설계 사례를 기록했다.

변경:

- `BASE_PROJECT_BIDIRECTIONAL_LEARNING_CASE.md`를 추가해 Base 문서 지도 확인→프로젝트 구체화→검증→Base 환류의 양방향 학습 순환을 사례화했다.
- `DIEGETIC_OPPONENT_INFORMATION_CASE.md`를 추가해 내부 강도·행운·투자 스타일과 이명·풍문·평가·정탐 표현을 의미 키로 분리하는 방법을 정리했다.
- 두 사례에 프로젝트 전용 수치·세계관·파일 경로를 복사하지 않는 경계와 후속 검증 조건을 명시했다.
- `docs/knowledge/cases/README.md`의 사례 분류와 문제별 라우팅에 두 사례를 연결했다.
- 내부 데이터→세계관 표현 자동화와 표준 테스트는 실제 구현·플레이 검증 전이므로 새 검증 스킬로 승격하지 않고 사례 상태로 유지했다.

## v1.9.1 - learning Base, project specialization and cold-start continuity

Base를 **[학습형] [공용] 데이터 원본**, 프로젝트를 공용 지식을 실제 게임에 맞게 분화·적용·검증하는 전용 작업 공간으로 명확히 정의했다. 새 채팅·새 AI·새 작업자가 과거 대화 없이 저장소만으로 작업을 재개할 수 있도록 기획서·Roadmap·스킬·Active Context·Documentation Map의 지속성 계약을 최상위 규칙으로 추가했다.

변경:

- `AGENTS.md`에 Base·프로젝트 경계, 공용·전용 컨텍스트 동시 확인, 작업 종료·인수인계 학습 환류와 콜드 스타트 규칙을 추가했다.
- 프로젝트 기획서만으로 핵심 경험, 방향, 범위와 금지 방향을 이해하고 세부 구현은 참조 원본을 따라 확인하도록 책임을 분리했다.
- Roadmap에 현재 단계, 우선순위, 선행 조건, 다음 작업, 종료 기준과 검증을 항상 유지하도록 했다.
- Base skill과 프로젝트 skill extension을 실제 파일·데이터·완료·실패 기준에 연결하도록 했다.
- `AI_SHARED_WORK_RULES.md`, `AI_WORKFLOW_RULES.md`, `MVP_WORKFLOW_CHECKLIST.md`를 공용 학습→프로젝트 분화→실제 검증→Base 환류 흐름으로 정렬했다.
- `docs/knowledge/README.md`에 관찰→가설→채택→패턴→검증의 학습 상태와 작업 시작·종료 규칙을 추가했다.
- `promoting-project-knowledge`와 `writing-game-design-documents` 스킬에 작업 종료·인수인계 사례 작성, 지식 상태, Roadmap·스킬 최신화와 콜드 스타트 검수를 추가했다.
- `PROJECT_HANDOFF_CONTEXT_METHOD.md`, `DESIGN_DOCUMENT_SYSTEM.md`, `HANDOFF_CONTEXT.md`, 프로젝트 `AGENTS.md` 템플릿을 새 작업자 재개 기준에 맞게 갱신했다.
- 인수인계 템플릿의 오래된 작성 방법 경로를 실제 `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`로 수정했다.
- `DOCUMENTATION_MAP.md`에 공용 학습 데이터와 프로젝트 전용 데이터의 읽기 순서, 책임 원본, 종료 갱신 체크를 연결했다.
- 공용화 가능한 내용이 없을 때 Base를 억지로 수정하지 않고 프로젝트 전용·단발성 작업으로 기록하도록 했다.

## v1.9.0 - external AI worktrees and art prompt technique library

DeepSeek를 포함한 외부 AI의 대용량 초안을 별도 worktree에서 생성하고 Codex가 실제 diff·근거·테스트를 검수해 반영하는 협업 구조를 추가했다. 아트·UI 디자인 기술을 프롬프트 사례, 모델 호환성, 실패 기준과 함께 관리하고 FACS 표정 편집 및 캐릭터 프로모션 포스터 사례를 공용 지식으로 정리했다.

변경:

- `orchestrating-deepseek-worktrees`와 `reviewing-external-ai-drafts` 실행 스킬을 추가했다.
- GPT가 기획·작업 패키지를 만들고 DeepSeek가 격리 공간에서 대량 초안을 작성하며 Codex가 세부 검수·실제 반영을 담당하는 역할 계약을 추가했다.
- 안정적인 프롬프트 접두부, 파일 allowlist, 구조화 출력, cache hit·miss 기록 등 토큰·컨텍스트 효율 원칙을 정리했다.
- 프로젝트별 GPT·DeepSeek·Codex 역할, worktree, 비용·보안 정책을 기록하는 AI 협업 프로필과 작업·검수 템플릿을 추가했다.
- `designing-art-prompts-and-technique-cards` 스킬과 `AI_ART_PROMPT_TECHNIQUE_METHOD.md`를 추가했다.
- 아트·UI 기술 카드에 사용자 가치, 사용·비사용 조건, 모델 호환성, 프롬프트 패턴, 제어어, UI/UX 데이터, QA와 검증 상태를 기록하도록 했다.
- FACS AU를 자연어 표정 설명의 보조 어휘로 사용하는 방법과 표준 코드·제공 레퍼런스의 비표준 별칭 경계를 정리했다.
- 캐릭터 포스터를 메인 일러스트, 정보 슬롯, 인셋 표정, 편집 가능한 타이포그래피로 분리하는 사례와 템플릿을 추가했다.
- 아트디자인 기획서에 디자인 기술 라이브러리, 기본·편집·실패 수정 프롬프트, 모델·현지화·후처리 QA를 추가했다.
- Git worktree, DeepSeek context caching·JSON output, OpenAI prompt caching·prompt engineering 공식 자료 메모를 추가했다.
- README, Documentation Map, 작업 흐름, 스킬 가이드, 아트 스킬 매트릭스와 사례 인덱스를 갱신했다.

## v1.8.0 - executable prompt, design-document and vertical-slice skills

짧은 사용자 요청을 실행 가능한 프롬프트로 변환하고, 기획서 체계·Vertical Slice·프로젝트 지식 승격을 실제로 적용할 수 있는 실행 스킬 구조를 추가했다. 동시에 중복 설명을 책임 문서와 스킬로 분리해 Base 진입 문서를 압축했다.

변경:

- 루트 `skills/`에 실행 가능한 `SKILL.md` 구조와 라우터를 추가했다.
- `transforming-requests-into-prompts`에 목적·맥락·경험·범위·제약·산출물·완료·검증의 8요소 공식을 추가했다.
- `designing-vertical-slices`에 Prototype·Vertical Slice·MVP·Demo 구분, 대표 경험, 품질 기준, 제작 파이프라인 검증을 추가했다.
- `writing-game-design-documents`에 기획서 종류, 질문별 책임 원본, 프로젝트 전용 확장 기준을 추가했다.
- `promoting-project-knowledge`에 프로젝트 결과를 규칙·method·research·skill·template·case로 분류하는 승격 절차를 추가했다.
- 실행 프롬프트, Vertical Slice, 기획 문서 체계, 프로젝트 스킬 확장 템플릿을 추가했다.
- `AGENTS.md`, `README.md`, 작업 흐름, 스킬 가이드, 문서 지도와 지식 베이스 라우터를 새 구조에 맞게 압축·정렬했다.
- 저장소 전체 무조건 읽기 대신 Documentation Map 기반 영향 범위 검토, L0~L4 작업 분류, 리팩터링 동작 불변, GitHub·로컬 비자동 동기화 규칙을 명확히 했다.
- 활성 기준 문서를 새 버전 복제본으로 만들지 않고 기존 원본을 직접 갱신하는 정책을 유지했다.

## v1.7.1 - deferred item lifecycle

아이디어를 삭제하지 않고 보존하면서도 활성 기획·구현 범위와 혼동하지 않도록 보류 문서의 수명주기 규칙을 추가했다.

변경:

- `docs/AI_SHARED_WORK_RULES.md`에 `[보류]`, `deferred`, `parking-lot` 영역을 활성 작업의 기본 읽기 대상에서 제외하는 규칙을 추가했다.
- 구현 AI가 보류 문서를 직접 구현하지 않고, 재개 시 기준 문서와 Issue·Goal·Plan에 다시 통합하도록 했다.
- 백업·아카이브와 보류 영역의 목적을 구분했다. 백업은 과거 상태 보존, 보류는 미확정·후속 아이디어 보존이다.

## v1.7.0 - automatic Base promotion and canonical document lifecycle

프로젝트 작업에서 발견한 안정적이고 일반화 가능한 공용 규칙을 후보 보고에서 멈추지 않고 Base에 자동 반영하는 운영 방식으로 변경했다.

변경:

- `AGENTS.md`에 모든 프로젝트 작업의 공용 규칙 자동 승격을 기본 원칙으로 추가했다.
- `docs/AI_SHARED_WORK_RULES.md`의 승인 후 수동 승격 절차를 자동 승격 절차와 금지 기준으로 교체했다.
- `docs/AI_WORKFLOW_RULES.md` 종료 단계에 공용 규칙 분리, Base 자동 반영, 프로젝트 동기화 확인을 추가했다.
- `docs/MVP_WORKFLOW_CHECKLIST.md`의 `Base 승격 후보` 단계를 자동 승격 체크리스트로 교체했다.
- `README.md`, `docs/DOCUMENTATION_MAP.md`, `docs/knowledge/README.md`의 승격 흐름을 동일한 정책으로 정렬했다.
- 검증되지 않은 가설과 프로젝트 고유 이름·수치·세계관·엔진 경로는 자동 승격에서 제외하도록 했다.
- 현행 책임 문서 하나만 유지하고 기존 파일을 직접 갱신하며, 이전 내용은 Git 이력으로 보존하는 문서 수명주기 원칙을 추가했다.

## v1.6.0 - planning, narrative and presentation knowledge expansion

공용 기획 지식 베이스를 전체 기획 체계, 서사·관계, 캐릭터 아트, 대화·이벤트 연출, 기획·조사·인수인계 방법과 프로젝트 사례까지 확장했다.

변경:

- `PLANNING_SYSTEM_METHOD.md`를 추가해 상태·방향·분야별 책임 문서·로드맵·검증의 계층을 정리했다.
- `NARRATIVE_AND_RELATIONSHIP_METHOD.md`를 추가해 장면, 대사 모드, 선택 기억, 관계 태그, 후일담과 데이터 경계를 정의했다.
- `CHARACTER_AND_NARRATIVE_ART_METHOD.md`를 추가해 초상·표정·캐릭터 자산·생성 이미지·텍스트 분리와 실제 화면 QA를 정리했다.
- `DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`를 추가해 대화 UI, 배치, 표정 의미 키, 컷인, 음향, 접근성, 상태 비소유 원칙을 정리했다.
- `PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md`를 추가해 의도 합성, 현재 상태 감사, PoC, 수용 기준, 인수인계와 지식 승격 능력을 계약화했다.
- urban-legend 프로젝트에서 추출한 장면 중심 UI, 표시명·내부 ID 분리, 대사 밀도, 선택 기억, 프레젠테이션 상태 경계, 텍스트 없는 생성 자산, 문서 생명주기 사례 7건을 추가했다.
- 프로젝트 방향, 서사, 아트, 연출, handoff 전문 템플릿을 `templates/planning/`에 추가했다.
- README, Documentation Map, knowledge 인덱스와 사례 인덱스를 새 구조에 맞게 갱신했다.
- 병렬로 생긴 `docs/planning/` 중복 구조는 canonical `docs/knowledge/`로 통합하고 제거하도록 정리했다.

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
