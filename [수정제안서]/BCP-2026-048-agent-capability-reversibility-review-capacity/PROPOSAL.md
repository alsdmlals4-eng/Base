# BCP-2026-048 — Agent Capability·Reversibility·Human Review Capacity Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `32f4dd5ba6042dc34611e2c8912f300b90491e0a`
- 제출일: `2026-09-01`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- 외부 근거 확인일: `2026-09-01`

## 후보보고서 상태와 정본 경계

`CANDIDATE_REPORT_IS_NOT_BASE_CANON`

- 후보보고서·첨부물의 역할: 2026-09-01의 AI-native development 조사와 Base current-owner audit는 **입력 증거·외부 사례·현행 구조 관찰**이다.
- Base 정본 또는 구현 지시가 아닌 이유: Base에는 이미 instruction/context, external-agent safety, isolated autonomy, evidence validation owner가 존재하며, 이번 조사만으로 새 필드의 프로젝트 효과·기계 강제력·적정 임계값을 검증하지 않았다.
- 프로젝트 고유 결론·설정·수치·경로·자산 중 제외한 것:
  - AWS 내부 팀의 인력·기간·`4.5x` 보고값과 monorepo 선택;
  - Kiro 제품의 실제 `permissions.yaml` 경로·capability 이름·UI·CLI 설정;
  - 특정 프로젝트의 agent 수, review backlog 수치, 파일·줄 수 기준;
  - vendor-specific hook, account, API key, hosted session, telemetry 또는 paid service.

## 관찰과 증거

- 실제로 확인한 작업·구현·검증:
  - Base main `32f4dd5ba6042dc34611e2c8912f300b90491e0a`의 `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`는 Interface-first Prompt에서 authority/source, invariants, failure conditions와 validation을 요구한다.
  - `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`가 optional external-agent/tool adoption의 authoritative owner이고, 그 active reference인 `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`는 inspect/mutate/verify 분리, argument-array/no-shell 실행, capability별 network/filesystem/credential/remote-write 승인, bounded retry, raw fallback, kill switch와 provider-independent rollback을 정의한다.
  - `docs/OPERATING_MODEL.md`가 `LOOP_ENGINEERING_CONTROL_PLANE`의 상위 계약을 소유하고, `templates/project-operations/LOOP_ENGINEERING_PROFILE.md`는 프로젝트별 자율권·resource lock·budget 값을 선언하며 초기 기본을 `A2_EXECUTE_ISOLATED`, `max_parallel_agents: 1`로 둔다.
  - `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`는 승인 범위, 보호 범위, acceptance criteria, runtime/play evidence와 exact repository rehydration을 요구한다.
  - `schemas/loop-run-contract-v1.schema.json`에는 planning gate, resource lease/lock, execution budget, evidence, blocker와 approval ref가 존재한다.
  - AWS 공식 글은 고성과 팀의 공통점으로 agent context, 초기 기반 투자, 검증 가능한 완료 조건, 의도 명세와 test-first를 설명하지만, 내부 생산성 수치를 다른 조직의 보장치로 제시하지 않는다: <https://aws.amazon.com/blogs/machine-learning/how-frontier-teams-are-reinventing-ai-native-development/>.
  - Kiro 공식 문서는 capability별 `deny / ask / allow`, `deny > ask > allow`, workspace scope와 agent가 자신의 permission 파일을 수정하지 못하는 hardcoded deny를 설명한다: <https://kiro.dev/docs/cli/chat/permissions/>.
  - OWASP Agentic AI AAIK는 credential 단위가 아니라 action 단위 최소 권한, 고영향 작업의 사람 검토 가능한 분해, 가역적 transaction/dry-run, 시스템별 최소 자격증명과 worst-reachable reversibility 분류를 권고한다: <https://cornucopia.owasp.org/cards/AAIK>.
