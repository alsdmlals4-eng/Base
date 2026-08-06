---
name: evolving-project-discipline-skills
description: Use when creating, consolidating, evaluating, or improving project Foundation and discipline skills from reusable evidence.
---

# Evolving Project Discipline Skills

## Core principle

**Consolidation-first**: 새 Skill을 만들기 전에 기존 Skill mode·reference 확장으로 해결 가능한지 확인한다. 독립 입력·산출물·품질 기준·도구·승인 경계가 있을 때만 분리한다.

새 Skill·Mode·도구 통합은 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`의 Existing Solution First Gate도 적용한다. 기존 Base owner뿐 아니라 installed tool, connected MCP, addon, open/recent PR과 유지되는 external solution을 비교하고 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` 판정이 없으면 생성하지 않는다.

활성 Skill 개수는 고정 목표나 상한이 아니다. 독립 입력·산출물·Quality Bar·검증·승인 경계가 반복적으로 필요하면 새 Skill을 추가할 수 있고, 책임 경계가 없으면 기존 mode로 통합한다.

가지치기 자체는 `pruning-stale-and-nonfunctional-material`, 본문 압축은 `simplifying-skill-bodies`, 기능 보존 구조 변경은 `refactoring-with-contract-preservation`이 책임진다.

## Skill Modes

`inventory → existing-solution-disposition → decide-boundary → create-or-integrate → register → behavior-eval → verify → learn`

- `existing-solution-disposition`: 현재 Registry·package뿐 아니라 installed external solution·addon·MCP·CLI·관련 PR을 `evaluating-godot-assets-and-plugins-before-creation`과 비교하고 재사용·흡수·리팩터링 가능성을 먼저 닫는다.
- `behavior-eval`: 현실적인 사용자 Prompt에서 예상 Work Mode·주/보조 Skill·Skill Mode·금지 라우팅·필수 증거를 비교한다. 모든 ACTIVE Skill에 주 책임 사례와 잘못 선택하면 안 되는 non-selection 사례가 있어야 하며, 실제 모델 결과가 없으면 `MODEL_RUN_STATUS: NOT_RUN`으로 유지한다.

## Required inputs

```yaml
skill_registry_and_entrypoints:
existing_skills_references_scripts:
installed_and_external_solutions:
connected_mcp_and_addons:
related_open_and_recent_prs:
existing_solution_disposition:
legacy_aliases:
learning_and_failure_evidence:
actual_work_examples:
validation_and_publication_paths:
behavior_eval_cases:
behavior_eval_coverage_cases:
behavior_eval_results:
behavior_result_source_identity:
independent_reviewer_context:
skill_implementation_evidence_index:
```

## Boundary decision

1. 기존 통합 Skill의 mode로 처리 가능한가?
2. trigger·mode·reference 확장으로 해결 가능한가?
3. 검증된 external solution·addon·MCP·CLI를 `REUSE / ABSORB / REFACTOR`할 수 있는가?
4. 독립 입력·산출물·Quality Bar·검증·승인 경계가 있는가?
5. 여러 작업에서 반복될 책임인가?
6. `BUILD_NEW`가 필요한 차단 결함과 사용자 승인이 있는가?

세부 인벤토리·통합 전 보존표·Health Review는 `references/consolidation-and-health-review.md`를 필요할 때만 읽는다.

## Workflow

1. Registry·실제 패키지·entrypoint·Learning Log를 대조한다.
2. installed tool, connected MCP, addon, external solution, 같은 Goal의 open/recent PR을 조사한다.
3. `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` disposition과 근거·미검증·승인 상태를 기록한다.
4. 중복, 과분할, 누락, 죽은 자료, 과도한 기본 로드를 판정한다.
5. 고유 기능·입력·산출물·검증을 먼저 보존한다.
6. Skill·mode·reference 중 가장 작은 책임 단위로 생성 또는 통합한다.
7. `BUILD_NEW`는 기존 대안으로 충족 불가능한 최소 범위와 사용자 승인이 있을 때만 사용한다.
8. `load_by_default=false`, trigger, use/do-not-use, Learning Log를 등록한다.
9. `behavior-eval`에서 정상·비사용·경계·교차 Skill Prompt를 평가한다.
   - 핵심 압력·경계 fixture는 `skills/SKILL_BEHAVIOR_EVALS.json`에 둔다.
   - 전체 ACTIVE Skill의 주 책임·non-selection coverage는 `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json`에 보완한다.
   - 계약 검사와 실제 모델 결과 채점을 분리한다.
   - 모든 ACTIVE Skill은 `primary behavior coverage >= 1`, `non-selection behavior coverage >= 1`을 만족해야 한다.
   - 실제 결과는 `schemas/skill-behavior-results-v1.schema.json`과 `skills/SKILL_BEHAVIOR_RESULTS.template.json`을 사용하고 exact commit·Registry SHA-256·평가셋 SHA-256을 기록한다.
   - 작성 컨텍스트와 다른 `independent reviewer context`를 기록하지 못하면 실제 모델 행동 통과로 인정하지 않는다.
