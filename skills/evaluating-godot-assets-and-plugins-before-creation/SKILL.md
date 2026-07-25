---
name: evaluating-godot-assets-and-plugins-before-creation
description: Use when a Godot feature, editor tool, content pipeline, UI system, integration, art asset, audio asset, shader, template, or reusable subsystem might already exist as a built-in capability, free asset, open-source addon, or commercial plugin before custom creation begins.
---

# Evaluating Godot Assets and Plugins Before Creation

## Core principle

새로 만들기 전에 **Godot 기본 기능과 검증 가능한 기존 자산으로 안전하게 해결할 수 있는지** 조사한다. 발견했다는 이유만으로 설치하지 않으며, 프로젝트 코어·데이터 소유권·라이선스·제거 가능성을 확인한 뒤 `ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM` 중 하나로 결정한다.

## Skill Modes

- `frame-need`: 플레이어 가치와 필요한 결과를 기능이 아니라 해결 문제로 정의한다.
- `search`: 공식·오픈소스·상용 소스를 우선순위대로 검색한다.
- `evaluate`: 호환성·라이선스·유지보수·종속성·비용·위험을 비교한다.
- `trial-plan`: 격리 브랜치·샘플 Scene·제거 절차·검증 기준을 설계한다.
- `adoption-decision`: 채택·수정 채택·시험·제외·직접 제작을 판정한다.
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
```

프로젝트에는 검색 정책과 Skill 본문을 복사하지 않는다. 프로젝트 어댑터는 실제 버전·경로·플랫폼·검증기와 프로젝트 고유 제약만 제공한다.

## Search order

1. Godot 기본 노드·Resource·Editor 기능·공식 문서.
2. 공식 Godot Asset Store.
3. 전환 기간 동안 기존 Godot Asset Library.
4. 제작자 공식 GitHub의 안정 Release·태그.
5. itch.io의 Godot assets·tools·plugins.
6. 제작자 공식 판매 페이지와 신뢰 가능한 Godot 전문 마켓.
7. 위 후보가 없거나 부적합할 때만 직접 제작.

세부 사이트와 검색 패턴은 `references/source-catalog.md`를 사용한다.

## Evaluation matrix

| 항목 | 확인 내용 |
|---|---|
| 요구 적합성 | 필요한 플레이어 경험과 완료 기준을 실제로 충족하는가 |
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

## Decision states

```text
ADOPT        그대로 채택할 가치가 있고 검증 계획이 있음
ADAPT        제한된 수정·wrapper·adapter를 전제로 채택
TRIAL        격리된 PoC에서만 시험
REJECT       라이선스·호환성·품질·종속 위험으로 제외
BUILD_CUSTOM 기존 후보보다 직접 제작이 명확히 안전하거나 코어 차별화에 필요
DEFER        지금은 필요하지 않아 조사 기록만 보존
UNVERIFIED   필수 정보나 실행 증거가 없음
```

## Workflow

1. 요구를 `목표 / 플레이어 가치 / 범위 / 제외 / 완료 기준 / 테스트`로 변환한다.
2. 프로젝트 어댑터에서 Godot 버전, 플랫폼, 보호 경로와 기존 제3자 자산을 읽는다.
3. 검색 전에 비교 차원과 중단 조건을 고정한다.
4. 검색 순서에 따라 후보를 수집하고 공식 원본·확인일·버전을 기록한다.
5. 후보별 평가표를 작성하고 마케팅 설명과 실제 문서·릴리스·라이선스를 분리한다.
6. 무료·유료를 가격만으로 우열화하지 않고 총 도입·유지·제거 비용을 비교한다.
7. 구매·계정 연결·프로젝트 설치·네이티브 SDK 추가는 사용자 승인 전 수행하지 않는다.
8. `TRIAL`은 별도 브랜치나 샘플 프로젝트에서 수행하고 핵심 Scene·세이브에 바로 결합하지 않는다.
9. 적합한 후보가 없거나 프로젝트 코어 차별화가 필요한 경우에만 `BUILD_CUSTOM`으로 전환한다.
10. 채택 시 버전·출처·라이선스·변경 사항·검증·제거 절차를 프로젝트 기록에 남긴다.

## Core-system rule

프로젝트의 핵심 재미, 핵심 판정, 세이브 정본, 게임 데이터 소유권은 범용 플러그인에 무비판적으로 위임하지 않는다. 외부 도구는 가능한 한 adapter·wrapper 뒤에 두고 교체 가능한 경계를 유지한다.

## Output contract

```md
## 해결하려는 문제와 플레이어 가치
## 프로젝트 Godot·플랫폼 제약
## 검색한 공식·오픈소스·상용 소스
## 후보 비교표
## 라이선스·가격·유지보수·종속 위험
## ADOPT·ADAPT·TRIAL·REJECT·BUILD_CUSTOM 판정
## 승인 필요한 구매·설치·계정·권한
## PoC·통합·제거·회귀 검증
## 직접 제작으로 남은 최소 범위
```

## Quality gate

- 직접 제작 전에 검색 기록이 있다.
- 검색 결과의 확인일·버전·원본·라이선스를 구분했다.
- 가격이나 별점만으로 채택하지 않았다.
- 구매와 설치를 조사와 혼동하지 않았다.
- 프로젝트 코어와 외부 도구의 소유권 경계가 명확하다.
- 제거·롤백·저장 호환성 계획이 있다.
- 실행하지 않은 플랫폼·성능·보안 검증을 통과로 보고하지 않았다.

## Do not use

- 이미 승인·고정된 자산의 단순 경로 변경.
- 외부 도구와 무관한 오탈자나 단일 수치 수정.
- 실제 UI 결과의 시각 품질 감사만 필요한 경우. 이때는 `auditing-and-refining-ui-art`를 사용한다.

## Learning Log

채택·제외 이유, 버전 파손, 라이선스 변화, 성공한 wrapper, 제거 실패, 프로젝트별 재사용 가능성과 실제 검증 결과를 `skills/SKILL_LEARNING_LOG.md`에 기록한다.
