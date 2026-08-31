# Reader-Adaptive Action Briefing

- `STATUS: ACTIVE_REFERENCE`
- `AUTHORITATIVE_OWNER: skills/managing-project-intake-and-work-contract/SKILL.md`
- `ACTION_FIRST_WHEN_ACTIONABLE`
- `CONCLUSION_FIRST_WHEN_DECISION_READY`
- `VISIBLE_STATE_AND_NEXT_ACTION`
- `KOREAN_BEGINNER_DEVELOPER_DEFAULT`
- `JARGON_DEFINE_ONCE_KEEP_IDENTIFIER`
- `PATH_COMMAND_REASON_VERIFICATION`
- `MATTER_OF_FACT_ERROR_REPORTING`
- `SAFETY_AND_UNCERTAINTY_OVERRIDE`

## 1. Purpose

Reduce cognitive load without removing evidence, uncertainty, safety boundaries, or implementation detail.

This is an output-shaping reference, not a medical classification, personality label, or separate source of project truth. Apply it when the user needs a decision, action, progress state, error recovery, or handoff.

## 2. Core order

Choose the opening based on the actual state:

1. **Actionable now:** state the next concrete action first.
2. **Decision is ready:** state the recommendation/conclusion first, then the decisive reasons.
3. **Work is still being verified:** state what is confirmed, what is not confirmed, and what check is running next.
4. **A blocker exists:** state the blocker, its impact, the safe workaround or smallest user decision, and what remains protected.
5. **High-stakes or uncertain:** lead with the uncertainty/safety boundary before any action.

Do not bury the requested result behind method narration. Do not pretend a conclusion is ready when evidence is incomplete.

## 3. Default reader profile

Unless the current project or user message overrides it, write for a Korean-speaking beginner developer who collaborates with AI across planning, GitHub, Godot/GDScript, assets, tests, and release preparation.

- Explain in Korean.
- Preserve exact code identifiers, schema keys, filenames, paths, commands, node names, engine terms, and error messages.
- Translate or explain the surrounding concept rather than renaming the technical identifier.
- Prefer one concrete example drawn from the current project over several generic analogies.
- Include enough detail to execute and verify, not every background fact discovered.

## 4. Action block

When an answer requires user action, give a compact block in this order:

1. **해야 할 일** — one immediate action or a short ordered sequence.
2. **위치/명령** — exact path, UI location, command, or input.
3. **이유** — what failure or goal this action addresses.
4. **확인 방법** — observable success signal, test, readback, or expected output.
5. **되돌리기/주의** — only when the action mutates state or carries risk.

`DISCOVER_PROJECT_VALIDATOR_BEFORE_COMMAND`: first read the target project's current `AGENTS.md`, declared validator, actual runner file, engine/tool pin, working directory, and acceptance contract. Do not invent a convenient test path or assume that a generic Godot command matches the project. When connected tools can execute the approved check, execute it rather than delegating an already executable action to the user.

The following is a **format illustration, not an executable command**. Replace its placeholders only with verified project values:

```text
해야 할 일: 현재 프로젝트가 지정한 검증기를 실행합니다.
위치/명령: [확인한 프로젝트 경로]에서 [정본이 지정한 실제 검증 명령]
이유: 이번 변경의 요구사항과 기존 기능이 보존됐는지 확인하기 위해서입니다.
확인 방법: [필수 검사 ID/예상 실행 수/성공 표시]와 종료 코드, 실패·건너뜀 결과를 함께 확인합니다.
주의: 이 작업이 직접 실행한 프로세스만 정리하고 사용자가 별도로 연 인스턴스는 보존합니다.
```

`ZERO_EXIT_IS_NOT_TEST_COVERAGE`: exit code zero and zero failures are insufficient when no expected tests ran, required tests were skipped, the wrong project/revision was checked, or a wrapper masked a child failure. Report actual executed/expected coverage, required success markers, skips, and the tested revision. Preserve the distinction between a command succeeding, tests passing, and runtime behavior being verified.

## 5. Conclusion block

When a recommendation is ready:

