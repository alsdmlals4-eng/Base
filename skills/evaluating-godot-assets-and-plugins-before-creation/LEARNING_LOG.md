# Evaluating Godot Assets and Plugins Learning Log

## 2026-08-05 — Direct adoption versus reference-to-original

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 외부 에셋·플러그인·이미지·사운드의 구조와 기술을 조사하되 원본을 그대로 또는 약간 변형해 사용하지 않고 새 자산을 만들라는 승인된 Base 변경.
- **Finding:** 기존 `ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM` 판정은 후보 도입에는 충분했지만, 직접 제품 포함과 `REFERENCE_TO_ORIGINAL` 분석 입력을 명시적으로 분리하지 않아 상업 사용·게임 포함 배포·원본 재배포와 유사성 증거가 섞일 수 있었다.
- **Decision:** 새 광역 Skill을 추가하지 않음. 기존 Skill에서 직접 포함은 `LICENSED_THIRD_PARTY`·`OPEN_SOURCE`, 참조 전용은 `REFERENCE_TO_ORIGINAL`, 직접 제작은 `OWNED_ORIGINAL`·`COMMISSIONED_ORIGINAL`·`AI_GENERATED`·`MIXED_ROUTE`로 연결한다.
- **Evidence contract:** `commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`을 분리한다. 참조 전용 입력은 shipping package에서 제외하고 `reference_brief`, `forbidden_expression`, `final_asset_record`, `reference_similarity_status`를 요구한다.
- **Boundary:** 자동 법률 판정기를 추가하지 않음. 정적 검사는 누락·불일치만 차단하며 실제 권리 해석·침해 여부·플랫폼 승인·법률 clearance를 확정하지 않는다.
- **Verification state:** focused RED는 확인됨. exact-head GREEN, 공유 Route·reference freshness·전체 회귀는 후속 증거로 분리한다.
- **Next trigger:** 여러 프로젝트에서 같은 자산 유형과 라이선스 조건이 반복되고 기계 판정 가능한 안정 입력이 확보될 때 자동 validator를 별도 제안으로 검토한다.

