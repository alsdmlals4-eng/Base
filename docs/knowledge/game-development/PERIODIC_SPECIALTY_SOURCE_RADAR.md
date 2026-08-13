# 주기적 전문 Source Radar — 프롬프트·기획·작법·Skill·Godot 자산

```yaml
radar_role: periodic-specialty-source-discovery-extension
status: ACTIVE_DISCOVERY_EXTENSION
owner_policy: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
scheduler_authority: EXTERNAL_TO_BASE
new_active_skill: false
independent_ledger: false
```

## 1. 목적과 권위 경계

이 Radar는 Base와 각 프로젝트에 필요한 **프롬프트·기획·글쓰기 작법·작업구조·외부 Skill·Godot 재사용 자산** Source를 주기적으로 발견하고 기존 owner로 보내기 위한 비실행 Reference다.

이 문서는 두 번째 Watchlist가 아니다. Source role, Evidence tier, `ORIGINAL_SOURCE_BACKTRACE`, 신규 Source 승격, scan 상태, Ledger 갱신, PR·exact-head 검증은 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`와 `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`가 계속 소유한다.

```text
현재 프로젝트의 문제·실패 증상·바뀔 결정
→ 원출처·게시일·버전·매체·표본·상업 이해관계
→ 기존 Base/project owner overlap
→ 가장 작은 decision delta
→ validation artifact·consumer·rollback
→ 적대적 공격·비판 검증
→ ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
```

외부 Source는 프로젝트 정본, 실제 코드·데이터·씬·원고, 실행한 테스트, 플레이어·독자 evidence를 대체하지 않는다. 새 사이트 수, Skill 수, 문서량, Issue 수, PR 수 자체는 개선 지표가 아니다.

공통 candidate packet:

```yaml
candidate_id:
source_domain:
source_name:
source_role: AUTHORITY_TARGET | PROFESSIONAL_PRACTICE | DISCOVERY_FEED | OBSERVATIONAL_DATA_OR_VENDOR_GUIDE
original_url:
published_or_updated_at:
checked_at:
exact_product_model_surface_or_version:
medium_platform_sample_or_method:
commercial_or_vendor_interest:
claim_or_practice:
context_conditions:
original_source_backtrace:
current_base_owner:
current_project_consumer:
base_overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
decision_delta:
failure_or_counterevidence:
validation_artifact:
rollback_or_discard_condition:
disposition: ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
```

## 2. `PROMPT_AND_AGENT_WORKFLOW`

### 2.1 공식·표준 Source

| Source | role | 주요 조사 표면 | 적용 한계 |
|---|---|---|---|
| **OpenAI Developers — prompting, evals, instruction hierarchy, Codex/Agents** | `AUTHORITY_TARGET` | OpenAI 제품의 prompt·instruction·tool·agent·eval·권한·장기 작업 변화 | OpenAI 제품 사실에만 authority. 다른 모델의 보편 법칙으로 확대 금지 |
| **Anthropic Docs / Engineering — prompt engineering, evals, context engineering** | `AUTHORITY_TARGET` | Claude prompt·context·tool·sandbox·agent harness | Claude 제품 사실에만 authority |
| **GitHub Copilot Docs** | `AUTHORITY_TARGET` | repository instructions, prompt files, custom agents, Agent Skills, hooks, MCP | 현재 surface·preview·호환성 재확인 |
| **Google Gemini / Google Cloud AI / ADK official guidance** | `AUTHORITY_TARGET` | prompt design, context engineering, agent lifecycle, evaluation | Gemini·Google 제품 사실과 일반 architecture 주장을 분리 |
| **Microsoft Learn** | `AUTHORITY_TARGET` | Agent Skills, Copilot surface, instruction structure, preview testing | 제품·preview 상태 재확인 |
| **Agent Skills Specification** | `AUTHORITY_TARGET` | `SKILL.md`, progressive disclosure, references/scripts/assets, compatibility | 형식 준수는 품질·안전·프로젝트 적합성 증거가 아님 |

### 2.2 연구·평가·발견 Source

| Source | role | URL / use | claim ceiling |
|---|---|---|---|
| **DSPy official docs + repository** | `AUTHORITY_TARGET` | `https://dspy.ai/` — modules, signatures, optimizers, evaluation workflow | optimizer score != project correctness |
| **promptfoo official docs + repository** | `AUTHORITY_TARGET` | `https://www.promptfoo.dev/docs/` — regression eval, red-team configuration, releases | red-team tool pass != security/compliance PASS |
| **OWASP GenAI Security Project** | `PROFESSIONAL_PRACTICE` | `https://genai.owasp.org/` — prompt injection, excessive agency, untrusted input, threat questions | guidance·checklist·scanner PASS는 전체 보안 증명이 아님 |
| **DAIR.AI Prompt Engineering Guide** | `DISCOVERY_FEED` | `https://www.promptingguide.ai/` 및 원 논문·공식 문서 링크 | prompt popularity != authority; 원문 역추적 필수 |
| **Learn Prompting** | `DISCOVERY_FEED` | `https://learnprompting.org/` — 교육·용어·공격·평가 자료 발견 | 강의 문구를 모델 불변 규칙으로 승격 금지 |
| **ACL Anthology / arXiv cs.CL·cs.AI** | `DISCOVERY_FEED` | 원 연구·후속 출판·dataset·method·ablation 발견 | preprint·benchmark를 실제 프로젝트 성과로 과장 금지 |

