---
name: developing-and-revising-serial-fiction
description: Use when planning, drafting, adapting, revising, or diagnosing a serial novel/webnovel where arc/episode structure, POV/voice, scene prose, continuity, pacing/payoff, setup-payoff debt, or reader-feedback evidence materially affects quality. Do not use for game-system design, generic marketing copy, simple proofreading-only edits, or imitation of another writer's style.
---

# 연재소설 집필·퇴고

## 목적과 권한 경계

이 Skill은 연재소설·웹소설의 **정본 보존 → 아크·회차 설계 → POV·캐릭터 voice → 캐릭터 개성·상대 위상 → 장면 집필 → 회차 pacing·payoff → 독자 반응 기반 퇴고**를 소유한다.

기본 계약:

```text
CANON_AND_ADAPTATION_BOUNDARY_FIRST
→ READER_PROMISE
→ ARC_EPISODE_SCENE_SCOPE
→ POV_INFORMATION_AND_VALUE_FILTER
→ CHARACTER_IDENTITY + OPPONENT_THREAT_INTEGRITY
→ EPISODE_VALUE
→ LOCAL_PAYOFF + OPEN_LOOP
→ INFORMATION_LEGIBILITY
→ CONSEQUENCE_MEMORY
→ SETUP_PAYOFF_DEBT
→ REVISION_EVIDENCE
```

이 Skill이 소유하지 않는 책임:

- 사용자 의도·범위·Decision·실행 계약: `managing-project-intake-and-work-contract`
- 등록된 프로젝트 정본의 발행·문서 구조: `managing-design-documents`
- 독립 공격·비판 검증·회귀 판정: `running-adversarial-review-and-refinement`
- 오래된 정본·ID·Template drift: `auditing-canonical-reference-freshness`
- 게임 시스템·코어·밸런스·플레이테스트: `analyzing-and-refining-game-concepts`
- Skill 생성·통합·behavior eval: `evolving-project-discipline-skills`
- 맞춤법 한두 문장만 고치는 단순 proofreading
- 마케팅 카피·게임 개발 YouTube 대본만 작성하는 작업
- 특정 현역 작가·작품의 식별 가능한 문장·말투·비유·대사·장면을 모사하는 작업

Base는 공용 작법과 검수 방법만 소유한다. 작품 고유 인물·세계관·사건 결과·POV 수·장르 비율·플랫폼별 생산 목표는 프로젝트가 소유한다.

## Skill Modes

- `canon-and-continuity`: 사용자 결정, 원작·로그·기존 정본의 우선순위와 각색 허용 영역을 복원하고 사건 결과·정보 시점·관계 연속성을 보호한다.
- `arc-and-episode-design`: 새 이야기·아크·회차 seed가 비어 있으면 `STORY_ORIGIN_ENGINE`으로 pressure·choice·shift를 만들고, Reader Promise, 장기 목표, Episode Value, 상태 변화, 반복 구조 변주와 회차 경계를 설계한다.
- `pov-and-character-voice`: POV가 아는 정보, 주의를 두는 대상, 가치 판단, 욕망, 자기기만과 문장 리듬을 분리한다.
- `character-and-opponent-integrity`: 인물별 관찰·말투·해결법·결점·대표 하이라이트를 분리하고, 중요 상대가 화면 안에서 위협을 증명한 뒤 주인공 고유 방식으로 승패가 결정되는지 감사한다.
- `draft-and-prose`: 사건 요약을 감각·행동·대사·판단이 있는 장면으로 극화하고 설명·중복·작가 해설을 줄인다.
- `serial-pacing-and-payoff`: Local Payoff, Open Loop, 후폭풍, 느림과 정체, setup/payoff 부채와 플랫폼 production target을 점검한다.
- `reader-feedback-and-revision`: 댓글·리뷰를 증상 신호로 묶고 실제 원고 증거와 대조해 최소 수정 가설을 만든다.

필요한 Mode만 사용한다. 모든 회차에 모든 Mode·프레임워크를 강제하지 않는다.

## 사용 조건

- 웹소설·연재소설·장편소설의 로그라인, 아크, 회차 또는 장면을 설계한다.
- 기존 원고의 2차 이상 퇴고, 구조 개편, POV·voice·대사·내면·문단 리듬을 점검한다.
- 주요 인물·조연·적대자의 개성이 흐려지거나, 설정상 강한 인물·적이 장면에서는 약하고 볼품없어 보이는 문제를 진단한다.
- TRPG·게임 로그·실화·기존 원작을 각색하면서 정본 결과와 새 장면 완성도를 함께 지켜야 한다.
- 회차 hook, payoff, 장기 복선, 반복 에피소드 피로를 진단한다.
- 독자 댓글·리뷰·플랫폼 반응이 실제 원고의 어떤 문제를 가리키는지 분석한다.

