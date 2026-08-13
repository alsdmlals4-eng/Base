# BCP-2026-027 — Claim and Intent Verification Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 관찰 기준 Base 커밋: `453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- 제출일: `2026-08-13`
- Registry 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `반복 관찰 + 외부 1차 출처 비교 + 승인된 공용 운영 보완`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/319`
- 사용자 구현 승인 증거: 2026-08-13 현재 ChatGPT 세션 지시 — “할루시네이션 현상방지, 우리가 의도한대로 제대로 구현이 되었는지 확인하는 스킬을 Base에 추가하고 작업구조에도 반영” 및 병합까지 수행 요청
- 상태 설명: 신규 제안은 검사 규칙에 따라 `SUBMITTED`로 시작한다. `approval_ref`는 위 명시적 사용자 승인 증거의 위치를 가리키며, 구현 완료 상태와 `implementation_pr`은 별도 구현 PR의 검증·병합 단계에서 전환한다.

## 관찰과 증거

Base에는 이미 다음 안전 장치가 있다.

- 실제 파일·diff·실행 결과를 설명보다 우선하는 `reviewing-and-validating-project-changes`
- 요구사항→수용 기준→Task→구현 경로→검증 증거를 잇는 `FEATURE_SPEC_TRACEABILITY_PACKET`
- 사용자안과 AI 최초안을 같은 기준으로 공격·비판 검증하는 `running-adversarial-review-and-refinement`
- 낮은 Evidence가 높은 Evidence를 대신하지 못하게 하는 Evidence ceiling
- exact HEAD, 독립 검토, post-merge main readback, untouched consumer 재검사

그러나 이 규칙은 여러 문서에 분산돼 있어 다음 네 질문을 한 번에 닫는 실행 Gate가 부족하다.

1. AI·Agent·작업자가 보고한 사실과 완료 주장은 실제 근거가 있는가?
2. 승인된 WHAT/WHY·Acceptance Criteria가 실제 구현 경로와 관찰 동작에 연결되는가?
3. 테스트 파일의 존재가 아니라 해당 exact HEAD에서 검증이 실제 실행됐는가?
4. 병합 주장이 실제 merge SHA와 새 `main` readback까지 확인됐는가?

반복 실패 형태:

- 존재하는 파일·명령·테스트를 실행한 것으로 과장
- 구현 경로 일부만 보고 전체 요구사항을 충족했다고 결론
- HOW 변경이 승인된 플레이어 경험·제품 의미를 바꾼 사실을 놓침
- 오래된 branch·문서·웹 정보를 현재 사실처럼 사용
- Builder 설명이나 모델 자신감을 독립 Evidence로 사용
- 테스트 PASS를 사람 사용성·재미·시장성 PASS로 승격

### Existing Solution First

판정: `ABSORB`

새 ACTIVE Skill을 만들지 않는다. 현재 30개 ACTIVE Skill과 세 Work Mode를 유지하면서 기존 owner `reviewing-and-validating-project-changes`에 다음을 흡수한다.

- `claim-and-intent-verification` Skill Mode와 전용 reference
- 기존 Registry 항목의 좁은 trigger/use_when 보강
- 원자 주장·의도 충실도·완료 주장 Gate Template
- `SBE-038` 행동 fixture와 계약 회귀

| 선택지 | 장점 | 위험 | 결론 |
|---|---|---|---|
| 새 광역 Skill 생성 | 발견이 쉬움 | 기존 통합 검증 owner와 중복, 라우팅 비용 증가 | 제외 |
| 기존 Skill에 Mode·reference·Registry metadata·Template·평가 흡수 | owner·입출력·Evidence 구조 재사용, Skill 수 불변 | 파생 요약 재생성 필요 | 채택 |
| Skill 본문과 Template만 변경하고 Registry 고정 | 변경량이 작음 | `model_run_status: NOT_RUN`에서 자동 호출 경로를 증명하지 못함 | 제외 |
| 외부 Eval SaaS 필수화 | 추적 대시보드 제공 | 공급자 종속, 비용·보안·설정 부담 | 제외; 프로젝트 선택 도구로만 허용 |

### 외부 1차 출처·현업 비교

- NIST AI 600-1은 confabulation을 거짓·오류, prompt 불일치, 응답 내부 모순까지 포함해 다루고, 알려진 정답 기반 평가, 사람·자동 평가 병행, 사실·인용 확인, 적대 테스트와 지속 모니터링을 권고한다.
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- NASA Requirements Verification Matrix는 요구사항에 ID·출처·검증 방법·결과를 연결한다.
  - https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/
- OpenAI SimpleQA는 긴 completion의 다수 주장을 신뢰성 있게 채점하기 어려워 짧은 factual question으로 범위를 제한하고 `correct / incorrect / not attempted`를 구분한다.
  - https://openai.com/index/introducing-simpleqa/
- Phoenix, LangSmith, Braintrust, Promptfoo의 공식 Eval 문서는 고정 dataset·reference 또는 snapshot, deterministic evaluator, 보조 rubric/judge, CI 회귀와 production feedback 분리를 공통적으로 사용한다.
  - https://arize.com/docs/phoenix/evaluation/how-to-evals/running-pre-tested-evals/faithfulness
  - https://docs.smith.langchain.com/evaluation
  - https://www.braintrust.dev/docs/guides/evals
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/factuality/
  - https://www.promptfoo.dev/docs/red-team/plugins/hallucination/

### 채택·변형·제외

| 구분 | 결정 |
|---|---|
| 채택 | material claim, authority, freshness, counterevidence, deterministic-first, 요구사항 추적성, Evidence ceiling, 회귀·readback |
| 변형 | 범용 정답보다 저장소 정본·실제 diff·실행 결과 우선; LLM judge는 보조 Evidence |
| 제외 | 단일 self-evaluation을 진실 판정으로 사용, 모든 문장 원장화, 외부 SaaS 의무화, 테스트 정의만으로 PASS |

### 제안 PR 적대적 검토 재검증

| Finding | 재검증 | 최종 반영 |
|---|---|---|
| `SBE-015` 충돌 | 유효 P1 | 다음 사용 가능 ID `SBE-038` 사용 |
| Registry 고정 시 자동 호출 증거 부족 | 유효 P1 | 기존 owner의 `completion-claim`, `claim-evidence`, `intent-conformance`, `hallucination-audit` trigger/use_when 보강 |
| SimpleQA 표현 과장 | 유효 P2 | short factual question의 공식 범위로 교정 |
| `SUBMITTED`의 `approval_ref` 선기입 | P2 권고이나 사용자 구현 승인은 이미 존재하며 CI 실제 동작도 재검증 필요 | 상태는 `SUBMITTED`로 유지하고 `approval_ref`는 명시적 승인 증거 locator로 보존; 구현 완료와 혼동하지 않음 |
| Skill body 변경의 Learning Log 누락 가능성 | 유효 P1 | 중앙 `skills/SKILL_LEARNING_LOG.md` 갱신을 영향 경로에 추가 |

## 일반화 후보

### `MATERIAL_CLAIM_LEDGER`

결정·구현·검증·병합 상태를 바꾸는 material claim만 원자화한다.

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
→ exact SHA의 실제 저장소·등록 정본
→ 해당 SHA에서 실행된 도구·테스트·런타임 결과
→ 날짜·버전이 확인된 공식 외부 1차 출처
→ 명시적 추론
→ 작업자·Builder·모델 설명(검증할 lead일 뿐 Evidence 아님)
```

