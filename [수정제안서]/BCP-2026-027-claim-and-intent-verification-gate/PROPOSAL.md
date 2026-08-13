# BCP-2026-027 — Claim and Intent Verification Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 관찰 기준 Base 커밋: `453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- 제출일: `2026-08-13`
- Registry 상태: `SUBMITTED`
- 지식 상태: `반복 관찰 + 외부 1차 출처 비교 + 승인된 공용 운영 보완`
- 사용자 구현 승인 증거: 2026-08-13 현재 ChatGPT 세션 지시 — “할루시네이션 현상방지, 우리가 의도한대로 제대로 구현이 되었는지 확인하는 스킬을 Base에 추가하고 작업구조에도 반영” 및 병합까지 수행 요청
- 상태 설명: 신규 제안 PR은 Base 검사 규칙에 따라 반드시 `SUBMITTED`로 시작한다. 제안 병합 뒤 별도 구현 PR에서 위 사용자 승인 증거를 `approval_ref`로 사용하고, 검증·병합 시 `IMPLEMENTED`로 전환한다.

## 관찰과 증거

Base에는 이미 다음 안전 장치가 있다.

- 실제 파일·diff·실행 결과를 설명보다 우선하는 `reviewing-and-validating-project-changes`
- 요구사항→수용 기준→Task→구현 경로→검증 증거를 잇는 `FEATURE_SPEC_TRACEABILITY_PACKET`
- 사용자안과 AI 최초안을 같은 기준으로 공격·비판 검증하는 `running-adversarial-review-and-refinement`
- 낮은 Evidence가 높은 Evidence를 대신하지 못하게 하는 Evidence ceiling
- exact HEAD, 독립 검토, post-merge main readback, untouched consumer 재검사

그러나 이 규칙은 여러 문서에 분산돼 있어 다음 네 질문을 한 번에 닫는 명시적 실행 Gate가 부족하다.

1. 외부 AI·Agent·작업자가 보고한 사실과 완료 주장은 실제 근거가 있는가?
2. 승인된 WHAT/WHY·Acceptance Criteria가 실제 구현 경로와 관찰 동작에 연결되는가?
3. 테스트 파일의 존재가 아니라 해당 exact HEAD에서 검증이 실제 실행됐는가?
4. PR 병합 주장이 실제 merge SHA와 새 `main` readback까지 확인됐는가?

반복 실패 형태:

- 존재하는 파일·명령·테스트를 실행한 것으로 과장
- 구현 경로 일부만 보고 전체 요구사항을 충족했다고 결론
- 기술적 HOW 변경이 승인된 플레이어 경험·제품 의미를 바꾼 사실을 놓침
- 오래된 branch·문서·웹 정보를 현재 사실처럼 사용
- Builder의 설명이나 모델의 자신감을 독립 Evidence로 사용
- 테스트 PASS를 사람 사용성·재미·시장성 PASS로 승격

### Existing Solution First

판정: `ABSORB`

새 ACTIVE Skill을 추가하지 않는다. 현재 30개 ACTIVE Skill 수를 유지하고 기존 owner인 `reviewing-and-validating-project-changes`에 `claim-and-intent-verification` Skill Mode와 전용 reference를 흡수한다.

| 선택지 | 장점 | 위험 | 결론 |
|---|---|---|---|
| 새 광역 Skill `verifying-ai-truth` 추가 | 이름이 눈에 띔 | 외부 산출물 검수·계약 대조·회귀·증거 보고 owner와 중복, 라우팅 비용 증가 | 제외 |
| 기존 Skill에 Mode·reference·Template·행동 평가 흡수 | 기존 권한·입출력·판정과 일치, active Skill 수 불변 | 본문 과밀 가능 | 채택; 상세 절차는 reference로 분리 |
| Template 문구만 추가 | 변경량이 작음 | 자동 라우팅·실패 조건·완료 Gate가 없어 쉽게 생략 | 제외 |
| 외부 Eval SaaS를 Base 필수 의존성으로 채택 | 실험 추적·대시보드 편리 | 공급자 종속, 비용·보안·설정 부담, 비게임 문서 작업에 과잉 | 제외; 프로젝트 선택 도구로만 허용 |