- 확인한 현재 gap:
  - 위 책임은 각각 존재하지만, **한 작업에서 실제로 허용된 capability·최악의 도달 가능한 부작용·가역성·rollback·완료 증거를 함께 읽는 선택적 projection**은 명시적이지 않다.
  - 병렬 agent budget은 있으나 **미검토 산출물·사용자 검토 backlog·변경 설명 가능성 때문에 병렬성을 낮추는 조건**은 명시적이지 않다.
- 추측·미실행 항목과 evidence ceiling:
  - 어떤 프로젝트에서도 이 projection을 적용한 A/B trial, 사용자 개입 횟수·review time·rework·runtime completion lead time 측정을 수행하지 않았다.
  - 문서에 규칙을 추가하는 것이 실제 filesystem/shell/network/secret/remote-write 차단을 구현한다는 증거는 없다.
  - 제안은 보안 인증, sandbox 구현, runtime enforcement, Human/UX 개선 또는 생산성 향상을 입증하지 않는다.

## 일반화 후보

`COMMON_LESSON_AND_CORRECTION_REQUEST_REQUIRED`

### 후보 원칙 1 — Task Capability & Reversibility Projection

`ILLUSTRATIVE_PROJECTION_NOT_SCHEMA`

아래 YAML은 검토할 의미 집합을 보여 주는 예시이며, 승인 전에는 공용 필드명·controlled vocabulary·machine schema가 아니다.

Mutating, agentic, external-tool 또는 remote-side-effect 작업에서는 기존 정본과 실행 owner로부터 다음을 **선택적으로 투영**해 한 작업 계약에서 읽을 수 있게 한다.

```yaml
task_capability_projection:
  trusted_instruction_sources: []
  untrusted_data_sources: []
  inspect: []
  write:
    allowed_paths: []
    denied_paths: []
  execute:
    allowed_commands: []
    denied_commands: []
  network:
    policy: DENY | ASK | ALLOWLIST
    allowed_domains: []
  secrets:
    policy: DENY | SHORT_LIVED_INJECTION
  remote_write:
    policy: DENY | ASK | APPROVED_SCOPE_ONLY
  self_permission_edit: DENY

reversibility:
  class: READ_ONLY | ISOLATED_REVERSIBLE | REMOTE_REVERSIBLE | IRREVERSIBLE
  worst_reachable_effect:
  rollback:
  confirmation_required:

completion_evidence:
  validation_commands: []
  expected_results: []
  destination_readback: []
  evidence_ceiling:
```

- 이 projection은 권한을 새로 부여하지 않는다. 상위 정본·도구 capability·repository ruleset보다 넓은 `allow`를 만들 수 없다.
- 외부 문서·Issue/PR 본문·모델 출력·다운로드 파일 같은 `untrusted_data_sources`는 permission rule이나 approval source를 정의하지 못한다.
- trusted rule끼리 충돌하면 먼저 현재 Base/project의 **권위 우선순위·범위·freshness**로 해결한다. 더 높은 권위의 명시적 최신 승인은 낮은 권위의 일반 default/ask를 그 승인 범위 안에서 대체할 수 있다.
- 시스템·도구 capability·repository Ruleset·법적/보안 hard ceiling과 보호된 불변조건은 낮출 수 없다. 같은 권위에서 충돌하거나 범위·freshness가 불명확하면 더 제한적인 결과를 적용한다.
- secret 값 자체, credential material, 민감한 원문 경로를 공개 기록에 복제하지 않는다.

### 후보 원칙 2 — Human Review Capacity Gate

`UNREVIEWED_AGENT_OUTPUT_IS_WIP_NOT_PROGRESS`

- 병렬성은 model/runner capacity가 아니라 **사람이 의도·위험·diff·증거를 검토할 수 있는 처리량**에 의해 제한한다.
- review backlog 증가, 변경의 owner/consumer 설명 실패, 반복적인 raw reread, post-change rework 증가가 관찰되면 새 agent fan-out보다 병렬성을 먼저 낮춘다.
- 현재 Base 기본 `max_parallel_agents: 1`을 유지한다. 더 높은 수치는 project-local 반복 증거와 rollback이 있을 때만 채택한다.
- 고정 줄 수·파일 수·시간 임계값을 Base 전역 규칙으로 만들지 않는다.
- 별도 backlog dashboard·병렬 task tracker·새 정본을 만들지 않고, 기존 run/profile/evidence owner가 이미 가진 상태에서 필요한 신호만 소비한다.

