# Base Controlled Vocabulary and Implementation Reality Gate Design

## 상태

- 승인 근거: 2026-08-14 사용자의 직접 Base 변경 요청과 후속 `진행해`
- 기준 Base: `main@39936ff6a83410b4169878c1335de9eb3e4c25cf`
- 변경 등급: L1 공용 운영·용어 계약
- Existing Solution First 판정: `ABSORB`
- 신규 ACTIVE Skill·Work Mode·실행 Framework: 추가하지 않음

## 목표

Base와 채택 프로젝트에서 반복되는 긴 설명을 짧은 현업 용어로 압축하되, 같은 단어가 서로 다른 단계·권한·증거를 뜻하지 않도록 한다. `Implementation Reality Gate`는 새 기능이 아니라 기존 `claim-and-intent-verification`과 `COMPLETION_CLAIM_GATE`를 찾기 쉽게 부르는 공용 압축명으로 고정한다.

## 해결할 문제

현재 Base에는 Work Mode·Skill·Skill Mode, Prototype·Vertical Slice·MVP·Demo, Gate·상태·Evidence 같은 중요한 구분이 여러 책임 원본에 분산되어 있다. 각 원본의 상세 정의는 유효하지만 다음 문제가 남는다.

1. 같은 용어를 찾기 위해 여러 문서를 순회해야 한다.
2. `Prototype`, `PoC`, `MVP`, `Vertical Slice`, `Demo`가 하나의 선형 단계처럼 오해될 수 있다.
3. Checklist·Gate·Gate Verdict·Implementation Status가 혼용될 수 있다.
4. 테스트 파일 존재나 정적 PASS를 실제 구현·런타임·UX 완료로 과장할 수 있다.
5. 같은 용어를 각 Skill에 반복 정의하면 정의가 갈라지고 수정 전파 비용이 커진다.

## 검토한 접근

| 접근 | 장점 | 결함 | 판정 |
|---|---|---|---|
| 거대한 독립 용어사전 | 한 파일에서 많은 용어 검색 | 비관련 용어까지 컨텍스트를 차지하고 책임 원본과 쉽게 분기 | 제외 |
| 각 Skill에서 정의 반복 | 해당 Skill만 읽을 때 편함 | 중복·불일치·전파 누락 위험 | 제외 |
| 새 Terminology Skill | 자동 trigger를 붙이기 쉬움 | 독립 입력·산출물·승인·검증 경계가 없어 기존 owner와 중복 | 제외 |
| 얇은 통제 어휘 색인 + 기존 owner 링크 + 회귀 검사 | 한 단계 발견성, 낮은 중복, 기존 권한 보존 | 색인과 owner 일치 검사가 필요 | 채택 |

## 설계 원칙

### 1. Bounded Context

공용 용어는 적용 경계를 먼저 선언한다.

```text
BASE_SHARED
├─ Work Mode·Skill·Gate·Evidence·공용 제작/검증 용어
PROJECT_SHARED
├─ 프로젝트 시스템·데이터·UI·제작 파이프라인 용어
PROJECT_LORE
└─ 세계관·세력·캐릭터·지역·고유 설정 용어
```

Base는 `BASE_SHARED`만 직접 소유한다. 프로젝트별 실제 의미·수치·구현 상태와 세계관 고유명사는 프로젝트 책임 원본이 소유한다. 같은 표기가 다른 context에서 다른 뜻이면 전체 이름 또는 context prefix를 사용한다.

### 2. Controlled Vocabulary

`docs/CONTROLLED_VOCABULARY.md`는 빠른 정의와 owner 경로를 제공하는 얇은 색인이다. 상세 절차·상태·실제 결과를 복제하지 않는다.

용어 레코드의 최소 필드는 다음과 같다.

```yaml
term_id:
kind: ACTIVITY | ARTIFACT | PRODUCT_STAGE | GATE | VERDICT | STATUS | EVIDENCE
bounded_context:
canonical_name:
korean_name:
one_line_definition:
answers_question:
use_when:
do_not_use_when:
required_evidence:
canonical_owner:
allowed_aliases:
forbidden_meanings:
status: ACTIVE | PROJECT_LOCAL | LEGACY | REJECTED
```

새 용어는 다음 중 하나 이상을 명확히 바꿀 때만 추가한다.

- 적용 범위
- 산출물
- 필요한 증거
- 다음 Gate 또는 결정

어느 것도 달라지지 않으면 새 용어를 만들지 않고 기존 용어의 설명·별칭을 보완한다.

### 3. 권한 보존

통제 어휘는 기존 책임 원본을 대체하지 않는다.

- Work Mode·Skill·Skill Mode: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- 작업 생명주기·제품 단계·Evidence ceiling: `docs/OPERATING_MODEL.md`
- Vertical Slice: `skills/designing-vertical-slices/SKILL.md`
- 구현·검증 완료 주장: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- 문서 위치·책임: `docs/DOCUMENTATION_MAP.md`

