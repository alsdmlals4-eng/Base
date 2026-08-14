# Base 공용 통제 어휘

이 문서는 반복되는 긴 작업 계약을 짧은 용어로 호출하기 위한 **Controlled Vocabulary**다. 한 줄 정의·적용 경계·금지 의미·기존 책임 원본을 연결하며, 상세 절차와 프로젝트 실제 상태는 복제하지 않는다.

```text
통제 어휘
= 빠른 탐색·컨텍스트 압축·용어 충돌 방지
≠ 새 Work Mode·Skill·Skill Mode·Gate·제품 단계
≠ 프로젝트 구현·수치·세계관의 두 번째 정본
≠ 여기 적힌 모든 표현이 외부 업계 표준이라는 주장
```

## Bounded Context

**Bounded Context**는 같은 용어가 같은 뜻을 보장받는 경계다.

| Context | 소유 내용 |
|---|---|
| `BASE_SHARED` | 공용 작업 구조, Skill, Gate, Evidence, 재사용 가능한 제작·검증 용어 |
| `PROJECT_SHARED` | 프로젝트 시스템·데이터·UI·제작 파이프라인 용어 |
| `PROJECT_LORE` | 세계관·세력·캐릭터·지역·설정 고유명사 |

**Ubiquitous Language**는 한 Context 안에서 사용자·기획·Issue·문서·코드·데이터·테스트가 함께 쓰는 공통 언어다. 같은 표기가 다른 Context에서 다른 뜻이면 전체 이름이나 Context prefix를 사용한다. 예를 들어 `DDD`는 `Digital Dopamine Design`과 `Domain-Driven Design` 중 하나를 풀어 써야 한다.

새 용어는 기존 용어와 **범위, 산출물, 필요한 Evidence, 다음 Gate** 중 하나 이상이 실제로 다를 때만 추가한다.

## 용어 출처 성격

Base는 용어의 **유용성**과 **외부 표준성**을 구분한다.

| Class | 의미 | 사용 규칙 |
|---|---|---|
| `STANDARDIZED_CONTEXT` | 특정 표준·가이드·전문기관 문맥에서 명시적으로 정의된 용어 | 그 문맥을 벗어나 보편 표준처럼 과장하지 않는다. |
| `INDUSTRY_COMMON` | 현업에서 널리 쓰이지만 조직·분야별 경계가 달라질 수 있는 용어 | 프로젝트가 Entry/Exit Criteria와 품질선을 필요하면 추가 고정한다. |
| `BASE_LOCAL_ALIAS` | 기존 Base 계약을 짧게 호출하기 위해 Base가 정한 압축명 | 외부 업계 표준처럼 소개하지 않고 반드시 기존 owner로 연결한다. |

별도 표시가 없다는 이유로 어떤 용어를 국제 표준·업계 공인 정의라고 추정하지 않는다. 특히 **Implementation Reality Gate(IRG)는 `BASE_LOCAL_ALIAS`이며 업계 표준 용어가 아니다.**

### 권한 분리

이 문서는 `BASE_SHARED`의 **교차 분야 압축명과 용어 간 차이**를 소유한다. 연결된 Skill·reference는 각 용어의 상세 절차·입력·산출물·판정을 계속 소유한다.

