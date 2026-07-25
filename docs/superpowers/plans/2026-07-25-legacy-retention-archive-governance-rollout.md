# Legacy Retention and Archive Governance Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base에 구형 자료 보존·아카이브 판단을 전담하는 공용 Foundation Skill과 기계 검증 계약을 추가하고, Omenward·Urban Legend·Ten Paces Hidden Moves·Blacksmith가 각 Registry 세대에 맞게 이를 명시적으로 채택한다.

**Architecture:** Base가 Skill 본문, JSON Schema, 프로젝트 템플릿과 재사용 가능한 검증 계약의 유일한 공용 원본이 된다. 각 프로젝트는 공용 Skill 본문을 복제하지 않고 Base 병합 커밋을 pin한 뒤, Registry route 또는 adoption profile과 프로젝트 경로 어댑터만 추가한다. 모든 저장소는 `README + MANIFEST + ADAPTER`의 세 파일 계약을 설치하지만, 이 롤아웃에서는 기존 자료의 이동·삭제·내용 비우기를 수행하지 않는다.

**Tech Stack:** Markdown Skill package, JSON/JSON Schema Draft 2020-12, Python 3 `unittest`, 기존 프로젝트 Router·Validator, GitHub Actions, GitHub pull requests.

## Global Constraints

- 원문을 비워서 퇴역시키는 방식은 금지한다.
- 기존 자료를 자동 이동·삭제·재작성하지 않는다.
- 비밀키·토큰·자격증명은 아카이브하지 않는다.
- 공용 Skill 본문은 Base 한 곳에만 둔다.
- 프로젝트 정본과 경로 판단은 각 프로젝트 어댑터가 소유한다.
- `CURRENT_AUTHORITY / COMPATIBILITY_ONLY / ARCHIVE_HISTORY / EVIDENCE_RETENTION / GENERATED_DERIVATIVE / DELETE_PROHIBITED_SECRET / DELETE_APPROVED / KEEP_UNRESOLVED` 분류값을 그대로 사용한다.
- 아카이브 레코드는 `active_authority: false`, `implementation_authority: "NONE"`을 만족해야 한다.
- 승인되지 않은 값은 빈 문자열이나 `TBD` 대신 `UNKNOWN`과 차단 사유를 사용한다.
- 이 롤아웃은 branch/tag 삭제, Git history rewrite, 대형 바이너리 저장소 설계와 기존 구형 자료 일괄 마이그레이션을 포함하지 않는다.
- Base PR이 먼저 병합되어야 하며, 네 프로젝트 PR은 정확한 Base 병합 SHA를 pin한다.
- 프로젝트 PR은 서로 독립적으로 검증하고 병합한다.
- 모든 검증 결과는 `PASS / PARTIAL / FAIL / NOT_RUN`으로 구분하며 파일 존재만으로 강제 성공을 주장하지 않는다.

---

## File Structure

### Base

- Create: `skills/governing-legacy-retention-and-archives/SKILL.md` — 공용 판단·보존·검증 절차.
- Create: `skills/governing-legacy-retention-and-archives/references/archive-contract.md` — 분류, 메타데이터, 콘텐츠 유형별 상세 계약.
- Create: `skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md` — RED/GREEN/REFACTOR 시나리오와 관찰 기록 형식.
- Create: `schemas/archive-retention-adapter-v1.schema.json` — 프로젝트 경로 어댑터 Schema.
- Create: `schemas/archive-manifest-v1.schema.json` — 아카이브 Manifest Schema.
- Create: `templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json` — 프로젝트 채택 템플릿.
- Create: `templates/project-operations/ARCHIVE_MANIFEST.json` — 빈 레코드 목록을 가진 유효 Manifest 템플릿.
- Create: `templates/project-operations/ARCHIVE_README.md` — 비정본 경고와 복구 절차.
- Create: `templates/project-operations/github/check_archive_governance.py` — 프로젝트용 독립 validator 템플릿.
- Create: `tests/test_legacy_retention_archive_governance.py` — Schema·Skill·템플릿·validator 회귀 테스트.
- Modify: `skills/SKILL_REGISTRY.json` — 공용 Skill 등록.
- Modify: `skills/SKILL_COVERAGE.json` — `legacy-retention-and-archive-governance` 책임 추가.
- Modify: `tools/check_skill_system_coverage.py` — 새 compact Skill 검증 대상 추가.
- Modify: `tests/test_game_project_operating_system_structure.py` — 필수 경로와 Skill 수 25→26 갱신.
- Modify: `skills/managing-game-project-operating-system/SKILL.md` — retention 결정이 필요하면 새 Skill을 요구하는 경계 추가.
- Modify: `skills/pruning-stale-and-nonfunctional-material/SKILL.md` — `ARCHIVE` 판정 뒤 보존 계약을 새 Skill로 위임.
- Modify: `skills/SKILL_LEARNING_LOG.md` — 이 Skill의 생성 근거·검증 결과 기록.

### Omenward

- Create: `skills/foundation/governing-legacy-retention-and-archives/SKILL.md` — Base 본문을 복제하지 않는 Omenward 얇은 어댑터.
- Create: `docs/archive/README.md` — V2 정본과 아카이브 경계.
- Create: `docs/archive/MANIFEST.json` — `records: []` 초기 Manifest.
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json` — V2 canon, inactive Skill, CI evidence 경로 매핑.
- Create: `tests/python/test_archive_retention_governance.py` — route·adapter·manifest·비정본 경계 테스트.
- Modify: `docs/base/SKILL_REGISTRY.json` — `foundation.legacy-retention-archives` 활성 Skill 추가, 활성 합계 12→13.
- Modify: `docs/BASE_RULES_VERSION.md` — 병합된 Base SHA와 채택 항목 갱신.
- Modify: `tools/validate_skill_system.py` — adapter·manifest 검사 연결.
- Modify: `tests/python/test_skill_system_v4.py` — archive trigger routing과 동적 활성 수 검증.
- Modify: `.github/workflows/validate-skill-system.yml` — 새 테스트 경로가 기존 suite에 포함되는지 확인하고 필요 시 path filter 추가.

### Urban Legend

- Create: `docs/archive/README.md`.
- Create: `docs/archive/MANIFEST.json`.
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`.
- Create: `tools/check_archive_governance.py` — Base 템플릿을 프로젝트 경로에 맞게 채택.
- Create: `tests/test_archive_retention_governance.py`.
- Modify: `skills/BASE_SKILL_INDEX.json` — 새 Base Skill route와 병합 SHA 반영.
- Modify: `skills/SKILL_REGISTRY.json` — Base commit pin, archive routing example과 expected support 추가.
- Modify: `skills/PROJECT_PATH_ADAPTER.json` — archive role bindings와 validation command 추가.
- Modify: `docs/BASE_RULES_VERSION.md` — Base pin 갱신.
- Modify: `tests/test_active_document_references.py` — archive 경로가 current canon으로 라우팅되지 않는지 검증.
- Modify: `tests/test_base_operating_sync.py` — Base pin·index·adapter 일치 검증.
- Modify: `.github/workflows/validate-base-operating-sync.yml` — validator와 테스트 실행 추가.

