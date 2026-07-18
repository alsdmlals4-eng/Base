# [프로젝트명] Documentation Map

- 책임: 프로젝트 허브·통합검수
- 공식 위치: 저장소 루트 `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- 마지막 검토일:
- 기준 커밋:
- Base 기준 커밋:

> 모든 파일을 무작정 읽지 않는다. 질문·작업 유형에 맞는 현행 책임 원본, 최소 foundation 스킬, 주 책임 분야 스킬과 실제 검증 경로만 선택한다.

`[기획서]`는 저장소 루트 바로 아래에 둔다. 중첩 기획서 폴더를 별도 현행 책임 원본으로 만들지 않는다.

## 1. 기본 읽기 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 적용 Base 기준
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md·HANDOFF.md
→ 이 DOCUMENTATION_MAP.md
→ 관련 분야 본책
→ SKILL_REGISTRY.json
→ PROJECT_SKILL_MAP.md의 필요한 foundation + 주 책임 분야 스킬
→ DEVELOPMENT_GATES.md
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
```

기본 제외: `[백업]`, `[보류]`, `[제거 후보]`, archive, hold, deprecated.

## 2. 프로젝트 허브 책임

| 질문 | 현행 책임 원본 | 보조·증거 | 상태 | 갱신 트리거 |
|---|---|---|---|---|
| 프로젝트를 어디서 시작하는가? |  |  |  | 시작 경로 변경 |
| 루트 기획서 위치는 어디인가? | `[기획서]/` |  |  | 기획서 루트·경로 변경 |
| 현재 무엇이 사실인가? |  |  |  | 구현·검증·우선순위 변경 |
| 왜 이 프로젝트를 만드는가? |  |  |  | 방향·대상 플레이어 변경 |
| 다음 개발 게이트는 무엇인가? |  |  |  | 게이트 판정 변경 |
| 어떤 문서가 무엇을 책임하는가? |  |  |  | 생성·이동·통합·삭제 |
| 현재 요청에 어떤 스킬을 사용하는가? | `SKILL_REGISTRY.json` | `PROJECT_SKILL_MAP.md` |  | 스킬 추가·통합·검증·trigger 변경 |
| 스킬이 무엇을 학습했는가? | 각 스킬 Learning Log |  |  | 모든 의미 있는 스킬 호출 |
| 왜 이 결정을 했는가? |  |  |  | 주요 결정 변경 |
| 최근 무엇이 바뀌었는가? |  |  |  | Base·프로젝트 변경 |
| 승인 이미지와 자산은 어디인가? |  |  |  | 승인·교체·이전 |
| 최신 PDF는 어디인가? |  |  |  | 본책·승인 이미지 변경 |
| 운영체계가 실제로 정상인가? | 통합검수 Health Review | Governance Workflow |  | 설치·마이그레이션·주요 게이트·실패 |

## 3. 분야별 책임·스킬·검증

| 분야 | 활성 본책 | Registry 진입 ID | 진입 스킬 | 실제 파일·자산 | 테스트·검증 | Learning Log | PDF | 상태 |
|---|---|---|---|---|---|---|---|---|
| 설정·내러티브 |  |  |  |  |  |  |  |  |
| 게임 디자인 |  |  |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |  |  |
| 개발·엔지니어링 |  |  |  |  |  |  |  |  |
| 테크니컬 아트·파이프라인 |  |  |  |  |  |  |  |  |
| 아트 |  |  |  |  |  |  |  |  |
| 사운드 |  |  |  |  |  |  |  |  |
| QA |  |  |  |  |  |  |  |  |
| 프로덕션·PM |  |  |  |  |  |  |  |  |
| 분석·유저리서치 |  |  |  |  |  |  |  |  |
| 통합검수 |  |  |  |  |  |  |  |  |

## 4. 작업 유형별 최소 읽기