- `skills/designing-vertical-slices/SKILL.md`는 Vertical Slice 실행 절차를 소유하지만 MVP·Demo·Release Candidate 전체의 공용 명명 규칙을 소유하지 않는다.
- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`는 완료 주장 검증 절차를 소유하고, 이 문서는 그 기존 계약을 부르는 `Implementation Reality Gate` 압축명을 소유한다.
- 프로젝트가 다른 뜻을 채택해야 하면 Base 정의를 조용히 덮어쓰지 않고 `PROJECT_SHARED` Context와 번역 규칙을 기록한다.

## 운영·권한

| 용어 | Kind | 압축 정의 | 사용하지 않을 의미 | Canonical owner |
|---|---|---|---|---|
| **Work Mode** | STATUS | 현재 작업자의 주된 자세·권한·Evidence 기준 | 제품 개발 단계 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` |
| **Skill** | ARTIFACT | 반복 책임의 trigger·입력·절차·산출물·실패·검증 계약 | 단순 참고 문서 | `skills/SKILL_REGISTRY.json`과 해당 `SKILL.md` |
| **Skill Mode** | STATUS | 한 Skill 안에서 선택하는 세부 절차·권한 | 독립 Skill | 해당 `SKILL.md` |
| **Product Stage** | PRODUCT_STAGE | 제품이 무엇을 증명해야 하는 단계인지 나타내는 상태 | PLAN·BUILD·REVIEW | `docs/OPERATING_MODEL.md`와 분야 owner |
| **Gate** | GATE | Evidence로 진입·확장·보류·중단을 판단하는 경계 | Checklist·단순 단계 이름 | Gate를 선언한 owner |
| **Gate Verdict** | VERDICT | Gate의 승인·재작업·보류·중단·미검증 판정 | 구현 진행률 | Gate를 선언한 owner |
| **Implementation Status** | STATUS | 실제 구현 범위의 존재·완성·보류·미검증 상태 | 승인 여부 | 프로젝트 실제 파일·상태 정본 |
| **Canonical Source** | ARTIFACT | 현재 질문의 답을 소유하는 단일 책임 원본 | 참고 자료 전체 | `docs/DOCUMENTATION_MAP.md` |
| **Decision Record, DR** | ARTIFACT | 결정의 맥락·대안·선택·영향을 남기는 결정 영수증 | 단순 메모 | 결정 분야 owner |
| **Architecture Decision Record, ADR** | ARTIFACT | 기술 구조와 장기 기술 제약을 다루는 DR | 모든 기획 결정 | 기술 owner |
| **Work Contract** | ARTIFACT | 목표·범위·보호·완료·검증·롤백을 닫는 실행 계약 | 아이디어 메모 | `managing-project-intake-and-work-contract` |
| **Golden Path** | ACTIVITY | 판단 비용과 오류를 줄이는 기본 권장 경로 | 예외를 금지하는 강제 경로 | 해당 운영 owner |

```text
Work Mode = 작업자의 현재 자세
Product Stage = 제품이 증명해야 할 단계
Gate = 단계 전환 판단
Gate Verdict = 그 판단 결과
Implementation Status = 실제 구현 상태
```

## 기획·대안 비교

| 용어 | 압축 정의 |
|---|---|
| **Design Space Exploration** | 한 답에 착수하기 전에 유효한 해법 공간을 펼쳐 같은 기준으로 비교하는 과정 |
| **Diverge–Converge** | 대안을 넓게 만든 뒤 Evidence·제약·평가 기준으로 좁히는 리듬 |
| **Riskiest Assumption** | 틀리면 계획 전체가 무너지는 가장 위험한 전제 |
| **Riskiest Assumption Test** | 가장 위험한 전제를 가장 싸고 빠르게 반증하는 시험 |
| **Kill Criteria / Stop Rule** | 결과를 보기 전에 고정한 중단·보류·재설계 조건 |
| **Decision Gate** | Evidence로 확장·재작업·반복·보류·중단을 선택하는 지점 |

## 프로젝트 관리·작업 단위

Scrum의 공식 용어와 일반 현업 용어를 섞지 않는다. Scrum 문맥에서 `Sprint`, `Product Backlog`처럼 Guide가 정의하는 표현은 `STANDARDIZED_CONTEXT`로 다루고, 일반 조직에서 폭넓게 쓰이는 `Milestone`, `Epic`, `User Story`, 일반 `Backlog`는 `INDUSTRY_COMMON`으로 다룬다.

