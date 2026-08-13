# Expression Studio

`Expression Studio`는 승인된 캐릭터 원본을 기준으로 FACS에서 영감을 받은 표정 제어를 검증하고, 선택한 한 장의 후보를 프로젝트 내부에 내보낸 뒤 정확한 프로젝트 Figma 전달 패킷을 준비하는 로컬 도구입니다.

## 역할 경계

- 이 도구는 얼굴 제어·시선·머리 방향·게임 표정 프리셋을 자연어 편집 지시로 해석합니다.
- `AU46` 같은 코드는 단독으로 이미지 모델에 보장된 명령이 아닙니다. 예: `AU46 + left`는 `wink the left eye`로 풀어 씁니다. `left`/`right`는 **뷰어 기준이 아니라 캐릭터의 해부학적 좌/우**입니다.
- 강도는 검토 가능한 자연어로 항상 함께 해석합니다: `A` 매우 미세함, `B` 미세함, `C` 보통, `D` 강함, `E` 최대로 읽히는 강도. 이는 모델별 수치 보장이 아니라 수정 범위의 의도를 뜻합니다.
- 원본의 얼굴 형태·머리카락·의상·팔레트·구도·조명·화풍은 변경 금지 제약으로 계보와 생성 지시에 기록합니다. 엔진에는 실행별 사본만 전달하고, 원본 해시가 바뀌면 사용자·외부 편집을 덮어쓰지 않은 채 실행을 차단합니다. 자동 복구는 하지 않으므로 사용자가 변경 원인을 확인해야 합니다.
- 로컬 도구는 Figma에 직접 업로드하지 않습니다; it **does not upload** anything. `ready_for_project_gpt` 패킷을 받은 **matching project GPT workspace**가 Figma 연결 도구로 배치합니다.
- 실제 외부 이미지 생성 모델의 API 키·토큰·이미지 바이트·ZIP을 저장하거나 전송하지 않습니다.
- 멀티프레임 스프라이트시트·GIF·Godot 핸드오프는 `Sprite Animation Studio`의 책임입니다.

## 실행

```bash
cd tools/expression-studio
python -m venv .venv
.venv/bin/python -m pip install -e ../base-tool-contracts
.venv/bin/python -m pip install -e '.[dev]'

PYTHONPATH=src .venv/bin/python -m expression_studio.app \
  --project-root /absolute/path/to/project \
  --project-id coc-fiction \
  --figma-target-registry /absolute/path/to/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /absolute/path/to/project/docs/APPROVED_VISUAL_ANCHORS.json
```

Windows PowerShell에서는 `.venv\Scripts\python -m pip install -e '.[dev]'`를 사용합니다. 브라우저에서 `http://127.0.0.1:8766`을 열어 원본 경로, Figma 원본 노드 URL, 표정 제어를 입력합니다.

현재 mutable engine/export 경로는 Linux의 `/proc/self/fd` 안정 디렉터리 핸들로 symlink 교체 중 외부 쓰기를 차단합니다. 해당 기능이 없는 Windows 실행은 생성 단계에서 fail-closed이며 실제 Windows 런타임은 `BLOCKED_UNVERIFIED`입니다.

`--project-root`는 Git 작업트리 루트여야 합니다. 먼저 `.asset-vault/library/`를 초기화하고 프로젝트의 `.gitignore`에서 `.asset-vault/`를 실제로 제외해야 합니다. 전역 ignore, 뒤의 부정 규칙, tracked/protected 경로, symlink/reparse 경유는 거부합니다. 모든 후보와 실행 기록은 `.asset-vault/library/generated/expression-studio/<asset>/<run>/`에만 생성됩니다.

브라우저의 `approval_status` 문자열은 승인 증거가 아닙니다. export/Figma 전달에는 project-owned `--approved-anchor-registry`가 Git에 커밋된 현재 blob과 정확히 일치하고, exact source path, Figma node URL, source SHA-256, `APPROVED`, evidence와 checked-at을 검증해야 합니다. 없거나 작업트리에서만 수정된 경우 `ANCHOR_ROUTE_SYNTAX_VALID` 또는 `ANCHOR_UNVERIFIED`로만 표시되고 전달은 차단됩니다.

현재 기본 엔진은 원본 훼손·경로·후보 선택 계약을 검증하는 `FakeExpressionEngine`입니다. 화면과 API에 `SIMULATED / DELIVERY_BLOCKED`로 표시되며 후보 검토만 가능하고 export와 Figma 전달은 서비스에서 차단됩니다. 외부 이미지 생성 어댑터는 해당 프로젝트 작업공간에서 모델, 비용, 데이터 처리, 이미지 편집 기능을 검증한 뒤 별도로 추가해야 합니다. 따라서 이 기본 실행은 실제 표정 이미지 생성 성공을 주장하지 않습니다.

서버는 loopback Host와 Origin만 허용하고 mutation 요청에 same-site session과 `X-Studio-CSRF`를 요구합니다. `/api/status`는 Hub가 비교할 tool/project/engine/launch nonce/config hash를 반환하지만, 상태 응답 자체가 이미지 생성이나 Figma 배치 증거는 아닙니다.

## 검토와 전달 흐름

1. Figma에서 원본을 승인하고, 프로젝트에 원본 PNG를 저장합니다.
2. 얼굴 제어는 최대 네 개까지 선택합니다. 모순된 제어·알 수 없는 제어는 생성 전에 차단됩니다. 양쪽 `AU46` 윙크를 동시에 요청하는 경우는 양안 감김에 해당하므로 `AU43`을 사용해야 합니다.
3. 후보를 비교해 하나를 명시적으로 선택합니다. 선택 전에는 내보내기와 Figma 전달 준비가 차단됩니다.
4. production-eligible 엔진에서만 선택 결과, 컨택트시트, 계보, 매니페스트를 `.asset-vault/library/generated/expression-studio/` 아래에 내보낼 수 있습니다.
5. `프로젝트 GPT 전송 준비`는 registry의 현재 `project_id`, `READY_FOR_DELIVERY`, Figma 파일 키, 페이지 ID, 생성 영역 ID를 검사합니다. 일치하지 않으면 전달하지 않습니다.
6. 같은 프로젝트 GPT가 Figma의 `Sprite Animation Studio` / `Generated Assets` / `Expression Runs` 안에 새 실행 섹션을 추가합니다. 이전 실행은 교체하지 않습니다.

정확한 GPT 전달 절차는 [`project-gpt-figma-delivery.md`](../../templates/expression-studio/project-gpt-figma-delivery.md)를 따릅니다.

## 테스트

```bash
cd tools/expression-studio
PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q
node --check web/app.js
```
