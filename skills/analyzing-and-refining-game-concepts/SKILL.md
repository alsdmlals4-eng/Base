---
name: analyzing-and-refining-game-concepts
description: Use when defining or revising game concept, pointed fun, systems, difficulty, combat AI, tutorials, onboarding, benchmarks, playtests, PoC, or production direction.
---

# Analyzing and Refining Game Concepts

## Core principle

기능을 늘리는 것이 아니라 플레이어가 반복할 **뾰족한 재미**와 핵심 선택을 선명하게 만들고, 게임 시스템·난이도·전투 AI를 플레이어 경험 목표와 공정성·가독성·대응 가능성에 연결한 뒤 외부 사례·사용자 반응·행동 증거·필요한 기술 Spike와 완성형 Vertical Slice 증거로 가장 위험한 가설을 검증한다.

프로젝트 코어의 사실 판정·승인은 코어 Skill, 11영역 Games User Research 구조의 설치·누락 감사는 `governing-game-user-research-coverage`, 기획 책임 원본 작성·발행은 `managing-design-documents`, 실제 변경 검증은 `reviewing-and-validating-project-changes`가 책임진다.

`PLAYER_APPEAL_QUALITY_GATE`: Production 후보와 플레이테스트용 Vertical Slice는 기능 수가 아니라 플레이어 가치로 검수한다. 최소한 **독창성/차별점**, `DDD`의 행동-피드백-보상 품질, 아트·UI·사운드·연출의 **일관성**, 불필요한 **복잡성**, 의도한 **난이도와 접근 가능성**, 캐릭터/세계관/상호작용의 개성과 기억에 남는 순간을 함께 공격한다. 자동 테스트나 정적 문서만으로 재미·몰입을 PASS 처리하지 않으며 실제 인간 플레이가 필요한 축은 실행 전까지 `NOT_RUN`이다.

`EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`: 벤치마크·기존 시스템·자산·UI·오디오·도구를 먼저 조사하되 복사하지 않고 현재 프로젝트 코어와 장기 방향에 맞게 `ADOPT / ADAPT / REJECT`한다.

`RELEASE_NEAR_VERTICAL_SLICE_FIRST`: 시스템-only PoC는 기술 Spike로 제한한다. 재미·몰입·첫인상·전체 UX를 검증할 때는 shipping-intent UI/UX·이미지/아트·사운드·VFX·시스템/콘텐츠가 연결된 짧은 완성형 Vertical Slice를 사용한다.

`TECHNICAL_SPIKE_INTERNAL_ONLY`: 알고리즘·호환성·성능·데이터 흐름처럼 데모 전체를 막는 좁은 기술 불확실성만 최소 Spike로 검증한다. Spike 결과는 구현 가능성의 증거일 뿐 플레이어 재미·몰입·가독성·감정·기억의 PASS 근거가 아니다.

`DECISION_SPECIFIC_RESEARCH`: 이 Skill은 현재 게임 결정을 바꾸는 구체적 질문에 대해 벤치마크·플레이테스트·행동/자기보고 증거를 해석한다. 연구 영역의 전수 채움이나 coverage 상태 관리는 `governing-game-user-research-coverage`가 소유하며, 두 Skill이 같은 연구 책임을 중복 수행하지 않는다.

`WORLD_STORYLINE_FIT_REQUIRED`: 주요 컨셉·기능·시스템·난이도·기술 Spike/Vertical Slice 후보는 기능적으로 작동하거나 벤치마크가 강하더라도 프로젝트가 확정한 **세계관·핵심 스토리·플레이어 판타지**와 충돌하면 Production 후보로 승격하지 않는다. 해당 축이 현재 프로젝트에 실질적으로 없으면 이유가 있는 `NOT_APPLICABLE`로 남기고, 존재한다면 `FIT / CONFLICT / UNVERIFIED`를 근거와 함께 판정한다.

## Modes and state

`frame` → `constrain` → `sharpen` → `structure` → 필요한 경우 `tutorial-and-onboarding-design` → 필요한 경우 `system-design` → 필요한 경우 `difficulty-and-combat-ai` → `benchmark-and-player-research` → `analyze` → `playtest-and-experiment` → 필요한 경우 `technical-spike-contract` → `release-near-vertical-slice-handoff` → `recalibrate` → `production-gate`

