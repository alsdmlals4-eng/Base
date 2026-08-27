# Skill 오케스트레이션·실행 프로필·완전성 증거

이 reference는 장기 기획·버티컬 슬라이스·검수·발행 작업에서 Skill 누락이나 과잉 호출 위험이 있을 때만 읽는다.

## 1. 원칙

Grill Me와 적대적 검토는 전체 파이프라인의 일부다. 최고의 결과를 위해 필요한 것은 많은 Skill 이름을 나열하는 것이 아니라 **각 단계에 필요한 독립 책임을 빠짐없이 실행하고 증거를 남기는 것**이다.

```text
요청 접수·계약
→ 저장소·컨텍스트 조사
→ 콘셉트·코어·사용자 연구
→ 책임 원본 작성
→ 데모 핵심 위험 등록·필요 시 내부 TECHNICAL_SPIKE
→ DEMO_FIRST_VERTICAL_SLICE 계약·품질·파이프라인
→ 구현 계획·TDD·디버깅
→ 에셋·UI·사운드 검토
→ 외부 플레이 검증
→ 적대적 검토·통합 검증
→ 정본·GitHub·발행 동기화
→ Gate 판정·Learning Log·Base 환류
```

금지:

- 전체 `skills/` 기본 로드
- Trigger와 무관한 Skill 호출
- 여러 Skill이 같은 단계·범위·상태를 중복 판정
- Skill 문서만 읽고 실행했다고 보고
- 검증·발행·Handoff 조기 실행
- 존재하지 않거나 비활성인 Skill 사용 주장

## 2. 실행 프로필

### `PLANNING_ONLY_PROFILE`

GPT가 총기획·조사·Grill Me·문서·검수를 수행한다.

허용:

- 프로젝트 코어·세일즈포인트·Core Loop
- 벤치마킹·SWOT·VRIO
- Demo-First Vertical Slice·데모 핵심 위험·내부 Spike 계약
- P0~P3
- Codex Plan·Issue·Goal 초안
- 기획 Branch·PR·필요한 PDF

금지:

- 실제 Godot 구현
- Codex Build 실행
- 구현 완료 선언

### `DEMO_FIRST_FULL_PROFILE`

과거 `VERTICAL_SLICE_FULL_PROFILE`은 호환 이름이며 새 작업에서는 `DEMO_FIRST_FULL_PROFILE`로 해석한다.

```text
GPT PLAN
→ 사용자 승인
→ Codex PLAN 재검수
→ Codex BUILD
→ GPT REVIEW
→ 기술 검수안과 기획 충돌 분리
→ 승인 수정
→ 통합 QA·내부 플레이테스트
→ 외부 플레이테스트·반응 조사
→ DEMO_VALIDATION
→ Gate 판정
```

### `REVIEW_ONLY_PROFILE`

읽기 전용 영향 범위 지도와 Finding을 먼저 만든다. 승인된 최소 수정만 `BUILD`로 전환한 뒤 다시 `REVIEW`한다.

### `PUBLICATION_PROFILE`

책임 원본의 발행 정책이 실제로 요구할 때만 PDF·DOCX·대시보드·PR을 생성한다. 파생본은 정본을 대체하지 않는다.

### `HIGODOT_IMPLEMENTATION_PROFILE`

HiGodot이 실제로 연결되어 있고 도구 목록·버전·프로젝트 경로를 확인한 경우에만 사용한다. Scene·Node·Resource·Signal 변경을 실제 파일 diff·에디터 로그·런타임으로 검증한다.

## 3. 단계별 Base Skill 체인

### A. 접수·컨텍스트

- `managing-project-intake-and-work-contract`
- 필요 시 `managing-game-project-operating-system`
- `maintaining-project-context-and-handoff`
- 필요 시 `synchronizing-local-and-github-state`
- 필요 시 `maintaining-long-running-task-continuity`

### B. 콘셉트·코어·시장

- `analyzing-and-refining-game-concepts`
- `identifying-project-core`
- `establishing-project-core`
- 필요 시 `governing-game-user-research-coverage`
- 창작 설계 전 Superpowers `brainstorming`

### C. 문서·정본·학습

