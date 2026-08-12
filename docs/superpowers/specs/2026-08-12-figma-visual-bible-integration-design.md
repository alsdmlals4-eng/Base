# Figma Visual Bible Integration Design

## Goal

Base의 기존 시각 협업·이미지 생성·자산 보존 체계를 깨지 않고, 각 프로젝트의 Figma를 **승인된 시각 레퍼런스와 작업 흐름을 모으는 Visual Bible**로 운영한다.

## Existing-solution-first 판정

- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`: Figma/Whimsical의 권위 경계와 visual artifact lifecycle을 이미 소유한다. → **ABSORB**
- `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`: Figma frame/node, Decision, snapshot, status를 이미 추적한다. → **REUSE**
- `skills/designing-art-prompts-and-technique-cards/SKILL.md`: 이미지 생성 전 정본·승인 자산·레퍼런스와 생성 후 QA를 이미 소유한다. → **REFACTOR/EXTEND**
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`: 실제 이미지 생성·검수 입력과 승인 동기화를 이미 소유한다. → **EXTEND**
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`: 이미지 bytes의 로컬 후보/승격 권위를 이미 소유한다. → **KEEP SEPARATE**
- 신규 `figma-*` Skill: 기존 정책이 명시적으로 금지하고 책임 중복을 만든다. → **DO NOT BUILD**

## Authority boundary

```text
GitHub/GDD/Decision
  → 게임 사실·규칙·승인 결정 정본

Figma Visual Bible
  → 승인된 시각 방향·화면·컴포넌트·레퍼런스 작업면

.asset-vault / tracked assets
  → 실제 이미지 bytes 후보·제품 자산 파일 권위

Godot + tests
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

- `01_APPROVED_REFERENCE`의 기준이 되는 artifact는 최소 `APPROVED_VISUAL_REFERENCE` 상태여야 한다.
- `02_WIP`는 `DRAFT_VISUAL` 또는 `REVIEW_CANDIDATE`와 대응한다.
- `03_REJECTED`는 폐기 이유를 남기되 Registry 승인 상태로 재사용하지 않는다.
- `04_FINAL`은 '시각적으로 확정된 표현'을 뜻할 수 있으나 `PROJECT_ASSET_APPROVED`나 런타임 검증을 자동 의미하지 않는다.

## Figma continuity gate

사용자가 프로젝트 이미지 생성·시각 자료 생성을 요청하면, 접근 가능한 경우 다음 순서를 따른다.

1. 최신 프로젝트 정본·Decision·실제 소비 화면을 확인한다.
2. Visual Artifact Registry에서 연결된 Figma와 `APPROVED_VISUAL_REFERENCE`를 찾는다.
3. 해당 Figma frame/node를 실제로 읽을 수 있으면 승인 레퍼런스를 확인한다.
4. `Keep / Avoid / Do Not Drift`를 생성 계약에 반영한다.
5. 새 결과는 기본 `WIP`/review 후보로 취급한다.
6. 기존 승인본과 스타일·비율·색·형태·카메라·UI 계층을 비교한다.
7. 사용자 승인 뒤에만 Approved/Final 시각 위치와 Registry 상태를 갱신한다.
8. 실제 제품 자산 승격은 별도 `PROJECT_ASSET_APPROVED → promote` 절차를 따른다.

Figma 접근이 불가능하면 내용을 본 것으로 가정하지 않고 `LINK_UNVERIFIED`, `ACCESS_DENIED`, `AUTH_REQUIRED` 또는 `UNVERIFIED`를 사용한다.

## Project-local template

새 `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`는 다음을 제공한다.

- 프로젝트/Figma 링크와 권위 경계
- 페이지 구조
- 섹션과 frame ID naming
- `Keep / Avoid / Notes` 메타 카드
- WIP→Approved/Rejected/Final 작업 흐름
- 실제 예시 구조
- Figma가 없는 프로젝트의 fallback

이 파일은 프로젝트에 복제·최적화하는 template이며 Base 자체의 활성 프로젝트 상태를 만들지 않는다.

## Benchmark notes — 2026-08-12

Figma 공식 문서를 기준으로 다음을 채택한다.

- Pages: 작업 단계나 개발 준비 상태를 분리하는 데 사용 가능.
- Sections: 관련 작업을 묶고 탐색·협업·ready-for-development 표시를 지원.
- Components/Styles/Libraries: 반복되는 시각 요소의 일관성 유지에 적합.
- Naming: 컴포넌트 naming structure를 팀 차원에서 정의·문서화하는 것을 권장.
- Version history/Branches: milestone·변경·복구 이력을 관리할 수 있음.

Primary sources:
- https://help.figma.com/hc/en-us/articles/360038511293-Create-and-manage-pages
- https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections
- https://help.figma.com/hc/en-us/articles/39723547036055-Components-collection-Library-fundamentals
- https://help.figma.com/hc/en-us/articles/360038663994-Name-and-organize-components
- https://help.figma.com/hc/en-us/articles/360038006754-View-a-file-s-version-history

## Adversarial review

### 공격

1. Figma를 '시각 정본'이라고 부르면 GitHub 정본보다 우선하는 두 번째 canon으로 오해할 수 있다.
2. `FINAL`이라는 페이지명이 실제 제품 자산 승인/런타임 검증으로 오해될 수 있다.
3. WIP/Rejected를 별도 lifecycle 상태로 추가하면 기존 artifact lifecycle과 중복된다.
4. 실제 이미지 bytes를 Figma에만 보관하면 `.asset-vault`/Repo 자산 정책과 충돌한다.
5. 모든 이미지 생성마다 Figma를 강제하면 접근 불가·비Figma 프로젝트에서 작업이 막힌다.

### 검증 및 최소 개선

- 'Visual Source of Truth' 대신 **Visual Bible / 승인 시각 레퍼런스 작업면**으로 표현하고 권위 경계를 명시한다.
- `FINAL`은 Figma 조직명일 뿐 제품 승인 상태가 아니라고 명시한다.
- lifecycle은 기존 상태를 그대로 사용하고 Figma page와 mapping만 제공한다.
- bytes 권위는 `.asset-vault`/tracked assets에 유지한다.
- Figma는 프로젝트가 구성했고 접근 가능한 경우 우선 소비하며, 불가 시 fallback 상태를 기록한다.

## Completion criteria

- 기존 `VISUAL_COLLABORATION_TOOL_POLICY`에 압축 운영 규칙이 추가된다.
- 프로젝트 로컬 Figma Visual Bible template이 추가된다.
- 기존 이미지 생성 Skill에 Figma continuity gate가 연결된다.
- 이미지 생성/검수 template에 Figma context fields와 sync checklist가 추가된다.
- Documentation Map에서 새 template을 찾을 수 있다.
- 계약 테스트와 CI가 위 연결을 검증한다.
