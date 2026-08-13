# State and Evidence

정상 Run은 생성, 사전 점검, 권위 동기화, 계약 검증, Coverage 초기화, Lease 획득, 격리 작업공간 준비, 실행, 검증, 적대적 검토, PR, Integration 대기, 병합 후 재조회, 폐쇄 순서로 진행한다.

중지 사유에는 stale main SHA, Resource 충돌, 잘못된 계약, Coverage 누락, 보호면 침범, 기획·시각 충돌, 미승인 추가, 테스트 실패, 진전 없음, 예산 초과, 일시 장애, 격리, 사용자 결정 필요가 포함된다. 실패 상태와 근거를 보존하며 같은 입력으로 무한 재시도하지 않는다.

Evidence는 기존 E0 계약, E1 정적 검사, E2 자동 테스트, E3 Runtime, E4 시각 비교, E5 실제 플레이, E6 사람 플레이테스트 계층을 유지한다. Package가 요구한 Evidence를 실행하지 않았으면 완료로 표시하지 않는다. 시각 구현은 Runtime Capture 없이 E4 일치 판정을 할 수 없다.
