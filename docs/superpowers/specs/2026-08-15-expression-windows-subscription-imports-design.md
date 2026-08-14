# Expression Studio Windows Subscription Import Portability Design

Issue: #413

## Goal

이미 병합된 `subscription_handoff_import` + `CHATGPT_INCLUDED` Expression import 경로를 Ubuntu와 Windows 양쪽의 실제 FastAPI endpoint에서 검증하고, Windows에서만 남아 있는 로컬 portability blocker가 재현될 때 기존 Base portable primitives를 재사용해 최소 수정한다.

## Existing-solution-first

- 새 Studio/runtime/provider adapter를 만들지 않는다.
- #410에서 병합된 shared Windows portable Asset Vault staging을 그대로 재사용한다.
- #410의 `Validate Sprite Subscription Import Portability` workflow를 Expression까지 확장해 하나의 Visual Studio portability gate로 통합한다. 새 중복 workflow를 만들지 않는다.
- 기존 Expression `test_import_expression_candidates_without_a_provider_call`이 이미 두 distinct PNG, `CHATGPT_INCLUDED`, `subscription_handoff_import`, `INCLUDED_OR_LOCAL_HANDOFF`, `provider_call_made=false`를 검증하므로 같은 의미의 새 endpoint test를 복제하지 않는다.

## RED-first contract

첫 PR head는 production code를 변경하지 않고 기존 Expression import test만 Ubuntu/Windows portability matrix에 추가한다.

예상 가능한 실패는 추정하지 않고 실제 로그로 분리한다.

1. clean test environment에서 current Starlette TestClient dependency가 누락되는가?
2. 그 의존성을 만족한 뒤 Windows normal PNG anchor read가 POSIX-only reader 때문에 실패하는가?
3. #410 shared staging은 별도 수정 없이 Expression lifecycle을 통과하는가?

각 실패를 하나씩 재현한 뒤 한 원인만 수정한다.

## Minimal implementation candidates

실제 RED가 확인된 경우에만 다음을 적용한다.

- TestClient dependency가 누락되면 Expression `dev` extra에 Sprite와 동일한 reviewed `httpx2>=2.9,<3`를 추가한다.
- Windows anchor reader가 실패하면 Expression `_read_project_image()`를 새 구현으로 만들지 않고 Base의 `read_regular_nofollow` / `read_regular_portable_nofollow` 선택 패턴으로 교체한다.
- shared `staging.py`는 #410 main 결과를 소비할 뿐 이 PR에서 수정하지 않는다.

## Security ceiling

- POSIX는 기존 descriptor-relative `O_NOFOLLOW` semantics를 유지한다.
- Windows anchor read는 Base portable trusted-file threat model을 사용한다: path component symlink/reparse rejection, bounded regular-file read, identity revalidation.
- 이 PR은 Windows portable path를 POSIX의 malicious same-user rename-race guarantee와 동등하다고 주장하지 않는다.

## Protected work boundary

현재 #373 changed-file inventory에는 다음이 없다.

- `tools/expression-studio/src/expression_studio/service.py`
- `tools/expression-studio/tests/test_import_api.py`
- `tools/expression-studio/pyproject.toml`

#373가 소유하는 models/engine/catalog/web/character tests/Tool Hub adapters는 수정하지 않는다. #376 Figma Bridge 및 #386 Windows child supervisor 파일도 수정하지 않는다.

## IRG ceiling

이 작업이 증명할 수 있는 것은 fixture PNG의 local import/validation/provenance와 Windows/Ubuntu project-confined staging이다. 실제 ChatGPT Pro image generation, character identity quality, outfit/scene quality, Figma delivery, Windows Tool Hub child ownership, real game-project consumption은 별도 gate다.
