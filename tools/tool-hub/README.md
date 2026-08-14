# Base Tool Hub

`Base Tool Hub`는 검토된 사용자용 localhost 도구를 프로젝트 ID에 묶어 실행하는 얇은 진입점입니다. 도구 기능을 한 앱에 합치지 않으며, 브라우저가 명령어·환경 변수·인터프리터·출력 경로를 만들 수 없습니다.

## 현재 단일 Hub 세로 단면

PR #328/#329에서 병합된 Tool Hub·QA Evidence Studio·Expression/Sprite import baseline을 흡수한 `tools/tool-hub/` 하나가 유일한 사용자 진입점입니다. 별도 Tool Radar runtime, 두 번째 Hub, marketplace, iframe은 없습니다.

- 세 도구를 `tools/TOOL_REGISTRY.json`에서 조회합니다.
- `PROJECT_BASE_ADAPTER.json` v2의 정확한 `project.project_id`로 프로젝트를 연결합니다.
- 로컬 절대 경로는 기기 로컬 locator에만 저장하며 catalog API에는 노출하지 않습니다.
- `QA Evidence Studio`, `Expression Studio`, `Sprite Animation Studio`를 고정 typed adapter와 독립 `(tool_id, project_id)` child로 실행합니다.
- Hub가 시작한 child가 반환한 authenticated `http://127.0.0.1:<port>` URL만 새 탭으로 엽니다.
- Linux에서는 `127.0.0.1:47640` 소유권 endpoint를 한 Hub만 점유하며, 비정상 종료 시 OS가 이를 회수합니다.
- 두 visual Studio는 항상 `subscription_handoff_import`로 시작합니다. UI의 `INCLUDED_OR_LOCAL_HANDOFF`와 `provider_call_made=false`는 가져오기 경로의 비용 상태이며 AI 생성 증거가 아닙니다.
- `ROUTING_REGISTERED`는 canonical Figma route 등록, `ANCHOR_EVIDENCE_MISSING`은 프로젝트 소유 anchor 증거 부재, `BLOCKED_UNVERIFIED`는 실행 증거 상한을 뜻합니다. 어느 상태도 Figma upload나 live node 존재를 증명하지 않습니다.

## 로컬 신뢰 경계

이 도구는 개발자 개인 PC에서 실행하는 localhost 작업 도구입니다. **동일 OS 사용자 계정과 기기 관리자는 신뢰 대상**입니다. 현재 구현은 브라우저·프로젝트 입력·경로 교체·설정 drift, 잘못된 registry/adapter 연결, 다른 프로젝트로의 출력 이탈을 차단하고 실행 직전 reviewed runtime의 변경을 탐지합니다.

같은 OS 계정으로 이미 임의 코드를 실행할 수 있는 악성 프로세스까지 완전히 격리한다고 주장하지 않습니다. 그 공격자는 Tool Hub뿐 아니라 같은 계정의 파일·프로세스·메모리에도 접근할 수 있기 때문입니다. 이 수준의 방어에는 **별도 OS 계정·컨테이너·서명된 읽기 전용 runtime**이 필요하며 현재 상태는 `HARDENED_RUNTIME_DEFERRED`입니다. 현행 runtime hash와 descriptor binding은 승인되지 않은 입력과 우발적 drift를 막는 방어 계층이지, 동일 계정 공격자에 대한 sandbox 증거가 아닙니다.

## 2026-08-13 실행 증거

Linux smoke에서 공백이 있는 두 임시 Git 프로젝트 fixture를 각각 v2 adapter, canonical Base Figma route, committed project-owned anchor registry에 결합했습니다. 두 Expression child와 두 Sprite child는 네 고유 PID·loopback port와 정확한 tool/project identity를 보고했습니다. Expression 후보 2개 import/export, Sprite action frame 4개 import/export, Sprite `effect_stages` frame 4개 import/export가 모두 local vault에서 완료됐고 모든 packet은 `subscription_handoff_import`, `INCLUDED_OR_LOCAL_HANDOFF`, `provider_call_made=false`였습니다. run ID와 출력은 각 프로젝트 안에만 존재했습니다.

기존 QA API vertical slice도 별도로 재실행해 session → visual/UX ready → developer PC results → image evidence → `QA_EVIDENCE_PACKET.json` 흐름과 Android `DEFERRED_NOT_CONNECTED` 상태를 확인했습니다. 이는 자동 테스트 fixture 증거이며 실제 특정 게임의 사람 검토를 대신하지 않습니다.

## Windows PowerShell 실행

Base 루트에서:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e '.\tools\qa-evidence-studio[dev]' -e '.\tools\expression-studio[dev]' -e '.\tools\sprite-animation-studio[dev]' -e '.\tools\tool-hub[dev]'

$projectConfig = Join-Path $env:LOCALAPPDATA 'BaseToolHub\projects.json'
.\.venv\Scripts\python -m tool_hub.app `
  --base-root (Get-Location) `
  --project-config $projectConfig `
  --port 8764
```

브라우저에서 `http://127.0.0.1:8764`를 엽니다.

연결할 프로젝트는 Git 루트, v2 adapter, gitignored Asset Vault를 모두 갖춰야 합니다. visual Studio에는 canonical Base Figma route와 committed `docs/APPROVED_VISUAL_ANCHORS.json`도 필요합니다. 위 Windows 명령은 실행 경로 안내이며 실제 Windows child process-tree·공백 경로 smoke 통과 증거가 아닙니다.

## 현재 검증되지 않은 것

- Windows child process-tree ownership과 두 프로젝트·네 child 공백 경로 smoke
- Android 기기 연결과 테스트
- live Figma connector 배치·upload·node 존재
- paid OpenAI 또는 pinned sprite provider 호출과 실제 AI 생성 품질·비용
- 특정 게임의 사람 검토 이미지·UX 품질
- 동일 OS 계정의 악성 프로세스를 격리하는 hardened runtime

이 항목은 현재 `BLOCKED_UNVERIFIED`, `NOT_RUN` 또는 명시적 `DEFERRED`이며, Linux/import 테스트 통과로 대체하지 않습니다. 다음 독립 vertical slice 후보는 `Balance & Scenario Lab`이지만 현재 Hub에 placeholder/card/runtime은 추가하지 않았습니다.
