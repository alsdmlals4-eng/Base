# Base

여러 게임 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 설계 방법, 실행 스킬, 템플릿과 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 각 프로젝트는 자신의 세계관, 규칙, 수치, 엔진, 실제 경로, 승인 이미지와 구현 상태를 자체 저장소에서 관리하고 Base를 프로젝트 상황에 맞게 **분화·적용·검증**합니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 Method·Skill·Template·Case
→ 대상 프로젝트 현행 책임 원본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 AI 작업 규칙](AGENTS.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [공용 스킬 Registry](skills/SKILL_REGISTRY.json)
- [공용 스킬 학습 기록](skills/SKILL_LEARNING_LOG.md)

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

저장소 접근이 가능한 GPT·Codex는 Base 전체와 모든 스킬을 무작정 읽지 않습니다. Base Skill Registry에서 현재 요청에 필요한 공용 스킬만 선택하고, 대상 프로젝트의 루트 `[기획서]`, Active Context, 분야 본책, Project Skill Registry와 실제 파일을 함께 확인합니다.

## 프로젝트의 기획서 위치

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 사용자가 쉽게 찾을 수 있도록 저장소 루트 바로 아래에 둡니다.

```text
<repository-root>/[기획서]/
```

`docs/[기획서]`, `src/[기획서]` 같은 중첩 현행 복제본은 만들지 않습니다. 운영 중인 기존 프로젝트의 안정된 경로는 감사와 사용자 승인 없이 강제로 이동하지 않습니다.

## 운영 모델

```text
Base 공용 Method·Skill·Template·Test
→ Skill Registry로 필요한 스킬만 선택
→ 프로젝트별 본책·스킬·실제 경로로 분화
→ 기획·구현·제작·검증
→ 성공·실패·미검증을 Learning Log에 기록
→ 근거가 있을 때 프로젝트 스킬 갱신
→ 반복 검증된 공용 원리만 Base로 환류
```

한 번 성공한 방법은 먼저 `관찰` 또는 `가설`로 기록하고 반복 검증 뒤 `패턴`, `검증`, `승격 후보`로 올립니다.

## 저장소 구조

```text
START_HERE.md      새 채팅·새 AI 최초 라우터
AGENTS.md          최소 공용 규칙
README.md          저장소 개요
docs/              상세 규칙·Method·Research·Skill Matrix·Case
skills/            직접 실행 가능한 공용 Skill·Registry·Learning Log
templates/         프로젝트에 복사·분화할 템플릿
tests/             운영체계·라우팅·문서·PDF 회귀 테스트
```

## 게임 프로젝트 운영체계

공용 운영체계는 다음을 연결합니다.

```text
프로젝트 방향
→ 루트 [기획서]
→ 분야별 활성 본책
→ 개발 게이트·Roadmap
→ Project Skill Registry·Map
→ 필요한 Foundation·분야 프로젝트 스킬
→ Issue·Goal·Plan
→ 코드·데이터·자산
→ 테스트·캡처·PDF 증거
→ Active Context·Handoff·Learning Log 갱신
```

기본 책임 분야:

1. 설정·내러티브
2. 게임 디자인
3. UX·UI·접근성
4. 개발·엔지니어링
5. 테크니컬 아트·콘텐츠 파이프라인
6. 아트
7. 사운드
8. QA
9. 프로덕션·PM
10. 분석·유저리서치
11. 통합검수

작은 프로젝트는 폴더·본책을 통합할 수 있지만 책임, 입력·출력, 프로젝트 스킬과 검증 경계는 유지합니다.

## 핵심 Method

| Method | 역할 |
|---|---|
| `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` | 분야별 본책·스킬·이미지·GitHub 운영체계 |
| `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md` | Ready·Implementation·Verification·Documentation·Completion과 제품 마일스톤 게이트 |
| `docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | 기존 프로젝트 고유 정보·참조를 보존하는 안전 마이그레이션 |
| `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | 선택적 스킬 호출, Foundation·분야 분리, 항상 학습과 Base 환류 |
| `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md` | 승인 이미지를 포함한 분야별 최신 PDF 통합본 |
| `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md` | 기획 책임 계층과 추적성 |
| `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` | 새 AI의 콜드 스타트와 인수인계 |

서사·아트·연출·조사 Method는 [Documentation Map](docs/DOCUMENTATION_MAP.md)에서 작업별로 선택합니다.

## 실행 스킬

| Skill | 사용할 때 |
|---|---|
| `skills/routing-project-work-by-discipline/` | 새 요청의 주 책임 분야·영향 분야·최소 스킬 집합을 판정할 때 |
| `skills/installing-game-project-operating-system/` | 새 프로젝트 또는 운영체계 미설치 프로젝트 |
| `skills/migrating-existing-game-project-structure/` | 운영 중인 기존 프로젝트의 안전한 구조 검수·재배치 |
| `skills/evolving-project-discipline-skills/` | 분야별 프로젝트 스킬 생성·통합·학습·Registry 갱신 |
| `skills/maintaining-project-context-and-handoff/` | 현재 상태·다음 작업·위험을 새 채팅용으로 압축할 때 |
| `skills/verifying-game-project-operating-system/` | 설치·마이그레이션·주요 게이트 후 운영체계 연결을 검수할 때 |
| `skills/publishing-discipline-bibles/` | 분야 Markdown·승인 이미지에서 PDF 생성·최신성 검수 |
| `skills/transforming-requests-into-prompts/` | 짧거나 모호한 요청을 실행 가능한 작업 계약으로 변환 |
| `skills/designing-vertical-slices/` | 최종 품질과 제작 파이프라인을 대표 구간에서 검증 |
| `skills/writing-game-design-documents/` | 책임 원본·Roadmap·기획서 구조 설계 |
| `skills/orchestrating-deepseek-worktrees/` | 외부 AI 대량 초안을 격리 worktree에서 생성 |
| `skills/reviewing-external-ai-drafts/` | 외부 AI 결과를 실제 diff·근거·테스트로 검수 |
| `skills/designing-art-prompts-and-technique-cards/` | 아트·UI 기술 카드와 이미지 프롬프트 설계 |
| `skills/promoting-project-knowledge/` | 프로젝트 교훈을 Base 공용 지식으로 환류 |

스킬은 특정 AI 브랜드가 아니라 사용 조건, 사용하지 않는 조건, trigger tags, 입력, 책임 원본, 절차, 산출물, 완료 기준, 검증, 실패 조건과 학습 조건을 정의합니다.

## 선택적 호출과 항상 학습

- `skills/SKILL_REGISTRY.json`은 Base 공용 스킬의 기계 판독 라우터입니다.
- 활성 스킬도 `load_by_default=false`입니다.
- 전체 skills 폴더를 기본 로드하지 않습니다.
- 주 책임 분야 스킬은 최대 하나, Foundation 스킬은 실제로 필요한 최소 개수만 선택합니다.
- 검증·PDF·Handoff 스킬은 해당 단계에 도달했을 때만 호출합니다.
- 모든 의미 있는 스킬 호출은 Learning Log에 성공·실패·예외·사용자 피드백과 변경 필요성을 기록합니다.
- 스킬 본문은 매번 무조건 수정하지 않습니다. 반복 실패, 새 예외, 책임·경로·검증 변경처럼 근거가 있을 때만 갱신합니다.
- 변경할 근거가 없으면 `스킬 변경 없음`과 이유를 기록합니다.

## 게임 프로젝트 운영 키트

`templates/project-operations/`에는 다음이 있습니다.

- 신규 설치 계획과 기존 프로젝트 마이그레이션 감사
- 루트 `[기획서]` 사용자·AI START_HERE와 Documentation Map
- Development Gates와 Document Update Matrix
- 분야별 활성 본책
- Project Skill Map과 기계 판독 Skill Registry
- Foundation·분야 스킬 계약과 Learning Log
- 운영체계 Health Review 보고서
- GPT·Codex·GitHub Workflow
- Visual Source of Truth와 Asset Manifest
- 분야 PDF 발행 계획과 Publication Manifest
- `[현행]`, `[백업]`, `[보류]`, `[제거 후보]` 수명주기
- Issue·PR·CODEOWNERS·문서·스킬 Governance 검사 예시

템플릿 폴더를 그대로 복사하지 않습니다. 기존 프로젝트는 먼저 현재 책임·참조·고유 정보를 감사하고 승인된 처리표 범위만 변경합니다.

## 개발 게이트

작업 단위:

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

제품 단계:

```text
Concept
→ Prototype
→ Graybox
→ First Playable
→ Vertical Slice
→ Production
→ Alpha
→ Feature Complete
→ Content Complete
→ Beta
→ Release Candidate
```

**Vertical Slice(버티컬 슬라이스)**는 최종 게임의 핵심 시스템·아트·사운드·UX·성능과 제작 파이프라인을 좁은 범위에서 목표 품질로 증명하는 플레이 가능한 구간입니다.

## 문서·이미지·PDF 원칙

- 한 질문에는 현행 책임 원본 하나만 둡니다.
- Markdown·구조화 데이터가 편집 가능한 책임 원본입니다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않습니다.
- 기존 승인 이미지가 있으면 별도 지시 없이 같은 항목의 새 시안을 만들지 않습니다.
- 이미지에는 Asset ID, 상태, 캐노니컬 경로, 채택·비채택 요소와 실제 캡처를 연결합니다.
- 분야 PDF는 요약이 아니라 목적부터 전체 작업 과정, 승인 이미지, 구현·검증 상태와 다음 작업까지 포함하는 읽기 전용 통합본입니다.
- Publication Manifest와 입력 해시로 PDF 최신성을 추적합니다.

## 수명주기와 컨텍스트 효율

- `[현행]`: 현재 책임 원본과 실행 스킬
- `[백업]`: 외부 원본·감사·승인 근거처럼 Git 이력만으로 부족한 자료
- `[보류]`: 재개 이유·조건·선행 작업을 가진 미래 항목
- `[제거 후보]`: 고유 정보·참조·복구·승인을 검증하기 전 삭제하지 않는 후보

단순 이전 버전은 별도 백업 복제본 대신 Git 이력으로 보존합니다. 기본 컨텍스트는 Documentation Map과 Skill Registry에서 현재 작업에 필요한 현행 문서와 스킬만 선택합니다.

## GitHub 운영

프로젝트 적용 시 다음을 분화할 수 있습니다.

- Issue Form: 목표·분야·범위·Ready·선택 스킬·검증
- PR Template: 영향 분야·게이트·문서·Registry·Learning Log·Manifest·PDF·미검증
- CODEOWNERS: 분야별 문서·스킬·자동화 리뷰
- Documentation Governance Checker: 필수 경로·링크·금지 파일명·Manifest·PDF 최신성·갱신 누락
- Skill Routing Governance Checker: 루트 `[기획서]`, Registry·진입 스킬·Learning Log·선택적 호출·동기화 누락
- GitHub Actions·Required Status Checks

파일이 존재하는 것과 실제 브랜치 보호·Required Check가 활성화된 것을 구분합니다.

## Base와 프로젝트 경계

Base에 둡니다.

- 여러 프로젝트에 재사용 가능한 판단법·절차·템플릿·검증 계약
- 적용 조건·실패 조건이 기록된 스킬
- Base 공용 Skill Registry·Learning Log
- 일반화한 성공·실패·미검증 사례와 회귀 테스트

프로젝트에 둡니다.

- 세계관·캐릭터·규칙·수치·용어
- 실제 엔진·코드·데이터·자산 경로
- 승인 이미지·프롬프트·PDF
- 구현·테스트·Roadmap·Issue·Plan
- Project Skill Registry와 실제 경로에 연결된 프로젝트 스킬

## 동기화와 완료

GitHub와 로컬은 자동 양방향 동기화되지 않습니다. 로컬 변경은 commit·push, 원격 변경은 fetch·pull이 필요합니다.

작업 완료 전에는 다음을 확인합니다.

1. 실제 결과와 승인·구현·검증 상태가 일치하는가?
2. 관련 본책·게이트·Project Skill Map·Registry·Active Context가 최신인가?
3. 호출 스킬의 Learning Log에 결과와 변경 필요성이 기록됐는가?
4. 이미지·자산·PDF Manifest가 최신인가?
5. 실행한 검증과 미검증이 분리됐는가?
6. 백업·보류·제거 후보가 기본 컨텍스트에서 제외됐는가?
7. 루트 `[기획서]`와 중첩 현행 복제 여부를 확인했는가?
8. 새 AI가 10분 안에 방향·상태·다음 작업·최소 스킬·검증을 찾는가?
9. 설치·마이그레이션·주요 게이트 후 Health Review가 필요한가?
10. 프로젝트 고유 정보와 Base 환류 후보가 분리됐는가?
