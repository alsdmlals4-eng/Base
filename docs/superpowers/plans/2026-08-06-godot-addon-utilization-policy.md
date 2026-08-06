# Godot Addon Utilization Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Base require selective, evidence-backed use of approved Godot addons when they solve a current project need, while prohibiting blanket installation, unused addon accumulation, and duplicate execution authority.

**Architecture:** Strengthen the existing global gate, Godot addon evaluation Skill, shared Skill route metadata, and canonical HiGodot policy instead of creating a new Skill or central project inventory. Add focused static contract tests first, then update the existing owner documents and route metadata, preserving project-specific addon decisions in each project repository.

**Tech Stack:** Markdown policy and Skill contracts, JSON shared Skill routes, Python 3.12 `unittest`, existing Base v9 reference-freshness and integrity validators, GitHub Actions.

## Global Constraints

- Base stores common addon-selection and utilization rules only; it does not store a fixed project-by-project addon table.
- Approved and validated addons are preferred over duplicate custom implementation only when they solve a current, evidenced need.
- Addons are not copied into every project preemptively.
- An installed addon without a real editor, runtime, test, platform, or content-pipeline consumption path is `INSTALLED_UNUSED` and must be removed or deferred.
- HiGodot remains the sole Godot authoring and editor-automation execution authority.
- HiGodot sole authority does not prohibit separately scoped test, dialogue, platform-service, camera, icon, or other non-authoring addons.
- Same-role duplicate addons or mutation authorities are forbidden.
- Project core rules, save authority, canonical data ownership, credentials, and release boundaries are not transferred to a plugin without explicit evaluation and approval.
- No new ACTIVE Skill, project addon installation, runtime integration, platform account change, credential change, or product-code change is included.
- Exact addon versions, sources, licenses, adoption states, consumption paths, validation, and rollback remain project-owned records.
- Runtime, device, platform-service, accessibility, and human validation remain `NOT_RUN` unless actually executed.
- PR #206 remains Draft and must not be merged without fresh user authorization.

---

### Task 1: Add RED contract tests for selective addon utilization

**Files:**
- Create: `tests/test_godot_addon_utilization_policy.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`

**Interfaces:**
- Consumes: repository text files through `pathlib.Path` and shared route JSON through `json.loads`.
- Produces: `GodotAddonUtilizationPolicyTests`, executed by the existing Base v9 focused test workflow.

- [ ] **Step 1: Write the failing policy test module**

Create `tests/test_godot_addon_utilization_policy.py` with the following complete content:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
EVALUATION_SKILL = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md"
)
LEARNING_LOG = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md"
)
HIGODOT_POLICY = (
    ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
)
SHARED_ROUTES = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"
COMMON_POLICY_FILES = (AGENTS, EVALUATION_SKILL, HIGODOT_POLICY)
PROJECT_NAMES = (
    "Switchy Express",
    "Blacksmith",
    "urban-legend",
    "OMENWARD",
    "GRIMOIRE",
    "Ten Paces",
)


