# Loop A2 Unattended Local Executor Evidence

## Identity

- Tracking issue: `#397`
- Implementation PR: `#398`
- Goal: bridge bounded GitHub jobs to the merged subscription-native REAL Loop A2 path on the user's Windows machine without a separately billed OpenAI API or API-key fallback.
- Product authority: unchanged. This slice does not select a Blacksmith product Package, change Planning/Visual meaning, enable A3, or configure Scheduler.

## Existing-solution-first result

The implementation reuses the merged REAL A2 path from PR `#391`, including post-baseline authority snapshots, isolated exact-SHA worktrees, deterministic ProjectTestExecutor evidence before Critic, and the ChatGPT-authenticated Codex CLI provider boundary. It also reuses the existing one-shot/project-dedicated local execution policy rather than creating another model runtime.

The new responsibility is only the unattended control bridge:

```text
bounded GitHub issue job
→ exact author/label/schema validation
→ executor-owned exact-SHA repositories/worktrees
→ reviewed Docker DENIED boundary preflight
→ merged REAL A2 host command
→ bounded public receipt
```

## TDD chronology

### Initial contract RED

- Test-only head: `5847611e2321288aacbc0750df2380607693faec`
- Focused workflow: `31821098000`
- Ubuntu and Windows failed at the new local-executor contract because the production package did not yet exist.

### Parser hardening

The first parser implementation exposed a cross-platform path bug: `PurePosixPath` alone could treat a Windows drive spelling such as `C:/...` as relative. The contract remained strict and production was corrected to reject drive-prefixed Capsule paths rather than weakening the test.

### Incremental RED/GREEN slices

Separate test-first slices covered:

- exact issue author/label and closed JSON job schema;
- prohibition on remotely supplied `argv`, command, environment, local path, prompt, merge authority, or arbitrary repository URL;
- GitHub CLI queue reads and allowlisted receipt publication;
- executor-owned clone/worktree isolation from the user's normal checkout;
- exact Base runtime SHA and exact project authority SHA;
- host-derived REAL A2 argv only;
- digest-pinned Docker image inspection without automatic pull;
- secret-stripped child environment;
- no-console Windows `.pyw` entry shape;
- queue-label preflight;
- singleton executor ownership.

### Adversarial RED

Head `99ede4ee7969c6944c5bf47e5c2ef103da261a8b` / focused run `31822513857` deliberately exposed four remaining gaps while the existing contracts stayed green:

1. installed console entrypoint missing;
2. singleton lock module missing;
3. symlinked Capsule reached later runtime preflight instead of failing before process execution;
4. managed-repository failure escaped without a terminal public blocker receipt.

A follow-up test head also required `once` and `daemon` themselves, not merely a standalone lock helper, to acquire the same state-root singleton lock and run control-plane preflight before processing.

### Adversarial remediation GREEN

Implementation head `3d6967bfda6ace07f56c6373bea8ce4fce2ede88` passed focused run `31824214099` on both Ubuntu 24.04 and Windows 2025.

Ubuntu evidence: `43` tests, all PASS. The suite covers queue schema, secret-free GitHub argv/environment, idempotent queue-label setup, receipt allowlisting, installed command, singleton lock integration, executor-owned repositories, exact worktree SHA, user-checkout non-mutation, reviewed image identity, no image pull, API/GitHub secret exclusion, REAL receipt identity, Capsule symlink rejection, managed-repository blocker publication, and one-job processing.

At the same head:

- Validate Base v9 Operating Contracts `31824214095`: PASS.
- Dependency Review `31824214113`: PASS.
- Game Project Operating System validation was triggered as a broad regression gate; merge eligibility remains bound to the final exact-head result, not to this intermediate evidence line.

## Security and authority boundaries

### Remote job cannot become a shell

The job contract accepts only closed identity fields:

```text
schema_version
contract_role
target_repository
base_runtime_sha
authority_sha
capsule
run_id
provider
```

It rejects remote command/argv/environment/local-path/prompt/merge fields. Repository source URLs are constructed by host code from validated GitHub `owner/name`; the issue body cannot provide a clone URL.

### Local user checkout remains out of scope

The executor creates and reuses only its own managed repositories beneath its state root. Execution worktrees are detached, exact-SHA, external to the user's ordinary checkout, and removed after use. Contract tests preserve an independent dirty user checkout and prove it is unchanged.

### Model/payment boundary

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
active_model_path: CHATGPT_AUTHENTICATED_CODEX_CLI
model_shell_tool: DISABLED_BY_MERGED_A2_RUNTIME
model_web_search: DISABLED_BY_MERGED_A2_RUNTIME
```

The local executor does not add an OpenAI SDK/API-key route. Provider execution remains the merged subscription-native Codex CLI transport.

### Project-test network boundary

The host does not pull a Docker image during a job. It inspects the reviewed digest-pinned image reference, obtains the exact local immutable image ID, and passes only that ID into the merged REAL A2 `DockerNoneDeniedNetworkBoundary` path.

### Queue ownership and duplicate execution

Control-plane preflight verifies the existing `gh` login and idempotently ensures the dedicated `loop-a2-local-job` label. `once` and `daemon` acquire the same OS-backed state-root lock, preflight once, and only then inspect the queue. A second local executor against the same state root fails closed with `LOCAL_EXECUTOR_ALREADY_RUNNING`.

### Public receipt ceiling

GitHub receipts are allowlisted. Raw stdout/stderr, local paths, tokens, reasoning, arbitrary changed content, or child environment are not published. Runtime/repository blockers publish only their bounded code and job identity before the queue issue is closed, preventing silent infinite retry.

## Adversarial review disposition

- arbitrary remote shell/argv/environment: **BLOCKED**
- arbitrary clone URL: **BLOCKED**
- user checkout mutation: **BLOCKED BY MANAGED-ROOT DESIGN + TEST**
- symlink Capsule indirection: **BLOCKED BEFORE PROCESS EXECUTION**
- API/GitHub secret inheritance into REAL A2 child: **BLOCKED BY ALLOWLIST**
- Docker pull during job: **FORBIDDEN**
- duplicate daemon on same state root: **BLOCKED BY OS FILE LOCK**
- failed repository/runtime job silently retried forever: **BLOCKED BY TERMINAL RECEIPT + CLOSE**
- A3 activation: **DISABLED**
- Scheduler activation: **NOT_CONFIGURED**
- automatic product Package selection: **FORBIDDEN**

No validated adversarial finding requires a broader Skill, Tool Hub UI change, product change, or modification of unrelated open PRs.

## Implementation Reality Gate

Proved by repository/CI evidence:

- bounded job parser and remote-command rejection;
- GitHub control-plane argv/environment and receipt contract;
- executor-owned exact-SHA repository/worktree orchestration;
- host-derived REAL A2 invocation shape;
- Docker no-pull preflight shape;
- cross-platform singleton lock behavior;
- Windows no-console entry source shape;
- Ubuntu/Windows focused contract execution.

Not proved by this repository CI:

- the user's Windows machine currently has the executor installed and registered at login;
- `gh auth status` is currently ready on that machine;
- `codex login status` is currently ChatGPT-authenticated on that machine;
- the reviewed Docker image is already present on that machine;
- a real ChatGPT-plan Codex Builder/Critic turn has occurred through this bridge;
- Blacksmith REAL A2 burn-in run 1/2/3 has occurred.

Those remain local execution evidence, not repository implementation claims.

## Rollback

Revert the eventual PR #398 squash merge. Queue issues are control-plane records only. Reverting this bridge does not authorize paid API usage, mutate project product data, alter Planning/Visual authority, enable A3, or configure Scheduler.
