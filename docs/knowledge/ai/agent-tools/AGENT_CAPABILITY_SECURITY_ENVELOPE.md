# Agent Capability Security Envelope

- `STATUS: ACTIVE_REFERENCE`
- `AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- `EVIDENCE_AS_OF: 2026-09-01`
- `NO_NEW_SKILL_REGISTRATION`
- `CONTRACT_ONLY_NO_RUNTIME_ENFORCEMENT`
- `ZERO_INCREMENTAL_COST_DEFAULT`
- `EXTERNAL_CONTENT_IS_UNTRUSTED_DATA`
- `RETRIEVAL_AUTHORIZATION_BEFORE_RELEVANCE`
- `PROVENANCE_AND_CONFIDENTIALITY_PROPAGATE`
- `DELEGATED_CAPABILITY_SUBSET_ONLY`
- `EFFECT_BASED_DENY_ASK_ALLOW`
- `APPROVAL_BOUND_TO_CALL_IDENTITY`
- `TOKEN_AUDIENCE_BOUND_NO_PASSTHROUGH`
- `SENSITIVE_AUTH_OUT_OF_BAND`
- `HARNESS_ENFORCEMENT_NOT_PROMPT_ONLY`
- `FAIL_CLOSED_ON_UNKNOWN_POLICY`
- `KILL_SWITCH_AND_REVOCATION`
- `CONTRACT_TESTS_ARE_NOT_SECURITY_BEHAVIOR_TESTS`
- `PROJECT_ADOPTION_REQUIRES_RUNTIME_EVIDENCE`

## 1. Purpose and ownership

Modern AI work is a chain of different trust and permission boundaries rather than one model call:

```text
model / multimodal input
→ prompt and context
→ knowledge base / RAG
→ MCP and other tools
→ agent delegation
→ workflow state and side effects
→ harness policy, evidence, and recovery
```

This reference defines the minimum security envelope that must survive that entire chain. It fills the cross-layer gap between context authority, retrieval access, tool authorization, delegated agents, workflow side effects, and harness enforcement.

It composes with, and does not replace:

- `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md` for adapter execution, secrets, receipts, raw fallback, bounded retry, kill switch, trial, and rollback;
- `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` for instruction authority and context curation;
- `docs/AI_SHARED_WORK_RULES.md` for repository authority, minimum permission, and no silent privilege expansion;
- the current project `AGENTS.md`, adopted Base pin, actual code/data/assets/tests, and explicit approval boundaries.

A document contract is not an installed firewall, runtime middleware, MCP server, identity provider, or implemented agent harness. Project activation remains separate and requires behavior evidence on the exact implementation and revision.

## 2. Threat model and non-goals

The envelope addresses these failure classes:

- direct or indirect prompt injection hidden in documents, issues, webpages, images, audio transcripts, retrieved chunks, tool descriptions, or tool responses;
- RAG or memory retrieval that crosses project, user, tenant, confidentiality, deletion, or revocation boundaries;
- malicious or drifted MCP servers, poisoned tool descriptions, hidden side effects, wrong-audience tokens, token passthrough, or confused-deputy behavior;
- approvals reused for a different server, tool version, arguments, destination, repository revision, data class, or effect;
- a child agent, handoff, or agent-as-tool receiving more permissions than the parent or approved task;
- prompt-only controls that can be overridden while no deterministic policy exists before a sensitive side effect;
- retry or resume behavior that duplicates a mutation or restores stale privileges;
- logs, memory, traces, or serialized run state retaining credentials or confidential content beyond the approved scope.

This reference does **not** authorize a generic orchestration product, paid AI firewall, universal always-on human approval, new identity infrastructure, external account connection, project rollout, or replacement of current project security rules.

## 3. Shared content and authority labels

Every external or derived content item that can influence a decision or tool call should retain an equivalent of the following metadata when the implementation supports it:

```yaml
content_id:
origin: SYSTEM | USER | REPOSITORY | FILE | WEB | TOOL | AGENT | MEMORY
instruction_authority: SYSTEM_INSTRUCTION | USER_INSTRUCTION | CANON | REFERENCE | UNTRUSTED_DATA
integrity: TRUSTED | UNTRUSTED | UNKNOWN
confidentiality: PUBLIC | PROJECT_PRIVATE | SECRET | IDENTITY_BOUND
project_or_tenant_scope:
user_or_principal_scope:
source_locator:
source_revision_or_hash:
created_at:
expires_or_refreshes_at:
```

`PROVENANCE_AND_CONFIDENTIALITY_PROPAGATE`: transformations, extraction, OCR, summarization, embeddings, cached retrieval, model output, and agent delegation preserve the most restrictive applicable integrity, confidentiality, and scope labels. A derived answer may cite better evidence, but the act of summarizing does not make hostile or private input trusted.

`SUMMARY_DOES_NOT_LAUNDER_TRUST`: a summary, embedding, tool result, or model rewrite does not silently upgrade source authority, remove confidentiality, broaden project scope, or authorize a side effect.

`UNKNOWN_IS_UNTRUSTED_FOR_SENSITIVE_EFFECTS`: unknown origin, tool identity, policy, confidentiality, or approval binding is treated as untrusted for credential access, external communication, remote writes, canon mutation, destructive work, and cost-bearing actions.

`UNTRUSTED_DATA_CANNOT_AUTHORIZE_SENSITIVE_SINK`: untrusted content may provide evidence or candidate parameters after validation. It cannot grant itself authority, approve a tool, reveal a secret, widen scope, or instruct the system to perform a sensitive effect.

## 4. Model and multimodal input boundary

`MODEL_AND_MULTIMODAL_INPUT_BOUNDARY`

- Text, images, PDFs, issue bodies, repository files, audio transcripts, captions, metadata, and generated model output are data until the current authority chain classifies them otherwise.
- Hidden text, alt text, OCR output, comments, file metadata, and visual overlays are subject to the same instruction/data separation as visible prose.
- External content cannot redefine the system prompt, current user request, project canon, protected paths, approval state, or security policy.
- The model receives only the minimum content needed for the bounded task. Secrets and unrelated private project material are excluded before model invocation.
- Model output remains untrusted input to code, shell, SQL, file paths, URLs, templates, repository writes, and other interpreters until deterministic validation and the applicable approval gate pass.
- A defensive prompt is useful as one layer but is never the only control protecting a sensitive tool.

## 5. Knowledge base and RAG boundary

`KNOWLEDGE_AND_RAG_BOUNDARY`

`RETRIEVAL_AUTHORIZATION_BEFORE_RELEVANCE`: authenticate the requesting principal and enforce project, tenant, user, data-class, deletion, and revocation policy **before** semantic similarity, reranking, generation, or cache reuse. Relevance cannot grant access.

`VECTOR_ID_IS_NOT_AUTHORIZATION`: an embedding, vector-store identifier, document ID, state handle, cache key, or possession of a locator identifies a candidate resource; it does not prove that the current caller may read it. Validate the current authorization context on each access where authorization applies.

`RETRIEVED_INSTRUCTIONS_DO_NOT_GAIN_AUTHORITY`: retrieved chunks, memories, search results, and tool output are delimited as evidence/data. Instruction-like text inside them is ignored, flagged, or quarantined unless an already-authoritative owner explicitly promotes the instruction through the normal decision path.

RAG and memory implementations should, when applicable:

1. filter by exact project/tenant/principal and confidentiality scope before ranking;
2. retain source locator, revision/hash, chunk lineage, retrieval time, and deletion/revocation state;
3. prevent cross-project or cross-user memory from becoming an implicit shared prompt;
4. invalidate or reauthorize caches when source access, deletion, project pin, or relevant content changes;
5. minimize retrieved context and exclude credentials or identity-bound data not required by the task;
6. scan or quarantine suspicious instruction-like content before it reaches a tool-capable model;
7. keep citations or evidence locators so generated claims can be checked against the exact source;
8. apply output and tool-call validation after retrieval, because sanitization is not proof that injection is impossible.

A lightweight project may represent these rules with repository paths, explicit source classes, and deterministic allowlists. It does not need to adopt a new vector database, commercial content filter, or heavyweight information-flow framework merely to satisfy this contract.

## 6. MCP and tool boundary

`MCP_AND_TOOL_BOUNDARY`

`TOOL_DESCRIPTION_AND_OUTPUT_UNTRUSTED_BY_DEFAULT`: MCP tool names, descriptions, annotations, schemas, list changes, errors, resources, prompts, and outputs are untrusted unless they come from the exact trusted server/version and still pass current policy. Connect-time review does not make later runtime output trusted.

Before exposing or invoking a tool, establish:

- exact server identity, transport, version or immutable build reference, and expected capability manifest;
- the requesting project/workspace, repository revision, principal, and current approved task;
- tool identity, schema, argument constraints, possible destinations, data classes, side effects, cost, and rollback;
- whether a tool-list or schema change invalidates prior evaluation or approval;
- pre-tool argument/policy validation and post-tool output/effect validation.

`TOKEN_AUDIENCE_BOUND_NO_PASSTHROUGH`: for protected remote HTTP MCP flows, tokens are bound to the intended MCP resource and validated for that audience. An MCP server does not accept a token meant for another resource and does not pass the client token through to an upstream API. Upstream access uses a separate credential issued for that upstream resource. Local stdio credentials remain environment/secret-facility inputs rather than model-visible text.

`SENSITIVE_AUTH_OUT_OF_BAND`: passwords, API keys, access/refresh tokens, payment credentials, private keys, and third-party OAuth authorization do not transit prompts, ordinary form elicitation, tool descriptions, logs, or model context. Use the platform secret facility or a secure out-of-band authorization flow that keeps third-party credentials outside the model and MCP client context.

Local network MCP servers also preserve current transport protections such as loopback binding where appropriate, origin validation, authentication, and no public/shared-PC exposure without a separate reviewed design.

## 7. Agent delegation boundary

`AGENT_DELEGATION_BOUNDARY`

`DELEGATED_CAPABILITY_SUBSET_ONLY`: a child agent, handoff, reviewer, agent-as-tool, or background worker receives only the intersection of:

```text
parent capability
∩ current user-approved task scope
∩ project policy
∩ child task need
∩ current environment availability
```

`PARENT_CANNOT_GRANT_UNHELD_CAPABILITY`: a parent agent cannot delegate a permission, secret, data scope, remote-write right, branch authority, budget, or approval it does not possess. Delegation never repairs missing authority.

`ROOT_APPROVAL_SURFACE_PRESERVED`: sensitive approvals raised inside a child or nested agent surface to the root run or central policy owner with the actual agent, server, tool, arguments, destination, effect, and data class visible. A nested agent cannot hide a sensitive call behind a generic delegation label.

`STICKY_APPROVAL_DOES_NOT_CROSS_IDENTITY`: an always-allow or cached decision does not cross project, principal, run, server identity, tool version, destination, effect class, or materially changed arguments. The same tool name on another server is a different identity.

Each delegated run records its parent run, child identity, bounded task, context subset, capabilities, time/budget limits, exact revision, outputs, side effects, and verification status. Child output is advisory until the root workflow or an independent verifier checks it against current repository/project evidence.

## 8. Workflow effect and approval boundary

`WORKFLOW_EFFECT_BOUNDARY`

Classify the **actual effect**, not the friendly tool name. A call may have more than one class; the highest-risk applicable class controls the gate.

| Effect class | Examples | Default policy |
| --- | --- | --- |
| `OBSERVE_ONLY` | bounded read, search, metadata inspection | `ALLOW` only inside an already approved exact scope; otherwise `ASK` or `DENY` |
| `LOCAL_REVERSIBLE_WRITE` | isolated generated file, reversible branch edit | `ASK` unless covered by an exact current work contract and rollback |
| `REMOTE_WRITE_OR_PUBLISH` | email/send, issue/PR mutation, upload, deployment | `ASK`; no approval inferred from retrieved content |
| `CREDENTIAL_IDENTITY_OR_PRIVATE_DATA` | secret use, OAuth, identity-bound data | `ASK` or `DENY`; secret-safe path required |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | delete, force, payment, account/security change | `DENY` without explicit current authorization and recovery evidence |
| `COST_BEARING` | paid credits, plan upgrade, metered route | `ASK`; current free/included route remains default |

`EFFECT_BASED_DENY_ASK_ALLOW`:

- `DENY` when scope, identity, policy, destination, confidentiality, rollback, or authority is unknown; when an action exceeds the parent/task capability; or when untrusted content is the only reason for a sensitive effect.
- `ASK` when an action changes external state, uses credentials/private data, is destructive, spends money, changes security/permissions, or materially differs from the existing approval.
- `ALLOW` only when the exact effect is low-risk or already covered by a valid scoped approval, the identity and arguments match, and deterministic validation still passes.

This avoids approval fatigue without turning convenience into blanket authority. Reuse a valid scoped approval for the same call class and unchanged risk boundary; do not repeatedly ask for routine safe work. Re-open the gate when meaning, arguments, destination, data class, tool/server identity, revision, cost, or reversibility changes.

`APPROVAL_BOUND_TO_CALL_IDENTITY`: an approval receipt includes, when applicable:

```yaml
approval_ref:
principal:
project_and_revision:
parent_and_child_run:
server_identity_and_version:
tool_identity_and_schema:
call_id:
normalized_arguments_hash:
effect_classes: []
data_classes: []
destination:
allowed_result_scope:
one_shot_or_sticky:
expires_at:
rollback:
```

Malformed arguments, unknown constants, schema drift, changed tool lists, stale revisions, or missing receipt fields fail closed for sensitive effects. Resume/retry follows the existing no-automatic-replay rule in `EXTERNAL_AGENT_ADAPTER_CONTRACT.md`.

## 9. Harness policy boundary

`HARNESS_POLICY_BOUNDARY`

`HARNESS_ENFORCEMENT_NOT_PROMPT_ONLY`: the harness is the enforcement and evidence layer around the model. It should apply policy at every relevant transition rather than relying on one system prompt:

```text
intake and identity
→ context/source labeling
→ retrieval authorization and provenance
→ model output validation
→ delegation capability intersection
→ pre-tool policy and approval
→ tool execution
→ post-tool output/effect validation
→ memory/persistence filtering
→ completion verification and receipt
```

`PRE_TOOL_AND_POST_TOOL_GUARD_REQUIRED`: sensitive tools need validation before execution and verification after execution. Pre-tool checks validate identity, arguments, authority, effect, destination, confidentiality, and approval. Post-tool checks validate the observed result, changed artifacts/external state, output safety, evidence, and rollback status.

`FAIL_CLOSED_ON_UNKNOWN_POLICY`: a malformed request, unknown server/tool/version, missing identity, ambiguous data class, unavailable policy engine, or unsupported approval binding does not default to allow. The system may continue independent safe work, but the affected sensitive call remains blocked or requires explicit review.

`KILL_SWITCH_AND_REVOCATION`: capability grants, server connections, sticky approvals, child runs, credentials, and persisted state can be revoked without the failed provider. The kill switch blocks new sensitive calls, terminates only task-owned execution, preserves current repository/user state, and restores the approved raw/manual path.

`POLICY_RECEIPT_REQUIRED`: the harness records the exact project/ref, principal, content provenance and labels, selected capabilities, policy decision, approval reference, server/tool identity, arguments/effect, result, changed state, retries, evidence locator, and explicit `NOT_RUN`/`BLOCKED` gaps. Logs redact secrets and obey bounded retention.

## 10. Verification and evidence ceiling

Use a staged evidence ladder:

```text
CONTRACT_DEFINED
→ STATIC_POLICY_VERIFIED
→ DISPOSABLE_ATTACK_FIXTURE_VERIFIED
→ INTEGRATION_BEHAVIOR_VERIFIED
→ PROJECT_RUNTIME_VERIFIED
→ USER_APPROVED
```

- `CONTRACT_DEFINED`: the rule and owner exist.
- `STATIC_POLICY_VERIFIED`: schemas/configuration/tests prove required fields and forbidden defaults are represented.
- `DISPOSABLE_ATTACK_FIXTURE_VERIFIED`: isolated negative tests exercise prompt injection, cross-scope retrieval, poisoned tool output, privilege amplification, stale approval, wrong-audience token, replay, revocation, and fallback.
- `INTEGRATION_BEHAVIOR_VERIFIED`: the real adapter/harness blocks or gates representative effects through actual interfaces.
- `PROJECT_RUNTIME_VERIFIED`: the adopted project version behaves correctly at the exact revision and target environment.
- `USER_APPROVED`: the user accepts the resulting workflow and remaining risk.

`CONTRACT_TESTS_ARE_NOT_SECURITY_BEHAVIOR_TESTS`: repository string/structure tests can prevent policy deletion and routing drift. They do not prove that an MCP server validates tokens, a RAG store enforces ACLs, a guard blocks injection, or a child agent cannot exceed permissions at runtime.

`PROJECT_ADOPTION_REQUIRES_RUNTIME_EVIDENCE`: project activation requires the applicable implementation, negative fixtures, integration tests, exact-revision readback, rollback/kill-switch evidence, and the project adoption decision. Until then, runtime enforcement is `NOT_RUN`.

Minimum attack fixtures for an implementation that reaches these layers include:

1. a retrieved document or tool response that instructs the agent to read a secret and transmit it;
2. a query that attempts cross-project or cross-user retrieval;
3. the same tool name exposed by a different server or changed schema;
4. a child agent requesting a capability absent from the parent;
5. approval replay after arguments, destination, revision, or effect changes;
6. a protected remote MCP call with a wrong-audience or passed-through token;
7. kill-switch and provider-unavailable recovery without replaying a possible mutation.

## 11. Adoption disposition

| Candidate principle | Disposition | Base adaptation |
| --- | --- | --- |
| Security boundaries across RAG, MCP, agents, workflow, and harness | `ADOPT` | one thin shared envelope under the existing evaluation owner |
| Authorization before retrieval relevance | `ADOPT` | project/principal/data-class filter before ranking or cache reuse |
| Instruction/data separation and provenance | `ADOPT` | lightweight labels and exact source receipts; summaries do not upgrade trust |
| Effect-based tool approval and nested approval visibility | `ADOPT` | `DENY / ASK / ALLOW`, exact call identity, root approval surface |
| Delegated least privilege | `ADOPT` | child capabilities are a strict subset; no privilege amplification |
| OAuth audience binding and no token passthrough for protected remote MCP | `ADOPT` | protocol-specific rule only where remote authorization applies |
| Deterministic information-flow middleware or quarantined model | `ADAPT` | useful implementation option, not a required framework or dependency |
| Commercial AI firewall as the default | `REJECT` | zero-incremental-cost local/current controls first |
| Prompt-only defense | `REJECT` | prompt wording cannot own authorization or sensitive side effects |
| Approval on every harmless read | `REJECT` | valid exact scoped approval may be reused to avoid fatigue |
| New generic agent/security Skill | `REJECT` | existing evaluation, context, adapter, review, and project owners remain authoritative |

## 12. Primary-source benchmark record

The source video at `https://www.youtube.com/watch?v=N3st1ZrB_zc` presents the stack from model and prompting through knowledge base/RAG, MCP, agents, workflow automation, and harness. It is used as a discovery map, not as a security specification. The security rules above are derived from current primary or specialist security sources and reconciled with existing Base owners.

