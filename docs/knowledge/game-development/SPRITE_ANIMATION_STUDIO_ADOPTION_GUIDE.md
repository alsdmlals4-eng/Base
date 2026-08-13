# Sprite Animation Studio 채택 가이드

## 목적과 범위

이 도구는 Figma에서 검토한 원본을 승인 앵커로 삼아 애니메이션 후보를 만들고, 사람의 큐레이션 후 프로젝트 로컬 경로에 스프라이트시트를 내보냅니다. Base는 도구의 공용 구현만 소유하며, 프로젝트별 이미지·생성 실행·Figma 파일·자격 증명은 소유하지 않습니다.

포함: 승인 앵커 계보, 후보 생성, 프레임 선택·순서·변형, PNG/GIF/아틀라스/manifest/Godot 핸드오프.

제외: 로컬 브라우저의 Figma 자동 쓰기, 프로젝트 저장소 자동 커밋, Godot Scene 자동 수정, 플랫폼 출시 권리 판정, 런타임 통과 주장.

## 프로젝트 준비

1. `--project-root`에 프로젝트 절대 경로를 지정합니다.
2. 원본 앵커와 생성 출력은 프로젝트 안에 두고, Base 경로는 입력·출력으로 사용하지 않습니다.
3. 요청마다 다음을 기록합니다.
   - 프로젝트·에셋 ID와 에셋 종류
   - 작업 모드(`expression_variation`, `pose_sequence`, `effect_stages`, `sprite_action`)
   - 원본 파일의 프로젝트 상대 경로
   - **Figma 노드 URL**
   - `approved` 상태와 요청한 프레임 수·FPS·반복 방식
4. 저작권·상업 사용·배포 권한은 프로젝트의 자산 권리 기록에서 별도로 확인합니다. 레퍼런스 이미지를 프로젝트 산출물에 무단 포함하지 않습니다.

## 검토 흐름

```text
Figma 원본 → 승인 앵커 → 동작 후보 → 채택 프레임 → 최종 아틀라스/GIF
```

- `lineage.json`은 앵커의 Figma URL과 실제 바이트 SHA-256을 저장합니다.
- `curation.json`은 선택·거절·위치·크기를 별도로 저장합니다. `frames/`의 후보 PNG는 수정하지 않습니다.
- 내보내기는 요청 프레임 수가 모두 선택될 때만 진행합니다. 부족하거나 엔진 결과 수가 다르면 `blocked`로 남습니다.

## 프로젝트 GPT → Figma 전달

프로젝트 GPT는 같은 프로젝트 작업공간에서만 Base 도구의 `ready_for_project_gpt` 패킷을 사용합니다. 이 패킷은 실제 Figma 업로드 완료가 아니라 대상·앵커 계보·선택된 시각 산출물의 프로젝트 상대 경로를 검증한 결과입니다.

1. `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`의 정확한 `project_id`를 조회합니다. 다른 프로젝트로 fallback하지 않습니다.
2. `REGISTERED_NO_MUTATION` 또는 `ARCHIVED`는 차단 상태입니다. Figma 도구를 호출하거나 해당 파일 내용을 검사·수정하지 않습니다.
3. `READY_FOR_DELIVERY`이고 프로젝트 GPT가 해당 이미지 바이트 및 수정 권한을 실제로 가진 경우에만 Figma 도구로 `Sprite Animation Studio` / `Generated Assets`를 resolve 또는 생성합니다.
4. 기존 승인 결과를 덮어쓰지 않고 run ID를 포함한 새 실행 섹션에 시각 산출물과 최소 메타데이터를 배치합니다.
5. 배치 후 정확한 Figma 섹션 URL, 업로드한 시각 산출물, 메타데이터만 둔 항목, 미실행 검증을 반환합니다.

재사용 가능한 프로젝트 GPT 지시문은 `templates/sprite-animation/project-gpt-figma-delivery.md`입니다. ZIP, 토큰 저장, 다른 채팅/프로젝트의 무단 전달은 이 경로에 포함하지 않습니다.

## Godot 적용과 확인

`exports/godot/<action>.spriteframes.json`은 참조용 핸드오프입니다. 다음 **Godot 런타임 검증**은 프로젝트에서 별도로 수행해야 합니다.

1. `atlas.png`와 `manifest.json`의 좌표·프레임 순서를 Godot Resource 또는 SpriteFrames에 적용합니다.
2. 애니메이션의 FPS·반복 여부·방향을 의도한 상태 전환에서 확인합니다.
3. 목표 해상도와 실제 캐릭터/이펙트 장면에서 피벗·잘림·깜빡임·입력 중단·재진입을 확인합니다.
4. 런타임 증거가 없으면 `GODOT_RUNTIME_NOT_RUN`으로 기록합니다. 핸드오프 JSON만으로 통과를 주장하지 않습니다.

## 실패, 롤백, 보안

- 로컬 어댑터 실패, PNG 검사 실패, 프레임 수 불일치, 경로 탈출은 성공으로 대체하지 않습니다.
- 실패한 출력은 프로젝트의 해당 실행 폴더만 제거하거나 이전 승인 실행으로 되돌립니다. Base 코드 변경은 PR revert로 복구합니다.
- API 키, 세션 토큰, 원본 아트, 생성 결과물은 Base PR에 추가하지 않습니다.
- `sprite-gen` 버전을 바꿀 때는 정확한 commit·라이선스·테스트 결과를 기록하고, 문제 시 기존 pin으로 되돌립니다. 계획된 생성 경로는 `prepare → gen --provider codex → extract`이지만, 현재는 OS-isolated workspace runner가 없어 subprocess 실행 전에 차단됩니다. 다른 제공자로 자동 전환하거나 이를 실제 생성 성공으로 보고하지 않습니다.
