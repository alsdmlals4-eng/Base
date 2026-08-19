# Project GDD Google Sheets Retirement Stub

## Status

`RETIRED_MIGRATION_ONLY`

Google Sheets는 새 프로젝트 기획, GDD, 시각 작업, 자산 카탈로그, 상태 관리의 작업면이 아니다.

현행 권위는 다음과 같다.

```text
latest user decision
→ Notion human-facing project canon
→ repository structured/runtime truth
→ historical Google Sheet only for one-time unique-material migration when explicitly needed
```

## `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`

기존 Sheet에 아직 고유 정보가 남아 있을 가능성이 검증된 경우에만 한 번 읽는다.

```text
legacy Sheet
→ unique / duplicate / obsolete 분류
→ exact Project 확정
→ human-facing meaning → Notion
→ machine/runtime structured meaning → repository-native owner
→ provenance / Decision ID 보존
→ destination readback
→ conflict check
→ MIGRATED_READBACK_VERIFIED
→ active Sheet reference 제거
→ 삭제 또는 사용자가 접근 가능한 archive/trash 처리
```

- workbook 전체를 Notion에 복제하지 않는다.
- 중복 표현, superseded/rejected 결정, tool-specific layout은 이관하지 않는다.
- Project identity가 불명확하면 추정하지 않고 `BLOCKED_UNVERIFIED`로 둔다.
- Sheet row, screenshot, Notion record는 runtime proof가 아니다.
- migration 완료 후 Sheet를 다시 기본 참고 자료로 읽지 않는다.

세부 흡수·삭제 기준은 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`가 소유한다.

이 Stub은 기존 링크가 새 정책으로 안전하게 이동하도록 하는 임시 compatibility locator다. active consumer가 모두 새 정책으로 전환되면 이 파일 자체도 삭제 후보다.
