# Evidence-Based Game Development Knowledge System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base의 기존 Skill 수와 책임 경계를 보존하면서 게임 기획·아트·개발·AI·벤치마킹·검증을 외부 근거와 실제 사례로 개선하는 공용 지식 허브와 Template를 추가한다.

**Architecture:** 기존 Skill이 실행 권한을 유지하고 `docs/knowledge/game-development/`가 조건부 Method·Guide·Reference를 제공한다. 프로젝트는 Base 본문을 복제하지 않고 Evidence Pack과 Case Card만 프로젝트 고유 결정에 맞춰 작성한다. 문서 라우터·기획 근거 정책·README가 허브를 연결하고 계약 테스트가 고아 문서·중복 Skill·필수 필드 누락을 막는다.

**Tech Stack:** Markdown, Python `unittest`, GitHub Actions, Base canonical reference freshness·governance tests

## Global Constraints

- Base main의 기존 활성 Skill ID와 실행 책임을 변경하지 않는다.
- 새 광역 Skill을 추가하지 않는다.
- 프로젝트 고유 세계관·수치·경로·자산·구현 상태를 Base에 넣지 않는다.
- 외부 원문을 복제하지 않고 출처 메타데이터와 적용 메모만 기록한다.
- 공식·현업·행동·자기보고·종합·AI 추론을 분리한다.
- AI 산출물은 독립 검수 전까지 권한 원본이 아니다.
- 접근성·성능·라이선스·보안·목표 플랫폼을 적용 가능한 작업의 Quality Bar에 포함한다.
- 모든 변경은 별도 Branch·PR에서 수행하고 Required Checks 후 squash merge한다.

---

### Task 1: RED 계약 테스트와 설계 기준선

**Files:**
- Create: `tests/test_evidence_based_game_development_knowledge.py`
- Create: `docs/superpowers/specs/2026-07-29-evidence-based-game-development-knowledge-system-design.md`
- Create: `docs/superpowers/plans/2026-07-29-evidence-based-game-development-knowledge-system.md`

**Interfaces:**
- Consumes: Base `README.md`, `docs/DOCUMENTATION_MAP.md`, `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`, `skills/SKILL_REGISTRY.json`
- Produces: 필수 파일·라우팅·용어·비중복 계약을 검사하는 unittest

- [ ] **Step 1: 설계 문서를 작성한다**

설계 문서에 목적, 비목표, 정보 구조, 12개 Coverage, Evidence 층·상태·판정, 기존 Skill 라우팅, 프로젝트 적용, 검증 계약을 기록한다.

- [ ] **Step 2: 구현 계획을 작성한다**

각 Task를 독립 검토 가능한 산출물과 검증 단위로 분리한다.

- [ ] **Step 3: 실패하는 계약 테스트를 작성한다**

테스트는 아직 존재하지 않는 지식 문서·Template와 아직 연결되지 않은 라우터를 요구한다.

- [ ] **Step 4: PR을 열고 RED를 확인한다**

Run: GitHub Actions `Validate Game Project Operating System`

Expected: 새 지식 문서 또는 라우팅 경로가 없어 `tests/test_evidence_based_game_development_knowledge.py`가 FAIL.

- [ ] **Step 5: RED 증거를 PR 본문에 기록한다**

실패 Job·테스트 이름·원인을 기록하고 기존 main 실패와 구분한다.

---

### Task 2: 공용 지식 허브와 Method

**Files:**
- Create: `docs/knowledge/game-development/README.md`
- Create: `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`

**Interfaces:**
- Consumes: 설계 문서의 12개 Coverage·Evidence 모델·PLAN/BUILD/REVIEW 흐름
- Produces: 모든 분야 Guide·Template의 단일 라우터와 공통 조사→판정→적용→검증 계약

- [ ] **Step 1: 허브 README를 작성한다**

요청별 최소 읽기, 분야별 Guide, 관련 Skill, 산출물, 비사용 조건을 표로 제공한다.

- [ ] **Step 2: 공통 Method를 작성한다**

`BASELINE_RECOVERY → DECISION_QUESTION → COVERAGE_SELECTION → SOURCE_PLAN → EVIDENCE_COLLECTION → SOURCE_VALIDATION → SYNTHESIS → DECISION → CANON_UPDATE → REVIEW → VALIDATION → LEARNING` 흐름을 작성한다.

- [ ] **Step 3: Evidence 층과 상태를 정의한다**

`T1_PRIMARY_OFFICIAL`부터 `T6_AI_INFERENCE`, `VERIFIED_SOURCE`부터 `UNVERIFIED`, `ADOPT/ADAPT/TEST/AVOID/IGNORE/REFERENCE_ONLY`를 포함한다.

- [ ] **Step 4: 공용/프로젝트 경계를 작성한다**

Base 승격 요소와 프로젝트 유지 요소를 분리한다.

