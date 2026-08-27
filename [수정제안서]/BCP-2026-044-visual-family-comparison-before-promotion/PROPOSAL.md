# BCP-2026-044 · 프로젝트 시각군 비교를 통한 후보 승격 전 Drift 차단

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 기준 커밋: `09a5f61ef4ca1fdb5cd6e785fa1b3742c7accbb9`
- 제출일: `2026-08-27`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`

## 관찰과 증거

한 실제 게임 소비처용 초상 후보가 개별 기존 fallback 이미지와는 역할·구도상 연결됐지만, 현재 프로젝트의 승인된 캐릭터·카드·전투 화면군과 함께 비교하지 않아 팔레트, 명암, 종이/수묵 재질, 선 밀도에서 눈에 띄는 이질감을 보였다.

현재 Base의 visual-anchor pipeline은 global/layer anchor와 style-continuity review를 요구한다. 그러나 candidate를 보존·Notion 전달·asset 승격하기 전에 **서로 다른 두 개 이상의 관련 승인 visual surface**와 대조해 blocking drift를 판정하는 최소 비교 receipt는 명시하지 않는다.

## 일반화 후보

프로젝트 범위의 생성·편집 후보는 current global style anchor와 관련 surface/layer anchor를 실제 preview 또는 source binary로 읽은 뒤, candidate 승격 전에 다음 축의 짧은 `VISUAL_FAMILY_COMPARISON_RECEIPT`를 남긴다.

```yaml
reference_ids: [at_least_two_related_approved_references]
axes:
  - palette_and_value_hierarchy
  - line_shape_material_language
  - lighting_and_negative_space
  - framing_and_runtime_crop_readability
blocking_drift: []
result: PASS | REVISION_REQUIRED | REJECTED | BLOCKED_UNVERIFIED
```

- 실제 consumer는 제작 필요성과 기능 적합성을 확인하지만, 단독으로 project visual family 적합성을 증명하지 않는다.
- 하나라도 blocking axis에서 어긋나면 candidate는 `REVISION_REQUIRED` 또는 `REJECTED`이며, `PROJECT_ASSET_APPROVED`, runtime route, 승인 Notion record로 승격하지 않는다.
- 기준이 부족하거나 preview/binary를 읽지 못하면 `BLOCKED_UNVERIFIED`이며, 기억이나 draft·rejected image를 앵커로 추정하지 않는다.

## 프로젝트 전용으로 남길 내용

- 특정 게임의 인물, 파일 경로, 이미지명, 색상값, 문서/Notion ID, runtime route
- 어떤 candidate가 실제로 거절됐는지와 해당 프로젝트의 사용자가 내린 미감 판단
- 해당 게임의 고유한 수묵·전술 UI 어휘와 사용 플랫폼

## 적용 조건과 비사용 조건

적용:

- current project visual canon과 실제 consumer가 확인된 생성·편집 candidate
- 후보를 Notion/asset record에 전달하거나 `APPROVED_CANDIDATE` 이상으로 승격하려는 경우
- 동일 project 내 global grammar와 layer/surface 표현 모두가 관련된 경우

비사용:

- 단순 파일 경로·상태·메타데이터 정리
- 생성하지 않는 결정론적 crop/mask/resample이며 출력이 승인 source의 정체성·팔레트·재질을 바꾸지 않는 경우
- 승인된 canon이 없어 concept comparison 자체가 목적일 때; 이 경우 anchor lock 전에는 candidate 승격을 하지 않는다

## 반례와 위험

- 모든 layer를 같은 질감과 렌더 밀도로 강제하면 UI, VFX, marketing 등 다른 layer의 목적을 해친다. 따라서 두 reference는 동일한 픽셀 표현이 아니라 현재 요청에 관련된 global/layer 역할을 대표해야 한다.
- 두 reference가 서로 충돌하면 숫자 다수결로 해결하지 않고 `VISUAL_CANONICAL_CONFLICT`로 둔다.
- 자동 유사도 점수만으로 미감·가독성·runtime crop을 판정하지 않는다. receipt는 실제 preview/readback과 사람 또는 명시된 review judgment를 남긴다.
- 외부 reference는 권리·유사성 경계가 별도이므로 내부 approved project reference를 대체하지 않는다.

## 영향 범위와 검증

예상 owner는 기존 thin owner `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`와 candidate review/continuity reference다. 새 visual canon, 새 provider, 새 자동 승인 또는 batch 생성 권한은 만들지 않는다.

구현 시 검증:

1. 두 개 미만의 관련 승인 reference 또는 unreadable preview/binary면 PASS가 불가한지 regression으로 확인한다.
2. consumer 적합하지만 palette/value/line/material/crop 중 blocking drift가 있는 candidate가 promotion되지 않는지 확인한다.
3. related layer variation은 허용하되 project global grammar가 보존되는 대표 사례와, anchor conflict 사례를 함께 확인한다.
4. 기존 one-output, no-auto-chain, candidate/approval/runtime 분리와 external-reference rights 경계가 비퇴행인지 전체 regression으로 확인한다.

## 필요한 도구·파일·권한

- 필요 항목: 기존 Base 문서·test와 승인 visual preview/source readback.
- 필요한 이유: 실제 reference를 보지 않은 추정 비교를 막고 receipt를 검증하기 위해서다.
- 설치·적용 방법: 새 의존성 없이 기존 visual-anchor owner와 focused regression에 최소 항목을 추가한다.
- 설치 후 확인 명령: Base의 focused visual-anchor regression과 전체 core regression.
- 최소 권한: project-local current approved visual preview/readback 접근; 외부 source 업로드·runtime 변경 권한은 필요 없다.

## 승인과 구현

- 사용자 승인 근거: `미승인 — proposal-only stage`
- 구현 PR: `없음`
- 롤백: 후속 구현의 receipt requirement와 focused regression만 revert한다. 기존 anchor resolution, candidate lifecycle, approval boundary는 유지한다.