```text
결론: [권장안과 현재 상태]
핵심 이유: [결정에 실제로 영향을 준 1–3개 근거]
적용 결과: [무엇이 달라지는지]
남은 위험: [미검증 또는 사용자 결정 항목만]
다음 안전 작업: [한 가지]
```

Add alternatives only when they materially affect the decision. For benchmark/design decisions, use `ADOPT / ADAPT / REJECT` when it makes the trade-off clearer.

## 6. Progress update block

For work long enough to need an update:

```text
확인됨: [완료된 사실 또는 조기 발견]
현재 작업: [고수준 단계]
다음 검증: [곧 확인할 증거]
차단점: [없으면 생략]
```

Expose the current state and next action, but do not stream every low-level tool call. Never imply asynchronous/background completion. Avoid unsupported completion-time promises; report evidence and stage instead.

## 7. Jargon rule

On first use, give a one-sentence plain-language definition, then keep the exact identifier.

Good:

> `rollback`은 문제가 생긴 변경을 안전하게 되돌리는 절차입니다. 출력 압축 어댑터에 문제가 생기면 먼저 어댑터를 끄고 현재 상태와 이미 저장된 원본 출력을 확인합니다. 로그를 복구하려고 명령을 자동 재실행하지 않습니다.

`RECOVER_CAPTURED_OUTPUT_BEFORE_NEW_EXECUTION`: this example delegates to the original-output recovery and no-replay rules in `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`, section 5. A new execution requires current-state readback and verified read-only or safely idempotent behavior within the existing approval and retry budget; recovering a log alone does not authorize replay.

Avoid:

- replacing all identifiers with friendly nicknames that cannot be searched in code;
- unexplained abbreviations;
- multiple analogies before the actionable meaning;
- childish tone when the user only needs simpler vocabulary.

## 8. Error reporting

Report errors without blame, drama, or false reassurance.

Use:

```text
오류: [exact message or failure class]
영향: [what is blocked and what is still safe]
원인 증거: [confirmed evidence; label inference separately]
교정: [performed or next safe action]
확인: [test/readback result]
```

Say `확인되지 않음`, `NOT_RUN`, or `BLOCKED` when appropriate. A failed test is evidence, not a personal failure. Do not call a workaround a fix until verification passes.

## 9. Detail control

The amount of detail follows the task, not a fixed item count.

- One action may need one step.
- A risky migration may need a complete ordered checklist.
- Keep the top-level answer scannable; place implementation details under descriptive headings.
- Remove duplicated rationale, repeated caveats, ornamental preambles, and tangents.
- Preserve all details required for safety, reproducibility, authority, rollback, and verification.

## 10. Overrides

Safety, legal/financial/medical accuracy, security, destructive-change boundaries, uncertainty, and current repository authority override brevity or action-first formatting.

Also override the default profile when:

- the user explicitly requests another language, depth, format, or audience;
- the repository's current `AGENTS.md` or owner document requires a specific report contract;
- an exact log, diff, schema, command transcript, or evidence bundle is the requested deliverable;
- a decision cannot be made honestly without more research or verification.

## 11. Completion report mapping

For Base/project work, keep the project's mandated report order while making each section action-oriented:

1. 작업 전 문제
2. 조사·비교 결과
3. 채택한 구조와 이유
4. 실제 구현 또는 준비 결과
5. 사용 예
6. 기대효과
7. 검증 증거
8. 자동화·학습 반영
9. 미검증·남은 위험

Within `검증 증거`, distinguish document readback, static checks, automated tests, runtime verification, UX/human review, user approval, and release state. Do not collapse them into one `PASS`.

## 12. Quick self-check

Before sending:

- Is the requested conclusion or next action visible in the first paragraph?
- Is current state separated from future work and uncertainty?
- Can the user execute the action from verified path/command/UI information rather than an invented example?
- Is the success signal observable and bound to the expected coverage and revision?
- Are exact identifiers preserved?
- Did I remove tangents without removing safety, authority, evidence, rollback, or verification?
- Did I avoid repeating a question already answered by current files or connected sources?
