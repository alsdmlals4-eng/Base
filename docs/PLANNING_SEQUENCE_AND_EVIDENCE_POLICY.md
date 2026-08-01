# 기획 작업순서·근거·데모 우선 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 기획 작업을 어떤 순서로 묶고, 무엇을 먼저 비교하며, 어떤 근거로 승인하고, 새 정책·Template·Skill을 어디까지 전파 검증할지 정하는 공용 책임 원본이다.

승인 결정의 즉시 정본화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`, 작업 분해의 상세 의존성은 `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`, 외부 근거의 판정은 `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`, 분야 횡단 게임 개발 근거·Guide·Case는 `docs/knowledge/game-development/README.md`, 데모 제작 Gate는 `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`, 프로젝트 Sheet와 GPT 이미지 생성·검수는 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 책임진다. 프로젝트 GDD Google Sheets의 사용자 작업면·편집·동기화·시각화·수치화 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다.

공통 조사 기록은 `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`, 성공·실패·혼합 사례는 `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`를 사용한다. 이 Template은 외부 자료를 프로젝트 정본으로 승격하지 않고 결정 질문·Evidence ID·적용 판정·검증을 연결한다.

## 1. 적용 범위

### Google Sheets

- Base 저장소 자체: `BASE_EXCLUDED`. 프로젝트 Google Sheets를 만들거나 동기화하지 않는다.
- 개별 프로젝트의 정확한 Sheet URL·ID·tab·권한이 확인됨: `PROJECT_SHEET_CONFIGURED`이며 역할은 `USER_FACING_GDD_WORKSPACE`다.
- 개별 프로젝트에 Sheet가 없거나 아직 연결하지 않음: `NOT_CONFIGURED`.
- Base 작업을 Sheet 미동기화로 실패 처리하지 않는다.
- 사용자는 Sheet에서 전체 GDD 흐름·방향성·메인 시스템·이미지·수치·상태를 확인하고 수정한다.
- AI는 GitHub 정본·실제 파일과 Sheet를 함께 읽고 `PROPOSED_SHEET_CHANGE`·누락·충돌을 판정한다.
- Sheet는 시각화 우선, 지속 갱신, 명확한 수치화를 따르며 GitHub 정본이나 실제 구현을 대체하지 않는다.
- 승인된 변경만 GitHub 정본·Commit·Sheet에 반영하고 재조회해 `SYNCED`를 증명한다.

### 내용 보존

- 문서·Skill·정책·Template에 줄 수, 문자 수, 페이지 수, 분량 상한을 완료 조건으로 두지 않는다.
- 간결성보다 내용 보존, 실행 가능성, 책임 경계, 한 단계 발견성, 검증 가능성을 우선한다.
- Reference 분리는 문서를 짧게 만들기 위한 축약이 아니라 책임 분리와 조건부 발견성을 위한 것이다.
- 기존 결정·예외·실패 조건·표·검증 절차가 손실되면 간소화가 아니라 회귀다.

## 2. 모든 L1 이상 작업의 선행 감사

새 질문·기획·계획·구현·검수 전에 다음을 비교한다.

```text
최신 main
→ CURRENT_CONFIRMED_DECISIONS.md
→ 관련 분야 책임 원본
→ 같은 Goal의 열린 PR·최근 병합 PR·대체 PR
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 개별 프로젝트 Google Sheets(PROJECT_SHEET_CONFIGURED일 때)
→ Decision ID·Commit·대체 관계·현재 단계 비교
→ 중복·누락·충돌·구형 참조·미반영 판정
```

필수 판정:

- `DUPLICATE_WORK`: 같은 결과가 이미 정본·구현·PR에 존재한다.
- `DUPLICATE_QUESTION`: 유효한 기존 Decision을 다시 묻는다.
- `MISSING_CANON`: 승인된 내용이 책임 원본에 승격되지 않았다.
- `MISSING_CONSUMER`: 새 정책·Template·Skill을 읽어야 할 소비처가 연결되지 않았다.
- `CANON_CONFLICT`: 둘 이상의 현행 책임 원본이 서로 다른 결정을 주장한다.
- `IMPLEMENTATION_CONFLICT`: 정본과 실제 구현이 다르다.
- `STALE_REFERENCE`: 구형 경로·ID·정책·대체된 결정을 계속 참조한다.
- `MISSING_SYNC`: GitHub 정본·개별 프로젝트 Sheet·추적 surface 중 일부가 누락됐다.
- `NO_CONFLICT`: 현재 범위에서 신규 작업을 진행할 수 있다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·권한·도구·실행 증거가 없어 판정할 수 없다.

차단 Finding이 있으면 새 작업보다 복원·정리·재동기화를 먼저 수행한다.

## 3. 공통 8단계 작업 루프

```text
1. BASELINE_RECOVERY
→ 2. DUPLICATE_OMISSION_CONFLICT_AUDIT
→ 3. EVIDENCE_PACK
→ 4. APPROVAL_BUNDLE
→ 5. CANONICAL_UPDATE
→ 6. PROPAGATION_AUDIT
→ 7. VALIDATION
→ 8. GATE_CLOSE
```

### 3.1 BASELINE_RECOVERY

현재 Decision, 정본, 실제 구현, PR, 프로젝트 Sheet 상태를 복원한다. 이미 확인 가능한 사실은 사용자에게 되묻지 않는다.

### 3.2 DUPLICATE_OMISSION_CONFLICT_AUDIT

작업 시작 전에 필수 판정을 기록한다. 같은 작업·질문을 문구만 바꿔 반복하지 않는다.

### 3.3 EVIDENCE_PACK

중요 기획·방향성·제품 결정은 다음 세 층을 모두 검토한다.

1. `BENCHMARK_EVIDENCE`: 직접 경쟁작, 인접 장르, 실패·혼합 반응 사례.
2. `PLAYER_RESPONSE_EVIDENCE`: 긍정·부정·혼합 리뷰, 커뮤니티, 플레이테스트, 행동 데이터.
3. `PROFESSIONAL_OFFICIAL_EVIDENCE`: 현업 발표·사후 분석·공식 플랫폼·엔진·접근성·운영 권장사항.

분야 횡단 결정에서는 `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`의 12영역 Coverage 중 현재 결정에 필요한 영역만 선택한다.

```text
프로젝트 코어·게임 기획
플레이어 경험·게임 필·보상·난이도
아트 디렉션·캐릭터·환경·UI·애니메이션
내러티브·세계관·콘텐츠
UX·UI·접근성
사운드·오디오 정보
Godot·데이터·저장·성능·플랫폼
QA·자동화·런타임·회귀
프로덕션·Vertical Slice·반복 제작성
벤치마킹·Games User Research·텔레메트리
AI 협업·Prompt·Evals·보안·권리
출시·스토어·마케팅 약속·출시 후 학습
```

모든 영역을 형식적으로 조사하지 않는다. 근거가 없으면 `NOT_STARTED`, 관련 없으면 이유를 가진 `NOT_APPLICABLE`로 둔다.

Evidence는 다음을 분리한다.

- `T1_PRIMARY_OFFICIAL`: 공식·원 논문·실제 프로젝트 증거
- `T2_PROFESSIONAL_PRACTICE`: 현업 발표·개발자 회고·스튜디오 기술 자료
- `T3_PLAYER_BEHAVIOR`: 플레이테스트 관찰·텔레메트리·퍼널
- `T4_PLAYER_SELF_REPORT`: 리뷰·인터뷰·설문·커뮤니티 반응
- `T5_SYNTHESIS`: 전문 서적·리뷰 논문·종합 자료
- `T6_AI_INFERENCE`: AI 요약·분류·가설. 독립 권한 없음

조사 결과는 `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`에 Evidence ID·원출처·날짜·버전·상태·한계로 기록하고, 성공·실패·혼합 사례는 `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`로 연결한다.

단순 오탈자, 기계적 링크 수정, 같은 입력의 검사 재실행 같은 L0 작업은 대규모 근거 조사를 요구하지 않는다. 근거는 정본을 대체하지 않으며 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 변환한다.

### 3.4 APPROVAL_BUNDLE

같은 플레이어 경험·시스템·정본·후속 구현에 영향을 주는 결정을 분야별 묶음으로 승인한다.

```yaml
bundle_id:
discipline:
current_decisions:
duplicate_omission_conflict_result:
evidence_pack_path:
evidence_ids:
case_card_paths:
questions_and_options:
gpt_recommendation:
approved_decisions:
dependencies:
affected_canonical_sources:
affected_consumers:
project_sheet_tabs:
validation_gate:
```

기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리한다. 프로젝트 코어·중요 기획·방향성·정본 충돌만 `USER_DECISION_REQUIRED`로 올린다.

### 3.5 CANONICAL_UPDATE

승인된 Decision을 `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 필요한 Active Context·Issue·Plan에 반영한다. 개별 프로젝트가 `PROJECT_SHEET_CONFIGURED`이면 같은 승인 단위에서 Sheet도 갱신한다.

