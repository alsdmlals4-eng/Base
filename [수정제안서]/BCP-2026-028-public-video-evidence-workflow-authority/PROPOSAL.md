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

권한은 `contents: read`로 유지됐지만, **어떤 변경이 Required workflow를 호출하고 무엇이 Required evidence를 구성하는지**가 바뀌었다. Workflow Authority는 보호된 의미 변경이므로 현재 retained 상태를 유지할지, 줄일지, 되돌릴지를 사용자 결정으로 닫아야 한다.

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

새 workflow를 만드는 것은 필요하지 않다. 현재 가능한 materially distinct 선택지는 기존 owner 안에서 세 가지다.

### 후보 A — 현행 #575 workflow delta 유지

기존 Evidence Knowledge workflow가 public-video adapter의 canonical CI owner를 계속 맡는다.

장점:
- tool/source contract 변경 시 focused public-video regressions가 자동 소비된다.
- 별도 workflow와 중복 CI를 만들지 않는다.
- current implementation과 rollback 경로가 이미 존재한다.

비용:
- Evidence Knowledge workflow의 trigger/test surface가 넓어진다.
- docs/reuse 변경이 public-video regressions까지 실행할 수 있어 CI 비용이 소폭 증가한다.

### 후보 B — 기존 workflow owner 안에서 trigger/test/evidence surface 축소

public-video 관련 path가 Evidence Knowledge를 깨우되, focused assertion 일부를 이미 실행되는 broader consumer에 흡수해 explicit consumer 수를 줄인다.

장점:
- 새 workflow 없이 topology를 유지한다.

비용:
- focused failure locality가 약해질 수 있다.
- 축소가 실제 유지비 절감으로 이어지는지 별도 증거가 필요하다.

### 후보 C — #575 workflow delta만 revert

tool/module/docs는 유지하되 Evidence Knowledge trigger/test/evidence additions를 제거한다.

장점:
- workflow authority를 pre-#575 상태로 되돌린다.

비용:
- public-video tool 변경이 기존 Required path에서 직접 회귀되지 않을 수 있다.
- 다른 영구 consumer를 새로 만들면 Existing-Solution-First 원칙에 반한다.

임시 권장안은 **후보 A 유지**다. #575의 adapter가 game-development evidence ingestion의 기존 Evidence Knowledge owner와 직접 맞닿아 있고, 새 workflow를 만들지 않았으며 permission도 `contents: read`에서 확대되지 않았기 때문이다. 다만 이는 사용자 결정 전 승인 상태가 아니다.

## 적용 조건과 비사용 조건

### 적용 조건

- public-video evidence adapter와 그 provenance/fail-closed contract를 Base 공용 Required evidence 경로에서 지속적으로 보호하려는 경우
- 별도 workflow를 만들지 않고 기존 Evidence Knowledge owner를 재사용하려는 경우
- 현재 `contents: read` permission ceiling을 유지하는 경우

### 비사용 조건

- public-video adapter 자체를 Base 공용 evidence owner에서 제거하기로 결정한 경우
- workflow trigger/test 확대 비용이 실제 사용가치보다 크다는 근거가 생긴 경우
- 별도 project-local validation으로만 충분하고 Base Required consumer가 불필요하다고 결정한 경우

이 BCP는 live YouTube retrieval, project adoption, provider 품질, paid API/proxy 도입을 승인하지 않는다.

## 반례와 위험

### 위험 1 — Required workflow surface 과확장

public-video와 무관한 reuse/docs 변경까지 focused tests를 실행해 CI 비용이 늘 수 있다.

완화: 후보 B를 선택할 경우 기존 owner 안에서 trigger/test surface만 최소화하고 새 workflow는 만들지 않는다.

### 위험 2 — workflow delta revert 후 회귀 owner 부재

후보 C를 선택하면서 replacement consumer 없이 제거하면 tool 변경이 Required CI에서 보호되지 않을 수 있다.

완화: revert 전에 existing broader consumer가 동일 assertion을 실제 실행하는지 증거로 확인한다. 없으면 조용히 PASS로 간주하지 않는다.

### 위험 3 — CI GREEN을 live-site 호환성으로 오인

unit/contract test는 현재 YouTube site compatibility나 실제 caption availability를 증명하지 않는다.

완화: `LIVE_YOUTUBE_RETRIEVAL: NOT_RUN`과 `CURRENT_YOUTUBE_SITE_COMPATIBILITY: NOT_PROVEN`을 유지한다.

### 위험 4 — 병합 사실을 사전 승인으로 소급 해석

#575가 이미 main에 있다는 사실은 lifecycle 승인 증거가 아니다.

완화: 이 record는 `SUBMITTED`, `approval_ref: null`, `implementation_pr: null`로 시작하고 `historical_reconciliation`을 사용하지 않는다.

## 영향 범위와 검증

이 BCP의 결정 범위는 #575가 기존 `.github/workflows/validate-evidence-knowledge.yml`에 추가한 **trigger / compile / unittest / evidence-artifact authority delta**다.

다음을 자동 변경하지 않는다.

- `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER` contract
- `RM-VIS-006 VISUAL_CREATIVE_PROVIDER_ADAPTER` contract
- `HUMAN_EDIT_DELTA`
- project repositories
- paid account / API secret / proxy
- runtime data

Proposal-only 검증:

```text
[수정제안서]/** only
→ PROPOSAL_REGISTRY schema
→ check_base_change_proposals.py
→ tests.test_base_change_proposals
→ Base v9 / Game Project OS when actually triggered
→ USER_DECISION_REQUIRED
```

후보 B/C가 승인되어 implementation이 필요한 경우에만:

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

## 승인과 구현

현재 상태는 `SUBMITTED`다.

사용자 결정:

- **KEEP / 후보 A**: 현재 #575 workflow delta를 유지한다. 승인 뒤 proposal lifecycle에 `approval_ref`를 연결하되 동일 implementation을 다시 만드는 PR은 만들지 않는다.
- **ADJUST / 후보 B**: approval_ref를 연결한 뒤 별도 narrow implementation PR에서 existing workflow owner 안의 trigger/test/evidence surface만 조정한다.
- **REVERT / 후보 C**: approval_ref를 연결한 뒤 별도 narrow implementation PR에서 #575의 workflow-authority delta만 되돌린다. module/tool의 다른 현행 계약을 자동 철회하지 않는다.

승인 전에는 #575 implementation을 확대·축소·철회하지 않는다.

Rollback:

- 후보 A: 현재 main 유지. 별도 runtime/data migration 없음.
- 후보 B/C: 해당 implementation PR을 revert하면 #575 retained workflow behavior로 복귀한다.
- project repository, paid account, secret, runtime data migration은 이 BCP 범위에 없다.
