# Tool Hub Launcher Repair Diagnostics Plan

## Goal
Make the Windows Tool Hub self-repair path expose bounded, actionable fail-closed reason codes during user-PC IRG without weakening any trust boundary.

## Scope
- Split the current generic `LAUNCHER_UPDATE_REQUIRED` repair failures into bounded reason codes for static identity, reviewed-main, runtime cleanliness, and desktop shortcut checks.
- Preserve all existing rejection conditions.
- Add focused regression tests consumed by Tool Hub Subscription Contracts on Ubuntu and Windows.
- Do not change Git pull/fetch/reset/checkout behavior, project files, Figma routes, or Studio runtime behavior.

## Verification
1. RED tests prove the current generic codes cannot distinguish the boundaries.
2. GREEN focused tests on Ubuntu and Windows.
3. Base v9/adversarial and Game Project OS Windows Tool Hub smoke.
4. Merge only on exact verified head.
5. User-PC reruns the existing no-console repair command and reports the precise code.