기존 consumer:

- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `docs/knowledge/research/AI_WORKFLOW_AND_PROMPT_SOURCE_NOTES.md`
- `docs/AI_SKILL_ADOPTION_GUIDE.md`
- `managing-project-intake-and-work-contract`
- `evolving-project-discipline-skills`
- `optimizing-ai-model-and-prompt-costs`
- `reviewing-and-validating-project-changes`

평가 흐름:

```text
baseline prompt / workflow + observed failure
→ source of truth·protected constraints·stop/handoff
→ prompt / instruction / skill / tool / agent 배치
→ REPRESENTATIVE_GOLDEN_SET + failure set + adversarial set
→ independent expected behavior / rubric
→ model·version·configuration·tool·permission·budget
→ 한 번에 하나의 controlled change
→ ACTUAL_HARNESS_EVAL
→ quality·cost·latency·context·blast radius
→ consumer review·version·rollback
```

magic phrase, 단일 좋은 출력, vendor benchmark, LLM judge, optimizer score, prompt 길이, Skill 수, agent 수는 품질 증거가 아니다. 웹·문서·파일 출력은 prompt injection과 misinformation을 포함할 수 있는 untrusted input으로 다룬다.

## 3. `PLANNING_AND_DESIGN_METHODS`

### 3.1 게임 기획·플레이어 경험 Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **GDC Vault / Game Developer / Games User Research** | `PROFESSIONAL_PRACTICE` | shipped-game postmortem, 제작 제약, 연구 질문·관찰·playtest timing | 프로젝트 규모·장르·표본을 보존 |
| **DiGRA Digital Library** | `DISCOVERY_FEED` | `https://dl.digra.org/` — game research papers, methods, references | publication venue != project fit |
| **Game Studies** | `DISCOVERY_FEED` | `https://gamestudies.org/` — interdisciplinary analysis | analysis != actual player evidence |
| **MDA 원문** | `PROFESSIONAL_PRACTICE` | mechanics–dynamics–aesthetics 질문과 비판 | framework != universal design law |
| **Game Design Patterns** | `PROFESSIONAL_PRACTICE` | interaction pattern, relation, consequence vocabulary | pattern catalog != design prescription |
| **Game Design Workshop** | `PROFESSIONAL_PRACTICE` | playcentric process, prototype, playtest exercise | textbook process != mandatory pipeline |
| **Machinations docs + original modeling research** | `AUTHORITY_TARGET` + `PROFESSIONAL_PRACTICE` | `https://machinations.io/docs` — resource/economy diagram and simulation hypothesis | simulation != playtest |

