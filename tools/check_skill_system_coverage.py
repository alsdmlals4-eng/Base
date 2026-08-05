from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
COVERAGE = ROOT / "skills/SKILL_COVERAGE.json"
FRONT_NAME = re.compile(r"^name:\s*['\"]?([^'\"\n]+)", re.MULTILINE)
ALLOWED_COVERAGE_STATUSES = {"COVERED", "COVERED_EXISTING"}

# These packages were historically called compact targets. They now use a
# completeness-first contract: required navigation and quality sections must be
# present, but line, character, page, and file-size ceilings are not quality gates.
CONTRACT_STRUCTURE_TARGETS = {
    "identifying-project-core",
    "establishing-project-core",
    "running-adversarial-review-and-refinement",
    "evolving-project-discipline-skills",
    "analyzing-and-refining-game-concepts",
    "refactoring-with-contract-preservation",
    "simplifying-skill-bodies",
    "pruning-stale-and-nonfunctional-material",
    "synchronizing-local-and-github-state",
    "maintaining-long-running-task-continuity",
    "governing-game-user-research-coverage",
    "creating-user-learning-notes",
    "building-project-visual-dashboards",
    "diagnosing-game-engine-runtime-failures",
    "governing-legacy-retention-and-archives",
}

BCP008_CONTRACTS = {
    "templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md": (
        "L2 이상",
        "별도 책임 원본이 아니다",
        "decision_id",
        "requirement_id",
        "acceptance_criteria_ids",
        "task_ids",
        "implementation_paths",
        "verification_ids",
        "coverage_status",
        "BLOCKED_UNVERIFIED",
    ),
    "skills/running-adversarial-review-and-refinement/references/cross-discipline-review-lenses.md": (
        "제품·플레이어 가치",
        "UX·접근성",
        "아키텍처·상태 소유권",
        "구현·성능·플랫폼",
        "QA·회귀·출시",
        "문서·추적성·인수인계",
        "결정을 소유하지 않는다",
        "NOT_APPLICABLE",
    ),
    "templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md": (
        "format_version",
        "source_commit_or_release",
        "last_verified_at",
        "colors:",
        "typography:",
        "spacing:",
        "components:",
        "godot_theme_mapping",
        "web_token_mapping",
        "reference_provenance",
        "게임 규칙",
        "소유하지 않는다",
    ),
    "skills/auditing-and-refining-ui-art/references/design-md-project-adapter.md": (
        "GAME_UX_UI_SYSTEM",
        "Theme",
        "CSS",
        "시각 토큰",
    ),
    "skills/auditing-and-refining-ui-art/references/external-ui-procurement-and-anti-generic-quality.md": (
        "registry_source",
        "exact_version_or_commit",
        "content_hash",
        "license",
        "dependencies",
        "scripts",
        "secrets",
        "files_added_or_replaced",
        "accessibility_review",
        "runtime_review",
        "rollback",
        "BLOCKED_UNVERIFIED",
        "MCP 연결 성공",
        "설치 승인",
        "Design Read",
        "실제 렌더",
    ),
}

