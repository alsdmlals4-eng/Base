# Base 공용 통제 어휘

이 문서는 반복되는 긴 작업 계약을 짧은 현업 용어로 호출하기 위한 **Controlled Vocabulary**다. 한 줄 정의·적용 경계·금지 의미·기존 책임 원본만 연결하며, 상세 절차와 프로젝트 실제 상태는 복제하지 않는다.

```text
통제 어휘
= 빠른 탐색·컨텍스트 압축·용어 충돌 방지
≠ 새 Work Mode·Skill·Skill Mode·Gate·제품 단계
≠ 프로젝트 구현·수치·세계관의 두 번째 정본
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

## 제작·실험·제품 단계

이 용어들은 강제 선형 단계가 아니라 서로 다른 검증 질문이다.

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

**Implementation Reality Gate(IRG)**는 새 ACTIVE Skill·Work Mode·제품 단계가 아니다. 다음 기존 계약을 짧게 부르는 압축명이다.

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

## 금지 용례

1. **거친 Prototype을 MVP**라고 부르지 않는다.
2. Demo를 자동으로 Vertical Slice라고 부르지 않는다.
3. Walking Skeleton의 연결을 목표 품질 증명으로 승격하지 않는다.
4. **Checklist를 Gate**라고 부르지 않는다.
5. **테스트 파일 존재를 테스트 실행**으로 보고하지 않는다.
6. **정적 PASS를 runtime**·render·UX·재미 PASS로 승격하지 않는다.
7. 모든 Decision Record를 ADR이라고 부르지 않는다.
8. 적대적 검토를 Red Team 공격 하나로 축약하지 않는다.
9. `DDD`를 단독 사용하지 않는다.
10. 단일 도구를 근거 없이 Framework·Platform·Control Plane으로 과장하지 않는다.

## 프로젝트 채택

프로젝트는 이 파일을 통째로 복제해 두 번째 공용 정본을 만들지 않는다. 실제로 쓰는 용어만 프로젝트 Documentation Map에 연결하고, 프로젝트별 범위·수치·품질선·상태는 프로젝트 책임 원본에 둔다. Base 정의와 프로젝트 정의가 다르면 Bounded Context와 번역 규칙을 기록한다.
