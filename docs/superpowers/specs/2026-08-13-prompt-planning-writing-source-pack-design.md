# 프롬프트·기획·글쓰기 작법 Source Pack 설계

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-13 사용자 요청
base_main_sha: f08a78b33aa1d458376da8f783553fe9ce7aa9cd
source_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
new_active_skill: false
scheduler_authority: EXTERNAL_TO_BASE
```

## 1. 문제와 목표

Base에는 외부 Source Watchlist, 프롬프트·Context 설계 Method, 게임 기획 Skill, 문서 관리 Skill, 연재소설 집필·퇴고 Skill과 인터랙티브 서사 Method가 이미 있다. 다만 프롬프트·기획·글쓰기 작법 자료를 조사할 때 공식 자료, 현업 방법, 교육·큐레이션이 같은 권위로 보이거나 특정 모델·조직·장르의 조언을 공용 법칙으로 과잉 일반화할 위험이 있다.

이번 변경은 다음을 목표로 한다.

- 세 분야 Source를 `AUTHORITY_TARGET`, `PROFESSIONAL_PRACTICE`, `DISCOVERY_FEED`, `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE`로 구분한다.
- Source마다 바꿀 수 있는 결정, 적용 한계, 기존 Base consumer를 명시한다.
- 발견 자료는 공식 문서·원 연구·원 발표로 역추적한다.
- 프롬프트는 대표 입력과 실제 실행 환경 평가, 기획은 소비자·결정·검증·롤백, 글쓰기는 실제 원고와 독자·플레이어 근거로 닫는다.
- 새 ACTIVE Skill, 별도 scheduler, 중복 ledger를 만들지 않는다.

외부 글을 Base 정본으로 복제하거나 특정 프롬프트 문구·기획 프레임워크·작법 공식을 Hard Rule로 만들지 않는다. 특정 작가·작품의 식별 가능한 문체·대사·장면도 모사하지 않는다.

## 2. 채택 구조

기존 Watchlist에 모든 세부 자료를 계속 누적하거나 분야별 새 Skill을 만드는 대신 전용 Reference Pack을 둔다.

```text
PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
= Source role·Evidence·scan·승격 정책 owner

PROMPT_PLANNING_WRITING_SOURCE_PACK.md
= 세 분야 Source surface·consumer routing·적용 Gate

EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
= claim별 Evidence tier·상태·판정 owner

기존 Skill·Method·Guide
= 실제 작업 실행과 프로젝트 적용 owner
```

Pack은 두 번째 Watchlist가 아니다. 별도 실행·일정·승격 권한을 갖지 않으며 Watchlist의 `ORIGINAL_SOURCE_BACKTRACE`, Existing Solution First, Evidence tier, 적대적 검토와 PR 검증을 재사용한다.

## 3. 프롬프트·Agent 작업구조

공식 Source는 OpenAI Developers, Anthropic Docs/Engineering, GitHub Copilot Docs, Google Cloud/ADK, Microsoft Learn, Agent Skills Specification이다. `anthropics/skills`, `obra/superpowers`와 실제 설치·흡수한 Skill의 원본 저장소는 upstream 관찰 대상으로 둔다. promptfoo, Learn Prompting, Prompt Engineering Guide는 평가 도구 또는 발견 자료로 낮은 권한에서 사용한다.

결과는 다음 기존 owner로 보낸다.

- `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- `managing-project-intake-and-work-contract`
- `AI_SKILL_ADOPTION_GUIDE.md`
- `evolving-project-discipline-skills`
- `simplifying-skill-bodies`
- `optimizing-ai-model-and-prompt-costs`
- `reviewing-and-validating-project-changes`

```text
현재 결정과 실패 증상
→ exact model / product / surface / version
→ prompt / instruction / skill / tool / agent 배치
→ authority·context·constraint·output·validation 계약
→ 정상·경계·실패 Golden Set
→ 실제 harness·tool·budget에서 평가
→ 회귀·비용·반대 사례
→ 기존 owner에 ABSORB | ADAPT | TEST | REFERENCE_ONLY | AVOID
```

인기 prompt, magic phrase, vendor benchmark, prompt 길이, Skill 수와 agent 수는 품질 증거가 아니다. 외부 Skill과 도구는 원본, 사용 조건, 고정 버전, 격리된 시험과 제거 경로를 확인하기 전 직접 채택하지 않는다.

## 4. 기획·결정·문서 구조

Source 후보는 다음과 같다.

