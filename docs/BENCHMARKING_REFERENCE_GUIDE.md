# 벤치마킹 참고 가이드

## 목적

벤치마킹은 다른 제품의 표면을 복제하는 일이 아니라, 사용자가 느끼는 가치와 문제 해결 방식을 현재 프로젝트에 맞게 해석하는 과정이다.

조사 방법의 상세 기준은 `docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`를 따른다. 반복 재사용할 가치가 있는 결과는 `docs/knowledge/cases/`에 사례 연구로 남긴다.

## 기본 원칙

- 벤치마킹은 선택 절차가 아니라 중요한 기획·UI·아트·연출 작업 전 기본 절차다.
- 작업 범위가 작으면 1~3개 사례만 압축 확인해도 된다.
- 큰 방향 전환, 핵심 시스템, 시장성, 아트 스타일, UI/UX는 더 넓게 본다.
- 게임성, 디자인, UX, 아트, 연출, 시장성, 구현 방식을 구분한다.
- 결과는 장문 복사가 아니라 문제, 근거, 적용·제외 결론으로 정리한다.
- Issue와 Goal에는 실행에 필요한 결론만 반영한다.
- 공용 가치가 있는 교훈은 사례로 남기되 활성 프로젝트 기획서를 Base에 복제하지 않는다.

## 조사 시작 형식

```md
## 벤치마킹 질문
- 결정할 내용:
- 현재 가설:
- 대상 사용자·플랫폼:
- 제약:
- 필요한 최신성:
- 종료 조건:
- 반영할 책임 문서:
```

## 기본 기록 형식

```md
| 사례 | 관찰 근거 | 해결한 문제 | 강점 | 한계 | 프로젝트 적용 | 검증 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
```

| 항목 | 기록할 내용 |
|---|---|
| 사례 | 참고한 게임, 제품, 기능, 장면, 저장소, 사용자 흐름 |
| 관찰 근거 | 직접 사용, 공식 문서, 영상, 리뷰 등 확인 방식 |
| 해결한 문제 | 해당 사례가 해결하려는 실제 사용자·제작 문제 |
| 강점 | 잘 작동하는 이유와 전제 |
| 한계 | 피로, 비용, 기술, 플랫폼, 접근성, 운영 위험 |
| 프로젝트 적용 | 그대로 복제하지 않고 현재 제약에 맞춘 결정 |
| 검증 | PoC, 플레이테스트, 화면 비교, 성능·데이터 테스트 |

## 원리와 표면 분리

예시:

```text
표면: 특정 게임의 미니맵
원리: 화면 밖 중요 상태를 빠르게 파악해야 함

표면: 진영별 유닛 데이터
원리: 진영은 다르게 보이면서 역할은 비교 가능해야 함
```

현재 프로젝트가 같은 문제를 더 단순한 구조로 해결할 수 있다면 표면 기능을 복제하지 않는다.

## BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE

벤치마크 역공학은 **외부 제품을 복제하는 절차가 아니라 관찰 가능한 행동·문제 해결 구조를 재사용 가능한 계약으로 바꾸는 절차**다. 장르 문법뿐 아니라 시스템, 콘텐츠·데이터 구조, UI/UX, 도구, 에셋·이미지 재료, 작업구조, 반복 프로세스와 Skill 후보까지 `REUSABLE_UNIT_DISCOVERY` 대상으로 본다.

프로젝트 단위 실행은 `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`를 읽고 `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`에 기록한다.

```text
BENCHMARK / PRACTICE OBSERVATION
→ SOURCE_AND_RIGHTS_PRECHECK
→ MULTI_SOURCE_EXTRACTION
→ REUSABLE_UNIT_DISCOVERY
→ CONTRACT_ABSTRACTION
→ PROJECT_FIT_DISCOVERY
→ REUSE_MODE_DECISION
→ NOVELTY_DELTA
→ PROJECT-SPECIFIC ADAPT / REBUILD
→ FIT-FOR-UNIT VALIDATION
→ EXISTING OWNER PROMOTION / PROJECT-ONLY RETENTION
```

### 1. SOURCE_AND_RIGHTS_PRECHECK

먼저 무엇을 관찰하고 무엇을 실제로 재사용할 권리가 있는지 분리한다.

