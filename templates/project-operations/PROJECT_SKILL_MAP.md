# [프로젝트명] 프로젝트 스킬 지도

- 책임: 프로젝트 허브·통합검수
- 마지막 검토일:
- 기준 커밋:
- Base 기준 커밋:
- 기계 판독 Registry: `SKILL_REGISTRY.json`

> 새 채팅은 전체 skills 폴더를 읽지 않는다. 현재 작업에 필요한 foundation 스킬과 주 책임 분야 스킬만 `SKILL_REGISTRY.json`에서 선택하고 이 지도에서 책임·관계를 확인한다.

## 1. 스킬 읽기 순서

```text
프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ Documentation Map
→ Active Context
→ 관련 분야 본책
→ SKILL_REGISTRY.json
→ 이 PROJECT_SKILL_MAP.md
→ 필요한 foundation 스킬
→ 주 책임 분야 프로젝트 스킬
→ 실제 파일·데이터·자산·테스트
```

`routing-project-work-by-discipline`를 사용해 L1 이상 작업의 최소 스킬 집합을 판정한다.

## 2. 선택적 호출 정책

- 전체 스킬 자동 로드: 금지
- 기본 선택: 없음
- 주 책임 분야 스킬: 최대 1개
- Foundation 스킬: 실제 절차에 필요한 최소 개수
- 검증·PDF·인수인계 스킬: 해당 단계에서만 후속 호출
- 보류·백업·제거 후보 스킬: 호출 금지
- 같은 책임의 중복 스킬: 동시 호출 금지

## 3. Foundation·공용 스킬

| 작업 | 현행 프로젝트 스킬 | Base 원본 | trigger tags | 비호출 조건 | 입력 | 산출물 | 검증 | Learning Log | 상태 |
|---|---|---|---|---|---|---|---|---|---|
| 요청 접수·분야·스킬 라우팅 |  | `skills/routing-project-work-by-discipline/` |  |  |  |  |  |  |  |
| 요구 구체화·작업 계약 |  | `skills/transforming-requests-into-prompts/` |  |  |  |  |  |  |  |
| 영향도 분석 |  |  |  |  |  |  |  |  |  |
| 개발 게이트 검수 |  | `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md` |  |  |  |  |  |  |  |
| 결정 기록·추적성 |  |  |  |  |  |  |  |  |  |
| 문서 수명주기·지도 갱신 |  | `skills/writing-game-design-documents/` |  |  |  |  |  |  |  |
| 검증·완료 선언 |  |  |  |  |  |  |  |  |  |
| 분야 PDF 발행 |  | `skills/publishing-discipline-bibles/` |  |  |  |  |  |  |  |
| Active Context·Handoff |  | `skills/maintaining-project-context-and-handoff/` |  |  |  |  |  |  |  |
| 외부 AI 결과 검수 |  | `skills/reviewing-external-ai-drafts/` |  |  |  |  |  |  |  |
| 운영체계 Health Review |  | `skills/verifying-game-project-operating-system/` |  |  |  |  |  |  |  |
| 프로젝트 학습·Base 환류 |  | `skills/promoting-project-knowledge/` |  |  |  |  |  |  |  |

## 4. 분야별 진입 스킬

| 분야 | 분야 본책 | 현행 진입 스킬 | trigger tags | 비호출 조건 | 주요 입력 | 주요 산출물 | 검증 | Learning Log | 하위 스킬 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|
| 설정·내러티브 |  |  |  |  |  |  |  |  |  |  |
| 게임 디자인 |  |  |  |  |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |  |  |  |  |
| 개발·엔지니어링 |  |  |  |  |  |  |  |  |  |  |
| 테크니컬 아트·파이프라인 |  |  |  |  |  |  |  |  |  |  |
| 아트 |  |  |  |  |  |  |  |  |  |  |
| 사운드 |  |  |  |  |  |  |  |  |  |  |
| QA |  |  |  |  |  |  |  |  |  |  |
| 프로덕션·PM |  |  |  |  |  |  |  |  |  |  |
| 분석·유저리서치 |  |  |  |  |  |  |  |  |  |  |
| 통합검수 |  |  |  |  |  |  |  |  |  |  |

프로젝트 규모상 통합된 분야는 동일 스킬 파일의 별도 책임 장 또는 명확한 연결 스킬로 표시한다. 책임 자체를 삭제하지 않는다.

## 5. 권장 분야별 스킬 후보

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
- verifying-operating-system-health

후보를 모두 만들지 않는다. 실제 반복 작업·별도 품질 기준·검증 경로가 있을 때만 현행 스킬로 채택한다.

## 6. 스킬 상태

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

## 7. 중복·통합 검수

| 스킬 A | 스킬 B | 공통 부분 | 고유 부분 | 처리 | 새 책임 원본 | Registry 갱신 | 검증 |
|---|---|---|---|---|---|---|---|
|  |  |  |  | 유지/통합/foundation 분리/제거 후보 |  |  |  |

## 8. 항상 학습·갱신 계약

모든 의미 있는 스킬 호출은 해당 Learning Log에 기록한다.

- 결과: 성공 / 부분 성공 / 실패 / 미검증
- 호출 트리거와 실제 범위
- 성공 조건과 실패·예외
- 사용자 피드백
- 불필요하게 호출한 스킬
- 누락된 스킬·검증
- 스킬 변경 필요 여부
- 변경하지 않는 경우 그 이유
- 지식 상태와 다음 검토 트리거

스킬 본문을 매번 무조건 수정하지 않는다. 반복 실패, 새 예외, 책임·경로·검증 변경처럼 근거가 있을 때만 갱신한다.

## 9. 학습·갱신 트리거

- 동일 실패가 반복됨
- 사용자 피드백이 기존 완료 기준과 다름
- 실제 파일·도구·경로가 변경됨
- 새 예외·폴백이 필요함
- 검증 명령·Quality Bar가 변경됨
- 여러 분야에 같은 절차가 복제됨
- 프로젝트 교훈이 다른 프로젝트에도 재현됨
- 새 작업 유형에 대응하는 스킬이 없음
- 새 채팅이 필요한 스킬을 찾지 못함
- 90일 이상 활성 스킬 검토 기록이 없음

## 10. Registry 동기화 체크

- [ ] 모든 현행·보조 스킬 ID가 고유하다.
- [ ] 활성 스킬 경로가 실제 존재한다.
- [ ] `trigger_tags`, 사용·비사용 조건이 있다.
- [ ] `load_by_default=false`다.
- [ ] Learning Log와 review trigger가 있다.
- [ ] 각 분야의 진입 스킬이 `discipline_entrypoints`에 등록됐다.
- [ ] 보류·백업·제거 후보가 기본 선택에서 제외됐다.
- [ ] 이 Map과 Registry의 상태·경로가 일치한다.

## 11. 콜드 스타트 검수

- [ ] 각 분야의 진입 스킬을 2분 안에 찾을 수 있다.
- [ ] 새 요청에서 필요한 최소 스킬만 선택할 수 있다.
- [ ] 분야 스킬에서 본책·실제 파일·검증으로 이동할 수 있다.
- [ ] 공용 스킬과 분야 스킬의 책임이 겹치지 않는다.
- [ ] 백업·보류 스킬은 기본 읽기에서 제외된다.
- [ ] 미검증 가설을 현행 강제 규칙처럼 사용하지 않는다.
- [ ] 마지막 사용·검토·학습 상태를 찾을 수 있다.
