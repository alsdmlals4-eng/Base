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
| 어떤 외부 사이트를 주기적으로 확인하고 발견 글을 어떻게 원출처로 역추적하는가? | `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` | Source Pool·scan checkpoint·원출처 역추적·freshness·적용 판정 |
| 프롬프트·기획·글쓰기 작법·작업구조·외부 Skill·Godot 자산 후보를 분야별로 어디서 찾고 어떻게 검증하는가? | `PERIODIC_SPECIALTY_SOURCE_RADAR.md` | 전문 Source 후보·기존 owner route·실행 위험·validation·rollback |
| 세계관·캐릭터·장르·현실 고증·표현·현지화·추리 단서·중국 무협·서브컬처 밈을 어디서 조사하고 어떻게 검증하는가? | `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md` | 후보 수 무제한 Source capture·매체/시대/지역 경계·기존 owner route·프로젝트 검증·폐기 조건 |
| 게임 코어·플레이어 경험·게임 필·보상·난이도를 어떻게 설계하는가? | `GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md` | 플레이어 약속·MDE 추적표·플레이테스트 계약 |
| 튜토리얼·온보딩·첫 세션에서 규칙·필요·성장·독립 수행을 어떻게 가르치는가? | `TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md` | `RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER` 학습 계약·측정·적대적 검토 |
| 프로젝트마다 어떤 이미지·시각 자산·UI 컴포넌트를 정말 만들어야 하는가? | `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate` | `requirement_id`·Delete Test·role·P0~P3·disposition·검증 |
| 그림체·비주얼·캐릭터·환경·UI·애니메이션·에셋을 어떻게 기획하는가? | `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` | Visual Pillar·Art Bible·Asset Specification |
| 픽셀 아트를 어떤 축으로 조합하고 프로젝트별 후보를 어떻게 비교하는가? | `PIXEL_ART_STYLE_SYSTEM.md` + `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md` | 5축 후보·20 Preset·시각 Reference·최소 3대안·장기계획 적합성·재검토 |
| 게임 다운로드·설치·런타임·패치 용량을 화질·음질·성능 저하 없이 어떻게 줄이는가? | `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` | 용량 breakdown·품질 등급·font/texture/audio profile·patch/delivery 증거 |
| ChatGPT·Codex·외부 AI를 어떻게 안전하고 검증 가능하게 협업시키는가? | `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md` | Prompt 계약·Context Pack·Evals·독립 검수 |
| Godot·플랫폼·성능·제작 파이프라인·출시를 어떻게 기획에 연결하는가? | `TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md` | 기술 계약·성능 예산·반복 제작성·출시 증거 |
| Windows+Android를 처음부터 함께 설계하고 STOVE·Google Play·Steam 출시 wave를 어떻게 나누는가? | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` | 적합성 판정·공용 코어/플랫폼 어댑터·기기 QA·출시 Profile |
| Steam·STOVE·Google Play 등급·설문·자산 권리·참조 독립 제작을 어떻게 관리하는가? | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` | 등급 전략·자산 권리 Record·출시 Compliance Pack |
| 어떤 공식·학술·현업 자료를 우선 참조하는가? | `REFERENCE_SOURCE_CATALOG.md` | 출처 메타데이터·사용 범위·재검증 조건 |
| 작은 표본·저충실도 사람 세션을 어떻게 과장 없이 설계하는가? | `docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md` | 사람 세션 패킷·claim ceiling·미검증 분리 |
| 실제 테스터가 없을 때 AI 가상 페르소나로 무엇을 검토할 수 있는가? | `docs/knowledge/game-development/SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md` | 프로젝트 구조 분석·T6 합성 위험 검토·TEST 게이트 |

`PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`는 새 실행 Skill이나 Evidence 권위가 아니다. 주기적으로 어디를 훑고 어떻게 후보를 원출처로 되돌릴지만 책임지며, 실제 Evidence tier·상태·적용 판정은 `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`가 계속 소유한다.

`PERIODIC_SPECIALTY_SOURCE_RADAR.md`는 Watchlist에 종속된 전문 discovery extension이다. 두 번째 Watchlist·실행 Skill·scheduler·Ledger가 아니며, 후보는 기존 owner와 프로젝트 검증·rollback 경로로 보낸다.

`NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`는 상위 전문 Radar에 종속된 서사·세계관·캐릭터 하위 Reference다. 후보 수에는 최소·최대 상한을 두지 않지만, 관련성·원출처·현재 consumer·반례·권리/표현 위험·검증·폐기 조건 없는 후보를 채택하지 않는다. 프로젝트 고유 설정과 실제 정본은 각 프로젝트가 소유한다.

`TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md`는 실행 권한을 소유하지 않는다. 실제 작업은 `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design`이 주 책임이며, 튜토리얼 이해도 연구 coverage 설치·누락 감사는 `governing-game-user-research-coverage`가 담당한다.