- [ ] **Step 5: 테스트의 허브·Method 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_knowledge_hub_and_method_contract`

Expected: PASS.

---

### Task 3: 게임 기획·플레이어 경험 Guide

**Files:**
- Create: `docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`

**Interfaces:**
- Consumes: MDA·게임 필·Games User Research·Vertical Slice·접근성 근거
- Produces: 프로젝트 코어부터 플레이테스트 판정까지의 게임 기획 절차

- [ ] **Step 1: 플레이어 약속과 코어 정렬 절차를 작성한다**

대상 플레이어, 플레이 상황, 감정·판타지, 핵심 선택, 반복 행동, 보상·기억, 차별 원리를 연결한다.

- [ ] **Step 2: Mechanics→Dynamics→Experience 추적표를 작성한다**

기능 목록이 아니라 규칙·행동·결과·감정·다음 선택을 추적한다.

- [ ] **Step 3: 게임 필·보상·난이도·온보딩 기준을 작성한다**

명료성, 예측 가능성, 피드백, 복구, 피로, 접근성 장벽을 포함한다.

- [ ] **Step 4: 벤치마킹과 플레이테스트 연결을 작성한다**

비교 차원과 결정 질문을 먼저 고정하고 행동·자기보고·실험을 분리한다.

- [ ] **Step 5: 테스트의 게임 기획 Guide 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_game_design_guide_contract`

Expected: PASS.

---

### Task 4: 아트 디렉션·에셋 기획 Guide

**Files:**
- Create: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`

**Interfaces:**
- Consumes: GDC Art Direction·Preproduction·Shape Language·Asset Production·Base 이미지 검수 정책
- Produces: Visual Pillar부터 Runtime Asset Approval까지의 아트 기획 절차

- [ ] **Step 1: 아트 문제 정의를 작성한다**

플레이어 경험, 정보 역할, 세일즈포인트, 제작 규모를 먼저 정의한다.

- [ ] **Step 2: Visual Pillar·Shape·Color·Value·Composition 기준을 작성한다**

캐릭터·환경·UI·이펙트·사운드 연출의 역할과 가독성을 연결한다.

- [ ] **Step 3: Concept→Art Bible→Asset Specification 흐름을 작성한다**

각 단계의 입력·출력·승인 상태·재작업 원인을 정의한다.

- [ ] **Step 4: 인게임 검수와 자산 파이프라인 기준을 작성한다**

실제 해상도·거리·입력·애니메이션·메모리·Import·반복 생산성을 포함한다.

- [ ] **Step 5: 생성형 이미지·외주·기존 에셋의 권리 경계를 작성한다**

원출처·라이선스·유사성·승인 원장·비채택 요소를 기록한다.

- [ ] **Step 6: 테스트의 아트 Guide 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_art_direction_guide_contract`

Expected: PASS.

---

### Task 5: AI 협업 Guide

**Files:**
- Create: `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`

**Interfaces:**
- Consumes: Base GPT–Codex 정책, NIST AI RMF, OpenAI Evals, GitHub Copilot review, Google People + AI guidance
- Produces: AI 역할·권한·Prompt·Evals·보안·비용·독립 검수 계약

- [ ] **Step 1: AI 역할과 권한을 작성한다**

GPT 기획·검수, Codex 구현, 외부 AI 대량 초안, 사용자 승인 경계를 정의한다.

- [ ] **Step 2: Prompt와 Context Pack 구조를 작성한다**

목적·플레이어 가치·범위·제외·입력·산출물·완료·검증·롤백을 포함한다.

- [ ] **Step 3: Contextual Eval 절차를 작성한다**

`SPECIFY → MEASURE → IMPROVE`, golden examples, 실패 분류, 회귀 eval을 정의한다.

- [ ] **Step 4: AI 결과 독립 검수와 보안·권리를 작성한다**

환각 경로, prompt injection, secret, 개인정보, 라이선스, 모델·도구·비용 기록을 포함한다.

- [ ] **Step 5: 테스트의 AI Guide 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_ai_assisted_development_guide_contract`

Expected: PASS.

---

### Task 6: 기술·프로덕션·출시 Guide

**Files:**
- Create: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`

**Interfaces:**
- Consumes: Godot 공식 문서, Android 게임 최적화, Steamworks Playtest·Store·Review, XAG
- Produces: 기획 의도→기술 실현 가능성→제작 파이프라인→플랫폼 검증→출시 후 학습 계약

- [ ] **Step 1: 기술 기획 경계를 작성한다**

Godot Scene·Resource·Autoload·데이터·저장·결정론·디버그·플러그인 경계를 기획 판단과 연결한다.

- [ ] **Step 2: 플랫폼·해상도·입력·성능 계약을 작성한다**

PC·모바일의 base resolution, aspect ratio, UI scale, 터치·키보드·패드, frame time·메모리·발열을 포함한다.

- [ ] **Step 3: 반복 제작성과 Vertical Slice 계약을 작성한다**

