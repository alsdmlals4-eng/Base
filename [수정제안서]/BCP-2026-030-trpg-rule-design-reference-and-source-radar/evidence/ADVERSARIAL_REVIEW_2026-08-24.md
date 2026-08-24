# BCP-2026-030 Adversarial Review — 2026-08-24

Scope: proposal, proposal registry entry, TRPG source scan, rights/frontier addendum. Active Base docs are intentionally out of scope until implementation approval.

## Loop 1 — 변경 범위 / diff hygiene

공격 질문:
- proposal-only PR이 `[수정제안서]/**` 밖을 건드리는가?
- Registry 포맷 변경 때문에 실제 의미보다 큰 diff가 생겼는가?
- 기존 open PR/branch를 침범했는가?

Finding:
- 최초 Registry 쓰기가 minified JSON으로 바뀌어 321-line deletion으로 보이는 불필요한 diff가 발생했다.

Correction:
- 기존 pretty formatting을 복원하고 BCP-030 object 추가만 남겼다.
- PR은 proposal/evidence/registry만 변경한다.

Result: PASS after correction.

## Loop 2 — provenance / rights / access status

공격 질문:
- 무료 배포를 open license로 오인했는가?
- SRD의 라이선스를 전체 제품의 art/setting/trademark까지 확대했는가?
- 직접 읽지 못한 Dropbox/Naver 자료를 확정 사실처럼 썼는가?
- 축약 URL이 나중에 검증 불가능하게 만드는가?

Finding:
- GUMSHOE/YZE source scan의 URL이 축약형이어서 재검증성이 부족했다.
- BRP ORC는 percentile/traditional toolkit과 다른 권리 모델을 추가하는 좋은 반례였다.

Correction:
- `TRPG_SOURCE_RIGHTS_AND_FRONTIER_ADDENDUM_2026-08-24.md`에 exact official URLs와 license boundaries를 추가했다.
- Dropbox/Naver는 `UNVERIFIED_DIRECT` 유지.
- SRD text와 Product Identity/상표/artwork를 분리했다.

Result: PASS after correction.

## Loop 3 — 특정 시스템 과적합

공격 질문:
- PbtA의 fiction trigger, Fate의 aspect, Blades의 position/effect를 모든 TRPG 규칙으로 강제하는가?
- 현재 이클립스의 2d6 구조가 Base 공용 원리로 새어 들어갔는가?
- 조사형/전통형/경량형/percentile 등 다른 계열과 비교했는가?

Finding:
- 초기 표현의 `FICTION_FIRST_TRIGGER_CONTRACT`가 읽는 방식에 따라 모든 TRPG의 mandatory move trigger처럼 보일 수 있었다.

Correction:
- fiction-triggered system에 적용되는 conditional pattern임을 proposal에 명시했다.
- d20(D&D SRD), percentile(BRP), dice-pool/step-die(YZE), rules-light(24XX/Lasers & Feelings), OSR-light(Cairn), investigative(GUMSHOE), fiction-first(Dungeon World), aspect-driven(Fate), FitD(Blades), GM-less support(Ironsworn) 등 materially distinct 사례를 유지했다.
- 이클립스 고유 수치/세계관은 active Base 후보에서 제외한다.

Result: PASS after correction.

## Loop 4 — 사용자가 요구한 '룰북 설명 방식' 누락 여부

공격 질문:
- 단순 메커닉 목록만 모으고 '어떤 문제를 어떻게 풀었는가'를 놓쳤는가?
- 목차만 복사하고 개념이 처음 소개→예시→심화→reference로 이동하는 pedagogy를 분석하지 않았는가?
- 실제 플레이 중 펼쳐 쓰는 support artifact를 룰북 부록 정도로 축소했는가?

Finding:
- Source Radar proposal 필드가 source tier/access/rights에 치우쳐 teaching-order 분석을 machine-readable하게 요구하지 않았다.

Correction:
- source record에 `signature_experience`, `problem_solved`, `mechanic_solution`, `teaching_order`, `progressive_disclosure`, `support_artifacts`, `gm_player_information_boundary`, `adopt_adapt_reject`, `limitations`를 필수 분석 축으로 추가했다.
- `REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER`를 공용 후보로 추가했다.
- ZIP 후속 분석 계약도 실제 목차뿐 아니라 개념의 first appearance→re-explanation→reference transition을 추적하도록 명시했다.

Result: PASS after correction.

## Loop 5 — Base owner fit / 장기 유지비 / 실행 현실성

공격 질문:
- 새 Skill이나 두 번째 benchmark workflow가 생기는가?
- 기존 `BENCHMARKING_REFERENCE_GUIDE`, `REVERSE_ENGINEERING_REUSE_PIPELINE`, game-development knowledge hub와 책임이 중복되는가?
- 모든 프로젝트가 방대한 TRPG 자료를 기본 로드하게 되는가?
- 외부 링크 stale/권리 변경에 대응할 재검증 필드가 있는가?

Finding:
- 신규 광역 Skill은 불필요하다. 공용 knowledge reference + source radar만 있으면 기존 game-design skill이 필요할 때 선택적으로 로드할 수 있다.

Decision:
- 새 Skill/tool/dependency/scheduler를 만들지 않는다.
- Guide는 설계 질문/패턴/실패조건 owner, Radar는 source provenance/rights/pedagogy owner로만 둔다.
- game-development README에서 조건부 라우팅한다.
- source record에 recheck condition을 두고 project application은 Evidence Pack/ADOPT-ADAPT-REJECT 경로로 보낸다.

Result: PASS.

## Clean exit

- full-scope loops completed: 5/5
- new valid blocking finding after Loop 5: 0
- project-specific leakage into proposed active Base owners: 0 by design
- new Skill/tool/dependency/runtime change: 0
- proposal-only scope preserved: yes
- implementation status: NOT RUN by lifecycle; separate approved implementation PR required
