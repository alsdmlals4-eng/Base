# Godot 에이전트 자동화·MCP 도입 작업 구조 설계

- 작성일: 2026-08-05
- 기준 저장소: `alsdmlals4-eng/Base`
- 기준 main: `0b7c94f38d959efc0fc9442274c60b2e268a3c97` (`Base v9.4.3`)
- 상태: `APPROVED_DIRECTION_SPEC_REVIEW_PENDING`
- 사용자 승인: 2026-08-05 권장안 A 승인
- 이번 문서 범위: Base 공용 작업 구조·Skill 경계·검증 계약 설계
- 범위 밖: 실제 Godot 프로젝트 설치, HiGodot/Godot AI PoC, 자체 MCP 서버 구현, 프로젝트 코드·Scene·Resource 변경

## 1. 목표

Unity의 현행 `CLI → Pipeline → Editor/개발 Player` 구조에서 재사용 가능한 원리를 추출하고, Godot에서는 기존 공식 CLI·Editor 확장점과 검증 가능한 MCP 도구를 우선 활용해 다음 폐쇄 루프를 Base 공용 작업 구조로 만든다.

```text
프로젝트·엔진·보호 경계 조사
→ 공식 Godot 기능과 기존 MCP 후보 평가
→ ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM 판정
→ 격리된 PoC 설계
→ Editor·실행 게임 관찰/변경/검증
→ 보안·권한·Undo·롤백·제거 검증
→ 프로젝트별 도입 결정
→ 반복 근거가 쌓일 때만 Base Skill 구조 승격
```

목표는 “Godot MCP를 무조건 새로 만든다”가 아니다. AI 에이전트가 Godot 프로젝트를 안전하게 관찰하고, 승인된 범위만 변경하고, 실제 Editor·게임 결과를 검증할 수 있는 최소·교체 가능한 실행 계층을 정의하는 것이다.

## 2. 조사 기준과 확인된 구조

### 2.1 Unity에서 추출할 원리

Unity 공식 자료에서 확인되는 핵심 구조는 다음과 같다.

```text
AI Agent / Script / CI
→ Unity CLI 또는 CLI MCP mode
→ com.unity.pipeline
→ localhost 실행 계층
→ 실행 중인 Unity Editor 또는 개발용 Player
```

재사용할 원리는 제품명이나 C# API가 아니라 다음 여섯 가지다.

1. **터미널 우선 제어면**: 구조화된 출력과 예측 가능한 종료 코드.
2. **얇은 엔진 브리지**: Editor와 실행 중인 개발 Player에 연결되는 로컬 계층.
3. **자기 기술형 명령 표면**: 사용 가능한 명령을 런타임에 검색할 수 있음.
4. **프로젝트 전용 확장**: 프로젝트가 자체 명령을 등록할 수 있음.
5. **관찰→행동→검증 루프**: 실행 결과를 에이전트가 다시 확인함.
6. **강력 기능의 별도 보안 게이트**: 임의 코드 실행·런타임 변경은 토큰·개발 환경·로컬 범위로 제한.

Unity CLI와 Pipeline은 2026-08-05 기준 실험 단계이므로, Unity의 명령명·패키지 상태를 Godot의 안정 계약으로 복사하지 않는다.

공식 출처:

- https://unity.com/blog/meet-the-unity-cli
- https://docs.unity.com/en-us/unity-cli/unity-cli
- https://discussions.unity.com/t/announcing-the-unity-cli-a-new-way-to-connect-your-tools-and-agents/1731104

### 2.2 Godot 공식 기반

Godot의 공식 기능만으로도 다음 기반을 구성할 수 있다.

- CLI·headless 실행, import, export, 스크립트 실행, 프로젝트·Scene 실행
- GDScript LSP·DAP와 Editor debug server
- `EditorPlugin`을 통한 Editor 확장
- `EditorDebuggerPlugin`과 `EditorDebuggerSession`을 통한 실행 세션 연결
- `EngineDebugger` 계층을 통한 게임 측 디버거 메시지
- SceneTree·Resource·EditorInterface를 통한 Editor 상태 접근