## 2026-08-06 — Existing solution must precede custom MCP or addon design

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** Base custom Godot MCP와 Bridge를 설계·구현한 뒤 사용자가 이미 HiGodot을 사용 중이라는 사실과 더 완성된 외부 구현을 뒤늦게 대조함.
- **Finding:** 기존 Skill은 외부 Godot 에셋·플러그인 검색을 권장했지만, 사용자의 현재 connected MCP·enabled addon·dependency·관련 open/recent PR 인벤토리를 설계 전 필수 Gate로 강제하지 않았다. 안전 요구를 곧바로 신규 구현 요구로 해석하면 기능 중복과 유지비를 키울 수 있다.
- **Decision:** 새 Skill을 만들지 않고 이 Skill에 `inventory-current-environment`와 `disposition`을 추가한다. 신규 MCP·addon·CLI·framework·Skill·Mode는 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` 판정 전 설계·구현하지 않는다. Godot 실행 권위는 HiGodot 하나로 유지하고 Base custom MCP·Bridge는 정책 추출 뒤 참고 기록으로 보존한다.
- **Evidence contract:** 사용 도구, connected MCP, enabled addon, package/lock, Base·프로젝트 구현, open and recently merged PR, 유지되는 외부 대안, 기능·보안·라이선스·호환성·유지비·전환비, 사용자 승인 상태를 기록한다.
- **Operational boundary:** HiGodot의 Node 삭제·file write·project settings·autoload 기능은 허용하며 L2/L3 rollback·diff·import·test Gate로 통제한다. DeepSeek는 host profile에서 MCP 등록과 credential을 모두 제거하고 network는 loopback only로 제한한다.
- **Verification state:** test-only RED와 reference-freshness 실패를 확인함. exact-head GREEN, 실제 HiGodot 설치·Windows·Codex/GPT E2E·project runtime은 아직 `NOT_RUN`이다.
- **Next trigger:** HiGodot exact release 변경, tool schema·transport·security 변경, 새 공급자 제안 또는 custom build 요구가 발생하면 current-environment inventory와 disposition을 다시 수행한다.

## 2026-08-06 — Selective addon utilization requires a consumption path

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 여러 Godot 프로젝트에 유용한 addon 후보를 정리하는 과정에서 “검증된 addon은 활용하라”는 원칙과 “모든 프로젝트에 미리 설치하지 말라”는 원칙을 함께 고정할 필요가 생김.
- **Finding:** 기존 평가 절차는 채택·직접 제작 판정은 했지만, 설치 뒤 실제 editor·runtime·test·platform·content pipeline에서 사용하는지와 불필요해진 addon을 제거하는 상태를 충분히 강제하지 않았다. 이 공백은 blanket installation과 폴더만 존재하는 미사용 의존성을 만들 수 있다.
- **Decision:** 새 Skill이나 중앙 addon registry를 만들지 않는다. 기존 Skill에 Selective addon utilization 수명주기와 `consumption_path`를 추가하고, 소비 경로가 없는 설치는 `INSTALLED_UNUSED`로 판정해 제거하거나 `DEFERRED`로 되돌린다.
- **Evidence contract:** 프로젝트가 exact version, source, license, Godot·platform 호환성, adoption state, consumption path, owner boundary, validation, rollback 또는 removal을 소유한다. Base에는 프로젝트별 고정 설치표를 두지 않는다.
- **Boundary:** HiGodot 단일 권위는 저작·편집 mutation authority에 한정된다. 테스트·대화·플랫폼·카메라·아이콘처럼 역할이 다른 addon도 자동 허용하지 않고 같은 평가와 소비 경로 Gate를 통과한다.
- **Verification state:** blanket installation 금지, `INSTALLED_UNUSED`, consumption path, stage routing을 요구하는 focused RED를 확인했다. 실제 프로젝트 addon 설치·runtime·device·platform service·human 검증은 `NOT_RUN`이다.
- **Next trigger:** 프로젝트에서 새 addon 도입·비활성화·교체·업데이트·제거 또는 사용 경로 소멸이 발생하면 adoption state와 consumption path를 재평가한다.

## 2026-08-07 — Separate persistent authoring, deterministic tests, and live QA

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** Godot 작업에서 이미 채택된 HiGodot에 GUT과 Hera Agent Godot CLI를 함께 활용하되 권위 중복 없이 실제 구현·테스트·실행 QA를 한 흐름으로 만들라는 승인된 요청.
- **Finding:** HiGodot의 넓은 editor authoring surface, GUT의 반복 가능한 GDScript test suite, Hera의 low-context CLI live QA를 같은 “Godot 자동화 도구”로만 보면 두 번째 mutation authority와 두 테스트 정본이 쉽게 생긴다. 반대로 Hera를 도구 전체로 금지하면 runtime input·assert·diagnostics·screenshot 검증 가치를 잃는다.
- **Decision:** 새 광역 Skill이나 중앙 addon registry를 추가하지 않는다. `HiGodot = SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY`, `GUT = DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED`, `Hera = REUSE + LIVE_QA_AND_OBSERVABILITY_ONLY`로 역할을 분리한다.
- **Evidence contract:** GUT은 exact Godot-compatible version과 실제 test/CI consumption을 요구하고 같은 GDScript case를 HiGodot `McpTestSuite`와 두 canonical suite로 유지하지 않는다. Hera는 exact CLI/addon pair, localhost, shared token, 실제 live-QA consumption, acceptance 전후 tracked source delta `NONE`을 요구한다.
- **Boundary:** GUT은 C#/.NET·native·platform test authority를 강제 대체하지 않는다. Hera persistent editor/source mutation은 금지하며 `game set` 또는 state-changing runtime `call`은 `DIAGNOSTIC_ONLY`, acceptance evidence false, restore/restart required다. 모든 프로젝트 일괄 설치는 금지하고 소비 경로가 없으면 `INSTALLED_UNUSED` 또는 `DEFERRED`다.
- **Verification state:** GitHub Actions RED에서 Base 생성물·무결성 단계는 PASS했고 새 focused contract 단계가 의도대로 실패했다. Base static GREEN과 project runtime E2E는 후속 단계이며 실제 프로젝트 addon 설치·Hera runtime QA·human validation은 아직 `NOT_RUN`이다.
- **Next trigger:** Godot/GUT/Hera version change, project adoption, Hera command surface change, McpTestSuite migration, or real project live-QA evidence가 생기면 exact pin·authority boundary·source-delta guard를 재검증한다.

## 2026-08-31 — External agent tool absorption is not runtime enforcement

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 사용자 승인 “좋아 확인 후 교정,병합,흡수 진행해”에 따라 PR #788의 외부 도구 10종 평가·연결·검증 상태를 fresh-read함.
- **Finding:** 최초 `91fbcc0a89f3c1b3ce1eb5a68a9a619074fabdf6`는 Draft·미병합인데 완료 보고가 흡수 상태를 과장했다. 검토 관점 5개를 실행 루프처럼 표시했고, 출력 필터 실패 뒤 원문 복구가 명령 재실행으로 해석될 여지와 실제 프로젝트에 없는 Godot 검증 명령 예시가 있었다.
- **Decision:** 새 Skill·hook·reviewer·CLI·memory engine·running-mate를 만들거나 설치하지 않는다. 기존 owner의 reference 연결과 계약 검사만 강화하고, 기존 학습·재사용·handoff·검증 책임을 그대로 재사용한다. 상세 흡수 기록은 `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_TOOL_ADOPTION_REVIEW_2026-08-31.md`가 소유한다.
- **Evidence contract:** `CONTRACT_TESTS_ARE_NOT_BEHAVIOR_EVALUATIONS`, `EXISTING_OWNER_REUSE_NOT_NEW_HOOK_IMPLEMENTATION`, `RAW_CAPTURE_BEFORE_TRANSFORM`, `PRESERVE_UPSTREAM_EXIT_STATUS`, `NO_AUTOMATIC_COMMAND_REPLAY`를 구분한다. 원문 복구는 기존 호출의 기록과 부작용 readback이 먼저이며 성공했을 수 있는 변경 명령을 자동 반복하지 않는다.
- **Historical RED receipt:** `32232d523c52bc02f963bc64652f711988f5e6cb`, Actions run `33345247103`, 2,360 tests 중 의도한 7 failures·37 skips. 진단 ZIP SHA-256 `7fa047b9e68b395e2f30e0f574bf37bd26c8b9e6a906416a50fd6f110d7b6d43`를 다운로드한 실제 bytes와 대조했다. 이는 당시 RED 증거이며 최신 GREEN·병합 여부를 대신하지 않는다.
- **Boundary:** 소스 제작자 벤치마크는 우리 프로젝트의 A/B 실험이 아니다. 동일 작성자의 자기검토와 CI는 독립 검토가 아니다. 사용자 결정은 정본에 즉시 기록하고, 프로젝트 교훈의 공용 일반화에 필요한 반복 증거와 혼동하지 않는다. 프로젝트 채택 pin·승인 자산·비용·권한은 이 변경으로 바꾸지 않는다.
- **Current-state owner:** 최종 exact HEAD, 전체 CI, 별도 독립 검토, 허용된 merge와 postmerge main readback은 PR #788의 최신 기록에서 확인한다. 문서 존재·브랜치 GREEN만으로 merged-main absorption이나 실제 도구 동작 PASS를 선언하지 않는다.
- **Next trigger:** 실제 프로젝트가 하나의 선택형 도구를 필요로 할 때 현재 환경·exact version·데이터/비용/권한·동등한 격리 baseline·원문 복구·rollback을 확인한 뒤 별도 trial gate를 적용한다. 기존 작업 중 HEAD가 바뀌면 새 diff를 읽고 다른 변경을 보존하며 stale 문서로 덮어쓰지 않는다.
