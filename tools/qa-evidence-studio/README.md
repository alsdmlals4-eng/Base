# QA Evidence Studio

`QA Evidence Studio`는 이미지와 UX 요소가 실제 PC 빌드에 배치된 뒤, 개발자 본인이 체크리스트·화면 증거·판정을 같은 Git 커밋에 묶는 로컬 도구입니다. 외부 AI나 유료 API를 호출하지 않습니다.

## 현재 적용 범위

- 검토 플랫폼: PC
- 검토자: `DEVELOPER_OWNER` 1명
- 외부 테스터: 현재 없음. Phase 1 완료 조건이 아님
- Android: `DEFERRED_NOT_CONNECTED`
- Android 연결 Gate: PC 기획안·이미지·UX 구현 종료 후, 출시 준비 직전
- 실제 검증 시작 Gate: 이미지와 UX 배치에 대한 개발자 확인 이후

자동화된 테스트는 도구의 상태·보안·증거 계약을 확인합니다. 특정 게임의 이미지 품질, UX 품질, Android 동작 또는 출시 준비 완료를 대신 증명하지 않습니다.

## Windows PowerShell 실행

Base 루트에서 최초 한 번:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e '.\tools\qa-evidence-studio[dev]'
```

대상 프로젝트에는 다음이 필요합니다.

1. 프로젝트 루트가 Git 작업트리 루트여야 합니다.
2. `.asset-vault/library/` 폴더가 있어야 합니다.
3. 프로젝트 `.gitignore`가 `.asset-vault/`를 제외해야 합니다.

```powershell
.\.venv\Scripts\python -m qa_evidence_studio.app `
  --project-root 'C:\Users\user\Documents\GitHub\MyProject' `
  --project-id 'my-project' `
  --port 8767
```

브라우저에서 `http://127.0.0.1:8767`을 엽니다.

## 사용 순서

1. 검토할 40자리 Git 커밋과 체크 항목으로 세션을 만듭니다.
2. 이미지와 UX 요소를 실제 PC 빌드에 배치합니다.
3. 배치 완료 확인 문구를 입력해 PC 검토를 엽니다.
4. 각 항목을 `PASS / FAIL / BLOCKED / NOT_RUN`으로 기록합니다.
5. PNG/JPEG/WebP 화면 증거를 추가합니다. 파일당 최대 25 MiB입니다.
6. 모든 필수 항목과 이미지 증거가 있을 때 증거 패킷을 확정합니다.

결과는 다음 로컬 전용 경로에 저장됩니다.

```text
<project>/.asset-vault/library/generated/qa-evidence-studio/<session-id>/
```

`FAIL`이 하나라도 있으면 전체 PC 결과는 `FAIL`, `BLOCKED`만 있으면 `BLOCKED`입니다. Android 상태는 PC 결과와 무관하게 계속 `DEFERRED_NOT_CONNECTED`로 남습니다.

## 보안과 롤백

- loopback Host와 정확한 Origin만 허용합니다.
- 변경 요청은 브라우저 session cookie와 CSRF token을 모두 요구합니다.
- 프로젝트 밖 출력, tracked Asset Vault, symlink/reparse 경유를 차단합니다.
- 완료 세션은 변경할 수 없습니다.
- 롤백은 Hub/Studio 프로세스를 종료한 뒤 해당 로컬 세션 폴더를 보존 또는 사용자가 직접 제거하는 것입니다. 프로젝트 정본·런타임 자산은 자동 수정되지 않습니다.