`PIXEL_ART_STYLE_SYSTEM.md`와 `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`는 새 Art Skill이나 두 번째 Art Bible이 아니다. Base는 조합 가능한 픽셀 시각 어휘·비용·실패조건·Reference를 제공하고, 실제 선택과 승인·Figma Visual Bible·제품 자산 권위는 각 프로젝트가 소유한다.

## 4. 기존 Skill 라우팅

| 작업 | 실행 책임 Skill | 이 허브에서 읽을 내용 |
|---|---|---|
| 요청 해석·범위·완료 기준·실행 순서 | `managing-project-intake-and-work-contract` | Method의 결정 질문·Coverage·Evidence Pack 계약 |
| 코어 컨셉·DDD·벤치마킹·플레이테스트 | `analyzing-and-refining-game-concepts` | 게임 기획 Guide·Reference Catalog |
| 프롬프트·기획·작법·작업구조·외부 Skill·Godot 자산 Source 조사 | 기존 intake·game design·fiction·Skill evolution·asset evaluation·validation Skill 조합 | `PERIODIC_SPECIALTY_SOURCE_RADAR.md`; 새 광역 Skill을 만들지 않음 |
| 세계관·캐릭터·장르·현실 고증·표현·현지화·추리·중국 무협·밈 Source 조사 | 기존 fiction·game design·narrative·character-art·documentation·validation Skill 조합 | `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`; 프로젝트 정본·원고·데이터·플레이테스트가 최종 consumer |
| 튜토리얼·온보딩·첫 세션 학습·성장 체감 | `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design` | 튜토리얼 Guide·프로젝트 Contract·공식 접근성 근거 |
| Windows+Android 적합성·공용 코어·입력/UI/lifecycle·출시 wave | `analyzing-and-refining-game-concepts` + 기존 기술·Vertical Slice·검증 Skill | PC·Android Delivery Guide·`templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` |
| 게임 build/package/download/patch·font/texture/audio 자산 최적화 | 기존 기획·아트·Vertical Slice·검증 Skill 조합 | `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` + 프로젝트 Delivery Profile |
| Games User Research 누락 감사 | `governing-game-user-research-coverage` | 연구 관련 Coverage와 Evidence 상태 |
| 이미지·시각 자산·UI 컴포넌트 필요성·우선순위·제작 방식 선정 | 기존 Art/UX/asset evaluation Skill 조합 | Art Guide의 `Visual Requirement Gate`; 새 광역 Skill을 만들지 않음 |
| 픽셀 아트 후보 탐색·비교·프로젝트 스타일 결정 준비 | `designing-art-prompts-and-technique-cards` + 프로젝트 Art/UX 책임 | `PIXEL_ART_STYLE_SYSTEM.md`의 5축·최소 3대안·장기 적합성 + `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`의 REFERENCE_ONLY 예시 |
| 아트 방향·프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | 아트 Guide·원출처·권리·승인 상태 |
| 자산·플러그인 직접 채택과 참조 독립 제작 선택 | `evaluating-godot-assets-and-plugins-before-creation` | 플랫폼·자산 권리 Guide의 제작·도입 경로 |
| 대표 경험·품질·제작 파이프라인 | `designing-vertical-slices` | 기획·아트·기술 Guide의 Quality Bar |
| 변경·외부 AI 결과·접근성·성능 검증 | `reviewing-and-validating-project-changes` | Evidence 상태·AI 독립 검수·플랫폼 증거 |
| 실패 가정·반례·과잉 일반화 공격 | `running-adversarial-review-and-refinement` | Evidence Pack·Case Card의 한계·비복제 요소 |
| Skill 중복·과분할·학습 | `evolving-project-discipline-skills` | 반복 실패·Case·새 책임 경계 증거 |
| 프로젝트 교훈의 Base 승격 | `managing-base-change-proposals` | 공용 원리와 프로젝트 고유값 분리 |

합성 테스터 작업, 게임 용량 최적화 작업, Visual Requirement Gate, 픽셀 아트 Reference, 주기 외부 Source 발견은 별도 광역 Skill을 만들지 않는다. 프로젝트 Registry가 선택한 기존 게임 디자인·아트·UX·자산 평가·Vertical Slice·검증 책임을 조합한다.

## 5. Template