```text
player_or_user_problem + intended emotion / fantasy / job
→ meaningful choice·sacrifice·feedback·reward·failure learning
→ direct competitor + adjacent mechanic + failure/mixed evidence
→ decision_delta
→ production·content·UI·learning·QA cost
→ smallest playable PoC
→ current_project_consumer
→ validation_artifact: playtest observation / interview / telemetry / build
→ rollback_or_discard_condition
```

기존 consumer:

- `analyzing-and-refining-game-concepts`
- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md`
- `designing-vertical-slices`
- `managing-design-documents`
- `managing-game-project-operating-system`
- `running-adversarial-review-and-refinement`

논문·framework·pattern·simulation은 질문과 가설을 개선한다. 실제 재미·가독성·감정·기억·시장 가독성은 실제 player evidence로 검증한다.

### 3.2 작업구조·문서·결정 Source

| Source | role | use | 적용 한계 |
|---|---|---|---|
| **Diátaxis** | `PROFESSIONAL_PRACTICE` | tutorial·how-to·reference·explanation의 사용자 필요 구분 | 모든 파일을 네 폴더로 강제하지 않음 |
| **Architecture Decision Records** | `PROFESSIONAL_PRACTICE` | 되돌리기 비싼 결정의 context·대안·결과·supersession | 사소한 결정을 전부 기록하지 않음 |
| **C4 model** | `PROFESSIONAL_PRACTICE` | 가장 작은 유용한 architecture zoom | 1인 소규모 프로젝트에 모든 diagram 강제 금지 |
| **DORA** | `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE` | application/service delivery 경향과 개선 가설 | 개인 생산성 순위·게임 품질 지표가 아님 |

문서량·Issue 수·PR 수·diagram 수·ADR 수·metric 자체는 진척이나 플레이어 가치의 증거가 아니다. 기존 owner가 해결하면 새 Skill·Guide보다 기존 계약에 흡수한다.

## 4. `WRITING_AND_REVISION_CRAFT`

### 4.1 한국어 규범·편집·작법 Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **국립국어원** | `AUTHORITY_TARGET` | `https://www.korean.go.kr/` — 맞춤법·표준어·띄어쓰기·사전·공식 용례·말뭉치 출발점 | 한국어 규범·용례 authority이지 창작 미학의 authority가 아니다 |
| **Purdue OWL 등 대학 Writing Center** | `PROFESSIONAL_PRACTICE` | 문장·문단·revision·citation 질문 | 영어 교육 맥락을 한국어 창작에 그대로 강제 금지 |
| **한국콘텐츠진흥원 / Storyum** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | `https://www.storyum.kr/` — 플랫폼·지원사업 사실, 산업 보고서, 창작 기회 | 선정·노출 != 문학적·상업적 인과 |
| **Reedsy** | `PROFESSIONAL_PRACTICE` | developmental·copy·proof 단계, editor/writer practice | marketplace·교육 이해관계와 구조 공식을 분리 |
| **Writing Excuses** | `PROFESSIONAL_PRACTICE` | `https://writingexcuses.com/` — focused craft discussion, exercise, contrasting views | creator advice != universal craft law |
| **Brandon Sanderson BYU writing class** | `PROFESSIONAL_PRACTICE` | 장르소설 craft self-report와 강의 | 특정 작가의 방법·성공 원인을 보편화 금지 |
| **Scriptnotes / John August** | `PROFESSIONAL_PRACTICE` | screenplay scene·dialogue·industry practice | 소설·게임에 그대로 강제 금지 |
| **Jane Friedman / Writer's Digest** | `PROFESSIONAL_PRACTICE` + `DISCOVERY_FEED` | publishing practice, revision, career·industry discovery | 상업 이해관계·시기·매체 조건 기록 |
| **SFWA / Writer Beware** | `PROFESSIONAL_PRACTICE` | 출판 사기·계약·서비스 위험 신호 | 법률 자문 아님 |
| **IGDA Game Writing / GDC narrative / Emily Short / ink / Yarn Spinner** | `PROFESSIONAL_PRACTICE` | interactive narrative, choice·state·dialogue·localization·runtime | 선형 소설과 interactive narrative의 매체 경계를 보존 |

기존 consumer:

