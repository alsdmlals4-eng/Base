# 근거 기반 게임 개발 지식 허브

이 디렉터리는 게임 기획·아트 기획·개발·AI 활용·벤치마킹·유저리서치·검증·출시를 외부 근거와 실제 프로젝트 사례로 개선하기 위한 **조건부 공용 지식 허브**다.

이 허브는 새로운 실행 Skill이 아니다. 실행 권한은 기존 Base Skill이 유지하며, 이 문서들은 해당 Skill이 필요한 Method·Guide·Reference·Case·Template를 선택적으로 읽게 한다.

## 1. 핵심 원칙

- 자료 수집량보다 현재 결정을 개선하는가를 우선한다.
- 기능 목록보다 플레이어 경험·감정·판타지·선택·고민·보상·기억·세일즈포인트를 먼저 정의한다.
- 공식 사실, 현업 경험, 플레이어 행동, 플레이어 자기보고, 종합 자료, AI 추론을 구분한다.
- 성공 사례뿐 아니라 실패·혼합 사례, 적용 조건과 반례를 기록한다.
- 외부 사례는 프로젝트 정본이나 실제 구현 사실을 대체하지 않는다.
- 공용 원리와 프로젝트 고유 세계관·수치·경로·자산·구현 상태를 분리한다.
- AI 결과는 독립 검수 전까지 검수 대기 입력이다.
- 한 번의 성공은 관찰 또는 가설이며 반복 검증 전에는 공용 강제 규칙으로 승격하지 않는다.
- 모든 분야를 매 작업마다 읽지 않는다. 현재 결정과 연결된 문서만 연다.

## 2. 최소 읽기

```text
프로젝트 AGENTS·START_HERE·Active Context
→ 현재 결정·책임 원본·실제 파일
→ skills/SKILL_REGISTRY.json
→ 자동 선택된 기존 Skill·Skill Mode
→ 이 허브의 관련 Method·Guide·Reference·Template
→ 프로젝트 Evidence Pack·Case Card
→ 적대적 검토·검증·학습
```

## 3. 문서 지도

| 질문 | 먼저 읽을 문서 | 주요 산출물 |
|---|---|---|
| 외부 근거를 어떻게 찾고 판정·적용하는가? | `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md` | Evidence Pack·개선 판정·검증 계획 |
| 게임 코어·플레이어 경험·게임 필·보상·난이도를 어떻게 설계하는가? | `GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md` | 플레이어 약속·MDE 추적표·플레이테스트 계약 |
| 그림체·비주얼·캐릭터·환경·UI·애니메이션·에셋을 어떻게 기획하는가? | `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` | Visual Pillar·Art Bible·Asset Specification |
| ChatGPT·Codex·외부 AI를 어떻게 안전하고 검증 가능하게 협업시키는가? | `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md` | Prompt 계약·Context Pack·Evals·독립 검수 |
| Godot·플랫폼·성능·제작 파이프라인·출시를 어떻게 기획에 연결하는가? | `TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md` | 기술 계약·성능 예산·반복 제작성·출시 증거 |
| Windows+Android를 처음부터 함께 설계하고 STOVE·Google Play·Steam 출시 wave를 어떻게 나누는가? | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` | 적합성 판정·공용 코어/플랫폼 어댑터·기기 QA·출시 Profile |
| Steam·STOVE·Google Play 등급·설문·자산 권리·참조 독립 제작을 어떻게 관리하는가? | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` | 등급 전략·자산 권리 Record·출시 Compliance Pack |
| 어떤 공식·학술·현업 자료를 우선 참조하는가? | `REFERENCE_SOURCE_CATALOG.md` | 출처 메타데이터·사용 범위·재검증 조건 |
| 작은 표본·저충실도 사람 세션을 어떻게 과장 없이 설계하는가? | `docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md` | 사람 세션 패킷·claim ceiling·미검증 분리 |
| 실제 테스터가 없을 때 AI 가상 페르소나로 무엇을 검토할 수 있는가? | `docs/knowledge/game-development/SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md` | 프로젝트 구조 분석·T6 합성 위험 검토·TEST 게이트 |

## 4. 기존 Skill 라우팅

