# Sprite Animation Studio

캐릭터 또는 이펙트의 **승인된 원본 앵커**를 기준으로 프레임을 가져오거나 검증하고, 사람이 채택·순서·변형을 확인한 뒤 PNG, GIF, 아틀라스와 Godot 핸드오프 JSON을 프로젝트 내부에 내보내는 로컬 도구입니다.

지원 workflow는 `sprite_action`, `pose_sequence`, `effect_stages`, `expression_variation`입니다. Figma 전달 목적지는 브라우저가 고르지 않으며 서버에 저장된 run의 `request.mode`만으로 결정됩니다.

## 소유·비용 경계

- Base에는 코드, 테스트, 템플릿, 문서와 제3자 고지만 둡니다.
- 원본 이미지·Figma 내보내기·생성 후보·GIF·아틀라스·실행 기록은 프로젝트 경로에만 남깁니다.
- API 키와 프로젝트 생성물은 Base에 **커밋하지 않습니다**.
- Tool Hub 정상 경로는 `subscription_handoff_import` + `CHATGPT_INCLUDED`이며 `provider_call_made=false`, `requires_additional_payment=false`를 유지합니다.
- 별도 OpenAI API, credit, 추가 유료 provider를 정상 경로에 사용하지 않습니다.
- 브라우저 입력은 Figma file/node/route 권한이 아닙니다. Tool Hub가 인증된 Studio identity와 Base의 exact route registry를 다시 검증합니다.

## dedicated Figma route

현재 Base 정본은 8개 프로젝트 각각에 아래 3개 exact route를 사용합니다.

- Character/Expression: `character_expression_runs` → `Expression Runs`
- Sprite Action/Pose: `sprite_action_runs` → `Sprite Action Runs`
- Effect: `effect_runs` → `Effect Runs`

Sprite Studio의 서버 소유 mode mapping은 고정입니다.

- `pose_sequence` → **Sprite Action Runs**
- `sprite_action` → **Sprite Action Runs**
- `effect_stages` → **Effect Runs**
- `expression_variation` → Sprite Studio Figma delivery 불가, `DELIVERY_TOOL_ROUTE_UNAVAILABLE`

Sprite/Effect 결과를 Character의 `Expression Runs` 또는 generic `Generated Assets`로 fallback하지 않습니다. route 누락·잘못된 route·registry drift·project mismatch는 모두 fail-closed입니다.

## 설치와 실행

정상 사용자는 Windows의 `Base Tool Hub.lnk`에서 프로젝트와 Sprite Animation Studio를 선택하므로 매번 PowerShell을 열 필요가 없습니다. 수동 개발 실행 예시는 다음과 같습니다.

```bash
cd tools/sprite-animation-studio
python -m venv .venv
.venv/bin/python -m pip install -e ../base-tool-contracts
.venv/bin/python -m pip install -e '.[dev]'

PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --port 8765 \
  --project-id coc-fiction \
  --figma-target-registry /절대/경로/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /절대/경로/프로젝트/docs/APPROVED_VISUAL_ANCHORS.json
```

`--project-root`는 Git 작업트리 루트여야 하며 `.asset-vault/`가 프로젝트 `.gitignore`에 실제로 제외되어 있어야 합니다. 모든 후보와 실행 기록은 `.asset-vault/library/generated/sprite-animation-studio/<asset>/<action>/<run>/` 아래에서 관리합니다.

기본 `subscription_handoff_import`에서는 ChatGPT 구독 화면 또는 로컬 도구에서 만든 1–16개 프레임을 가져옵니다. 각 파일은 25 MiB 이하, 최대 변 4096px인 PNG/JPEG/WebP여야 하며 요청 전체는 402 MiB 이하입니다. 서버는 프레임 수, 크기 일치, 투명/빈 이미지, pixel duplicate, 프로젝트 identity, 승인 앵커 증거를 검증합니다.

테스트 엔진은 `--run-mode simulated --fake-engine`으로만 선택합니다. 결과는 `SIMULATED / DELIVERY_BLOCKED`이며 실제 생성·export·Figma 전달 성공으로 간주하지 않습니다.

별도 `pinned_sprite_gen` 경로는 OS-isolated workspace adapter가 완성되기 전까지 fail-closed이며 정상 구독 handoff 경로와 별개입니다.

## 승인 앵커와 export

브라우저의 `approval_status` 문자열은 승인 증거가 아닙니다. 실제 export에는 project-owned `docs/APPROVED_VISUAL_ANCHORS.json`이 필요하며 다음이 현재 파일과 정확히 일치해야 합니다.

- project ID
- source path
- source SHA-256
- Figma node URL
- 승인 상태와 evidence

export가 성공하면 run의 `exports/` 아래에 선택 프레임, `preview.gif`, `atlas.png`, manifest, Godot handoff가 만들어집니다. Figma confirmed delivery의 payload는 이 중 **exported atlas PNG** 하나이며 `record.export_output_sha256["atlas"]`과 실제 읽은 bytes의 SHA-256이 동일할 때만 전송합니다.

## 확정 및 전달

export 뒤 사용자는 **확정 및 전달**을 실행합니다.

```text
exported run
  → 서버가 request.mode에서 route 결정
  → export된 atlas SHA 재검증
  → Tool Hub private loopback delivery
  → Figma Bridge
  → exact Sprite Action Runs 또는 Effect Runs
  → receipt/status readback
```

브라우저는 route ID, Figma file key, target node ID, marker node ID를 전송하지 않습니다. `confirm-delivery` 요청에는 사용자 선택 route body가 없습니다.

관련 API:

- `POST /api/runs/{run_id}/confirm-delivery`
- `GET /api/runs/{run_id}/delivery-status`
- `GET /api/runs/{run_id}/confirmed-download`

서버가 반환한 `target_node_name`, `bridge_state`, `delivery_state`, pairing code(필요한 경우), Figma URL과 download URL만 UI에서 표시합니다. confirmed download도 처음 전달한 atlas와 같은 SHA를 다시 검증합니다. atlas bytes가 이후 변조되면 sender 호출 또는 status/download 전에 차단합니다.

## 현재 증거 한계

Cloud/Figma preflight와 사용자 PC live IRG는 구분합니다.

```text
DEDICATED_SPRITE_EFFECT_ROUTE_CLOUD_PREFLIGHT = PASS_8_OF_8
BASE_TOOL_ROUTE_REGISTRY = READY_24_OF_24
SPRITE_MODE_ROUTE_TRUST = VERIFIED_BY_TESTS
SPRITE_CONFIRMED_ATLAS_SHA_BINDING = VERIFIED_BY_TESTS
USER_PC_TOOL_HUB = NOT_RUN
REAL_CHATGPT_PRO_POSE_SEQUENCE = NOT_RUN
REAL_CHATGPT_PRO_EFFECT_STAGES = NOT_RUN
LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN
GODOT_CONSUMPTION = NOT_RUN
```

따라서 CI와 Figma MCP read/write 성공만으로 사용자 PC Tool Hub, 실제 ChatGPT Pro 생성 품질, localhost Figma Bridge receipt, Godot 소비를 PASS로 올리지 않습니다.

## 테스트

```bash
cd tools/sprite-animation-studio
PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q
```

실제 엔진·route·delivery 계약 변경 전에는 테스트, exact-head CI, Figma node readback을 함께 검증합니다.
