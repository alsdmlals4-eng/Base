# Base Controlled Vocabulary and Implementation Reality Gate Design

## 상태

- 승인 근거: 2026-08-14 사용자의 직접 Base 변경 요청과 후속 `진행해`
- 최초 설계 기준: `main@39936ff6a83410b4169878c1335de9eb3e4c25cf`
- 최신 재검토 기준: `main@b1317f2c1b83e57f016ce4efd4e169bf7c0acd90`
- 변경 등급: L1 공용 운영·용어 계약
- Existing Solution First 판정: `ABSORB`
- 신규 ACTIVE Skill·Work Mode·실행 Framework·Schema: 추가하지 않음

## 목표

Base와 채택 프로젝트에서 반복되는 긴 설명을 짧은 용어로 압축하되, 같은 단어가 서로 다른 단계·권한·증거를 뜻하지 않도록 한다. 특히 사용자가 실제 현업 용어와 Base 내부 압축명을 혼동하지 않도록 **외부 표준성·현업 관행·Base-local alias를 분리**한다.

`Implementation Reality Gate(IRG)`는 새 기능이나 업계 표준 용어가 아니라 기존 `claim-and-intent-verification` 계약을 찾기 쉽게 부르는 `BASE_LOCAL_ALIAS`로 고정한다.

## 해결할 문제

현재 Base에는 Work Mode·Skill·Skill Mode, Prototype·Vertical Slice·MVP·Demo, Gate·상태·Evidence 같은 중요한 구분이 여러 책임 원본에 분산되어 있다. 각 원본의 상세 정의는 유효하지만 다음 문제가 남는다.

1. 같은 용어를 찾기 위해 여러 문서를 순회해야 한다.
2. `Prototype`, `PoC`, `MVP`, `Vertical Slice`, `Demo`가 하나의 선형 단계처럼 오해될 수 있다.
3. Checklist·Gate·Gate Verdict·Implementation Status가 혼용될 수 있다.
4. 테스트 파일 존재나 정적 PASS를 실제 실행·런타임·UX 완료로 과장할 수 있다.
5. Base가 만든 압축명을 외부 업계 표준 용어처럼 오해할 수 있다.
6. 같은 용어를 각 Skill에 반복 정의하면 정의가 갈라지고 수정 전파 비용이 커진다.

## 검토한 접근

| 접근 | 장점 | 결함 | 판정 |
|---|---|---|---|
| 거대한 독립 용어사전 | 한 파일에서 많은 용어 검색 | 비관련 용어까지 컨텍스트를 차지하고 책임 원본과 쉽게 분기 | 제외 |
| 각 Skill에서 정의 반복 | 해당 Skill만 읽을 때 편함 | 중복·불일치·전파 누락 위험 | 제외 |
| 새 Terminology Skill | 자동 trigger를 붙이기 쉬움 | 독립 입력·산출물·승인·검증 경계가 없어 기존 owner와 중복 | 제외 |
| 얇은 통제 어휘 색인 + 기존 owner 링크 + 회귀 검사 | 한 단계 발견성, 낮은 중복, 기존 권한 보존 | 색인과 owner 일치 검사가 필요 | 채택 |

## 설계 원칙

### 1. Bounded Context

```text
BASE_SHARED
├─ Work Mode·Skill·Gate·Evidence·공용 제작/검증 용어
PROJECT_SHARED
├─ 프로젝트 시스템·데이터·UI·제작 파이프라인 용어
PROJECT_LORE
└─ 세계관·세력·캐릭터·지역·고유 설정 용어
```

Base는 `BASE_SHARED`만 직접 소유한다. 프로젝트별 실제 의미·수치·구현 상태와 세계관 고유명사는 프로젝트 책임 원본이 소유한다. 같은 표기가 다른 Context에서 다른 뜻이면 전체 이름 또는 Context prefix를 사용한다.

### 2. Controlled Vocabulary

`docs/CONTROLLED_VOCABULARY.md`는 빠른 정의와 owner 경로를 제공하는 얇은 색인이다. 상세 절차·상태·실제 결과를 복제하지 않는다.

모든 용어를 동일한 거대 Schema로 강제하지 않는다. 대신 용어군별로 혼동을 막는 최소 필드를 사용한다.

- 운영·권한: Kind, 압축 정의, 금지 의미, owner
- 제작·실험: 핵심 질문, 증명하지 못하는 것, 조직별 보정 필요 여부
- 완료·검증: 압축 정의, Evidence ceiling, fail-closed 경계
- Base-local alias: 외부 표준이 아님을 명시하고 기존 owner를 연결

