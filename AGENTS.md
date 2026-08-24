# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** Skill·Template·Case·Test의 원본이다. 이 파일은 repository-wide **항상 적용되는 불변 규칙**(`ALWAYS_ON_CONTEXT_ONLY`)만 유지한다. 상세 절차·표·예시는 해당 책임 원본을 작업 필요 시 읽는 **`PROGRESSIVE_LOAD_DETAILED_CONTRACTS`** 방식으로 적용한다. root `AGENTS.md`에 세부 playbook을 다시 복제하지 않는다.

## 1. 권한·증거·읽기 경계

우선순위는 **사용자의 최신 지시** → 대상 프로젝트 `AGENTS.md`와 프로젝트 고유 보안·엔진·데이터 규칙 → Active Context와 승인된 작업 계약 → 등록된 책임 원본과 실제 코드·데이터·자산·테스트 → 채택된 Base 계약 → Base 원격 원본 → 외부 사례·과거 대화·초안·추정 순이다.

- 정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다. 외부 벤치마크·리뷰·커뮤니티·모델 해석은 요구사항이나 실제 구현의 정본이 아니다.
- **사용자가 작업 근거로 직접 제공한 외부 링크**를 현재 도구로 읽지 못하고 그 내용이 필수라면 **즉시 `BLOCKED_UNVERIFIED`로 작업을 중단**하고 **원문 텍스트·파일·스크린샷**처럼 현재 세션에서 검증 가능한 형태를 요청한다. **링크 제목·검색 스니펫·과거 기억·주변 자료·추정**으로 대체하지 않으며, 사용자가 해제하기 전에는 **다른 독립 작업으로 임의 전환하지 않는다**.
- 저장소·실행 증거 없이 설치·마이그레이션·검수 완료를 주장하지 않는다. **실행하지 않은** 조사·Skill·테스트·렌더·빌드·접근성·성능 검증은 완료 증거가 아니다.
- 모든 파일과 전체 `skills/`를 기본 로드하지 않는다. `skills/SKILL_REGISTRY.json` trigger로 필요한 최소 Skill을 고르고 현행 목록은 `docs/generated/BASE_ACTIVE_SKILLS.md`에서 확인한다.
- 보호 경로, 권한, 생성물, released lock, frozen artifact는 전용 계약 없이 수정하지 않는다.

### 상세 owner — 필요할 때만 읽기

- 전체 생명주기·상태·발행·완료: `docs/OPERATING_MODEL.md`
- Work Mode·Skill·검토·병합: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- 기획 우선 원칙·Grill Me: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- 장기 작업·완료·비용·PR 안전: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- 연속작업 실행: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- UI/UX 설계·폴리싱·실행 결과 감사: `auditing-and-refining-ui-art`
- 문서 위치: `docs/DOCUMENTATION_MAP.md`
- CI 비용/실행 계층: `docs/CI_EXECUTION_COST_POLICY.md`
- Notion/Sheet migration: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`
- 플랫폼 심사·자산 권리·reference production: `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- Godot 단일 저작 권위: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- PowerShell fresh shell: `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`
- Base 변경 제안: `managing-base-change-proposals`

## 2. L1+ 작업 진입·판단 불변식

