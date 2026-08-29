# 자율 품질·선제 후보 제작·증거 기반 교정 설계

```yaml
status: USER_APPROVED_EXECUTION_DESIGN
approved_at: 2026-08-29 KST
baseline_repository: alsdmlals4-eng/Base
baseline_main_sha: b384f4750b06287a0768dee5b2077807a41484e5
scope:
  - GPT custom-instruction template
  - image generation/review authority
  - implementation research and feasibility gate
  - long-horizon optimization
  - low-intervention automation and learning
  - evidence-backed adversarial review
implementation_owner: GPT_WORK_BASE_GOVERNANCE
runtime_product_implementation: NOT_IN_THIS_BASE_CHANGE
```

## 1. 목표

이 설계는 다음 사용자 결정을 Base와 프로젝트 작업에 재사용 가능한 계약으로 승격한다.

1. 실제 필요성이 확인된 이미지는 기존 프로젝트 정본·승인 이미지·시안을 먼저 읽고 일관된 후보를 제작한 뒤 사용자에게 `LOCK / REVISE / REJECT`를 받는다.
2. 실제 시스템·데이터·Scene·Resource·UI·자동화 구조는 최신 공식/1차 자료, 직접 관련된 실무 사례와 최소 세 개의 실질 대안을 비교하고 현재 프로젝트에서 실제 구현 가능한지 검증한다.
3. 빠른 임시 완료보다 장기 효율, 유지보수성, 검증 가능성, 재사용성, 완성도를 우선하되 근거 없는 과설계는 피한다.
4. 사용자의 반복 관여를 줄이고 조사·비교·후보 제작·검증·교정·readback·교훈 환류를 승인 범위에서 자동 진행한다.
5. 적대적 검토는 보고 문구가 아니라 실제 읽기·검사·수정·재검증 증거로만 계수한다.

## 2. 비교한 접근

| 접근 | 장점 | 위험 | 판정 |
|---|---|---|---|
| A. 모든 이미지 생성 전 사용자 승인 | 오생성 위험이 낮음 | 반복 중단과 승인 피로, Blueprint 준비 지연 | REJECT |
| B. 이미지 완전 자동 생성·자동 승격 | 사용자 개입 최소 | 시각 방향 drift, 불필요한 대량 생성, 승인·runtime 상태 혼동 | REJECT |
| C. 구체적 필요 확인 후 후보 선제작, 사후 최종 잠금 | 흐름을 끊지 않으면서 최종 통제 유지 | 필요성·정본 readback·상태 분리 Gate 필요 | ADOPT |
| D. 빠른 최소 패치 우선 | 즉시 결과 | 반복 부채와 검증 누락 | REJECT_AS_DEFAULT |
| E. 모든 미래 상황을 포괄하는 대형 자동화 | 재사용 가능성 | 과설계·유지비 증가 | REJECT |
| F. 현재 반복비용이 큰 단계부터 점진 자동화 | 장기 효율과 위험 제어의 균형 | 측정·환류 규칙 필요 | ADOPT |

## 3. 외부 근거와 적용

- OpenAI ChatGPT Projects는 프로젝트별 지침이 전역 맞춤형 지침을 덮어쓰므로, 전역에는 안정적인 공용 원칙을 두고 프로젝트별 현재 사실은 저장소와 프로젝트 지침에서 읽는다.
  - https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- OpenAI 맞춤형 지침은 모든 채팅에 즉시 적용되고 Pro는 5,000자 한도이므로, 변동 상태·SHA·프로젝트 세부 규칙을 복제하지 않는 압축된 bootstrap이 적합하다.
  - https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions
- Godot 4.7 공식 Best Practices는 Scene 조직, Scene/Script 경계, Autoload, data/logic/project organization을 별도 판단 대상으로 두므로, 구현 가능성은 실제 Scene·Node·Resource·data owner에서 확인해야 한다.
  - https://docs.godotengine.org/en/4.7/tutorials/best_practices/index.html
- GitHub status checks는 특정 commit이 저장소 조건을 충족하는지 보여 주며 required check는 merge 전에 통과해야 하므로, `검토했다`는 서술 대신 exact-head check/readback을 증거로 사용한다.
  - https://docs.github.com/en/enterprise-cloud@latest/pull-requests/reference/status-checks