이 기능들은 MCP 서버 자체를 제공하지는 않지만, MCP나 다른 에이전트 프로토콜을 연결할 엔진 측 브리지의 공식 기반이 된다.

공식 출처:

- https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html
- https://docs.godotengine.org/en/4.6/classes/class_editorplugin.html
- https://docs.godotengine.org/en/4.6/classes/class_editordebuggerplugin.html
- https://docs.godotengine.org/en/4.6/classes/class_enginedebugger.html

### 2.3 기존 Godot MCP 후보

`hi-godot/godot-ai`는 현재 다음 구조를 공개한다.

```text
MCP Client
→ local HTTP MCP server
→ Python / FastMCP
→ WebSocket
→ Godot EditorPlugin
→ EditorInterface·SceneTree·실행 게임 보조 계층
```

공개 저장소는 Scene·Node·Script·Resource·UI·Animation·Material·Project 실행·로그·스크린샷·성능·실행 게임 입력/상태 등 넓은 작업 표면과 Codex 연결 방법을 제공한다. 따라서 자체 구현 전에 우선 평가할 실질 후보이다.

단, 공개 기능 설명만으로 프로젝트 채택을 확정하지 않는다. 정확한 Godot 버전, 설치 버전, 텔레메트리, 로컬 포트, Python/uv 종속성, 파일 쓰기 범위, 임의 실행 능력, Undo, 재연결, Windows 잠금 문제, 제거 가능성을 실제 PoC에서 확인해야 한다.

후보 출처:

- https://github.com/hi-godot/godot-ai

## 3. 범위와 비범위

### 3.1 이번 Base 개선 범위

- Godot 에이전트 자동화·MCP 도입 요청을 기존 Skill 구조에 라우팅하는 계약
- Unity 구조에서 추출한 엔진 중립적 설계 원리
- Godot 공식 기능·기존 MCP·직접 구현의 비교 기준
- 프로젝트 어댑터 필수 필드
- 보안·권한·Undo·관찰·검증·제거 계약
- 격리 PoC의 완료 기준과 중단 조건
- Base 행동 평가·계약 테스트 설계

### 3.2 이번 단계에서 하지 않는 것

- 새 광역 `godot-mcp` Skill 생성
- Base `skills/SKILL_REGISTRY.json`의 즉시 변경
- HiGodot/Godot AI 설치 또는 자동 승인
- 특정 프로젝트에 Addon 복사
- 자체 FastMCP·WebSocket·EditorPlugin 구현
- `eval` 또는 임의 GDScript/C# 실행을 기본 허용
- production build에 원격 제어 계층 포함
- 프로젝트 핵심 Scene·세이브·데이터 정본에서 첫 시험 수행

## 4. Skill 책임 경계

### 4.1 주 책임 Skill

새 독립 Skill을 만들지 않고 다음 기존 Skill을 주 책임으로 확장하는 안을 채택한다.

`evaluating-godot-assets-and-plugins-before-creation`

기존 Skill Mode 생명주기는 그대로 유지한다.

```text
frame-need → search → evaluate → trial-plan → adoption-decision → revalidate
```

Godot 에이전트 자동화 요청에는 다음 조건부 평가 프로필과 reference를 적용한다.

```text
agentic-editor-automation
```

이 프로필은 새 Skill Mode가 아니다. 기존 각 Skill Mode에서 필요한 입력·평가표·보안·검증을 강화하며 다음 요청을 책임진다.

- Godot MCP·에디터 자동화·AI 에이전트 제어 계층 평가
- 기존 도구 채택과 자체 구현 비교
- 로컬 서버·EditorPlugin·실행 게임 브리지의 보안·권한 평가
- 격리 PoC·도입·제거 계획

