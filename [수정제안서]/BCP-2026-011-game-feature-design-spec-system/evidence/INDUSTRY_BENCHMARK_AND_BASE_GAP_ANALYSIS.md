# Industry Benchmark & Base Gap Analysis

## 1. 조사 질문

우리는 **Base의 게임 세부기획 구조가 실제 제작 단계에서 필요한 명확성과 유지 가능성을 제공하도록 개선하기 위해**, 현대 게임 제작의 문서 해상도·프로토타이핑·팀 커뮤니케이션 사례와 Base 현행 책임 경계를 비교한다.

```yaml
decision:
  - 새 광역 Skill이 필요한가
  - 거대한 GDD가 필요한가
  - 기능 단위 상세 Spec이 필요한가
  - 기존 Traceability와 어떤 경계를 가져야 하는가
current_hypothesis:
  - 새 Skill보다 기존 concept/document/validation owner에 조건부 Feature Spec 계층을 흡수하는 편이 낫다
target_context:
  - 소규모~중규모 게임 프로젝트
  - GPT 기획 → 필요 시 Codex 구현 인계
  - Godot 중심이지만 엔진 비종속 공용 기획 계약
constraints:
  - 한 질문 한 정본
  - 새 Skill 과분할 금지
  - PoC 이전 과설계 금지
  - 실제 구현/검증 상태 이중 정본 금지
checked_at: 2026-08-10
```

## 2. Base 현행 책임 감사

### 2.1 이미 존재하는 강점

| Base 자산 | 현재 책임 | 보존 이유 |
|---|---|---|
| `analyzing-and-refining-game-concepts` | 핵심 컨셉·제약·시스템 설계·벤치마크·PoC·재조정 | 기능이 존재할 이유와 위험을 먼저 검증함 |
| `managing-design-documents` | 기획 정본 작성·갱신·발행 | 문서 authority를 이미 소유함 |
| `DESIGN_DOCUMENT_SYSTEM` | 프로젝트 기획 문서 지도와 수명주기 | 새 문서가 어디에 위치하는지 연결 가능 |
| `PROJECT_GDD_GOOGLE_SHEETS_POLICY` | 사용자용 GDD 작업면 | 장문 전문을 복제하지 않고 요약·상태·링크를 제공함 |
| `FEATURE_SPEC_TRACEABILITY_PACKET` | L2+ Requirement→Task→Implementation→Verification 연결 | 승인 후 제작 추적을 이미 해결함 |
| `running-adversarial-review-and-refinement` | 설계·정책·구조의 실패 가정과 검증 | 새 별도 red-team 체계 불필요 |

### 2.2 실제 공백

현재 범용 문서 작성 구조는 충분히 좋은 방향성을 주지만, 여러 직군이 한 기능을 제작할 때 다음 항목을 한 기능 단위로 닫는 공용 Template이 약하다.

- Player Problem과 Experience Intent.
- player verb와 input lifecycle.
- state/rule/priority.
- success/failure/recovery.
- edge cases.
- UI/VFX/Animation/Audio feedback.
- data/balance source와 조정 조건.
- cross-discipline production inputs.
- technical/platform constraints.
- content production pipeline.
- predeclared acceptance/playtest/telemetry.
- cut-down/rollback.

따라서 공백은 **새 작업 분야**가 아니라 `concept evidence → production-ready design document → existing traceability` 사이의 문서 해상도다.

## 3. 외부 벤치마크

### EVIDENCE-01 — GDC 2025: Four One-Page Design Docs

- 출처: GDC Vault, Ian Schreiber, *The Four One-Page Design Docs You Need (And How to Use Them)*.
- URL: `https://gdcvault.com/play/1035510/The-Four-One-Page-Design`
- 출처 계층: `T2_PROFESSIONAL_PRACTICE`.
- 관찰:
  - 게임 문서는 프로젝트·회사마다 크게 다를 수 있다.
  - broadly useful한 네 문서로 `game vision`, `pillars`, `loops`, `resource flow`를 제안한다.
  - 핵심은 각각을 유용하고 유지 가능하게 만들고 후속 설계 작업을 쉽게 하는 것이다.
- Base 적용:
  - `ADOPT`: 프로젝트 방향의 핵심 문서를 기능 상세 Spec과 분리한다.
  - `ADAPT`: Base는 이미 GDD/Direction 구조가 있으므로 네 파일을 그대로 강제하지 않고 L0 responsibility로 흡수한다.
- 제외:
  - 모든 프로젝트에 물리적으로 정확히 네 파일 생성 강제.

### EVIDENCE-02 — GDC 2010: One-Page Designs

