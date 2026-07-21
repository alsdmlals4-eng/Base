---
name: simplifying-skill-bodies
description: Use when a SKILL.md or operating router has grown too large and must retain only always-needed routing and execution rules while moving conditional templates, examples, domain detail, and decision tables into linked references with verified progressive disclosure.
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