새 용어는 **범위, 산출물, 필요한 Evidence, 다음 Gate** 중 하나 이상이 기존 용어와 실제로 다를 때만 추가한다.

### 3. 용어 출처 성격

- `STANDARDIZED_CONTEXT`: 특정 표준·전문기관 문맥에서 명시적으로 정의된 용어
- `INDUSTRY_COMMON`: 현업에서 널리 쓰이지만 조직별 경계가 달라질 수 있는 용어
- `BASE_LOCAL_ALIAS`: Base의 기존 계약을 짧게 호출하기 위한 내부 압축명

이 분류는 “유용한 용어”와 “외부 표준 용어”를 동일시하지 않기 위한 안전장치다.

### 4. 권한 보존

통제 어휘는 기존 책임 원본을 대체하지 않는다.

- Work Mode·Skill·Skill Mode: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- 작업 생명주기·제품 단계·Evidence ceiling: `docs/OPERATING_MODEL.md`
- Vertical Slice: `skills/designing-vertical-slices/SKILL.md`
- 구현·검증 완료 주장: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- 문서 위치·책임: `docs/DOCUMENTATION_MAP.md`

색인과 owner가 충돌하면 owner가 우선하며, 충돌 자체는 색인 회귀로 수정한다. 새 공용 책임 원본을 만들면 `START_HERE.md`의 사용자 라우팅과 `docs/DOCUMENTATION_MAP.md`의 위치·책임 지도를 함께 갱신한다.

## 핵심 용어군

### 운영·권한

`Work Mode`, `Skill`, `Skill Mode`, `Product Stage`, `Gate`, `Gate Verdict`, `Implementation Status`, `Canonical Source`, `Decision Record`, `ADR`, `Work Contract`, `Golden Path`.

### 기획·대안 비교

`Design Space Exploration`, `Diverge–Converge`, `Riskiest Assumption`, `Riskiest Assumption Test`, `Kill Criteria`, `Decision Gate`.

### 제작·실험·제품 단계

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

`First Playable`, `Demo`, `Vertical Slice`처럼 조직별 편차가 큰 표현은 프로젝트가 범위·품질선·Entry/Exit Criteria를 별도로 고정한다.

### 완료·검증

`Acceptance Criteria`, `Entry Criteria`, `Exit Criteria`, `Definition of Done`, `Verification`, `Validation`, `Bidirectional Traceability`, `Evidence Provenance`, `Evidence Ceiling`, `Fail-Closed`, `Assurance Case`, `Regression Recheck`, `Implementation Reality Gate`.

## Implementation Reality Gate

`Implementation Reality Gate`, 약칭 `IRG`는 `BASE_LOCAL_ALIAS`다. 업계 표준 용어가 아니며 새 ACTIVE Skill·Work Mode·제품 단계가 아니다. 기존 `reviewing-and-validating-project-changes: claim-and-intent-verification`이 소유하는 다음 계약을 한 문장으로 호출한다.

```text
MATERIAL_CLAIM_LEDGER
+ INTENT_IMPLEMENTATION_FIDELITY_MATRIX
+ COMPLETION_CLAIM_GATE
```

```text
Implementation Reality Gate
=
승인 Intent·Acceptance
↔ 실제 Diff·구현 경로
+ exact-HEAD fresh execution
+ Evidence Provenance
+ Evidence Ceiling
+ 보호·범위 밖 변경 부재
+ merged PR·merge SHA
+ post-merge main readback
```