- Google SRE의 toil 제거 지침은 반복·수동·자동화 가능한 작업을 식별하고 비용 대비 효과, 방어적 안전장치, 부분 자동화, feedback 개선을 요구한다. 따라서 사용자 개입 최소화는 무조건 자동화가 아니라 위험 시 사람에게 되돌아오는 점진 자동화다.
  - https://sre.google/workbook/eliminating-toil/
- Google SRE postmortem 지침은 문제·원인·조치·재발 방지 action을 기록하고 실제로 추적할 때 학습 효과가 생긴다고 본다. 따라서 교훈은 대화 요약이 아니라 owner·검증·재발 방지 변경으로 환류한다.
  - https://sre.google/sre-book/postmortem-culture/

## 4. 이미지 후보 선제작 계약

```text
NEED_CONFIRMED
→ PROJECT_AND_CONSUMER_READBACK
→ APPROVED_VISUAL_ANCHOR_RESOLVED
→ BRIEF_READY
→ GENERATE_ONE_CANDIDATE
→ USER_LOCK | USER_REVISE | USER_REJECT
→ LOCK only: CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_VERIFIED
```

### 4.1 생성 권한

`NEED_DRIVEN_GENERATE_THEN_LOCK`

다음 조건을 모두 만족하면 별도의 생성 전 승인 질문 없이 후보 1건을 만들 수 있다.

- 구체적인 `GAME_RUNTIME`, `PLANNED_GAME_SURFACE`, `PLAYER_FACING_EXPLANATORY`, `PRODUCT_DISTRIBUTION` 소비처 또는 현재 Blueprint 검수에 필요한 planning-board 목적이 있다.
- 프로젝트의 최신 visual canon, 기존 승인 이미지, 시안과 실제 consumer를 읽었다.
- 기존 자산 재사용·편집으로 해결 가능한지 먼저 확인했다.
- 유지 요소, 금지 drift, 규격, 상태군, 권리·provenance 경계를 brief로 고정했다.
- host/system policy가 이미지 생성을 허용한다.

다음은 생성 권한이 아니다.

- 막연한 이미지 공백
- 채팅을 시작했다는 사실
- consumer 없는 장식성 이미지
- 기존 승인 자산을 새로 보이게 만들고 싶은 욕구
- 다른 프로젝트의 시각 결과를 편의상 복제하는 행위

### 4.2 상태 분리

