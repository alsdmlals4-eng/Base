# BCP-2026-009 — 연재소설 집필·퇴고 공용 Discipline

## 출처와 상태

- 제안 ID: `BCP-2026-009-serial-fiction-writing-and-revision-discipline`
- 출처 프로젝트: 《폭풍의 눈》 TRPG 로그 기반 한국어 웹소설 각색
- Base 기준 커밋: `fa69a77a14f923a756064f6ae151d34cadb374f7`
- 제출일: `2026-08-08`
- 상태: `SUBMITTED`
- 지식 상태: `HYPOTHESIS_TO_PATTERN_CANDIDATE`
- 설계: `DESIGN.md`
- 벤치마크·적대 검토: `evidence/BENCHMARK_AND_ADVERSARIAL_REVIEW.md`
- 구현 PR: `null` — 제안 PR과 분리한다.

`BCP-2026-008`은 현재 main Registry에는 없지만 과거 미병합 PR #190에서 사용된 식별자이므로 이력을 재사용하지 않고 009를 사용한다.

## 관찰과 증거

Base는 게임 기획·Godot·UI·아트·검증·적대 검토·문서 운영을 세밀하게 라우팅하지만, 소설의 장기 플롯·회차 설계·POV·문체·장면 집필·퇴고·독자 피드백을 한 책임 경계에서 다루는 활성 Discipline Skill이 없다.

《폭풍의 눈》 프로젝트 Sheet의 `작법서`에는 대사, 감정 연속성, 정보 공개, 장면 종료, 장면 목적, POV, 괴담 규칙, 실패 누적, 생활 루틴, 복선과 후속 연결 등 유효한 원칙이 이미 축적되어 있다. 동시에 다음 과잉 고정 규칙이 남아 있다.

- 회차·씬을 `공백 제외 2,000자 이상` 같은 단일 숫자로 강제
- 대사·행동·상황·서술 비율을 고정 퍼센트로 취급
- `느린 구간 없음`으로 저속 장면과 정체 장면을 구분하지 않음
- 모든 장면을 동일 구조 공식에 넣을 위험
- 인기작의 사건·문체·장르 장치를 성공 공식처럼 복사할 위험
- 개별 댓글을 작품 정본이나 해결책으로 오인할 위험

현재 225화 압축 초안은 완성 연재본이 아니라 사건·관계·결과를 배치한 압축 뼈대다. 단순 증량보다 회차 경계 재설계와 장면 극화가 필요한 상태다.

외부 표본은 사용자 지정 14작품과 한국콘텐츠진흥원 현업 교육, 산경의 웹소설 작법 자료를 포함한다. 공식 플랫폼 지표는 조회·관심·선호·추천의 정의가 서로 다르므로 고유 독자 수로 환산하지 않는다. 상세 출처·표본 한계·독자 반응은 evidence 문서에 기록한다.

## 일반화 후보

인기·장기 연재작은 문체·장르·정보량·개그 강도가 서로 크게 다르지만 다음 책임은 반복된다.

1. **Reader Promise** — 초반과 각 아크가 독자에게 약속하는 경험을 명확히 한다.
2. **Episode Value / State Change** — 매 회차는 정보·관계·위험·목표·위치·능력·감정·평판 중 하나 이상의 상태를 실제로 바꾼다.
3. **Local Payoff + Open Loop** — 작은 질문·갈등 하나는 갚고 더 큰 질문 또는 선택 비용을 남긴다. 절단식 클리프행어만 반복하지 않는다.
4. **Information Legibility** — 미스터리의 정답은 숨길 수 있어도 `누가 무엇을 원하고, 무엇이 바뀌고, 당장 무엇이 위험한가`는 추적 가능하게 한다.
5. **Pattern Variation** — 루프·미션·학원·업무·던전·괴담 골격은 예외·대가·보상·감정·관계·해결 주체 중 하나 이상을 변주한다.
6. **Voice as Filter** — 다른 작품의 1인칭 어휘를 복사하지 않고 인물의 편견·판단·욕망을 통과시켜 같은 사실을 다르게 보이게 한다.
7. **Consequence Memory** — 실패·폭력·능력·선택은 정보·상흔·관계·평판·금기·부채로 남는다.
8. **Setup–Payoff Debt** — 장기 떡밥은 설치·재호명·부분 회수·최종 회수·폐기 상태를 추적한다.
9. **Reader Feedback as Evidence** — 댓글·리뷰는 혼란·지루함·불공정·보상 부족·애착·웃음·공포·떡밥 기대 같은 증상으로 집계하고, 독자가 제시한 해결책은 자동 채택하지 않는다.
10. **Platform Range, not Universal Count** — Base에는 5천/5.5천/6천자 같은 보편 숫자를 고정하지 않고 프로젝트가 현재 플랫폼과 비교 표본을 검증해 production target을 둔다.

