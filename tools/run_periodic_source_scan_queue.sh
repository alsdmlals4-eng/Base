#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"

ISSUE_TITLE="[Periodic Source Scan Queue]"
QUEUE_DATE="$(python -c 'from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo("Asia/Seoul")).date().isoformat())')"
RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-$GH_REPO}/actions/runs/${GITHUB_RUN_ID:-manual}"
STATUS_PATH="source-analysis-status.json"
QUEUE_PATH="periodic-source-scan-queue.md"
FINAL_PATH="queue-final.md"
MODE="ZERO_INCREMENTAL_COST_QUEUE_PREP"
FINAL_STATE="AWAITING_CHATGPT_REVIEW"
NEXT_EXECUTOR="USER_DIRECTED_CHATGPT_REVIEW"

python tools/periodic_source_scan_queue.py \
  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --date "$QUEUE_DATE" \
  --output "$QUEUE_PATH"

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

issue_number="$(
  gh issue list \
    --repo "$GH_REPO" \
    --state open \
    --search 'in:title "[Periodic Source Scan Queue]"' \
    --limit 100 \
    --json number,title \
    --jq '.[] | select(.title == "[Periodic Source Scan Queue]") | .number' \
    | head -n 1
)"

if [[ -n "$issue_number" ]]; then
  gh issue edit "$issue_number" \
    --repo "$GH_REPO" \
    --title "$ISSUE_TITLE" \
    --body-file "$FINAL_PATH"
else
  gh issue create \
    --repo "$GH_REPO" \
    --title "$ISSUE_TITLE" \
    --body-file "$FINAL_PATH" >/dev/null
fi

printf 'Source Queue prepared: %s\n' "$FINAL_STATE"
