# Rollout and Validation

구축 순서는 다음과 같다.

1. Base #314의 보호 디렉터리 하위 경로 감지를 수정한다.
2. Capsule, Planning Lock, Visual Lock, Implementation Package, Coverage, Active Run, 불변 Run Schema를 만든다.
3. 결정론적 상태기계, 권한, Lease, 예산, Coverage와 Drift Gate를 구현한다.
4. GitHub, Godot, GUT, Figma, Asset Manifest, Runtime Capture Capability를 연결한다.
5. Blacksmith의 기존 A2 실행 이력을 새 Capsule 구조로 이전한다.
6. 서사·데이터 프로젝트와 시각·UI 프로젝트에서 추가 Pilot을 수행한다.
7. 그 뒤에만 Multi-Agent, 제한적 자동 병합, Scheduled SHADOW를 검토한다.

범용성 완료 조건은 구조가 다른 프로젝트 세 곳, Pilot 사이 Kernel 수정 0, 기획·시각 drift escape 0, 누락 요구사항 0, 미승인 추가 0, 프로젝트 간 Context 혼입 0이다.

A2는 각 프로젝트에서 최소 한 건 이상 검증하고, 전체 Runtime은 연속 성공 Run과 stale SHA, Lease 충돌, 범위 밖 쓰기, 반복 실패, 일시 장애, 시각 근거 부재를 안전하게 중지·복구하는 시험을 통과해야 한다.

A3 자동 병합과 Scheduler의 초기 상태는 비활성이다.
