# 주기적 Source Radar — 프롬프트·기획·작법·실행 Source 확장 설계

```yaml
status: USER_APPROVED
approved_at: 2026-08-13
baseline_main_sha: f08a78b33aa1d458376da8f783553fe9ce7aa9cd
change_class: ABSORB_EXISTING_OWNER
new_active_skill: false
new_authority_owner: false
scheduler_authority: EXTERNAL_TO_BASE
```

## 1. 목표

기존 주기적 외부 Source 구조가 다음 자료를 반복적으로 발견·검증·흡수하도록 확장한다.

- 프롬프트·instruction·context·evaluation 설계
- 게임 기획·플레이어 경험·시스템 모델링
- 소설·연재소설·글쓰기 작법과 한국어 규범
- 문서·결정·아키텍처·작업구조 방법
- 외부 Skill·addon·script·MCP·binary 같은 실행 Source
- Godot 재사용 자산·addon·art·audio·shader Source

외부 자료를 많이 모으는 것이 목적이 아니다. 현재 결정과 플레이어·독자·개발자 경험을 바꿀 수 있고, 기존 owner와 검증·rollback 경로가 있는 자료만 유지한다.

## 2. 현행 구조와 Gap

```text
PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
= durable Source pool·권위·조사·승격 정책

PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md
= 반복 가치가 아직 확정되지 않은 active candidate

REFERENCE_SOURCE_CATALOG.md
= article·claim Evidence와 재검증 조건

PERIODIC_SOURCE_OPERATIONS_LEDGER.json
= 실제 scan·material candidate·Base 기여 관측 상태
```

새 광역 Skill이나 별도 Source Pack은 필요하지 않다. Gap은 다음 두 가지다.

1. Discovery Seeds에 프롬프트 평가, 게임디자인 연구, 작법, 작업구조, 실행 Source 격리와 Godot 자산 경로가 충분히 구체적이지 않다.
2. Watchlist의 Evidence 권위와 별개로, 후보가 code·tool·file·secret·network에 접근할 수 있는지 추적하는 실행 위험 축이 부족하다.

따라서 새 파일·Skill보다 기존 Watchlist와 Discovery Seeds에 직접 흡수한다.

## 3. 설계 결정

### 3.1 기존 owner 유지

| Source group | 기존 consumer |
|---|---|
| Prompt / instruction / context / eval | `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`, `AI_SKILL_ADOPTION_GUIDE.md`, intake·validation owner |
| 게임 기획 / 플레이어 경험 | `analyzing-and-refining-game-concepts`, feature spec, benchmark·playtest owner |
| 소설 / 연재소설 작법 | `developing-and-revising-serial-fiction`, serial-fiction knowledge, narrative method |
| 문서 / 결정 / architecture | 현행 document·decision·project-operating owner |
| Skill / addon / executable source | AI Skill adoption, dependency/security review, target project tests |
| Godot 자산 / 제작 Source | art direction, Godot implementation, build-size, rights/provenance owner |

새 ACTIVE Skill, Skill Registry entry, Work Mode, specialist agent, 독립 scheduler 또는 Source canon을 추가하지 않는다.

### 3.2 Evidence 권위와 실행 위험 분리

기존 Source role은 유지한다.

```text
AUTHORITY_TARGET
PROFESSIONAL_PRACTICE
DISCOVERY_FEED
OBSERVATIONAL_DATA_OR_VENDOR_GUIDE
```

실행 가능한 후보에는 별도 축을 추가한다.

```yaml
executable_surface: NONE | COPYABLE_SNIPPET | SCRIPT | GODOT_ADDON | GDEXTENSION | AGENT_SKILL | HOOK | MCP_SERVER | BINARY | INSTALL_COMMAND
trust_state: DISCOVERED | QUARANTINED | SOURCE_REVIEWED | SANDBOX_TESTED | APPROVED_PINNED | REJECTED
```

높은 권위의 Source도 현재 프로젝트와 비호환일 수 있다. 인기 있는 community Source도 위험할 수 있다. Source role·별점·설치 수만으로 `trust_state`를 올리지 않는다.

### 3.3 발견 후 승격