- 공개적으로 관찰 가능한 동작, 공식 문서, 개발자 발표, 합법적으로 확보한 제품·자료를 근거로 삼는다.
- 라이선스가 허용하는 코드·도구·에셋은 역공학보다 `DIRECT_LICENSED_REUSE` 또는 `ADAPT_LICENSED`가 더 단순하고 안전한지 먼저 비교한다.
- 소스 코드, 아트, 사운드, 문구, 고유 명칭, 고유 UI 표현, 고유 수치표를 권한 없이 복사해 패턴 라이브러리에 넣지 않는다.
- 접근 통제 우회, 비공개 데이터 추출, 보안 우회, 서비스 약관을 회피하는 방법은 이 파이프라인의 범위가 아니다.
- 라이선스·상표·특허·계약·플랫폼 정책 등 별도 권리 검토가 필요한 경우 `RIGHTS_REVIEW_REQUIRED`로 둔다.

### 2. MULTI_SOURCE_EXTRACTION

하나의 작품에서 본 기능을 바로 공용 원리로 승격하지 않는다.

- 단일 사례는 그 사례의 관찰 근거가 될 수 있다.
- `MECHANIC_PATTERN_LIBRARY` 또는 `GENRE_FOUNDATION_REFERENCE`처럼 일반화된 공용 패턴으로 만들 때는 가능한 경우 **서로 다른 구현·전제를 가진 3개 이상의 materially distinct 사례**를 비교한다.
- 여러 작품에서 반복되는 불변 구조와 작품별 표현을 분리한다.
- 성공 사례뿐 아니라 실패·혼합 사례를 함께 보며 “장르 관습”과 “특정 작품의 강한 시그니처”를 구분한다.
- 세 사례를 확보하기 어렵다면 보편 법칙처럼 쓰지 않고 `SINGLE_SOURCE_HYPOTHESIS`로 남긴다.

### 3. REUSABLE_UNIT_DISCOVERY

발견 후보를 다음처럼 분류한다. 한 사례에서 여러 단위를 추출할 수 있다.

- `GENRE_FOUNDATION_REFERENCE`: 장르에서 반복되는 최소 플레이 문법과 기대.
- `MECHANIC_PATTERN_LIBRARY`: 입력·상태·규칙·결과·피드백으로 설명 가능한 메커닉 패턴.
- `SYSTEM_PATTERN`: 전투, 경제, 진행, 생성, 상태 관리 등 여러 메커닉을 묶는 시스템 구조.
- `CONTENT_PATTERN`: 이벤트, 적, 방, 퀘스트, 카드, 스테이지 등 콘텐츠를 생산하는 문법.
- `DATA_SCHEMA_PATTERN`: 상태·콘텐츠를 안정적으로 표현하는 데이터 관계와 경계.
- `UI_UX_PATTERN`: 정보 우선순위, 조작 흐름, 피드백, 오류·복구 패턴.
- `TOOL_PATTERN`: 반복 제작·검증 비용을 줄이는 도구의 입력/처리/출력 계약.
- `ASSET_MATERIAL_PATTERN`: 재사용 가능한 레이어, 모듈 파츠, 타일, 아이콘 계열, 배경 재료, 마스크·구조 패턴 등 시각 재료.
- `WORKFLOW_PATTERN`: 조사→기획→구현→검증처럼 반복되는 생산 절차와 handoff 구조.
- `SKILL_PATTERN`: AI/사람이 반복 수행할 판단 작업의 trigger, 입력, 정본, 절차, 산출물, 검증 계약.

각 후보는 최소한 다음을 설명할 수 있어야 한다.

```yaml
problem_or_player_need:
inputs:
state:
rule_or_process:
outputs:
feedback:
tunable_parameters:
dependencies:
failure_and_recovery:
source_observations:
rights_and_license_boundary:
```

“화면이 비슷하다”, “유명 게임이 쓴다”만으로는 재사용 단위가 아니다.

#### TOOL_INTERFACE_SURFACE_SELECTION

`TOOL_PATTERN`이 실제 사람이 반복 조작하는 도구로 구체화될 때는 구현 난이도나 유행만 보고 CLI/TUI/GUI를 고르지 않는다. `docs/CAPABILITY_COMPOSITION_MAP.md`의 `TOOL_INTERFACE_SURFACE_SELECTION`을 적용해 **CLI-only / CLI+TUI / reusable core·CLI+thin GUI**를 materially applicable한 후보로 비교한다.

