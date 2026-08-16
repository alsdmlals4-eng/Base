# Sprite Animation Studio 채택 가이드

## 목적과 범위

이 도구는 Figma에서 검토한 원본을 승인 앵커로 삼아 애니메이션 후보를 만들고, 사람의 큐레이션 후 프로젝트 로컬 경로에 스프라이트시트를 내보냅니다. Base는 도구의 공용 구현만 소유하며, 프로젝트별 이미지·생성 실행·Figma 파일·자격 증명은 소유하지 않습니다.

포함: 승인 앵커 계보, 후보 생성/가져오기, 프레임 선택·순서·변형, PNG/GIF/아틀라스/manifest/Godot 핸드오프, Tool Hub의 exact project/tool route를 통한 Figma Bridge 전달.

제외: 프로젝트 저장소 자동 커밋, Godot Scene 자동 수정, 플랫폼 출시 권리 판정, 실제 ChatGPT Pro 이미지 품질 통과 주장, 사용자 PC에서 실행하지 않은 Tool Hub/Bridge를 PASS로 승격하는 것.

## 프로젝트 준비

1. `--project-root`에 프로젝트 절대 경로를 지정합니다.
2. 원본 앵커와 생성 출력은 프로젝트 안에 두고, Base 경로는 입력·출력으로 사용하지 않습니다.
3. 요청마다 다음을 기록합니다.
   - 프로젝트·에셋 ID와 에셋 종류
   - 작업 모드(`expression_variation`, `pose_sequence`, `effect_stages`, `sprite_action`)
   - 원본 파일의 프로젝트 상대 경로
   - **Figma 노드 URL**
   - 승인 앵커 증거와 요청한 프레임 수·FPS·반복 방식
4. 저작권·상업 사용·배포 권한은 프로젝트의 자산 권리 기록에서 별도로 확인합니다. 레퍼런스 이미지를 프로젝트 산출물에 무단 포함하지 않습니다.

## 검토 흐름

```text
Figma 원본 → 승인 앵커 → 동작 후보/가져오기 → 채택 프레임 → 최종 아틀라스/GIF → 확정 및 전달
```

- `lineage.json`은 앵커의 Figma URL과 실제 바이트 SHA-256을 저장합니다.
- `curation.json`은 선택·거절·위치·크기를 별도로 저장합니다. `frames/`의 후보 PNG는 수정하지 않습니다.
- 내보내기는 요청 프레임 수가 모두 선택될 때만 진행합니다. 부족하거나 엔진 결과 수가 다르면 `blocked`로 남습니다.
- `subscription_handoff_import` 정상 경로는 별도 provider API를 호출하지 않으며 `provider_call_made=false`를 유지합니다.

## Tool Hub → Figma Bridge 전달

현재 canonical 전달은 Project GPT packet 수동 배치가 아니라 **인증된 Sprite Studio child → Base Tool Hub → Figma Bridge** 흐름입니다.

1. Tool Hub가 Studio child에 canonical `project_id`와 child-only localhost credential을 부여합니다. 브라우저는 project/file/node/route 권한을 새로 만들지 못합니다.
2. 서버는 저장된 `RunRecord.request.mode`에서 route를 결정합니다.
   - `pose_sequence` / `sprite_action` → `sprite_action_runs` → `Sprite Action Runs`
   - `effect_stages` → `effect_runs` → `Effect Runs`
   - `expression_variation` → 이 slice에서는 `DELIVERY_TOOL_ROUTE_UNAVAILABLE`
3. `PROJECT_FIGMA_TARGET_REGISTRY.json`과 `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`을 함께 재검증합니다. 다른 프로젝트, generic `Generated Assets`, Character용 `Expression Runs`로 fallback하지 않습니다.
4. export manifest와 `record.export_output_sha256["atlas"]`을 다시 검증하고, 정확히 같은 exported atlas PNG bytes만 Tool Hub에 전달합니다.
5. Tool Hub는 동일 run·route·SHA를 idempotent하게 재사용하고 route 변경은 `DELIVERY_RUN_ROUTE_MISMATCH`, bytes 변경은 `DELIVERY_RUN_CONTENT_MISMATCH`로 차단합니다.
6. Figma Bridge plugin은 paired project의 exact destination에 bytes를 배치합니다. receipt의 target/hash/bridge/image identity가 일치한 뒤에만 `DELIVERED_VERIFIED`입니다.
7. Figma 전달 실패는 프로젝트 로컬 export를 되돌리지 않습니다. 같은 run의 검증된 bytes로 안전하게 재시도할 수 있습니다.

재사용 가능한 운영 지시문은 `templates/sprite-animation/project-gpt-figma-delivery.md`라는 legacy 파일명에 남아 있지만, 내용의 canonical owner는 Tool Hub/Figma Bridge입니다. `ready_for_project_gpt` packet, ZIP 전달, 토큰 저장, 다른 채팅/프로젝트의 무단 전달은 정상 경로가 아닙니다.

## Godot 적용과 확인

`exports/godot/<action>.spriteframes.json`은 참조용 핸드오프입니다. 다음 **Godot 런타임 검증**은 프로젝트에서 별도로 수행해야 합니다.

1. `atlas.png`와 `manifest.json`의 좌표·프레임 순서를 Godot Resource 또는 SpriteFrames에 적용합니다.
2. 애니메이션의 FPS·반복 여부·방향을 의도한 상태 전환에서 확인합니다.
3. 목표 해상도와 실제 캐릭터/이펙트 장면에서 피벗·잘림·깜빡임·입력 중단·재진입을 확인합니다.
4. 런타임 증거가 없으면 `GODOT_RUNTIME_NOT_RUN`으로 기록합니다. 핸드오프 JSON만으로 통과를 주장하지 않습니다.

## 증거 경계

저장소/클라우드 검증과 사용자 PC 실행을 구분합니다.

```text
DEDICATED_SPRITE_EFFECT_ROUTE_CLOUD_PREFLIGHT = PASS_8_OF_8
BASE_TOOL_ROUTE_REGISTRY = READY_24_OF_24
USER_PC_TOOL_HUB = NOT_RUN
REAL_CHATGPT_PRO_POSE_SEQUENCE = NOT_RUN
REAL_CHATGPT_PRO_EFFECT_STAGES = NOT_RUN
LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN
GODOT_CONSUMPTION = NOT_RUN
```

Figma route node가 실제 존재하고 CI가 통과해도 위 `NOT_RUN` 항목을 자동으로 PASS로 바꾸지 않습니다.

## 실패, 롤백, 보안

- 로컬 어댑터 실패, PNG 검사 실패, 프레임 수 불일치, 경로 탈출, route/SHA 불일치는 성공으로 대체하지 않습니다.
- 실패한 출력은 프로젝트의 해당 실행 폴더만 제거하거나 이전 승인 실행으로 되돌립니다. Base 코드 변경은 PR revert로 복구합니다.
- API 키, 세션 토큰, 원본 아트, 생성 결과물은 Base PR에 추가하지 않습니다.
- `sprite-gen` 버전을 바꿀 때는 정확한 commit·라이선스·테스트 결과를 기록하고, 문제 시 기존 pin으로 되돌립니다. 계획된 생성 경로는 `prepare → gen --provider codex → extract`이지만, 현재는 OS-isolated workspace runner가 없어 subprocess 실행 전에 차단됩니다. 다른 제공자로 자동 전환하거나 이를 실제 생성 성공으로 보고하지 않습니다.
