# Capsule-to-SHADOW Adapter Evidence

## Identity

- Program: issue `#321`
- Adapter issue: `#355`
- Adapter PR: `#356`
- Source main: `842a5771f37c12aaf0193f680739ad478f70f6a5`
- M2 prerequisite: PR `#333`
- M3 prerequisite: PR `#337` / merge `842a5771f37c12aaf0193f680739ad478f70f6a5`
- M4 ownership exclusion: PR `#354` (`tools/loop_a2_runtime/**`)

## Initial RED

- Test/workflow-only head: `42e6ebaf935c2c1564f68b613e837469f2aeef04`
- Adapter run: `31781330784`
- Ubuntu: seven expected failures because `tools.loop_capsule_shadow_adapter` did not exist.
- Failure boundary was the missing production package, not an existing Base/M2/M3 failure.

## Minimum GREEN

- Minimum production API/CLI added after RED.
- Head `ee4d6e53d843bbabcca0b920141c29298b111e52` produced Ubuntu and Windows GREEN for the original seven tests in adapter run `31781438824`.

## Adversarial RED and remediation

Independent review found that M3's parser intentionally accepts conflict/unverified drift states for later Kernel gating, while issue #355 requires the Adapter itself to stop those states before translation.

- Adversarial head: `c56906452048f3b7337165a8e9ecead76fe9de46`
- Run: `31781609434`
- Result: four expected failures only:
  - `PLANNING_CONFLICT`
  - Planning `UNVERIFIED`
  - `VISUAL_CONFLICT`
  - Visual `UNVERIFIED`
- Existing translation, source immutability, caller-injection rejection, CLI, Windows-separator/Unicode normalization, and original contract tests remained GREEN.
- Remediation: explicit fail-closed Planning/Visual drift boundary in the Adapter before M3 parsing.

## Covered boundaries

- complete M2 bundle validation before translation;
- project and stale-authority enforcement inherited from M2;
- trusted observed-main equality;
- M3 closed runtime identifier/drift contract;
- new visual design user-decision block;
- conflict/unverified Planning/Visual block;
- deterministic Coverage-output-derived changed paths;
- `/` and `\\` normalization and Unicode NFC through M3 parser;
- no caller injection of output paths, budgets, references, or authority;
- source JSON bytes unchanged;
- no model/network/subprocess/Git-writer import in the adapter package;
- CLI produces request only and does not create `.loop-engineering` state.

## Non-claims

```yaml
MODEL_PROVIDER: NOT_CALLED
REAL_OPENAI_API: NOT_RUN
M3_STATE_EXECUTION: NOT_PERFORMED_BY_ADAPTER
PROJECT_PRODUCT_MUTATION: NONE
PROJECT_MIGRATION: NONE
A3_AUTO_MERGE: DISABLED
SCHEDULER: NOT_CONFIGURED
```

## Final integration gate

Before merge:

1. final exact-head Adapter Ubuntu/Windows PASS;
2. Base-v9 PASS;
3. Game Project OS PASS;
4. Dependency Review PASS;
5. unresolved review threads `0`;
6. exclusive path overlap `0`;
7. current-main compatibility recheck;
8. expected-head squash merge;
9. postmerge main readback and push validation.

Final exact-head and postmerge run IDs are added to PR #356 after those gates complete.
