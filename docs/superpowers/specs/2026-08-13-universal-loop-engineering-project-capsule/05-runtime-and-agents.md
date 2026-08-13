# Runtime and Agents

초기 Runtime은 장기 서버가 아니라 수동 Trigger 방식이다. 승인된 Capsule, Implementation Package, 기준 main SHA를 입력받아 격리 작업공간에서 구현하고 PR을 만든 뒤 기존 CI와 병합 후 재검증을 사용한다. 프로젝트별 Workflow 복제는 공용 재사용 Workflow로 줄인다.

상태·권한·예산·Lease·완료 판정은 결정론적 Kernel이 소유한다. 기본 역할은 Builder와 별도 Verifier/Critic이다. Builder는 허용 경로만 수정하고 자신의 결과를 최종 승인하지 않는다. 조사 전용 Scout와 시각 비교 전용 Verifier는 필요할 때만 추가한다.

여러 Writer는 요구사항, 입력과 출력, 의미적 Resource Lock이 모두 독립일 때만 병렬화한다. 동일 저장 계약, Scene, Asset Family, 주요 UX 흐름을 수정하면 직렬 실행한다.

Agent에게 제한 없는 Shell이나 Git 권한을 직접 주지 않는다. 프로젝트 ID, Run ID, 기준 SHA, 허용 경로, 보호면, Lease를 확인하는 안전 Wrapper를 거쳐 읽기·쓰기·테스트·Commit·PR 작업을 실행한다.
