# BCP-2026-028 — Public Video Evidence Workflow Authority

## 출처와 상태

```yaml
proposal_id: BCP-2026-028-public-video-evidence-workflow-authority
status: APPROVED_FOR_IMPLEMENTATION
source_project: alsdmlals4-eng/Base
source_commit: b1852eea26af1e0445aefdf717eeaf5e9717af6e
submitted_at: 2026-08-22
approval_ref: https://github.com/alsdmlals4-eng/Base/pull/596#issuecomment-5377786729
implementation_pr: null
```

이 제안은 이미 `main`에 유지된 PR #575의 **Evidence Knowledge workflow authority delta**를 사용자 결정 대상으로 분리했다. PR #596에서 proposal-only 상태로 제출·검증된 뒤, 사용자가 2026-08-22 13:06 KST에 **KEEP / 후보 A**를 명시 승인했다. #575가 승인 전에 이미 병합돼 있었다는 사실은 그대로 보존하며, 이 승인 기록이 사전 승인이나 `historical_reconciliation`을 소급 생성한다는 뜻은 아니다.

## 관찰과 증거

관찰된 retained implementation:

- PR: `https://github.com/alsdmlals4-eng/Base/pull/575`
- merge SHA: `b1852eea26af1e0445aefdf717eeaf5e9717af6e`
- workflow: `.github/workflows/validate-evidence-knowledge.yml`
- permission: `contents: read`
- live YouTube retrieval: `NOT_RUN`
- project adoption of RM-TOOL-005 / RM-VIS-006: `NOT_RUN`

PR #575는 `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`, provider-neutral visual-production contract, `HUMAN_EDIT_DELTA`를 기존 owner에 추가하면서 기존 `Validate Evidence-Based Game Development Knowledge` workflow의 다음 의미도 변경했다.

1. public-video spec/plan/tool/test path가 workflow trigger가 됐다.
2. `tools/public_video_research_ingest.py`가 compile 대상에 추가됐다.
3. `tests/test_public_video_research_ingest.py`와 `tests/test_public_video_research_integration_contract.py`가 Required unittest consumer에 추가됐다.
4. public-video/reuse 관련 docs/tool/tests가 evidence artifact 범위에 추가됐다.

권한은 `contents: read`로 유지됐지만, **어떤 변경이 Required workflow를 호출하고 무엇이 Required evidence를 구성하는지**가 바뀌었다. 사용자는 이 retained workflow authority를 현재 범위 그대로 유지하는 후보 A를 승인했다.

Evidence ceiling:

```text
LIVE_YOUTUBE_RETRIEVAL: NOT_RUN
CURRENT_YOUTUBE_SITE_COMPATIBILITY: NOT_PROVEN
PROJECT_ADOPTION_RM_TOOL_005: NOT_RUN
PROJECT_ADOPTION_RM_VIS_006: NOT_RUN
HUMAN_EDIT_DELTA_REAL_MEASUREMENT: NOT_RUN
PAID_API_OR_PROXY: NOT_APPROVED
NEW_WORKFLOW_PERMISSION: NOT_PROPOSED
```

## 일반화 후보

새 workflow를 만드는 것은 필요하지 않다. 검토한 materially distinct 선택지는 기존 owner 안의 세 가지였다.

### 후보 A — 현행 #575 workflow delta 유지 — APPROVED

기존 Evidence Knowledge workflow가 public-video adapter의 canonical CI owner를 계속 맡는다.

장점:
- tool/source contract 변경 시 focused public-video regressions가 자동 소비된다.
- 별도 workflow와 중복 CI를 만들지 않는다.
- current implementation과 rollback 경로가 이미 존재한다.

비용:
- Evidence Knowledge workflow의 trigger/test surface가 넓어진다.
- docs/reuse 변경이 public-video regressions까지 실행할 수 있어 CI 비용이 소폭 증가한다.

### 후보 B — 기존 workflow owner 안에서 trigger/test/evidence surface 축소 — NOT_SELECTED

public-video 관련 path가 Evidence Knowledge를 깨우되, focused assertion 일부를 이미 실행되는 broader consumer에 흡수해 explicit consumer 수를 줄인다.

장점:
- 새 workflow 없이 topology를 유지한다.

비용:
- focused failure locality가 약해질 수 있다.
- 축소가 실제 유지비 절감으로 이어지는지 별도 증거가 필요하다.

### 후보 C — #575 workflow delta만 revert — NOT_SELECTED

tool/module/docs는 유지하되 Evidence Knowledge trigger/test/evidence additions를 제거한다.

장점:
- workflow authority를 pre-#575 상태로 되돌린다.

비용:
- public-video tool 변경이 기존 Required path에서 직접 회귀되지 않을 수 있다.
- 다른 영구 consumer를 새로 만들면 Existing-Solution-First 원칙에 반한다.

## 적용 조건과 비사용 조건

### 적용 조건

- public-video evidence adapter와 그 provenance/fail-closed contract를 Base 공용 Required evidence 경로에서 지속적으로 보호하려는 경우
- 별도 workflow를 만들지 않고 기존 Evidence Knowledge owner를 재사용하려는 경우
- 현재 `contents: read` permission ceiling을 유지하는 경우