- 출처: GDC Vault, Stone Librande, EA/Maxis, *One-Page Designs*.
- URL: `https://www.gdcvault.com/play/1012356/One-Page`
- 출처 계층: `T2_PROFESSIONAL_PRACTICE`.
- 관찰:
  - 핵심 설계 아이디어를 짧고 명확하게 전달하기 위한 one-page 방식.
  - Diablo III, The Simpsons, Spore 사례를 통해 효과적인/비효과적인 전달법을 비교한다.
- Base 적용:
  - `ADOPT`: Feature Brief는 짧은 판단 문서여야 한다.
  - `ADAPT`: 복잡한 L2 기능 Spec까지 한 페이지로 제한하지 않는다. 한 페이지 제한보다 책임 명확성과 조건부 상세화를 우선한다.
- 제외:
  - “모든 기획 문서는 한 페이지”라는 분량 규칙.

### EVIDENCE-03 — Ubisoft Creative Process

- 출처: Ubisoft, *Creative Process | How We Make Games*.
- URL: `https://www.ubisoft.com/en-us/company/how-we-make-games/creative-process`
- 출처 계층: `T1_PRIMARY_OFFICIAL`.
- 관찰:
  - Preconception/Conception에서 아이디어를 시험·실패·연구·prototype/PoC로 성숙시킨다.
  - Project Mandate는 비전·목표·계획을 up-to-date orientation point로 둔다.
  - Preproduction의 First Playable은 core experience의 work-in-progress draft를 실제로 시험한다.
  - Production은 본격적인 assets/source code 제작 단계다.
- Base 적용:
  - `ADOPT`: 상세 Spec 투자는 concept/PoC 검증 이후로 미룬다.
  - `ADAPT`: Base의 `PoC → Feature Design Spec → Traceability/Production` Gate로 번역한다.
- 제외:
  - Ubisoft의 조직/승인 계층을 소규모 프로젝트에 그대로 복제.

### EVIDENCE-04 — Game Developer 2023: Modern GDD practice

- 출처: Game Developer, Danielle Riendeau, *How To: Write a Game Design Document*, 2023-08-15.
- URL: `https://www.gamedeveloper.com/design/how-to-write-a-game-design-document`
- 출처 계층: `T2_PROFESSIONAL_PRACTICE / interview synthesis`.
- 관찰:
  - monolithic design bible 시대는 지나갔으며 팀마다 필요한 형식이 다르다.
  - 좋은 문서는 searchable, readable, concise해야 한다.
  - GDD는 engineer, system designer, level designer, artist, animator, sound, producer 등 다양한 직군이 같은 vision을 이해하도록 해야 한다.
  - mechanics는 player verbs와 게임의 반응/rules를 명확히 전달해야 한다.
- Base 적용:
  - `ADOPT`: 기능 Spec은 cross-discipline communication contract여야 한다.
  - `ADAPT`: Base의 기존 specialist 문서와 연결하고 중복 전문은 피한다.
- 한계:
  - 단일 스튜디오 표준이 아니라 여러 개발자 조언을 합친 편집 기사이므로 universal rule로 승격하지 않는다.

### EVIDENCE-05 — Game Developer 2016: prototype before resource commitment

- 출처: Game Developer, Leandro Gonzalez, *How to Write a Game Design Document*, 2016-07-26.
- URL: `https://www.gamedeveloper.com/business/how-to-write-a-game-design-document`
- 출처 계층: `T2_PROFESSIONAL_PRACTICE`.
- 관찰:
  - monolithic GDD를 생산 이후 계속 갱신하는 방식이 유일한 답이 아니라고 명시한다.
  - mechanics 설명은 팀이 합리적 의심을 최소화할 정도로 명확해야 한다.
  - mechanics가 재미있는지 prototype으로 확인한 뒤 자원을 크게 투입하는 방식을 선호한다고 설명한다.
- Base 적용:
  - `ADOPT`: 구현자가 동작 의미를 재해석하지 않을 정도의 명확성.
  - `ADOPT`: 상세 production 투자 전 핵심 mechanics prototype/PoC.
- 한계:
  - 오래된 단일 팀 사례이므로 최신 조직 표준으로 일반화하지 않는다.

## 4. 대안 비교