외부 Evidence Pack과 Case Card는 결정 근거를 소유하지만 최종 프로젝트 기획 권한은 등록된 책임 원본이 가진다. 실제 구현 사실은 코드·데이터·자산·테스트가 가진다.

### 3.6 PROPAGATION_AUDIT

새 정책·Template·Skill·경로·ID를 추가하거나 바꾸면 파일 존재가 아니라 실제 소비를 검사한다.

- 항상 읽는 진입점: `AGENTS.md`, `START_HERE.md`, `README.md`.
- 운영 정본: `OPERATING_MODEL`, Work Mode·Skill routing, Documentation Map.
- 라우팅: Skill Registry, Legacy Alias, shared route.
- 프로젝트 설치: Template README, Project START_HERE, AI_WORKFLOW, 설치·감사·검증 Skill.
- 분야 소비자: 관련 기획서, 분야 Skill, Reference, 데이터 계약.
- 근거 소비자: Evidence Pack, Case Card, 벤치마크 Template, Reference Catalog.
- 검증: reference freshness, 회귀 테스트, publication·generation, Governance.
- 기록: Learning Log, Changelog, 구현 계획, 병합 후 보고.
- 프로젝트 작업면: 개별 프로젝트 Google Sheets의 해당 tab·row.

소비처가 빠지면 `MISSING_CONSUMER`이며 Gate를 닫지 않는다.

