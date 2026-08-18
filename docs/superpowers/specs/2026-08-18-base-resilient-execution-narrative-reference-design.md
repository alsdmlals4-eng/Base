# Base Resilient Execution and Narrative Reference Design

## Goal

Base의 기존 장기 작업 계약을 복제하지 않고, 현재 빠진 네 경계를 기존 owner에 연결한다.

1. 새 PowerShell 창에서 시작해 한 블록만 붙여넣는 재현 가능한 사용자 실행 계약
2. 사용자 관리 `글따라쓰기` Google Doc을 실시간 사용자 선호 증거로 읽는 소설/스토리/대화 참고 경로
3. 병합·postmerge 뒤 `REQUIRED_WORK_REMAINING`을 다시 계산하고 0이 아니면 승인 범위 안의 후속 작업을 재큐잉하는 연속작업 종료 계약
4. 작업 중 얻은 공용 교훈·구조·시스템의 재사용 승격을 기존 Base-change / Skill-evolution owner에 연결하는 Gate

## Current-state findings

현재 `AGENTS.md`와 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`에는 이미 현행 조사, 최소 3개 실질 대안, 벤치마킹, 더 나은 대안 탐색, 장기 적합성, 최소 5회 전체 적대적 개선 루프, 비용 경계, 독립 workstream 격리, core loop/dummy balance/build/test, 세계관-스토리 정합성, 재사용 시스템 추출, Figma/legacy Sheets 전환, Tool Hub/Loop Engineering 사용 경계가 있다.

따라서 새 요구를 상위 파일에 장문으로 중복하지 않는다. 세부 실행 semantics는 기존 owner 또는 새 narrow operations contract가 소유하고, 상위 문서는 발견 가능한 invariant/pointer만 가진다.

## Alternatives

### A. 모든 새 요구를 `AGENTS.md`에 직접 장문 추가

- 장점: 즉시 발견 가능
- 단점: owner 문서와 중복되고 Base 업데이트 때 drift가 커진다.
- 판정: `REJECT`

### B. `resilient-base-workflow` 같은 새 광역 Skill 생성

- 장점: 하나의 진입점
- 단점: intake, continuous work, Base promotion, serial fiction, Tool Hub/Loop Engineering과 책임이 중첩되고 sparse routing 정확도를 낮춘다.
- 판정: `REJECT`

### C. 얇은 상위 invariant + 기존 owner Skill/reference + narrow PowerShell contract

- 장점: 현재 책임 구조를 보존하고, 독립된 PowerShell 사용자 실행 semantics만 별도 문서로 격리한다. 새 Skill 없이도 재사용 가능하며 Base 변화에 강하다.
- 단점: discoverability를 테스트로 보장해야 한다.
- 판정: `ADOPT`

## Architecture

### PowerShell

새 문서 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`가 사용자에게 제공하는 PowerShell 블록의 공용 형식을 소유한다.

- `FRESH_SHELL_ASSUMPTION`
- `ONE_COPY_PASTE_BLOCK`
- `LOCATION_FIRST`
- `NO_PRIOR_SHELL_STATE_DEPENDENCY`
- `FAIL_FAST`
- `NATIVE_EXIT_CODE_REQUIRED`
- `ERROR_STAGE_MARKER`
- `BEGINNER_SAFE_USER_ACTION`

상위 `AGENTS.md`, `START_HERE.md`, `LONG_HORIZON_WORK_EXECUTION_POLICY.md`, `DOCUMENTATION_MAP.md`는 이 owner를 가리킨다.

### Serial-fiction preference reference

기존 `developing-and-revising-serial-fiction`이 소유한다. 새 Skill을 만들지 않는다.

새 포인터 `docs/knowledge/serial-fiction/BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md`에는 문서 원문/URL/ID를 저장하지 않는다. 연결된 Google Drive에서 정확한 제목 `글따라쓰기`를 live read할 수 있을 때만 `USER_PREFERENCE_EVIDENCE`로 사용한다.

분석 대상은 식별 가능한 문체 복제가 아니라 다음 구조다.

- `PARAGRAPH_BREAK_AND_BREATH`
- `LINE_BREAK_RHYTHM`
- `PARAGRAPH_LENGTH_PATTERN`
- `DIALOGUE_NARRATION_ALTERNATION`
- `REACTION_ISOLATION`
- blank-line beat / scene transition

고정 문단 길이나 “한 문장 = 한 문단” 같은 universal quota를 만들지 않는다.

### Continuous completion

`continuous-work-execution.md`가 merge를 terminal state로 취급하지 않게 한다.

```text
merge
→ postmerge readback
→ REQUIRED_WORK_REMAINING recalc
→ 0 ? complete : derive in-scope ready/deferred work and continue
```

진짜 전역 blocker나 새 사용자 결정이 아닌 한 routine approval로 멈추지 않는다.

### Reusable lesson promotion

`REUSABLE_LESSON_PROMOTION_GATE`는 새 Skill이 아니라 라우팅 계약이다.

```text
incident / failure / solution / repeated pattern
→ project-specific vs reusable 분리
→ existing owner reuse/extend 우선
→ reusable module extraction when executable boundary exists
→ Base proposal when shared policy/skill/module change is warranted
→ new Skill last, only with independent boundary
```

활성 Skill 수를 고정 목표로 두지 않는다.

## Privacy and copyright boundary

- 사용자 Google Doc의 URL, document ID, 원문을 공개 Base에 커밋하지 않는다.
- 사용자 선호 증거는 정본이나 외부 공개 benchmark가 아니다.
- 구조적 특성을 추출하되 특정 작품/작가의 식별 가능한 문장·말투·비유를 모사하지 않는다.
- live source가 현재 접근 불가하고 그 분석이 결과에 필수면 `BLOCKED_UNVERIFIED`; 독립 작업은 계속할 수 있다.

## Verification

TDD 계약 테스트가 다음을 강제한다.

- PowerShell owner 존재와 entrypoint discoverability
- continuous-work remaining-work 재계산/재큐잉
- reuse promotion owner routing
- serial-fiction line-break/breath contract
- live Drive pointer의 privacy: `docs.google.com/document/d/` 및 raw document ID 금지
- preference evidence가 canon/style imitation이 아님

그 뒤 exact-head CI, PR diff/content preservation, 최소 5회 전체 적대적 개선 루프, latest-main reconciliation, unresolved threads 0을 거쳐 병합한다.
