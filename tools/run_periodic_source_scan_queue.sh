#!/usr/bin/env bash
set -euo pipefail

# A failed retry must not leave a previous preparation-success receipt current.
record_failure() {
  local exit_code=$?
  if [[ "$exit_code" -ne 0 ]]; then
    printf '%s\n' '{"state":"BLOCKED_QUEUE_PREPARATION","review_execution":"NOT_RUN","merge_execution":"NOT_RUN","ai_api_call":"NONE"}' > source-analysis-status.json
  fi
}
trap record_failure EXIT

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"

# Fail before any remote call when a task contains a wrong Base address or fork.
GH_REPO="$(python tools/periodic_source_scan_queue.py --normalize-repository "$GH_REPO")"
python tools/periodic_source_scan_queue.py --normalize-repository "${GITHUB_REPOSITORY:-$GH_REPO}" >/dev/null
repository_id="$(gh api "repos/$GH_REPO" --jq '.id')"
expected_repository_id="$(python -c 'from tools.periodic_source_scan_queue import BASE_REPOSITORY_ID; print(BASE_REPOSITORY_ID)')"
if [[ "$repository_id" != "$expected_repository_id" ]]; then
  printf '%s\n' 'BASE_REPOSITORY_MISMATCH: repository identity changed' >&2
  exit 1
fi

ISSUE_TITLE="[Periodic Source Scan Queue]"
QUEUE_DATE="$(python -c 'from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo("Asia/Seoul")).date().isoformat())')"
RUN_URL="https://github.com/$GH_REPO/actions/runs/${GITHUB_RUN_ID:-manual}"
STATUS_PATH="source-analysis-status.json"
QUEUE_PATH="periodic-source-scan-queue.md"
FINAL_PATH="queue-final.md"
MODE="ZERO_INCREMENTAL_COST_QUEUE_PREP"
FINAL_STATE="AWAITING_CHATGPT_REVIEW"
NEXT_EXECUTOR="USER_DIRECTED_CHATGPT_REVIEW"

python tools/periodic_source_scan_queue.py \
  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --partition-manifest docs/operations/BASE_PARTITION_MANIFEST.json \
  --date "$QUEUE_DATE" \
  --output "$QUEUE_PATH"

cp "$QUEUE_PATH" "$FINAL_PATH"
python - "$FINAL_PATH" "$MODE" "$FINAL_STATE" "$NEXT_EXECUTOR" "$RUN_URL" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
mode = sys.argv[2]
state = sys.argv[3]
next_executor = sys.argv[4]
run_url = sys.argv[5]
receipt = f"""

## Zero incremental cost Queue preparation

```yaml
mode: {mode}
state: {state}
ai_api_call: NONE
repository_change: NONE
ledger_scan_timestamp_change: NONE
candidate_evidence_claim: NOT_RUN
next_executor: {next_executor}
run: {run_url}
```

- Queue preparation only selected due Sources and refreshed this Issue.
- Actual external research, Candidate Packet evaluation, Evidence disposition, and `NO_CHANGE` determination have **not** run in this automation.
- A later user-directed ChatGPT review must perform original-source research before any scan-success or evidence claim.
"""
with path.open("a", encoding="utf-8", newline="\n") as handle:
    handle.write(receipt)
PY

# Avoid the search index and never interpret a capped or ambiguous result as absence.
gh issue list --repo "$GH_REPO" --state open --limit 100 \
  --json number,title,body,state > queue-open-issues.json
issue_number="$(python tools/periodic_source_scan_queue.py --resolve-queue-issues queue-open-issues.json)"

if [[ -n "$issue_number" ]]; then
  gh issue edit "$issue_number" \
    --repo "$GH_REPO" \
    --title "$ISSUE_TITLE" \
    --body-file "$FINAL_PATH"
else
  issue_url="$(gh issue create \
    --repo "$GH_REPO" \
    --title "$ISSUE_TITLE" \
    --body-file "$FINAL_PATH")"
  prefix="https://github.com/$GH_REPO/issues/"
  if [[ "$issue_url" != "$prefix"* ]]; then
    printf '%s\n' 'QUEUE_CREATE_RESPONSE_INVALID: unexpected destination URL' >&2
    exit 1
  fi
  issue_number="${issue_url#"$prefix"}"
  if [[ ! "$issue_number" =~ ^[1-9][0-9]*$ ]]; then
    printf '%s\n' 'QUEUE_CREATE_RESPONSE_INVALID: invalid issue number' >&2
    exit 1
  fi
fi

# API success alone is not destination readback.
gh issue view "$issue_number" --repo "$GH_REPO" --json title,body,state > queue-readback.json
python - "$FINAL_PATH" <<'PY'
import json
import sys
from pathlib import Path
from tools.periodic_source_scan_queue import ISSUE_TITLE

actual = json.loads(Path("queue-readback.json").read_text(encoding="utf-8"))
expected = Path(sys.argv[1]).read_text(encoding="utf-8")
if (actual.get("state") != "OPEN" or actual.get("title") != ISSUE_TITLE
        or actual.get("body", "").rstrip("\r\n") != expected.rstrip("\r\n")):
    raise SystemExit("QUEUE_READBACK_MISMATCH: publication is not verified")
PY

python - "$STATUS_PATH" "$MODE" "$FINAL_STATE" "$NEXT_EXECUTOR" "$RUN_URL" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = {
    "state": sys.argv[3],
    "mode": sys.argv[2],
    "ai_api_call": "NONE",
    "repository_change": "NONE",
    "ledger_scan_timestamp_change": "NONE",
    "candidate_evidence_claim": "NOT_RUN",
    "review_execution": "NOT_RUN",
    "merge_execution": "NOT_RUN",
    "next_executor": sys.argv[4],
    "run_url": sys.argv[5],
    "detail": "Due-Source Queue prepared without metered AI/API execution; actual research has not run.",
}
path.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)
PY

printf 'Source Queue prepared: %s\n' "$FINAL_STATE"
