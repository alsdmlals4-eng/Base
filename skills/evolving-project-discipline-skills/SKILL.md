---
name: evolving-project-discipline-skills
description: Use when creating, reviewing, consolidating, or improving project Foundation and discipline skills from actual work and validation evidence while keeping the Registry, entrypoints, tests, references, and human derivatives synchronized.
---

# Evolving Project Discipline Skills

## Core principle

**Consolidation-first**: 새 Skill을 만들기 전에 기존 Skill mode·reference 확장으로 해결 가능한지 확인한다. 독립 입력·산출물·품질 기준·도구·승인 경계가 있을 때만 분리한다.

가지치기 자체는 `pruning-stale-and-nonfunctional-material`, 본문 압축은 `simplifying-skill-bodies`, 기능 보존 구조 변경은 `refactoring-with-contract-preservation`이 책임진다.

## Skill Modes

`inventory → decide-boundary → create-or-integrate → register → verify → learn`

## Required inputs

```yaml
skill_registry_and_entrypoints:
existing_skills_references_scripts:
legacy_aliases:
learning_and_failure_evidence:
actual_work_examples:
validation_and_publication_paths:
```

## Boundary decision

1. 기존 통합 Skill의 mode로 처리 가능한가?
2. trigger·mode·reference 확장으로 해결 가능한가?
3. 독립 입력·산출물·Quality Bar·검증·승인 경계가 있는가?
4. 여러 작업에서 반복될 책임인가?

세부 인벤토리·통합 전 보존표·Health Review는 `references/consolidation-and-health-review.md`를 필요할 때만 읽는다.

## Workflow

1. Registry·실제 패키지·entrypoint·Learning Log를 대조한다.
2. 중복, 과분할, 누락, 죽은 자료, 과도한 기본 로드를 판정한다.
3. 고유 기능·입력·산출물·검증을 먼저 보존한다.
4. Skill·mode·reference 중 가장 작은 책임 단위로 생성 또는 통합한다.
5. `load_by_default=false`, trigger, use/do-not-use, Learning Log를 등록한다.
6. `auditing-canonical-reference-freshness`와 `managing-game-project-operating-system` verify를 실행한다.

## Output contract

```md
## 통합 전·후 구조와 활성 Skill 수
## 유지·추가·통합·제거한 책임과 이유
## 고유 기능 보존표
## Registry·entrypoint·alias·reference·test 동기화
## 선택적 호출·콜드 스타트·Health Review
## 검증·미검증·Learning Log·다음 trigger
```

## Quality gate

- 기존 mode 검토 없이 새 Skill을 추가하지 않는다.
- 이름만 합치며 기능·검증·승인 경계를 잃지 않는다.
- `LEGACY_SKILL_ALIASES.md`와 오래된 참조를 처리한다.
- 전체 skills 폴더를 기본 로드하지 않는다.
- 실제 결과 없이 지식 상태를 승격하지 않는다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
