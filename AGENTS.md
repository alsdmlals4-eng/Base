# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** Skill·Template·Case·Test의 원본이다. 이 파일은 모든 Base 작업에 항상 적용되는 불변 규칙만 책임진다. 요청별 탐색은 `START_HERE.md`, 전체 운영 생명주기는 `docs/OPERATING_MODEL.md`, Work Mode·Skill 선택과 병합 게이트는 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 기획 우선·Grill Me 승인 배치는 `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`, 장기 작업 공용 계약은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, 문서 위치는 `docs/DOCUMENTATION_MAP.md`가 책임진다.

## 1. 권한과 읽기 순서

우선순위는 다음과 같다.

1. 사용자의 최신 지시
2. 대상 프로젝트 `AGENTS.md`와 보안·엔진·데이터 규칙
3. 프로젝트 Active Context와 승인된 작업 계약
4. 등록된 책임 원본과 실제 코드·데이터·자산·테스트
5. 프로젝트가 채택한 Base 계약
6. Base 원격 원본
7. 외부 사례·리뷰·과거 대화·초안·추정

- 정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다.
- 외부 벤치마크·리뷰·커뮤니티·모델 해석은 요구사항 권한이나 구현 사실의 정본이 아니다.
- **사용자가 작업 근거로 직접 제공한 외부 링크의 본문을 현재 도구로 읽지 못하고 그 내용이 작업에 필요하면 즉시 `BLOCKED_UNVERIFIED`로 작업을 중단하고 원문 텍스트·파일·스크린샷 등 현재 세션에서 검증 가능한 형태를 요청한다. 링크 제목·검색 스니펫·과거 기억·주변 자료·추정으로 내용을 대체해 진행하지 않으며, 사용자가 원문을 제공하거나 해당 자료 없이 진행하라고 명시하기 전에는 다른 독립 작업으로 임의 전환하지 않는다. 이 예외는 3절의 연속작업 blocker recovery보다 우선한다.**
- 저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.
- 모든 파일과 전체 `skills/`를 기본 로드하지 않는다. `skills/SKILL_REGISTRY.json`의 trigger로 최소 Skill만 고르고, 현행 목록은 `docs/generated/BASE_ACTIVE_SKILLS.md`에서 확인한다.

## 2. 작업 진입 게이트