- Diátaxis: 문서 사용자의 서로 다른 필요와 문서 형식 구분.
- Architecture Decision Records: 장기 영향 결정의 배경·대안·결과 기록.
- C4 model: 필요한 수준의 소프트웨어 구조 시각화.
- Design Council Double Diamond와 GOV.UK Service Manual: 문제 탐색·정의·가설 검증.
- Shape Up: 범위·위험·비목표와 중단 기준.
- DORA: 전달·운영 연구와 개선 가설.
- 게임 고유 기획은 기존 GDC, Games User Research, 플레이어 근거 Source를 재사용한다.

결과는 intake, game concept, design documents, project operating system, vertical slice, adversarial review owner로 보낸다.

```text
플레이어/사용자 문제와 바뀔 결정
→ 성공 기준·보호 대상·비목표
→ 직접·인접·실패/혼합 사례
→ 가장 작은 검증 가능한 Artifact
→ owner·consumer·Decision 연결
→ PoC / playtest / test / review
→ rollback·폐기 조건
```

Diátaxis의 네 형식, ADR, C4의 네 수준, Shape Up의 조직 운영 방식, DORA 지표를 모든 1인 프로젝트에 그대로 강제하지 않는다. 문서량·Issue 수·PR 수는 플레이어 가치나 진척 증거가 아니다.

## 5. 글쓰기·작법·퇴고

한국어 규범·용례는 국립국어원 한국어 어문 규범, 표준국어대사전, 온라인가나다를 사용한다. 대학 Writing Center는 Purdue OWL 등을 참고한다. 현업 작법은 Reedsy, Writing Excuses, Scriptnotes/John August, Jane Friedman 등 원저자 자료를 본다. 연재·게임 서사는 기존 GDC narrative, IGDA Game Writing, Emily Short, ink, Yarn Spinner Source를 재사용한다. KCI·RISS·KOCCA는 원 연구·원 보고서를 찾는 발견 경로로 사용한다.

결과는 `developing-and-revising-serial-fiction`, `NARRATIVE_AND_RELATIONSHIP_METHOD.md`와 기존 연재소설 Guide로 보낸다.

```text
CANON_AND_CONTINUITY
→ DEVELOPMENTAL_STRUCTURE
→ SCENE_AND_CHARACTER
→ DIALOGUE_AND_INFORMATION
→ LINE_AND_PROSE
→ COPY_AND_PROOF
→ READER_OR_PLAYER_EVIDENCE
```

국립국어원은 한국어 규범·용례 authority이지 창작 미학의 authority가 아니다. 작법 강의와 구조 공식은 실제 원고 문제에 맞춰 `ADAPT` 또는 `TEST`한다. 선형 소설과 게임의 agency·state·branch budget을 구분한다. 댓글·좋아요·조회·판매량은 특정 작법의 인과 증거가 아니다.

## 6. 연결과 검증

`docs/knowledge/game-development/README.md`에 Source Pack 문서 지도와 세 분야의 기존 Skill routing을 추가한다. 새 책임 owner가 아니므로 고수준 Documentation Map에는 별도 항목을 만들지 않는다.

`tests/test_periodic_external_source_watchlist.py`를 먼저 확장한다.

1. Pack이 없고 Hub route가 없어 예상대로 RED인지 확인한다.
2. 최소 Pack과 Hub route를 추가한다.
3. 세 domain·Source role·consumer·과장 방지 Gate를 검사한다.
4. focused unittest와 관련 GitHub Actions를 exact head에서 확인한다.

## 7. 적대적 검토

- 두 번째 Watchlist 또는 새 실행 owner가 되었는가?
- 기존 prompt·game-design·fiction 책임을 복제했는가?
- 제품별 prompt tip과 조직별 기획법을 공용 법칙으로 만들었는가?
- 문법 authority와 창작 품질 authority를 혼동했는가?
- 선형·연재·인터랙티브 매체 경계를 잃었는가?
- 특정 창작자 모사·권리 위험을 만들었는가?
- consumer·검증·rollback 없는 Source를 영구 채택했는가?
- Source 수 증가나 문서 증가 자체를 개선으로 오인했는가?

## 8. 롤백과 완료

단일 squash merge commit을 revert하면 Pack, Hub route, test, spec, plan을 함께 되돌릴 수 있다. 데이터·Schema·runtime migration은 없다.

완료는 Source의 권위·용도·한계·consumer 명시, 기존 owner 유지, 새 Skill·scheduler·ledger 부재, Hub one-hop route, RED→GREEN, exact-head CI, 독립 적대적 검토, 병합 후 `main` readback을 모두 요구한다.