이 구조는 Skill Mode의 절차 의미를 보존하면서 특정 도구군의 전문 기준만 조건부로 로드한다.

### 4.2 보조 책임

- `managing-project-intake-and-work-contract`
  - 프로젝트·엔진·목표·승인 범위·완료 기준을 작업 계약으로 고정한다.
- `running-adversarial-review-and-refinement`
  - 과도한 권한, 임의 실행, 잘못된 채택, 누락된 소비자와 회귀를 공격한다.
- `reviewing-and-validating-project-changes`
  - 실제 설치·diff·Editor·게임 Runtime·테스트·롤백 증거를 판정한다.
- `diagnosing-game-engine-runtime-failures`
  - 도입 뒤 발생한 Editor·import·plugin·runtime 실패를 진단한다.
- `maintaining-project-context-and-handoff`
  - GPT 계획에서 Codex Plan/Build로 넘길 프로젝트별 PoC 패킷을 만든다.
- `evolving-project-discipline-skills`
  - 여러 프로젝트에서 독립 입력·산출물·검증 경계가 반복된 경우에만 새 Skill 승격 여부를 재검토한다.

### 4.3 새 Skill 분리 조건

아래 조건이 모두 반복적으로 확인되기 전에는 새 Skill을 만들지 않는다.

1. 일반 Godot 플러그인 평가와 다른 독립 입력이 있다.
2. 별도의 산출물·Quality Gate·테스트·승인 경계가 있다.
3. 최소 두 프로젝트 이상에서 같은 책임이 반복된다.
4. 기존 Skill Mode와 조건부 reference 프로필로는 행동 평가를 명확히 분리할 수 없다.
5. 실제 PoC 또는 Runtime 근거가 있다.

## 5. 제안 아키텍처

### 5.1 논리 계층

```text
[1] Agent Client
    Codex / Claude / Copilot / CI / local script

[2] Agent Protocol Adapter
    MCP HTTP/stdio 또는 CLI wrapper
    - 인증·세션·도구 발견
    - 구조화 입력·출력
    - timeout·cancel·error code

[3] Local Automation Service
    기존 도구의 Python server 또는 자체 최소 service
    - localhost bind
    - 명령 allowlist
    - path·schema validation
    - audit log

[4] Godot Editor Bridge
    EditorPlugin / EditorDebuggerPlugin
    - EditorInterface·SceneTree·Resource 접근
    - main-thread 실행
    - UndoRedo와 dirty-state 관리

[5] Development Runtime Bridge
    debug/development build에서만 활성
    - 실행 SceneTree 관찰
    - 로그·성능·입력·상태 확인
    - production export에는 미포함

[6] Verification and Recovery
    project validators / tests / screenshot / logs / diff / rollback
```

### 5.2 인터페이스 원칙

- MCP는 필수 구현이 아니라 에이전트 연결 어댑터다.
- 핵심 명령 계약은 MCP transport와 분리해 테스트 가능해야 한다.
- 읽기 작업과 쓰기 작업을 분리한다.
- 자주 쓰는 최소 읽기 명령만 기본 노출하고 나머지는 검색·도메인별 지연 로드를 허용한다.
- 프로젝트 전용 명령은 범용 임의 실행보다 명시적 schema와 제한된 기능을 우선한다.
- Scene·Resource 변경은 가능하면 Godot `UndoRedo`와 연결한다.
- 파일 쓰기는 프로젝트 루트와 승인된 경로 안에서만 허용한다.
- 실행 게임 제어는 개발·QA 빌드로 제한하고 production에는 포함하지 않는다.

## 6. 프로젝트 어댑터 계약

기존 Godot 자산 평가 어댑터에 다음 역할을 조건부 추가한다.

