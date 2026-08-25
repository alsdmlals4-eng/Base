# BCP-2026-033 — Visual Canon Approval & Handoff Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 출처 Decision: `OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01`
- 출처 작업 PR: `alsdmlals4-eng/omenward#210`
- 출처 관찰 commit: `315d5e48b2a2d49f9d9863f3d07b66ba651bf9f7`
- 기준 Base main: `80e51d99e0f9c4dc2f675e0f9ce6467a7c1dfe0f`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- active Base implementation: `NOT_AUTHORIZED`
- 추가 금전 비용: `0`

## 기존 BCP와의 관계

Base에는 이미 `BCP-2026-032-ai-visual-continuity-and-notion-preview-fallback`이 존재하고 `APPROVED_FOR_IMPLEMENTATION` 상태다. #032는 주로 다음을 소유한다.

- persistent protagonist identity를 additive visual layer로 보존하는 규칙;
- Notion connector의 inline SVG raster **preview transport fallback**.

이 BCP-033은 그것을 복제하지 않는다. 별도 문제는 **사용자가 한 시각 방향/Reference를 승인한 뒤, 오래된 visual/document가 남아 있는 프로젝트에서 current canon·supersession·asset locator·new-session handoff를 어떻게 잃지 않는가**다.

따라서:

```text
BCP-032 = visual identity continuity + Notion preview transport fallback
BCP-033 = approved visual canon persistence + explicit supersession + new-session refetch/handoff integrity
```

BCP-032의 preview fallback 구현 owner/규칙을 재정의하거나 확장하지 않는다.

## 문제

프로젝트의 시각 정본이 여러 세션에 걸쳐 발전할 때, 최신 사용자 승인보다 오래된 이미지/문서가 더 눈에 띄는 위치에 남으면 다음 오류가 재발할 수 있다.

1. 오래된 North Star/시안이 current canon처럼 읽힌다.
2. 최신 승인 Decision은 repository에 있지만 사람이 보는 Home/Visual Bible 첫 화면은 오래된 상태다.
3. 승인 이미지는 대화 산출물에만 있고 stable Asset ID/full-resolution locator/hash가 없다.
4. 새 이미지 생성 시 실제 승인 이미지를 refetch하지 않고 prose memory만으로 스타일을 재구성한다.
5. 무엇이 `RETAIN / SUPERSEDE / REFERENCE_ONLY`인지 명시되지 않아 과거 규칙이 다음 세션에서 부활한다.
6. user visual approval이 runtime readability/human usability/rights PASS로 잘못 승격될 수 있다.

OMENWARD에서는 실제로 generic fantasy/RPG 및 잘못된 art lineage 쪽으로 visual generation이 drift했고, 사용자가 `프로젝트랑 노션에서 시안부터 확인`하도록 작업 순서를 교정했다. 이후 current Decision + approved Asset ID + Notion current override first + repository router + new-session handoff를 함께 기록하자 복원 경계가 명확해졌다.

상세 evidence:
`[수정제안서]/BCP-2026-033-visual-canon-approval-and-handoff-integrity/evidence/OMENWARD_VISUAL_CANON_HANDOFF_LESSONS.md`

## 일반화 후보

새 Skill을 기본안으로 만들지 않고 기존 project intake/design-document/UI-art/handoff owner에 다음 closeout invariant를 흡수하는 방안을 제안한다.

```text
USER_APPROVES_VISUAL_DIRECTION_OR_REFERENCE
→ stable Decision ID + Asset ID
→ durable full-resolution asset locator + optional hash
→ explicit RETAIN / SUPERSEDE / REFERENCE_ONLY boundaries
→ update repository high-authority visual router
→ place current approved visual/override before legacy visuals on human-facing surface
→ preserve legacy visual lineage without treating it as current
→ destination readback of structured locator + human visual surface
→ new-session handoff requires approved asset refetch before further generation
→ keep visual approval separate from runtime/human/rights evidence
```

Candidate markers:

- `APPROVED_VISUAL_ASSET_REQUIRED_FOR_HANDOFF`
- `VISUAL_SUPERSESSION_BOUNDARY_REQUIRED`
- `HUMAN_SURFACE_CURRENT_OVERRIDE_FIRST`
- `APPROVED_VISUAL_REFETCH_BEFORE_GENERATION`
- `VISUAL_APPROVAL_EVIDENCE_SPLIT`
- `VISUAL_HANDOFF_DESTINATION_READBACK`