색인과 owner가 충돌하면 owner가 우선하며, 충돌 자체는 색인 회귀로 수정한다.

## 핵심 용어군

### 운영·권한

`Work Mode`, `Skill`, `Skill Mode`, `Protocol`, `Execution Flag/State`, `Product Stage`, `Gate`, `Gate Verdict`, `Implementation Status`, `Canonical Source`, `Canonical Owner`, `Decision Record`, `ADR`, `Work Contract`, `Golden Path`.

### 기획·대안 비교

`Design Space Exploration`, `Diverge–Converge`, `Riskiest Assumption`, `Riskiest Assumption Test`, `Kill Criteria`, `Decision Gate`.

### 제작·실험

`Prototype`, `Spike`, `Proof of Concept`, `Walking Skeleton`, `Graybox/Blockout`, `First Playable`, `Vertical Slice`, `MVP`, `Demo`, `Release Candidate`.

이 용어들은 강제 선형 단계가 아니라 서로 다른 질문을 증명하는 도구다.

```text
Spike             = 무엇을 알아내야 하는가?
PoC               = 가장 위험한 가설이 조건 안에서 가능한가?
Walking Skeleton  = 최소 종단 경로가 실제로 연결되는가?
Graybox           = 공간·동선·거리·시야가 작동하는가?
First Playable    = 핵심 루프를 처음부터 끝까지 완주할 수 있는가?
Vertical Slice    = 대표 경험의 목표 품질과 반복 제작성을 증명했는가?
MVP               = 실제 목표 사용자와 핵심 가치 가설을 학습할 수 있는가?
Demo              = 외부 플레이어가 제품 약속을 이해하고 더 원하게 되는가?
Release Candidate = 차단 결함이 없다면 그대로 출시 가능한가?
```

`First Playable`은 조직별 사용 차이가 크므로 기본 정의를 제공하되 프로젝트가 범위와 품질선을 별도로 고정한다.

### 완료·검증

`Acceptance Criteria`, `Entry Criteria`, `Exit Criteria`, `Definition of Done`, `Verification`, `Validation`, `Bidirectional Traceability`, `Evidence Provenance`, `Evidence Ceiling`, `Fail-Closed`, `Assurance Case`, `Regression Recheck`, `Implementation Reality Gate`.

## Implementation Reality Gate

`Implementation Reality Gate`, 약칭 `IRG`는 새 ACTIVE Skill·Work Mode·제품 단계가 아니다. 기존 `reviewing-and-validating-project-changes: claim-and-intent-verification`이 소유하는 `MATERIAL_CLAIM_LEDGER`, `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`, `COMPLETION_CLAIM_GATE`를 한 문장으로 호출하는 공용 압축명이다.

```text
Implementation Reality Gate
=
승인 Intent·Acceptance
↔ 실제 Diff·구현 경로
+ exact-HEAD fresh execution
+ Evidence provenance
+ Evidence ceiling
+ 범위 밖 변경 부재
+ post-merge main readback
```

최소 판정 규칙:

- 구현 완료: actual diff, Acceptance별 implementation path, 보호·제외 범위 보존
- 검증 완료: 명령, 환경, exact HEAD, 새 실행 결과, 실패·skip 수
- 의도 적합: Acceptance별 관찰 결과와 필요한 Evidence level
- 통합 완료: merged PR 상태, merge SHA, 새 main readback, post-merge 필수 검사
- 증거 부족: `BLOCKED_UNVERIFIED`; 반증이 없다는 이유로 PASS 금지

## 금지 용례

1. 거친 Prototype을 실제 사용자 학습 없는 MVP라고 부르지 않는다.
2. 공개 가능한 Demo를 자동으로 Vertical Slice라고 부르지 않는다.
3. Walking Skeleton의 종단 연결을 목표 품질 증명으로 승격하지 않는다.
4. Checklist를 단계 전환 판정인 Gate라고 부르지 않는다.
5. 테스트 파일 존재를 테스트 실행 증거로 부르지 않는다.
6. 정적 PASS를 runtime·render·UX·재미 PASS로 승격하지 않는다.
7. 모든 의사결정 문서를 ADR이라고 부르지 않는다. ADR은 기술 구조·장기 기술 제약 Decision Record에 한정한다.
8. 적대적 검토를 공격 역할인 Red Team 하나로 축약하지 않는다. attack 뒤 critique 검증·최소 수정·회귀 재검사가 필요하다.
9. `DDD`는 단독 사용하지 않는다. `Digital Dopamine Design`과 `Domain-Driven Design` 중 전체 이름 또는 context prefix를 쓴다.
10. 책임·권한·수명주기 조율이 없는 단일 도구를 Framework·Platform·Control Plane으로 과장하지 않는다.