```yaml
engine_version:
engine_distribution:
project_root:
project_godot_path:
renderer:
script_runtime: GDScript | .NET | mixed
platforms:
editor_binary_path:
headless_binary_path:
addon_root:
protected_paths:
allowed_write_roots:
canonical_design_sources:
validators:
third_party_inventory:
license_record:

agent_automation:
  target: editor | development_player | both
  candidate_tool:
  candidate_version:
  candidate_source:
  transport: http | stdio | cli | websocket
  bind_address:
  ports:
  allowed_clients:
  auth_mode:
  command_allowlist:
  denied_capabilities:
  arbitrary_eval_default: false
  telemetry_policy:
  audit_log_path:
  timeout_seconds:
  concurrency_limit:
  undo_required:
  dirty_state_policy:
  reconnect_policy:
  generated_file_roots:
  uninstall_steps:
  rollback_reference:
```

필수 값이 없으면 채택 판정은 `UNVERIFIED` 또는 `TRIAL`을 넘지 못한다.

## 7. 도입 판정

### 7.1 기본 판정

현재 Base 수준 판정은 다음과 같다.

```text
HiGodot/Godot AI: TRIAL_CANDIDATE
자체 Godot MCP: DEFER_UNTIL_GAP_PROVEN
공식 Godot 기능 직접 활용: REQUIRED_BASELINE
```

### 7.2 ADOPT

다음 조건을 실제 프로젝트 PoC에서 충족하면 채택할 수 있다.

- 정확한 Godot 버전·스크립트 런타임·플랫폼에서 동작
- localhost와 인증·세션 정책이 확인됨
- 보호 경로 밖 쓰기가 차단됨
- 핵심 읽기·쓰기·실행·검증 작업이 완료 기준을 충족
- Undo 또는 명시적 롤백이 검증됨
- 텔레메트리·외부 전송이 프로젝트 정책과 일치
- 제거 뒤 프로젝트가 정상 import·실행됨
- 라이선스·버전 핀·업데이트 정책 기록

### 7.3 ADAPT

다음과 같은 제한된 wrapper가 필요하지만 도구 전체를 새로 만들 필요는 없을 때 사용한다.

- 프로젝트 전용 command allowlist
- 텔레메트리 기본 비활성화
- 도메인별 도구 노출 제한
- 경로·Scene·Resource schema 추가 검증
- 프로젝트 전용 validator 호출
- 기존 도구의 MCP 표면을 Base/Codex 작업 계약에 맞게 축소

### 7.4 TRIAL

아래 중 하나라도 미검증이면 격리 PoC에만 사용한다.

- 정확한 엔진 버전 호환성
- Windows 프로세스·uv·포트 안정성
- domain reload·plugin reload 뒤 재연결
- Undo·dirty state·Scene 저장 안정성
- 실행 게임 브리지의 개발 빌드 격리
- 텔레메트리와 외부 전송
- 동시 Editor 인스턴스 선택
- 파일 경로 탈출·명령 오용 방어

### 7.5 REJECT

- production build에 원격 제어가 기본 포함됨
- 비밀값·프로젝트 파일을 승인 없이 외부 전송함
- 프로젝트 루트 밖 쓰기 차단이 불가능함
- 라이선스가 프로젝트 사용·수정·배포와 충돌함
- 제거가 불가능하거나 핵심 데이터 형식을 잠금
- 실행한 검증 없이 “전체 Godot API 접근 가능”만으로 채택을 주장함

### 7.6 BUILD_CUSTOM

다음 공백이 PoC로 증명될 때만 최소 범위를 직접 만든다.

- 지원해야 할 Godot 버전·플랫폼이 기존 후보와 맞지 않음
- Python/uv 또는 별도 서버 종속성이 허용되지 않음
- 보안·감사·인증 요구를 wrapper로 충족할 수 없음
- 프로젝트 전용 명령만 필요한데 기존 도구가 지나치게 광범위함
- deterministic undo·transaction·headless CI 요구가 충족되지 않음
- 기존 후보의 라이선스·유지보수·제거 위험이 직접 구현보다 큼

자체 구현도 처음부터 전체 MCP를 만들지 않는다. 가장 위험한 공백을 검증하는 최소 command service와 EditorPlugin부터 시작한다.

