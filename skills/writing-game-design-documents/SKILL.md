---
name: writing-game-design-documents
description: Use when creating, restructuring, reviewing, updating, or handing off game design responsibility structures, schema v3 Markdown or JSON sources, roadmaps, specifications, or documentation maps.
---

# Writing Structured Game Design Documents

## Core principle

좋은 기획서는 정보량이 아니라 **질문별 책임 원본, 실행 가능한 결정, 관찰 가능한 검증, 사람 가독성, 새 작업자의 재개 가능성**으로 평가한다.

서술 중심 프로젝트·분야 본책은 Markdown을 기본으로 하고, 구조 검증이 필요한 상태·ID·관계·게임 데이터는 JSON을 사용한다. Registry에 문서별 단일 책임 원본을 선언하며 사람은 항상 동기화된 PDF와 필요한 선택 파생본을 본다.

## Responsibility contract

```text
AI·자동 검사 → DESIGN_DOCUMENT_REGISTRY.json·문서별 Markdown 또는 JSON 책임 원본
사람 기본 열람 → 기획서 PDF
사람 Word 검토 → 선택 기획서 DOCX
시각 자료 → 필요한 경우의 기획서.assets/
최신성 → 기획서_PUBLICATION_MANIFEST.json
현재 상태 → ACTIVE_CONTEXT.md
작업 순서 → Roadmap·Issue·Plan
반복 절차 → Project Skill
```

서술 중심 기획은 Registry에 등록한 Markdown을 기본 책임 원본으로 사용할 수 있다. 같은 서술을 JSON과 중복 책임 원본으로 두지 않는다.

## Continuity contract

항상 최신화:

- Design Document Registry: 문서 ID·책임 범위·source format/path·필수 PDF·Manifest·선택 DOCX/자산 경로
- 기획 책임 원본: 서술 중심 Markdown 또는 구조 검증·게임 데이터 JSON
- 사람용 발행본: 필수 PDF와 선언한 선택 DOCX·다이어그램·승인 이미지
- Roadmap: 현재 단계·우선순위·선행 조건·다음 작업·종료 기준
- Skill Registry·Project Skill: 실제 경로·데이터·검증 연결
- Active Context·Handoff: 현재 상태와 읽기 순서
- Documentation Map: 질문별 현행 책임 원본

방향, 수치, 용어, 범위, 구현 상태, 우선순위 또는 절차가 바뀌면 같은 작업에서 관련 책임 원본·PDF·Manifest·상태 문서를 갱신한다.

## Document router

| 질문 | 책임 원본 |
|---|---|
| 왜 이 게임을 만드는가? | 프로젝트 종합 기획 책임 원본 |
| 플레이어가 무엇을 반복하는가? | 등록된 게임 디자인 책임 원본 |
| 한 시스템이 어떻게 작동하는가? | 책임 분야 원본의 상세 Section·실제 데이터 |
| 한 기능을 무엇까지 구현하는가? | 등록된 승인 범위·작업 계약·Plan |
| 장면·대사·콘텐츠가 어떻게 흐르는가? | 등록된 설정·내러티브 책임 원본 |
| 화면·카메라·사운드가 무엇을 전달하는가? | 등록된 UX·아트·사운드 책임 원본 |
| 어떤 데이터를 누가 소유하는가? | 개발 책임 원본·스키마·코드 |
| 어떤 순서로 진행하는가? | Roadmap·Development Gates |
| 현재 무엇이 사실인가? | Active Context·실제 파일·테스트 |
| 반복 작업을 어떤 절차로 수행하는가? | Skill Registry·Project Skill |
| 완료를 어떻게 판단하는가? | QA 책임 원본·테스트 증거 |
| 왜 이 결정을 했는가? | Decision Log·기획 책임 원본의 결정 섹션 |
| 사람이 무엇을 읽는가? | 각 PDF와 선언한 선택 DOCX·assets |

