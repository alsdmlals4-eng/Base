# 근거 기반 게임 개발 지식체계 설계

## 1. 목적

Base의 기존 공용 Skill·정책·Template을 유지하면서, 게임 기획·아트 기획·개발·UX·사운드·내러티브·AI 활용·벤치마킹·유저리서치·QA·프로덕션·출시를 외부 근거와 실제 프로젝트 사례로 지속 개선할 수 있는 공용 지식체계를 추가한다.

이 체계의 목표는 자료를 많이 모으는 것이 아니라 다음 질문에 반복 가능하게 답하는 것이다.

> 현재 프로젝트의 플레이어 경험과 제작 결정을 더 좋게 만들기 위해 어떤 근거를 찾고, 어떻게 판정하며, 무엇을 공용화하고, 무엇을 프로젝트에 남겨야 하는가?

## 2. 배경

Base main에는 이미 다음 책임이 존재한다.

- `analyzing-and-refining-game-concepts`: 컨셉·벤치마크·플레이어 근거·플레이테스트
- `governing-game-user-research-coverage`: 11영역 연구 coverage
- `designing-vertical-slices`: 대표 플레이·품질·제작 파이프라인·플레이 증거
- `designing-art-prompts-and-technique-cards`: 이미지 프롬프트·기술 카드·시각화
- `reviewing-and-validating-project-changes`: 변경·접근성·성능·회귀 증거
- `running-adversarial-review-and-refinement`: 실패 가정·비판 검증·승인 개선·회귀
- `evolving-project-discipline-skills`: Skill 생성·통합·학습
- `managing-base-change-proposals`: 프로젝트 교훈의 Base 승격
- `GPT_CODEX_WORKFLOW_POLICY`: GPT 기획·검수와 Codex 구현 권한 분리

문제는 각 책임을 연결해 주는 분야 횡단 지식 허브와 공통 근거 기록 형식이 부족하다는 점이다. 새 Skill을 추가하면 기존 책임과 중복될 가능성이 높으므로, 이번 변경은 기존 Skill의 소비처가 읽는 Method·Guide·Reference·Case·Template 계층을 보강한다.

## 3. 설계 원칙

1. **Skill 수를 늘리지 않는다.** 기존 Skill과 mode가 실행 책임을 유지한다.
2. **자료 수집보다 결정 개선을 우선한다.** 조사에는 반드시 바뀔 결정 질문이 있어야 한다.
3. **기능보다 플레이어 경험을 먼저 본다.** 감정·판타지·선택·고민·보상·기억·세일즈포인트에서 출발한다.
4. **공식 사실·현업 경험·플레이어 반응·행동 증거·AI 해석을 분리한다.** 서로 다른 증거를 같은 권위로 취급하지 않는다.
5. **성공과 실패를 함께 기록한다.** 성공 사례의 표면 기능을 복제하지 않고 적용 조건과 반례를 남긴다.
6. **공용 원리와 프로젝트 고유값을 분리한다.** 세계관·수치·경로·승인 자산·실제 구현 상태는 프로젝트에 남긴다.
7. **AI 결과는 검수 대기 입력이다.** 모델·프롬프트·도구·컨텍스트·비용·검수 결과를 기록한다.
8. **접근성·성능·플랫폼·라이선스를 기획 후반의 부가 검사로 미루지 않는다.** 관련 변경의 Quality Bar에 포함한다.
9. **한 번의 성공은 관찰 또는 가설이다.** 여러 프로젝트 또는 반복 실행 증거 없이 강제 규칙으로 승격하지 않는다.
10. **Progressive Disclosure를 유지한다.** 요청과 관련된 Guide·Reference·Case만 읽는다.

## 4. 정보 구조

```text
docs/knowledge/game-development/
├── README.md
├── EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
├── GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md
├── ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
├── AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
├── TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md
└── REFERENCE_SOURCE_CATALOG.md

templates/research/
├── GAME_DEVELOPMENT_EVIDENCE_PACK.md
└── GAME_DEVELOPMENT_CASE_CARD.md
```

### 4.1 Skill

실행 시점·입력·절차·산출물·품질 기준을 소유한다. 이번 변경에서는 새 Skill을 만들지 않는다.

### 4.2 Method

여러 분야를 관통하는 전체 조사→판정→적용→검증→학습 흐름을 소유한다.

### 4.3 Guide

특정 분야에서 어떤 질문과 산출물을 다뤄야 하는지 설명한다.

