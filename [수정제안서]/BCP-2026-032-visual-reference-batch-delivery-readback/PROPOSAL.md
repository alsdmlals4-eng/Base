# BCP-2026-032 · Visual Reference Batch & Delivery Readback

## 상태

`SUBMITTED`

- source project: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- source project evidence head: `fddd42d27721200f5c49f1dbf7c075b9ba61794d` (`docs/visual-production-handoff-20260825` workstream)
- observed Base main at extraction: `af013a311dd2dadd991080e92bacb0572f0c2f69`
- implementation authorization: `NONE`
- approval_ref: `PENDING_USER_REVIEW_OF_THIS_BCP`

이 제안은 프로젝트에서 실제로 수행된 시각 제작/승인/Notion 전달 과정을 Base 공용 원리 후보로 추출한다. **프로젝트 고유 아트 스타일·수치·캐릭터·이미지·ID를 Base에 복사하지 않는다.** 이 PR은 proposal 단계이며 `IMAGE_CONVERSATION_APPROVAL_GATE.md`, Art Direction Guide, Skill, Template, Test의 활성 동작을 바꾸지 않는다.

---

## 1. 출처·관찰

십보강호 시각 작업에서 다음 순서가 실제로 수행됐다.

1. 프로젝트/Notion/runtime 구조를 읽고 대표 전투 화면을 탐색했다.
2. 캐릭터가 짧고 카드가 너무 커 전장 존재감이 약해지는 문제를 사용자 피드백으로 수정했다.
3. 배경/캐릭터/UI를 같은 renderer로 밀지 않고 역할별 treatment로 분리했다.
4. 대표 전투 화면, Character Master, 작은 행동 삽화 시트, common clean plate를 먼저 사용자 승인했다.
5. 대량 상대/무공/Route 제작은 이 reference set 이후로 미뤘다.
6. 초기 Base image gate의 1장 cadence 대신, 사용자가 명시적으로 `한번에 3장씩`을 요청한 이후 독립 brief가 있는 최대 3장 묶음으로 전환했다.
7. Notion 전달 뒤 page image block 존재만 확인하지 않고, 첨부 파일을 다시 읽어 non-empty image payload가 존재하는지 검증했다.

Project evidence:

- `docs/18_VISUAL_PRODUCTION_HANDOFF_2026-08-25.md`
- `docs/planning-data/current_visual_production_handoff_20260825.json`
- `docs/reviews/2026-08-25_VISUAL_PRODUCTION_PROBLEMS_AND_LESSONS.md`
- exact Project Notion Home / Visual Bible / Asset Library destination readback

---

## 2. 공용화 후보 A · `REFERENCE_SET_BEFORE_SCALE`

### 제안

반복 자산을 대량 생산하기 전에 프로젝트의 주요 소비처를 대표하는 **작은 reference set**을 먼저 승인한다.

예시 구조:

```text
representative screen/composition
+ character master or subject master
+ repeated small-format element sample sheet
+ representative environment/clean plate
→ user/style approval
→ bounded repeated production
```

위 4종은 고정 숫자가 아니다. 프로젝트마다 실제 반복 생산 병목을 대표하는 `3~5`개 정도의 최소 reference를 선택한다.

### 기대 효과

- 캐릭터 비율·정보 밀도·배경 대비가 잠기기 전에 15~100개의 자산을 만드는 낭비를 줄인다.
- 한 장의 key art만 승인하고 UI/아이콘/작은 카드로 확장할 때 생기는 scale mismatch를 조기에 발견한다.
- `Character Master → derivatives` 같은 재사용 파이프라인을 실제 소비처와 함께 검증한다.

### 비사용/반례

- 단일 이미지 한 장만 필요한 작업.
- 반복 생산이 없고 파생 소비처가 없는 작업.
- 이미 동일 format의 승인 production set이 충분히 존재하는 작업.

---

## 3. 공용화 후보 B · `LAYERED_VISUAL_STYLE_RESPONSIBILITY`

### 제안

