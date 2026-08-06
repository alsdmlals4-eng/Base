---
name: evaluating-godot-assets-and-plugins-before-creation
description: Use when a Godot feature, tool, pipeline, UI, integration, asset, shader, template, or subsystem may be reusable before custom creation.
---

# Evaluating Godot Assets and Plugins Before Creation

## Core principle

새로 만들기 전에 **현재 환경에서 이미 사용 중인 도구와 검증 가능한 기존 구현으로 안전하게 해결할 수 있는지** 조사한다. 발견했다는 이유만으로 설치하지 않으며, 프로젝트 코어·데이터 소유권·라이선스·제거 가능성을 확인한다.

새 MCP·addon·CLI·framework·Skill·Mode·실행 계층에는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`의 Existing Solution First Gate가 의무다. 현재 환경·내부 구현·관련 PR·외부 대안을 조사하고 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` disposition을 기록하기 전에는 설계·구현으로 진행하지 않는다.

## Skill Modes

- `frame-need`: 플레이어 가치와 필요한 결과를 기능이 아니라 해결 문제로 정의한다.
- `inventory-current-environment`: 사용자가 이미 쓰는 addon·connected MCP·CLI·host profile·dependency·Base/프로젝트 구현·open and recently merged PR·인수인계를 먼저 확인한다.
- `search`: 공식·오픈소스·상용 소스를 우선순위대로 검색한다.
- `evaluate`: 호환성·라이선스·유지보수·종속성·비용·위험을 비교한다.
- `disposition`: `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` 중 하나를 근거·미검증·승인 상태와 함께 판정한다.
- `trial-plan`: 격리 브랜치·샘플 Scene·제거 절차·검증 기준을 설계한다.
- `adoption-decision`: 채택·수정 채택·시험·제외·직접 제작을 프로젝트 기록에 반영한다.
- `revalidate`: Godot·애드온 버전, 가격, 라이선스, 저장 형식이 변했을 때 재검증한다.

## Required project adapter roles

```text
engine_version
renderer
platforms
project_root
addon_root
asset_roots
canonical_design_sources
protected_paths
validators
third_party_inventory
license_record
mcp_host_inventory
related_open_and_recent_prs
```

프로젝트에는 검색 정책과 Skill 본문을 복사하지 않는다. 프로젝트 어댑터는 실제 버전·경로·플랫폼·검증기와 프로젝트 고유 제약만 제공한다.

## Current environment inventory

외부 검색 전에 가능한 범위에서 다음을 확인한다.

1. 최신 사용자 지시와 다른 채팅의 handoff·승인 결정.
2. `project.godot`의 enabled addon과 프로젝트 `addons/`.
3. connected MCP, Codex·VS Code host profile의 등록 여부와 client 격리 상태.
4. package·dependency manifest와 lock, 설치된 CLI·SDK.
5. Base Skill Registry, 프로젝트 adapter·template·기존 실행 계약.
6. 같은 Goal의 branch, open and recently merged PR, 중단된 구현과 과거 disposition.
7. 사용자가 이미 사용 중이라고 말한 도구와 실제 버전·경로·연결 상태.

credential 원문과 개인 설정 전체를 공개 저장소나 evidence에 복사하지 않는다. 확인할 수 없는 환경은 `UNVERIFIED`로 남기되, 존재를 확인하지 않은 채 새 구현이 필요하다고 추론하지 않는다.

## Search order

1. 현재 환경에 이미 설치·연결·채택된 도구.
2. Base·프로젝트의 현행 구현과 관련 open and recently merged PR.
3. Godot 기본 노드·Resource·Editor 기능·공식 문서.
4. 공식 Godot Asset Store.
5. 전환 기간 동안 기존 Godot Asset Library.
6. 제작자 공식 GitHub의 안정 Release·태그.
7. itch.io의 Godot assets·tools·plugins.
8. 제작자 공식 판매 페이지와 신뢰 가능한 Godot 전문 마켓.
9. 위 후보가 없거나 부적합할 때만 `BUILD_NEW` 검토.

