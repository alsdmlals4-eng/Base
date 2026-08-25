# BCP-2026-032-visual-reference-batch-delivery-readback — Visual Reference Batch & Delivery Readback

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 기준 증거 커밋: `fddd42d27721200f5c49f1dbf7c075b9ba61794d`
- 후속 형식 교정 커밋: `a81d7f390fa7c8a67011f811ee877ee85052b424` — machine JSON pretty-print only
- 관련 프로젝트 PR: `https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves/pull/201`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- 지식 상태: `패턴 후보`
- 구현 권한: `NONE`
- approval_ref: `PENDING_USER_REVIEW_OF_THIS_BCP`

이 제안은 십보강호에서 실제 수행된 시각 제작·승인·Notion 전달 과정을 Base 공용 원리 후보로 추출한다. 프로젝트 고유 아트 스타일·수치·캐릭터·이미지·ID는 Base에 복사하지 않는다. 이 PR은 proposal 단계이며 `IMAGE_CONVERSATION_APPROVAL_GATE.md`, Art Direction Guide, Skill, Template, Test의 활성 동작을 바꾸지 않는다.

## 관찰과 증거

십보강호 시각 작업에서 다음 순서가 실제로 수행됐다.

1. 프로젝트 GitHub/Notion/runtime 구조를 먼저 읽고 대표 전투 화면을 탐색했다.
2. 초기 시안에서 캐릭터가 짧고 행동 카드가 너무 커 전장 존재감이 약해지는 문제가 사용자 피드백으로 드러났다.
3. 배경·캐릭터·UI를 같은 renderer로 밀지 않고 역할별 treatment로 분리했다.
4. 대표 전투 화면, Character Master, 작은 행동 삽화 시트, common clean plate를 먼저 사용자 승인했다.
5. 대량 상대·무공·Route 제작은 이 reference set 이후로 미뤘다.
6. Base의 기존 1장 승인 cadence를 그대로 자동 적용하지 않고, 사용자가 명시적으로 `한번에 3장씩`을 요청한 이후 독립 brief가 있는 작은 묶음으로 전환했다.
7. Notion 전달 뒤 page image block 존재만 확인하지 않고, 첨부 파일을 다시 읽어 non-empty visual payload가 존재하는지 확인했다.
8. 사용자 승인 Reference와 runtime/source-master/Human-device PASS를 서로 다른 상태로 유지했다.

Project evidence:

- `docs/18_VISUAL_PRODUCTION_HANDOFF_2026-08-25.md`
- `docs/planning-data/current_visual_production_handoff_20260825.json`
- `docs/reviews/2026-08-25_VISUAL_PRODUCTION_PROBLEMS_AND_LESSONS.md`
- exact Project Notion Home / Visual Bible / Asset Library destination readback
- 네 Notion 첨부의 content readback: non-empty SVG + embedded JPEG image data 확인

### Existing Base Coverage

기존 `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`는 이미 다음을 소유한다.

- Visual Requirement Gate
- reuse-first
- Layer / Provenance
- Primary Use Gate → Reusable Visual Harvest

기존 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`는 기본적으로 다음을 소유한다.

```text
NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

따라서 새 broad Skill이나 별도 대형 Visual Guide를 만드는 것보다 기존 owner의 조건/예외/검증 언어를 좁게 보강하는 것이 우선이다.

### Existing Solution Verdict

`ABSORB_WITH_CONDITIONAL_EXTENSION`

- reference-set/layer responsibility는 기존 Art Direction owner에 흡수 후보.
- bounded batch는 기존 Image Conversation Gate의 **기본 1장 규칙을 폐기하지 않는 조건부 예외** 후보.
- Notion attachment readback은 기존 handoff/delivery owner 중 단일 canonical owner를 정해 흡수 후보.

## 일반화 후보

### Candidate A · `REFERENCE_SET_BEFORE_SCALE`

반복 자산을 대량 생산하기 전에 프로젝트의 주요 소비처를 대표하는 작은 reference set을 먼저 승인한다.

예시 구조:

```text
representative screen/composition
+ character or subject master
+ repeated small-format element sample sheet
+ representative environment/clean plate
→ user/style approval
→ bounded repeated production
```

위 4종은 고정 숫자가 아니다. 프로젝트마다 실제 반복 생산 병목을 대표하는 `3~5`개 정도의 최소 reference를 선택한다.

기대 효과:

- 캐릭터 비율·정보 밀도·배경 대비가 잠기기 전에 다량 자산을 만드는 낭비를 줄인다.
- key art 한 장만 승인하고 UI/아이콘/작은 카드로 확장할 때 생기는 scale mismatch를 조기에 발견한다.
- `Character Master → derivatives` 같은 재사용 파이프라인을 실제 소비처와 함께 검증한다.

### Candidate B · `LAYERED_VISUAL_STYLE_RESPONSIBILITY`

Visual consistency를 모든 레이어의 동일 renderer/style로 정의하지 않는다. 배경·주 피사체·UI·VFX가 각자 다른 treatment를 사용할 수 있으며 다음 공통 계약으로 제품 언어를 통일한다.

