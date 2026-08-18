# Local Visual Tool Lessons and Fallback

Status for normal image work after the 2026-08-18 user-PC stop-loss:

```yaml
local_visual_runtime_status: REFERENCE_ONLY_FOR_VISUAL_WORKFLOW
normal_image_work_dependency: NOT_REQUIRED
figma_direct_organization: PREFERRED
source_code_retention: KEEP
```

## What remains useful

The local visual tools produced reusable domain lessons that remain valid reference material:

### Expression Studio

- preserve approved character identity;
- separate facial movement, gaze, and head pose;
- use bounded candidate counts when comparison is useful;
- do not treat provider calls or generated pixels as automatic approval;
- keep source/reference hashes and provenance concepts explicit.

### Sprite Animation Studio

- preserve identity across pose/action variants;
- define pose/action intent and sequence continuity;
- distinguish pose/atlas visual evidence from runtime animation proof;
- preserve project isolation and exact target identity concepts.

### Effect workflow

- describe staged effect changes explicitly;
- preserve alpha/compositing expectations;
- separate visual VFX reference from runtime shader/particle implementation.

### Tool Hub / delivery work

- exact project identity matters;
- exact artifact destinations are preferable to generic drop zones;
- success claims need readback rather than request completion alone;
- candidate/approval/product-asset/runtime states must not collapse into one status.

## What is no longer required

The normal image-work path must not require:

- Tool Hub launcher/runtime;
- localhost Hub ports;
- PowerShell startup;
- Studio child-process ownership;
- private delivery-token lifecycle;
- localhost Figma Bridge pairing;
- automated Studio-to-Hub delivery.

The preferred normal image-work path is now:

```text
project canon
→ project Figma approved references
→ GPT image generation/editing
→ direct Figma WIP organization when write capability exists
→ user approval
→ approved visual organization
→ separate product asset/runtime gates when needed
```

## Source retention

Do not delete these implementations merely because they are no longer the normal visual workflow:

- `tools/tool-hub/`
- `tools/expression-studio/`
- `tools/sprite-animation-studio/`

They remain referenceable implementation history and may support unrelated audits or an explicitly requested future experiment.

This fallback does not globally deprecate unrelated QA tooling such as QA Evidence Studio.

## Re-entry rule

Do not reopen full local visual-runtime repair as an automatic response to a future image task. A new runtime experiment requires an explicit user request and a new scoped decision. Until then, use the Figma-direct workflow and the modular visual controls in this Skill package.
