# Sprite Animation Studio

캐릭터 또는 이펙트의 **승인된 원본 앵커**를 기준으로 동작 후보를 만들고, 사람이 채택·순서·변형을 검토한 뒤 PNG, GIF, 아틀라스와 Godot 핸드오프 JSON을 프로젝트 내부에 내보내는 로컬 도구입니다.

## 소유 경계

- Base에는 코드, 테스트, 템플릿, 문서와 제3자 고지만 둡니다.
- 원본 이미지·Figma 내보내기·생성 후보·GIF·아틀라스·실행 기록은 프로젝트 경로에만 남깁니다.
- API 키와 프로젝트 생성물은 Base에 **커밋하지 않습니다**. MVP는 API 키를 직접 읽거나 저장하지 않으며, 명시적으로 지정한 로컬 `sprite-gen` 실행 파일만 호출합니다.

## 설치

```bash
cd tools/sprite-animation-studio
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

Windows PowerShell에서는 `.venv\Scripts\python -m pip install -e '.[dev]'`를 사용합니다.

## 실행

테스트/화면 점검만 할 때는 실제 그림을 만들지 않는 가짜 엔진을 명시적으로 사용합니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --fake-engine
```

실제 생성에는 정확한 `sprite-gen` 커밋 `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`에서 설치한 실행 파일을 직접 지정합니다. 도구는 `prepare → gen --provider codex → extract` 컴포넌트-행 파이프라인을 실행한 뒤, 추출 프레임 수를 다시 검증합니다.

```bash
PYTHONPATH=src .venv/bin/python -m sprite_animation_studio.app \
  --project-root /절대/경로/프로젝트 \
  --sprite-gen-executable /절대/경로/sprite-gen/.venv/bin/sprite-gen
```

서버는 루프백 인터페이스만 사용합니다. 경로는 모두 `--project-root` 아래여야 하며, 앵커가 승인되지 않았거나 엔진이 요청한 프레임 수와 다른 결과를 내면 작업은 `blocked` 상태로 남습니다.

## Figma → 스프라이트시트 흐름

1. Figma에서 원본 이미지와 사용할 노드 URL을 확정합니다.
2. 프로젝트에 원본 PNG를 저장하고, 경로·Figma 노드 URL·승인 상태를 입력합니다.
3. 후보가 생성되면 프레임을 선택하고 순서·위치·크기를 조정합니다. 원본 후보 PNG는 수정하지 않습니다.
4. 전체 요청 프레임을 다시 검토한 뒤 내보냅니다.
5. 프로젝트의 `art/animation-runs/<asset>/<run>/exports/`에서 프레임, `preview.gif`, `atlas.png`, `manifest.json`, Godot 핸드오프를 확인합니다.

`*.spriteframes.json`은 Godot에 적용할 정보를 담은 **핸드오프**이며, 실제 Godot Import·Scene 연결·런타임 동작을 자동으로 검증했다는 뜻은 아닙니다.

## 테스트

```bash
cd tools/sprite-animation-studio
PYTHONPATH=src .venv/bin/python -m pytest -v
```

실제 생성 엔진을 바꾸기 전에는 `THIRD_PARTY_NOTICES.md`의 업그레이드·롤백 절차를 따르세요.