이번에 추가하는 사이트는 기본적으로 `ACTIVE_DISCOVERY_SEED`다. 반복 material value와 Watchlist의 새 사이트 추가 Gate를 통과하기 전 `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`의 durable Source family로 승격하지 않는다. 과거 scan이나 기여 counter를 추정해 기록하지 않는다.

## 4. Source group

### 4.1 프롬프트·instruction·context·eval

OpenAI, Anthropic, Google Gemini, GitHub, Microsoft의 공식 guidance를 제품 사실의 authority로 유지한다. DSPy, promptfoo, OWASP GenAI, DAIR.AI Prompt Engineering Guide는 역할을 구분해 discovery·evaluation·security 질문에 사용한다.

```text
현재 task와 실패 증상
→ source of truth·보호 constraint
→ baseline prompt / workflow
→ representative Golden Set·failure set·adversarial set
→ model·version·configuration·tool·permission
→ 한 번에 하나의 controlled change
→ 독립 expected behavior·rubric
→ quality·cost·latency·context·blast radius
→ 실제 consumer·human review
→ version·rollback
```

한두 개 좋은 출력, optimizer score, LLM judge, red-team 도구 PASS는 프로젝트 정확성·사용자 의도·security/compliance를 증명하지 않는다. 제품별 prompt tip을 모델 불변 Hard Rule로 만들지 않는다.

### 4.2 게임 기획·플레이어 경험

DiGRA, Game Studies, MDA 원문, Game Design Patterns, Game Design Workshop, Machinations와 기존 GDC·Games User Research Source를 질문·가설·PoC 설계에 사용한다.

```text
플레이어 job·감정·판타지
→ 의미 있는 선택·고민·포기
→ feedback·보상·기억·결과
→ 첫인상·시장 가독성
→ 제작 범위·콘텐츠·QA 비용
→ 가장 작은 playable PoC
→ playtest·관찰·인터뷰·telemetry
```

framework 이름이나 simulation 결과는 보편 기획 법칙이나 player evidence가 아니다. 장르·플랫폼·대상·팀 규모·예산·실패/혼합 사례를 보존한다.

### 4.3 글쓰기·연재소설·한국어

국립국어원, KOCCA/Storyum, Reedsy, Writing Excuses, Brandon Sanderson BYU 강의, Jane Friedman, Writer's Digest, Writer Beware와 기존 interactive narrative Source를 역할별로 구분한다.

```text
독자 promise·genre·medium
→ character desire·agency·cost
→ scene purpose·state change
→ POV·voice·dialogue·information
→ pacing·setup·payoff·aftermath
→ developmental·scene·line·copy·proof pass
→ editor·reader·platform evidence
```

국립국어원은 한국어 규범·사전·공식 용례 authority이지 문학성·장르 적합성·독자 선호의 authority가 아니다. 작가 인기도·수상·판매 성과는 특정 voice·plot·장면을 복제할 권한이 아니다. 특정 현존 창작자의 식별 가능한 문체·표현은 `AVOID`한다.

### 4.4 작업구조·문서·결정

Diátaxis, Architecture Decision Records, C4 model, DORA를 관찰된 문제에만 적용한다.

- Diátaxis: tutorial·how-to·reference·explanation 사용자 필요 구분.
- ADR: 되돌리기 비싼 중요 결정의 context·대안·결과·supersession.
- C4: 가장 작은 유용한 zoom; 소규모 프로젝트는 context·container로 충분할 수 있다.
- DORA: application/service delivery 경향과 개선 가설; 개인 생산성 순위가 아니다.

문서 분류·ADR 수·diagram 완성도·DORA metric 자체는 작업 품질의 증거가 아니다. 기존 Base owner가 책임을 소유하면 새 형식을 만들지 않고 그 owner를 최소 보강한다.

### 4.5 Skill·addon·실행 Source

Agent Skills specification, `anthropics/skills`, `obra/superpowers`, `skills.sh`, OpenSSF Scorecard, OSV/OSV-Scanner, deps.dev, SLSA를 역할별로 사용한다.

