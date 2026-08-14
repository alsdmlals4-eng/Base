# Tool Hub

**실행 정본:** `tools/tool-hub`

Base 로컬 도구 스위트의 프로젝트·프로세스 오케스트레이터입니다.

- canonical GitHub URL 기준 프로젝트 자동 탐색·복제·등록
- 프로젝트별 격리된 도구 카탈로그/상태
- Windows 바탕화면 `.lnk` 설치와 `pythonw.exe` 기반 무콘솔 실행
- 이미 실행 중인 Hub 재사용, 인증된 종료, bounded local logs

Windows에서 **Hub 자체의 실행과 프로젝트 온보딩은 검증됨**입니다. 다만 Character/Sprite/QA child Studio 실행은 별도 Windows process ownership/portable staging 단계 전까지 `BLOCKED_PLATFORM`입니다.