### 외부 1차 출처·현업 비교

#### NIST AI 600-1 Generative AI Profile

NIST는 confabulation을 거짓이거나 잘못된 콘텐츠, prompt와의 불일치, 응답 내부 모순까지 포함하는 위험으로 다룬다. 알려진 정답이 있는 평가, 사람·자동 평가의 병행, 사실 확인, 정기적 적대 테스트, 인용·출처 검증과 지속 모니터링을 권고한다.

- https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

#### NASA Systems Engineering Handbook — Requirements Verification Matrix

NASA는 요구사항에 고유 식별자와 출처를 부여하고, 요구사항별 검증 방법과 결과를 Verification Matrix로 추적한다. Base에는 이를 일반화해 승인 의도와 구현·검증을 연결하는 `intent_id` 중심 매트릭스를 사용한다.

- https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/

#### OpenAI SimpleQA

SimpleQA는 긴 응답을 짧고 원자적으로 검증 가능한 주장으로 다루고 정답·오답·미응답을 구분한다. Base는 이를 결과 문장 전체의 모호한 신뢰 점수 대신 중요한 원자 주장별 판정으로 변형한다.

- https://openai.com/index/introducing-simpleqa/

#### 현업 Eval 도구의 공통 패턴

Arize Phoenix, LangSmith, Braintrust, Promptfoo의 공식 문서는 대체로 고정된 dataset·reference 또는 experiment snapshot, 가능한 사실의 deterministic evaluator, 의미 판단용 rubric·judge, CI 회귀와 production feedback 분리, hallucination·faithfulness·fabricated citation·tool selection 독립 평가를 조합한다.

- https://arize.com/docs/phoenix/evaluation/how-to-evals/running-pre-tested-evals/faithfulness
- https://docs.smith.langchain.com/evaluation
- https://www.braintrust.dev/docs/guides/evals
- https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/factuality/
- https://www.promptfoo.dev/docs/red-team/plugins/hallucination/

### 채택·변형·제외

| 구분 | 결정 |
|---|---|
| 채택 | 원자 주장, authority source, 반증 탐색, deterministic-first, 요구사항 추적성, Evidence ceiling, 회귀·지속 readback |
| 변형 | 범용 지식 정답보다 저장소 정본·실제 diff·도구 출력·실행 결과를 우선; LLM judge는 보조 Evidence로만 사용 |
| 제외 | 단일 모델 self-evaluation을 진실 판정으로 사용, 모든 문장을 원장화, 외부 SaaS 의무화, 테스트 정의만으로 PASS 처리 |

## 일반화 후보

### 1. `MATERIAL_CLAIM_LEDGER`

결정·구현·검증·병합 상태를 바꾸는 중요한 주장만 원자화한다. 설명용 모든 문장을 기록하지 않는다.

```yaml
claim_id:
claim_type: REPOSITORY_FACT | EXTERNAL_FACT | INFERENCE | IMPLEMENTATION | VERIFICATION | INTEGRATION
claim_text:
authority_source:
evidence_locator:
freshness:
counterevidence:
status: CLAIM_VERIFIED | CLAIM_CONTRADICTED | CLAIM_UNVERIFIED | NOT_APPLICABLE
```

권한 순서:

```text
최신 사용자 지시·승인 계약
→ exact SHA의 실제 저장소·등록된 정본
→ 해당 exact SHA에서 실행된 도구·테스트·런타임 결과
→ 날짜·버전이 확인된 공식 외부 1차 출처
→ 명시적 추론
→ 작업자·Builder·모델 설명(검증할 lead일 뿐 Evidence 아님)
```

### 2. `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`

