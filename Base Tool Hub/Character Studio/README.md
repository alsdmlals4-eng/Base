# Character Studio

**실행 정본:** `tools/expression-studio`  
**호환 tool_id:** `expression-studio`

기존 Expression Studio를 중복 앱으로 복제하지 않고 확장한 캐릭터 일관성 편집 도구입니다.

## 편집 모드

- `expression`: 기존 표정·시선·머리 방향·프리셋 편집.
- `outfit`: 얼굴 형태·얼굴 특징·헤어·체형·포즈·구도·배경·조명·화풍을 보호하고 **복장·의상·착용 장비만** 변경.
- `scene`: 얼굴 형태·얼굴 특징·헤어·복장·체형·포즈·구도·화풍을 보호하고 **장소·환경·배경만** 변경. 배경과 어울리는 조명·그림자 통합은 허용하되 캐릭터 디자인 변경은 금지.

한 요청은 한 편집 모드만 가질 수 있습니다. `outfit`/`scene`은 표정 AU·프리셋·시선·머리 방향 변경을 함께 요청하지 못하도록 서버 계약에서 차단합니다.

## 일관성의 의미

보호 문구는 이미지 모델에 전달되는 편집 범위를 좁히는 **강한 지시 계약**이지, 픽셀 단위 동일성을 자동 보장하는 수학적 증명은 아닙니다. 따라서 실제 후보는 원본 캐릭터와 사람이 비교해 정체성·복장/배경 범위·화풍을 검수해야 합니다.

기본 `subscription_handoff_import` 모드에서는 ChatGPT/Figma/로컬 생성기로 만든 후보를 가져와 검토할 수 있습니다. `openai` 모드는 별도 API 크레딧이 필요하며, provider 성공 이미지가 생기기 전까지 실제 생성 품질은 `BLOCKED_UNVERIFIED`입니다.

Figma 전달은 `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`의 exact-project target을 사용하며, 실제 배치는 같은 프로젝트 GPT의 연결된 Figma 실행 계층이 담당합니다.