| 용어 | Class | 압축 정의 | 혼동 방지 |
|---|---|---|---|
| **Milestone** | `INDUSTRY_COMMON` | 중요한 결과·의존성·날짜 또는 승인 지점을 묶어 진행 상태를 판단하는 체크포인트 | 일정 길이를 가진 반복 개발 주기와 동일하지 않음 |
| **Sprint** | `STANDARDIZED_CONTEXT (Scrum)` | Scrum에서 한 달 이하의 고정 길이로 반복되는 이벤트이며 Sprint Goal을 중심으로 가치 있는 Increment를 만든다 | 단순한 1~2주 마감·Milestone의 동의어가 아님 |
| **Product Backlog** | `STANDARDIZED_CONTEXT (Scrum)` | 제품 개선에 필요한 작업의 등장·변화를 허용하는 정렬된 목록 | 일반 업무 대기열 전체와 자동으로 동일하지 않음 |
| **Backlog** | `INDUSTRY_COMMON` | 아직 착수하지 않았거나 우선순위 결정을 기다리는 작업·요구·아이디어의 대기 목록 | Scrum Product Backlog를 쓴다는 선언 없이 동일시하지 않음 |
| **Epic** | `INDUSTRY_COMMON` | 여러 Story·Task·요구를 묶을 만큼 큰 목표·기능·가치 단위 | Scrum이 요구하는 공식 Artifact가 아님 |
| **User Story** | `INDUSTRY_COMMON` | 사용자 관점의 가치·필요를 짧게 표현해 대화와 상세화의 출발점으로 삼는 요구 표현 | 전체 요구 명세·Acceptance Criteria·설계서 자체가 아님 |

```text
Sprint ≠ Milestone
Product Backlog ≠ 모든 Backlog
User Story ≠ 전체 명세
Epic과 User Story는 Scrum Guide의 필수 Artifact가 아니다.
```

## 제작·실험·제품 단계

이 용어들은 강제 선형 단계가 아니라 서로 다른 검증 질문이다. `First Playable`, `Demo`, `Vertical Slice`처럼 스튜디오마다 경계가 달라질 수 있는 표현은 `INDUSTRY_COMMON`으로 보고 프로젝트 계약에서 품질선과 Entry/Exit Criteria를 고정한다.

| 용어 | 핵심 질문 | 증명하지 못하는 것 |
|---|---|---|
| **Prototype** | 아이디어·규칙·상호작용을 시험할 수 있는가? | 목표 품질·시장성 |
| **Spike** | 결정을 위해 무엇을 알아내야 하는가? | 제품 기능 완료 |
| **Proof of Concept** | 가장 위험한 가설이 조건 안에서 가능한가? | 전체 경험·반복 제작성 |
| **Walking Skeleton** | 입력부터 결과까지 최소 종단 경로가 연결되는가? | 목표 아트·UX·재미 품질 |
| **Graybox / Blockout** | 공간·동선·거리·시야·교전 배치가 작동하는가? | 최종 시각 품질 |
| **First Playable** | 핵심 루프를 처음부터 끝까지 완주할 수 있는가? | 목표 품질·시장 검증 |
| **Vertical Slice** | 대표 경험·목표 품질·통합·실제 플레이·반복 제작성을 증명했는가? | 전체 게임 분량 |
| **Minimum Viable Product, MVP** | 실제 목표 사용자와 핵심 가치 가설을 학습할 수 있는가? | 기능 수가 적다는 사실만으로는 부족 |
| **Demo** | 외부 플레이어가 제품 약속을 이해하고 더 원하게 되는가? | 전체 제작 준비 |
| **Release Candidate** | 차단 결함이 없다면 그대로 출시 가능한가? | 최종 출시 승인 자체 |

Vertical Slice 상세 owner는 `skills/designing-vertical-slices/SKILL.md`다. `First Playable`처럼 조직별 편차가 큰 용어는 프로젝트가 범위·품질선·Entry/Exit Criteria를 별도로 고정한다.

