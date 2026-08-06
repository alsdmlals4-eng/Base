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
