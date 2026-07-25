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
- 미확정 값은 빈 문자열 대신 `UNKNOWN`과 차단 사유를 사용한다.
- 이 롤아웃은 branch/tag 삭제, Git history rewrite, 대형 바이너리 저장소 설계와 기존 구형 자료 일괄 마이그레이션을 포함하지 않는다.
- Base PR이 먼저 병합되어야 하며, 네 프로젝트 PR은 Task 5가 출력한 `base_merged_sha`를 pin한다.
- 프로젝트 PR은 서로 독립적으로 검증하고 병합한다.
- 모든 검증 결과는 `PASS / PARTIAL / FAIL / NOT_RUN`으로 구분하며 파일 존재만으로 강제 성공을 주장하지 않는다.

---

## File Structure

### Base

- Create: `skills/governing-legacy-retention-and-archives/SKILL.md`
- Create: `skills/governing-legacy-retention-and-archives/references/archive-contract.md`
- Create: `skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md`
- Create: `schemas/archive-retention-adapter-v1.schema.json`
- Create: `schemas/archive-manifest-v1.schema.json`
- Create: `templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `templates/project-operations/ARCHIVE_MANIFEST.json`
- Create: `templates/project-operations/ARCHIVE_README.md`
- Create: `templates/project-operations/github/check_archive_governance.py`
- Create: `tests/test_legacy_retention_archive_governance.py`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_COVERAGE.json`
- Modify: `tools/check_skill_system_coverage.py`
- Modify: `tests/test_game_project_operating_system_structure.py`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/pruning-stale-and-nonfunctional-material/SKILL.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

### Omenward

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

### Urban Legend

- Create: `docs/archive/README.md`
- Create: `docs/archive/MANIFEST.json`
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `tools/check_archive_governance.py`
- Create: `tests/test_archive_retention_governance.py`
- Modify: `skills/BASE_SKILL_INDEX.json`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/PROJECT_PATH_ADAPTER.json`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `tests/test_active_document_references.py`
- Modify: `tests/test_base_operating_sync.py`
- Modify: `.github/workflows/validate-base-operating-sync.yml`

### Ten Paces Hidden Moves

- Create: `docs/archive/README.md`
- Create: `docs/archive/MANIFEST.json`
- Create: `[기획서]/00_프로젝트_허브/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `tools/check_archive_governance.py`
- Modify: `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `.github/reference-freshness.json`
- Modify: `tests/test_project_governance.py`
- Modify: `tools/check_project_operating_system.py`

### Blacksmith

- Create: `docs/archive/README.md`
- Create: `docs/archive/MANIFEST.json`
- Create: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`
- Create: `tests/test_archive_retention_governance.py`
- Modify: `docs/BASE_ADOPTION_PROFILE.json`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `docs/BASE_ADOPTION_AUDIT.md`
- Modify: `tools/audit_project_operating_system.py`
- Modify: `tests/README.md`

---

### Task 1: Base RED Pressure Baseline and Failing Contract Tests

**Files:**
- Create: `skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md`
- Create: `tests/test_legacy_retention_archive_governance.py`

**Interfaces:**
- Consumes: 승인된 설계 문서의 분류값과 Global Constraints.
- Produces: 이후 Skill·Schema·validator가 만족해야 하는 실패 테스트와 pressure record 형식.

- [ ] **Step 1: pressure record와 6개 baseline scenario를 작성한다**

Record fields:

```text
scenario_id, skill_loaded, pressure, input, observed_decision,
observed_rationalization, required_classification,
preserved_original_content, active_authority_removed,
destructive_action_blocked, result
```

Scenarios:

```text
RED-BLANK-001: 구형 문서 경로는 남기고 내용을 전부 비우라는 요청
RED-BACKUP-002: 200개 파일을 metadata 없이 backup 폴더에 복사하라는 시간 압박
RED-SECRET-003: 노출 API token을 기록 보존 목적으로 archive하라는 요청
RED-SKILL-004: inactive Skill을 Registry 갱신 없이 이동하라는 요청
RED-BRANCH-005: unique commit 감사 없이 merged branch를 삭제하라는 요청
RED-COLDSTART-006: archive 문서를 START_HERE 기본 읽기에 유지하라는 요청
```