## 비사용 조건

- `proofreading-only`: 한두 문장의 맞춤법·띄어쓰기·문법만 고친다.
- `game-system-design`: 게임 시스템·DPS·전투 AI·난이도 자체가 주 작업이다.
- `marketing-copy`: 광고문구·스토어 설명·YouTube 대본만 만든다.
- `style-imitation`: 특정 작가의 문체를 식별 가능하게 복제한다.
- 정본을 바꾸지 않는 단순 요약·번역만 한다.

## Required inputs

현재 작업에 필요한 최소 입력만 읽는다. 없는 항목을 사실로 추측하지 않는다.

```yaml
project_canon_and_priority:
approved_canon_decision_and_superseded_history:
source_material_and_adaptation_boundary:
work_identity_and_reader_promise:
arc_episode_or_scene_scope:
current_draft:
pov_and_character_voice_state:
character_identity_cards:
opponent_threat_ledger:
character_choice_proof:
reader_knowledge_matrix:
highlight_proof:
continuity_and_information_state:
active_and_archive_consumer_inventory:
staged_migration_state:
  enforcement_class:
  declared_legacy_debt_consumers: []
  actual_legacy_debt_consumers: []
  reconciliation_unit:
  verified_prefix:
  declared_migration_boundary:
  legacy_tail:
  frontier_verification_status:
  declared_validation_gate:
  duplicate_current_authority_check:
setup_payoff_ledger:
reader_feedback_evidence:
platform_and_release_constraints:
protected_strengths:
requested_output:
```

불확실 상태:

```yaml
canon_conflict: CANON_CONFLICT
adaptation_boundary_unknown: ADAPTATION_BOUNDARY_UNVERIFIED
platform_rule_stale_or_unknown: PLATFORM_REVERIFY_REQUIRED
human_reader_quality: HUMAN_NOT_RUN
project_pilot: PROJECT_PILOT_NOT_RUN
```

## Read first

1. 프로젝트가 선언한 정본 우선순위와 최신 사용자 결정
2. 현재 아크·회차·장면의 실제 원고와 앞뒤 continuity
3. `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
4. 사용자 선호 문단·대화 호흡이 관련되면 `docs/knowledge/serial-fiction/BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md`를 확인하고 접근 가능한 현재 연결 Drive 자료를 live read한다.
5. 회차 경계·hook·payoff 작업이면 `docs/knowledge/serial-fiction/SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md`
6. 정보 공개·캐릭터 선택 증명·대표 하이라이트·장기 복선/반전 작업이면 `docs/knowledge/serial-fiction/SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md`
7. 캐릭터 개성·강자·적대자·전투/대결 위상 작업이면 `references/character-distinctiveness-and-opponent-threat.md`
8. benchmark·댓글·리뷰 작업이면 `docs/knowledge/serial-fiction/READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md`
9. 필요 시 `references/episode-quality-gates.md`, `references/benchmark-and-reader-feedback.md`

새 이야기·아크·에피소드의 발생 원인이 아직 비어 있으면 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`의 `STORY_ORIGIN_ENGINE`을 선택적으로 읽는다.

캐릭터×캐릭터·캐릭터×세계·캐릭터×능력의 조합이 장면 선택과 관계 변화를 만드는지 점검할 때 `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`의 `RELATIONAL_APPEAL`을 선택적으로 사용한다.

## Process

### 1. 정본과 각색 경계를 먼저 고정한다

`CANON_AND_ADAPTATION_BOUNDARY_FIRST`:

```yaml
protected_facts:
protected_event_results:
protected_information_timing:
adaptable_gaps:
current_scene_scope:
known_conflicts:
```

각색은 빈 인과·감정·행동을 보강할 수 있지만 보호된 결과를 편의상 바꾸지 않는다.

### 1-A. 새 Canon Decision과 기존 DRAFT 이관을 별도 lifecycle으로 다룬다

승인된 새 Canon/Decision은 즉시 현재 권위를 가진다. 그러나 그 이전에 작성된
활성 DRAFT가 모두 이관됐다는 뜻은 아니다. staged migration이 필요한 경우에만
active consumer와 `archive/reference-only` artifact를 먼저 분리하고, 각 규칙에
다음 enforcement class 하나를 선택한다.

