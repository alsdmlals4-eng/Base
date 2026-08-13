# 주기적 전문 Source Radar — 프롬프트·기획·작법·실행 Source 설계

```yaml
status: IMPLEMENTED_PENDING_MERGE
approved_at: 2026-08-13
baseline_main_sha: f08a78b33aa1d458376da8f783553fe9ce7aa9cd
change_class: ABSORB_EXISTING_OWNER
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
specialty_radar: docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md
new_active_skill: false
new_authority_owner: false
scheduler_authority: EXTERNAL_TO_BASE
independent_ledger: false
```

## 1. 문제

Base에는 durable Source Pool·Evidence 판정·scan 상태·Ledger가 이미 있다. 하지만 프롬프트 평가, 게임 기획 연구, 글쓰기 작법, 문서·결정 방법, 외부 Skill·addon·script, Godot 재사용 자산을 한 번에 찾고 기존 owner로 보내는 전문 discovery surface가 부족했다.

모든 항목을 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`나 `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`에 직접 누적하면 두 대형 문서가 비대해지고 Source 정책·후보 목록·분야별 적용 절차가 섞인다. 반대로 분야별 새 Skill을 만들면 기존 prompt·game-design·fiction·asset owner와 충돌한다.

## 2. 채택 구조

```text
PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
= Source role·Evidence·scan·승격 정책 owner

EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
= claim별 Evidence tier·상태·적용 판정 owner

PERIODIC_SPECIALTY_SOURCE_RADAR.md
= 전문 Source 후보·consumer route·실행 위험·validation·rollback