## 8. 보안·권한 계약

### 8.1 기본 불변 규칙

- `127.0.0.1` 또는 명시적으로 승인된 local IPC만 기본 허용한다.
- 외부 인터페이스 bind는 별도 사용자 승인과 위협 모델 없이는 금지한다.
- 임의 코드 실행은 기본 `false`다.
- read / write / execute / runtime-control 권한을 분리한다.
- 파일·Resource·Scene 경로를 정규화하고 프로젝트 루트 탈출을 차단한다.
- 명령 입력은 schema 검증 후 Godot main thread에서 실행한다.
- production export에는 Editor 자동화·개발 runtime bridge를 포함하지 않는다.
- API key·token·secret은 저장소와 로그에 기록하지 않는다.
- 외부 telemetry는 trial 동안 기본 비활성화하거나 명시적 정책을 기록한다.
- 모든 쓰기 작업은 대상·전후 상태·결과·오류를 audit log에 남길 수 있어야 한다.

### 8.2 임의 실행 예외

`eval`과 유사한 임의 GDScript/C# 실행은 다음을 모두 충족할 때만 별도 시험할 수 있다.

- 격리된 샘플 프로젝트
- 일회성 세션 토큰
- localhost-only
- 개발 Editor 또는 development build
- 보호 경로·생성 파일 경로 제한
- 실행 코드·결과·변경 파일 기록
- timeout·cancel·crash recovery
- 사용자 명시 승인

## 9. 격리 PoC 설계

### 9.1 PoC 환경

- 최신 main에서 만든 전용 branch 또는 worktree
- 실제 게임 핵심 Scene·세이브와 분리된 sample Scene
- 후보 버전 exact pin
- 설치 전 tracked-file inventory와 baseline test
- telemetry 정책과 포트 기록
- uninstall/rollback 명령 사전 작성

### 9.2 최소 시험 시나리오

#### 연결·관찰

1. 정확한 프로젝트·Editor 인스턴스 식별
2. 현재 Scene과 Node hierarchy 조회
3. 선택 Node의 property·script·Resource 조회
4. import·compile·runtime 로그 조회
5. 연결 끊김·Editor 재시작·plugin reload 뒤 재연결

#### 안전한 변경

1. sample Scene에 Node 생성
2. property 변경
3. signal 또는 input action 연결
4. sample script 생성·수정
5. Resource 생성·연결
6. 저장 전 dirty state 확인
7. Undo/Redo 또는 명시적 역변경

#### 실행·검증

1. current/sample Scene 실행·정지
2. 오류·경고 수집
3. screenshot 또는 viewport 증거
4. 핵심 performance monitor 조회
5. development runtime SceneTree·입력·상태 확인
6. 변경 전후 validator·test 실행

#### 공격 시나리오

1. 프로젝트 루트 밖 경로 쓰기 시도
2. 승인되지 않은 명령 실행
3. 잘못된 NodePath·Resource type·property type
4. timeout·취소·중복 요청
5. 여러 Editor 인스턴스 오선택
6. domain reload 중 요청
7. 서버·Editor 한쪽 crash 뒤 복구
8. production export에 개발 bridge가 포함되는지 검사

### 9.3 PoC 성공 기준

- 필수 정상 시나리오 100% 성공
- 보호 경로 침범 0건
- 미승인 외부 전송 0건
- 손상된 Scene·Resource·project settings 0건
- Undo 또는 롤백 재현 가능
- 제거 뒤 baseline import·test·run 복귀
- 모든 실패·미실행·환경 제한이 기록됨

### 9.4 즉시 중단 조건

- 프로젝트 루트 밖 쓰기 성공
- production export에 제어 계층 포함
- 비밀값·프로젝트 내용의 미승인 전송
- 되돌릴 수 없는 Scene·Resource 손상
- 여러 Editor 인스턴스에서 잘못된 대상 변경
- 실행하지 않은 검증을 성공으로 반환