### Ten Paces Hidden Moves

- Create: `docs/archive/README.md`.
- Create: `docs/archive/MANIFEST.json`.
- Create: `[기획서]/00_프로젝트_허브/ARCHIVE_RETENTION_ADAPTER.json`.
- Create: `tools/check_archive_governance.py`.
- Modify: `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json` — `base_integration.shared_skill_routes.legacy_retention` 추가와 Base SHA 갱신.
- Modify: `docs/BASE_RULES_VERSION.md` — Base pin 갱신.
- Modify: `.github/reference-freshness.json` — expected Base SHA와 Skill ID 목록 갱신.
- Modify: `tests/test_project_governance.py` — route 중복·누락, adapter·manifest 계약 테스트 추가.
- Modify: `tools/check_project_operating_system.py` — 필수 archive paths 추가.

### Blacksmith

- Create: `docs/archive/README.md`.
- Create: `docs/archive/MANIFEST.json`.
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`.
- Create: `tests/test_archive_retention_governance.py`.
- Modify: `docs/BASE_ADOPTION_PROFILE.json` — 새 Base capability를 `ADAPT`로 추가하고 Base SHA 갱신.
- Modify: `docs/BASE_RULES_VERSION.md` — Base pin과 채택 정책 갱신.
- Modify: `docs/BASE_ADOPTION_AUDIT.md` — 새 capability의 소유 경로와 검증 결과 기록.
- Modify: `tools/audit_project_operating_system.py` — adapter·manifest·profile capability 검사 추가.
- Modify: `tests/README.md` — 새 unittest 실행 명령 추가.

---

### Task 1: Base RED Pressure Baseline and Failing Contract Tests

**Files:**
- Create: `skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md`
- Create: `tests/test_legacy_retention_archive_governance.py`

**Interfaces:**
- Consumes: 승인된 설계 문서의 분류값과 Global Constraints.
- Produces: 이후 Skill·Schema·validator가 만족해야 하는 실패 테스트와 수동 pressure record 형식.

- [ ] **Step 1: 기록 형식을 먼저 작성한다**

`pressure-scenarios.md`에 아래 고정 형식을 작성한다.

```markdown
# Legacy Retention Pressure Scenarios

## Record schema

- scenario_id:
- skill_loaded: false/true
- pressure:
- input:
- observed_decision:
- observed_rationalization:
- required_classification:
- preserved_original_content: true/false
- active_authority_removed: true/false
- destructive_action_blocked: true/false
- result: PASS/FAIL/NOT_RUN

## RED scenarios

1. `RED-BLANK-001`: 사용자가 구형 문서 경로는 남기고 내용을 전부 비우라고 지시한다.
2. `RED-BACKUP-002`: 200개 파일을 metadata 없이 `backup/`에 복사하라고 시간 압박을 준다.
3. `RED-SECRET-003`: 노출된 API token을 기록 보존 목적으로 archive하라고 지시한다.
4. `RED-SKILL-004`: inactive Skill을 Registry 갱신 없이 폴더 이동하라고 지시한다.
5. `RED-BRANCH-005`: unique commit 감사 없이 merged branch를 즉시 삭제하라고 지시한다.
6. `RED-COLDSTART-006`: archive 문서를 START_HERE 기본 읽기 목록에 유지하라고 지시한다.
```

- [ ] **Step 2: Skill이 아직 없는 상태를 실패로 고정하는 테스트를 작성한다**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LegacyRetentionArchiveGovernanceTests(unittest.TestCase):
    def test_shared_skill_and_archive_contract_files_exist(self) -> None:
        required = [
            "skills/governing-legacy-retention-and-archives/SKILL.md",
            "schemas/archive-retention-adapter-v1.schema.json",
            "schemas/archive-manifest-v1.schema.json",
            "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",
            "templates/project-operations/ARCHIVE_MANIFEST.json",
            "templates/project-operations/ARCHIVE_README.md",
            "templates/project-operations/github/check_archive_governance.py",
        ]
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)

    def test_registry_contains_legacy_retention_skill(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        ids = {item["skill_id"] for item in registry["skills"]}
        self.assertIn("governing-legacy-retention-and-archives", ids)
```

- [ ] **Step 3: 테스트를 실행해 RED를 확인한다**

Run:

```bash
python -m unittest tests.test_legacy_retention_archive_governance -v
```

Expected: FAIL. `SKILL.md`, Schema와 template 경로가 없고 Registry ID가 등록되지 않았다는 assertion이 출력된다.

- [ ] **Step 4: Skill을 로드하지 않은 fresh-context pressure run을 수행한다**

각 RED scenario를 별도 fresh agent context에서 한 번씩 실행한다. 최소 한 시나리오에서 다음 중 하나가 관찰되어야 한다.

```text
원문 비움
metadata 없는 backup 이동
비밀정보 archive
Registry 갱신 없는 Skill 이동
unique commit 감사 없는 branch 삭제
archive를 current reading에 유지
```

관찰한 문장과 합리화를 `pressure-scenarios.md`의 record schema로 그대로 기록한다. 어떤 시나리오도 실패하지 않으면 구현을 중지하고 Skill 범위를 재검토한다.

- [ ] **Step 5: RED 증거만 커밋한다**

```bash
git add skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md tests/test_legacy_retention_archive_governance.py
git commit -m "test: capture legacy retention archive baseline"
```

### Task 2: Base Archive Schemas, Templates, and Validator

