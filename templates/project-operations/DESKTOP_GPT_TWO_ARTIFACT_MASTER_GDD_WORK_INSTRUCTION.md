# Desktop GPT Two-Artifact Master GDD — Compatibility Alias

> Status: `LEGACY_COMPATIBILITY_ALIAS`
> Historical Template ID: `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`
> Current policy: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
> Current paste-ready instruction: `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md`
> Workspace authority: `docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json`

이 파일은 #770 이전에 만들어진 경로를 깨뜨리지 않기 위한 호환 별칭이다. **새 작업지시문을 이 파일에서 복사하지 않는다.** 현재 canonical 실행 지시문은 다음 파일 하나다.

```text
templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md
```

현재 계약:

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN

PDF_ONLY_USER_DOWNLOAD
NOTION_INPUT_ONLY_NO_OUTPUT
SHARED_ID_AND_SOURCE_SHA_REQUIRED
CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED
NO_AUTOMATIC_IMAGE_GENERATION
```

- 사람용 PDF는 `HUMAN_GDD_PDF_DERIVED_VIEW`다.
- AI Markdown과 구현·asset·test evidence는 `REPOSITORY_PRIMARY_PROJECT_CANON`에 둔다.
- 새 Notion page/database/write/upload/sync/readback은 기본 작업이나 완료 조건이 아니다.
- 기존 Notion은 `LEGACY_READ_ONLY_MIGRATION_SOURCE`로만 읽는다.
- 이미지 생성·편집은 사용자가 명시적으로 요청했을 때만 진행한다.

이 파일은 current instruction owner가 아니며 내용 확장·분기·프로젝트별 복제를 금지한다. 오래된 문서·handoff가 이 경로를 가리키면 위 canonical instruction으로 해석한다.
