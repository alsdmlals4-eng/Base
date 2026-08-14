# Base Tool Hub Figma Bridge

`Base Tool Hub Figma Bridge`는 로컬 Base Tool Hub가 준비한 **검증된 PNG 바이트**를 현재 Figma 파일의 canonical `Generated Assets` 영역에 쓰는 작은 개발 플러그인입니다.

이 플러그인은 이미지 생성 엔진이 아니며 프로젝트·Figma 목적지를 사용자가 입력받지 않습니다. Base Tool Hub가 pairing code로 프로젝트를 고정하고, 플러그인은 현재 파일 안에서 다음 두 조건이 모두 맞을 때만 이미지를 만듭니다.

1. Base가 제공한 exact `generation_area_node_id`가 존재한다.
2. 그 노드의 직접 자식으로 `Base Tool Hub Route · <project_id>` marker가 존재하며 hidden + locked 상태다.

## 왜 manifest.template.json 인가

Figma 플러그인 manifest의 `id`는 Figma가 발급합니다. 저장소가 임의 ID를 만들어 실제 발급 ID라고 주장하지 않습니다.

현재 개발 단계에서는 Figma Desktop에서 **Development > New plugin** 흐름으로 한 번 플러그인 ID를 발급한 뒤, `manifest.template.json`의 `FIGMA_ASSIGNED_PLUGIN_ID`를 그 값으로 치환하여 `manifest.json`을 만듭니다. `manifest.json`은 기기별 개발 설정으로 취급하며 Base 정본에는 발급되지 않은 ID를 커밋하지 않습니다.

장기적으로 내부/공개 배포 플러그인으로 게시하면 이 1회 개발 설정은 제거할 수 있습니다. 그 전까지 실제 local bridge smoke를 통과했다고 과장하지 않습니다.

## 개발 manifest 예

`manifest.template.json`을 같은 폴더의 `manifest.json`으로 복사한 뒤 Figma가 발급한 ID만 교체합니다.

```json
{
  "name": "Base Tool Hub Figma Bridge",
  "id": "<FIGMA가 발급한 plugin id>",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "documentAccess": "dynamic-page",
  "networkAccess": {
    "allowedDomains": ["none"],
    "devAllowedDomains": ["http://127.0.0.1:8764"]
  }
}
```

개발 bridge는 `127.0.0.1:8764` 이외의 네트워크 목적지를 사용하지 않습니다. production publishing으로 전환할 때는 Figma의 배포 요구에 맞춘 HTTPS transport를 별도 검토합니다.

## 사용 흐름

1. Windows에서 바탕화면 `Base Tool Hub`를 실행합니다.
2. Tool Hub에서 프로젝트를 선택합니다.
3. `Figma Bridge 연결 코드 만들기`를 눌러 6자리 pairing code를 만듭니다.
4. Base에 등록된 해당 프로젝트 Figma 파일을 엽니다.
5. Figma Desktop에서 개발 플러그인 `Base Tool Hub Figma Bridge`를 실행합니다.
6. pairing code만 입력합니다. 프로젝트 ID, file key, node ID, Git 경로는 입력하지 않습니다.
7. `다음 이미지 전달`을 누릅니다.
8. 플러그인은 exact bytes SHA-256, target node, project route marker를 검사합니다.
9. 조건이 맞을 때만 image node를 만들고 receipt를 Tool Hub로 보냅니다.
10. Tool Hub가 receipt를 승인한 뒤에만 `FIGMA_DELIVERED_VERIFIED`가 됩니다.

## 실패와 재시도

- Figma가 닫혔거나 bridge가 실행 중이 아니어도 프로젝트의 accepted local output은 삭제하지 않습니다.
- content hash가 다르면 Figma mutation 전에 `CONTENT_HASH_MISMATCH`로 중단합니다.
- target/marker가 다르면 `FIGMA_ROUTE_MARKER_MISSING`으로 중단합니다.
- 같은 `node_name`이 이미 있고 image fill이면 lost receipt response 재시도로 간주해 기존 node를 재사용합니다.
- 같은 이름의 비이미지 node가 있으면 `FIGMA_DUPLICATE_NODE_CONFLICT`로 중단합니다.
- mutation 뒤 receipt 응답이 끊기면 pending receipt를 `figma.clientStorage`에 저장하고 다음 실행에서 재검증합니다.

## 보안 경계

- 브라우저 Tool Hub: 기존 cookie + CSRF.
- Figma Bridge: 별도 short-lived pairing + scoped Bearer token.
- token/pairing code는 GitHub, project receipt, Figma document node/pluginData에 저장하지 않습니다.
- bridge token은 Figma device-local `clientStorage`에만 저장합니다.
- 프로젝트 간 queue/content/receipt 접근은 `project_id` scope로 차단합니다.

## Implementation Reality Gate

현재 저장소 코드와 CI가 증명할 수 있는 것과 실제 Figma Desktop bridge 실행은 별도입니다.

- plugin static contract PASS = manifest/code 경계 검증.
- Figma route marker live readback PASS = 정확한 destination marker 존재 증명.
- **local Tool Hub → 실제 development plugin → image write → receipt** 전체는 실제 Figma Desktop에서 smoke를 수행하기 전까지 `NOT_RUN`입니다.
- real OpenAI/other provider image quality, real Sprite action/effect, Godot integration도 각각 별도 증거가 필요합니다.