`poc-contract`은 과거 호환 mode 이름이다. 새 작업에서는 `technical-spike-contract`로 해석하며 `TECHNICAL_SPIKE_INTERNAL_ONLY`의 좁은 기술 질문만 소유한다. 사람 플레이 경험 검증은 이 mode에서 수행하지 않고 `designing-vertical-slices`의 `RELEASE_NEAR_VERTICAL_SLICE_FIRST` 계약으로 넘긴다.

`CONCEPT_SEED → CONSTRAINTS_CHECKED → POINTED_FUN_HYPOTHESIS → CONCEPT_STRUCTURED → SYSTEM_AND_DIFFICULTY_CONTRACTED → TECHNICAL_SPIKE_IF_NEEDED → RELEASE_NEAR_VERTICAL_SLICE_REQUIRED_FOR_PLAYER_VALIDATION → CONCEPT_RECALIBRATION → PRODUCTION_READY | REPEAT_VERTICAL_SLICE | HOLD | STOP`

`tutorial-and-onboarding-design`은 새 독립 Skill이 아니라, 첫 세션·신규/복귀 플레이어가 현재 프로젝트의 핵심 규칙과 성장·도구·판단을 실제 플레이로 배우도록 하는 조건부 mode다. 튜토리얼 이해도 연구 coverage의 설치·누락 감사는 `governing-game-user-research-coverage`가 소유한다.

## Required inputs

```yaml
current_idea_or_gdd:
target_player_and_play_context:
player_experience_goal:
core_loop_and_game_elements:
world_storyline_and_player_fantasy_invariants:
current_system_and_combat_rules:
difficulty_barriers_and_assists:
enemy_roles_ai_and_encounter_pacing:
constraints_and_production_capacity:
reference_games_and_player_evidence:
telemetry_playtest_experiment_evidence:
prototype_or_poc_results:
risks_unknowns_and_decision_to_make:
pc_android_delivery_profile:
```

`prototype_or_poc_results`는 기존 자료의 기술 증거를 받을 수 있는 compatibility 입력이다. system-only PoC 결과가 들어와도 `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`에 따라 플레이어 경험 증거로 승격하지 않는다.

`tutorial-and-onboarding-design`을 선택할 때만 `current_tutorial_onboarding_and_first_session`, `prerequisite_knowledge_and_learning_goals`, `growth_or_capability_change_to_teach`, `help_skip_replay_returning_player_paths`를 추가로 확인한다.

## Analysis lenses

- `SWOT`은 설명에서 끝내지 않고 `SO / WO / ST / WT` 행동으로 변환한다.
- `MDA / DDE / DDD`, 3C, 루프, 동기, 차별화, 제작성을 교차 확인한다.
- Base에서 `DDD`는 `Digital Dopamine Design`이며 첫 의미 있는 보상, 행동-피드백 지연, 보상 명료성·밀도, Micro→Session→Meta 사다리, 피로·인플레이션을 본다. 외부 동명 약어는 정의 확인 전 **임의 해석하지 않는다**.
- `system-design`은 **플레이어 경험 목표 → 시스템 경계 → 입력·행동·상태·규칙 → 피드백·결과 → Evidence**를 추적한다.
- `difficulty-and-combat-ai`는 적의 지능과 압박량을 분리하고 **공정성·가독성·대응 가능성**, 공격 예산, 위협 예산, 긴장도 페이싱, 동적 난이도 조절을 설계한다.
- `tutorial-and-onboarding-design`은 **프로젝트 선감사 → RULE → NEED → DISCOVER → FEEL → PROVE → TRANSFER → 플레이테스트·텔레메트리 → 적대적 검토**를 추적한다.

세부 컨셉·제약·뾰족한 재미·기술 Spike gate는 `references/concept-evidence-and-gates.md`를 읽는다. 과거 `PoC gate` 표현은 compatibility locator이며 새 실행에서 player-experience validation 권위를 만들지 않는다. 벤치마크·사용자 반응·플레이테스트의 전체 증거 필드는 `references/benchmark-player-evidence-and-playtests.md`, DDD의 경계와 축약 계약은 `references/benchmark-playtest-and-ddd.md`를 해당 mode에서만 읽는다. 게임 시스템·난이도·전투 AI는 `references/game-system-difficulty-and-combat-ai.md`를 `system-design` 또는 `difficulty-and-combat-ai`에서만 읽고, 외부 근거를 확인할 때는 `references/game-system-difficulty-evidence-sources.md`를 함께 읽으며, `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`를 프로젝트 책임 원본 작성 틀로 사용한다.