### 비교한 대안

| 대안 | 장점 | 한계 | 판정 |
|---|---|---|---|
| A — 현행 owner만 유지 | 변경·migration·context 비용이 없다 | 한 task에서 권한·가역성·검토 감속 조건을 재구성해야 한다 | 유효한 fallback |
| B — 기존 owner에 선택적 projection과 review-capacity 감속 조건 추가 | 중복 owner 없이 발견된 gap만 닫고 rollback이 쉽다 | 문서만으로 runtime enforcement를 만들지 못한다 | `SELECTED_CANDIDATE` |
| C — 새 Skill·필수 Schema·권한 엔진 구축 | 기계 강제력을 중앙화할 수 있다 | 현재 owner와 중복되고 프로젝트 migration·유지비·권한 위험이 크다 | `REJECT` |

## 적용 조건과 비사용 조건

### Capability·Reversibility Projection 활성 조건

```text
HAS_MUTATING_OR_PRIVILEGED_CAPABILITY
AND
(BOUNDARY_NOT_ALREADY_CLEAR OR REVERSIBILITY_NOT_ALREADY_CLEAR)
```

- `HAS_MUTATING_OR_PRIVILEGED_CAPABILITY`: task가 filesystem mutation, shell, network, secret, MCP/connector 또는 remote write 중 하나 이상을 실제로 사용한다.
- `BOUNDARY_NOT_ALREADY_CLEAR`: 현재 작업 계약만으로 allowed/denied capability와 보호 범위를 즉시 확인할 수 없다.
- `REVERSIBILITY_NOT_ALREADY_CLEAR`: worst reachable effect, rollback 또는 confirmation requirement 중 하나 이상이 명확하지 않다.
- 따라서 병렬·장기 작업이 아니더라도 비가역 remote write와 불명확한 rollback이 있는 단일 작업은 projection 대상이다.

### Human Review Capacity Gate 활성 조건

```text
AGENT_OUTPUT_CAN_ACCUMULATE
AND
(REVIEW_CAPACITY_RISK_PRESENT OR PARALLELISM_INCREASE_PROPOSED)
```

- `AGENT_OUTPUT_CAN_ACCUMULATE`: 병렬 agent, 장기 연속 실행 또는 여러 미검토 결과가 쌓일 수 있는 orchestration이다.
- `REVIEW_CAPACITY_RISK_PRESENT`: review backlog 증가, owner/consumer 설명 실패, 반복 raw reread 또는 post-change rework 증가가 관찰됐다.
- `PARALLELISM_INCREASE_PROPOSED`: 현재 project profile보다 agent fan-out을 높이려 한다.
- review backlog 신호만으로 capability permission projection을 활성화하지 않으며, mutating capability 존재만으로 별도 review-capacity Gate를 강제하지 않는다.

### 비사용 조건

- L0 오탈자, 순수 read-only 조사, 기존 project contract가 동일 정보를 더 강하게 소유하는 경우;
- deterministic single-file change로 기존 protected scope·validation·rollback이 이미 명확한 경우;
- projection을 채우기 위해 secret·private path·불필요한 내부 세부를 더 노출해야 하는 경우.

### 그대로 복사하면 안 되는 요소

- Kiro의 실제 capability literal·설정 파일·UI 흐름;
- AWS의 기간·인력·생산성 수치와 monorepo topology;
- OWASP의 권고 문구를 프로젝트 승인·실제 enforcement PASS로 취급하는 것;
- 전역 고정 agent 수, review backlog 숫자, 줄 수·파일 수 제한;
- 새 dashboard, permission service, hook 또는 paid external dependency.

## 기존 Base owner gap과 최소 수정 요청

`MINIMUM_OWNER_CORRECTION_REQUEST`

