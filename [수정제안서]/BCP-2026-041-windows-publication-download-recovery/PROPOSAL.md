# BCP-2026-041 — Windows publication dependency download recovery

## 상태

```yaml
proposal_id: BCP-2026-041
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-27 user standing instruction — 지연·반복 실패 시 안전한 우회 경로 사용, 실제 검증, 문제·교훈 Base 환류
source_incident_run: 33041116377
baseline_main: b146e939a7ed4019fe85ce5135b29a28c5d7b98f
incremental_cost: 0
```

## 문제

Base main의 `Validate Game Project Operating System` 전체 검증에서 Windows publication smoke가 pinned LibreOffice MSI 다운로드 도중 두 번 연속 실패했다.

```text
attempt 1: Received an unexpected EOF or 0 bytes from the transport stream.
attempt 2: An existing connection was forcibly closed by the remote host.
```

같은 run에서 다음은 모두 PASS였다.

```text
docs-validation
core-regression
ubuntu-contract
publication-validation
Base v9 Operating Contracts
```

따라서 제품·계약 회귀가 아니라 외부 transport의 일시적/반복 가능 실패로 분류한다.

## 선택지 비교

| 안 | 장점 | 실패 | 판정 |
|---|---|---|---|
| 동일 `Invoke-WebRequest` 무한 재실행 | 변경 없음 | 지연·불확실성·완료 불가 | REJECT |
| Windows smoke 또는 hash 검사 제거 | 즉시 green | 검증/공급망 약화 | REJECT |
| floating mirror/latest 사용 | 우회 가능 | provenance·identity drift | REJECT |
| bounded retry + 같은 official URI의 `curl.exe` fallback + SHA 검증 | evidence와 pin 유지, zero-cost | workflow helper 필요 | ADOPT |

## 승인 구현

- `Invoke-VerifiedDownload` helper를 Windows dependency install step 안에 둔다.
- primary: PowerShell `Invoke-WebRequest`.
- 각 transport route는 bounded retry와 partial-file cleanup을 사용한다.
- fallback: runner에 포함된 `curl.exe`의 `--fail --location --retry --retry-all-errors`.
- 같은 official URI, pinned version, expected SHA-256을 유지한다.
- 다운로드가 끝난 뒤에만 hash를 검증하며 mismatch는 fail-closed한다.
- LibreOffice와 Poppler가 같은 helper를 사용한다.
- retry/fallback이 모두 실패하면 `TRANSPORT_RETRY_EXHAUSTED`로 실패한다.

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
- Windows platform smoke actual PASS.
- required `ci-gate` PASS.
- safe squash merge and post-merge full workflow readback.
- 최소 5회 전체 적대적 검토.

## 롤백

구현 squash commit을 revert해 이전 single-route download step으로 복원한다. pinned versions, hashes, product code, project canons and release artifacts remain unchanged.
