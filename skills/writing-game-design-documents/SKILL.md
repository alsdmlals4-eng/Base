---
name: writing-game-design-documents
description: Use when creating, restructuring, reviewing, updating, or handing off game design documents, roadmaps, system specifications, presentation plans, project skill extensions, or documentation maps.
---

# Writing Game Design Documents

## Core principle

좋은 기획서는 정보량이 아니라 **질문별 책임 원본, 실행 가능한 결정, 관찰 가능한 검증, 새 작업자의 재개 가능성**으로 평가한다.

기획서만 읽어도 프로젝트 방향, 핵심 플레이어 경험, 범위와 금지 방향을 이해할 수 있어야 한다. 세부 데이터·파일·테스트는 명시된 책임 원본으로 연결한다.

## Continuity contract

새 채팅, 새 AI, 새 작업자가 과거 대화 없이 작업을 이어갈 수 있도록 다음 원본을 항상 최신화한다.

- 기획서: 방향, 핵심 경험, 승인·미확정 사항, 범위와 금지 방향
- Roadmap: 현재 단계, 우선순위, 선행 조건, 다음 작업, 종료 기준과 검증
- Project skill extension: Base skill을 실제 경로·데이터·검증에 연결
- Active Context·Handoff: 현재 상태와 읽기 순서
- Documentation Map: 질문별 현행 책임 원본

방향, 수치, 용어, 범위, 구현 상태, 우선순위 또는 작업 절차가 바뀌면 같은 작업 안에서 관련 원본을 갱신한다.

## Document router

| 질문 | 책임 문서 |
|---|---|
| 왜 이 게임을 만드는가 | 프로젝트 비전·방향서 |
| 플레이어가 무엇을 반복하는가 | 전체 GDD·핵심 루프 |
| 한 시스템이 어떻게 작동하는가 | 시스템 기획서 |
| 한 기능을 무엇까지 구현하는가 | 기능 명세·Issue |
| 장면·대사·콘텐츠가 어떻게 흐르는가 | 콘텐츠·내러티브 기획서 |
| 화면·카메라·사운드가 무엇을 전달하는가 | UI·UX·연출 기획서 |
| 어떤 데이터를 누가 소유하는가 | 데이터 설계서 |
| 어떤 순서로 진행하는가 | Roadmap |
| 현재 무엇이 사실인가 | Active Context·Handoff |
| 반복 작업을 어떤 절차로 수행하는가 | Base skill·Project skill extension |
| 완료를 어떻게 판단하는가 | 테스트·QA 명세 |
| 왜 이 결정을 했는가 | Decision Record |
| 다음 작업자는 무엇을 먼저 읽는가 | Documentation Map·Handoff |

## Process

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. Base 공용 method·skill·template과 프로젝트 현행 문서를 함께 확인한다.
3. 기존 Documentation Map을 확인하고 새 문서가 필요한지 판단한다.
4. 한 질문에 현행 책임 원본 하나만 지정한다.
5. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.
6. 각 기획을 목적→경험→규칙→흐름→예외→검증 순서로 작성한다.
7. 실제 파일·데이터·Issue와 연결하되 전문을 중복 복사하지 않는다.
8. 포함·제외 범위, 위험, 완료 기준을 명시한다.
9. Roadmap에 현재 단계, 선행 조건, 다음 작업, 종료 기준과 검증을 연결한다.
10. Base skill과 Project extension을 실제 경로·데이터·검증에 연결한다.
11. 새 작업자가 3~6개 시작 문서에서 모든 책임 원본으로 이동할 수 있는 읽기 순서를 만든다.
12. 파일 생성·통합·이동·삭제 시 Documentation Map, README와 참조를 갱신한다.
13. 작업 종료·인수인계에서 프로젝트 전용 결과와 Base 공용 학습 데이터를 분리하고 case를 기록한다.
14. 콜드 스타트 질문을 10분 안에 답할 수 있는지 확인한다.

## Base and project split

### Base — [학습형] [공용]

- 작성 방법, 문서 종류, 검수 기준, 템플릿
- 여러 프로젝트에서 반복 검증된 일반 원칙
- 성공·실패·미검증 사례와 지식 상태

### Project — [전용] [분화·적용·검증]

- 실제 비전, 세계관, 시스템, 수치, 콘텐츠
- 현재 파일 경로, 상태, Roadmap, 테스트 결과
- Base 규칙을 구체화한 전용 문서와 skill extension
- 공용화 전 관찰·가설·실험 결과

## Output contract

```md
## 프로젝트 방향과 플레이어 경험
## 책임 문서 지도
## 문서별 승인·구현·검증 상태
## Roadmap 연결
## Base skill·Project extension 연결
## 실제 파일·데이터·테스트 참조
## 최초 읽기 순서
## 콜드 스타트 검수
## 프로젝트 전용 최신화
## Base 공용 학습 데이터·case
```

## Failure conditions

- 한 문서가 상태·계획·Roadmap·QA를 모두 소유
- 같은 규칙을 여러 문서에 장문 복사
- `final`, `latest`, `v2` 활성 복제본 생성
- 문서 존재를 구현 완료로 판단
- 플레이어 경험과 제외 범위가 없음
- 구현자가 찾을 실제 경로와 검증 방법이 없음
- Issue만 최신이고 기획서·Roadmap·Handoff는 오래된 상태
- Base skill과 프로젝트 실제 경로·검증이 연결되지 않음
- 새 작업자가 과거 대화 없이는 방향과 다음 작업을 알 수 없음

## Validation scenarios

1. 새 프로젝트는 비전, 전체 기획, 분야별 원본, Roadmap, Handoff, skill extension, QA의 책임을 분리한다.
2. 기존 문서가 중복되면 최신 기준을 하나로 통합하고 참조 확인 후 구버전을 제거한다.
3. 작은 기능은 새 GDD를 만들지 않고 기존 시스템 문서, Roadmap 상태와 Issue에 차이만 기록한다.
4. 방향 변경은 기획서뿐 아니라 Roadmap, Handoff, Documentation Map과 관련 skill extension까지 갱신한다.
5. 새 작업자는 10분 안에 핵심 경험, 현재 단계, 다음 작업, 책임 원본과 검증 방법을 찾는다.

Template: `templates/planning/DESIGN_DOCUMENT_SYSTEM.md`
