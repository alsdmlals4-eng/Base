# BCP-2026-009 — 연재소설 집필·퇴고 공용 Discipline

## 출처와 상태

- 제안 ID: `BCP-2026-009-serial-fiction-writing-and-revision-discipline`
- 출처 프로젝트: 《폭풍의 눈》 TRPG 로그 기반 한국어 웹소설 각색
- Base 기준 커밋: `fa69a77a14f923a756064f6ae151d34cadb374f7`
- 제출일: `2026-08-08`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `HYPOTHESIS_TO_PATTERN_CANDIDATE`
- 설계: `DESIGN.md`
- 벤치마크·적대 검토: `evidence/BENCHMARK_AND_ADVERSARIAL_REVIEW.md`
- 사용자 승인 근거: 이 문서의 `사용자 승인 근거` 절
- 구현 PR: `null` — 제안 PR과 분리해 최신 main에서 생성한다.

`BCP-2026-008`은 현재 main Registry에는 없지만 과거 미병합 PR #190에서 사용된 식별자이므로 이력을 재사용하지 않고 009를 사용한다.

## 문제

Base는 현재 게임 기획·Godot·UI·아트·검증·적대 검토·문서 운영을 세밀하게 라우팅하지만, 소설의 장기 플롯·회차 설계·POV·문체·장면 집필·퇴고·독자 피드백을 한 책임 경계에서 다루는 활성 Discipline Skill이 없다.

《폭풍의 눈》 프로젝트 Sheet의 `작법서`에는 이미 대사, 감정 연속성, 정보 공개, 장면 종료, 장면 목적, POV, 괴담 규칙, 실패 누적, 생활 루틴, 장면 5요소, 복선과 후속 연결 등의 유효한 원칙이 축적되어 있다. 반면 다음과 같은 과잉 고정 규칙과 혼합 책임도 남아 있다.

- 회차·씬을 `공백 제외 2,000자 이상` 같은 단일 숫자로 강제하는 규칙
- 대사·행동·상황·서술 비율을 고정 퍼센트로 다루는 규칙
- `느린 구간 없음`처럼 정적인 장면과 의도적인 저속 장면을 구분하지 않는 규칙
- 인기작의 사건·문체·장르 장치를 성공 공식처럼 복사할 위험
- 모든 장면을 동일한 구조 공식에 넣을 위험
- 개별 댓글을 작품 정본이나 해결책으로 오인할 위험

현재 225화 압축 초안은 완성 연재본이 아니라 사건·관계·결과를 배치한 압축 뼈대이므로, 단순 증량보다 회차 경계 재설계와 장면 극화가 필요하다.

## 공용화 가능한 관찰

인기·장기 연재작과 현업 교육을 비교하면 문체·장르·속도는 서로 크게 다르지만 다음 책임은 반복된다.

1. **Reader Promise** — 초반과 각 아크가 독자에게 어떤 경험을 약속하는지 명확해야 한다.
2. **Episode Value** — 매 회차는 정보·관계·위험·목표·위치·능력·감정 중 적어도 하나의 상태를 실제로 바꾼다.
3. **Local Payoff + Open Loop** — 작은 질문·갈등 하나는 갚고 더 큰 질문 또는 선택 비용을 남긴다. 절단식 클리프행어만 반복하지 않는다.
4. **Legibility under Complexity** — 미스터리의 정답은 숨길 수 있지만 `누가 무엇을 원하고, 무엇이 바뀌고, 당장 무엇이 위험한가`는 추적 가능해야 한다.
5. **Pattern Variation** — 루프·미션·학원·업무·던전·괴담 같은 반복 골격은 예외·대가·보상·감정·관계 중 하나 이상을 변주시킨다.
6. **Voice as Filter** — 강한 문체는 특정 작품의 1인칭 어휘를 복제하는 것이 아니라 같은 사실을 인물별 편견·판단·욕망을 통과시켜 다르게 보이게 하는 것이다.
7. **Consequence Memory** — 실패·폭력·능력 사용·선택은 정보·상흔·관계·평판·금기·부채 중 하나로 남는다.
8. **Setup–Payoff Ledger** — 장기 떡밥은 설치·재호명·부분 회수·최종 회수·폐기 상태를 추적하고, 미회수 부채가 무한히 늘지 않게 한다.
9. **Reader Feedback as Evidence** — 댓글·리뷰는 `혼란, 지루함, 불공정, 보상 부족, 캐릭터 애착, 웃음, 공포, 떡밥 기대` 같은 증상 신호로 집계한다. 독자가 제안한 해결책을 자동 채택하지 않는다.
10. **Platform Range, not Universal Count** — 회차 글자 수는 플랫폼·작품·장면에 따라 달라지며 Base에 단일 숫자를 보편 규칙으로 고정하지 않는다. 프로젝트가 현재 플랫폼과 표본을 확인해 production target을 둔다.

