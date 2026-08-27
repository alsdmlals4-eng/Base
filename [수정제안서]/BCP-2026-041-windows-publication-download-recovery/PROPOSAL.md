# BCP-2026-041 — Windows publication dependency download recovery

## 상태

```yaml
proposal_id: BCP-2026-041
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-27 user standing instruction — 지연·반복 실패 시 안전한 우회 경로 사용, 실제 검증, 문제·교훈 Base 환류
source_incident_run: 33041116377
first_green_attempt_run: 33042041600
baseline_main: b146e939a7ed4019fe85ce5135b29a28c5d7b98f
incremental_cost: 0
```

## 문제

Base main의 `Validate Game Project Operating System` 전체 검증에서 Windows publication smoke가 pinned LibreOffice MSI 다운로드 도중 두 번 연속 실패했다.

```text
attempt 1: Received an unexpected EOF or 0 bytes from the transport stream.
attempt 2: An existing connection was forcibly closed by the remote host.
```

첫 bounded-retry 구현 뒤에도 원본 endpoint가 `HTTP 429`를 반환해 같은 URI의 다른 transport client만으로는 복구되지 않았다.

같은 run 계보에서 다음은 모두 PASS였다.

```text
docs-validation
core-regression before new recovery contract
ubuntu-contract
publication-validation
Base v9 Operating Contracts
```

따라서 제품·계약 회귀가 아니라 외부 transport와 원본 endpoint rate-limit에 대한 복구 경로 부족으로 분류한다.

## 선택지 비교

| 안 | 장점 | 실패 | 판정 |
|---|---|---|---|
| 동일 `Invoke-WebRequest` 무한 재실행 | 변경 없음 | 지연·불확실성·완료 불가 | REJECT |
| Windows smoke 또는 hash 검사 제거 | 즉시 green | 검증/공급망 약화 | REJECT |
| floating latest 또는 임의 mirror | 우회 가능 | provenance·identity drift | REJECT |
| 같은 URI의 `curl.exe`만 추가 | transport stack 분리 | endpoint 429는 그대로 | PARTIAL |
| official TDF mirror 직접 경로 + TDF endpoint source fallback + 각 경로의 bounded transport retry + SHA 검증 | source와 transport 모두 우회, pin 유지, zero-cost | workflow helper 필요 | ADOPT |

## 승인 구현

- `Invoke-VerifiedDownload` helper를 Windows dependency install step 안에 둔다.
- 각 source route에서 primary transport는 PowerShell `Invoke-WebRequest`다.
- bounded retry, partial-file cleanup과 runner 내장 `curl.exe --fail --location --retry --retry-all-errors` fallback을 사용한다.
- LibreOffice primary source는 TDF mirror network에 속한 verified direct mirror인 `mirror.clarkson.edu/tdf`다.
- source fallback은 `download.documentfoundation.org`의 동일 pinned 파일이다.
- 어느 source/transport 경로에서도 같은 pinned version과 expected SHA-256을 통과해야 한다.
- hash mismatch는 source fallback으로 숨기지 않고 즉시 fail-closed한다.
- Poppler도 같은 verified transport helper를 사용한다.
- source/transport retry가 모두 실패하면 `TRANSPORT_RETRY_EXHAUSTED`로 실패한다.

## 근거

The Document Foundation의 다운로드 안내는 문제가 생기면 file detail/mirror list에서 다른 server를 선택하도록 안내한다. `mirror.clarkson.edu`의 TDF LibreOffice stable index에는 정확한 `26.2.3` 디렉터리와 Windows MSI가 존재하며, 기존 package verification에서도 같은 파일의 실제 mirror response로 관찰됐다.

이 BCP는 mirror 이름만 신뢰하지 않는다. exact pinned SHA-256을 최종 공급망 identity로 유지한다.

## 금지

```text
NO_TEST_OR_HASH_WEAKENING
NO_FLOATING_LATEST
NO_UNVERIFIED_MIRROR_SUBSTITUTION
NO_SILENT_SUCCESS
NO_PAID_FALLBACK
```

## 검증

- RED-first focused contract.
- workflow parser/governance regression.
- exact-head CI-high-risk tier.
- direct official TDF mirror와 fallback endpoint route contract.
- Windows platform smoke actual PASS.
- required `ci-gate` PASS.
- safe squash merge and post-merge full workflow readback.
- 최소 5회 전체 적대적 검토.

## 롤백

구현 squash commit을 revert해 이전 single-source/single-route download step으로 복원한다. pinned versions, hashes, product code, project canons and release artifacts remain unchanged.
