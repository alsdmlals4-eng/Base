# Project Integration Capsule Contract

## 목적

`PROJECT_INTEGRATION_CAPSULE`은 한 프로젝트의 Git worktree, Notion Project/Record,
Godot Editor root, HiGodot 단일 작성 권위, 비용 경계와 검증 증거를 같은 시점에
묶는 **프로젝트별 read-only sidecar**다.

이 Capsule은 다음 어느 것도 대체하지 않는다.

- 프로젝트 기획서·Decision·Notion 사람용 정본
- `PROJECT_BASE_ADAPTER`
- Loop Engineering `PROJECT_EXECUTION_CAPSULE`
- Notion write/concurrency 계약
- HiGodot authoring 계약
- Git diff·test·runtime evidence

```yaml
artifact_role: PROJECT_INTEGRATION_CAPSULE
authority: READ_ONLY_BINDING_NOT_CANON
schema_version: 1
product_write_capability: none
git_metadata_preflight: caller_fetch_required
```

## 도입 판정

```text
Codex local filesystem / Git / Godot CLI
→ REUSE

Notion official hosted MCP search/fetch
→ REUSE_READ_ONLY_FIRST

HiGodot
→ REUSE_AS_SOLE_GODOT_WRITER
→ v1 Capsule에서는 L0_OBSERVE만 허용

신규 godot-gpt-codex-notion monolithic MCP
→ REJECT
```

Codex는 로컬 worktree를 네이티브로 읽으므로 같은 파일을 별도 MCP로 다시
노출하지 않는다. Notion은 Free 범위의 search/fetch와 destination readback만
사용한다. 이 v1 Capsule은 Notion page write, Codex의 Godot 파일 write, HiGodot
L1~L3 mutation을 승인하지 않는다.

## 책임 원본 참조

Capsule은 아래 파일을 복제하지 않고 정확한 경로로 참조한다.

