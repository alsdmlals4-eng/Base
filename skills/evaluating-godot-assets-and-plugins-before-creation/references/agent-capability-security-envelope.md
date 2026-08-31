# Agent Capability Security Envelope Router

- `STATUS: ACTIVE_SUBORDINATE_REFERENCE`
- `AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- `CANONICAL_SECURITY_CONTRACT: docs/knowledge/ai/agent-tools/AGENT_CAPABILITY_SECURITY_ENVELOPE.md`
- `SECURITY_CONTRACT_OWNER: docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`
- `LOAD_TRIGGER: external agent | AI agent | knowledge base | embedding | vector database | RAG | retrieval | MCP | delegated agent | subagent | agentic workflow | harness | prompt injection | tool authorization | permission boundary`
- `NO_INDEPENDENT_AUTHORITY`
- `NO_INSTALLATION_OR_PERMISSION_GRANT`

## Routing rule

When any `LOAD_TRIGGER` applies to external-tool research, evaluation, adoption, activation, or review:

1. keep `EXTERNAL_AGENT_ADAPTER_CONTRACT.md` as the authoritative external-agent owner;
2. read `AGENT_CAPABILITY_SECURITY_ENVELOPE.md` before recommending or activating retrieval, MCP, delegation, workflow, or harness behavior;
3. apply the envelope together with the current project authority, exact revision, and existing approval boundary;
4. do not infer runtime enforcement from the presence of this router, contract text, or document tests;
5. require separate project/runtime evidence for authorization, denial, revocation, redaction, and rollback claims.

This file is a progressive-loading router only. It must not duplicate the canonical security contract, grant credentials, widen capabilities, install a provider, alter GitHub rulesets, or authorize a sensitive action.