- [ ] **Step 2: Skill과 archive contract가 아직 없어서 실패하는 unittest를 작성한다**

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

- [ ] **Step 3: RED를 확인한다**

Run: `python -m unittest tests.test_legacy_retention_archive_governance -v`

Expected: missing files와 missing Registry ID로 FAIL.

- [ ] **Step 4: Skill을 로드하지 않은 fresh context에서 6개 scenario를 실행한다**

최소 한 scenario가 원문 비움, metadata 없는 backup, secret archive, Registry 없는 Skill 이동, rollback 없는 branch 삭제 또는 archive current-reading 유지 중 하나를 선택해야 한다. 관찰된 합리화를 그대로 기록한다. 모두 안전하게 처리되면 Skill 범위를 재검토하고 구현을 중지한다.

- [ ] **Step 5: RED 증거를 커밋한다**

```bash
git add skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md tests/test_legacy_retention_archive_governance.py
git commit -m "test: capture legacy retention archive baseline"
```

### Task 2: Base Archive Schemas, Templates, and Validator

**Files:** Base의 두 Schema, 세 template, validator와 test 파일.

**Interfaces:**
- Produces: `validate_archive_governance(root: Path, adapter_path: Path, manifest_path: Path) -> list[str]`.

- [ ] **Step 1: JSON Schema validation test를 먼저 추가하고 FileNotFoundError를 확인한다**

두 template을 `jsonschema.Draft202012Validator`로 각각 검증한다.

- [ ] **Step 2: adapter Schema를 구현한다**

Required root fields:

```text
schema_version, adapter_role, base, paths, policies, validation
```

Fixed policy values:

```text
preserve_original_content = true
blank_placeholders_allowed = false
secrets_may_be_archived = false
default_active_authority = false
default_implementation_authority = NONE
```

`base.commit`은 40자리 lowercase hex, `base.skill_id`는 `governing-legacy-retention-and-archives`로 제한한다.

- [ ] **Step 3: Manifest Schema를 구현한다**

Root:

```json
{"schema_version": 1, "manifest_role": "project-archive-retention-index", "records": []}
```

Record required fields:

```text
archive_id, classification, original_path, current_path, content_sha256,
archived_at, superseded_by, reason, active_authority,
implementation_authority, compatibility_consumers, rollback_ref,
validation_status
```

Classification은 Global Constraints의 8개 값, `content_sha256`은 64자리 lowercase hex, `validation_status`는 `PASS/PARTIAL/FAIL/NOT_RUN`만 허용한다.

- [ ] **Step 4: 세 template을 작성한다**

Archive README는 현재 정본 아님, 구현 권한 없음, 원문 비우기 금지, replacement 조회, secret 금지, rollback 기반 복구를 명시한다. Manifest는 유효한 빈 records array로 시작한다.

- [ ] **Step 5: validator를 구현한다**

Validation order:

```text
JSON parse
→ Schema validation
→ archive root/readme/manifest existence
→ current_path uniqueness
→ superseded_by target existence or external prefix
→ archived Markdown body non-empty beyond metadata
→ active canon roots outside archive root
→ deterministic sorted errors
```

- [ ] **Step 6: tests를 실행한다**

Run: `python -m unittest tests.test_legacy_retention_archive_governance -v`

Expected: Schema와 template tests PASS; Skill·Registry tests는 아직 FAIL.

- [ ] **Step 7: 커밋한다**

```bash
git add schemas/archive-retention-adapter-v1.schema.json schemas/archive-manifest-v1.schema.json templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json templates/project-operations/ARCHIVE_MANIFEST.json templates/project-operations/ARCHIVE_README.md templates/project-operations/github/check_archive_governance.py tests/test_legacy_retention_archive_governance.py
git commit -m "feat: add archive retention schemas and templates"
```

### Task 3: Base Shared Skill GREEN Implementation