| 경계 | 책임 원본 |
|---|---|
| Notion/repository 정본 분할 | `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` |
| Notion Project 격리·충돌·readback | `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md` |
| GPT/Codex 역할·handoff | `docs/GPT_CODEX_WORKFLOW_POLICY.md` |
| Godot 단일 작성 권위 | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` |

Capsule은 프로젝트의 canonical `skills/PROJECT_BASE_ADAPTER.json`과
`HIGODOT_ADOPTION_RECORD.json`을 경로+SHA-256으로 참조한다. Base release,
project identity, HiGodot exact pin, Godot version을 새 필드가 다시 소유하지 않는다.
Capsule의 기록이 책임 원본과 충돌하면 책임 원본이 우선하고 Capsule은
`BLOCKED_UNVERIFIED`로 되돌아간다.

## v1 local receipt-binding 게이트

`READ_ONLY_BINDING_VERIFIED`는 다음을 모두 만족할 때만 허용한다.

1. 승인 Decision record가 Git에 추적되고 Decision ID, approval reference, Project ID,
   repository, Notion Project/Record Key를 정확히 포함한다.
2. 호출자가 검사 직전에 `git fetch --prune origin`을 수행했다는 전제 아래,
   validator는 cached local base branch, `refs/remotes/origin/<base_branch>`,
   `base_sha`, `result_sha`, HEAD가 모두 같은 commit인지 확인한다.
3. Godot Editor root와 Git top-level worktree root가 같은 경로로 resolve된다.
4. Git index가 `result_sha` tree와 object ID·mode·stage까지 같고, capsule 자신 외
   untracked file, 제한된 `.godot` generated-cache allowlist 외 ignored file,
   `skip-worktree`/`assume-unchanged`가 없다.
5. 모든 tracked regular file의 raw worktree bytes가 Git clean filter를 실행하지 않고
   계산한 Git blob object ID 기준으로 `result_sha`와 정확히 일치한다. POSIX에서는
   executable bit도 committed `100644`/`100755` mode와 일치해야 한다. v1은 검증되지
   않은 nested worktree를 만들 수 있는 gitlink/submodule과 tracked symlink를
   fail-closed로 거부한다.
6. canonical `skills/PROJECT_BASE_ADAPTER.json`이 현행 v1 또는 v2 schema-valid하고,
   같은 repository/root 및 canonical Base release lock의
   release/evidence/finalization pin을 가리킨다. v2이면 Project ID도 같아야 하며,
   v1 Project ID는 승인 Decision record와 Capsule이 소유하고 Adapter에서 추론하지 않는다.
7. `HIGODOT_ADOPTION_RECORD`가 Git에 추적되고 floating ref가 아닌 exact
   release/tag 또는 40-hex commit pin, Godot version,
   loopback, Codex host, DeepSeek 금지, verification evidence를 소유한다.
8. Notion record는 정확히 하나의 Project relation을 가지며 Record Key가
   `<ProjectKey>::<RecordType>::<LocalId>` 형식이다.
9. 공식 Notion MCP search/fetch로 만든 receipt의 Project, Record Key, Revision,
   엄격한 RFC3339 Last Edited(`T` separator와 `Z` 또는 colon offset 필수), relation
   count와 destination readback `PASS`가 Capsule과 일치한다.
10. Notion 접근은 `SEARCH_FETCH_ONLY`, 기존 page write는 `FORBIDDEN`이다.
11. Codex의 mutation authority는 `NONE_READ_ONLY`이며 Godot 직접 write는
    `FORBIDDEN`이고 Git에 추적된 second-writer canary receipt가 있다.
12. HiGodot은 Adoption Record의 exact pin·`LOOPBACK_ONLY`·`L0_OBSERVE` 경계 안에서
    유일한 future writer다.
13. 비용 필드는 billing 증거가 아니라 `DECLARED_ZERO_INCREMENTAL_COST_POLICY`다.
    GPT Pro, Notion Free, local open-source tools와 선택적 GitHub included/free만
    허용하고 OpenAI API PAYG, paid Notion AI, paid runner/hosting을 명시적으로 금지한다.
14. v1 Evidence는 정확히 한 Notion receipt(E3)와 한 writer canary(E2)만 허용한다.
    Acceptance ID·문장도 local read-only binding 목적에 고정되고 두 receipt를 연결한다.
15. rollback ref는 exact base/result commit이고, 제품 mutation이 없으므로 drill은
    `NOT_APPLICABLE`이어야 한다.
16. Evidence ceiling은 `LOCAL_RECEIPT_BINDING_ONLY`다. Human playtest, visual,
    production, Godot runtime Evidence를 v1에 추가해 PASS 범위를 넓힐 수 없다.

v1의 commit identity field는 GitHub 현행 호환 경계인 40-hex SHA-1만 허용한다.
SHA-256 object-format repository는 v1 지원 범위가 아니며 schema에서 fail-closed로
차단한다. 이를 지원하려면 64-hex identity, rollback, remote-ref, fixture 전체를 함께
승격한 후 별도 version으로 검증해야 한다.

index/tree, visibility flag, untracked, ignored, object availability 중 어느 필수 Git
probe라도 실행·파싱에 실패하면 전용 `*_UNREADABLE` Finding으로 gate를 차단한다.

연결 성공, OAuth 성공, `tools/list`, 문서 존재는 위 항목을 대신하지 않는다.
Notion readback과 writer canary receipt도 정의된 필드가 Capsule과 일치해야 한다.
내용을 만들지 않고 `PASS`로 채우면 허위 증거다.

이 gate는 Git에 고정된 **로컬 receipt의 상호 일치**만 검증한다. 종료 코드 `0`도
Notion credential의 현재 유효성, 실제 page의 실시간 상태, GitHub 원격의 fetch 이후
변경, 실행 중 Godot Editor session, HiGodot runtime 성공을 독립적으로 증명하지 않는다.
그 상태를 주장하려면 같은 실행에서 live connector/readback 또는 producer-authenticated
receipt가 추가로 필요하다.

비용 gate는 현재 plan, invoice, quota 또는 Actions 잔여량을 검증하지 않는다. 이는
별도 과금을 요구하는 구현을 이 경로에서 금지하는 **선언형 설계 정책**이다. 실제
청구 상태를 `SUBSCRIPTION_INCLUDED`로 증명하지 않으며, 비용 조건이 바뀌면 별도
승인과 live billing evidence가 필요하다.

validator는 inherited `GIT_*` 환경변수를 제거하고 명시한 worktree만 검사한다.
snapshot뿐 아니라 canonical Base release/evidence/finalization pin 검사도 같은
fail-closed runner를 사용하므로 clean/smudge filter, optional lock, lazy object fetch를
실행하지 않는다. Git 실행 자체가 실패하면 readiness Finding으로 변환한다. 다만
검사 직전 호출자가 수행하는 `git fetch --prune origin`은 `.git` remote-tracking
metadata를 갱신한다. 따라서 여기서 read-only/no-write는 **제품 파일, Notion page,
Godot Scene/Script/Resource mutation이 없음**을 뜻하며 Git metadata가 영원히
불변이라는 뜻이 아니다.

### Receipt 최소 형식

Notion receipt는 공식 MCP search/fetch 결과를 아래 필드로 정규화한다.
`source` 문자열 자체는 인증서가 아니며, tracked evidence provenance label이다.

```json
{
  "source": "NOTION_OFFICIAL_MCP_SEARCH_FETCH",
  "access_mode": "SEARCH_FETCH_ONLY",
  "existing_page_write": "FORBIDDEN",
  "project": "PROJECT_KEY",
  "project_relation_count": 1,
  "record_key": "PROJECT_KEY::SYSTEM::LOCAL_ID",
  "revision": 1,
  "last_edited": "2026-08-20T00:00:00Z",
  "status": "PASS"
}
```

Writer canary receipt는 Codex의 `project.godot` write 시도가 실제 경계에서
차단됐고 모든 Godot authoring path class가 보호됐음을 기록한다.

```json
{
  "attempted_actor": "CODEX",
  "attempted_path": "project.godot",
  "authoring_provider": "hi-godot/godot-ai",
  "operation_level": "L0_OBSERVE",
  "blocked_paths": ["project.godot", "**/*.gd", "**/*.tscn", "**/*.tres", "**/*.res", "**/*.scn"],
  "observed": "BLOCKED",
  "second_writer_blocked": true,
  "status": "PASS"
}
```

두 receipt는 `result_sha`에 tracked되어야 한다. Capsule 파일 하나만 자기 commit
hash 순환을 피하기 위한 untracked sidecar로 허용한다. `.godot/editor/**`,
`.godot/imported/**`, `.godot/shader_cache/**`와 명시된 generated cache file만
예외다. 이 경로 안에서도 `.gd`, `.gdshader`, Scene/Resource, native library,
`.gdextension`, `.wasm`, `.pck` 등 authoring/executable suffix는 binding을 차단한다.

## 설치와 실행

프로젝트에 필요한 경우에만 Template을 복사한다.

```text
templates/project-operations/PROJECT_INTEGRATION_CAPSULE.json
→ <project>/docs/operations/integration/PROJECT_INTEGRATION_CAPSULE.json
```

Template 구조만 검사:

```bash
python tools/check_project_integration_capsule.py \
  templates/project-operations/PROJECT_INTEGRATION_CAPSULE.json \
  --schema-only \
  --format json
```

프로젝트 local receipt binding 검사(`git fetch --prune origin` 직후 실행):

```bash
python <Base>/tools/check_project_integration_capsule.py \
  docs/operations/integration/PROJECT_INTEGRATION_CAPSULE.json \
  --project-root . \
  --format json
```

출력이 `[]`이고 종료 코드가 `0`이면 `READ_ONLY_BINDING_VERIFIED`다. 이는
`LOCAL_RECEIPT_BINDING_ONLY` 범위이며 live external readiness가 아니다. Finding이
하나라도 있으면 해당 프로젝트의 binding은 `BLOCKED_UNVERIFIED`다.

## 의도적으로 포함하지 않는 것

- Notion 양방향·실시간 동기화
- Notion 기존 인간 작성 page 자동 overwrite
- public URL, LAN, port forwarding, remote tunnel
- Codex/ChatGPT API pay-as-you-go 호출
- Godot Scene·Script·Resource write
- HiGodot L1/L2/L3 mutation 승인
- 자동 commit·push·merge
- SHA-256 object-format Git repository
- runtime·visual·human playtest PASS

쓰기 도입은 이 파일에 필드를 추가해 우회하지 않는다. 대상 프로젝트의 실제
HiGodot adoption record, second-writer fail-closed enforcement, rollback drill, Godot
import/test와 사용자 승인 범위를 갖춘 별도 후속 계약으로 승격한다.

## Rollback

Capsule은 제품 파일을 쓰지 않으므로 제거 시 제품 migration이 없다. 프로젝트에서
Capsule과 read-only evidence를 제거하거나 이전 commit으로 되돌린 뒤 기존 Git,
Notion, HiGodot 책임 원본을 그대로 사용한다. Capsule 삭제가 Notion page·Godot
파일·MCP credential 삭제 권한을 만들지 않는다.