### 3.7 VALIDATION

정본 비교, 정적 검사, 런타임, 접근성, 성능, 플레이테스트, 반응 조사, AI Eval, 적대적 검토 중 현재 범위에 필요한 검증을 실제 실행한다.

적대적 검토는 다음을 포함한다.

- 성공 사례 표면 복사
- 다른 장르·팀 규모·플랫폼 과잉 일반화
- 행동과 자기보고 혼동
- AI 추론을 공식 사실로 사용
- 접근성·성능·보안·라이선스·제작 비용 누락
- 새 Skill·Guide·Template의 중복 책임
- 실행하지 않은 검증 완료 주장

### 3.8 GATE_CLOSE

다음을 기록한다.

```text
APPROVED
CANON_UPDATED
CONSUMERS_UPDATED
IMPLEMENTED | IMPLEMENTATION_PENDING
VALIDATED | BLOCKED_UNVERIFIED
SHEET_SYNCED | BASE_EXCLUDED | NOT_CONFIGURED
NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

## 4. 프로젝트 기획 작업순서

분야별 Approval Bundle과 단계별 Gate를 혼합한다.

```text
00 프로젝트 기반·현재 상태
→ 10 제품 방향·시장 약속
→ 11 세계관
→ 12 핵심루프
→ 13 주요인물
→ 14 조연·세력·관계
→ 20 코어 경험·메인게임·데모 목표
→ 30 데모 범위·품질 기준·제작 기반
→ 40 핵심시스템·메인콘텐츠
→ 41 성장·경제
→ 50 메인 콘텐츠
→ 51 미니게임(해당 프로젝트만)
→ 52 글쓰기·서사(해당 프로젝트만)
→ 60 UX·UI·접근성
→ 70 아트·오디오·에셋
→ 71 기획 이미지·목업 생성
→ 72 이미지 검수·승인
→ 80 완성 품질 Vertical Slice 데모·플레이테스트
→ 90 본제작·출시·사업
→ 98 Base 반영 후보
→ 99 변경 이력·회고
```

앞 단계가 완전히 끝날 때까지 뒤 분야를 금지하는 폭포수 모델이 아니다. 다만 승인 묶음의 책임 원본과 의존성이 고정되지 않았다면 같은 파일·Schema·자산을 경쟁적으로 수정하지 않는다.

## 5. Demo-First Vertical Slice

기본 제품 경로는 별도 `CORE_POC` Gate를 사용하지 않는다.

```text
CONCEPT_APPROVAL
→ DEMO_FIRST_VERTICAL_SLICE
→ 통합 데모 QA
→ 내부 플레이테스트
→ 외부 플레이테스트·반응 조사
→ DEMO_VALIDATION
→ PRODUCTION_APPROVAL
```

목표는 폐기형 Prototype이 아니라 최종 방향에 가까운 아트·UI·UX·사운드·데이터·저장·복구·성능·접근성을 갖춘 **완성 품질 데모**다.

기술 불확실성이 데모 전체를 차단할 때만 Vertical Slice 작업 내부에 제한된 `TECHNICAL_SPIKE`를 둔다.

- 별도 제품 단계나 사용자 공개 데모로 간주하지 않는다.
- 질문 하나와 성공·실패·중단 기준을 가진다.
- 결과는 데모 구현에 재사용하거나 결정 근거로 기록한다.
- Spike를 이유로 저품질 임시 빌드를 최종 데모처럼 승인하지 않는다.
- 위험한 가설을 숨기지 않되 `CORE_POC` 완료를 별도 Gate로 요구하지 않는다.

과거 `PROTOTYPE_AND_VERTICAL_SLICE`, `CORE_POC`, `SLICE_VALIDATION` 기록은 역사·호환 용어로 보존할 수 있다. 새 작업에서는 각각 `DEMO_FIRST_VERTICAL_SLICE`, 내부 `TECHNICAL_SPIKE`, `DEMO_VALIDATION`으로 해석한다.

## 6. 개별 프로젝트 Google Sheets tab 기준

Base에는 생성하지 않는다. 개별 프로젝트에서만 다음 순서를 사용한다.

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
05_GDD_요약
10_제품방향
11_세계관
12_핵심루프
13_주요인물
14_조연_세력_관계
15_조작_게임규칙
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_핵심시스템_메인콘텐츠
41_성장_경제
50_메인콘텐츠
51_미니게임
52_글쓰기_서사
60_UX_UI_접근성
70_아트_오디오_에셋
71_이미지기획_생성목록
72_이미지검수_승인로그
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

필요하지 않은 `51_미니게임`, `52_글쓰기_서사`는 생성하지 않는다. 공통 열과 분야별 세부 열은 `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`를 따른다.

`03_근거_라이브러리`는 프로젝트별 Evidence Pack·Evidence ID·Case Card·원출처·확인일·판정·적용 위치를 연결한다. Base 자체에는 프로젝트 Sheet를 만들지 않는다.

## 7. 실패 조건

- 이전 기록을 읽지 않고 같은 질문·작업을 반복한다.
- 새 정책·Template·Skill을 만들고 실제 소비처를 연결하지 않는다.
- 인기작 기능이나 단일 리뷰만으로 방향을 바꾼다.
- 성공 사례만 조사하고 실패·혼합 반응·적용 조건을 누락한다.
- 현업·공식 근거를 조사하지 않고 모델 추론만 권장안으로 제시한다.
- 플레이어 행동과 플레이어 자기보고를 같은 증거로 취급한다.
- 관련 결정을 여러 탭·문서·PR에 흩어 승인한다.
- 문서 길이를 줄이기 위해 결정·예외·검증·실패 조건을 삭제한다.
- 별도 `CORE_POC`를 필수 Gate로 되살린다.
- 임시 Prototype 품질을 완성 데모 품질로 오인한다.
- Base에 프로젝트 Google Sheets 동기화를 요구한다.
- Evidence Pack·Case Card 작성만으로 실제 재미·접근성·성능·출시 준비를 검증했다고 주장한다.

## Base v9.4 Context 큐레이션 Gate

Context 선별이 기획 근거를 바꾸는 작업에서는 `decision_question / include_criteria / exclude_criteria / authority_level / freshness / representation / deduplication / known_conflicts / progressive_load_trigger / refresh_trigger`를 기록한다.

반대 근거·실패 사례·보호 규칙을 관련 없다는 이유로 제거하지 않는다. 제외에는 이유와 재조회 조건을 남기며, 화면·Schema·Fixture 같은 Artifact가 런타임·사람 이해·접근성·성능을 증명한다고 과장하지 않는다.