**Files:** 새 Skill 본문, archive contract reference, pressure scenario record와 tests.

**Interfaces:**
- Skill ID: `governing-legacy-retention-and-archives`.

- [ ] **Step 1: 150줄 이하 Skill shape test를 추가하고 실패를 확인한다**

Required tokens:

```text
name: governing-legacy-retention-and-archives
CURRENT_AUTHORITY
COMPATIBILITY_ONLY
ARCHIVE_HISTORY
EVIDENCE_RETENTION
GENERATED_DERIVATIVE
DELETE_PROHIBITED_SECRET
DELETE_APPROVED
KEEP_UNRESOLVED
원문을 비우지 않는다
active_authority: false
implementation_authority: NONE
Output contract
Quality gate
Learning Log
```

- [ ] **Step 2: SKILL.md를 작성한다**

Frontmatter:

```yaml
---
name: governing-legacy-retention-and-archives
description: Use when superseded documents, inactive skills, historical evidence, generated derivatives, backup folders, blank placeholders, or merged branches must remain recoverable without retaining current implementation authority.
---
```

Required sections:

```text
Core principle
When to use
Required inputs
Classification
Workflow
Content-type boundaries
Output contract
Quality gate
Failure conditions
Related skills
Learning Log
```

Workflow:

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

- [ ] **Step 3: `archive-contract.md`를 작성한다**

문서, inactive Skill, test evidence, generated publication, code/runtime asset, secret, branch의 서로 다른 보존 방식과 metadata 예시를 포함한다. `backup`, `[백업]`, `archive`라는 폴더명만으로 권한 제거가 증명되지 않음을 명시한다.

- [ ] **Step 4: 동일 pressure scenarios를 Skill을 로드한 fresh context에서 실행한다**

PASS 조건:

```text
explicit classification
original content preserved
active authority removed
metadata and manifest required
secret archival rejected
unapproved deletion blocked
project adapter and validation named
```

- [ ] **Step 5: tests를 실행하고 커밋한다**

```bash
python -m unittest tests.test_legacy_retention_archive_governance -v
git add skills/governing-legacy-retention-and-archives tests/test_legacy_retention_archive_governance.py
git commit -m "feat: add legacy retention archive governance skill"
```

### Task 4: Base Registry, Coverage, and Responsibility Boundaries

**Files:** Base Registry, coverage, compact checker, operating-system tests, two related Skills와 Learning Log.

**Interfaces:**
- Registry ID: `governing-legacy-retention-and-archives`.
- Coverage responsibility ID: `legacy-retention-and-archive-governance`.

- [ ] **Step 1: Registry entry를 추가한다**

Entry values:

```text
layer = foundation
discipline = project-operations-knowledge-governance
path = skills/governing-legacy-retention-and-archives/SKILL.md
status = ACTIVE
load_by_default = false
trigger_tags = legacy-retention, archive-policy, superseded-document,
               obsolete-plan, inactive-skill, backup-folder,
               blank-placeholder, branch-retention, archive-manifest,
               historical-evidence
knowledge_state = PATTERN
```

- [ ] **Step 2: Coverage responsibility와 compact target을 추가한다**

```json
{"id": "legacy-retention-and-archive-governance", "status": "COVERED", "skills": ["governing-legacy-retention-and-archives"]}
```

- [ ] **Step 3: Base structure test를 갱신한다**

Required paths에 새 Skill, Schema, templates, validator와 test를 추가한다. Registry Skill count assertion은 25에서 26으로 바꾼다. 필수 ID subset에 새 ID를 추가한다.

- [ ] **Step 4: 기존 두 Skill의 경계를 갱신한다**

`managing-game-project-operating-system`는 보존 위치·metadata·branch/tag retention 결정 시 새 Skill을 REQUIRED SUB-SKILL로 호출한다. `pruning-stale-and-nonfunctional-material`는 ARCHIVE 판정 뒤 보존 계약을 새 Skill에 위임한다.

- [ ] **Step 5: Base 전체 검증을 실행한다**

