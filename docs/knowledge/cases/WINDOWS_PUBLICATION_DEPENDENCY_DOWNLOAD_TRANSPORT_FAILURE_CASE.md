# Windows publication dependency download transport failure — Case

```text
WINDOWS_PUBLICATION_DEPENDENCY_DOWNLOAD_TRANSPORT_FAILURE
NO_TEST_OR_HASH_WEAKENING
BOUNDED_RETRY_AND_VERIFIED_FALLBACK
TDF_MIRROR_SOURCE_FALLBACK_WITH_SAME_PINNED_HASH
```

## 1. 증상

Base main `b146e939a7ed4019fe85ce5135b29a28c5d7b98f`의 full post-merge workflow run `33041116377`에서 `platform-smoke-windows`가 pinned LibreOffice MSI 다운로드 단계에서 실패했다.

첫 실행:

```text
Received an unexpected EOF or 0 bytes from the transport stream.
```

failed-job rerun:

```text
Unable to read data from the transport connection:
An existing connection was forcibly closed by the remote host.
```

첫 bounded transport retry 구현 run `33042041600`에서는 같은 endpoint가 `HTTP 429`를 반환했다. 이는 `Invoke-WebRequest`와 `curl.exe`를 같은 URL에 적용하는 것만으로는 source-level rate limit을 복구할 수 없다는 추가 evidence다.

동일 run 계보의 결과:

```text
core-regression: PASS before new focused contract / focused mismatch found after contract addition
docs-validation: PASS
ubuntu-contract: PASS
publication-validation: PASS
platform-smoke-windows: FAIL before publication tests
ci-gate: FAIL because required Windows job failed
```

## 2. 원인 판정

- 최초 workflow가 `Invoke-WebRequest` 단일 transport invocation에 의존했다.
- partial transfer cleanup, bounded retry, alternate client fallback이 없었다.
- transport retry를 추가한 뒤에는 원본 endpoint 자체가 HTTP 429를 반환했다.
- exact version·official mirror-network file·SHA-256 자체가 틀렸다는 evidence는 없었다.
- 따라서 product/test regression이 아니라 external transport와 source endpoint resilience gap으로 분류했다.

## 3. 거부한 우회

```text
Windows job 삭제/skip
hash verification 제거
다른 SHA의 GREEN 재사용
floating latest 또는 검증되지 않은 mirror
무제한 재실행
ci-gate/ruleset bypass
```

위 방식은 검증 수준·공급망 identity 또는 완료 신뢰도를 낮추므로 거부했다.

## 4. 해결 패턴

```text
verified direct TDF mirror source
→ partial output cleanup
→ Invoke-WebRequest bounded retry
→ SHA-256 verification
→ 실패 시 curl.exe fallback with bounded retry
→ SHA-256 verification
→ source transport exhausted?
→ original TDF download endpoint fallback
→ same bounded transport routes
→ same SHA-256 verification
→ install/extract
→ actual Windows smoke
```

helper contract:

```text
function Invoke-VerifiedDownload
$maxAttempts = 3
Start-Sleep -Seconds <bounded backoff>
curl.exe --fail --location --retry 3 --retry-all-errors
DOWNLOAD_SHA256_MISMATCH
TRANSPORT_RETRY_EXHAUSTED
```

LibreOffice source routes:

```text
primary: https://mirror.clarkson.edu/tdf/libreoffice/stable/<version>/...
fallback: https://download.documentfoundation.org/libreoffice/stable/<version>/...
identity: same pinned SHA-256
```

The Document Foundation의 사용자 안내는 다운로드 문제 시 해당 파일의 mirror list에서 다른 server를 고르도록 설명한다. Clarkson은 TDF LibreOffice stable tree를 제공하며 정확한 `26.2.3` 디렉터리와 MSI가 실제로 관찰됐다.

LibreOffice와 Poppler는 같은 verified transport helper를 사용한다. source fallback은 LibreOffice의 실제 429 evidence가 있는 경우에만 추가했고, Poppler에 불필요한 mirror policy를 확장하지 않았다.

## 5. 왜 이 방식인가

- runner에 이미 포함된 transport client를 재사용해 incremental cost가 0이다.
- official TDF mirror network와 원본 endpoint 사이에서 source route를 전환한다.
- exact version과 pinned hash를 유지한다.
- PowerShell/.NET transport와 curl의 다른 network stack을 fallback으로 사용할 수 있다.
- 실패를 숨기지 않고 retry exhaustion 또는 hash mismatch로 fail-closed한다.
- hash mismatch는 다른 source로 조용히 우회하지 않고 즉시 실패한다.
- same-command rerun을 반복하는 대신 재현 가능한 workflow guard가 된다.

## 6. Evidence ceiling

```text
workflow contract present
!= remote download succeeds
!= package installs
!= Windows publication tests pass
!= ci-gate pass
```

최종 완료에는 exact-head Windows job과 required `ci-gate`의 실제 성공이 필요하다.

## 7. 재사용 조건

적용:

- 공식 binary/archive를 CI에서 직접 받아야 함.
- transient connection reset/EOF/429가 material blocker임.
- expected SHA 또는 signature를 알고 있음.
- official project mirror network 또는 source-authorized fallback이 있음.
- runner에 evidence-equivalent fallback client가 있음.

비적용:

- URL/version/hash가 실제로 잘못됨.
- license/rights/source authority가 불확실함.
- 임의 third-party mirror만 존재함.
- retry가 비용·rate limit·보안 정책을 위반함.
- 다운로드가 없어도 되는 불필요한 job임.

## 8. 검색 trigger

```text
unexpected EOF
0 bytes from transport stream
connection forcibly closed by remote host
HTTP 429 download
Invoke-WebRequest CI download
Windows publication dependency
TDF mirror
pinned binary retry hash verification
```