## 출시 단계·배포 상태

`Alpha`, `Beta`, `Gold / Gold Master`는 조직·플랫폼마다 경계가 달라지는 `INDUSTRY_COMMON` 표현이다. Base는 이를 보편적 선형 단계로 강제하지 않는다. **Alpha·Beta는 조직별 Entry/Exit Criteria**와 대상 사용자·안정성·콘텐츠 범위를 프로젝트가 명시해야 한다. `Release Candidate`는 위 `제작·실험·제품 단계`의 기존 canonical row를 재사용한다.

| 용어 | Class | 압축 정의 | 증명하지 못하는 것 |
|---|---|---|---|
| **Alpha** | `INDUSTRY_COMMON` | 핵심 기능·루프가 실제로 시험 가능하지만 기능·콘텐츠·안정성이 아직 크게 변할 수 있는 개발·검증 상태 | 기능 완성·시장 공개 준비를 자동 보장하지 않음 |
| **Beta** | `INDUSTRY_COMMON` | 더 넓은 사용·호환성·안정성·밸런스·콘텐츠 검증을 수행하는 후기 개발 상태 | 모든 기능 완료·출시 승인을 자동 의미하지 않음 |
| **Early Access** | `STANDARDIZED_CONTEXT (platform-specific)` + `INDUSTRY_COMMON` | 완성 전 플레이 가능한 제품을 고객에게 제공하면서 개발을 계속하는 상업·배포 상태; 플랫폼별 정책이 의미를 추가로 제한한다 | 단순 테스트 단계·예약 구매·미래 약속의 판매를 의미하지 않음 |
| **Gold / Gold Master** | `INDUSTRY_COMMON / HISTORICAL` | 조직이 출시·복제·배포의 기준본으로 승인한 마스터 상태를 가리키는 전통적 표현 | 아직 승인 전인 Release Candidate와 동일하지 않음 |

Steam 문맥의 Early Access는 개발 중인 미완성 제품을 현재 플레이 가능한 상태로 판매하는 별도 출시 방식이다. Alpha/Beta라는 내부 품질 단계와 플랫폼의 Early Access 상업 상태를 동일 축으로 취급하지 않는다. 디지털 라이브 배포에서는 `Gold / Gold Master`를 사용하지 않는 팀도 있으므로 프로젝트가 실제 release vocabulary를 선언한다.

```text
Early Access ≠ Beta
Early Access ≠ Pre-Purchase
Gold / Gold Master ≠ Release Candidate
```

## 테스트 범위·목적

테스트 용어는 **무엇을 연결해 검증하는가**, **왜 실행하는가**, **누가 수용 판정을 내리는가**를 분리한다. 테스트 파일 개수나 실행 시간만으로 level을 정하지 않는다.

| 용어 | Class | 압축 정의 | 사용하지 않을 의미 |
|---|---|---|---|
| **Component Test** | `STANDARDIZED_CONTEXT (ISTQB)` | 개별 소프트웨어 컴포넌트의 동작을 분리해 검증 | 빠른 테스트 전체 |
| **Unit Test** | `INDUSTRY_COMMON` | 팀이 정의한 작은 코드 단위의 동작을 외부 의존성에서 최대한 분리해 검증 | 모든 조직에서 Component Test와 반드시 같은 범위 |
| **Integration Test** | `STANDARDIZED_CONTEXT (ISTQB)` | 둘 이상의 컴포넌트·모듈·서비스·시스템 사이 인터페이스와 상호작용을 검증 | 단순히 테스트 파일이 큰 경우 |
| **End-to-End / E2E Test** | `INDUSTRY_COMMON` | 사용자·업무 흐름의 입력부터 최종 결과까지 여러 실제 통합 경계를 관통해 검증 | 모든 하위 실패 원인을 정밀 격리하는 테스트 |
| **Smoke Test** | `INDUSTRY_COMMON` | 빌드·환경·핵심 경로가 더 깊은 검증을 시작할 최소 상태인지 넓고 얕게 확인 | 전체 회귀·품질 보증 |
| **Sanity Test** | `INDUSTRY_COMMON / HIGH_VARIANCE` | 제한된 수정·기능 영역이 상식적으로 동작하는지 좁고 빠르게 확인하는 관행적 표현 | 조직 간 완전히 동일한 표준 범위 |
| **User Acceptance Testing / UAT** | `INDUSTRY_COMMON` | 이해관계자·대표 사용자·사업 측이 실제 요구와 수용 조건에 맞는지 확인 | QA 팀의 모든 기능 테스트 |
| **Regression Testing** | `STANDARDIZED_CONTEXT (ISTQB)` | 변경 후 이전에 정상 동작하던 영역에 의도치 않은 영향이 생겼는지 재검증 | 새 기능 자체의 최초 검증만 수행하는 것 |

