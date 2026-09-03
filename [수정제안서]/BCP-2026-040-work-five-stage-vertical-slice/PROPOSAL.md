# BCP-2026-040 — Work 5단계 버티컬 슬라이스 실행 계약

## 상태

```yaml
proposal_id: BCP-2026-040
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-27 user instruction in current chat
baseline_main: 9b45125d087521fa98696cbd1e857bf2ffbf816a
incremental_cost: 0
public_release_authority: false
human_player_evidence: NOT_RUN
```

## 사용자 목표

앞으로 프로젝트 Work 작업을 다음 다섯 단계로 명확하게 운영한다.

```text
1. 기획
2. 검수
3. 이미지·사운드·UI·Data·VFX 등 요소 생성
4. Codex 제품 구현과 Machine QA
5. 사용자 실제 검증
```

기획의 핵심 요소는 GPT가 독단적으로 확정하지 않는다. 현재 프로젝트 정본·실제 구현·재사용 자료·최신 벤치마크·성공/실패 사례를 먼저 조사하고, 핵심 재미·Core Loop·플레이어 판타지·의미 있는 선택·보상/실패·차별점·첫 세션·Slice 범위처럼 제품 의미를 바꾸는 결정은 Grill Me를 사용해 사용자와 함께 확정한다.

## 실제 발견 문제

Base current main의 `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`는 active orchestration을 다음 세 단계로 정의한다.

```text
Stage A — Work production input completion
Stage B — one Codex implementation window
Stage C — consolidated return / final Work review / user handoff
```

그 결과:

- 기획, 기획 검수, 이미지·사운드·데이터 제작이 Stage A 하나에 묶인다.
- Machine QA와 사용자 검증 준비가 Stage C에 함께 묶인다.
- `AUTOMATED_VERTICAL_SLICE_READY`와 사용자 검증을 거친 완성 상태의 이름이 충분히 강하게 분리되지 않는다.
- 핵심 기획에서 Grill Me와 벤치마크를 언제 실행해야 하는지 Starter에서 즉시 보이지 않는다.

프로젝트 정본도 서로 다른 상태 어휘를 사용한다.

- `PLAN`, `PLANNING_COMPLETE`
- `IMPLEMENTATION_READY`
- `MERGED_MAIN_AUTOMATED_VERTICAL_SLICE_READY`
- `USER_VERTICAL_SLICE_VALIDATION_PENDING`
- `runtime implementation authorization`
- package candidate / physical / human gates

이 값들을 전 프로젝트에서 강제 개명하면 정본 churn과 현재 workstream 충돌이 커진다.

## 비교한 대안

### A. 현행 3단계 유지 + 설명만 보강

- 장점: 변경이 작다.
- 문제: 기획·검수·요소 제작의 실제 책임과 종료 Gate가 계속 섞인다.
- 판정: REJECT.

### B. 단방향 엄격 5단계

- 장점: 이해가 쉽다.
- 문제: 사용자 검증이나 구현 중 발견이 앞 단계로 돌아갈 때 폭포수식 재작업과 우회가 발생한다.
- 판정: REJECT.

### C. 명시적 5단계 + 단계별 반환 경로 + 기존 세부 owner 재사용

- 장점: 역할·입출력·완료선을 명확히 하면서 실제 반복 개발을 보존한다.
- 기존 Minimum Transition, Local Visual, Evidence Identity, Grill Me, Benchmark, Vertical Slice Skill을 재사용한다.
- 프로젝트 고유 상태는 mapping receipt로 연결해 대량 개명을 피한다.
- 판정: ADOPT.

## 외부 benchmark 요약

- Unity Learn은 게임 개발을 stages/milestones로 나누고 Vertical Slice를 첫 주요 milestone으로 다룬다.
- Unity의 공식 2D Roguelike 과정은 Vertical Slice를 더 큰 게임의 기능하는 구간이며 최종 게임이 어떻게 보이고 플레이되는지 시험하는 용도로 설명한다.
- Unity의 prototype 과정은 핵심 기능과 필요한 이미지·사운드·모델·애니메이션 자산 계획을 개발 전에 확인하도록 한다.
- Epic UEFN 문서는 playtesting이 메커닉이 의도대로 동작하는지 확인하는 별도의 핵심 단계라고 설명한다.
- Unreal packaging 문서는 독립 실행 가능한 패키지가 build/cook/stage/package를 통과해야 함을 구분한다.

위 근거는 Base/Project canon을 덮어쓰지 않고, Stage 4의 machine-ready build와 Stage 5의 실제 사용자 검증을 분리하는 보조 근거로 사용한다.

## 승인 구현 범위

1. 새 얇은 stage orchestration owner를 추가한다.
2. current Starter와 Router가 이를 찾도록 한다.
3. 기존 3-stage profile은 세부 실행 owner로 유지하되 stage label authority만 새 5-stage contract가 supersede한다.
4. Stage 1 핵심 기획은 benchmark + 최소 3안 + Grill Me + 사용자 Decision을 요구한다.
5. Stage 2는 기획 정합성·실현 가능성·IRG·Requirement Trace·acceptance·asset coverage를 검수한다.
6. Stage 3은 Work가 이미지·사운드·UI·Data·VFX·권리·manifest·handoff input을 만든다.
7. Stage 4는 Codex 구현·test/runtime/build·Work machine evidence review·safe merge/readback까지 닫는다.
8. Stage 5는 사용자가 실제 다운로드 build를 플레이하고 확장/수정/튜닝/재기획/보류/중단을 결정한다.
9. `VERTICAL_SLICE_COMPLETE`는 Stage 5를 통과한 상태로만 정의한다.
10. 실제 프로젝트 GitHub·Notion current state를 관찰한 audit를 evidence-only로 남긴다.

## 제외 범위

- 프로젝트별 현재 Decision·Core·Art Direction 변경
- 모든 프로젝트 문서의 상태명을 일괄 rename/migrate
- Notion portfolio 대량 write
- Codex 또는 Godot 제품 구현
- 이미지·사운드 실제 생성
- Human/Player PASS 주장
- 공개 배포·스토어 제출
- 유료 도구·API·runner 추가
- 다른 open PR 수정·흡수·병합

## 단계 완료 정의

```text
Stage 4 PASS
= AUTOMATED_VERTICAL_SLICE_READY_FOR_USER_VALIDATION
= machine-executable work 0
= downloadable build available
= Human/Player NOT_RUN
!= Vertical Slice Complete

Stage 5 PASS
= user actually played exact build
+ feedback/observation captured
+ blocking findings corrected or explicitly accepted/deferred
+ canonical reflection/readback
= USER_VALIDATED_VERTICAL_SLICE_COMPLETE
```

`USER_VALIDATED_VERTICAL_SLICE_COMPLETE`는 현재 Slice 완료이며 전체 게임·출시 준비 완료를 뜻하지 않는다.

## 검증

- RED-first focused contract
- current Starter/Router routing
- exact five stage order and stage output/exit gates
- Grill Me/benchmark/3 alternatives/User Decision Stage 1 gate
- stage-boundary negative contracts
- Stage 4 != complete / Stage 5 = complete
- representative project GitHub/Notion status mapping audit
- project-specific value leakage negative test
- exact-head Base required workflows
- minimum five full-scope adversarial loops
- safe squash merge and new-main readback

## 롤백

implementation squash commit을 revert하고 Starter/Router에서 새 stage owner link를 제거한다. 기존 3-stage detail profile, startup checklist, local Visual owner, evidence identity owner, 프로젝트 정본·제품 구현은 그대로 유지한다.
