# Base-current project work bootstrap

- Status: `CURRENT_BASE_OPERATIONAL_OWNER`
- Scope: use one fresh Base checkout to bootstrap PM/intake work against a target project without preinstalling Base files in that project.
- Does not own: project product meaning, project canon, adopted Base release, protected paths, deployment, permissions, runtime approval, or release approval.

`BASE_CURRENT_OPERATIONAL_BOOTSTRAP` · `NO_PROJECT_PREINSTALL_REQUIRED` · `NO_FLEET_PROJECT_MUTATION` · `EPHEMERAL_RECEIPT_ALLOWED`

## 1. Authority boundary

`PROJECT_CANON_PRECEDENCE` · `ADOPTED_BASE_RELEASE_UNCHANGED` · `BASE_CURRENT_IS_WORKFLOW_OVERLAY_NOT_PRODUCT_ADOPTION`

The latest user instruction and the target project's current `AGENTS.md`, approved decisions, actual code/data/scenes/assets/tests, current work items, and protected-path rules remain authoritative for project facts and product behavior. The project's adopted Base release and generated adapter remain unchanged unless a separate project adoption change is explicitly approved and validated.

A fresh exact Base `main` checkout may provide the current **PM/intake/workflow procedure** as a nonpersistent operational overlay. This overlay does not silently replace the project's adopted Base contract, create a project-local Skill copy, rewrite project canon, or make Base the owner of project-specific facts. When current Base workflow guidance conflicts with a project-specific owner, preserve the project owner and record the drift instead of rewriting it by inference.

## 2. Why this path exists

The normal adopted-adapter route remains valid for projects that already maintain a project-owned receipt and exact Base pin. It must not be a prerequisite for merely beginning a newly approved project task.

`NO_PROJECT_PREINSTALL_REQUIRED` means a work session can:

1. fresh-read the target project's exact revision and `AGENTS.md`;
2. fresh-read an exact current Base revision and this owner;
3. construct the task's root receipt in memory, stdin, a temporary file, or an existing project owner;
4. run the Base-owned gate directly against the target repository;
5. proceed only when the gate passes.

No project wrapper, copied validator, empty dashboard, generated adapter edit, reusable-workflow caller, daemon, scheduler, or fleet-wide project commit is required.

## 3. Required fresh-read order

```text
latest user instruction and approved scope
→ target project AGENTS.md and its bootstrap/read order
→ target project current main/selected source, relevant open PR boundary,
  current owner, actual consumer and implementation/test evidence
→ exact current Base main AGENTS.md
→ this owner
→ templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md
→ task-appropriate Base Skill/owner only
→ root work receipt and executable start/resume/closeout gate
```

Do not use an old chat summary, old Base SHA, project title, or receipt self-claim as the trusted revision input.

## 4. Ephemeral and durable receipts

`EPHEMERAL_RECEIPT_ALLOWED` · `PERSIST_TO_EXISTING_PROJECT_OWNER_ONLY_WHEN_WORK_REQUIRES`

The executable receipt schema remains the root contract defined by `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`: `benchmark_preflight_receipt`, `context_configuration_hygiene`, and `project_work_kanban` are sibling fields.

For a new session, the receipt may be supplied through stdin or a temporary UTF-8 JSON file outside the project repository. This lets the PM view and start gate run without changing the project.

When the approved work must persist across sessions, update the project's **existing** Issue, PR, Active Context, work receipt, or other current owner selected by project `AGENTS.md`. Create a new project-owned receipt only when no existing owner can carry the required durable state. Do not create a second design/status canon or distribute empty receipt files to every project.

The Base CLI never writes the receipt or target repository.

## 5. Commands

Fresh-read the exact Base and target-project revisions independently, then run from any directory:

```text
python -I <fresh-Base-root>/tools/run_project_work_gate.py \
  --expected-base-sha <fresh-exact-Base-SHA> \
  --project-root <target-project-root> \
  --project-source-sha <fresh-exact-project-source-SHA> \
  --receipt <receipt.json-or-> \
  --phase start \
  --render-markdown
```

Before the next approved item, first select that item as `IN_PROGRESS` or `VERIFY_REVIEW` in the same receipt and set `active_work_item_ref`, then use `--phase resume`.

Final closeout additionally requires an independently fresh-read verified project subject HEAD:

```text
python -I <fresh-Base-root>/tools/run_project_work_gate.py \
  --expected-base-sha <fresh-exact-Base-SHA> \
  --project-root <target-project-root> \
  --project-source-sha <fresh-exact-project-source-SHA> \
  --verified-head-sha <fresh-exact-verified-project-HEAD> \
  --receipt <receipt.json-or-> \
  --phase closeout \
  --render-markdown
```

`-` reads one receipt from stdin. The CLI requires an exact Base checkout, exact tracked executable bytes, an exact target Git root, and project revision objects that exist in that repository. It runs in isolated Python mode and performs no Git writes.

## 6. Start, resume and closeout semantics

- `start` and `resume` compare the receipt's `source_main_sha` to the independently supplied project source SHA.
- `closeout` additionally compares every required DONE item's `verified_head_sha` to the independently supplied verified project HEAD.
- Failed gates remain nonzero. A structurally valid blocked board may still be rendered as information, but receipt-owned execution actions are suppressed.
- A checkpoint commit is a recovery point, not DONE, merge permission, runtime/visual approval, or user approval.
- If protected merge and postmerge readback belong to the approved denominator, branch completion is `PREMERGE_CANDIDATE_NOT_CLOSEOUT`; perform protected merge and readback before final closeout.
- Approved-scope exhaustion ends with `STOP_APPROVED_SCOPE_COMPLETE`; the next session does not invent a new Goal.

## 7. Non-mutation and evidence ceiling

`NO_FLEET_PROJECT_MUTATION`

The bootstrap CLI is read-only for both repositories. It does not fetch, checkout, reset, stage, commit, push, edit, install, register services, change permissions, update adapters, or create project files. Repository preparation and mutation remain explicit operations governed by the target project's authority.

A gate PASS proves that the supplied receipt is structurally consistent with the supplied exact revisions. It does not authenticate external evidence, prove that the receipt lists the complete product backlog, establish Godot/runtime/visual/Human/release PASS, or validate current-machine services.

## 8. Existing adopted route and rollback

Projects may continue to use their adopted Base pin and project-owned wrapper/receipt when their current owner requires it. This Base-current route is an additional zero-install entry path, not a forced migration.

Before merge, rollback is closing the Base change PR. After merge, rollback is a normal revert of the Base squash commit. No project repository rollback is required because this contract performs no fleet project mutation.
