# [프로젝트명] 프로젝트 스킬 지도

- 책임: 프로젝트 허브·통합검수
- 마지막 검토일:
- 기준 커밋:
- Base 기준 커밋:

> 새 채팅은 전체 skills 폴더를 읽지 않는다. 현재 작업에 필요한 foundation 스킬과 주 책임 분야 스킬만 이 지도에서 선택한다.

## 1. 스킬 읽기 순서

```text
프로젝트 AGENTS.md
→ START_HERE.md
→ Documentation Map
→ 관련 분야 본책
→ 이 PROJECT_SKILL_MAP.md
→ 필요한 foundation 스킬
→ 필요한 분야별 프로젝트 스킬
→ 실제 파일·데이터·자산·테스트
```

## 2. Foundation·공용 스킬

| 작업 | 현행 프로젝트 스킬 | Base 원본 | 입력 | 산출물 | 검증 | 상태 |
|---|---|---|---|---|---|---|
| 요청 접수·컨텍스트 라우팅 |  | `skills/transforming-requests-into-prompts/` |  |  |  |  |
| 영향도 분석 |  |  |  |  |  |  |
| 개발 게이트 검수 |  | `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md` |  |  |  |  |
| 결정 기록 |  |  |  |  |  |  |
| 문서 수명주기·지도 갱신 |  | `skills/writing-game-design-documents/` |  |  |  |  |
| 검증·완료 선언 |  |  |  |  |  |  |
| 분야 PDF 발행 |  | `skills/publishing-discipline-bibles/` |  |  |  |  |
| 인수인계·컨텍스트 압축 |  | `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` |  |  |  |  |
| 외부 AI 결과 검수 |  | `skills/reviewing-external-ai-drafts/` |  |  |  |  |
| 프로젝트 학습·Base 환류 |  | `skills/promoting-project-knowledge/` |  |  |  |  |

## 3. 분야별 진입 스킬

| 분야 | 분야 본책 | 현행 진입 스킬 | 주요 입력 | 주요 산출물 | 검증 | 하위 스킬 | 상태 |
|---|---|---|---|---|---|---|---|
| 설정·내러티브 |  |  |  |  |  |  |  |
| 게임 디자인 |  |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |  |
| 개발·엔지니어링 |  |  |  |  |  |  |  |
| 테크니컬 아트·파이프라인 |  |  |  |  |  |  |  |
| 아트 |  |  |  |  |  |  |  |
| 사운드 |  |  |  |  |  |  |  |
| QA |  |  |  |  |  |  |  |
| 프로덕션·PM |  |  |  |  |  |  |  |
| 분석·유저리서치 |  |  |  |  |  |  |  |
| 통합검수 |  |  |  |  |  |  |  |

프로젝트 규모상 통합된 분야는 동일 스킬 파일의 별도 책임 장 또는 명확한 연결 스킬로 표시한다. 책임 자체를 삭제하지 않는다.

## 4. 권장 분야별 스킬 후보

### 설정·내러티브

- maintaining-world-canon
- designing-narrative-content
- reviewing-character-and-dialogue-consistency

### 게임 디자인

- designing-game-systems
- designing-combat-and-economy
- balancing-gameplay-data
- planning-content-and-progression

### UX·UI·접근성

- designing-information-architecture
- designing-gameplay-interactions
- validating-onboarding-and-accessibility

### 개발·엔지니어링

- designing-project-architecture
- implementing-approved-features
- refactoring-with-regression-safety
- validating-save-performance-and-builds

### 테크니컬 아트·파이프라인

- defining-asset-contracts
- importing-and-validating-assets
- optimizing-visual-pipelines

### 아트

- directing-game-art
- producing-game-assets
- reviewing-visual-consistency
- controlling-image-generation-and-postprocess

### 사운드

- designing-game-audio
- implementing-audio-events
- reviewing-mix-repetition-and-accessibility

### QA

- designing-test-strategy
- executing-regression-and-release-qa
- triaging-and-verifying-defects

### 프로덕션·PM

- planning-milestones-and-dependencies
- managing-scope-risk-and-budget-status
- running-greenlight-reviews

### 분석·유저리서치

- conducting-benchmark-research
- designing-playtests
- analyzing-telemetry-and-behavior

### 통합검수

- auditing-cross-discipline-consistency
- validating-documentation-governance
- reviewing-release-readiness

후보를 모두 만들지 않는다. 실제 반복 작업·별도 품질 기준·검증 경로가 있을 때만 현행 스킬로 채택한다.

## 5. 스킬 상태

| 상태 | 의미 |
|---|---|
| 현행 | 현재 작업에서 사용하는 책임 스킬 |
| 보조 | 현행 스킬이 연결하는 세부 절차 |
| 관찰 | 한 번 발견한 개선점 |
| 가설 | 추가 적용·검증 필요 |
| 패턴 | 프로젝트 안에서 반복된 경향 |
| 검증 | 여러 조건에서 재현된 안정적 방법 |
| 승격 후보 | Base 공용화 검토 가치 있음 |
| 보류 | 재개 조건 전에는 사용하지 않음 |
| 백업 | 외부 원본·감사 목적으로만 보존 |
| 제거 후보 | 통합·참조 검증과 승인 대기 |

## 6. 중복·통합 검수

| 스킬 A | 스킬 B | 공통 부분 | 고유 부분 | 처리 | 새 책임 원본 | 검증 |
|---|---|---|---|---|---|---|
|  |  |  |  | 유지/통합/foundation 분리/제거 후보 |  |  |

## 7. 학습·갱신 트리거

- 동일 실패가 반복됨
- 사용자 피드백이 기존 완료 기준과 다름
- 실제 파일·도구·경로가 변경됨
- 새 예외·폴백이 필요함
- 검증 명령·Quality Bar가 변경됨
- 여러 분야에 같은 절차가 복제됨
- 프로젝트 교훈이 다른 프로젝트에도 재현됨

## 8. 콜드 스타트 검수

- [ ] 각 분야의 진입 스킬을 2분 안에 찾을 수 있다.
- [ ] 분야 스킬에서 본책·실제 파일·검증으로 이동할 수 있다.
- [ ] 공용 스킬과 분야 스킬의 책임이 겹치지 않는다.
- [ ] 백업·보류 스킬은 기본 읽기에서 제외된다.
- [ ] 미검증 가설을 현행 강제 규칙처럼 사용하지 않는다.