### `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`

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

### `COMPLETION_CLAIM_GATE`

| 주장 | 최소 Evidence |
|---|---|
| 구현 완료 | 실제 diff + 요구사항별 `implementation_paths` + 범위 밖 변경 부재 |
| 테스트/검증 완료 | 실행 명령·환경·결과 + exact HEAD + 실패 수 |
| 의도대로 동작 | Acceptance별 관찰 결과 + 필요한 Evidence level |
| 병합 완료 | PR merged 상태 + merge SHA + 새 `main` readback + post-merge 필수 검사 |

필수 Evidence가 없으면 `BLOCKED_UNVERIFIED` 또는 `IMPLEMENTATION_UNVERIFIED`를 유지한다. 파일 존재, Builder 보고, 모델 자신감은 PASS 근거가 아니다.

### 작업 구조

```text
승인 Intent·Acceptance·Protected Scope
→ material claim 원자화
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
- 프로젝트 정본 전체를 ledger에 복제하지 않는다.
- 외부 SaaS·LLM judge를 필수 조건으로 만들지 않는다.
- 낮은 Evidence에서 높은 Evidence를 추론하지 않는다.

프로젝트 전용:

- 게임별 플레이어 경험·UX·수치·세계관·Acceptance
- 실제 Godot scene·script·data·asset 경로
- 프로젝트별 테스트 명령과 플랫폼·device 조건
- 선택한 외부 Eval 도구와 dataset

## 반례와 위험

| 공격 | 검증 | 최소 대응 |
|---|---|---|
| 모든 문장을 원장화 | 비용 폭증 | material claim만 기록, L0 경량화 |
| 출처는 있으나 stale·충돌 | URL만으로 현재성 불충분 | 날짜·버전·exact SHA·counterevidence 요구 |
| 테스트 파일을 실행 결과로 오인 | 정의와 실행은 다름 | 명령·환경·HEAD·결과 요구 |
| Builder 자기확증 | 생산자 설명은 독립 Evidence 아님 | VERIFIER/CRITIC 역할 분리 |
| LLM judge 환각 | judge도 오류 가능 | deterministic-first, judge 보조, 미검증 허용 |
| 테스트 PASS로 UX·재미 과장 | Evidence 층 불일치 | E0–E6 ceiling과 사람 Evidence 유지 |
| 병합 직전 main 이동 | stale 검증 | exact-head/current-main/post-merge readback |
| 기존 owner와 중복 | 새 Skill 생성 시 충돌 | Mode/reference로 흡수 |
| trigger만 있고 live model 결과 없음 | 명시 경로와 실제 행동은 다름 | deterministic contract + `SBE-038`; live model은 미실행 시 `NOT_RUN` |

대표 반례:

1. 테스트 정의만 존재 → `CLAIM_UNVERIFIED`.
2. 다른 SHA에서 PASS → `CLAIM_UNVERIFIED`.
3. Acceptance 하나가 unmapped → `IMPLEMENTATION_UNVERIFIED`.
4. 기술 구조는 작동하지만 승인 UX 의미가 다름 → `PLANNING_CONFLICT`.
5. 공식 문서지만 버전·날짜가 결정과 불일치 → stale/contradictory.
6. merged 상태만 있고 main readback이 없음 → integration claim 미완료.

## 영향 범위와 검증

### 구현 대상

- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`
- `skills/SKILL_BEHAVIOR_EVALS.json`
- `skills/SKILL_LEARNING_LOG.md`
- `tests/test_neutral_adversarial_feature_lifecycle.py`
- `docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md`
- `docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md`