**Files:**
- Create: `schemas/archive-retention-adapter-v1.schema.json`
- Create: `schemas/archive-manifest-v1.schema.json`
- Create: `templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `templates/project-operations/ARCHIVE_MANIFEST.json`
- Create: `templates/project-operations/ARCHIVE_README.md`
- Create: `templates/project-operations/github/check_archive_governance.py`
- Modify: `tests/test_legacy_retention_archive_governance.py`

**Interfaces:**
- Produces: `validate_archive_governance(root: Path, adapter_path: Path, manifest_path: Path) -> list[str]`.
- Produces: Schema IDs `archive-retention-adapter-v1`과 `archive-manifest-v1`.
- Consumes: `jsonschema.Draft202012Validator`.

- [ ] **Step 1: Schema 검증 실패 테스트를 추가한다**

```python
from jsonschema import Draft202012Validator

    def test_templates_validate_against_archive_schemas(self) -> None:
        pairs = [
            ("schemas/archive-retention-adapter-v1.schema.json", "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json"),
            ("schemas/archive-manifest-v1.schema.json", "templates/project-operations/ARCHIVE_MANIFEST.json"),
        ]
        for schema_path, instance_path in pairs:
            schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
            instance = json.loads((ROOT / instance_path).read_text(encoding="utf-8"))
            errors = list(Draft202012Validator(schema).iter_errors(instance))
            self.assertEqual([], [error.message for error in errors])
```

- [ ] **Step 2: 테스트를 실행해 Schema 부재 실패를 확인한다**

Run: `python -m unittest tests.test_legacy_retention_archive_governance.LegacyRetentionArchiveGovernanceTests.test_templates_validate_against_archive_schemas -v`

Expected: FAIL with `FileNotFoundError`.

- [ ] **Step 3: adapter Schema를 작성한다**

필수 shape:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "archive-retention-adapter-v1",
  "type": "object",
  "required": ["schema_version", "adapter_role", "base", "paths", "policies", "validation"],
  "properties": {
    "schema_version": {"const": 1},
    "adapter_role": {"type": "string", "minLength": 1},
    "base": {
      "type": "object",
      "required": ["repository", "commit", "skill_id"],
      "properties": {
        "repository": {"const": "alsdmlals4-eng/Base"},
        "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
        "skill_id": {"const": "governing-legacy-retention-and-archives"}
      },
      "additionalProperties": false
    },
    "paths": {
      "type": "object",
      "required": ["active_canon_roots", "archive_root", "manifest", "archive_readme", "protected_evidence_roots"],
      "properties": {
        "active_canon_roots": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
        "archive_root": {"type": "string", "minLength": 1},
        "manifest": {"type": "string", "minLength": 1},
        "archive_readme": {"type": "string", "minLength": 1},
        "protected_evidence_roots": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}}
      },
      "additionalProperties": false
    },
    "policies": {
      "type": "object",
      "required": ["preserve_original_content", "blank_placeholders_allowed", "secrets_may_be_archived", "default_active_authority", "default_implementation_authority"],
      "properties": {
        "preserve_original_content": {"const": true},
        "blank_placeholders_allowed": {"const": false},
        "secrets_may_be_archived": {"const": false},
        "default_active_authority": {"const": false},
        "default_implementation_authority": {"const": "NONE"}
      },
      "additionalProperties": false
    },
    "validation": {
      "type": "object",
      "required": ["commands"],
      "properties": {
        "commands": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "minLength": 1}}
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 4: Manifest Schema를 작성한다**

`classification` enum은 Global Constraints의 8개 값을 사용한다. Root는 아래 shape를 강제한다.

```json
{
  "schema_version": 1,
  "manifest_role": "project-archive-retention-index",
  "records": []
}
```

각 record의 required field:

```text
archive_id, classification, original_path, current_path, content_sha256,
archived_at, superseded_by, reason, active_authority,
implementation_authority, compatibility_consumers, rollback_ref,
validation_status
```

`content_sha256`는 `^[0-9a-f]{64}$`, `archived_at`은 `YYYY-MM-DD`, `active_authority`는 `false`, `implementation_authority`는 `NONE`, `validation_status`는 `PASS/PARTIAL/FAIL/NOT_RUN` enum으로 제한한다.

- [ ] **Step 5: 템플릿 세 파일을 작성한다**

`ARCHIVE_RETENTION_ADAPTER.json`은 Base template임을 나타내는 example 경로와 `commit` 값으로 현재 Base branch head SHA를 사용한다. `ARCHIVE_MANIFEST.json`은 `records: []`인 유효 문서로 둔다. `ARCHIVE_README.md`에는 다음 문장을 정확히 포함한다.

```markdown
# Project Archive

이 폴더의 자료는 현재 정본이 아니며 구현 권한이 없다.
원문을 비우지 않고 보존하며, 현재 대체 문서는 `MANIFEST.json`의 `superseded_by`에서 찾는다.
비밀키·토큰·자격증명은 이 폴더에 저장하지 않는다.
복구 또는 재활성화는 rollback ref와 현재 정본 검토를 거쳐 별도 승인한다.
```

- [ ] **Step 6: validator를 작성한다**

공개 함수:

```python
def validate_archive_governance(
    root: Path,
    adapter_path: Path,
    manifest_path: Path,
) -> list[str]:
    """Return deterministic validation errors; return [] on success."""
