# [프로젝트명] 시작 지점

> 사용자, 새 GPT, 새 Codex와 새 작업자가 프로젝트 전체 상태를 가장 먼저 확인하는 대시보드다. 세부 기획은 문서별 Markdown 또는 JSON 책임 원본을, 사람 열람은 최신 PDF를, 구현 상태는 실제 파일과 테스트를 따른다.

- 공식 위치: 저장소 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
- 기획서 Registry: `DESIGN_DOCUMENT_REGISTRY.json`
- 스킬 Registry: `SKILL_REGISTRY.json`
- 사람용 스킬맵: 필수 `PROJECT_SKILL_MAP.pdf`, 선택 `PROJECT_SKILL_MAP.md`·`PROJECT_SKILL_MAP.docx`

## 한눈에 보기

| 항목 | 현재 기준 |
|---|---|
| 한 줄 약속 |  |
| 대상 플레이어 |  |
| 장르·플랫폼 |  |
| 엔진·핵심 기술 |  |
| 현재 제품 단계 |  |
| 현재 작업 게이트 |  |
| 다음 Greenlight |  |
| 최우선 작업 |  |
| 가장 큰 위험 |  |
| 마지막 검토일 |  |
| 기준 Git 커밋 |  |
| Base 기준 커밋 |  |
| 최근 운영체계 Health Review |  |

## 현재 상태

| 구분 | 요약 | Markdown/JSON 책임 원본·실제 증거 |
|---|---|---|
| 확정 |  |  |
| 구현 |  |  |
| 검증 |  |  |
| 진행 중 |  |  |
| 미확정·확인 필요 |  |  |
| 보류 |  |  |
| 불일치 |  |  |

## 핵심 플레이어 경험

- 플레이어가 반복해서 보는 것:
- 반복해서 판단하는 것:
- 반복해서 행동하는 것:
- 행동 직후 받아야 하는 피드백:
- 지켜야 할 감정·약속:
- 금지 방향:

프로젝트 전체의 상세 방향은 `DESIGN_DOCUMENT_REGISTRY.json`에서 프로젝트 종합 책임 원본과 최신 PDF를 찾는다.

## 현재 개발 단계와 게이트

| 구분 | 현재 상태 | 진입 조건 | 종료 기준 | 증거 | 책임 원본 |
|---|---|---|---|---|---|
| 작업 실행 게이트 |  |  |  |  | `DEVELOPMENT_GATES.md` |
| 제품 마일스톤 |  |  |  |  | `DEVELOPMENT_GATES.md`·Roadmap |

```text
작업: Intake·Context → Ready → Approval → Implementation → Verification → Documentation → Completion
제품: Concept → Prototype → Graybox → First Playable → Vertical Slice → Production → Alpha → Beta → Release Candidate
```

## 분야별 활성 기획서

| 분야·책임 범위 | Markdown/JSON 책임 원본 | 선택 DOCX | 최신 PDF | 선택 자산·다이어그램 | 발행 Manifest | 상태 | 현재 핵심 과제 |
|---|---|---|---|---|---|---|---|
| 프로젝트 전체 |  |  |  |  |  |  |  |
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

작은 프로젝트에서 여러 책임을 한 JSON에 통합하면 `DESIGN_DOCUMENT_REGISTRY.json`의 `responsibility_coverage`에 담당 범위를 모두 기록한다.

## 기획서 읽기 규칙

```text
AI·자동 검사
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 Markdown 또는 JSON 책임 원본

사람
→ 현재 분야 기획서 PDF
→ 필요 시 DOCX·다이어그램·승인 이미지
```

서술 중심 기획은 Registry에 등록한 Markdown을 사용할 수 있다. 같은 서술을 JSON과 중복 책임 원본으로 만들지 않는다.

## 최신 시각 자료

| Asset ID | 항목 | 상태 | 캐노니컬 이미지 | 실제 게임 캡처 | 포함 기획서 | 차이·다음 작업 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

콘셉트 이미지와 실제 구현 캡처를 같은 상태로 취급하지 않는다. 세부 상태는 Visual Source와 Asset Manifest, 각 책임 원본의 승인 이미지 메타데이터를 따른다.

