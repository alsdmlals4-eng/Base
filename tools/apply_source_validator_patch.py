#!/usr/bin/env python3
"""Apply the reviewed Base-v9 dispatch patch to the trusted Source runner."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "run_periodic_source_scan_queue.sh"
SELF = ROOT / "tools" / "apply_source_validator_patch.py"

text = TARGET.read_text(encoding="utf-8")

replacements = (
    (
        "declare -a generated_cleanup_paths=()\n\n",
        "",
        "unused cleanup declaration",
    ),
    (
        "This PR is eligible only after exact-head Evidence Knowledge and full Game Project OS validation, current-main ancestry, zero unresolved review threads, and expected-head squash auto-merge.",
        "This PR is eligible only after exact-head Evidence Knowledge, Base v9, and full Game Project OS validation, current-main ancestry, zero unresolved review threads, and expected-head squash auto-merge.",
        "generated PR validation description",
    ),
    (
        '''  if [[ "$input_mode" == "full" ]]; then
    gh workflow run validate-game-project-operating-system.yml --ref "$branch" -f validation_level=full || return 40
  else
    gh workflow run validate-evidence-knowledge.yml --ref "$branch" || return 40
  fi
''',
        '''  case "$workflow" in
    validate-evidence-knowledge.yml)
      gh workflow run validate-evidence-knowledge.yml --ref "$branch" || return 40
      ;;
    validate-base-v9-rc.yml)
      gh workflow run validate-base-v9-rc.yml --ref "$branch" || return 40
      ;;
    validate-game-project-operating-system.yml)
      [[ "$input_mode" == "full" ]] || return 42
      gh workflow run validate-game-project-operating-system.yml \\
        --ref "$branch" \\
        -f validation_level=full || return 40
      ;;
    *)
      return 42
      ;;
  esac
''',
        "validation dispatch switch",
    ),
    (
        '''  dispatch_and_wait validate-evidence-knowledge.yml "$reviewed_head" || block "BLOCKED_ACTIONS_DISPATCH" "Evidence Knowledge dispatch or exact-head validation failed."
  dispatch_and_wait validate-game-project-operating-system.yml "$reviewed_head" full || block "BLOCKED_VALIDATION" "Full Game Project OS validation failed."
''',
        '''  dispatch_and_wait validate-evidence-knowledge.yml "$reviewed_head" || block "BLOCKED_ACTIONS_DISPATCH" "Evidence Knowledge dispatch or exact-head validation failed."
  dispatch_and_wait validate-base-v9-rc.yml "$reviewed_head" || block "BLOCKED_VALIDATION" "Base v9 dispatch or exact-head validation failed."
  dispatch_and_wait validate-game-project-operating-system.yml "$reviewed_head" full || block "BLOCKED_VALIDATION" "Full Game Project OS validation failed."
''',
        "three-validator loop",
    ),
)

for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    text = text.replace(old, new, 1)

TARGET.write_text(text, encoding="utf-8", newline="\n")
SELF.unlink()