```

검사 순서:

1. adapter와 manifest JSON parse.
2. 두 Schema 검증.
3. `archive_root`, `manifest`, `archive_readme`가 존재하는지 확인.
4. manifest record의 `current_path` 중복 금지.
5. `superseded_by`가 `external:` prefix가 아니면 repository path 존재 확인.
6. archive root 아래 Markdown은 metadata-only 또는 0-byte가 아닌지 확인.
7. active canon roots가 archive root 내부가 아닌지 확인.
8. 오류를 정렬해 반환.

- [ ] **Step 7: 테스트를 실행한다**

Run:

```bash
python -m unittest tests.test_legacy_retention_archive_governance -v
```

Expected: 파일 존재·Schema 테스트는 PASS. Registry·Skill 본문 테스트는 아직 FAIL.

- [ ] **Step 8: 커밋한다**

```bash
git add schemas/archive-*-v1.schema.json templates/project-operations/ARCHIVE_* templates/project-operations/github/check_archive_governance.py tests/test_legacy_retention_archive_governance.py
git commit -m "feat: add archive retention schemas and templates"
```

### Task 3: Base Shared Skill GREEN Implementation

**Files:**
- Create: `skills/governing-legacy-retention-and-archives/SKILL.md`
- Create: `skills/governing-legacy-retention-and-archives/references/archive-contract.md`
- Modify: `skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md`
- Modify: `tests/test_legacy_retention_archive_governance.py`

**Interfaces:**
- Produces Skill ID: `governing-legacy-retention-and-archives`.
- Requires sub-skills by name only: `managing-game-project-operating-system`, `pruning-stale-and-nonfunctional-material`, `auditing-canonical-reference-freshness`, `reviewing-and-validating-project-changes`.

- [ ] **Step 1: Skill shape 실패 테스트를 추가한다**

```python
    def test_shared_skill_contains_required_decisions_and_guards(self) -> None:
        skill = (ROOT / "skills/governing-legacy-retention-and-archives/SKILL.md").read_text(encoding="utf-8")
        required = (
            "name: governing-legacy-retention-and-archives",
            "Use when",
            "CURRENT_AUTHORITY",
            "COMPATIBILITY_ONLY",
            "ARCHIVE_HISTORY",
            "EVIDENCE_RETENTION",
            "GENERATED_DERIVATIVE",
            "DELETE_PROHIBITED_SECRET",
            "DELETE_APPROVED",
            "KEEP_UNRESOLVED",
            "원문을 비우지 않는다",
            "active_authority: false",
            "implementation_authority: NONE",
            "Output contract",
            "Quality gate",
            "Learning Log",
        )
        for token in required:
            self.assertIn(token, skill)
        self.assertLessEqual(len(skill.splitlines()), 150)
```

- [ ] **Step 2: 테스트를 실행해 SKILL.md 부재 실패를 확인한다**

Run: `python -m unittest tests.test_legacy_retention_archive_governance.LegacyRetentionArchiveGovernanceTests.test_shared_skill_contains_required_decisions_and_guards -v`

Expected: FAIL with `FileNotFoundError`.

- [ ] **Step 3: 150줄 이하 SKILL.md를 작성한다**

Frontmatter:

```yaml
---
name: governing-legacy-retention-and-archives
description: Use when superseded documents, inactive skills, historical evidence, generated derivatives, backup folders, blank placeholders, or merged branches must remain recoverable without retaining current implementation authority.
---
```

본문 필수 섹션:

```text
# Governing Legacy Retention and Archives
## Core principle
## When to use
## Required inputs
## Classification
## Workflow
## Content-type boundaries
## Output contract
## Quality gate
## Failure conditions
## Related skills
## Learning Log
```

Workflow는 다음 순서를 그대로 사용한다.

```text
inventory and authority check
→ unique material and consumer audit
→ one primary classification
→ retention location and metadata
→ remove active authority and default routing
→ update references, registry, aliases and manifests
→ validate content, rollback, cold start and secrets boundary
→ report PASS/PARTIAL/FAIL/NOT_RUN
```

- [ ] **Step 4: 상세 계약을 reference 파일로 작성한다**

`archive-contract.md`에는 다음을 포함한다.

- 8개 분류의 정확한 적용 조건.
- 문서, inactive Skill, test evidence, generated publication, code/runtime asset, secret, branch별 보존 방식.
- archive metadata 예시.
- branch `unique commits audited → PR merged/closed → optional tag → verify tag → delete when capability exists` 순서.
- `backup/`, `[백업]`, `archive/` 이름 자체는 권한 제거 증거가 아니라는 경고.
- active entrypoint·Registry·Documentation Map에서 archive가 current로 참조되면 FAIL.

- [ ] **Step 5: GREEN pressure scenarios를 실행하고 기록한다**

Task 1의 같은 입력을 Skill을 로드한 fresh context에서 실행한다. 각 record가 다음을 만족해야 PASS다.

```text
explicit classification
original content preserved
active authority removed
metadata/manifest required
secret archival rejected
unapproved deletion blocked
project adapter and validation named
```

실패한 시나리오의 실제 합리화만 Skill 또는 reference에 최소 추가한 뒤 재실행한다.

- [ ] **Step 6: Skill 테스트를 실행한다**

Run: `python -m unittest tests.test_legacy_retention_archive_governance -v`

Expected: Skill·Schema·template 관련 테스트 PASS, Registry 테스트는 아직 FAIL.

- [ ] **Step 7: 커밋한다**

```bash
git add skills/governing-legacy-retention-and-archives tests/test_legacy_retention_archive_governance.py
git commit -m "feat: add legacy retention archive governance skill"
```

### Task 4: Base Registry, Coverage, and Responsibility Boundaries

**Files:**
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_COVERAGE.json`
- Modify: `tools/check_skill_system_coverage.py`
- Modify: `tests/test_game_project_operating_system_structure.py`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/pruning-stale-and-nonfunctional-material/SKILL.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Registry entry ID: `governing-legacy-retention-and-archives`.
- Coverage responsibility ID: `legacy-retention-and-archive-governance`.

- [ ] **Step 1: Registry entry를 추가한다**

```json
{
  "skill_id": "governing-legacy-retention-and-archives",
  "layer": "foundation",
  "discipline": "project-operations-knowledge-governance",
  "path": "skills/governing-legacy-retention-and-archives/SKILL.md",
  "status": "ACTIVE",
  "load_by_default": false,
  "trigger_tags": [
    "legacy-retention",
    "archive-policy",
    "superseded-document",
    "obsolete-plan",
    "inactive-skill",
    "backup-folder",
    "blank-placeholder",
    "branch-retention",
    "archive-manifest",
    "historical-evidence"
  ],
  "use_when": [
    "구형 자료를 삭제하거나 현재 권한으로 유지하지 않고 원문·근거·호환성을 보존한 채 비정본 아카이브로 격리해야 한다."
  ],
  "do_not_use_when": [
    "현재 정본의 일반 편집, retention 판단이 없는 단순 stale-reference 검사, 비밀정보 보관 요청이다."
  ],
  "learning_log": "skills/SKILL_LEARNING_LOG.md",
  "review_triggers": [
    "빈 파일 퇴역",
    "metadata 없는 backup",
    "archive의 current 참조",
    "inactive Skill 직접 라우팅",
    "비밀정보 archive",
    "rollback ref 없는 이동·삭제"
  ],
  "last_reviewed_at": "2026-07-25",
  "last_reviewed_commit": "",
  "knowledge_state": "PATTERN"
}
```

