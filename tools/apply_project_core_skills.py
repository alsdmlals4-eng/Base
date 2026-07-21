from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "identifying-project-core": ROOT / "skills/identifying-project-core/SKILL.md",
    "establishing-project-core": ROOT / "skills/establishing-project-core/SKILL.md",
    "running-adversarial-review-and-refinement": ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md",
}

registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
registered = {item["skill_id"]: item for item in registry["skills"]}

missing = [skill_id for skill_id, path in EXPECTED.items() if skill_id not in registered or not path.is_file()]
if missing:
    raise SystemExit(f"Project core skill synchronization is incomplete: {', '.join(missing)}")

if len(registry["skills"]) != 16:
    raise SystemExit(f"Expected 16 active registry entries, found {len(registry['skills'])}")

required_surfaces = {
    "README.md": tuple(EXPECTED),
    "START_HERE.md": tuple(EXPECTED),
    "docs/DOCUMENTATION_MAP.md": tuple(EXPECTED),
    "templates/project-operations/AI_WORKFLOW.md": tuple(EXPECTED),
}
for relative_path, terms in required_surfaces.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    absent = [term for term in terms if term not in text]
    if absent:
        raise SystemExit(f"{relative_path} is missing routing entries: {', '.join(absent)}")

# This helper and the temporary base-branch workflow exist only to make the
# one-time synchronization self-validating. Remove both from the final PR.
for relative_path in (
    ".github/workflows/agent-sync-project-core-pr.yml",
    "tools/apply_project_core_skills.py",
):
    path = ROOT / relative_path
    if path.exists():
        path.unlink()
