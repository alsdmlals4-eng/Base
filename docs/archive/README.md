# Base Archive

이 디렉터리는 현재 Base 권한에서 제외됐지만 고유 기록·근거·복구 가치가 있어 보존해야 하는 문서를 관리한다.

## 권한 규칙

- Archive 문서는 Base의 기본 콜드 스타트, 현재 정본, 자동 Skill 라우팅 또는 구현 권한으로 사용하지 않는다.
- 모든 항목은 `docs/archive/ARCHIVE_MANIFEST.json`에 등록한다.
- 모든 보관 항목은 `active_authority: false`, `implementation_authority: NONE`을 유지한다.
- 현재 상태는 `docs/CHANGELOG.md`, GitHub Issue·PR·Actions와 각 프로젝트 저장소의 책임 원본에서 확인한다.
- Archive 내용을 복원할 때는 원문 hash와 rollback ref를 확인하고, 현재 정본과 충돌을 검토한 별도 변경안으로 승계한다.

## 분류

- `ARCHIVE_HISTORY`: 대체된 계획·상태·설명 원문
- `EVIDENCE_RETENTION`: 승인·검증·실패·감사 증거
- `COMPATIBILITY_ONLY`: 과거 경로 소비자를 현재 위치로 연결하는 Stub

Archive 경로명만으로 권한이 제거되는 것은 아니다. Manifest와 Documentation Map에서 활성 권한이 없음을 함께 선언해야 한다.