- value/contrast hierarchy
- semantic color roles
- material/edge vocabulary
- proportions and silhouette rules
- composition ownership
- layer priority
- feedback intensity ceiling

핵심은 “스타일 자유화”가 아니라 **역할별 책임 분리 + 공통 의미 체계**다.

### Candidate C · `BOUNDED_EXPLICIT_IMAGE_BATCH`

현행 `GENERATE_EXACTLY_ONE`을 기본값으로 유지하되, 다음 조건을 모두 만족하면 프로젝트가 정한 작은 bounded batch를 허용하는 방안을 검토한다.

```yaml
reference_style_locked: true
user_explicit_batch_size: required
batch_size_cap: small_project_defined_cap
item_briefs_independent_and_complete: true
same_approved_reference_family: true
automatic_next_batch: false
review_after_batch: required
per_item_accept_modify_reject: required
```

십보강호의 source evidence에서는 사용자가 cap `3`을 명시했다. Base 공용 숫자로 3을 고정하지 않는다.

`bounded batch`는 `NO_AUTOMATIC_IMAGE_CHAIN`을 완화하지 않는다. 승인된 batch가 끝나면 반드시 멈추고 사용자 검토를 받는다.

### Candidate D · `NOTION_ATTACHMENT_CONTENT_READBACK`

Visual delivery의 두 상태를 분리한다.

```text
page contains image/file block
!= attachment actually contains a usable visual payload
```

가능하면 전달 완료 증거를 다음으로 나눈다.

```text
1. destination page readback
   - expected block exists
   - expected approval/status text exists

2. attachment/content readback where capability exists
   - file is non-empty
   - media payload/type is plausible
   - wrapper/embed actually references visual data

3. evidence ceiling
   - preview/readback PASS != source-master preservation
   - preview/readback PASS != runtime integration
```

## 프로젝트 전용으로 남길 내용

다음은 Base 공용 규칙으로 승격하지 않는다.

- 십보강호의 `3/3/4`, `거리 N`, 무공/절초 시스템
- 상대 15명이라는 수량
- 프로젝트 exact 수묵/세피아/금색 palette
- 실제 캐릭터 외형 및 승인 이미지
- `TEN-VIS-A01~A07` ID
- `5×2 = 10`이라는 게임 고유 행동 UI 최대치
- 프로젝트에서 사용한 구체 CTA `진행`

## 적용 조건과 비사용 조건

### Use When — Reference Set

- 동일한 캐릭터/카드/아이콘/환경을 반복 생산한다.
- 대표 화면과 실제 반복 asset format 사이의 scale mismatch 가능성이 있다.
- 한 번의 잘못된 style lock이 다수 자산 폐기로 이어질 수 있다.

### Do Not Use — Reference Set

- 단일 이미지 한 장만 필요한 작업.
- 반복 생산이 없고 파생 소비처가 없는 작업.
- 이미 동일 format의 승인 production set이 충분히 존재하는 작업.

### Use When — Bounded Batch

- style/reference가 이미 승인돼 있다.
- 사용자가 batch size를 명시했다.
- 각 항목 brief가 독립적으로 완결되어 있다.
- 같은 reference family를 공유한다.
- batch 결과 뒤 검토/중단이 가능하다.

### Default Back To One Image

- style/reference가 아직 잠기지 않았다.
- 앞 이미지 승인 결과가 뒤 이미지의 크기·구도·언어를 결정한다.
- 서로 다른 제품 표면·아트 방향을 탐색한다.
- 사용자가 batch size를 명시하지 않았다.
- 한 장 실패가 이후 전체 생산을 무효화할 가능성이 크다.

### Use When — Attachment Readback

- Notion/외부 workspace에 시각 Reference를 전달한다.
- connector/API 변환·wrapper·temporary upload 경로가 있다.
- 후속 세션이 전달된 이미지 자체를 기준으로 재개해야 한다.

### Capability Unavailable

provider가 첨부 content readback을 제공하지 않으면 가짜 PASS를 만들지 않는다.

`DESTINATION_BLOCK_PASS / ATTACHMENT_CONTENT_UNVERIFIED`

처럼 증거를 분리한다.

## 반례와 위험

### Counterexamples

1. style exploration 초기 3개 후보를 한 묶음으로 자동 양산하면 세 이미지가 같은 잘못된 방향으로 drift할 수 있다. 이 경우 1장 Gate가 더 안전하다.
2. 대표 화면이 확정되어야 캐릭터 크기가 결정되는 sequential dependency에서는 bounded batch보다 순차 생성이 맞다.
3. UI가 거의 없는 한 장짜리 일러스트는 layered visual responsibility를 과하게 세분화하면 오히려 부자연스럽다.
4. Notion provider가 attachment bytes/content를 재조회할 수 없는 환경에서는 block+status readback까지만 검증할 수 있다.

### Risks

