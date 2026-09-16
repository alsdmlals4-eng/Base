# Agent Capability Security Envelope Review — 2026-09-01

- `STATUS: RESEARCH_AND_DESIGN_EVIDENCE`
- `BASELINE_MAIN: 32f4dd5ba6042dc34611e2c8912f300b90491e0a`
- `VIDEO_URL: https://www.youtube.com/watch?v=N3st1ZrB_zc`
- `VIDEO_EVIDENCE_CEILING: PUBLIC_TITLE_DESCRIPTION_AND_CHAPTER_INDEX_ONLY`
- `FULL_TRANSCRIPT_OR_CAPTIONS: NOT_VERIFIED`
- `NO_RUNTIME_PERMISSION_CHANGE`
- `NO_ACCOUNT_OR_RULESET_CHANGE`
- `NO_PROVIDER_INSTALLATION`
- `ZERO_INCREMENTAL_COST`

## 1. Source observation boundary

The public title/description/chapter index exposed a concept stack covering LLM, API, fine-tuning, knowledge base, embedding, vector database, RAG, MCP, AI agent, agentic AI, workflow automation, and harness. Full captions or a complete transcript were not available through the current session, so this record does not attribute security claims or exact wording to the video.

The security analysis treats the chapter stack only as a discovery prompt and verifies candidate controls against current primary sources:

- MCP Authorization specification: OAuth resource indicators and audience-bound access tokens.
- MCP Tools specification: tool calls can reach external systems; servers validate inputs/access and clients keep human visibility and confirmation for sensitive operations.
- MCP Security Best Practices: no token passthrough, audience validation, minimal scopes, and confused-deputy controls.
- MCP Elicitation: sensitive credentials and payment information use out-of-band flows rather than in-band form data.
- OpenAI Agent Builder safety: untrusted data must not directly drive agent behavior; structured outputs, tool approvals, and guardrails reduce risk.
- OpenAI Agents SDK human-in-the-loop: sensitive tool calls pause for approval; nested agents and handoffs surface approval requests to the outer run.

## 2. Current Base state

Existing Base owners already cover:

- external adapter inspect/mutate/verify separation;
- argument-array execution and no-shell operation;
- explicit capabilities for network, mutation, credentials, and remote writes;
- secrets, telemetry, cost, bounded retry, kill switch, raw evidence, and adoption A/B gates;
- prompt-injection basics and repository authority.

The cross-layer gap was not a missing general security policy. It was the absence of one progressive reference joining:

1. retrieval authorization before semantic relevance;
2. provenance/confidentiality propagation through summaries and tool outputs;
3. untrusted context being unable to grant authority;
4. delegated-agent capability intersection and no privilege amplification;
5. MCP token audience/resource binding and no passthrough;
6. effect-based deny/ask/allow decisions;
7. harness checkpoints before retrieval, context insertion, tool use, delegation, response consumption, and final output.

## 3. Alternatives

### A. Append the complete envelope to the existing external adapter contract — REJECT

This preserves one file but adds substantial progressive-load cost to every adapter evaluation, even when RAG, MCP, delegation, or harness security is not relevant.

### B. Create a new top-level Skill or independent security owner — REJECT

The existing evaluation/adoption Skill already owns external agent/tool decisions. A new Skill would duplicate routing and authority.

### C. Existing owner + subordinate security reference + thin trigger router — ADOPT

Keep `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` authoritative, preserve `EXTERNAL_AGENT_ADAPTER_CONTRACT.md` as the general adapter contract, load the cross-layer security envelope only for matching triggers, and protect the relationship with focused document-contract tests.

### D. Build a runtime authorization broker or universal harness — DEFER

No concrete project/runtime consumer, identity provider, MCP server, secret store, or revocation system is in current scope. Runtime enforcement would require a separate project-specific design, approval, implementation, and behavior test.

## 4. Selected structure

- `docs/knowledge/ai/agent-tools/AGENT_CAPABILITY_SECURITY_ENVELOPE.md`
  - provider-neutral cross-layer security reference;
  - no permission grant, installation authority, or runtime-enforcement claim.
- `skills/evaluating-godot-assets-and-plugins-before-creation/references/agent-capability-security-envelope.md`
  - progressive-load router for knowledge base/RAG/MCP/delegation/workflow/harness/security triggers;
  - keeps the existing Skill authoritative.
- `tests/test_agent_capability_security_envelope.py`
  - verifies routing, key security invariants, and evidence ceilings;
  - explicitly remains a document-contract test, not a security behavior test.

## 5. Claim and adoption ceiling

This change can prove only that Base contains and routes a reusable security contract. It does not prove that a project has implemented retrieval ACL filtering, token audience validation, delegated capability enforcement, approval storage, redaction, revocation, or a policy-enforcing harness.

A project may claim those controls only after its current `AGENTS.md`, actual consumer, identity model, permission store, tool registry, runtime implementation, negative tests, denial/readback evidence, rollback, and user approval have been verified at an exact revision.