기술 Spike·benchmark·적대적 검토를 통과한 주요 기능이 release-near Vertical Slice 구현을 위해 여러 직군의 production handoff가 필요하면 기획 책임 원본 작성은 `managing-design-documents`에 넘기고 `templates/planning/GAME_FEATURE_DESIGN_SPEC.md`를 사용한다. 이 Skill은 상세 문서의 canonical ownership을 가져오지 않는다. 튜토리얼·온보딩·첫 세션 학습은 `tutorial-and-onboarding-design` mode에서만 `docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md`와 `templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`를 사용한다.

Windows+Android 동시 목표, STOVE·Google Play·Steam 단계 출시, 모바일 레이아웃·입력·중단 복구가 기획 제약을 바꿀 때는 `constrain`, `technical-spike-contract`(과거 `poc-contract` 호환), `release-near-vertical-slice-handoff`, `production-gate`에서만 `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`를 읽고 `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`를 작성한다. 모든 프로젝트에 이 프로필을 강제하거나 두 플랫폼의 같은 날 공개를 요구하지 않는다.

## Workflow

1. 대상 플레이어, 핵심 행동·선택, 감정·판타지, 차별 원리를 한 문장으로 고정한다.
2. 플레이·제작·기술·콘텐츠·표현·시장 제약을 확인한다.
3. 요소를 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 정렬하고, 세계관·핵심 스토리·플레이어 판타지가 실질적 축이면 `WORLD_STORYLINE_FIT_REQUIRED`를 함께 판정한다.
4. `tutorial-and-onboarding-design`에서는 최신 사용자 지시·프로젝트 Notion/GitHub 정본·실제 코드·데이터·Scene·Resource·UI·입력·테스트·동일 Goal PR을 먼저 감사하고, 미확인 사실은 `BLOCKED_UNVERIFIED`로 분리한다. 폐기된 Google Sheets는 프로젝트가 명시적으로 보존한 migration/read-only evidence가 있을 때만 비교 자료로 읽고 신규 입력·활성 정본으로 사용하지 않는다.
5. 해당 mode에서는 학습 목표를 팝업 확인이 아닌 행동·필요 정보·시스템 반응·성공·실패·복구·독립 수행·전이로 정의하고 `RULE → NEED → DISCOVER → FEEL → PROVE → TRANSFER`를 설계한다.
6. 해당 mode에서는 성장 전후 행동 차이, Skip·복습·복귀, 접근성 대체 채널, 완료율 외의 힌트·재시도·독립 수행·전이 측정을 연결한다.
7. 시스템 설계가 필요하면 책임·입력·출력·비책임·정본·실패·검증을 나누고 행동·선택·결과 계약으로 연결한다.
8. 난이도·전투 AI가 필요하면 난이도 장벽 프로필과 공정성 안전 규칙을 먼저 고정하고, 개별 적 판단·전투 조율자·난이도/페이싱 디렉터를 분리한다.
9. 공격·위협 예산, 반응시간·예고·회복, `Build Up → Sustain Peak → Peak Fade → Relax`, 고정 난이도별 조절 변수를 설계한다.
10. 적응형 난이도는 장기 실력과 단기 스트레스를 분리하고 히스테리시스·변경 쿨다운·안전한 적용 시점을 정하며 성공을 즉시 상쇄하지 않는다.
11. 결정을 바꿀 질문만 벤치마킹하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 결론낸다.
12. 필요한 사람 플레이 질문은 빌드·표본·과제·관찰·이벤트·퍼널·지표를 설계한 뒤 `designing-vertical-slices`의 release-near Slice 계약으로 넘긴다. 이미 확보된 유효 human evidence는 분석할 수 있지만 새 system-only PoC로 사람 경험을 대체하지 않는다.
13. 데모 전체를 차단하는 가장 위험한 **기술 불확실성**이 있을 때만 최소 `TECHNICAL_SPIKE_INTERNAL_ONLY`를 실행해 `KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST`를 결정한다. 기술 Spike가 필요 없으면 생략한다. 이 결과만으로 재미·몰입·전체 UX를 판정하지 않는다.
14. `KEEP / CHANGE / RETEST`로 살아남고 release-near Vertical Slice 구현을 위해 여러 직군의 production handoff가 필요한 **주요 L2 기능만** 상세 기획 후보로 승격한다. pre-evidence 아이디어(과거 문서의 `pre-PoC` 포함), `REMOVE / DEFER`, L0·L1 단일 수정은 승격하지 않는다. 승격 시 `managing-design-documents`에 넘겨 `GAME_FEATURE_DESIGN_SPEC.md`를 작성·등록하고, 승인 뒤 기존 Traceability Packet으로 구현·검증 연결을 넘긴다.

