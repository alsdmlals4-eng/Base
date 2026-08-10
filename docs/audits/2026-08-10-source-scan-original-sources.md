# 2026-08-10 Source Scan — Primary Evidence Notes

## GitHub Copilot customization surfaces

GitHub's current official documentation distinguishes support for repository-wide instructions, path-specific instructions, agent instructions, prompt files, agent skills, and custom agents across GitHub.com, IDEs, CLI, cloud agent, and code review surfaces. Some surfaces support only a subset. Current code-review documentation also describes branch-specific instruction/Skill consumption during PR review. Base implication: evaluate the exact consumer surface and branch state instead of assuming a customization works everywhere.

Disposition: `ALREADY_COVERED + ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE` into `docs/AI_SKILL_ADOPTION_GUIDE.md`.

## Yarn Spinner saliency

Yarn Spinner's official saliency API separates a read-only query for the best content from the later notification that content was actually selected. The query result is not guaranteed to run and should not mutate selection state. Base implication: dynamic narrative selection/probing should not consume one-shot state, recency counters, or irreversible narrative state until the chosen content is committed to execution.

Disposition: `PARTIAL + ADAPT / LOW_RISK_BOUNDED_UPDATE` into the existing Narrative Method. Preserve this as a tool-neutral guardrail, not a Yarn API requirement.

## Adobe Premiere official release notes

Adobe maintains current Premiere release notes with recurring feature, bug-fix, security, media-management, audio, timeline navigation, relink, and review-related changes. Base implication: add Premiere official release notes as a second first-party NLE change surface alongside DaVinci. Do not convert Premiere-specific features into universal editing rules.

Disposition: `PARTIAL + REFERENCE_ONLY / LOW_RISK_BOUNDED_UPDATE` into the existing Watchlist.
