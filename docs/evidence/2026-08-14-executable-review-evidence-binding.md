# Executable Review Evidence Binding — Pre-Merge Evidence

## 상태

- 구현 PR: `#330`
- 기준 `main`: `39936ff6a83410b4169878c1335de9eb3e4c25cf`
- 검증된 구현 HEAD: `d25819cb47005ed7f5644c4624fda85553653421`
- PR test-merge SHA: `c30be65721861caac28fc616ee925f9285ce85de`
- 구현·검증·Intent Gate: `PASS`
- Integration Gate: `BLOCKED_UNVERIFIED`

이 문서는 병합 전 증거다. PR merged 상태, merge SHA, 새 `main` readback과 post-merge checks는 아직 완료로 기록하지 않는다.

## 목표와 적용 구조

기존 BCP-2026-027의 `claim-and-intent-verification` Mode에 실행 가능한 검수 계층을 흡수했다. 새 ACTIVE Skill이나 중복 BCP owner는 만들지 않았다.

주요 산출물:

- 정본 verifier: `tools/check_review_evidence.py`
- 입력·결과 Schema: `skills/reviewing-and-validating-project-changes/contracts/`
- Skill package compatibility entrypoint: `skills/reviewing-and-validating-project-changes/scripts/verify_evidence.py`
- task record Template: `templates/quality/REVIEW_EVIDENCE_RECORD.json`
- 행동·통합 회귀: `tests/test_claim_evidence_binding.py`, `tests/test_skill_implementation_evidence.py`
- owner Skill, Learning Log, reference-freshness companion 갱신

보호 범위:

- ACTIVE Skill 30개와 `PLAN / BUILD / REVIEW` 유지
- 제품·Godot·scene·data·asset·migration 변경 없음
- 외부 Eval 서비스 비의무화
- TEST Evidence의 runtime·render·human 자동 승격 금지

## 검증하는 사실

1. reviewer가 지정한 base와 현재 HEAD가 실제 Git commit이며 ancestor 관계인지 확인한다.
2. clean worktree와 actual diff를 확인한다.
3. allowed·protected path와 Acceptance implementation path를 실제 diff에 대조한다.
4. 검증을 실제로 실행하지 않았으면 `NOT_RUN`을 유지한다.
5. 성공 결과와 required marker를 함께 확인한다.
6. 검증 실행 전후의 base SHA, HEAD, changed-file set, clean state를 다시 대조한다.
7. 기본 Evidence ceiling은 `TEST`이며 높은 층은 check별 명시 승인을 요구한다.
8. 병합 전 integration은 항상 `BLOCKED_UNVERIFIED`다.

경로 pattern은 단일 `*`가 디렉터리 구분자를 넘지 않고 `**`만 descendant를 포함하도록 구현했다. 대괄호가 들어간 저장소 경로는 literal로 처리한다.

## TDD·디버깅 증거

### package owner 연결 실패

최초 Game Project Operating System 검사는 새 packaged verifier가 owner Skill에 연결되지 않은 package-integrity 오류를 검출했다.

- workflow run: `31722720638`
- failing job: `94523549169`
- 수정: owner Skill에 canonical tool, Schema, Template과 compatibility entrypoint를 연결

### scope pattern RED

Required-CI 소비자 테스트에서 단일-directory pattern이 nested path를 잘못 포함하는 문제를 재현했다.

- RED HEAD: `b57674d0c979f52494b49a75f86f8234c454fa0f`
- workflow run: `31752582511`
- failing job: `94621355000`
- 결과: `42 tests / 1 failure`
- 수정: slash-aware pattern matcher 적용

### post-check mutation RED

성공 결과를 낸 검증이 저장소 파일을 바꾸면 결과를 무효화하는 반례를 추가했다. verifier는 실행 전후 snapshot 차이를 확인하고 verification·Intent·claim을 fail-closed 상태로 돌린다.

## exact-head GREEN

검증된 구현 HEAD `d25819cb47005ed7f5644c4624fda85553653421`에서 다음 workflow가 모두 성공했다.

| Workflow | Run ID | 결과 |
|---|---:|---|
| Evidence-Based Game Development Knowledge | `31753003616` | success |
| BCA Visual and Sheet Workflow | `31753003618` | success |
| Integrated Vertical Slice Prompt | `31753003623` | success |
| Base v9 Operating Contracts | `31753003631` | success |
| Skill Behavior Evidence | `31753003674` | success |
| Game Project Operating System | `31753003679` | success |

Load-bearing 결과:

- Skill Behavior focused suite: `42 passed / 0 failed`
- Game Project OS contract suite: `93 passed / 0 failed`
- Base change proposal checker: `27 proposals validated`
- canonical reference freshness: `PASS — 795 files scanned / 14 changed files`
- publication validation: success
- docs validation: success
- Windows-specific runtime validation: not claimed

## 동시 변경·적대적 검토

열린 PR #333, #336, #337과 #330의 exact changed-path overlap은 각각 0개였다. 검증 시점의 `main`은 기준 SHA에서 이동하지 않았다.

| Finding | 심각도 | 처리 |
|---|---|---|
| packaged verifier owner 연결 누락 | P1 | owner Skill 연결 |
| single-star scope widening | P1 | slash-aware matcher와 RED/GREEN 회귀 |
| successful check의 repository mutation | P1 | post-check exact state 검증 |
| packaged/canonical 구현 중복 | P2 | packaged entrypoint를 canonical delegate로 축소 |
| 불필요한 evidence-index churn | P2 | index·generated view 변경 원상복구 |
| runtime·render·human Evidence 부재 | 경계 | 미실행·미주장 유지 |

```text
unresolved P0: 0
unresolved P1: 0
implementation: PASS
verification: PASS
intent: PASS
integration: BLOCKED_UNVERIFIED
```

## 남은 절차와 롤백

이 문서 추가 뒤 새 exact HEAD를 다시 검증하고, PR을 ready 상태로 전환해 expected-head squash merge한다. 이후 merged state, merge SHA, 새 `main` file readback과 post-merge workflows를 별도 확인한다.

롤백은 기능 merge commit 하나를 revert한다. 기존 BCP-2026-027과 제품 저장소는 영향받지 않는다.