**Component / Unit Test는 검색 묶음 이름**일 뿐 완전 동일성 주장이 아니다. Unit Test를 모든 조직에서 Component Test와 완전히 동일한 범위로 강제하지 않는다.

**Smoke/Sanity의 경계는 조직별 편차가 크다.** 같은 팀에서도 두 표현을 겹쳐 쓰는 경우가 있으므로 자동으로 서로의 PASS를 대체하지 않고 프로젝트 Test Strategy가 실제 범위를 고정한다. `Regression Recheck`는 아래 `완료·검증`의 기존 `BASE_LOCAL_ALIAS` canonical row를 재사용한다.

```text
UAT ≠ 일반 QA
Regression Testing ≠ Regression Recheck
Smoke Test PASS ≠ 전체 Regression PASS
E2E PASS ≠ 모든 Unit·Integration 결함 부재
```

## 완료·검증

| 용어 | 압축 정의 |
|---|---|
| **Acceptance Criteria** | 이번 결과를 받아들이기 위해 관찰되어야 할 항목별 조건 |
| **Entry Criteria** | 단계에 들어가기 전에 필요한 조건 |
| **Exit Criteria** | 단계를 벗어나기 위해 필요한 Evidence |
| **Definition of Done** | 모든 완료 결과가 공통으로 지켜야 하는 품질선 |
| **Verification** | 승인된 계약대로 만들었는지 확인 |
| **Validation** | 만든 결과가 실제 사용자·플레이어 목적에 유효한지 확인 |
| **Bidirectional Traceability** | 요구↔구현·검증을 양방향으로 추적 가능한 상태 |
| **Evidence Provenance** | Evidence가 생성된 SHA·환경·명령·도구·시간·입력 기록 |
| **Evidence Ceiling** | 낮은 Evidence PASS를 더 높은 주장으로 승격하지 않는 상한 |
| **Fail-Closed** | Evidence가 없거나 깨졌으면 PASS 대신 차단·미검증을 유지하는 정책 |
| **Assurance Case** | 중요한 주장과 논증·Evidence·가정·반례를 감사 가능하게 연결한 검증 패키지 |
| **Regression Recheck** | 수정 뒤 원래 실패·보호 동작·인접 소비자를 다시 공격하는 검사 |
| **Implementation Reality Gate** | 실제 구현·새 실행·통합 Evidence가 연결될 때만 완료 주장을 허용하는 fail-closed Gate |

## Implementation Reality Gate

**Implementation Reality Gate(IRG)**는 `BASE_LOCAL_ALIAS`다. **업계 표준 용어가 아니다.** 새 ACTIVE Skill·Work Mode·제품 단계도 아니다. 다음 기존 계약을 짧게 부르는 압축명이다.

```text
MATERIAL_CLAIM_LEDGER
+ INTENT_IMPLEMENTATION_FIDELITY_MATRIX
+ COMPLETION_CLAIM_GATE
```