- L1 이상 작업은 최신 main, 현재 결정, 분야 정본, 같은 Goal의 열린·최근 병합 PR, 실제 구현을 비교해 중복·누락·충돌·구형 참조·미반영을 먼저 판정한다.
- **`DEEP_WORK_PREANSWER_GATE` / `REQUIRED_EVIDENCE_BEFORE_FINAL`:** L1 이상 또는 사용자가 조사·벤치마킹·검토·구현·검증을 요청한 작업은 저장소/현재 정본 조사, 필요한 인터넷·외부 원출처 조사, 최소 3개 실질 대안 비교, 구현 현실성 확인, 요구된 적대적 검토와 실제 검증을 **수행한 뒤에만** substantive final answer를 낸다. 계획을 말하거나 빠른 초안을 내는 것은 이 Gate의 완료가 아니다.
- **`NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION`:** 필수 조사·벤치마킹·테스트·검토가 `NOT_RUN`이면 완료 답변을 금지한다. 실행 불가능한 항목은 `BLOCKED_UNVERIFIED`와 필요한 해제 조건으로만 보고한다.
- **`INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION`:** 사용자가 중간보고를 줄이거나 한 번에 끝내 달라고 해도 사용자에게 보이는 설명만 줄인다. 실제 조사·도구 호출·대안 비교·검토·테스트·readback은 생략하거나 뒤로 미루지 않는다.
- **`GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY` / `REASONING_EFFORT_IS_NOT_WORK_EVIDENCE`:** GPT가 주 기획자·검수자라는 뜻은 채팅 문장만 작성한다는 뜻이 아니다. `매우 높음` 같은 추론 강도는 사고 자원일 뿐 저장소 readback, 인터넷 원출처, 실제 Tool 호출, 실행·테스트·렌더 증거를 대신하지 않는다.
- **`REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF`:** 별도 Codex 인계는 GPT가 현재 도구로 직접 수행할 수 없고 filesystem/runtime/build 권위가 필요할 때만 선택적이다. 반대로 현재 요청의 필수 evidence를 이 세션의 browser·repository·connector·runtime Tool로 얻을 수 있으면 실제 호출은 의무이며, `OPTIONAL_CODEX_EXECUTOR`를 이유로 생략하지 않는다.
- **`OPEN_PR_READ_ONLY_BY_DEFAULT` / `FOLLOW_UP_TARGET_IS_MERGED_MAIN`:** `open/draft/ready` PR·Branch는 현재 작업자의 활동 여부와 무관하게 기본 read-only 보호 대상이다. 같은 Goal의 현황·충돌 확인에는 읽을 수 있지만 checkout/write/rebase/close/merge/selective-copy/material-delta 흡수 대상으로 삼지 않는다. 기본 후속 수정 대상은 최신 completed `main`에 실제로 유지된 변경뿐이다. 단, 아래 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`를 만족하는 현재 작업의 own PR은 그 예외 범위 안에서만 계속 실행한다.
- **`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`:** 열린 PR을 변경·인수·종료·병합·흡수하려면 사용자가 현재 작업에서 **PR 번호와 허용 동작을 명시적으로 지정**하는 것이 기본이다. “현재 채팅만 활성”, 같은 Goal, owner evidence 부재, standing authorization은 예외 권한이 아니다. 다만 아래 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`는 이미 승인된 동일 작업 계약이 **직접 생성한 단일 current-task PR**에 한해 별도 PR 번호 재입력을 요구하지 않는 좁은 예외다.
- **`CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`:** `APPROVED_CONTRACT_CONTINUATION`이 활성이고, 현재 승인된 작업 계약이 latest completed `main`에서 직접 만든 **단 하나의 명확한 current-task PR**이라면 `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행`, `끝까지 진행` 같은 continuation intent는 그 PR의 안전한 latest-main reconciliation, exact HEAD 재검증, repository가 요구하는 `required checks`·review·unresolved-thread·ruleset Gate 통과 뒤 merge, 그리고 `postmerge readback`까지 포함한다. 이 경우 같은 작업에 대해 PR 번호를 다시 요구하지 않는다. 이 예외는 `pre-existing`, `unrelated`, `other-workstream`, `draft` PR, 복수의 모호한 PR 후보, 다른 작업의 material delta 흡수·종료·supersede에는 적용되지 않는다. `force push`, direct `main` push, `--admin`, `ruleset bypass`는 계속 금지한다. 사용자가 `병합하지 마`, `PR만 열어`, `검토만`처럼 더 좁게 지시하면 그 최신 지시가 우선하며 merge 권한을 제거한다.
- **`CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`:** L1 이상 중요한 설계·구현·정책 결정은 한 방법을 먼저 정해 놓고 근거를 끼워 맞추지 않는다. 먼저 **현행 조사**로 실제 상태·기존 해법·제약·실패 사례를 확인하고, 현행 유지·재사용·흡수·최소 수정·구조 개선·신규 구축 등 현재 Goal에서 실제로 가능한 **최소 3개**의 materially distinct 유효 대안을 확보해 동일 기준으로 비교한다. `MINIMUM_VIABLE_ALTERNATIVES: 3`. 숫자를 채우기 위한 허수 대안은 금지하며, 세 후보를 찾기 어렵다면 조사·추상화 수준을 넓혀 전략적으로 다른 실행 경로를 더 찾는다. 조사 뒤에도 세 실질 후보를 만들 수 없는 특수 제약이라면 임의로 기준을 낮추지 말고 그 제한과 탈락 근거를 `BLOCKED_UNVERIFIED` 또는 해당 Decision evidence로 남긴다.
- **`BETTER_ALTERNATIVE_SEARCH`:** 최초 비교에서 권장안을 고른 뒤에도 새 증거·실패·검토 finding이 나오면 **더 나은 방안**이 생겼는지 다시 탐색한다. 기존 선택을 지키는 것이 목표가 아니며, 승인된 큰 방향을 보존하면서 더 강한 기술적 방법이 확인되면 근거와 함께 교체한다. 핵심 게임 방향·플레이어 경험·비용·범위를 바꾸는 더 나은 안이면 `USER_DECISION_REQUIRED`로 올린다.
- **`LONG_TERM_PLAN_FIT_REQUIRED`:** 권장안은 단기 구현량뿐 아니라 **장기계획**에 적합한지 반드시 판정한다. 사용자/플레이어 가치, 정확성·기획 충실도, 위험, 수명주기 비용, 유지보수성, 되돌리기 난이도, 재사용·모듈성, Base의 향후 변화에 대한 신선도·호환성, 증거 강도, 현재 비용 경계를 함께 비교하고, 어떤 조건에서 권장안을 재검토해야 하는지도 기록한다.
- **`BEST_LONG_TERM_EFFICIENT_METHOD` / `QUALITY_OVER_RESPONSE_SPEED` / `BENCHMARK_PRACTICE_COMPARISON`:** Base와 이를 적용한 프로젝트의 기본 목표는 **현재 가능한 방법 중 사용자·플레이어 가치, 정확성, 출시 품질, 유지보수성, 재사용성, 되돌리기 가능성, 수명주기 비용을 함께 보아 가장 효율적이고 장기적인 방법**을 찾고 실행하는 것이다. 효율을 가장 빠른 답변·최소 Tool 호출·최소 토큰으로 축소하지 않는다. 중요한 작업은 필요한 만큼 더 오래 조사하고 더 많은 추론·도구·검증 자원을 사용해도 되며, 답변 속도보다 증거와 결과 품질을 우선한다. 현행 정본·실제 구현을 확인한 뒤 최소 3개 실질 대안을 공식/1차 자료, 벤치마크, 현업 운영 방식, 실무 성공·실패 사례와 비교하고 `ADOPT / ADAPT / REJECT` 및 장기 총비용으로 판정한다.
- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:** L1 이상에서 적대적 검토를 실행하면 `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`를 적용한다. **전체 승인 범위 적대적 검토 → 충돌·누락·오류·위험 finding 검증 → 검증된 finding 개선·보완 → 실제 검증·회귀검사 → 개선된 상태 전체를 다시 공격**하는 완전한 개선 루프를 **최소 5회** 수행하며, 5회의 완전한 전체 개선 루프를 마치기 전에는 finding이 0이어도 `CLEAN_REVIEW_EXIT`로 종료하지 않는다. **5회 이후에도** 새로 검증되는 `MUST_FIX`·blocking finding·정본 충돌·acceptance failure가 하나라도 나오면 수정·검증 뒤 추가 전체 루프를 계속한다. 종료는 최소 5회를 충족한 뒤 **새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정의 회귀가 없으며, acceptance criteria·정본 신선도·증거 ceiling을 모두 만족하는 `CLEAN_REVIEW_EXIT`**으로만 판정한다. 5회는 최소 floor이지 최대치가 아니며, 횟수를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않는다.
- 벤치마킹·현업/실무 조사·성공사례·실패사례는 최소 3개 대안의 원리와 실패조건을 비교하는 근거로 사용하고, `ADOPT / ADAPT / REJECT`로 현재 환경 적합성을 판정한다. 외부 사례가 Base 요구사항 정본이 되지는 않는다.
- **`ZERO_INCREMENTAL_COST_REQUIRED`:** Base와 Base를 적용한 프로젝트의 기본 실행 경로는 사용자의 추가 금전 지출을 만들지 않아야 한다. 이미 보유한 구독 기능도 해당 기능이 구독에 포함되고 별도 API·credit·marketplace·runner·storage·SaaS 같은 **separately metered** 과금으로 전환되지 않는 범위에서만 사용한다. `pay-as-you-go` API, 유료 credit, 신규 유료 구독·구매, 별도 과금 compute·runner·service는 사용자가 이 정책을 명시적으로 바꾸기 전에는 도입·실행하지 않는다. 비용 상태를 확정할 수 없으면 live call·구매·유료 실행을 하지 않고 `COST_GATE_BLOCKED`로 둔다. CI의 구체적 실행·비용 계층은 `docs/CI_EXECUTION_COST_POLICY.md`가 책임진다.**
- **현재 유료 플랜 고정:** `CURRENT_PAID_PLANS: GPT_PRO`, `PAID_PLAN_COUNT: 1`. 현재 기본 유료 플랜은 **GPT Pro 하나**다. Notion은 별도 유료 기능이나 metered billing 없이 Free 범위에서 사용한다. 다른 유료 AI/API/SaaS/상위 플랜/marketplace/runner/compute/storage를 사용하거나 결제하려면 **새 사용자 승인**이 필요하다.
- **Existing Solution First Gate:** 신규 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층은 현재 사용 도구·connected MCP·enabled addon·dependency·같은 Goal의 열린/최근 병합 PR·유지되는 외부 대안을 먼저 조사하고 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` 판정을 기록하기 전에는 설계·구현하지 않는다. Godot 관련 정본은 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`이며, 직접 제작 판단은 `evaluating-godot-assets-and-plugins-before-creation`이 소유한다.
- `BUILD_NEW`는 기존 대안의 핵심 기능·보안·라이선스·유지·Godot/OS/클라이언트 적합성 결함을 설정·격리·bounded patch로 해결할 수 없다는 증거와 사용자 승인이 있어야 한다. “직접 만들면 더 엄격하다”는 단독 근거가 아니다.
- 검증·승인된 애드온이 현재 작업의 실제 문제를 해결하면 직접 중복 구현보다 활용을 우선한다. 단, 모든 프로젝트에 일괄 설치하지 않는다. 프로젝트 단계·Godot 버전·플랫폼·권위 경계·실제 소비 경로를 확인하고 필요한 프로젝트에만 선택적으로 채택한다.
- 설치된 애드온은 편집기 작업, 런타임 기능, 테스트·CI, 플랫폼 서비스 또는 콘텐츠 제작 파이프라인 중 하나 이상의 실제 소비 경로를 가져야 한다. 소비 경로가 없으면 `INSTALLED_UNUSED`로 판정해 제거하거나 도입을 연기한다.
- HiGodot 단일 권위는 Godot 저작·편집 자동화의 중복 실행 권위를 금지하는 규칙이다. 역할이 다른 테스트·대화·플랫폼 서비스·개발 편의 애드온의 검증된 선택적 사용을 전면 금지하지 않는다.
- 새 정책·Template·Skill·경로·ID는 파일 존재가 아니라 README·`START_HERE.md`·운영 정본·Registry·프로젝트 Template·활성 소비자·Test 연결을 확인한다.
- 필요한 실행 파일, 라이브러리, 폰트, 입력, 인증, 저장소·브랜치 권한을 작업과 검증 전에 확인한다.
- 누락 환경은 `필요 항목 / 이유 / 설치·설정 / 적용 / 확인 명령 / 최소 권한`으로 안내한다. 사용자 승인 없이 시스템 전역 설치, 계정·보안 설정, 권한 확대, Branch protection 변경을 수행하지 않는다.
- 사용자가 설치·권한 부여를 알렸어도 실제 경로·버전·인증·쓰기 가능 여부를 다시 확인한다.
- 실행하지 않은 조사·검사·테스트·렌더·빌드·권한을 통과로 보고하지 않는다.
- 문서·Skill의 줄 수·문자 수·분량 상한보다 내용 보존, 실행 가능성, 한 단계 발견성을 우선한다.