```yaml
intent_id:
approved_intent_or_acceptance:
protected_and_excluded_scope:
implementation_paths:
observed_behavior:
verification_evidence:
evidence_ceiling:
drift_status: INTENT_CONFORMANT | MINOR_TECHNICAL_DRIFT | PLANNING_CONFLICT | IMPLEMENTATION_UNVERIFIED
```

- `INTENT_CONFORMANT`: 승인 결과·보호 동작과 관찰 결과가 일치한다.
- `MINOR_TECHNICAL_DRIFT`: HOW만 달라졌고 WHAT/WHY·제품 의미·보호 동작은 동일하다.
- `PLANNING_CONFLICT`: 플레이어 경험·주요 UX·콘텐츠 의미·범위·우선순위가 승인 내용과 충돌한다.
- `IMPLEMENTATION_UNVERIFIED`: 필요한 diff·runtime·test·render·사람 Evidence가 없다.

### 3. `COMPLETION_CLAIM_GATE`

| 주장 | 최소 Evidence |
|---|---|
| 구현 완료 | 실제 diff + 요구사항별 `implementation_paths` + 범위 밖 변경 부재 |
| 테스트/검증 완료 | 실행 명령·환경·결과 + exact HEAD + 실패 수 |
| 의도대로 동작 | Acceptance별 관찰 결과 + 필요한 Evidence level; 낮은 층이 높은 층을 대체하지 않음 |
| 병합 완료 | PR merged 상태 + merge SHA + 새 `main` readback + post-merge 필수 검사 |

필수 Evidence가 없으면 `BLOCKED_UNVERIFIED` 또는 `IMPLEMENTATION_UNVERIFIED`를 유지한다. “대체로 맞음”, “파일이 있으므로 실행됐을 것”, “Builder가 완료라고 보고함”은 PASS 근거가 아니다.

### 4. 작업 구조

```text
승인 Intent·Acceptance·Protected Scope
→ 중요한 완료/사실 주장 원자화
→ authority·freshness·counterevidence 검사
→ 실제 diff·consumer·implementation path 연결
→ deterministic static/test/runtime evidence 실행
→ Evidence ceiling 적용
→ 독립 VERIFIER/CRITIC 검토
→ exact-head 판정
→ merge 뒤 main readback
→ CLAIM / INTENT / VERIFICATION 최종 보고
```

## 적용 조건과 비사용 조건

적용:

- L1 이상 AI/Agent 완료 보고
- 외부 사실·인용·현재 버전 주장
- 승인 의도와 실제 구현의 일치 판정
- 테스트·검증·병합 완료 주장
- L2 이상 복합 변경의 Traceability Packet 검증

비사용 또는 경량화:

- L0 오탈자·동일 입력 재검사는 전체 원장을 강제하지 않는다.
- 순수 창작에서 사실·정본·완료 상태를 주장하지 않는 문장은 원장화하지 않는다.
- 프로젝트 정본 전체를 claim ledger에 복제하지 않는다.
- 외부 SaaS·LLM judge 사용을 필수 조건으로 만들지 않는다.
- 구현되지 않은 높은 Evidence를 낮은 Evidence에서 추론하지 않는다.

프로젝트 전용으로 남길 내용:

- 게임별 플레이어 경험·UX·수치·세계관·Acceptance 문구
- 실제 Godot scene·script·data·asset 경로
- 프로젝트별 테스트 명령과 플랫폼·device 조건
- 사용하기로 선택한 외부 Eval 도구와 dataset

## 반례와 위험