| 작업 | 실행 책임 Skill | 이 허브에서 읽을 내용 |
|---|---|---|
| 요청 해석·범위·완료 기준·실행 순서 | `managing-project-intake-and-work-contract` | Method의 결정 질문·Coverage·Evidence Pack 계약 |
| 코어 컨셉·DDD·벤치마킹·플레이테스트 | `analyzing-and-refining-game-concepts` | 게임 기획 Guide·Reference Catalog |
| Windows+Android 적합성·공용 코어·입력/UI/lifecycle·출시 wave | `analyzing-and-refining-game-concepts` + 기존 기술·Vertical Slice·검증 Skill | PC·Android Delivery Guide·`templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` |
| Games User Research 누락 감사 | `governing-game-user-research-coverage` | 연구 관련 Coverage와 Evidence 상태 |
| 아트 방향·프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | 아트 Guide·원출처·권리·승인 상태 |
| 자산·플러그인 직접 채택과 참조 독립 제작 선택 | `evaluating-godot-assets-and-plugins-before-creation` | 플랫폼·자산 권리 Guide의 제작·도입 경로 |
| 대표 경험·품질·제작 파이프라인 | `designing-vertical-slices` | 기획·아트·기술 Guide의 Quality Bar |
| 변경·외부 AI 결과·접근성·성능 검증 | `reviewing-and-validating-project-changes` | Evidence 상태·AI 독립 검수·플랫폼 증거 |
| 실패 가정·반례·과잉 일반화 공격 | `running-adversarial-review-and-refinement` | Evidence Pack·Case Card의 한계·비복제 요소 |
| Skill 중복·과분할·학습 | `evolving-project-discipline-skills` | 반복 실패·Case·새 책임 경계 증거 |
| 프로젝트 교훈의 Base 승격 | `managing-base-change-proposals` | 공용 원리와 프로젝트 고유값 분리 |

합성 테스터 작업은 별도 Skill을 만들지 않는다. 프로젝트 Registry가 선택한 게임 디자인·유저리서치·UX·QA Skill과 Base GUR·적대적 검토·통합검증을 조합한다.

## 5. Template

- 통합 조사 기록: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- 성공·실패·혼합 사례: `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`
- PC·Android 공용 코어·플랫폼 적응·출시 wave: `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
- 자산별 권리·출처·참조 독립 제작: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- 플랫폼 출시 등급·설문·권리 Coverage: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- 사람 검증 세션 패킷: `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`
- 합성 테스터 시뮬레이션: `templates/research/SYNTHETIC_TESTER_SIMULATION_PACKET.md`
- 게임 벤치마크·플레이어 근거: `templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md`

프로젝트는 Base 문서를 복제하지 않는다. 프로젝트 저장소에는 결정 질문, 선택한 Coverage, Evidence ID, 개선 판정, 실제 기획 반영, 검증 결과와 프로젝트 고유 Case만 둔다.

## 6. 사용하지 않는 경우

다음 작업에는 이 허브 전체를 불러오지 않는다.

- 오탈자·링크·서식 같은 L0 기계 수정
- 이미 승인된 단일 파일 변경의 동일 검사 재실행
- 외부 근거가 현재 결정을 바꾸지 않는 단순 조회
- 실제 대상 프로젝트의 정본·코드·데이터·자산을 읽지 않은 구현 주장
- 목적 없이 비슷한 게임·이미지·도구를 많이 모으는 조사

## 7. 완료 판정

이 허브를 읽거나 문서를 작성한 것만으로 기획·구현·접근성·성능·출시가 검증된 것은 아니다. 합성 테스터 결과도 실제 사람 행동·재미·선호·조작감·접근성·성능을 검증하지 않는다. 등급·권리 Template도 법률 검토·플랫폼 제출·승인을 대신하지 않는다. PC·Android Profile도 실제 Windows build, Android 실기기, 모바일 UI·입력·중단 복구, 성능·발열, 상점 계정·테스트·심사 증거를 대신하지 않는다. 완료는 선택한 기존 Skill의 Output Contract와 실제 프로젝트 증거를 따른다.

계약·라우팅·중복 Skill 방지·Learning Log 연결은 `tests/test_evidence_based_game_development_knowledge.py`, `tests/test_evidence_knowledge_workflow_contract.py`, `tests/test_pc_android_cross_platform_delivery.py`, `tests/test_platform_review_asset_rights_reference_production.py`, `tests/test_human_validation_artifact_governance.py`, `tests/test_synthetic_tester_simulation_governance.py`, `.github/workflows/validate-evidence-knowledge.yml`의 전용 GitHub Actions에서 검증한다. Workflow 파일 존재와 실제 실행 성공을 분리해 확인한다.

## 8. Cloud Run 게임 백엔드 Capability Pack

- 서버 필요가 발견되면 `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`에서 `SERVER_FEATURE_DETECTED` → `CLOUD_RUN_DEFAULT_CANDIDATE` → `FIT_AND_RISK_ASSESSMENT`를 수행한다.
- 실제 프로젝트 계약은 `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`가 소유하며 문서 존재만으로 배포·부하·비용·보안 준비를 주장하지 않는다.
- 고주파 authoritative realtime, UDP, indefinite worker, instance-local durable authority는 기본 후보에서 제외한다.
