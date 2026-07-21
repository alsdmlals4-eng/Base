---
name: creating-user-learning-notes
description: Use when completed project work, AI collaboration, tools, mistakes, or decisions should be converted into concise user-facing study notes that explain concepts, reasons, examples, misconceptions, practice steps, and reusable lessons rather than operational instructions for an AI.
---

# Creating User Learning Notes

## Core principle

학습 노트는 AI 지침을 복사하는 문서가 아니라 사용자가 **왜 이런 구조가 필요한지 이해하고 스스로 판단·적용**하도록 돕는 설명 자료다.

## Modes

`capture → explain → connect → practice → update`

## Required inputs

```yaml
learning_goal_and_reader_level:
completed_work_or_case:
key_decisions_and_reasons:
failures_misconceptions_and_evidence:
terms_tools_and_references:
practice_or_next_application:
```

## Output contract

```md
## 이번에 배울 핵심
## 개념과 쉬운 정의
## 왜 필요한가
## 실제 작업 흐름과 역할 구분
## 좋은 예·나쁜 예
## 자주 하는 오해와 수정
## 직접 해볼 연습
## 확인 질문과 다음 학습
## 근거·출처·미확인
```

## Rules

- 확정 사실, 경험적 교훈, 가설을 구분한다.
- 특정 프로젝트 사례와 공용 원리를 분리한다.
- 전문 용어는 첫 사용에서 정의한다.
- 결과만 나열하지 않고 원인→판단→결과를 연결한다.
- 긴 작업 로그와 내부 지침 전문을 학습 노트로 복제하지 않는다.

## Quality gate

독자가 원문 대화 없이 이해하고, 배운 원리를 새로운 작업에 적용하며, 무엇이 검증됐고 무엇이 가설인지 구분할 수 있어야 한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