- 자동화·CI·agent 호출·조합성이 중요하면 안정적인 CLI/programmatic contract를 우선한다.
- SSH/tmux, 저대역폭 원격 운영, terminal residency 자체가 가치이면 TUI를 조건부 채택한다.
- 이미지·프리뷰·시각 비교·drag-and-drop·공간 배치·다중 패널·표준 컨트롤처럼 반복 인간 작업의 마찰을 실질적으로 줄일 때만 thin GUI를 추가한다.
- keyboard-first와 높은 정보 밀도는 TUI 전용 장점으로 간주하지 않는다. GUI에서도 같은 상호작용 목표를 설계할 수 있다.
- CLI/TUI/GUI는 동일 domain core를 공유하며 어느 surface도 정본·상태·runtime truth를 새로 소유하지 않는다.
- agent가 UI를 생성했거나 한 플랫폼에서 그럴듯하게 동작했다는 사실만으로 품질·접근성·크로스플랫폼 성공을 주장하지 않는다.

검증 ceiling은 다음 순서로 제한한다.

```text
DESIGN_ONLY
→ STATIC_BUILD_VERIFIED
→ INTERACTION_PATH_VERIFIED
→ TARGET_PLATFORM_VERIFIED
→ HUMAN_WORKFLOW_VALUE_VERIFIED
```

`TARGET_PLATFORM_VERIFIED`가 없으면 다른 OS 지원을 추정하지 않는다. `HUMAN_WORKFLOW_VALUE_VERIFIED`가 없으면 GUI/TUI 추가가 CLI-only보다 실제 반복 작업 비용을 줄였다고 주장하지 않는다.

#### AI_GAME_ENGINE_MACHINE_BOUNDARY

게임 엔진·에디터·QA 도구 벤치마크에서 CLI, MCP, typed API, schema/code generation, headless automation 같은 machine-facing 구조가 관찰되면 제품 자체를 복제하거나 엔진 교체를 전제로 하지 않고 `docs/CAPABILITY_COMPOSITION_MAP.md`의 `AI_GAME_ENGINE_MACHINE_BOUNDARY`로 추상화한다.

- `PROJECT_IDENTITY_BEFORE_OPERATION`: 자동화가 암묵적 현재 창·Scene·작업 폴더를 추측하지 않도록 정확한 project identity와 version/pin을 먼저 결속한다.
- `SHARED_CORE_FOR_CLI_AND_MCP`: CLI와 MCP가 각각 별도 mutation/business logic을 갖지 않고 동일 bounded operation core를 호출하는지 본다.
- `SCHEMA_GENERATED_TOOL_SURFACE`: 가능한 경우 하나의 closed schema/type source에서 CLI/MCP contract와 test fixture를 생성하거나 기계 검증해 surface drift를 줄인다.
- `MCP_E2E_BEHAVIOR_CONTRACT`: MCP 연결·tool listing·schema load가 아니라 실제 대표 operation이 project/result/evidence까지 도달하는 behavior E2E를 요구한다.
- `NONINTERACTIVE_AUTOMATION_PATH`: CI/agent가 승인된 bounded operation을 GUI prompt 없이 실행할 수 있는 경로가 있는지 보되 권한·보호 Gate는 유지한다.
- `STRUCTURED_EXECUTION_EVIDENCE`: project/ref, adapter version, typed operation, 결과, 변경/관찰 artifact, log와 `NOT_RUN`/`BLOCKED` 상태를 구조적으로 남긴다.
- 외부 엔진에서 이 패턴이 관찰됐다는 이유만으로 해당 엔진, CLI, SDK, MCP server를 Base나 프로젝트 dependency로 추가하지 않는다. 엔진·provider 채택은 별도 Existing Solution First와 실제 target-project evidence를 요구한다.

COCOS 4/Cocos CLI에서 추출한 현재 사례는 `docs/knowledge/cases/COCOS_AI_NATIVE_ENGINE_INTERFACE_CASE.md`에 둔다. 이 사례의 채택 대상은 provider-neutral machine boundary이며 Cocos runtime이나 TypeScript/C++ stack 자체가 아니다.

### 4. CONTRACT_ABSTRACTION

특정 작품의 이름과 표현을 제거한 뒤 **무엇이 들어오면 어떤 상태 변화와 판단을 거쳐 무엇이 나가는가**를 다시 적는다.

예시:

