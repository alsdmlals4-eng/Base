# Godot Asset·Plugin Source Catalog

- 기준 확인일: `2026-07-25`
- 목적: Godot 기능·에셋·플러그인을 직접 제작하기 전에 검색할 원본과 검증 순서를 제공한다.
- 주의: 가격, 라이선스, Godot 호환 버전, 판매 상태는 바뀔 수 있으므로 채택 시점에 다시 확인한다.

- MCP 비교·흡수 작업은 8절 사전점검을 설계 전에 적용한다. 다른 자산 검색에는 추가 절차를 강제하지 않는다.

## 0. 현재 사용자 PC의 로컬 참고 라이브러리

외부 검색 전에 현재 프로젝트·Base 현행 상태를 먼저 확인하고, 관련성이 있으면 다음 로컬 참고 라이브러리를 확인한다.

```text
C:\Users\user\Documents\GitHub\Godot_Reference
```

역할은 `LOCAL_TEMPLATE_AND_OFFICIAL_DEMO_REFERENCE_LIBRARY`이며 세부 경계는 `docs/knowledge/godot/LOCAL_GODOT_REFERENCE_LIBRARY.md`가 책임진다.

```text
현재 프로젝트·Base 현행 구현
→ Local Godot Reference Library
→ Godot 공식 문서·Store·Asset Library·upstream 원본
```

- 현재 등록된 공식 데모 참고 코퍼스에 `godot-demo-projects-master`가 포함된다. upstream은 `godotengine/godot-demo-projects`이며 기본 상태는 `REFERENCE_ONLY`다.
- `godot-demo-projects-master`의 예제는 엔진 네이티브 구현 패턴 탐색에 활용하되, 로컬 폴더명의 `master`를 exact upstream version으로 간주하지 않는다. 실제 채택 시 commit/tag와 현재 Godot 버전 호환성을 다시 검증한다.
- 이 경로는 현재 사용자 Windows PC 전용이며 다른 PC·CI·원격 agent의 필수 경로가 아니다.
- 경로가 없거나 접근할 수 없으면 `UNAVAILABLE_LOCAL_REFERENCE`로 두고 정상 외부 검색을 계속한다.
- 템플릿·공식 데모·플러그인 원본은 기본 `REFERENCE_ONLY`다. 다운로드 또는 폴더 존재만으로 프로젝트 채택을 선언하지 않는다.
- 실제 채택 전에는 exact version, Godot 호환성, 원본 source, 라이선스, 현재 유지보수 상태, consumption path, 제거·rollback을 다시 확인한다.
- 템플릿 전체 복사보다 현재 프로젝트에 필요한 패턴·컴포넌트의 선택적 `REUSE / ABSORB / REFACTOR`를 우선 검토한다.
- 로컬 참고 라이브러리 전체를 Base 또는 게임 프로젝트 저장소에 복제하지 않는다.

## 1. 필수 검색 소스

| 우선 | 소스 | 주소 | 주 용도 | 검증 포인트 |
|---|---|---|---|---|
| 1 | Godot 공식 문서 | https://docs.godotengine.org/ | 엔진 기본 기능·API·플러그인 설치 방식 | 프로젝트 Godot 버전 문서를 선택했는가 |
| 2 | Godot Asset Store | https://store.godotengine.org/ | 공식 신규 에셋 탐색 | 2026-07 기준 무료 자산 중심이며 유료 판매 기능은 재확인 필요 |
| 3 | Godot Asset Library | https://godotengine.org/asset-library/asset | 기존 무료 애드온·데모·도구 | 신규 Store로 자동 이전되지 않은 자산이 있어 전환 기간 함께 검색 |
| 4 | GitHub Godot addon topic | https://github.com/topics/godot-addon | 오픈소스 애드온·소스·Release | 기본 브랜치보다 안정 Release·태그, 라이선스, 최근 이슈를 우선 확인 |
| 5 | itch.io Godot assets | https://itch.io/game-assets/tag-godot | 2D·3D 아트, UI, 오디오, 템플릿 | 상업 사용·수정·재배포·크레딧 조건을 상품별 확인 |
| 6 | itch.io Godot tools | https://itch.io/tools/tag-godot | 에디터 도구·상용 플러그인·제작 툴 | 지원 Godot 버전, 업데이트 권리, 환불·지원 범위 확인 |
| 7 | 제작자 공식 사이트 | 후보의 README·Store 페이지에서 연결 | 공식 문서·라이선스·지원·결제 | 제3자 재판매 페이지보다 제작자 원본 우선 |
| 8 | Godot Foundry | https://godot-foundry.com/ | Godot 전문 제3자 마켓 후보 탐색 | 공식 Godot 재단 마켓으로 오인하지 말고 판매자·라이선스·지원 검증 |