- bounded batch 예외가 “여러 장 자동 생성 허용”으로 오해될 수 있다.
- reference set이 모든 프로젝트에서 동일한 네 장 checklist로 굳어질 수 있다.
- layer responsibility를 공통 token 없이 적용하면 collage처럼 보일 수 있다.
- attachment content readback을 특정 provider API에 hard dependency로 만들면 portability가 떨어진다.
- preview가 정상이라고 source master/runtime 품질까지 PASS로 과장할 수 있다.

### Mitigation

- default 1장 유지.
- batch 조건을 AND gate로 둔다.
- fixed reference count를 만들지 않는다.
- provider capability unavailable 상태를 명시적으로 허용한다.
- `preview / source master / runtime / Human-device` 증거 층을 분리한다.

## 영향 범위와 검증

### Future Implementation Candidates Only

이번 proposal-only 단계에서는 아래 활성 Base 파일을 변경하지 않는다.

- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- visual handoff/delivery 관련 기존 owner 중 하나
- 관련 contract tests/examples

새 broad Skill은 현재 verdict에서 `REJECT`; existing owner 흡수가 우선이다.

### Validation Plan — Reference Set

1. 반복 캐릭터/카드/UI/배경 생산이 있는 프로젝트 fixture에서 대량 생산 전 최소 reference set gate를 통과한다.
2. single-image fixture에서는 불필요한 mandatory multi-reference gate를 만들지 않는다.
3. reference count를 fixed `4`로 요구하지 않는다.

### Validation Plan — Bounded Batch

1. explicit batch size 없음 → default one image.
2. style lock 없음 → default one image.
3. dependent briefs → sequential one-image path.
4. independent complete briefs + explicit small cap + same reference family → bounded batch eligible.
5. batch 완료 뒤 automatic next generation 금지.
6. batch 내 결과별 accept/modify/reject 가능.

### Validation Plan — Notion Readback

1. destination block + valid non-empty visual attachment → PASS.
2. block만 있고 empty/wrong wrapper → attachment FAIL.
3. destination block은 확인되지만 content readback capability 없음 → `CONTENT_UNVERIFIED`, PASS로 승격 금지.
4. preview PASS와 source-master/runtime PASS가 독립 상태인지 검증.

### Regression Plan

- 기존 `GENERATE_EXACTLY_ONE` 기본 경로를 유지한다.
- 기존 `NO_AUTOMATIC_IMAGE_CHAIN`을 약화하지 않는다.
- 기존 layer/provenance 및 reusable visual harvest 계약을 약화하지 않는다.
- project-specific 숫자/스타일/asset ID를 Base default로 올리지 않는다.

### Rollback

- Candidate C가 품질 drift를 늘리면 bounded batch 예외만 제거하고 기존 1장 Gate로 완전히 돌아갈 수 있어야 한다.
- Candidate A/B는 기존 Art Direction owner의 additive subsection으로만 구현해 기존 프로젝트를 강제 migration하지 않는다.
- Candidate D는 capability-specific implementation을 제거해도 destination readback 기본 계약은 유지할 수 있어야 한다.

## 필요한 도구·파일·권한

- 이미지 제작/승인 기록과 대표 reference set
- 프로젝트 Visual Bible/Asset Library 또는 동등한 human-facing visual owner
- 현재 runtime/UI 구조 문서 또는 구현
- Notion/외부 workspace destination readback capability
- attachment content readback capability가 있으면 해당 provider tool
- Base 활성 owner 수정 권한은 **향후 별도 구현 승인 뒤에만** 필요

## 승인과 구현

### 현재 상태

`SUBMITTED / IMPLEMENTATION_AUTHORITY_NONE`

사용자 요청은 “Base 승격, 문제-교훈 자료도 잘 올려줘”였으므로 다음은 현재 요청 범위에서 수행했다.

- 프로젝트 문제→교훈 증거 기록.
- 프로젝트 handoff 작성.
- Base 공용화 후보 추출.
- BCP registry 등록 및 proposal PR 제출.

그러나 현행 Base lifecycle은 **제안 제출과 활성 Base 구현을 분리**한다. 따라서 이 제안의 세부 조건을 사용자/리뷰가 검토하고 재현 가능한 `approval_ref`를 제공하기 전에는 활성 Guide/Gate/Skill/Test를 수정하지 않는다.

### 향후 구현 승인 시

1. fresh Base main과 open PR concurrency를 다시 확인한다.
2. Existing Solution First를 재수행한다.
3. Candidate A/B/C/D 중 승인된 subset만 구현한다.
4. TDD/contract regression으로 default-one, no-auto-chain, evidence ceiling을 보호한다.
5. implementation PR과 post-merge readback 뒤에만 proposal 상태를 `IMPLEMENTED`로 승격한다.

### 현재 승인 필요 사항

- BCP-2026-032의 어떤 Candidate를 Base 활성 owner에 실제 구현할지에 대한 scoped approval.
- 특히 Candidate C는 현행 image gate 행동을 바꾸므로 명시적 구현 승인 없이는 적용하지 않는다.