### 4.4 Reference Catalog

외부 자료의 출처·날짜·유형·신뢰도·적용 범위·한계를 기록한다. 원문을 복제하지 않고 경로와 사용 메모만 둔다.

### 4.5 Case Card

성공·실패·혼합 사례와 프로젝트 적용 결과를 같은 필드로 기록한다.

### 4.6 Template

개별 프로젝트가 조사 결과와 적용 판정을 일관되게 작성하게 한다.

## 5. Coverage 영역

지식 허브는 다음 12개 영역을 다룬다.

1. 프로젝트 코어·게임 기획
2. 플레이어 경험·게임 필·보상·난이도
3. 아트 디렉션·캐릭터·환경·UI·애니메이션
4. 내러티브·세계관·콘텐츠 설계
5. UX·UI·접근성
6. 사운드·음악·오디오 정보 전달
7. Godot·데이터·저장·성능·플랫폼 기술 기획
8. QA·자동화·런타임·회귀 검증
9. 프로덕션·범위·Vertical Slice·반복 제작성
10. 벤치마킹·Games User Research·텔레메트리
11. AI 협업·Prompt·Evals·보안·권리·독립 검수
12. 출시·스토어·마케팅 약속·출시 후 학습

모든 영역을 매 작업마다 조사하지 않는다. 관련 없는 영역은 이유와 함께 `NOT_APPLICABLE`, 아직 조사하지 않은 영역은 `NOT_STARTED`로 둔다.

## 6. Evidence 모델

### 6.1 근거 층

- `T1_PRIMARY_OFFICIAL`: 공식 플랫폼·엔진·표준·원 논문·개발사 원문
- `T2_PROFESSIONAL_PRACTICE`: GDC 발표·개발자 회고·스튜디오 기술 블로그·현업 가이드
- `T3_PLAYER_BEHAVIOR`: 플레이테스트 관찰·텔레메트리·퍼널·사용성 결과
- `T4_PLAYER_SELF_REPORT`: 리뷰·인터뷰·설문·커뮤니티 반응
- `T5_SYNTHESIS`: 책·리뷰 논문·전문가 종합 자료
- `T6_AI_INFERENCE`: AI 요약·비교·가설. 독립 권한 없음

### 6.2 증거 상태

- `VERIFIED_SOURCE`
- `PARTIALLY_VERIFIED`
- `CONTEXT_LIMITED`
- `STALE_RECHECK_REQUIRED`
- `CONFLICTING_EVIDENCE`
- `UNVERIFIED`

### 6.3 개선 판정

- `ADOPT`
- `ADAPT`
- `TEST`
- `AVOID`
- `IGNORE`
- `REFERENCE_ONLY`

판정에는 플레이어 가치, 코어 정렬, 제작 비용, 기술 위험, 접근성, 성능, 라이선스, 검증 계획이 포함된다.

## 7. 실행 흐름

```text
BASELINE_RECOVERY
→ DECISION_QUESTION
→ COVERAGE_SELECTION
→ SOURCE_PLAN
→ EVIDENCE_COLLECTION
→ SOURCE_VALIDATION
→ SYNTHESIS
→ ADOPT/ADAPT/TEST/AVOID/IGNORE/REFERENCE_ONLY
→ PROJECT_CANON_UPDATE
→ TECHNICAL/ART/CONTENT FEASIBILITY
→ ADVERSARIAL_REVIEW
→ PLAYTEST/EVAL/VALIDATION
→ LEARNING_LOG
→ 필요 시 BCP
```

### 7.1 PLAN

- 프로젝트 코어와 현재 결정을 복원한다.
- 바꿀 결정 질문과 조사 범위를 정한다.
- 공식·현업·플레이어·행동·실패 사례를 분리한다.
- Guide와 Evidence Pack으로 개선안을 제안한다.

### 7.2 BUILD

- 승인된 기획 문서·Template·Reference·Case를 갱신한다.
- Codex에는 승인된 Godot 구현 패키지만 넘긴다.
- AI 생성 결과는 출처·프롬프트·도구·승인 상태를 기록한다.

### 7.3 REVIEW

- `running-adversarial-review-and-refinement`로 범위·전제·표본·과잉 일반화·비용·권리·접근성·성능·회귀를 공격한다.
- `reviewing-and-validating-project-changes`로 실제 diff와 증거를 대조한다.
- 기술적으로 판정 가능한 항목은 사용자에게 질문으로 전가하지 않는다.