## 반례와 적대적 검토

### REJECTED_CRITIQUE — 인기작의 공통 문체를 만들자

기각한다. 《방랑기사로 살아가는 법》처럼 낮은 피로도와 단순·담백한 진행이 강점인 작품과, 《괴담 호텔 탈출기》처럼 정보 복잡도·군상 추론 자체가 재미인 작품이 동시에 성공한다. 하나의 문장 길이·대사 비율·설명량을 공용 규칙으로 만들면 양쪽을 모두 손상시킨다.

### REJECTED_CRITIQUE — 모든 회차에 강제 이분법 선택과 5단계 장면 구조를 넣자

기각한다. Story Grid, Save the Cat, Story Circle 등은 진단 Lens로 유용하지만 휴식·후폭풍·관계 결산·공포 분위기 장면까지 동일 공식으로 강제하면 기계적 리듬이 된다.

### MUST_FIX — 단일 글자 수를 완성도 Gate로 사용

글자 수는 생산·가격·플랫폼 계약의 보조 지표다. 회차 가치와 장면 완결성을 대체할 수 없다.

### MUST_FIX — 미스터리와 불가독성을 혼동

정답을 숨기는 것은 허용하지만 행동 주체·즉시 목표·위험·결과까지 흐려지면 미지성이 아니라 가독성 실패다.

### MUST_FIX — 댓글을 정본 또는 지시로 취급

독자 반응은 외부 Evidence다. 반복 신호와 표본 편향을 기록하고 프로젝트 코어·정본·실제 원고와 대조한다.

### SHOULD_FIX — 장기 떡밥 부채를 별도 추적하지 않음

장기 연재에서 미회수 복선은 후반 만족도와 결말 신뢰에 직접 영향을 줄 수 있으므로 설치·회수 상태를 추적하는 Ledger를 공용 기준으로 둔다.

## 제안 구조

새 broad Skill을 여러 개 만들지 않는다. 독립 입력·산출물·Quality Bar·검증 경계가 있는 소설 Discipline 하나만 추가한다.

```text
developing-and-revising-serial-fiction
├─ canon-and-continuity
├─ arc-and-episode-design
├─ pov-and-character-voice
├─ draft-and-prose
├─ serial-pacing-and-payoff
└─ reader-feedback-and-revision
```

공용 지식은 최초 구현에서 과분할하지 않고 다음 최소 구조로 시작한다.

```text
docs/knowledge/serial-fiction/
├─ README.md
├─ SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md
├─ SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md
└─ READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md
```

필요한 세부 Lens는 Skill `references/`에 둔다. 실제 반복 사용에서 독립 책임이 확인될 때만 별도 Guide로 승격한다.

## 기존 책임과 경계

- `managing-project-intake-and-work-contract`: 요청·범위·Decision·작업 계약
- `managing-design-documents`: 등록된 정본·문서 발행·동기화
- `running-adversarial-review-and-refinement`: 공격→비판 검증→회귀 재검토
- `auditing-canonical-reference-freshness`: 정본·복선 ID·Template·파생본 drift
- `evolving-project-discipline-skills`: 새 Skill 등록·behavior eval·학습
- `managing-base-change-proposals`: BCP 생명주기
- `developing-and-revising-serial-fiction`: 소설 고유의 플롯·회차·POV·문체·집필·퇴고·독자 반응 해석

