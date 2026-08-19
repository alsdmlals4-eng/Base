# Legacy Skill Aliases

2026-07-21 스킬 통합 이전의 Skill ID와 사용자가 부르는 호환 이름을 새 통합 Skill과 Mode로 연결한다. 이 파일은 호환성 검색용이며 실행 스킬 Registry가 아니다.

`엄격 실행 ID` 열은 **현재 실행 entrypoint에 bare identifier로 남으면 stale로 판정해야 하는 과거 Skill ID**만 적는다. 사람에게 보여주는 호환 이름이나 현행 Skill Mode는 첫 열에는 유지할 수 있지만 엄격 실행 ID로 취급하지 않는다.

| 이전 Skill ID·호환 이름 | 새 Skill ID | Mode | 엄격 실행 ID |
|---|---|---|---|
| `routing-project-work-by-discipline` | `managing-project-intake-and-work-contract` | `route` | `routing-project-work-by-discipline` |
| `conducting-deep-requirement-interviews` | `managing-project-intake-and-work-contract` | `clarify` | `conducting-deep-requirement-interviews` |
| `grill-me`, `grillme`, `Grill Me` | `managing-project-intake-and-work-contract` | `clarify` + `grill-me-protocol.md` | — |
| `transforming-requests-into-prompts` | `managing-project-intake-and-work-contract` | `first-prompt` + `contract` + `clarify` | `transforming-requests-into-prompts` |
| `[좋은 프롬프트]`, `좋은 프롬프트`, `퍼스트 프롬프트`, `first prompt` | `managing-project-intake-and-work-contract` | `first-prompt` + `contract` + `clarify` | — |
| `installing-game-project-operating-system` | `managing-game-project-operating-system` | `install` | `installing-game-project-operating-system` |
| `migrating-existing-game-project-structure` | `managing-game-project-operating-system` | `audit` / `migrate` | `migrating-existing-game-project-structure` |
| `verifying-game-project-operating-system` | `managing-game-project-operating-system` | `verify` | `verifying-game-project-operating-system` |
| `writing-game-design-documents` | `managing-design-documents` | `author` / `update` / `restructure` | `writing-game-design-documents` |
| `publishing-discipline-bibles` | `managing-design-documents` | `publish` / `validate` | `publishing-discipline-bibles` |
| `promoting-project-knowledge` | `managing-base-change-proposals` | `extract` / `submit` | `promoting-project-knowledge` |
| `reviewing-and-implementing-base-change-proposals` | `managing-base-change-proposals` | `review` / `implement` / `verify` | `reviewing-and-implementing-base-change-proposals` |
| `reviewing-external-ai-drafts` | `reviewing-and-validating-project-changes` | `external-source-review` / `static-validation` / `regression` / `evidence-report` | `reviewing-external-ai-drafts` |
| `reconcile-legacy`, `legacy-retention-archives` | `governing-legacy-retention-and-archives` | `inventory` / `classify` / `reconcile` / `archive` / `verify` | `legacy-retention-archives` |
| `asset-store-first`, `godot-asset-search-first`, `commercial-plugin-search` | `evaluating-godot-assets-and-plugins-before-creation` | `search` / `evaluate` / `trial-plan` / `adoption-decision` | `asset-store-first`, `godot-asset-search-first`, `commercial-plugin-search` |

## Migration rule

- 새 문서와 Registry에는 새 Skill ID만 사용한다.
- 과거 Issue·PR·case·Git 이력의 이전 ID는 수정하지 않아도 된다.
- 실행 중 이전 ID나 호환 이름을 발견하면 이 표로 라우팅하고 새 ID·Mode를 기록한다.
- `[좋은 프롬프트]` 계열 이름은 새 Skill을 만들지 않고 intake Skill에서 direction anchor 작성, 실행 계약 변환, Grill Me 정합성 확인 순서로 처리한다.
- `grill-me`, `Grill Me`, `좋은 프롬프트`, `reconcile-legacy` 같은 호환 이름/현행 Mode는 사용자-facing 표현 또는 Mode로 사용될 수 있으므로 bare stale Skill ID 검사 대상이 아니다.
- 이전 Skill 파일은 활성 Registry에서 제거하며, 고유 절차는 새 Skill 또는 해당 reference에 승계한다.