### 보호 대상

- ACTIVE Skill ID 집합과 전체 수 `30`
- `PLAN / BUILD / REVIEW` 세 Work Mode
- 릴리스된 Base lock·pin·immutable artifact
- 기존 owner와 responsibility boundary
- 프로젝트별 수치·세계관·구현 경로
- 기존 Evidence E0–E6 의미
- BCP-008 Traceability와 BCP-020 Player Experience Evidence owner

### 의도적 변경

- 기존 reviewer Skill의 trigger/use_when/review trigger metadata
- Registry 변경에서 파생되는 `docs/generated/BASE_ACTIVE_SKILLS.md` hash와 해당 row
- `SBE-038` fixture, 중앙 Learning Log, 계약 테스트

### RED→GREEN 검증

RED:

- 전용 계약 테스트와 `SBE-038`가 새 reference·Mode·Registry trigger·Template·작업 구조를 요구하도록 먼저 추가한다.
- 생산 계약이 없는 exact HEAD에서 GitHub Actions 실패를 관찰한다.

GREEN:

- focused unittest PASS
- Base v9 contract·integrity PASS
- active Skill ID 집합과 수 `30` 유지
- `python tools/build_base_v9_artifacts.py --check` PASS
- `SBE-038`이 REVIEW의 기존 owner와 새 Mode를 요구
- live model behavior는 실행되지 않으면 `NOT_RUN`으로 보고
- diff가 승인 영향 경로 안에 있음
- 독립 reviewer finding 검토, unresolved thread 0
- merge SHA와 post-merge `main` readback

### 롤백

구현 PR의 squash commit을 revert한다. Registry metadata·파생 요약·reference·Mode·Template·fixture·Learning Log·test를 함께 되돌려 부분 활성 상태를 남기지 않는다. 제품 데이터·런타임·릴리스 pin은 바꾸지 않는다.

## 승인과 구현

- 사용자 구현 승인 증거: 2026-08-13 현재 ChatGPT 세션의 직접 요청과 병합 지시
- 신규 제안 Registry 상태: `SUBMITTED`
- 승인된 구현 범위: 이 문서의 영향 경로·보호 대상·검증 계약
- 구현 방식: 제안 PR 병합 뒤 fresh `main`에서 별도 구현 PR
- 구현 PR: 아직 없음
