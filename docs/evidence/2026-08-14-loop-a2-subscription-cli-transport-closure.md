# Loop A2 Subscription-Native Transport Closure Evidence

Date: 2026-08-14

## Closure purpose

This closure records the user-approved Universal Loop provider policy after implementation PR #380 merged to Base `main`.

```yaml
paid_openai_api: FORBIDDEN
paid_provider_smoke: NOT_PLANNED
primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI
api_key_fallback: FORBIDDEN
```

The former paid-provider decision issue #352 is closed as `not_planned`. No separately billed OpenAI API request was run and no separately billed API cost was incurred.

## Implementation authority

- implementation issue: #379
- implementation PR: #380
- exact implementation head: `c6ee0f6765ed166619cc6e39c3dd5b5e05b01f83`
- merge/main: `ef5f1f79945d3b083c96a89295ac4bcd88d61e2d`

Main readback confirmed the subscription gate, Codex CLI transport, REAL CLI wiring, and implementation evidence remain present after merge.

## Postmerge validation

The merge SHA completed the required postmerge validations:

- A2 Runtime Foundation: `31809731573` — PASS
- OpenAI transport regression: `31809731526` — PASS
- Base-v9 Operating Contracts: `31809731528` — PASS, including adversarial gate
- Game Project Operating System: `31809731626` — PASS
  - docs validation: PASS
  - Ubuntu contract: PASS
  - publication validation: PASS
  - Windows publication smoke: PASS
  - Windows Tool Hub import/catalog smoke: PASS
  - final `ci-gate`: PASS

No retry was required for this postmerge validation.

## Closure TDD RED

Closure issue: #388
Closure PR: #389

The closure test was routed through the required docs gate before the checkpoint was modified.

- RED head: `bc187331e6792fee17b2910701c90c8ff771853d`
- Game Project Operating System run: `31810132757`
- `docs-validation`: FAIL as expected
- 124 tests ran; existing contracts passed and only the new successor-policy requirements failed

Observed missing/stale state:

1. `provider_policy` was absent.
2. `subscription_codex_cli_evidence` was absent.
3. `remaining_external_gate.real_openai_api` still said `NOT_RUN_USER_CREDENTIAL_DECISION_REQUIRED`.

## Adversarial regression finding

Two earlier closure tests encoded the former `PAID_SMOKE_GATED` state as a permanent present-state requirement:

- `tests/test_universal_loop_network_boundary_closure.py`
- `tests/test_universal_loop_provider_transport_closure.py`

Their historical #374 and #365 evidence remains unchanged. Only their present-state assertions are migrated to the approved successor policy. This prevents historical evidence tests from blocking a legitimate later policy transition.

## Machine-readable successor state

The checkpoint now records:

```yaml
status: PORTABILITY_CONFIRMED_SUBSCRIPTION_TRANSPORT_READY_LOCAL_SMOKE_GATED
provider_policy:
  paid_openai_api: FORBIDDEN
  paid_provider_smoke: NOT_PLANNED
  primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI
  api_key_fallback: FORBIDDEN
remaining_external_gate:
  real_openai_api: NOT_APPLICABLE_POLICY_FORBIDDEN
  subscription_codex_cli_smoke: NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED
  real_a2_burnin_runs: 0
  paid_smoke_issue: null
```

Historical provider-transport and denied-network evidence is retained unchanged. The runtime foundation additionally records the subscription Codex CLI transport as `MERGED_MAIN_VALIDATED`.

## Claim ceiling

This closure does **not** claim that a real ChatGPT-subscription model turn has executed. GitHub Actions does not contain the user's local ChatGPT-authenticated Codex session.

```yaml
real_subscription_smoke: NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED
real_a2_burnin_runs: 0
paid_openai_api_request: NOT_APPLICABLE_POLICY_FORBIDDEN
paid_api_cost: NOT_RUN
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_scope_selection: FORBIDDEN
```

The next external validation is a bounded local smoke where `codex login status` reports ChatGPT authentication, followed by Blacksmith A2 burn-in runs #1 through #3. No API-key or separately billed API-cost approval is required for that path.

## Rollback

Reverting this closure should restore only the previous checkpoint representation. It must not reopen or authorize the paid API path. Changing the approved `paid_openai_api: FORBIDDEN` policy requires a new explicit user decision.