- 현재 owner·경로:
  - 작업 의도·정본·입출력·불변조건: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`;
  - 요청 접수와 실행 계약: `skills/managing-project-intake-and-work-contract/SKILL.md`;
  - optional external-agent/tool adoption owner와 실행 안전 reference: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` + `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`;
  - 자율 실행 Control Plane과 프로젝트별 profile: `docs/OPERATING_MODEL.md` + `templates/project-operations/LOOP_ENGINEERING_PROFILE.md`;
  - 제품 구현 인계: `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`;
  - 실제 변경·증거 검증: `skills/reviewing-and-validating-project-changes/SKILL.md`.
- 확인한 gap 또는 충돌:
  - owner 충돌은 확인되지 않았다.
  - capability·reversibility·completion evidence는 분산돼 있어 mutating task의 bounded 실행 계약에서 한 번에 확인하기 어렵다.
  - Control Plane과 project profile은 agent 수·repair·CI budget을 소유하지만 human review backlog로 병렬성을 감속하는 명시적 조건은 없다.
- 최소 수정 요청:
  1. `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`의 Interface-first Prompt에 **적용 조건이 있는 선택적 capability/reversibility projection**을 추가하고, 실제 process safety는 기존 External Agent Adapter Contract를 참조한다.
  2. `docs/OPERATING_MODEL.md`의 `LOOP_ENGINEERING_CONTROL_PLANE`에 `UNREVIEWED_AGENT_OUTPUT_IS_WIP_NOT_PROGRESS`와 review-capacity 기반 병렬성 downshift 원칙을 추가하고, `LOOP_ENGINEERING_PROFILE.md`에는 프로젝트별 signal/stop 조건만 선언한다. `max_parallel_agents: 1` 기본값은 유지한다.
  3. `tests/test_external_agent_tool_adoption_contract.py`와 `tests/test_loop_engineering_control_plane_contract.py`의 기존 owner-local consumer를 먼저 사용해 “optional projection, no new Skill/schema/vendor dependency, no fixed productivity promise”를 검증한다. 새 broad test file은 현재 consumer가 부족하다는 증거가 있을 때만 검토한다.
  4. `CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`와 `loop-run-contract-v1.schema.json`은 먼저 readback만 하고, 중복 필드나 migration 필요가 확인되지 않으면 변경하지 않는다.
- 새 Skill·문서·registry가 필요 없는 이유:
  - 입력·권한·자율화·검증 owner가 이미 존재한다. 새 책임 원본은 중복과 routing drift를 만든다.
  - project adoption 이전의 공용 문서 projection이므로 mandatory machine schema와 adapter 구현은 근거가 부족하다.
- 변경하지 않을 보호 범위:
  - root `AGENTS.md`, `START_HERE.md`, `skills/SKILL_REGISTRY.json`, generated/released locks;
  - GitHub Ruleset, workflow permissions, secrets, accounts, billing, network policy와 actual sandbox implementation;
  - project-local AGENTS/version pin, core gameplay, UX meaning, save/schema, approved assets;
  - 모든 open/draft/ready PR과 다른 BCP lifecycle.

## 프로젝트 전용으로 남길 내용

- 각 프로젝트의 allowed paths/commands/domains, credential owner, rollback command, review backlog threshold, agent count와 evidence commands는 project-local owner에 남긴다.
- 실제 Kiro·Codex·ChatGPT·MCP·GitHub connector 설정은 사용하는 execution surface의 current capability에서 관리하며 Base proposal이 설치·활성화하지 않는다.
- AWS 사례의 조직 구조·monorepo·수치와 특정 tool의 permission vocabulary는 외부 reference로만 남긴다.

## 반례와 위험

`EVIDENCE_CEILING_AND_NONUSE_CONDITIONS`

- 반례:
  - 이미 OS/container/repository ruleset에서 엄격하게 제한된 single-command task는 추가 projection이 인지부하만 늘릴 수 있다.
  - Markdown의 `DENY`는 실제 tool permission이 더 넓으면 기술적으로 차단하지 못한다.
  - review backlog Gate를 고정 숫자로 만들면 작은 generated diff와 위험한 semantic diff를 동일하게 취급할 수 있다.
  - allowed path 목록이 너무 넓거나 stale이면 명시성이 오히려 잘못된 안전감을 만들 수 있다.
  - 민감 경로·credential 이름을 상세히 기록하면 secret exposure surface가 증가할 수 있다.
