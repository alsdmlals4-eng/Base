---
name: analyzing-and-refining-game-concepts
description: Use when defining or reworking a game's core concept, pointed fun, constraints, design coherence, Digital Dopamine Design, benchmark and player evidence, playtest or experiment design, PoC hypothesis, or production direction.
---

# Analyzing and Refining Game Concepts

## Core principle

기능을 늘리는 것이 아니라 플레이어가 반복할 **뾰족한 재미**와 핵심 선택을 선명하게 만들고, 외부 사례·사용자 반응·행동 증거·PoC로 가장 위험한 가설을 검증한다.

프로젝트 코어의 사실 판정·승인은 코어 Skill, 11영역 Games User Research 구조의 설치·누락 감사는 `governing-game-user-research-coverage`, 문서 작성은 `managing-design-documents`가 책임진다.

## Modes and state

`frame → constrain → sharpen → structure → benchmark-and-player-research → analyze → playtest-and-experiment → poc-contract → recalibrate → production-gate`

`CONCEPT_SEED → CONSTRAINTS_CHECKED → POINTED_FUN_HYPOTHESIS → CONCEPT_STRUCTURED → POC_BUILD_AND_TEST → CONCEPT_RECALIBRATION → PRODUCTION_READY | REPEAT_POC | HOLD | STOP`

## Required inputs

```yaml
current_idea_or_gdd:
target_player_and_play_context:
core_loop_and_game_elements:
constraints_and_production_capacity:
reference_games_and_player_evidence:
telemetry_playtest_experiment_evidence:
prototype_or_poc_results:
risks_unknowns_and_decision_to_make:
```

## Analysis lenses

- `SWOT`은 설명에서 끝내지 않고 `SO / WO / ST / WT` 행동으로 변환한다.
- `MDA / DDE / DDD`, 3C, 루프, 동기, 차별화, 제작성을 교차 확인한다.
- Base에서 `DDD`는 `Digital Dopamine Design`이며 첫 의미 있는 보상, 행동-피드백 지연, 보상 명료성·밀도, Micro→Session→Meta 사다리, 피로·인플레이션을 본다. 외부 동명 약어는 정의 확인 전 **임의 해석하지 않는다**.

세부 컨셉·제약·뾰족한 재미·PoC 게이트는 `references/concept-evidence-and-gates.md`, 벤치마크·사용자 근거·플레이테스트·DDD 계약은 `references/benchmark-playtest-and-ddd.md`를 필요할 때만 읽는다.

## Workflow

1. 대상 플레이어, 핵심 행동·선택, 감정·판타지, 차별 원리를 한 문장으로 고정한다.
2. 플레이·제작·기술·콘텐츠·표현·시장 제약을 확인한다.
3. 요소를 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 정렬한다.
4. 결정을 바꿀 질문만 벤치마킹하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 결론낸다.
5. 빌드·표본·과제·관찰·이벤트·퍼널·지표가 있는 플레이테스트·실험을 설계한다.
6. 가장 위험한 가설을 최소 PoC로 검증하고 `KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST`를 결정한다.

## Output contract

```md
## 핵심 컨셉·대상 플레이어·뾰족한 재미
## 제약과 코어 정렬
## SWOT·MDA/DDE/DDD·루프·차별화 분석
## 벤치마크·사용자·행동 증거와 판정
## 플레이테스트·실험·PoC 계약
## 유지·수정·삭제·보류 결정
## Production gate·미검증·다음 검증
```

## Quality gate

기능 복사, 리뷰 표본 편향, 자기보고와 행동 혼동, 여러 변수 동시 실험, PoC 범위 팽창, DDD의 무의미한 자극화, 결과를 본 뒤 성공 기준 변경을 금지한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
