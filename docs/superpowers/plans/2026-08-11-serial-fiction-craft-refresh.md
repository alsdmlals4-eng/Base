# Serial Fiction Craft Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 최신 현업·편집 실무 벤치마킹을 Base 연재소설 작법 지식 허브에 일반화하고 Coc-Fiction의 《폭풍의 눈》 구조 감사에 즉시 적용한다.

**Architecture:** 새 broad Skill은 만들지 않는다. Base에는 기존 `developing-and-revising-serial-fiction`의 조건부 companion guide로 정보 공개·캐릭터 선택·하이라이트·복선 회수 규칙을 추가하고, Coc-Fiction에는 출처·적용 판단만 기록한다. 작품 고유 Canon과 플랫폼 고유값은 Base에 넣지 않는다.

**Tech Stack:** Markdown knowledge guides, Python contract tests, GitHub Actions.

## Global Constraints

- Consolidation-first: 새 broad Skill 금지.
- 특정 작가/작품의 문체·사건 배열 복제 금지.
- 외부 자료는 universal rule이 아니라 evidence로 취급한다.
- 현재 본문 대규모 rewrite는 캐릭터→사건/하이라이트→복선/정보구조 감사가 끝난 뒤 진행한다.

---

### Task 1: Contract surface

**Files:**
- Modify: `tests/test_serial_fiction_discipline.py`

- [ ] 정보/맥락 구분, choice-proof arc, highlight proof, staged foreshadowing 토큰을 요구하는 failing contract test를 추가한다.
- [ ] GitHub Actions에서 새 토큰 부재로 RED를 확인한다.

### Task 2: Base craft knowledge

**Files:**
- Create: `docs/knowledge/serial-fiction/SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md`
- Modify: `docs/knowledge/serial-fiction/README.md`
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md`

- [ ] `WITHHOLD_INFORMATION_NOT_CONTEXT` 계약을 추가한다.
- [ ] 캐릭터 변화는 설명이 아니라 반복되는 `CHOICE_PROOF`로 검증한다.
- [ ] 대표 하이라이트는 `IDENTITY + COMPETENCE + COST + CHOICE + CONSEQUENCE`로 감사한다.
- [ ] 복선을 `SETUP → RECALL → RECONTEXTUALIZE → PARTIAL_PAYOFF → PAYOFF → AFTERMATH` 상태로 추적한다.
- [ ] 미스터리/공포용 reader knowledge matrix를 추가한다.
- [ ] contract test와 Base required workflows를 Green으로 만든다.

### Task 3: Project evidence and application

**Files:**
- Modify: `docs/fiction-ops/CRAFT_RESEARCH.md`
- Modify: `fiction/ACTIVE_CONTEXT.md`

- [ ] 2025–2026 편집/작가 실무 자료와 한국 웹소설 현업 신호를 source/evidence/transfer-decision 형식으로 기록한다.
- [ ] 《폭풍의 눈》의 다음 감사에 character choice proof, highlight proof, information/context matrix, foreshadow ladder를 적용하도록 현재 작업 순서를 갱신한다.
- [ ] 프로젝트 전체 CI를 Green으로 확인한다.

### Task 4: Adversarial review and merge

- [ ] Base와 Coc-Fiction diff에서 공용/프로젝트 경계 혼입, 과도한 공식화, 출처 과잉 일반화, 기존 계약 회귀를 검사한다.
- [ ] 필수 CI Green 후 각각 PR을 병합한다.
- [ ] 병합된 Base SHA를 Coc-Fiction Registry 소비자가 요구하는 경우 동기화한다.