- evidence ceiling:
  - proposal/contract validation은 **제안의 추적성·경계·형식**만 증명한다.
  - 이번 단계는 actual capability enforcement, sandbox/network isolation, secret non-leakage, project productivity, Human review burden, Godot runtime, UX, release readiness를 증명하지 않는다.
- 승인 전 구현 금지 범위:
  - active Method·Skill·Template·Schema·Test·workflow·project adapter 수정;
  - 새 tool install, permission/account/security setting 변경, secret 사용, remote execution 또는 project rollout;
  - BCP 상태를 `APPROVED_FOR_IMPLEMENTATION`·`IMPLEMENTED`로 승격하는 것.

## 영향 범위와 검증

- proposal-only 변경 범위:
  - `[수정제안서]/BCP-2026-048-agent-capability-reversibility-review-capacity/PROPOSAL.md`;
  - `[수정제안서]/PROPOSAL_REGISTRY.json`.
- proposal-only 검증:
  - 신규 entry가 `SUBMITTED`, `approval_ref: null`, `implementation_pr: null`인지 확인;
  - proposal registry JSON Schema와 `tools/check_base_change_proposals.py --base-ref 32f4dd5ba6042dc34611e2c8912f300b90491e0a`;
  - `tests/test_base_change_proposals.py`;
  - changed paths가 `[수정제안서]/**` 안에만 있는지 확인;
  - exact-head `ci-gate`, independent review, unresolved thread와 latest-main reconciliation.
- 향후 승인 구현의 예상 검증:
  - focused contract regression RED→GREEN;
  - full Base local/remote validation;
  - reference freshness와 generated artifact check;
  - project adoption은 별도 project-local A/B evidence와 runtime/readback을 요구한다.
- 롤백과 lifecycle 보존:
  - proposal PR이 병합 전 거절·철회되면 PR을 닫아 main을 변경하지 않는다.
  - proposal이 main에 기록된 뒤 거절·보류·대체되면 proposal file과 Registry entry를 삭제하지 않는다. 별도 reviewed lifecycle change에서 Registry status를 `REJECTED`, `DEFERRED` 또는 `SUPERSEDED`로 전환하고 결정 근거를 proposal에 보존한다.
  - active Base behavior, project files, permissions와 runtime evidence는 이 proposal-only PR로 변경되지 않는다.

## 필요한 도구·파일·권한

- 필요 항목: 기존 Base proposal registry, BCP validator/test, GitHub proposal-only branch/PR.
- 필요한 이유: active owner를 변경하지 않고 검토 가능한 candidate와 rollback 경계를 남기기 위해서다.
- 설치·적용 방법: 설치 없음. 새 dependency, API, credential, service 또는 paid credit 없음.
- 설치 후 확인 명령:
  - `python tools/check_base_change_proposals.py --base-ref 32f4dd5ba6042dc34611e2c8912f300b90491e0a`
  - `python -m unittest tests.test_base_change_proposals -v`
  - `git diff --check`
- 최소 권한: proposal-only branch write와 PR creation. `main` direct push, force push, admin/ruleset bypass, secret, workflow permission 또는 project write 불필요.

## 승인과 구현

- 사용자 승인 근거: `2026-09-01` 현재 대화의 `권장안대로 진행해`는 **권장안 B의 proposal-only 제출과 검증**을 승인한다.
- Base implementation approval ref: `미승인`.
- 구현 PR: `없음`.
- 롤백: 병합 전에는 PR을 닫아 main을 보존한다. 병합 후에는 proposal·Registry 이력을 삭제하지 않고 별도 reviewed lifecycle change로 `REJECTED`, `DEFERRED` 또는 `SUPERSEDED` 상태와 근거를 기록한다.