실행 계약 owner: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`

```text
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

## 코드 유지보수

| 용어 | Class | 압축 정의 | 사용하지 않을 의미 |
|---|---|---|---|
| **Code Smell** | `INDUSTRY_COMMON` | 구조·명명·의존성·복잡도에서 추가 검토가 필요할 수 있음을 알리는 설계 신호 | 버그·Technical Debt의 확정 증거 |
| **Technical Debt** | `INDUSTRY_COMMON` | 현재의 빠른 선택·누적된 구조적 타협 때문에 미래 변경·검증·운영 비용과 위험이 증가한 상태 | 모든 버그·오래된 코드·마음에 들지 않는 코드 |
| **Refactor** | `INDUSTRY_COMMON` | 외부에서 관찰 가능한 동작·계약을 유지하면서 내부 구조를 개선하는 변경 | 기능 의미·공개 계약을 바꾸는 기능 개발 |
| **Rewrite** | `INDUSTRY_COMMON` | 기존 구현의 상당 부분을 대체해 새 구현 계보를 만드는 변경 | 자동으로 안전한 대규모 Refactor |

```text
Refactor = 외부 관찰 가능한 동작·계약을 보존
Rewrite ≠ 큰 Refactor
Code Smell ≠ 버그·Technical Debt 확정 증거
Technical Debt ≠ 모든 Bug
```

Rewrite에서 목표 동작이 같더라도 기존 구현의 검증 Evidence가 자동 승계되지는 않는다. 동등성·마이그레이션·회귀·롤백 Evidence를 새 구현에 다시 연결한다.

## Git·버전 관리

| 용어 | Class | 압축 정의 | 혼동 방지 |
|---|---|---|---|
| **Branch** | `STANDARDIZED_CONTEXT (Git)` | 특정 commit을 가리키며 개발 진행에 따라 이동하는 이름 있는 ref·작업 계보 | 저장소 전체를 복사한 별도 프로젝트가 아님 |
| **Merge** | `STANDARDIZED_CONTEXT (Git)` | 서로 다른 commit history의 변경을 한 계보에서 함께 이어 가도록 통합 | 선택 commit 하나만 옮기는 Cherry-pick과 다름 |
| **Rebase** | `STANDARDIZED_CONTEXT (Git)` | 현재 계보의 commit들을 새 base 위에 순서대로 다시 적용해 history 기반을 옮김 | Merge commit을 만드는 동작과 동일하지 않으며 commit identity가 바뀔 수 있음 |
| **Cherry-pick** | `STANDARDIZED_CONTEXT (Git)` | 선택한 기존 commit이 도입한 변경을 현재 계보에 적용해 새 commit으로 기록 | Branch 전체를 병합하는 작업 |
| **Hotfix** | `INDUSTRY_COMMON` | 출시·운영 중인 심각한 문제를 빠르게 교정하기 위한 긴급 수정 흐름·라벨 | Git 자체의 명령·객체·branch type |
| **Semantic Versioning / SemVer** | `STANDARDIZED_CONTEXT (SemVer 2.0.0)` | 선언된 public API의 호환성 변화를 `MAJOR.MINOR.PATCH`에 의미 있게 반영하는 버전 규약 | 단순히 숫자가 `X.Y.Z`처럼 보이는 모든 게임 빌드 버전 |

```text
Rebase ≠ Merge
Cherry-pick ≠ Branch Merge
Hotfix ≠ Git 명령
SemVer는 public API를 선언한 소프트웨어에 의미 규칙을 적용한다.
```

게임 프로젝트가 public API를 정의하지 않았다면 `1.2.3` 형태를 쓴다는 이유만으로 SemVer 호환성을 주장하지 않는다. 스토어 표시 버전, 내부 빌드 번호, 저장 데이터 Schema 버전, 네트워크 프로토콜 버전은 필요하면 서로 다른 version axis로 관리한다.