## Output contract

```md
## 핵심 컨셉·대상 플레이어·뾰족한 재미
## 제약과 코어 정렬
## 세계관·핵심 스토리·플레이어 판타지 정합성
## 플레이어 경험 목표·시스템 경계·행동/선택/결과
## 난이도 장벽 프로필·공정성 안전 규칙
## 개별 적 판단·전투 조율자·난이도/페이싱 디렉터
## 공격·위협 예산·긴장도 페이싱·고정/동적 난이도 조절
## SWOT·MDA/DDE/DDD·루프·차별화 분석
## 벤치마크·사용자·행동 증거와 판정
## 플레이테스트 계획·Technical Spike 계약·release-near Vertical Slice handoff
## 유지·수정·삭제·보류 결정
## L2 상세기획 승격 여부·근거·GAME_FEATURE_DESIGN_SPEC handoff
## Base 승격 후보·프로젝트 전용 유지
## Production gate·미검증·롤백·다음 검증
```

`tutorial-and-onboarding-design` mode를 사용한 경우에는 `RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER`, 안내 감소·독립 수행·전이·Skip·복습·복귀·접근성, 성장 전후 비교와 튜토리얼 플레이테스트·텔레메트리 산출물을 함께 기록한다.

## Quality gate

기능 복사, 리뷰 표본 편향, 자기보고와 행동 혼동, 여러 변수 동시 실험, technical Spike 범위 팽창, system-only PoC의 player-experience evidence 승격, DDD의 무의미한 자극화, 결과를 본 뒤 성공 기준 변경을 금지한다. 세계관·핵심 스토리·플레이어 판타지가 실질적 프로젝트 축인데 기능 편의나 벤치마크 인기를 이유로 그 충돌을 무시하는 것도 금지한다.

`tutorial-and-onboarding-design`에서는 프로젝트 정본·실제 구현 선감사 누락, 정적 조작표를 학습 완료로 판정, 문제 인식 전 해결책 광고, 상점·과금을 위한 강제 패배, 숨은 규칙으로 만든 가짜 결핍, 숫자·연출만 바뀌는 가짜 성장, 안내 없는 독립 수행·다른 상황 전이 검사·Skip·복습·복귀·접근성 대체 채널 누락을 금지한다.

난이도·전투 AI에서는 보이지 않는 정보로 처벌, 플레이어 입력 직접 읽기, 카메라 밖 즉사, 연속 기절·회피 불가능 조합, 체력 스펀지로 선택 대체, 성공 직후 성장 무효화, 현재 전투 중 노골적인 수치 조작, 히스테리시스 없는 난이도 진동, 텔레메트리만으로 감정·원인 확정을 금지한다.

상세 기획 승격에서는 pre-evidence 아이디어(과거 `pre-PoC` 포함)를 문서 완성도로 정당화하거나, 전문 분야 정본을 범용 Spec으로 대체하거나, Feature Spec에 Task progress·PR 상태·executed verification을 복제하는 것을 금지한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`

## Cloud Run backend capability handoff

게임 기능 분석 중 `SERVER_FEATURE_DETECTED`가 확인되면 플레이어 가치와 서버 필요성을 먼저 판정하고 `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`의 fit Gate로 넘긴다. 공급자 선택은 서버 필요성보다 앞서지 않는다.