## 8. 기존 Skill 라우팅

| 작업 | 주 실행 Skill | 지식 허브 역할 |
|---|---|---|
| 요청·범위·실행 계약 | `managing-project-intake-and-work-contract` | 조사 질문·Coverage·완료 기준 제공 |
| 게임 코어·벤치마킹 | `analyzing-and-refining-game-concepts` | 게임 기획 Guide·Evidence Pack 사용 |
| 11영역 연구 감사 | `governing-game-user-research-coverage` | 12영역 중 연구 관련 영역과 연결 |
| 아트 기획·프롬프트 | `designing-art-prompts-and-technique-cards` | Art Direction Guide·출처·권리 기준 사용 |
| Vertical Slice | `designing-vertical-slices` | 제작성·플랫폼·출시 약속 Guide 사용 |
| Godot 자산·플러그인 | `evaluating-godot-assets-and-plugins-before-creation` | 기술·라이선스·구매 판단 기준 사용 |
| AI 결과 검수 | `reviewing-and-validating-project-changes` | AI Guide의 Evals·독립 검수 기준 사용 |
| 적대적 검토 | `running-adversarial-review-and-refinement` | Case·Evidence의 반례와 한계 공격 |
| Skill 개선 | `evolving-project-discipline-skills` | 반복 실패와 실제 Case를 경계 결정에 사용 |
| Base 승격 | `managing-base-change-proposals` | 공용 원리·프로젝트 고유값 분리 |

## 9. 프로젝트 적용

프로젝트는 Base 문서를 복제하지 않는다. 다음만 프로젝트에 기록한다.

- 현재 결정 질문
- 선택한 Coverage 영역
- Evidence Pack과 Case Card
- `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`
- 프로젝트 고유 기획 결정
- 검증 빌드·표본·플랫폼·결과
- Base 승격 후보와 비승격 이유

## 10. 외부 자료 취급

- 원문 전체를 복제하지 않는다.
- URL·제목·저자/기관·게시일·확인일·버전·핵심 사용 메모를 기록한다.
- 플랫폼 정책·도구 기능·가격·요건은 적용 시점에 공식 출처로 재검증한다.
- Pinterest·커뮤니티·리뷰는 탐색·반응 근거로 사용하되 원출처와 권리를 추적한다.
- 생성형 AI 자료는 저작권·상표·개인정보·비밀·라이선스 위험을 검수한다.

## 11. 검증 계약

1. 새 Skill ID가 추가되지 않는다.
2. 모든 지식 문서와 Template이 존재한다.
3. Documentation Map·README·기획 근거 정책에서 허브를 찾을 수 있다.
4. Evidence Pack이 근거 층·상태·판정·한계·검증을 포함한다.
5. Case Card가 성공·실패·혼합·비복제 요소를 포함한다.
6. Guide가 플레이어 경험→기획→제작성→검증 흐름을 유지한다.
7. AI Guide가 역할·권한·출처·보안·Evals·독립 검수를 포함한다.
8. 기술 Guide가 Godot·모바일/PC·저장·성능·접근성·출시를 연결한다.
9. Reference Catalog가 공식·학술·현업·플랫폼 자료를 분류하고 최신성 재검증 규칙을 가진다.
10. 적대적 검토에서 중복 Skill·광역 문서·근거 없는 강제 규칙·프로젝트 고유값 유입이 없어야 한다.

## 12. 비목표

- 다섯 프로젝트의 기획서를 이번 PR에서 직접 변경하지 않는다.
- 특정 게임의 밸런스 수치·세계관·자산을 Base에 복사하지 않는다.
- 외부 자료를 무단 복제하거나 긴 인용문을 저장하지 않는다.
- AI 모델·도구 하나를 모든 작업의 기본값으로 강제하지 않는다.
- 조사 없이 모든 12영역을 `COMPLETE`로 표시하지 않는다.
- 문서 추가만으로 실제 플레이 재미·접근성·성능·출시 준비가 검증됐다고 주장하지 않는다.

## 13. 완료 기준

- 지식 허브·4개 분야 Guide·Reference Catalog·2개 Template가 추가된다.
- 기존 문서 라우터와 정책에 연결된다.
- 계약 테스트가 통과한다.
- PR의 Required Checks가 통과한다.
- 적대적 검토에서 차단 Finding이 없다.
- main 병합 후 새 main에서 파일·라우팅·PR 상태를 재검사한다.