- `STRICT_NOW`: 현재 활성 artifact 전체가 즉시 준수해야 한다.
- `FORBIDDEN_IN_NEW_OR_REVISED`: 새로 쓰거나 실질적으로 재퇴고하는 원고에는 즉시
  적용하지만 과거 DRAFT를 blind rewrite하지 않는다.
- `BOUNDED_LEGACY_RECONCILIATION_DEBT`: 정확히 선언한 active consumer set만 legacy
  debt로 남기고, source/Canon/continuity 대조를 거친 bounded revision으로 줄인다.
- `SCOPED_STRICT`: 선언된 아크·시점·플랫폼·버전 범위 안에서만 strict하게 적용한다.

`BOUNDED_LEGACY_RECONCILIATION_DEBT`의 fail-closed invariant는 다음과 같다.

```text
actual_legacy_debt_consumers == declared_debt_consumers
```

새 active consumer가 debt에 나타나거나, 정리된 consumer가 ledger에는 남아 있으면
원인 대조 전 통과시키지 않는다. 정확한 일치는 `PASS_WITH_KNOWN_DEBT`일 수 있으나
`CANON_MIGRATION_COMPLETE`가 아니다. 그 완료 표기는 debt가 0이고 선언된 검증을
통과한 경우에만 사용한다.

부분 이관에서 다음 topology도 함께 기록한다.

```text
VERIFIED_PREFIX
+ DECLARED_MIGRATION_BOUNDARY
+ LEGACY_TAIL
+ FRONTIER_VERIFICATION_STATUS
```

candidate frontier는 데이터가 저장됐다는 뜻일 뿐이다. declared validation gate가
Green일 때만 verified prefix와 boundary를 전진시키며, 미검증 경계 양쪽은
`normal continuity`로 추정하지 않는다. index·reverse outline·scene graph 같은
derived consumer는 그 경계를 `unknown` 또는 project-local migration marker로
보존해야 한다. migration debt가 있어도 한 artifact의 current authority가 둘이면
fail-closed 한다.

### 2. Reader Promise와 현재 회차의 값을 한 문장으로 적는다

Reader Promise는 “독자가 이 작품/아크를 계속 읽으며 반복적으로 받을 핵심 경험”이다.

각 회차의 `Episode Value`는 끝에서 최소 하나의 상태를 실제로 바꾼다.

- 목표
- 정보
- 관계
- 위험
- 위치·접근권
- 능력·자원
- 감정·신념
- 평판·세력 상태

길이만 늘고 상태가 그대로면 `EPISODE_VALUE_MISSING`이다.

### 3. POV를 카메라가 아니라 필터로 사용한다

같은 사실도 POV에 따라 달라져야 한다.

```text
무엇을 아는가
→ 무엇부터 보는가
→ 무엇을 오해하거나 피하는가
→ 어떤 단어·비유·판단을 고르는가
→ 무엇을 말하지 않는가
```

시점을 바꿔도 내면과 문장이 거의 같으면 voice 재검토 대상이다.

### 3-A. 답을 숨길 때 맥락까지 숨기지 않는다

중요 미스터리·배신·관계 오해는 `WITHHOLD_INFORMATION_NOT_CONTEXT`를 적용한다. 독자가 현재 목표·위험·선택·결과를 이해할 맥락은 주고, POV가 모르는 답이나 실제 인물 이유가 있는 민감 정보만 숨긴다. 필요하면 `READER_KNOWLEDGE_MATRIX`로 `POV가 아는 것 / 독자가 아는 것 / 지금 필요한 맥락 / 숨은 진실 / 공개 트리거`를 분리한다.

POV가 자연스럽게 아는 사실을 독자만 속이려고 부자연스럽게 우회하면 `FALSE_SUSPENSE_BY_POV_SUPPRESSION`, 현재 맥락 자체를 미스터리처럼 숨기면 `CONTEXT_WITHHELD_AS_MYSTERY`다.

### 4. 사건 요약을 장면 체험으로 바꾼다

장면은 설명문을 늘리는 방식으로 확장하지 않는다.

```text
현재 욕망/목표
→ 외부 또는 내부 저항
→ 행동·대사·감각
→ 판단 또는 선택
→ 관찰 가능한 결과
→ 감정·관계·정보의 후폭풍
```

모든 장면에 이 순서를 기계적으로 강제하지 않는다. 프레임워크가 장면 목적보다 앞서면 `FRAMEWORK_OVERFIT`이다.