BCP008_BEHAVIOR_CASES = {
    "SBE-901",
    "SBE-902",
    "SBE-903",
    "SBE-904",
}


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_bcp008(errors: list[str]) -> None:
    for relative, required_terms in BCP008_CONTRACTS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing BCP-008 contract: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in required_terms:
            if term not in text:
                errors.append(f"Missing BCP-008 contract token {term!r}: {relative}")

    owner_routes = {
        "skills/managing-project-intake-and-work-contract/SKILL.md": (
            "FEATURE_SPEC_TRACEABILITY_PACKET.md",
            "L0·L1",
        ),
        "skills/managing-design-documents/SKILL.md": (
            "FEATURE_SPEC_TRACEABILITY_PACKET.md",
            "상세 책임 원본",
        ),
        "skills/reviewing-and-validating-project-changes/SKILL.md": (
            "FEATURE_SPEC_TRACEABILITY_PACKET.md",
            "coverage_status",
        ),
        "skills/running-adversarial-review-and-refinement/SKILL.md": (
            "cross-discipline-review-lenses.md",
            "L2 이상",
        ),
        "skills/auditing-and-refining-ui-art/SKILL.md": (
            "design-md-project-adapter.md",
            "external-ui-procurement-and-anti-generic-quality.md",
            "기본 설치",
        ),
        "templates/planning/GAME_UX_UI_SYSTEM.md": (
            "DESIGN.md",
            "시각 토큰",
            "플레이어 경험",
        ),
    }
    for relative, required_terms in owner_routes.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing BCP-008 owner route: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in required_terms:
            if term not in text:
                errors.append(f"Missing BCP-008 owner route token {term!r}: {relative}")

    behavior_path = ROOT / "skills/SKILL_BEHAVIOR_EVALS.json"
    try:
        behavior = json.loads(behavior_path.read_text(encoding="utf-8"))
        case_ids = {case.get("case_id") for case in behavior.get("cases", [])}
        missing_cases = sorted(BCP008_BEHAVIOR_CASES - case_ids)
        if missing_cases:
            errors.append(f"Missing BCP-008 behavior cases: {missing_cases}")
        if behavior.get("model_run_status") != "NOT_RUN":
            errors.append("BCP-008 must not claim independent model behavior without a current result")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot validate BCP-008 behavior cases: {exc}")

    validator_path = ROOT / "tools/validate_external_ui_procurement_receipt.py"
    receipt_path = (
        ROOT
        / "docs/evidence/external-ui-procurement/BCP008_SHADCN_BUTTON_PILOT.json"
    )
    if not validator_path.is_file():
        errors.append("Missing BCP-008 procurement receipt validator")
    if not receipt_path.is_file():
        errors.append("Missing BCP-008 shadcn procurement receipt")
    if validator_path.is_file() and receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            validator = _load_module(validator_path, "bcp008_procurement_validator")
            result = validator.validate_receipt(receipt)
            if not result.get("valid"):
                errors.extend(
                    f"Invalid BCP-008 procurement receipt: {item}"
                    for item in result.get("errors", ["unknown error"])
                )
            if result.get("decision") != "BLOCKED_UNVERIFIED":
                errors.append("BCP-008 source-only pilot must remain BLOCKED_UNVERIFIED")
            if receipt.get("installation") != "NOT_RUN":
                errors.append("BCP-008 must not claim external UI installation into Base")
        except (OSError, json.JSONDecodeError, RuntimeError, AttributeError) as exc:
            errors.append(f"Cannot validate BCP-008 procurement receipt: {exc}")


def validate() -> list[str]:
    errors: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    by_id = {item["skill_id"]: item for item in registry["skills"]}

    responsibility_ids: set[str] = set()
    for responsibility in coverage["responsibilities"]:
        responsibility_id = responsibility["id"]
        if responsibility_id in responsibility_ids:
            errors.append(f"Duplicate responsibility id: {responsibility_id}")
        responsibility_ids.add(responsibility_id)

        if responsibility.get("status") not in ALLOWED_COVERAGE_STATUSES:
            errors.append(
                f"Invalid coverage status: {responsibility_id} -> {responsibility.get('status')}"
            )
        targets = responsibility.get("skills", [])
        if not targets:
            errors.append(f"No skill target: {responsibility_id}")
        if len(targets) != len(set(targets)):
            errors.append(f"Duplicate skill target: {responsibility_id}")
        for skill_id in targets:
            entry = by_id.get(skill_id)
            if entry is None:
                errors.append(f"Coverage target not registered: {responsibility_id} -> {skill_id}")
            elif entry["status"] != "ACTIVE":
                errors.append(f"Coverage target not active: {responsibility_id} -> {skill_id}")

    for skill_id in sorted(CONTRACT_STRUCTURE_TARGETS):
        if skill_id not in by_id:
            errors.append(f"Contract structure target not registered: {skill_id}")

    for skill_id, item in by_id.items():
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append(f"Missing skill file: {skill_id} -> {item['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONT_NAME.search(text)
        if not match or match.group(1).strip() != skill_id:
            errors.append(f"Front matter mismatch: {skill_id}")
        if skill_id in CONTRACT_STRUCTURE_TARGETS:
            for required in ("##", "Output contract", "Quality gate", "Learning Log"):
                if required not in text:
                    errors.append(f"Missing completeness contract token {required!r}: {skill_id}")

    for obsolete in (
        ROOT / "tools/apply_skill_system_expansion.py",
        ROOT / ".github/workflows/agent-expand-and-optimize-skill-system.yml",
    ):
        if obsolete.exists():
            errors.append(f"Temporary expansion artifact remains: {obsolete.relative_to(ROOT)}")

    _validate_bcp008(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Skill system coverage check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill system coverage check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