## 변경 범위

### 생성

- `docs/CONTROLLED_VOCABULARY.md`
- `docs/superpowers/specs/2026-08-14-controlled-vocabulary-and-irg-design.md`
- `docs/superpowers/plans/2026-08-14-controlled-vocabulary-and-irg.md`

### 수정

- `START_HERE.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `skills/designing-vertical-slices/SKILL.md`
- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `tests/test_v9_governance_documents.py`
- `docs/CHANGELOG.md`

### 제외·보호

- `AGENTS.md`
- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- released lock·frozen release artifact
- 프로젝트 고유 문서·게임 코드·데이터·Scene·Resource·자산
- PR #333, #336, #337 소유 경로

## 완료 기준

1. 공용 용어를 `docs/CONTROLLED_VOCABULARY.md`에서 한 단계로 찾을 수 있다.
2. 모든 용어는 kind·context·짧은 정의·질문·비사용 의미·owner를 가진다.
3. Work Mode·Skill·Skill Mode·제품 단계·Gate·Verdict·Status가 분리된다.
4. Prototype부터 Release Candidate까지 서로 다른 검증 질문이 구분되고 MVP는 실제 사용자 학습을 요구한다.
5. IRG가 기존 검증 owner의 별칭으로 연결되고 새 Skill·Mode가 생기지 않는다.
6. `START_HERE.md`와 `DOCUMENTATION_MAP.md`가 새 정본을 찾게 한다.
7. 회귀 테스트가 정본·라우팅·금지된 새 Skill 등록·핵심 정의를 검사한다.
8. exact-head CI, 독립 적대적 검토, unresolved thread 0, 현재 main 충돌 검사를 통과한다.
9. 병합 뒤 새 main에서 파일·용어·merge SHA와 필수 검사를 재조회한다.

## 검증 전략

```text
RED
- 회귀 테스트를 먼저 추가한다.
- 새 정본과 라우팅이 아직 없어 예상한 이유로 실패함을 exact-head CI에서 확인한다.

GREEN
- 새 정본과 최소 owner/route 수정만 추가한다.
- focused governance test와 Base v9 contract workflow를 통과시킨다.

REVIEW
- 실제 diff와 승인 범위를 Acceptance별 연결한다.
- 동일 Goal PR과 untouched consumer를 재검사한다.
- 용어 중복·권한 탈취·과장·모호성을 attack → validate-critique로 검토한다.
- 수정 뒤 regression-recheck를 실행한다.

INTEGRATION
- 검토한 exact HEAD만 squash merge한다.
- merge SHA와 새 main readback을 확인한다.
```

## 롤백

단일 squash merge를 revert한다. 신규 Skill·Registry·Schema·프로젝트 데이터·마이그레이션이 없으므로 롤백은 문서·테스트 경로에 한정된다. 되돌린 뒤 `START_HERE.md`, `DOCUMENTATION_MAP.md`, 검증 reference, Vertical Slice 구분표와 회귀 테스트가 함께 이전 상태로 복원됐는지 확인한다.

## 외부 근거

- Martin Fowler, *Bounded Context*: 큰 모델을 명시적 경계로 나누고 각 경계 안에서 통일된 모델·언어를 유지하며 context map으로 관계를 표현한다.
- Design Council, *Framework for Innovation*: Double Diamond는 문제·해법을 확산한 뒤 수렴하는 비선형 탐색 구조다.
- Scrum Guide, November 2020 official current version: Definition of Done은 품질 기준과 완료 투명성에 사용한다. Base의 단계 진입 조건은 더 일반적인 `Entry Criteria`를 정식명으로 두고 `Definition of Ready`는 호환 별칭으로 다룬다.
- AWS Prescriptive Guidance, *Architectural decision record process*: ADR은 중요한 기술·아키텍처 결정의 맥락·선택·결과를 기록하는 Decision Record다.
- Lean Startup Co., *What Is an MVP?*: MVP는 단순히 기능이 적은 빌드가 아니라 실제 고객과 핵심 가설을 학습하기 위한 최소 제품이다.
- Microsoft Learn, *Build a proof of concept*: PoC는 상위 위험과 미지수를 작은 실험으로 검증하고 생산 구현 전에 가능성을 판단한다.
- SLSA v1.2 Provenance: Evidence provenance는 산출물이 어디서·언제·어떻게 생성됐는지 추적하는 근거다.
- NIST CSRC, *assurance case*: 상위 주장과 구조화된 논증·증거·가정을 감사 가능하게 연결한다.

외부 용어는 Base 권한을 대체하지 않는다. 현재 Base 문제에 필요한 경계·검증 질문·증거 규칙만 `ADOPT / ADAPT / AVOID` 판정으로 흡수한다.