- L1 이상은 **최신 main**, 현재 결정, 분야 정본, 같은 Goal의 열린·최근 병합 PR, **실제 구현**을 먼저 비교한다. 저장소 사실로 판단 가능한 오류·누락을 사용자에게 되묻지 않는다.
- `DEEP_WORK_PREANSWER_GATE` / `REQUIRED_EVIDENCE_BEFORE_FINAL`: 요청된 조사·벤치마킹·검토·구현·검증은 실제 수행 뒤 substantive final을 낸다. `NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION`: 필수 항목이 `NOT_RUN`이면 완료가 아니라 `BLOCKED_UNVERIFIED`다.
- `INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION`: 중간보고 축소는 작업 축소가 아니다. `REASONING_EFFORT_IS_NOT_WORK_EVIDENCE`: 추론 강도는 evidence가 아니다. `REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF`: 현재 세션 도구로 필요한 필수 증거를 얻을 수 있으면 실제 Tool 실행을 optional executor handoff로 대체하거나 생략하지 않는다.
- `GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY`: GPT primary는 판단·조정 책임을 뜻하며 텍스트 작성만으로 조사·실행·검증 책임을 충족한 것으로 보지 않는다.
- **`CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`**: 중요한 결정은 먼저 **현행 조사**를 하고, **최소 3개**의 materially distinct 유효 대안을 같은 기준으로 비교한다. `MINIMUM_VIABLE_ALTERNATIVES: 3`. 허수 대안으로 수를 채우지 않는다.
- **`BETTER_ALTERNATIVE_SEARCH`**: 새 증거·실패·finding이 나오면 **더 나은 방안**을 다시 찾는다. 핵심 방향·플레이어 경험·비용·범위를 바꾸면 `USER_DECISION_REQUIRED`다.
- **`LONG_TERM_PLAN_FIT_REQUIRED`**: 권장안은 사용자/플레이어 가치, 정확성, 위험, 수명주기 비용, 유지보수성, 재사용·모듈성, 증거 강도, **되돌리기 난이도**, **장기계획** 적합성과 재검토 조건까지 비교한다.
- **`BEST_LONG_TERM_EFFICIENT_METHOD` / `QUALITY_OVER_RESPONSE_SPEED` / `BENCHMARK_PRACTICE_COMPARISON`**: 가장 빠른 답보다 장기 총비용과 결과 품질을 우선하고 공식/1차 자료·현업 성공/실패 사례를 `ADOPT / ADAPT / REJECT`로 판정한다.
- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`**: `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`. 매 회 전체 결과 상태를 다시 읽고 공격·검증·수정·회귀검사를 반복한다. 최소 5회 뒤 새 유효 blocking finding 0과 acceptance 충족일 때만 `CLEAN_REVIEW_EXIT`다. **사용자 주장과 AI의 최초 제안** 모두 **동일한 평가 기준**으로 검토하며 **근거 없는 동의**와 **반대를 위한 반대**를 모두 금지한다.
- `REQUIRED_WORK_REMAINING`, `REMAINING_WORK_COMPLETION_GATE`, `IMPLEMENTATION_CORRECTION_RESCAN`, `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`를 거쳐 남은 필수 작업·퇴행·누락을 다시 계산한다.

## 3. 기획·승인·연속작업

- 새 L1 이상 요청은 `managing-project-intake-and-work-contract`에서 한 번 접수한다. 사용자에게 Skill·Skill Mode 선택을 전가하지 않는다.
- **모든 L1 이상 지시문 작성**은 intake의 first-prompt → contract → clarify 순서를 사용하고 **좋은 프롬프트 변환**으로 Task·Context·Source·Constraints·Output·Validation 충돌을 검사한다.
- **실행 전** `Grill Me alignment gate`로 사용자 의도와 기획 정합성을 확인한다. 유효한 기존 승인 근거를 재사용하고, 필요한 승인 없이 구현으로 넘어가면 `AWAITING_USER_CONFIRMATION`이다.
- 프로젝트 코어·플레이어 경험·주요 UX·비용·범위를 바꾸는 충돌만 사용자 결정으로 올린다. 승인 범위 안의 기계적·기술적 선택은 정본과 테스트로 해결한다.
- `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행`, `끝까지 진행`처럼 이미 승인된 동일 계약의 continuation intent가 명확하면 `APPROVED_CONTRACT_CONTINUATION`으로 위 연속작업 owner를 적용한다. 새 범위를 자동 승인하지 않는다.
- `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`: 승인 계약이 **latest completed `main`**에서 직접 만든 단 하나의 명확한 **current-task PR**이라면 latest-main reconciliation → **exact HEAD** 재검증 → repository `required checks`·review·unresolved thread·ruleset → 안전한 merge → `postmerge readback`까지 같은 계약으로 진행할 수 있다.
- 이 예외는 `pre-existing`, `unrelated`, `other-workstream`, `draft` PR이나 복수 후보 takeover 권한이 아니다. `force push`, direct main push, `--admin`, `ruleset bypass`는 금지한다. 사용자가 `병합하지 마`, `PR만 열어`, `검토만`으로 제한하면 최신 지시가 우선한다.
- recoverable blocker는 recover first → defer locally → independent work continuation → global stop last 순서를 사용하되 진짜 `USER_DECISION_REQUIRED`, 범위 확대, 고위험 외부 행위는 자동 승인하지 않는다.

## 4. GitHub·동시성·보호 표면

- **`OPEN_PR_READ_ONLY_BY_DEFAULT` / `FOLLOW_UP_TARGET_IS_MERGED_MAIN`**: 모든 open/draft/ready PR·Branch는 기본 read-only다. 현황·중복·충돌은 읽되 다른 작업 PR을 checkout/write/rebase/close/merge/흡수하지 않는다. 후속 수정은 최신 completed main에서 시작한다.
- **`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`**: current-task continuation의 좁은 예외가 아니면 열린 PR 변경은 사용자가 PR 번호와 허용 동작을 명시해야 한다.
- 현재 작업도 병합 전 검토한 **정확한 HEAD**, 필수 검사, 독립 검토, unresolved thread 0, 결정 Gate를 다시 확인한다.
- 같은 파일·Schema·자산을 **소유 경계 없이 병렬** 수정하지 않는다. 동시 변경 증거가 있으면 stale 가정을 버리고 latest main을 다시 읽는다.
- GitHub 게시·검토는 연결된 **GitHub plugin/connector** capability를 우선 사용한다. connector가 필요한 동작을 지원하면 **missing `gh` alone is not a blocker**다.
- 보호 경로 밖에서 `skills/SKILL_REGISTRY.json`, `[수정제안서]`, released lock/frozen/generated release artifact bytes를 건드리지 않는다.

## 5. 비용·workspace·프로젝트 정본

- **`ZERO_INCREMENTAL_COST_REQUIRED`**: 기본 경로는 추가 금전 지출 0이다. 포함된 구독 기능도 별도 **separately metered** API·credit·runner·storage·SaaS 과금으로 바뀌지 않는 범위에서만 사용한다. **pay-as-you-go**나 신규 유료 서비스는 승인 전 실행하지 않으며 불명확하면 `COST_GATE_BLOCKED`다.
- `CURRENT_PAID_PLANS: GPT_PRO`, `PAID_PLAN_COUNT: 1`. 현재 기본 유료 플랜은 **GPT Pro** 하나다. **Notion**은 별도 유료 기능 없이 현재 범위에서 사용하고 다른 유료 기능은 **새 사용자 승인**이 필요하다.
- 새 프로젝트·새 시각 기획의 사람용 기본 협업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`; 프로젝트별 Work/Asset/Screen/Reference/Benchmark는 `PROJECT_RELATION_REQUIRED`로 분리한다. runtime·구현 사실은 repository source와 실제 실행 증거가 소유한다.
- `USER_FACING_GDD_WORKSPACE`는 현재 Notion 사람용 Project Home으로 라우팅하는 compatibility alias다. 기존 Google Sheets는 `COMPATIBILITY_ONLY` migration source이며 `PROPOSED_SHEET_CHANGE`를 승인 Decision으로 자동 승격하지 않는다.
- Base 자체는 프로젝트 Sheet 동기화 대상이 아니다. HTML/Figma/Sheet를 독립 정본으로 복원하지 않는다.
- 기존 승인 이미지·자산은 별도 승인 없이 새 시안으로 제거·교체하지 않는다.