## 2. 공식 Store와 기존 Asset Library 병행 규칙

공식 Godot Asset Store가 열렸더라도 기존 Asset Library 자산이 모두 자동 이전된 것은 아니다. 검색 누락을 줄이기 위해 다음을 함께 수행한다.

```text
Godot Asset Store 검색
+ 기존 Asset Library 동일 키워드 검색
+ GitHub 원본·Release·라이선스 대조
```

Asset Store 또는 Asset Library의 등록 정보만으로 유지보수와 상업 사용을 확정하지 않는다. 제작자 저장소와 라이선스 원문을 확인한다.

## 3. 검색 쿼리 템플릿

### 일반 기능

```text
Godot 4.7 <기능명> addon
Godot 4 <기능명> plugin release
site:store.godotengine.org <기능명>
site:godotengine.org/asset-library <기능명>
site:github.com <기능명> godot addon
site:itch.io <기능명> Godot plugin
```

### 프로젝트 유형별

```text
Godot dialogue editor branching localization
Godot card game framework deck hand tooltip
Godot inventory crafting save system addon
Godot behavior tree state machine addon
Godot Android safe area billing analytics plugin
Godot visual novel timeline dialogue plugin
Godot 2D shader pixel art VFX pack
Godot UI theme icon pack commercial license
```

### 버전·유지보수 확인

```text
<후보명> Godot 4.7 compatibility
<후보명> releases changelog migration
<후보명> license commercial use
<후보명> issues Godot 4.7
<후보명> uninstall migration save format
```

## 4. 후보 기록 최소 필드

```yaml
candidate_name:
category:
source_url:
creator:
checked_at:
version:
supported_godot_versions:
platforms:
license:
price_and_purchase_model:
source_available:
latest_release:
maintenance_signal:
dependencies:
data_and_save_ownership:
version_control_impact:
removal_plan:
security_and_privacy:
project_fit:
decision: ADOPT | ADAPT | TRIAL | REJECT | BUILD_CUSTOM | DEFER | UNVERIFIED
reason:
validation:
```

## 5. 구매·설치 안전 규칙

- 조사와 구매·설치는 별개다.
- 사용자 승인 없이 유료 구매, 계정 연결, API 키 발급, 네이티브 SDK 설치를 수행하지 않는다.
- 프로젝트 브랜치에 바로 설치하지 않고 가능한 경우 샘플 프로젝트나 격리 브랜치에서 시험한다.
- `addons/`, Autoload, Project Settings, import 설정, Android plugin, 빌드 템플릿 변경을 기록한다.
- 채택된 제3자 자산은 버전·원본·라이선스·수정 내역·크레딧·제거 방법을 프로젝트의 제3자 기록에 남긴다.

## 6. 프로젝트별 기본 검색 초점

| 프로젝트 | 먼저 찾을 범주 |
|---|---|
| Ten-Paces-Hidden-Moves | 카드 UI·툴팁·턴/행동 시퀀스·그리드·전투 로그·테스트 보조 |
| Blacksmith | 모바일 UI·Safe Area·인벤토리·제작 데이터·Android 빌드·터치 피드백 |
| urban-legend | 대화·분기·로컬라이제이션·타임라인·조사 기록 UI·오디오 이벤트 |
| omenward | 룰렛·결정론 테스트·3라인 전투·상태 머신·디버그 시각화·데이터 검증 |

이 표는 검색 우선순위이며 자동 채택 목록이 아니다. 각 프로젝트의 코어 경험과 실제 구현 상태를 먼저 확인한다.

## 7. 외부 Agent·CLI·Skill·Workspace 후보

