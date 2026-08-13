# BCP-2026-028 — Executable Review Evidence Binding

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 관찰 기준 Base 커밋: `3e3f59b1b835f9675f0b8dbc4543a6c69a526c36`
- 제출일: `2026-08-14`
- Registry 상태: `SUBMITTED`
- 지식 상태: `BCP-2026-027 후속 실행화 + 외부 1차 출처 비교 + 반례 TDD`
- 구현 후보 PR: `https://github.com/alsdmlals4-eng/Base/pull/330`
- 상태 설명: 이 PR은 공용 변경 제안만 등록한다. 신규 BCP는 proposal-only PR에서 `SUBMITTED`로 먼저 병합한 뒤 별도 구현 PR에서 승인·구현 상태와 exact-head 증거를 갱신한다.

## 관찰과 증거

BCP-2026-027은 이미 `MATERIAL_CLAIM_LEDGER`, `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`, `COMPLETION_CLAIM_GATE`, Evidence ceiling, exact HEAD, post-merge main readback을 정의했다. 현재 `reviewing-and-validating-project-changes`의 `claim-and-intent-verification` Mode와 전용 reference, 검수 템플릿, 계약 테스트도 존재한다.

그러나 현행 회귀는 주로 문구·경로·Registry·fixture 존재 여부를 검사한다. 작업자가 “구현 완료”, “테스트 통과”라고 기록해도 다음 사실을 독립 실행기로 대조하는 계층이 부족하다.

1. 검수자가 지정한 base ref와 현재 HEAD가 실제 commit이며 ancestor 관계인가?
2. worktree가 깨끗하고 실제 diff가 비어 있지 않은가?
3. 모든 변경 경로가 허용 범위 안이고 보호 경로는 그대로인가?
4. 각 Acceptance의 implementation path가 실제 diff에 포함되고 HEAD에 존재하는가?
5. 선언된 검증 명령을 현재 상태에서 실제 실행했는가?
6. 종료 코드 0뿐 아니라 기대 성공 marker도 관찰됐는가?
7. TEST 증거를 RUNTIME·RENDER·HUMAN 증거로 과장하지 않았는가?
8. 병합 전 결과를 integration PASS로 승격하지 않았는가?

### Existing Solution First

판정: `ABSORB`

새 ACTIVE Skill을 만들지 않는다. 기존 30개 ACTIVE Skill과 PLAN / BUILD / REVIEW 구조를 유지하고, 기존 owner `reviewing-and-validating-project-changes`의 `claim-and-intent-verification` Mode에 다음을 흡수한다.

- 입력 `REVIEW_EVIDENCE_RECORD` Schema
- 생성 결과 `REVIEW_EVIDENCE_RESULT` Schema
- exact Git·actual diff·fresh execution을 검사하는 Skill 내부 script
- fail-closed 템플릿
- 정상·반례 행동 테스트와 Required CI 소비 경로
- Skill 구현 증거 인덱스의 `TOOL + TEST` 연결

| 선택지 | 장점 | 위험 | 결론 |
|---|---|---|---|
| 새 hallucination Skill 생성 | 이름으로 발견하기 쉬움 | 기존 통합 검수 owner와 중복, 라우팅·학습 비용 증가 | 제외 |
| BCP-027 문구만 강화 | 변경량이 작음 | 파일 존재와 실제 실행의 간극이 그대로 남음 | 제외 |
| 기존 Mode에 실행 계약·검사기·반례를 흡수 | owner·상태어·Evidence ceiling·post-merge 절차 재사용 | 명령 실행 안전 경계가 필요 | 채택 |
| 외부 Eval SaaS·LLM judge 의무화 | 대시보드·평가 자동화 가능 | 비용·공급자 종속·보안·judge 환각 | 제외; 선택 보조만 허용 |

### 외부 1차 출처·현업 비교

- Chain-of-Verification은 초안 생성과 독립 검증 질문·응답·최종 교정을 분리한다. 이 제안도 생산자의 완료 문장을 증거가 아니라 검증 입력으로 취급한다.
  - https://arxiv.org/abs/2309.11495
- OWASP LLM09:2025는 LLM의 허위·오해 소지가 있는 출력과 과신을 위험으로 다루며, 검증·교차 확인과 human oversight를 권고한다.
  - https://genai.owasp.org/llmrisk/llm092025-misinformation/
- GitHub protected branch와 required status checks는 병합 가능성을 최신 commit의 검사 상태에 연결한다.
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- SLSA provenance는 산출물을 정확한 subject·source/build 정보에 연결한다. 이 제안은 서명 인프라를 추가하지 않고 exact base/HEAD와 actual changed files 결속 원칙만 채택한다.
  - https://slsa.dev/spec/v1.1/provenance
- NIST AI 600-1은 confabulation 통제에서 측정·문서화·사람/자동 평가·적대 검증을 함께 사용한다.
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

## 일반화 후보

### 입력 계약

생산자가 PASS나 SHA를 자기기입하지 않는다. 승인 Intent·범위·claim·Acceptance·검증 명령만 기록하고, 신뢰할 base ref는 reviewer 또는 CI가 실행 시 전달한다.

```text
approved intent + material claims + protected scope
→ REVIEW_EVIDENCE_RECORD
→ trusted base ref + current HEAD + clean worktree + actual diff
→ allowed/protected path gate
→ Acceptance-to-implementation-path gate
→ reviewed command execution (shell expansion 없음)
→ exit code + required marker
→ Evidence ceiling
→ REVIEW_EVIDENCE_RESULT
→ independent review
→ 기존 post-merge main readback
```

### Evidence ceiling

