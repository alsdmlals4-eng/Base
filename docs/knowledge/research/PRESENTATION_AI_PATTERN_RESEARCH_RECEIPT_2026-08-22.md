# Presentation-AI Pattern Research Receipt · 2026-08-22

- user discovery input: `https://todayfreeai.com/recommendations/make-presentation/`
- TodayFreeAI exact body: `BLOCKED_UNVERIFIED_CACHE_MISS`
- reader-proxy attempt: `BLOCKED_BY_FETCH_SAFETY_ROUTE`
- first-party backtrace checked_at: `2026-08-22 KST`
- disposition: `DISCOVERY_ONLY`
- absorption target: `RM-WORK-003 HUMAN_FACING_ARTIFACT_SYNTHESIS`
- direct provider adoption: `NO`
- paid dependency added: `NO`

## Source backtrace

The TodayFreeAI page itself could not be fetched in the current environment, so its exact product list and editorial claims are not treated as evidence. The following provider-neutral patterns were checked against current first-party sources instead. Exact URLs are retained so a later freshness pass can re-open the same evidence surface rather than searching by product name alone.

| Provider | Exact first-party source | Reusable observation | Base use |
|---|---|---|---|
| Gamma | `https://help.gamma.app/en/articles/7838093-how-do-i-create-a-new-presentation-document-or-webpage-in-gamma` + `https://help.gamma.app/en/articles/11047840-how-can-i-import-slides-or-documents-into-gamma` | Generate/Paste/Import separation, editable output, and import text does not preserve original styling/layout | input-mode and visual-canon boundary |
| Canva | `https://www.canva.com/create/ai-presentations/` | generated draft remains editable and branding can be applied | brand/editability pattern only |
| Beautiful.ai | `https://support.beautiful.ai/hc/en-us/articles/12885226948109-Creating-a-presentation-with-AI` | prompt → text-only outline review/edit → visual preferences → generated slides | `OUTLINE_BEFORE_LAYOUT` |
| Pitch | `https://pitch.com/use-cases/ai-presentation-maker` + `https://help.pitch.com/en/articles/14981091-pitch-agent` | prompt/files/template input, chat refinement, ask-deck questions, weak proof/gap review, editable on-brand workspace | `CLAIM_GAP_REVIEW_AFTER_GENERATION` |
| SlidesAI | `https://help.slidesai.io/generate-your-first-presentation-cdcmj` | audience/type/tone instructions, outline review/edit before theme/generation | audience packet + outline gate |

## Claim ceiling

- Provider marketing claims, user counts, speed/quality claims and commercial outcomes are not treated as Base validation.
- No provider is designated as `DEFAULT_PROVIDER`.
- The extracted contract is provider-neutral and remains `MODULE_CONTRACT_DEFINED · VALIDATION_NOT_RUN` until a real Base/project artifact Pilot measures source fidelity, human edit/QA effort and human visual review.
- `IMPORTED_CONTENT_IS_NOT_IMPORTED_VISUAL_CANON` remains explicit because import support does not imply preservation of the source deck's original visual system.
- Exact URL preservation is provenance only; it does not convert a volatile product page into permanent authority. Re-check current content when a later decision materially depends on it.

## Revisit

If the TodayFreeAI body later becomes directly readable, compare its exact product list and claims against this receipt. Only new decision-relevant deltas should update Base; duplicated discovery does not justify another module or provider default.
