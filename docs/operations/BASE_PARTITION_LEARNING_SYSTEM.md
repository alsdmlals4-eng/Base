# Base Partition Learning & Source Discovery System

## 목적

P01~P09가 단발 최적화로 끝나지 않고 **작업마다 실제 교훈을 축적하고, 주기적으로 새 외부 Source를 찾아 검증한 뒤 필요한 최소 개선만 흡수**하도록 한다. 새 광역 Skill이나 별도 유료 AI 파이프라인을 만들지 않고 기존 Periodic Source Scan Queue를 재사용한다.

## 1. 작업마다 Learning Checkpoint

모든 Part 작업은 완료 직전에 자기 `learning_log`에 checkpoint 하나를 남긴다. 이것은 회고문이 아니라 재사용 가능한 운영 증거다.

- 무엇이 실제로 잘 작동했는가
- 무엇이 실패/기각됐는가
- 어떤 규칙·Skill·Module에 영향을 주는가
- evidence는 무엇인가
- Part 전용인가, 프로젝트 전용인가, Base 승격 후보인가
- 다음에 확인할 Source 질문과 재검토 조건은 무엇인가

새 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`을 기록한다. 작업마다 억지로 새 원칙을 만들지 않는다.

## 2. 승격 흐름

```text
Part work
→ Part Learning Log
→ PART_ONLY / PROJECT_ONLY / NO_NEW_REUSABLE_LESSON / BASE_PROMOTION_CANDIDATE
→ BASE_PROMOTION_CANDIDATE만 Integration 검토
→ 기존 canonical owner가 있으면 흡수
→ 없고 반복 재사용 가치가 입증될 때만 새 owner 검토
→ regression + adversarial review + merge
```

Learning Log는 새 정본이 아니다. 현행 정책·Skill과 충돌하면 기존 canonical owner가 우선하며, Integration이 승격을 판정한다.

## 3. 주기 Source Learning

기존 `.github/workflows/periodic-source-scan-queue.yml`이 주기적으로 due Source Queue를 준비한다. Queue 준비는 무료/결정론적이며 AI 웹조사를 자동 수행하지 않는다. 실제 조사와 Evidence disposition은 `USER_DIRECTED_CHATGPT_REVIEW`가 수행한다.

Queue는 Manifest의 각 Part `source_discovery`를 읽어 P01~P09별 Learning Radar를 보여준다. 각 Radar는 기존 Source 새 글/변경과 **추가 신규 Source 사이트 탐색** 질문을 함께 가진다.

### Source 후보 판정

`ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE` 중 하나로 닫는다. Source 개수, 조회수, 기사 제목, AI 요약만으로 Canon/학습을 만들지 않는다.

## 4. Part별 Source Radar

### P01 · Project Planning, Operations & Notion
- domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION
- Notion/project operating systems that reduce duplicate decisions and handoff loss
- human-facing documentation patterns that preserve one machine/runtime truth
- agent instruction/context patterns that reduce repeated clarification and unnecessary executor hops
### P02 · Skill Governance, Canon Freshness & Legacy
- domains: SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW
- skill consolidation, progressive disclosure, routing precision and evaluation
- deprecation/legacy retirement patterns that preserve unique knowledge before deletion
- canonical-reference freshness and stale-reference detection practices
### P03 · Adversarial Quality, Refactoring & Git Integrity
- domains: CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW
- adversarial review and defect-finding methods that avoid performative checklist loops
- contract-preserving refactoring and semantic regression detection
- Git/worktree/PR concurrency and exact-head integration safety
### P04 · Game Design, Core, Player Research & Vertical Slice
- domains: GAME_DEVELOPMENT
- player motivation, choice, reward, memory and first-impression evidence
- vertical-slice and prototype validation practices for small teams
- game balance, difficulty, onboarding and player-research methods with usable evidence
### P05 · Art, UX/UI & Visual Assets
- domains: GAME_DEVELOPMENT
- art direction and visual-consistency pipelines that reduce synthetic/AI-looking artifacts
- game UX/UI readability, accessibility and first-impression evaluation
- image-to-structured-layer/reusable-asset workflows and visual provenance management
### P06 · Godot, Runtime & Technical Toolchain
- domains: GAME_DEVELOPMENT, CODE_ENGINEERING
- current Godot engine/runtime/debugging guidance and regressions
- addon/plugin evaluation, editor tooling and local execution reliability
- runtime QA tooling that provides unique evidence without duplicating the authoring authority
### P07 · Platform, Release & Execution Validation
- domains: GAME_DEVELOPMENT, CODE_ENGINEERING
- platform/store/build/release requirements and official policy changes
- evidence-led validation, accessibility/performance/release readiness practices
- backend, entitlement, DRM, rights and distribution practices appropriate for small games
### P08 · AI Operations & External Executors
- domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING
- current agent/context/prompt/eval patterns that reduce tool and skill overload
- model routing and cost-control practices that preserve quality without new paid dependencies
- safe external-executor/worktree patterns for long-running coding tasks
### P09 · Content, Narrative & Publication
- domains: FICTION_AND_INTERACTIVE_NARRATIVE, YOUTUBE_AND_VIDEO_EDITING
- serial-fiction revision, character voice and continuity methods
- interactive narrative, mystery/clue and worldbuilding practices with audience evidence
- game-development YouTube packaging, script, edit and analytics practices without copying expression

## 5. Integration

Integration GPT는 Part별 Learning Log를 읽어 같은 교훈을 중복 승격하지 않는다. Part 고유 교훈은 Part에 남기고, 여러 Part/프로젝트에서 반복되며 evidence가 있는 교훈만 기존 Base canonical owner에 반영한다.

## 6. 완료/안전 경계

- Queue prepared != research completed
- research completed != lesson validated
- lesson validated != Base canon promoted
- external source != project/runtime truth
- periodic scan 때문에 새 Skill/Tool을 강제로 만들지 않음
- 추가 유료 API/SaaS를 기본 경로로 만들지 않음
