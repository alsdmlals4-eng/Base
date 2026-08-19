# P02 · Skill Governance, Canon Freshness & Legacy — Context Pack

## 역할
Skill 생명주기·중복/과잉·canonical reference freshness·BCP·stale pruning·legacy 흡수/삭제를 책임진다.

## 핵심 Skill
`evolving-project-discipline-skills`, `auditing-canonical-reference-freshness`, `managing-base-change-proposals`, `simplifying-skill-bodies`, `pruning-stale-and-nonfunctional-material`, `governing-legacy-retention-and-archives`.

## 중요 규칙
Existing Solution First, 최소 Skill routing, LEGACY_ABSORB_VERIFY_REMOVE, Google Sheets migration-only, generated artifact hand-edit 금지.

## 핵심 Module
Skill Lifecycle → Freshness → BCP → Simplification → Stale Pruning → Legacy Absorb/Verify/Remove.

## 경계
Skill Registry·shared routes·generated map은 CP0라 직접 수정하지 않는다. 각 Part Skill 본체는 audit 입력으로 읽되 타 Part 본체는 수정하지 않는다.

## 우선 공격 대상
중복 Skill/Mode, 소비자 없는 규칙, Registry와 실제 Skill drift, Figma/HTML/local tool/Sheets 잔존 active authority, unique material 확인 없는 삭제.

## 검증/완료
reference freshness와 관련 회귀를 실행하고 최소 5회 전체 적대적 개선 뒤 clean까지 계속한다.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P02_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
