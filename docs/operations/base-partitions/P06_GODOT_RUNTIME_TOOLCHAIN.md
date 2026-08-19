# P06 · Godot, Runtime & Technical Toolchain — Context Pack

## 역할
Godot authoring/runtime/debugging, addon/plugin 평가, editor/runtime adapter, QA technical tooling과 로컬 실행환경을 책임진다.

## 핵심 Skill
`diagnosing-game-engine-runtime-failures`, `evaluating-godot-assets-and-plugins-before-creation`.

## 중요 규칙
HiGodot single authority when adopted, Existing Solution First, actual runtime evidence before PASS, project-dedicated environment, no authoring bypass.

## 핵심 Module
Authoring Authority → Runtime Diagnostics → Addon Evaluation → Adapter → QA Technical Tooling → Local Execution.

## 경계
P04 acceptance와 P05 visual 입력을 소비하고 P07에 runtime evidence를 제공한다. QA Evidence Studio/local tooling은 존재 자체를 유지 근거로 삼지 않는다.

## 우선 공격 대상
중복 writer, process 존재를 readiness로 오판, 사용자 PC에서 실행하지 않은 테스트 PASS, 불필요 addon/tool, QA/local tool unique 기능 없는 잔존.

## 검증/완료
Godot focused tests와 가능한 실제 runtime evidence를 분리 보고. 최소 5회 전체 적대적 개선 후 clean까지.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P06_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.

