# 게임 엔진 런타임 디버깅 체크리스트

- 재현: 엔진·플랫폼·Scene·입력·저장 데이터·빈도·최초 실패 프레임.
- 로그: 최초 원인 오류와 후속 연쇄 오류를 분리.
- 구조: 누락 Node/Component, 경로, prefab/scene override, lifecycle 순서.
- 연결: Signal·event 구독/해제, 중복 호출, null·destroyed reference.
- 데이터: ID·Schema·직렬화·마이그레이션·리소스 경로.
- 상태: 초기화, scene 전환, pause, async, 재진입, 저장/불러오기.
- 재검증: 원래 재현, 정상 경로, 경계, 저장 호환, export/build, 성능.