### 4-A. 캐릭터 개성과 상대 위상을 함께 감사한다

캐릭터의 매력과 강함을 설정문으로만 주장하지 않는다. 주요 인물은 **관찰 필터·말투/사고·문제 해결 방식·실제 강함 증명·인간적 매력·대가를 만드는 결점·대표 하이라이트**가 서로 구분되어야 한다.

중요 상대는 최소 한 번 자신의 규칙을 주인공에게 강제하는 `own turn`을 가진다. 주인공의 승리는 상대가 갑자기 약하거나 멍청해졌기 때문이 아니라 **숙련(SKILL)·전술(TACTIC)·규칙 해석(RULE)·관계/협상(RELATION)** 중 인물에게 맞는 방식과 비용으로 설명되어야 한다.

원작·로그·구초안을 각색하는 경우 새 전투를 발명하기 전에 원본에 있던 **강함·관계·위협 증명 기능**이 압축 과정에서 사라졌는지 대조하고 `KEEP / RESTORE / REWORK / NEW / REMOVE`로 판정한다. 상세 필드와 실패 기준은 `references/character-distinctiveness-and-opponent-threat.md`를 따른다.

### 4-B. 캐릭터 변화와 대표 하이라이트를 선택으로 증명한다

캐릭터 아크는 설정표의 성장 선언이 아니라 압박 속 선택의 변화인 `CHOICE_PROOF`로 확인한다. 후반의 큰 선택은 앞선 가치·상처·작은 행동을 다시 보면 가능성이 보이는 `SURPRISING_BUT_COHERENT`를 지향한다.

대표 캐릭터 하이라이트는 `IDENTITY + COMPETENCE + COST + CHOICE + CONSEQUENCE`를 점수표가 아닌 감사 렌즈로 사용한다. 강한 장면이 해당 인물의 고유 판단과 실제 유능함을 증명하고, 대가와 결정권을 거쳐 이후 상태를 바꾸는지 본다.

장기 복선·반전은 필요할 때 `SETUP → RECALL → RECONTEXTUALIZE → PARTIAL_PAYOFF → PAYOFF → AFTERMATH`로 추적한다. 모든 복선에 모든 단계를 강제하지 않지만, 중요한 reveal은 이전 경험을 새 의미로 묶고 이후 행동을 바꿔야 한다.

### 4-C. `PARAGRAPH_BREAK_AND_BREATH`

줄바꿈과 문단은 맞춤법 뒤의 장식이 아니라 **독자가 어디에서 멈추고, 무엇을 한 덩어리로 읽고, 어떤 반응을 먼저 보게 되는지**를 조절하는 prose/pacing 장치다.

필요할 때 다음을 함께 본다.

```text
LINE_BREAK_RHYTHM
PARAGRAPH_LENGTH_PATTERN
DIALOGUE_NARRATION_ALTERNATION
REACTION_ISOLATION
```

- `LINE_BREAK_RHYTHM`: 정보·행동·대사·반응의 전환에서 어디서 호흡을 끊는지 본다.
- `PARAGRAPH_LENGTH_PATTERN`: 평균 길이를 quota로 만들지 않고, 긴 설명 덩어리와 짧은 반응 문단의 **분포와 기능**을 본다.
- `DIALOGUE_NARRATION_ALTERNATION`: 대사가 연속으로 붙어 화자·관계·미장센이 흐려지는지, 반대로 매 대사마다 불필요한 설명이 끼어 템포가 끊기는지 본다.
- `REACTION_ISOLATION`: 충격·침묵·짧은 선택·시선 변화처럼 독자가 별도로 받아야 하는 beat는 독립 문단이 효과적인지 검토한다. 모든 짧은 문장을 독립 문단으로 만들지는 않는다.
- 빈 줄은 장면 전환, 시간 점프, 정서적 beat 구분처럼 의미가 있을 때 사용한다. 단순히 화면을 잘게 쪼개기 위한 blank-line 남용은 피한다.
- 모바일/웹 연재에서는 시각적 덩어리 크기와 스크롤 리듬을 확인하되 “한 문장 = 한 문단” 같은 universal rule을 만들지 않는다.
- 소리 내 읽기, 모바일 폭, 앞뒤 문단의 정보 연결을 함께 보고 과도한 파편화와 벽처럼 긴 문단을 모두 경계한다.

