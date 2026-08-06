# Base Godot Local MCP Gateway

Godot 편집기 작업을 Codex와 VS Code의 MCP 호스트에서 호출하기 위한 로컬 stdio Gateway입니다. 현재 구현은 **Gateway Core**이며 실제 Godot EditorPlugin Bridge는 별도 단계입니다.

```yaml
python: "Python 3.12"
mcp_sdk: "mcp==2.0.0"
transport: stdio
bridge_transport: authenticated loopback length-prefixed JSON
production_adapter_ready: false
```

## 제공 도구

정확히 다음 여섯 도구만 노출합니다.

- `godot_doctor`
- `godot_status`
- `godot_catalog`
- `godot_scene_inspect`
- `godot_node_rename`
- `godot_task_status`

임의 셸, 임의 파일 접근, 임의 GDScript 실행, 삭제, export/build, MCP 내부 승인 도구는 제공하지 않습니다. `node.rename`이 사람 승인을 요구하면 Gateway는 승인 토큰을 노출하지 않고 `APPROVAL_PENDING`만 반환합니다.

## 현재 경계

```yaml
gateway_stdio_server: IMPLEMENTED
authenticated_fake_bridge_e2e: PASS
real_godot_editor_bridge: NOT_IMPLEMENTED
human_approval_dock: NOT_IMPLEMENTED
live_project_e2e: NOT_RUN
production_adapter_ready: false
```

실제 Bridge descriptor 없이 실행하면 서버 자체는 시작되지만 `godot_status`는 `BRIDGE_NOT_CONNECTED`를 반환합니다. 이 상태에서도 `godot_doctor`로 호스트 프로필과 `project.godot` 기반 프로젝트 identity를 확인할 수 있습니다.

## 설치

Gateway는 Python 3.12와 `mcp==2.0.0`에 고정되어 있습니다.

```bash
cd "<BASE_ROOT>/templates/project-operations/godot-local-mcp/gateway"
python -m pip install .
```

개발 checkout을 직접 사용할 때는 host 설정의 `PYTHONPATH`를 다음 폴더로 지정할 수 있습니다.

```text
<BASE_ROOT>/templates/project-operations/godot-local-mcp/gateway/src
```

## 프로젝트 identity 생성

Gateway는 포트 번호가 아니라 정규화된 프로젝트 경로와 `project.godot` 실제 바이트 SHA-256을 함께 사용합니다.

```bash
python -c "from base_godot_mcp.project_identity import ProjectIdentity; import json,sys; print(json.dumps(ProjectIdentity.from_root(sys.argv[1]).public_summary(), indent=2))" "<ABSOLUTE_PROJECT_ROOT>"
```

출력의 `project_fingerprint`를 해당 client profile의 `allowed_project_fingerprints`에 기록합니다.

## client profile 준비

예제:

- `profiles/codex.profile.json.example`
- `profiles/gpt-vscode.profile.json.example`

각 예제를 저장소 밖의 `<ABSOLUTE_CONFIG_DIR>`로 복사하고 다음을 교체합니다.

1. `credential_secret`: 최소 32자의 새 무작위 비밀
2. `allowed_project_fingerprints`: 위 단계에서 계산한 정확한 fingerprint
3. `expires_at`: 필요한 최소 유효기간

무작위 비밀 예시:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

POSIX 계열에서는 profile과 Bridge descriptor를 소유자 전용으로 제한합니다.

```bash
chmod 600 "<ABSOLUTE_CONFIG_DIR>/codex.json"
chmod 600 "<ABSOLUTE_DESCRIPTOR_PATH>"
```

허용 profile ID는 `codex`와 `gpt-vscode`뿐입니다. `deepseek`와 알 수 없는 profile은 파일 조회 전에 fail-closed로 거부합니다.

## Codex 연결

OpenAI Codex는 로컬 stdio MCP 서버를 `~/.codex/config.toml` 또는 신뢰된 프로젝트의 `.codex/config.toml`에 등록합니다. 저장소의 다음 예제를 개인 설정에 복사하고 절대 경로 placeholder를 교체합니다.

```text
hosts/codex.config.toml.example
```

Gateway Core만 점검할 때 실제 descriptor가 없다면 `BASE_GODOT_MCP_BRIDGE_DESCRIPTOR` 줄을 제거합니다. 실제 Godot Bridge가 descriptor를 생성한 뒤 해당 환경 변수를 다시 추가합니다.

설정 확인:

```bash
codex mcp list
```

Codex 세션에서는 `/mcp`로 연결 상태를 확인하고 먼저 `godot_doctor`, `godot_status`, `godot_catalog`를 호출합니다.

## VS Code 연결

VS Code 명령 팔레트에서 **MCP: Open User Configuration**을 실행하고 다음 예제의 `servers` 항목을 개인 user profile `mcp.json`에 복사합니다.

```text
hosts/vscode.user.mcp.json.example
```

필요한 경로는 사용자 환경 변수로 전달합니다.

- `BASE_GODOT_MCP_GATEWAY_SRC`
- `BASE_GODOT_MCP_CONFIG_DIR`
- `BASE_GODOT_MCP_BRIDGE_DESCRIPTOR`

설정 확인은 **MCP: List Servers**에서 수행합니다. 이 Base 저장소에는 활성 `.vscode/mcp.json`이나 `.codex/config.toml`을 커밋하지 않습니다.

## Bridge descriptor

`bridge/bridge-descriptor.json.example`은 형식 설명용입니다. 실제 descriptor는 향후 Godot EditorPlugin Bridge가 다음 조건으로 생성해야 합니다.

- `127.0.0.1` 또는 `::1`만 사용
- owner-private 파일
- profile ID와 project fingerprint 정확히 결속
- 짧은 만료시간
- 매 실행마다 새로운 descriptor nonce와 Bridge instance ID

Gateway와 Bridge는 4바이트 big-endian 길이 prefix, 최대 256 KiB JSON object frame, HMAC-SHA256 HELLO/REQUEST/RESPONSE 결속을 사용합니다.

## 정상 확인 순서

1. `godot_doctor` → profile ID와 project fingerprint 확인
2. `godot_status` → Bridge 미연결이면 `BRIDGE_NOT_CONNECTED`
3. `godot_catalog` → 허용된 typed capability만 확인
4. `godot_scene_inspect` → 읽기 전용 Scene/Node 확인
5. `godot_node_rename` → 승인 필요 시 `APPROVAL_PENDING`
6. `godot_task_status` → 동일 operation ID의 상태 확인

## 검증

```bash
python -m unittest \
  tests.test_godot_local_mcp_server \
  tests.test_godot_local_mcp_profile_store \
  tests.test_godot_local_mcp_stdio \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_bridge_client \
  tests.test_godot_local_mcp_authenticated_stdio \
  tests.test_godot_local_mcp_host_configs \
  -v
```

CI는 실제 `python -m base_godot_mcp` 자식 프로세스를 시작하고 MCP handshake 후 인증된 fake Bridge를 통해 다섯 Bridge-backed 도구를 왕복 검증합니다.

## 공식 설정 참고

- Codex MCP: `https://developers.openai.com/codex/mcp/`
- VS Code MCP configuration: `https://code.visualstudio.com/docs/agents/reference/mcp-configuration`