```text
표면: 전투 후 세 장 중 한 장을 고르는 카드 보상
추상 계약:
  current build state
  → constrained candidate generation
  → mutually exclusive visible choice
  → build state mutation
  → future candidate/value landscape changes
```

이 단계에서 고유 카드, 문구, 아이콘, 확률값, 화면 배치가 남아 있다면 추상화가 충분하지 않은지 다시 확인한다.

### 5. PROJECT_FIT_DISCOVERY

사용자가 예시로 든 장르에만 머물지 않는다. 대상 프로젝트의 최신 정본을 먼저 읽고 다음 병목을 기준으로 **추가 역공학 후보를 능동적으로 찾는다.**

- 플레이어 약속과 핵심 감정.
- Core Loop와 의미 있는 선택.
- 현재 반복되는 설계·콘텐츠 제작 비용.
- 밸런스·검증·QA 병목.
- UI/UX 정보 전달과 입력 마찰.
- 아트·이미지 제작의 반복 파츠와 일관성 병목.
- 프로젝트 데이터·씬·Resource의 반복 구조.
- 개발자가 반복 수행하는 수작업과 도구화 후보.
- GPT/Codex 협업에서 반복되는 작업구조·검수·Skill 후보.
- 플랫폼, 성능, 접근성, 비용, 일정과 권리 제약.

검색 범위는 순서대로 `직접 장르 → 인접 장르/시스템 → 비게임 인터랙션·제품 → 도구/에셋/워크플로/Skill → 실패·반례`까지 넓힌다. 프로젝트 코어에 맞지 않으면 유명하거나 재사용하기 쉬워도 제외한다.

### 6. 재사용 모드 결정

후보마다 다음 중 하나를 명시한다.

- `DIRECT_LICENSED_REUSE`: 라이선스·보안·의존성 검토 후 원본 패키지/에셋을 그대로 재사용.
- `ADAPT_LICENSED`: 허용 범위에서 수정·래핑하여 재사용.
- `PATTERN_EXTRACT`: 원리·계약만 추출하고 프로젝트 구현은 별도로 설계.
- `CLEAN_ROOM_REIMPLEMENTATION`: 직접 원본 구현물을 복사하지 않고, 독립적으로 문서화한 관찰 계약과 테스트를 바탕으로 새 구현을 작성.
- `REJECT`: 권리, 안전, 비용, 품질, 프로젝트 적합성 또는 유지보수 문제로 사용하지 않음.

`CLEAN_ROOM_REIMPLEMENTATION`은 **Base의 엔지니어링 격리 방식 이름일 뿐 법적 면책이나 권리 적합성을 자동 보장하지 않는다.** 직접 재사용이 허용되는 검증된 오픈소스·에셋·도구라면 Existing Solution First에 따라 불필요한 재구현을 피한다.

### 7. NOVELTY_DELTA

`PATTERN_EXTRACT` 또는 `CLEAN_ROOM_REIMPLEMENTATION` 후보는 원본과의 거리만 묻지 않고 **프로젝트에서 실제 판단·경험·생산성이 어떻게 바뀌는지** 기록한다.

```yaml
NOVELTY_DELTA:
  keep:
  remove:
  invert:
  combine:
  add:
  changed_player_decision:
  changed_feedback_or_pacing:
  changed_production_result:
  project_identity_gain:
```

스킨, 명칭, 색만 바뀌고 플레이어 판단이나 제작 계약이 사실상 동일하면 `NOVELTY_DELTA_INSUFFICIENT`로 재검토한다. 장르의 익숙한 문법을 의도적으로 유지하는 경우에는 “익숙함”과 “프로젝트 고유 차별점”을 분리해 기록한다.

### 8. 단위별 검증

재사용 후보의 종류에 맞는 증거를 요구한다.

- 장르·메커닉·시스템·콘텐츠: PoC는 기술/규칙 증거, 플레이 경험은 대표 Vertical Slice와 실제 플레이 증거.
- 데이터 구조: 샘플 데이터, 마이그레이션·직렬화·무결성·극단값 테스트.
- UI/UX: 실제 해상도·입력 흐름·오류 복구·가독성 검증.
- Tool: 대표 프로젝트 입력, 실패/복구, 반복 실행, 성능·의존성·보안 검증.
- Asset/Image material: 실제 사용 맥락의 시각 품질·출처·권리·유사성·재사용성 검토.
- Workflow/Skill: 대표 정상 사례, 실패 사례, 비선택/오라우팅 사례를 포함한 Eval 전후 비교.

