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

이 도구는 개발자 개인 PC에서 실행하는 localhost 작업 도구입니다. **동일 OS 사용자 계정과 기기 관리자는 신뢰 대상**입니다. 현재 구현은 브라우저·프로젝트 입력, 잘못된 registry/adapter 연결, 다른 프로젝트로의 출력 이탈을 차단하고 최종 launch 검사 시점까지의 경로·설정 drift를 탐지합니다.

같은 OS 계정으로 이미 임의 코드를 실행할 수 있는 악성 프로세스까지 완전히 격리한다고 주장하지 않습니다. 그 공격자는 Tool Hub뿐 아니라 같은 계정의 파일·프로세스·메모리에도 접근할 수 있기 때문입니다. 또한 최종 검사와 child import 사이에 신뢰 사용자가 Base·Studio runtime을 동시에 편집하는 동작은 지원하지 않으므로, 도구 실행 중 해당 파일을 저장하지 않습니다. 이 수준까지 원자적으로 격리하려면 **별도 OS 계정·컨테이너·서명된 읽기 전용 runtime**이 필요하며 현재 상태는 `HARDENED_RUNTIME_DEFERRED`입니다. 현행 runtime hash와 descriptor binding은 승인되지 않은 입력과 launch 전 drift를 막는 방어 계층이지, 동일 계정의 동시 변경에 대한 sandbox 증거가 아닙니다.

## 2026-08-13 실행 증거

Linux smoke에서 공백이 있는 두 임시 Git 프로젝트 fixture를 각각 v2 adapter, canonical Base Figma route, committed project-owned anchor registry에 결합했습니다. 두 Expression child와 두 Sprite child는 네 고유 PID·loopback port와 정확한 tool/project identity를 보고했습니다. Expression 후보 2개 import/export, Sprite action frame 4개 import/export, Sprite `effect_stages` frame 4개 import/export가 모두 local vault에서 완료됐고 모든 packet은 `subscription_handoff_import`, `INCLUDED_OR_LOCAL_HANDOFF`, `provider_call_made=false`였습니다. run ID와 출력은 각 프로젝트 안에만 존재했습니다.

기존 QA API vertical slice도 별도로 재실행해 session → visual/UX ready → developer PC results → image evidence → `QA_EVIDENCE_PACKET.json` 흐름과 Android `DEFERRED_NOT_CONNECTED` 상태를 확인했습니다. 이는 자동 테스트 fixture 증거이며 실제 특정 게임의 사람 검토를 대신하지 않습니다.

## 2026-08-16 통합 상태

PR #428이 `main`에 squash merge되어 Character/Outfit/Scene 편집, ChatGPT Pro same-run handoff, exact Figma tool-route delivery, Windows Job Object child ownership을 하나의 current-main 경로로 통합했습니다.

- Windows child는 더 이상 `BLOCKED_PLATFORM` 구현 상태가 아닙니다. Tool Hub는 suspended root process를 만든 뒤 unnamed Windows Job Object에 연결하고, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`와 실제 Studio runtime PID의 Job membership을 검증합니다.
- PR #428 exact head와 merge 후 `main`에서 Linux supervisor regression 및 Windows real process-tree / reviewed launch / multi-project smoke가 통과했습니다.
- Expression Studio는 server-issued same-run handoff를 만들고, `CHATGPT_INCLUDED` PNG를 동일 run으로 다시 가져온 뒤 검토/내보내기/전달 경로를 이어갑니다.
- Figma delivery는 project/tool별 canonical route를 검증하며 잘못된 project/route/hash/node는 fail closed합니다.
- 위 CI/코드 readback은 **사용자 개발자 PC에서 실제 Tool Hub와 Studio를 실행했다는 증거가 아닙니다.** 실제 PC 실행, 실제 ChatGPT Pro 픽셀, live Figma Desktop/plugin mutation/readback, 실제 게임 소비는 별도 IRG로 남습니다.

## Windows 최초 전환과 이후 실행

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

브라우저에서 `http://127.0.0.1:8764`를 연 뒤 `바탕화면 실행 아이콘 설치/복구`를 한 번 누릅니다. 설치가 성공하면 바탕화면에 `Base Tool Hub.lnk`가 생깁니다. 설치기는 외부 PowerShell을 띄우지 않고 Windows Shell Link API를 직접 사용하며, 바로가기는 검증된 `pythonw.exe`와 private launcher를 직접 가리켜 `.pyw` 연결 프로그램에도 의존하지 않습니다. 이후 정상 사용은 PowerShell을 열지 않고 이 아이콘을 두 번 클릭하면 됩니다. 같은 Hub가 이미 실행 중이면 새 프로세스를 만들지 않고 브라우저만 다시 엽니다. 정상 종료는 **마지막 Tool Hub 브라우저 탭을 닫는 것만으로 충분**하며, 약 2초의 새로고침 보호 유예 뒤 Hub와 Hub가 시작한 Studio child가 함께 종료됩니다. 여러 Tool Hub 탭 중 하나만 닫거나 페이지를 새로고침하면 다른/대체 browser lease가 Hub를 유지합니다. 화면의 `Tool Hub 종료`는 기다리지 않고 즉시 종료해야 할 때 사용하는 fallback입니다.