- `managing-design-documents`
- `evolving-project-discipline-skills`
- `auditing-canonical-reference-freshness`
- `managing-base-change-proposals`
- `skills/SKILL_LEARNING_LOG.md`

### D. 버티컬 슬라이스

- `designing-vertical-slices`
- `reviewing-and-validating-project-changes: accessibility-review`
- `reviewing-and-validating-project-changes: performance-profile`

### E. 에셋·아트·UI·사운드

- `evaluating-godot-assets-and-plugins-before-creation`
- `designing-art-prompts-and-technique-cards`
- `auditing-and-refining-ui-art`
- 접근성은 통합 검증 Skill의 전문 mode

### F. 구현·Superpowers

환경에 실제 설치된 경우 다음을 Trigger에 맞춰 사용한다.

```text
brainstorming
→ writing-plans
→ using-git-worktrees
→ test-driven-development
→ 필요한 경우 subagent-driven-development 또는 dispatching-parallel-agents
→ systematic-debugging
→ requesting-code-review
→ receiving-code-review
→ verification-before-completion
→ finishing-a-development-branch
```

Base Work Mode·프로젝트 규칙·승인 계약이 Superpowers보다 상위다.

### G. 검수·런타임

- `running-adversarial-review-and-refinement`
- `reviewing-and-validating-project-changes`
- `auditing-canonical-reference-freshness`
- 필요 시 `diagnosing-game-engine-runtime-failures`
- 외부 AI 결과는 `external-source-review`

### H. 발행·GitHub·사용자 전달

- `managing-design-documents`
- `maintaining-project-context-and-handoff`
- `managing-base-change-proposals`
- GitHub 생명주기 정책과 PR Template

## 4. Skill 실행 계획

| Skill | Mode | Trigger | 사용 이유 | 예상 산출물 | 검증 방법 |
|---|---|---|---|---|---|

작업 시작 보고에는 실제 사용할 Skill과 이유만 압축해서 표시한다. 관련 없는 Skill은 `ROUTED_NOT_NEEDED`로 남길 수 있지만 호출하지 않는다.

## 5. Skill 실행 증거

| Skill | Mode | 상태 | 실제 입력 | 실제 산출물 | 증거 경로·빌드·Commit | 누락·차단 |
|---|---|---|---|---|---|---|

상태:

- `EXECUTED_AND_EVIDENCED`
- `EXECUTED_UNVERIFIED`
- `ROUTED_NOT_NEEDED`
- `NOT_AVAILABLE`
- `BLOCKED`
- `FALLBACK_USED`

### 5.1 Godot 실행·증거·프로세스 생명주기 연결

이 문서는 실행 여부, fresh evidence, task-owned cleanup, 잔여 확인, 완료 주장을 한 경로로 묶는 `EXECUTION_EVIDENCE_CANONICAL_OWNER`다. Godot 안전 정책은 프로세스 조작 방법을 소유하지만 완료 증거를 별도로 소유하지 않는다.

```text
EXECUTABLE_COVERAGE_OR_EXPLICIT_ENV_GATE
→ WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL
→ FRESH_RUNTIME_ARTIFACT_GATE
→ TASK_OWNED_PROCESS_CLEANUP
→ RESIDUAL_PROCESS_READBACK
→ COMPLETION_CLAIM_AFTER_VERIFICATION_AND_CLEANUP
```

- 현재 환경에서 실행 가능하면 실제 실행하고 current run evidence를 남긴다.
- 정당한 필수 환경에서만 실행 가능하면 `ENV_GATED_EXPECTED_SKIP`으로 환경·버전·device·tool을 기록하며 현재 환경을 PASS로 승격하지 않는다.
- 어느 합법적 owned layer에서도 실행할 수 없으면 `UNRUNNABLE_COVERAGE_GAP`으로 남겨 driver를 만들거나 owner를 재배치하고, 영구 SKIP을 정상 coverage로 숨기지 않는다.
- runtime assertion과 프로세스 정리는 별도 판정이다. `CLEANUP_PASS_IS_NOT_RUNTIME_PASS`이며, runtime PASS도 cleanup/readback 누락을 덮지 못한다.
- 이번 작업이 시작한 exact process만 `TASK_OWNED_PROCESS_CLEANUP` 대상으로 삼는다. 소유권을 안전하게 증명할 수 없으면 broad kill 대신 `PROCESS_OWNERSHIP_UNVERIFIED`와 residual risk를 보고한다.
- `RESIDUAL_PROCESS_READBACK`은 child process, project lock, editor/game/test/server session 잔여와 pre-existing/unrelated instance 보존을 확인한다.
- 세부 실행·정리 안전 경계는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`, Work 라우팅은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`와 `docs/WORK_MODE_AND_SKILL_ROUTING.md`를 따른다.