10. `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`의 명시적 근거 경로를 검증하고 `tools/build_skill_implementation_evidence.py`로 `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md`를 생성·대조한다.
11. `auditing-canonical-reference-freshness`와 `managing-game-project-operating-system` verify를 실행한다.

`behavior-eval`의 계약·coverage·결과 채점은 `tools/check_skill_behavior_evals.py`가 책임진다. Prompt에 예상 Skill ID나 Skill Mode를 노출하지 않고, 실제 결과 파일이 없으면 fixture와 coverage 유효성만 통과시키며 라우팅 품질은 통과로 보고하지 않는다. 결과 파일이 있어도 source identity가 현재 HEAD·Registry·평가셋과 다르거나 독립 검토 컨텍스트가 아니면 fail-closed 한다.

## Evidence interpretation

- `EXECUTABLE_EVIDENCE`: Test·Tool·Workflow·Script 경로가 등록되고 실제 파일이 존재한다. 현재 commit에서 통과했다는 뜻은 아니다.
- `CONTRACT_EVIDENCE`: 계약·문서 소비자는 있으나 실행형 근거가 아직 없다.
- `MISSING_EVIDENCE`: Skill package, 주 책임·non-selection coverage 또는 등록 증거가 누락됐다.
- 실제 모델 행동, 프로젝트 Pilot, 엔진 Runtime, 사람 이해도는 별도 상태이며 파일 존재로 승격하지 않는다.

## Output contract

```md
## 통합 전·후 구조와 활성 Skill 수
## 현재 도구·addon·MCP·external solution·관련 PR 인벤토리
## REUSE·ABSORB·REFACTOR·ARCHIVE·BUILD_NEW 판정과 승인 상태
## 유지·추가·통합·제거한 책임과 이유
## 고유 기능 보존표
## Registry·entrypoint·alias·reference·test 동기화
## ACTIVE Skill별 primary·non-selection behavior coverage
## 실제 모델 결과의 exact commit·Registry·평가셋 identity
## independent reviewer context와 독립성 상태
## Skill별 EXECUTABLE_EVIDENCE·CONTRACT_EVIDENCE·MISSING_EVIDENCE
## 선택적 호출·콜드 스타트·Health Review
## 행동 평가 계약·실제 모델 실행 상태
## 검증·미검증·Learning Log·다음 trigger
```

## Quality gate

- 기존 mode와 external solution 검토 없이 새 Skill을 추가하지 않는다.
- `BUILD_NEW` 판정의 차단 결함·비교 근거·사용자 승인이 없다면 생성하지 않는다.
- 이름만 합치며 기능·검증·승인 경계를 잃지 않는다.
- `LEGACY_SKILL_ALIASES.md`와 오래된 참조를 처리한다.
- 전체 skills 폴더를 기본 로드하지 않는다.
- 모든 ACTIVE Skill의 주 책임·non-selection behavior coverage가 없다면 계약을 통과시키지 않는다.
- stale commit·Registry·평가셋 결과를 현재 모델 행동 증거로 채점하지 않는다.
- 작성자와 같은 컨텍스트의 자기검토를 독립 검토로 표시하지 않는다.
- 실제 결과 없이 지식 상태를 승격하지 않는다.
- fixture·schema·증거 경로 존재를 실제 모델·Runtime·사람 행동 통과로 표현하지 않는다.

Registry Learning Log index: `skills/SKILL_LEARNING_LOG.md`

Focused behavior-evidence log: `skills/evolving-project-discipline-skills/LEARNING_LOG.md`
