# Base Tool Hub

`Base Tool Hub`는 검토된 사용자용 localhost 도구를 프로젝트 ID에 묶어 실행하는 얇은 진입점입니다. 도구 기능을 한 앱에 합치지 않으며, 브라우저가 명령어·환경 변수·인터프리터·출력 경로를 만들 수 없습니다.

## 현재 세로 단면

- 세 도구를 `tools/TOOL_REGISTRY.json`에서 조회합니다.
- `PROJECT_BASE_ADAPTER.json` v2의 정확한 `project.project_id`로 프로젝트를 연결합니다.
- 로컬 절대 경로는 기기 로컬 locator에만 저장하며 catalog API에는 노출하지 않습니다.
- `QA Evidence Studio`만 typed adapter로 실제 실행합니다.
- Expression Studio와 Sprite Animation Studio는 등록 상태를 보여 주지만, Hub 실행 어댑터는 후속 단계입니다. 두 도구는 기존 독립 실행법을 계속 사용합니다.

## Windows PowerShell 실행

Base 루트에서:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e '.\tools\qa-evidence-studio[dev]' -e '.\tools\tool-hub[dev]'

$projectConfig = Join-Path $env:LOCALAPPDATA 'BaseToolHub\projects.json'
.\.venv\Scripts\python -m tool_hub.app `
  --base-root (Get-Location) `
  --project-config $projectConfig `
  --port 8764
```

브라우저에서 `http://127.0.0.1:8764`를 엽니다.

연결할 프로젝트는 Git 루트, v2 adapter, gitignored Asset Vault를 모두 갖춰야 합니다. 공백이 들어간 Windows 경로도 하나의 typed 인자로 전달합니다.

## 현재 검증되지 않은 것

- 실제 Windows에서 여러 프로젝트를 동시에 장시간 사용하는 운영 검증
- Hub에서 Expression/Sprite Studio 실행
- Android 기기 연결과 테스트
- 특정 게임의 이미지·UX 품질

이 항목은 현재 `NOT_RUN` 또는 명시적 `DEFERRED`이며, Hub나 QA Studio의 테스트 통과로 대체하지 않습니다.
