# 분야별 프로젝트 스킬 학습·진화 방법

- 상태: 공용 원칙·호환 경로
- 실행 Skill: `skills/evolving-project-discipline-skills/SKILL.md`
- 채택 기준: `docs/AI_SKILL_ADOPTION_GUIDE.md`

이 문서는 Skill 학습·통합의 불변 원칙만 책임진다. Inventory, Registry 갱신, 사람용 Skill Map 생성과 Health Review의 단계형 절차는 실행 Skill이 책임진다.

## 핵심 원칙

Skill은 조언 모음이 아니라 다음을 고정하는 반복 실행 계약이다.

```text
사용 조건
→ 비사용 조건
→ 필수 입력
→ 책임 원본
→ mode·절차
→ 산출물
→ 완료·검증
→ 실패·학습
```

공용 절차는 Foundation에 한 번만 두고, 분야 Skill은 해당 분야의 고유 판단·경로·산출물·검증만 책임진다.

## 통합 우선 규칙

새 Skill을 만들기 전에 다음 순서로 판단한다.

1. 기존 통합 Skill의 mode로 표현 가능한가?
2. 기존 Skill의 trigger·mode·reference 확장으로 해결 가능한가?
3. 독립된 입력·산출물·Quality Bar·검증 경로가 있는가?
4. 여러 작업에서 반복될 가능성이 있는가?

하나의 생명주기를 단계별 Skill 파일로 쪼개지 않는다. 반대로 생성 전 설계와 구현 후 감사처럼 입력·도구·승인 경계가 다른 책임은 독립 Skill로 유지한다.

## 선택적 호출

```json
{
  "load_all_skills": false,
  "default_selection": "none",
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

같은 요청의 상태와 사실을 통합 Skill의 mode가 재사용한다. 발행·검증·Handoff는 해당 단계에 도달할 때만 실행한다.

## 최소 Skill 계약

- Skill ID·분야·상태
- 목적과 사용하는 조건·사용하지 않는 조건
- trigger tags와 `load_by_default=false`
- mode와 상태 흐름
- 필수 입력·먼저 읽을 책임 원본
- 프로젝트 고유 규칙과 실제 경로
- 절차·산출물·Ready·Done
- 자동·수동 검증과 실패 조건
- Learning Log·review trigger
- 마지막 검토일·기준 커밋·지식 상태

## 학습 상태

```text
관찰 → 가설 → 패턴 → 검증 → 승격 후보
```

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출은 Learning Log에 기록한다. 사소한 성공 호출은 기록을 강제하지 않는다. 한 번의 성공은 공용 강제 규칙이 아니다.

## 통합 절차

통합 전 다음을 대조한다.

- 고유 입력·산출물·실패 조건·검증
- 프로젝트 전용 규칙
- 책임 원본·Documentation Map·작업 계약 참조
- Learning Log와 지식 상태
- Registry와 사람용 발행본 경로

통합 후 이전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에 연결하고 새 Registry·문서에는 새 ID만 사용한다. 단순 이전 버전은 Git 이력으로 보존한다.

## Health Review

다음 상황에서 Skill 구조를 검토한다.

- 동일 실패 반복
- 여러 Skill에 같은 절차 복제
- 새 작업 유형에 대응할 mode·Skill이 없음
- 새 채팅이 필요한 Skill을 찾지 못함
- Registry·실제 경로·발행본 불일치
- 90일 이상 활성 Skill 미검토