## 2.1 중립적 결론과 동의 편향 방지

- 사용자 주장과 AI의 최초 제안은 모두 검토 가능한 가설로 취급하고 동일한 평가 기준을 적용한다.
- 권장안·판정·설계 선택은 평가 기준, 유효한 대안, 반증, 이익·비용·위험, 되돌리기 난이도와 미검증을 비교한다.
- 사용자의 선호나 이전 승인만을 이유로 근거 없는 동의를 하지 않는다.
- 적대적 검토를 반대를 위한 반대로 오용하거나 유효한 장점을 억지로 부정하지 않는다.
- 검토 뒤 사용자안이 가장 강하면 근거와 함께 동의하고, 다른 안이 더 강하면 근거와 함께 이견을 제시한다.
- 판정할 증거가 없으면 결론을 꾸미지 않고 `BLOCKED_UNVERIFIED`와 확인 조건을 기록한다.

## 2.2 기획 우선 원칙

- `L1` 이상 작업은 `PLAN`에서 최신 정본·실제 구현·대안·기획 충돌·완료 기준·검증·롤백을 먼저 닫는다. 사용자 승인 또는 기존에 승인된 실행 계약 없이 제품·정본 변경 `BUILD`에 진입하지 않는다.
- `L0` 오탈자, 명백한 단일 파일 기계 수정, 동일 입력 검사 재실행은 기획 우선 Gate의 예외다.
- 프로젝트 방향을 바꾸지 않는 가역적 상세 데이터·초기 시험 수치는 `DETAILED_NUMERIC_DEFAULT`이자 `RECOMMENDED_DEFAULT`로 GPT 권장안을 적용하고 근거·조정 조건·검증·미검증을 기록한다.
- 난이도 곡선·경제·성장 속도·세션 길이·빌드 우열·보상 의미·핵심 플레이 경험 또는 분야 책임 원본이 충돌하면 `PLANNING_CONFLICT`, `USER_DECISION_REQUIRED`, `GRILL_ME_REQUIRED`로 분류하고 Grill Me 사용자 승인 전 확정하지 않는다.
- Grill Me 승인 Decision은 즉시 활성 배치 Branch와 GitHub 추적 surface에 같은 Decision ID로 기록한다. `MAX_APPROVED_DECISIONS_PER_BATCH: 10`은 최소 대기량이 아니라 최대 배치 크기이며, 10건 또는 조기 체크포인트에서 하나의 PR로 exact-head 검사와 `attack → validate-critique → regression-recheck → decision-report`를 수행한다.
- 10번째 승인 뒤에는 배치 PR 병합·재동기화 전 11번째 질문을 금지한다. `unresolved thread 0`, `P0/P1 0`과 필수 검사가 충족된 뒤 병합하고 merged main SHA와 구성된 프로젝트 workspace를 재조회해 `SYNCED_TO_MAIN`을 확정한다.