- 통합 조사 기록: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- 성공·실패·혼합 사례: `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`
- 시각 요구 선정·아트 방향: `templates/planning/ART_DIRECTION_BRIEF.md`
- UX/UI requirement 소비·상태 계약: `templates/planning/GAME_UX_UI_SYSTEM.md`
- PC·Android 공용 코어·플랫폼 적응·출시 wave·build size evidence: `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
- 자산별 권리·출처·참조 독립 제작: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- 플랫폼 출시 등급·설문·권리 Coverage: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- 사람 검증 세션 패킷: `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`
- 합성 테스터 시뮬레이션: `templates/research/SYNTHETIC_TESTER_SIMULATION_PACKET.md`
- 게임 벤치마크·플레이어 근거: `templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md`
- 튜토리얼·온보딩 설계: `templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`

프로젝트는 Base 문서를 복제하지 않는다. 프로젝트 저장소에는 결정 질문, 선택한 Coverage, Evidence ID, 개선 판정, 실제 기획 반영, 검증 결과와 프로젝트 고유 Case만 둔다. 픽셀 아트 후보를 선택할 때도 Base의 20 Preset을 프로젝트 정본 목록으로 복제하지 않고 실제 후보와 선택 결과만 기록한다.

## 6. 사용하지 않는 경우

다음 작업에는 이 허브 전체를 불러오지 않는다.

- 오탈자·링크·서식 같은 L0 기계 수정
- 이미 승인된 단일 파일 변경의 동일 검사 재실행
- 외부 근거가 현재 결정을 바꾸지 않는 단순 조회
- 실제 대상 프로젝트의 정본·코드·데이터·자산을 읽지 않은 구현 주장
- 목적 없이 비슷한 게임·이미지·도구를 많이 모으는 조사

## 7. 완료 판정

이 허브를 읽거나 문서를 작성한 것만으로 기획·구현·접근성·성능·출시가 검증된 것은 아니다. 합성 테스터 결과도 실제 사람 행동·재미·선호·조작감·접근성·성능을 검증하지 않는다. 등급·권리 Template도 법률 검토·플랫폼 제출·승인을 대신하지 않는다. PC·Android Profile도 실제 Windows build, Android 실기기, 모바일 UI·입력·중단 복구, 성능·발열, 상점 계정·테스트·심사 증거를 대신하지 않는다. 빌드 용량 Guide도 실제 프로젝트 build, store-served size, Steam patch preview, Android device, 사람의 시각·청각 품질 검증을 대신하지 않는다. Pixel Art System과 Gallery도 프로젝트 스타일 승인·실제 이미지 품질·엔진 렌더·제품 자산 권리를 대신하지 않는다. 완료는 선택한 기존 Skill의 Output Contract와 실제 프로젝트 증거를 따른다.

계약·라우팅·중복 Skill 방지·Learning Log 연결은 `tests/test_evidence_based_game_development_knowledge.py`, `tests/test_evidence_knowledge_workflow_contract.py`, `tests/test_visual_requirement_gate.py`, `tests/test_pixel_art_style_system.py`, `tests/test_pc_android_cross_platform_delivery.py`, `tests/test_game_build_size_asset_optimization.py`, `tests/test_platform_review_asset_rights_reference_production.py`, `tests/test_human_validation_artifact_governance.py`, `tests/test_synthetic_tester_simulation_governance.py`, `tests/test_periodic_external_source_watchlist.py`, `tests/test_periodic_external_source_discovery_seeds.py`, `.github/workflows/validate-evidence-knowledge.yml`의 전용 GitHub Actions에서 검증한다. Workflow 파일 존재와 실제 실행 성공을 분리해 확인한다.

## 8. Cloud Run 게임 백엔드 Capability Pack

- 서버 필요가 발견되면 `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`에서 `SERVER_FEATURE_DETECTED` → `CLOUD_RUN_DEFAULT_CANDIDATE` → `FIT_AND_RISK_ASSESSMENT`를 수행한다.
- 실제 프로젝트 계약은 `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`가 소유하며 문서 존재만으로 배포·부하·비용·보안 준비를 주장하지 않는다.
- 서비스-backed Demo/Test가 필요하면 같은 Guide와 Contract에서 `ONE_CONSUMER_INTERFACE` → `REAL_ADAPTER | FAKE_ADAPTER`를 사용하고 `CONTRACT_PARITY_REQUIRED`, `FAIL_CLOSED_UNKNOWN_OPERATION`, deterministic/resettable synthetic fixture를 유지한다.
- 공개·공유 Demo는 `PUBLIC_DEMO_SANITIZATION`과 `SYNTHETIC_DATA_ONLY`를 적용하며 fake 실행 증거는 `SIMULATED_ONLY`라서 실제 provider `RUNTIME_VERIFIED`나 production readiness를 대신하지 않는다.
- 고주파 authoritative realtime, UDP, indefinite worker, instance-local durable authority는 기본 후보에서 제외한다.

## 9. 게임 권한·무결성·DRM Capability Pack

- 권한·앱/요청 무결성·DRM·오프라인 라이선스·고가치 서버 권위 질문은 `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`를 사용한다.
- 프로젝트별 신호·복구·개인정보·서비스 종료 증거는 `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`가 소유한다.
- `PLATFORM_NATIVE_FIRST`, `NO_CUSTOM_DRM_DEFAULT`, `PLAYER_HARM_REVIEW`를 유지하며 플랫폼별 미확인 기능은 `PLATFORM_CAPABILITY_UNVERIFIED`로 남긴다.