```text
discovery
→ official upstream / third-party / fork / archive
→ exact release·tag·commit·checksum
→ license·maintenance·compatibility·provenance
→ install command·scripts·hooks·binary·MCP
→ network·secret/environment·filesystem·permission
→ QUARANTINED disposable workspace
→ source review·sandbox·representative behavior
→ uninstall·rollback
→ APPROVED_PINNED | REJECTED | BLOCKED_UNVERIFIED
```

marketplace·directory listing, stars, installs, Scorecard, vulnerability scan이나 형식 준수는 vetted dependency·malware 부재·프로젝트 적합성 증거가 아니다.

### 4.6 Godot 자산·재사용 제작 Source

Godot Asset Store, legacy Asset Library, `godotengine/awesome-godot`, GDQuest, Kenney, Poly Haven, Freesound, OpenGameArt, Godot Shaders를 역할별로 조사한다.

```text
플레이어가 볼 필요·프로젝트 art/audio/code 방향
→ 원 source page·exact item/repository/version
→ 항목별 license·귀속·재배포
→ Godot version·import·permission·native code
→ 실행 addon/GDExtension 격리
→ 실제 build size·memory·performance·readability·identity QA
→ 프로젝트 rights manifest·pin·rollback
```

Store·curated list 등록은 검증 완료가 아니다. 플랫폼 전체에 하나의 라이선스를 가정하지 않으며, 실제 asset ID·파일·license copy·import 설정·승인 상태는 프로젝트 정본이 소유한다.

## 5. Data flow와 실패 상태

```text
Source seed
→ ORIGINAL_SOURCE_BACKTRACE
→ Source role·Evidence tier
→ executable_surface·trust_state
→ freshness·scope·version·medium·commercial interest
→ 기존 Base/project owner overlap
→ smallest decision delta
→ 적대적 공격·비판 검증
→ ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
→ 기존 owner 또는 project-only destination
→ exact-head validation
```

- 실행 행동이 불명확하면 `QUARANTINED`다.
- 원출처가 없으면 `PARTIALLY_VERIFIED | CONTEXT_LIMITED | UNVERIFIED`다.
- status가 충돌하면 `UNKNOWN | REVERIFY_BEFORE_USE`를 쓴다.
- 외부 article·prompt·prose·asset 전체를 Base에 복제하지 않는다.
- 외부 조언은 프로젝트 canon·승인된 플레이어 경험·story direction·author voice를 덮어쓰지 않는다.

## 6. 검증·적대적 검토

계약 테스트는 baseline에서 실패하고 구현 뒤 다음을 검증한다.

- 여섯 Source group과 대표 원출처.
- 기존 owner 라우팅.
- `executable_surface`, `trust_state`, pin·sandbox·rollback.
- discovery-only·non-vetting 경계.
- framework·popularity·security tool·style copy의 claim ceiling.
- Watchlist와 Discovery Seeds 권위 분리.

전체 diff에서 다음을 공격한다.

- 새 Skill·owner·Source canon 중복.
- 결정 relevance 없는 링크 목록 비대화.
- vendor/model prompt 조언의 전역 규칙화.
- framework·simulation을 player evidence로 오인.
- 작가 popularity나 예시를 voice/style 복제 근거로 사용.
- listing·marketplace를 vetting으로 오인.
- 보안 도구 성공을 전체 security PASS로 과장.
- 실행 후보가 quarantine을 우회.
- Ledger 이력·contribution의 추정 기록.
- 열린 PR과 경로·책임 충돌.

## 7. 제외·롤백·완료

제외:

- crawler·background scheduler·자동 설치/실행.
- 새 ACTIVE Skill·specialist agent.
- project-specific game/story/UI/art/numeric canon.
- 검증 없는 Ledger 승격.
- 특정 prompt·game-design·writing formula의 universal rule화.

롤백은 이 PR의 squash merge commit을 revert한다. Watchlist 필드, Discovery Seed group, 계약 테스트와 이 설계·계획이 함께 되돌아가며 runtime·data Schema·Skill Registry migration은 없다.

완료는 RED→GREEN, 관련 전체 CI, exact-head와 최신 main 동기화, unresolved 중요 finding 0, 병합 SHA와 post-merge readback을 요구한다. 실행하지 않은 검사는 `NOT_RUN`으로 보고한다.
