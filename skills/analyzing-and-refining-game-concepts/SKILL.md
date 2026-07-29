---
name: analyzing-and-refining-game-concepts
description: Use when defining or reworking a game's core concept, pointed fun, constraints, game systems, difficulty, combat AI, Digital Dopamine Design, benchmark and player evidence, playtest or experiment design, PoC hypothesis, or production direction.
---

# Analyzing and Refining Game Concepts

## Core principle

기능을 늘리는 것이 아니라 플레이어가 반복할 **뾰족한 재미**와 핵심 선택을 선명하게 만들고, 게임 시스템·난이도·전투 AI를 플레이어 경험 목표와 공정성·가독성·대응 가능성에 연결한 뒤 외부 사례·사용자 반응·행동 증거·PoC로 가장 위험한 가설을 검증한다.

프로젝트 코어의 사실 판정·승인은 코어 Skill, 11영역 Games User Research 구조의 설치·누락 감사는 `governing-game-user-research-coverage`, 기획 책임 원본 작성·발행은 `managing-design-documents`, 실제 변경 검증은 `reviewing-and-validating-project-changes`가 책임진다.

## Modes and state

`frame` → `constrain` → `sharpen` → `structure` → 필요한 경우 `system-design` → 필요한 경우 `difficulty-and-combat-ai` → `benchmark-and-player-research` → `analyze` → `playtest-and-experiment` → `poc-contract` → `recalibrate` → `production-gate`

`CONCEPT_SEED → CONSTRAINTS_CHECKED → POINTED_FUN_HYPOTHESIS → CONCEPT_STRUCTURED → SYSTEM_AND_DIFFICULTY_CONTRACTED → POC_BUILD_AND_TEST → CONCEPT_RECALIBRATION → PRODUCTION_READY | REPEAT_POC | HOLD | STOP`

## Required inputs

```yaml
current_idea_or_gdd:
target_player_and_play_context:
player_experience_goal:
core_loop_and_game_elements:
current_system_and_combat_rules:
difficulty_barriers_and_assists:
enemy_roles_ai_and_encounter_pacing:
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
- `system-design`은 **플레이어 경험 목표 → 시스템 경계 → 입력·행동·상태·규칙 → 피드백·결과 → Evidence**를 추적한다.
- `difficulty-and-combat-ai`는 적의 지능과 압박량을 분리하고 **공정성·가독성·대응 가능성**, 공격 예산, 위협 예산, 긴장도 페이싱, 동적 난이도 조절을 설계한다.

세부 컨셉·제약·뾰족한 재미·PoC 게이트는 `references/concept-evidence-and-gates.md`를 읽는다. 벤치마크·사용자 반응·플레이테스트의 전체 증거 필드는 `references/benchmark-player-evidence-and-playtests.md`, DDD의 경계와 축약 계약은 `references/benchmark-playtest-and-ddd.md`를 해당 mode에서만 읽는다. 게임 시스템·난이도·전투 AI는 `references/game-system-difficulty-and-combat-ai.md`를 `system-design` 또는 `difficulty-and-combat-ai`에서만 읽고, 외부 근거를 확인할 때는 `references/game-system-difficulty-evidence-sources.md`를 함께 읽으며, `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`를 프로젝트 책임 원본 작성 틀로 사용한다.

## Workflow

1. 대상 플레이어, 핵심 행동·선택, 감정·판타지, 차별 원리를 한 문장으로 고정한다.
2. 플레이·제작·기술·콘텐츠·표현·시장 제약을 확인한다.
3. 요소를 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 정렬한다.
4. 시스템 설계가 필요하면 책임·입력·출력·비책임·정본·실패·검증을 나누고 행동·선택·결과 계약으로 연결한다.
5. 난이도·전투 AI가 필요하면 난이도 장벽 프로필과 공정성 안전 규칙을 먼저 고정하고, 개별 적 판단·전투 조율자·난이도/페이싱 디렉터를 분리한다.
6. 공격·위협 예산, 반응시간·예고·회복, `Build Up → Sustain Peak → Peak Fade → Relax`, 고정 난이도별 조절 변수를 설계한다.
7. 적응형 난이도는 장기 실력과 단기 스트레스를 분리하고 히스테리시스·변경 쿨다운·안전한 적용 시점을 정하며 성공을 즉시 상쇄하지 않는다.
8. 결정을 바꿀 질문만 벤치마킹하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 결론낸다.
9. 빌드·표본·과제·관찰·이벤트·퍼널·지표가 있는 플레이테스트·실험을 설계한다.
10. 가장 위험한 가설을 최소 PoC로 검증하고 `KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST`를 결정한다.

## Output contract

```md
## 핵심 컨셉·대상 플레이어·뾰족한 재미
## 제약과 코어 정렬
## 플레이어 경험 목표·시스템 경계·행동/선택/결과
## 난이도 장벽 프로필·공정성 안전 규칙
## 개별 적 판단·전투 조율자·난이도/페이싱 디렉터
## 공격·위협 예산·긴장도 페이싱·고정/동적 난이도 조절
## SWOT·MDA/DDE/DDD·루프·차별화 분석
## 벤치마크·사용자·행동 증거와 판정
## 텔레메트리·플레이테스트·실험·PoC 계약
## 유지·수정·삭제·보류 결정
## Base 승격 후보·프로젝트 전용 유지
## Production gate·미검증·롤백·다음 검증
```

## Quality gate

기능 복사, 리뷰 표본 편향, 자기보고와 행동 혼동, 여러 변수 동시 실험, PoC 범위 팽창, DDD의 무의미한 자극화, 결과를 본 뒤 성공 기준 변경을 금지한다.

난이도·전투 AI에서는 보이지 않는 정보로 처벌, 플레이어 입력 직접 읽기, 카메라 밖 즉사, 연속 기절·회피 불가능 조합, 체력 스펀지로 선택 대체, 성공 직후 성장 무효화, 현재 전투 중 노골적인 수치 조작, 히스테리시스 없는 난이도 진동, 텔레메트리만으로 감정·원인 확정을 금지한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
