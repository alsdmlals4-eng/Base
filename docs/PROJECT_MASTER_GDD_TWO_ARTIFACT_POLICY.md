# Project Master GDD — Desktop GPT 2파일 발행 정책

## 0. 상태와 목적

- Profile ID: `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`
- 상태: `ACTIVE_WHEN_EXPLICITLY_SELECTED`
- 적용 기준: 사용자가 프로젝트 정본을 **사용자용 상세 기획서 PDF + AI용 repository Markdown**의 정확히 두 산출물로 정리하라고 명시한 경우
- 목적: Desktop GPT에서 사람이 읽을 완성도 높은 제작 기획서와 AI/Codex가 실행할 정밀 구현 계약을 중복 surface 없이 유지한다.
- 비목적: 모든 프로젝트의 기본 workspace를 일괄 변경하거나 기존 Notion 자료를 삭제·폐기하는 것

이 profile은 기존 `DOMAIN_SPLIT_CANON` 위에 선택적으로 적용하는 bounded publication profile이다. `GLOBAL_NOTION_DEPRECATION_FORBIDDEN`: 이 문서를 근거로 모든 프로젝트에서 Notion을 폐기하거나 기존 사람용 정본을 자동 삭제하지 않는다.

## 1. 산출물 계약

`EXACTLY_TWO_DELIVERABLES`

| 구분 | 고정 역할 | 기본 경로 | 사용자 다운로드 |
|---|---|---|---|
| `HUMAN_MASTER_GDD_PDF` | 사람이 프로젝트 전체·핵심 시스템·핵심 콘텐츠·구현 원리를 시각적으로 이해하는 상세 제작 기획서 snapshot | `exports/[PROJECT]_MASTER_PRODUCTION_GDD_[YYYYMMDD].pdf` | 제공 |
| `AI_PRODUCTION_SPEC_MARKDOWN` | GPT/Codex가 후속 기획·구현·테스트·검수를 이어가는 구조화 기획·구현 명세 | `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` | 제공하지 않고 repository 위치만 보고 |

산출물 제한:

- `NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX`
- `NO_SEPARATE_IMAGE_BUNDLE`
- 별도 benchmark 보고서, traceability 표, asset matrix, QA 부록은 만들지 않고 두 산출물 내부에 통합한다.
- 외부 제출처가 다른 형식을 명시한 경우에만 별도 profile 또는 사용자 승인으로 예외를 둔다.

## 2. 사용자용 상세 PDF 계약

`CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED`

사용자용 PDF는 홍보용 개요나 짧은 요약본이 아니다. 이 파일 하나만 읽어도 다음을 이해할 수 있는 시각 중심 통합 제작 기획서여야 한다.

### 2.1 프로젝트와 플레이어 경험

- 한 줄 소개, 장르, 플랫폼, 대상 플레이어, 현재 단계
- 플레이어 역할·판타지·핵심 약속
- 플레이어 감정, 선택, 고민, 보상, 기억, 첫인상
- 디자인 필러, 차별점, 판매 포인트, 범위 안/밖
- 첫 5분·15분·30분 경험과 학습 순서
- Core Loop, Session Loop, Meta Loop, 실패·복구 Loop

### 2.2 핵심 시스템

각 핵심 시스템과 필요한 서브 시스템은 공통 ID로 식별하고 다음 5단 구조로 설명한다.

1. **왜 존재하는가**: 플레이어 가치, 목표 감정, 핵심 선택, 보상, 차별점
2. **어떻게 플레이하는가**: 진입·종료 조건, 입력, 규칙, 처리 순서, 성공·실패, 예외·복구
3. **어떤 콘텐츠가 필요한가**: 스테이지, 유닛, 적, 아이템, 능력, 사건, UI, 이미지, 애니메이션, VFX, SFX, 데이터
4. **어떻게 구현하는가**: Godot 씬, 노드, 스크립트 책임, 데이터 소유권, 상태 전이, 신호·이벤트, 입력, UI 연결, 저장·로드, 의존성, 성능 위험, 구현 순서
5. **어떻게 완료를 판정하는가**: Acceptance Criteria, 자동 테스트, 통합 테스트, runtime 검증, UX 검증, 남은 범위

### 2.3 핵심 콘텐츠

각 핵심 콘텐츠는 단순 목록이 아니라 다음을 포함한다.