| 작업 | 필수 현행 원본 | Foundation 스킬 | 분야 스킬 | 후속 호출 | 실제 검증 |
|---|---|---|---|---|---|
| 새 요청·분야 판정 | START_HERE·Active Context·Registry | routing-project-work-by-discipline | 주 책임 분야 진입 스킬 | 필요 시 요구 구체화 | 라우팅 재현성 |
| 방향·핵심 경험 변경 |  |  |  | Handoff·PDF |  |
| 시스템·수치 변경 |  |  |  | QA·통합검수 |  |
| UI·UX 변경 |  |  |  | 시각 QA·PDF |  |
| 코드·데이터·저장 변경 |  |  |  | QA·Handoff |  |
| 이미지·자산·VFX 변경 |  |  |  | PDF·시각 검수 |  |
| 사운드 변경 |  |  |  | 오디오 QA·PDF |  |
| 일정·범위·예산 상태 변경 |  |  |  | Handoff |  |
| PDF 발행 |  | publishing-discipline-bibles | 해당 분야 | 통합검수 | PDF·Manifest·시각 검수 |
| Active Context·Handoff |  | maintaining-project-context-and-handoff | 영향 분야 | 콜드 스타트 | 상태·경로 검수 |
| 분야 스킬 생성·갱신 | 본책·실제 작업·검증 | evolving-project-discipline-skills | 해당 분야 | Health Review | Registry·Log·선택적 호출 |
| 기존 구조 마이그레이션 |  | migrating-existing-game-project-structure | 영향 분야 | verifying-game-project-operating-system | 보존 대조·링크·콜드 스타트 |
| 운영체계 Health Review | 전체 활성 원본·검사 결과 | verifying-game-project-operating-system | 통합검수 | 수정 스킬만 호출 | 구조·Registry·PDF·Workflow |
| 릴리스 준비 검수 |  | development-gate-review | QA·통합검수 | Health Review | 회귀·성능·Release Candidate |

## 5. 상태와 수명주기

| 구분 | 위치 | 기본 읽기 | 사용 조건 | 책임 문서 |
|---|---|---|---|---|
| 현행 |  | 포함 | 현재 작업 관련 |  |
| 백업 |  | 제외 | 감사·출처·사용자 요청 |  |
| 보류 |  | 제외 | 재개 승인·조건 충족 |  |
| 제거 후보 |  | 제외 | 삭제 검수·승인 |  |

## 6. 스킬 Registry·학습

| 항목 | 책임 원본 | 갱신 조건 | 검증 |
|---|---|---|---|
| 스킬 경로·상태·trigger | `SKILL_REGISTRY.json` | 추가·이동·통합·상태 변경 | JSON·경로·중복 ID |
| 사람용 책임·관계 | `PROJECT_SKILL_MAP.md` | 분야·관계·설명 변경 | Registry와 대조 |
| 실행 결과·실패·예외 | 각 Learning Log | 모든 의미 있는 호출 | 누락·지식 상태·다음 트리거 |
| 스킬 계약 | 각 `SKILL.md` | 반복 실패·새 예외·경로·검증 변경 | Ready·Done·회귀 테스트 |

## 7. 파생본·Manifest

| 분야 | 책임 Markdown | 출력 PDF | Publication Manifest | 승인 이미지 Manifest | 최신 상태 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

PDF는 읽기 전용 파생본이며 Markdown 책임 원본과 승인 이미지에서 생성한다.

## 8. 콜드 스타트 검수

새 AI가 10분 안에 다음을 찾을 수 있어야 한다.

- 저장소 루트 `[기획서]`
- 프로젝트 목적과 핵심 경험
- 현재 구현·검증 상태
- 다음 작업·선행 조건·게이트
- 금지·보호 범위
- 분야별 본책·Registry 진입 스킬
- 현재 요청에 필요한 최소 스킬
- 실제 코드·데이터·자산·테스트
- 승인 이미지와 최신 PDF
- 보류·확인 필요·미검증
- 작업 종료 갱신 대상과 Learning Log

답하지 못한 질문은 이 지도 또는 연결된 책임 원본·Registry를 보강한다.