Visual consistency를 **모든 레이어의 동일 renderer/style**로 정의하지 않는다. 배경·주 피사체·UI·VFX가 각자 다른 treatment를 사용할 수 있으며, 다음 공통 계약으로 제품 언어를 통일한다.

- value/contrast hierarchy
- semantic color roles
- material/edge vocabulary
- proportions and silhouette rules
- composition ownership
- layer priority
- feedback intensity ceiling

### 프로젝트 관찰

십보강호에서는 저대비 수묵 배경, 수묵 선화+제한 디더링 캐릭터, 별도 정제 UI가 전체를 같은 도트/수묵 renderer로 만드는 것보다 전투 가독성과 무협 존재감을 동시에 유지했다.

### 위험

레이어별 treatment가 아무 공통 token/계약 없이 독립적으로 설계되면 오히려 collage처럼 보일 수 있다. 따라서 이 원리는 “스타일 자유화”가 아니라 **역할별 책임 분리 + 공통 의미 체계**다.

---

## 4. 공용화 후보 C · `BOUNDED_EXPLICIT_IMAGE_BATCH`

### 현재 Base와의 충돌

현행 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`는 기본적으로:

```text
NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

을 요구한다.

이 기본값은 탐색 초기 drift 방지에 유효하다. 다만 style/reference가 이미 잠긴 반복 제작에서는 사용자 명시 batch 요청이 있어도 대화가 과도하게 잘게 끊길 수 있다.

### 조건부 예외 제안

기본값 `1 image`는 유지하되 다음 조건을 **모두** 만족하면 프로젝트가 정한 작은 bounded batch를 허용하는 방안을 검토한다.

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

십보강호의 source evidence에서는 사용자 명시 cap이 `3`이었다. **Base 공용 숫자로 3을 고정하지 않는다.**

### 기본 1장 유지 조건

아래에서는 계속 1장씩 순차 생성이 더 안전하다.

- style/reference가 아직 잠기지 않음.
- 앞 이미지 승인 결과가 뒤 이미지의 크기/구도/언어를 결정함.
- 서로 다른 제품 표면·아트 방향을 탐색하는 이미지들.
- 사용자가 batch size를 명시하지 않음.
- 한 장의 실패가 이후 전체 생산을 무효화할 가능성이 큼.

### 핵심 보호선

`bounded batch`는 `NO_AUTOMATIC_IMAGE_CHAIN`을 완화하지 않는다. 승인된 batch가 끝나면 반드시 멈추고 사용자 검토를 받는다.

---

## 5. 공용화 후보 D · `NOTION_ATTACHMENT_CONTENT_READBACK`

### 문제

Notion Visual 전달에서 다음 두 상태는 동일하지 않다.

```text
page contains image/file block
!= attachment actually contains a usable visual payload
```

특히 connector/API를 통한 변환·wrapper·temporary upload에서는 빈 파일, 깨진 URL, 잘못된 wrapper, 만료된 임시 파일을 block 존재만으로 놓칠 수 있다.

### 제안

Visual delivery 완료 증거를 최소 다음으로 분리한다.

```text
1. destination page readback
   - expected block exists
   - expected approval/status text exists

2. attachment/content readback where capability exists
   - file is non-empty
   - media payload/type is plausible
   - wrapper/embed actually references image data

3. evidence ceiling
   - preview/readback PASS != source-master preservation
   - preview/readback PASS != runtime integration
```

### 비사용/대체

provider가 첨부 contents readback capability를 제공하지 않으면 이를 가짜 PASS로 만들지 않는다. 그 경우 `DESTINATION_BLOCK_PASS / ATTACHMENT_CONTENT_UNVERIFIED`처럼 분리한다.

---

## 6. 기존 Base와 중복·충돌

### `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`

이미 다음을 소유한다.

- Visual Requirement Gate.
- reuse-first.
- Layer / Provenance.
- Primary Use Gate → Reusable Visual Harvest.

따라서 Candidate A/B는 새 독립 대형 Guide보다 **기존 Guide의 반복 생산/Reference Set 섹션 보강** 후보가 적합하다.