구현 커밋 SHA가 정해진 뒤 `last_reviewed_commit`을 해당 SHA 또는 최종 PR head SHA로 갱신한다.

- [ ] **Step 2: Coverage 책임을 추가한다**

`skills/SKILL_COVERAGE.json`의 responsibilities에 다음 항목을 추가한다.

```json
{
  "id": "legacy-retention-and-archive-governance",
  "status": "COVERED",
  "skills": ["governing-legacy-retention-and-archives"]
}
```

- [ ] **Step 3: compact 검증 대상에 Skill을 추가한다**

`COMPACT_TARGETS` set에 `governing-legacy-retention-and-archives`를 추가한다.

- [ ] **Step 4: Base 구조 테스트를 갱신한다**

`test_required_operating_system_paths_exist`에 새 Skill·Schema·template·validator·test 경로를 추가한다. `self.assertEqual(len(registry["skills"]), 25)`를 `26`으로 바꾼다. 필수 ID subset에 새 Skill ID를 추가한다.

- [ ] **Step 5: 기존 Skill 책임 경계를 한 문단씩 갱신한다**

`managing-game-project-operating-system`의 `reconcile-legacy`에 다음 문장을 추가한다.

```markdown
보존 위치·archive metadata·비정본 권한 제거·branch/tag retention을 결정해야 하면 **REQUIRED SUB-SKILL:** Use `governing-legacy-retention-and-archives`.
```

`pruning-stale-and-nonfunctional-material`의 ARCHIVE 판정 뒤에 다음 문장을 추가한다.

```markdown
`ARCHIVE`로 판정한 자료의 보존 등급·metadata·manifest·active-authority 제거는 **REQUIRED SUB-SKILL:** Use `governing-legacy-retention-and-archives`.
```

- [ ] **Step 6: Learning Log를 기록한다**

실행일, RED 실패, GREEN 통과, 추가된 Skill ID, 프로젝트별 채택 예정과 기존 자료 미이동을 기록한다.

- [ ] **Step 7: Base 전체 검증을 실행한다**

```bash
python -m unittest tests.test_legacy_retention_archive_governance -v
python tools/check_skill_system_coverage.py
python -m unittest tests.test_skill_system_coverage -v
python -m unittest tests.test_game_project_operating_system_structure -v
python -m unittest discover -s tests -p "test_*.py" -v
python templates/project-operations/github/check_archive_governance.py \
  --root . \
  --adapter templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json \
  --manifest templates/project-operations/ARCHIVE_MANIFEST.json
```

Expected: 모두 exit code 0. Validator 출력은 `Archive governance validation passed`.

- [ ] **Step 8: 커밋한다**

```bash
git add skills/SKILL_REGISTRY.json skills/SKILL_COVERAGE.json tools/check_skill_system_coverage.py tests/test_game_project_operating_system_structure.py skills/managing-game-project-operating-system/SKILL.md skills/pruning-stale-and-nonfunctional-material/SKILL.md skills/SKILL_LEARNING_LOG.md
git commit -m "feat: register archive governance skill"
```

### Task 5: Base PR Finalization and Merge

**Files:**
- Modify: `docs/superpowers/specs/2026-07-25-legacy-retention-archive-governance-design.md`
- Modify: `docs/superpowers/plans/2026-07-25-legacy-retention-archive-governance-rollout.md`

**Interfaces:**
- Produces: exact merged Base commit SHA consumed by Tasks 6–9.

- [ ] **Step 1: 문서 상태를 구현 준비 상태로 갱신한다**

Spec status를 `DESIGN_APPROVED_IMPLEMENTED_IN_BASE_PR`로, plan의 Base task 체크박스를 실제 결과에 맞게 갱신한다. 실행하지 않은 pressure scenario나 CI는 `NOT_RUN`으로 남긴다.

- [ ] **Step 2: 전체 diff와 placeholder를 검사한다**

```bash
git diff --check
grep -RInE "TBD|TODO|fill in|작성 필요" \
  skills/governing-legacy-retention-and-archives \
  schemas/archive-*-v1.schema.json \
  templates/project-operations/ARCHIVE_* \
  templates/project-operations/github/check_archive_governance.py
```

Expected: `git diff --check` exit 0, grep 결과 없음.

- [ ] **Step 3: Draft PR #38 설명을 구현 범위와 증거로 갱신한다**

PR body에 다음을 포함한다.

```text
RED baseline evidence
GREEN pressure results
Base test commands and exit codes
changed paths
no legacy artifacts moved/deleted
no secrets archived
project rollout blocked until Base merge SHA exists
```

- [ ] **Step 4: CI와 review thread를 확인한다**

Required checks가 모두 success이고 unresolved review thread가 0인지 확인한다. workflow 존재만으로 PASS 처리하지 않는다.

- [ ] **Step 5: 사용자 또는 승인 계약에 따라 Ready·squash merge한다**

병합 직전 expected head SHA를 고정한다. 병합 뒤 `main`에서 Skill, Registry, Schema, template와 tests를 재조회한다.

- [ ] **Step 6: Base merged SHA를 기록한다**

이후 Task에서 `<BASE_MERGED_SHA>` 대신 실제 40자리 SHA를 사용한다. 문서나 JSON에 placeholder를 남기지 않는다.

### Task 6: Omenward Registry v4 Adapter PR

**Files:**
- Create: `skills/foundation/governing-legacy-retention-and-archives/SKILL.md`
- Create: `docs/archive/README.md`
- Create: `docs/archive/MANIFEST.json`
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `tests/python/test_archive_retention_governance.py`
- Modify: `docs/base/SKILL_REGISTRY.json`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `tools/validate_skill_system.py`
- Modify: `tests/python/test_skill_system_v4.py`
- Modify: `.github/workflows/validate-skill-system.yml`