세부 사이트와 검색 패턴은 `references/source-catalog.md`를 사용한다.

## Evaluation matrix

| 항목 | 확인 내용 |
|---|---|
| 요구 적합성 | 필요한 플레이어 경험과 완료 기준을 실제로 충족하는가 |
| 현재 사용 상태 | 이미 설치·연결·프로젝트 채택·PR 구현 중인가 |
| 기능 중복 | 새 구현이 현행 도구·Skill·PR과 같은 권위를 두 벌 만드는가 |
| Godot 호환성 | 프로젝트의 정확한 Godot 버전·렌더러·GDScript/.NET과 맞는가 |
| 플랫폼 | Windows·Web·Android·콘솔 등 목표 플랫폼에서 작동하는가 |
| 유지보수 | 최근 안정 릴리스, 이슈 대응, 마이그레이션 기록이 있는가 |
| 라이선스 | 상업 사용, 수정, 소스 포함, 재배포, 크레딧 의무가 명확한가 |
| 가격 | 일회성·구독·좌석·프로젝트별 비용과 업데이트 권리가 명확한가 |
| 소스 접근 | 문제 발생 시 검사·수정·포크가 가능한가 |
| 의존성 | 다른 애드온·SDK·서버·계정·네이티브 라이브러리가 필요한가 |
| 데이터 소유권 | 세이브·콘텐츠·Scene·Resource 포맷을 과도하게 잠그지 않는가 |
| 버전 관리 | 텍스트 diff, Git LFS, 생성 파일, `.godot/` 오염 위험이 관리 가능한가 |
| 제거 가능성 | 애드온 제거 뒤 프로젝트가 복구 가능한가 |
| 보안·개인정보 | 네트워크, 텔레메트리, API 키, 사용자 데이터 접근이 필요한가 |
| 성능·접근성 | 목표 장치의 frame time·메모리·입력·가독성 기준을 해치지 않는가 |
| 도입·전환비 | 기존 도구 유지보다 custom build가 실제로 유리한가 |

## Disposition states

```text
REUSE       기존 구현을 주 권위로 거의 그대로 사용
ABSORB      정책·테스트·패턴만 현행 권위에 흡수
REFACTOR    기존 구현을 bounded 수정해 사용
ARCHIVE     중복·위험 구현의 활성 권위를 제거하고 기록 보존
BUILD_NEW   기존 대안으로 충족할 수 없는 최소 범위만 신규 제작
```

기존 프로젝트 출력과의 호환 매핑:

```yaml
REUSE: ADOPT
ABSORB: ADAPT
REFACTOR: ADAPT_OR_TRIAL
ARCHIVE: REJECT_OR_DEFER
BUILD_NEW: BUILD_CUSTOM
```

`BUILD_NEW`는 필수 핵심 기능 부재, 설정·격리·bounded patch로 해결 불가능한 차단 결함, 라이선스 충돌, 유지 중단, Godot·OS·클라이언트·성능 미충족 중 하나를 증거로 확인하고 사용자가 비교 결과를 승인해야 한다. “직접 만들면 더 엄격하다”는 단독 근거가 아니다.

## Workflow

1. 요구를 `목표 / 플레이어 가치 / 범위 / 제외 / 완료 기준 / 테스트`로 변환한다.
2. `inventory-current-environment`로 사용 중 도구·connected MCP·enabled addon·dependency·기존 구현·관련 PR을 확인한다.
3. 검색 전에 비교 차원과 중단 조건을 고정한다.
4. 검색 순서에 따라 후보를 수집하고 공식 원본·확인일·버전을 기록한다.
5. 후보별 평가표를 작성하고 마케팅 설명과 실제 문서·릴리스·라이선스를 분리한다.
6. 무료·유료를 가격만으로 우열화하지 않고 총 도입·유지·제거 비용을 비교한다.
7. `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` disposition과 반대 측 공격을 적대적으로 검토한다.
8. 구매·계정 연결·프로젝트 설치·네이티브 SDK 추가는 사용자 승인 전 수행하지 않는다.
9. `TRIAL`은 별도 브랜치나 샘플 프로젝트에서 수행하고 핵심 Scene·세이브에 바로 결합하지 않는다.
10. `BUILD_NEW`는 Gate 증거와 사용자 승인 뒤 최소 범위로만 전환한다.
11. 채택 시 버전·출처·라이선스·변경 사항·검증·제거 절차를 프로젝트 기록에 남긴다.

