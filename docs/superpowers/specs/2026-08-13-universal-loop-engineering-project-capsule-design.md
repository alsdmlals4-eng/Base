# Universal Loop Engineering + Project Execution Capsule Design

Tracking issue: `#321`.

Status: `USER_APPROVED / IMPLEMENTATION_PLAN_APPROVED / IMPLEMENTATION_NOT_STARTED`.

Approval date: `2026-08-14`.

Base는 하나의 공용 Loop Kernel과 프로젝트별 선언형 Execution Capsule을 사용한다. 사용자가 GPT와 확정·검수한 기획과 아트 디자인은 Planning Lock·Visual Lock으로 보호하며, Agent는 승인된 WHAT/WHY를 바꾸지 않고 기술적 HOW만 자동 실행한다.

Figma는 선택형 Visual Lock provider다. 그러나 시각 영향을 받는 구현 Package의 Visual Lock 자체는 필수다. 승인 요구사항은 Requirement Coverage Ledger에서 Task·실제 변경·Test·필수 Evidence까지 양방향 추적하며, 누락과 미승인 추가를 모두 차단한다.

세부 설계는 같은 이름의 하위 디렉터리 `2026-08-13-universal-loop-engineering-project-capsule/`에서 책임별로 분리한다. 읽기 순서는 `01-goal-and-authority.md`부터 `10-state-and-evidence.md`까지다.

구축 순서:

```text
Base #314 보호 경로 수정
→ Capsule/Lock/Package/Coverage 계약
→ 결정론적 SHADOW Kernel
→ A2 Codex Builder + 독립 Critic Runtime
→ Blacksmith Reference Migration
→ 서사·데이터 Pilot
→ 시각·UI Pilot
→ Multi-Agent/A3/Scheduler 검토
```

초기 최대 자율성은 `A2_EXECUTE_ISOLATED`다. `a3_auto_merge_allowlist`는 비어 있고 Scheduler는 `NOT_CONFIGURED` 상태로 시작한다.
