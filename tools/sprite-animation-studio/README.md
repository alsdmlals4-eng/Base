# Sprite Animation Studio

캐릭터 또는 이펙트의 **승인된 원본 앵커**를 기준으로 동작 후보를 만들고, 사람이 채택·순서·변형을 검토한 뒤 PNG, GIF, 아틀라스와 Godot 핸드오프 JSON을 프로젝트 내부에 내보내는 로컬 도구입니다.

작업 목적은 `sprite_action`(기본), `expression_variation`, `pose_sequence`, `effect_stages` 중 하나로 명시합니다. 캐릭터 전용 표정/포즈와 이펙트 전용 단계 모드는 요청 단계에서 차단해 서로 섞이지 않게 합니다.

## 소유 경계

- Base에는 코드, 테스트, 템플릿, 문서와 제3자 고지만 둡니다.
- 원본 이미지·Figma 내보내기·생성 후보·GIF·아틀라스·실행 기록은 프로젝트 경로에만 남깁니다.
- API 키와 프로젝트 생성물은 Base에 **커밋하지 않습니다**. Tool Hub 정상 경로는 `subscription_handoff_import`만 사용하며 별도 OpenAI API 키를 읽거나 저장하지 않습니다.
- 브라우저는 Figma 파일 키, 목적 node, route를 선택하거나 전송 권한으로 제출하지 않습니다. 서버에 저장된 `RunRecord.request.mode`만 delivery route 권한을 가집니다.
- 현재 canonical exact route는 프로젝트마다 세 개입니다.
  - `character_expression_runs` → `Expression Runs`
  - `sprite_action_runs` → `Sprite Action Runs`
  - `effect_runs` → `Effect Runs`
- Sprite Studio에서는 `pose_sequence`와 `sprite_action`이 `Sprite Action Runs`, `effect_stages`가 `Effect Runs`로만 전달됩니다. `expression_variation`은 이 slice에서 전용 전달 목적지가 없으므로 `DELIVERY_TOOL_ROUTE_UNAVAILABLE`로 fail-closed합니다.
- Sprite/Effect output을 generic `Generated Assets` 또는 Character용 `Expression Runs`로 fallback하지 않습니다.

## 설치

```bash
cd tools/sprite-animation-studio
python -m venv .venv
.venv/bin/python -m pip install -e ../base-tool-contracts
.venv/bin/python -m pip install -e '.[dev]'
```

Windows PowerShell에서는 `.venv\Scripts\python -m pip install -e '.[dev]'`를 사용할 수 있지만, 정상 사용자 흐름은 설치된 `Base Tool Hub.lnk`에서 Studio child를 시작하므로 매 실행마다 PowerShell을 열 필요가 없습니다.

GitHub-hosted Windows에서는 reviewed Tool Hub child launch, 실제 process-tree ownership, multi-project isolation, subscription import portability가 검증됐습니다. 이것은 사용자 개발자 PC에서 실제 Tool Hub와 Studio child를 실행했다는 증거가 아닙니다. 별도 `pinned_sprite_gen` production 엔진은 OS-isolated workspace adapter가 없으므로 계속 fail-closed이며, 이 제한은 subscription import 경로의 Windows child 지원 여부와 별개입니다.

## 실행

기본 실행은 추가 API 과금 없는 가져오기 모드입니다. ChatGPT Pro 구독 또는 로컬 생성기로 만든 1–16개 프레임을 브라우저에서 순서대로 넣습니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --port 8765 \
  --project-id coc-fiction \
  --figma-target-registry /절대/경로/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /절대/경로/프로젝트/docs/APPROVED_VISUAL_ANCHORS.json
```

파일마다 25 MiB 이하, 최대 변 4096px인 PNG/JPEG/WebP만 받고 요청 전체는 402 MiB 이하입니다. 제출 전 업로드 순서를 앞/뒤로 바꾸거나 제거할 수 있습니다. 서버는 프레임 수, 동일 크기, 비어 있지 않은 픽셀, 중복 여부를 검사하며 행동·포즈·표정·단계별 이펙트 모두 같은 경계를 사용합니다. 이펙트 프레임에 알파 채널이 없으면 차단 대신 배경 정리 경고를 냅니다.

실제 그림을 만들지 않는 테스트 엔진은 `--run-mode simulated --fake-engine`으로만 선택합니다. Tool Hub 정상 경로는 `subscription_handoff_import`를 고정하며 `CHATGPT_INCLUDED`, `provider_call_made=false`, `requires_additional_payment=false` truth를 유지합니다.

아래 인자는 정확한 `sprite-gen` 커밋 `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`을 검증하기 위한 예약된 production 설정입니다. 현재 구현은 같은 사용자 프로세스가 실행 중 하위 출력 경로를 바꾸는 공격까지 격리할 OS sandbox runner가 없으므로 실제 `prepare → gen → extract` 실행을 명시적으로 차단합니다. 이 명령은 production 실행법이 아니라 fail-closed 설정 확인용입니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --sprite-gen-executable /절대/경로/sprite-gen/.venv/bin/sprite-gen \
  --sprite-gen-repository /절대/경로/sprite-gen \
  --run-mode pinned_sprite_gen \
  --project-id coc-fiction \
  --figma-target-registry /절대/경로/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /절대/경로/프로젝트/docs/APPROVED_VISUAL_ANCHORS.json
```