## 6. Existing Solution First·Godot·외부 도구

- **Existing Solution First Gate**: 신규 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층은 기존 대안을 조사하고 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW`를 판정한 뒤 선택한다.
- Godot 저작·편집 자동화 정본은 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`; 직접 제작 판단은 `evaluating-godot-assets-and-plugins-before-creation`이 소유한다.
- **검증·승인된 애드온**이 실제 문제를 해결하면 **직접 중복 구현보다 활용을 우선**한다. 그러나 **모든 프로젝트에 일괄 설치하지 않는다**. 설치됐지만 실제 소비 경로가 없으면 `INSTALLED_UNUSED`로 구분한다.
- 신규 제작은 기존 대안의 핵심 기능·보안·라이선스·유지·Godot/OS 적합성 결함을 설정·격리·bounded patch로 해결할 수 없다는 증거가 필요하다.

## 7. 플랫폼·자산·보안 상한

상세 플랫폼·등급·라이선스·reference-production 절차는 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`를 필요 시 읽는다. root에는 release safety만 유지한다.

- 상업 사용·게임 포함 배포·출처·약관·계약·유사성·등급 증거가 부족하면 `RELEASE_BLOCKED_UNVERIFIED`다.
- 공개 저장소에 **unredacted** 계약서·신분증·서명·주소·결제·세금·개인정보를 넣지 않는다. 최소 metadata·hash·검토 결과와 `secure_original_location`만 공개 가능한 형태로 남긴다.
- Template·정적 검사 통과는 법률 검토, 등급 확정, 플랫폼 제출·승인 증거가 아니다.

## 8. Base 변경·보존

- 사용자 승인 전 대량 삭제·이동·통합, 구형 이름만 근거로 한 삭제, 승인 자산 제거, 프로젝트 용어·수치·결정 변경, `[보류]` 폐기, 강제 개명을 하지 않는다.
- Legacy/archive 상세 판정은 `governing-legacy-retention-and-archives`; 프로젝트 교훈의 Base 승격은 `managing-base-change-proposals`가 소유한다.
- `[수정제안서]`는 승인 뒤 **별도 구현 PR**에서 반영한다. 다만 사용자가 **직접 승인한 Base 변경 요청**은 **별도 제안서 없이 작업 계약**이 될 수 있다.
- 새 Skill보다 기존 통합 Skill의 mode/reference 확장을 먼저 검토한다. 독립 입력·산출물·권한·검증 경계가 있을 때만 새 Skill을 만든다.
- 실패·중요 결정·재사용 가능한 교훈은 Learning Log에 기록하되 한 번의 성공을 공용 강제 규칙으로 승격하지 않는다.

## 9. 검증·완료 보고

- 일반 변경은 `reviewing-and-validating-project-changes`, 실패 가정 공격은 `running-adversarial-review-and-refinement`, 정본·경로·ID·Schema 전파는 필요 시 `auditing-canonical-reference-freshness`로 검증한다.
- 전체 로컬 계약은 `python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>`로 실행하며 이동 ref가 아니라 검증한 40자 main SHA를 사용한다. 환경 미준비 skip을 pass로 바꾸지 않는다.
- 사용자에게 PowerShell 실행이 필요하면 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`를 적용한다.
- `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`, `POSTMERGE_CORRECTION_REQUIRED`, `PROGRESS_READBACK_REQUIRED`로 merge 후 GitHub/Notion/readback과 남은 작업을 다시 확인한다.

### 사용자 학습형 완료보고

L1 이상 완료보고는 역할 → 핵심 규칙/작동 시점 → 사용한 Work Mode·Skill·Skill Mode → 입력/판단/출력/검증 연결 → 작업 전/후/기대효과/trade-off → 장기 적합성 → 실제 검증 증거 → 미검증·남은 위험·롤백 순으로 사람에게 이해되게 설명한다. 파일명·테스트명만 나열하지 않는다.

완료보고에는 승인 범위·제외·보호 대상, 변경/유지/통합/보류/제거 후보, 테스트·런타임·렌더·정확한 HEAD 증거, `REMAINING_WORK_COMPLETION_GATE`, `IMPLEMENTATION_CORRECTION_RESCAN`, `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`, `CLEAN_REVIEW_EXIT`, 남은 작업과 Base 환류 여부를 포함한다.