상세 상태·조기 체크포인트·workspace 의미는 `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`가 책임진다.

## 2.3 장기 작업 불변 계약

장기·복합 L1 이상 작업은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`를 적용한다. 이 계약은 새 Skill이 아니라 기존 intake·검증·archive·Loop Engineering 책임을 연결한다.

```text
DIRECTION_FIRST
DEEP_WORK_PREANSWER_GATE
REQUIRED_EVIDENCE_BEFORE_FINAL
NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION
INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION
GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY
REASONING_EFFORT_IS_NOT_WORK_EVIDENCE
REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF
CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY
MINIMUM_VIABLE_ALTERNATIVES: 3
BENCHMARK_SYNTHESIS
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
BEST_LONG_TERM_EFFICIENT_METHOD
QUALITY_OVER_RESPONSE_SPEED
BENCHMARK_PRACTICE_COMPARISON
EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD
SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
REQUIRED_WORK_REMAINING
POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP
POSTMERGE_CORRECTION_REQUIRED
PROGRESS_READBACK_REQUIRED
NOTION_DEFAULT_PROJECT_WORKSPACE
PROJECT_RELATION_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
```

- 전체 방향·의도·플레이어 가치와 실제 정본을 먼저 고정하고, 최소 3개 실질 대안과 벤치마킹·실무사례·실패사례를 비교한 뒤 예상 효과·문제·보완·롤백을 BUILD 전에 제시한다.
- 중간보고 생략은 사용자 노출을 줄이는 것일 뿐 실제 연구·검토·실행을 줄이는 지시가 아니다. 필수 evidence가 `NOT_RUN`이면 완료 답변 대신 차단 상태를 보고한다.
- 최초 권장안 뒤에도 새 증거·finding이 생기면 더 나은 방안을 다시 찾고, 선택안이 장기계획·유지보수·모듈화·비용·Base 신선도에 적합한지 재판정한다.
- 완전한 작업 계약은 한 번 승인받고, 같은 범위의 구현·테스트·PR·적대적 검토·병합·postmerge는 routine approval로 멈추지 않는다. 핵심 방향 변경, 파괴적 migration, 비용·보안 권한 확대만 새 사용자 결정을 요구한다. `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`가 성립하면 현재 계약이 직접 만든 current-task PR의 ready merge와 postmerge readback도 이 연속 실행에 포함한다.
- 적대적 검토는 `전체 범위 공격 → finding 검증 → 개선·보완 → 실제 검증·회귀 → 개선된 전체 상태 재공격`의 **완전한 개선 루프를 최소 5회** 수행한다. 다섯 공격면으로 쪼개서 한 번씩 보는 것은 이 계약을 충족하지 않는다.
- 완료는 승인된 acceptance criteria의 `REQUIRED_WORK_REMAINING: 0`으로 판정한다. 외부 차단과 선택 backlog는 별도 축으로 남긴다.
- 게임 작업은 core loop·핵심 시스템·세계관/핵심 스토리라인 정합성·가역적 dummy `BALANCE_BUDGET`·playable build/test·재사용 가능한 모듈 경계를 함께 설계한다.
- 새 프로젝트와 새 시각 작업의 기본 협업면은 단일 Notion workspace의 프로젝트별 filtered page다. `Project` relation으로 작업·자산·화면·Reference·Benchmark를 분리하며, balance/economy/schema/runtime config와 실제 구현은 repo-native structured source를 사용한다. 기존 Google Sheets는 검증된 migration이 끝날 때까지 compatibility-only migration source로 보존한다. 상세 compatibility/migration owner는 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`다.
- 사용자에게 PowerShell 실행이 필요하면 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`를 적용한다. 매 작업을 새 PowerShell 창 기준으로 보고 위치 세팅을 첫 실행 단계에 두며, 가능한 절차는 한 번에 붙여넣는 단일 블록으로 제공한다.

## 3. Work Mode·Skill·사용자 결정

새 L1 이상 요청은 `managing-project-intake-and-work-contract`에서 한 번만 접수한다. 사용자는 Skill이나 Skill Mode를 고를 필요가 없다.

- 현재 단계에 주 Work Mode `PLAN / BUILD / REVIEW` 하나와 주 책임 분야 하나를 둔다.
- Registry의 `automatic-trigger-match`로 필요한 최소 Skill·Skill Mode만 선택한다. `load_by_default=false`는 자동 선택 금지가 아니라 비관련 기본 로드 금지다.
- 오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행 외에는 저장소 사실을 조사하고 범위·제외·보호 대상·완료 기준·검증·롤백을 확정한다.
- 모든 L1 이상 지시문 작성은 intake Skill의 `first-prompt → contract → clarify` 순서를 사용한다.
- 좋은 프롬프트 변환에서는 핵심 행동·결과·지배 기준을 방향 문장으로 압축해 지시문 가장 앞에 두고, Task·Context·Source·Constraints·Output·Validation 및 뒤쪽 제약과 충돌하지 않는지 검사한다. 앞 순서는 상위 권한을 만들지 않는다.
- 지시문 작성 뒤 실행 전 `Grill Me alignment gate`로 사용자 의도와 기획 정합성을 확인한다. 중대한 모호성이 있으면 질문 하나씩 닫고, 완전한 계약은 한 번 승인받으며, 동일한 계약의 유효한 승인 근거가 있으면 중복 질문 없이 재사용한다.
- `Grill Me alignment gate` 또는 유효한 기존 승인 근거가 없으면 `AWAITING_USER_CONFIRMATION`을 유지하고 구현·Codex 인계·외부 AI 위임·제품 변경으로 진행하지 않는다.
- 프로젝트 코어, 플레이어 경험, 주요 UX, 콘텐츠 의미, 비용·범위를 바꾸는 충돌만 사용자 결정으로 올린다. 저장소·정본·테스트로 판단 가능한 오류나 누락을 사용자에게 전가하지 않는다.
- 사용자 확인 전 실행 계약을 확정하거나 구현하지 않는다. 사용자가 승인한 범위에서는 단계별 구현·검증·적대적 재검토를 끝까지 수행한다.
- 사용자가 `[연속작업] 진행해`라고 명시하거나, 이미 승인된 동일 작업 계약에 대해 `진행해`, `계속해`, `남은 작업 진행`처럼 계속 실행 의도를 명확히 표현하면 `APPROVED_CONTRACT_CONTINUATION`으로 `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`를 적용한다. 이를 `CONTINUATION_INTENT_ALIASES`라 하며 승인되지 않은 범위나 새 범위를 자동 승인하는 마법 문구가 아니다. `작업 → 적대적 검토 → 범위 안의 기술적 권장안 자동 승인 → 최소 반영·회귀 검증 → blocker recovery → 다음 ready task`를 반복한다. 현재 계약이 직접 생성한 단 하나의 current-task PR은 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE` 조건을 만족할 때 latest-main reconciliation → exact HEAD `required checks` → merge → `postmerge readback`까지 이어서 수행하며 같은 PR 번호를 다시 묻지 않는다. `BLOCKED_UNVERIFIED`·현재 세션 도구 부재·일시적 증거 전송 실패는 그 자체로 전역 종료가 아니며, **recover first → defer locally → continue independent work → stop globally last** 순서로 처리한다. 진짜 `USER_DECISION_REQUIRED`, 고위험 외부 행위, 범위 확대는 자동 승인하지 않되 독립 작업이 남아 있으면 해당 task만 보류한다. 승인된 계약도 계속 실행 의도도 없으면 기존 승인 흐름을 유지한다.
- 상세 라우팅·권한 전환·리뷰·GPT→Codex·병합 절차는 `docs/WORK_MODE_AND_SKILL_ROUTING.md`를 따른다.

