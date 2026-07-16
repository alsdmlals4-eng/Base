---
name: writing-game-design-documents
description: Use when creating, restructuring, reviewing, or handing off game design documents, roadmaps, system specifications, presentation plans, or project documentation maps.
---

# Writing Game Design Documents

## Core principle

좋은 기획서는 정보량이 아니라 **질문별 책임 원본, 실행 가능한 결정, 관찰 가능한 검증**으로 평가한다.

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
| 어떤 순서로 진행하는가 | 로드맵 |
| 현재 무엇이 사실인가 | 상태·Handoff 문서 |
| 완료를 어떻게 판단하는가 | 테스트·QA 명세 |
| 왜 이 결정을 했는가 | Decision Record |

## Process

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. 기존 문서 지도를 확인하고 새 문서가 필요한지 판단한다.
3. 한 질문에 현행 책임 원본 하나만 지정한다.
4. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.
5. 각 기획을 목적→경험→규칙→흐름→예외→검증 순서로 작성한다.
6. 실제 파일·데이터·Issue와 연결하되 전문을 중복 복사하지 않는다.
7. 포함·제외 범위, 위험, 완료 기준을 명시한다.
8. 다른 작업자가 3~6개 문서만 읽고 시작할 수 있는 읽기 순서를 만든다.
9. 파일 생성·통합·이동·삭제 시 Documentation Map과 참조를 갱신한다.

## Base and project split

Base:

- 작성 방법, 문서 종류, 검수 기준, 템플릿
- 여러 프로젝트에서 검증된 일반 원칙

Project:

- 실제 비전, 세계관, 시스템, 수치, 콘텐츠
- 현재 파일 경로, 상태, 로드맵, 테스트 결과
- Base 규칙을 구체화한 전용 문서

## Failure conditions

- 한 문서가 상태·계획·로드맵·QA를 모두 소유
- 같은 규칙을 여러 문서에 장문 복사
- `final`, `latest`, `v2` 활성 복제본 생성
- 문서 존재를 구현 완료로 판단
- 플레이어 경험과 제외 범위가 없음
- 구현자가 찾을 실제 경로와 검증 방법이 없음

## Validation scenarios

1. 새 프로젝트는 비전, 전체 기획, 분야별 원본, 로드맵, Handoff, QA의 책임을 분리한다.
2. 기존 문서가 중복되면 최신 기준을 하나로 통합하고 참조 확인 후 구버전을 제거한다.
3. 작은 기능은 새 GDD를 만들지 않고 기존 시스템 문서와 Issue에 차이만 기록한다.

Template: `templates/planning/DESIGN_DOCUMENT_SYSTEM.md`