### 비사용 조건

- public-video adapter 자체를 Base 공용 evidence owner에서 제거하기로 결정한 경우
- workflow trigger/test 확대 비용이 실제 사용가치보다 크다는 근거가 생긴 경우
- 별도 project-local validation으로만 충분하고 Base Required consumer가 불필요하다고 다시 결정한 경우

이 BCP는 live YouTube retrieval, project adoption, provider 품질, paid API/proxy 도입을 승인하지 않는다.

## 반례와 위험

### 위험 1 — Required workflow surface 과확장

public-video와 무관한 reuse/docs 변경까지 focused tests를 실행해 CI 비용이 늘 수 있다.

완화: 실제 비용 증거가 생기면 별도 승인으로 후보 B를 재검토한다. 현재 승인 범위에서는 새 workflow를 만들지 않는다.

### 위험 2 — workflow delta revert 후 회귀 owner 부재

후보 C를 선택하면서 replacement consumer 없이 제거하면 tool 변경이 Required CI에서 보호되지 않을 수 있다.

완화: 현재 선택은 후보 A이므로 이 위험을 만들지 않는다. 향후 revert를 검토할 경우 existing broader consumer가 동일 assertion을 실제 실행하는지 먼저 확인한다.

### 위험 3 — CI GREEN을 live-site 호환성으로 오인

unit/contract test는 현재 YouTube site compatibility나 실제 caption availability를 증명하지 않는다.

완화: `LIVE_YOUTUBE_RETRIEVAL: NOT_RUN`과 `CURRENT_YOUTUBE_SITE_COMPATIBILITY: NOT_PROVEN`을 유지한다.

### 위험 4 — 병합 사실을 사전 승인으로 소급 해석

#575가 이미 main에 있다는 사실은 lifecycle 승인 증거가 아니다.

완화: 이 record는 `SUBMITTED`로 시작했고, 별도 proposal PR #596과 사용자 KEEP 승인 comment를 거쳐 `APPROVED_FOR_IMPLEMENTATION`으로 전환한다. `historical_reconciliation`은 사용하지 않는다.

## 영향 범위와 검증

승인 범위는 #575가 기존 `.github/workflows/validate-evidence-knowledge.yml`에 추가한 **trigger / compile / unittest / evidence-artifact authority delta**의 유지다.

다음을 자동 변경하지 않는다.

- `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER` contract
- `RM-VIS-006 VISUAL_CREATIVE_PROVIDER_ADAPTER` contract
- `HUMAN_EDIT_DELTA`
- project repositories
- paid account / API secret / proxy
- runtime data

승인 상태 전이 검증:

```text
[수정제안서]/** only
→ PROPOSAL_REGISTRY schema
→ check_base_change_proposals.py
→ tests.test_base_change_proposals
→ approval_ref readback
→ APPROVED_FOR_IMPLEMENTATION
```

KEEP 후보의 구현 검증은 새 구현을 만드는 대신 현재 `main`의 retained #575 workflow를 직접 재검증한다.

```text
latest main
→ #575 merge/readback
→ workflow permission == contents: read
→ public-video trigger paths present
→ public-video compile/unittest consumers present
→ evidence artifact coverage present
→ Evidence Knowledge
→ Base v9
→ Game Project OS final ci-gate
→ IMPLEMENTED lifecycle closeout
```

`SKIPPED`, `NOT_RUN`, `CANCELLED`는 PASS가 아니다.

## 승인과 구현

사용자 결정:

- 선택: **KEEP / 후보 A**
- 승인 시각: `2026-08-22 13:06 KST`
- approval_ref: `https://github.com/alsdmlals4-eng/Base/pull/596#issuecomment-5377786729`
- 승인 범위: 현재 #575 Evidence Knowledge workflow의 public-video trigger / compile / unittest / evidence-artifact delta 유지
- 권한 상한: `contents: read` 유지
- 제외: live YouTube retrieval, current-site compatibility, project adoption, paid API/proxy, 새 workflow permission

현재 상태는 `APPROVED_FOR_IMPLEMENTATION`이다.

#575 구현은 이 승인보다 먼저 main에 존재했다. 따라서 동일 implementation을 다시 만드는 PR은 만들지 않는다. 다음 lifecycle 단계는 현재 retained #575 implementation이 위 승인 범위와 일치하는지 latest-main에서 검증하고, 일치할 경우 `implementation_pr=https://github.com/alsdmlals4-eng/Base/pull/575`로 연결해 `IMPLEMENTED`를 닫는 것이다. 이는 사전 승인을 소급 주장하는 것이 아니라 **승인 후 현재 retained implementation을 검증해 유지 결정을 닫는 절차**다.

Rollback:

- 후보 A 승인 상태에서 implementation 검증이 승인 범위와 불일치하면 `IMPLEMENTED`로 올리지 않고 별도 조정 결정을 요청한다.
- 향후 ADJUST/REVERT가 새로 승인되면 별도 narrow implementation PR로 수행한다.
- project repository, paid account, secret, runtime data migration은 이 BCP 범위에 없다.