금지:

- 사용자에게 Skill·Skill Mode 선택 전가
- 전체 Skill 자동 로드, trigger 없는 호출, 주 책임 분야 Skill 중복
- Skill 파일을 읽은 사실을 실제 Skill 실행으로 보고
- L1 이상 지시문을 intake·좋은 프롬프트 변환·Grill Me 확인 없이 바로 실행
- 방향 문장의 앞 배치를 이유로 사용자 지시·정본·`HARD_CONSTRAINT`를 무시
- 사용자 확인 전 범위 확대·대량 병렬화
- 승인된 동일 계약이나 명확한 계속 실행 의도 없이 일반 요청을 연속작업 자동 승인으로 처리
- 연속작업을 이유로 사용자 전용 결정·미검증·고위험 외부 행위 Gate를 우회
- 같은 파일·Schema·자산의 소유 경계 없이 병렬 작업
- 검증·발행·Handoff 조기 실행
- `[백업]`, `[보류]`, `[제거 후보]` Skill 호출
- 근거 없는 일정·수치 발명

## 4. 책임 원본·프로젝트·발행 경계

- 한 질문에는 Registry에 등록된 Markdown 또는 JSON 책임 원본 하나만 둔다. DOCX·PDF·대시보드·과거 대화는 독립 정본이 아니다.
- 프로젝트를 넘어 재사용되는 작업 규칙, 검증 절차, PR·정본·workspace 동기화 원칙, 공용 플랫폼·자산·권리 기준은 Base 책임 원본에만 둔다. 프로젝트 저장소에서 같은 규칙을 재서술하거나 별도 공통 정책으로 승격하지 않는다.
- 프로젝트 저장소에는 채택한 Base 책임 원본의 경로·버전, 프로젝트 고유의 엔진·보안·데이터·제품 제약, 프로젝트별 Decision·구현·테스트·실행 증거·미검증만 기록한다. 과거 프로젝트 내부 공통 정책은 활성 권위를 제거하고 Base 대체 경로만 남긴다.
- 프로젝트 고유 제약이 Base보다 엄격할 수는 있지만, 공통 절차를 복제해 독립 권위로 만들 수 없다. 충돌 시 사용자 최신 지시와 프로젝트 고유 제약을 보존하면서 공통 규칙은 Base에서만 수정한다.
- 신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 `[기획서]/` 아래에 둔다. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 상세 책임 원본, 상태 축, 발행 정책, 완료 조건은 `docs/OPERATING_MODEL.md`를 따른다.
- 새 프로젝트·새 시각 기획의 기본 협업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`다. 하나의 Notion workspace 안에서 프로젝트별 페이지를 충분히 분리하고, Work/Asset/Screen/Reference/Benchmark는 `PROJECT_RELATION_REQUIRED`로 필터한다. 비주얼 맵은 파생 표현이며, 규칙·Decision과 실제 구현 상태는 GitHub/repository 정본과 런타임 증거가 소유한다.
- `USER_FACING_GDD_WORKSPACE`는 현재 `NOTION_DEFAULT_PROJECT_WORKSPACE`의 compatibility alias다. 과거 소비자가 이 이름을 사용해도 사람용 Project Home으로 라우팅하되 별도 Sheet·HTML·Figma 권한을 만들지 않는다.
- 기존 구성된 프로젝트 Google Sheet는 검증된 migration이 끝날 때까지 `COMPATIBILITY_ONLY` migration source로 취급한다. 상세 정본은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`다. Sheet-only 고유 내용과 proposal을 Notion/repository source에 reconcile하고 readback을 확인하기 전에는 삭제·폐기·migration 완료를 주장하지 않는다. Base 자체는 프로젝트 Sheet 동기화 대상이 아니다.
- `PROPOSED_SHEET_CHANGE`는 compatibility-only Sheet에서 발견된 미확정 변경 제안 상태다. 이를 승인 Decision이나 현행 정본으로 승격하지 않고 Notion/repository 책임 원본과 대조·승인·readback한다.
- 일반 기획·상태 확인은 프로젝트 Notion page와 GitHub/repository 정본을 함께 사용하고, 구조화 runtime data는 repo-native source를 사용한다. 기존 Sheet는 migration/proposal 확인이 필요한 경우에만 읽는다. HTML 대시보드·외부 HTML 도구 카탈로그는 사용자 명시 요청 또는 발견/유지보수 surface이며 독립 정본·실행 증거가 아니다.
- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들거나 제거·교체하지 않는다. UI 설계·폴리싱·구현 결과 감사는 `auditing-and-refining-ui-art`로 라우팅하고, 사용자 승인 finding만 실제 렌더로 재검수한다.
- 접근성·성능·플레이테스트·벤치마크 결과는 실제 적용된 경우만 보고하며 법적 인증이나 제품 구현 사실로 과장하지 않는다.