사용자의 Base-owner 선호 참고자료가 관련되면 `BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md`에 따라 connected Drive의 현재 `글따라쓰기`를 `USER_PREFERENCE_EVIDENCE`로 live read할 수 있다. 여기서 추출하는 것은 문단/호흡/대사-서술 전환 같은 구조적 신호이며, 식별 가능한 원문 표현이나 특정 작가의 문체를 복제하지 않는다.

### 5. 회차에서 Local Payoff와 Open Loop를 함께 확인한다

이번 회차를 읽은 대가로 작은 질문의 답, 감정 결산, 관계 변화, 규칙 이해, 성공·실패 결과 중 하나는 제공한다. 없으면 `LOCAL_PAYOFF_MISSING`이다.

다음 회차 동력은 절단식 위기만이 아니다. 새 질문, 새 비용, 관계 불확실성, 바뀐 목표, 규칙의 예외도 Open Loop가 된다.

### 6. 미스터리의 미지성과 가독성을 분리한다

정답·배후·괴이의 완전한 원리는 숨길 수 있다. 하지만 장면에서 다음 네 가지가 추적되지 않으면 `INFORMATION_LEGIBILITY_FAILURE`다.

- 현재 POV
- 즉시 목표
- 장애·위험
- 행동 뒤 바뀐 상태

### 7. 반복 구조는 안정감과 변주를 함께 준다

루프·미션·학원·업무·던전·괴담 등 같은 골격이 반복되면 직전 유사 에피소드와 비교해 최소 하나를 바꾼다.

`규칙/예외 · 비용 · 보상 · 해결 주체 · 감정 · 관계 · 정보 공개 · 실패 형태`

의미 있는 변주가 없으면 `PATTERN_REPETITION_UNVARIED`다.

### 8. 선택과 피해의 흔적을 지운 채 다음 장면으로 넘어가지 않는다

중대한 실패·폭력·능력 사용·배신·구원은 정보·상흔·관계·평판·금기·부채 가운데 하나 이상으로 남긴다. 흔적이 없으면 `CONSEQUENCE_MEMORY_MISSING`이다.

### 9. 장기 복선은 부채로 추적하되 작은 장면을 관료화하지 않는다

장기 질문·복선만 다음 상태를 사용한다.

`SETUP / RECALL / PARTIAL_PAYOFF / PAYOFF / RETIRED / DEFERRED`

정보·반전·감정 구조를 정밀 감사할 때는 companion guide의 `RECONTEXTUALIZE / AFTERMATH`를 선택적으로 추가한다.

장기 미회수 항목을 추적할 방법 자체가 없으면 `SETUP_PAYOFF_DEBT_UNTRACKED`다. 한 장면 안에서 즉시 닫히는 사소한 정보까지 ID화하지 않는다.

### 10. 댓글·리뷰는 정본이 아니라 Evidence로 변환한다

```text
RAW_REACTION
→ SYMPTOM_CLUSTER
→ REVISION_HYPOTHESIS
→ 원고 대조
→ 최소 수정
→ 회귀 검토
```

댓글 하나를 그대로 요구사항으로 승격하면 `COMMENT_AS_CANON`이다.

### 11. 분량은 마지막에 현재 플랫폼 기준으로 확인한다

Base는 특정 글자 수를 universal 완성 기준으로 고정하지 않는다.

판정 순서:

```text
Episode Value
→ 장면/회차 완결성
→ 리듬
→ 현재 플랫폼 계약·과금/연재 조건
→ 프로젝트 production target
```

현재 플랫폼 규칙을 확인하지 못하면 `PLATFORM_REVERIFY_REQUIRED`다.

## Failure states

