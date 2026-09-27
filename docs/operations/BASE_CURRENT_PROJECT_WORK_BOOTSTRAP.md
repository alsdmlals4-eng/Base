# Base-current project work bootstrap

- Status: `CURRENT_BASE_OPERATIONAL_OWNER`
- Trigger: `ORDINARY_TARGET_PROJECT_WORK_TRIGGER`
- Scope: let an ordinary target-project work session fresh-read and use the current Base PM/intake/workflow procedure without first copying Base files into that project.
- Does not own: project product meaning, project canon, adopted Base release, protected paths, deployment, permissions, runtime approval, or release approval.

`BASE_CURRENT_OPERATIONAL_BOOTSTRAP` · `PROJECT_WORK_FRESH_BASE_ENTRY` · `NO_PROJECT_PREINSTALL_REQUIRED` · `NO_FLEET_PROJECT_MUTATION` · `EPHEMERAL_RECEIPT_ALLOWED` · `REGULAR_BOUNDED_RECEIPT_ONLY` · `TRUSTED_COMMIT_STREAM_ENTRYPOINT` · `ABSOLUTE_SYSTEM_GIT_REQUIRED` · `LOCAL_COMMIT_OBJECTS_ONLY`

## 1. Authority boundary

`PROJECT_CANON_PRECEDENCE` · `ADOPTED_BASE_RELEASE_UNCHANGED` · `BASE_CURRENT_IS_WORKFLOW_OVERLAY_NOT_PRODUCT_ADOPTION`

The latest user instruction and the target project's current `AGENTS.md`, approved decisions, actual code/data/scenes/assets/tests, current work items, and protected-path rules remain authoritative for project facts and product behavior. The project's adopted Base release and generated adapter remain unchanged unless a separate project adoption change is explicitly approved and validated.

A fresh exact Base `main` may provide the current **PM/intake/workflow procedure** as a nonpersistent operational overlay. This overlay does not silently replace the project's adopted Base contract, create a project-local Skill copy, rewrite project canon, or make Base the owner of project-specific facts. When current Base workflow guidance conflicts with a project-specific owner, preserve the project owner and record the drift instead of rewriting it by inference.

## 2. When this route is used

The route applies to **ordinary target-project work**, not only Base maintenance. A project session must fresh-read the current Base operational owner when it needs current shared intake, PM checklist, work decomposition, evidence, review, or closeout behavior and the project does not already carry an equivalent current owner.

`NO_PROJECT_PREINSTALL_REQUIRED` means the session can:

1. fresh-read the target project's exact revision, `AGENTS.md`, current decisions/context, actual implementation and open-PR boundary;
2. fresh-read the exact current Base `main`, root `AGENTS.md`, this owner and the task-appropriate shared owners;
3. construct the task's root receipt in memory, then write one bounded temporary JSON file outside the project or update the existing project owner selected by project authority;
4. apply the Base-current intake/PM contract without installing a wrapper, Skill copy, empty board, or generated adapter into the project;
5. use the mechanical Base CLI when a local exact Base checkout and trusted launcher boundary are available;
6. persist only the work state that the project already requires in its current repository owner.

An AI session that can read both repositories may apply this contract directly as an execution procedure. The CLI is a mechanical verification companion; inability to execute it does not authorize skipping the PM fields. Record the unavailable local execution as `ENV_GATED_EXPECTED_SKIP` or `BLOCKED_UNVERIFIED` according to the current evidence owner.

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

Do not use an old chat summary, old Base SHA, project title, or receipt self-claim as a trusted revision input. Base identifies the shared procedure; the project still supplies all mutable project facts.

## 4. Receipt ownership

`EPHEMERAL_RECEIPT_ALLOWED` · `PERSIST_TO_EXISTING_PROJECT_OWNER_ONLY_WHEN_WORK_REQUIRES` · `REGULAR_BOUNDED_RECEIPT_ONLY`

The executable receipt schema remains the root contract defined by `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`: `benchmark_preflight_receipt`, `context_configuration_hygiene`, and `project_work_kanban` are sibling fields.

For a newly resumed session, the receipt may exist in memory while the agent prepares it. Mechanical CLI validation accepts only a nonsymlink regular UTF-8 JSON file of at most 2,000,000 bytes. FIFO, socket, device, symlink and stdin are rejected. The opened descriptor is rechecked and read with the same byte ceiling. Duplicate JSON keys and non-finite JSON constants are rejected.

When approved work must persist across sessions, update the project's **existing** Issue, PR, Active Context, work receipt, or other current owner selected by project `AGENTS.md`. Create a new project-owned receipt only when no existing owner can carry the required durable state. Do not create a second design/status canon or distribute empty receipt files to every project.