```text
GENERATED_CANDIDATE
!= USER_LOCKED
!= PROJECT_ASSET_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

후보 생성 뒤 사용자는 최종적으로 `LOCK / REVISE / REJECT`만 결정한다. `LOCK` 전에는 tracked production path, asset manifest final 상태, Scene 연결 또는 runtime PASS로 승격하지 않는다.

### 4.3 범위 제어

- 기본 생성 단위는 시각 deliverable 1건이다.
- 사용자 또는 current package가 명시한 state family는 하나의 bounded batch로 준비할 수 있다.
- 별개 캐릭터·화면·스타일·variant로 자동 연쇄 확장하지 않는다.
- 실제 이미지 생성·편집은 image model로만 한다.
- Mermaid, Flow, 표, JSON과 정확한 구조도는 text-native artifact로 유지한다.

## 5. 구현·실구조 연구와 가능성 Gate

`CURRENT_RESEARCH_AND_IMPLEMENTATION_FEASIBILITY_REQUIRED`

L1 이상 시스템·UX·데이터·Scene·Resource·파이프라인·자동화 결정은 다음을 실제로 수행한다.

```text
current repository owner and implementation read
→ existing project/Base solution search
→ current official/primary-source research
→ at least 3 materially distinct viable alternatives
→ ADOPT / ADAPT / TEST / REJECT
→ actual project boundary mapping
→ FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
→ specification + rollback + verification plan
```

구현 가능성 기록에는 최소 다음이 포함된다.

- player/user value와 actual consumer
- Godot version 및 API compatibility
- Scene·Node·Resource·script 책임
- data schema와 save/load/migration
- UI state·input·accessibility
- 이미지·오디오·텍스트·animation dependency
- performance/platform/security/rights risk
- test seam, debug signal, rollback
- Codex가 실행할 bounded implementation package
- automated/runtime/human evidence ceiling

`RESEARCH_SUMMARY_IS_NOT_IMPLEMENTATION_PROOF`: 링크 목록이나 문서상 가능성은 구현 PASS가 아니다.

## 6. 장기 품질과 과설계 방지

`LONG_TERM_EFFICIENCY_AND_COMPLETENESS_FIRST`

선택 기준은 다음 순서다.

1. 플레이어·사용자 가치
2. 정본과 책임 owner의 명확성
3. 자동 검증·rollback 가능성
4. 유지보수·확장·재사용성
5. 총 반복비용과 사용자 개입 감소
6. 출시 수준 품질
7. 현재 범위에 필요한 최소 복잡도

`NO_UNSUPPORTED_OVERENGINEERING`: 미래 가능성만을 이유로 새로운 framework, service, schema, abstraction 또는 paid dependency를 만들지 않는다. 장기 개선은 측정 가능한 반복비용·품질·위험 감소가 구현·유지 비용보다 클 때 채택한다.

## 7. 자동화·최적화·학습 루프

```text
READ CURRENT AUTHORITY
→ RESEARCH / COMPARE
→ PREPARE CANDIDATE OR IMPLEMENTATION PACKAGE
→ EXECUTE SAFE WORK
→ VERIFY / READBACK
→ ADVERSARIAL REVIEW
→ CORRECT VALID FINDINGS
→ REVERIFY
→ RECORD INCIDENT / SOLUTION / LESSON
→ PROMOTE REUSABLE RULE OR AUTOMATION
→ RECALCULATE REMAINING WORK
```

사용자에게 올리는 결정은 핵심 제품 의미, 최종 visual lock, 큰 비용·범위 증가, 보안·권한, 파괴적 migration·삭제·배포와 객관적 우열이 없는 취향 선택으로 제한한다.

반복 가능한 조사·검증·readback·문서 동기화·회귀 교정은 가능한 범위에서 자동 수행한다. 위험 또는 정본 충돌을 만나면 fail-closed로 사용자에게 되돌린다.

## 8. 증거 기반 적대적 검토

`CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID`

L1 이상 retained change는 최소 5회의 full-scope loop 후 clean exit까지 진행한다. 각 loop는 다음 receipt를 남겨야 계수된다.

```yaml
loop_index:
input_exact_head:
actual_reads: []
actual_commands_or_checks: []
findings: []
validation_of_findings: []
corrections_applied: []
verification_results: []
untouched_consumers_rechecked: []
better_alternative_search:
long_term_fit_recheck:
remaining_blockers: []
output_exact_head:
```

다음은 loop 증거가 아니다.

- `검토 완료`, `문제 없음` 같은 서술만 존재
- 같은 diff를 다시 읽지 않고 관점 이름만 바꿈
- 실행하지 않은 test/runtime/readback을 PASS로 기재
- finding을 발견했지만 수정·blocker 기록 없이 종료
- exact head·경로·명령·결과가 없는 자체 주장

## 9. Blueprint 구현 승인과의 관계

후보 이미지와 자료는 Blueprint 검수 전에 준비할 수 있다. 그러나 신규 구현 package는 기존 `BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE`를 유지한다.

```text
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

`GENERATED_CANDIDATE`는 `USER_FINAL_REVIEW_APPROVAL`이나 implementation authority를 대신하지 않는다.

## 10. 완료 기준

- 맞춤형 지침 템플릿이 repository-first와 네 사용자 원칙을 반영한다.
- assistant-initiated concrete visual need가 사전 생성 승인 없이 후보 1건을 만들 수 있다.
- old two-turn rule은 active path가 아니라 superseded compatibility marker로만 남는다.
- final visual lock·asset promotion·runtime evidence는 분리된다.
- research/benchmark/feasibility는 actual project boundary를 요구한다.
- 장기 효율과 과설계 방지가 함께 명시된다.
- 사용자 개입 최소화와 fail-closed 경계가 함께 명시된다.
- 적대적 검토는 loop별 실제 증거 없이는 계수할 수 없다.
- 회귀 테스트와 exact-head CI/readback이 통과한다.
- 프로젝트 전수 감사 결과가 `CHANGE_REQUIRED` 또는 `ALREADY_ALIGNED`로 기록된다.
