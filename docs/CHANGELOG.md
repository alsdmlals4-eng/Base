# Changelog

## Unreleased - Base audit and operating-contract consistency

- GPT가 기획·벤치마킹·시스템·데이터·UX·비-Godot 파일·GitHub 계약과 검수를 완료하고 Codex에는 읽기 전용 Plan 재검수 뒤 단계별 Godot 구현만 인계하는 공용 정책을 추가했다.
- Codex의 동작 보존 기술 개선과 프로젝트 코어·플레이 규칙·MVP·주요 UX·저장 호환성 변경을 `CHANGE_PROPOSAL`로 분리했다.
- 마스터 구현계획, Codex 패키지 Plan 보고서, Godot 구현 패키지 계약, 상위 Issue·패키지별 Branch·PR·사용자 병합 승인 Template을 추가했다.
- Grill Me를 새 중복 Skill로 만들지 않고 `managing-project-intake-and-work-contract`의 `clarify` Mode에 통합해 저장소 우선 조사, 한 번에 하나의 질문, GPT 권장안, 결정 원장과 종료 기준을 고정했다.
- `maintaining-project-context-and-handoff`에 `implementation-package-handoff` Mode를 추가해 GPT 계약 갱신 → Codex Build → GPT diff·테스트 검수 → 사용자 승인 흐름을 연결했다.
- GitHub Actions를 `DOCS_ONLY / CANONICAL_CONTRACT / CODE_OR_ENGINE / CI_TOOLCHAIN_HIGH_RISK / FULL_MATRIX`로 계층화하고 PR concurrency 취소, 조건부 발행·Windows smoke와 안정된 `ci-gate`를 추가했다.
- Issue·Goal·Branch·PR·Run·Artifact·Release의 책임을 분리하고, 같은 Goal의 기존 PR 재사용, 열린 PR WIP 권장 최대 3개, 종료·Branch 처리, 임시 증거 만료 전 PR 검증 요약을 공용 정책과 Template으로 고정했다.
- 첫 Actions 실행에서 발견한 pnpm 초기화 순서와 Skill Registry·Learning Log·집중 회귀 동기화 누락을 수정하고 재발 방지 테스트를 추가했다.
- 제공된 학습 텍스트의 책임을 전수 매핑하고 9개 독립 Skill을 추가했으며, 중복 책임은 기존 통합 Skill에 유지했다.
- 가지치기·본문 간소화·행동 보존 리팩토링 Skill을 분리하고 이를 Base의 코어·컨셉·적대적 검토·Skill 진화 본문에 실제 적용했다.
- Games User Research 11영역, 로컬·GitHub 동기화, 장기 작업 연속성, 사용자 학습 노트, 프로젝트 대시보드, 엔진 런타임 디버깅 계약을 추가했다.
- 원문 책임 coverage JSON·checker·회귀 테스트와 최적화 보고서를 추가했다.
- 기존 프로젝트의 기획·시스템·코드 코어와 코어·MVP 경계를 판정하는 `identifying-project-core`를 추가했다.
- PLAN 단계에서 코어 제안·반례 검토·사용자 승인·책임 원본 연결을 수행하는 `establishing-project-core`를 추가했다.
- 레드팀 공격·비판 검증·승인된 finding만 개선·회귀 재검토하는 `running-adversarial-review-and-refinement`를 추가했다.
- SlopSlap 기준 커밋의 51개 tracked 파일과 27개 시각 자산을 전수 감사하고, 외부 Claude·브라우저 런타임 없이 동작하는 Godot/Web UI 아트 감사 스킬을 추가했다.
- A~E 읽기 전용 후보 검사, 목적 있는 디자인 반례, 사용자 승인 게이트, 순차 개선, 독립 재감사와 실제 전후 렌더 계약을 추가했다.
- UI Art Findings JSON Schema와 Windows/Linux 호환 정적 검사기를 추가했으며, 정적 패턴만으로 결함이나 “AI slop”을 확정하지 않도록 했다.
- Ouroboros 기준 커밋의 1,465개 tracked 파일을 전수 인벤토리화하고, 외부 MCP 없이 동작하는 `conducting-deep-requirement-interviews` Foundation 스킬을 추가했다.
- 기능·게임 경험·아트 방향·구조·워크플로·Base 변경 제안에 저장소 사실 확인 → 딥인터뷰 → 사용자 마지막 확인 → 실행 프롬프트 게이트를 연결했다.
- 인터뷰 Registry·기록 템플릿·JSON Schema·검사기를 추가해 사용자 확인 전 실행 프롬프트 생성을 차단한다.
- 프로젝트 교훈을 `[수정제안서]`의 제안 전용 PR로 먼저 보존하고 사용자 승인 뒤 별도 구현 PR로 승격하는 계약을 추가했다.
- Base Skill Registry와 수정제안서 Registry에 JSON Schema 검증을 추가했다.
- 분야 스킬 진화 계약의 JSON 전용 입력, 11개 분야 전체 진입점, DOCX·다이어그램 상시 생성 표현을 schema v3 선택 계약에 맞게 수정했다.
- LibreOffice는 격리된 임시 문서를 실제 PDF로 변환하고 Poppler·Mermaid는 실행 결과를 확인해 경로만 존재하는 고장 난 환경을 사전점검에서 차단한다.
- schema v3에서 서술형 Markdown과 구조화 JSON을 문서별 단일 책임 원본으로 선택한다.
- PDF 상시 동기화, 선택 DOCX·Mermaid, 독립된 자동/Codex/사람 검수 상태를 구현했다.
- Registry·구조 데이터·Manifest JSON Schema와 v2.2.0 수동 마이그레이션 안내를 추가했다.
- 동일 입력 무재작성, 임시 생성·전 페이지 검증·원자 교체, 실패 시 기존 정상 산출물 보존을 구현했다.
- Windows·Linux 의존성 사전 점검과 실제 생성 CI를 추가했다.
- PR #8 이전 템플릿과 현재 `main`의 무손실 승계를 대조한 읽기 전용 감사를 추가했다.
- GitHub Issue와 사용자 승인 직접 요청을 동등한 작업 계약으로 지원한다.
- 프로젝트 로컬 Base 버전을 우선하고 원격 Base는 업데이트 조사 때만 비교하도록 통일했다.
- Active Context, Handoff, Roadmap, Decision Log, Changelog, Base Rules Version 템플릿을 추가했다.
- 11개 분야를 선택 가능한 공용 카탈로그로 정의하고 미선택 분야 강제를 제거했다.
- 자동 렌더 검수와 사람 시각 검수를 서로 독립된 상태로 분리했다.
- 삭제된 템플릿 참조와 임시 Google Docs 가져오기 파일을 정리했다.
- 필요한 도구·파일·폰트·인증·권한이 없을 때 사용자에게 이유와 설치·적용·확인 방법을 요청하고 실제 환경을 재검증하는 계약을 추가했다.
- schema v3 최종 감사에서 요구사항 추적, 무손실 승계, 13페이지 Codex 시각 검수, Actions·콜드 스타트·Branch protection 상태를 증거별로 기록했다.

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
- FACS AU를 자연어 표정 설명의 보조 어휘로 사용하는 방법과 표준 코드·제공 레퍼런스의 비표준 별칭 경계를 명시했다.
- 캐릭터 포스터를 메인 일러스트, 정보 슬롯, 인셋 표정, 편집 가능한 타이포그래피로 분리하는 사례와 템플릿을 추가했다.
- 아트디자인 기획서에 디자인 기술 라이브러리, 기본·편집·실패 수정 프롬프트, 모델·현지화·후처리 QA를 추가했다.
- Git worktree, DeepSeek context caching·JSON output, OpenAI prompt caching·prompt engineering 공식 자료 메모를 추가했다.
- README, Documentation Map, 작업 흐름, 스킬 가이드, 아트 스킬 매트릭스와 사례 인덱스를 갱신했다.