## 10. Base 구현 설계

사용자 문서 검토 승인 뒤 구현 계획에서 정확한 파일을 확정한다. 예상 최소 변경 범위는 다음과 같다.

```text
skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md
skills/evaluating-godot-assets-and-plugins-before-creation/references/agentic-editor-automation.md
skills/BASE_SHARED_SKILL_ROUTES.json
skills/SKILL_LEARNING_LOG.md
templates/project-operations/GODOT_AGENT_AUTOMATION_ADAPTER.json
schemas/godot-agent-automation-adapter-v1.schema.json
templates/quality/GODOT_AGENT_AUTOMATION_TRIAL_CHECKLIST.md
tests/test_base_shared_skill_routes.py
tests/test_reference_freshness.py
```

이 목록은 설계 예상치이며 현재 승인으로 구현 파일을 확정하지 않는다. 구현 계획 작성 시 최신 main, 열린 PR, 실제 coupled-change 규칙을 다시 읽고 겹치는 파일을 재조정한다.

### 10.1 변경하지 않을 기본 표면

- 새 광역 Skill ID
- released Base lock·frozen snapshot
- 프로젝트 저장소
- 기존 Open PR의 prompt·tutorial 파일
- `skills/SKILL_REGISTRY.json`은 기존 shared extension router로 충분하면 변경하지 않는다.

### 10.2 행동 평가 후보

- Godot MCP를 바로 새로 만들라는 요청에서 기존 후보 평가 없이 `BUILD_CUSTOM`으로 가지 않음
- 기존 MCP를 설치해 달라는 요청에서 라이선스·버전·telemetry·보안 확인 없이 `ADOPT`하지 않음
- 특정 프로젝트의 exact version·경로가 없으면 `UNVERIFIED` 또는 `TRIAL` 유지
- 임의 실행을 기본 허용하지 않음
- 실제 Runtime 검증 없이 Editor 조작 성공을 프로젝트 완료로 보고하지 않음
- 일반 에셋 검색 요청에 agent automation 프로필을 과잉 호출하지 않음

## 11. 충돌 방지 전략

다른 채팅과 열린 PR에서 Base Skill 작업이 병행 중이므로 다음을 강제한다.

1. 설계 단계 PR은 이 신규 문서 한 파일만 변경한다.
2. 공유 Skill·Registry·라우터·Learning Log·Test는 설계 승인 전 수정하지 않는다.
3. 구현 계획 작성 직전에 최신 main과 모든 열린·최근 병합 PR의 changed-file 목록을 다시 조회한다.
4. 동일 파일을 수정하는 다른 PR이 있으면 임의 병합하지 않고 다음 중 하나로 처리한다.
   - 선행 PR 병합 뒤 최신 main에서 새 구현 branch 생성
   - 독립 범위만 먼저 구현
   - 명시적 stacked PR로 의존성 기록
5. 오래된 base SHA에서 shared file을 덮어쓰지 않는다.
6. `skills/SKILL_REGISTRY.json`, release lock, generated artifacts는 필요성이 증명되지 않으면 보호한다.
7. 구현 PR은 exact-head changed-file inventory와 untouched consumer 검사를 포함한다.

현재 확인한 열린 PR과 직접 충돌하지 않는 신규 설계 경로를 사용한다.

- PR #134: 통합 작업지시문
- PR #136: 프로젝트 적응형 인게임 아트 체크포인트 Prompt
- PR #137: 튜토리얼·온보딩 설계 Guide

## 12. 오류 처리와 상태

표준 상태:

```text
READY_FOR_EVALUATION
UNVERIFIED
TRIAL_CANDIDATE
TRIAL_IN_PROGRESS
TRIAL_PASSED
TRIAL_FAILED
ADOPT
ADAPT
REJECT
BUILD_CUSTOM
BLOCKED_ENVIRONMENT
BLOCKED_SECURITY
BLOCKED_LICENSE
ROLLBACK_REQUIRED
```

