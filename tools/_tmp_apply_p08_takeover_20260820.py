from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "2b83d5b227259f66aacfed5ccb822c67ff414d67"


def old(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{OLD}:{path}"], cwd=ROOT, text=True, encoding="utf-8")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


# Old P08 baseline -> current main comparison showed these files were not changed
# by completed main after the original P08 baseline, so the reviewed P08 semantic
# blobs can be rehydrated without overwriting newer same-file work.
for path in (
    "docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md",
    "docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md",
    "skills/orchestrating-deepseek-worktrees/SKILL.md",
    "skills/orchestrating-deepseek-worktrees/LEARNING_LOG.md",
    "skills/optimizing-ai-model-and-prompt-costs/SKILL.md",
    "skills/optimizing-ai-model-and-prompt-costs/LEARNING_LOG.md",
):
    write(path, old(path))

# Exact semantic companion. Do not use a broad P0x wildcard; an unrelated Part
# test must not satisfy a P08 Skill contract change.
freshness_path = ROOT / ".github/reference-freshness.json"
freshness = json.loads(freshness_path.read_text(encoding="utf-8"))
rule = next(row for row in freshness["coupled_change_rules"] if row["name"] == "local-skill-contract-learning-test-sync")
exact_test = "tests/test_p08_ai_operations_contract.py"
if exact_test not in rule["require_any_changed"]:
    rule["require_any_changed"].append(exact_test)
freshness_path.write_text(json.dumps(freshness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Permanent CI consumption. File existence alone is not execution evidence.
workflow_path = ".github/workflows/validate-base-v9-rc.yml"
workflow = read(workflow_path)
module = "tests.test_p08_ai_operations_contract"
if module not in workflow:
    anchor = "            tests.test_pr530_selective_integration_contract \\\n"
    if anchor not in workflow:
        raise SystemExit("Base v9 permanent test anchor missing")
    workflow = workflow.replace(anchor, anchor + f"            {module} \\\n", 1)
write(workflow_path, workflow)

# Current-main P08 learning checkpoint. Do not reuse the old lens-style loop count.
log_path = "docs/operations/base-partitions/learning/P08_LEARNING_LOG.md"
log = read(log_path)
entry = """

## 2026-08-20 · Current-main P08 coordinator takeover

```yaml
work_ref: "P08 current-main coordinator takeover / PR #551; supersedes unfinished #535"
baseline_and_result: "Base main b1aef553bd09db6328add4988f596467f46d1179 -> selective P08 semantic rehydration"
what_worked:
  - "Revalidated #535 as coordinator backlog under OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM."
  - "Compared the old P08 baseline to current main and confirmed the six semantic P08 files had not changed before rehydrating their reviewed delta."
  - "Made tests/test_p08_ai_operations_contract.py both an exact canonical-freshness companion and a permanent Base v9 CI consumer."
what_failed_or_was_rejected:
  - "The old #535 loop count is not reused because current review accounting requires each counted loop to repeat the whole lifecycle."
  - "Broad tests/test_p0[1-9]_*.py companion patterns were rejected because an unrelated Part test could satisfy P08 freshness."
  - "Whole stale-branch merge and provider-neutral subsystem rewrite were rejected as unnecessary blast radius."
reusable_lesson: "Owner-local freshness coupling should use a semantic exact companion that permanent CI actually executes; external executors must rehydrate current canon and cost surface before action."
anti_pattern:
  - "test file exists but no permanent CI executes it"
  - "broad wildcard lets unrelated tests satisfy freshness"
  - "handoff summary treated as current canon"
  - "subscription approval treated as approval for metered add-ons"
affected_rules_skills_modules:
  - "orchestrating-deepseek-worktrees"
  - "optimizing-ai-model-and-prompt-costs"
  - "Skill/Tool routing precision"
  - "canonical reference freshness"
  - "AI Operations / External Executor Handoff"
evidence:
  - "Temporary P08 RED run 32273781518"
  - "tests/test_p08_ai_operations_contract.py"
  - ".github/reference-freshness.json"
  - ".github/workflows/validate-base-v9-rc.yml"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "semantic exact freshness companion + permanent-CI-consumption rule"
source_followup_questions: []
revisit_condition: "Revisit when AI provider/subscription billing surfaces change, multiple external executors become routine, or routing eval shows measured regression."
```
"""
if "Current-main P08 coordinator takeover" not in log:
    log = log.rstrip() + entry
write(log_path, log)

print("P08_CURRENT_MAIN_TAKEOVER_APPLIED")