class GodotAddonUtilizationPolicyTests(unittest.TestCase):
    def test_global_gate_prefers_approved_addon_use_without_blanket_installation(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        for marker in (
            "검증·승인된 애드온",
            "직접 중복 구현보다 활용을 우선",
            "모든 프로젝트에 일괄 설치하지 않는다",
            "INSTALLED_UNUSED",
        ):
            self.assertIn(marker, text)

    def test_evaluation_skill_requires_consumption_and_lifecycle_states(self) -> None:
        text = EVALUATION_SKILL.read_text(encoding="utf-8")
        for marker in (
            "Selective addon utilization",
            "consumption_path",
            "INSTALLED_UNUSED",
            "CANDIDATE",
            "TRIAL_APPROVED",
            "ADOPTED_ACTIVE",
            "DEFERRED",
            "REMOVAL_PENDING",
            "테스트 프레임워크",
            "대화·서사 프레임워크",
            "플랫폼 서비스 애드온",
            "개발 편의·카메라·아이콘 애드온",
        ):
            self.assertIn(marker, text)

    def test_higodot_authority_scope_allows_non_authoring_addons(self) -> None:
        text = HIGODOT_POLICY.read_text(encoding="utf-8")
        for marker in (
            "저작·편집 자동화",
            "비저작 애드온",
            "테스트",
            "대화",
            "플랫폼 서비스",
            "동일 저작 권위",
        ):
            self.assertIn(marker, text)
        self.assertIn("authority_count: 1", text)

    def test_shared_route_exposes_selective_adoption_state(self) -> None:
        payload = json.loads(SHARED_ROUTES.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in payload["shared_skills"]
            if entry["skill_id"]
            == "evaluating-godot-assets-and-plugins-before-creation"
        )
        for tag in (
            "selective-addon-utilization",
            "installed-unused",
            "addon-consumption-path",
        ):
            self.assertIn(tag, item["trigger_tags"])
        for role in (
            "addon_adoption_state",
            "addon_consumption_path",
            "addon_removal_or_rollback",
        ):
            self.assertIn(role, item["project_adapter_roles"])

    def test_common_policy_does_not_freeze_project_specific_addon_tables(self) -> None:
        for path in COMMON_POLICY_FILES:
            text = path.read_text(encoding="utf-8")
            for project_name in PROJECT_NAMES:
                self.assertNotIn(project_name, text, f"{project_name} leaked into {path}")

    def test_learning_log_records_the_selective_use_decision(self) -> None:
        text = LEARNING_LOG.read_text(encoding="utf-8")
        for marker in (
            "Selective addon utilization",
            "INSTALLED_UNUSED",
            "blanket installation",
            "consumption path",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Add the focused test to the Base v9 workflow**

In `.github/workflows/validate-base-v9-rc.yml`, append the module below immediately after `tests.test_higodot_single_authority_policy` in the focused `python -m unittest` command:

```text
tests.test_godot_addon_utilization_policy \
```

- [ ] **Step 3: Run the focused test to verify RED**

Run:

```bash
python -m unittest tests.test_godot_addon_utilization_policy -v
```

Expected: FAIL because the current documents do not yet contain the selective-utilization markers, lifecycle states, route tags, and HiGodot scope clarification. Failures must be assertion failures about missing policy markers, not syntax, JSON parse, or file-not-found errors.

- [ ] **Step 4: Commit RED only**

```bash
git add tests/test_godot_addon_utilization_policy.py .github/workflows/validate-base-v9-rc.yml
git commit -m "test: define selective Godot addon utilization contracts"
```

---

### Task 2: Strengthen the global gate and clarify HiGodot authority scope

**Files:**
- Modify: `AGENTS.md`, under `## 2. 작업 진입 게이트`
- Modify: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`, under `## 2. 실행 권위` and failure conditions
- Test: `tests/test_godot_addon_utilization_policy.py`

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-08-06-godot-addon-utilization-policy-design.md`.
- Produces: one global invariant and one canonical authority-scope clarification used by the evaluation Skill.

- [ ] **Step 1: Add the global selective-utilization invariant to AGENTS**

Immediately after the current Existing Solution First Gate and `BUILD_NEW` rule, add these bullets:

```markdown
- 검증·승인된 애드온이 현재 작업의 실제 문제를 해결하면 직접 중복 구현보다 활용을 우선한다. 단, 모든 프로젝트에 일괄 설치하지 않는다. 프로젝트 단계·Godot 버전·플랫폼·권위 경계·실제 소비 경로를 확인하고 필요한 프로젝트에만 선택적으로 채택한다.
- 설치된 애드온은 편집기 작업, 런타임 기능, 테스트·CI, 플랫폼 서비스 또는 콘텐츠 제작 파이프라인 중 하나 이상의 실제 소비 경로를 가져야 한다. 소비 경로가 없으면 `INSTALLED_UNUSED`로 판정해 제거하거나 도입을 연기한다.
- HiGodot 단일 권위는 Godot 저작·편집 자동화의 중복 실행 권위를 금지하는 규칙이다. 역할이 다른 테스트·대화·플랫폼 서비스·개발 편의 애드온의 검증된 선택적 사용을 전면 금지하지 않는다.
```

Do not add project names, fixed addon lists, or project-specific recommendations.

- [ ] **Step 2: Clarify the canonical HiGodot authority boundary**

Under `## 2. 실행 권위`, after the existing sole-authority bullets, add:

```markdown
### 저작 권위와 비저작 애드온의 경계

HiGodot의 단일 권위는 Godot 저작·편집 자동화와 mutation 실행 경로에 한정된다. 동일 저작 권위를 가진 두 번째 MCP·EditorPlugin·Bridge·CLI mutation authority는 금지한다.

테스트 프레임워크, 대화·서사 도구, 플랫폼 서비스, 카메라, 아이콘, 자산 제작 보조처럼 역할이 다른 비저작 애드온은 `evaluating-godot-assets-and-plugins-before-creation`의 평가와 프로젝트별 채택 기록을 통과하면 공존할 수 있다. 공존 가능성은 자동 채택을 뜻하지 않으며, 실제 필요·정확한 버전·라이선스·소비 경로·검증·제거 절차가 없으면 설치하지 않는다.
```

Add these failure conditions under the existing failure list:

```markdown
- HiGodot 단일 권위를 비저작 애드온 전면 금지로 오해해 검증된 테스트·대화·플랫폼 도구까지 배제
- 역할이 다른 애드온이라는 이유만으로 평가·소비 경로·rollback 없이 일괄 설치
```

- [ ] **Step 3: Run the focused test**

```bash
python -m unittest tests.test_godot_addon_utilization_policy -v
```

Expected: the global-gate and HiGodot-scope tests pass; evaluation-Skill, route, and learning-log tests remain red.

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
git commit -m "docs: require selective use of approved Godot addons"
```

---

### Task 3: Extend the existing addon evaluation owner and shared route

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`
- Modify: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Modify: `tests/test_base_shared_skill_routes.py`
- Test: `tests/test_godot_addon_utilization_policy.py`

**Interfaces:**
- Consumes: global invariant from Task 2 and the existing `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` disposition model.
- Produces: project-owned addon lifecycle fields, stage-based addon routing, consumption-path enforcement, and route discovery without adding a new Skill ID.

- [ ] **Step 1: Add a selective addon utilization section to the Skill**

Insert the following section after `## Disposition states` and before `## Workflow`:

```markdown
## Selective addon utilization

평가가 `REUSE` 또는 사용자 승인된 `REFACTOR`이고 현재 작업에 실제 효용이 있으면 직접 중복 구현보다 애드온 활용을 우선한다. 발견했거나 유명하다는 이유만으로 설치하지 않으며 모든 프로젝트에 같은 애드온을 일괄 복사하지 않는다.

프로젝트별 채택 상태는 다음 중 하나다.

```text
CANDIDATE
TRIAL_APPROVED
ADOPTED_ACTIVE
ADOPTED_DISABLED
DEFERRED
REJECTED
INSTALLED_UNUSED
REMOVAL_PENDING
REMOVED
```

최소 프로젝트 기록:

```yaml
addon_name:
role:
exact_version:
source:
license:
godot_compatibility:
platform_scope:
adoption_state:
consumption_path:
owner_boundary:
validation:
rollback_or_removal:
unverified:
```

`consumption_path`는 다음 중 하나 이상을 실제로 가리킨다.

- 프로젝트 테스트 명령 또는 CI
- 편집기 작업 흐름
- 런타임 기능
- 플랫폼 빌드·서비스 연결
- 콘텐츠 제작 파이프라인

설치됐지만 소비 경로가 없으면 `INSTALLED_UNUSED`다. 제거하거나 필요가 생길 때까지 `DEFERRED`로 되돌리며, 단순 폴더 존재를 채택 완료로 보고하지 않는다.

### 단계별 기본 라우팅

#### 테스트 프레임워크

- 테스트 가능한 제품 코드, 저장, 경제, 전투, 퍼즐, 분기 또는 반복 가능한 상태 규칙 구현이 시작되면 우선 검토한다.
- 기획 전용 저장소 또는 실행 가능한 제품 코드가 없는 단계에서는 `DEFERRED`다.
- 실제 테스트 파일·실행 명령·CI 소비 경로와 exact version이 없으면 설치하지 않는다.

#### 대화·서사 프레임워크

- 분기, 조건, 화자, 현지화, 저장 복구와 콘텐츠 편집 요구가 기존 JSON·Resource·Scene 구조보다 복잡해질 때 검토한다.
- 운영 중인 사건·대화 정본을 사전 비교 없이 교체하지 않는다.
- 작은 대표 흐름에서 마이그레이션·저장 호환성·제거 절차를 시험한다.

#### 플랫폼 서비스 애드온

- Google Play Billing·Games, Steam 또는 동등한 플랫폼 기능이 승인된 출시 범위에 들어오고 실제 통합 작업을 시작할 때 검토한다.
- 플랫폼이 미래 후보이거나 결제·업적·클라우드 저장 요구가 승인되지 않았으면 `DEFERRED`다.
- 목표 플랫폼별 빌드 분리, credential 비공개, 테스트 트랙, 실패 시 게임 코어 독립 실행을 요구한다.

#### 개발 편의·카메라·아이콘 애드온

- 실제 반복 작업이나 승인된 UX·카메라 요구를 줄일 때만 검토한다.
- Godot 기본 Node·Resource·Editor 기능으로 충분하면 추가하지 않는다.
- build 포함 여부, runtime dependency, Scene 복구와 제거 절차를 확인한다.
```

- [ ] **Step 2: Extend the Skill workflow and quality gate**

In `## Workflow`, after the disposition step, add exact requirements to:

```text
current project stage 확인
→ project-owned adoption state 기록
→ exact version/source/license 기록
→ consumption_path 확인
→ isolated trial and rollback/removal 검증
→ ADOPTED_ACTIVE or DEFERRED/REJECTED 결정
```

In `## Quality gate`, add:

```markdown
- 채택된 애드온에는 실제 `consumption_path`가 있다.
- 현재 단계에 필요 없는 애드온을 미리 설치하지 않았다.
- `INSTALLED_UNUSED`는 제거 또는 도입 연기 판정을 받았다.
- 같은 역할의 애드온이나 mutation authority를 둘 이상 활성화하지 않았다.
- 프로젝트별 채택 상태를 Base 공용 정책에 고정하지 않았다.
```

In `## Output contract`, add:

```markdown
## Addon adoption state and consumption path
## Removal or rollback evidence
```

- [ ] **Step 3: Record the learning**

Append this entry to `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`:

```markdown
## 2026-08-06 — Selective addon utilization requires a consumption path

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 여러 Godot 프로젝트의 addon 폴더를 정리한 뒤 HiGodot, 테스트, 대화, 플랫폼 애드온을 어느 단계에서 실제로 사용해야 하는지 공용 원칙이 필요해짐.
- **Finding:** 기존 Existing Solution First Gate는 중복 제작을 막지만 평가를 통과한 애드온의 실제 활용, blanket installation 금지, unused addon 제거 기준을 충분히 명시하지 않았다.
- **Decision:** 승인·검증된 애드온이 현재 문제를 해결하면 직접 구현보다 활용을 우선한다. 모든 프로젝트에 일괄 설치하지 않고 project stage, exact version, owner boundary, validation, rollback과 consumption path를 요구한다.
- **Failure state:** 설치됐지만 editor, runtime, test/CI, platform service 또는 content pipeline 소비 경로가 없으면 `INSTALLED_UNUSED`이며 제거하거나 도입을 연기한다.
- **Authority boundary:** HiGodot은 Godot authoring automation의 단일 권위다. 테스트·대화·플랫폼 서비스처럼 역할이 다른 비저작 애드온은 평가 후 공존할 수 있지만 같은 역할의 중복 권위는 허용하지 않는다.
- **Verification state:** Base static contract planned; actual project addon installation, runtime, device, store service and human validation remain `NOT_RUN`.
- **Next trigger:** addon version, Godot version, license, platform scope, consumption path or project stage가 바뀌면 `revalidate`한다.
```

- [ ] **Step 4: Extend the shared Skill route metadata**

In the `evaluating-godot-assets-and-plugins-before-creation` entry of `skills/BASE_SHARED_SKILL_ROUTES.json`, add these unique values:

```json
"trigger_tags": [
  "selective-addon-utilization",
  "installed-unused",
  "addon-consumption-path"
]
```

Merge them into the existing array; do not replace current tags.

Add these unique project adapter roles:

```json
"project_adapter_roles": [
  "addon_adoption_state",
  "addon_consumption_path",
  "addon_removal_or_rollback"
]
```

Merge them into the existing array; do not replace current roles. Do not create a new shared Skill entry or change the ACTIVE Skill count.

- [ ] **Step 5: Extend the existing shared-route test**

In `tests/test_base_shared_skill_routes.py`, extend `test_godot_provider_route_exposes_reuse_first_and_higodot_contracts` with these assertions:

```python
for tag in (
    "selective-addon-utilization",
    "installed-unused",
    "addon-consumption-path",
):
    self.assertIn(tag, item["trigger_tags"])

for role in (
    "addon_adoption_state",
    "addon_consumption_path",
    "addon_removal_or_rollback",
):
    self.assertIn(role, item["project_adapter_roles"])
```

- [ ] **Step 6: Run focused tests**

```bash
python -m unittest \
  tests.test_godot_addon_utilization_policy \
  tests.test_base_shared_skill_routes \
  -v
```

Expected: PASS.

- [ ] **Step 7: Run the reference-freshness focused test**

```bash
python -m unittest tests.test_reference_freshness -v
```

Expected: PASS. If it reports an existing coupled-change requirement for this Skill, satisfy only the exact required companion file from the current rule; do not create a new policy owner or broad Skill.

- [ ] **Step 8: Commit**

```bash
git add \
  skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md \
  skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md \
  skills/BASE_SHARED_SKILL_ROUTES.json \
  tests/test_base_shared_skill_routes.py
git commit -m "feat: route approved addons by need and consumption"
```

---

### Task 4: Full validation, adversarial review, and Draft PR update

**Files:**
- Modify only files required by validated failures from Tasks 1–3.
- Update: PR #206 body after exact-head evidence is available.
- Create no new Skill, addon registry, project recommendation table, or runtime integration.

**Interfaces:**
- Consumes: Tasks 1–3 exact branch head.
- Produces: evidence-backed Draft PR with selective addon utilization enforced and no unresolved P0/P1 findings.

- [ ] **Step 1: Run focused policy and route tests**

```bash
python -m unittest \
  tests.test_godot_addon_utilization_policy \
  tests.test_higodot_single_authority_policy \
  tests.test_base_shared_skill_routes \
  tests.test_reference_freshness \
  -v
```

Expected: PASS.

- [ ] **Step 2: Check generated artifacts and Base integrity**

Resolve the exact trusted `main` SHA first:

```bash
MAIN_SHA=$(git rev-parse origin/main)
python tools/build_base_v9_artifacts.py --check
python tools/check_base_v9_integrity.py --trusted-history-commit "$MAIN_SHA"
```

Expected: PASS. If generated artifacts are stale because the shared route is a generated input, run the repository's canonical generator identified by the failing command, commit only its deterministic outputs, and rerun both checks.

- [ ] **Step 3: Run the required Base contract subset**

```bash
python -m unittest \
  tests.test_v9_machine_contracts \
  tests.test_v9_registry_generation \
  tests.test_v9_governance_documents \
  tests.test_v9_1_project_operating_contract \
  tests.test_v9_1_review_remediation \
  tests.test_v9_1_skill_pressure_contracts \
  tests.test_higodot_single_authority_policy \
  tests.test_godot_addon_utilization_policy \
  tests.test_base_shared_skill_routes \
  -v
```

Expected: PASS.

- [ ] **Step 4: Verify scope and no new Skill identity**

Run:

```bash
git diff --check
git diff --name-only origin/main...HEAD
find skills -name SKILL.md -type f | sort > /tmp/current-skill-files.txt
git ls-tree -r --name-only origin/main -- 'skills/*/SKILL.md' | sort > /tmp/main-skill-files.txt
diff -u /tmp/main-skill-files.txt /tmp/current-skill-files.txt
```

Expected:

- `git diff --check`: no output.
- The Skill-file inventory diff: no output.
- No project repository, `addons/`, `project.godot`, credential, platform config, or product code path in changed files.

- [ ] **Step 5: Run adversarial patch review**

Inspect the entire PR patch and attack these failure modes:

```text
approved addon use accidentally becomes mandatory installation
blanket installation wording survives elsewhere
HiGodot sole authority is weakened into multiple mutation authorities
HiGodot sole authority is misread as banning all non-authoring addons
same-role duplicate addons remain permitted
INSTALLED_UNUSED has no removal or defer action
project-specific names or fixed addon tables leak into Base common policy
project core/save/data authority is delegated to plugins without a boundary
platform credentials or personal MCP configuration are requested in public records
static policy is overstated as runtime, device, store-service, or production evidence
new ACTIVE Skill or duplicate owner is introduced
shared route or generated artifact drift remains
```

Classify findings as `P0 / P1 / P2 / ACCEPTED_RISK`. Fix all validated P0/P1 findings, rerun Steps 1–4, and record remaining P2 or accepted risk in the PR body.

- [ ] **Step 6: Update Draft PR #206**

Replace the design-only status in the PR body with:

```markdown
## Implemented

- global selective addon utilization invariant
- actual consumption-path requirement and `INSTALLED_UNUSED` removal/defer rule
- stage-based routing for test, dialogue, platform-service, and development-convenience addons
- HiGodot authority scope clarified as Godot authoring/editor automation only
- shared route tags and project adapter roles for addon adoption state
- no project-specific addon table and no new ACTIVE Skill

## Validation

- focused addon policy tests: PASS
- HiGodot authority regression: PASS
- shared route tests: PASS
- reference freshness: PASS
- Base generated artifact and integrity checks: PASS
- required Base contract subset: PASS
- `git diff --check`: PASS
- project runtime/device/store service/human validation: NOT_RUN

## Merge boundary

Draft review only. Do not merge without fresh explicit user authorization.
```

Include the exact head SHA and final changed-path list.

- [ ] **Step 7: Run exact-head GitHub Actions**

Require at minimum:

```yaml
Validate Base v9 Operating Contracts: PASS
Validate Game Project Operating System: PASS
Dependency Review: PASS
```

Do not convert a skipped, queued, missing-runner, or cancelled workflow into PASS.

- [ ] **Step 8: Stop at merge gate**

Report:

```yaml
pr: 206
exact_head:
changed_paths:
focused_tests:
base_contracts:
github_actions:
adversarial_findings:
new_active_skill: false
project_addon_installation: NOT_PERFORMED
runtime_device_store_human: NOT_RUN
merge_authorization: NOT_GRANTED
rollback: close PR or revert the policy commits
```

Do not merge, install addons into product repositories, or edit project-specific addon inventories without a separate approved task.