## 4.1 플랫폼 심사·자산 권리 불변 규칙

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다.

- 기본 플랫폼 검토는 Steam·STOVE·Google Play다.
- 등급 전략은 프로젝트 핵심 경험을 보존하는 `LOWEST_VIABLE_RATING`이며 청소년이용불가·18+를 기본 회피한다. 전체이용가를 모든 프로젝트에 강제하지 않는다.
- `content_rating_target`과 `target_audience`를 분리하고 설문·build·store·trailer·screenshot·AI·UGC·ads 일치를 확인한다.
- 이미지·사운드·폰트·3D·애니메이션·플러그인·오픈소스·AI·외주·성우·작곡·번역 자료는 직접 포함과 `REFERENCE_TO_ORIGINAL`을 분리한다.
- 참조 자료는 구조·기능·일반 제작 원리만 추출한 `reference_brief`로 새 자산을 만들며, 원본·고유 표현을 그대로 또는 약간 변형해 사용하지 않는다.
- 필수 상업 사용·게임 포함 배포·출처·약관·계약·유사성·등급 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.
- 공개 저장소에 unredacted 계약서, 신분증, 서명, 주소, 결제·세금·개인정보를 넣지 않는다. 최소 metadata·hash·검토 결과와 `secure_original_location`만 둔다.
- Template·정적 검사 통과는 법률 검토, 등급 확정, 플랫폼 제출·승인 증거가 아니다.