Godot addon 범위를 넘어 코드 리뷰 도구, 출력 압축 프록시, 외부 모델 CLI, 에이전트 Skill·hook, 통합 workspace를 평가할 때도 이 Skill의 현재 환경 인벤토리·중복 권위·비용·라이선스·보안·제거 가능성 Gate를 재사용한다.

- 2026-08-31 후보 10종의 원문 대조와 `ADOPT / ADAPT / TRIAL_OPTIONAL / REFERENCE_ONLY / REJECT_AS_REQUIRED_DEPENDENCY` 판정: `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_TOOL_ADOPTION_REVIEW_2026-08-31.md`
- 선택형 외부 reviewer·output proxy·model CLI·agent workspace의 권위·원문 fallback·비용·비밀·실행 안전·킬 스위치 계약: `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`

이 두 문서는 새 실행 권위나 설치 승인이 아니다. 후보의 버전·라이선스·가격·telemetry·auth·model·hook·출력 의미가 바뀌거나 프로젝트별 A/B 결과가 달라지면 현재 1차 자료로 재검증한다. ordinary Godot 에셋 검색에서는 불필요하게 로드하지 않는다.

## 8. MCP 기능 비교·흡수 사전점검

MCP 추가, 기존 MCP 기능 보강, 다른 MCP의 구조 흡수 요청에서는 이 Skill의 `inventory-current-environment`에서 이 절을 적용한다. ordinary asset 검색에는 강제하지 않는다. 새 Skill·실행 서버·중앙 인벤토리를 만들지 않고 기존 작업 계약과 프로젝트의 adoption record를 사용한다. 공용 권위는 기존 HiGodot 정책과 외부 어댑터 계약에 남는다.

### 8.1 현재 기능의 증거를 먼저 분리

프로젝트 `AGENTS.md` → adopted pin·기존 설정 owner → 해당 host의 현재 profile·workspace → 실제 기능·검증 근거 순서로 읽는다. 서로 다른 증거를 한 개의 “사용 중” 상태로 합치지 않는다.

| 확인 대상 | 얻을 수 있는 근거 | 이 근거만으로 확정할 수 없는 것 |
|---|---|---|
| 프로젝트 채택 기록·exact pin | 프로젝트가 선택한 provider·version·역할 | 현재 PC 설치·실행·연결 |
| host 등록·설정 | 해당 profile에 등록된 서버와 설정 출처 | 활성 여부·인증·현재 tool schema·정상 작동 |
| 현재 host 활성·연결 및 schema 관찰 | 이번 세션에서 호출 가능한 범위 | 실제 작업 검증·영구 변경의 정확성 |
| exact revision의 readback·테스트·화면 | 실제로 실행한 작업의 결과 | 다른 프로젝트·버전·세션의 PASS |

- 별도 인벤토리 CLI 또는 config parser를 만들기 전에 host 기본 기능을 재사용한다. Codex는 해당 프로젝트의 `CODEX_HOME`·작업 디렉터리에서 `codex mcp list`로 등록을, `/mcp`로 현재 활성 서버를 확인한다. 설치된 CLI의 도움말과 버전에 맞는 기능만 사용한다.
- VS Code는 `MCP: List Servers`와 해당 profile/workspace의 enabled 상태·로그를 대조한다. enable/disable은 `mcp.json`과 별도 저장될 수 있으므로 설정 파일만으로 활성 상태를 확정하지 않는다. Codex의 `enabled_tools`·`disabled_tools`도 지원되는 현재 버전에서 effective tool 범위와 함께 대조한다.
- 이 단계는 읽기 범위다. 목록 조회를 이유로 서버 추가·삭제·로그인·권한 변경, 전역 profile 재작성, `Configure all`을 자동 실행하지 않는다. 다른 프로젝트의 설정을 흡수하거나 덮어쓰지 않는다.
- 현재 세션에서 host에 접근하지 못하면 해당 환경은 `UNVERIFIED`다. 도구 목록에서 보이지 않는 것은 PC에 없는 기능 부재의 증거가 아니다. 새 구현이 필요하다고 추론하지 않는다. 미확인 host 수정·설치는 보류하고 독립적으로 가능한 Base 계약 교정과 구분해 보고한다.
- host 출력이나 설정에는 민감정보가 있을 수 있다. 전체 설정·원본 환경변수 대신 provider·version·scope·operation·redacted 상태와 안전한 evidence locator만 기존 기록에 남긴다.