## 최소 3안 비교

| 안 | 장점 | 위험·비용 | 판정 |
| --- | --- | --- | --- |
| A. 승인 이미지만 파일로 보존 | 단순 | old canon/supersession/router/new-session drift 해결 못함 | `REJECT` |
| B. 과거 visual 문서를 모두 삭제/전면 재작성 | current는 명확 | lineage 손실, 큰 churn, owner 충돌 | `REJECT` |
| C. Asset+Decision + current override first + explicit supersession + handoff/refetch/readback | lineage와 current를 동시에 보존, 재생성 drift 감소 | 소량의 metadata/handoff 비용 | `ADOPT` |

## 프로젝트 전용으로 남길 내용

Base로 승격하지 않는다.

- OMENWARD의 3개 전선, per-front minimap, 3×3 roulette.
- Omen Warden/긴 지휘 깃발/Veil 세계관.
- Fantasy/Magic/SD Tactical Pixel 그림체와 palette.
- OMENWARD Asset/Decision/Notion/Drive ID.
- 특정 게임 UI geometry/병종/건물.

## 비사용 조건 / 반례

- throwaway exploration/moodboard이며 사용자가 canon/reference로 승인하지 않은 경우.
- visual authority가 변하지 않은 순수 code/data 변경.
- Notion 미사용 프로젝트 — 프로젝트가 선언한 human-facing surface로 대체한다.
- full-resolution binary를 Git repository에 강제로 넣는 규칙으로 사용하지 않는다.
- 오래된 visual에 감사/계보 가치가 있으면 삭제 대신 `SUPERSEDED`/`REFERENCE_ONLY`를 우선한다.
- prompt 자체를 visual canon으로 승격하지 않는다.

## BCP-032와 중복 금지 경계

이 제안은 다음을 구현 대상으로 삼지 않는다.

- SVG/data-URI preview encoding 방법;
- Notion connector binary/preview transport 선택;
- persistent-character additive-layer visual identity;
- high-resolution Notion upload capability.

해당 영역은 BCP-032와 기존 Notion visual delivery owner를 따른다.

## 예상 영향 범위

승인 후 implementation 후보 owner:

- `skills/managing-project-intake-and-work-contract/` — visual task 진입 시 current approved asset/reference refetch 및 supersession 확인.
- `skills/managing-design-documents/` — Decision/Asset/human-surface sync + current override + destination readback.
- existing UI/art audit owner — candidate가 current approved reference와의 retained/superseded boundary를 지키는지 비교.
- handoff/continuation owner — Asset ID/locator/supersession/new-session refetch 보존.

실제 owner/파일/테스트 변경은 별도 review와 `APPROVED_FOR_IMPLEMENTATION` 이후 결정한다.

## 검증 제안

승인 후 구현 시 focused regression은 최소 다음을 증명해야 한다.

1. approved visual Decision이 있으면 handoff에 Asset ID/locator/supersession가 존재한다.
2. legacy visual이 남아 있어도 current human surface가 current override/visual을 먼저 노출한다.
3. visual approval과 runtime/human/rights evidence가 별도다.
4. 다음 visual generation은 prose memory가 아니라 current approved reference refetch를 요구한다.
5. Notion 미사용 프로젝트에 과도한 결합을 만들지 않는다.
6. 프로젝트 고유 art/content를 Base로 복제하지 않는다.
7. BCP-032 preview transport owner와 중복/충돌하지 않는다.

## 비용·보안·권리

- 신규 SaaS/dependency/runtime 없음.
- 추가 비용 0.
- binary 저장 위치는 프로젝트 정책 유지.
- AI/external visual rights review는 별도 evidence이며 자동 승인하지 않는다.
- temporary signed URL을 durable authority locator로 고정하지 않는다.

## 승인과 구현

- 현재 상태: `SUBMITTED`.
- 사용자 요청 근거: OMENWARD closeout에서 `Base 승격, 문제-교훈 자료도 잘 올려줘` 명시.
- 이 요청은 Base **제안 제출·evidence 보존** 권한으로 해석한다.
- active Base Method/Skill/Template/Tool/Test 변경은 별도 `APPROVED_FOR_IMPLEMENTATION` gate가 필요하다.
- 구현 권한: `NOT_AUTHORIZED_IN_THIS_PROPOSAL`.