- `developing-and-revising-serial-fiction`
- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
- `docs/knowledge/serial-fiction/SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md`
- `docs/knowledge/serial-fiction/SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md`
- `docs/knowledge/serial-fiction/READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md`

수정 단계:

```text
CANON_AND_CONTINUITY
→ DEVELOPMENTAL_STRUCTURE
→ SCENE_AND_CHARACTER
→ DIALOGUE_AND_INFORMATION
→ LINE_AND_PROSE
→ COPY_AND_PROOF
→ READER_OR_PLAYER_EVIDENCE
```

어문 규범 준수 != 문학적 완성도다. 댓글·좋아요·조회·판매량은 특정 작법의 인과 증거가 아니다. author popularity != permission to copy voice or style. 특정 현존 창작자의 식별 가능한 문체·말투·비유·대사·장면을 모사하지 않는다.

선형 소설의 pacing·정보 공개 규칙을 interactive narrative의 agency·choice·state·branch budget에 그대로 강제하지 않고, 게임의 상태·분기 규칙을 모든 선형 장면에 강제하지 않는다.

## 5. `EXECUTABLE_SOURCE_AND_SUPPLY_CHAIN`

### 5.1 Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Agent Skills specification** | `AUTHORITY_TARGET` | 형식·progressive disclosure·호환성 | 형식 준수 != 안전·품질·적합성 |
| **`anthropics/skills`** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | 공식 예제·구조·개별 license·변경 관찰 | 예제마다 license·권한·소비자 적합성 확인 |
| **`obra/superpowers`** | `PROFESSIONAL_PRACTICE` | brainstorming·planning·TDD·review·verification upstream | 현재 Base와 자동 동기화하지 않음 |
| **skills.sh 등 Skill directory** | `DISCOVERY_FEED` | 후보 이름·upstream 발견 | listing != vetted dependency; installs != authority |
| **OpenSSF Scorecard** | `AUTHORITY_TARGET` | repository practice risk signal | score != malware 부재·전체 보안 PASS |
| **OSV / OSV-Scanner** | `AUTHORITY_TARGET` | 알려진 vulnerability·advisory | scan 성공 != 미공개 취약점·runtime 안전성 |
| **deps.dev** | `AUTHORITY_TARGET` | dependency graph·version·license metadata·advisory | metadata != 법률 자문·complete inventory |
| **SLSA** | `AUTHORITY_TARGET` | build provenance·artifact integrity 질문 | 표준 준수 주장 != 실제 provenance evidence |

Evidence 권위와 실행 신뢰는 별도 축이다.

```yaml
executable_surface: NONE | COPYABLE_SNIPPET | SCRIPT | GODOT_ADDON | GDEXTENSION | AGENT_SKILL | HOOK | MCP_SERVER | BINARY | INSTALL_COMMAND
trust_state: DISCOVERED | QUARANTINED | SOURCE_REVIEWED | SANDBOX_TESTED | APPROVED_PINNED | REJECTED
upstream_repository:
pinned_release_or_commit:
checksum_or_digest:
license:
install_command_reviewed:
scripts_and_hooks_reviewed:
network_access:
secret_or_environment_access:
filesystem_scope:
requested_permissions: []
sandbox_result:
representative_behavior_result:
uninstall_or_rollback_path:
```

```text
discovery
→ official upstream / third-party / fork / archive
→ exact release·tag·commit·checksum
→ license·maintenance·compatibility·provenance
→ install command·scripts·hooks·binary·MCP
→ network·secret/environment·filesystem·permissions
→ QUARANTINED disposable workspace
→ source review·minimal sandbox·representative behavior
→ uninstall·rollback
→ APPROVED_PINNED | REJECTED | BLOCKED_UNVERIFIED
```

실행 행동·upstream·권한·제거 경로 중 하나라도 불명확하면 `QUARANTINED` 또는 `BLOCKED_UNVERIFIED`다. marketplace, stars, installs, Scorecard, scanner, schema validation, sandbox 한 번의 성공은 vetted dependency나 security/compliance PASS가 아니다.