- 명령의 기본 최대 증거 등급은 `TEST`다.
- `RUNTIME`·`RENDER`는 reviewer가 해당 check ID를 명시 승인했을 때만 승격한다.
- 명령 출력으로 `HUMAN` 증거를 자동 생성하지 않는다.
- 실행하지 않았으면 `NOT_RUN`, 미충족 Acceptance는 `BLOCKED_UNVERIFIED` 또는 `CLAIM_UNVERIFIED`다.
- 병합 전 integration은 항상 `BLOCKED_UNVERIFIED`다.

### 명령 안전 경계

- 명시적 실행 flag가 없으면 명령을 실행하지 않는다.
- `subprocess.run`의 argv 목록을 사용하고 shell expansion을 사용하지 않는다.
- 현재 Python 외 program은 reviewer가 정확히 allowlist해야 한다.
- timeout, exit code, required output marker를 모두 확인한다.
- producer-controlled record는 증거가 아니라 verifier 입력이다.

## 적용 조건과 비사용 조건

적용:

- L2 이상 또는 결과 판정을 바꾸는 구현·검증 완료 주장
- 저장소와 재현 가능한 검증 명령에 접근할 수 있는 변경
- 외부 AI·Agent·병렬 작업자의 완료 보고 독립 검수
- protected path·actual diff·Acceptance mapping이 중요한 공용 변경

비사용 또는 경량화:

- 저장소가 없는 순수 창작 문장
- L0 오탈자·동일 입력의 단순 재실행
- 사람 사용성·재미·시장성을 자동 명령만으로 평가하는 작업
- 현재 환경에서 재현할 수 없는 외부 서비스·기기 검증

이 경우 기존 원장·Evidence ceiling·`NOT_RUN`/`BLOCKED_UNVERIFIED` 상태를 유지하되 거짓 PASS를 만들지 않는다.

## 반례와 위험

| 공격·실패 | 판정 | 최소 대응 |
|---|---|---|
| 자신감 있는 “완료” 문구 | 증거 아님 | actual diff·fresh run으로 재검사 |
| 테스트 파일만 존재 | `NOT_RUN` | 명시 실행과 결과 필요 |
| 다른 SHA의 PASS | stale evidence | exact base/HEAD 기록 |
| base와 HEAD가 같음 | no-op | 빈 diff 차단 |
| dirty worktree | HEAD와 불결속 | 실행 전 clean 상태 요구 |
| 허용 범위 밖·보호 경로 변경 | 구현 Gate FAIL | path pattern 대조 |
| 종료 코드 0이나 성공 marker 없음 | 검증 Gate FAIL | marker와 exit code 모두 요구 |
| arbitrary executable | 안전 경계 위반 | current Python 기본, 나머지 명시 승인 |
| self-declared RUNTIME | Evidence inflation | 기본 TEST ceiling |
| unit test PASS로 HUMAN 주장 | 층위 위반 | HUMAN 자동 승격 금지 |
| pre-merge 결과로 병합 완료 주장 | integration 과장 | merged state·merge SHA·main readback 별도 확인 |
| `[수정제안서]` 같은 대괄호 경로 | glob 오판 가능 | literal bracket 회귀 테스트 |

남은 위험:

- 실행 허용된 프로그램 자체가 외부 상태를 변경할 수 있으므로 reviewer는 명령을 사전 검토해야 한다.
- RUNTIME/RENDER 등급 승격은 명령 이름이 아니라 실제 절차·환경을 사람이 확인해야 한다.
- 이 구조는 사실·구현 검증을 강화하지만 재미·미감·시장성을 자동 판정하지 않는다.

## 영향 범위와 검증

예정 영향:

- `skills/reviewing-and-validating-project-changes/` 내부 script·Schema·reference
- `templates/quality/` 검수 record·report surface
- `tests/` 정상·반례·Required CI 통합 계약
- `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`과 생성 evidence 문서
- 본 BCP의 상태·승인·구현 PR 기록

보호 대상:

- ACTIVE Skill 수와 PLAN / BUILD / REVIEW Mode 수
- 제품·Godot·scene·data·asset·project migration
- 기존 BCP-027의 상태어와 post-merge readback 계약
- 외부 Eval SaaS·서명 서비스 비의무화

검증 계약:

1. Schema 자체와 기본 template을 검증한다.
2. 임시 Git 저장소에서 exact base/HEAD·actual diff·fresh command PASS를 확인한다.
3. 미실행·실패 명령·marker 누락·stale/dirty Git·범위 이탈·보호 경로·Evidence inflation 반례가 non-zero/FAIL인지 확인한다.
4. 기존 Required CI가 production verifier를 실제 import·실행하는지 확인한다.
5. 구현 PR의 exact HEAD CI와 병합 후 새 main readback을 별도로 확인한다.

롤백: 구현 PR 한 건을 revert하면 script·Schema·template·tests·reference·evidence index를 함께 제거할 수 있다. BCP-027과 제품 프로젝트는 영향받지 않는다.

## 승인과 구현

- 현재 상태: `SUBMITTED`
- 승인 상태: `PENDING_REGISTRY_MERGE`
- 승인 locator: proposal-only PR 병합 뒤 이 절의 사용자 지시 기록을 사용한다.
- 사용자 요청 근거: 2026-08-14 현재 ChatGPT 세션에서 “검수 작업에서 실제로 구현 되는지, 할루시네이션은 아닌지도 확인할 스킬, 구조를 추가”하고 병합까지 진행하라는 지시.
- 구현 후보: 기존 owner에 `ABSORB`; draft PR `#330`
- 완료 조건: 제안 Registry 병합 → 구현 PR 최신 main 재기준화 → exact-head 테스트·CI GREEN → PR 병합 → merge SHA·새 main 파일 readback·post-merge 검사 확인.