- 콘텐츠 ID, 목적, 목표 경험, 등장·해금 조건
- 소비하는 시스템과 영향을 받는 시스템
- 규칙, 상태, 변주, 난이도, 보상, 실패·복구
- 요구 UI·runtime asset·animation·VFX·SFX·audio
- Godot scene/resource/data/script 구성과 재사용 구조
- 구현·튜닝·검증 순서 및 Acceptance Criteria

### 2.4 구현 설명의 최소 깊이

- 권장 scene tree와 각 노드 책임
- controller/model/view/resolver/persistence 책임 분리
- script 간 입력·출력과 공개 API
- Resource/JSON/Dictionary 등 실제 data owner와 field/type/default/range
- 상태 전이와 비정상·중복 입력 처리
- 신호의 emitter/receiver/payload/timing
- UI 기본·hover·pressed·disabled·locked·warning/error 상태
- 저장·로드 시 복원 범위와 migration 고려
- 플랫폼·해상도·입력·성능 제약
- 기존 module/asset/reference 재사용 여부
- 구현 순서와 각 단계의 확인 방법

### 2.5 필수 시각자료

프로젝트에 해당하는 범위에서 다음을 PDF 내부에 포함한다.

- 승인 대표 이미지 또는 실제 플레이 화면
- One-Page Project Vision
- Core/Session/Meta Loop
- 전체 Game Flow와 시스템 관계도
- 상태 전이도와 시스템 처리 순서도
- UX Screen Flow, 주요 화면 wireframe, 첫 10~30분 storyboard
- 진행·해금 구조, 자원 Source–Sink, 콘텐츠 관계도
- 세계·세력·인물 관계도
- Visual Bible과 asset family
- Runtime Asset/Audio Consumer 연결도
- 실제 구현 증거 화면 또는 실제 build capture

모든 도식·이미지에는 목적, 관련 ID, source, 승인 상태, consumer, 구현 상태, runtime 검증 상태를 표시한다.

## 3. AI용 상세 기획·구현 명세 계약

`AI_PRODUCTION_SPEC_MARKDOWN`은 사람이 읽는 PDF의 원문 복제본이 아니라 machine-searchable active specification이다. 최소 구조는 다음과 같다.

1. `CANON SNAPSHOT`
2. `SOURCE REGISTRY`
3. Current Project State
4. Confirmed Decisions
5. Design Pillars / Player Experience Contract
6. Core / Session / Meta Loop
7. `SYSTEM REGISTRY`
8. System Specifications
9. `CONTENT REGISTRY`
10. Content Specifications
11. UI/UX and Input Contract
12. Visual Asset Consumer Matrix
13. Audio Consumer Matrix
14. Technical Architecture
15. `DATA CONTRACTS`
16. `SCENE MAP`
17. `SCRIPT RESPONSIBILITY MAP`
18. `SIGNAL AND EVENT FLOW`
19. `STATE MACHINES`
20. `SAVE/LOAD CONTRACT`
21. `IMPLEMENTATION TRACEABILITY`
22. `TEST AND QA CONTRACT`
23. Vertical Slice Definition
24. Risks and Blockers
25. User Decision Required
26. `IMPLEMENTATION QUEUE`
27. Change Log

각 시스템·콘텐츠 명세는 ID, player contract, rules, entry/exit, states, transitions, data contract, scene/node/script owner, signals/events, UI/asset/audio consumers, save/load, dependencies, implementation order, Acceptance Criteria, automated/integration/runtime/UX verification, remaining work를 포함한다.

`RUNTIME_TRUTH_SEPARATE`: AI 명세는 기획·구현 계약의 active owner가 될 수 있지만 실제 `.gd`, `.tscn`, `.tres`, `.json`, import 설정, test, build, runtime evidence를 대체하지 않는다.

## 4. Notion 입력 전용 경계

`NOTION_INPUT_ONLY_NO_OUTPUT`

이 profile에서는:

- 기존 Notion에 repository로 이관되지 않은 **고유 미이관 자료**가 있는지 먼저 확인한다.
- 해당 자료가 있으면 기존 Notion을 입력 자료로만 fresh-read하고 Source Registry와 migration gap에 출처를 남긴다.
- master GDD를 위해 새 Notion page/database/view를 만들지 않는다.
- Notion은 신규 출력·갱신·동기화·readback 대상이 아니다.
- 기존 승인 정보와 시각자료를 이관한 뒤 원본 폐기 여부는 별도 migration 결정으로 다룬다.
- 사용자가 일반 프로젝트 운영에서 Notion 정본을 유지하라고 명시하면 기존 `DOMAIN_SPLIT_CANON`과 `NOTION_OPERATION_GATE`를 계속 적용한다.