## Asset rights and reference-production route

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다. 후보는 제품에 직접 넣는지, 참조만 하는지, 새로 만드는지를 먼저 분리한다.

```text
ADOPT / ADAPT
→ direct inclusion
→ LICENSED_THIRD_PARTY 또는 OPEN_SOURCE
→ commercial_use와 distribution_in_game_build 확인
→ 필요한 attribution·NOTICE·source·조건 기록

REFERENCE_ONLY
→ REFERENCE_TO_ORIGINAL
→ 원본을 build·marketing package에서 제외
→ reference_brief와 forbidden_expression 작성
→ 별도 final asset record와 similarity review

BUILD_CUSTOM
→ OWNED_ORIGINAL / COMMISSIONED_ORIGINAL / AI_GENERATED / MIXED_ROUTE
→ 입력·모델·약관·계약·작업 파일 증빙
```

`distribution_in_game_build`와 `raw_source_redistribution`은 분리한다. 상업 사용 가능 문구만으로 게임 포함 배포를 추론하지 않고, 원본 재배포가 불필요하면 `NOT_REQUIRED`로 기록한다.

필수 권리·출처·약관·계약·참조 유사성 증거가 없으면 채택 판정은 `RELEASE_BLOCKED_UNVERIFIED`다. “수정했다”, “AI로 다시 만들었다”, “영감을 받았다”는 독립 제작 증거가 아니다.

## Core-system rule

프로젝트의 핵심 재미, 핵심 판정, 세이브 정본, 게임 데이터 소유권은 범용 플러그인에 무비판적으로 위임하지 않는다. 외부 도구는 가능한 한 교체 가능한 경계를 유지하되, 이를 이유로 검증된 공급자와 중복되는 두 번째 실행 권위를 만들지 않는다.

## Output contract

```md
## 해결하려는 문제와 플레이어 가치
## 현재 사용 중인 addon·MCP·CLI·dependency·관련 PR
## 프로젝트 Godot·플랫폼 제약
## 검색한 공식·오픈소스·상용 소스
## 후보 비교표
## 라이선스·가격·유지보수·종속 위험
## REUSE·ABSORB·REFACTOR·ARCHIVE·BUILD_NEW 판정
## 판정 반대 측 공격과 완화 가능성
## 승인 필요한 구매·설치·계정·권한
## PoC·통합·제거·회귀 검증
## 직접 제작으로 남은 최소 범위
## UNVERIFIED·RELEASE_BLOCKED_UNVERIFIED 항목
```

## Quality gate

- 직접 제작 전에 현재 환경과 외부 대안 검색 기록이 있다.
- connected MCP·enabled addon·dependency·관련 PR을 확인했다.
- disposition과 사용자 승인 상태가 기록됐다.
- 검색 결과의 확인일·버전·원본·라이선스를 구분했다.
- 가격이나 별점만으로 채택하지 않았다.
- 구매와 설치를 조사와 혼동하지 않았다.
- 프로젝트 코어와 외부 도구의 소유권 경계가 명확하다.
- 제거·rollback·저장 호환성 계획이 있다.
- 실행하지 않은 플랫폼·성능·보안·법률 검증을 통과로 보고하지 않았다.

## Do not use

- 이미 승인·고정된 자산의 단순 경로 변경.
- 외부 도구와 무관한 오탈자나 단일 수치 수정.
- 실제 UI 결과의 시각 품질 감사만 필요한 경우. 이때는 `auditing-and-refining-ui-art`를 사용한다.

## Learning Log

채택·제외 이유, 버전 파손, 라이선스 변화, 성공한 wrapper, 제거 실패, 프로젝트별 재사용 가능성과 실제 검증 결과를 `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`에 기록한다.
