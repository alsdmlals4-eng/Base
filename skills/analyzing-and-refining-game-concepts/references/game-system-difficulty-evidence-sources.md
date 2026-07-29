# Game System, Difficulty, and Combat AI Evidence Sources

## Purpose

`system-design` 또는 `difficulty-and-combat-ai`에서 외부 근거가 필요한 경우 읽는다. 이 문서는 수치 정본이 아니라 **출처·적용 질문·한계·재검증 조건**을 제공한다. 프로젝트 값은 플레이테스트와 실제 구현 증거로 확정한다.

```yaml
checked_at: 2026-07-29
owner_skill: analyzing-and-refining-game-concepts
modes: [system-design, difficulty-and-combat-ai]
```

## Source use rule

1. 현재 결정 질문과 연결되지 않은 출처는 추가하지 않는다.
2. 사례의 구조를 `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY`로 판정한다.
3. 상용 게임의 실제 수치·장르·카메라·입력 조건을 그대로 복제하지 않는다.
4. 외부 사례보다 프로젝트 텔레메트리·플레이 영상·관찰·인터뷰를 우선한다.
5. 출처가 존재한다는 이유로 실제 플레이어 검증을 완료했다고 주장하지 않는다.

---

## AI-L4D-PACING-001

```yaml
source_id: AI-L4D-PACING-001
title: The AI Systems of Left 4 Dead
organization_or_author: Michael Booth / Valve
url: https://cdn.akamai.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: Valve presentation, 2009
checked_at: 2026-07-29
topics: [AI Director, dramatic pacing, intensity, Build Up, Sustain Peak, Peak Fade, Relax, fairness]
use_for: 지속 전투가 아닌 압박과 회복의 파형, 위협 빈도 조절, 플레이어 강도 추정, 공정한 불완전 지식·반응시간 설계를 검토한다.
사용_한계: 협동 FPS·Left 4 Dead의 적 종류·세션·수치·30~45초 Relax 값을 다른 장르에 그대로 사용하지 않는다. 발표는 페이싱과 난이도를 구분하므로 프로젝트에서 둘을 혼용하지 않는다.
재검증_조건: AI Director 상태·강도 입력·보스 예외·생성 빈도를 실제 프로젝트 규칙으로 확정할 때.
```

## AI-ATTACK-BUDGET-001

```yaml
source_id: AI-ATTACK-BUDGET-001
title: Beyond the Kung-Fu Circle: A Flexible System for Managing NPC Attacks
organization_or_author: Giacomo M. Vaccari / Game AI Pro
url: https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter28_Beyond_the_Kung-Fu_Circle_A_Flexible_System_for_Managing_NPC_Attacks.pdf
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: Game AI Pro, Chapter 28
checked_at: 2026-07-29
topics: [grid capacity, attack capacity, enemy weight, attack weight, stage manager, positioning]
use_for: 적 수만 제한하지 않고 적·공격별 비용과 중앙 전투 조율자로 동시 압박을 통제하는 공격·위협 예산 구조를 검토한다.
사용_한계: 원문의 격자·내외부 원·비용 값은 해당 게임 사례다. 2D·원거리·턴제·보스전에서는 위치 슬롯과 예산 의미를 다시 정의한다.
재검증_조건: 실제 적 역할·공격 비용·슬롯 해제 조건·동시 공격 상한을 프로젝트 데이터로 확정할 때.
```

## AI-REACTION-001

```yaml
source_id: AI-REACTION-001
title: Agent Reaction Time: How Fast Should an AI React?
organization_or_author: Steve Rabin / Game AI Pro 2
url: https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter05_Agent_Reaction_Time_How_Fast_Should_An_AI_React.pdf
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: Game AI Pro 2, Chapter 5
checked_at: 2026-07-29
topics: [reaction time, simple response, recognition, context, attention, aiming]
use_for: 감지 즉시 반응하는 AI를 피하고, 단순 반응·식별·조준·약한 자극·주의 상태를 분리한 반응시간 가설을 세운다.
사용_한계: 0.2~0.4초는 문맥 설명을 위한 출발 범위이며 프로젝트 기본값이 아니다. 애니메이션, 네트워크, 장르 속도, 입력 지연, 대상 플레이어를 포함해 측정한다.
재검증_조건: 난이도별 반응시간이나 보스·기습·정면 감지 값을 실제 수치로 채택할 때.
```