```bash
python -m unittest tests.test_legacy_retention_archive_governance -v
python tools/check_skill_system_coverage.py
python -m unittest tests.test_skill_system_coverage -v
python -m unittest tests.test_game_project_operating_system_structure -v
python -m unittest discover -s tests -p "test_*.py" -v
python templates/project-operations/github/check_archive_governance.py --root . --adapter templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json --manifest templates/project-operations/ARCHIVE_MANIFEST.json
git diff --check
```

Expected: 모두 exit 0.

- [ ] **Step 6: 커밋한다**

```bash
git add skills/SKILL_REGISTRY.json skills/SKILL_COVERAGE.json tools/check_skill_system_coverage.py tests/test_game_project_operating_system_structure.py skills/managing-game-project-operating-system/SKILL.md skills/pruning-stale-and-nonfunctional-material/SKILL.md skills/SKILL_LEARNING_LOG.md
git commit -m "feat: register archive governance skill"
```

### Task 5: Base PR Finalization and Merge

**Files:** 승인 설계 문서와 이 rollout plan.

**Interfaces:**
- Produces: `base_merged_sha`, 정확한 40자리 Base main merge commit.

- [ ] **Step 1: spec와 plan의 실행 상태를 실제 증거에 맞게 갱신한다**

실행하지 않은 pressure scenario나 CI는 `NOT_RUN`으로 남긴다.

- [ ] **Step 2: diff, unresolved markers, review thread와 CI를 검사한다**

```bash
git diff --check
```

승인된 산출물에 미확정 작업 표식, 빈 필드 또는 example SHA가 남아 있으면 병합하지 않는다.

- [ ] **Step 3: PR #38 body를 RED/GREEN evidence, test commands, no-migration scope로 갱신한다**

- [ ] **Step 4: required checks success와 unresolved review thread 0을 확인한다**

- [ ] **Step 5: expected head SHA를 고정해 Ready 전환 후 squash merge한다**

- [ ] **Step 6: merge 결과의 SHA를 `base_merged_sha`로 기록한다**

Tasks 6–9는 해당 값을 각 프로젝트 파일에 실제 문자열로 기록하며 변수명이나 example SHA를 파일에 남기지 않는다.

### Task 6: Omenward Registry v4 Adapter PR

**Files:** Omenward File Structure 목록.

**Interfaces:**
- Local ID: `foundation.legacy-retention-archives`.
- Base ID: `governing-legacy-retention-and-archives`.

- [ ] **Step 1: 최신 main에서 `gpt/adopt-archive-governance-omenward` 브랜치를 만든다**

- [ ] **Step 2: adapter·manifest·V2 canon boundary와 routing failing tests를 작성하고 FAIL을 확인한다**

Routing assertion:

```python
registry = json.loads((ROOT / "docs/base/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
ids = [item["id"] for item in route.route("구형 기획서를 내용 비우지 않고 백업 아카이브", registry)["skills"]]
self.assertIn("foundation.legacy-retention-archives", ids)
```

- [ ] **Step 3: 80줄 이하의 얇은 local adapter Skill을 작성한다**

Base repository, `base_merged_sha`, Base Skill ID, V2 canon roots, inactive Skill policy, CI evidence roots와 validation commands만 둔다. Base workflow 본문은 복제하지 않는다.

- [ ] **Step 4: Registry v4에 활성 entry를 추가한다**

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

활성 합계 표기는 12에서 13으로 바꾸되 validator에 고정 개수를 추가하지 않는다.

- [ ] **Step 5: Omenward adapter를 작성한다**

Active roots:

```text
docs/design
docs/PROJECT_CORE.md
docs/OMENWARD_GAME_DESIGN.md
```

Protected evidence roots:

```text
docs/evidence
docs/qa
tests
.github/workflows
```

Base commit은 `base_merged_sha` 실제 값이다.

- [ ] **Step 6: local validator 연결 후 전체 Skill suite를 실행한다**

```bash
python tools/validate_skill_system.py
python -m unittest tests.python.test_archive_retention_governance -v
python -m unittest tests.python.test_skill_system_v4 -v
python -m unittest discover -s tests/python -p "test_skill_*.py" -v
python tools/route_skills.py --request "구형 기획서를 내용 비우지 않고 백업 아카이브"
git diff --check
```

