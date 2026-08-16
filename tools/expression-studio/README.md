# Expression Studio

`Expression Studio`는 승인된 캐릭터 원본을 기준으로 FACS에서 영감을 받은 표정 제어를 검증하고, 선택한 한 장의 후보를 프로젝트 내부에 내보낸 뒤 Tool Hub의 정확한 프로젝트/Figma tool route로 전달하는 로컬 도구입니다.

## 역할 경계

- 이 도구는 얼굴 제어·시선·머리 방향·게임 표정 프리셋을 자연어 편집 지시로 해석합니다.
- `AU46` 같은 코드는 단독으로 이미지 모델에 보장된 명령이 아닙니다. 예: `AU46 + left`는 `wink the left eye`로 풀어 씁니다. `left`/`right`는 **뷰어 기준이 아니라 캐릭터의 해부학적 좌/우**입니다.
- 강도는 검토 가능한 자연어로 항상 함께 해석합니다: `A` 매우 미세함, `B` 미세함, `C` 보통, `D` 강함, `E` 최대로 읽히는 강도. 이는 모델별 수치 보장이 아니라 수정 범위의 의도를 뜻합니다.
- 원본의 얼굴 형태·머리카락·의상·팔레트·구도·조명·화풍은 변경 금지 제약으로 계보와 생성 지시에 기록합니다. 엔진에는 실행별 사본만 전달하고, 원본 해시가 바뀌면 사용자·외부 편집을 덮어쓰지 않은 채 실행을 차단합니다. 자동 복구는 하지 않으므로 사용자가 변경 원인을 확인해야 합니다.
- Studio 자체가 임의의 Figma node를 선택하거나 Figma API를 직접 호출하지 않습니다. `확정 및 전달`은 정확히 선택·내보낸 bytes를 child-only 자격으로 부모 Tool Hub에 전달하고, Tool Hub의 Figma Bridge가 canonical `character_expression_runs` route를 재검증한 뒤 queue/receipt를 관리합니다. 실제 plugin receipt가 오기 전에는 `VERIFIED`로 표시하지 않습니다.
- 기본 `subscription_handoff_import` 모드는 ChatGPT Pro 구독 또는 로컬 도구에서 이미 만든 PNG/JPEG/WebP 후보를 가져오며 외부 provider를 호출하지 않습니다. Tool Hub 정상 경로는 이 모드를 고정하며 `provider_call_made=false`, `requires_additional_payment=false`를 유지합니다. 명시적 독립 실행의 `--run-mode openai`는 호환 경로일 뿐 Tool Hub의 canonical production path가 아니며 별도 API 비용이 필요합니다.
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

위 명령은 추가 API 과금 없는 기본 가져오기 모드로 실행됩니다. 브라우저에서 보유 중인 ChatGPT Pro 구독 또는 로컬 생성기로 만든 후보 1–8장을 선택하고, 후보 수와 파일 수를 일치시킵니다. 모든 파일은 25 MiB 이하, 최대 변 4096px인 PNG/JPEG/WebP여야 하며 요청 전체는 202 MiB 이하입니다.

Tool Hub를 통한 정상 사용자 흐름은 Studio를 직접 명령행으로 실행하지 않습니다. Hub가 검토된 interpreter, project ID, adapter/config hash, launch nonce를 고정하고 `subscription_handoff_import`로 child를 시작합니다. Windows 정상 사용은 설치된 `Base Tool Hub.lnk`에서 시작하며 외부 PowerShell 창을 유지할 필요가 없습니다.

```bash
set -a
. /absolute/path/to/Base/.env.local
set +a

PYTHONPATH=src .venv/bin/python -m expression_studio.app \
  --project-root /absolute/path/to/project \
  --project-id coc-fiction \
  --run-mode openai \
  --figma-target-registry /absolute/path/to/Base/docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json \
  --approved-anchor-registry /absolute/path/to/project/docs/APPROVED_VISUAL_ANCHORS.json
```

위 `openai` 예시는 독립 호환/진단 경로입니다. Tool Hub 정상 production 경로로 사용하지 않습니다. 별도 API 크레딧을 사용하는 경우에만 `credit_balance_exhausted`, `insufficient_quota`, `rate_limit_exceeded` 같은 provider 상태가 관련됩니다.