### 8.2 추가 위치와 대안 선택

```text
현재 기능 재사용
→ 기존 설정·작업 절차·검증 보강
→ 확인된 결함만 기존 구현에 제한 수정
→ 역할이 다른 기존 전문 도구 재사용
→ 대안 부적합 증거가 있을 때만 최소 신규 제작
```

이 순서는 하나의 거대 MCP에 기능을 몰아넣는 지시가 아니다. `ABSORB`는 정책·테스트·작업 패턴 흡수이며 반드시 MCP 코드 수정이 아니다. 요구에 필요 없는 도구는 현행 유지·`DEFERRED`가 유효한 대안이다.

| 확인된 필요 | 우선 판정 | 수정 위치와 금지 사항 |
|---|---|---|
| 기존 provider가 이미 수행하며 근거도 있음 | `REUSE` | 현행 경로 유지; 같은 기능을 다시 구현하지 않음 |
| 기능은 있으나 호출 순서·확인·실패 복구가 부족함 | `ABSORB` | 기존 작업 절차·설정 owner·테스트의 부족한 부분만 교정 |
| actual consumer가 있고 기존 기능의 결함이 재현됨 | `REFACTOR` 검토 | exact pin·라이선스·회귀·rollback을 갖춘 bounded patch; vendor 전체 fork는 기본안 아님 |
| Blender 등 다른 프로그램만 담당하는 작업이 실제로 필요함 | 제한된 역할의 `REUSE` 검토 | 기존 전문 도구를 격리 시험; 실제 채택은 프로젝트 Gate 이후 |
| 현재 host나 기능 지원 여부가 미확인임 | `UNVERIFIED` | missing evidence를 채우기 전 설치·기능 부재 판정 금지 |

기존 작업 계약에 필요한 기능별로 **실제 consumer / provider와 exact version / 현재 operation·schema·근거 / 기존 충족·확인된 결함·미확인 / 변경 대상 owner / disposition / 검증 / rollback**을 연결한다. 이는 기존 필드를 묶어 보는 작업별 projection이지 새 중앙 Registry·공용 Schema가 아니다. `UNVERIFIED이면` 결함으로 간주하지 않으며 `BUILD_NEW 근거로 바꾸지 않는다`.

### 8.3 다중 MCP와 Blender의 경계

서버 개수보다 **같은 대상의 persistent mutation authority**가 겹치는지를 먼저 본다. HiGodot의 경계는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다. 별도 역할의 자산 제작·검증 도구 공존은 가능하지만 자동 채택은 아니다. “MCP 하나 유지”만을 이유로 범용 MCP·새 Bridge를 만들거나 기존 Blender 연결 기능을 중복 구현하지 않는다.

Blender 후보는 실제 3D 소비처가 있을 때만 다음을 시험한다. 도구의 역할 이름이나 작업 폴더 지정은 권한 격리의 증거는 아니다. Python 실행 등으로 다른 경로까지 변경할 수 있는지는 별도 검증하며, 그런 검증 없이 안전한 sandbox라고 보고하지 않는다.

```text
기존 승인 자산·actual consumer 확인
→ 원본을 보호한 복제본에서 Blender 상태 관찰
→ 승인된 bounded 변경
→ Blender 상태·파일 readback
→ 격리 staging 산출물과 SHA-256·내보내기 형식·설정 기록
→ 기존 프로젝트 권위의 검토·승인·가져오기
→ 실제 Godot consumer에서 import·test·Godot 실행 증거 확인
```

Blender가 프로젝트 정본을 직접 덮어쓰지 않는다. 기존 승인 자산·아트 방향·이미지 모델 제작·승인 규칙은 그대로 유지하며, 이 비교로 2D 이미지 제작을 Blender 렌더로 자동 교체하지 않는다. Blender 뷰포트나 자산 파일 존재는 게임 runtime 증거가 아니다.

