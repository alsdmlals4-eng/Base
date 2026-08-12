# Figma Visual Bible Integration Design

## Goal

Base의 기존 시각 협업·이미지 생성·자산 보존 체계를 깨지 않고, 각 프로젝트의 Figma를 **승인된 시각 레퍼런스, 화면 Flow, GPT 해석 기록, 구현 비교를 모으는 Visual Bible**로 운영한다.

## Existing-solution-first 판정

- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`: Figma/Whimsical의 권위 경계와 visual artifact lifecycle을 이미 소유한다. → **ABSORB**
- `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`: Figma frame/node, Decision, snapshot, status를 이미 추적한다. → **REUSE/EXTEND**
- `skills/designing-art-prompts-and-technique-cards/SKILL.md`: 이미지 생성 전 정본·승인 자산·레퍼런스와 생성 후 QA·Screen Interpretation Review를 이미 소유한다. → **REFACTOR/EXTEND**
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`: 실제 이미지 생성·검수 입력과 승인 동기화를 이미 소유한다. → **EXTEND**
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`: 이미지 bytes의 로컬 후보/승격 권위를 이미 소유한다. → **KEEP SEPARATE**
- 신규 `figma-*` Skill: 기존 정책이 명시적으로 금지하고 책임 중복을 만든다. → **DO NOT BUILD**

동일 Goal로 병렬 생성된 Visual Flow 제안은 별도 PR·Skill로 유지하지 않고 이 Visual Bible 작업에 **ABSORB**한다.

## Authority boundary

```text
GitHub/GDD/Decision
  → 게임 사실·규칙·승인 결정 정본

Figma Visual Bible / Project Visual Flow Workspace
  → 승인 시각 방향·화면·Flow·Prototype·해석 기록·비교 작업면

.asset-vault / tracked assets
  → 실제 이미지 bytes 후보·제품 자산 파일 권위

Godot + tests + runtime capture
  → 실제 구현·런타임 증거
```

Figma는 두 번째 게임 기획 정본이나 제품 자산 파일 권위가 아니다. Figma와 GitHub 정본이 충돌하면 기존 `VISUAL_CANONICAL_CONFLICT`를 사용한다.

## Project Visual Bible profile

권장 Figma 페이지는 다음 5개를 최소 세트로 사용한다.

1. `00_DIRECTION`
2. `01_APPROVED_REFERENCE`
3. `02_WIP`
4. `03_REJECTED`
5. `04_FINAL`

필요하면 `05_DEPRECATED`, `06_MARKETING`, `07_ARCHIVE`를 추가한다.

페이지명은 프로젝트 협업 UX를 위한 Figma 조직 규칙이며 Base artifact lifecycle을 대체하지 않는다.

- `00_DIRECTION / 00.8_VISUAL_FLOW_HUB`는 대표 화면과 이동 관계를 `FLOW_MAP`으로 빠르게 복원한다.
- `01_APPROVED_REFERENCE`의 기준이 되는 artifact는 최소 `APPROVED_VISUAL_REFERENCE` 상태여야 한다.
- `02_WIP`는 `DRAFT_VISUAL` 또는 `REVIEW_CANDIDATE`와 대응하고 `FLOW_PROTOTYPE`·`GPT_INTERPRETATION`을 포함할 수 있다.
- `03_REJECTED`는 폐기 이유를 남기되 Registry 승인 상태로 재사용하지 않는다.
- `04_FINAL`은 '시각적으로 확정된 표현'을 뜻할 수 있으나 `PROJECT_ASSET_APPROVED`나 런타임 검증을 자동 의미하지 않는다.
- `04_FINAL / 04.2_IMPLEMENTATION_COMPARE`는 실제 `RUNTIME_CAPTURE`가 있을 때 승인 시안과 구현 결과를 비교한다.

## Figma continuity and interpretation gate

사용자가 프로젝트 이미지 생성·시각 자료 생성을 요청하면, 접근 가능한 경우 다음 순서를 따른다.

1. 최신 프로젝트 정본·Decision·실제 소비 화면을 확인한다.
2. Visual Artifact Registry에서 연결된 Figma와 `APPROVED_VISUAL_REFERENCE`를 찾는다.
3. 해당 Figma frame/node를 실제로 읽을 수 있으면 승인 레퍼런스를 확인한다.
4. `Keep / Avoid / Do Not Drift`를 생성 계약에 반영한다.
5. 새 결과는 기본 `WIP`/review 후보로 취급한다.
6. AI 화면은 `INTERPRETATION_RECORD`에 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION / MISSING_CANON / VISUAL_CANONICAL_CONFLICT`를 분리한다.
7. 여러 화면이 연결되면 `screen_id / flow_id`를 가진 `FLOW_MAP`을 갱신하고, 클릭 검토가 필요할 때만 `PROTOTYPE_FLOW`를 추가한다.
8. 기존 승인본과 스타일·비율·색·형태·카메라·UI 계층을 비교한다.
9. 사용자 승인 뒤에만 Approved/Final 시각 위치와 Registry 상태를 갱신한다.
10. 실제 제품 자산 승격은 별도 `PROJECT_ASSET_APPROVED → promote` 절차를 따른다.
11. 구현 뒤 실제 `RUNTIME_CAPTURE`가 있으면 `COMPARE_BOARD`에서 drift를 분류한다.

