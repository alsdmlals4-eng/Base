---
name: evolving-project-discipline-skills
description: Use when creating, reviewing, consolidating, or improving project Foundation and discipline skills from actual work and validation evidence while keeping the Registry and configured human derivatives synchronized.
---

# Evolving Project Discipline Skills

## Core principle

새 Skill을 추가하기 전에 기존 통합 Skill의 mode로 흡수할 수 있는지 먼저 판정한다. 공용 절차는 Foundation에 한 번만 두고, 분야 Skill은 고유 판단·책임 원본·실제 경로·산출물·검증만 책임진다.

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출만 Learning Log에 기록한다. 한 번의 성공은 관찰 또는 가설이다.

## Use when

- Skill Registry와 실제 경로·상태가 불일치한다.
- 여러 Skill에 같은 절차가 복제됐다.
- 하나의 생명주기가 단계별 Skill로 과도하게 쪼개졌다.
- 기존 Skill의 mode로 처리할 수 없는 반복 작업이 확인됐다.
- 실제 실패·예외·검증 결과를 Skill 계약에 반영한다.
- 새 채팅이 필요한 최소 Skill을 찾지 못한다.
- 사람용 Skill Map이 Registry보다 오래됐다.

## Do not use when

- Skill 계약에 영향 없는 일반 구현이다.
- 단순히 파일 수를 늘리려는 작업이다.
- 한 번의 성공을 공용 강제 규칙으로 승격하려는 경우다.
- 전체 skills 폴더를 기본 컨텍스트로 읽게 하려는 경우다.

## Required inputs

```yaml
project_start_here:
documentation_map:
skill_registry:
skill_map_publication_manifest:
design_document_registry:
relevant_design_document_sources:
existing_skills:
legacy_skill_aliases:
reference_freshness_config:
learning_logs:
actual_work_examples:
validation_and_failures:
base_version:
```

## Phase 1 — Inventory

| Skill | mode | 분야 | trigger | 입력 | 산출물 | 검증 | 고유 책임 | 중복 | 상태 |
|---|---|---|---|---|---|---|---|---|---|

찾을 것:

- 기존 통합 Skill mode와 중복
- 같은 요청의 라우팅·조사·상태 판정 반복
- Method·Checklist·Skill에 같은 실행 절차 복제
- 설명만 있고 실행 계약이 없음
- 등록된 책임 원본·실제 파일·검증 경로가 없음
- 사용·비사용 조건이나 trigger가 없음
- `load_by_default=true` 또는 전체 로드 요구
- Learning Log·review trigger 누락
- 백업·보류·제거 후보의 기본 읽기 혼입

## Phase 2 — Consolidation-first decision

다음 순서로 판정한다.

1. 기존 Skill의 mode로 처리 가능한가?
2. 기존 Skill의 trigger·mode·reference 확장으로 해결 가능한가?
3. 독립된 입력·산출물·Quality Bar·검증·승인 경계가 있는가?
4. 여러 작업에서 반복될 가능성이 있는가?

하나의 생명주기는 통합 Skill과 상태 머신으로 우선 표현한다.

독립 Skill을 유지하는 예:

- 이미지 생성 전 프롬프트 설계
- 구현된 Godot·Web UI 결과 감사
- 범용 변경 검증이 오케스트레이션하지만 독립 자동 검사·영향 지도·파생본 증거를 가진 정본 최신성 감사

시점·입력·도구·승인 경계 또는 독립된 자동 증거가 다르면 억지로 한 파일에 합치지 않는다.

## Phase 3 — Skill contract

각 Skill 필수 항목:

- Skill ID·분야·상태
- 목적·사용 조건·비사용 조건
- `trigger_tags`, `load_by_default=false`
- mode와 상태 흐름
- 필수 입력·먼저 읽을 책임 원본
- 실제 경로·절차·산출물
- Definition of Ready·Done
- 자동·수동 검증·실패 조건
- 관련 Skill·Learning Log·review trigger
- 마지막 검토일·기준 커밋·지식 상태

## Phase 4 — Register selective routing

Registry에는 활성 Skill만 등록한다. 통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 연결한다.

기본 정책:

```json
{
  "load_all_skills": false,
  "default_selection": "none",
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

주 책임 분야 Skill은 최대 하나다. 발행·검증·Handoff는 해당 단계에서만 실행한다.

## Phase 5 — Preserve before consolidation

통합 전 다음을 추출·대조한다.

- 고유 입력·산출물·실패 조건·검증
- 프로젝트 전용 규칙과 실제 경로
- 책임 원본·Documentation Map·Issue·PR 참조
- Learning Log와 지식 상태
- scripts·references·templates
- Registry와 사람용 발행본 경로

고유 절차는 새 Skill 또는 새 Skill의 `references/`에 승계한다. 이전 버전은 Git 이력으로 보존한다.

통합·이름 변경·경로 이동 뒤에는 `auditing-canonical-reference-freshness`로 다음을 확인한다.

- 이전 Skill ID·경로가 활성 파일에 남지 않았는가?
- Legacy Alias가 모든 제거 ID를 새 Skill·mode로 연결하는가?
- START_HERE·Documentation Map·템플릿·테스트가 새 진입점을 사용하는가?
- Registry·사람용 Skill Map·Manifest가 현재 Skill 계약과 일치하는가?
- 변경됐어야 하지만 untouched인 소비자가 없는가?

## Phase 6 — Apply and learn

```text
통합·수정안
→ Registry·Skill·alias 갱신
→ 관련 문서·템플릿·검사 갱신
→ canonical reference freshness 감사
→ 대표·변형·반례 검증
→ 필요 시 사람용 Skill Map 재생성
→ 결과·실패·예외·사용자 피드백 기록
→ 지식 상태 판정
```

지식 상태:

```text
관찰 → 가설 → 패턴 → 검증 → 승격 후보
```

## Phase 7 — Health Review

스킬 구조를 크게 변경한 뒤 `managing-game-project-operating-system`의 `verify` mode로 다음을 확인한다.

- Registry 경로·trigger·비사용 조건
- 활성 Skill 수와 중복 mode
- Legacy alias의 완전성
- 오래된 ID·경로·설명과 변경 전파 누락
- Learning Log·지식 상태
- 선택적 호출과 Foundation 연쇄 호출 수
- 사람용 Skill Map·Manifest 최신성
- Governance checker·reference freshness·회귀 테스트·GitHub Actions
- 새 채팅의 최소 Skill 탐색

## Output contract

```md
## 프로젝트 Skill 구조 검수
- 통합 전·후 활성 Skill 수:
- 유지한 독립 Skill과 이유:
- 새 mode·통합 Skill:
- Legacy alias:
- Registry 상태:
- 고유 절차·reference·script 보존:
- 정본·참조 최신성·전파 누락:
- 선택적 호출 검증:
- 실행한 검사·회귀·Actions:
- Learning Log·지식 상태:
- 미검증·위험·다음 검토 trigger:
```

## Failure conditions

- 기존 Skill mode 검토 없이 새 파일을 추가함
- 고유 입력·검증을 잃고 이름만 합침
- 전체 skills 폴더를 기본 로드함
- trigger 없이 호출함
- 이전 ID를 alias 없이 제거함
- Registry 변경 뒤 관련 문서·검사·발행본을 갱신하지 않음
- 통합 뒤 오래된 ID·경로·untouched 소비자를 검사하지 않음
- 실제 결과 없이 지식 상태를 검증으로 승격함
- Learning Log를 누락함