기존 Skill·Method·Guide
= 실제 작업 실행과 프로젝트 적용 owner
```

Radar는 두 번째 Watchlist가 아니다. 별도 Source 승격 권한, scheduler, Ledger, 자동 설치기, 실행 권한을 갖지 않는다. 반복 material value와 기존 새 사이트 Gate를 통과한 후보만 Watchlist·Ledger family로 승격한다.

## 3. 포함 분야

### `PROMPT_AND_AGENT_WORKFLOW`

- 공식 제품·표준: OpenAI, Anthropic, GitHub Copilot, Google Gemini/ADK, Microsoft Learn, Agent Skills Specification.
- 평가·보안·발견: DSPy, promptfoo, OWASP GenAI, DAIR.AI, Learn Prompting, ACL/arXiv.
- 검증: exact model/product/surface/version, prompt/instruction/skill/tool/agent 배치, representative Golden Set, actual harness eval, quality·cost·latency·context·blast radius, rollback.

제품별 prompt tip, magic phrase, 단일 좋은 출력, vendor benchmark, LLM judge, optimizer score, prompt 길이, Skill·agent 수는 품질 증거가 아니다.

### `PLANNING_AND_DESIGN_METHODS`

- 게임 기획·연구: GDC, Game Developer, Games User Research, DiGRA, Game Studies, MDA, Game Design Patterns, Game Design Workshop, Machinations.
- 작업구조·문서·결정: Diátaxis, ADR, C4, DORA.
- 검증: player/user problem, decision delta, production cost, current project consumer, playable/provable artifact, playtest·interview·telemetry, rollback/discard condition.

framework·pattern·논문·simulation은 질문과 가설을 개선하지만 실제 player evidence를 대체하지 않는다. 문서량·Issue·PR·diagram·ADR·metric 수는 플레이어 가치나 진척 증거가 아니다.

### `WRITING_AND_REVISION_CRAFT`

- 한국어 규범·산업: 국립국어원, KOCCA/Storyum.
- 편집·작법: Purdue OWL, Reedsy, Writing Excuses, Brandon Sanderson BYU, Scriptnotes/John August, Jane Friedman/Writer's Digest, Writer Beware.
- 게임 서사: 기존 IGDA Game Writing, GDC narrative, Emily Short, ink, Yarn Spinner.
- 단계: `CANON_AND_CONTINUITY → DEVELOPMENTAL_STRUCTURE → SCENE_AND_CHARACTER → DIALOGUE_AND_INFORMATION → LINE_AND_PROSE → COPY_AND_PROOF → READER_OR_PLAYER_EVIDENCE`.

언어 규범 authority와 창작 품질을 분리한다. 인기·수상·판매 성과는 특정 작가의 식별 가능한 voice/style·장면·대사를 복제할 권한이 아니다. 선형 소설과 interactive narrative의 agency·state·branch budget 경계를 보존한다.

### `EXECUTABLE_SOURCE_AND_SUPPLY_CHAIN`

- Agent Skills Specification, `anthropics/skills`, `obra/superpowers`, skills.sh.
- OpenSSF Scorecard, OSV/OSV-Scanner, deps.dev, SLSA.
- 실행 위험 축:

```yaml
executable_surface: NONE | COPYABLE_SNIPPET | SCRIPT | GODOT_ADDON | GDEXTENSION | AGENT_SKILL | HOOK | MCP_SERVER | BINARY | INSTALL_COMMAND
trust_state: DISCOVERED | QUARANTINED | SOURCE_REVIEWED | SANDBOX_TESTED | APPROVED_PINNED | REJECTED
```

upstream, exact pin, checksum, license, install command, scripts/hooks, network·secret·filesystem·permission, sandbox, representative behavior, uninstall/rollback을 확인한다. marketplace listing, stars, installs, Scorecard, scanner, schema validation은 vetted dependency나 전체 security/compliance PASS가 아니다.

### `GODOT_ASSET_AND_PRODUCTION_SOURCES`

- Godot Asset Store, legacy Asset Library, `godotengine/awesome-godot`, GDQuest.
- Kenney, Poly Haven, Freesound, OpenGameArt, Godot Shaders.
- 항목별 원 page·repository·version·license·attribution·redistribution·Godot compatibility·import·native code·실제 build size/performance/readability·rights manifest·pin·rollback을 확인한다.

Store·curated list·CC0 표시·인기·별점만으로 dependency 품질, 전체 권리, 용량·가독성·시장성을 증명하지 않는다.

## 4. 기존 consumer

- Prompt/Agent: `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`, `AI_WORKFLOW_AND_PROMPT_SOURCE_NOTES.md`, `AI_SKILL_ADOPTION_GUIDE.md`, intake·Skill evolution·validation owner.
- Game planning: `analyzing-and-refining-game-concepts`, `GAME_FEATURE_DESIGN_SPEC.md`, vertical slice·document·adversarial review owner.
- Writing: `developing-and-revising-serial-fiction`, `NARRATIVE_AND_RELATIONSHIP_METHOD.md`, serial-fiction Guides.
- Assets: art direction, `evaluating-godot-assets-and-plugins-before-creation`, build-size, rights/provenance, target project Godot owner and tests.

프로젝트 고유 세계관·수치·UI·story direction·실제 dependency pin은 프로젝트 정본이 소유한다.

## 5. Hub·테스트·완료

`docs/knowledge/game-development/README.md`는 Radar를 한 단계로 연결하고, 새 광역 Skill이 아니라 기존 Skill 조합으로 실행한다고 명시한다.

기존 Evidence Knowledge 테스트 두 개를 확장한다.

- `tests/test_periodic_external_source_watchlist.py`: Watchlist·Evidence owner 경계, 분야별 검증·실행 위험·과장 방지.
- `tests/test_periodic_external_source_discovery_seeds.py`: Source coverage와 기존 owner routing.

완료는 다음을 모두 요구한다.

- 기존 Watchlist·Ledger·ACTIVE Skill·Work Mode 권위 불변.
- 신규 Radar·Hub route·두 계약 테스트 존재.
- focused contract, 관련 전체 unittest, workflow exact-head 성공.
- 같은 Goal의 열린 PR path/owner 충돌 0.
- 적대적 검토 blocker 0, unresolved review thread 0.
- merge 후 새 `main`에서 Radar·Hub·tests readback.

## 6. 적대적 검토

- Radar가 두 번째 Watchlist·Source canon·실행 owner가 되었는가?
- 분야별 목록이 decision relevance 없는 링크 dump가 되었는가?
- vendor/model/creator 조언을 전역 Hard Rule로 만들었는가?
- framework·simulation·benchmark를 player evidence로 위장했는가?
- 언어 authority와 문학적 완성도를 혼동했는가?
- 식별 가능한 creator style·게임 구조·asset을 복제하려는가?
- listing·score·scanner·format 준수를 vetting으로 오인했는가?
- 실행 후보가 quarantine·pin·rollback을 우회했는가?
- 프로젝트 고유 canon과 실제 dependency 상태를 Base로 승격했는가?
- Source 수·Skill 수·문서량 증가 자체를 개선으로 오인했는가?

## 7. 롤백

이 PR의 squash merge commit을 revert한다. Radar, Hub route, 두 테스트와 spec·plan이 함께 되돌아가며 runtime, save/data Schema, Skill Registry, project canon migration은 없다.