## 5. 기존 자료와 Base 변경 안전

- 기존 프로젝트 감사·정리는 `managing-game-project-operating-system`의 현재 mode를 사용한다.
- 사용자 승인 전 파일·폴더 대량 삭제·이동·통합, 구형 이름만 근거로 한 삭제, 기존 책임 문서 대규모 축약, 승인 자산 제거, 프로젝트 용어·수치·결정 변경, `[보류]` 폐기, Base 구조에 맞춘 강제 개명을 하지 않는다.
- 고유 정보·활성 참조·파생본·복구·사용자 승인이 확인되지 않은 항목은 보존한다. Legacy·archive의 상세 판정은 운영 모델과 `governing-legacy-retention-and-archives`가 책임진다.
- 프로젝트 교훈의 Base 승격은 `managing-base-change-proposals`를 사용한다. `[수정제안서]` 제출·검토와 사용자 승인 뒤 별도 구현 PR에서 반영하며, 신규 제안 PR과 활성 Base 구현 PR을 섞지 않는다. 사용자가 직접 승인한 Base 변경 요청은 별도 제안서 없이 작업 계약이 될 수 있다.
- 새 Skill보다 기존 통합 Skill의 mode·reference 확장을 먼저 검토한다. 독립 입력·산출물·권한·검증 경계가 있을 때만 새 Skill을 만든다.
- 실패·중요 결정·재사용 가능한 교훈·실제 검증을 Learning Log에 기록하되 한 번의 성공을 공용 강제 규칙으로 승격하지 않는다.

## 6. 검증·GitHub·보호 표면