제안 Skill은 하나만 둔다.

```text
developing-and-revising-serial-fiction
├─ canon-and-continuity
├─ arc-and-episode-design
├─ pov-and-character-voice
├─ draft-and-prose
├─ serial-pacing-and-payoff
└─ reader-feedback-and-revision
```

공용 지식도 최초 구현에서는 다음 최소 구조로 시작한다.

```text
docs/knowledge/serial-fiction/
├─ README.md
├─ SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md
├─ SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md
└─ READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md
```

POV 전용 Guide와 복선 전용 Guide는 실제 반복 사용에서 독립 소비자가 확인될 때만 분리한다.

## 적용 조건과 비사용 조건

사용:

- 웹소설·장편/연재 소설의 로그라인, 아크, 회차, 장면 설계
- 원고 초안·2차 이상 퇴고
- POV·캐릭터 voice·대사·내면·문단 리듬 점검
- 회차 pacing·hook·payoff·복선 부채 검수
- 독자 댓글·리뷰·플랫폼 반응의 증상 분류와 수정 가설 생성
- TRPG·게임 로그·실화·기존 원작을 소설 장면으로 각색할 때 continuity 보존

비사용:

- 게임 시스템·레벨 디자인·밸런스 판단
- 마케팅 카피·YouTube 대본만 작성하는 작업
- 단순 맞춤법·문법 교정만 필요한 짧은 문장
- 사용자에게 받은 정본을 바꾸지 않는 단순 요약
- 외부 인기작의 문장·비유·캐릭터 voice를 모사하거나 재현하는 작업

기존 책임은 유지한다.

- 요청·Decision·작업 계약 → `managing-project-intake-and-work-contract`
- 등록된 정본·문서 발행 → `managing-design-documents`
- 공격·비판 검증·회귀 → `running-adversarial-review-and-refinement`
- 정본·Template·파생본 drift → `auditing-canonical-reference-freshness`
- Skill 등록·behavior eval → `evolving-project-discipline-skills`
- BCP 생명주기 → `managing-base-change-proposals`

게임 기획 Skill에 소설을 억지로 흡수하지 않는다. benchmark라는 활동은 공유하지만 입력, 산출물, Quality Bar와 검증 단위가 다르다.

## 반례와 위험

### REJECTED_CRITIQUE — 인기작의 공통 문체를 Base 표준으로 만든다

《방랑기사로 살아가는 법》처럼 낮은 피로도와 단순·담백한 진행이 강점인 작품과 《괴담 호텔 탈출기》처럼 정보 복잡도·군상 추론 자체가 재미인 작품이 함께 성공한다. 하나의 문장 길이·대사 비율·설명량을 공용 규칙으로 만들면 양쪽을 손상시킨다.

### REJECTED_CRITIQUE — 모든 장면에 강제 이분법 선택과 5단계 구조를 넣는다

Story Grid, Save the Cat, Story Circle 등은 진단 Lens로 유용하지만 휴식·후폭풍·관계 결산·공포 분위기까지 동일 공식으로 강제하면 기계적 리듬이 된다.

### MUST_FIX — 단일 글자 수를 완성도 Gate로 사용

글자 수는 생산·가격·플랫폼 계약의 보조 지표다. 회차 가치와 장면 완결성을 대체하지 않는다.

### MUST_FIX — 느림과 정체를 동일시

저속 대화·생활·여운 장면도 관계·정보·결정이 변하면 전진한다. 반대로 빠른 전투도 상태가 변하지 않으면 정체다.

### MUST_FIX — 미스터리와 불가독성을 혼동