Windows에서는 Tool Hub가 reviewed Studio child를 suspended 상태로 만들고 Windows Job Object에 연결한 뒤 실행하며, 실제 Studio runtime PID가 해당 Job에 속하는지 검증합니다. GitHub-hosted Windows에서 real process-tree/reviewed launch/multi-project smoke와 subscription import/confirm-delivery 계약이 통과했습니다. **사용자 개발자 PC에서 같은 경로를 실제 실행한 결과는 아직 `NOT_RUN`**이므로 그 전에는 developer-PC IRG를 PASS로 올리지 않습니다.

`--project-root`는 Git 작업트리 루트여야 합니다. 먼저 `.asset-vault/library/`를 초기화하고 프로젝트의 `.gitignore`에서 `.asset-vault/`를 실제로 제외해야 합니다. 전역 ignore, 뒤의 부정 규칙, tracked/protected 경로, symlink/reparse 경유는 거부합니다. 모든 후보와 실행 기록은 `.asset-vault/library/generated/expression-studio/<asset>/<run>/`에만 생성됩니다.

브라우저의 `approval_status` 문자열은 승인 증거가 아닙니다. production import/export/Figma 전달에는 project-owned `--approved-anchor-registry`가 Git에 커밋된 현재 blob과 정확히 일치하고, exact source path, Figma node URL, source SHA-256, `APPROVED`, evidence와 checked-at을 검증해야 합니다. 이 증거가 없거나 작업트리에서만 수정된 경우 전달 전에 차단됩니다. simulated 실행은 `ANCHOR_ROUTE_SYNTAX_VALID` 또는 `ANCHOR_UNVERIFIED`로 로컬 검토만 할 수 있습니다.

`--run-mode simulated`은 테스트용 `FakeExpressionEngine`이며 화면과 API에 `SIMULATED / DELIVERY_BLOCKED`로 표시되고 export와 Figma 전달이 차단됩니다. `--run-mode openai`는 별도 API 비용을 요구하는 독립 호환 경로입니다. 기본 subscription import 결과도 export에는 project-owned 승인 앵커 증거가 필요하고, Figma 전달에는 준비된 exact-project/tool routing이 추가로 필요합니다.

서버는 loopback Host와 Origin만 허용하고 mutation 요청에 same-site session과 `X-Studio-CSRF`를 요구합니다. `/api/status`는 Hub가 비교할 tool/project/engine/launch nonce/config hash를 반환하지만, 상태 응답 자체가 이미지 생성이나 Figma 배치 증거는 아닙니다.

## ChatGPT Pro same-run → 검토 → Figma Bridge 흐름

1. Figma에서 원본을 승인하고, 프로젝트에 원본 PNG와 committed `docs/APPROVED_VISUAL_ANCHORS.json` 증거를 준비합니다.
2. 얼굴 제어/Outfit/Scene 요청을 입력합니다. 모순된 제어·알 수 없는 제어는 handoff 전에 차단됩니다.
3. Studio가 server-issued run ID와 verified anchor에 묶인 ChatGPT Pro handoff prompt를 준비합니다. prompt는 provider API 호출을 수행하지 않습니다.
4. 일반 ChatGPT Pro 구독 화면에서 실제 후보 PNG를 만든 뒤 Studio의 **같은 run**으로 가져옵니다. 브라우저가 project/request/source truth를 새로 정하지 못하며 import source는 `CHATGPT_INCLUDED`로 고정됩니다.
5. 후보를 비교해 하나를 명시적으로 선택하고 export를 수행합니다. 선택 전에는 전달이 차단됩니다.
6. `확정 및 전달`은 export 직후 exact selected bytes와 기록된 SHA를 다시 읽어 부모 Tool Hub에 전달합니다. 브라우저가 다른 project ID나 Figma node를 지정할 수 없습니다.
7. Tool Hub는 `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`의 현재 project에 대한 `character_expression_runs` route, parent/destination/marker를 다시 검증한 뒤 Figma Bridge queue에 넣습니다.
8. Figma plugin이 exact target에 같은 bytes를 배치하고 receipt의 target/hash/bridge/image identity가 검증되어야 `VERIFIED`가 됩니다. queue 상태나 Figma 창 열기만으로는 성공으로 간주하지 않습니다.

현재 Base registry에는 Character/Expression용 exact `Expression Runs` route만 등록되어 있습니다. Sprite/Effect의 별도 destination node는 검토 전이므로 임의로 재사용하지 않습니다.

## 테스트

```bash
cd tools/expression-studio
PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q
node --check web/app.js
```
