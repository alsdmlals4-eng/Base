# Legacy Skill Aliases

2026-07-21 스킬 통합 이전의 Skill ID를 새 통합 Skill과 모드로 연결한다. 이 파일은 호환성 검색용이며 실행 스킬 Registry가 아니다.

| 이전 Skill ID | 새 Skill ID | Mode |
|---|---|---|
| `routing-project-work-by-discipline` | `managing-project-intake-and-work-contract` | `route` |
| `conducting-deep-requirement-interviews` | `managing-project-intake-and-work-contract` | `clarify` |
| `transforming-requests-into-prompts` | `managing-project-intake-and-work-contract` | `contract` |
| `installing-game-project-operating-system` | `managing-game-project-operating-system` | `install` |
| `migrating-existing-game-project-structure` | `managing-game-project-operating-system` | `audit` / `migrate` |
| `verifying-game-project-operating-system` | `managing-game-project-operating-system` | `verify` |
| `writing-game-design-documents` | `managing-design-documents` | `author` / `update` / `restructure` |
| `publishing-discipline-bibles` | `managing-design-documents` | `publish` / `validate` |
| `promoting-project-knowledge` | `managing-base-change-proposals` | `extract` / `submit` |
| `reviewing-and-implementing-base-change-proposals` | `managing-base-change-proposals` | `review` / `implement` / `verify` |

## Migration rule

- 새 문서와 Registry에는 새 Skill ID만 사용한다.
- 과거 Issue·PR·case·Git 이력의 이전 ID는 수정하지 않아도 된다.
- 실행 중 이전 ID를 발견하면 이 표로 라우팅하고 새 ID를 기록한다.
- 이전 Skill 파일은 활성 Registry에서 제거하며, 고유 절차는 새 Skill 또는 해당 reference에 승계한다.
