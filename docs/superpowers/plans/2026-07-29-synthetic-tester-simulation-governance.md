# Synthetic Tester Simulation Governance Implementation Plan

## 목표

실제 테스터를 구할 수 없는 프로젝트가 AI 가상 페르소나로 설계 위험을 검토하되, 이를 실제 사람 행동·재미·선호·사용성 증거로 오인하지 않도록 공용 Governance와 Template을 제공한다.

## 구조

- 새 광역 Skill을 만들지 않는다.
- 기존 프로젝트 Skill Registry가 게임 디자인·유저리서치·UX·QA 책임을 선택한다.
- Base의 GUR·적대적 검토·통합검증 Skill은 지원 책임만 가진다.
- 결과는 `T6_AI_INFERENCE`, `human_validation: NOT_RUN`, `implementation_authority: NONE`으로 고정한다.

## 작업

1. 실패 계약 테스트를 먼저 추가하고 필수 Governance·Template 부재로 실패하는지 확인한다.
2. `SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md`를 추가한다.
3. `SYNTHETIC_TESTER_SIMULATION_PACKET.md`를 추가한다.
4. 사람 검증 Governance와 지식 허브에서 합성 경로를 분리 라우팅한다.
5. Evidence Workflow에 전용 계약 테스트를 연결한다.
6. 전용·전체 저장소 계약을 통과시킨 뒤 Base에 병합한다.
7. 확정 Base commit을 기준으로 각 프로젝트의 현행 Skill·작업 구조 분석서와 합성 보고서를 작성한다.

## 완료 조건

- 프로젝트 구조 분석 전 합성 보고서를 작성할 수 없다.
- 가상 행동은 `assumption_not_observation`으로 표시된다.
- 가상 페르소나 수를 표본 수로 사용하지 않는다.
- `ADOPT`, `VALIDATED`, `HUMAN_TEST_PASSED`를 합성 결과에 사용하지 않는다.
- 실제 사람·Build·기기·RNG·알고리즘이 필요한 항목은 `TEST` 또는 `NOT_RUN`으로 남는다.
- 제품 코드·데이터·Scene·정본 변경 권한을 생성하지 않는다.
