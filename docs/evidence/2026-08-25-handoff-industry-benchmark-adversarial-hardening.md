# 2026-08-25 · Handoff industry benchmark / adversarial hardening evidence

## Status

- classification: `BASE_PROMOTION_EVIDENCE`
- implementation_authority: `METHOD_TEMPLATE_HARDENING`
- baseline_main: `6f8ca83efbb34862bd8cdceb38321090734a57ba`
- target_owners:
  - `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
  - `templates/project-operations/HANDOFF.md`
- protected_concurrent_owner:
  - `skills/maintaining-project-context-and-handoff/SKILL.md` — Base PR #674가 수정 중이므로 이번 작업에서는 read-only

## Question

Base #698에서 강화한 인수인계 종료 프로토콜이 실제 AI agent handoff, 장기 workflow, repository instruction, 운영/incident handoff 관행과 비교했을 때 빠뜨린 안전 장치가 있는지 확인한다.

이번 조사의 목표는 새 framework를 추가하는 것이 아니라 **현재 Base의 얇은 handoff method/template가 새 채팅 재개 실패, 중복 mutation, 승인 대기 소실, context 과적재, 정본 drift를 더 잘 막도록 최소 교정**하는 것이다.

## External benchmark

### 1. OpenAI Agents SDK · Handoffs / Sessions — `ADAPT`

Sources:
- https://openai.github.io/openai-agents-python/handoffs/
- https://openai.github.io/openai-agents-python/running_agents/
- https://openai.github.io/openai-agents-js/guides/sessions/

Observed pattern:
- Handoff는 다음 agent로 control을 넘기는 명시적 mechanism이다.
- 전체 conversation history를 그대로 보내는 것이 기본일 수 있지만 `input_filter`, `handoff_input_filter`, history mapper/compaction으로 전달 context를 선택적으로 줄일 수 있다.
- session/run state는 장기 흐름을 지속하고, 동일 item의 중복 append를 피하는 동작을 제공한다.

Base absorption:
- 전체 대화/도구 로그를 Handoff 정본처럼 복사하지 않고 `context_sanitation` + 3~7 canonical locator를 사용한다.
- 수신 세션이 필요한 evidence만 fresh-read한다.
- 동일 mutation이 재실행되지 않도록 `side_effects_already_applied`와 idempotency 확인을 추가한다.

Rejected copying:
- Agents SDK의 특정 API나 session backend 자체를 Base 필수 dependency로 도입하지 않는다.

### 2. Anthropic · Effective context engineering for AI agents — `ADAPT`

Source:
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Observed pattern:
- agent context는 유한한 attention resource이며, 더 많은 history가 항상 더 높은 품질을 의미하지 않는다.
- 장기 agent는 매 턴 무엇을 context에 넣을지 지속적으로 curate해야 한다.
- 작은 high-signal context 집합을 유지하는 것이 중요하다.

Base absorption:
- Handoff 본문은 현재 상태·결정·위험·다음 행동·rollback 중심으로 압축한다.
- raw tool log/full transcript는 기본 payload에서 제외한다.
- 압축 때문에 보호 범위·미결 승인·NOT_RUN·실패 원인이 사라지면 `over-compaction` 실패로 본다.

Rejected copying:
- 별도 vector memory/context service를 신규 기본 인프라로 만들지 않는다.

### 3. GitHub Copilot · repository/path/agent instructions — `ADOPT`

Sources:
- https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions

Observed pattern:
- repository-wide, path-specific, agent instruction surface를 분리한다.
- `AGENTS.md`는 repository/current/intermediate/nested 경로에서 발견될 수 있고 더 가까운 applicable instruction이 중요하다.
- path-specific instruction은 해당 path에만 적용해 global instruction overload를 줄인다.

Base absorption:
- 새 채팅의 first mutation 전에 root `AGENTS.md`, nearest applicable `AGENTS.md`, project/path-specific instruction을 fresh-read한다.
- Handoff 요약문이 현재 instruction surface를 대체하지 못하도록 한다.

Rejected copying:
- GitHub Copilot 전용 instruction 파일을 모든 프로젝트에 강제 생성하지 않는다. 프로젝트가 이미 사용하는 authority를 우선한다.

### 4. Microsoft Agent Framework · Handoff / HITL / checkpoints — `ADAPT`

Sources:
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff
- https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop
- https://learn.microsoft.com/en-us/agent-framework/journey/workflows

Observed pattern:
- handoff는 context에 따라 control을 transfer한다.
- workflow는 checkpoint storage로 pause/resume할 수 있고, pending human request도 checkpoint state에 함께 보존한다.
- human approval이 필요한 tool/action은 workflow를 pause하고 응답을 기다린다.
- internal handoff tool call/result를 다음 agent context에서 filter해 workflow mechanics가 모델 판단을 오염시키지 않게 할 수 있다.
- 복잡한 orchestration보다 요구를 만족하는 가장 단순한 pattern을 권장한다.

Base absorption:
- `last_safe_checkpoint` + `next_safe_action`을 분리한다.
- `pending_user_decisions`와 `approval_required_before_resume`를 일반 next work와 분리한다.
- 이미 적용된 side effect를 기록해 resume 시 duplicate mutation을 막는다.

Rejected copying:
- Base에 별도 durable workflow engine/orchestrator를 만들지 않는다. GitHub/Notion current canon + Handoff template로 필요한 안전성만 흡수한다.

### 5. Google SRE · Clear, Live Handoff — `ADAPT`

Source:
- https://sre.google/sre-book/managing-incidents/

Observed pattern:
- incident command handoff는 outgoing이 넘겼다고 말하는 것만으로 끝나지 않고 incoming commander의 명시적 acknowledgement가 필요하다.
- living state document는 중요 정보를 위쪽에 두고, 이후 postmortem/analysis에 보존한다.

Base absorption:
- `PACKET_READY`와 실제 `TRANSFER_ACCEPTED`를 분리한다.
- 새 채팅/담당자가 아직 없다면 정상 종료는 `PACKET_READY / PENDING_RECEIVER_ACK`다.
- 새 receiver는 current state, next action, protected scope, pending decisions, already-applied side effects를 자기 말로 readback한 뒤 `receiver_ack`한다.

Rejected copying:
- incident commander 조직 역할 자체를 1인 프로젝트 운영에 복제하지 않는다. 핵심 원리인 명시적 수신 확인만 흡수한다.

## Alternatives

### A · ACK only

- Add: `PACKET_READY -> receiver_ack -> TRANSFER_ACCEPTED`
- 장점: 변경이 가장 작다.
- 단점: duplicate side effect, pending approval loss, instruction drift를 막지 못한다.
- verdict: `REJECT_INSUFFICIENT`

### B · Bounded handoff hardening — selected

- Add:
  - packet/receiver state separation
  - durable resume checkpoint + idempotency receipt
  - pending user decision gate
  - applicable instruction/canon freshness readback
  - context sanitation
- 장점: 현재 failure mode를 직접 막으면서 기존 method/template owner를 재사용한다.
- 단점: Handoff template 필드가 늘어난다. 따라서 conditional/compact 사용이 필요하다.
- verdict: `ADOPT_SELECTED`

### C · Automated handoff service / workflow engine

- Add: dedicated service, schema store, event-driven receiver ACK, automated retries.
- 장점: 조직 규모에서는 강한 자동화 가능.
- 단점: 1인 프로젝트 Base에는 dependency/context/maintenance 비용이 과도하고 GitHub/Notion authority와 중복될 수 있다.
- verdict: `REJECT_YAGNI_DUPLICATE_OWNER`

## Adversarial review loops

### Loop 1 · Authority / control-transfer attack

Attack:
- 송신자가 Handoff 문서를 만들고 `READY`라고 쓰면 실제 새 채팅도 인수했다고 오인할 수 있다.

Finding:
- `packet prepared`와 `receiver accepted`가 같은 상태 공간에 있었다.

Correction:
- `PACKET_READY`, `PENDING_RECEIVER_ACK`, `TRANSFER_ACCEPTED`, `CONTEXT_DRIFT_RECHECK_REQUIRED` 분리.
- receiver의 state/action/protected-scope readback을 `receiver_ack`로 요구.

### Loop 2 · Duplicate mutation / recovery attack

Attack:
- 새 채팅이 “다음 행동”만 보고 이전 세션이 이미 실행한 Notion upload, commit/push, merge, PR/Issue mutation을 다시 수행할 수 있다.

Finding:
- 마지막 안전 완료점과 이미 발생한 external side effect가 명시적이지 않았다.

Correction:
- `last_safe_checkpoint`, `next_safe_action`, `side_effects_already_applied`, `idempotency.retry_safe`, `verify_before_retry` 추가.

### Loop 3 · Pending approval attack

Attack:
- 아직 사용자 선택이 필요한 항목이 일반 `남은 작업`에 섞이면 receiver가 가역적 기술 선택처럼 잘못 처리할 수 있다.

Finding:
- 승인된 결정은 `CURRENT_CONFIRMED_DECISIONS`로 잘 관리하지만, **미결 사용자 결정**의 별도 handoff field가 없었다.

Correction:
- `pending_user_decisions`, `approval_required_before_resume`, `safe_work_while_pending` 추가.

### Loop 4 · Context pollution / instruction hierarchy attack

Attack:
- 품질을 높이려고 transcript와 tool log를 통째로 넘기면 context 비용이 커지고 오래된 규칙이 최신 정본과 경쟁한다.
- Handoff가 최신 `AGENTS.md`보다 강하게 소비될 수 있다.

Finding:
- 기존 3~7 read order 원칙은 있었지만 sanitation receipt와 applicable nested instruction fresh-read가 명시적이지 않았다.

Correction:
- `context_sanitation` 추가.
- root + nearest applicable `AGENTS.md`, project/path instruction surface readback 추가.

### Loop 5 · Freshness / concurrent drift attack

Attack:
- packet 작성 후 Base/project main, open PR, Notion canon이 이동했는데 receiver가 old SHA 기준으로 바로 mutation할 수 있다.

Finding:
- fresh-read 원칙은 있었지만 prepared baseline과 resume observed baseline 비교 receipt가 없었다.

Correction:
- `prepared_from_main_sha`, `resume_observed_main_sha`, `canon_freshness`, `CONTEXT_DRIFT_RECHECK_REQUIRED` 추가.

### Loop 6 · Overengineering / usability attack

Attack:
- 안전 필드를 계속 추가하면 Handoff가 장문 checklist가 되어 오히려 새 채팅이 읽기 어려워질 수 있다.

Finding:
- 모든 benchmark 기능을 새 Skill/engine으로 구현하면 기존 Base 철학과 충돌한다.

Correction:
- 기존 method/template만 보강.
- field는 조건부 사용.
- 3~7 canonical locator, raw log 제외, full transcript 금지 유지.
- 신규 broad Skill/service/dependency 생성 없음.

Result:
- new in-scope MUST_FIX after Loop 6: `0`
- known trade-off: template field 수 증가. `context_sanitation`과 conditional sections로 제어.

## Concurrency protection

2026-08-25 조사 시점의 관련 open workstream은 read-only로 보호한다.

- PR #674: GPT/Codex role split + `skills/maintaining-project-context-and-handoff/SKILL.md`
- PR #689: visual continuity implementation
- PR #693: visual canon handoff proposal
- PR #679/#678: adjacent visual approval/delivery proposals
- PR #660: active planning surface alignment

이번 hardening은 `PROJECT_HANDOFF_CONTEXT_METHOD.md`, `HANDOFF.md`, focused regression test, 이 evidence 파일만 소유한다. 위 open PR의 branch/file을 수정·흡수·rebase·close하지 않는다.

## Implementation Reality Gate

Claimable after merge + readback:
- Base 공용 method/template에 위 상태/필드가 존재한다.
- focused regression이 exact head에서 PASS한다.
- Notion Base/P01 human view가 새 semantics를 설명하고 destination readback된다.

Not claimable from this work alone:
- 모든 게임 프로젝트가 이미 새 template로 handoff를 재작성했다.
- 실제 새 채팅에서의 cross-project `TRANSFER_ACCEPTED` 성공률이 측정됐다.
- Notion human-visible image rendering 또는 runtime product asset 품질이 검증됐다.
- Microsoft/OpenAI/GitHub/Anthropic/Google의 framework를 프로젝트 runtime dependency로 도입했다.

## Promotion disposition

- Existing method owner: `PROMOTE_ADDITIVE_HARDENING`
- Existing handoff template: `PROMOTE_ADDITIVE_HARDENING`
- New broad Skill: `REJECT_DUPLICATE_OWNER`
- New workflow service/orchestrator: `REJECT_YAGNI`
- P01 human explanation: `SYNC_AFTER_GITHUB_CHANGE`
- P05 change: `NOT_REQUIRED` — #698 visual audit semantics remain unchanged

## Revisit condition

- 실제 새 채팅에서 `receiver_ack`가 반복적으로 형식적 문구만 남기고 상태 오류를 못 잡을 때
- duplicate side effect가 다시 발생할 때
- pending approval이 resume 과정에서 손실될 때
- instruction/canon drift로 receiver의 첫 mutation이 잘못될 때
- handoff template가 너무 길어져 3~7 canonical locator 원칙을 오히려 훼손할 때