## 6. `GODOT_ASSET_AND_PRODUCTION_SOURCES`

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Godot Asset Store** | `DISCOVERY_FEED` | 현재 addon·plugin·script·tool·template 후보와 Store 상태 | Store listing != vetted dependency |
| **Godot Asset Library — legacy discovery** | `DISCOVERY_FEED` | 기존 dependency·과거 addon·미이관 항목 | 신규 채택 기본 경로가 아님 |
| **`godotengine/awesome-godot`** | `DISCOVERY_FEED` | open-source tool·plugin·demo 후보 | curated list != vetted dependency |
| **GDQuest** | `PROFESSIONAL_PRACTICE` | Godot·GDScript·UI·system example | exact Godot version과 프로젝트 조건에 `ADAPT / TEST` |
| **Kenney / Poly Haven** | `DISCOVERY_FEED` | prototype 2D·3D·audio·HDRI 후보 | exact item·license·version 기록 |
| **Freesound / OpenGameArt** | `DISCOVERY_FEED` | audio·2D·3D 후보 | 플랫폼 전체에 하나의 license를 가정하지 않음 |
| **Godot Shaders** | `DISCOVERY_FEED` | shader code·effect 후보 | code·preview·upstream license와 compatibility 분리 확인 |

기존 consumer:

- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `evaluating-godot-assets-and-plugins-before-creation`
- `designing-art-prompts-and-technique-cards`
- `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`
- `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- target project Godot implementation owner and tests

```text
플레이어가 실제로 볼·들을 필요와 프로젝트 방향
→ original item page / repository / exact version
→ item별 license·attribution·redistribution·commercial use
→ Godot version·import·permission·native code
→ addon/GDExtension은 Section 5 quarantine
→ actual build size·memory·performance·readability·identity QA
→ project rights manifest·pin·rollback
```

저해상도, 적은 색, CC0 표시, Store 등록, 인기·별점만으로 용량·가독성·권리·품질·시장성을 증명하지 않는다.

## 7. 주기·승격·완료 상태

권장 cadence:

- `daily-or-weekly`: 공식 AI/Codex/Claude/Gemini/Copilot 변경, 보안 advisory, Godot release·Store·사용 중인 upstream release.
- `weekly`: prompt/eval 도구, skills.sh discovery, 게임 시장·기획 Source, 현재 활성 프로젝트의 작법·아트·addon 후보.
- `monthly-or-on-demand`: 학술·GDC·GUR·작법 archive·Diátaxis/ADR/C4/DORA·자산 Source.
- `quarterly`: Source 중복·stale·license·owner·archive·실제 기여와 설치된 dependency pin 감사.

이 cadence는 실행 명령이 아니며 실제 scheduler는 Base 밖에서 소유한다. 이번 등록은 durable Watchlist/Ledger 승격이 아니다. 반복 material value와 새 사이트 Gate를 통과한 Source만 기존 Watchlist·Ledger family로 승격한다.

각 후보는 다음 중 하나로 닫는다.

```text
NO_CHANGE
EVIDENCE_ONLY_UPDATE
ABSORB_EXISTING_OWNER
PROJECT_ONLY
TEST
REFERENCE_ONLY
AVOID
PROMOTION_CANDIDATE
BLOCKED_UNVERIFIED
```

적대적 검토:

- Source가 바꿀 구체적 결정·consumer·validation·rollback이 있는가?
- 같은 책임이 기존 owner에 있는데 새 Skill·Guide·Source canon을 만들었는가?
- vendor/model/creator의 조언을 전역 Hard Rule로 만들었는가?
- framework·simulation·benchmark를 player evidence로 위장했는가?
- 언어 authority와 창작 품질을 혼동했는가?
- 식별 가능한 voice/style·게임 구조·asset을 복제하려는가?
- listing·score·scanner·format 준수를 vetting으로 오인했는가?
- 실행 후보가 quarantine·pin·rollback을 우회했는가?
- 프로젝트 고유 canon·수치·UI·story direction을 Base로 승격했는가?
- Source 수 증가를 개선으로 오인해 억지 변경을 만들었는가?