- 일반 변경은 `reviewing-and-validating-project-changes`, 실패 가정 공격은 `running-adversarial-review-and-refinement`, 정본·경로·ID·Schema 전파는 필요할 때 `auditing-canonical-reference-freshness`로 검증한다.
- 계약·diff 대조, 포맷·정적 검사, 관련 테스트, 가능한 런타임·렌더·빌드, 정상·실패·경계·회귀, 미검증·위험·롤백을 분리한다.
- 전체 로컬 계약은 `python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>`로 실행한다. 인자는 검증 전에 확인한 정확한 40자 main SHA이며, 이동 가능한 ref 이름을 넘기지 않는다. 환경 미준비 skip을 pass로 바꾸지 않는다.
- 작업 전 원격·로컬 상태를 확인하고, 검증된 변경만 commit·push한다. Workflow 파일 존재와 실제 Actions 실행·Required Check 강제를 구분한다.
- GitHub 게시·검토는 연결된 GitHub plugin/connector capability를 먼저 사용한다. connector가 필요한 동작을 지원하면 missing `gh` alone is not a blocker이며 사용자에게 CLI 반복 설치·재인증을 요구하지 않는다. 상세 fallback과 exact-SHA 안전 규칙은 `synchronizing-local-and-github-state`가 소유한다.
- **`OPEN_PR_READ_ONLY_BY_DEFAULT` / `FOLLOW_UP_TARGET_IS_MERGED_MAIN`: 모든 `open/draft/ready` PR·Branch는 기본 read-only다. 현황·충돌·중복 확인을 위해 읽을 수 있지만 checkout/write/rebase/close/merge/selective-copy/material-delta 흡수를 하지 않는다. 후속 수정은 exact latest completed `main`에서 새 작업 Branch로 시작하며, main에 실제 유지된 의미만 대상으로 한다. `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`를 만족하는 현재 작업 own PR만 그 승인 계약의 merge-ready 실행 범위에서 예외다.**
- **`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`: 열린 PR 변경은 사용자가 현재 작업에서 PR 번호와 허용 동작을 지정하는 것이 기본이다. 같은 Goal, owner evidence 부재, `CURRENT_COORDINATOR_CHAT`, `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`은 이 권한을 대신하지 않는다. 단, 현재 승인 계약이 직접 생성한 단일 current-task PR에 `APPROVED_CONTRACT_CONTINUATION`과 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`가 함께 성립하면 PR 번호 재지정 없이 그 own PR의 latest-main reconciliation·exact HEAD 재검증·ready merge·postmerge readback을 수행할 수 있다. 명시 승인이 있거나 이 좁은 예외가 성립하더라도 exact head·범위·rollback을 다시 확인하고 허용된 동작만 수행한다.**
- **`CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`는 `pre-existing`, `unrelated`, `other-workstream`, `draft` PR이나 복수 후보의 takeover 권한이 아니다. 다른 PR의 변경·흡수·close·supersede에는 여전히 `OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`이 적용된다. `force push`, direct main push, `--admin`, `ruleset bypass`는 금지하며, `병합하지 마`·`PR만 열어`·`검토만` 같은 최신 제한 지시는 언제나 이 예외보다 우선한다.**
- 병합은 검토한 정확한 HEAD, 필수 검사, 독립 검토, unresolved thread 0, 결정 게이트를 다시 확인한 뒤 저장소가 허용한 방식으로 수행한다.
- `skills/SKILL_REGISTRY.json`, released lock, frozen/generated release artifact, 보호 경로를 변경하려면 해당 전용 계약과 검증을 먼저 충족한다. 범위 밖에서는 bytes를 보존한다.
- 생성 실패·미검증 바이너리·로컬 임시 산출물을 자동 push하지 않는다.

## 7. 완료 보고

### 사용자 학습형 완료보고

Base와 Base를 채택한 프로젝트의 L1 이상 완료보고는 단순히 `작업 완료 / 테스트 통과`로 끝내지 않는다. 사용자가 작업 구조를 학습하고 다음 결정을 더 정확히 내릴 수 있도록 다음을 사람용으로 먼저 설명한다.

- 이 작업/파트가 전체 Base 또는 프로젝트에서 담당하는 역할
- 가장 중요한 상위 규칙과 실제 작동 시점
- 사용한 핵심 Skill·Skill Mode와 서로의 책임 차이
- 핵심 모듈과 `입력 → 판단/처리 → 출력 → 소비자/검증` 연결
- 유지한 것 / 개선한 것 / 흡수·통합한 것 / 제거·폐기한 것 / 의도적으로 추가하지 않은 것
- 변경 전 → 변경 후 → 사용자/플레이어 관점 기대효과 → trade-off
- 장기계획 적합성 및 재검토 조건
- 실행·검증 증거, 미검증, 남은 위험

파일명·테스트명만 나열하지 말고 **왜 존재하고 무엇과 연결되며 없어지면 무엇이 깨지는지**까지 설명한다. 프로젝트 고유 내용은 프로젝트 전용으로, 반복 가능한 공용 교훈은 Base 승격 후보로 분리한다.


L1 이상 완료 보고에는 다음을 실제 수행 증거와 함께 포함한다.

- 사용한 Work Mode·Skill·Skill Mode와 선택 이유
- 주 책임·영향 분야, 승인 범위·제외·보호 대상
- 변경한 문서·코드·데이터·자산·Skill과 유지한 기존 결정
- 실행 단계·의존성·게이트와 실제 결과
- 테스트·런타임·렌더·접근성·성능·참조 최신성·정확한 HEAD 증거
- 실행하지 않은 항목, 불일치, 남은 위험, 롤백, 다음 작업
- 보존·통합·보류·제거 후보, Base 환류 여부

실행하지 않은 Skill, 조사, 테스트, 렌더, 구현, 접근성·성능 검증, 브랜치 보호를 완료로 보고하지 않는다.