Figma 쓰기 권한이 있으면 GPT는 `INTERPRETATION_RECORD`를 이미지에 구워 넣지 않고 **편집 가능한 text panel/annotation 또는 동등한 Figma 객체**로 화면 옆에 남길 수 있다. `DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 전에는 기획 요구로 승격하지 않는다.

Figma 접근이 불가능하면 내용을 본 것으로 가정하지 않고 `LINK_UNVERIFIED`, `ACCESS_DENIED`, `AUTH_REQUIRED`, `READ_ONLY` 또는 `UNVERIFIED`를 사용한다.

## Runtime comparison boundary

Prototype은 Flow·전환·복귀·정보 위계·피드백 가설을 검토하는 증거다. Godot runtime, 저장·경제·보상 규칙, 성능, 실제 입력, 접근성 완료 증거가 아니다.

실제 구현 비교는 `RUNTIME_CAPTURE`가 있을 때 다음 상태를 사용한다.

```text
MATCHED
INTENDED_DIFFERENCE
IMPLEMENTATION_GAP
PLANNING_CHANGE_REQUIRED
AI_MOCKUP_ERROR
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

runtime 캡처가 없으면 Prototype만으로 `MATCHED`를 주장하지 않는다.

## Project-local template

`templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`는 다음을 제공한다.

- 프로젝트/Figma 링크와 권위 경계
- 페이지 구조와 `00.8_VISUAL_FLOW_HUB`
- Section/frame ID naming (`UI_ / FLOW_ / INT_ / CMP_` 포함)
- `Keep / Avoid / Do Not Drift` 메타 카드
- GPT interpretation card
- Flow map / Prototype card
- Runtime compare card
- WIP→Approved/Rejected/Final 작업 흐름
- 실제 예시 구조
- Figma가 없는 프로젝트의 fallback

이 파일은 프로젝트에 복제·최적화하는 template이며 Base 자체의 활성 프로젝트 상태를 만들지 않는다. `VISUAL_COLLABORATION_TOOL_POLICY`, Art Skill 및 continuity gate에서 직접 링크해 발견 가능성을 유지한다.

## Benchmark notes — 2026-08-12

Figma 공식 문서를 기준으로 다음을 채택한다.

- Pages/Sections: 작업 단계와 관련 frame을 구조화한다.
- Prototype flows/starting points: 여러 화면 이동을 클릭 가능한 흐름으로 검토한다.
- Annotation/text context: 화면 요소에 구현·해석 문맥을 편집 가능한 형태로 연결한다.
- Components/Styles/Libraries: 반복되는 시각 요소의 일관성 유지에 사용한다.
- Naming: 컴포넌트·frame naming structure를 팀/프로젝트 차원에서 고정한다.
- Version history/checkpoint: 큰 변경 전 복구 가능성을 확보한다.

Primary sources are recorded in the policy/profile research history and PR evidence. External capability details are rechecked before live project use.

## Adversarial review

### 공격

1. Figma를 '시각 정본'이라고 부르면 GitHub 정본보다 우선하는 두 번째 canon으로 오해할 수 있다.
2. `FINAL`이라는 페이지명이 실제 제품 자산 승인/런타임 검증으로 오해될 수 있다.
3. WIP/Rejected를 별도 lifecycle 상태로 추가하면 기존 artifact lifecycle과 중복된다.
4. 실제 이미지 bytes를 Figma에만 보관하면 `.asset-vault`/Repo 자산 정책과 충돌한다.
5. 모든 이미지 생성마다 Figma를 강제하면 접근 불가·비Figma 프로젝트에서 작업이 막힌다.
6. AI가 목업에 임의로 넣은 기능이 보기 좋다는 이유로 정본에 역수입될 수 있다.
7. Prototype이 실제 구현 완료 증거로 과장될 수 있다.
8. Flow/해석 전문을 Sheet까지 복제하면 시각 작업면이 또 다른 문서 중복을 만든다.

### 검증 및 최소 개선

- 'Visual Source of Truth' 대신 **Visual Bible / 승인 시각 레퍼런스 작업면**으로 표현하고 권위 경계를 명시한다.
- `FINAL`은 Figma 조직명일 뿐 제품 승인 상태가 아니라고 명시한다.
- lifecycle은 기존 상태를 그대로 사용하고 Figma page와 mapping만 제공한다.
- bytes 권위는 `.asset-vault`/tracked assets에 유지한다.
- Figma는 프로젝트가 구성했고 접근 가능한 경우 우선 소비하며, 불가 시 fallback 상태를 기록한다.
- AI 시각 해석을 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION`으로 분리하고 승인 없는 역수입을 막는다.
- Prototype과 runtime evidence를 분리한다.
- 해석 전문은 Figma 또는 책임 GitHub 기록에 두고 Sheet에는 필요한 경우 짧은 Artifact index만 둔다.

## Completion criteria

- 기존 `VISUAL_COLLABORATION_TOOL_POLICY`에 Visual Bible + Visual Flow + GPT interpretation 운영 규칙이 추가된다.
- 프로젝트 로컬 Figma Visual Bible template이 추가되고 policy/Skill에서 직접 발견 가능하다.
- 기존 이미지 생성 Skill에 Figma continuity gate가 연결된다.
- 이미지 생성/검수 template에 Figma context, `screen_id / flow_id`, interpretation, runtime compare fields가 추가된다.
- Visual Artifact Registry에서 Flow/Interpretation/Runtime Compare를 추적할 수 있다.
- 계약 테스트와 CI가 위 연결을 검증한다.
- 신규 `figma-*` Skill은 추가되지 않는다.
- 실제 프로젝트 Figma/Godot pilot은 실행하지 않았다면 `NOT_RUN`으로 남는다.
