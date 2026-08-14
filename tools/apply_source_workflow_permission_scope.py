#!/usr/bin/env python3
"""Move Source automation write permissions from workflow scope to its only job."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
SELF = ROOT / "tools" / "apply_source_workflow_permission_scope.py"
TEMP = ROOT / ".github" / "workflows" / "tmp-source-workflow-permission-scope.yml"

text = WORKFLOW.read_text(encoding="utf-8")
old_permissions = """permissions:
  actions: write
  contents: write
  issues: write
  pull-requests: write
"""
new_permissions = """permissions:
  contents: read
"""
old_job = """jobs:
  analyze-validate-and-merge:
    runs-on: ubuntu-latest
"""
new_job = """jobs:
  analyze-validate-and-merge:
    permissions:
      actions: write
      contents: write
      issues: write
      pull-requests: write
    runs-on: ubuntu-latest
"""
if text.count(old_permissions) != 1:
    raise SystemExit("unexpected workflow permission block")
if text.count(old_job) != 1:
    raise SystemExit("unexpected Source automation job block")
text = text.replace(old_permissions, new_permissions, 1)
text = text.replace(old_job, new_job, 1)
WORKFLOW.write_text(text, encoding="utf-8", newline="\n")
SELF.unlink()
TEMP.unlink()
