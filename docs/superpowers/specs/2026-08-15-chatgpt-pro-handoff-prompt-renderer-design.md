# ChatGPT Pro Handoff Prompt Renderer Design

Issue: #411

## Goal

검증된 `SubscriptionHandoffPacket` 하나를 사용자가 일반 ChatGPT Pro UI에 그대로 붙여넣을 수 있는 결정적 텍스트 지시문으로 렌더한다. 새 request schema나 provider adapter를 만들지 않는다.

## Contract

`render_chatgpt_pro_prompt(packet: SubscriptionHandoffPacket) -> str`

렌더 결과는 다음만 포함한다.

- project/tool/run/workflow identity
- source display filename + SHA-256
- 사용자가 승인한 exact generation instruction
- PNG output count + min/max dimensions
- review checklist
- 생성 결과를 같은 Tool Hub run으로 import하라는 안내
- fixed import truth: `subscription_handoff_import`, `CHATGPT_INCLUDED`
- no API/provider call requested, existing ChatGPT Pro subscription surface 사용

## Safety

- packet validation을 우회하지 않는다.
- renderer에 임의 문자열/경로/Figma target/provider credential 입력을 받지 않는다.
- Figma file key/node id, absolute path, API key, shell/browser automation instruction을 생성하지 않는다.
- deterministic output이며 12 KiB를 넘으면 fail closed한다.

## Scope

`base-tool-contracts`와 테스트만 변경한다. UI/clipboard/browser opening은 진행 중 #373 등 owner가 merge된 뒤 follow-up에서 연결한다.

## IRG

이 기능은 copy-ready prompt 생성만 증명한다. 실제 ChatGPT Pro UI 상호작용, 이미지 생성, 다운로드/import, visual QA는 증명하지 않는다.