## 5. 공통 ID·동일 시점 계약

`SHARED_ID_AND_SOURCE_SHA_REQUIRED`

PDF와 AI Markdown은 같은 항목에 같은 ID를 사용한다.

- 시스템: `SYS-`
- 콘텐츠: `CNT-`
- UI: `UI-`
- UX Flow: `UX-`
- 시각 에셋: `AST-`
- 오디오: `AUD-`
- 데이터 계약: `DAT-`
- QA: `QA-`
- 결정: `DEC-`

두 파일에는 동일한 source branch, 기준 commit SHA, 생성일을 기록한다. PDF 생성 직전 AI 명세와 실제 repository를 다시 읽어 ID·규칙·상태·SHA 불일치를 검사한다.

구현 현실 상태는 다음을 합치지 않는다.

```text
DOCUMENTED
→ CONFIRMED
→ IMPLEMENTED
→ AUTOMATED_TEST_PASS
→ RUNTIME_VERIFIED
→ UX_VERIFIED
→ RELEASE_READY
```

하위 evidence가 없으면 상위 상태를 주장하지 않는다.

## 6. 벤치마킹·현업 조사 계약

Master GDD를 새로 만들거나 대규모 갱신할 때는 현재 장르·플랫폼에 맞는 근거를 조사한다.

- 직접 경쟁작 5~8개
- 인접 장르 참고작 2~3개
- 핵심 시스템, UI/UX, 접근성, 시각 가독성, 사운드 피드백, 콘텐츠 생산, 실패 사례

결과는 `ADOPT / ADAPT / REJECT`로 판정하며 관찰, 적용 범위, 적용 금지점, 플레이어 영향, 구현·콘텐츠 비용, 위험, 검증 방법, 출처, 조사일을 남긴다. 레퍼런스 게임 이름만 적고 구현을 위임하지 않는다.

## 7. 이미지·시각자료 경계

`NO_AUTOMATIC_IMAGE_GENERATION`

- 기존 승인 이미지와 실제 build capture를 우선 사용한다.
- 승인 visual이 없으면 `현재 승인 Visual 없음`과 필요한 consumer·상태·규격을 기록한다.
- 문서용 flow/state/system diagram은 편집 가능한 text/Mermaid/vector 방식으로 만들 수 있다.
- 새로운 concept/runtime/store image 생성·편집은 별도의 사용자 명시적 요청이 있을 때만 진행한다.
- 이미지 존재를 runtime consumer 연결 또는 UX 검증 완료로 간주하지 않는다.

## 8. 생성·검증 순서

```text
fresh-read current authority
→ conflict/gap reconciliation
→ benchmark and field research
→ shared ID registry
→ AI production spec update
→ implementation/runtime traceability readback
→ human PDF composition
→ same branch/SHA check
→ PDF render and page inspection
→ focused regression + repository checks
→ final delivery
```

PDF 검증에는 파일 열기, 페이지 수, 목차·페이지 번호, 한글 font, 표·도식 잘림, 이미지 해상도, caption, 내부 link, 빈 페이지, 기준 SHA, 실제 page render inspection을 포함한다.

## 9. 최종 제공 계약

`PDF_ONLY_USER_DOWNLOAD`

최종 사용자 응답에는 사용자용 상세 PDF 하나만 다운로드 링크로 제공한다.

`AI_SPEC_REPOSITORY_PATH_REPORT_ONLY`

AI 명세는 별도 다운로드 링크를 제공하지 않고 다음 정보만 보고한다.

- repository path
- branch
- commit SHA
- PR
- validation result

작업지시문 템플릿 자체를 사용자가 별도로 요청한 경우에는 그 템플릿 파일을 배포할 수 있다. 이것은 프로젝트 master GDD의 2개 결과물에 포함되지 않는 Base 운영 도구다.

## 10. 완료 조건

- 정확히 두 프로젝트 산출물만 생성됨
- 최신 정본 누락·미표시 충돌 0
- 핵심 시스템·핵심 콘텐츠 누락 0
- 시스템·콘텐츠별 Godot 구현 설명 누락 0
- 시스템↔콘텐츠↔UI↔asset/audio↔scene/script/data↔test 추적 누락 0
- PDF와 AI 문서 ID·source SHA 불일치 0
- 근거 없는 구현·runtime·UX·release 완료 주장 0
- 목적 없는 시각자료와 자동 이미지 생성 0
- Notion 신규 출력·동기화 0
- PDF 렌더 오류 0
- 검증 가능한 문서 생성 작업의 남은 작업 0
