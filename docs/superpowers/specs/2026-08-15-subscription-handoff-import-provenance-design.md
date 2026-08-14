# GPT Pro Handoff → Studio Import Provenance Binding Design

Issue: #404

## Goal

Merged #394의 `SubscriptionHandoffPacket`이 현재 Expression/Sprite Studio의 실제 `subscription_handoff_import` API에 들어갈 때 provenance 선택이 다시 사용자 입력으로 흔들리지 않도록 정확한 import 계약을 고정한다.

## Existing-solution-first

새 adapter/runtime을 만들지 않는다. 두 Studio 모두 이미 `DeclaredSource`에 `CHATGPT_INCLUDED`를 지원하고 Tool Hub launch adapter는 `subscription_handoff_import`를 고정한다. 따라서 shared handoff packet의 truth field만 확장하고 저장소 회귀 테스트로 양쪽 consumer와의 호환성을 묶는다.

## Contract

`SubscriptionHandoffPacket`에 생성자 입력이 아닌 고정 필드 두 개를 추가한다.

- `import_run_mode = "subscription_handoff_import"`
- `import_declared_source = "CHATGPT_INCLUDED"`

`public_view()`에는 `import` 객체로 노출한다.

```json
{
  "import": {
    "run_mode": "subscription_handoff_import",
    "declared_source": "CHATGPT_INCLUDED"
  }
}
```

이 값들은 사용자가 임의 변경할 수 없고 API key/Figma/private path와 동일하게 packet authority 밖 입력을 허용하지 않는다.

## Consumer compatibility

영구 repository-level contract는 다음을 검사한다.

- Expression Studio import source set에 `CHATGPT_INCLUDED`가 존재한다.
- Sprite Animation Studio import source set에 `CHATGPT_INCLUDED`가 존재한다.
- 두 Studio CLI 기본값이 `subscription_handoff_import`다.
- shared packet의 고정 import truth와 consumer 문자열이 동일하다.

Studio source 자체는 수정하지 않는다. 오픈 PR #373/#376/#386과 파일 충돌을 만들지 않는다.

## IRG

증명 가능:
- GPT Pro handoff packet → Studio import provenance 문자열 호환성
- 추가 결제/Provider call 없는 truth field 유지
- 사용자 provenance override 제거

증명하지 않음:
- 실제 ChatGPT Pro 이미지 생성
- 실제 브라우저 import UX
- visual identity/pose/effect 품질
- Figma Bridge live delivery

## Rollback

shared contract와 tests를 revert한다. 프로젝트 자산/런타임 데이터 migration은 없다.
