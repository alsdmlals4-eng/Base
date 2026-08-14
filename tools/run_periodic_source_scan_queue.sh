#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"
: "${SOURCE_ANALYSIS_MODEL:?SOURCE_ANALYSIS_MODEL is required}"
: "${SOURCE_SCAN_BATCH_SIZE:?SOURCE_SCAN_BATCH_SIZE is required}"

ISSUE_TITLE="[Periodic Source Scan Queue]"
QUEUE_DATE="$(python -c 'from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo("Asia/Seoul")).date().isoformat())')"
RUN_IDENTITY="${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"
RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
STATUS_PATH="source-analysis-status.json"
QUEUE_PATH="periodic-source-scan-queue.md"

python tools/periodic_source_scan_queue.py \
  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --date "$QUEUE_DATE" \
  --output "$QUEUE_PATH"

issue_number="$(
  gh issue list \
    --state open \
    --search 'in:title "[Periodic Source Scan Queue]"' \
    --limit 100 \
    --json number,title \
    --jq '.[] | select(.title == "[Periodic Source Scan Queue]") | .number' \
    | head -n 1
)"
{
  echo
  echo "## Automated daily run"
  echo
  echo "- Schedule: daily 18:00 Asia/Seoul"
  echo "- Run: $RUN_URL"
  echo "- Model: $SOURCE_ANALYSIS_MODEL"
  echo "- Status: ANALYSIS_PENDING"
} >> "$QUEUE_PATH"
if [[ -n "$issue_number" ]]; then
  gh issue edit "$issue_number" --title "$ISSUE_TITLE" --body-file "$QUEUE_PATH"
else
  issue_url="$(gh issue create --title "$ISSUE_TITLE" --body-file "$QUEUE_PATH")"
  issue_number="${issue_url##*/}"
fi

declare -a generated_cleanup_paths=()

update_queue() {
  local final_state="$1"
  local detail="$2"
  cp "$QUEUE_PATH" queue-final.md
  {
    echo
    echo "## Latest automation result"
    echo
    echo "- State: $final_state"
    echo "- Detail: $detail"
    echo "- Run: $RUN_URL"
  } >> queue-final.md
  gh issue edit "$issue_number" --body-file queue-final.md
}

write_status() {
  local code="$1"
  local detail="$2"
  python - "$STATUS_PATH" "$code" "$detail" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
try:
    payload = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    payload = {}
payload["state"] = sys.argv[2]
payload["detail"] = sys.argv[3]
path.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)
PY
}

block() {
  local code="$1"
  local detail="$2"
  write_status "$code" "$detail"
  update_queue "$code" "$detail"
  exit 0
}

python tools/periodic_source_analysis.py \
  --operations-ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --candidate-ledger docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json \
  --output-root docs/knowledge/game-development/source-scans \
  --date "$QUEUE_DATE" \
  --run-id "$RUN_IDENTITY" \
  --model "$SOURCE_ANALYSIS_MODEL" \
  --batch-size "$SOURCE_SCAN_BATCH_SIZE" \
  --status-output "$STATUS_PATH"

state="$(python -c 'import json; print(json.load(open("source-analysis-status.json", encoding="utf-8"))["state"])')"
if [[ "$state" == BLOCKED_* ]]; then
  detail="$(python -c 'import json; print(json.load(open("source-analysis-status.json", encoding="utf-8")).get("detail", "analysis blocked"))')"
  update_queue "$state" "$detail"
  exit 0
fi
if [[ "$state" == "NO_CHANGE" ]]; then
  detail="$(python -c 'import json; print(json.load(open("source-analysis-status.json", encoding="utf-8")).get("detail", "No material repository change."))')"
  update_queue "NO_CHANGE" "$detail"
  exit 0
fi
[[ "$state" == "READY_FOR_PR" ]] || block "BLOCKED_VALIDATION" "Unexpected analysis state: $state"

# A successful scan with no retained material and no new Source candidate must not create daily repository churn.
if python - "$STATUS_PATH" <<'PY'
import json
import sys
from pathlib import Path

status = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
records = [
    Path(path)
    for path in status.get("generated_paths", [])
    if "source-scans" in Path(path).parts and Path(path).suffix == ".json"
]
if len(records) != 1:
    raise SystemExit(2)
record = json.loads(records[0].read_text(encoding="utf-8"))
analysis = record.get("analysis", {})
raise SystemExit(0 if not record.get("retained_candidate_ids", []) and not analysis.get("new_source_candidates", []) else 1)
PY
then
  while IFS= read -r generated_path; do
    [[ -n "$generated_path" ]] || continue
    if [[ "$generated_path" == docs/knowledge/game-development/source-scans/* ]]; then
      rm -f -- "$generated_path"
    fi
  done < <(python -c 'import json; print("\n".join(json.load(open("source-analysis-status.json", encoding="utf-8")).get("generated_paths", [])))')
  git checkout -- \
    docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
    docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json
  detail="$(python -c 'import json,glob; p=glob.glob("docs/knowledge/game-development/source-scans/**/*.json", recursive=True); print("No material candidate survived the Evidence gate.")')"
  write_status "NO_CHANGE" "$detail"
  python - "$STATUS_PATH" <<'PY'
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["generated_paths"] = []
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
PY
  update_queue "NO_CHANGE" "$detail"
  exit 0
else
  no_change_probe=$?
  [[ "$no_change_probe" == "1" ]] || block "BLOCKED_VALIDATION" "Evidence record shape was not valid for no-change evaluation."
fi

{
  git diff --name-only -- \
    docs/knowledge/game-development/source-scans \
    docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json \
    docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
  git ls-files --others --exclude-standard -- \
    docs/knowledge/game-development/source-scans \
    docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json \
    docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
} | sed '/^$/d' | sort -u > changed-files.txt
[[ -s changed-files.txt ]] || block "NO_CHANGE" "Analysis produced no repository change."

if ! python - <<'PY'
from pathlib import Path
allowed_exact = {
    "docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json",
    "docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
}
allowed_prefix = "docs/knowledge/game-development/source-scans/"
paths = [line.strip() for line in Path("changed-files.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
bad = [path for path in paths if path not in allowed_exact and not path.startswith(allowed_prefix)]
if bad:
    raise SystemExit("out-of-scope paths: " + ", ".join(bad))
PY
then
  block "BLOCKED_PATH_SCOPE" "Generated changes escaped the approved evidence/state paths."
fi

conflict=""
while read -r pr_number; do
  [[ -n "$pr_number" ]] || continue
  gh pr view "$pr_number" --json files --jq '.files[].path' | sort -u > "pr-$pr_number-files.txt"
  overlap="$(comm -12 changed-files.txt "pr-$pr_number-files.txt" || true)"
  if [[ -n "$overlap" ]]; then
    conflict="PR #$pr_number: ${overlap//$'\n'/, }"
    break
  fi
done < <(gh pr list --state open --limit 100 --json number --jq '.[].number')
[[ -z "$conflict" ]] || block "BLOCKED_OPEN_PR_CONFLICT" "$conflict"

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
branch="automation/source-scan-${QUEUE_DATE//-/}-${RUN_IDENTITY}"
git switch -c "$branch"
git add -- \
  docs/knowledge/game-development/source-scans \
  docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json \
  docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
git commit -m "docs: absorb source scan $QUEUE_DATE"
git push --set-upstream origin "$branch"

cat > source-scan-pr-body.md <<EOF
## Daily Source evidence

- Run: $RUN_URL
- Date: $QUEUE_DATE
- Context extraction: strict structured Evidence packet
- Independent adversarial review: completed before repository mutation
- Generated path scope: immutable scan records and Source state only
- Project Canon/runtime/policy write: none

## Merge gate

This PR is eligible only after exact-head Evidence Knowledge and full Game Project OS validation, current-main ancestry, zero unresolved review threads, and expected-head squash auto-merge.
EOF

if ! pr_url="$(gh pr create \
  --base main \
  --head "$branch" \
  --title "docs: absorb source scan $QUEUE_DATE" \
  --body-file source-scan-pr-body.md)"; then
  block "BLOCKED_ACTIONS_PR_CREATION_SETTING" "GitHub Actions could not create the bounded PR."
fi
pr_number="${pr_url##*/}"

dispatch_and_wait() {
  local workflow="$1"
  local head="$2"
  local input_mode="${3:-}"
  local started
  started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if [[ "$input_mode" == "full" ]]; then
    gh workflow run validate-game-project-operating-system.yml --ref "$branch" -f validation_level=full || return 40
  else
    gh workflow run validate-evidence-knowledge.yml --ref "$branch" || return 40
  fi
  local validation_run=""
  while [[ -z "$validation_run" ]]; do
    validation_run="$(
      gh run list \
        --workflow "$workflow" \
        --branch "$branch" \
        --event workflow_dispatch \
        --limit 30 \
        --json databaseId,headSha,createdAt \
        --jq ".[] | select(.headSha == \"$head\" and .createdAt >= \"$started\") | .databaseId" \
        | head -n 1
    )"
    [[ -n "$validation_run" ]] || sleep 5
  done
  gh run watch "$validation_run" --exit-status || return 41
  local evidence
  evidence="$(gh run view "$validation_run" --json headSha,conclusion --jq '[.headSha,.conclusion] | @tsv')"
  [[ "$evidence" == "$head"$'\t'"success" ]] || return 41
}

while true; do
  reviewed_head="$(git rev-parse HEAD)"
  dispatch_and_wait validate-evidence-knowledge.yml "$reviewed_head" || block "BLOCKED_ACTIONS_DISPATCH" "Evidence Knowledge dispatch or exact-head validation failed."
  dispatch_and_wait validate-game-project-operating-system.yml "$reviewed_head" full || block "BLOCKED_VALIDATION" "Full Game Project OS validation failed."
  git fetch origin main
  if git merge-base --is-ancestor origin/main "$reviewed_head"; then
    break
  fi
  git merge --no-edit origin/main || block "BLOCKED_MAIN_MOVED_RETRY_REQUIRED" "Current main could not be merged cleanly."
  git push origin "$branch"
done

remote_head="$(gh pr view "$pr_number" --json headRefOid --jq .headRefOid)"
[[ "$remote_head" == "$reviewed_head" ]] || block "BLOCKED_VALIDATION" "PR head changed after exact-head validation."

owner="${GITHUB_REPOSITORY%%/*}"
repo="${GITHUB_REPOSITORY##*/}"
unresolved="$(gh api graphql \
  -f owner="$owner" \
  -f name="$repo" \
  -F number="$pr_number" \
  -f query='query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){reviewThreads(first:100){nodes{isResolved}}}}}' \
  --jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length')"
[[ "$unresolved" == "0" ]] || block "BLOCKED_UNRESOLVED_REVIEW_THREAD" "$unresolved unresolved review thread(s)."

gh pr merge "$pr_number" \
  --auto \
  --squash \
  --delete-branch \
  --match-head-commit "$reviewed_head"

pr_state="$(gh pr view "$pr_number" --json state,mergedAt,mergeCommit,headRefOid,autoMergeRequest)"
merged_at="$(python -c 'import json,sys; print(json.load(sys.stdin).get("mergedAt") or "")' <<<"$pr_state")"
if [[ -n "$merged_at" ]]; then
  merge_sha="$(python -c 'import json,sys; print((json.load(sys.stdin).get("mergeCommit") or {}).get("oid") or "UNKNOWN")' <<<"$pr_state")"
  update_queue "MERGED" "PR #$pr_number squash-merged at $merge_sha after exact-head validation."
else
  update_queue "AUTO_MERGE_ENABLED" "PR #$pr_number passed all local gates and auto-merge is enabled for head $reviewed_head."
fi