유명 작품의 성공 자체는 현재 프로젝트에서의 PASS가 아니다.

### 9. 기존 owner로 승격

이 파이프라인은 **발굴·추상화·분류·라우팅 owner**이지 병렬 자산/도구/Skill 정본을 만들지 않는다.

- 게임 장르·메커닉·시스템·콘텐츠·UI 패턴 → 현재 벤치마크 Case와 프로젝트 기획 정본.
- 에셋·이미지 재료 → `PROJECT_LOCAL_ASSET_VAULT_POLICY.md`의 Reusable Visual Harvest/명시적 승격 절차. 발견만으로 `PROJECT_ASSET_APPROVED`가 되지 않는다.
- Skill·작업구조 후보 → `AI_SKILL_ADOPTION_GUIDE.md`; 기본은 기존 Skill/Mode/Reference에 흡수하고 새 Skill은 마지막 수단이다.
- 외부 작업 프로세스 → `CAPABILITY_COMPOSITION_MAP.md`의 `EXTERNAL_PROCESS_OVERLAY` 경계를 유지한다.
- Godot addon/plugin/tool 후보 → Existing Solution First와 현재 Godot 자산·플러그인 평가 owner를 따른다.
- 라이선스된 코드·도구·에셋 직접 재사용 → 해당 라이선스, 보안, 공급망, 의존성, 프로젝트 소비 경로를 별도로 검증한다.

프로젝트 하나에서만 유효한 결과는 Base에 억지로 승격하지 않고 프로젝트 전용으로 둔다.

## 출처 우선순위

1. 공식 문서·개발자 발표·직접 사용.
2. 신뢰도 높은 연구·분석.
3. 다수 사용자 반응과 패치 이력.
4. 단일 후기·요약·2차 인용.

- 정확한 수치와 규칙은 1차 출처를 확인한다.
- 변경 가능한 정보는 확인 날짜를 남긴다.
- 출처 없이 기억에 의존한 주장은 `가설`로 표시한다.
- 검색 결과 요약만으로 채택 결론을 쓰지 않는다.

## 고정 참고 링크

프로젝트가 고정 참고 링크를 지정하면 작업 유형에 맞는 링크를 먼저 확인한다.

공용 예시:

- 엔진·플랫폼 공식 문서: 기술 가능 범위와 최신 제약.
- 공개 저장소: 폴더, 상태 소유, 테스트, 문서화 사례.
- Steam·itch.io 데모 페이지: 소개, 스크린샷, 데모 흐름, 플레이어 반응.
- 에셋 스토어: 자산 범위, 패키징, 제작 비용과 시장 표현.
- 접근성·인지 연구: 색, 움직임, 입력, 정보 밀도 검수.

프로젝트별 고정 링크와 채택 결론은 프로젝트 저장소에 둔다.

## 사례 수 기준

- 빠른 수정: 관련 사례 1개 이상 또는 기존 고정 참고 확인.
- 일반 기능·아트·연출 판단: 3~5개.
- 장르 핵심 구조, 시장성, 큰 방향 전환: 10개 이상 또는 충분히 다른 접근을 대표하는 표본.
- 이미 승인된 구현 작업: 고정 참고와 충돌 여부만 압축 확인.

자료 수보다 서로 다른 대안과 전제를 비교했는지가 중요하다.

## 적용 결론

```md
## 벤치마킹 결론
- 반드시 반영:
- PoC 검증:
- 조건부 참고:
- 제외:
- 비용·권리 위험:
- 반영할 문서:
- 다음 검증:
```

사례는 영감이 아니라 가설의 근거로 사용하고 실제 사용자·화면·데이터 검증으로 결정한다.

## Base 사례 승격

다음 조건을 만족하면 `templates/KNOWLEDGE_CASE_STUDY.md`로 Base 사례 후보를 작성한다.

- 해결한 문제가 다른 프로젝트에서도 반복될 수 있음.
- 채택·제외 이유와 제약이 명확함.
- 외부 작품의 코드·아트·문구를 복제하지 않음.
- 프로젝트 비공개 정보가 제거되거나 공개가 승인됨.
- 실제 결과 또는 아직 미검증인 항목을 구분함.

한 사례를 바로 보편적 방법으로 승격하지 않는다. 다른 맥락에서 반복 확인된 뒤 method·skill 갱신을 검토한다.