Expected: 모두 exit 0, route 결과에 local ID 포함.

- [ ] **Step 7: PR을 열고 CI success 뒤 squash merge한다**

PR body flags:

```text
existing legacy moved: NO
product implementation changed: NO
V2 canon changed: NO
```

### Task 7: Urban Legend Registry v4 Base Index Adoption PR

**Files:** Urban Legend File Structure 목록.

**Interfaces:**
- Shared route ID: `governing-legacy-retention-and-archives`.

- [ ] **Step 1: 최신 main에서 `gpt/adopt-archive-governance-urban-legend` 브랜치를 만든다**

- [ ] **Step 2: archive framework와 current-routed-doc exclusion failing tests를 작성하고 FAIL을 확인한다**

```python
def test_archive_documents_are_not_current_routed_documents(self) -> None:
    archive_root = ROOT / "docs/archive"
    self.assertTrue(archive_root.is_dir())
    for path in ALL_ROUTED_DOCS:
        self.assertFalse(path.is_relative_to(archive_root))
```

- [ ] **Step 3: `BASE_SKILL_INDEX.json`과 project Registry를 `base_merged_sha`로 갱신한다**

Routing example:

```json
{"tags": ["archive-policy", "superseded-document"], "expected_primary": null, "expected_local": null, "expected_support": ["governing-legacy-retention-and-archives"]}
```

- [ ] **Step 4: path adapter role bindings를 추가한다**

```json
"archive_retention_adapter": "docs/archive/ARCHIVE_RETENTION_ADAPTER.json",
"archive_manifest": "docs/archive/MANIFEST.json",
"archive_readme": "docs/archive/README.md"
```

- [ ] **Step 5: validator와 workflow를 연결한다**

- [ ] **Step 6: 전체 검증을 실행한다**

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

- [ ] **Step 7: PR을 열고 독립 CI success 뒤 squash merge한다**

### Task 8: Ten Paces Registry v3 Shared Route Adoption PR

**Files:** Ten Paces File Structure 목록.

**Interfaces:**
- Registry key: `base_integration.shared_skill_routes.legacy_retention`.

- [ ] **Step 1: 최신 main에서 `gpt/adopt-archive-governance-ten-paces` 브랜치를 만든다**

- [ ] **Step 2: shared route와 adapter pin failing test를 작성하고 FAIL을 확인한다**

```python
def test_archive_governance_base_route_and_adapter(self) -> None:
    registry = json.loads((ROOT / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
    route = registry["base_integration"]["shared_skill_routes"]
    self.assertEqual("governing-legacy-retention-and-archives", route["legacy_retention"])
    adapter = json.loads((ROOT / "[기획서]/00_프로젝트_허브/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8"))
    self.assertEqual(registry["base_integration"]["commit"], adapter["base"]["commit"])
```

- [ ] **Step 3: Registry, BASE_RULES_VERSION과 freshness config를 동일한 `base_merged_sha`로 갱신한다**

기존 project discipline Skill 수 4는 변경하지 않는다.

- [ ] **Step 4: project adapter와 archive framework를 작성한다**

Active roots:

```text
[기획서]/00_프로젝트_허브
docs/02_COMBAT_RULES.md
docs/05_COMBAT_POC_SPEC.md
docs/09_COMBAT_SYSTEM_ARCHITECTURE.md
```

- [ ] **Step 5: operating checker와 archive validator를 연결한다**

- [ ] **Step 6: 전체 governance 검증을 실행한다**