## 자주 헷갈리는 구분

```text
Prototype ≠ MVP
PoC ≠ Vertical Slice
First Playable ≠ 목표 품질 완료
Demo ≠ Vertical Slice
Sprint ≠ Milestone
Early Access ≠ Beta
Gold / Gold Master ≠ Release Candidate
Smoke Test ≠ 전체 Regression Testing
UAT ≠ 일반 QA
Regression Testing ≠ Regression Recheck
Code Smell ≠ Technical Debt 확정
Refactor ≠ Rewrite
Rebase ≠ Merge
Cherry-pick ≠ Branch Merge
Hotfix ≠ Git 명령
Acceptance Criteria ≠ Definition of Done
Checklist ≠ Gate
Verification ≠ Validation
테스트 파일 존재 ≠ 테스트 실행 Evidence
정적 PASS ≠ runtime·render·UX·재미 PASS
```

## 금지 용례

1. **거친 Prototype을 MVP**라고 부르지 않는다.
2. Demo를 자동으로 Vertical Slice라고 부르지 않는다.
3. Walking Skeleton의 연결을 목표 품질 증명으로 승격하지 않는다.
4. Alpha·Beta를 프로젝트 Entry/Exit Criteria 없이 보편적인 완성도 퍼센트로 고정하지 않는다.
5. Early Access를 Beta·Pre-Purchase·Crowdfunding의 동의어로 쓰지 않는다.
6. Gold / Gold Master를 아직 승인되지 않은 Release Candidate와 동일시하지 않는다.
7. Epic·User Story를 Scrum Guide가 요구하는 공식 Artifact라고 보고하지 않는다.
8. User Story 한 줄을 전체 요구 명세·Acceptance Criteria로 취급하지 않는다.
9. Smoke·Sanity의 조직별 범위를 확인하지 않고 서로의 PASS를 자동 승계하지 않는다.
10. UAT PASS를 전체 기술 QA·성능·보안·접근성 PASS로 승격하지 않는다.
11. **Checklist를 Gate**라고 부르지 않는다.
12. **테스트 파일 존재를 테스트 실행**으로 보고하지 않는다.
13. **정적 PASS를 runtime**·render·UX·재미 PASS로 승격하지 않는다.
14. Code Smell을 발견했다는 이유만으로 버그나 Technical Debt를 확정하지 않는다.
15. 외부 동작·공개 계약이 바뀌는 기능 변경을 순수 Refactor라고 숨기지 않는다.
16. Rewrite를 큰 Refactor라고 낮춰 부르며 기존 Evidence를 자동 승계하지 않는다.
17. Rebase를 Merge와 같은 history operation이라고 설명하지 않는다.
18. Cherry-pick을 Branch 전체 Merge라고 설명하지 않는다.
19. Hotfix를 Git 내장 명령이나 고정 branch 구조라고 설명하지 않는다.
20. public API 계약 없이 `X.Y.Z`만 보고 Semantic Versioning 준수라고 주장하지 않는다.
21. 모든 Decision Record를 ADR이라고 부르지 않는다.
22. 적대적 검토를 Red Team 공격 하나로 축약하지 않는다.
23. `DDD`를 단독 사용하지 않는다.
24. 단일 도구를 근거 없이 Framework·Platform·Control Plane으로 과장하지 않는다.
25. `BASE_LOCAL_ALIAS`를 외부 표준·업계 공인 용어처럼 소개하지 않는다.

## 프로젝트 채택

프로젝트는 이 파일을 통째로 복제해 두 번째 공용 정본을 만들지 않는다. 실제로 쓰는 용어만 프로젝트 Documentation Map에 연결하고, 프로젝트별 범위·수치·품질선·상태는 프로젝트 책임 원본에 둔다. Base 정의와 프로젝트 정의가 다르면 Bounded Context와 번역 규칙을 기록한다.
