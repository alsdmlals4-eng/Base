# QA Evidence Studio

**실행 정본:** `tools/qa-evidence-studio`

도구 결과를 단순 UI 동작이 아니라 실제 증거로 검토하기 위한 로컬 QA 도구입니다.

주요 책임:

- 이미지/실행 증거 수집과 검토 패킷
- 결과가 실제 파일·프로젝트 범위 안에 존재하는지 확인
- Implementation Reality Gate에서 “실행됨/생성됨/반영됨” 주장과 증거를 분리

도구는 구현되어 있으나 Windows Tool Hub child로 직접 실행하는 경로는 현재 `BLOCKED_PLATFORM`이며, 그 상태를 성공으로 보고하지 않습니다.