정답을 숨기는 것은 허용하지만 행동 주체·즉시 목표·위험·결과까지 흐리면 가독성 실패다.

### MUST_FIX — 댓글을 정본 또는 지시로 취급

독자 반응은 외부 Evidence다. 반복 신호와 표본 편향을 기록하고 프로젝트 코어·정본·실제 원고와 대조한다.

### SHOULD_FIX — 장기 떡밥 부채를 추적하지 않음

설치·재호명·부분 회수·회수·폐기 상태를 관찰할 Ledger가 필요하다.

주요 위험:

- 인기작 표본의 생존자 편향
- 플랫폼 조회·관심·선호를 고유 독자 수로 오해
- 현역 작가 voice를 모방하는 저작권·독창성 저하
- framework overfit으로 모든 장면 리듬이 동일해짐
- 새 Skill이 일반 문서 작성이나 게임 기획까지 과다 라우팅
- Base 정적 계약을 실제 독자 만족도 개선 증거로 과장

## 영향 범위와 검증

승인 후보 구현 범위:

1. 새 ACTIVE Skill `developing-and-revising-serial-fiction` 1개
2. 최소 Knowledge Hub 4개 파일
3. Skill local references / learning log
4. `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, `docs/OPERATING_MODEL.md` one-hop routing
5. `skills/SKILL_REGISTRY.json` 및 current generated active Skill view
6. primary/non-selection behavior eval coverage
7. Skill implementation evidence 등록
8. 전용 계약·반례 테스트와 필요한 기존 CI 소비처
9. Changelog·Learning Log·reference freshness 동기화
10. 외부 benchmark 출처·날짜·플랫폼 지표 의미 기록

보호 범위:

- 《폭풍의 눈》 인물명·세계관·TRPG 사건 순서·능력 수치
- 작품별 고정 POV 수, 장르 비율, 회차 수
- 특정 플랫폼의 영구 고정 글자 수
- 특정 인기작의 문장·대사·비유·플롯 장면
- 개별 댓글 원문 대량 수집
- frozen v9.0 release lock/snapshot/plugin payload

검증 순서:

```text
proposal-only validation
→ 별도 lifecycle 승인 상태 기록
→ 별도 implementation branch
→ RED: 전담 라우팅·fixed-count/style-copy/comment-as-canon 금지 계약 부재 재현
→ GREEN: Skill·Guide·Registry·cold-start·behavior fixtures 구현
→ focused contract tests
→ Registry/behavior/reference-freshness regression
→ canonical CI exact-head
→ adversarial attack / validate-critique
→ approved minimal fixes
→ regression recheck
→ merge
→ post-merge review
```

Base 정적 구현만으로 실제 판매 증가, 독자 만족도 향상, 사람 편집자의 품질 승인, 모든 장르의 최적 회차 길이는 증명하지 않는다. 해당 항목은 `NOT_RUN / HUMAN_NOT_RUN / PLATFORM_REVERIFY_REQUIRED`다.

## 승인과 구현

사용자는 2026-08-08 현재 대화에서 직전 제안된 `소설 전담 Skill 1개 + Knowledge/검수 기준 + BCP` 방향에 대해 다음과 같이 명시했다.

> “좋아 지금 작법서 학습을 먼저 진행하자. … 참고해서 적대적 검토루프로 학습을 진행한 후에 네가 말한대로 스킬 추가,BCP설계,작법 기준 작성을 진행해”

이 문구는 구현 방향에 대한 사용자 승인 의사 증거로 보존한다. 다만 Base의 proposal checker는 **신규 제안이 반드시 `SUBMITTED`에서 시작**하도록 강제하므로 이 제안 PR에서는 상태를 승격하지 않는다. 제안 병합 뒤 별도 lifecycle 변경에서 `APPROVED_FOR_IMPLEMENTATION`과 재현 가능한 `approval_ref`를 기록한 뒤 구현한다.

동일 승인 범위는 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 따르되 새 범위·새 사용자 결정·P0/P1·검증 실패는 자동 승인으로 간주하지 않는다.

롤백은 제안 단계에서 이 BCP 디렉터리와 Registry 항목만 되돌리면 된다. 실제 Skill 구현은 별도 PR에서 독립적으로 롤백 가능해야 한다.