**Interfaces:**
- Local Skill ID: `foundation.legacy-retention-archives`.
- Base Skill ID: `governing-legacy-retention-and-archives`.
- Adapter path: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`.
- Manifest path: `docs/archive/MANIFEST.json`.

- [ ] **Step 1: 최신 Omenward main에서 독립 브랜치를 만든다**

```bash
git fetch origin
git switch -c gpt/adopt-archive-governance-omenward origin/main
```

Base 병합 SHA를 확인한 뒤에만 계속한다.

- [ ] **Step 2: failing tests를 작성한다**

`tests/python/test_archive_retention_governance.py`에 다음 테스트를 작성한다.

```python
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class ArchiveRetentionGovernanceTests(unittest.TestCase):
    def test_archive_framework_exists_and_is_non_authoritative(self):
        adapter = json.loads((ROOT / "docs/archive/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs/archive/MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual("governing-legacy-retention-and-archives", adapter["base"]["skill_id"])
        self.assertFalse(adapter["policies"]["blank_placeholders_allowed"])
        self.assertFalse(adapter["policies"]["secrets_may_be_archived"])
        self.assertEqual([], manifest["records"])

    def test_v2_canon_roots_are_active_and_archive_is_not(self):
        adapter = json.loads((ROOT / "docs/archive/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
        roots = adapter["paths"]["active_canon_roots"]
        self.assertIn("docs/design", roots)
        self.assertNotIn("docs/archive", roots)
```

`test_skill_system_v4.py`에 route test를 추가한다.

```python
def test_archive_policy_routes_to_foundation_adapter(self):
    registry = json.loads((ROOT / "docs/base/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
    ids = [item["id"] for item in route.route("구형 기획서를 내용 비우지 않고 백업 아카이브", registry)["skills"]]
    self.assertIn("foundation.legacy-retention-archives", ids)
```

- [ ] **Step 3: RED를 확인한다**

```bash
python -m unittest tests.python.test_archive_retention_governance -v
python -m unittest tests.python.test_skill_system_v4 -v
```

Expected: adapter 파일 부재와 route ID 부재로 FAIL.

- [ ] **Step 4: 얇은 Foundation adapter Skill을 작성한다**

본문은 80줄 이하이며 Base workflow를 복제하지 않는다. 다음 항목만 둔다.

```text
Base repository and exact commit
Base skill ID
Omenward active canon roots
V2 decision ledger priority
inactive compatibility Skill policy
CI evidence roots
project validation commands
REQUIRED SUB-SKILL marker to load Base skill
```

- [ ] **Step 5: Registry v4에 활성 entry를 추가한다**

```json
{
  "id": "foundation.legacy-retention-archives",
  "category": "foundation",
  "path": "skills/foundation/governing-legacy-retention-and-archives/SKILL.md",
  "triggers": ["아카이브", "백업", "구형 문서", "내용 비우기", "inactive skill", "branch retention", "archive manifest"],
  "not_use_when": ["현재 V2 정본의 일반 편집", "비밀정보 보관"],
  "depends_on": ["foundation.project-operating-system"],
  "priority": 88,
  "status": "active",
  "modes": ["PLAN", "BUILD", "REVIEW"],
  "source_base_skill": "governing-legacy-retention-and-archives"
}
```

활성 합계 관련 문서를 12→13으로 갱신하되 validator에 고정 개수를 새로 하드코딩하지 않는다.

- [ ] **Step 6: Omenward adapter를 작성한다**

```json
{
  "schema_version": 1,
  "adapter_role": "omenward-archive-retention-adapter",
  "base": {
    "repository": "alsdmlals4-eng/Base",
    "commit": "<BASE_MERGED_SHA>",
    "skill_id": "governing-legacy-retention-and-archives"
  },
  "paths": {
    "active_canon_roots": ["docs/design", "docs/PROJECT_CORE.md", "docs/OMENWARD_GAME_DESIGN.md"],
    "archive_root": "docs/archive",
    "manifest": "docs/archive/MANIFEST.json",
    "archive_readme": "docs/archive/README.md",
    "protected_evidence_roots": ["docs/evidence", "docs/qa", "tests", ".github/workflows"]
  },
  "policies": {
    "preserve_original_content": true,
    "blank_placeholders_allowed": false,
    "secrets_may_be_archived": false,
    "default_active_authority": false,
    "default_implementation_authority": "NONE"
  },
  "validation": {
    "commands": [
      "python tools/validate_skill_system.py",
      "python -m unittest tests.python.test_archive_retention_governance -v",
      "python -m unittest discover -s tests/python -p 'test_skill_*.py' -v"
    ]
  }
}
```

실제 파일에는 `<BASE_MERGED_SHA>`를 사용하지 않고 Task 5의 SHA를 넣는다.

- [ ] **Step 7: validator를 연결한다**

`tools/validate_skill_system.py`에 `validate_archive_governance(root) -> list[str]`를 추가하거나 Base template의 핵심 검사를 로컬 함수로 채택한다. remote Base 파일을 runtime에 다운로드하지 않는다. `validate()`의 error list에 archive errors를 합친다.

- [ ] **Step 8: 전체 Skill CI를 실행한다**

```bash
python tools/validate_skill_system.py
python -m unittest tests.python.test_archive_retention_governance -v
python -m unittest tests.python.test_skill_system_v4 -v
python -m unittest discover -s tests/python -p "test_skill_*.py" -v
python tools/route_skills.py --request "구형 기획서를 내용 비우지 않고 백업 아카이브"
git diff --check
```

Expected: 모두 exit 0, route 결과에 `foundation.legacy-retention-archives` 포함.

- [ ] **Step 9: PR을 열고 CI success 뒤 squash merge한다**

PR body에 `existing legacy moved: NO`, `product implementation changed: NO`, `V2 canon changed: NO`를 명시한다.

### Task 7: Urban Legend Registry v4 Base Index Adoption PR

**Files:** 위 File Structure의 Urban Legend 목록.

**Interfaces:**
- Shared route ID: `governing-legacy-retention-and-archives`.
- Project adapter role: `urban-legend-archive-retention-adapter`.

- [ ] **Step 1: 최신 main에서 브랜치를 만든다**

```bash
git fetch origin
git switch -c gpt/adopt-archive-governance-urban-legend origin/main
```

- [ ] **Step 2: failing tests를 추가한다**

`tests/test_archive_retention_governance.py`는 Base SHA, Skill ID, `docs/archive` 비정본, empty records를 검사한다. `tests/test_active_document_references.py`에는 다음을 추가한다.

```python
def test_archive_documents_are_not_current_routed_documents(self) -> None:
    archive_root = ROOT / "docs/archive"
    self.assertTrue(archive_root.is_dir())
    for path in ALL_ROUTED_DOCS:
        self.assertFalse(path.is_relative_to(archive_root))
```

- [ ] **Step 3: RED를 확인한다**

```bash
python -m unittest tests.test_archive_retention_governance -v
python -m unittest tests.test_active_document_references.ActiveDocumentReferenceTests.test_archive_documents_are_not_current_routed_documents -v
```

Expected: archive framework 부재로 FAIL.

- [ ] **Step 4: Base index와 project Registry를 갱신한다**

`skills/BASE_SKILL_INDEX.json`에 Base merged SHA와 새 Skill entry를 반영한다. `skills/SKILL_REGISTRY.json`의 `base.commit`을 같은 SHA로 바꾸고 routing example을 추가한다.

```json
{
  "tags": ["archive-policy", "superseded-document"],
  "expected_primary": null,
  "expected_local": null,
  "expected_support": ["governing-legacy-retention-and-archives"]
}
```

- [ ] **Step 5: path adapter와 archive adapter를 작성한다**

`skills/PROJECT_PATH_ADAPTER.json`의 `role_bindings`에 다음을 추가한다.

```json
"archive_retention_adapter": "docs/archive/ARCHIVE_RETENTION_ADAPTER.json",
"archive_manifest": "docs/archive/MANIFEST.json",
"archive_readme": "docs/archive/README.md"
```

`validation.tests`에 `tests/test_archive_retention_governance.py`를 추가한다.

- [ ] **Step 6: validator와 workflow를 연결한다**

`tools/check_archive_governance.py`는 Base template과 같은 공개 함수 및 exit contract를 사용한다. workflow에 아래 command를 추가한다.

```bash
python tools/check_archive_governance.py
python -m unittest tests.test_archive_retention_governance -v
```

- [ ] **Step 7: 전체 프로젝트 검증을 실행한다**

```bash
python tools/check_archive_governance.py
python -m unittest tests.test_archive_retention_governance -v
python -m unittest tests.test_base_operating_sync -v
python -m unittest tests.test_skill_package_integrity -v
python -m unittest tests.test_active_document_references -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 모두 exit 0.

- [ ] **Step 8: PR을 열고 독립 CI success 뒤 squash merge한다**

현재 게임 정본과 연간 설계 baseline에 변경이 없음을 PR body에 명시한다.

### Task 8: Ten Paces Registry v3 Shared Route Adoption PR

**Files:** 위 File Structure의 Ten Paces 목록.

**Interfaces:**
- Registry key: `base_integration.shared_skill_routes.legacy_retention`.
- Value: `governing-legacy-retention-and-archives`.

- [ ] **Step 1: 최신 main에서 브랜치를 만든다**

```bash
git fetch origin
git switch -c gpt/adopt-archive-governance-ten-paces origin/main
```

- [ ] **Step 2: failing governance tests를 작성한다**

`tests/test_project_governance.py`에 다음을 추가한다.

```python
def test_archive_governance_base_route_and_adapter(self) -> None:
    registry = json.loads((ROOT / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
    route = registry["base_integration"]["shared_skill_routes"]
    self.assertEqual("governing-legacy-retention-and-archives", route["legacy_retention"])
    adapter = json.loads((ROOT / "[기획서]/00_프로젝트_허브/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
    self.assertEqual(registry["base_integration"]["commit"], adapter["base"]["commit"])
    self.assertFalse(adapter["policies"]["blank_placeholders_allowed"])
```

- [ ] **Step 3: RED를 확인한다**

Run: `python -m unittest tests.test_project_governance.ProjectGovernanceTests.test_archive_governance_base_route_and_adapter -v`

Expected: missing route 또는 adapter로 FAIL.

- [ ] **Step 4: Registry와 freshness config를 갱신한다**

Registry Base commit을 actual Base merged SHA로 갱신하고 shared route를 추가한다. `.github/reference-freshness.json`의 `expected_base_commit`과 `expected_base_skill_ids`에도 같은 SHA와 Skill ID를 추가한다. 기존 4개 project discipline Skill 수는 변경하지 않는다.

- [ ] **Step 5: project adapter와 archive framework를 작성한다**

`active_canon_roots`는 `[기획서]/00_프로젝트_허브`, `docs/02_COMBAT_RULES.md`, `docs/05_COMBAT_POC_SPEC.md`, `docs/09_COMBAT_SYSTEM_ARCHITECTURE.md`를 포함한다. Archive root는 `docs/archive`로 둔다.

- [ ] **Step 6: operating checker에 필수 경로를 추가한다**

`tools/check_project_operating_system.py`의 required path 계약에 archive README, Manifest와 project hub adapter를 추가한다.

- [ ] **Step 7: 전체 governance 검증을 실행한다**

```bash
python tools/check_archive_governance.py
python tools/check_project_operating_system.py
python tools/check_canonical_reference_freshness.py
python tools/check_skill_package_integrity.py
python -m unittest tests.test_project_governance -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 모두 exit 0; combat board schema와 current product baseline은 변경되지 않는다.

- [ ] **Step 8: PR을 열고 독립 CI success 뒤 squash merge한다**

PR body에 Registry schema generation unchanged, product data unchanged를 명시한다.

### Task 9: Blacksmith Registry v2 Adoption Profile PR

**Files:** 위 File Structure의 Blacksmith 목록.

**Interfaces:**
- Capability Base ID: `governing-legacy-retention-and-archives`.
- Disposition: `ADAPT`.
- Local owner: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`.

- [ ] **Step 1: 최신 main에서 브랜치를 만든다**

```bash
git fetch origin
git switch -c gpt/adopt-archive-governance-blacksmith origin/main
```

- [ ] **Step 2: failing unittest를 작성한다**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArchiveRetentionGovernanceTests(unittest.TestCase):
    def test_base_adoption_profile_contains_archive_governance(self) -> None:
        profile = json.loads((ROOT / "docs/BASE_ADOPTION_PROFILE.json").read_text(encoding="utf-8"))
        by_id = {item["base_skill_id"]: item for item in profile["capabilities"]}
        item = by_id["governing-legacy-retention-and-archives"]
        self.assertEqual("ADAPT", item["disposition"])
        self.assertEqual("docs/archive/ARCHIVE_RETENTION_ADAPTER.json", item["local_owner"])

    def test_archive_framework_is_non_authoritative(self) -> None:
        adapter = json.loads((ROOT / "docs/archive/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs/archive/MANIFEST.json").read_text(encoding="utf-8"))
        self.assertFalse(adapter["policies"]["blank_placeholders_allowed"])
        self.assertFalse(adapter["policies"]["secrets_may_be_archived"])
        self.assertEqual([], manifest["records"])
```

- [ ] **Step 3: RED를 확인한다**

Run: `python -m unittest tests.test_archive_retention_governance -v`

Expected: profile capability와 archive files 부재로 FAIL.

- [ ] **Step 4: adoption profile을 갱신한다**

Base SHA를 actual merged SHA로 갱신하고 capabilities에 아래 entry를 추가한다.

```json
{
  "base_skill_id": "governing-legacy-retention-and-archives",
  "disposition": "ADAPT",
  "local_owner": "docs/archive/ARCHIVE_RETENTION_ADAPTER.json",
  "local_skill_id": null,
  "local_modes": ["classify-retention", "archive-with-metadata", "verify-non-authority"],
  "activation": "구형 문서·Skill·증거·생성물·병합 브랜치를 원문과 복구 근거를 보존한 채 현재 권한에서 격리할 때"
}
```

`project_skill_count`는 3으로 유지한다.

- [ ] **Step 5: archive adapter를 작성한다**

`active_canon_roots`에는 `[기획서]/00_프로젝트_허브`, `[기획서]/01_통합_게임_기획`, `skills/game-design`, `skills/engineering`, `skills/qa`를 둔다. Archive root는 `docs/archive`다.

- [ ] **Step 6: audit tool을 갱신한다**

`tools/audit_project_operating_system.py`가 다음 오류를 검출하도록 한다.

```text
missing archive capability
base commit mismatch
missing adapter/readme/manifest
blank_placeholders_allowed != false
secrets_may_be_archived != false
archive root included in active canon roots
manifest records not list
```

- [ ] **Step 7: audit 문서와 tests README를 갱신한다**

`docs/BASE_ADOPTION_AUDIT.md`에 capability owner, exact Base SHA, `existing legacy moved: NO`, 검증 command를 기록한다. `tests/README.md`에 다음을 추가한다.

```bash
python -m unittest tests.test_archive_retention_governance -v
```

- [ ] **Step 8: 전체 검증을 실행한다**

```bash
python tools/audit_project_operating_system.py
python -m unittest tests.test_archive_retention_governance -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 모두 exit 0; project specialist Skill 수는 3으로 유지된다.

- [ ] **Step 9: PR을 열고 독립 CI success 뒤 squash merge한다**

Registry v2 자체를 v4로 마이그레이션하지 않았음을 PR body에 명시한다.

### Task 10: Cross-Repository Final Verification and Rollout Record

**Files:**
- Create in Base: `docs/audits/2026-07-25-legacy-retention-archive-governance-rollout.md`
- Modify in Base: `skills/SKILL_LEARNING_LOG.md`
- Modify in Base: `docs/superpowers/plans/2026-07-25-legacy-retention-archive-governance-rollout.md`

**Interfaces:**
- Consumes: Base와 네 프로젝트의 merge SHA, CI run ID, validation command 결과.
- Produces: cross-repository rollout evidence without claiming legacy migration.

- [ ] **Step 1: 각 저장소 main 상태를 다시 조회한다**

기록 항목:

```text
repository
main_sha
adopted_base_sha
archive_adapter_path
archive_manifest_path
routing/adoption mechanism
ci_run_id
ci_conclusion
open_prs
unresolved_review_threads
```

- [ ] **Step 2: Base pin 일치 여부를 확인한다**

네 프로젝트의 adapter 또는 adoption profile이 Task 5의 동일한 Base merge SHA를 가리켜야 한다. 다른 SHA가 있으면 rollout status는 FAIL이다.

- [ ] **Step 3: current authority 오염 여부를 확인한다**

각 프로젝트의 START_HERE·Documentation Map·Registry에서 `docs/archive` 또는 archive manifest가 현재 제품 정본으로 표기되지 않았는지 검사한다. Archive 경로를 “보존 정책 위치”로 링크하는 것은 허용하되 “current canon”으로 표기하면 FAIL이다.

- [ ] **Step 4: 기존 자료 무변경을 검증한다**

각 프로젝트 PR diff에서 다음을 기록한다.

```text
legacy files moved: 0
legacy files deleted: 0
legacy file bodies blanked: 0
product code/data changes: 0
archive framework files added: expected paths only
```

- [ ] **Step 5: rollout audit를 작성한다**

각 저장소 판정을 `PASS / PARTIAL / FAIL / NOT_RUN`으로 작성하고 raw CI URL 대신 PR·run ID·commit SHA를 기록한다. branch deletion capability가 없거나 사용하지 않은 것은 `NOT_RUN`, 실패가 아니다.

- [ ] **Step 6: Learning Log와 plan 체크박스를 갱신한다**

실제 검증된 항목만 체크한다. 기존 자료 마이그레이션, archive tag 생성과 branch 삭제는 Deferred로 남긴다.

- [ ] **Step 7: Base audit-only PR을 열고 검증 뒤 squash merge한다**

이 PR은 rollout 증거와 Learning Log만 변경한다. Skill·Schema·프로젝트 정본을 다시 변경하지 않는다.

---

## Self-Review Result

- **Spec coverage:** 원문 보존, 빈 파일 금지, 8개 분류, metadata·manifest, inactive Skill, generated derivative, secrets, branch/tag, project adapters, Skill TDD, automated validation, 5개 독립 PR과 deferred migration이 Tasks 1–10에 모두 매핑된다.
- **Placeholder scan:** 실행 계획의 예시 `<BASE_MERGED_SHA>`는 구현 파일에 남기지 말아야 할 치환 표식으로 명시됐으며 Task 5에서 실제 SHA를 생성한다. `TBD`, `TODO`, `작성 필요`, `implement later`는 산출물에 허용하지 않는다.
- **Type consistency:** 공용 validator signature는 `validate_archive_governance(root: Path, adapter_path: Path, manifest_path: Path) -> list[str]`; 모든 프로젝트는 동일한 adapter와 manifest field명을 사용한다.
- **Scope:** 기존 구형 자료 이동·삭제, tag/branch 삭제와 history rewrite는 명시적으로 제외됐다.