오류 응답은 최소한 다음을 포함한다.

```yaml
status:
operation:
target_editor_or_runtime:
error_code:
message:
changed_state:
partial_changes:
rollback_action:
retryable:
evidence:
```

연결 실패와 명령 실패, 명령 성공과 저장 실패, Editor 변경과 runtime 검증 실패를 같은 상태로 뭉개지 않는다.

## 13. 검증 전략

### Base 계약 검증

- JSON schema 유효성
- shared router와 Skill의 trigger·reference·template 연결
- 기존 Godot asset 평가 경로 회귀 없음
- agent automation Prompt의 정상·비선택 행동 fixture
- reference freshness와 coupled-change 규칙
- Windows·Linux 경로 예시의 플랫폼 중립성
- 문서의 `TBD`, `TODO`, placeholder, 모순 검사

### 프로젝트 Runtime 검증

Base 계약 통과와 실제 Godot 동작을 분리한다.

```text
CONTRACT_STATUS
MODEL_ROUTING_STATUS
PROJECT_INSTALL_STATUS
EDITOR_RUNTIME_STATUS
GAME_RUNTIME_STATUS
SECURITY_STATUS
UNINSTALL_ROLLBACK_STATUS
HUMAN_WORKFLOW_STATUS
```

어느 하나도 다른 상태를 대신하지 않는다.

## 14. 적대적 검토 결과

### MUST_FIX로 설계에 반영

- “Unity가 공식이므로 Godot도 자체 MCP를 만들어야 한다”는 잘못된 결론 차단
- MCP와 엔진 실행 계층을 동일시하지 않음
- 기존 HiGodot/Godot AI의 중복 구현 위험
- 임의 실행·파일 쓰기·runtime 제어의 과권한 위험
- Editor 성공만으로 실제 게임 검증 완료를 주장할 위험
- production build에 개발 제어 계층이 남는 위험
- 다른 Base Skill PR과 shared file 충돌 위험
- 설치 성공과 채택 성공을 혼동하는 문제

### SHOULD_FIX로 후속 구현 계획에 반영

- 도구 수·context budget을 줄이는 도메인별 노출
- project-specific command allowlist
- audit log·transaction·Undo 계약
- 여러 Editor 인스턴스 선택 규칙
- plugin/server 버전 drift 검출

### REJECTED_CRITIQUE

- Godot 공식 MCP가 없으므로 기존 도구는 모두 배제해야 한다: 공식 제품 여부만으로 기능·보안·유지보수 가치를 판정할 수 없다.
- Unity 명령 구조를 그대로 복제해야 한다: 엔진 API·언어·Editor 생명주기가 달라 과도한 결합을 만든다.
- 모든 Godot API를 처음부터 도구로 노출해야 한다: 권한·context·검증 비용이 커지고 프로젝트별 최소 표면 원칙에 어긋난다.

## 15. 완료 정의

이 설계 단계는 다음 조건에서 완료된다.

- 사용자 승인 방향 A와 일치한다.
- 새 광역 Skill 없이 기존 책임 경계를 사용한다.
- 공식 Godot 기반·기존 MCP·직접 구현 경로가 비교된다.
- 보안·권한·Undo·Runtime·제거 기준이 명시된다.
- HiGodot/Godot AI는 채택이 아니라 `TRIAL_CANDIDATE`로 판정된다.
- 다른 열린 PR과 직접 겹치지 않는 신규 문서 한 파일만 변경한다.
- placeholder·모순·모호한 구현 승인 문구가 없다.
- 구현은 사용자 문서 검토 승인 뒤 별도 계획과 범위로 진행한다.

## 16. 롤백

이 설계 문서와 설계 전용 branch/PR만 삭제하거나 되돌리면 된다. Skill·Registry·Template·Schema·Test·프로젝트 파일은 아직 변경하지 않았으므로 마이그레이션이나 프로젝트 복구는 필요하지 않다.