Primary references checked on 2026-09-01:

- Model Context Protocol specification — security/trust principles, tools, authorization, audience binding, token handling, and sensitive elicitation:
  - `https://modelcontextprotocol.io/specification/2025-11-25`
  - `https://modelcontextprotocol.io/specification/2025-06-18/server/tools`
  - `https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization`
  - `https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation`
- OpenAI Agents SDK — nested human-in-the-loop approvals and per-tool guardrails:
  - `https://openai.github.io/openai-agents-python/human_in_the_loop/`
  - `https://openai.github.io/openai-agents-js/guides/guardrails/`
- OWASP GenAI Security Project — prompt injection, vector/embedding access weaknesses, excessive agency, and MCP tool poisoning:
  - `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
  - `https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/`
  - `https://owasp.org/www-community/attacks/MCP_Tool_Poisoning`
- Microsoft architecture and agent safety guidance — indirect prompt injection in RAG/tool output and provenance-aware policy enforcement:
  - `https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-prompt-engineering`
  - `https://learn.microsoft.com/en-us/agent-framework/agents/safety`
  - `https://learn.microsoft.com/en-us/agent-framework/agents/security`
- NIST AI RMF Generative AI Profile, NIST AI 600-1:
  - `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence`

Vendor-specific middleware and paid security services remain reference implementations, not required Base dependencies.

## 13. Readiness checklist

Before adopting an agentic or MCP path in a project, confirm:

- exact project/principal/revision and current approval scope;
- content origin, authority, integrity, confidentiality, and project/user scope;
- retrieval authorization before relevance and cache reuse;
- server/tool identity, schema, version, data path, possible effects, and rollback;
- protected remote-token audience validation, no passthrough, and out-of-band sensitive auth where applicable;
- child capability subset, root approval visibility, and non-transfer of sticky approvals;
- effect-based `DENY / ASK / ALLOW` with an exact call-bound receipt;
- pre-tool and post-tool guards, no automatic replay, kill switch, revocation, and provider-independent fallback;
- disposable negative fixtures and exact-revision integration/runtime evidence;
- zero-incremental-cost route first and explicit approval for any new paid, identity, permission, or external-write boundary.