The Base CLI never writes the receipt or target repository.

## 5. Trusted mechanical invocation

Direct execution of the working-copy path is unsupported because an unverified file cannot authenticate itself. `TRUSTED_COMMIT_STREAM_ENTRYPOINT` requires a trusted caller to:

1. select an exact current Base commit independently;
2. select an absolute system Git executable outside both repositories;
3. read `tools/run_project_work_gate.py` as raw bytes from that exact local commit with replacement objects and lazy fetch disabled;
4. compute SHA-256 over those exact bytes;
5. stream those same bytes to isolated Python as standard input;
6. pass the digest, exact Base root/SHA, exact project root/source SHA, and bounded receipt path.

Conceptual command shape:

```text
<absolute-git> --no-replace-objects -C <base-root> \
  cat-file blob <base-sha>:tools/run_project_work_gate.py \
  > <trusted-temporary-entrypoint>

<sha256-tool> <trusted-temporary-entrypoint>

<isolated-python> -I - \
  --entrypoint-source commit-stream \
  --entrypoint-sha256 <digest-of-exact-stream> \
  --git-executable <absolute-system-git> \
  --base-root <exact-base-root> \
  --expected-base-sha <exact-base-sha> \
  --project-root <target-project-root> \
  --project-source-sha <exact-project-source-sha> \
  --receipt <bounded-regular-receipt.json> \
  --phase start \
  --render-markdown \
  < <trusted-temporary-entrypoint>
```

The launcher must preserve raw bytes. Do not use a text pipeline that rewrites encoding or line endings. On Windows, use the repository's fresh-shell execution contract and binary-safe redirection/temporary-file handling.

## 6. Verified operational closure

The streamed entrypoint validates a bounded `VERIFIED_BASE_OPERATIONAL_CLOSURE`, including:

- root `AGENTS.md` and `START_HERE.md`;
- this bootstrap owner;
- the intake owner and Base project router;
- project start and PM checklist owners;
- the canonical receipt validator and work-tracking implementation;
- the streamed entrypoint itself.

Every closure file must be a tracked nonsymlink regular file whose working bytes equal the selected Base commit bytes. Validator modules are compiled from those already verified commit bytes; they are not reopened from mutable working paths after verification.

`ABSOLUTE_SYSTEM_GIT_REQUIRED` and `LOCAL_COMMIT_OBJECTS_ONLY` mean the CLI uses only the supplied absolute Git executable, strips inherited Git/Python path overrides, disables replacement objects, lazy fetch, optional locks and automatic maintenance, and requires each supplied Git object itself to be a locally available `commit`. It performs no fetch and does not peel an annotated tag into a trusted commit identity.

## 7. Start, resume and closeout semantics

- `start` and `resume` compare the receipt's `source_main_sha` to the independently supplied project source SHA.
- `closeout` additionally requires the supplied verified project HEAD to be a local commit descended from the supplied project source SHA, then compares every required DONE item's `verified_head_sha` to that exact HEAD.
- Failed gates remain nonzero. A structurally valid blocked board may still be rendered as information, but receipt-owned execution actions are suppressed.
- A checkpoint commit is a recovery point, not DONE, merge permission, runtime/visual approval, or user approval.
- If protected merge and postmerge readback belong to the approved denominator, branch completion is `PREMERGE_CANDIDATE_NOT_CLOSEOUT`; perform protected merge and readback before final closeout.
- Approved-scope exhaustion ends with `STOP_APPROVED_SCOPE_COMPLETE`; the next session does not invent a new Goal.

## 8. Non-mutation and evidence ceiling

`NO_FLEET_PROJECT_MUTATION`

The bootstrap CLI is read-only for both repositories. It does not fetch, checkout, reset, stage, commit, push, edit, install, register services, change permissions, update adapters, or create project files. Repository preparation and mutation remain explicit operations governed by the target project's authority.

A gate PASS proves only that the supplied receipt is structurally consistent with the supplied exact revisions and that the streamed entrypoint, validators and declared Base operational closure match the selected Base commit under the documented local read-only boundary. It does not authenticate external evidence, prove the receipt contains the complete product backlog, establish project adoption, or establish Godot/runtime/visual/Human/device/release/player PASS.

## 9. Existing adopted route and rollback

Projects may continue to use their adopted Base pin and project-owned wrapper/receipt when their current owner requires it. This Base-current route is an additional zero-install entry path, not a forced migration.

Before merge, rollback is closing the Base change PR. After merge, rollback is a normal revert of the Base squash commit. No project repository rollback is required because this contract performs no fleet project mutation.