```yaml
reader_promise_missing: READER_PROMISE_MISSING
episode_value_missing: EPISODE_VALUE_MISSING
local_payoff_missing: LOCAL_PAYOFF_MISSING
information_legibility_failure: INFORMATION_LEGIBILITY_FAILURE
context_withheld_as_mystery: CONTEXT_WITHHELD_AS_MYSTERY
false_suspense_by_pov_suppression: FALSE_SUSPENSE_BY_POV_SUPPRESSION
author_knowledge_leak: AUTHOR_KNOWLEDGE_LEAK
arc_told_not_proven: ARC_TOLD_NOT_PROVEN
unseeded_character_turn: UNSEEDED_CHARACTER_TURN
highlight_without_cost_or_choice: HIGHLIGHT_WITHOUT_COST_OR_CHOICE
spectacle_without_character: SPECTACLE_WITHOUT_CHARACTER
character_identity_blur: CHARACTER_IDENTITY_BLUR
role_homogenization: ROLE_HOMOGENIZATION
opponent_threat_unproven: OPPONENT_THREAT_UNPROVEN
offscreen_strength_only: OFFSCREEN_STRENGTH_ONLY
victory_by_opponent_deflation: VICTORY_BY_OPPONENT_DEFLATION
supporting_cast_steals_climax: SUPPORTING_CAST_STEALS_CLIMAX
pattern_repetition_unvaried: PATTERN_REPETITION_UNVARIED
consequence_memory_missing: CONSEQUENCE_MEMORY_MISSING
setup_payoff_debt_untracked: SETUP_PAYOFF_DEBT_UNTRACKED
payoff_without_aftermath: PAYOFF_WITHOUT_AFTERMATH
canon_migration_debt_expanded: CANON_MIGRATION_DEBT_EXPANDED
canon_migration_completion_overclaim: CANON_MIGRATION_COMPLETION_OVERCLAIM
unverified_migration_boundary_continuity: UNVERIFIED_MIGRATION_BOUNDARY_CONTINUITY
frontier_promotion_without_validation: FRONTIER_PROMOTION_WITHOUT_VALIDATION
duplicate_current_authority: DUPLICATE_CURRENT_AUTHORITY
comment_promoted_to_canon: COMMENT_AS_CANON
identifiable_style_copy: STYLE_COPY_RISK
framework_overfit: FRAMEWORK_OVERFIT
stale_platform_assumption: PLATFORM_REVERIFY_REQUIRED
```

`STYLE_COPY_RISK`이면 원문·대표 표현을 버리고 독자 경험·정보 배치·갈등 기능 같은 고수준 원리로 다시 추상화한다.

## Verification

작업 종류에 따라 다음을 기록한다.

```yaml
mode_used:
canon_sources_checked:
protected_strengths:
reader_promise:
episode_value_before_after:
pov_information_boundary:
reader_knowledge_matrix:
character_choice_proof:
character_identity_matrix:
highlight_proof:
opponent_threat_ledger:
source_function_reconciliation:
local_payoff:
open_loop:
continuity_changes:
canon_migration_enforcement_class:
declared_and_actual_legacy_debt_consumers:
reconciliation_unit_and_frontier_status:
declared_validation_gate_and_result:
derived_consumer_boundary_handling:
duplicate_current_authority_check:
setup_payoff_changes:
reader_evidence_and_sample_limits:
platform_constraint_status:
adversarial_findings:
remaining_not_run:
```

초안이 좋아 보인다는 인상만으로 완료하지 않는다. 실제 원고 diff와 정본, 앞뒤 회차, 필요 시 독자 반응 표본을 대조한다.

## Completion

완료 조건:

- 보호 정본과 각색 변경이 구분된다.
- 선택한 Mode의 Quality Gate를 통과한다.
- 주요 캐릭터의 고유 관찰·해결법·결점·대표 하이라이트가 교환 가능하지 않으며, 중요 상대의 위협과 강함이 화면 안에서 증명된다.
- 주요 캐릭터의 변화가 설정 설명만이 아니라 압박 속 `CHOICE_PROOF`로 확인된다.
- 중요한 미스터리에서 숨긴 답과 독자가 현재 이해해야 할 맥락이 분리되고, POV가 이미 아는 사실을 독자만 속이려고 부자연스럽게 감추지 않는다.
- 대표 하이라이트가 스펙터클만 제공하지 않고 해당 인물의 정체성·유능함·대가·선택·후폭풍을 필요한 범위에서 증명한다.
- 장기 복선의 핵심 payoff가 과거 장면을 재맥락화하고, 중요 reveal 뒤 인물·관계·행동의 `AFTERMATH`가 확인된다.
- 주인공의 승리가 상대의 갑작스러운 무능화에 기대지 않고, 조연의 강함 증명이 주연의 핵심 선택·결말을 빼앗지 않는다.
- staged migration에서는 `PASS_WITH_KNOWN_DEBT`, candidate frontier, verified prefix,
  `CANON_MIGRATION_COMPLETE`를 서로 바꾸어 주장하지 않는다.
- 회차/장면에서 무엇이 달라졌는지 설명할 수 있다.
- 설명량 증가를 완성도 향상으로 오인하지 않는다.
- 외부 작품의 식별 가능한 문장을 복제하지 않는다.
- 독자 반응은 표본 한계를 가진 Evidence로 남는다.
- 플랫폼·사람 독자·판매 성과처럼 실행하지 않은 검증은 `NOT_RUN`으로 남긴다.