### 5.2 `FRESH_RUNTIME_ARTIFACT_GATE`

현재 build·commit의 runtime/render 결과를 근거로 PASS를 주장할 때 **기존 artifact가 존재한다는 사실은 fresh evidence가 아니다.** `PRIOR_ARTIFACT_EXISTENCE_IS_NOT_FRESH_EVIDENCE`를 적용한다. Godot 전용 실행·provider 권위는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`, 일반 완료 주장은 `reviewing-and-validating-project-changes: claim-and-intent-verification`이 계속 소유하며 이 reference는 중복 provider나 새 Skill을 만들지 않는다.

```text
exact build/commit + run identity 고정
→ 이전 transient output을 삭제·격리하거나 unique run directory 사용
→ 현재 producer/runtime를 실제 실행
→ 이번 run이 expected artifact를 새로 생성했는지 확인
→ artifact path + bytes/hash + run/build identity를 evidence에 묶음
→ semantic/runtime assertion과 함께 판정
```

- baseline·golden artifact는 비교 기준이므로 transient output처럼 무조건 삭제하지 않는다. baseline identity를 pin하고 baseline 교체는 별도 review로 처리한다.
- screenshot·video·runtime report·trace처럼 producer가 다시 만들 수 있는 material artifact는 가능하면 기존 결과를 재사용하지 않고 현재 run에서 재생성한다.
- 동일 파일명을 재사용해야 하면 이전 파일을 먼저 격리하거나 제거하고, 새 파일의 생성 여부·크기 또는 digest를 확인한다.
- capture/runtime 환경이 필요한데 unavailable, timeout, render 불가, producer 실패, 새 artifact 미생성이면 `INCONCLUSIVE_NOT_PASS` 또는 기존 owner의 `BLOCKED_UNVERIFIED`로 남긴다. 작업자·Agent의 성공 설명은 이를 PASS로 덮지 못한다.
- artifact freshness는 품질 자체의 증거가 아니다. fresh screenshot도 디자인 품질·가독성·접근성·재미·human approval을 자동 증명하지 않는다.
- deterministic state가 구조화된 assertion으로 판정 가능하면 screenshot을 강제하지 않는다. 반대로 pixel/layout이 acceptance 대상이면 fresh visual artifact를 요구한다.

이 Gate의 목적은 과거 screenshot·log·report가 남아 있어 현재 run이 실패했는데도 완료로 오인하는 `STALE_ARTIFACT_FALSE_PASS`를 줄이는 것이다. 실제 프로젝트에 capture producer가 연결되지 않았다면 기능이 구현됐다고 추정하지 않고 해당 runtime/render evidence를 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 유지한다.

## 6. Gate별 Skill Coverage

### Gate 1

- Intake·Work Mode·계약
- 콘셉트·제약·뾰족한 재미
- 프로젝트 코어 판정·확정
- 벤치마킹·사용자 근거
- 기획 책임 원본
- Grill Me 차단 결정
- 데모 핵심 위험 등록부·필요 시 내부 `TECHNICAL_SPIKE` 계약

### Gate 2

- Slice 계약·Quality Bar·Pipeline proof
- 에셋·플러그인 선행 조사
- 구현 계획·TDD·디버깅
- 저장·UI·아트·사운드 통합
- 접근성·성능
- 외부 플레이 증거
- 통합 데모·상점·후원 준비
- 적대적 검토·회귀

### Gate 3

- 외부 증거 분석
- 제작 범위·비용·기간
- 텀블벅 또는 모바일 수익 모델 판단
- 기획 재조정 또는 본제작 승인
- Decision Ledger·Roadmap·Context 동기화

### Gate 4

- 출시 빌드·정적·런타임·회귀
- 저장·업데이트 호환
- 상점·등급·개인정보·라이선스
- 출시 Runbook·롤백·지원
- 파생본·GitHub·최종 증거

## 7. Grill Me 단계

Grill Me는 `managing-project-intake-and-work-contract: clarify`의 의사결정 프로토콜이다. 저장소·도구·기술 검수로 답할 수 있는 사실이나 개별 수치는 묻지 않는다.

- `GRILL_0_INITIAL_INTENT`: 초기 의도·목표·비타협 조건이 실제로 불명확할 때.
- `GRILL_1_CORE_REVIEW`: 코어·뾰족한 재미·주요 UX가 서로 충돌할 때.
- `GRILL_2_MARKET_AND_PRODUCTION`: 타깃·플랫폼·수익 모델·범위·예산이 방향을 바꿀 때.
- `GRILL_3_CORE_CONFIRMATION`: Gate 승인 직전 남은 차단 결정 확인.

한 번에 질문 하나만 제시한다. 질문에는 충돌·선택지·장단점·GPT 권장안·확정 영향을 포함한다. 사용자가 `남은 항목 모두 권장안대로`라고 하면 같은 유형의 남은 충돌을 권장안으로 확정한다.

## 8. P0~P3

- `P0`: 프로젝트 코어·실행 불가·저장 파손·치명적 UX·Gate 차단.
- `P1`: 핵심 재미·첫 경험·대표 품질·외부 검증에 직접 영향.
- `P2`: 품질·제작성·운영 효율 개선이지만 Gate를 즉시 막지 않음.
- `P3`: 후속 확장·장식·장기 최적화.

세부 수치 조정은 기본적으로 P2 또는 플레이테스트 Backlog다. 프로젝트 약속을 바꾸는 수치만 사용자 결정으로 승격한다.

## 9. 적대적 검토 5개 렌즈

큰 Gate에서는 다음 렌즈를 모두 적용하되 같은 검사를 횟수만 채우기 위해 반복하지 않는다.

1. 대화·요구·정체성·정본
2. 논리·Core Loop·판정 가능성
3. 경계·데이터·저장·호환성
4. 플레이어 경험·UI/UX·접근성·제작성
5. GitHub·시장·문서·통합 회귀

Finding은 다음으로 라우팅한다.

- `TECHNICAL_REVIEW_PROPOSAL`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- `NO_CHANGE`

## 10. 외부 AI·DeepSeek

외부 AI는 대량 초안·분류처럼 격리 가능한 작업에서만 사용한다.

- 격리 Branch·Worktree
- 입력 정본·범위·금지 사항 고정
- 결과를 기준 원본으로 자동 채택 금지
- 실제 diff·출처·테스트·라이선스 재검증
- 프로젝트 코어·사용자 승인 결정은 외부화 금지

## 11. GitHub·PDF·HiGodot 조건

- 기본 Branch 직접 수정 금지
- 결과·검증 단위 Commit
- 기획 PR과 구현 PR 분리
- 사용자가 명시하지 않으면 병합 금지
- Push·원격 HEAD·PR·Actions를 실제 확인
- PDF는 Registry 발행 정책이 요구할 때만 생성
- PDF 생성 후 전 페이지 렌더·한글·표·이미지·링크·최신성 검수
- HiGodot 도구 이름을 추측하지 않고 실제 도구 목록 확인
- 실행하지 않은 도구·렌더·런타임을 PASS로 보고하지 않음

## 12. 최종 3중 완전성 감사

### Requirement Coverage

사용자의 최신 요구와 이전 승인 내용이 책임 원본·구현·테스트·파생본에 연결됐는가?

### Skill Coverage

현재 Gate에 필요한 독립 책임이 실행됐고 Skill 실행 증거가 있는가?

### Artifact Coverage

필요한 게임 빌드·데이터·자산·문서·상점·테스트·GitHub 산출물이 실제로 존재하는가?

누락은 `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY`로 분류한다.