```bash
python tools/check_archive_governance.py
python tools/check_project_operating_system.py
python tools/check_canonical_reference_freshness.py
python tools/check_skill_package_integrity.py
python -m unittest tests.test_project_governance -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 모두 exit 0; combat board schema와 product baseline은 unchanged.

- [ ] **Step 7: PR을 열고 독립 CI success 뒤 squash merge한다**

### Task 9: Blacksmith Registry v2 Adoption Profile PR

**Files:** Blacksmith File Structure 목록.

**Interfaces:**
- Capability ID: `governing-legacy-retention-and-archives`.
- Disposition: `ADAPT`.

- [ ] **Step 1: 최신 main에서 `gpt/adopt-archive-governance-blacksmith` 브랜치를 만든다**

- [ ] **Step 2: adoption profile capability와 archive framework failing tests를 작성하고 FAIL을 확인한다**

```python
profile = json.loads((ROOT / "docs/BASE_ADOPTION_PROFILE.json").read_text(encoding="utf-8"))
by_id = {item["base_skill_id"]: item for item in profile["capabilities"]}
item = by_id["governing-legacy-retention-and-archives"]
self.assertEqual("ADAPT", item["disposition"])
self.assertEqual("docs/archive/ARCHIVE_RETENTION_ADAPTER.json", item["local_owner"])
```

- [ ] **Step 3: adoption profile을 `base_merged_sha`로 갱신하고 capability를 추가한다**

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

- [ ] **Step 4: archive adapter를 작성한다**

Active roots:

```text
[기획서]/00_프로젝트_허브
[기획서]/01_통합_게임_기획
skills/game-design
skills/engineering
skills/qa
```

- [ ] **Step 5: audit tool에 missing capability, pin mismatch, missing files와 unsafe policy 검사를 추가한다**

- [ ] **Step 6: audit docs와 tests README를 갱신한다**

- [ ] **Step 7: 전체 검증을 실행한다**

```bash
python tools/audit_project_operating_system.py
python -m unittest tests.test_archive_retention_governance -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 모두 exit 0; project specialist Skill 수 3 유지.

- [ ] **Step 8: PR을 열고 독립 CI success 뒤 squash merge한다**

### Task 10: Cross-Repository Final Verification and Rollout Record

**Files:**
- Create in Base: `docs/audits/2026-07-25-legacy-retention-archive-governance-rollout.md`
- Modify in Base: `skills/SKILL_LEARNING_LOG.md`
- Modify in Base: this plan.

**Interfaces:**
- Consumes: 다섯 저장소의 main SHA, adopted Base SHA, PR, CI run과 validation results.

- [ ] **Step 1: 각 저장소의 main SHA, adapter, manifest, route mechanism, CI와 open PR을 기록한다**

- [ ] **Step 2: 네 프로젝트의 adopted Base SHA가 `base_merged_sha`와 정확히 일치하는지 확인한다**

- [ ] **Step 3: archive가 current canon 또는 default route로 오염되지 않았는지 검사한다**

- [ ] **Step 4: 각 project PR diff에서 아래 값을 증명한다**

```text
legacy files moved: 0
legacy files deleted: 0
legacy file bodies blanked: 0
product code/data changes: 0
```

- [ ] **Step 5: rollout audit를 `PASS / PARTIAL / FAIL / NOT_RUN`으로 작성한다**

Branch deletion은 이 rollout에서 `NOT_RUN`이다.

- [ ] **Step 6: 실제 검증된 checklist와 Learning Log만 갱신한다**

- [ ] **Step 7: Base audit-only PR을 열고 검증 뒤 squash merge한다**

---

## Self-Review Result

- **Spec coverage:** 원문 보존, 빈 파일 금지, 8개 분류, metadata·manifest, inactive Skill, generated derivative, secrets, branch/tag, project adapters, Skill TDD, automated validation, 5개 독립 PR과 deferred migration이 Tasks 1–10에 매핑된다.
- **Runtime value handling:** Base 병합 시점에만 정해지는 SHA는 Task 5의 명명된 출력 `base_merged_sha`로 전달하며 저장소 파일에는 실제 40자리 값만 기록한다.
- **Type consistency:** 공용 validator signature는 `validate_archive_governance(root: Path, adapter_path: Path, manifest_path: Path) -> list[str]`; 모든 프로젝트는 동일한 adapter와 manifest field명을 사용한다.
- **Scope:** 기존 구형 자료 이동·삭제, tag/branch 삭제와 history rewrite는 제외됐다.