## 프로젝트 스킬 시작 경로

- AI용 Registry: `SKILL_REGISTRY.json`
- 사람용 최신본: `PROJECT_SKILL_MAP.pdf`
- 선택 문서 검토본: `PROJECT_SKILL_MAP.md` 또는 `PROJECT_SKILL_MAP.docx`
- 다이어그램: `PROJECT_SKILL_MAP.assets/`
- 발행 Manifest: `SKILL_MAP_PUBLICATION_MANIFEST.json`
- 요청 라우팅 스킬: `routing-project-work-by-discipline`
- 현재 작업의 주 책임 분야 스킬:
- 필요한 Foundation 스킬:
- 후속 단계에서만 호출할 스킬:
- Learning Log:

전체 skills 폴더를 읽지 않고 현재 작업에 필요한 최소 스킬만 선택한다. 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과는 Learning Log에 남긴다.

## 새 작업자의 읽기 순서

```text
프로젝트 AGENTS.md
→ 이 START_HERE.md
→ ACTIVE_CONTEXT.md·HANDOFF.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 Markdown 또는 JSON 책임 원본
→ SKILL_REGISTRY.json
→ 필요한 Foundation·분야 스킬
→ 사람 검토 시 기획서 PDF·DOCX·자산
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 필요한 Base Method·Skill
```

## 지금 하지 말아야 할 것

- 보류 영역을 재개 승인 없이 구현하지 않는다.
- 기존 승인 이미지가 있는 항목의 새 시안을 별도 지시 없이 만들지 않는다.
- JSON·DOCX·PDF 존재를 구현·검증 완료로 표시하지 않는다.
- DOCX·PDF를 독립 책임 원본으로 수동 수정하지 않는다.
- Markdown·JSON 기획 본책을 Registry 밖에 새로 만들지 않는다.
- 범위 밖 리팩터링과 기능 확장을 현재 작업에 섞지 않는다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 백업·보류·제거 후보를 기본 컨텍스트에 포함하지 않는다.
- 전체 skills 폴더를 기본 로드하지 않는다.
- 사용자 승인 전 기존 프로젝트의 파일을 대량 삭제·이동·통합하지 않는다.

## 다음 작업

| 우선순위 | 작업 | 주 책임 | 영향 분야 | 선행 조건·Ready | 완료 기준 | 검증 | 관련 JSON·스킬 |
|---:|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |

## 최근 결정과 변경

- 최근 결정: `DECISION_LOG.md`
- 최근 변경: `CHANGELOG.md`
- 현재 단계·게이트: `DEVELOPMENT_GATES.md`
- 기획서 Registry: `DESIGN_DOCUMENT_REGISTRY.json`
- 스킬 Registry: `SKILL_REGISTRY.json`
- 사람용 스킬맵: `PROJECT_SKILL_MAP.pdf`
- 기획서 발행 상태: 각 `_PUBLICATION_MANIFEST.json`
- 운영체계 Health Review: 통합검수 보고서

## 수명주기 영역

- 현행:
- 백업 위치·보존 이유:
- 보류 위치·재개 조건:
- 제거 후보·승인 상태:

## 콜드 스타트 확인

새 작업자는 10분 안에 다음을 답할 수 있어야 한다.

- 게임의 핵심 약속은 무엇인가?
- 현재 구현·검증 상태는 무엇인가?
- 현재 단계와 다음 게이트는 무엇인가?
- 무엇을 변경하면 안 되는가?
- 프로젝트 전체와 각 분야의 등록된 Markdown 또는 JSON 책임 원본은 어디인가?
- 사람이 볼 최신 DOCX/PDF와 승인 이미지는 어디인가?
- 각 분야의 진입 스킬과 검증 방법은 무엇인가?
- 보류·확인 필요·미검증은 어디인가?
- 실제 코드·데이터·테스트는 어디인가?

답하지 못하면 이 문서 또는 연결된 Registry·JSON·실제 증거를 갱신한다.