`sprite-gen execution is blocked until an OS-isolated workspace adapter is configured`가 현재의 정상적인 보호 결과입니다. 실제 생성이 가능하다고 판단하려면 별도 sandbox runner 구현, 경로 교체 공격 회귀 테스트, 실제 provider smoke가 모두 필요합니다.

`--figma-target-registry`를 사용하는 실행은 반드시 `--project-id`로 작업공간의 정식 프로젝트 ID를 고정합니다. 요청의 프로젝트 ID가 다르면 후보 생성 단계에서 차단되므로 한 프로젝트 작업공간에서 다른 프로젝트 대상으로 라우팅할 수 없습니다. Figma target registry와 별도로 Base의 canonical tool-route registry가 project/tool별 exact descendant node를 고정합니다.

`--project-root`는 Git 작업트리 루트여야 합니다. `.asset-vault/library/`를 만들고 프로젝트 `.gitignore`에서 `.asset-vault/`를 실제로 제외해야 합니다. 전역 ignore만 있는 경우, 뒤의 부정 규칙, tracked/protected 경로, symlink/reparse 경유는 거부합니다. 모든 후보와 실행 기록은 `.asset-vault/library/generated/sprite-animation-studio/<asset>/<action>/<run>/`에만 생성됩니다.

브라우저가 보내는 `approval_status`는 승인 증거가 아닙니다. export에는 project-owned `--approved-anchor-registry`가 Git에 커밋된 현재 blob과 정확히 일치하고, exact source path, Figma node URL, source SHA-256, 승인 상태, evidence/checked-at 검증을 통과해야 합니다. 없거나 작업트리에서만 수정된 경우 검토 전용이며 export가 차단됩니다.

서버는 루프백 인터페이스만 사용합니다. `--port`로 프로젝트별 포트를 명시할 수 있습니다. loopback Host/Origin, same-site session과 `X-Studio-CSRF`가 맞지 않는 mutation은 거부합니다. 앵커가 승인되지 않았거나 요청한 프레임 수와 import 결과가 다르면 작업은 `blocked` 상태로 남습니다.

`--fake-engine` 결과는 `SIMULATED / DELIVERY_BLOCKED`로 표시됩니다. 프레임 검토는 가능하지만 export와 외부 전달은 서비스/API에서 차단되며 실제 액션·표정·포즈·이펙트 생성 성공으로 간주하지 않습니다.

## ChatGPT Pro same-run → export → 확정 및 전달

1. Figma에서 원본 이미지와 사용할 승인 앵커 node URL을 확정하고 프로젝트에 원본 PNG와 committed `docs/APPROVED_VISUAL_ANCHORS.json` 증거를 준비합니다.
2. `pose_sequence`, `sprite_action`, `effect_stages` 등 정확한 workflow와 프레임 수를 지정합니다.
3. 일반 ChatGPT Pro 구독 화면에서 실제 프레임을 생성하고 Studio의 같은 run으로 순서대로 가져옵니다. import source는 `CHATGPT_INCLUDED`로 기록되고 Studio 자체의 `provider_call_made=false`를 유지합니다.
4. 프레임을 검토하고 순서·위치·크기를 조정합니다. 원본 후보 PNG는 수정하지 않습니다.
5. 전체 요청 프레임을 다시 검토한 뒤 project-local export를 수행합니다. production-eligible import에서만 `.asset-vault/library/generated/sprite-animation-studio/<asset>/<action>/<run>/exports/`의 프레임, `preview.gif`, `atlas.png`, `manifest.json`, Godot 핸드오프를 확인할 수 있습니다.
6. **확정 및 전달**은 manifest와 export evidence를 다시 검증하고, `record.export_output_sha256["atlas"]`에 묶인 정확한 **exported atlas PNG**만 localhost Tool Hub에 전달합니다.
7. 서버가 run mode에서 목적지를 결정합니다. `pose_sequence`/`sprite_action`은 `Sprite Action Runs`, `effect_stages`는 `Effect Runs`입니다. `expression_variation`은 `DELIVERY_TOOL_ROUTE_UNAVAILABLE`입니다.
8. Tool Hub는 인증된 child의 tool identity와 route allowlist, canonical registry, project binding을 다시 검증합니다. 동일 run·동일 route·동일 SHA는 재사용하고 route 변경은 `DELIVERY_RUN_ROUTE_MISMATCH`, bytes 변경은 `DELIVERY_RUN_CONTENT_MISMATCH`로 차단합니다.
9. 브라우저는 서버가 반환한 target name, bridge state, pairing code(필요한 경우), delivery state만 표시합니다. 전달 상태 새로고침과 `confirmed-download`도 같은 atlas SHA를 다시 검증합니다.
10. `*.spriteframes.json`은 Godot에 적용할 정보를 담은 핸드오프이며, 실제 Godot Import·Scene 연결·런타임 동작을 자동으로 검증했다는 뜻은 아닙니다.

## 증거 등급

현재 저장소/클라우드 검증과 실제 사용자 PC 검증을 혼합하지 않습니다.

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

Figma의 8개 프로젝트에는 `Sprite Action Runs`와 `Effect Runs`가 실제 생성·readback되어 있지만, 이 cloud preflight를 사용자 PC의 `Base Tool Hub.lnk` 실행, real ChatGPT Pro 생성 품질, localhost Bridge receipt, Godot 소비 증거로 승격하지 않습니다.

## 테스트

```bash
cd tools/sprite-animation-studio
PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q
```

실제 생성 엔진을 바꾸기 전에는 `THIRD_PARTY_NOTICES.md`의 업그레이드·롤백 절차를 따르세요.
