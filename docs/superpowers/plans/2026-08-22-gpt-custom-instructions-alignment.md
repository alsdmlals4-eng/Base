# GPT Custom Instructions Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the Base GPT custom-instructions template and guide with the current domain-split canon while preventing future drift from duplicated Base rules.

**Architecture:** Treat ChatGPT Custom Instructions as a stable bootstrap layer, not as a second project/Base canon. Keep user/work-style constraints and dynamic authority routing in the template; leave volatile project facts and detailed Base gates in current repository/Notion authorities. Preserve the moved AI-instruction Method through a no-content compatibility alias rather than duplicating its canonical body.

**Tech Stack:** Markdown, GitHub branch/PR workflow, repository readback validation

**Spec:** `docs/superpowers/specs/2026-08-22-gpt-custom-instructions-alignment-design.md`

## Global Constraints

- Latest user instruction outranks repository guidance.
- Do not create a second canon by copying volatile Base rules into Custom Instructions.
- Preserve `DOMAIN_SPLIT_CANON`: Notion human-facing canon, repository structured/runtime canon, Google Sheets migration-only compatibility.
- Do not restore deprecated HTML dashboard/project workspace routes.
- `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` remains the canonical AI-instruction Method.
- The old `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` path may exist only as `COMPATIBILITY_ALIAS_ONLY` with no duplicated Method body.
- Do not change `templates/custom-instructions.codex.md` in this scope.
- Work on an isolated branch, then PR, verification, merge, and post-merge readback.

---

### Task 1: Replace the GPT custom-instructions template

**Files:**
- Modify: `templates/custom-instructions.gpt.md`

**Interfaces:**
- Consumes: current Base authority and domain-split contracts.
- Produces: copy-paste-ready stable user context and response/work behavior blocks.

- [ ] **Step 1: Read the current template and confirm stale items**

Verify the current file contains the old fixed read order and `HTML 대시보드` role, and does not express current `DOMAIN_SPLIT_CANON`.

- [ ] **Step 2: Replace it with the stable-bootstrap template**

The replacement must contain:

```text
stable user context
→ project/Base authority bootstrap
→ DOMAIN_SPLIT_CANON
→ current Base gate delegation
→ connected-tool evidence rule
→ beginner-friendly Korean explanation
→ free/local/current-tool cost boundary
→ explicit image-generation request boundary
```

Do not embed current PR numbers, project progress, current system values, or a copied list of every Base gate.

- [ ] **Step 3: Read back the branch file**

Confirm the replacement contains no active `HTML 대시보드` role and no claim that Google Sheets is the default project workspace.

---

### Task 2: Rewrite the Custom Instructions guide around stable vs dynamic authority

**Files:**
- Modify: `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`

**Interfaces:**
- Consumes: design spec and updated GPT template.
- Produces: maintenance rules preventing future Custom Instructions/Base drift.

- [ ] **Step 1: Replace the outdated guide sections**

The guide must explicitly distinguish:

```text
Custom Instructions = stable bootstrap
Memory = long-lived user preference/context aid
Project Notion/repository = project canon by domain
Base/project AGENTS = current operating rules
Conversation/request = current task intent
```

- [ ] **Step 2: Add anti-drift inclusion/exclusion rules**

Include in Custom Instructions:

```text
stable role, language/explanation preference, cost boundary, image-generation boundary,
authority routing, dynamic Base lookup rule
```

Exclude:

```text
current PR/Issue state, current project progress, detailed worldbuilding,
exact volatile Base gate counts copied as independent authority,
long file lists, one-time task instructions, deprecated tool routes
```

- [ ] **Step 3: Add current product-personalization guidance**

Record that `Professional` is the recommended Base style for this workflow, while personality changes communication style rather than task authority. Characteristics remain optional because availability can vary.

- [ ] **Step 4: Read back the guide**

Confirm the guide points users to `templates/custom-instructions.gpt.md` and does not present HTML dashboard or Google Sheets as current defaults.

---

### Task 3: Restore the moved AI-instruction Method route without duplicating canon

**Files:**
- Create: `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- Read: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`

**Interfaces:**
- Consumes: the current Documentation Map old-path route and canonical game-development Method.
- Produces: a resolvable compatibility path that cannot become a second Method authority.

- [ ] **Step 1: Verify canonical target**

Read `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` and confirm it owns instruction authority, context curation, fixture/example and artifact-claim design.

- [ ] **Step 2: Create a compatibility-only router**

The new old-path file must contain only:

```text
COMPATIBILITY_ALIAS_ONLY
canonical owner path
custom-instructions guide path
migration/read rule
no duplicated Method body
```

It must explicitly state that edits belong in the canonical target, not in the alias.

- [ ] **Step 3: Read back both paths**

Confirm the old path resolves and the canonical Method remains the only content authority.

---

### Task 4: Validate the change adversarially and merge safely

**Files:**
- Review: all files changed by this branch

**Interfaces:**
- Consumes: Tasks 1–3 outputs.
- Produces: verified PR and merged main readback.

- [ ] **Step 1: Run adversarial review loop 1 — authority drift**

Attack the change for duplicated or contradictory authority. Fix any finding, then re-read all modified documents.

- [ ] **Step 2: Run adversarial review loop 2 — stale/deprecated routes**

Search the changed scope for HTML dashboard/default Sheets/deprecated visual workspace language. Fix any active-route finding and re-read.

- [ ] **Step 3: Run adversarial review loop 3 — usability and character-budget pressure**

Check that the GPT copy-paste blocks remain compact enough for current Custom Instructions limits and do not bury the highest-value routing rules. Fix and re-read.

- [ ] **Step 4: Run adversarial review loop 4 — project/runtime truth boundary**

Attack for cases where Memory, Notion, static visuals, or Custom Instructions could be misread as runtime proof. Fix and re-read.

- [ ] **Step 5: Run adversarial review loop 5 — cold-start behavior**

Simulate a new chat with no historical context. Verify the instructions route the agent to the current project and Base authorities without requiring copied project facts. Fix and re-read.

- [ ] **Step 6: Compare branch against latest main**

Confirm the branch still derives from the intended main lineage and contains only approved-scope changes.

- [ ] **Step 7: Open a non-draft PR**

PR body must summarize the stale-state problem, adopted hybrid design, affected files, validation evidence, and explicit non-goals.

- [ ] **Step 8: Verify exact PR head**

Inspect changed filenames, diff, unresolved review threads, reviews, and commit status/workflow evidence available for the exact head SHA.

- [ ] **Step 9: Merge only the exact verified head**

Use the repository-supported merge method without bypassing rulesets or forcing main.

- [ ] **Step 10: Post-merge readback**

Read `templates/custom-instructions.gpt.md`, `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`, the old-path compatibility alias, and the canonical AI-instruction Method from main and confirm the merged state matches the approved design.