비용·보안·복구·A/B의 상세 owner는 `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`다. 개인 설정 전체·키·토큰·비공개 자산을 공개 기록에 복사하지 않는다. 텔레메트리·외부 생성 API·추가 비용·권한은 기존 Gate로 확인하며 모호하면 해당 trial을 보류한다. 응답 누락·timeout 뒤 변경을 자동 재실행하지 않는다. 기존 출력과 현재 상태를 먼저 확인한다. 안전한 `TRIAL_APPROVED` 시험 결과를 얻기 전부터 A/B 완료를 요구하지 않으며, `ADOPTED_ACTIVE`는 실제 비교·복구·프로젝트 채택 근거 이후다.

### 8.4 2026-09-07 비교 근거와 적용 판정

아래는 이 절의 조사 근거이지 사용자의 현재 PC 설치 목록이나 고정 설치 지시가 아니다. 최신 README는 로컬 설치 상태의 증거가 아니다. 후속 작업에서는 프로젝트 exact pin과 당시 공식 문서를 다시 대조한다.

| 원출처와 관찰 | 적용 판정 | 적용 범위 |
|---|---|---|
| [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture): host가 여러 서버에 연결하는 구조 | `ADOPT` | 서버 수가 아니라 각 도구의 역할·실제 영향 범위를 비교 |
| [Codex MCP](https://developers.openai.com/codex/mcp), [VS Code MCP 관리](https://code.visualstudio.com/docs/agent-customization/mcp-servers): native 목록·활성 상태·도구 설정 | `ADOPT` | 기존 host 기능으로 조사; 새 parser나 전역 설정 변경은 만들지 않음 |
| [Blender MCP](https://github.com/ahujasid/blender-mcp): Blender 애드온과 MCP 서버, 장면 조회·수정·Python 실행 | `ADAPT` | 상태 관찰→변경→readback 패턴은 기존 owner에 필요한 차이만 흡수; Blender 고유 기능은 실제 수요 전까지 `DEFERRED` |
| Blender 기능을 전부 기존 Godot MCP에 재구현하거나 모든 MCP를 상시 활성화 | `REJECT` | 확인된 결함·consumer 없이 유지비와 중복 writer를 추가하지 않음 |

버전 비교 사례: Tetris의 [채택 기록](https://github.com/alsdmlals4-eng/Tetris/blob/b3a0975d2586dc093d3a3929a426bdcd7e4f3575/docs/operations/HIGODOT_ADOPTION_RECORD.json)은 HiGodot `v3.2.0`, upstream `42c44e4d02ca1836a0e1866361509d3a14d83b0c`와 연결·runtime `NOT_RUN`을 기록한다. [해당 pin의 README](https://github.com/hi-godot/godot-ai/blob/42c44e4d02ca1836a0e1866361509d3a14d83b0c/README.md)와 [현재 upstream](https://github.com/hi-godot/godot-ai)의 v4 안내는 구분한다. 최신 예시를 복사해 자동 업데이트하거나 프로젝트가 선택한 transport·vendor extension을 교체하지 않는다. 이 사례는 해당 기록의 증거 상한이며 다른 프로젝트의 설치·작동 상태로 일반화하지 않는다.

### 8.5 검증과 종료

변경 전후 같은 bounded task로 정확성·사용자 개입·재시도·실패 복구·유지 비용을 비교하고, 관찰하지 못한 사용량·속도 향상은 수치로 만들지 않는다. 기존 consumer와 승인 범위를 유지하는 변경만 해당 owner의 테스트·readback으로 검증한다.

`문서 반영 → 문서 계약 검사 → 프로젝트 채택 → 실제 MCP 연결 → 기능 실행 → runtime PASS → UX/Human`은 별개 증거다. 앞 단계 성공으로 뒤 단계를 자동으로 승격하지 않는다. 각 작업에서 실행하지 못한 단계는 `NOT_RUN`과 정확한 blocker를 남긴다. 문서 계약 검사는 해당 절차의 누락·퇴행만 확인하며 실제 MCP 실행·권한 격리·성능을 증명하지 않는다.

Base 교정의 롤백은 해당 변경의 일반 revert이며, 프로젝트 설정이나 pin은 건드리지 않는다. 나중에 실제 도구를 시험하면 기존 provider 없이도 복구 가능한 프로젝트별 rollback을 먼저 정한다. 자체 검토·자동 테스트와 독립 검토도 서로 다른 증거로 보고한다.
