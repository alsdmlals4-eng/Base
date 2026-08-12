# Backend, AI Coding, Deployment, and Media Source Expansion Design

- Date: 2026-08-12
- Baseline: `aa45a7589cede16be027b55f15ea4813681df8e3`
- Scope: source/reference expansion only; no new ACTIVE Skill, no deployment, no cloud resource creation, no product-direction change

## Goal

Expand Base's periodic source system so future work can research four practical areas with current official sources:

1. backend/API implementation structure and security,
2. AI coding tools and coding-agent evaluation,
3. WAS/deployment systems with Cloud Run as the current Base-owned default candidate and explicit alternatives,
4. PC game/development capture plus AI-assisted video/image editing.

The change must route findings into existing owners instead of creating duplicate Skills.

## Existing owners

- Backend / online service architecture: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
- AI development workflow/evals: `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- General source governance: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Video production: `skills/producing-game-development-youtube-videos/SKILL.md`
- Image/thumbnail/visual work: `skills/designing-art-prompts-and-technique-cards/SKILL.md` and art-direction owner

## Design choice

Use `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md` as the single new-source intake surface. Add four grouped source sets with role boundaries and consumer routing. Do not create a backend Skill, deployment Skill, AI-coding Skill, capture Skill, or editing Skill.

## Source groups

### Backend/API engineering

Primary starting points:

- OpenAPI Specification — HTTP API contract/interface standard authority.
- FastAPI official docs — FastAPI framework behavior and Python API implementation patterns only.
- PostgreSQL official docs — PostgreSQL behavior, transactions, indexing, operations.
- Redis official docs — Redis data types/persistence/caching/queue behavior when Redis is actually selected.
- OWASP API Security Project — security risk/reference guidance, not a security PASS certificate.

Route to the existing Cloud Run/backend owner and target-project implementation/tests.

### AI coding

Primary starting points:

- OpenAI Developers / Codex official documentation — OpenAI/Codex product behavior only.
- Anthropic Claude Code official documentation — Claude Code behavior only.
- Gemini CLI / Gemini Code Assist official docs — Google coding-tool behavior only.
- GitHub Copilot docs — retain existing authority; do not duplicate as a new family.
- aider official docs/repository — open-source terminal coding workflow reference.
- SWE-bench official leaderboard/papers — benchmark/discovery evidence, never a direct project-quality proof.

Tool marketing, leaderboard rank, model name, or benchmark score must not prove project productivity, correctness, security, or merge readiness. Require project-local tasks/tests/review evidence.

### Deployment / WAS / cloud runtime

Keep `GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md` as the decision owner. Cloud Run remains the Base-owned default candidate for appropriate stateless HTTPS/container workloads, but alternatives are actively compared:

- Google Cloud Run official docs — service/job/worker-pool/container/IAM/runtime behavior.
- Cloudflare Workers official docs — edge/serverless APIs, bindings, Durable Objects/queues/workflows where appropriate.
- Fly.io Machines official docs — VM lifecycle, regional placement, persistent volume cases and lower-level runtime control.
- Railway official docs — simple container/PaaS deployment, services, jobs, variables, GitHub deployment.
- Render official docs — managed web/private services, workers, cron, datastore and Docker deployment.

No provider is globally superior. Compare workload shape, protocol, state, latency/region, background lifetime, operational burden, portability, observability, quota, lock-in, failure recovery, and measured cost.

### PC capture and AI-assisted media editing

Capture / local processing:

- OBS official Knowledge Base — game/window/display capture, recording, audio tracks, encoding, troubleshooting.
- FFmpeg official docs — capture/transcode/filter/automation behavior.
- Microsoft Xbox Game Bar / Snipping Tool official support — low-friction Windows fallback capture.
- NVIDIA App/ShadowPlay official docs — NVIDIA-hardware capture path when applicable.

Editing / AI-assisted production:

- DaVinci Resolve official docs — desktop NLE, color, audio, Fusion and current Neural Engine features.
- Adobe Premiere / Photoshop / Firefly official docs — vendor feature authority for text-based editing, generative video/image editing and image retouching.
- Runway official help — current generative/editing workflows and deprecations.

Route capture/editing findings to `producing-game-development-youtube-videos`; image/thumbnail findings to the existing art/technique owner. Tool feature availability does not prove output quality, rights safety, cost efficiency, or suitability for the project.

## Evaluation / claim ceilings

- Cloud Run is not universally better than Workers/Fly/Railway/Render; it remains a project-fit candidate under the existing backend guide.
- FastAPI/PostgreSQL/Redis are examples and authorities for their own behavior, not mandatory stack choices.
- AI coding vendor claims or benchmark ranks do not prove correctness; project tests, diff review, security checks, and exact-head evidence remain authoritative.
- OBS/ShadowPlay/Game Bar capture capability does not prove acceptable frame pacing, audio sync, encoder overhead, storage cost, or visual quality; measure on the actual PC/build.
- AI image/video editing availability does not grant rights to source assets or generated outputs and does not waive provenance/similarity review.
- Vendor pricing, quotas, model availability and product features are volatile; re-check current official sources before adoption.

## Validation

Extend `tests/test_periodic_external_source_discovery_seeds.py` so the repository contract requires:

- all four source groups,
- key source identities,
- routing to existing backend/AI/video/art owners,
- Cloud Run non-universal comparison language,
- AI-coding benchmark/project-evidence ceiling,
- capture performance/quality measurement boundary,
- media rights/provenance boundary.

TDD order: add the focused regression first and confirm RED, then add the source groups and confirm GREEN, followed by Base required workflows and adversarial review.

## Expected repository disposition

`ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`

No new ACTIVE Skill, Registry identity, BCP, workflow authority, Required Check, dependency, cloud resource, or deployment is required.