# BCP-2026-028 — Public Video Evidence Workflow Authority

## 출처와 상태

```yaml
proposal_id: BCP-2026-028-public-video-evidence-workflow-authority
status: SUBMITTED
source_project: alsdmlals4-eng/Base
source_commit: b1852eea26af1e0445aefdf717eeaf5e9717af6e
submitted_at: 2026-08-22
approval_ref: null
implementation_pr: null
```

이 제안은 이미 `main`에 유지된 PR #575의 **Evidence Knowledge workflow authority delta**를 사용자 결정 대상으로 분리한다. #575가 이미 병합됐다는 사실은 현재 상태 증거일 뿐, 이 proposal이 사전 승인이나 `historical_reconciliation`을 소급 생성한다는 뜻이 아니다.

관찰된 retained implementation:

- PR: `https://github.com/alsdmlals4-eng/Base/pull/575`
- merge SHA: `b1852eea26af1e0445aefdf717eeaf5e9717af6e`
- workflow: `.github/workflows/validate-evidence-knowledge.yml`
- permission: `contents: read`
- live YouTube retrieval: `NOT_RUN`
- project adoption of RM-TOOL-005 / RM-VIS-006: `NOT_RUN`

## 문제

PR #575는 `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`, provider-neutral visual-production contract, `HUMAN_EDIT_DELTA`를 기존 owner에 추가하면서 기존 `Validate Evidence-Based Game Development Knowledge` workflow의 다음 의미도 변경했다.

1. public-video spec/plan/tool/test path가 workflow trigger가 됐다.
2. `tools/public_video_research_ingest.py`가 compile 대상에 추가됐다.
3. `tests/test_public_video_research_ingest.py`와 `tests/test_public_video_research_integration_contract.py`가 Required unittest consumer에 추가됐다.
4. public-video/reuse 관련 docs/tool/tests가 evidence artifact 범위에 추가됐다.

권한은 `contents: read`로 유지됐지만, **어떤 변경이 Required workflow를 호출하고 무엇이 Required evidence를 구성하는지**가 바뀌었다. Workflow Authority는 보호된 의미 변경이므로 현재 retained 상태를 유지할지, 줄일지, 되돌릴지를 사용자 결정으로 닫아야 한다.

## 기존 해법 우선 조사

새 workflow를 만드는 것은 필요하지 않다. 현재 가능한 materially distinct 선택지는 기존 owner 안에서 세 가지다.

### 선택 A — 현행 #575 workflow delta 유지

기존 Evidence Knowledge workflow가 public-video adapter의 canonical CI owner를 계속 맡는다.

장점:
- tool/source contract 변경 시 focused public-video regressions가 자동 소비된다.
- 별도 workflow와 중복 CI를 만들지 않는다.
- current implementation과 rollback 경로가 이미 존재한다.

위험/비용:
- Evidence Knowledge workflow의 trigger/test surface가 넓어진다.
- docs/reuse 변경이 public-video regressions까지 실행할 수 있어 CI 비용이 소폭 증가한다.

### 선택 B — trigger는 유지하고 Required unittest/evidence artifact 범위를 축소

public-video 관련 path가 Evidence Knowledge를 깨우되, 새 focused tests를 기존 broader consumer에 흡수해 explicit test 목록을 줄인다.

장점:
- workflow topology는 유지하면서 required consumer 수를 줄일 수 있다.

위험:
- 기존 focused failure locality가 약해질 수 있다.
- 단순 축소가 실제 유지비 절감으로 이어지는지 별도 증거가 필요하다.

### 선택 C — #575 workflow delta만 revert

tool/module/docs는 유지하되 Evidence Knowledge trigger/test/evidence additions를 제거한다.

장점:
- workflow authority를 pre-#575 상태로 되돌린다.

위험:
- public-video tool 변경이 기존 Required path에서 직접 회귀되지 않을 수 있다.
- 다른 영구 consumer를 새로 만들면 Existing-Solution-First 원칙에 반한다.

## 임시 권장안

**선택 A 유지**를 provisional recommendation으로 둔다.

이유:

- #575의 public-video adapter는 game-development evidence ingestion의 기존 Evidence Knowledge owner와 직접 맞닿아 있다.
- 새 workflow를 만들지 않고 기존 owner를 재사용했다.
- permission은 `contents: read`에서 확대되지 않았다.
- tool/test path와 Required consumer가 동일 workflow에 함께 있어 변경→회귀 연결이 명확하다.

다만 이는 사용자 결정 전 승인 상태가 아니다.

## Evidence ceiling

이 BCP가 다루는 것은 **workflow authority**뿐이다.

다음을 승인하거나 증명하지 않는다.

```text
LIVE_YOUTUBE_RETRIEVAL: NOT_RUN
CURRENT_YOUTUBE_SITE_COMPATIBILITY: NOT_PROVEN
PROJECT_ADOPTION_RM_TOOL_005: NOT_RUN
PROJECT_ADOPTION_RM_VIS_006: NOT_RUN
HUMAN_EDIT_DELTA_REAL_MEASUREMENT: NOT_RUN
PAID_API_OR_PROXY: NOT_APPROVED
NEW_WORKFLOW_PERMISSION: NOT_PROPOSED
```

## 승인 시 적용 범위

### 선택 A가 승인되면

- 현재 #575 implementation을 다시 만드는 PR은 필요 없다.
- Registry/Proposal lifecycle에서 승인 근거만 연결한다.
- 이후 변경은 기존 Evidence Knowledge workflow와 focused regression을 사용한다.

### 선택 B 또는 C가 승인되면

별도의 narrow implementation PR에서 **workflow delta만** 조정한다. RM-TOOL-005, RM-VIS-006, `HUMAN_EDIT_DELTA`의 다른 현행 계약을 자동 철회하지 않는다.

## 검증 Gate

Proposal-only 단계:

```text
[수정제안서]/** only
→ PROPOSAL_REGISTRY schema
→ check_base_change_proposals.py
→ tests.test_base_change_proposals
→ Base v9 / Game Project OS when actually triggered
→ USER_DECISION_REQUIRED
```

Implementation 단계가 필요한 선택 B/C에서만:

```text
latest main
→ workflow delta minimum diff
→ public-video focused regressions
→ Evidence Knowledge
→ Base v9
→ Game Project OS final ci-gate
→ unresolved thread 0
→ exact-head merge
→ merged-main readback
```

`SKIPPED`, `NOT_RUN`, `CANCELLED`는 PASS가 아니다.

## 롤백

- 선택 A: 현재 main 유지. 별도 runtime/data migration 없음.
- 선택 B/C: 해당 implementation PR을 revert하면 #575 retained workflow behavior로 복귀한다.
- project repository, paid account, secret, runtime data migration은 이 BCP 범위에 없다.
