# Base

여러 게임 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 실행 스킬, 템플릿과 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 각 프로젝트의 세계관, 규칙, 수치, 엔진, 실제 경로, 승인 이미지와 구현 상태는 프로젝트 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 Skill·mode·reference·Template·Case
→ 대상 프로젝트의 책임 원본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [기획 작업순서·근거 정책](docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md)
- [근거 기반 게임 개발 지식 허브](docs/knowledge/game-development/README.md)
- [게임 개발 Evidence Pack](templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md)
- [게임 개발 Case Card](templates/research/GAME_DEVELOPMENT_CASE_CARD.md)
- [통합 Vertical Slice 실행문 v8](templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md)
- [GPT 이미지 생성·검수 및 Sheet 정책](docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md)
- [프로젝트 Google Sheets Workbook 계약](templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md)
- [프로젝트 GDD Google Sheets 정책](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [GPT 이미지 생성·검수 Plan](templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md)
- [공용 스킬 Registry](skills/SKILL_REGISTRY.json)
- [공용 어댑터 Skill Route](skills/BASE_SHARED_SKILL_ROUTES.json)
- [프로젝트 어댑터 계약](docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md)
- [이전 Skill ID 별칭](skills/LEGACY_SKILL_ALIASES.md)
- [공용 스킬 학습 기록](skills/SKILL_LEARNING_LOG.md)
- [Base 수정제안서]([수정제안서]/README.md)

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 스킬을 무작정 읽는다는 뜻이 아닙니다. Registry와 Documentation Map에서 현재 요청에 필요한 책임 원본과 최소 스킬만 선택합니다.

게임 기획·아트 기획·개발·AI 활용·벤치마킹·유저리서치·출시 판단을 외부 공식·현업·개발자·플레이어 근거로 개선할 때는 `docs/knowledge/game-development/README.md`에서 관련 Guide만 선택하고, `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`와 `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`로 결정 질문·근거·성공/실패 사례·적용 판정·검증을 연결합니다. 이 허브는 새 Skill이 아니며 기존 Skill의 실행 책임을 대체하지 않습니다.

상세 정본·작업 시작 인터뷰·Demo-First Vertical Slice·GPT→Codex·프로젝트 Sheet·GPT 이미지 생성과 검수를 파일 하나로 첨부하려면 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`를 사용합니다. 프로젝트 Sheet는 정확한 URL이 확인된 개별 프로젝트에서만 연결하며 Base 자체는 `BASE_EXCLUDED`입니다.

작업에 필요한 실행 파일·라이브러리·폰트·입력 파일·인증·권한이 없으면 필요한 이유, 설치·적용 방법, 확인 명령과 최소 권한을 안내합니다. 실행하지 않은 조사·검사·권한·도구는 통과로 보고하지 않습니다.

## 통합된 운영 구조

```text
요청 라우팅·요구 확정
→ 승인된 작업 계약·필요 시 실행 순서
→ 프로젝트 Sheet 의미 구조·기획 정본 연결
→ 결정 질문·분야 Coverage·외부 근거·성공/실패 Case
→ 기획 방향·GPT 시각화·이미지 검수 또는 구현·제작
→ Demo-First Vertical Slice·플레이테스트·AI Eval
→ 정본·정적·런타임·접근성·성능·회귀 검증
→ 책임 원본·Sheet·자산 원장·현재 상태 동기화
→ 인수인계·학습·필요 시 Base 승격
```

자세한 공용 규칙과 상태·발행 정책은 [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md)가 단일 설명 원본입니다.

## 활성 실행 스킬

활성 Registry는 **핵심 통합 실행 Skill 13개 + 구조·운영·지원 Skill 14개 = 전체 ACTIVE Skill 27개**를 관리합니다. 기계적 권한은 `skills/SKILL_REGISTRY.json`이 가집니다.

| Skill | 책임 |
|---|---|
| `managing-project-intake-and-work-contract` | 요청 라우팅·저장소 사실 조사·사용자 확인·실행 계약·작업 분해·의존성·순서화 |
| `managing-game-project-operating-system` | 신규 설치·기존 감사·승인된 마이그레이션·Health Review |
| `managing-design-documents` | 기획 책임 원본 작성·구조 변경·발행·검수 |
| `evolving-project-discipline-skills` | 프로젝트 스킬 생성·통합·학습 |
| `pruning-stale-and-nonfunctional-material` | 중복·죽은 자료·오래된 경로의 무손실 가지치기 |
| `simplifying-skill-bodies` | SKILL.md 핵심 계약 유지와 조건부 reference 분리 |
| `refactoring-with-contract-preservation` | 기능·인터페이스·데이터 보존 리팩토링 |
| `synchronizing-local-and-github-state` | 로컬·GitHub 상태의 안전한 비교·동기화 |
| `maintaining-long-running-task-continuity` | 장기 작업 checkpoint·재개·부분 전달 |
| `governing-game-user-research-coverage` | 게임 사용자 연구 11영역 설치·증거 coverage 감사 |
| `creating-user-learning-notes` | 작업 교훈을 사용자 학습 노트로 변환 |
| `building-project-visual-dashboards` | 정본 연결형 프로젝트 시각 대시보드 |
| `diagnosing-game-engine-runtime-failures` | Godot·Unity 런타임 재현·원인 격리·최소 수정 |
| `maintaining-project-context-and-handoff` | 현재 상태·다음 작업·위험 압축 |
| `analyzing-and-refining-game-concepts` | 핵심 컨셉·DDD·벤치마크·플레이어 반응·플레이테스트·PoC·기획 재조정 |
| `identifying-project-core` | 기존 프로젝트의 기획·시스템·코드 코어와 코어·MVP 경계를 근거로 판정 |
| `establishing-project-core` | PLAN 단계에서 프로젝트 코어를 제안·반례 검토하고 사용자 승인으로 확정 |
| `running-adversarial-review-and-refinement` | 실패 가정 공격·비판 검증·승인된 개선·회귀 재검토·저장소 전체 감사 |
| `designing-vertical-slices` | 대표 구간의 목표 품질·실제 플레이 증거·접근성·성능·제작 파이프라인 검증 |
| `orchestrating-deepseek-worktrees` | 외부 AI 대량 작업의 격리된 작업 공간 운용 |
| `reviewing-and-validating-project-changes` | 코드·데이터·문서·자산 변경의 계약·정본·정적·런타임·접근성·성능·회귀 검증 |
| `auditing-canonical-reference-freshness` | 오래된 경로·ID·정본 drift·파생본·변경 전파 누락 감사 |
| `designing-art-prompts-and-technique-cards` | 기획 시각화·최종 후보 이미지·목업·프롬프트·검수·승인 원장 |
| `auditing-and-refining-ui-art` | Godot·Web UI 결과 감사와 승인된 개선 |
| `managing-base-change-proposals` | 프로젝트 교훈 추출·BCP 제출·검토·승인된 구현 |
| `governing-legacy-retention-and-archives` | 레거시 보존·정본 통합·호환 stub·아카이브·승인 삭제 |
| `evaluating-godot-assets-and-plugins-before-creation` | Godot 기본 기능·무료·오픈소스·상용 자산을 직접 제작 전에 평가 |

통합 전 Skill ID는 [skills/LEGACY_SKILL_ALIASES.md](skills/LEGACY_SKILL_ALIASES.md)에서 새 Skill과 mode로 연결합니다.

주요 통합 mode:

- `decompose-and-sequence`: 검증 가능한 작업 결과·의존성·병렬화·게이트·롤백
- `benchmark-and-player-research`: 비교 게임·유저 반응·행동 근거의 분석과 개선 판정
- `playtest-and-experiment`: 빌드·테스터·피드백·이벤트·퍼널·A/B 테스트 계약
- `planning-visualization`: 기획 중 세계관·인물·핵심루프·시스템·UI 시각화
- `final-visual-candidate`: 기획 종료 후 Demo·상점·홍보·UI·캐릭터 후보 제작
- `visual-qa-and-approval`: 실제 화면·구현·권리·오류·재사용성 검수와 승인 판정
- `accessibility-review`: 핵심 정보·입력·UI·시간·난이도·모션의 장벽·대안
- `performance-profile`: 목표 플랫폼 frame time·CPU·GPU·메모리·네트워크·로딩 비교
- `reference-freshness`: 정본·경로·ID·Schema 변경의 전파 감사
- `repository-wide-audit`: tracked 파일·권한·구형 계약·untouched 소비자·Prompt drift 감사

## 프로젝트 GDD와 선택형 대시보드

일반 프로젝트 기획·상태 확인은 GitHub 정본과 **프로젝트 GDD Google Sheets**를 우선합니다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 선택적으로 사용합니다.

## 프로젝트 책임 원본

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 등록된 Markdown 또는 JSON 책임 원본
→ 실제 코드·데이터·자산·테스트
```

한 질문에는 현행 책임 원본 하나만 둡니다. 같은 서술을 Markdown과 JSON 양쪽에 독립 원본으로 복제하지 않습니다. 외부 벤치마크·리뷰·커뮤니티는 요구사항이나 구현 상태의 정본을 대체하지 않습니다.

각 문서는 Registry에서 발행 정책을 선택합니다.

- `source_only`: 원본과 직접 검증만 유지
- `milestone_sync`: 주요 게이트·공유 시 PDF·Manifest 동기화
- `always_sync`: 원본 변경과 같은 작업에서 PDF·Manifest 상시 동기화

DOCX와 다이어그램은 선언한 경우만 생성합니다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사용자 시각 검수는 독립 상태입니다.

## 저장소 구조

```text
START_HERE.md      새 채팅·새 AI 최초 라우터
AGENTS.md          항상 적용되는 공용 실행 규칙
README.md          저장소 개요
docs/OPERATING_MODEL.md  공용 작업 구조 단일 설명 원본
docs/knowledge/game-development/  기획·아트·개발·AI·근거 공용 Guide
docs/              Method·Research·Case·체크리스트
skills/            실행 Skill·Registry·Learning Log·상세 reference
templates/research/ 근거 조사·사례 기록 템플릿
templates/         프로젝트 분화·조사·실행·검증 템플릿
tools/             DOCX/PDF·다이어그램 생성기·Governance checker
tests/             운영체계·발행·라우팅·정본 최신성 회귀 테스트
[수정제안서]/      프로젝트발 Base 승격 후보·승인·구현 이력
```

## 개발 게이트

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval·Sequencing
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```
