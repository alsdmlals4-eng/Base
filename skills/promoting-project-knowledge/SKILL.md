---
name: promoting-project-knowledge
description: Use when a project produces a reusable rule, method, checklist, template, skill, or case that may belong in the shared Base repository.
---

# Promoting Project Knowledge

## Core principle

프로젝트의 구체 해답을 복사하지 말고, 반복 가능한 문제 해결 원리와 검증 방법만 공용화한다.

## Promotion gate

다음을 모두 만족해야 확정 규칙·method·skill로 승격한다.

- 특정 프로젝트 이름과 수치 없이 설명 가능
- 반복 실패를 예방하거나 품질을 안정적으로 높임
- 사용 조건과 사용하지 않을 조건이 명확함
- 실행 또는 판단 절차를 재현할 수 있음
- 실제 작업·테스트 근거가 있음
- 기존 Base 책임 문서와 중복·충돌을 검토함

검증 전 내용은 프로젝트의 `관찰`, `가설`, `확인 필요`, `보류`에 남긴다.

## Classify destination

| 내용 | 위치 |
|---|---|
| 모든 작업의 짧은 필수 규칙 | `AGENTS.md` 또는 공용 작업 규칙 |
| 반복 가능한 판단·설계법 | `docs/knowledge/methods/` |
| 조사·출처·근거 평가 | `docs/knowledge/research/` |
| 직접 실행하는 단계형 절차 | `skills/<name>/SKILL.md` |
| 분야별 역량·검수 지도 | `docs/knowledge/skills/` |
| 복사할 출력 양식 | `templates/` |
| 구체 문제·결정·결과 | `docs/knowledge/cases/` |

## Process

1. 프로젝트에서 발생한 문제, 해결, 결과를 기록한다.
2. 프로젝트 고유 이름·세계관·수치·경로·ID를 분리한다.
3. 공용 원칙과 프로젝트 전용 규칙을 각각 작성한다.
4. Base에서 같은 책임을 가진 현행 문서를 찾는다.
5. 기존 문서를 갱신할지 새 유형이 필요한지 판단한다.
6. 새 스킬이면 baseline 실패와 대표·변형·반례 시나리오를 만든다.
7. README, Documentation Map, 템플릿, 참조 링크를 함께 갱신한다.
8. Base 버전과 Changelog를 갱신한다.
9. 프로젝트 로컬 사본과 `BASE_RULES_VERSION.md`의 동기화 필요를 보고한다.

## Do not promote

- 프로젝트 전체 GDD와 현재 밸런스
- 고유 세계관·캐릭터·파일 경로
- 일회성 함수명·씬명·데이터 ID
- 검증되지 않은 가설
- 비공개 원문과 권한 없는 자료
- 외부 작품의 코드·아트·문구·UI 복제본

## Validation scenarios

1. 특정 카드 UI 사례는 프로젝트에 남기고, “상시 정보와 상세 정보를 분리하는 판단법”만 일반화한다.
2. 한 번 성공한 프롬프트는 case 또는 가설로 기록하고, 여러 작업에서 반복 검증한 뒤 skill로 승격한다.
3. 기존 method와 같은 내용이면 새 파일을 만들지 않고 현행 원본을 갱신한다.

Template: `templates/skills/PROJECT_SKILL_EXTENSION.md`
