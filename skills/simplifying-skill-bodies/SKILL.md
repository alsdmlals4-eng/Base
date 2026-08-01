---
name: simplifying-skill-bodies
description: Use when a SKILL.md or router needs verified progressive disclosure without losing required behavior, safety, examples, or discoverability.
---

# Simplifying Skill Bodies

## Core principle

본문 간소화는 정보를 지우는 작업이 아니라 **항상 필요한 실행 계약만 본문에 남기고 조건부 세부사항을 필요할 때 읽는 reference로 이동**하는 작업이다.

이 Skill은 SKILL.md와 실행 라우터의 점진적 공개만 책임진다. 죽은 자료 제거는 `pruning-stale-and-nonfunctional-material`, 사용 중인 구조의 재배치는 `refactoring-with-contract-preservation`, 일반 기획 문서의 편집·발행은 `managing-design-documents`로 넘긴다.

## Modes

`inventory` → `classify-always-vs-conditional` → `extract-references` → `rewrite-router` → `validate-disclosure`

## Keep in SKILL.md

목적·호출/비호출 조건, 권한 경계, 필수 입력, mode·작업 순서, 출력 계약, 중단·품질 게이트, 조건별 reference 주소만 둔다.

## Move to references

긴 예시, 템플릿 전문, 분야별 체크리스트, 상세 판정표, 드문 예외, 벤치마크·도메인 규칙, 반복 설명을 이동한다.

세부 분류와 검증 기준은 `references/progressive-disclosure-rules.md`를 필요할 때만 읽는다.

## Completeness-first rule

- 줄 수, 문자 수, 페이지 수, 파일 크기나 임의의 분량 상한을 완료 조건으로 사용하지 않는다.
- 본문과 reference의 총 내용에서 승인 결정·예외·검증·실패 조건이 보존돼야 한다.
- Reference 이동은 내용 삭제나 테스트 통과용 축약이 아니라 책임 분리와 한 단계 발견성을 위한 것이다.
- 짧아졌지만 필요한 판단을 찾기 어렵거나 내용이 빠지면 실패다. 길어도 책임과 경로가 명확하고 실행 가능하면 허용한다.

## Workflow

1. 각 문단이 매 호출의 행동을 바꾸는지 판정한다.
2. 항상 필요한 규칙과 조건부 지식을 분리한다.
3. 조건부 지식을 의미 있는 전문 reference로 묶고 본문에 읽는 조건과 경로를 남긴다.
4. 중복 문장을 한 계약으로 압축한다.
5. 대표·변형·예외 요청에서 필요한 reference가 실제로 발견되고 기능이 보존되는지 검사한다.

## Output contract

```md
## 간소화 전·후 본문 크기
## 본문에 유지한 필수 계약
## 이동한 reference와 호출 조건
## 삭제·통합한 중복
## 기능 보존표
## 발견성·깨진 링크·회귀 결과
```

## Quality gate

본문을 목차만 남긴 빈 라우터로 만들거나, 중요 안전 규칙을 reference 깊숙이 숨기거나, 여러 문서를 한 거대 reference로 합치거나, 이동한 파일을 본문에서 연결하지 않으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`

## Base v9.4 지시 분류와 Fixture 보존

Skill 본문을 정리할 때 문단을 `Always hard constraint / Conditional default / Judgment space / Fixture or example / Historical / Duplicate`로 분류한다. 강한 안전 규칙을 단순화 명목으로 숨기지 않고, 판단 가능한 표현·배치·비파괴 초안은 불필요한 강제 규칙으로 고정하지 않는다.

Example은 삭제 대상이 아니라 정상·실패·경계·회귀를 검출하는 Fixture다. 예시를 이동·축약할 때 그 행동을 Golden Set·Test·Reference가 계속 검증하는지 비교한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.