### `IMAGE_CONVERSATION_APPROVAL_GATE.md`

Candidate C가 직접 영향을 주는 owner다. 현행 1장 기본값은 폐기하지 않고 조건부 bounded batch 예외만 추가 검토한다.

### Notion delivery / handoff owners

Candidate D는 이미지 Gate, handoff, Notion delivery 관련 기존 owner 중 **한 곳만 canonical owner로 선정**하고 다른 문서는 링크/consumer로 두어 중복 원장을 만들지 않아야 한다.

---

## 7. 프로젝트 전용으로 남길 요소

다음은 Base에 승격하지 않는다.

- 십보강호의 `3/3/4`, `거리 N`, 무공/절초 시스템.
- 상대 15명이라는 수량.
- 프로젝트의 exact 수묵/세피아/금색 palette.
- 실제 캐릭터 외형 및 승인 이미지.
- `TEN-VIS-A01~A07` ID.
- `5×2 = 10`이라는 게임 고유 행동 UI 최대치.
- 프로젝트에서 사용한 구체 CTA `진행`.

---

## 8. 검증·반례 계획

구현 승인 시 최소 다음을 검증한다.

### Reference Set

- 반복 캐릭터/카드/UI/배경 생산이 있는 프로젝트 예제.
- single-image 작업에서는 불필요한 gate가 되지 않는지.

### Bounded Batch

- default 1장 경로 유지.
- explicit batch size 없으면 batch 금지.
- style lock 없으면 batch 금지.
- batch cap 초과 요청 fail-closed 또는 사용자 재결정.
- batch 이후 automatic next generation 금지.
- dependent chain은 sequential path로 남음.

### Notion Readback

- non-empty valid visual attachment.
- empty/wrong wrapper.
- destination block만 있고 attachment readback 불가.
- preview PASS와 source master/runtime PASS가 분리되는지.

---

## 9. 위험·롤백

### 위험

- batch 예외가 “여러 장 자동 생성 허용”으로 오해될 수 있음.
- reference set이 모든 프로젝트에서 동일 4종 checklist로 굳어질 수 있음.
- Notion content readback을 provider-specific mandatory API로 고정하면 capability portability가 나빠질 수 있음.

### 롤백

- Candidate C가 품질 drift를 늘리면 `GENERATE_EXACTLY_ONE` 기본 경로만 유지하고 bounded batch 예외를 제거할 수 있어야 한다.
- Candidate A/B는 Guide 보강만으로 구현해 기존 프로젝트 계약을 강제 migration하지 않는다.
- Candidate D는 capability-unavailable 상태를 명시하는 evidence language로 유지하고 특정 provider에 hard dependency를 만들지 않는다.

---

## 10. 제안 구현 범위

현재는 **제안만 제출**한다.

사용자/리뷰가 `APPROVED_FOR_IMPLEMENTATION`을 명시하면 별도 구현 PR에서 후보 범위를 좁혀 다음을 검토한다.

1. `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`에 `REFERENCE_SET_BEFORE_SCALE` / layered responsibility 명료화.
2. `IMAGE_CONVERSATION_APPROVAL_GATE.md`에 default-one + conditional bounded batch contract.
3. Notion Visual delivery owner에 attachment content readback evidence language.
4. 관련 contract tests/examples.

승인 전에는 위 활성 owner를 수정하지 않는다.

---

## 11. 사용자 승인 상태

현재 사용자 요청은 “Base 승격, 문제-교훈 자료도 잘 올려줘”였으므로 **공용화 후보 추출과 BCP 제출은 승인된 요청 범위**로 해석한다.

그러나 현행 Base lifecycle은 **제안 제출과 활성 Base 구현을 분리**한다. 따라서 이 문서의 세부 조건을 사용자가 검토/승인하거나 별도 재현 가능한 `approval_ref`가 생기기 전까지 상태는 `SUBMITTED`, 구현은 `NONE`으로 유지한다.
