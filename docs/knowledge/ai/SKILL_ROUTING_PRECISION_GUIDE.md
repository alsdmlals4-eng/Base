# Skill Routing Precision Guide

## 목적

활성 Skill 수 자체를 고정 상한으로 관리하지 않고, **한 요청에서 실제로 노출·실행하는 Skill 후보를 작게 유지해 라우팅 혼동과 문맥 비용을 줄인다.**

이 Guide는 `skills/SKILL_REGISTRY.json`을 대체하지 않는다. Registry의 trigger, `do_not_use_when`, status, hard ceiling이 기계 권한이며 이 문서는 그 범위 안에서 더 보수적인 기본 shortlist 운용법을 정의한다.

## 근거

2026 ACL ToolScope는 이름·설명이 겹치는 도구가 선택 모호성을 만들고 정확도를 낮출 수 있으며, 중복 도구 병합과 질의별 관련 도구 필터링이 세 모델·세 tool-use benchmark에서 tool-selection accuracy를 8.38%~38.6% 높였다고 보고했다.

- Liu et al., *ToolScope: Enhancing LLM Agent Tool Use through Tool Merging and Context-Aware Filtering*, ACL 2026: https://aclanthology.org/2026.acl-long.1573/

SkillRouter는 약 8만 Skill의 겹침이 큰 pool에서 metadata-only routing보다 Skill 본문을 포함한 retrieval/reranking이 훨씬 강한 신호였고, 본문 제거 시 주요 설정에서 Hit@1이 31.4~44.0 percentage point 감소했다고 보고했다.

- Zheng et al., *SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale*, 2026: https://arxiv.org/abs/2603.22455

MetaTool은 비슷한 선택지, 특정 상황, 신뢰성 이슈, multi-tool selection에서 LLM의 tool-selection 한계를 별도 평가해야 함을 보여준다.

- Huang et al., *MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use*, ICLR 2024: https://proceedings.iclr.cc/paper_files/paper/2024/hash/bc12914d66b41b6bfc2d3a5decdb498b-Abstract-Conference.html

이 근거는 Base의 30개 Skill에 동일한 효과 크기가 그대로 재현된다는 뜻이 아니다. Base는 이미 `load_all_skills=false`, trigger match, negative trigger, 주 분야 Skill 1개 제한을 사용하므로 대규모 flat tool list보다 유리하다. 이 Guide는 남은 위험인 **겹치는 supporting/foundation 후보의 과잉 활성화**를 줄이는 보수적 운영 계약이다.

## Operational contract

```text
DEFAULT_SUPPORTING_SKILL_BUDGET: 1
SECOND_SUPPORTING_SKILL: EXCEPTION_ONLY
FULL_SKILL_BODY_TIE_BREAK: REQUIRED
DO_NOT_FILL_BUDGET: REQUIRED
FUNCTIONAL_OVERLAP: REUSE_ABSORB_MERGE_FIRST
```

### 1. 먼저 주 책임 하나를 고른다

1. 요청을 원자적 목표로 해석한다.
2. Registry의 status, trigger, `do_not_use_when`으로 후보를 만든다.
3. 최종 결정을 소유하는 primary discipline Skill은 하나만 남긴다.
4. 단순 L0·기계 작업은 관련 Skill이 명시적으로 불필요하면 Skill을 억지로 추가하지 않는다.

Registry의 `max_primary_discipline_skills=1`은 그대로 지킨다.

### 2. supporting Skill 기본 budget은 1이다

주 책임 외 supporting/foundation/검증/발행/Handoff Skill은 **현재 단계에서 없으면 결과가 불완전해지는 책임 하나**만 기본으로 붙인다.

다음은 supporting Skill 추가 사유가 아니다.

- trigger 단어가 일부 겹친다.
- “있으면 더 꼼꼼할 것 같다.”
- Registry hard ceiling에 아직 자리가 남는다.
- 같은 사실을 다른 관점에서 다시 확인할 수 있다.
- 미래 단계에서 필요할 수 있다.

미래 단계의 Skill은 현재 실행하지 않고 deferred 후보로 둔 뒤 단계 전환 시 재라우팅한다.

### 3. 두 번째 supporting Skill은 예외다

두 번째 supporting Skill은 아래 중 하나를 증명할 때만 선택한다.

- 서로 다른 **독립 산출물**을 각각 소유한다.
- 하나는 구현 owner이고 다른 하나는 현재 단계에 반드시 필요한 **독립 검증/권한 경계**를 소유한다.
- 안전·보안·법적/릴리스 차단처럼 누락 시 결과를 유효하다고 주장할 수 없는 hard guard가 있다.
- 사용자 요청이 실제로 두 개의 독립 하위 문제를 명시하고 한 Skill로 흡수하면 책임 경계가 무너진다.