게임 기획 Skill에 소설을 흡수하지 않는다. 두 분야는 benchmark라는 활동은 공유하지만 입력, 산출물, Quality Bar와 검증 질문이 다르다.

## 적용 조건

사용:

- 웹소설·장편/연재 소설의 로그라인, 아크, 회차, 장면 설계
- 원고 초안·2차 이상 퇴고
- POV·캐릭터 voice·대사·내면·문단 리듬 점검
- 회차 pacing·hook·payoff·복선 부채 검수
- 독자 댓글·리뷰·플랫폼 반응의 증상 분류와 수정 가설 생성
- TRPG·게임 로그·실화·기존 원작을 소설 장면으로 각색할 때의 continuity 보존

비사용:

- 게임 시스템·레벨 디자인·밸런스 판단
- 마케팅 카피·YouTube 대본만 작성하는 작업
- 단순 문법 교정만 필요한 짧은 문장
- 사용자에게 받은 정본을 바꾸지 않는 단순 요약
- 외부 인기작의 문장·비유·캐릭터 voice를 모사하거나 재현하는 작업

## 보호 범위

Base에 넣지 않는다.

- 《폭풍의 눈》 인물명·세계관·TRPG 사건 순서·능력 수치
- 작품별 고정 POV 수, 장르 비율, 회차 수
- 특정 플랫폼의 영구 고정 글자 수
- 특정 인기작의 문장·대사·비유·플롯 장면
- 개별 댓글 원문 대량 수집
- 프로젝트별 미공개 독자 데이터

## 승인된 구현 범위

1. 새 ACTIVE Skill `developing-and-revising-serial-fiction` 1개
2. 위 최소 Knowledge Hub 4개 파일
3. Skill local references / learning log
4. `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, `docs/OPERATING_MODEL.md`의 one-hop routing
5. `skills/SKILL_REGISTRY.json` 및 생성된 활성 Skill 뷰
6. primary/non-selection behavior eval coverage
7. Skill implementation evidence 등록
8. 전용 계약·반례 테스트와 필요한 기존 CI 소비처
9. Changelog·Learning Log·reference freshness 동기화
10. 외부 벤치마크는 출처·날짜·플랫폼 지표 의미를 기록하고, 저작권 텍스트를 복사하지 않는다.

## 구현 검증

```text
RED: 소설 요청이 현재 Registry에서 전담 owner로 라우팅되지 않고,
     fixed-count / style-copy / comment-as-canon 금지 계약이 존재하지 않음을 재현
→ GREEN: Skill·Guide·Registry·cold-start·behavior fixtures 구현
→ focused contract tests
→ Base existing registry/behavior/reference-freshness tests
→ canonical CI exact-head
→ adversarial attack / validate-critique
→ approved minimal fixes
→ regression recheck
→ merge
→ post-merge review
```

실제 독자 만족도·상업 성과·사람 편집자 품질 평가는 Base 정적 계약으로 증명하지 않는다. 프로젝트 적용 후 별도 evidence로 남긴다.

## 사용자 승인 근거

2026-08-08 사용자 지시:

> “좋아 지금 작법서 학습을 먼저 진행하자. … 참고해서 적대적 검토루프로 학습을 진행한 후에 네가 말한대로 스킬 추가,BCP설계,작법 기준 작성을 진행해”

이 지시는 직전 제안된 `소설 전담 Skill 1개 + Knowledge/검수 기준 + BCP` 경계를 명시적으로 승인한 것으로 기록한다. 동일 범위는 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 적용하되, 새 범위·새 사용자 결정·P0/P1·검증 실패가 생기면 자동으로 확장하지 않는다.

## 롤백

제안 단계는 이 BCP 디렉터리와 Registry 항목만 되돌리면 된다. 구현 단계는 별도 PR로 분리하며, 새 Skill·Knowledge routing·behavior fixtures·tests를 한 묶음으로 되돌릴 수 있어야 한다.