## AI-ACCURACY-001

```yaml
source_id: AI-ACCURACY-001
title: Using Your Combat AI Accuracy to Balance Difficulty
organization_or_author: Álvaro Castanho / Game AI Pro 3
url: https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter33_Using_Your_Combat_AI_Accuracy_to_Balance_Difficulty.pdf
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: Game AI Pro 3, Chapter 33
checked_at: 2026-07-29
topics: [damage throughput, accuracy control, attack token, intentional miss, urgency, tracers, VFX, sound]
use_for: 실제 피해량을 통제하면서도 공격 의도·탄착·사운드·파괴 효과로 압박과 AI 신뢰성을 유지하는 방법을 검토한다.
사용_한계: 플레이어를 속이는 명중 조작을 기본 규칙으로 삼지 않는다. 원거리 슈팅 사례를 근접·전술 게임에 적용할 때 후딜레이·짧은 사거리·직전 위치 공격 등으로 변환하고 공정성 규칙을 유지한다.
재검증_조건: 명중 권한·빗나감 위치·탄착 VFX·피해 간격을 실제 전투에 적용할 때.
```

## DDA-REVIEW-001

```yaml
source_id: DDA-REVIEW-001
title: Dynamic Difficulty Adjustment (DDA) in Computer Games: A Review
organization_or_author: Mohammad Zohaib / Advances in Human-Computer Interaction
url: https://doi.org/10.1155/2018/5681652
source_tier: T5_SYNTHESIS
published_or_version: 2018
checked_at: 2026-07-29
topics: [dynamic difficulty adjustment, player ability, game state, adaptation timing, coherence]
use_for: DDA의 입력·조절 대상·적용 시점·플레이어 감지 가능성·연속 상태 일관성을 분리해 설계한다.
사용_한계: 리뷰가 소개하는 접근들의 효과와 평가 품질은 서로 다르다. 현재 HP 같은 단일 신호나 실시간 수치 변경을 자동 정답으로 간주하지 않는다.
재검증_조건: DDA를 실제 기능으로 채택하거나 특정 알고리즘·모델·평가 방법을 선택할 때 원 연구를 확인한다.
```

## DDA-SLR-2025-001

```yaml
source_id: DDA-SLR-2025-001
title: Solutions for Dynamic Difficulty Adjustment in Digital Games: A Systematic Literature Review
organization_or_author: Entertainment Computing / Elsevier
url: https://doi.org/10.1016/j.entcom.2025.101041
source_tier: T5_SYNTHESIS
published_or_version: 2025
checked_at: 2026-07-29
topics: [DDA solutions, heuristics, AI methods, frameworks, models, modularity, evaluation]
use_for: 규칙 기반·AI 기반 조절을 모두 후보로 두되, 1인 개발에서는 설명 가능하고 모듈화된 최소 구조부터 검토한다.
사용_한계: 선정 연구와 장르가 다양하고, 일반화 가능하고 유연한 DDA는 여전히 연구 과제다. 머신러닝 도입 필요성을 자동으로 정당화하지 않는다.
재검증_조건: 새로운 DDA framework·ML 모델·생리 신호·감정 추정을 프로젝트 범위에 넣을 때.
```

---

## Evidence-to-design mapping

| 설계 질문 | 우선 Source | Base에서의 사용 |
|---|---|---|
| 압박과 회복을 어떻게 배치하는가? | `AI-L4D-PACING-001` | 긴장도 상태와 페이싱 가설 |
| 여러 적의 동시 공격을 어떻게 제한하는가? | `AI-ATTACK-BUDGET-001` | 공격·위협 예산과 중앙 조율자 |
| 적이 얼마나 빨리 반응해야 하는가? | `AI-REACTION-001` | 상황별 반응시간 가설과 측정 |
| 피해는 줄이면서 압박은 어떻게 유지하는가? | `AI-ACCURACY-001` | 명중 권한·의도적 빗나감·피드백 |
| 무엇을 언제 적응시킬 것인가? | `DDA-REVIEW-001`, `DDA-SLR-2025-001` | 장기 실력·단기 스트레스·적용 시점·검증 |

프로젝트 적용 결과는 `skills/SKILL_LEARNING_LOG.md`에 직접 승격하지 않는다. 프로젝트 Pilot과 반복 증거를 거쳐 `managing-base-change-proposals`로 환류한다.
