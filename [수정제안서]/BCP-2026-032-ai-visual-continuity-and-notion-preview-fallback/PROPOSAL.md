# BCP-2026-032 — AI 시각 제작 연속성·Notion Preview Fallback 강화

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/ninja-survival-godot`
- 기준 커밋: `5b7c86e25c53e4a2667f1a70dc59938fc60c4c9a`
- 제출일: `2026-08-25`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴 / 검증(부분)`

## 관찰과 증거

닌자서바이벌의 2026-08-25 Hybrid Visual 작업에서 두 개의 반복 가능한 공용 문제가 확인됐다.

### A. 하나의 지속 캐릭터가 여러 전승/직업/진영 특징을 습득할 때 identity drift

초기 캐릭터 시트는 네 유파를 잘 구분했지만, 각 유파를 서로 다른 전신 캐릭터로 표현하면서 런타임 주인공이 교체되는 것처럼 읽힐 위험이 생겼다.

사용자 피드백과 후속 설계에서 다음 구조가 승인됐다.

```text
persistent base character identity
+ bounded item layer
+ aura / energy layer
+ companion / shadow layer
= accumulated learned traditions
```

핵심은 faction/class/school differentiation과 protagonist continuity를 별도 요구사항으로 다루는 것이다. 강한 최종 단계가 여러 계열에서 동시에 최대치로 겹치면 시각 과밀과 identity 충돌이 생기므로, 프로젝트 규칙에 따라 main/start 계열의 dominant stage와 supporting layers의 위계를 둘 수 있다.

프로젝트 증거: `docs/CURRENT_VISUAL_HANDOFF.md`, `docs/learning/2026-08-25-hybrid-visual-and-notion-delivery-lessons.md` at source commit.

### B. Notion connector에 local binary input이 없을 때 low-resolution durable preview 전달

현재 Notion `create-attachment` surface는 small UTF-8 `content` 또는 direct public HTTPS `source_url`을 받았고, local generated PNG를 직접 binary parameter로 넣는 route는 없었다.

기존 Base owner `NOTION_CONNECTOR_IMAGE_DELIVERY_CORRECTION_2026-08-22.md`의 primary path를 먼저 확인했다. 이번 프로젝트에서는 private Drive source가 Notion server fetch에 적합하지 않았다.

preview 품질로 충분한 경우 다음 bounded fallback이 실제 동작했다.

```text
local approved raster
-> downscale/compress preview
-> embed raster data URI inside UTF-8 SVG
-> create-attachment(content=<svg...>)
-> status=uploaded
-> consume returned file-upload:// directly in page
-> destination fetch
-> Notion-owned prod-files-secure readback
```

Hybrid Key Visual, four-school supporting sheet, SD/action/icon working sheet 모두 Visual Bible에서 Notion-owned `prod-files-secure`로 server readback 됐다.

단, 이 증거는 low-resolution durable preview까지만 증명한다. high-resolution pixel-equivalent upload와 Android/iOS/browser human-visible pixels는 증명하지 않는다.

## 일반화 후보

### Candidate 1 — `PERSISTENT_CHARACTER_ADDITIVE_VISUAL_LAYER_GATE`

적용 대상:
- 하나의 주인공이 여러 class/faction/tradition/stance/affinity를 누적 습득하는 게임,
- key art와 gameplay rendering density가 다른 프로젝트,
- AI 이미지 제작에서 반복 시 character identity가 drift하기 쉬운 프로젝트.

공용 원칙:
1. faction differentiation 전에 persistent character identity owner를 명시한다.
2. 얼굴/머리/체형/core outfit 같은 identity invariant와 장비/aura/companion/effect 같은 additive layer를 분리한다.
3. 모든 누적 layer가 동시에 존재하는 final composite를 별도 acceptance로 검토한다.
4. small gameplay scale에서 silhouette/readability를 검토한다.
5. key art와 gameplay가 다른 rendering style을 써도 identity/motif/palette/hierarchy invariant로 연결한다.

### Candidate 2 — `NOTION_INLINE_SVG_RASTER_PREVIEW_FALLBACK`

적용 대상:
- current connector가 local binary parameter를 노출하지 않음,
- public HTTPS transport를 만들 수 없거나 만들 필요가 없음,
- **low-resolution preview만으로 해당 Notion human-facing surface 목적이 충족됨**,
- SVG/data-URI 크기가 inline text attachment limit 안에 들어감.

공용 원칙:
1. existing typed binary / verified primary transport를 먼저 사용한다.
2. fallback은 preview-only로 명시한다.
3. raster derivative를 bounded resolution/quality로 축소한다.
4. self-contained SVG에 raster data URI를 넣어 `content` upload를 사용한다.
5. connector-returned `file-upload://` source를 그대로 소비한다.
6. destination readback에서 Notion-owned file을 확인한다.
7. `SERVER_READBACK_PASS != HUMAN_VISIBLE_PASS`와 high-resolution limitation을 유지한다.

## 프로젝트 전용으로 남길 내용

Base로 올리지 않는다:

