# Sprite Animation Studio

캐릭터 또는 이펙트의 **승인된 원본 앵커**를 기준으로 동작 후보를 만들고, 사람이 채택·순서·변형을 검토한 뒤 PNG, GIF, 아틀라스와 Godot 핸드오프 JSON을 프로젝트 내부에 내보내는 로컬 도구입니다.

작업 목적은 `sprite_action`(기본), `expression_variation`, `pose_sequence`, `effect_stages` 중 하나로 명시합니다. 캐릭터 전용 표정/포즈와 이펙트 전용 단계 모드는 요청 단계에서 차단해 서로 섞이지 않게 합니다.

## 소유 경계

- Base에는 코드, 테스트, 템플릿, 문서와 제3자 고지만 둡니다.
- 원본 이미지·Figma 내보내기·생성 후보·GIF·아틀라스·실행 기록은 프로젝트 경로에만 남깁니다.
- API 키와 프로젝트 생성물은 Base에 **커밋하지 않습니다**. MVP는 API 키를 직접 읽거나 저장하지 않으며, 명시적으로 지정한 로컬 `sprite-gen` 실행 파일만 호출합니다.
- 로컬 앱은 Figma에 직접 업로드하지 않습니다. `ready_for_project_gpt` 전달 패킷은 같은 프로젝트 GPT 작업공간에서 Figma 도구를 사용할 수 있도록 대상·계보·시각 산출물 경로만 준비합니다.

## 설치

```bash
cd tools/sprite-animation-studio
python -m venv .venv
.venv/bin/python -m pip install -e ../base-tool-contracts
.venv/bin/python -m pip install -e '.[dev]'
```

Windows PowerShell에서는 `.venv\Scripts\python -m pip install -e '.[dev]'`를 사용합니다.

현재 mutable engine/export 경로는 Linux의 `/proc/self/fd` 안정 디렉터리 핸들로 symlink 교체 중 외부 쓰기를 차단합니다. 해당 기능이 없는 Windows 실행은 생성 단계에서 fail-closed이며 실제 Windows 런타임은 `BLOCKED_UNVERIFIED`입니다.

## 실행

테스트/화면 점검만 할 때는 실제 그림을 만들지 않는 가짜 엔진을 명시적으로 사용합니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --fake-engine \
  --port 8765 \
  --project-id coc-fiction \
  --figma-target-registry /절대/경로/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /절대/경로/프로젝트/docs/APPROVED_VISUAL_ANCHORS.json
```

실제 생성에는 정확한 `sprite-gen` 커밋 `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`에서 설치한 실행 파일을 직접 지정합니다. 도구는 `prepare → gen --provider codex → extract` 컴포넌트-행 파이프라인을 실행한 뒤, 추출 프레임 수를 다시 검증합니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --sprite-gen-executable /절대/경로/sprite-gen/.venv/bin/sprite-gen \
  --sprite-gen-repository /절대/경로/sprite-gen \
  --project-id coc-fiction \
  --figma-target-registry /절대/경로/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /절대/경로/프로젝트/docs/APPROVED_VISUAL_ANCHORS.json
```

`--figma-target-registry`를 사용하는 실행은 반드시 `--project-id`로 작업공간의 정식 프로젝트 ID를 고정합니다. 요청의 프로젝트 ID가 다르면 후보 생성 단계에서 차단되므로, 한 프로젝트 작업공간에서 다른 프로젝트 Figma 대상으로 라우팅할 수 없습니다.

`--project-root`는 Git 작업트리 루트여야 합니다. `.asset-vault/library/`를 만들고 프로젝트 `.gitignore`에서 `.asset-vault/`를 실제로 제외해야 합니다. 전역 ignore만 있는 경우, 뒤의 부정 규칙, tracked/protected 경로, symlink/reparse 경유는 거부합니다. 모든 후보와 실행 기록은 `.asset-vault/library/generated/sprite-animation-studio/<asset>/<action>/<run>/`에만 생성됩니다.

브라우저가 보내는 `approval_status`는 승인 증거가 아닙니다. export/Figma 전달에는 project-owned `--approved-anchor-registry`가 Git에 커밋된 현재 blob과 정확히 일치하고, exact source path, Figma node URL, source SHA-256, 승인 상태, evidence/checked-at 검증을 통과해야 합니다. 없거나 작업트리에서만 수정된 경우 검토 전용이며 전달은 차단됩니다.

서버는 루프백 인터페이스만 사용합니다. `--port`로 프로젝트별 포트를 명시할 수 있습니다. loopback Host/Origin, same-site session과 `X-Studio-CSRF`가 맞지 않는 mutation은 거부합니다. 앵커가 승인되지 않았거나 엔진이 요청한 프레임 수와 다른 결과를 내면 작업은 `blocked` 상태로 남습니다.

`--fake-engine` 결과는 `SIMULATED / DELIVERY_BLOCKED`로 표시됩니다. 프레임 검토는 가능하지만 export와 Figma 전달은 서비스/API에서 차단되며 실제 액션·표정·포즈·이펙트 생성 성공으로 간주하지 않습니다.

## Figma → 스프라이트시트 → 프로젝트 Figma 흐름

1. Figma에서 원본 이미지와 사용할 노드 URL을 확정합니다.
2. 프로젝트에 원본 PNG를 저장하고, 경로·Figma 노드 URL·승인 상태를 입력합니다.
3. 후보가 생성되면 프레임을 선택하고 순서·위치·크기를 조정합니다. 원본 후보 PNG는 수정하지 않습니다.
4. 전체 요청 프레임을 다시 검토한 뒤 프로젝트 출력 준비를 실행합니다.
5. `프로젝트 GPT 전송 준비`는 현재 `project_id`의 registry 상태를 fail-closed로 검사합니다. `REGISTERED_NO_MUTATION` 대상은 차단되며 다른 프로젝트로 바뀌지 않습니다.
6. `ready_for_project_gpt` 패킷을 받은 같은 프로젝트 GPT가 Figma 도구로 그 프로젝트의 `Sprite Animation Studio` / `Generated Assets`에 새 실행 섹션을 추가합니다. 이 도구 화면은 직접 업로드하지 않습니다.
7. production-eligible 엔진에서만 `.asset-vault/library/generated/sprite-animation-studio/<asset>/<action>/<run>/exports/`의 프레임, `preview.gif`, `atlas.png`, `manifest.json`, Godot 핸드오프를 확인합니다.

프로젝트 GPT의 정확한 전달 절차는 [`project-gpt-figma-delivery.md`](../../templates/sprite-animation/project-gpt-figma-delivery.md)를 사용합니다. 이 절차는 Figma 파일이 `READY_FOR_DELIVERY`로 명시된 경우에만 실행합니다.

`*.spriteframes.json`은 Godot에 적용할 정보를 담은 **핸드오프**이며, 실제 Godot Import·Scene 연결·런타임 동작을 자동으로 검증했다는 뜻은 아닙니다.

## 테스트

```bash
cd tools/sprite-animation-studio
PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q
```

실제 생성 엔진을 바꾸기 전에는 `THIRD_PARTY_NOTICES.md`의 업그레이드·롤백 절차를 따르세요.