Evidence가 부족하면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`, `BLOCKED_UNVERIFIED`를 유지한다.

## 금지 용례

1. 거친 Prototype을 실제 사용자 학습 없는 MVP라고 부르지 않는다.
2. 공개 가능한 Demo를 자동으로 Vertical Slice라고 부르지 않는다.
3. Walking Skeleton의 종단 연결을 목표 품질 증명으로 승격하지 않는다.
4. Checklist를 단계 전환 판정인 Gate라고 부르지 않는다.
5. 테스트 파일 존재를 테스트 실행 증거로 부르지 않는다.
6. 정적 PASS를 runtime·render·UX·재미 PASS로 승격하지 않는다.
7. 모든 의사결정 문서를 ADR이라고 부르지 않는다.
8. 적대적 검토를 Red Team 공격 하나로 축약하지 않는다.
9. `DDD`는 단독 사용하지 않는다.
10. 책임·권한·수명주기 조율이 없는 단일 도구를 Framework·Platform·Control Plane으로 과장하지 않는다.
11. `BASE_LOCAL_ALIAS`를 외부 표준·업계 공인 용어처럼 소개하지 않는다.

## 구현 범위

### 생성

- `docs/CONTROLLED_VOCABULARY.md`
- `docs/superpowers/specs/2026-08-14-controlled-vocabulary-and-irg-design.md`
- `docs/superpowers/plans/2026-08-14-controlled-vocabulary-and-irg.md`
- `tests/test_controlled_vocabulary_contract.py`

### 수정

- `START_HERE.md`
- `docs/DOCUMENTATION_MAP.md`

### 의도적으로 미수정·보호

- `AGENTS.md`
- `skills/**`
- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `schemas/**`
- `.github/workflows/**`
- released lock·frozen release artifact
- 프로젝트 고유 문서·게임 코드·데이터·Scene·Resource·자산

`docs/DOCUMENTATION_MAP.md`는 문서 위치·책임의 상위 정본이므로 적대적 재검토에서 누락을 `MUST_FIX`로 판정했다. 따라서 `START_HERE.md`의 한 단계 사용자 라우팅과 함께 Map의 공용 책임 원본 표에도 `docs/CONTROLLED_VOCABULARY.md`를 등록한다. 이 수정은 새 실행 owner를 만들지 않고 발견성과 권한 일치만 보강한다.

## 완료 기준

1. 공용 용어를 `docs/CONTROLLED_VOCABULARY.md`에서 한 단계로 찾을 수 있다.
2. Work Mode·Skill·Skill Mode·제품 단계·Gate·Verdict·Status가 분리된다.
3. Prototype부터 Release Candidate까지 서로 다른 검증 질문이 구분되고 MVP는 실제 사용자 학습을 요구한다.
4. IRG가 `BASE_LOCAL_ALIAS`로 명시되고 기존 검증 owner에 연결되며 새 Skill·Mode가 생기지 않는다.
5. `START_HERE.md`와 `docs/DOCUMENTATION_MAP.md`가 새 정본을 직접 찾게 한다.
6. semantic regression이 정본·양쪽 라우팅·금지된 새 Skill 등록·핵심 용어·IRG fail-closed 경계를 검사한다.
7. exact-head CI, 적대적 검토, unresolved thread 0, 현재 main 충돌 검사를 통과한다.
8. 병합 뒤 새 main에서 파일·용어·merge SHA와 필수 검사를 재조회한다.

## 검증 전략

```text
RED
- semantic regression을 먼저 추가한다.
- IRG의 BASE-local 표준성 경계와 Documentation Map 등록이 없으면 실패하도록 고정한다.

GREEN
- 통제 어휘에 source class와 IRG의 BASE_LOCAL_ALIAS 경계를 추가한다.
- START_HERE와 Documentation Map을 같은 canonical route로 맞춘다.
- exact-head CI로 새 regression과 기존 Base 계약을 함께 검증한다.

REVIEW
- actual diff와 승인 범위를 Acceptance별 연결한다.
- 동일 Goal PR과 untouched consumer를 재검사한다.
- 용어 중복·권한 탈취·과장·모호성을 attack → validate-critique로 검토한다.
- 수정 뒤 regression-recheck를 실행한다.

INTEGRATION
- 검토한 exact HEAD만 squash merge한다.
- merge SHA와 새 main readback을 확인한다.
```

## 롤백

단일 squash merge를 revert한다. 신규 Skill·Registry·Schema·프로젝트 데이터·마이그레이션이 없으므로 롤백은 문서·test route에 한정된다.

## 외부 근거

- W3C SKOS: controlled vocabulary의 concept, preferred/alternative label, definition, concept scheme 구조.
- Domain-Driven Design의 Bounded Context/Ubiquitous Language: 같은 단어의 의미를 명시적 context 경계 안에서 통일하고 context 사이의 번역을 관리.
- Scrum Guide 2020: Definition of Done을 Increment의 품질·완료 투명성에 사용하는 공식 문맥.
- ISTQB Glossary: 테스트 분야에서 공통 용어집을 권위 있는 참조로 유지하는 실무 사례.
- Lean Startup의 MVP: 단순히 기능 수가 적은 빌드가 아니라 실제 고객과 핵심 가치 가설을 학습하는 최소 제품이라는 구분.
- Microsoft의 PoC guidance: 생산 구현 전 위험·미지수를 작은 검증으로 줄이는 접근.
- SLSA provenance와 NIST assurance case: Evidence의 생성 근거와 주장–논증–증거 연결을 추적하는 사례.

외부 용어는 Base 권한을 대체하지 않는다. 현재 Base 문제에 필요한 경계·검증 질문·증거 규칙만 `ADOPT / ADAPT / AVOID` 판정으로 흡수한다.