| 접근 | 장점 | 실패 위험 | Base 적합성 | 판정 |
|---|---|---|---|---|
| 거대한 `MASTER_GDD` 하나 | 진입점 하나 | 수정 충돌, 낮은 검색성, 중복, 컨텍스트 팽창 | 낮음 | `AVOID` |
| 새 `game-detailed-planning` Skill | 이름이 명확함 | concept/document owner 중복 | 낮음 | `AVOID` |
| 모든 Feature에 상세 Spec | 양식 일관성 | PoC 전 문서 과투자 | 낮음 | `AVOID` |
| Feature Brief→PoC→Feature Spec→Traceability | 위험 기반 상세화, 기존 owner 재사용 | Gate·경계 설계 필요 | 높음 | `ADOPT` |
| Feature Spec 안에 Task/테스트 ledger 포함 | 한 파일에서 보임 | Traceability/실제 구현과 이중 정본 | 매우 낮음 | `AVOID` |
| 전문 분야 문서를 Feature Spec으로 대체 | 표면 통일 | 고유 전문 계약 손실 | 낮음 | `AVOID` |
| Feature Spec이 전문 분야 문서를 링크/조합 | 단일 기능 의미 + 전문성 보존 | 링크 신선도 필요 | 높음 | `ADOPT` |

## 5. 권장 구조

```text
PROJECT DIRECTION
  Game Vision / Pillars / Loops / Resource Flow
          │
          ▼
FEATURE BRIEF
  problem / value / scope / riskiest assumption
          │
          ▼
BENCHMARK + POC + ADVERSARIAL REVIEW
          │
          ├── REMOVE / DEFER / RETEST
          │
          ▼
GAME FEATURE DESIGN SPEC
  behavior / rules / state / feedback / edge cases
  data / specialist inputs / technical constraints
  acceptance / playtest / cut-down
          │
          ▼
APPROVAL
          │
          ▼
FEATURE SPEC TRACEABILITY PACKET
          │
          ▼
IMPLEMENTATION + VALIDATION
```

## 6. Base 통합 경계

### 반드시 반영 후보

- `GAME_FEATURE_DESIGN_SPEC.md` 공용 Template.
- 기존 `managing-design-documents` owner 연결.
- 기존 concept Skill의 PoC 생존 → detailed spec 승격 Gate.
- 기존 Traceability Packet의 upstream spec identity.
- cross-discipline adversarial review checklist.
- Sheet에는 링크·상태·요약만 유지.

### PoC 검증

실제 게임 프로젝트에서 다음을 검증해야 한다.

- 구현 질문 수 감소.
- QA test-case derivation 용이성.
- UI/아트/오디오 누락 감소.
- 문서 갱신 비용.
- 과설계 방지.

### 제외

- 새 ACTIVE Skill.
- monolithic GDD 강제.
- 모든 기능에 L2 Spec 강제.
- 모든 문서 한 페이지 제한.
- 전문 분야 정본을 범용 Feature Spec으로 대체.
- 실행하지 않은 사람/프로젝트 품질 개선 주장.

## 7. PRE_EXISTING_GOVERNANCE_FINDING

### 관찰

- current main `PROPOSAL_REGISTRY.json`은 007 다음 009로 이동하며 008 record가 없다.
- GitHub PR #190은 `BCP-2026-008-agentic-spec-design-ui-procurement-integration` proposal-only Draft였으나 closed unmerged 상태다.
- PR #192는 해당 BCP의 구현을 설명하며 merged되었고 current Base에 `FEATURE_SPEC_TRACEABILITY_PACKET` 등 결과가 존재한다.

### 위험

현재 Registry만 읽는 작업자는 BCP-008의 역사적 source/approval chain을 발견하지 못할 수 있다. 반대로 새 제안이 008 ID를 재사용하면 역사 충돌이 생긴다.

### 이번 판정

```yaml
finding: HISTORICAL_BCP_ID_WITHOUT_CURRENT_REGISTRY_RECORD
severity: SHOULD_FIX_GOVERNANCE
current_task_action: DO_NOT_REUSE_ID
new_proposal_id: BCP-2026-011
automatic_repair_in_this_proposal: NO
reason: 현재 Feature Spec 책임과 독립된 repository governance 문제이며 proposal-only scope를 오염시키지 않기 위함
followup: repository-wide audit에서 역사 보존 방식과 Registry repair 여부 판정
```

## 8. 조사 종료 판정

```yaml
multiple_approaches_compared: YES
primary_official_evidence: YES
professional_practice_evidence: YES
base_current_authority_compared: YES
adopt_and_avoid_reasons_explicit: YES
minimal_integration_path_defined: YES
validation_path_defined: YES
more_research_likely_to_change_architecture: LOW
research_status: SUFFICIENT_FOR_PROPOSAL
implementation_evidence: NOT_RUN
project_pilot: NOT_RUN
human_usability: HUMAN_NOT_RUN
```