같은 책임을 두 Skill이 반복하면 두 번째 Skill을 추가하지 않는다. 필요한 경우 상위 작업을 두 단계로 분해해 각 단계에서 다시 sparse routing한다.

Registry의 `max_foundation_skills=3`은 **호환성을 위한 hard ceiling**이며 매 요청에서 채워야 할 목표치가 아니다. 일반 shortlist는 이 Guide의 더 작은 default budget을 따른다.

### 4. 겹치는 후보는 Skill 본문으로 tie-break한다

이름·description·trigger만으로 둘 이상이 비슷해 보이면 동시에 활성화하지 않는다.

1. 각 후보의 `SKILL.md` 전체 본문에서 `Use when`, `Do not use when`, owner, required input/output, failure, verification을 비교한다.
2. 현재 요청의 실제 산출물과 가장 직접적으로 맞는 owner를 선택한다.
3. 다른 후보가 독립 산출물/guard를 소유하지 않으면 제외한다.
4. 동률이 남으면 더 좁고 구체적인 책임을 우선하고, 여전히 결정 불가하면 `BLOCKED_UNVERIFIED` 또는 사용자 결정이 아니라 **라우팅 메타데이터 결함**으로 기록한다.

SkillRouter 연구의 결과를 Base에 적용할 때 핵심은 “모든 Skill 본문을 매번 전부 로드”하는 것이 아니다. 먼저 Registry metadata로 작은 후보군을 만든 뒤 **동률 후보의 본문만** 읽는다.

### 5. 기능 중복은 추가가 아니라 통합 후보로 본다

Skill audit에서 둘 이상의 활성 Skill이 같은 입력·산출물·권한·검증 경계를 반복하면 다음 순서로 판정한다.

```text
REUSE → ABSORB → MERGE → ARCHIVE → BUILD_NEW
```

다음 중 하나가 독립적일 때만 별도 Skill 유지 근거가 된다.

- 입력 계약
- 산출물
- 승인/권한 경계
- failure semantics
- 검증 방법
- 사용자에게 제공하는 독립 가치

단순히 이름·예시·프레임워크가 다르다는 이유로 별도 Skill을 유지하지 않는다.

### 6. guard와 owner를 혼동하지 않는다

검증·적대 검토·보안 같은 guard는 분야 owner의 작성 책임을 빼앗지 않는다. guard가 필요한 단계에만 붙고, finding 구현은 원래 owner로 돌아간다.

따라서 `PLAN → BUILD → REVIEW` 전체에서 모든 Skill을 계속 유지하지 않는다. 단계가 바뀔 때 shortlist를 다시 계산한다.

## 예시

### 단일 게임 시스템 설계

```text
primary: analyzing-and-refining-game-concepts
supporting: 0~1 (실제 문서 정본 갱신이 현재 산출물이라면 managing-design-documents)
deferred: reviewing-and-validating-project-changes
```

검증 Skill을 PLAN 시작부터 미리 붙여 budget을 채우지 않는다.

### Base Skill 구조 최적화

```text
primary: evolving-project-discipline-skills
supporting: running-adversarial-review-and-refinement
second supporting: 기본 금지
```

문서 발행·Handoff·일반 검증이 실제 독립 산출물로 필요해진 시점에 재라우팅한다.

### 단순 오탈자

```text
primary/supporting: 없음 또는 해당 L0 owner 하나
full adversarial chain: 사용하지 않음
```

## 회귀 검사

- `python -m unittest tests.test_skill_routing_precision_policy -v`
- 기존 Skill behavior eval과 Base operating contract를 함께 통과해야 한다.
- 새 Skill 추가/통합 시 active count만 보지 말고 trigger overlap, negative trigger, owner 경계, actual shortlist를 검토한다.

## 성공 기준

정확도 개선을 “Skill 수 감소”로 대체 측정하지 않는다. 다음을 성공 신호로 사용한다.

- 불필요한 supporting Skill 연쇄 호출 감소
- 같은 책임의 중복 실행 감소
- close candidate에서 owner 선택 근거가 명시됨
- 단순 작업의 절차 비용 감소
- behavior eval에서 forbidden Skill 오선택이 증가하지 않음
- 검증·안전 hard guard 누락이 증가하지 않음

실제 모델 행동 정확도 향상은 별도 model-run eval 없이 `VERIFIED`로 주장하지 않는다.
