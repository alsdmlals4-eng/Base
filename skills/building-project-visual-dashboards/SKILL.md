---
name: building-project-visual-dashboards
description: Use when project concepts, loops, system relationships, MVP status, UX flows, evidence, risks, or next work need an editable visual dashboard while canonical decisions remain in registered GitHub documents and data sources.
---

# Building Project Visual Dashboards

## Core principle

대시보드는 복잡한 관계를 보고 토론하는 작업 공간이다. 확정 결정과 구현 상태의 정본을 대체하지 않으며, 원본 경로·갱신 시점·상태를 명시한다.

이 Skill은 시각화와 탐색 인터페이스를 책임진다. 기획 책임 원본의 작성·발행은 `managing-design-documents`, 수치 분석의 정확성은 해당 데이터 분석 계약, 대시보드가 주장하는 구현 상태는 `reviewing-and-validating-project-changes`의 증거로 확인한다.

## Modes

`frame` → `map-sources` → `build` → `bind-status` → `validate`

## Default form

특별한 요구가 없으면 단일 HTML + CSS + 최소 JavaScript로 만들고 PC 가독성, 의미 있는 카드·표·화살표·상태 배지, 수정 위치 주석을 우선한다.

정보 구조·검수표는 `references/dashboard-information-architecture.md`를 필요할 때만 읽는다.

## Output contract

```md
## 대시보드 목적·독자·결정
## 탭·흐름·데이터 원본
## 편집·미리보기 동작
## 상태·위험·누락 표시
## 생성 파일과 실행 방법
## 정본 동기화·검증·미확인
```

## Quality gate

예쁜 장식보다 정보 위계와 행동을 우선하고, 수동 복사된 오래된 상태를 최신으로 표시하지 않으며, 모바일·접근성·보안 요구가 있으면 별도 검증한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