## Process

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. Base Method·Skill과 프로젝트 Registry·현재 책임 원본·실제 파일을 확인한다.
3. Design Document Registry에서 기존 책임 원본을 확인한다.
4. 한 질문에 현행 단일 책임 원본 하나만 지정하고 `source_format`을 선언한다.
5. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.
6. `목적 → 경험 → 규칙 → 흐름 → 예외 → 검증` 순서로 선택한 Markdown 또는 JSON 책임 원본을 작성한다.
7. 세부 데이터·코드·자산·테스트 경로를 연결하고 전문을 복제하지 않는다.
8. 책임 범위, 포함·제외, 위험, Ready·Done을 명시한다.
9. 승인 이미지·실제 캡처는 Asset ID·상태·채택 범위와 함께 등록한다.
10. Registry 항목을 갱신한다.
11. `build_design_documents.py`로 PDF·Manifest와 선언한 선택 DOCX·다이어그램을 생성한다.
12. PDF 전 페이지와 승인 이미지·표·한글을 시각 검수한다.
13. Roadmap·Skill·Active Context·Documentation Map을 갱신한다.
14. 새 AI가 10분 안에 모든 책임 원본과 다음 작업을 찾는지 확인한다.

## Structured JSON minimum contract

- document ID·kind·title·discipline·owner·status
- 목적·플레이어 가치·현재 목표·요약
- 목표·Quality Bar·금지 방향
- 책임·비책임·분야 간 계약
- 전체 작업 과정
- 작업·제품 게이트
- Foundation·분야 Skill·Learning Log
- 확정·구현·검증·확인 필요·보류
- 결정·구현 경로·검증 증거
- 상세 Sections
- 승인 이미지·실제 캡처
- 위험·다음 작업·Ready·Done
- 부록·변경·학습 이력

## Base and project split

### Base — 공용

- Markdown/JSON 계약·작성 방법·검수 기준·생성기·템플릿
- 여러 프로젝트에서 반복 검증된 일반 원리
- 성공·실패·미검증 사례와 회귀 테스트

### Project — 전용

- 실제 비전·세계관·시스템·수치·콘텐츠
- 실제 경로·구현·검증·Roadmap
- 승인 이미지·프롬프트·PDF·선택 DOCX
- Project Skill과 관찰·가설

## Output contract

```md
## 구조화 기획서 작업 결과
- Design Document Registry 변경:
- 프로젝트·분야 source format/path:
- 책임 범위:
- 사람용 PDF·선택 DOCX:
- 다이어그램·승인 이미지:
- Publication Manifest:
- Roadmap·게이트 연결:
- Skill Registry·Project Skill 연결:
- 실제 파일·데이터·테스트:
- 콜드 스타트 검수:
- 미검증·보류·제거 후보:
```

## Failure conditions

- 한 책임 원본이 선택하지 않은 모든 분야의 세부 상태·Roadmap·QA를 무차별 소유
- 같은 규칙을 여러 책임 원본에 장문 복사
- `final`, `latest`, `v2` 활성 복제본 생성
- DOCX·PDF를 독립 책임 원본으로 수정
- Registry에 등록되지 않은 Markdown 기획 본책 생성
- 문서 존재를 구현 완료로 판단
- 플레이어 경험·제외 범위·검증 없음
- 실제 경로와 테스트가 없음
- 책임 원본은 최신인데 PDF·Manifest·선택 파생본이 오래됨
- 작업 계약만 최신이고 책임 원본·Roadmap·Handoff가 오래됨
- 새 작업자가 과거 대화 없이는 방향과 다음 작업을 알 수 없음

## Validation scenarios

1. 신규 프로젝트는 프로젝트 전체와 선택한 분야별 책임 원본의 형식·경로를 Registry에 등록한다.
2. 기존 문서는 안전 감사 후 고유 정보를 역할에 맞는 Markdown 또는 JSON에 승계하고 발행 검증 전 원본을 제거하지 않는다.
3. 작은 기능은 새 본책을 만들지 않고 기존 책임 원본 Section·작업 계약·Roadmap에 차이를 기록한다.
4. 방향 변경은 책임 원본·PDF/Manifest·Roadmap·Handoff·관련 Skill을 함께 갱신한다.
5. 새 작업자는 PDF로 전체 방향을 읽고 등록된 책임 원본·실제 파일로 세부 근거를 확인한다.