| 공격 | 검증 | 승인된 최소 대응 |
|---|---|---|
| 모든 문장을 원장화해 작업 비용 폭증 | 실질적 결정·완료 상태를 바꾸는 claim만 필요 | `material claim` 범위와 L0 비사용 조건 명시 |
| 출처가 있어도 오래됐거나 서로 충돌 | URL 존재만으로 현재성·정확성 보장 안 됨 | 날짜·버전·exact SHA·counterevidence 필드 요구 |
| 테스트 파일을 실행 결과로 오인 | 정의와 실행 Evidence는 다름 | 명령·환경·exact HEAD·결과 필수 |
| Builder와 검증자가 동일하면 자기확증 | 기존 Control Plane도 역할 분리를 요구 | Builder 설명을 Evidence로 금지, VERIFIER/CRITIC 판정 |
| LLM judge가 또 hallucination | 의미 판정 도구도 오류 가능 | deterministic-first, judge는 보조, 반증과 미검증 허용 |
| 구현은 맞지만 UX·재미까지 과장 | Evidence 층 불일치 | 기존 E0–E6 ceiling 및 BCP-020 사람 Evidence 유지 |
| 병합 직전 main 변경으로 검증 노후화 | stale base 위험 | exact-head, current-main freshness, post-merge readback 유지 |
| 기존 검증 Skill과 책임 중복 | 새 Skill 생성 시 owner 충돌 | Mode·reference로 흡수, Registry 불변 |

대표 반례:

1. “테스트가 있다”만 확인되고 실행 결과가 없음 → `CLAIM_UNVERIFIED`.
2. 테스트 PASS지만 다른 SHA에서 실행됨 → `CLAIM_UNVERIFIED`.
3. 구현 경로는 존재하지만 Acceptance 하나가 unmapped → `IMPLEMENTATION_UNVERIFIED`.
4. 기술 구조는 작동하지만 승인된 주요 UX 의미가 달라짐 → `PLANNING_CONFLICT`.
5. 외부 문서가 공식이지만 버전·날짜가 현재 결정과 불일치 → stale 또는 contradictory.
6. PR이 merged지만 새 main readback·push CI가 없음 → integration claim 미완료.

## 영향 범위와 검증

### 구현 대상

- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`
- `skills/SKILL_BEHAVIOR_EVALS.json`
- `tests/test_neutral_adversarial_feature_lifecycle.py`
- `docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md`
- `docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md`
- `docs/CHANGELOG.md`

### 보호 대상

- ACTIVE Skill 수와 `skills/SKILL_REGISTRY.json` bytes
- `PLAN / BUILD / REVIEW` 세 Work Mode
- 이미 릴리스된 Base lock·pin·generated artifact
- 프로젝트별 수치·세계관·구현 경로
- 기존 Evidence E0–E6 의미
- BCP-008 Traceability와 BCP-020 Player Experience Evidence owner

### RED→GREEN 검증

RED:

- 전용 계약 테스트가 새 reference·Mode·Template·행동 평가를 요구하도록 먼저 추가한다.
- 생산 계약이 없는 exact HEAD에서 GitHub Actions 실패를 관찰한다.

GREEN:

- focused unittest PASS
- Base v9 contract·integrity PASS
- Registry active Skill 수와 bytes 불필요 변경 없음
- 새 행동 fixture `SBE-015`가 REVIEW의 기존 owner로 라우팅
- PR diff가 승인된 영향 경로 안에 있음
- 가능한 독립 reviewer finding 검토
- unresolved review thread 0
- merge SHA와 post-merge `main` readback

### 롤백

문서·Skill Mode·reference·Template·behavior fixture·test만 추가·수정한다. 제품 데이터·런타임·릴리스 pin은 바꾸지 않는다.

문제가 생기면 구현 PR의 merge commit을 revert한다. 새 reference와 Mode 연결, Template 섹션, fixture·test를 함께 되돌려 부분 활성 상태를 남기지 않는다. BCP 제안 기록은 역사로 유지하고 Registry 상태를 후속 판정으로 갱신한다.

## 승인과 구현

- 사용자 구현 승인 증거: 2026-08-13 현재 ChatGPT 세션의 직접 요청과 병합 지시
- 신규 제안 PR Registry 상태: `SUBMITTED`
- 승인된 구현 범위: 이 문서의 영향 경로·보호 대상·검증 계약
- 구현 방식: 이 제안 PR 병합 뒤 fresh `main`에서 별도 구현 PR
- 구현 PR: 아직 없음
