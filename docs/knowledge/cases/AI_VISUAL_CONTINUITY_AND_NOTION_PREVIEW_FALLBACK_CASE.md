# AI Visual Continuity and Notion Preview Fallback Case

## 상태

- 출처: `alsdmlals4-eng/ninja-survival-godot@5b7c86e25c53e4a2667f1a70dc59938fc60c4c9a`
- BCP: `BCP-2026-032`
- 상태: **패턴 / 부분 검증**
- 적용 범위: AI-assisted game visual production, persistent-character visual variants, Notion human-facing preview delivery

이 사례는 특정 프로젝트의 캐릭터·색·진영·전승 이름을 Base canon으로 복제하지 않는다. 재사용 가능한 문제 구조와 검증 경계만 남긴다.

## 문제 A — 시각적 분화가 지속 캐릭터 identity를 침식

### 증상

하나의 주인공이 여러 faction/class/tradition 특징을 습득하는 프로젝트에서, 각 계열의 차이를 강하게 보여주려다 AI 시안이 서로 다른 전신 캐릭터처럼 분화될 수 있다.

개별 시트만 보면 구분은 잘 되지만, 실제 제품 약속이 `한 캐릭터가 여러 전승을 축적한다`라면 다음 문제가 생긴다.

- 얼굴/체형/core outfit이 variant마다 drift,
- full composite에서 여러 의상이 충돌,
- key art와 gameplay의 주인공이 다른 사람처럼 보임,
- 작은 인게임 실루엣에서 장식이 정보를 삼킴.

### 원인

`계열 간 차별화`를 먼저 설계하고 `persistent character identity owner`와 `additive layer owner`를 먼저 분리하지 않았다.

### 해결 패턴

`PERSISTENT_CHARACTER_ADDITIVE_VISUAL_LAYER_GATE`

```text
persistent character identity
→ face / hair / body proportion / core outfit / core silhouette

additive visual layers
→ equipment accent / aura / energy / companion / shadow / state effect
```

승인 전에 variant 하나만 보지 않고 **final composite**를 별도 acceptance로 공격한다.

검토 질문:

1. 동일 인물의 얼굴/머리/체형/core outfit이 유지되는가?
2. 누적 layer가 한 캐릭터의 성장으로 읽히는가?
3. 동시 최대치가 충돌하면 dominant/supporting hierarchy가 있는가?
4. gameplay hazard/UI 정보가 가려지지 않는가?
5. 실제 **small gameplay scale**에서 판독 가능한가?
6. key art와 gameplay rendering density가 달라도 identity / motif / palette / hierarchy가 이어지는가?

### 비적용

- 실제로 서로 다른 playable character를 선택하는 게임,
- body replacement 자체가 핵심 fantasy인 true transformation,
- 완전 교체가 의도된 state language인 경우.

## 문제 B — Notion connector가 local binary를 직접 받지 못함

### 증상

승인된 로컬 raster가 있지만 현재 connector는:

- small UTF-8 `content`, 또는
- direct public HTTPS `source_url`

만 받고 local binary parameter를 노출하지 않을 수 있다.

verified primary transport가 사용할 수 없는 상황에서도 사람용 Notion 페이지에는 **저해상도 preview만** 있으면 충분한 경우가 있다.

### 실패/비선호 경로

- private Drive URL을 public direct source처럼 사용,
- temporary source URL을 durable Notion image처럼 저장,
- 성공한 FileUpload를 임의 URL로 재구성,
- preview 하나 때문에 필요 이상의 로컬 bridge/hosting 구조를 강제.

### 해결 패턴

`NOTION_INLINE_SVG_RASTER_PREVIEW_FALLBACK`

```text
approved local raster
→ downscale/compress raster
→ embed raster data URI inside small UTF-8 SVG
→ create-attachment(content=SVG)
→ require uploaded status
→ consume returned file-upload:// directly
→ exact destination fetch
→ require Notion-owned prod-files-secure readback
```

이 방식은 출처 프로젝트에서 여러 low-resolution visual preview에 대해 server readback까지 재현됐다.

### 증거 ceiling

반드시 분리한다.

```text
SERVER_ATTACHMENT: upload result only
DESTINATION_READBACK: target fetch only
HIGH_RES_PIXEL_EQUIVALENT: NOT_PROVEN
READBACK_PASS != HUMAN_VISIBLE_PASS
```

SVG wrapper가 성공했다고 production-quality raster 원본이 Notion에 들어간 것으로 주장하지 않는다.

### 비적용

- high-resolution source 자체가 durable requirement,
- target client가 SVG/data URI를 허용하지 않음,
- typed binary / verified public transport가 이미 적합함,
- inline ceiling을 맞추면 중요한 visual information이 손상됨.

## 장기 교훈

### 1. 스타일 통일은 pixel density 통일이 아니다

Key art와 gameplay의 세부 표현이 달라도 `identity / motif / palette / hierarchy`가 같은 owner를 따르면 한 IP로 이어질 수 있다.

### 2. variant 생성 전에 ownership을 분리한다

AI에게 여러 variant를 만들게 하기 전에 무엇이 **절대 유지되는 identity**이고 무엇이 **추가/제거 가능한 layer**인지 먼저 고정한다.

### 3. 최종 누적 상태가 별도 acceptance다

각 variant가 individually good인 것만으로는 부족하다. 동시에 누적되는 제품이면 final composite를 따로 검증한다.

### 4. 전달 fallback은 evidence를 낮추는 편법이 아니다

Preview fallback을 썼다면 completion claim도 preview 수준으로 제한한다. Server readback과 human-visible pixels, low-res와 high-res는 각각 다른 증거다.

## 재발 방지 라우팅

- 캐릭터 variant / class visual / faction visual → `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`의 persistent-character gate 확인.
- Notion image delivery에서 local binary gap → `NOTION_CONNECTOR_IMAGE_DELIVERY_CORRECTION_2026-08-22.md`의 primary route → preview-only SVG fallback → local bridge 순으로 조건 비교.
- 성공한 이미지라도 project approval / Notion delivery / runtime integration / human-visible evidence를 서로 승격하지 않는다.
