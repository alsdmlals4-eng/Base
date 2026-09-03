# Agent Capability Security Envelope Router

- `STATUS: ACTIVE_SUBORDINATE_REFERENCE`
- `AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- `GENERAL_ADAPTER_CONTRACT: docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`
- `CANONICAL_SECURITY_REFERENCE: docs/knowledge/ai/agent-tools/AGENT_CAPABILITY_SECURITY_ENVELOPE.md`
- `LOAD_TRIGGER: external agent | AI agent | knowledge base | embedding | vector database | RAG | retrieval | MCP | delegated agent | subagent | agentic workflow | harness | prompt injection | tool authorization | permission boundary`
- `NO_INDEPENDENT_AUTHORITY`
- `NO_INSTALLATION_OR_PERMISSION_GRANT`

## Routing rule

When any `LOAD_TRIGGER` applies to external-tool research, evaluation, adoption, activation, or review:

1. keep `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` as the authoritative evaluation and adoption owner;
2. apply `EXTERNAL_AGENT_ADAPTER_CONTRACT.md` as the general adapter contract;
3. additionally read `AGENT_CAPABILITY_SECURITY_ENVELOPE.md` for retrieval, MCP, delegation, workflow, harness, prompt-injection, token, or effect-based permission boundaries;
4. reconcile both references with the current project authority, exact revision, and existing approval boundary;
5. do not infer runtime enforcement from this router, contract text, or document tests;
6. require separate project/runtime evidence for authorization, denial, revocation, redaction, and rollback claims.

This file is a progressive-loading router only. It must not duplicate the security contract, grant credentials, widen capabilities, install a provider, alter GitHub rulesets, or authorize a sensitive action.