- 닌자서바이벌의 봉마/천술/귀인/흑영 이름,
- 부적/식신/차크라/오니가면/귀기/그림자/어둠 motif,
- `Trace Stage 3 = starting school only`라는 제품 규칙,
- 2~3등신 SD라는 프로젝트별 렌더 비율,
- 특정 Notion page ID/file upload ID,
- 닌자서바이벌 색상·로고·키아트 구성.

## 적용 조건과 비사용 조건

### Persistent character layering

사용:
- one persistent protagonist가 여러 시각 상태를 누적할 때.

비사용:
- 실제로 서로 다른 playable characters를 선택하는 게임,
- transformation 자체가 body/identity replacement인 제품 약속,
- layer 합성보다 완전 교체가 UX상 더 명확한 bounded state.

### Inline SVG raster preview

사용:
- low-res durable preview가 acceptance에 충분하고 current connector surface가 text attachment를 지원할 때.

비사용:
- production-quality/high-resolution 원본 자체가 Notion에 필요할 때,
- SVG/data URI rendering이 target client에서 금지/실패할 때,
- typed binary upload 또는 검증된 public transport가 이미 더 강한 evidence로 사용 가능할 때,
- inline size ceiling을 맞추기 위해 의미 있는 시각 정보가 손상될 때.

## 반례와 위험

- additive layer 규칙을 과도하게 일반화하면 실제 class transformation fantasy를 약화시킬 수 있다.
- 모든 layer를 한 화면에 보이게 하는 것 자체가 목표가 아니며, 우선순위/LOD/activation state가 필요할 수 있다.
- SVG embedded raster는 connector/client 정책 변화에 취약할 수 있다.
- server readback만으로 실제 client rendering을 보장하면 안 된다.
- preview fallback 성공을 high-resolution asset delivery 성공으로 승격하면 evidence inflation이다.
- existing Base Notion primary route를 대체하면 오히려 capability regression이다.

## 영향 범위와 검증

승인된 최소 구현 owner:

1. `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`의 `Identity-preserving image edits` 뒤에 persistent-character additive-layer gate를 **추가**한다.
2. `docs/knowledge/game-development/NOTION_CONNECTOR_IMAGE_DELIVERY_CORRECTION_2026-08-22.md`에 inline SVG raster **preview-only fallback**을 secondary route로 추가한다.
3. 재사용 가능한 문제/해결/교훈 case를 Base knowledge case에 기록한다.
4. 기존 primary Notion transport, local bridge fallback, `READBACK_PASS != HUMAN_VISIBLE_PASS`를 삭제/약화하지 않는다.
5. 신규 Skill·MCP·서비스·대시보드는 만들지 않는다.

검증:
- 기존 visual requirement/Notion delivery contract tests non-regression,
- 새 계약 문구를 요구하는 focused test RED → owner 변경 후 GREEN,
- Base full relevant test regression,
- proposal/source provenance readback.

## Proposal review — 2026-08-25

최소 5회 whole-state review 결과:

1. **Source evidence:** project merge `5b7c86e...`와 Notion `prod-files-secure` destination readback 증거가 있고, runtime/human-visible 범위는 분리되어 있다.
2. **Generalization boundary:** 닌자서바이벌의 유파명·motif·Stage-3·SD 비율·색/로고는 Base 승격 대상에서 제외되어 있다.
3. **Existing owner reuse:** visual identity 원칙은 기존 `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`, preview fallback은 기존 Notion connector delivery correction owner에 흡수 가능하며 새 Skill/도구가 필요 없다.
4. **Evidence ceiling / counterexample:** true transformation/multi-character 게임, high-resolution delivery, target-client SVG 실패 등 비사용 조건이 명시되어 있다.
5. **Regression / rollback:** 기존 typed binary / verified transport를 primary로 유지하고 additive section + focused test만 추가하므로 rollback과 non-regression 경계가 명확하다.

새 blocking finding: `0`.

검토 판정: `APPROVED_FOR_IMPLEMENTATION`.

## 필요한 도구·파일·권한

- 필요 항목: Base GitHub repository write + PR workflow
- 필요한 이유: BCP 승인과 별도 구현 PR
- 설치·적용 방법: 신규 도구 설치 없음
- 설치 후 확인 명령: 해당 없음; repository-native tests/CI 사용
- 최소 권한: 현재 Base repository branch/PR 작성 및 안전 병합 권한

## 승인과 구현

- 사용자 승인 근거: `2026-08-25 닌자서바이벌 프로젝트 closeout current task — "Base 승격, 문제-교훈 자료도 잘 올려줘"`
- proposal PR: `https://github.com/alsdmlals4-eng/Base/pull/683` · MERGED at `104d63c3136ea6b4b630d4721a6eb2380a17ab17`
- 검토 판정: `APPROVED_FOR_IMPLEMENTATION`
- approval_ref: `[수정제안서]/BCP-2026-032-ai-visual-continuity-and-notion-preview-fallback/PROPOSAL.md#승인과-구현 (2026-08-25 current task user instruction; proposal PR #683 merged)`
- 구현 PR: `없음 — approval merge 뒤 별도 PR`
- 롤백: approval은 proposal/registry status revert; 구현은 owner별 additive section과 focused test를 implementation PR 단위로 revert.