브라우저나 renderer가 비정상 종료되어 `pagehide` 신호가 사라진 경우에는 정상 백그라운드 탭을 잘못 죽이지 않기 위해 보수적인 heartbeat stale timeout(약 5분)을 기다린 뒤 정리합니다. 이 자동 종료 경로는 Git Fetch/Pull/Reset/Clean/Checkout을 실행하지 않고, Hub가 소유하지 않은 Figma Desktop/plugin·Git·Python 프로세스를 종료하지 않습니다.

구현 기준은 Microsoft의 [Windows Shell Links](https://learn.microsoft.com/en-us/windows/win32/shell/links) 계약입니다.

이전 버전의 바탕화면 `Base Tool Hub.pyw`가 현재 검토된 launcher와 정확히 일치하면 설치 과정에서 새 `.lnk` 게시 후 제거합니다. 내용이 다르거나 비정상 파일이면 임의로 지우지 않고 `복구 필요`로 차단합니다.

이 PowerShell 블록은 최초 설치 또는 Base/가상환경 변경 뒤 복구에만 필요합니다. 바탕화면 실행기는 Git pull, pip install, branch 변경, 프로젝트 파일 수정, 다른 프로세스 종료를 수행하지 않습니다. 8764 포트가 다른 프로그램이면 이를 죽이지 않고 `PORT_IDENTITY_CONFLICT`로 차단합니다.

실행 중 진단은 `%LOCALAPPDATA%\BaseToolHub\logs`에 남으며 `tool-hub.log` 1개와 최대 2개의 1 MiB 회전본으로 제한됩니다. 강제 종료나 재부팅 뒤에는 OS가 실행기 잠금을 자동 회수하므로 남아 있는 `.launcher.lock` 파일 때문에 이후 더블클릭이 영구 차단되지 않습니다. 바탕화면 바로가기나 검토된 Python/Git/Base bytes가 바뀌면 `설치 복구 필요` 또는 `업데이트 필요`로 표시하고 자동으로 다른 실행 파일을 선택하지 않습니다.

`등록 가능한 프로젝트`에서 게임 이름이나 카드의 버튼을 누릅니다. Tool Hub는 저장된 위치, `%USERPROFILE%\Documents\GitHub\<정확한 저장소 이름>`, `%USERPROFILE%\source\repos\<정확한 저장소 이름>`만 확인합니다. 발견되지 않으면 Base에 검토·커밋된 정확한 GitHub URL을 `%USERPROFILE%\Documents\GitHub`에 임시 staging으로 clone하고, origin·Git 루트·v2 Adapter·project ID·Asset Vault ignore를 검증한 뒤 게시합니다. 사용자가 Git 폴더나 GitHub/Figma URL을 입력할 필요가 없습니다.

기존 폴더는 덮어쓰거나 삭제하지 않습니다. 기존 repository에는 pull, fetch, reset, clean, checkout, migration을 자동 수행하지 않습니다. `PATH_OCCUPIED`, `IDENTITY_MISMATCH`, `PROJECT_SETUP_REQUIRED`, `AUTHENTICATION_REQUIRED`가 표시되면 기존 파일은 그대로 보존되며 GitHub Desktop 또는 프로젝트 GPT의 정식 변경 절차로 해결합니다. 로컬 절대 경로와 Git 진단은 브라우저 catalog에 반환하지 않습니다.

연결할 프로젝트는 정확한 Git 루트, v2 adapter, gitignored Asset Vault를 모두 갖춰야 합니다. visual Studio에는 canonical Base Figma route와 committed `docs/APPROVED_VISUAL_ANCHORS.json`도 필요합니다. 프로젝트 등록은 도구 child 실행이나 Figma 배치 증거가 아닙니다.

Windows에서는 Hub 프로세스·검토된 도구 카탈로그와 portable v2 프로젝트 등록 경로뿐 아니라, reviewed visual Studio child의 native Job Object 소유권과 project/tool identity 검증 경로도 제공합니다. GitHub-hosted Windows 검증에서는 real child process tree, reviewed launch, 다중 프로젝트 child 격리를 확인했습니다. 다만 **사용자 개발자 PC에서 같은 경로를 실제로 실행한 결과는 아직 `NOT_RUN`**이며, 그 전에는 개발자-PC IRG를 PASS로 올리지 않습니다.

바탕화면 아이콘 설치와 Hub 재실행은 Tool Hub 자체의 Windows orchestration 증거입니다. Windows child CI 증거는 process ownership/runtime 격리 계약을 검증하지만, live Figma 배치, 실제 ChatGPT Pro 생성 품질 또는 특정 게임의 이미지·UX 검토를 통과시킨다는 뜻은 아닙니다.

## 실제 PC IRG 시작 순서

1. 바탕화면에 `Base Tool Hub.lnk`가 이미 있으면 PowerShell을 열지 말고 더블클릭합니다.
2. 바로가기가 없거나 `설치 복구 필요`가 표시될 때만 위 최초 전환 블록을 한 번 사용하고 `바탕화면 실행 아이콘 설치/복구`를 누릅니다.
3. Hub에서 실제 프로젝트 하나를 선택하고 Character/Expression Studio를 실행합니다.
4. approved anchor와 변경 요청을 지정해 `GPT Pro로 생성` handoff를 준비합니다.
5. 일반 ChatGPT Pro 화면에서 실제 이미지를 생성하고 반환된 PNG를 **같은 run**으로 가져옵니다.
6. 후보를 검토·선택한 뒤 `확정 및 전달`을 실행합니다.
7. Figma Bridge를 실제 프로젝트 파일과 pairing하고 상태를 새로고침해 exact `Expression Runs` route의 verified receipt를 확인합니다.
8. 그 다음 Sprite에서 실제 `pose_sequence` 1개와 `effect_stages` 1개를 같은 subscription handoff 경로로 검증합니다.
9. 마지막으로 실제 프로젝트/Godot 작업 경로가 승인된 자산을 소비하는지 확인합니다.

각 단계는 실제 관측 전까지 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`입니다. fixture/CI/코드 존재를 사용자 PC·Figma·시각 품질·게임 소비 PASS로 대체하지 않습니다.

## 현재 검증되지 않은 것

- 사용자 개발자 PC에서의 실제 Tool Hub 실행, reviewed Studio child launch, 두 실제 프로젝트 동시 실행/격리
- 실제 ChatGPT Pro 생성 이미지의 시각 품질과 Character/Expression identity 보존 결과
- 실제 `pose_sequence`와 `effect_stages` subscription handoff 샘플 품질
- live Figma Desktop/plugin mutation, exact node readback, same-SHA verified receipt
- 특정 게임/Godot의 실제 승인 자산 소비
- Android 기기 연결과 테스트
- 동일 OS 계정의 악성 프로세스를 격리하는 hardened runtime

이 항목은 현재 `BLOCKED_UNVERIFIED`, `NOT_RUN` 또는 명시적 `DEFERRED`이며, GitHub-hosted CI나 fixture/import 테스트 통과로 대체하지 않습니다. 다음 독립 vertical slice 후보는 `Balance & Scenario Lab`이지만 현재 Hub에 placeholder/card/runtime은 추가하지 않았습니다.