두 번째 콘텐츠를 만들 수 있는지, 병목·외주·에셋·자동화·QA 비용을 확인한다.

- [ ] **Step 4: 출시 약속과 플레이어 피드백 계약을 작성한다**

Store page·Demo·Steam Playtest·리뷰·Wishlist·Google Play 테스트가 어떤 결정 증거인지와 한계를 구분한다.

- [ ] **Step 5: 테스트의 기술 Guide 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_technical_production_guide_contract`

Expected: PASS.

---

### Task 7: Reference Catalog·Evidence Pack·Case Card

**Files:**
- Create: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- Create: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- Create: `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`
- Modify: `templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md`

**Interfaces:**
- Consumes: 조사한 공식·학술·현업 출처
- Produces: 출처 메타데이터·근거 판정·적용·반례·검증을 기록하는 공용 양식

- [ ] **Step 1: Reference Catalog를 작성한다**

기관·제목·URL·출처 유형·게시일/버전·확인일·사용 범위·한계·재검증 조건을 기록한다.

- [ ] **Step 2: Evidence Pack Template를 작성한다**

결정 질문, Coverage, Source Plan, 근거 표, 충돌, 판정, 적용 위치, 검증, 미검증을 포함한다.

- [ ] **Step 3: Case Card Template를 작성한다**

성공·실패·혼합, 문제, 접근, 결과, 플레이어 행동·반응, 적용 조건, 복제 금지 요소, 공용화 후보를 포함한다.

- [ ] **Step 4: 기존 벤치마크 Template를 확장한다**

근거 층·Evidence ID·원출처·확인일·실패 사례·`REFERENCE_ONLY`·Case Card 연결을 추가한다.

- [ ] **Step 5: 테스트의 Source·Template 항목을 실행한다**

Run: `python -m unittest tests.test_evidence_based_game_development_knowledge.EvidenceBasedGameDevelopmentKnowledgeTests.test_reference_catalog_and_templates_contract`

Expected: PASS.

---

### Task 8: 문서 라우팅·정본 전파

**Files:**
- Modify: `README.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: 새 허브·Guide·Template 경로
- Produces: 최초 읽기·질문별 라우팅·정책·변경·학습 연결

- [ ] **Step 1: README에 허브 진입점을 추가한다**

게임 기획·아트·개발·AI·벤치마킹 지식체계 링크를 저장소 주요 진입점에 추가한다.

- [ ] **Step 2: Documentation Map을 갱신한다**

공용 책임 원본, 질문별 Reference·Template, 독립 Method 섹션에 새 경로를 추가한다.

- [ ] **Step 3: 기획 근거 정책을 갱신한다**

EVIDENCE_PACK 단계에서 새 Method·Template·Case를 라우팅하고 12영역 Coverage 선택을 명시한다.

- [ ] **Step 4: Changelog·Learning Log를 갱신한다**

적용 이유, 보존한 Skill 경계, 미검증, 후속 프로젝트 Pilot을 기록한다.

- [ ] **Step 5: 전체 신규 계약 테스트를 실행한다**

Run: `python -m unittest tests/test_evidence_based_game_development_knowledge.py`

Expected: PASS.

---

### Task 9: 적대적 검토·회귀·PR 병합

**Files:**
- Review: 모든 변경 파일
- Update as needed: 차단 Finding이 있는 파일

**Interfaces:**
- Consumes: 전체 diff·설계·계획·CI 결과
- Produces: 차단 Finding 0, Required Checks PASS, squash merge, post-merge 증거

- [ ] **Step 1: repository-wide 영향 지도를 작성한다**

정본·진입점·Template·Skill 소비자·테스트·과거 호환 문맥을 확인한다.

- [ ] **Step 2: 적대적 공격을 수행한다**

중복 Skill, 광역 백과사전, 출처 권위 혼동, 성공 사례 편향, 프로젝트 고유값 유입, AI 자동 승인, 플랫폼 정책 고정, 라이선스 누락, 고아 문서, 검증 없는 완료를 공격한다.

- [ ] **Step 3: 비판을 검증하고 최소 수정한다**

`MUST_FIX / SHOULD_FIX / REFERENCE_ONLY / NO_CHANGE / BLOCKED_UNVERIFIED`로 분류하고 기술적으로 판정 가능한 문제를 수정한다.

- [ ] **Step 4: PR diff와 최신 main을 대조한다**

Run: GitHub compare `main...head`, PR changed files, review threads, open duplicate PR search.

- [ ] **Step 5: Required Checks를 확인한다**

Expected: `docs-validation`, `ubuntu-contract`, `publication-validation`, 적용되는 Windows smoke, `ci-gate` PASS.

- [ ] **Step 6: squash merge한다**

Expected: GitHub merge 성공, main이 PR 결과를 포함.

- [ ] **Step 7: post-merge 검증을 수행한다**

새 main에서 핵심 파일, 라우팅 문구, Skill 수 비변경, 열린 중복 PR, 병합 상태를 재확인한다.
