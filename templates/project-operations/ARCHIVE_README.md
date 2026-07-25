# 프로젝트 아카이브

이 경로의 자료는 현재 정본이 아니며 구현 권한이 없습니다.

- 현재 대체 문서는 각 Manifest record의 `superseded_by`와 프로젝트 Documentation Map에서 확인합니다.
- 아카이브할 때 원문 본문을 보존합니다. 경로만 남기고 내용을 비우는 방식은 금지합니다.
- 모든 항목은 `MANIFEST.json`에 분류, 원래 경로, 현재 경로, SHA-256, 대체 문서, 사유와 rollback ref를 기록합니다.
- 비밀키, API token, 자격증명과 private key는 아카이브하지 않습니다. revoke·rotate·remove 절차를 적용합니다.
- 복구는 `rollback_ref`에서 원문을 확인한 뒤 현재 정본과 충돌하지 않는 별도 변경으로 진행합니다.
- 폴더명이 `backup`, `[백업]` 또는 `archive`라는 사실만으로 현재 권한 제거가 증명되지는 않습니다.

아카이브 자료를 current canon, 기본 cold start 입력 또는 자동 Skill route 대상으로 등록하지 않습니다.
